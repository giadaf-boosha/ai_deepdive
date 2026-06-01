# spec.md — ai_deepdive

> Specifica del progetto. Sorgente di verità per scope, requisiti, decisioni di design.
> Ultima revisione: 2026-05-31

## 1. Scopo

`ai_deepdive` è una repo personale di Giada Franceschini che ogni mattina alle 07:00 (Europe/Rome) produce automaticamente:

1. Un **digest giornaliero** in italiano con le novità AI rilevanti delle ultime 24 ore, organizzato in sezioni tematiche.
2. Una **knowledge base** che cresce in modo incrementale estraendo concetti tecnici ricorrenti dal flusso quotidiano e producendo voci enciclopediche in italiano (1500-3000 parole).
3. Un'**email mattutina** in formato HTML con il digest del giorno, recapitata a `giada.f@me.com`.

Il sistema NON è un aggregatore esaustivo. È un curatore editoriale con criterio stretto: pochi segnali ad alto valore, integrati in profondità.

## 2. Stakeholder

- **Owner**: Giada Franceschini (giada.f@me.com)
- **Lettori primari**: Giada + colleghi vicini
- **Visibilità repo**: pubblica (predisposta a contributi futuri ma frame personale)
- **License**: MIT

## 3. Requisiti funzionali

### 3.1 Scraping fonti

Il sistema legge ogni mattina dalle seguenti categorie di fonti (lista canonica in `config/sources.yaml`):

**Newsletter / blog (17 fonti)**:
- TechCrunch (paywall parziale)
- AlphaSignal (alphasignal.ai/archive)
- Every (every.to)
- Unwind AI (unwindai.substack.com)
- Ben's Bites (bensbites.co / Substack)
- Daily Dose of Data Science (dailydoseofds.com)
- Cobus Greyling (cobusgreyling.substack.com)
- Robotic (robotic.substack.com)
- Simon Willison's Weblog (simonwillison.net)
- One Useful Thing (oneusefulthing.org — Ethan Mollick)
- The Week in AI (Substack — XaiGuy)
- Data Pizza (datapizza.it)
- Andreas' Newsletter (Substack)
- G Huntley (ghuntley.com)
- AI Snake Oil (aisnakeoil.substack.com)
- Peter Yang (peteryang.substack.com)
- Exponential View (Azeem Azhar)
- The Information (paywall)

**X accounts (40-60 curated, no italiani)**:
- Sottoinsieme dei following di @montemagno e @GiadaF_ con focus AI
- Categorie: ricercatori, founder/CEO AI lab, engineer Anthropic/OpenAI/Google DeepMind, developer relations AI, AI educator, technical writer
- Lista canonica in `config/sources.yaml` sezione `x_accounts`

### 3.2 Filtro editoriale (TLDR)

**Soglia**: max 10 voci giornaliere, organizzate in 4 sezioni tematiche:

1. **Modelli & framework** — nuovi LLM, release major framework (LangChain, LlamaIndex, DSPy…), aggiornamenti API provider
2. **Tool & prodotti** — nuovi tool/IDE/agent platform, AI coding assistant, prodotti consumer rilevanti
3. **Paper & ricerca** — paper rilevanti (arXiv, blog ricerca), benchmark, scoperte tecniche con sintesi tecnica
4. **Business & strategia** — funding, acquisizioni, mosse strategiche big player, regolamentazione

**Criteri di inclusione** (deve passare almeno UNO):
- Release modello LLM o framework AI
- Lancio prodotto/tool/feature significativa
- Paper rilevante con risultati riproducibili
- Annuncio business strategico (funding, acquisizione, regolamentazione)
- Tutorial concreto su tecnica AI applicata

**Criteri di esclusione** (scarta sempre):
- Bug fix minori, patch sense feature
- Tip generici di produttività AI
- Retweet, hot take, opinioni
- Marketing senza sostanza tecnica
- Contenuto duplicato già presente nel digest archive (ultime 7 entry)

### 3.3 Deduplicazione

Stessa news segnalata da fonti multiple → cluster automatico per topic. Una sola voce nel digest, con elenco fonti: "Segnalata da: AlphaSignal, Ben's Bites, Simon Willison".

