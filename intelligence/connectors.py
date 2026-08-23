from __future__ import annotations

import hashlib
import json
import re
from dataclasses import dataclass
from datetime import datetime, timezone
from email import policy
from email.message import Message
from email.parser import BytesParser
from email.utils import parsedate_to_datetime
from html.parser import HTMLParser
from pathlib import Path
from typing import Any, Generic, Iterable, Mapping, Protocol, Sequence, TypeVar
from xml.etree import ElementTree

from .http import HTTPResponse, HTTPTransport, require_success


StateT = TypeVar("StateT")
X_RECENT_SEARCH_URL = "https://api.x.com/2/tweets/search/recent"
X_BOOKMARKS_URL = "https://api.x.com/2/users/{user_id}/bookmarks"
_HANDLE = re.compile(r"^[A-Za-z0-9_]{1,15}$")


@dataclass(frozen=True)
class SourceRecord:
    source_id: str
    source_type: str
    external_id: str
    url: str | None
    title: str
    text: str
    published_at: datetime | None
    author: str | None = None


# Canonical ingestion name used by the pipeline; SourceRecord remains descriptive for callers.
RawItem = SourceRecord


@dataclass(frozen=True)
class ConnectorUsage:
    post_reads: int = 0
    user_reads: int = 0
    owned_post_reads: int = 0

    def __post_init__(self) -> None:
        if min(self.post_reads, self.user_reads, self.owned_post_reads) < 0:
            raise ValueError("I contatori usage non possono essere negativi")


@dataclass(frozen=True)
class ConnectorBatch(Generic[StateT]):
    records: tuple[SourceRecord, ...]
    state: StateT
    usage: ConnectorUsage = ConnectorUsage()


def _header(headers: Mapping[str, str], name: str) -> str | None:
    target = name.lower()
    return next((value for key, value in headers.items() if key.lower() == target), None)


def _aware_utc(value: datetime) -> datetime:
    if value.tzinfo is None:
        value = value.replace(tzinfo=timezone.utc)
    return value.astimezone(timezone.utc)


def _parse_datetime(value: object) -> datetime | None:
    if value is None or str(value).strip() == "":
        return None
    text = str(value).strip()
    try:
        parsed = parsedate_to_datetime(text)
    except (TypeError, ValueError, OverflowError):
        parsed = None
    if parsed is None:
        try:
            parsed = datetime.fromisoformat(text.replace("Z", "+00:00"))
        except ValueError as exc:
            raise ValueError(f"Timestamp non valido: {text}") from exc
    return _aware_utc(parsed)


def _x_timestamp(value: datetime) -> str:
    return _aware_utc(value).isoformat(timespec="seconds").replace("+00:00", "Z")


