from __future__ import annotations

import json
from datetime import datetime, timezone
from email.message import EmailMessage
from pathlib import Path

import pytest

from intelligence.connectors import (
    ConnectorUsage,
    IMAPConnector,
    IMAPState,
    JSONLImportConnector,
    RSSConnector,
    XBookmarksConnector,
    XBookmarksState,
    XRecentSearchConnector,
    batch_x_handles,
)
from intelligence.http import HTTPResponse, UrllibHTTPTransport


class QueueHTTPTransport:
    def __init__(self, *responses: HTTPResponse) -> None:
        self.responses = list(responses)
        self.calls: list[dict[str, object]] = []

    def request(self, method, url, *, headers=None, query=None):
        self.calls.append(
            {"method": method, "url": url, "headers": dict(headers or {}), "query": dict(query or {})}
        )
        if not self.responses:
            raise AssertionError("Chiamata HTTP inattesa")
        return self.responses.pop(0)


def json_response(value: dict[str, object], status: int = 200) -> HTTPResponse:
    return HTTPResponse(status, {"content-type": "application/json"}, json.dumps(value).encode())


def test_rss_connector_is_conditional_incremental_and_normalizes_html() -> None:
    body = b"""<?xml version="1.0"?>
    <rss version="2.0"><channel><item>
      <guid>entry-1</guid><title>Release</title>
      <link>https://example.com/release</link>
      <description><![CDATA[<p>Nuovo <strong>modello</strong>.</p>]]></description>
      <pubDate>Sat, 22 Aug 2026 08:00:00 +0000</pubDate>
    </item></channel></rss>"""
    transport = QueueHTTPTransport(
        HTTPResponse(200, {"ETag": '"v1"', "Last-Modified": "Sat, 22 Aug 2026 08:10:00 GMT"}, body),
        HTTPResponse(304, {}, b""),
    )
    connector = RSSConnector(source_id="official-blog", url="https://example.com/feed", transport=transport)

    first = connector.fetch()
    second = connector.fetch(first.state)

    assert first.records[0].external_id == "entry-1"
    assert first.records[0].text == "Nuovo modello."
    assert first.records[0].published_at == datetime(2026, 8, 22, 8, tzinfo=timezone.utc)
    assert second.records == ()
    assert transport.calls[1]["headers"]["If-None-Match"] == '"v1"'
    assert transport.calls[1]["headers"]["If-Modified-Since"].endswith("GMT")


class FakeIMAPTransport:
    def __init__(self, validity: int, messages: dict[int, bytes]) -> None:
        self.validity = validity
        self.messages = messages
        self.after_values: list[int] = []

    def select_readonly(self, mailbox: str) -> int:
        assert mailbox == "Newsletter/AI_TOP"
        return self.validity

    def search_uids(self, after_uid: int):
        self.after_values.append(after_uid)
        return tuple(uid for uid in self.messages if uid > after_uid)

    def fetch_rfc822(self, uid: int) -> bytes:
        return self.messages[uid]


def email_bytes() -> bytes:
    message = EmailMessage()
    message["Message-ID"] = "<newsletter-1@example.com>"
    message["Subject"] = "AI weekly"
    message["From"] = "Editor <editor@example.com>"
    message["Date"] = "Sat, 22 Aug 2026 10:00:00 +0200"
    message.set_content("Una sintesi verificata.")
    message.add_alternative(
        '<p>Una sintesi verificata.</p><a href="https://tracker.example/click/42">Track</a>'
        '<a href="https://example.com/article">Leggi</a>'
        '<a href="https://example.com/unsubscribe">Unsubscribe</a>',
        subtype="html",
    )
    return message.as_bytes()


def test_imap_connector_uses_uidvalidity_and_high_watermark() -> None:
    transport = FakeIMAPTransport(42, {11: email_bytes()})
    connector = IMAPConnector(
        source_id="icloud-ai", mailbox="Newsletter/AI_TOP", transport=transport
    )

    first = connector.fetch(IMAPState(uid_validity=42, last_uid=10))
    second = connector.fetch(first.state)

    assert first.records[0].external_id == "<newsletter-1@example.com>"
    assert first.records[0].source_type == "email"
    assert first.records[0].url == "https://example.com/article"
    assert first.state == IMAPState(uid_validity=42, last_uid=11)
    assert second.records == ()
    assert transport.after_values == [10, 11]


