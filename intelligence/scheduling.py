from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, time, timedelta
from typing import Literal
from zoneinfo import ZoneInfo


Slot = Literal["am", "pm", "weekly"]

_SCHEDULE: dict[Slot, tuple[frozenset[int], time]] = {
    "am": (frozenset(range(5)), time(7)),
    "pm": (frozenset(range(5)), time(21)),
    "weekly": (frozenset({5}), time(9)),
}


@dataclass(frozen=True)
class ScheduledWindow:
    slot: Slot
    starts_at: datetime
    ends_at: datetime
    idempotency_key: str


def expected_slot(now: datetime, timezone: str = "Europe/Rome") -> Slot | None:
    local = now.astimezone(ZoneInfo(timezone))
    weekday = local.weekday()
    if weekday < 5 and local.hour == 7:
        return "am"
    if weekday < 5 and local.hour == 21:
        return "pm"
    if weekday == 5 and local.hour == 9:
        return "weekly"
    return None


def make_window(
    slot: Slot,
    ends_at: datetime,
    *,
    previous_success_at: datetime | None,
    timezone: str = "Europe/Rome",
) -> ScheduledWindow:
    """Anchor a run to its latest scheduled occurrence and prior successful watermark."""
    zone = ZoneInfo(timezone)
    end = _latest_occurrence(slot, ends_at, zone)
    if previous_success_at is not None:
        start = previous_success_at.astimezone(zone)
    elif slot == "weekly":
        start = end - timedelta(days=7)
    elif slot == "am":
        previous_day = end.date() - timedelta(days=1)
        start = datetime.combine(previous_day, time(21), tzinfo=zone)
    else:
        start = datetime.combine(end.date(), time(7), tzinfo=zone)
    if start >= end:
        raise ValueError("Il watermark precedente deve precedere la fine della finestra")
    return ScheduledWindow(
        slot=slot,
        starts_at=start,
        ends_at=end,
        idempotency_key=f"{slot}:{end.date().isoformat()}",
    )


def _latest_occurrence(slot: Slot, as_of: datetime, zone: ZoneInfo) -> datetime:
    try:
        weekdays, scheduled_time = _SCHEDULE[slot]
    except KeyError as exc:
        raise ValueError(f"Slot non supportato: {slot}") from exc

    local = as_of.astimezone(zone)
    occurrence_date = local.date()
    candidate = datetime.combine(occurrence_date, scheduled_time, tzinfo=zone)
    if candidate > local:
        occurrence_date -= timedelta(days=1)
    while occurrence_date.weekday() not in weekdays:
        occurrence_date -= timedelta(days=1)
    return datetime.combine(occurrence_date, scheduled_time, tzinfo=zone)
