from __future__ import annotations

import re
from dataclasses import dataclass
from datetime import datetime
from typing import Iterable, Mapping, Sequence

from .domain import (
    Document,
    EditorialSignals,
    Event,
    EventStatus,
    Rights,
    RightsStatus,
    SourceRole,
    Visibility,
    normalize_text,
    stable_id,
)


_STOPWORDS = frozenset(
    {
        "a",
        "ai",
        "al",
        "and",
        "announces",
        "annuncio",
        "con",
        "da",
        "del",
        "della",
        "di",
        "for",
        "il",
        "in",
        "la",
        "launches",
        "lancia",
        "le",
        "new",
        "nuovo",
        "of",
        "per",
        "rilascia",
        "release",
        "releases",
        "the",
        "to",
        "un",
        "una",
        "with",
    }
)
_TOKEN_RE = re.compile(r"\b[\w][\w.+-]*\b", re.UNICODE)
_VISIBILITY_ORDER = {
    Visibility.PUBLIC_APPROVED: 0,
    Visibility.PUBLIC_CANDIDATE: 1,
    Visibility.TEAM: 2,
    Visibility.PRIVATE: 3,
}
_RIGHTS_ORDER = {
    RightsStatus.OWNED: 0,
    RightsStatus.OPEN_LICENSE: 1,
    RightsStatus.PUBLIC_LINK_ONLY: 2,
    RightsStatus.UNKNOWN: 3,
    RightsStatus.SUBSCRIBER_ONLY: 4,
    RightsStatus.PAYWALLED: 5,
    RightsStatus.PRIVATE_COMMUNICATION: 6,
}


@dataclass(frozen=True)
class RankedEvent:
    event: Event
    score: float
    components: Mapping[str, float]
    reasons: tuple[str, ...]


@dataclass(frozen=True)
class ReadingSelection:
    event_id: str
    document_id: str
    title: str
    url: str
    minutes: int
    score: float


@dataclass(frozen=True)
class ReadingQueue:
    selected: tuple[ReadingSelection, ...]
    deferred_event_ids: tuple[str, ...]
    total_minutes: int
    budget_minutes: int


def deduplicate_documents(documents: Iterable[Document]) -> tuple[Document, ...]:
    """Collapse only exact revisions; keep mirrors and later revisions as provenance."""
    ordered = sorted(documents, key=_document_quality_key)
    kept: list[Document] = []
    seen_revisions: set[tuple[str, str]] = set()
    for document in ordered:
        identity = (document.canonical_url, document.content_fingerprint)
        if identity in seen_revisions:
            continue
        kept.append(document)
        seen_revisions.add(identity)
    return tuple(sorted(kept, key=lambda item: item.id))


def document_similarity(left: Document, right: Document) -> float:
    if (
        left.canonical_url == right.canonical_url
        or left.content_fingerprint == right.content_fingerprint
    ):
        return 1.0
    title_score = _jaccard(_tokens(left.title), _tokens(right.title))
    excerpt_score = _jaccard(_tokens(left.excerpt), _tokens(right.excerpt))
    lane_score = _jaccard(set(left.lanes), set(right.lanes))
    return round(0.72 * title_score + 0.20 * excerpt_score + 0.08 * lane_score, 6)


def cluster_documents(
    documents: Iterable[Document], *, similarity_threshold: float = 0.58
) -> tuple[Event, ...]:
    """Build deterministic connected components and turn each into one event."""
    if not 0.0 <= similarity_threshold <= 1.0:
        raise ValueError("similarity_threshold deve essere compreso tra 0 e 1")
    items = list(deduplicate_documents(documents))
    adjacency: dict[str, set[str]] = {item.id: set() for item in items}
    by_id = {item.id: item for item in items}
    for index, left in enumerate(items):
        for right in items[index + 1 :]:
            if document_similarity(left, right) >= similarity_threshold:
                adjacency[left.id].add(right.id)
                adjacency[right.id].add(left.id)

    components: list[tuple[Document, ...]] = []
    unseen = set(by_id)
    while unseen:
        start = min(unseen)
        stack = [start]
        component_ids: set[str] = set()
        while stack:
            current = stack.pop()
            if current in component_ids:
                continue
            component_ids.add(current)
            stack.extend(sorted(adjacency[current] - component_ids, reverse=True))
        unseen -= component_ids
        components.append(tuple(by_id[item_id] for item_id in sorted(component_ids)))
    return tuple(sorted((_event_from_documents(group) for group in components), key=lambda e: e.id))