def test_imap_connector_resets_cursor_when_uidvalidity_changes() -> None:
    transport = FakeIMAPTransport(99, {2: email_bytes()})
    result = IMAPConnector(
        source_id="icloud-ai", mailbox="Newsletter/AI_TOP", transport=transport
    ).fetch(IMAPState(uid_validity=42, last_uid=100))
    assert transport.after_values == [0]
    assert result.state.last_uid == 2


def test_imap_connector_caps_and_resumes_large_mailbox() -> None:
    transport = FakeIMAPTransport(42, {11: email_bytes(), 12: email_bytes()})
    connector = IMAPConnector(
        source_id="icloud-ai",
        mailbox="Newsletter/AI_TOP",
        transport=transport,
        max_messages_per_run=1,
    )
    first = connector.fetch(IMAPState(uid_validity=42, last_uid=10))
    second = connector.fetch(first.state)
    assert first.state.last_uid == 11
    assert second.state.last_uid == 12


def test_batch_x_handles_is_stable_validated_and_bounded() -> None:
    batches = batch_x_handles(["@OpenAI", "Anthropic", "openai"], max_query_length=25)
    assert batches == ("(from:anthropic)", "(from:openai)")
    assert all(len(query) <= 25 for query in batches)
    with pytest.raises(ValueError, match="Handle X non validi"):
        batch_x_handles(["bad-handle"])


def test_x_recent_search_paginates_and_commits_since_id_only_when_drained() -> None:
    first_page = {
        "data": [
            {"id": "90", "text": "Launch", "author_id": "1", "created_at": "2026-08-22T08:00:00Z"}
        ],
        "includes": {"users": [{"id": "1", "username": "openai"}]},
        "meta": {"newest_id": "99", "next_token": "page-2"},
    }
    second_page = {
        "data": [
            {"id": "80", "text": "Earlier", "author_id": "1", "created_at": "2026-08-22T07:00:00Z"}
        ],
        "includes": {"users": [{"id": "1", "username": "openai"}]},
        "meta": {},
    }
    transport = QueueHTTPTransport(json_response(first_page), json_response(second_page))
    connector = XRecentSearchConnector(
        source_id="x-watchlist",
        handles=["openai"],
        transport=transport,
        authorization="Bearer offline-test",
        max_posts_per_run=10,
        max_pages_per_run=1,
    )
    start = datetime(2026, 8, 22, tzinfo=timezone.utc)

    first = connector.fetch(start_time=start)
    first_cursor = first.state.cursors[0][1]
    assert first_cursor.since_id is None
    assert first_cursor.pending_newest_id == "99"
    assert first_cursor.pagination_token == "page-2"

    second = connector.fetch(first.state)
    second_cursor = second.state.cursors[0][1]
    assert second_cursor.since_id == "99"
    assert second_cursor.pagination_token is None
    assert transport.calls[1]["query"]["next_token"] == "page-2"
    assert [record.url for record in (*first.records, *second.records)] == [
        "https://x.com/openai/status/90",
        "https://x.com/openai/status/80",
    ]
    assert first.usage == ConnectorUsage(post_reads=1, user_reads=1)
    assert second.usage == ConnectorUsage(post_reads=1, user_reads=1)


def test_x_recent_search_usage_counts_raw_duplicates_and_users_across_pages() -> None:
    first_page = {
        "data": [
            {"id": "90", "text": "Launch", "author_id": "1"},
            {"id": "90", "text": "Launch duplicate", "author_id": "1"},
        ],
        "includes": {
            "users": [
                {"id": "1", "username": "openai"},
                {"id": "2", "username": "observer"},
            ]
        },
        "meta": {"newest_id": "90", "next_token": "page-2"},
    }
    second_page = {
        "data": [
            {"id": "90", "text": "Launch repeated", "author_id": "1"},
            {"id": "80", "text": "Earlier", "author_id": "1"},
        ],
        "includes": {"users": [{"id": "1", "username": "openai"}]},
        "meta": {},
    }
    connector = XRecentSearchConnector(
        source_id="x-watchlist",
        handles=["openai"],
        transport=QueueHTTPTransport(json_response(first_page), json_response(second_page)),
        authorization="Bearer offline-test",
        max_posts_per_run=20,
        max_pages_per_run=2,
    )

    result = connector.fetch(start_time=datetime(2026, 8, 22, tzinfo=timezone.utc))

    assert [record.external_id for record in result.records] == ["90", "80"]
    assert result.usage == ConnectorUsage(post_reads=4, user_reads=3)


