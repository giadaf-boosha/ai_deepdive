from __future__ import annotations

import os
import tomllib
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


class ConfigurationError(ValueError):
    """Raised when a configuration could expose private data or is incomplete."""


DEFAULT_LANES = (
    "research",
    "agents_coding",
    "product",
    "labs_business",
    "business_strategy",
    "marketing",
    "education",
    "philosophy",
    "neuroscience",
    "linguistics_semantics",
    "mathematics",
    "management_leadership",
    "spatial_embodied_ai",
)


@dataclass(frozen=True)
class Settings:
    data_dir: Path
    public_repo_root: Path
    timezone: str = "Europe/Rome"
    owner_email: str = "giada.f@me.com"
    daily_reading_minutes: int = 30
    max_digest_events: int = 10
    recipient_allowlist: tuple[str, ...] = ("giada.f@me.com",)
    smtp_host: str = "smtp.gmail.com"
    smtp_port: int = 465
    x_max_posts_per_run: int = 300
    x_max_pages_per_run: int = 10
    x_monthly_budget_usd: float = 25.0
    x_post_read_unit_usd: float = 0.005
    x_owned_read_unit_usd: float = 0.001
    x_user_read_unit_usd: float = 0.010
    lanes: tuple[str, ...] = DEFAULT_LANES
    bridge_topics: tuple[str, ...] = field(default_factory=tuple)

    @property
    def database_path(self) -> Path:
        return self.data_dir / "intelligence.sqlite3"

    @property
    def outbox_dir(self) -> Path:
        return self.data_dir / "outbox"


def _inside(path: Path, parent: Path) -> bool:
    try:
        path.relative_to(parent)
        return True
    except ValueError:
        return False


def validate_private_data_dir(data_dir: Path, public_repo_root: Path) -> Path:
    resolved_data = data_dir.expanduser().resolve()
    resolved_repo = public_repo_root.expanduser().resolve()
    if resolved_data == resolved_repo or _inside(resolved_data, resolved_repo):
        raise ConfigurationError(
            "AI_INTEL_DATA_DIR deve essere esterna al repository pubblico"
        )
    if resolved_data == Path(resolved_data.anchor):
        raise ConfigurationError("AI_INTEL_DATA_DIR non puo' essere la root del filesystem")
    return resolved_data


def load_settings(
    config_path: str | Path,
    *,
    public_repo_root: str | Path | None = None,
    environ: dict[str, str] | None = None,
) -> Settings:
    env = os.environ if environ is None else environ
    path = Path(config_path)
    with path.open("rb") as handle:
        raw: dict[str, Any] = tomllib.load(handle)

    root = Path(public_repo_root or Path(__file__).resolve().parents[1])
    value = env.get("AI_INTEL_DATA_DIR")
    if not value:
        raise ConfigurationError(
            "AI_INTEL_DATA_DIR e' obbligatoria e deve puntare a storage privato esterno"
        )
    data_dir = validate_private_data_dir(Path(value), root)
    system = raw.get("system", {})
    delivery = raw.get("delivery", {})
    limits = raw.get("cost_limits", {})
    editorial = raw.get("editorial", {})

    reading_minutes = int(system.get("daily_reading_minutes", 30))
    if reading_minutes <= 0:
        raise ConfigurationError("daily_reading_minutes deve essere positivo")
    max_events = int(system.get("max_digest_events", 10))
    if not 1 <= max_events <= 30:
        raise ConfigurationError("max_digest_events deve essere tra 1 e 30")
    monthly_budget = float(limits.get("x_monthly_budget_usd", 25.0))
    post_unit = float(limits.get("x_post_read_unit_usd", 0.005))
    owned_unit = float(limits.get("x_owned_read_unit_usd", 0.001))
    user_unit = float(limits.get("x_user_read_unit_usd", 0.010))
    if monthly_budget <= 0 or post_unit <= 0 or owned_unit <= 0 or user_unit <= 0:
        raise ConfigurationError("Budget e costi unitari X devono essere positivi")

    return Settings(
        data_dir=data_dir,
        public_repo_root=root.resolve(),
        timezone=str(system.get("timezone", "Europe/Rome")),
        owner_email=str(system.get("owner_email", "giada.f@me.com")),
        daily_reading_minutes=reading_minutes,
        max_digest_events=max_events,
        recipient_allowlist=tuple(delivery.get("recipient_allowlist", ["giada.f@me.com"])),
        smtp_host=str(delivery.get("smtp_host", "smtp.gmail.com")),
        smtp_port=int(delivery.get("smtp_port", 465)),
        x_max_posts_per_run=int(limits.get("x_max_posts_per_run", 300)),
        x_max_pages_per_run=int(limits.get("x_max_pages_per_run", 10)),
        x_monthly_budget_usd=monthly_budget,
        x_post_read_unit_usd=post_unit,
        x_owned_read_unit_usd=owned_unit,
        x_user_read_unit_usd=user_unit,
        lanes=tuple(editorial.get("lanes", DEFAULT_LANES)),
        bridge_topics=tuple(editorial.get("bridge_topics", ())),
    )


def prepare_private_directories(settings: Settings) -> None:
    settings.data_dir.mkdir(mode=0o700, parents=True, exist_ok=True)
    settings.outbox_dir.mkdir(mode=0o700, parents=True, exist_ok=True)
    try:
        settings.data_dir.chmod(0o700)
        settings.outbox_dir.chmod(0o700)
    except OSError:
        # Alcuni filesystem non supportano permessi POSIX; la separazione dal repo resta attiva.
        pass
