from __future__ import annotations

import argparse
import imaplib
import json
import os
import sys
from dataclasses import asdict, replace
from datetime import datetime, timedelta
from decimal import Decimal
from pathlib import Path
from zoneinfo import ZoneInfo
from uuid import uuid4

from .config import Settings, load_settings, prepare_private_directories
from .connectors import (
    IMAPConnector,
    IMAPLibTransport,
    IMAPState,
    JSONLImportConnector,
    JSONLState,
    RSSConnector,
    RSSState,
    XBookmarksConnector,
    XBookmarksState,
    XQueryCursor,
    XRecentSearchConnector,
    XRecentSearchState,
)
from .curation import rank_events
from .delivery import DeliveryBlocked, SMTPConfig, deliver_email
from .domain import (
    DeliveryRecord,
    DeliveryStatus,
    CostEntry,
    CostStatus,
    RunRecord,
    RunStatus,
    Visibility,
    Watermark,
    stable_id,
)
from .pipeline import build_digest_entries, ingest_records, reconcile_events
from .providers import DeterministicProvider, StructuredHTTPProvider, urllib_post_json
from .rendering import Digest, render_html, write_digest
from .scheduling import make_window
from .storage import IntelligenceStore
from .http import UrllibHTTPTransport


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="ai-intel")
    parser.add_argument("--config", required=True, help="Configurazione TOML non-secret")
    commands = parser.add_subparsers(dest="command", required=True)
    commands.add_parser("init", help="Inizializza lo storage privato")
    commands.add_parser("status", help="Mostra lo stato locale senza contenuti raw")
    commands.add_parser("delivery-status", help="Elenca lo stato delle delivery")
    commands.add_parser("cost-status", help="Elenca reservation e costi stimati")

    resolve_delivery = commands.add_parser(
        "resolve-delivery", help="Riconcilia manualmente una delivery ambigua"
    )
    resolve_delivery.add_argument("--id", required=True)
    resolve_delivery.add_argument("--outcome", choices=("sent", "failed", "blocked"), required=True)

    reconcile_cost = commands.add_parser(
        "reconcile-cost", help="Riconcilia una reservation con l'usage verificato"
    )
    reconcile_cost.add_argument("--reservation-key", required=True)
    cost_result = reconcile_cost.add_mutually_exclusive_group(required=True)
    cost_result.add_argument("--actual-usd", type=Decimal)
    cost_result.add_argument("--release", action="store_true")

    ingest = commands.add_parser("ingest-jsonl", help="Import incrementale da JSONL")
    ingest.add_argument("path", type=Path)
    ingest.add_argument("--source-id", default="manual-jsonl")
    ingest.add_argument("--max-records", type=int, default=1_000)

    rss = commands.add_parser("ingest-rss", help="Import incrementale RSS/Atom")
    rss.add_argument("--source-id", required=True)
    rss.add_argument("--url", required=True)

    imap = commands.add_parser("ingest-imap", help="Import incrementale da mailbox IMAP")
    imap.add_argument("--source-id", required=True)
    imap.add_argument("--host", required=True)
    imap.add_argument("--mailbox", default="INBOX")
    imap.add_argument("--username-env", default="IMAP_USERNAME")
    imap.add_argument("--password-env", default="IMAP_PASSWORD")

    x_recent = commands.add_parser("ingest-x", help="Watchlist via X Recent Search")
    x_recent.add_argument("--source-id", default="x-watchlist")
    x_recent.add_argument("--handle", action="append", required=True)
    x_recent.add_argument("--start", help="Bootstrap ISO; default: 24 ore prima")
    x_recent.add_argument("--end", help="Fine finestra ISO opzionale")

    bookmarks = commands.add_parser("ingest-x-bookmarks", help="Importa bookmark X privati")
    bookmarks.add_argument("--source-id", default="x-bookmarks")
    bookmarks.add_argument("--user-id", required=True)

    curate = commands.add_parser("curate", help="Deduplica e riconcilia gli eventi")
    curate.add_argument("--similarity-threshold", type=float, default=0.58)

    render = commands.add_parser("render", help="Genera digest e preview email privata")
    render.add_argument("--slot", choices=("am", "pm", "weekly"), required=True)
    render.add_argument("--at", help="Timestamp ISO; default: ora corrente")
    render.add_argument("--since", help="Watermark ISO esplicito")
    render.add_argument("--provider-endpoint", help="Gateway editoriale HTTPS opzionale")
    render.add_argument("--send", action="store_true", help="Invia davvero all'owner in allowlist")
    return parser