def rank_event(event: Event, documents: Sequence[Document]) -> RankedEvent:
    matching = [document for document in documents if document.id in event.document_ids]
    if len(matching) != len(event.document_ids):
        raise ValueError("Mancano documenti necessari al ranking dell'evento")
    authority = max(document.provenance.authority for document in matching)
    official_bonus = 1.0 if any(document.provenance.is_official for document in matching) else 0.0
    distinct_sources = len({document.provenance.source_id for document in matching})
    corroboration = min(1.0, max(0, distinct_sources - 1) / 3)
    lane_diversity = min(1.0, max(0, len(event.lanes) - 1) / 3)
    interdisciplinary = min(
        1.0, 0.75 * event.signals.bridge_potential + 0.25 * lane_diversity
    )
    components = {
        "novelty": event.signals.novelty * 18,
        "impact": event.signals.impact * 20,
        "authority": authority * 14,
        "official_source": official_bonus * 5,
        "project_relevance": event.signals.project_relevance * 17,
        "information_density": event.signals.information_density * 10,
        "interdisciplinary_bridge": interdisciplinary * 12,
        "corroboration": corroboration * 4,
    }
    reasons: list[str] = []
    if official_bonus:
        reasons.append("fonte ufficiale presente")
    if distinct_sources >= 2:
        reasons.append(f"confermato da {distinct_sources} fonti distinte")
    if interdisciplinary >= 0.6:
        reasons.append("alto potenziale di connessione interdisciplinare")
    if event.signals.project_relevance >= 0.7:
        reasons.append("rilevante per i filoni operativi")
    score = round(sum(components.values()), 3)
    return RankedEvent(event, score, {key: round(value, 3) for key, value in components.items()}, tuple(reasons))


def rank_events(events: Iterable[Event], documents: Sequence[Document]) -> tuple[RankedEvent, ...]:
    ranked = (rank_event(event, documents) for event in events if event.status is not EventStatus.DISMISSED)
    return tuple(sorted(ranked, key=lambda item: (-item.score, item.event.id)))


def build_reading_queue(
    ranked_events: Iterable[RankedEvent],
    documents: Sequence[Document],
    *,
    budget_minutes: int,
) -> ReadingQueue:
    """Choose full reads with deterministic 0/1 knapsack under a hard budget."""
    if budget_minutes < 0:
        raise ValueError("budget_minutes non puo' essere negativo")
    by_id = {document.id: document for document in documents}
    candidates: list[ReadingSelection] = []
    all_ranked_ids: list[str] = []
    for ranked in ranked_events:
        event = ranked.event
        all_ranked_ids.append(event.id)
        readable = [
            by_id[document_id]
            for document_id in event.document_ids
            if document_id in by_id and by_id[document_id].estimated_read_minutes > 0
        ]
        if not readable:
            continue
        chosen = min(
            readable,
            key=lambda document: (
                document.estimated_read_minutes,
                _document_quality_key(document),
                document.id,
            ),
        )
        candidates.append(
            ReadingSelection(
                event_id=event.id,
                document_id=chosen.id,
                title=chosen.title,
                url=chosen.canonical_url,
                minutes=chosen.estimated_read_minutes,
                score=ranked.score,
            )
        )
    candidates.sort(key=lambda item: item.event_id)

    # Each state stores (value, selected indexes). Stable IDs settle exact ties.
    states: list[tuple[float, tuple[int, ...]]] = [(0.0, ()) for _ in range(budget_minutes + 1)]
    for index, candidate in enumerate(candidates):
        for capacity in range(budget_minutes, candidate.minutes - 1, -1):
            previous_value, previous_indexes = states[capacity - candidate.minutes]
            proposed = (round(previous_value + candidate.score, 6), previous_indexes + (index,))
            current = states[capacity]
            if _better_selection(proposed, current, candidates):
                states[capacity] = proposed

    best = states[0]
    for state in states[1:]:
        if _better_selection(state, best, candidates):
            best = state
    selected = tuple(candidates[index] for index in best[1])
    selected_ids = {item.event_id for item in selected}
    deferred = tuple(event_id for event_id in all_ranked_ids if event_id not in selected_ids)
    return ReadingQueue(
        selected=tuple(sorted(selected, key=lambda item: (-item.score, item.event_id))),
        deferred_event_ids=deferred,
        total_minutes=sum(item.minutes for item in selected),
        budget_minutes=budget_minutes,
    )


