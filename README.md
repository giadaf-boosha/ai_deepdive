# ai_deepdive / AI Intelligence System

Sistema privato-by-design per trasformare fonti AI eterogenee in eventi deduplicati, decisioni di lettura e conoscenza persistente. Il codice e' pubblico; dati acquisiti, note e output personali devono vivere fuori dal repository.

Il sito storico resta online su [aideepdive.vercel.app](https://aideepdive.vercel.app). I contenuti in `digest/`, `kb/`, `fondamenti/` e la routine Claude Code sono una baseline legacy: utili come corpus e interfaccia, ma non sono la fonte canonica della nuova pipeline.

## Perche' una v2

L'audit del 23 agosto 2026 ha rilevato che il sistema precedente era un prompt monolitico: feed spesso irraggiungibili, X quasi assente, fallback web non governato, deduplica limitata a sette file e nessun watermark. La v2 separa acquisizione, evento, giudizio editoriale, knowledge e delivery in componenti testabili.

Le decisioni complete sono in [spec.md](./spec.md); audit e strategie sono in [`docs/`](./docs); avanzamento e rollout sono in [implementation_plan.md](./implementation_plan.md).

## Architettura

```text
RSS / IMAP / X API / Bookmarks / JSONL
                   |
                   v
 Source -> Document -> Event -> Claim / Evidence
                   |              |
                   v              v
              Ranking        Concept / Bridge / Thesis
                   |
                   v
      Digest AM/PM/weekly + Reading queue
                   |
          +--------+---------+
          |                  |
       Email privata      Export controllati
                         Notion / talk / Substack
```

Principi:

- `AI_INTEL_DATA_DIR` obbligatoria e sempre esterna al repo;
- un evento puo' avere piu' fonti, ma compare una sola volta;
- fonte primaria, conferma e analisi hanno ruoli distinti;
- modello editoriale sostituibile; baseline deterministica offline;
- massimo 30 minuti di letture complete al giorno;
- X watchlist via API ufficiale con ledger costi atomico, For You tramite bookmark manuale, niente browser scraping;
- Substack solo tramite pacchetto revisionato e pubblicazione manuale;
- rete, invio e costi disabilitati nei test.

## Quickstart locale sicuro

Richiede Python 3.11+ e non ha dipendenze runtime esterne.

```bash
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -e .

export AI_INTEL_DATA_DIR=/percorso/privato/ai-intelligence-data
ai-intel --config config/intelligence.example.toml init
ai-intel --config config/intelligence.example.toml status
```

Per un ingest offline riproducibile:

```bash
ai-intel --config config/intelligence.example.toml ingest-jsonl ./miei-input.jsonl
ai-intel --config config/intelligence.example.toml curate
ai-intel --config config/intelligence.example.toml render --slot am
```

Il comando `render` scrive Markdown, HTML e preview `.eml` nell'outbox privata. Non invia nulla. L'invio richiede `--send`, credenziali SMTP in environment e destinatario presente nell'allowlist.

Le delivery e le reservation costi hanno ledger e comandi di riconciliazione manuale; i casi ambigui restano bloccati e non vengono ritentati automaticamente. Vedi [`docs/operations.md`](./docs/operations.md).

## Schedule prevista

- lunedi-venerdi 07:00 Europe/Rome: digest mattutino;
- lunedi-venerdi 21:00 Europe/Rome: digest serale;
- sabato 09:00 Europe/Rome: top 10 settimanale e long read.

La schedule non va attivata prima di cinque giorni di shadow run manuali. Le finestre usano il watermark dell'ultima esecuzione riuscita, quindi non duplicano la stessa notizia fra mattina e sera.

## X: decisione operativa

- watchlist misurabile: X Recent Search con query aggregate, `since_id` e hard cap;
- discovery: xAI X Search solo dopo benchmark;
- vero For You: Giada salva il post in una cartella bookmark, poi la pipeline usa Bookmarks API;
- Grok.com: ricerca manuale esplorativa;
- Grok Bot: orchestrazione, non automazione del browser X;
- X MCP: adapter possibile, con gli stessi costi dell'API e allowlist stretta.

Il benchmark e i criteri di accettazione sono in [`docs/x-retrieval-strategy.md`](./docs/x-retrieval-strategy.md).

## Knowledge, Notion e Substack

Il database privato e' la fonte canonica. Notion riceve una proiezione limitata con ownership dei campi; non contiene automaticamente raw paywalled. Gli articoli Substack vengono esportati come `article.md`, `manifest.json` e checklist. Il sistema non usa API private Substack e non pubblica né invia alla mailing list.

La precedente `scripts/substack/publish.py` e' legacy e non deve essere eseguita. Resta temporaneamente per non introdurre una rimozione distruttiva nello stesso cambiamento.

## Test

```bash
python3 -m pytest
```

I test verificano storage esterno, idempotenza, connector offline, hard cap X, schedule Europe/Rome, budget lettura, escaping HTML, allowlist email e rights gate.

## Struttura principale

```text
intelligence/                 pipeline v2
config/intelligence.example.toml
tests/                        test offline
docs/                         audit e decision record
digest/ kb/ fondamenti/ web/  baseline legacy
automations/                  routine legacy congelate
note-implementazione.md       decisioni e deviazioni del lavoro
```

## Stato

MVP implementato e in fase di QA locale. Nessuna schedule, API a pagamento, email live, Notion live o pubblicazione Substack e' stata attivata da questa implementazione.
