from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import Iterable, Mapping


SYSTEM_OWNED_FIELDS = frozenset(
    {"id", "title", "url", "score", "lane", "provenance", "updated_at"}
)
HUMAN_OWNED_FIELDS = frozenset(
    {"human_status", "human_notes", "read", "editorial_decision", "rehearsal_feedback"}
)


def export_notion_projection(
    records: Iterable[Mapping[str, object]], target: Path, *, view: str
) -> Path:
    """Export a bounded projection for an official Notion integration to consume."""
    allowed = SYSTEM_OWNED_FIELDS | HUMAN_OWNED_FIELDS
    rows = []
    for record in records:
        rows.append({key: value for key, value in record.items() if key in allowed})
    payload = {
        "view": view,
        "generated_at": datetime.now().astimezone().isoformat(),
        "ownership": {
            "system": sorted(SYSTEM_OWNED_FIELDS),
            "human": sorted(HUMAN_OWNED_FIELDS),
        },
        "records": rows,
    }
    target.parent.mkdir(mode=0o700, parents=True, exist_ok=True)
    target.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return target
