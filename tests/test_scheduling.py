from datetime import datetime
from zoneinfo import ZoneInfo

from intelligence.scheduling import expected_slot, make_window


ROME = ZoneInfo("Europe/Rome")


def test_slots_follow_rome_local_time() -> None:
    assert expected_slot(datetime(2026, 8, 24, 7, tzinfo=ROME)) == "am"
    assert expected_slot(datetime(2026, 8, 24, 21, tzinfo=ROME)) == "pm"
    assert expected_slot(datetime(2026, 8, 29, 9, tzinfo=ROME)) == "weekly"
    assert expected_slot(datetime(2026, 8, 30, 9, tzinfo=ROME)) is None


def test_windows_use_previous_success_watermark() -> None:
    previous = datetime(2026, 8, 24, 7, tzinfo=ROME)
    window = make_window(
        "pm", datetime(2026, 8, 24, 21, tzinfo=ROME), previous_success_at=previous
    )
    assert window.starts_at == previous
    assert window.idempotency_key == "pm:2026-08-24"


def test_occurrence_key_does_not_change_for_late_retry() -> None:
    on_time = make_window(
        "am", datetime(2026, 8, 24, 7, tzinfo=ROME), previous_success_at=None
    )
    late = make_window(
        "am", datetime(2026, 8, 24, 7, 5, tzinfo=ROME), previous_success_at=None
    )
    assert on_time.idempotency_key == late.idempotency_key
    assert on_time.ends_at == late.ends_at == datetime(2026, 8, 24, 7, tzinfo=ROME)


def test_pm_retry_after_midnight_keeps_previous_occurrence() -> None:
    on_time = make_window(
        "pm", datetime(2026, 8, 24, 21, tzinfo=ROME), previous_success_at=None
    )
    after_midnight = make_window(
        "pm", datetime(2026, 8, 25, 0, 15, tzinfo=ROME), previous_success_at=None
    )

    assert after_midnight.ends_at == on_time.ends_at
    assert after_midnight.idempotency_key == on_time.idempotency_key == "pm:2026-08-24"


def test_weekend_retries_use_last_valid_occurrence_for_each_slot() -> None:
    sunday = datetime(2026, 8, 30, 18, tzinfo=ROME)

    am = make_window("am", sunday, previous_success_at=None)
    pm = make_window("pm", sunday, previous_success_at=None)
    weekly = make_window("weekly", sunday, previous_success_at=None)

    assert am.ends_at == datetime(2026, 8, 28, 7, tzinfo=ROME)
    assert pm.ends_at == datetime(2026, 8, 28, 21, tzinfo=ROME)
    assert weekly.ends_at == datetime(2026, 8, 29, 9, tzinfo=ROME)
    assert am.idempotency_key == "am:2026-08-28"
    assert pm.idempotency_key == "pm:2026-08-28"
    assert weekly.idempotency_key == "weekly:2026-08-29"


def test_occurrences_follow_rome_offset_across_dst_changes() -> None:
    after_spring_change = make_window(
        "am", datetime(2026, 3, 30, 7, 30, tzinfo=ROME), previous_success_at=None
    )
    after_autumn_change = make_window(
        "am", datetime(2026, 10, 26, 7, 30, tzinfo=ROME), previous_success_at=None
    )

    assert after_spring_change.ends_at == datetime(2026, 3, 30, 7, tzinfo=ROME)
    assert after_spring_change.ends_at.utcoffset().total_seconds() == 2 * 60 * 60
    assert after_autumn_change.ends_at == datetime(2026, 10, 26, 7, tzinfo=ROME)
    assert after_autumn_change.ends_at.utcoffset().total_seconds() == 60 * 60


def test_first_am_window_starts_at_previous_evening() -> None:
    window = make_window(
        "am", datetime(2026, 8, 24, 7, tzinfo=ROME), previous_success_at=None
    )
    assert window.starts_at.hour == 21
    assert window.starts_at.day == 23
