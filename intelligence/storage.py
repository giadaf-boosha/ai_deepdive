from __future__ import annotations

import json
import os
import sqlite3
from dataclasses import asdict, replace
from datetime import datetime
from decimal import Decimal, ROUND_HALF_UP
from pathlib import Path
from typing import Iterable

from .config import validate_private_data_dir
from .domain import (
    Application,
    Bridge,
    BridgeRelation,
    Claim,
    ClaimEvidence,
    ClaimType,
    Concept,
    CostEntry,
    CostStatus,
    DeliveryRecord,
    DeliveryStatus,
    Document,
    EditorialSignals,
    EvidenceRelation,
    Event,
    EventStatus,
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
    Visibility,
    VerificationStatus,
    Watermark,
    canonicalize_url,
)


SCHEMA_VERSION = 3


class StorageError(RuntimeError):
    """Raised when persistent state is invalid or unsafe."""


class IntelligenceStore:
    def __init__(self, *, data_dir: Path, public_repo_root: Path) -> None:
        self.data_dir = validate_private_data_dir(data_dir, public_repo_root)
        self.data_dir.mkdir(mode=0o700, parents=True, exist_ok=True)
        try:
            self.data_dir.chmod(0o700)
        except OSError:
            pass
        self.database_path = self.data_dir / "intelligence.sqlite3"
        self._connection = sqlite3.connect(self.database_path)
        self._connection.row_factory = sqlite3.Row
        self._connection.execute("PRAGMA foreign_keys = ON")
        self._connection.execute("PRAGMA journal_mode = WAL")
        self._connection.execute("PRAGMA synchronous = FULL")
        self._initialize_schema()
        try:
            os.chmod(self.database_path, 0o600)
        except OSError:
            pass

    def __enter__(self) -> IntelligenceStore:
        return self

    def __exit__(self, exc_type: object, exc: object, traceback: object) -> None:
        self.close()

    def close(self) -> None:
        self._connection.close()

    def save_document(self, document: Document) -> Document:
        existing = self.find_duplicate(document)
        if existing is not None and existing.id != document.id:
            return existing
        payload = _serialize_document(document)
        with self._connection:
            self._connection.execute(
                """
                INSERT INTO documents (
                    id, title, canonical_url, excerpt, content_fingerprint,
                    source_id, source_name, source_url, retrieved_at, published_at,
                    access_method, source_role, source_authority, is_official,
                    visibility, rights_status, rights_license_url, rights_attribution,
                    rights_public_use, lanes_json, authors_json, estimated_read_minutes
                ) VALUES (
                    :id, :title, :canonical_url, :excerpt, :content_fingerprint,
                    :source_id, :source_name, :source_url, :retrieved_at, :published_at,
                    :access_method, :source_role, :source_authority, :is_official,
                    :visibility, :rights_status, :rights_license_url, :rights_attribution,
                    :rights_public_use, :lanes_json, :authors_json, :estimated_read_minutes
                )
                ON CONFLICT(id) DO UPDATE SET
                    title=excluded.title,
                    excerpt=excluded.excerpt,
                    retrieved_at=excluded.retrieved_at,
                    published_at=excluded.published_at,
                    source_role=excluded.source_role,
                    source_authority=excluded.source_authority,
                    is_official=excluded.is_official,
                    visibility=excluded.visibility,
                    rights_status=excluded.rights_status,
                    rights_license_url=excluded.rights_license_url,
                    rights_attribution=excluded.rights_attribution,
                    rights_public_use=excluded.rights_public_use,
                    lanes_json=excluded.lanes_json,
                    authors_json=excluded.authors_json,
                    estimated_read_minutes=excluded.estimated_read_minutes
                """,
                payload,
            )
        return document

    def find_duplicate(self, document: Document) -> Document | None:
        row = self._connection.execute(
            """
            SELECT * FROM documents
            WHERE canonical_url = ? AND content_fingerprint = ?
            ORDER BY id LIMIT 1
            """,
            (canonicalize_url(document.canonical_url), document.content_fingerprint),
        ).fetchone()
        return _row_to_document(row) if row is not None else None

    def get_document(self, document_id: str) -> Document | None:
        row = self._connection.execute(
            "SELECT * FROM documents WHERE id = ?", (document_id,)
        ).fetchone()
        return _row_to_document(row) if row is not None else None

    def list_documents(self) -> tuple[Document, ...]:
        rows = self._connection.execute("SELECT * FROM documents ORDER BY id").fetchall()
        return tuple(_row_to_document(row) for row in rows)

    def save_event(self, event: Event) -> None:
        missing = [item for item in event.document_ids if self.get_document(item) is None]
        if missing:
            raise StorageError(f"Documenti evento mancanti: {', '.join(sorted(missing))}")
        payload = _serialize_event(event)
        with self._connection:
            self._connection.execute(
                """
                INSERT INTO events (
                    id, title, summary, primary_document_id, lanes_json,
                    first_seen, last_seen, visibility, rights_status,
                    rights_license_url, rights_attribution, rights_public_use,
                    novelty, impact, information_density, project_relevance,
                    bridge_potential, status
                ) VALUES (
                    :id, :title, :summary, :primary_document_id, :lanes_json,
                    :first_seen, :last_seen, :visibility, :rights_status,
                    :rights_license_url, :rights_attribution, :rights_public_use,
                    :novelty, :impact, :information_density, :project_relevance,
                    :bridge_potential, :status
                )
                ON CONFLICT(id) DO UPDATE SET
                    title=excluded.title,
                    summary=excluded.summary,
                    primary_document_id=excluded.primary_document_id,
                    lanes_json=excluded.lanes_json,
                    first_seen=excluded.first_seen,
                    last_seen=excluded.last_seen,
                    visibility=excluded.visibility,
                    rights_status=excluded.rights_status,
                    rights_license_url=excluded.rights_license_url,
                    rights_attribution=excluded.rights_attribution,
                    rights_public_use=excluded.rights_public_use,
                    novelty=excluded.novelty,
                    impact=excluded.impact,
                    information_density=excluded.information_density,
                    project_relevance=excluded.project_relevance,
                    bridge_potential=excluded.bridge_potential,
                    status=excluded.status
                """,
                payload,
            )
            self._connection.execute("DELETE FROM event_documents WHERE event_id = ?", (event.id,))
            self._connection.executemany(
                "INSERT INTO event_documents (event_id, document_id, relation_role) VALUES (?, ?, ?)",
                [
                    (
                        event.id,
                        document_id,
                        "primary" if document_id == event.primary_document_id else "supporting",
                    )
                    for document_id in event.document_ids
                ],
            )

    def get_event(self, event_id: str) -> Event | None:
        row = self._connection.execute("SELECT * FROM events WHERE id = ?", (event_id,)).fetchone()
        if row is None:
            return None
        return self._row_to_event(row)

    def list_events(self) -> tuple[Event, ...]:
        rows = self._connection.execute("SELECT * FROM events ORDER BY id").fetchall()
        return tuple(self._row_to_event(row) for row in rows)

    def documents_for_event(self, event_id: str) -> tuple[Document, ...]:
        rows = self._connection.execute(
            """
            SELECT d.* FROM documents AS d
            JOIN event_documents AS ed ON ed.document_id = d.id
            WHERE ed.event_id = ? ORDER BY d.id
            """,
            (event_id,),
        ).fetchall()
        return tuple(_row_to_document(row) for row in rows)

    def save_claim(self, record: Claim) -> None:
        self._upsert_payload(
            "claims",
            record.id,
            record.visibility,
            record,
            {"event_id": record.event_id},
        )

    def get_claim(self, record_id: str) -> Claim | None:
        return self._get_payload("claims", record_id, _claim_from_payload)

    def list_claims(self) -> tuple[Claim, ...]:
        return self._list_payloads("claims", _claim_from_payload)

    def save_claim_evidence(self, record: ClaimEvidence) -> None:
        self._upsert_payload(
            "claim_evidence",
            record.id,
            record.visibility,
            record,
            {"claim_id": record.claim_id, "document_id": record.document_id},
        )

    def get_claim_evidence(self, record_id: str) -> ClaimEvidence | None:
        return self._get_payload("claim_evidence", record_id, _claim_evidence_from_payload)

    def list_claim_evidence(self) -> tuple[ClaimEvidence, ...]:
        return self._list_payloads("claim_evidence", _claim_evidence_from_payload)

    def save_concept(self, record: Concept) -> None:
        self._upsert_payload("concepts", record.id, record.visibility, record)

    def get_concept(self, record_id: str) -> Concept | None:
        return self._get_payload("concepts", record_id, _concept_from_payload)

    def list_concepts(self) -> tuple[Concept, ...]:
        return self._list_payloads("concepts", _concept_from_payload)

    def save_bridge(self, record: Bridge) -> None:
        self._require_claim_ids(record.supporting_claim_ids + record.opposing_claim_ids)
        self._upsert_payload(
            "bridges",
            record.id,
            record.visibility,
            record,
            {
                "from_concept_id": record.from_concept_id,
                "to_concept_id": record.to_concept_id,
            },
        )

    def get_bridge(self, record_id: str) -> Bridge | None:
        return self._get_payload("bridges", record_id, _bridge_from_payload)

    def list_bridges(self) -> tuple[Bridge, ...]:
        return self._list_payloads("bridges", _bridge_from_payload)

    def save_reading_decision(self, record: ReadingDecision) -> None:
        self._upsert_payload(
            "reading_decisions",
            record.id,
            record.visibility,
            record,
            {"event_id": record.event_id, "document_id": record.document_id},
        )

    def get_reading_decision(self, record_id: str) -> ReadingDecision | None:
        return self._get_payload("reading_decisions", record_id, _reading_decision_from_payload)

    def list_reading_decisions(self) -> tuple[ReadingDecision, ...]:
        return self._list_payloads("reading_decisions", _reading_decision_from_payload)

    def save_reading_note(self, record: ReadingNote) -> None:
        self._upsert_payload(
            "reading_notes",
            record.id,
            record.visibility,
            record,
            {"decision_id": record.decision_id},
        )

    def get_reading_note(self, record_id: str) -> ReadingNote | None:
        return self._get_payload("reading_notes", record_id, _reading_note_from_payload)

    def list_reading_notes(self) -> tuple[ReadingNote, ...]:
        return self._list_payloads("reading_notes", _reading_note_from_payload)

    def save_application(self, record: Application) -> None:
        self._require_claim_ids(record.evidence_claim_ids)
        self._upsert_payload("applications", record.id, record.visibility, record)

    def get_application(self, record_id: str) -> Application | None:
        return self._get_payload("applications", record_id, _application_from_payload)

    def list_applications(self) -> tuple[Application, ...]:
        return self._list_payloads("applications", _application_from_payload)

    def save_thesis(self, record: Thesis) -> None:
        self._require_claim_ids(record.supporting_claim_ids + record.opposing_claim_ids)
        self._upsert_payload("theses", record.id, record.visibility, record)

    def get_thesis(self, record_id: str) -> Thesis | None:
        return self._get_payload("theses", record_id, _thesis_from_payload)

    def list_theses(self) -> tuple[Thesis, ...]:
        return self._list_payloads("theses", _thesis_from_payload)

    def save_output(self, record: OutputRecord) -> None:
        self._upsert_payload(
            "outputs",
            record.id,
            record.visibility,
            record,
            {"thesis_id": record.thesis_id},
        )

    def get_output(self, record_id: str) -> OutputRecord | None:
        return self._get_payload("outputs", record_id, _output_from_payload)

    def list_outputs(self) -> tuple[OutputRecord, ...]:
        return self._list_payloads("outputs", _output_from_payload)

    def save_rights_record(self, record: RightsRecord) -> None:
        self._upsert_payload(
            "rights_records",
            record.id,
            record.visibility,
            record,
            {"resource_kind": record.resource_kind, "resource_id": record.resource_id},
        )

    def get_rights_record(self, record_id: str) -> RightsRecord | None:
        return self._get_payload("rights_records", record_id, _rights_record_from_payload)

    def list_rights_records(self) -> tuple[RightsRecord, ...]:
        return self._list_payloads("rights_records", _rights_record_from_payload)

    def save_run(self, record: RunRecord) -> None:
        self._upsert_payload("runs", record.id, record.visibility, record)

    def get_run(self, record_id: str) -> RunRecord | None:
        return self._get_payload("runs", record_id, _run_from_payload)

    def list_runs(self) -> tuple[RunRecord, ...]:
        return self._list_payloads("runs", _run_from_payload)

    def save_delivery(self, record: DeliveryRecord) -> DeliveryRecord:
        existing = self._connection.execute(
            "SELECT payload_json FROM deliveries WHERE idempotency_key = ?",
            (record.idempotency_key,),
        ).fetchone()
        if existing is not None:
            existing_record = _delivery_from_payload(json.loads(existing["payload_json"]))
            if existing_record.id != record.id:
                return existing_record
        self._upsert_payload(
            "deliveries",
            record.id,
            record.visibility,
            record,
            {
                "run_id": record.run_id,
                "idempotency_key": record.idempotency_key,
            },
        )
        return record

    def reserve_delivery(self, record: DeliveryRecord) -> DeliveryRecord | None:
        """Atomically acquire a send slot before SMTP; failed attempts are retryable."""
        if record.status is not DeliveryStatus.PENDING:
            raise ValueError("reserve_delivery richiede una DeliveryRecord PENDING")
        self._connection.execute("BEGIN IMMEDIATE")
        try:
            row = self._connection.execute(
                "SELECT payload_json FROM deliveries WHERE idempotency_key = ?",
                (record.idempotency_key,),
            ).fetchone()
            if row is not None:
                existing = _delivery_from_payload(json.loads(row["payload_json"]))
                if existing.status is not DeliveryStatus.FAILED:
                    self._connection.rollback()
                    return None
                acquired = replace(
                    record,
                    id=existing.id,
                    created_at=record.created_at,
                    delivered_at=None,
                    error=None,
                )
                self._connection.execute(
                    """
                    UPDATE deliveries
                    SET run_id = ?, visibility = ?, payload_json = ?
                    WHERE idempotency_key = ?
                    """,
                    (
                        acquired.run_id,
                        acquired.visibility.value,
                        _record_json(acquired),
                        acquired.idempotency_key,
                    ),
                )
            else:
                acquired = record
                self._connection.execute(
                    """
                    INSERT INTO deliveries
                        (id, run_id, idempotency_key, visibility, payload_json)
                    VALUES (?, ?, ?, ?, ?)
                    """,
                    (
                        acquired.id,
                        acquired.run_id,
                        acquired.idempotency_key,
                        acquired.visibility.value,
                        _record_json(acquired),
                    ),
                )
            self._connection.commit()
            return acquired
        except Exception:
            self._connection.rollback()
            raise

    def get_delivery(self, record_id: str) -> DeliveryRecord | None:
        return self._get_payload("deliveries", record_id, _delivery_from_payload)

    def list_deliveries(self) -> tuple[DeliveryRecord, ...]:
        return self._list_payloads("deliveries", _delivery_from_payload)

    def reserve_cost(self, record: CostEntry, *, monthly_budget_usd: Decimal | str | float) -> bool:
        """Reserve estimated spend atomically without ever crossing the monthly cap."""
        if record.status is not CostStatus.RESERVED:
            raise ValueError("reserve_cost richiede una CostEntry RESERVED")
        amount_micros = _usd_to_micros(record.amount_usd)
        budget_micros = _usd_to_micros(monthly_budget_usd)
        month_key = _month_key(record.incurred_at)
        self._connection.execute("BEGIN IMMEDIATE")
        try:
            duplicate = self._connection.execute(
                "SELECT 1 FROM cost_entries WHERE reservation_key = ?",
                (record.reservation_key,),
            ).fetchone()
            if duplicate is not None:
                self._connection.rollback()
                return False
            current = self._connection.execute(
                """
                SELECT COALESCE(SUM(amount_micros), 0) AS total
                FROM cost_entries
                WHERE month_key = ? AND status IN ('reserved', 'settled')
                """,
                (month_key,),
            ).fetchone()["total"]
            if current + amount_micros > budget_micros:
                self._connection.rollback()
                return False
            self._connection.execute(
                """
                INSERT INTO cost_entries (
                    id, reservation_key, run_id, provider, operation, month_key,
                    amount_micros, status, incurred_at, visibility, payload_json
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    record.id,
                    record.reservation_key,
                    record.run_id,
                    record.provider,
                    record.operation,
                    month_key,
                    amount_micros,
                    record.status.value,
                    record.incurred_at.isoformat(),
                    record.visibility.value,
                    _record_json(record),
                ),
            )
            self._connection.commit()
            return True
        except Exception:
            self._connection.rollback()
            raise

    def reconcile_cost(
        self,
        reservation_key: str,
        *,
        actual_amount_usd: Decimal | str | float,
        status: CostStatus = CostStatus.SETTLED,
    ) -> CostEntry:
        if status not in {CostStatus.SETTLED, CostStatus.RELEASED}:
            raise ValueError("reconcile_cost accetta solo SETTLED o RELEASED")
        actual = Decimal("0") if status is CostStatus.RELEASED else _as_usd(actual_amount_usd)
        amount_micros = _usd_to_micros(actual)
        self._connection.execute("BEGIN IMMEDIATE")
        try:
            row = self._connection.execute(
                "SELECT payload_json FROM cost_entries WHERE reservation_key = ?",
                (reservation_key,),
            ).fetchone()
            if row is None:
                raise StorageError(f"Reservation costi non trovata: {reservation_key}")
            existing = _cost_entry_from_payload(json.loads(row["payload_json"]))
            reconciled = replace(existing, amount_usd=actual, status=status)
            if reconciled == existing:
                self._connection.commit()
                return existing
            self._connection.execute(
                """
                UPDATE cost_entries
                SET amount_micros = ?, status = ?, visibility = ?, payload_json = ?
                WHERE reservation_key = ?
                """,
                (
                    amount_micros,
                    status.value,
                    reconciled.visibility.value,
                    _record_json(reconciled),
                    reservation_key,
                ),
            )
            self._connection.commit()
            return reconciled
        except Exception:
            self._connection.rollback()
            raise

    def get_cost_entry(self, record_id: str) -> CostEntry | None:
        row = self._connection.execute(
            "SELECT payload_json FROM cost_entries WHERE id = ?", (record_id,)
        ).fetchone()
        return _cost_entry_from_payload(json.loads(row["payload_json"])) if row else None

    def list_cost_entries(self) -> tuple[CostEntry, ...]:
        rows = self._connection.execute(
            "SELECT payload_json FROM cost_entries ORDER BY id"
        ).fetchall()
        return tuple(_cost_entry_from_payload(json.loads(row["payload_json"])) for row in rows)

    def monthly_cost(self, year: int, month: int, *, include_reserved: bool = True) -> Decimal:
        if not 1 <= month <= 12:
            raise ValueError("month deve essere tra 1 e 12")
        statuses = ("reserved", "settled") if include_reserved else ("settled",)
        placeholders = ",".join("?" for _ in statuses)
        row = self._connection.execute(
            f"""
            SELECT COALESCE(SUM(amount_micros), 0) AS total
            FROM cost_entries
            WHERE month_key = ? AND status IN ({placeholders})
            """,
            (f"{year:04d}-{month:02d}", *statuses),
        ).fetchone()
        return Decimal(row["total"]) / Decimal(1_000_000)

    def save_watermark(self, record: Watermark) -> Watermark:
        current = self.get_watermark(record.source_id)
        if current is not None and record.observed_at < current.observed_at:
            return current
        payload = _record_json(record)
        with self._connection:
            self._connection.execute(
                """
                INSERT INTO watermarks (source_id, run_id, observed_at, visibility, payload_json)
                VALUES (?, ?, ?, ?, ?)
                ON CONFLICT(source_id) DO UPDATE SET
                    run_id=excluded.run_id,
                    observed_at=excluded.observed_at,
                    visibility=excluded.visibility,
                    payload_json=excluded.payload_json
                """,
                (
                    record.source_id,
                    record.run_id,
                    record.observed_at.isoformat(),
                    record.visibility.value,
                    payload,
                ),
            )
        return record

    def get_watermark(self, source_id: str) -> Watermark | None:
        row = self._connection.execute(
            "SELECT payload_json FROM watermarks WHERE source_id = ?", (source_id,)
        ).fetchone()
        return _watermark_from_payload(json.loads(row["payload_json"])) if row else None

    def list_watermarks(self) -> tuple[Watermark, ...]:
        rows = self._connection.execute(
            "SELECT payload_json FROM watermarks ORDER BY source_id"
        ).fetchall()
        return tuple(_watermark_from_payload(json.loads(row["payload_json"])) for row in rows)

    def _upsert_payload(
        self,
        table: str,
        record_id: str,
        visibility: Visibility,
        record: object,
        extra: dict[str, object] | None = None,
    ) -> None:
        allowed = {
            "claims",
            "claim_evidence",
            "concepts",
            "bridges",
            "reading_decisions",
            "reading_notes",
            "applications",
            "theses",
            "outputs",
            "rights_records",
            "runs",
            "deliveries",
        }
        if table not in allowed:
            raise StorageError(f"Tabella payload non consentita: {table}")
        columns = {"id": record_id, "visibility": visibility.value, "payload_json": _record_json(record)}
        columns.update(extra or {})
        names = tuple(columns)
        placeholders = ", ".join("?" for _ in names)
        assignments = ", ".join(f"{name}=excluded.{name}" for name in names if name != "id")
        sql = (
            f"INSERT INTO {table} ({', '.join(names)}) VALUES ({placeholders}) "
            f"ON CONFLICT(id) DO UPDATE SET {assignments}"
        )
        with self._connection:
            self._connection.execute(sql, tuple(columns[name] for name in names))

    def _get_payload(self, table: str, record_id: str, decoder):
        row = self._connection.execute(
            f"SELECT payload_json FROM {table} WHERE id = ?", (record_id,)
        ).fetchone()
        return decoder(json.loads(row["payload_json"])) if row else None

    def _list_payloads(self, table: str, decoder) -> tuple[object, ...]:
        rows = self._connection.execute(
            f"SELECT payload_json FROM {table} ORDER BY id"
        ).fetchall()
        return tuple(decoder(json.loads(row["payload_json"])) for row in rows)

    def _require_claim_ids(self, claim_ids: Iterable[str]) -> None:
        missing = [claim_id for claim_id in claim_ids if self.get_claim(claim_id) is None]
        if missing:
            raise StorageError(f"Claim mancanti: {', '.join(sorted(missing))}")

    def _row_to_event(self, row: sqlite3.Row) -> Event:
        ids = tuple(
            item["document_id"]
            for item in self._connection.execute(
                "SELECT document_id FROM event_documents WHERE event_id = ? ORDER BY document_id",
                (row["id"],),
            ).fetchall()
        )
        return Event(
            id=row["id"],
            title=row["title"],
            summary=row["summary"],
            document_ids=ids,
            primary_document_id=row["primary_document_id"],
            lanes=tuple(json.loads(row["lanes_json"])),
            first_seen=datetime.fromisoformat(row["first_seen"]),
            last_seen=datetime.fromisoformat(row["last_seen"]),
            visibility=Visibility(row["visibility"]),
            rights=Rights(
                RightsStatus(row["rights_status"]),
                row["rights_license_url"],
                row["rights_attribution"],
                row["rights_public_use"],
            ),
            signals=EditorialSignals(
                novelty=row["novelty"],
                impact=row["impact"],
                information_density=row["information_density"],
                project_relevance=row["project_relevance"],
                bridge_potential=row["bridge_potential"],
            ),
            status=EventStatus(row["status"]),
        )

    def _initialize_schema(self) -> None:
        current = self._connection.execute("PRAGMA user_version").fetchone()[0]
        if current not in {0, 1, 2, SCHEMA_VERSION}:
            raise StorageError(
                f"Schema SQLite {current} non supportato; atteso {SCHEMA_VERSION}"
            )
        self._connection.executescript(
            """
            CREATE TABLE IF NOT EXISTS documents (
                id TEXT PRIMARY KEY,
                title TEXT NOT NULL,
                canonical_url TEXT NOT NULL UNIQUE,
                excerpt TEXT NOT NULL,
                content_fingerprint TEXT NOT NULL UNIQUE,
                source_id TEXT NOT NULL,
                source_name TEXT NOT NULL,
                source_url TEXT NOT NULL,
                retrieved_at TEXT NOT NULL,
                published_at TEXT,
                access_method TEXT NOT NULL,
                source_role TEXT NOT NULL,
                source_authority REAL NOT NULL CHECK(source_authority BETWEEN 0 AND 1),
                is_official INTEGER NOT NULL CHECK(is_official IN (0, 1)),
                visibility TEXT NOT NULL,
                rights_status TEXT NOT NULL,
                rights_license_url TEXT,
                rights_attribution TEXT,
                rights_public_use TEXT NOT NULL,
                lanes_json TEXT NOT NULL,
                authors_json TEXT NOT NULL,
                estimated_read_minutes INTEGER NOT NULL CHECK(estimated_read_minutes >= 0)
            );

            CREATE TABLE IF NOT EXISTS events (
                id TEXT PRIMARY KEY,
                title TEXT NOT NULL,
                summary TEXT NOT NULL,
                primary_document_id TEXT NOT NULL REFERENCES documents(id),
                lanes_json TEXT NOT NULL,
                first_seen TEXT NOT NULL,
                last_seen TEXT NOT NULL,
                visibility TEXT NOT NULL,
                rights_status TEXT NOT NULL,
                rights_license_url TEXT,
                rights_attribution TEXT,
                rights_public_use TEXT NOT NULL,
                novelty REAL NOT NULL CHECK(novelty BETWEEN 0 AND 1),
                impact REAL NOT NULL CHECK(impact BETWEEN 0 AND 1),
                information_density REAL NOT NULL CHECK(information_density BETWEEN 0 AND 1),
                project_relevance REAL NOT NULL CHECK(project_relevance BETWEEN 0 AND 1),
                bridge_potential REAL NOT NULL CHECK(bridge_potential BETWEEN 0 AND 1),
                status TEXT NOT NULL
            );

            CREATE TABLE IF NOT EXISTS event_documents (
                event_id TEXT NOT NULL REFERENCES events(id) ON DELETE CASCADE,
                document_id TEXT NOT NULL REFERENCES documents(id),
                relation_role TEXT NOT NULL,
                PRIMARY KEY(event_id, document_id)
            );

            CREATE INDEX IF NOT EXISTS idx_documents_source ON documents(source_id);
            CREATE INDEX IF NOT EXISTS idx_documents_retrieved ON documents(retrieved_at);
            CREATE INDEX IF NOT EXISTS idx_events_last_seen ON events(last_seen);
            """
        )
        if current < 2:
            self._connection.executescript(
                """
                CREATE TABLE IF NOT EXISTS claims (
                    id TEXT PRIMARY KEY,
                    event_id TEXT NOT NULL REFERENCES events(id) ON DELETE CASCADE,
                    visibility TEXT NOT NULL,
                    payload_json TEXT NOT NULL
                );
                CREATE TABLE IF NOT EXISTS claim_evidence (
                    id TEXT PRIMARY KEY,
                    claim_id TEXT NOT NULL REFERENCES claims(id) ON DELETE CASCADE,
                    document_id TEXT NOT NULL REFERENCES documents(id),
                    visibility TEXT NOT NULL,
                    payload_json TEXT NOT NULL
                );
                CREATE TABLE IF NOT EXISTS concepts (
                    id TEXT PRIMARY KEY,
                    visibility TEXT NOT NULL,
                    payload_json TEXT NOT NULL
                );
                CREATE TABLE IF NOT EXISTS bridges (
                    id TEXT PRIMARY KEY,
                    from_concept_id TEXT NOT NULL REFERENCES concepts(id),
                    to_concept_id TEXT NOT NULL REFERENCES concepts(id),
                    visibility TEXT NOT NULL,
                    payload_json TEXT NOT NULL
                );
                CREATE TABLE IF NOT EXISTS reading_decisions (
                    id TEXT PRIMARY KEY,
                    event_id TEXT NOT NULL REFERENCES events(id) ON DELETE CASCADE,
                    document_id TEXT NOT NULL REFERENCES documents(id),
                    visibility TEXT NOT NULL,
                    payload_json TEXT NOT NULL
                );
                CREATE TABLE IF NOT EXISTS reading_notes (
                    id TEXT PRIMARY KEY,
                    decision_id TEXT NOT NULL REFERENCES reading_decisions(id) ON DELETE CASCADE,
                    visibility TEXT NOT NULL,
                    payload_json TEXT NOT NULL
                );
                CREATE TABLE IF NOT EXISTS applications (
                    id TEXT PRIMARY KEY,
                    visibility TEXT NOT NULL,
                    payload_json TEXT NOT NULL
                );
                CREATE TABLE IF NOT EXISTS theses (
                    id TEXT PRIMARY KEY,
                    visibility TEXT NOT NULL,
                    payload_json TEXT NOT NULL
                );
                CREATE TABLE IF NOT EXISTS outputs (
                    id TEXT PRIMARY KEY,
                    thesis_id TEXT REFERENCES theses(id),
                    visibility TEXT NOT NULL,
                    payload_json TEXT NOT NULL
                );
                CREATE TABLE IF NOT EXISTS rights_records (
                    id TEXT PRIMARY KEY,
                    resource_kind TEXT NOT NULL,
                    resource_id TEXT NOT NULL,
                    visibility TEXT NOT NULL,
                    payload_json TEXT NOT NULL,
                    UNIQUE(resource_kind, resource_id)
                );
                CREATE TABLE IF NOT EXISTS runs (
                    id TEXT PRIMARY KEY,
                    visibility TEXT NOT NULL,
                    payload_json TEXT NOT NULL
                );
                CREATE TABLE IF NOT EXISTS deliveries (
                    id TEXT PRIMARY KEY,
                    run_id TEXT NOT NULL REFERENCES runs(id) ON DELETE CASCADE,
                    idempotency_key TEXT NOT NULL UNIQUE,
                    visibility TEXT NOT NULL,
                    payload_json TEXT NOT NULL
                );
                CREATE TABLE IF NOT EXISTS watermarks (
                    source_id TEXT PRIMARY KEY,
                    run_id TEXT NOT NULL REFERENCES runs(id),
                    observed_at TEXT NOT NULL,
                    visibility TEXT NOT NULL,
                    payload_json TEXT NOT NULL
                );
                CREATE INDEX IF NOT EXISTS idx_claims_event ON claims(event_id);
                CREATE INDEX IF NOT EXISTS idx_reading_decisions_event ON reading_decisions(event_id);
                CREATE INDEX IF NOT EXISTS idx_deliveries_run ON deliveries(run_id);
                """
            )
            self._connection.execute("PRAGMA user_version = 2")
        self._connection.commit()
        if current < 3:
            self._migrate_to_v3()

    def _migrate_to_v3(self) -> None:
        """Replace independent uniqueness constraints with exact-revision identity."""
        self._connection.commit()
        self._connection.execute("PRAGMA foreign_keys = OFF")
        try:
            self._connection.executescript(
                """
                BEGIN IMMEDIATE;
                CREATE TABLE documents_v3 (
                    id TEXT PRIMARY KEY,
                    title TEXT NOT NULL,
                    canonical_url TEXT NOT NULL,
                    excerpt TEXT NOT NULL,
                    content_fingerprint TEXT NOT NULL,
                    source_id TEXT NOT NULL,
                    source_name TEXT NOT NULL,
                    source_url TEXT NOT NULL,
                    retrieved_at TEXT NOT NULL,
                    published_at TEXT,
                    access_method TEXT NOT NULL,
                    source_role TEXT NOT NULL,
                    source_authority REAL NOT NULL CHECK(source_authority BETWEEN 0 AND 1),
                    is_official INTEGER NOT NULL CHECK(is_official IN (0, 1)),
                    visibility TEXT NOT NULL,
                    rights_status TEXT NOT NULL,
                    rights_license_url TEXT,
                    rights_attribution TEXT,
                    rights_public_use TEXT NOT NULL,
                    lanes_json TEXT NOT NULL,
                    authors_json TEXT NOT NULL,
                    estimated_read_minutes INTEGER NOT NULL CHECK(estimated_read_minutes >= 0),
                    UNIQUE(canonical_url, content_fingerprint)
                );
                INSERT INTO documents_v3 SELECT * FROM documents;
                DROP TABLE documents;
                ALTER TABLE documents_v3 RENAME TO documents;
                CREATE INDEX idx_documents_source ON documents(source_id);
                CREATE INDEX idx_documents_retrieved ON documents(retrieved_at);

                CREATE TABLE IF NOT EXISTS cost_entries (
                    id TEXT PRIMARY KEY,
                    reservation_key TEXT NOT NULL UNIQUE,
                    run_id TEXT REFERENCES runs(id),
                    provider TEXT NOT NULL,
                    operation TEXT NOT NULL,
                    month_key TEXT NOT NULL,
                    amount_micros INTEGER NOT NULL CHECK(amount_micros >= 0),
                    status TEXT NOT NULL,
                    incurred_at TEXT NOT NULL,
                    visibility TEXT NOT NULL,
                    payload_json TEXT NOT NULL
                );
                CREATE INDEX IF NOT EXISTS idx_cost_entries_month ON cost_entries(month_key, status);
                PRAGMA user_version = 3;
                COMMIT;
                """
            )
        except Exception:
            if self._connection.in_transaction:
                self._connection.rollback()
            raise
        finally:
            self._connection.execute("PRAGMA foreign_keys = ON")
        violations = self._connection.execute("PRAGMA foreign_key_check").fetchall()
        if violations:
            raise StorageError(f"Migrazione v3 ha prodotto FK non valide: {violations!r}")


def _serialize_document(document: Document) -> dict[str, object]:
    return {
        "id": document.id,
        "title": document.title,
        "canonical_url": canonicalize_url(document.canonical_url),
        "excerpt": document.excerpt,
        "content_fingerprint": document.content_fingerprint,
        "source_id": document.provenance.source_id,
        "source_name": document.provenance.source_name,
        "source_url": document.provenance.source_url,
        "retrieved_at": document.provenance.retrieved_at.isoformat(),
        "published_at": (
            document.provenance.published_at.isoformat()
            if document.provenance.published_at is not None
            else None
        ),
        "access_method": document.provenance.access_method,
        "source_role": document.provenance.role.value,
        "source_authority": document.provenance.authority,
        "is_official": int(document.provenance.is_official),
        "visibility": document.visibility.value,
        "rights_status": document.rights.status.value,
        "rights_license_url": document.rights.license_url,
        "rights_attribution": document.rights.attribution,
        "rights_public_use": document.rights.public_use,
        "lanes_json": json.dumps(document.lanes, ensure_ascii=False),
        "authors_json": json.dumps(document.authors, ensure_ascii=False),
        "estimated_read_minutes": document.estimated_read_minutes,
    }


def _serialize_event(event: Event) -> dict[str, object]:
    payload = asdict(event.signals)
    payload.update(
        {
            "id": event.id,
            "title": event.title,
            "summary": event.summary,
            "primary_document_id": event.primary_document_id,
            "lanes_json": json.dumps(event.lanes, ensure_ascii=False),
            "first_seen": event.first_seen.isoformat(),
            "last_seen": event.last_seen.isoformat(),
            "visibility": event.visibility.value,
            "rights_status": event.rights.status.value,
            "rights_license_url": event.rights.license_url,
            "rights_attribution": event.rights.attribution,
            "rights_public_use": event.rights.public_use,
            "status": event.status.value,
        }
    )
    return payload


def _row_to_document(row: sqlite3.Row) -> Document:
    return Document(
        id=row["id"],
        title=row["title"],
        canonical_url=row["canonical_url"],
        excerpt=row["excerpt"],
        provenance=Provenance(
            source_id=row["source_id"],
            source_name=row["source_name"],
            source_url=row["source_url"],
            retrieved_at=datetime.fromisoformat(row["retrieved_at"]),
            published_at=(
                datetime.fromisoformat(row["published_at"]) if row["published_at"] else None
            ),
            access_method=row["access_method"],
            role=SourceRole(row["source_role"]),
            authority=row["source_authority"],
            is_official=bool(row["is_official"]),
        ),
        visibility=Visibility(row["visibility"]),
        rights=Rights(
            RightsStatus(row["rights_status"]),
            row["rights_license_url"],
            row["rights_attribution"],
            row["rights_public_use"],
        ),
        content_fingerprint=row["content_fingerprint"],
        lanes=tuple(json.loads(row["lanes_json"])),
        authors=tuple(json.loads(row["authors_json"])),
        estimated_read_minutes=row["estimated_read_minutes"],
    )


def _record_json(record: object) -> str:
    return json.dumps(
        asdict(record),
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
        default=lambda value: value.isoformat() if isinstance(value, datetime) else str(value),
    )


def _datetime(value: str | None) -> datetime | None:
    return datetime.fromisoformat(value) if value is not None else None


def _claim_from_payload(data: dict[str, object]) -> Claim:
    return Claim(
        id=str(data["id"]),
        event_id=str(data["event_id"]),
        text=str(data["text"]),
        claim_type=ClaimType(str(data["claim_type"])),
        confidence=float(data["confidence"]),
        verification=VerificationStatus(str(data["verification"])),
        visibility=Visibility(str(data["visibility"])),
        created_at=datetime.fromisoformat(str(data["created_at"])),
    )


def _claim_evidence_from_payload(data: dict[str, object]) -> ClaimEvidence:
    return ClaimEvidence(
        id=str(data["id"]),
        claim_id=str(data["claim_id"]),
        document_id=str(data["document_id"]),
        relation=EvidenceRelation(str(data["relation"])),
        locator=str(data["locator"]),
        excerpt=str(data["excerpt"]),
        visibility=Visibility(str(data["visibility"])),
    )


def _concept_from_payload(data: dict[str, object]) -> Concept:
    return Concept(
        id=str(data["id"]),
        name=str(data["name"]),
        definition=str(data["definition"]),
        domains=tuple(str(value) for value in data["domains"]),
        maturity=KnowledgeMaturity(str(data["maturity"])),
        visibility=Visibility(str(data["visibility"])),
        created_at=datetime.fromisoformat(str(data["created_at"])),
        last_reviewed_at=_datetime(data.get("last_reviewed_at")),
    )


def _bridge_from_payload(data: dict[str, object]) -> Bridge:
    return Bridge(
        id=str(data["id"]),
        from_concept_id=str(data["from_concept_id"]),
        to_concept_id=str(data["to_concept_id"]),
        relation=BridgeRelation(str(data["relation"])),
        statement=str(data["statement"]),
        mechanism=str(data["mechanism"]),
        supporting_claim_ids=tuple(str(value) for value in data["supporting_claim_ids"]),
        opposing_claim_ids=tuple(str(value) for value in data["opposing_claim_ids"]),
        risk_of_analogy=float(data["risk_of_analogy"]),
        novelty=float(data["novelty"]),
        usefulness=float(data["usefulness"]),
        maturity=KnowledgeMaturity(str(data["maturity"])),
        visibility=Visibility(str(data["visibility"])),
    )


def _reading_decision_from_payload(data: dict[str, object]) -> ReadingDecision:
    return ReadingDecision(
        id=str(data["id"]),
        event_id=str(data["event_id"]),
        document_id=str(data["document_id"]),
        disposition=ReadingDisposition(str(data["disposition"])),
        reason=str(data["reason"]),
        estimated_minutes=int(data["estimated_minutes"]),
        priority=float(data["priority"]),
        visibility=Visibility(str(data["visibility"])),
        created_at=datetime.fromisoformat(str(data["created_at"])),
    )


def _reading_note_from_payload(data: dict[str, object]) -> ReadingNote:
    return ReadingNote(
        id=str(data["id"]),
        decision_id=str(data["decision_id"]),
        summary=str(data["summary"]),
        insights=tuple(str(value) for value in data["insights"]),
        questions=tuple(str(value) for value in data["questions"]),
        visibility=Visibility(str(data["visibility"])),
        completed_at=datetime.fromisoformat(str(data["completed_at"])),
    )


def _application_from_payload(data: dict[str, object]) -> Application:
    return Application(
        id=str(data["id"]),
        target=str(data["target"]),
        statement=str(data["statement"]),
        evidence_claim_ids=tuple(str(value) for value in data["evidence_claim_ids"]),
        maturity=KnowledgeMaturity(str(data["maturity"])),
        visibility=Visibility(str(data["visibility"])),
        created_at=datetime.fromisoformat(str(data["created_at"])),
    )


def _thesis_from_payload(data: dict[str, object]) -> Thesis:
    return Thesis(
        id=str(data["id"]),
        statement=str(data["statement"]),
        counterargument=str(data["counterargument"]),
        supporting_claim_ids=tuple(str(value) for value in data["supporting_claim_ids"]),
        opposing_claim_ids=tuple(str(value) for value in data["opposing_claim_ids"]),
        maturity=KnowledgeMaturity(str(data["maturity"])),
        visibility=Visibility(str(data["visibility"])),
        created_at=datetime.fromisoformat(str(data["created_at"])),
        updated_at=datetime.fromisoformat(str(data["updated_at"])),
    )


def _output_from_payload(data: dict[str, object]) -> OutputRecord:
    return OutputRecord(
        id=str(data["id"]),
        output_type=str(data["output_type"]),
        title=str(data["title"]),
        audience=str(data["audience"]),
        thesis_id=str(data["thesis_id"]) if data.get("thesis_id") is not None else None,
        status=OutputStatus(str(data["status"])),
        rights_reviewed=bool(data["rights_reviewed"]),
        fact_reviewed=bool(data["fact_reviewed"]),
        visibility=Visibility(str(data["visibility"])),
        created_at=datetime.fromisoformat(str(data["created_at"])),
        updated_at=datetime.fromisoformat(str(data["updated_at"])),
    )


def _rights_record_from_payload(data: dict[str, object]) -> RightsRecord:
    raw = data["rights"]
    if not isinstance(raw, dict):
        raise StorageError("Payload RightsRecord non valido")
    return RightsRecord(
        id=str(data["id"]),
        resource_kind=str(data["resource_kind"]),
        resource_id=str(data["resource_id"]),
        rights=Rights(
            status=RightsStatus(str(raw["status"])),
            license_url=str(raw["license_url"]) if raw.get("license_url") is not None else None,
            attribution=str(raw["attribution"]) if raw.get("attribution") is not None else None,
            public_use=str(raw["public_use"]),
        ),
        source_url=str(data["source_url"]),
        visibility=Visibility(str(data["visibility"])),
        reviewed_at=datetime.fromisoformat(str(data["reviewed_at"])),
    )


def _run_from_payload(data: dict[str, object]) -> RunRecord:
    return RunRecord(
        id=str(data["id"]),
        kind=str(data["kind"]),
        started_at=datetime.fromisoformat(str(data["started_at"])),
        status=RunStatus(str(data["status"])),
        completed_at=_datetime(data.get("completed_at")),
        error=str(data["error"]) if data.get("error") is not None else None,
        visibility=Visibility(str(data["visibility"])),
    )


def _delivery_from_payload(data: dict[str, object]) -> DeliveryRecord:
    return DeliveryRecord(
        id=str(data["id"]),
        run_id=str(data["run_id"]),
        channel=str(data["channel"]),
        recipient=str(data["recipient"]),
        status=DeliveryStatus(str(data["status"])),
        idempotency_key=str(data["idempotency_key"]),
        created_at=datetime.fromisoformat(str(data["created_at"])),
        delivered_at=_datetime(data.get("delivered_at")),
        error=str(data["error"]) if data.get("error") is not None else None,
        visibility=Visibility(str(data["visibility"])),
    )


def _watermark_from_payload(data: dict[str, object]) -> Watermark:
    return Watermark(
        source_id=str(data["source_id"]),
        cursor=str(data["cursor"]),
        observed_at=datetime.fromisoformat(str(data["observed_at"])),
        run_id=str(data["run_id"]),
        visibility=Visibility(str(data["visibility"])),
    )


def _cost_entry_from_payload(data: dict[str, object]) -> CostEntry:
    return CostEntry(
        id=str(data["id"]),
        reservation_key=str(data["reservation_key"]),
        provider=str(data["provider"]),
        operation=str(data["operation"]),
        amount_usd=Decimal(str(data["amount_usd"])),
        status=CostStatus(str(data["status"])),
        incurred_at=datetime.fromisoformat(str(data["incurred_at"])),
        run_id=str(data["run_id"]) if data.get("run_id") is not None else None,
        visibility=Visibility(str(data["visibility"])),
    )


def _as_usd(value: Decimal | str | float) -> Decimal:
    amount = Decimal(str(value))
    if not amount.is_finite() or amount < 0:
        raise ValueError("L'importo USD deve essere finito e non negativo")
    quantized = amount.quantize(Decimal("0.000001"), rounding=ROUND_HALF_UP)
    if quantized != amount:
        raise ValueError("Gli importi USD supportano al massimo 6 decimali")
    return quantized


def _usd_to_micros(value: Decimal | str | float) -> int:
    return int(_as_usd(value) * Decimal(1_000_000))


def _month_key(value: datetime) -> str:
    return f"{value.year:04d}-{value.month:02d}"


SQLiteStore = IntelligenceStore