class _TextExtractor(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.parts: list[str] = []
        self.links: list[str] = []

    def handle_data(self, data: str) -> None:
        self.parts.append(data)

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag.lower() != "a":
            return
        href = next((value for key, value in attrs if key.lower() == "href"), None)
        if href and href.startswith("https://"):
            self.links.append(href)


def _plain_text(value: str) -> str:
    if "<" not in value:
        return " ".join(value.split())
    parser = _TextExtractor()
    parser.feed(value)
    parser.close()
    normalized = " ".join(" ".join(parser.parts).split())
    return re.sub(r"\s+([,.;:!?])", r"\1", normalized)


def _stable_id(*parts: str) -> str:
    digest = hashlib.sha256("\x1f".join(parts).encode("utf-8")).hexdigest()
    return f"sha256:{digest}"


@dataclass(frozen=True)
class RSSState:
    etag: str | None = None
    last_modified: str | None = None
    seen_ids: tuple[str, ...] = ()


class RSSConnector:
    def __init__(
        self,
        *,
        source_id: str,
        url: str,
        transport: HTTPTransport,
        max_seen_ids: int = 5_000,
    ) -> None:
        if not source_id.strip():
            raise ValueError("source_id RSS obbligatorio")
        if not url.startswith("https://"):
            raise ValueError("Il feed RSS deve usare HTTPS")
        if max_seen_ids <= 0:
            raise ValueError("max_seen_ids deve essere positivo")
        self.source_id = source_id
        self.url = url
        self.transport = transport
        self.max_seen_ids = max_seen_ids

    def fetch(self, state: RSSState | None = None) -> ConnectorBatch[RSSState]:
        current = state or RSSState()
        headers: dict[str, str] = {"Accept": "application/atom+xml, application/rss+xml, application/xml"}
        if current.etag:
            headers["If-None-Match"] = current.etag
        if current.last_modified:
            headers["If-Modified-Since"] = current.last_modified
        response = self.transport.request("GET", self.url, headers=headers)
        if response.status == 304:
            return ConnectorBatch((), current)
        require_success(response, self.url)
        records = self._parse(response)
        seen = set(current.seen_ids)
        fresh = tuple(record for record in records if record.external_id not in seen)
        merged_ids = tuple(
            dict.fromkeys([*(record.external_id for record in records), *current.seen_ids])
        )[: self.max_seen_ids]
        next_state = RSSState(
            etag=_header(response.headers, "etag") or current.etag,
            last_modified=_header(response.headers, "last-modified") or current.last_modified,
            seen_ids=merged_ids,
        )
        return ConnectorBatch(fresh, next_state)

    def _parse(self, response: HTTPResponse) -> tuple[SourceRecord, ...]:
        try:
            root = ElementTree.fromstring(response.body)
        except ElementTree.ParseError as exc:
            raise ValueError(f"Feed XML non valido: {self.url}") from exc
        entries = [node for node in root.iter() if _local_name(node.tag) in {"item", "entry"}]
        output: list[SourceRecord] = []
        for entry in entries:
            values = _xml_values(entry)
            link = _entry_link(entry, values)
            title = values.get("title", "").strip()
            raw_text = (
                values.get("encoded")
                or values.get("content")
                or values.get("description")
                or values.get("summary")
                or ""
            )
            text = _plain_text(raw_text)
            external_id = (
                values.get("guid")
                or values.get("id")
                or link
                or _stable_id(title, values.get("published", ""), text)
            ).strip()
            published = _parse_datetime(
                values.get("pubdate") or values.get("published") or values.get("updated")
            )
            output.append(
                SourceRecord(
                    source_id=self.source_id,
                    source_type="rss",
                    external_id=external_id,
                    url=link or None,
                    title=title or text[:160] or external_id,
                    text=text,
                    published_at=published,
                    author=(values.get("author") or values.get("creator") or "").strip() or None,
                )
            )
        return tuple(output)


def _local_name(tag: str) -> str:
    return tag.rsplit("}", 1)[-1].lower()


def _xml_values(entry: ElementTree.Element) -> dict[str, str]:
    values: dict[str, str] = {}
    for child in entry:
        name = _local_name(child.tag)
        if name not in values and child.text:
            values[name] = child.text
    return values


def _entry_link(entry: ElementTree.Element, values: Mapping[str, str]) -> str:
    for child in entry:
        if _local_name(child.tag) != "link":
            continue
        relation = child.attrib.get("rel", "alternate")
        href = child.attrib.get("href")
        if href and relation in {"alternate", ""}:
            return href.strip()
    return values.get("link", "").strip()


class IMAPTransport(Protocol):
    def select_readonly(self, mailbox: str) -> int: ...

    def search_uids(self, after_uid: int) -> Sequence[int]: ...

    def fetch_rfc822(self, uid: int) -> bytes: ...


class IMAPLibTransport:
    """Adapter around an already-authenticated imaplib client; it owns no credentials."""

    def __init__(self, client: Any) -> None:
        self.client = client

    def select_readonly(self, mailbox: str) -> int:
        status, _ = self.client.select(mailbox, readonly=True)
        if status != "OK":
            raise RuntimeError(f"IMAP select fallita per {mailbox}")
        _, values = self.client.response("UIDVALIDITY")
        if not values or values[0] is None:
            raise RuntimeError("Il server IMAP non ha restituito UIDVALIDITY")
        raw = values[0].decode() if isinstance(values[0], bytes) else str(values[0])
        match = re.search(r"\d+", raw)
        if not match:
            raise RuntimeError("UIDVALIDITY IMAP non valida")
        return int(match.group())

    def search_uids(self, after_uid: int) -> Sequence[int]:
        status, values = self.client.uid("search", None, f"UID {after_uid + 1}:*")
        if status != "OK":
            raise RuntimeError("IMAP UID SEARCH fallita")
        if not values or not values[0]:
            return ()
        raw = values[0].decode() if isinstance(values[0], bytes) else str(values[0])
        return tuple(int(value) for value in raw.split())

    def fetch_rfc822(self, uid: int) -> bytes:
        status, values = self.client.uid("fetch", str(uid), "(RFC822)")
        if status != "OK":
            raise RuntimeError(f"IMAP UID FETCH fallita per {uid}")
        for value in values or ():
            if isinstance(value, tuple) and len(value) > 1 and isinstance(value[1], bytes):
                return value[1]
        raise RuntimeError(f"Messaggio RFC822 assente per UID {uid}")


@dataclass(frozen=True)
class IMAPState:
    uid_validity: int | None = None
    last_uid: int = 0


class IMAPConnector:
    def __init__(
        self,
        *,
        source_id: str,
        mailbox: str,
        transport: IMAPTransport,
        max_messages_per_run: int = 200,
    ) -> None:
        if not source_id.strip() or not mailbox.strip():
            raise ValueError("source_id e mailbox IMAP sono obbligatori")
        if max_messages_per_run <= 0:
            raise ValueError("max_messages_per_run deve essere positivo")
        self.source_id = source_id
        self.mailbox = mailbox
        self.transport = transport
        self.max_messages_per_run = max_messages_per_run

    def fetch(self, state: IMAPState | None = None) -> ConnectorBatch[IMAPState]:
        current = state or IMAPState()
        validity = self.transport.select_readonly(self.mailbox)
        after_uid = current.last_uid if current.uid_validity == validity else 0
        uids = sorted(set(int(uid) for uid in self.transport.search_uids(after_uid)))[
            : self.max_messages_per_run
        ]
        records = tuple(self._parse(uid, self.transport.fetch_rfc822(uid)) for uid in uids)
        return ConnectorBatch(
            records,
            IMAPState(uid_validity=validity, last_uid=max(uids, default=after_uid)),
        )

    def _parse(self, uid: int, raw: bytes) -> SourceRecord:
        message = BytesParser(policy=policy.default).parsebytes(raw)
        text, article_url = _message_content(message)
        message_id = str(message.get("Message-ID", "")).strip() or f"uid:{uid}"
        title = str(message.get("Subject", "")).strip() or text[:160] or message_id
        return SourceRecord(
            source_id=self.source_id,
            source_type="email",
            external_id=message_id,
            url=article_url,
            title=title,
            text=text,
            published_at=_parse_datetime(message.get("Date")),
            author=str(message.get("From", "")).strip() or None,
        )


def _message_content(message: Message) -> tuple[str, str | None]:
    if message.is_multipart():
        body = message.get_body(preferencelist=("plain", "html"))
        if body is None:
            text = ""
        else:
            text = _part_text(body)
    else:
        body = message
        text = _part_text(body)

    candidates: list[str] = []
    for header_name in ("Archived-At", "List-Archive"):
        header_value = str(message.get(header_name, "")).strip().strip("<>")
        if header_value.startswith("https://"):
            candidates.append(header_value)
    parts = message.walk() if message.is_multipart() else (message,)
    for part in parts:
        if part.get_content_type() != "text/html":
            continue
        html = _part_raw_content(part)
        parser = _TextExtractor()
        parser.feed(html)
        parser.close()
        candidates.extend(parser.links)
    if not candidates:
        candidates.extend(re.findall(r"https://[^\s<>\]\[\"']+", text))
    return text, _preferred_article_url(candidates)


def _part_text(body: Message) -> str:
    return _plain_text(_part_raw_content(body))


def _part_raw_content(body: Message) -> str:
    try:
        content = body.get_content()
    except (LookupError, UnicodeError):
        payload = body.get_payload(decode=True) or b""
        content = payload.decode("utf-8", errors="replace")
    return str(content)


def _preferred_article_url(candidates: Iterable[str]) -> str | None:
    unique = list(dict.fromkeys(candidate.strip() for candidate in candidates if candidate.strip()))
    if not unique:
        return None
    noisy_markers = ("unsubscribe", "optout", "opt-out", "preferences", "tracking", "/track", "/click")
    return min(unique, key=lambda url: (any(marker in url.lower() for marker in noisy_markers), unique.index(url)))


def batch_x_handles(handles: Iterable[str], *, max_query_length: int = 512) -> tuple[str, ...]:
    if max_query_length < 16:
        raise ValueError("max_query_length troppo piccolo")
    normalized = sorted({handle.strip().lstrip("@").lower() for handle in handles})
    if not normalized:
        raise ValueError("La watchlist X non puo' essere vuota")
    invalid = [handle for handle in normalized if not _HANDLE.fullmatch(handle)]
    if invalid:
        raise ValueError(f"Handle X non validi: {', '.join(invalid)}")
    batches: list[str] = []
    terms: list[str] = []
    for handle in normalized:
        candidate_terms = [*terms, f"from:{handle}"]
        candidate = f"({' OR '.join(candidate_terms)})"
        if len(candidate) <= max_query_length:
            terms = candidate_terms
            continue
        if not terms:
            raise ValueError(f"Handle incompatibile con il limite query: {handle}")
        batches.append(f"({' OR '.join(terms)})")
        terms = [f"from:{handle}"]
    if terms:
        batches.append(f"({' OR '.join(terms)})")
    return tuple(batches)


@dataclass(frozen=True)
class XQueryCursor:
    since_id: str | None = None
    pagination_token: str | None = None
    pending_newest_id: str | None = None
    start_time: str | None = None
    end_time: str | None = None


@dataclass(frozen=True)
class XRecentSearchState:
    cursors: tuple[tuple[str, XQueryCursor], ...] = ()

    def by_query(self) -> dict[str, XQueryCursor]:
        return dict(self.cursors)


class XRecentSearchConnector:
    def __init__(
        self,
        *,
        source_id: str,
        handles: Iterable[str],
        transport: HTTPTransport,
        authorization: str,
        max_posts_per_run: int,
        max_pages_per_run: int = 10,
        max_query_length: int = 512,
    ) -> None:
        if not source_id.strip() or not authorization.strip():
            raise ValueError("source_id e authorization X sono obbligatori")
        if max_posts_per_run < 10:
            raise ValueError("max_posts_per_run deve essere almeno 10 per X Recent Search")
        if max_pages_per_run <= 0:
            raise ValueError("max_pages_per_run deve essere positivo")
        self.source_id = source_id
        self.queries = batch_x_handles(handles, max_query_length=max_query_length)
        self.transport = transport
        self.authorization = authorization
        self.max_posts_per_run = max_posts_per_run
        self.max_pages_per_run = max_pages_per_run

    def fetch(
        self,
        state: XRecentSearchState | None = None,
        *,
        start_time: datetime | None = None,
        end_time: datetime | None = None,
    ) -> ConnectorBatch[XRecentSearchState]:
        current = (state or XRecentSearchState()).by_query()
        bootstrap_cursor = (
            XQueryCursor(
                start_time=_x_timestamp(start_time),
                end_time=_x_timestamp(end_time) if end_time else None,
            )
            if start_time is not None
            else None
        )
        next_cursors: dict[str, XQueryCursor] = {}
        records: list[SourceRecord] = []
        record_ids: set[str] = set()
        pages = 0
        post_reads = 0
        user_reads = 0

        for query in self.queries:
            original = current.get(query, XQueryCursor())
            cursor = original
            if not cursor.since_id and not cursor.pagination_token:
                if cursor.start_time:
                    pass
                elif bootstrap_cursor is None:
                    raise ValueError("start_time e' obbligatorio per il bootstrap X")
                else:
                    cursor = bootstrap_cursor

            while pages < self.max_pages_per_run:
                remaining = self.max_posts_per_run - len(records)
                if remaining < 10:
                    break
                query_args: dict[str, str | int] = {
                    "query": query,
                    "max_results": min(100, remaining),
                    "tweet.fields": "author_id,created_at,conversation_id,referenced_tweets",
                    "expansions": "author_id",
                    "user.fields": "username,name",
                }
                if cursor.since_id:
                    query_args["since_id"] = cursor.since_id
                elif cursor.start_time:
                    query_args["start_time"] = cursor.start_time
                if cursor.end_time:
                    query_args["end_time"] = cursor.end_time
                if cursor.pagination_token:
                    query_args["next_token"] = cursor.pagination_token

                payload = self._get(query_args)
                data = payload.get("data", [])
                meta = payload.get("meta", {})
                if not isinstance(data, list) or not isinstance(meta, dict):
                    raise ValueError("Risposta X Recent Search malformata")
                if len(data) > remaining:
                    raise ValueError("X ha restituito piu' post del max_results richiesto")
                post_reads += len(data)
                user_reads += _x_included_user_reads(payload.get("includes"))
                pages += 1
                pending_newest = cursor.pending_newest_id or _optional_string(meta.get("newest_id"))
                for record in _x_records(self.source_id, data, payload.get("includes")):
                    if record.external_id not in record_ids:
                        records.append(record)
                        record_ids.add(record.external_id)

                next_token = _optional_string(meta.get("next_token"))
                if next_token:
                    cursor = XQueryCursor(
                        since_id=cursor.since_id,
                        pagination_token=next_token,
                        pending_newest_id=pending_newest,
                        start_time=cursor.start_time,
                        end_time=cursor.end_time,
                    )
                    continue
                cursor = XQueryCursor(since_id=pending_newest or cursor.since_id)
                break

            next_cursors[query] = cursor
            if len(records) >= self.max_posts_per_run or pages >= self.max_pages_per_run:
                for remaining_query in self.queries:
                    if remaining_query not in next_cursors:
                        saved = current.get(remaining_query)
                        next_cursors[remaining_query] = saved or bootstrap_cursor or XQueryCursor()
                break

        state_items = tuple((query, next_cursors.get(query, current.get(query, XQueryCursor()))) for query in self.queries)
        return ConnectorBatch(
            tuple(records),
            XRecentSearchState(state_items),
            ConnectorUsage(post_reads=post_reads, user_reads=user_reads),
        )

    def _get(self, query: Mapping[str, str | int]) -> dict[str, object]:
        response = self.transport.request(
            "GET",
            X_RECENT_SEARCH_URL,
            headers={"Authorization": self.authorization, "Accept": "application/json"},
            query=query,
        )
        return require_success(response, X_RECENT_SEARCH_URL).json_object()


@dataclass(frozen=True)
class XBookmarksState:
    seen_ids: tuple[str, ...] = ()
    pagination_token: str | None = None


class XBookmarksConnector:
    def __init__(
        self,
        *,
        source_id: str,
        user_id: str,
        transport: HTTPTransport,
        authorization: str,
        max_posts_per_run: int,
        max_pages_per_run: int = 10,
    ) -> None:
        if not source_id.strip() or not user_id.isdigit() or not authorization.strip():
            raise ValueError("source_id, user_id numerico e authorization sono obbligatori")
        if max_posts_per_run <= 0 or max_pages_per_run <= 0:
            raise ValueError("I limiti X Bookmarks devono essere positivi")
        self.source_id = source_id
        self.url = X_BOOKMARKS_URL.format(user_id=user_id)
        self.transport = transport
        self.authorization = authorization
        self.max_posts_per_run = max_posts_per_run
        self.max_pages_per_run = max_pages_per_run

    def fetch(self, state: XBookmarksState | None = None) -> ConnectorBatch[XBookmarksState]:
        current = state or XBookmarksState()
        seen = set(current.seen_ids)
        records: list[SourceRecord] = []
        token = current.pagination_token
        pages = 0
        owned_post_reads = 0
        user_reads = 0
        while pages < self.max_pages_per_run and len(records) < self.max_posts_per_run:
            remaining = self.max_posts_per_run - len(records)
            query: dict[str, str | int] = {
                "max_results": min(100, remaining),
                "tweet.fields": "author_id,created_at,conversation_id,referenced_tweets",
                "expansions": "author_id",
                "user.fields": "username,name",
            }
            if token:
                query["pagination_token"] = token
            response = self.transport.request(
                "GET",
                self.url,
                headers={"Authorization": self.authorization, "Accept": "application/json"},
                query=query,
            )
            payload = require_success(response, self.url).json_object()
            data = payload.get("data", [])
            meta = payload.get("meta", {})
            if not isinstance(data, list) or not isinstance(meta, dict):
                raise ValueError("Risposta X Bookmarks malformata")
            if len(data) > remaining:
                raise ValueError("X ha restituito piu' bookmark del max_results richiesto")
            owned_post_reads += len(data)
            user_reads += _x_included_user_reads(payload.get("includes"))
            pages += 1
            for record in _x_records(self.source_id, data, payload.get("includes")):
                if record.external_id not in seen:
                    records.append(record)
                    seen.add(record.external_id)
            token = _optional_string(meta.get("next_token"))
            if not token:
                break
        ordered_seen = tuple(
            dict.fromkeys([*(record.external_id for record in records), *current.seen_ids])
        )
        return ConnectorBatch(
            tuple(records),
            XBookmarksState(ordered_seen, token),
            ConnectorUsage(owned_post_reads=owned_post_reads, user_reads=user_reads),
        )


def _optional_string(value: object) -> str | None:
    if value is None:
        return None
    text = str(value).strip()
    return text or None


def _x_included_user_reads(includes: object) -> int:
    if not isinstance(includes, dict):
        return 0
    users = includes.get("users")
    return len(users) if isinstance(users, list) else 0


def _x_records(
    source_id: str, data: Sequence[object], includes: object
) -> tuple[SourceRecord, ...]:
    users: dict[str, str] = {}
    if isinstance(includes, dict) and isinstance(includes.get("users"), list):
        for raw_user in includes["users"]:
            if isinstance(raw_user, dict) and raw_user.get("id") and raw_user.get("username"):
                users[str(raw_user["id"])] = str(raw_user["username"])
    records: list[SourceRecord] = []
    for raw in data:
        if not isinstance(raw, dict) or not raw.get("id") or "text" not in raw:
            raise ValueError("Post X privo di id o text")
        external_id = str(raw["id"])
        text = " ".join(str(raw["text"]).split())
        author = users.get(str(raw.get("author_id", "")))
        url = (
            f"https://x.com/{author}/status/{external_id}"
            if author
            else f"https://x.com/i/status/{external_id}"
        )
        records.append(
            SourceRecord(
                source_id=source_id,
                source_type="x",
                external_id=external_id,
                url=url,
                title=text[:160] or f"X post {external_id}",
                text=text,
                published_at=_parse_datetime(raw.get("created_at")),
                author=author,
            )
        )
    return tuple(records)


@dataclass(frozen=True)
class JSONLState:
    file_id: str | None = None
    byte_offset: int = 0
    line_number: int = 0


class JSONLImportConnector:
    def __init__(self, *, source_id: str, path: Path, max_records_per_run: int = 1_000) -> None:
        if not source_id.strip() or max_records_per_run <= 0:
            raise ValueError("source_id e max_records_per_run positivo sono obbligatori")
        self.source_id = source_id
        self.path = path
        self.max_records_per_run = max_records_per_run

    def fetch(self, state: JSONLState | None = None) -> ConnectorBatch[JSONLState]:
        current = state or JSONLState()
        info = self.path.stat()
        file_id = f"{info.st_dev}:{info.st_ino}"
        if current.file_id != file_id or info.st_size < current.byte_offset:
            offset = 0
            line_number = 0
        else:
            offset = current.byte_offset
            line_number = current.line_number

        records: list[SourceRecord] = []
        with self.path.open("rb") as handle:
            handle.seek(offset)
            while len(records) < self.max_records_per_run:
                raw_line = handle.readline()
                if not raw_line:
                    break
                line_number += 1
                offset = handle.tell()
                if not raw_line.strip():
                    continue
                try:
                    value = json.loads(raw_line.decode("utf-8"))
                except (UnicodeDecodeError, json.JSONDecodeError) as exc:
                    raise ValueError(f"JSONL non valido alla linea {line_number}") from exc
                if not isinstance(value, dict):
                    raise ValueError(f"La linea JSONL {line_number} deve essere un oggetto")
                records.append(self._normalize(value))
        return ConnectorBatch(records=tuple(records), state=JSONLState(file_id, offset, line_number))

    def _normalize(self, value: Mapping[str, object]) -> SourceRecord:
        text = " ".join(str(value.get("text") or value.get("content") or value.get("excerpt") or "").split())
        title = " ".join(str(value.get("title") or "").split())
        external_id = _optional_string(value.get("external_id") or value.get("id"))
        url = _optional_string(value.get("url"))
        if external_id is None:
            external_id = url or _stable_id(
                json.dumps(value, sort_keys=True, ensure_ascii=False, default=str)
            )
        if not title:
            title = text[:160] or external_id
        return SourceRecord(
            source_id=self.source_id,
            source_type=_optional_string(value.get("source_type")) or "jsonl",
            external_id=external_id,
            url=url,
            title=title,
            text=text,
            published_at=_parse_datetime(value.get("published_at")),
            author=_optional_string(value.get("author")),
        )