def _event_from_documents(documents: tuple[Document, ...]) -> Event:
    primary = min(documents, key=_document_quality_key)
    ordered_ids = tuple(sorted(document.id for document in documents))
    event_id = stable_id("event", *ordered_ids)
    first_seen = min(document.provenance.retrieved_at for document in documents)
    last_seen = max(document.provenance.retrieved_at for document in documents)
    lanes = tuple(sorted({lane for document in documents for lane in document.lanes}))
    visibility = max(
        (document.visibility for document in documents), key=_VISIBILITY_ORDER.__getitem__
    )
    most_restrictive = max(
        (document.rights for document in documents), key=lambda rights: _RIGHTS_ORDER[rights.status]
    )
    distinct_sources = len({document.provenance.source_id for document in documents})
    bridge = min(1.0, max(0, len(lanes) - 1) / 3)
    return Event(
        id=event_id,
        title=primary.title,
        summary=primary.excerpt,
        document_ids=ordered_ids,
        primary_document_id=primary.id,
        lanes=lanes,
        first_seen=first_seen,
        last_seen=last_seen,
        visibility=visibility,
        rights=Rights(
            status=most_restrictive.status,
            license_url=most_restrictive.license_url,
            attribution=most_restrictive.attribution,
            public_use=most_restrictive.public_use,
        ),
        signals=EditorialSignals(
            novelty=0.5,
            impact=0.5,
            information_density=0.5,
            project_relevance=0.5,
            bridge_potential=bridge,
        ),
        status=EventStatus.VERIFIED if distinct_sources >= 2 else EventStatus.CANDIDATE,
    )


def _document_quality_key(document: Document) -> tuple[float, int, float, str]:
    role_order = {
        SourceRole.PRIMARY: 0,
        SourceRole.CONFIRMATION: 1,
        SourceRole.ANALYSIS: 2,
        SourceRole.OPINION: 3,
        SourceRole.RUMOR: 4,
    }
    return (
        -float(document.provenance.is_official),
        role_order[document.provenance.role],
        -document.provenance.authority,
        document.id,
    )


def _tokens(value: str) -> set[str]:
    return {
        token
        for token in _TOKEN_RE.findall(normalize_text(value))
        if len(token) >= 2 and token not in _STOPWORDS
    }


def _jaccard(left: set[str], right: set[str]) -> float:
    if not left and not right:
        return 1.0
    if not left or not right:
        return 0.0
    return len(left & right) / len(left | right)


def _better_selection(
    proposed: tuple[float, tuple[int, ...]],
    current: tuple[float, tuple[int, ...]],
    candidates: Sequence[ReadingSelection],
) -> bool:
    if proposed[0] != current[0]:
        return proposed[0] > current[0]
    proposed_minutes = sum(candidates[index].minutes for index in proposed[1])
    current_minutes = sum(candidates[index].minutes for index in current[1])
    if proposed_minutes != current_minutes:
        return proposed_minutes < current_minutes
    proposed_ids = tuple(candidates[index].event_id for index in proposed[1])
    current_ids = tuple(candidates[index].event_id for index in current[1])
    return proposed_ids < current_ids
