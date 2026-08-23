from __future__ import annotations

import sqlite3
import threading
from concurrent.futures import ThreadPoolExecutor
from dataclasses import replace
from datetime import datetime, timedelta, timezone
from decimal import Decimal
from pathlib import Path

from intelligence.curation import cluster_documents
from intelligence.domain import (
    CostEntry,
    CostStatus,
    DeliveryRecord,
    DeliveryStatus,
    Document,
    Provenance,
    Rights,
    RightsStatus,
    RunRecord,
    RunStatus,
    SourceRole,
    Visibility,
)
from intelligence.storage import IntelligenceStore, SCHEMA_VERSION


NOW = datetime(2026, 8, 23, 10, 0, tzinfo=timezone.utc)


def _document(*, url: str, content: str, source: str) -> Document:
    return Document.create(
        title="Model release",
        url=url,
        excerpt=content,
        content=content,
        provenance=Provenance(
            source_id=source,
            source_name=source,
            source_url=f"https://{source}.example",
            retrieved_at=NOW,
            role=SourceRole.PRIMARY,
            authority=0.8,
        ),
        visibility=Visibility.PRIVATE,
        rights=Rights(RightsStatus.PUBLIC_LINK_ONLY),
        lanes=("research",),
    )


def test_v2_to_v3_preserves_fk_and_allows_revisions_and_mirrors(tmp_path: Path) -> None:
    repo = tmp_path / "repo"
    repo.mkdir()
    data = tmp_path / "data"
    original = _document(
        url="https://lab.example/release",
        content="First revision",
        source="lab",
    )
    with IntelligenceStore(data_dir=data, public_repo_root=repo) as store:
        store.save_document(original)
        event = cluster_documents((original,))[0]
        store.save_event(event)

    # Simula un database v2 già popolato. La tabella costi non esisteva in v2.
    connection = sqlite3.connect(data / "intelligence.sqlite3")
    connection.execute("DROP TABLE cost_entries")
    connection.execute("PRAGMA user_version = 2")
    connection.commit()
    connection.close()

    revision = _document(
        url="https://lab.example/release",
        content="Second revision with corrected data",
        source="lab",
    )
    mirror = _document(
        url="https://archive.example/release-copy",
        content="First revision",
        source="archive",
    )
    with IntelligenceStore(data_dir=data, public_repo_root=repo) as migrated:
        assert migrated.get_event(event.id) == event
        assert migrated.save_document(revision) == revision
        assert migrated.save_document(mirror) == mirror
        assert len(migrated.list_documents()) == 3
        assert migrated.save_document(original) == original
        assert len(migrated.list_documents()) == 3
        assert migrated._connection.execute("PRAGMA user_version").fetchone()[0] == SCHEMA_VERSION
        assert migrated._connection.execute("PRAGMA foreign_key_check").fetchall() == []


def test_cost_reservations_are_atomic_and_never_cross_monthly_budget(tmp_path: Path) -> None:
    repo = tmp_path / "repo"
    repo.mkdir()
    data = tmp_path / "data"
    with IntelligenceStore(data_dir=data, public_repo_root=repo) as store:
        store.save_run(RunRecord("run-cost", "am", NOW, RunStatus.RUNNING))

    barrier = threading.Barrier(2)

    def reserve(index: int) -> tuple[int, bool]:
        entry = CostEntry(
            id=f"cost-{index}",
            reservation_key=f"search-{index}",
            provider="xai",
            operation="x_search",
            amount_usd=Decimal("6"),
            status=CostStatus.RESERVED,
            incurred_at=NOW,
            run_id="run-cost",
        )
        with IntelligenceStore(data_dir=data, public_repo_root=repo) as store:
            barrier.wait()
            return index, store.reserve_cost(entry, monthly_budget_usd=Decimal("10"))

    with ThreadPoolExecutor(max_workers=2) as executor:
        results = list(executor.map(reserve, (1, 2)))
    assert sum(acquired for _, acquired in results) == 1
    winner = next(index for index, acquired in results if acquired)

    with IntelligenceStore(data_dir=data, public_repo_root=repo) as store:
        assert store.monthly_cost(2026, 8) == Decimal("6")
        settled = store.reconcile_cost(
            f"search-{winner}", actual_amount_usd=Decimal("5"), status=CostStatus.SETTLED
        )
        assert store.reconcile_cost(
            f"search-{winner}", actual_amount_usd=Decimal("5"), status=CostStatus.SETTLED
        ) == settled
        assert store.monthly_cost(2026, 8) == Decimal("5")
        remaining = CostEntry(
            "cost-remaining",
            "remaining",
            "anthropic",
            "analysis",
            Decimal("5"),
            CostStatus.RESERVED,
            NOW,
            "run-cost",
        )
        assert store.reserve_cost(remaining, monthly_budget_usd="10")
        blocked = CostEntry(
            "cost-blocked",
            "blocked",
            "openai",
            "analysis",
            Decimal("0.000001"),
            CostStatus.RESERVED,
            NOW,
            "run-cost",
        )
        assert not store.reserve_cost(blocked, monthly_budget_usd="10")
        assert store.monthly_cost(2026, 8) == Decimal("10")


def test_delivery_reservation_is_atomic_and_failed_is_retryable(tmp_path: Path) -> None:
    repo = tmp_path / "repo"
    repo.mkdir()
    data = tmp_path / "data"
    with IntelligenceStore(data_dir=data, public_repo_root=repo) as store:
        store.save_run(RunRecord("run-delivery", "pm", NOW, RunStatus.RUNNING))

    barrier = threading.Barrier(2)

    def reserve(index: int):
        candidate = DeliveryRecord(
            f"delivery-{index}",
            "run-delivery",
            "email",
            "giada.f@me.com",
            DeliveryStatus.PENDING,
            "pm:2026-08-23:giada",
            NOW,
        )
        with IntelligenceStore(data_dir=data, public_repo_root=repo) as store:
            barrier.wait()
            return store.reserve_delivery(candidate)

    with ThreadPoolExecutor(max_workers=2) as executor:
        reservations = list(executor.map(reserve, (1, 2)))
    acquired = next(item for item in reservations if item is not None)
    assert sum(item is not None for item in reservations) == 1

    with IntelligenceStore(data_dir=data, public_repo_root=repo) as store:
        failed = replace(acquired, status=DeliveryStatus.FAILED, error="SMTP timeout")
        store.save_delivery(failed)
        retry_request = DeliveryRecord(
            "delivery-retry",
            "run-delivery",
            "email",
            "giada.f@me.com",
            DeliveryStatus.PENDING,
            acquired.idempotency_key,
            NOW + timedelta(minutes=1),
        )
        retry = store.reserve_delivery(retry_request)
        assert retry is not None
        assert retry.id == acquired.id
        assert retry.status is DeliveryStatus.PENDING
        assert store.reserve_delivery(retry_request) is None

        sent = replace(
            retry,
            status=DeliveryStatus.SENT,
            delivered_at=NOW + timedelta(minutes=2),
        )
        store.save_delivery(sent)
        assert store.reserve_delivery(retry_request) is None