def _state_path(settings: Settings, source_id: str) -> Path:
    safe = "".join(character if character.isalnum() or character in "-_" else "_" for character in source_id)
    return settings.data_dir / "connector-state" / f"{safe}.json"


def _load_jsonl_state(path: Path) -> JSONLState:
    if not path.exists():
        return JSONLState()
    value = json.loads(path.read_text(encoding="utf-8"))
    return JSONLState(
        file_id=value.get("file_id"),
        byte_offset=int(value.get("byte_offset", 0)),
        line_number=int(value.get("line_number", 0)),
    )


def _save_jsonl_state(path: Path, state: JSONLState) -> None:
    path.parent.mkdir(mode=0o700, parents=True, exist_ok=True)
    temporary = path.with_suffix(".tmp")
    temporary.write_text(json.dumps(asdict(state), indent=2) + "\n", encoding="utf-8")
    temporary.replace(path)


def _load_state(path: Path, state_type):
    if not path.exists():
        return state_type()
    value = json.loads(path.read_text(encoding="utf-8"))
    if state_type is RSSState:
        return RSSState(value.get("etag"), value.get("last_modified"), tuple(value.get("seen_ids", ())))
    if state_type is IMAPState:
        return IMAPState(value.get("uid_validity"), int(value.get("last_uid", 0)))
    if state_type is XBookmarksState:
        return XBookmarksState(tuple(value.get("seen_ids", ())), value.get("pagination_token"))
    if state_type is XRecentSearchState:
        cursors = tuple(
            (query, XQueryCursor(**cursor)) for query, cursor in value.get("cursors", ())
        )
        return XRecentSearchState(cursors)
    raise TypeError(f"Tipo stato non supportato: {state_type}")


def _save_state(path: Path, state: object) -> None:
    path.parent.mkdir(mode=0o700, parents=True, exist_ok=True)
    temporary = path.with_suffix(".tmp")
    temporary.write_text(json.dumps(asdict(state), indent=2) + "\n", encoding="utf-8")
    temporary.replace(path)


def _reserve_x_budget(
    store: IntelligenceStore,
    settings: Settings,
    *,
    source_id: str,
    operation: str,
    at: datetime,
    unit_cost_usd: Decimal,
) -> tuple[str, int]:
    budget = Decimal(str(settings.x_monthly_budget_usd))
    remaining = budget - store.monthly_cost(at.year, at.month)
    budget_bound = int(remaining / unit_cost_usd)
    max_posts = min(settings.x_max_posts_per_run, budget_bound)
    if max_posts < 10:
        raise ValueError("Budget X mensile residuo insufficiente per una pagina minima")
    reservation_key = stable_id(
        "x-cost-reservation", source_id, operation, at.isoformat(timespec="seconds")
    )
    reservation = CostEntry(
        id=stable_id("cost", reservation_key),
        reservation_key=reservation_key,
        provider="x",
        operation=operation,
        amount_usd=unit_cost_usd * max_posts,
        status=CostStatus.RESERVED,
        incurred_at=at,
    )
    if not store.reserve_cost(reservation, monthly_budget_usd=budget):
        raise RuntimeError("Reservation costi X duplicata o oltre il budget mensile")
    return reservation_key, max_posts


def _digest_watermark_source(slot: str) -> str:
    return "digest:weekly" if slot == "weekly" else "digest:daily"


