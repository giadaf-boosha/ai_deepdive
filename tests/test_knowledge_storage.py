from __future__ import annotations

import sqlite3
from datetime import datetime, timedelta, timezone
from pathlib import Path

import pytest

from intelligence.curation import cluster_documents
from intelligence.domain import (
    Application,
    Bridge,
    BridgeRelation,
    Claim,
    ClaimEvidence,
    ClaimType,
    Concept,
    DeliveryRecord,
    DeliveryStatus,
    Document,
    EvidenceRelation,
    KnowledgeMaturity,
    OutputRecord,
    OutputStatus,
    Provenance,
    ReadingDecision,
    ReadingDisposition,
    ReadingNote,
    Rights,
    RightsRecord,
    RightsStatus,
    RunRecord,
    RunStatus,
    SourceRole,
    Thesis,
    VerificationStatus,
    Visibility,
    Watermark,
)
from intelligence.storage import IntelligenceStore, SCHEMA_VERSION, StorageError


NOW = datetime(2026, 8, 23, 7, 0, tzinfo=timezone.utc)


def _base(store: IntelligenceStore):
    document = Document.create(
        title="World models connect perception and action",
        url="https://lab.example/world-models",
        excerpt="A verified research result.",
        content="Full original abstract for fingerprinting.",
        provenance=Provenance(
            source_id="lab",
            source_name="Official Lab",
            source_url="https://lab.example",
            retrieved_at=NOW,
            role=SourceRole.PRIMARY,
            authority=0.95,
            is_official=True,
        ),
        visibility=Visibility.PRIVATE,
        rights=Rights(RightsStatus.PUBLIC_LINK_ONLY),
        lanes=("spatial_embodied_ai", "neuroscience"),
        estimated_read_minutes=12,
    )
    event = cluster_documents((document,))[0]
    store.save_document(document)
    store.save_event(event)
    return document, event


def _claim(event_id: str, *, text: str = "Perception guides action") -> Claim:
    return Claim(
        id="claim-1",
        event_id=event_id,
        text=text,
        claim_type=ClaimType.FACT,
        confidence=0.9,
        verification=VerificationStatus.VERIFIED,
        visibility=Visibility.PRIVATE,
        created_at=NOW,
    )


def test_claim_evidence_foreign_keys_and_idempotent_upsert(tmp_path: Path) -> None:
    repo = tmp_path / "repo"
    repo.mkdir()
    with IntelligenceStore(data_dir=tmp_path / "data", public_repo_root=repo) as store:
        document, event = _base(store)
        claim = _claim(event.id)
        store.save_claim(claim)
        updated = Claim(**{**claim.__dict__, "text": "Perception deterministically guides action"})
        store.save_claim(updated)
        assert store.list_claims() == (updated,)

        evidence = ClaimEvidence(
            id="evidence-1",
            claim_id=claim.id,
            document_id=document.id,
            relation=EvidenceRelation.SUPPORTS,
            locator="abstract",
            excerpt="A short necessary excerpt.",
            visibility=Visibility.PRIVATE,
        )
        store.save_claim_evidence(evidence)
        assert store.get_claim_evidence(evidence.id) == evidence

        invalid = ClaimEvidence(**{**evidence.__dict__, "id": "bad", "claim_id": "missing"})
        with pytest.raises(sqlite3.IntegrityError):
            store.save_claim_evidence(invalid)


