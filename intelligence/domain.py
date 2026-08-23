from __future__ import annotations

import hashlib
import re
from dataclasses import dataclass, field
from datetime import datetime, timezone
from decimal import Decimal
from enum import StrEnum
from typing import Iterable
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit


_TRACKING_PARAMETERS = frozenset(
    {
        "fbclid",
        "gclid",
        "mc_cid",
        "mc_eid",
        "ref_src",
        "ref_url",
        "s",
        "source",
    }
)
_WHITESPACE_RE = re.compile(r"\s+")


class Visibility(StrEnum):
    PRIVATE = "private"
    TEAM = "team"
    PUBLIC_CANDIDATE = "public_candidate"
    PUBLIC_APPROVED = "public_approved"


class RightsStatus(StrEnum):
    OWNED = "owned"
    OPEN_LICENSE = "open_license"
    PUBLIC_LINK_ONLY = "public_link_only"
    SUBSCRIBER_ONLY = "subscriber_only"
    PAYWALLED = "paywalled"
    PRIVATE_COMMUNICATION = "private_communication"
    UNKNOWN = "unknown"


class SourceRole(StrEnum):
    PRIMARY = "primary"
    CONFIRMATION = "confirmation"
    ANALYSIS = "analysis"
    OPINION = "opinion"
    RUMOR = "rumor"


class EventStatus(StrEnum):
    CANDIDATE = "candidate"
    VERIFIED = "verified"
    UPDATED = "updated"
    CORRECTED = "corrected"
    DISMISSED = "dismissed"


class ClaimType(StrEnum):
    FACT = "fact"
    INFERENCE = "inference"
    OPINION = "opinion"
    RUMOR = "rumor"


class VerificationStatus(StrEnum):
    UNVERIFIED = "unverified"
    CORROBORATED = "corroborated"
    VERIFIED = "verified"
    DISPUTED = "disputed"
    RETRACTED = "retracted"


class EvidenceRelation(StrEnum):
    SUPPORTS = "supports"
    CONTRADICTS = "contradicts"
    CONTEXT = "context"


class KnowledgeMaturity(StrEnum):
    SEED = "seed"
    DEVELOPING = "developing"
    VALIDATED = "validated"
    SUPERSEDED = "superseded"
    REJECTED = "rejected"


class BridgeRelation(StrEnum):
    ANALOGY = "analogy"
    CAUSAL = "causal"
    SHARED_MECHANISM = "shared_mechanism"
    TENSION = "tension"
    TRANSFER = "transfer"
    LINEAGE = "lineage"


class ReadingDisposition(StrEnum):
    READ_FULL = "read_full"
    TLDR = "tldr"
    DEFER = "defer"
    SKIP = "skip"


class OutputStatus(StrEnum):
    IDEA = "idea"
    RESEARCHING = "researching"
    DRAFT = "draft"
    REVIEW = "review"
    READY = "ready"
    PUBLISHED = "published"
    ARCHIVED = "archived"


class RunStatus(StrEnum):
    RUNNING = "running"
    SUCCEEDED = "succeeded"
    PARTIAL = "partial"
    FAILED = "failed"


class DeliveryStatus(StrEnum):
    PENDING = "pending"
    PREVIEW = "preview"
    SENT = "sent"
    FAILED = "failed"
    BLOCKED = "blocked"


class CostStatus(StrEnum):
    RESERVED = "reserved"
    SETTLED = "settled"
    RELEASED = "released"


@dataclass(frozen=True)
class Rights:
    status: RightsStatus
    license_url: str | None = None
    attribution: str | None = None
    public_use: str = "link_and_original_paraphrase_only"

    def __post_init__(self) -> None:
        if self.status is RightsStatus.OPEN_LICENSE and not self.license_url:
            raise ValueError("I contenuti open-license richiedono license_url")
        if self.status is RightsStatus.OWNED and self.public_use == "blocked":
            raise ValueError("Un contenuto owned non puo' avere public_use=blocked")


