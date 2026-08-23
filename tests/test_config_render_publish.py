from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

import pytest

from intelligence.config import ConfigurationError, load_settings
from intelligence.delivery import DeliveryBlocked, SMTPConfig, deliver_email
from intelligence.notion_export import export_notion_projection
from intelligence.publishing import (
    ArticlePackage,
    PublishingBlocked,
    RightsItem,
    export_substack_package,
)
from intelligence.rendering import (
    Digest,
    DigestEntry,
    SourceLink,
    allocate_reading_budget,
    render_html,
    render_markdown,
)


CONFIG = """
[system]
daily_reading_minutes = 30
max_digest_events = 10
[delivery]
recipient_allowlist = ["giada.f@me.com"]
"""


def test_private_data_cannot_live_in_public_repo(tmp_path: Path) -> None:
    config = tmp_path / "settings.toml"
    config.write_text(CONFIG, encoding="utf-8")
    with pytest.raises(ConfigurationError):
        load_settings(
            config,
            public_repo_root=tmp_path,
            environ={"AI_INTEL_DATA_DIR": str(tmp_path / "private-data")},
        )


def test_settings_require_explicit_private_data_dir(tmp_path: Path) -> None:
    config = tmp_path / "settings.toml"
    config.write_text(CONFIG, encoding="utf-8")
    with pytest.raises(ConfigurationError):
        load_settings(config, public_repo_root=tmp_path, environ={})


def _entry(event_id: str, score: float, minutes: int) -> DigestEntry:
    return DigestEntry(
        event_id=event_id,
        title=f"Evento {event_id}",
        tldr="Sintesi verificata.",
        why_it_matters="Cambia una decisione operativa.",
        score=score,
        lane="research",
        sources=(SourceLink("Fonte primaria", "https://example.com/source"),),
        read_minutes=minutes,
        read_decision="read_full",
    )


def test_reading_budget_is_hard_limit() -> None:
    allocated = allocate_reading_budget((_entry("a", 9, 20), _entry("b", 8, 20)), 30)
    assert [item.read_decision for item in allocated] == ["read_full", "reading_queue"]


def test_digest_renderers_include_sources_and_escape_html() -> None:
    entry = _entry("a", 9, 10)
    unsafe = DigestEntry(**{**entry.__dict__, "title": "<script>alert(1)</script>"})
    digest = Digest(
        kind="am",
        generated_at=datetime.fromisoformat("2026-08-24T07:00:00+02:00"),
        entries=(unsafe,),
        period_label="24 agosto 2026",
    )
    markdown = render_markdown(digest)
    rendered_html = render_html(digest)
    assert "https://example.com/source" in markdown
    assert "<script>" not in rendered_html
    assert "&lt;script&gt;" in rendered_html


def test_email_defaults_to_local_preview_and_enforces_allowlist(tmp_path: Path) -> None:
    config = SMTPConfig("smtp.example", 465, "", "", "giada.f@me.com", ("giada.f@me.com",))
    preview = deliver_email(
        config,
        recipient="giada.f@me.com",
        subject="Test",
        html_body="<p>Test</p>",
        send=False,
        outbox=tmp_path,
    )
    assert preview.exists()
    with pytest.raises(DeliveryBlocked):
        deliver_email(
            config,
            recipient="newsletter@example.com",
            subject="No",
            html_body="<p>No</p>",
            send=False,
            outbox=tmp_path,
        )


def test_substack_export_is_manual_and_rights_gated(tmp_path: Path) -> None:
    package = ArticlePackage(
        title="Titolo",
        subtitle="Sottotitolo",
        markdown="Testo originale.",
        audience="Leader",
        thesis="Una tesi.",
        rights=(RightsItem("https://example.com", "Example", "public", "paraphrase"),),
        fact_reviewed=True,
        rights_reviewed=True,
    )
    result = export_substack_package(package, tmp_path / "substack")
    manifest = json.loads((result / "manifest.json").read_text(encoding="utf-8"))
    assert manifest["publish_mode"] == "manual_only"
    assert (result / "QA-CHECKLIST.md").exists()

    blocked = ArticlePackage(
        **{**package.__dict__, "rights_reviewed": False}
    )
    with pytest.raises(PublishingBlocked):
        export_substack_package(blocked, tmp_path / "blocked")


def test_notion_projection_drops_private_unknown_fields(tmp_path: Path) -> None:
    path = export_notion_projection(
        [{"id": "1", "title": "T", "human_notes": "N", "raw_body": "secret"}],
        tmp_path / "notion.json",
        view="Radar & Reading",
    )
    payload = json.loads(path.read_text(encoding="utf-8"))
    assert payload["records"][0] == {"id": "1", "title": "T", "human_notes": "N"}
