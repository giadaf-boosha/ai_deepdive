from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path

import pytest

from intelligence.curation import (
    build_reading_queue,
    cluster_documents,
    deduplicate_documents,
    rank_events,
)
from intelligence.domain import (
    Document,
    EditorialSignals,
    Event,
    Provenance,
    Rights,
    RightsStatus,
    SourceRole,
    Visibility,
    canonicalize_url,
)
from intelligence.storage import IntelligenceStore, StorageError


NOW = datetime(2026, 8, 23, 8, 0, tzinfo=timezone.utc)


def _document(
    source_id: str,
    title: str,
    url: str,
    *,
    excerpt: str,
    official: bool = False,
    role: SourceRole = SourceRole.ANALYSIS,
    lanes: tuple[str, ...] = ("research",),
    minutes: int = 10,
    visibility: Visibility = Visibility.PRIVATE,
    rights: Rights | None = None,
) -> Document:
    return Document.create(
        title=title,
        url=url,
        excerpt=excerpt,
        content=f"{title} {excerpt} {source_id}",
        provenance=Provenance(
            source_id=source_id,
            source_name=source_id,
            source_url=f"https://{source_id}.example",
            retrieved_at=NOW,
            role=role,
            authority=0.95 if official else 0.7,
            is_official=official,
        ),
        visibility=visibility,
        rights=rights or Rights(RightsStatus.PUBLIC_LINK_ONLY),
        lanes=lanes,
        estimated_read_minutes=minutes,
    )


def test_url_normalization_and_exact_dedup_are_deterministic() -> None:
    assert canonicalize_url("HTTPS://Example.com:443/post/?utm_source=x&b=2&a=1#top") == (
        "https://example.com/post?a=1&b=2"
    )
    first = _document(
        "lab",
        "Acme releases Model Z",
        "https://example.com/z?utm_campaign=launch",
        excerpt="Model Z improves reasoning.",
        official=True,
        role=SourceRole.PRIMARY,
    )
    duplicate = _document(
        "press",
        "Acme releases Model Z",
        "https://example.com/z",
        excerpt="A copy of the launch.",
    )
    forward = deduplicate_documents((first, duplicate))
    backward = deduplicate_documents((duplicate, first))
    assert forward == backward
    assert set(forward) == {first, duplicate}

    exact = _document(
        "lab",
        "Acme releases Model Z",
        "https://example.com/z",
        excerpt="Model Z improves reasoning.",
        official=True,
        role=SourceRole.PRIMARY,
    )
    assert deduplicate_documents((first, exact)) == (first,)


def test_event_clustering_chooses_official_primary_and_restricts_visibility() -> None:
    official = _document(
        "acme",
        "Acme releases Model Z reasoning system",
        "https://acme.example/model-z",
        excerpt="Model Z reasoning system reaches a new benchmark.",
        official=True,
        role=SourceRole.PRIMARY,
        lanes=("research", "mathematics"),
    )
    press = _document(
        "press",
        "Model Z reasoning system reaches new benchmark",
        "https://press.example/model-z-news",
        excerpt="Acme's Model Z reasoning system reaches a new benchmark.",
        visibility=Visibility.TEAM,
        rights=Rights(RightsStatus.PAYWALLED, public_use="blocked"),
    )
    events = cluster_documents((press, official), similarity_threshold=0.4)
    assert len(events) == 1
    event = events[0]
    assert event.primary_document_id == official.id
    # Il cluster eredita sempre la visibilita' piu' restrittiva.
    assert event.visibility is Visibility.PRIVATE
    assert event.rights.status is RightsStatus.PAYWALLED
    assert event.status.value == "verified"


def test_sqlite_store_requires_external_dir_and_round_trips_provenance(tmp_path: Path) -> None:
    repo = tmp_path / "public"
    repo.mkdir()
    with pytest.raises(ValueError):
        IntelligenceStore(data_dir=repo / "private", public_repo_root=repo)

    data_dir = tmp_path / "private-store"
    document = _document(
        "official",
        "World model launch",
        "https://official.example/world-model",
        excerpt="An embodied AI world model launches.",
        official=True,
        role=SourceRole.PRIMARY,
        lanes=("spatial_embodied_ai", "neuroscience"),
    )
    event = cluster_documents((document,))[0]
    with IntelligenceStore(data_dir=data_dir, public_repo_root=repo) as store:
        assert store.save_document(document) == document
        store.save_event(event)
        restored = store.get_document(document.id)
        restored_event = store.get_event(event.id)
        assert restored == document
        assert restored_event == event
        assert store.documents_for_event(event.id) == (document,)
        assert (data_dir.stat().st_mode & 0o077) == 0


def test_store_rejects_event_with_missing_documents(tmp_path: Path) -> None:
    repo = tmp_path / "repo"
    repo.mkdir()
    document = _document(
        "lab",
        "New system",
        "https://lab.example/system",
        excerpt="Details.",
    )
    event = cluster_documents((document,))[0]
    with IntelligenceStore(data_dir=tmp_path / "data", public_repo_root=repo) as store:
        with pytest.raises(StorageError):
            store.save_event(event)


def test_interdisciplinary_ranking_and_knapsack_respect_30_minute_budget() -> None:
    bridge_document = _document(
        "research",
        "World models connect perception and action",
        "https://research.example/world-models",
        excerpt="Evidence connects embodied AI with neuroscience.",
        official=True,
        lanes=("spatial_embodied_ai", "neuroscience", "philosophy"),
        minutes=18,
    )
    product_document = _document(
        "product",
        "Coding assistant adds minor feature",
        "https://product.example/feature",
        excerpt="A product feature ships.",
        lanes=("agents_coding",),
        minutes=18,
    )
    short_document = _document(
        "strategy",
        "Leadership research on augmentation",
        "https://strategy.example/augmentation",
        excerpt="Research links augmentation and leadership.",
        lanes=("management_leadership", "education"),
        minutes=12,
    )
    events = list(cluster_documents((bridge_document, product_document, short_document)))
    by_primary = {event.primary_document_id: event for event in events}

    def with_signals(event: Event, signals: EditorialSignals) -> Event:
        return Event(**{**event.__dict__, "signals": signals})

    bridge = with_signals(
        by_primary[bridge_document.id],
        EditorialSignals(0.9, 0.9, 0.9, 0.95, 1.0),
    )
    product = with_signals(
        by_primary[product_document.id],
        EditorialSignals(0.4, 0.3, 0.3, 0.4, 0.0),
    )
    short = with_signals(
        by_primary[short_document.id],
        EditorialSignals(0.7, 0.65, 0.8, 0.8, 0.8),
    )
    documents = (bridge_document, product_document, short_document)
    ranked = rank_events((product, short, bridge), documents)
    assert ranked[0].event.id == bridge.id
    assert ranked[0].components["interdisciplinary_bridge"] > 10

    queue = build_reading_queue(ranked, documents, budget_minutes=30)
    assert queue.total_minutes <= 30
    assert {item.event_id for item in queue.selected} == {bridge.id, short.id}
    assert product.id in queue.deferred_event_ids