@dataclass(frozen=True)
class Provenance:
    source_id: str
    source_name: str
    source_url: str
    retrieved_at: datetime
    published_at: datetime | None = None
    access_method: str = "public_web"
    role: SourceRole = SourceRole.ANALYSIS
    authority: float = 0.5
    is_official: bool = False

    def __post_init__(self) -> None:
        if not self.source_id.strip() or not self.source_name.strip():
            raise ValueError("source_id e source_name sono obbligatori")
        _require_http_url(self.source_url, "source_url")
        _require_aware(self.retrieved_at, "retrieved_at")
        if self.published_at is not None:
            _require_aware(self.published_at, "published_at")
        _require_unit_interval(self.authority, "authority")


@dataclass(frozen=True)
class Document:
    id: str
    title: str
    canonical_url: str
    excerpt: str
    provenance: Provenance
    visibility: Visibility
    rights: Rights
    content_fingerprint: str
    lanes: tuple[str, ...] = field(default_factory=tuple)
    authors: tuple[str, ...] = field(default_factory=tuple)
    estimated_read_minutes: int = 0

    def __post_init__(self) -> None:
        if not self.id.strip() or not self.title.strip():
            raise ValueError("id e title del documento sono obbligatori")
        _require_http_url(self.canonical_url, "canonical_url")
        if not self.content_fingerprint.strip():
            raise ValueError("content_fingerprint e' obbligatorio")
        if self.estimated_read_minutes < 0:
            raise ValueError("estimated_read_minutes non puo' essere negativo")
        _require_unique_nonempty(self.lanes, "lanes")
        _require_unique_nonempty(self.authors, "authors")

    @classmethod
    def create(
        cls,
        *,
        title: str,
        url: str,
        excerpt: str,
        provenance: Provenance,
        visibility: Visibility = Visibility.PRIVATE,
        rights: Rights | None = None,
        content: str | None = None,
        lanes: Iterable[str] = (),
        authors: Iterable[str] = (),
        estimated_read_minutes: int = 0,
    ) -> Document:
        canonical_url = canonicalize_url(url)
        normalized_title = normalize_text(title)
        normalized_content = normalize_text(content if content is not None else excerpt)
        fingerprint = stable_id("content", normalized_content or normalized_title)
        document_id = stable_id("doc", canonical_url, fingerprint)
        return cls(
            id=document_id,
            title=_WHITESPACE_RE.sub(" ", title).strip(),
            canonical_url=canonical_url,
            excerpt=_WHITESPACE_RE.sub(" ", excerpt).strip(),
            provenance=provenance,
            visibility=visibility,
            rights=rights or Rights(RightsStatus.PUBLIC_LINK_ONLY),
            content_fingerprint=fingerprint,
            lanes=_clean_values(lanes),
            authors=_clean_values(authors),
            estimated_read_minutes=estimated_read_minutes,
        )


@dataclass(frozen=True)
class EditorialSignals:
    novelty: float = 0.5
    impact: float = 0.5
    information_density: float = 0.5
    project_relevance: float = 0.5
    bridge_potential: float = 0.0

    def __post_init__(self) -> None:
        for name in (
            "novelty",
            "impact",
            "information_density",
            "project_relevance",
            "bridge_potential",
        ):
            _require_unit_interval(getattr(self, name), name)


@dataclass(frozen=True)
class Event:
    id: str
    title: str
    summary: str
    document_ids: tuple[str, ...]
    primary_document_id: str
    lanes: tuple[str, ...]
    first_seen: datetime
    last_seen: datetime
    visibility: Visibility
    rights: Rights
    signals: EditorialSignals = field(default_factory=EditorialSignals)
    status: EventStatus = EventStatus.CANDIDATE

    def __post_init__(self) -> None:
        if not self.id.strip() or not self.title.strip():
            raise ValueError("id e title dell'evento sono obbligatori")
        if not self.document_ids:
            raise ValueError("Un evento richiede almeno un documento")
        _require_unique_nonempty(self.document_ids, "document_ids")
        if self.primary_document_id not in self.document_ids:
            raise ValueError("primary_document_id deve appartenere a document_ids")
        _require_unique_nonempty(self.lanes, "lanes")
        _require_aware(self.first_seen, "first_seen")
        _require_aware(self.last_seen, "last_seen")
        if self.last_seen < self.first_seen:
            raise ValueError("last_seen non puo' precedere first_seen")


