from __future__ import annotations

import hashlib
import json
from dataclasses import asdict, dataclass
from datetime import datetime
from pathlib import Path


class PublishingBlocked(RuntimeError):
    """Raised when a candidate has not passed the public-output gates."""


@dataclass(frozen=True)
class RightsItem:
    url: str
    source: str
    access_class: str
    usage: str
    excerpt_words: int = 0


@dataclass(frozen=True)
class ArticlePackage:
    title: str
    subtitle: str
    markdown: str
    audience: str
    thesis: str
    rights: tuple[RightsItem, ...]
    fact_reviewed: bool
    rights_reviewed: bool


def export_substack_package(package: ArticlePackage, target: Path) -> Path:
    """Create an offline review package. It never calls Substack."""
    if not package.fact_reviewed or not package.rights_reviewed:
        raise PublishingBlocked("Fact review e rights review sono obbligatorie")
    prohibited = [item for item in package.rights if item.usage == "raw_republication"]
    if prohibited:
        raise PublishingBlocked("Il pacchetto contiene ripubblicazione raw non consentita")

    target.mkdir(mode=0o700, parents=True, exist_ok=True)
    article_path = target / "article.md"
    manifest_path = target / "manifest.json"
    checklist_path = target / "QA-CHECKLIST.md"
    article_path.write_text(
        f"# {package.title}\n\n_{package.subtitle}_\n\n{package.markdown.rstrip()}\n",
        encoding="utf-8",
    )
    digest = hashlib.sha256(article_path.read_bytes()).hexdigest()
    manifest = {
        "created_at": datetime.now().astimezone().isoformat(),
        "publish_mode": "manual_only",
        "title": package.title,
        "audience": package.audience,
        "thesis": package.thesis,
        "article_sha256": digest,
        "fact_reviewed": package.fact_reviewed,
        "rights_reviewed": package.rights_reviewed,
        "rights": [asdict(item) for item in package.rights],
    }
    manifest_path.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    checklist_path.write_text(
        "# QA prima della pubblicazione manuale\n\n"
        "- [ ] Titolo, target e tesi sono coerenti.\n"
        "- [ ] Ogni claim fattuale ha una fonte primaria o una conferma autorevole.\n"
        "- [ ] Inferenze e opinioni sono etichettate.\n"
        "- [ ] Citazioni ed estratti rispettano il rights manifest.\n"
        "- [ ] Link, immagini, alt text e crediti sono verificati.\n"
        "- [ ] Preview desktop/mobile controllata in Substack.\n"
        "- [ ] Test email inviato solo all'autrice.\n"
        "- [ ] Pubblicazione finale decisa manualmente dall'autrice.\n",
        encoding="utf-8",
    )
    return target


def public_speaking_template(title: str, audience: str, thesis: str) -> str:
    return f"""# {title}

## Audience
{audience}

## Tesi in una frase
{thesis}

## Hook

## Definizioni indispensabili

## Tre passaggi logici
1. 
2. 
3. 

## Evidenze e fonti

## Controargomento piu' forte

## Ponti interdisciplinari
- Meccanismo condiviso:
- Dove l'analogia si rompe:

## Esempio concreto

## So what

## Versione 60 secondi

## Versione 5 minuti

## Versione 20 minuti

## Domande previste

## Frase memorabile originale

## Prova e feedback
"""
