from __future__ import annotations

from dataclasses import replace
from datetime import datetime, timezone
from typing import Iterable
from urllib.parse import quote

from .connectors import SourceRecord
from .curation import RankedEvent, cluster_documents, rank_events
from .domain import (
    Document,
    Event,
    EventStatus,
    Provenance,
    Rights,
    RightsStatus,
    SourceRole,
    Visibility,
    stable_id,
)
from .providers import Candidate, DeterministicProvider, EditorialProvider
from .rendering import DigestEntry, SourceLink, allocate_reading_budget
from .storage import IntelligenceStore


LANE_TERMS: dict[str, tuple[str, ...]] = {
    "research": ("paper", "arxiv", "benchmark", "research", "training", "evaluation"),
    "agents_coding": ("agent", "coding", "code", "sdk", "api", "mcp", "developer"),
    "product": ("launch", "product", "feature", "release", "tool"),
    "labs_business": ("openai", "anthropic", "deepmind", "meta ai", "xai", "mistral"),
    "business_strategy": ("funding", "acquisition", "strategy", "regulation", "enterprise"),
    "marketing": ("marketing", "brand", "creator", "sales", "pricing"),
    "education": ("education", "academy", "learning", "training course", "teaching"),
    "philosophy": ("philosophy", "epistemology", "intentionality", "agency", "ethics"),
    "neuroscience": ("brain", "neuroscience", "cognition", "perception"),
    "linguistics_semantics": ("language", "linguistic", "semantic", "meaning"),
    "mathematics": ("mathematics", "theorem", "proof", "optimization"),
    "management_leadership": ("management", "leadership", "organization", "team"),
    "spatial_embodied_ai": (
        "spatial intelligence",
        "world model",
        "robot",
        "embodied",
        "simulation",
    ),
}

_EXTERNAL_ALLOWED_RIGHTS = frozenset(
    {
        RightsStatus.OWNED,
        RightsStatus.OPEN_LICENSE,
        RightsStatus.PUBLIC_LINK_ONLY,
    }
)


def infer_lanes(title: str, text: str) -> tuple[str, ...]:
    haystack = f"{title} {text}".casefold()
    lanes = tuple(
        lane for lane, terms in LANE_TERMS.items() if any(term in haystack for term in terms)
    )
    return lanes or ("product",)


def source_record_to_document(record: SourceRecord, retrieved_at: datetime) -> Document:
    if retrieved_at.tzinfo is None:
        raise ValueError("retrieved_at deve includere il fuso orario")
    is_private = record.source_type == "email"
    if record.url:
        document_url = record.url
    else:
        document_url = (
            "https://private.invalid/"
            f"{quote(record.source_id, safe='')}/{stable_id('source-record', record.external_id)}"
        )
    source_url = record.url or "https://private.invalid/"
    authority = 0.7 if record.source_type in {"rss", "x"} else 0.5
    return Document.create(
        title=record.title,
        url=document_url,
        excerpt=record.text[:2_000],
        content=record.text,
        provenance=Provenance(
            source_id=record.source_id,
            source_name=record.author or record.source_id,
            source_url=source_url,
            retrieved_at=retrieved_at.astimezone(timezone.utc),
            published_at=record.published_at,
            access_method=record.source_type,
            role=SourceRole.ANALYSIS,
            authority=authority,
            is_official=False,
        ),
        visibility=Visibility.PRIVATE,
        rights=Rights(
            RightsStatus.PRIVATE_COMMUNICATION if is_private else RightsStatus.PUBLIC_LINK_ONLY
        ),
        lanes=infer_lanes(record.title, record.text),
        authors=(record.author,) if record.author else (),
        estimated_read_minutes=max(1, round(len(record.text.split()) / 220)) if record.text else 0,
    )


def ingest_records(
    store: IntelligenceStore,
    records: Iterable[SourceRecord],
    *,
    retrieved_at: datetime | None = None,
) -> tuple[Document, ...]:
    timestamp = retrieved_at or datetime.now(timezone.utc)
    saved = []
    for record in records:
        saved.append(store.save_document(source_record_to_document(record, timestamp)))
    return tuple(saved)


def reconcile_events(store: IntelligenceStore, *, similarity_threshold: float = 0.58) -> tuple[Event, ...]:
    documents = store.list_documents()
    candidates = cluster_documents(documents, similarity_threshold=similarity_threshold)
    existing = store.list_events()
    existing_sets = {event.id: set(event.document_ids) for event in existing}
    output = []
    for candidate in candidates:
        overlaps = [
            event
            for event in existing
            if existing_sets[event.id].intersection(candidate.document_ids)
        ]
        if overlaps:
            keeper = min(overlaps, key=lambda event: (event.first_seen, event.id))
            candidate = replace(candidate, id=keeper.id, first_seen=min(keeper.first_seen, candidate.first_seen))
            for absorbed in overlaps:
                if absorbed.id != keeper.id:
                    store.save_event(replace(absorbed, status=EventStatus.DISMISSED))
        store.save_event(candidate)
        output.append(candidate)
    return tuple(output)


def ranked_candidates(store: IntelligenceStore) -> tuple[RankedEvent, ...]:
    return rank_events(store.list_events(), store.list_documents())


def build_digest_entries(
    store: IntelligenceStore,
    ranked: Iterable[RankedEvent],
    provider: EditorialProvider,
    *,
    max_events: int,
    reading_budget_minutes: int,
) -> tuple[DigestEntry, ...]:
    selected = tuple(ranked)[:max_events]
    candidates = []
    for item in selected:
        documents = store.documents_for_event(item.event.id)
        candidates.append(
            Candidate(
                event_id=item.event.id,
                title=item.event.title,
                excerpt=item.event.summary,
                source_urls=tuple(document.canonical_url for document in documents),
                lane_hint=item.event.lanes[0] if item.event.lanes else "other",
            )
        )
    if provider.is_external:
        event_by_id = {item.event.id: item.event for item in selected}
        local_candidates = tuple(
            candidate
            for candidate in candidates
            if event_by_id[candidate.event_id].rights.status not in _EXTERNAL_ALLOWED_RIGHTS
        )
        external_candidates = tuple(
            candidate
            for candidate in candidates
            if event_by_id[candidate.event_id].rights.status in _EXTERNAL_ALLOWED_RIGHTS
        )
        external_analyses = provider.analyze(external_candidates) if external_candidates else ()
        local_analyses = DeterministicProvider().analyze(local_candidates)
        raw_analyses = (*external_analyses, *local_analyses)
    else:
        raw_analyses = provider.analyze(candidates)
    analyses = {analysis.event_id: analysis for analysis in raw_analyses}
    entries = []
    for item in selected:
        event = item.event
        analysis = analyses[event.id]
        documents = store.documents_for_event(event.id)
        sources = tuple(
            SourceLink(
                document.provenance.source_name,
                document.canonical_url,
                "primary" if document.id == event.primary_document_id else "supporting",
            )
            for document in documents
        )
        entries.append(
            DigestEntry(
                event_id=event.id,
                title=event.title,
                tldr=analysis.tldr,
                why_it_matters=analysis.why_it_matters,
                score=item.score,
                lane=analysis.lane,
                sources=sources,
                read_minutes=analysis.read_minutes,
                read_decision=analysis.read_decision,
                bridge=analysis.bridge,
                confidence=analysis.confidence,
            )
        )
    return allocate_reading_budget(entries, reading_budget_minutes)