@dataclass(frozen=True)
class Claim:
    id: str
    event_id: str
    text: str
    claim_type: ClaimType
    confidence: float
    verification: VerificationStatus
    visibility: Visibility
    created_at: datetime

    def __post_init__(self) -> None:
        _require_text_fields(self, "id", "event_id", "text")
        _require_unit_interval(self.confidence, "confidence")
        _require_aware(self.created_at, "created_at")


@dataclass(frozen=True)
class ClaimEvidence:
    id: str
    claim_id: str
    document_id: str
    relation: EvidenceRelation
    locator: str
    excerpt: str
    visibility: Visibility

    def __post_init__(self) -> None:
        _require_text_fields(self, "id", "claim_id", "document_id", "locator")


@dataclass(frozen=True)
class Concept:
    id: str
    name: str
    definition: str
    domains: tuple[str, ...]
    maturity: KnowledgeMaturity
    visibility: Visibility
    created_at: datetime
    last_reviewed_at: datetime | None = None

    def __post_init__(self) -> None:
        _require_text_fields(self, "id", "name", "definition")
        _require_unique_nonempty(self.domains, "domains")
        _require_aware(self.created_at, "created_at")
        if self.last_reviewed_at is not None:
            _require_aware(self.last_reviewed_at, "last_reviewed_at")


@dataclass(frozen=True)
class Bridge:
    id: str
    from_concept_id: str
    to_concept_id: str
    relation: BridgeRelation
    statement: str
    mechanism: str
    supporting_claim_ids: tuple[str, ...]
    opposing_claim_ids: tuple[str, ...]
    risk_of_analogy: float
    novelty: float
    usefulness: float
    maturity: KnowledgeMaturity
    visibility: Visibility

    def __post_init__(self) -> None:
        _require_text_fields(
            self, "id", "from_concept_id", "to_concept_id", "statement", "mechanism"
        )
        if self.from_concept_id == self.to_concept_id:
            raise ValueError("Un bridge richiede due concetti diversi")
        _require_unique_nonempty(self.supporting_claim_ids, "supporting_claim_ids")
        _require_unique_nonempty(self.opposing_claim_ids, "opposing_claim_ids")
        for name in ("risk_of_analogy", "novelty", "usefulness"):
            _require_unit_interval(getattr(self, name), name)


@dataclass(frozen=True)
class ReadingDecision:
    id: str
    event_id: str
    document_id: str
    disposition: ReadingDisposition
    reason: str
    estimated_minutes: int
    priority: float
    visibility: Visibility
    created_at: datetime

    def __post_init__(self) -> None:
        _require_text_fields(self, "id", "event_id", "document_id", "reason")
        if self.estimated_minutes < 0:
            raise ValueError("estimated_minutes non puo' essere negativo")
        _require_unit_interval(self.priority, "priority")
        _require_aware(self.created_at, "created_at")


@dataclass(frozen=True)
class ReadingNote:
    id: str
    decision_id: str
    summary: str
    insights: tuple[str, ...]
    questions: tuple[str, ...]
    visibility: Visibility
    completed_at: datetime

    def __post_init__(self) -> None:
        _require_text_fields(self, "id", "decision_id", "summary")
        _require_unique_nonempty(self.insights, "insights")
        _require_unique_nonempty(self.questions, "questions")
        _require_aware(self.completed_at, "completed_at")


@dataclass(frozen=True)
class Application:
    id: str
    target: str
    statement: str
    evidence_claim_ids: tuple[str, ...]
    maturity: KnowledgeMaturity
    visibility: Visibility
    created_at: datetime

    def __post_init__(self) -> None:
        _require_text_fields(self, "id", "target", "statement")
        _require_unique_nonempty(self.evidence_claim_ids, "evidence_claim_ids")
        _require_aware(self.created_at, "created_at")


