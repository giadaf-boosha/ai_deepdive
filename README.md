# ai_deepdive

> La mia raccolta quotidiana di segnali AI, in italiano. Curata da una routine Claude Code, aggiornata ogni mattina alle 07:00 (Europe/Rome).

**Sito web**: [aideepdive.vercel.app](https://aideepdive.vercel.app) — digest, knowledge base e radar modelli AI navigabili.

## Cosa trovi qui

Due tracce parallele:

1. **[`digest/`](./digest)** — Un file markdown al giorno con i segnali AI rilevanti delle ultime 24 ore. Organizzato in 4 sezioni: Modelli & framework, Tool & prodotti, Paper & ricerca, Business & strategia. Max 10 voci, criterio editoriale stretto.
2. **[`kb/`](./kb)** — Knowledge base in crescita. Concetti tecnici (LLM, RAG, agent harness, MCP, RLHF…) raccontati in italiano deep dive (1500-3000 parole), aggiornati man mano che ricorrono nei digest.

## Come funziona

Ogni mattina alle **07:00 Europe/Rome** una routine remota Claude Code (girata su Anthropic cloud) esegue questi step:

1. **Scrape**: legge ~17 newsletter/blog + 40-60 account X curati (lista canonica in [`config/sources.yaml`](./config/sources.yaml))
2. **Filtra**: applica criterio editoriale stretto — solo segnali ad alto valore (release modello, lancio tool, paper rilevante, mossa strategica). Scarta fix minori, tip generici, marketing senza sostanza.
3. **Cluster**: raggruppa news segnalate da fonti multiple in una singola voce con elenco fonti.
4. **Digest**: produce `digest/YYYY/MM/DD.md` con TLDR italiano in 4 sezioni tematiche.
5. **Knowledge base**: se un concetto tecnico ricorre in **3+ fonti oggi** o **5+ menzioni nelle ultime 7 giornate**, crea o aggiorna il file `kb/concetti/<slug>.md`.
6. **Commit & push**: push diretto su `main` (no PR).
7. **Email**: invia il digest in HTML a `giada.f@me.com` via Gmail MCP.

## Web frontend

Un layer web (Next.js 15, App Router, TypeScript, Tailwind) in [`web/`](./web) espone tutto il contenuto come applicazione navigabile, deployata su Vercel: **[aideepdive.vercel.app](https://aideepdive.vercel.app)**.

- **File-based, zero database**: legge a build time i markdown da `digest/` e `kb/` (SSG puro, export statico).
- **Rebuild automatico ad ogni push** su `main` via Git integration Vercel.
- **Route**:
  - `/` — homepage: ultimo digest, ultimi concetti KB, radar rapido.
  - `/digest` — archivio cronologico con ricerca full-text (Fuse.js) e filtro per mese.
  - `/digest/[date]` — singolo digest con sezioni tematiche, navigazione prev/next, concetti KB correlati.
  - `/kb` — indice dei concetti con filtro per categoria.
  - `/kb/[slug]` — articolo con TOC auto-generato, digest che lo citano, concetti correlati.
  - `/radar` — mappatura modelli AI (Claude, ChatGPT, Gemini, Copilot): panoramica, benchmark, casi d'uso, prezzi, privacy & enterprise.

Sviluppo locale: `cd web && npm install && npm run dev`. Build: `npm run build` (output statico in `web/out`).

I dati del radar vivono in [`web/data/models.json`](./web/data/models.json), aggiornati settimanalmente dalla routine `ai-deepdive-weekly-radar` (vedi [`automations/`](./automations)).

## Struttura repo

```
ai_deepdive/
├── README.md                 ← questo file
├── spec.md                   ← specifica completa
├── implementation_plan.md    ← piano di lavoro
├── CLAUDE.md                 ← istruzioni progetto + task routine radar
├── LICENSE                   ← MIT
├── config/
│   └── sources.yaml          ← lista newsletter + X accounts (sorgente di verità)
├── automations/
│   ├── whats-new-daily-prompt.md  + routine-body.json        ← routine giornaliera
│   └── weekly-radar-prompt.md     + weekly-radar-body.json   ← routine settimanale radar
├── digest/
│   └── YYYY/MM/DD.md         ← un file per giorno, archiviato per sempre
├── kb/
│   ├── README.md             ← indice alfabetico KB
│   └── concetti/
│       └── <slug>.md         ← un file per concetto tecnico
└── web/                      ← layer Next.js deployato su Vercel (app/, lib/, components/, data/)
```

## Fonti monitorate

**Newsletter / blog / paper**:
TechCrunch (categoria AI) · Hugging Face Papers · AlphaSignal · Every · Unwind AI · Ben's Bites · Daily Dose of Data Science · Cobus Greyling · Robotic · Simon Willison · One Useful Thing (Ethan Mollick) · The Week in AI · Data Pizza · Andreas' Newsletter · G Huntley · AI Snake Oil · Peter Yang · Exponential View · The Information.

**X accounts**: 40-60 account curati AI (ricercatori, founder/CEO AI lab, engineer Anthropic/OpenAI/Google DeepMind, dev rel, AI educator, technical writer). Lista completa in `config/sources.yaml`.

## Come modificare le fonti

Aggiungi/togli voci direttamente in [`config/sources.yaml`](./config/sources.yaml). Dal commit successivo la routine userà la nuova lista.

## Stack tecnico

- **Esecuzione**: routine remota Claude Code (CCR) su Anthropic cloud
- **Modello LLM**: `claude-sonnet-4-6`
- **Schedule**: cron `0 5 * * *` UTC (= 07:00 Europe/Rome ora legale)
- **Storage**: markdown nel repo Git (no DB)
- **Email**: Gmail MCP (HTML rendered)
- **Visibilità**: pubblica, MIT license

## Stato

- ✅ Scaffold + KB seed + primo digest manuale: 2026-04-28
- ✅ Routine giornaliera attiva: `ai-deepdive-daily` (ID: `trig_01U38R2BbWd86ZSZvv9uv5Jy`) — digest + KB ogni mattina alle 07:00
- ✅ Web frontend live su Vercel: [aideepdive.vercel.app](https://aideepdive.vercel.app) (rebuild automatico ad ogni push)
- ✅ Fonti Hugging Face Papers + TechCrunch (categoria AI) aggiunte a `config/sources.yaml`
- 🛠️ Routine settimanale radar `ai-deepdive-weekly-radar` preparata in `automations/` — da creare su claude.ai/code/routines (body pronto, cron domenicale)

Dashboard routine daily: https://claude.ai/code/routines/trig_01U38R2BbWd86ZSZvv9uv5Jy

## Identità editoriale

- Italiano sempre, nomi tecnici inglesi inalterati
- Tono tecnico, conciso, autoriale (non marketing, non aggregatore)
- Pochi segnali ad alto valore > coverage esaustiva
- Fonti citate sempre con link diretto

## Contributi

Repo personale. Issue / PR benvenuti se trovi errori, suggerisci fonti da aggiungere/togliere, o vuoi proporre concetti per la KB.

## Licenza

MIT — vedi [LICENSE](./LICENSE).
