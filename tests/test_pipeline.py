from datetime import datetime, timezone
from pathlib import Path

from intelligence.connectors import SourceRecord
from intelligence.curation import rank_events
from intelligence.domain import (
    Claim,
    ClaimType,
    Document,
    EventStatus,
    Provenance,
    Rights,
    RightsStatus,
    SourceRole,
    VerificationStatus,
    Visibility,
)
from intelligence.pipeline import build_digest_entries, ingest_records, reconcile_events
from intelligence.providers import StructuredHTTPProvider
from intelligence.storage import IntelligenceStore


def test_pipeline_ingest_and_event_reconciliation_are_idempotent(tmp_path: Path) -> None:
    public = tmp_path / "public"
    private = tmp_path / "private"
    public.mkdir()
    record = SourceRecord(
        source_id="official",
        source_type="rss",
        external_id="1",
        url="https://example.com/news?utm_source=test",
        title="New world model released",
        text="A lab releases a world model for embodied agents.",
        published_at=datetime(2026, 8, 23, tzinfo=timezone.utc),
        author="Example Lab",
    )
    with IntelligenceStore(data_dir=private, public_repo_root=public) as store:
        ingest_records(store, [record], retrieved_at=datetime(2026, 8, 23, tzinfo=timezone.utc))
        first = reconcile_events(store)
        ingest_records(store, [record], retrieved_at=datetime(2026, 8, 23, tzinfo=timezone.utc))
        second = reconcile_events(store)
        assert len(store.list_documents()) == 1
        assert len(store.list_events()) == 1
        assert first[0].id == second[0].id
        assert "spatial_embodied_ai" in second[0].lanes


def test_email_without_url_stays_private(tmp_path: Path) -> None:
    public = tmp_path / "public"
    private = tmp_path / "private"
    public.mkdir()
    record = SourceRecord("mail", "email", "m1", None, "Subject", "Private body", None, "Sender")
    with IntelligenceStore(data_dir=private, public_repo_root=public) as store:
        document = ingest_records(
            store, [record], retrieved_at=datetime(2026, 8, 23, tzinfo=timezone.utc)
        )[0]
        assert document.canonical_url.startswith("https://private.invalid/")
        assert document.rights.status.value == "private_communication"


def _document(
    *,
    slug: str,
    title: str,
    excerpt: str,
    retrieved_at: datetime,
    rights: RightsStatus = RightsStatus.PUBLIC_LINK_ONLY,
) -> Document:
    return Document.create(
        title=title,
        url=f"https://example.com/{slug}",
        excerpt=excerpt,
        content=excerpt,
        provenance=Provenance(
            source_id=slug,
            source_name=slug,
            source_url=f"https://example.com/{slug}",
            retrieved_at=retrieved_at,
            role=SourceRole.ANALYSIS,
        ),
        visibility=Visibility.PRIVATE,
        rights=Rights(rights),
        lanes=("research",),
    )


def test_external_provider_only_receives_public_rights_candidates(tmp_path: Path) -> None:
    public = tmp_path / "public"
    private = tmp_path / "private"
    public.mkdir()
    now = datetime(2026, 8, 23, tzinfo=timezone.utc)
    documents = (
        _document(slug="public", title="Public model launch", excerpt="Public release details", retrieved_at=now),
        _document(
            slug="private",
            title="Private leadership memo",
            excerpt="Confidential internal analysis",
            retrieved_at=now,
            rights=RightsStatus.PRIVATE_COMMUNICATION,
        ),
        _document(
            slug="paywall",
            title="Paywalled market report",
            excerpt="Subscriber market details",
            retrieved_at=now,
            rights=RightsStatus.PAYWALLED,
        ),
        _document(
            slug="subscriber",
            title="Subscriber research briefing",
            excerpt="Restricted research details",
            retrieved_at=now,
            rights=RightsStatus.SUBSCRIBER_ONLY,
        ),
        _document(
            slug="unknown",
            title="Unknown rights briefing",
            excerpt="Rights have not been classified",
            retrieved_at=now,
            rights=RightsStatus.UNKNOWN,
        ),
    )
    captured_ids: list[str] = []

    def post_json(endpoint, headers, payload):
        candidates = payload["candidates"]
        captured_ids.extend(candidate["event_id"] for candidate in candidates)
        return {
            "analyses": [
                {
                    "event_id": candidate["event_id"],
                    "tldr": "External analysis",
                    "why_it_matters": "Public evidence",
                    "lane": "research",
                    "confidence": "high",
                    "read_decision": "tldr",
                    "read_minutes": 0,
                    "bridge": None,
                }
                for candidate in candidates
            ]
        }

    provider = StructuredHTTPProvider(
        name="external",
        endpoint="https://gateway.example/analyze",
        bearer_token="secret",
        post_json=post_json,
    )
    with IntelligenceStore(data_dir=private, public_repo_root=public) as store:
        for document in documents:
            store.save_document(document)
        events = reconcile_events(store)
        entries = build_digest_entries(
            store,
            rank_events(events, store.list_documents()),
            provider,
            max_events=10,
            reading_budget_minutes=30,
        )

    public_event_id = next(
        event.id for event in events if event.rights.status is RightsStatus.PUBLIC_LINK_ONLY
    )
    assert captured_ids == [public_event_id]
    assert {entry.event_id for entry in entries if entry.confidence == "low"} == {
        event.id for event in events if event.rights.status in {
            RightsStatus.PRIVATE_COMMUNICATION,
            RightsStatus.PAYWALLED,
            RightsStatus.SUBSCRIBER_ONLY,
            RightsStatus.UNKNOWN,
        }
    }


def test_reconciliation_dismisses_absorbed_event_and_preserves_its_claim(tmp_path: Path) -> None:
    public = tmp_path / "public"
    private = tmp_path / "private"
    public.mkdir()
    first_seen = datetime(2026, 8, 23, 8, tzinfo=timezone.utc)
    later = datetime(2026, 8, 23, 9, tzinfo=timezone.utc)
    alpha = _document(
        slug="alpha", title="alpha beta", excerpt="shared alpha beta", retrieved_at=first_seen
    )
    gamma = _document(
        slug="gamma", title="gamma delta", excerpt="shared gamma delta", retrieved_at=later
    )
    bridge = _document(
        slug="bridge",
        title="alpha beta gamma delta",
        excerpt="shared alpha beta gamma delta",
        retrieved_at=later,
    )

    with IntelligenceStore(data_dir=private, public_repo_root=public) as store:
        store.save_document(alpha)
        store.save_document(gamma)
        initial = reconcile_events(store, similarity_threshold=0.5)
        assert len(initial) == 2
        keeper = min(initial, key=lambda event: (event.first_seen, event.id))
        absorbed = next(event for event in initial if event.id != keeper.id)
        claim = Claim(
            id="claim-absorbed",
            event_id=absorbed.id,
            text="Historical claim",
            claim_type=ClaimType.FACT,
            confidence=0.8,
            verification=VerificationStatus.CORROBORATED,
            visibility=Visibility.PRIVATE,
            created_at=later,
        )
        store.save_claim(claim)
        store.save_document(bridge)

        reconciled = reconcile_events(store, similarity_threshold=0.5)
        stored = {event.id: event for event in store.list_events()}

        assert len(reconciled) == 1
        assert reconciled[0].id == keeper.id
        assert stored[absorbed.id].status is EventStatus.DISMISSED
        assert stored[keeper.id].status is not EventStatus.DISMISSED
        assert store.get_claim(claim.id) == claim