@dataclass(frozen=True)
class Thesis:
    id: str
    statement: str
    counterargument: str
    supporting_claim_ids: tuple[str, ...]
    opposing_claim_ids: tuple[str, ...]
    maturity: KnowledgeMaturity
    visibility: Visibility
    created_at: datetime
    updated_at: datetime

    def __post_init__(self) -> None:
        _require_text_fields(self, "id", "statement", "counterargument")
        _require_unique_nonempty(self.supporting_claim_ids, "supporting_claim_ids")
        _require_unique_nonempty(self.opposing_claim_ids, "opposing_claim_ids")
        _require_aware(self.created_at, "created_at")
        _require_aware(self.updated_at, "updated_at")
        if self.updated_at < self.created_at:
            raise ValueError("updated_at non puo' precedere created_at")


@dataclass(frozen=True)
class OutputRecord:
    id: str
    output_type: str
    title: str
    audience: str
    thesis_id: str | None
    status: OutputStatus
    rights_reviewed: bool
    fact_reviewed: bool
    visibility: Visibility
    created_at: datetime
    updated_at: datetime

    def __post_init__(self) -> None:
        _require_text_fields(self, "id", "output_type", "title", "audience")
        if self.thesis_id is not None and not self.thesis_id.strip():
            raise ValueError("thesis_id non puo' essere vuoto")
        _require_aware(self.created_at, "created_at")
        _require_aware(self.updated_at, "updated_at")
        if self.updated_at < self.created_at:
            raise ValueError("updated_at non puo' precedere created_at")
        if self.visibility is Visibility.PUBLIC_APPROVED and not (
            self.rights_reviewed and self.fact_reviewed
        ):
            raise ValueError("Un output public_approved richiede fact e rights review")


@dataclass(frozen=True)
class RightsRecord:
    id: str
    resource_kind: str
    resource_id: str
    rights: Rights
    source_url: str
    visibility: Visibility
    reviewed_at: datetime

    def __post_init__(self) -> None:
        _require_text_fields(self, "id", "resource_kind", "resource_id")
        _require_http_url(self.source_url, "source_url")
        _require_aware(self.reviewed_at, "reviewed_at")


@dataclass(frozen=True)
class RunRecord:
    id: str
    kind: str
    started_at: datetime
    status: RunStatus
    completed_at: datetime | None = None
    error: str | None = None
    visibility: Visibility = Visibility.PRIVATE

    def __post_init__(self) -> None:
        _require_text_fields(self, "id", "kind")
        _require_aware(self.started_at, "started_at")
        if self.completed_at is not None:
            _require_aware(self.completed_at, "completed_at")
            if self.completed_at < self.started_at:
                raise ValueError("completed_at non puo' precedere started_at")
        if self.status is RunStatus.RUNNING and self.completed_at is not None:
            raise ValueError("Un run running non puo' avere completed_at")
        if self.status is not RunStatus.RUNNING and self.completed_at is None:
            raise ValueError("Un run concluso richiede completed_at")


@dataclass(frozen=True)
class DeliveryRecord:
    id: str
    run_id: str
    channel: str
    recipient: str
    status: DeliveryStatus
    idempotency_key: str
    created_at: datetime
    delivered_at: datetime | None = None
    error: str | None = None
    visibility: Visibility = Visibility.PRIVATE

    def __post_init__(self) -> None:
        _require_text_fields(
            self, "id", "run_id", "channel", "recipient", "idempotency_key"
        )
        _require_aware(self.created_at, "created_at")
        if self.delivered_at is not None:
            _require_aware(self.delivered_at, "delivered_at")
            if self.delivered_at < self.created_at:
                raise ValueError("delivered_at non puo' precedere created_at")
        if self.status is DeliveryStatus.SENT and self.delivered_at is None:
            raise ValueError("Una delivery sent richiede delivered_at")


