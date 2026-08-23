from __future__ import annotations

import json
from datetime import datetime, timedelta, timezone
from decimal import Decimal
from pathlib import Path

from intelligence.cli import _digest_watermark_source, _reserve_x_budget, main
from intelligence.config import Settings
from intelligence.domain import DeliveryRecord, DeliveryStatus, RunRecord, RunStatus
from intelligence.storage import IntelligenceStore


CONFIG = """
[system]
timezone = "Europe/Rome"
owner_email = "giada.f@me.com"
daily_reading_minutes = 30
max_digest_events = 10
[delivery]
recipient_allowlist = ["giada.f@me.com"]
"""


def test_am_and_pm_share_one_daily_watermark() -> None:
    assert _digest_watermark_source("am") == "digest:daily"
    assert _digest_watermark_source("pm") == "digest:daily"
    assert _digest_watermark_source("weekly") == "digest:weekly"


def test_x_preflight_uses_persistent_monthly_ledger(tmp_path: Path) -> None:
    public = tmp_path / "public"
    private = tmp_path / "private"
    public.mkdir()
    settings = Settings(
        data_dir=private,
        public_repo_root=public,
        x_max_posts_per_run=300,
        x_monthly_budget_usd=0.05,
    )
    now = datetime(2026, 8, 23, tzinfo=timezone.utc)
    with IntelligenceStore(data_dir=private, public_repo_root=public) as store:
        _key, cap = _reserve_x_budget(
            store,
            settings,
            source_id="x",
            operation="recent",
            at=now,
            unit_cost_usd=Decimal("0.005"),
        )
        assert cap == 10
        assert store.monthly_cost(2026, 8) == Decimal("0.05")
        try:
            _reserve_x_budget(
                store,
                settings,
                source_id="x",
                operation="recent",
                at=now + timedelta(seconds=1),
                unit_cost_usd=Decimal("0.005"),
            )
        except ValueError as exc:
            assert "Budget X" in str(exc)
        else:
            raise AssertionError("La seconda reservation doveva essere bloccata")


def test_cli_full_offline_flow(tmp_path: Path, monkeypatch) -> None:
    public = tmp_path / "public"
    private = tmp_path / "private"
    public.mkdir()
    config = public / "config.toml"
    config.write_text(CONFIG, encoding="utf-8")
    source = tmp_path / "items.jsonl"
    source.write_text(
        json.dumps(
            {
                "id": "1",
                "url": "https://example.com/world-model",
                "title": "World model for embodied agents",
                "text": "A research lab releases a world model for robots.",
                "published_at": "2026-08-24T05:00:00+00:00",
            }
        )
        + "\n",
        encoding="utf-8",
    )
    monkeypatch.setenv("AI_INTEL_DATA_DIR", str(private))

    assert main(["--config", str(config), "init"]) == 0
    assert main(["--config", str(config), "ingest-jsonl", str(source)]) == 0
    assert main(["--config", str(config), "ingest-jsonl", str(source)]) == 0
    assert main(["--config", str(config), "curate"]) == 0
    assert main(
        [
            "--config",
            str(config),
            "render",
            "--slot",
            "am",
            "--at",
            "2026-08-24T07:00:00+02:00",
        ]
    ) == 0
    assert len(list((private / "outbox").glob("*.md"))) == 1
    assert (private / "outbox" / "email-preview.eml").exists()
    with IntelligenceStore(
        data_dir=private, public_repo_root=Path(__file__).resolve().parents[1]
    ) as store:
        assert store.list_runs()[0].status.value == "succeeded"
        assert store.list_deliveries()[0].status.value == "preview"
        assert store.list_watermarks() == ()


def test_cli_blocks_live_send_with_deterministic_provider(tmp_path: Path, monkeypatch) -> None:
    private = tmp_path / "private"
    config = tmp_path / "config.toml"
    config.write_text(CONFIG, encoding="utf-8")
    monkeypatch.setenv("AI_INTEL_DATA_DIR", str(private))
    assert main(
        [
            "--config",
            str(config),
            "render",
            "--slot",
            "am",
            "--at",
            "2026-08-24T07:00:00+02:00",
            "--send",
        ]
    ) == 2
    assert not (private / "outbox" / "email-preview.eml").exists()


def test_cli_reconciles_ambiguous_delivery_and_cost(tmp_path: Path, monkeypatch) -> None:
    public = Path(__file__).resolve().parents[1]
    private = tmp_path / "private"
    config = tmp_path / "config.toml"
    config.write_text(CONFIG, encoding="utf-8")
    monkeypatch.setenv("AI_INTEL_DATA_DIR", str(private))
    now = datetime(2026, 8, 23, tzinfo=timezone.utc)
    settings = Settings(
        data_dir=private,
        public_repo_root=public,
        x_max_posts_per_run=10,
        x_monthly_budget_usd=1.0,
    )
    with IntelligenceStore(data_dir=private, public_repo_root=public) as store:
        store.save_run(RunRecord("run-1", "am", now, RunStatus.RUNNING))
        store.reserve_delivery(
            DeliveryRecord(
                "delivery-1",
                "run-1",
                "email",
                "giada.f@me.com",
                DeliveryStatus.PENDING,
                "email:am:2026-08-23",
                now,
            )
        )
        reservation_key, _ = _reserve_x_budget(
            store,
            settings,
            source_id="x",
            operation="recent",
            at=now,
            unit_cost_usd=Decimal("0.01"),
        )

    assert main(
        [
            "--config",
            str(config),
            "resolve-delivery",
            "--id",
            "delivery-1",
            "--outcome",
            "failed",
        ]
    ) == 0
    assert main(
        [
            "--config",
            str(config),
            "reconcile-cost",
            "--reservation-key",
            reservation_key,
            "--actual-usd",
            "0.03",
        ]
    ) == 0
    with IntelligenceStore(data_dir=private, public_repo_root=public) as store:
        assert store.get_delivery("delivery-1").status is DeliveryStatus.FAILED
        assert store.monthly_cost(2026, 8) == Decimal("0.03")