def test_complete_knowledge_records_round_trip(tmp_path: Path) -> None:
    repo = tmp_path / "repo"
    repo.mkdir()
    with IntelligenceStore(data_dir=tmp_path / "data", public_repo_root=repo) as store:
        document, event = _base(store)
        claim = _claim(event.id)
        store.save_claim(claim)
        first = Concept(
            "concept-perception",
            "Perception",
            "Acquisition and interpretation of signals.",
            ("neuroscience",),
            KnowledgeMaturity.VALIDATED,
            Visibility.TEAM,
            NOW,
            NOW,
        )
        second = Concept(
            "concept-agency",
            "Agency",
            "Capacity to select and enact goals.",
            ("philosophy",),
            KnowledgeMaturity.DEVELOPING,
            Visibility.PRIVATE,
            NOW,
        )
        store.save_concept(first)
        store.save_concept(second)
        bridge = Bridge(
            "bridge-1",
            first.id,
            second.id,
            BridgeRelation.SHARED_MECHANISM,
            "Perception constrains agency.",
            "Action selection depends on a representation of available state.",
            (claim.id,),
            (),
            0.3,
            0.8,
            0.9,
            KnowledgeMaturity.DEVELOPING,
            Visibility.PRIVATE,
        )
        store.save_bridge(bridge)
        decision = ReadingDecision(
            "decision-1",
            event.id,
            document.id,
            ReadingDisposition.READ_FULL,
            "High bridge potential",
            12,
            0.9,
            Visibility.PRIVATE,
            NOW,
        )
        store.save_reading_decision(decision)
        note = ReadingNote(
            "note-1",
            decision.id,
            "The paper grounds the bridge.",
            ("Perception is action-oriented",),
            ("How robust is the mechanism?",),
            Visibility.PRIVATE,
            NOW + timedelta(minutes=12),
        )
        store.save_reading_note(note)
        application = Application(
            "application-1",
            "Boosha",
            "Design training around perception-to-action loops.",
            (claim.id,),
            KnowledgeMaturity.SEED,
            Visibility.TEAM,
            NOW,
        )
        store.save_application(application)
        thesis = Thesis(
            "thesis-1",
            "Agency requires more than language.",
            "Language-only systems can still plan effectively.",
            (claim.id,),
            (),
            KnowledgeMaturity.DEVELOPING,
            Visibility.PRIVATE,
            NOW,
            NOW,
        )
        store.save_thesis(thesis)
        output = OutputRecord(
            "output-1",
            "talk",
            "Beyond language",
            "Business leaders",
            thesis.id,
            OutputStatus.DRAFT,
            False,
            False,
            Visibility.PRIVATE,
            NOW,
            NOW,
        )
        store.save_output(output)
        rights = RightsRecord(
            "rights-1",
            "document",
            document.id,
            Rights(RightsStatus.PUBLIC_LINK_ONLY),
            document.canonical_url,
            Visibility.PRIVATE,
            NOW,
        )
        store.save_rights_record(rights)

        assert store.list_concepts() == tuple(sorted((first, second), key=lambda item: item.id))
        assert store.get_bridge(bridge.id) == bridge
        assert store.get_reading_decision(decision.id) == decision
        assert store.get_reading_note(note.id) == note
        assert store.get_application(application.id) == application
        assert store.get_thesis(thesis.id) == thesis
        assert store.get_output(output.id) == output
        assert store.get_rights_record(rights.id) == rights


def test_public_output_requires_both_review_gates() -> None:
    with pytest.raises(ValueError):
        OutputRecord(
            "output-public",
            "substack",
            "Title",
            "Readers",
            None,
            OutputStatus.READY,
            True,
            False,
            Visibility.PUBLIC_APPROVED,
            NOW,
            NOW,
        )


def test_delivery_idempotency_and_monotonic_watermark(tmp_path: Path) -> None:
    repo = tmp_path / "repo"
    repo.mkdir()
    with IntelligenceStore(data_dir=tmp_path / "data", public_repo_root=repo) as store:
        run = RunRecord("run-1", "am", NOW, RunStatus.RUNNING)
        store.save_run(run)
        first = DeliveryRecord(
            "delivery-1",
            run.id,
            "email",
            "giada.f@me.com",
            DeliveryStatus.PREVIEW,
            "am:2026-08-23:giada",
            NOW,
        )
        duplicate = DeliveryRecord(
            "delivery-2",
            run.id,
            "email",
            "giada.f@me.com",
            DeliveryStatus.PREVIEW,
            first.idempotency_key,
            NOW,
        )
        assert store.save_delivery(first) == first
        assert store.save_delivery(duplicate) == first
        assert store.list_deliveries() == (first,)

        newer = Watermark("x-watchlist", "cursor-2", NOW + timedelta(minutes=10), run.id)
        older = Watermark("x-watchlist", "cursor-1", NOW, run.id)
        assert store.save_watermark(newer) == newer
        assert store.save_watermark(older) == newer
        assert store.get_watermark("x-watchlist") == newer


def test_v1_to_v2_migration_preserves_documents(tmp_path: Path) -> None:
    repo = tmp_path / "repo"
    repo.mkdir()
    data = tmp_path / "data"
    with IntelligenceStore(data_dir=data, public_repo_root=repo) as store:
        document, _ = _base(store)

    connection = sqlite3.connect(data / "intelligence.sqlite3")
    for table in (
        "watermarks",
        "deliveries",
        "runs",
        "rights_records",
        "outputs",
        "theses",
        "applications",
        "reading_notes",
        "reading_decisions",
        "bridges",
        "concepts",
        "claim_evidence",
        "claims",
    ):
        connection.execute(f"DROP TABLE {table}")
    connection.execute("PRAGMA user_version = 1")
    connection.commit()
    connection.close()

    with IntelligenceStore(data_dir=data, public_repo_root=repo) as migrated:
        assert migrated.get_document(document.id) == document
        assert migrated._connection.execute("PRAGMA user_version").fetchone()[0] == SCHEMA_VERSION
        run = RunRecord("run-after-migration", "pm", NOW, RunStatus.RUNNING)
        migrated.save_run(run)
        assert migrated.get_run(run.id) == run