@dataclass(frozen=True)
class Watermark:
    source_id: str
    cursor: str
    observed_at: datetime
    run_id: str
    visibility: Visibility = Visibility.PRIVATE

    def __post_init__(self) -> None:
        _require_text_fields(self, "source_id", "cursor", "run_id")
        _require_aware(self.observed_at, "observed_at")


@dataclass(frozen=True)
class CostEntry:
    id: str
    reservation_key: str
    provider: str
    operation: str
    amount_usd: Decimal
    status: CostStatus
    incurred_at: datetime
    run_id: str | None = None
    visibility: Visibility = Visibility.PRIVATE

    def __post_init__(self) -> None:
        _require_text_fields(self, "id", "reservation_key", "provider", "operation")
        amount = Decimal(self.amount_usd)
        if not amount.is_finite() or amount < 0:
            raise ValueError("amount_usd deve essere finito e non negativo")
        if amount.as_tuple().exponent < -6:
            raise ValueError("amount_usd supporta al massimo 6 decimali")
        if self.run_id is not None and not self.run_id.strip():
            raise ValueError("run_id non puo' essere vuoto")
        _require_aware(self.incurred_at, "incurred_at")
        if self.status is CostStatus.RELEASED and amount != 0:
            raise ValueError("Un costo released deve avere importo zero")


def canonicalize_url(url: str) -> str:
    raw = url.strip()
    parts = urlsplit(raw)
    if parts.scheme.lower() not in {"http", "https"} or not parts.hostname:
        raise ValueError(f"URL HTTP(S) non valido: {url!r}")
    scheme = parts.scheme.lower()
    host = parts.hostname.lower()
    port = parts.port
    if port and not ((scheme == "http" and port == 80) or (scheme == "https" and port == 443)):
        host = f"{host}:{port}"
    path = re.sub(r"/{2,}", "/", parts.path or "/")
    if path != "/":
        path = path.rstrip("/")
    query = []
    for key, value in parse_qsl(parts.query, keep_blank_values=True):
        lowered = key.lower()
        if lowered.startswith("utm_") or lowered in _TRACKING_PARAMETERS:
            continue
        query.append((key, value))
    query.sort()
    return urlunsplit((scheme, host, path, urlencode(query, doseq=True), ""))


def normalize_text(value: str) -> str:
    lowered = value.casefold()
    lowered = re.sub(r"[^\w\s]", " ", lowered, flags=re.UNICODE)
    return _WHITESPACE_RE.sub(" ", lowered).strip()


def stable_id(prefix: str, *parts: str) -> str:
    material = "\x1f".join(parts).encode("utf-8")
    return f"{prefix}_{hashlib.sha256(material).hexdigest()[:24]}"


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


def _clean_values(values: Iterable[str]) -> tuple[str, ...]:
    return tuple(dict.fromkeys(value.strip() for value in values if value.strip()))


def _require_http_url(value: str, name: str) -> None:
    parts = urlsplit(value)
    if parts.scheme.lower() not in {"http", "https"} or not parts.hostname:
        raise ValueError(f"{name} deve essere un URL HTTP(S)")


def _require_aware(value: datetime, name: str) -> None:
    if value.tzinfo is None or value.utcoffset() is None:
        raise ValueError(f"{name} deve includere il fuso orario")


def _require_unit_interval(value: float, name: str) -> None:
    if not 0.0 <= value <= 1.0:
        raise ValueError(f"{name} deve essere compreso tra 0 e 1")


def _require_unique_nonempty(values: tuple[str, ...], name: str) -> None:
    if any(not value.strip() for value in values):
        raise ValueError(f"{name} non puo' contenere valori vuoti")
    if len(values) != len(set(values)):
        raise ValueError(f"{name} non puo' contenere duplicati")


def _require_text_fields(instance: object, *names: str) -> None:
    for name in names:
        value = getattr(instance, name)
        if not isinstance(value, str) or not value.strip():
            raise ValueError(f"{name} e' obbligatorio")