def test_x_recent_search_enforces_global_hard_post_cap() -> None:
    data = [{"id": str(index), "text": f"Post {index}"} for index in range(10)]
    transport = QueueHTTPTransport(json_response({"data": data, "meta": {"newest_id": "9"}}))
    connector = XRecentSearchConnector(
        source_id="x",
        handles=["openai", "anthropic"],
        transport=transport,
        authorization="Bearer offline-test",
        max_posts_per_run=10,
        max_pages_per_run=10,
        max_query_length=20,
    )
    result = connector.fetch(start_time=datetime(2026, 8, 22, tzinfo=timezone.utc))
    assert len(result.records) == 10
    assert len(transport.calls) == 1
    assert result.state.cursors[1][1].start_time == "2026-08-22T00:00:00Z"


def test_x_bookmarks_resumes_pagination_and_filters_seen_ids() -> None:
    first = {
        "data": [{"id": "2", "text": "Saved", "created_at": "2026-08-22T08:00:00Z"}],
        "meta": {"next_token": "older"},
    }
    older = {
        "data": [{"id": "1", "text": "Older", "created_at": "2026-08-21T08:00:00Z"}],
        "meta": {},
    }
    transport = QueueHTTPTransport(json_response(first), json_response(older))
    connector = XBookmarksConnector(
        source_id="x-bookmarks",
        user_id="123",
        transport=transport,
        authorization="Bearer offline-test",
        max_posts_per_run=1,
        max_pages_per_run=1,
    )
    batch_one = connector.fetch(XBookmarksState())
    batch_two = connector.fetch(batch_one.state)
    assert [record.external_id for record in batch_one.records] == ["2"]
    assert [record.external_id for record in batch_two.records] == ["1"]
    assert batch_two.state.pagination_token is None
    assert transport.calls[1]["query"]["pagination_token"] == "older"
    assert batch_one.usage == ConnectorUsage(owned_post_reads=1)
    assert batch_two.usage == ConnectorUsage(owned_post_reads=1)


def test_x_bookmarks_usage_counts_raw_seen_duplicates_and_users_across_pages() -> None:
    first_page = {
        "data": [{"id": "2", "text": "Already seen", "author_id": "1"}],
        "includes": {"users": [{"id": "1", "username": "openai"}]},
        "meta": {"next_token": "older"},
    }
    second_page = {
        "data": [
            {"id": "2", "text": "Seen again", "author_id": "1"},
            {"id": "1", "text": "New bookmark", "author_id": "2"},
        ],
        "includes": {
            "users": [
                {"id": "1", "username": "openai"},
                {"id": "2", "username": "anthropic"},
            ]
        },
        "meta": {},
    }
    connector = XBookmarksConnector(
        source_id="x-bookmarks",
        user_id="123",
        transport=QueueHTTPTransport(json_response(first_page), json_response(second_page)),
        authorization="Bearer offline-test",
        max_posts_per_run=2,
        max_pages_per_run=2,
    )

    result = connector.fetch(XBookmarksState(seen_ids=("2",)))

    assert [record.external_id for record in result.records] == ["1"]
    assert result.usage == ConnectorUsage(owned_post_reads=3, user_reads=3)
    assert result.usage.post_reads == 0


def test_jsonl_import_is_incremental_and_resets_after_file_replacement(tmp_path: Path) -> None:
    path = tmp_path / "import.jsonl"
    path.write_text(
        json.dumps({"id": "a", "title": "A", "text": "Uno"}) + "\n"
        + json.dumps({"id": "b", "title": "B", "text": "Due"}) + "\n",
        encoding="utf-8",
    )
    connector = JSONLImportConnector(source_id="manual", path=path, max_records_per_run=1)
    first = connector.fetch()
    second = connector.fetch(first.state)
    assert [record.external_id for record in first.records] == ["a"]
    assert [record.external_id for record in second.records] == ["b"]
    assert second.records[0].source_type == "jsonl"


def test_jsonl_import_reports_exact_bad_line(tmp_path: Path) -> None:
    path = tmp_path / "bad.jsonl"
    path.write_text('{"id":"ok"}\nnot-json\n', encoding="utf-8")
    connector = JSONLImportConnector(source_id="manual", path=path)
    with pytest.raises(ValueError, match="linea 2"):
        connector.fetch()


def test_default_http_transport_rejects_non_https_without_network() -> None:
    with pytest.raises(ValueError, match="HTTPS"):
        UrllibHTTPTransport().request("GET", "http://example.com")