### 3.4 Knowledge base

**Trigger di estrazione**: un concetto tecnico viene aggiunto alla KB quando ricorre in **3+ fonti distinte oggi** OPPURE **5+ menzioni totali nelle ultime 7 giornate di digest**.

**Format file** (`kb/concetti/<slug>.md`):
- Italiano deep dive (1500-3000 parole)
- Header con metadata YAML: `name`, `aliases`, `categoria`, `created`, `last_updated`, `mentions_count`
- Sezioni standard: Cos'è, Come funziona, Varianti / approcci, Quando usarlo / quando no, Esempi pratici, Letture, Aggiornamenti
- Sezione "Aggiornamenti" cresce nel tempo (nuove menzioni/articoli aggiungono entry datate)

**Bootstrap**: 15 concetti foundation seed — LLM, RAG, Agent, MCP, Embedding, Fine-tuning, RLHF, Tool use / Function calling, Context window, Prompt engineering, Agent harness, Inference, Tokenization, Vector database, Chain of thought / Reasoning.

### 3.5 Output extra

**Email mattutina via Gmail MCP**:
- Destinatario: `giada.f@me.com`
- Subject: `AI Deepdive — YYYY-MM-DD`
- Body: HTML rendered da markdown del digest del giorno
- Inviata DOPO il commit su main (così l'email contiene link al commit)

**No** RSS feed, **no** newsletter settimanale email, **no** post X automatico (predisposto per v2 ma non in scope ora).

### 3.6 Archive policy

- Digest: archiviato per sempre con gerarchia `digest/YYYY/MM/DD.md`
- KB: file unico per concetto, accumula sezione "Aggiornamenti" nel tempo
- Nessuna rotation/cancellazione automatica

### 3.7 Web frontend (aggiunto 2026-05-31)

Layer web in `web/` (Next.js 15 App Router, TypeScript, Tailwind) deployato su Vercel a [aideepdive.vercel.app](https://aideepdive.vercel.app). Espone il contenuto già prodotto dalle routine come applicazione navigabile.

- **File-based**: legge i markdown da `digest/` e `kb/` a build time (SSG, export statico in `web/out`). Nessun database, nessuna API esterna a runtime.
- **Rebuild automatico** ad ogni push su `main` (Git integration Vercel).
- **Route**: `/` (home), `/digest` (archivio + ricerca Fuse.js + filtro mese), `/digest/[date]` (singolo digest, prev/next, KB correlata), `/kb` (indice + filtro), `/kb/[slug]` (articolo + TOC + digest correlati), `/radar` ("Modelli e tools AI a confronto": modelli vs app, catalogo tool, matrice "cosa usare per cosa", benchmark — analisi generale, no finance), `/claude-code` (guida Claude Code sincronizzata dal repo separato + "What's new").
- **Identità visiva**: brand Boosha da boosha.it — viola `#7531E3` primario + arancione `#FE990B` secondario, Geist + Geist Mono, eyebrow monospace, icone outline, gerarchie H1/H2 chiare, responsive.
- **Sync Claude Code**: `web/scripts/sync-claude-code.mjs` copia docs/ + whats-new-archive dal repo `giadaf-boosha/claude-code` in `web/content/claude-code/` (frontmatter iniettato, link riscritti); contenuto committato, build dal proprio repo.
- **Parser** robusto ai due formati storici dei digest (frontmatter IT del bootstrap 2026-04-28 ed EN auto-generato) e al frontmatter KB.
- **Radar**: dati in `web/data/models.json` (schema TypeScript in `web/lib/models.ts`), aggiornati dalla routine settimanale.

### 3.8 Routine settimanale radar (aggiunto 2026-05-31)

`ai-deepdive-weekly-radar` aggiorna `web/data/models.json` ogni domenica alle 08:00 Europe/Rome (cron `0 6 * * 0` UTC, guard `RADAR_UPDATE`). Ricerca web su fonti ufficiali dei vendor, aggiorna campi + changelog, valida con `tsc --noEmit`, committa e pusha (Vercel ricostruisce). Prompt e body in `automations/weekly-radar-*`. Non modifica file fuori da `web/data/models.json`.

## 4. Requisiti non funzionali

### 4.1 Esecuzione

- **Modello**: routine remota Claude Code (CCR) su Anthropic cloud
- **Schedule**: cron `0 5 * * *` UTC (= 07:00 Europe/Rome ora legale, 06:00 ora solare; user accetta lo shift estate/inverno)
- **Modello LLM**: `claude-sonnet-4-6` (default)
- **Tools allowed**: Bash, Read, Write, Edit, Glob, Grep, WebFetch, WebSearch
- **MCP**: Gmail (per email mattutina)
- **Repo source**: `https://github.com/giadaf-boosha/ai_deepdive`

### 4.2 Resilienza

- **Best effort**: se alcune fonti falliscono (timeout, paywall, errore HTTP), completa il digest con quelle disponibili e elenca le fonti fallite nel commit body.
- Mai abort totale del run a meno che il git push fallisca.
- Se 0 voci rilevanti: digest con messaggio "Nessuna novità significativa", commit comunque per traccia.
- Paywall: skip integrale (TechCrunch, The Information) o solo titoli da RSS parziale.

### 4.3 Git workflow

- **Push diretto su main** — niente branch, niente PR
- **No** `--force`, **no** `--no-verify`
- Pull rebase prima del push
- Se non clean per cambi NON di routine: ABORT
- Se conflitto rebase: ABORT

### 4.4 Identità editoriale

- Lingua: italiano sempre, nomi tecnici inglesi inalterati
- Tono: tecnico, conciso, autoriale (frame personale di Giada)
- Apostrofi ASCII `'` (compatibilità brand_checker)
- Verbi al presente / participi
- No emoji extra, no esclamativi

## 5. Non requisiti (out of scope v1)

- ❌ Scraping live di X via API ufficiale (uso curated list + WebFetch/WebSearch fallback)
- ✅ ~~Frontend / sito statico~~ — aggiunto 2026-05-31: web layer in `web/` su Vercel (vedi 3.7)
- ❌ Database / vector DB per ricerca semantica (KB cercabile via grep; ricerca digest client-side via Fuse.js nel web)
- ❌ Newsletter pubblica / RSS feed pubblicato
- ❌ Post X automatico
- ❌ PDF export della KB
- ❌ Multi-utente / autenticazione

## 6. Decisioni chiave (rationale)

| Decisione | Razionale |
|---|---|
| Routine remota vs GitHub Actions | Coerenza con `whats-new-daily`, zero infra Python da mantenere, agente LLM gestisce nativamente filtro editoriale + scraping web. |
| Push diretto su main | User non ha protection rule; modello già validato sull'altra repo; meno attrito quotidiano. |
| Filtro medio (max 10) vs stretto (max 5) | Coverage AI è più ampia di "Claude Code only", servono più voci per dare valore. Sezioni tematiche aiutano lettura veloce. |
| KB italiano deep dive (1500-3000) | User vuole asset di lungo termine, non scheda riassuntiva; obiettivo è studio personale + condivisione colleghi. |
| Gmail MCP vs solo commit | User vuole spinta giornaliera attiva (push notification), commit da solo è passivo. |
| Archive per sempre | Storico indicizzabile è un asset; storage Git markdown è economico; nessun motivo di pulire. |

## 7. Sicurezza & privacy

- Nessuna credenziale paywall in repo (skip fonti gated)
- `.gitignore` escludes `.env*`
- Email mattutina solo a `giada.f@me.com` (no leak destinatari multipli)
- Visibilità repo pubblica: contenuto è citazione + parafrasi di fonti pubbliche, no scraping di dati gated

## 8. Open question (per v2)

- Verifica se le fonti hanno feed RSS affidabili o richiedono HTML scraping (impatta resilienza)
- Curated X account list: 40-60 nomi finali da definire nello sviluppo (Round 1 della cura)
- Threshold KB (3+ oggi / 5+ in 7gg) potrebbe essere troppo permissivo o troppo stretto: rivalutare dopo 2 settimane di dati
- Eventuale `kb/glossario.md` (indice alfabetico auto-generato) come quality-of-life
