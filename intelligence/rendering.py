from __future__ import annotations

import html
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Iterable, Literal


DigestKind = Literal["am", "pm", "weekly"]


@dataclass(frozen=True)
class SourceLink:
    name: str
    url: str
    role: str = "source"


@dataclass(frozen=True)
class DigestEntry:
    event_id: str
    title: str
    tldr: str
    why_it_matters: str
    score: float
    lane: str
    sources: tuple[SourceLink, ...]
    read_minutes: int = 0
    read_decision: str = "tldr"
    bridge: str | None = None
    confidence: str = "medium"


@dataclass(frozen=True)
class Digest:
    kind: DigestKind
    generated_at: datetime
    entries: tuple[DigestEntry, ...]
    period_label: str
    coverage_notes: tuple[str, ...] = field(default_factory=tuple)


def _title(kind: DigestKind) -> str:
    return {
        "am": "AI Intelligence — Mattina",
        "pm": "AI Intelligence — Sera",
        "weekly": "AI Intelligence — Settimana",
    }[kind]


def render_markdown(digest: Digest) -> str:
    lines = [
        f"# {_title(digest.kind)} — {digest.period_label}",
        "",
        f"Generato: {digest.generated_at.isoformat(timespec='minutes')}",
        "",
    ]
    if not digest.entries:
        lines.extend(["Nessuna novita' significativa nel periodo.", ""])
    for index, entry in enumerate(digest.entries, start=1):
        lines.extend(
            [
                f"## {index}. {entry.title}",
                "",
                entry.tldr,
                "",
                f"**Perche' conta:** {entry.why_it_matters}",
                "",
                f"**Corsia:** {entry.lane} · **Confidenza:** {entry.confidence} · "
                f"**Decisione:** {entry.read_decision} ({entry.read_minutes} min)",
            ]
        )
        if entry.bridge:
            lines.extend(["", f"**Ponte:** {entry.bridge}"])
        links = " — ".join(f"[{source.name}]({source.url})" for source in entry.sources)
        lines.extend(["", f"**Fonti:** {links}", ""])
    if digest.coverage_notes:
        lines.extend(["## Note di copertura", ""])
        lines.extend(f"- {note}" for note in digest.coverage_notes)
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def render_html(digest: Digest) -> str:
    parts = [
        "<!doctype html><html><body>",
        f"<h1>{html.escape(_title(digest.kind))} — {html.escape(digest.period_label)}</h1>",
    ]
    if not digest.entries:
        parts.append("<p>Nessuna novita' significativa nel periodo.</p>")
    for entry in digest.entries:
        parts.extend(
            [
                f"<h2>{html.escape(entry.title)}</h2>",
                f"<p>{html.escape(entry.tldr)}</p>",
                f"<p><strong>Perche' conta:</strong> {html.escape(entry.why_it_matters)}</p>",
                "<p><strong>Corsia:</strong> "
                f"{html.escape(entry.lane)} · <strong>Confidenza:</strong> "
                f"{html.escape(entry.confidence)} · <strong>Decisione:</strong> "
                f"{html.escape(entry.read_decision)} ({entry.read_minutes} min)</p>",
            ]
        )
        if entry.bridge:
            parts.append(f"<p><strong>Ponte:</strong> {html.escape(entry.bridge)}</p>")
        links = " — ".join(
            f'<a href="{html.escape(source.url, quote=True)}">{html.escape(source.name)}</a>'
            for source in entry.sources
        )
        parts.append(f"<p><strong>Fonti:</strong> {links}</p>")
    if digest.coverage_notes:
        parts.append("<h2>Note di copertura</h2><ul>")
        parts.extend(f"<li>{html.escape(note)}</li>" for note in digest.coverage_notes)
        parts.append("</ul>")
    parts.append("</body></html>")
    return "\n".join(parts) + "\n"


def write_digest(digest: Digest, outbox: Path) -> tuple[Path, Path]:
    outbox.mkdir(mode=0o700, parents=True, exist_ok=True)
    stamp = digest.generated_at.strftime("%Y%m%d-%H%M")
    base = outbox / f"{stamp}-{digest.kind}"
    markdown_path = base.with_suffix(".md")
    html_path = base.with_suffix(".html")
    markdown_path.write_text(render_markdown(digest), encoding="utf-8")
    html_path.write_text(render_html(digest), encoding="utf-8")
    return markdown_path, html_path


def allocate_reading_budget(
    entries: Iterable[DigestEntry], daily_minutes: int
) -> tuple[DigestEntry, ...]:
    """Keep the best long reads within the daily budget; all other items remain TLDRs."""
    remaining = daily_minutes
    output: list[DigestEntry] = []
    for entry in sorted(entries, key=lambda item: (-item.score, item.event_id)):
        requested = max(0, entry.read_minutes)
        if entry.read_decision == "read_full" and requested <= remaining:
            remaining -= requested
            output.append(entry)
        elif entry.read_decision == "read_full":
            output.append(
                DigestEntry(
                    **{
                        **entry.__dict__,
                        "read_decision": "reading_queue",
                    }
                )
            )
        else:
            output.append(entry)
    return tuple(output)