def _provider(args: argparse.Namespace):
    if not args.provider_endpoint:
        return DeterministicProvider()
    token = os.environ.get("EDITORIAL_PROVIDER_TOKEN", "")
    if not token:
        raise ValueError("EDITORIAL_PROVIDER_TOKEN obbligatorio con --provider-endpoint")
    return StructuredHTTPProvider(
        name="configured-gateway",
        endpoint=args.provider_endpoint,
        bearer_token=token,
        post_json=urllib_post_json,
    )


def _parse_timestamp(value: str | None, zone: ZoneInfo) -> datetime:
    if value is None:
        return datetime.now(zone)
    parsed = datetime.fromisoformat(value)
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=zone)
    return parsed.astimezone(zone)


def _run(args: argparse.Namespace, settings: Settings) -> int:
    prepare_private_directories(settings)
    with IntelligenceStore(
        data_dir=settings.data_dir, public_repo_root=settings.public_repo_root
    ) as store:
        if args.command == "init":
            print(f"Storage privato inizializzato: {settings.database_path}")
            return 0
        if args.command == "status":
            print(
                json.dumps(
                    {
                        "database": str(settings.database_path),
                        "documents": len(store.list_documents()),
                        "events": len(store.list_events()),
                        "claims": len(store.list_claims()),
                        "concepts": len(store.list_concepts()),
                        "reading_decisions": len(store.list_reading_decisions()),
                        "runs": len(store.list_runs()),
                        "deliveries": len(store.list_deliveries()),
                        "outbox": str(settings.outbox_dir),
                    },
                    indent=2,
                )
            )
            return 0
        if args.command == "delivery-status":
            print(
                json.dumps(
                    [
                        {
                            "id": item.id,
                            "slot": item.idempotency_key,
                            "status": item.status.value,
                            "created_at": item.created_at.isoformat(),
                            "delivered_at": item.delivered_at.isoformat() if item.delivered_at else None,
                            "error": item.error,
                        }
                        for item in store.list_deliveries()
                    ],
                    indent=2,
                )
            )
            return 0
        if args.command == "resolve-delivery":
            current = store.get_delivery(args.id)
            if current is None:
                raise ValueError(f"Delivery non trovata: {args.id}")
            if current.status is DeliveryStatus.SENT:
                raise ValueError("Una delivery gia' SENT non puo' essere modificata")
            now = datetime.now(ZoneInfo(settings.timezone))
            outcome = DeliveryStatus(args.outcome)
            resolved = replace(
                current,
                status=outcome,
                delivered_at=now if outcome is DeliveryStatus.SENT else None,
                error=(
                    "Riconciliazione umana: invio confermato assente, retry consentito"
                    if outcome is DeliveryStatus.FAILED
                    else (
                        "Riconciliazione umana richiesta prima del retry"
                        if outcome is DeliveryStatus.BLOCKED
                        else None
                    )
                ),
            )
            store.save_delivery(resolved)
            print(json.dumps({"id": resolved.id, "status": resolved.status.value}, indent=2))
            return 0
        if args.command == "cost-status":
            print(
                json.dumps(
                    [
                        {
                            "reservation_key": item.reservation_key,
                            "provider": item.provider,
                            "operation": item.operation,
                            "amount_usd": str(item.amount_usd),
                            "status": item.status.value,
                            "incurred_at": item.incurred_at.isoformat(),
                        }
                        for item in store.list_cost_entries()
                    ],
                    indent=2,
                )
            )
            return 0
        if args.command == "reconcile-cost":
            reconciled = store.reconcile_cost(
                args.reservation_key,
                actual_amount_usd=Decimal("0") if args.release else args.actual_usd,
                status=CostStatus.RELEASED if args.release else CostStatus.SETTLED,
            )
            print(
                json.dumps(
                    {
                        "reservation_key": reconciled.reservation_key,
                        "amount_usd": str(reconciled.amount_usd),
                        "status": reconciled.status.value,
                    },
                    indent=2,
                )
            )
            return 0
        if args.command == "ingest-jsonl":
            state_path = _state_path(settings, args.source_id)
            connector = JSONLImportConnector(
                source_id=args.source_id,
                path=args.path,
                max_records_per_run=args.max_records,
            )
            batch = connector.fetch(_load_jsonl_state(state_path))
            saved = ingest_records(store, batch.records)
            _save_jsonl_state(state_path, batch.state)
            print(json.dumps({"acquired": len(batch.records), "saved": len(saved)}, indent=2))
            return 0
        if args.command == "ingest-rss":
            state_path = _state_path(settings, args.source_id)
            connector = RSSConnector(
                source_id=args.source_id,
                url=args.url,
                transport=UrllibHTTPTransport(),
            )
            batch = connector.fetch(_load_state(state_path, RSSState))
            saved = ingest_records(store, batch.records)
            _save_state(state_path, batch.state)
            print(json.dumps({"acquired": len(batch.records), "saved": len(saved)}, indent=2))
            return 0
        if args.command == "ingest-imap":
            username = os.environ.get(args.username_env, "")
            password = os.environ.get(args.password_env, "")
            if not username or not password:
                raise ValueError(f"Credenziali mancanti: {args.username_env}/{args.password_env}")
            state_path = _state_path(settings, args.source_id)
            client = imaplib.IMAP4_SSL(args.host)
            try:
                client.login(username, password)
                connector = IMAPConnector(
                    source_id=args.source_id,
                    mailbox=args.mailbox,
                    transport=IMAPLibTransport(client),
                )
                batch = connector.fetch(_load_state(state_path, IMAPState))
            finally:
                try:
                    client.logout()
                except imaplib.IMAP4.error:
                    pass
            saved = ingest_records(store, batch.records)
            _save_state(state_path, batch.state)
            print(json.dumps({"acquired": len(batch.records), "saved": len(saved)}, indent=2))
            return 0
        if args.command == "ingest-x":
            token = os.environ.get("X_BEARER_TOKEN", "")
            if not token:
                raise ValueError("X_BEARER_TOKEN mancante")
            zone = ZoneInfo(settings.timezone)
            end = _parse_timestamp(args.end, zone) if args.end else datetime.now(zone)
            start = _parse_timestamp(args.start, zone) if args.start else end - timedelta(days=1)
            reservation_key, max_posts = _reserve_x_budget(
                store,
                settings,
                source_id=args.source_id,
                operation="recent_search_post_read",
                at=end,
                unit_cost_usd=(
                    Decimal(str(settings.x_post_read_unit_usd))
                    + Decimal(str(settings.x_user_read_unit_usd))
                ),
            )
            state_path = _state_path(settings, args.source_id)
            connector = XRecentSearchConnector(
                source_id=args.source_id,
                handles=args.handle,
                transport=UrllibHTTPTransport(),
                authorization=f"Bearer {token}",
                max_posts_per_run=max_posts,
                max_pages_per_run=settings.x_max_pages_per_run,
            )
            batch = connector.fetch(
                _load_state(state_path, XRecentSearchState), start_time=start, end_time=end
            )
            saved = ingest_records(store, batch.records)
            _save_state(state_path, batch.state)
            actual_cost = (
                Decimal(str(settings.x_post_read_unit_usd)) * batch.usage.post_reads
                + Decimal(str(settings.x_user_read_unit_usd)) * batch.usage.user_reads
            )
            store.reconcile_cost(reservation_key, actual_amount_usd=actual_cost)
            print(
                json.dumps(
                    {
                        "acquired": len(batch.records),
                        "saved": len(saved),
                        "hard_cap": max_posts,
                        "estimated_cost_usd": str(actual_cost),
                        "usage": asdict(batch.usage),
                    },
                    indent=2,
                )
            )
            return 0
        if args.command == "ingest-x-bookmarks":
            token = os.environ.get("X_USER_ACCESS_TOKEN", "")
            if not token:
                raise ValueError("X_USER_ACCESS_TOKEN mancante")
            now = datetime.now(ZoneInfo(settings.timezone))
            reservation_key, max_posts = _reserve_x_budget(
                store,
                settings,
                source_id=args.source_id,
                operation="bookmarks_owned_read",
                at=now,
                unit_cost_usd=(
                    Decimal(str(settings.x_owned_read_unit_usd))
                    + Decimal(str(settings.x_user_read_unit_usd))
                ),
            )
            state_path = _state_path(settings, args.source_id)
            connector = XBookmarksConnector(
                source_id=args.source_id,
                user_id=args.user_id,
                transport=UrllibHTTPTransport(),
                authorization=f"Bearer {token}",
                max_posts_per_run=max_posts,
                max_pages_per_run=settings.x_max_pages_per_run,
            )
            batch = connector.fetch(_load_state(state_path, XBookmarksState))
            saved = ingest_records(store, batch.records)
            _save_state(state_path, batch.state)
            actual_cost = (
                Decimal(str(settings.x_owned_read_unit_usd)) * batch.usage.owned_post_reads
                + Decimal(str(settings.x_user_read_unit_usd)) * batch.usage.user_reads
            )
            store.reconcile_cost(reservation_key, actual_amount_usd=actual_cost)
            print(
                json.dumps(
                    {
                        "acquired": len(batch.records),
                        "saved": len(saved),
                        "hard_cap": max_posts,
                        "estimated_cost_usd": str(actual_cost),
                        "usage": asdict(batch.usage),
                    },
                    indent=2,
                )
            )
            return 0
        if args.command == "curate":
            events = reconcile_events(store, similarity_threshold=args.similarity_threshold)
            print(json.dumps({"documents": len(store.list_documents()), "events": len(events)}, indent=2))
            return 0
        if args.command == "render":
            zone = ZoneInfo(settings.timezone)
            end = _parse_timestamp(args.at, zone)
            watermark_source = _digest_watermark_source(args.slot)
            saved_watermark = store.get_watermark(watermark_source)
            previous = (
                _parse_timestamp(args.since, zone)
                if args.since
                else (
                    _parse_timestamp(saved_watermark.cursor, zone)
                    if saved_watermark is not None
                    else None
                )
            )
            window = make_window(
                args.slot,
                end,
                previous_success_at=previous,
                timezone=settings.timezone,
            )
            provider = _provider(args)
            if args.send and isinstance(provider, DeterministicProvider):
                raise RuntimeError(
                    "Invio bloccato: la baseline deterministica produce solo preview da revisionare"
                )
            started_at = datetime.now(zone)
            run_id = stable_id("run", window.idempotency_key, uuid4().hex)
            store.save_run(
                RunRecord(
                    id=run_id,
                    kind=f"digest:{args.slot}",
                    started_at=started_at,
                    status=RunStatus.RUNNING,
                )
            )
            events = tuple(
                event
                for event in store.list_events()
                if window.starts_at < event.last_seen.astimezone(zone) <= window.ends_at
            )
            ranked = rank_events(events, store.list_documents())
            entries = build_digest_entries(
                store,
                ranked,
                provider,
                max_events=settings.max_digest_events,
                reading_budget_minutes=settings.daily_reading_minutes,
            )
            if args.send and any(entry.confidence == "low" for entry in entries):
                failed_at = datetime.now(zone)
                store.save_run(
                    RunRecord(
                        id=run_id,
                        kind=f"digest:{args.slot}",
                        started_at=started_at,
                        completed_at=failed_at,
                        status=RunStatus.FAILED,
                        error="Digest con voci a bassa confidenza",
                    )
                )
                raise RuntimeError("Invio bloccato: il digest contiene voci a bassa confidenza")
            digest = Digest(
                kind=args.slot,
                generated_at=end,
                entries=entries,
                period_label=(
                    f"{window.starts_at.isoformat(timespec='minutes')} — "
                    f"{window.ends_at.isoformat(timespec='minutes')}"
                ),
                coverage_notes=(f"Provider editoriale: {provider.name}",),
            )
            markdown_path, html_path = write_digest(digest, settings.outbox_dir)
            smtp = SMTPConfig(
                host=settings.smtp_host,
                port=settings.smtp_port,
                username=os.environ.get("SMTP_USERNAME", settings.owner_email),
                password=os.environ.get("SMTP_PASSWORD", ""),
                sender=settings.owner_email,
                recipient_allowlist=settings.recipient_allowlist,
            )
            delivery_key = (
                f"email:{window.idempotency_key}:{settings.owner_email}"
                if args.send
                else f"preview:{window.idempotency_key}:{settings.owner_email}"
            )
            delivery_id = stable_id("delivery", delivery_key)
            if args.send:
                reservation = store.reserve_delivery(
                    DeliveryRecord(
                        id=delivery_id,
                        run_id=run_id,
                        channel="email",
                        recipient=settings.owner_email,
                        status=DeliveryStatus.PENDING,
                        idempotency_key=delivery_key,
                        created_at=started_at,
                        visibility=Visibility.PRIVATE,
                    )
                )
                if reservation is None:
                    failed_at = datetime.now(zone)
                    store.save_run(
                        RunRecord(
                            id=run_id,
                            kind=f"digest:{args.slot}",
                            started_at=started_at,
                            completed_at=failed_at,
                            status=RunStatus.FAILED,
                            error="Delivery gia' riservata o inviata",
                        )
                    )
                    raise RuntimeError("Delivery gia' riservata o inviata per questa finestra")
                delivery_id = reservation.id
            try:
                email_path = deliver_email(
                    smtp,
                    recipient=settings.owner_email,
                    subject=f"AI Intelligence — {args.slot.upper()} — {end.date().isoformat()}",
                    html_body=render_html(digest),
                    send=args.send,
                    outbox=settings.outbox_dir,
                )
            except Exception as exc:
                failed_at = datetime.now(zone)
                failure_status = (
                    DeliveryStatus.FAILED
                    if isinstance(exc, DeliveryBlocked) or not args.send
                    else DeliveryStatus.BLOCKED
                )
                store.save_delivery(
                    DeliveryRecord(
                        id=delivery_id,
                        run_id=run_id,
                        channel="email",
                        recipient=settings.owner_email,
                        status=failure_status,
                        idempotency_key=delivery_key,
                        created_at=started_at,
                        error=str(exc),
                    )
                )
                store.save_run(
                    RunRecord(
                        id=run_id,
                        kind=f"digest:{args.slot}",
                        started_at=started_at,
                        completed_at=failed_at,
                        status=RunStatus.FAILED,
                        error=str(exc),
                    )
                )
                raise
            finished_at = datetime.now(zone)
            delivery = DeliveryRecord(
                id=delivery_id,
                run_id=run_id,
                channel="email",
                recipient=settings.owner_email,
                status=DeliveryStatus.SENT if args.send else DeliveryStatus.PREVIEW,
                idempotency_key=delivery_key,
                created_at=started_at,
                delivered_at=finished_at if args.send else None,
                visibility=Visibility.PRIVATE,
            )
            store.save_delivery(delivery)
            store.save_run(
                RunRecord(
                    id=run_id,
                    kind=f"digest:{args.slot}",
                    started_at=started_at,
                    completed_at=finished_at,
                    status=RunStatus.SUCCEEDED,
                )
            )
            if args.send:
                store.save_watermark(
                    Watermark(
                        source_id=watermark_source,
                        cursor=window.ends_at.isoformat(),
                        observed_at=finished_at,
                        run_id=run_id,
                    )
                )
            print(
                json.dumps(
                    {
                        "slot": args.slot,
                        "entries": len(entries),
                        "markdown": str(markdown_path),
                        "html": str(html_path),
                        "email_preview": str(email_path),
                        "sent": bool(args.send),
                    },
                    indent=2,
                )
            )
            return 0
    raise AssertionError("Comando non gestito")


def main(argv: list[str] | None = None) -> int:
    parser = _parser()
    args = parser.parse_args(argv)
    try:
        settings = load_settings(args.config)
        return _run(args, settings)
    except (OSError, ValueError, RuntimeError, json.JSONDecodeError) as exc:
        print(f"ERRORE: {exc}", file=sys.stderr)
        return 2
