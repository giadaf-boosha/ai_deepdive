# implementation_plan.md — ai_deepdive

> Piano operativo. Suddivisione fasi, owner, deliverable, criteri di accettazione.
> Ultima revisione: 2026-07-06

## Fase 0 — Scaffold (locale)

**Owner**: Giada (lead)
**Stato**: completata

- [x] Init repo locale `~/code/ai_deepdive` con `git init -b main` e remote `giadaf-boosha/ai_deepdive`
- [x] Struttura directory: `digest/2026/04/`, `kb/concetti/`, `config/`, `.github/workflows/`
- [x] `.gitignore` + `LICENSE` (MIT)
- [x] `spec.md` (questa specifica)
- [x] `implementation_plan.md` (questo file)
- [x] `README.md` (front page)

## Fase 1 — Lavoro parallelo team (4 agenti)

Spawno un team di 4 sub-agent specializzati. Ogni agente lavora su un'area indipendente e committa nel filesystem locale.

### Agent A — `kb-architect`
**Deliverable**: 15 file `kb/concetti/<slug>.md` con deep dive italiano 1500-3000 parole.

**Concetti foundation**:
1. `llm.md` — Large Language Model
2. `rag.md` — Retrieval-Augmented Generation
3. `agent.md` — AI Agent
4. `mcp.md` — Model Context Protocol
5. `embedding.md` — Embedding
6. `fine-tuning.md` — Fine-tuning
7. `rlhf.md` — Reinforcement Learning from Human Feedback
8. `tool-use.md` — Tool use / Function calling
9. `context-window.md` — Context window
10. `prompt-engineering.md` — Prompt engineering
11. `agent-harness.md` — Agent harness
12. `inference.md` — Inference (e ottimizzazione)
13. `tokenization.md` — Tokenization
14. `vector-database.md` — Vector database
15. `chain-of-thought.md` — Chain of Thought / Reasoning

**Format ogni file**:
```yaml
---
name: Nome concetto
aliases: [Alias 1, Alias 2]
categoria: [architettura | tecnica | infrastruttura | training]
created: 2026-04-28
last_updated: 2026-04-28
---

# Nome concetto

## Cos'è
## Come funziona
## Varianti / approcci
## Quando usarlo / quando no
## Esempi pratici
## Letture
## Aggiornamenti
```

### Agent B — `sources-curator`
**Deliverable**: `config/sources.yaml` completo.

Per ogni fonte newsletter: verifica esistenza feed RSS (preferito) o URL archive HTML, language, paywall flag, priority.
Per X accounts: selezione 40-60 account broad coverage AI no italiani — ricercatori, founder/CEO AI lab, engineer Anthropic/OpenAI/Google DeepMind, dev rel AI, AI educator, technical writer.

**Format**:
```yaml
newsletters:
  - name: AlphaSignal
    url: https://alphasignal.ai/archive
    rss: https://alphasignal.ai/feed.xml  # se esiste
    type: html  # rss | html
    priority: high
    paywall: false
    language: en
  ...

x_accounts:
  - handle: karpathy
    role: ricercatore
    why: deep dive AI educational, ex Tesla/OpenAI
  ...
```

### Agent C — `digest-writer`
**Deliverable**: `digest/2026/04/28.md` (primo digest manuale di oggi).

Esegue WebFetch live su top 10 fonti, applica filtro editoriale stretto, produce digest in 4 sezioni tematiche (Modelli & framework, Tool & prodotti, Paper & ricerca, Business & strategia). Cluster dedup. Citazioni in IT.

### Agent D — `automation-eng`
**Deliverable**: prompt completo per la routine remota + script di setup.

Scrive `automations/whats-new-daily-prompt.md` con il prompt finale (filosofia editoriale, step 1-7 incluso step di invio email Gmail HTML). Configura body JSON completo per `RemoteTrigger create` con `mcp_connections` per Gmail.

## Fase 2 — Integrazione & QA (lead)

**Owner**: Giada (lead, sequenziale)

- [ ] Review degli output dei 4 agenti
- [ ] Cross-link tra digest e KB (link bidirezionali)
- [ ] Glossario indice in `kb/README.md`
- [ ] Verifica formato YAML sources, parsing test mentale
- [ ] Verifica primo digest 2026-04-28: copertura, qualità editoriale, formato

## Fase 3 — Commit + push + routine remota

**Owner**: Giada (lead)

- [ ] `git add . && git commit -m "chore: initial scaffold + KB seed + first digest"`
- [ ] `git push -u origin main`
- [ ] `RemoteTrigger create` con prompt finale + Gmail MCP
- [ ] Test routine: `RemoteTrigger run` e monitor
- [ ] Aggiornamento `README.md` con link routine

## Fase 4 — Web frontend + radar (2026-05-31)

**Owner**: Giada (lead) · **Stato**: completato (deploy live)

Layer web `web/` deployato su Vercel + routine settimanale radar preparata.

- [x] Scaffold `web/` (Next.js 15 App Router, TS, Tailwind v3, font Geist locali)
- [x] `lib/digest.ts` + `lib/kb.ts`: parser dei digest (frontmatter + sezioni canoniche) e del frontmatter KB
- [x] `lib/relations.ts`: cross-link digest ↔ KB; `lib/markdown.ts`: riscrittura link relativi + TOC
- [x] Route: `/`, `/digest` (+archivio Fuse.js), `/digest/[date]`, `/kb`, `/kb/[slug]`, `/radar`
- [x] `data/models.json`: seed maggio 2026 + dati verificati da fonti ufficiali (Claude Opus 4.8, GPT-5.5, Gemini 3.1 Pro, Microsoft 365 Copilot)
- [x] `output: export` statico → deploy Vercel (`vercel.json` root, build dentro `web/`)
- [x] Deploy live: **[aideepdive.vercel.app](https://aideepdive.vercel.app)** + Git integration (rebuild su push)
- [x] `config/sources.yaml`: +Hugging Face Papers, +TechCrunch categoria AI
- [x] `CLAUDE.md` + `automations/weekly-radar-*`: routine `ai-deepdive-weekly-radar` (ID `trig_017UcxBB68S2FaiQGQWnNh39`, cron domenicale) **creata e attiva** su claude.ai (primo run 2026-06-07)
- [x] README/spec/implementation_plan aggiornati

Acceptance verificati: `npm run build` verde, `tsc --noEmit` pulito, 55 pagine statiche, tutte le route live rispondono 200.

## Criteri di accettazione (Done definition)

Il progetto è considerato live quando tutte queste condizioni sono vere:

1. ✅ Repo `giadaf-boosha/ai_deepdive` ha branch `main` con scaffold + KB seed + primo digest
2. ✅ `spec.md`, `implementation_plan.md`, `README.md` presenti e coerenti
3. ✅ `config/sources.yaml` con 19 newsletter + 40-60 X account documentati
4. ✅ `kb/concetti/` ha 15 file deep dive completi
5. ✅ `digest/2026/04/28.md` esiste con almeno 4 sezioni tematiche
6. ✅ Routine remota `ai-deepdive-daily` creata, abilitata, prossimo run schedulato
7. ✅ Test run della routine completato con successo (commit + email recapitata)
8. ✅ README ha link al routine dashboard e istruzioni per modifica fonti

## Risk / mitigation

| Rischio | Probabilità | Mitigation |
|---|---|---|
| WebFetch su X fallisce 402 | Alta | Fallback WebSearch site:x.com per ogni account; degradare a "X non disponibile" senza abort |
| Feed RSS instabili o cambiati | Media | Sources YAML versionato; agente curator verifica feed live alla prima esecuzione e aggiorna |
| Email Gmail non recapitata (auth scope MCP) | Media | Test in fase 3 prima del go-live; fallback: solo commit, no email |
| KB cresce troppo / qualità degrada | Media | Threshold 3+ fonti / 5+ menzioni-7gg già conservativo; review manuale settimanale primi 30 giorni |
| Conflitti git su main da run multipli | Bassa | Pull rebase before push, abort on conflict, fix manuale |
| Costo run routine | Bassa | Sonnet 4.6 default, prompt ottimizzato, filtro stretto riduce token output |

## Timeline

- **Fase 0** (scaffold): 5 minuti — in corso
- **Fase 1** (team parallel): 30-45 minuti
- **Fase 2** (QA): 10-15 minuti
- **Fase 3** (commit + routine): 5-10 minuti
- **Total**: ~60-75 minuti dal kick-off

Prossimo run automatico: domani 2026-04-29 alle 07:00 Europe/Rome.

## Aggiornamenti

| Data | Cambio |
|---|---|
| 2026-04-28 | Creazione iniziale del piano |
| 2026-05-31 | Fase 4: web frontend Next.js su Vercel (aideepdive.vercel.app), routine radar preparata, fonti HF/TechCrunch aggiunte |
| 2026-05-31 | Routine radar creata/attivata (trig_017UcxBB68S2FaiQGQWnNh39) + primo run di test OK (commit `chore: weekly radar update 2026-05-31`) |
| 2026-05-31 | Redesign UI/UX con brand Boosha (palette avorio/charcoal + arancione, eyebrow mono, stile Apple, responsive verificato desktop+mobile) |
| 2026-06-01 | Identità Boosha da boosha.it (viola #7531E3 primario + arancione secondario, icone outline, gerarchie); copy in ToV; nuova sezione `/claude-code` (sync dal repo claude-code); Radar -> "Modelli e tools AI a confronto" (modelli vs app + catalogo tool + matrice, no finance); routine radar aggiornata al nuovo schema; refresh KB (9 concetti + 3 nuovi) via workflow |
| 2026-06-01 | Radar ampliato: 10 modelli, 15 schede tool ricche + tabella contenitori + decision tree, 38 use case cross-dominio, loghi (favicon) ovunque, link benchmark pinnati (HF, Artificial Analysis); routine radar aggiornata al nuovo schema; cross-ref Claude Code 12/13 |
| 2026-06-01 | Rifiniture: nav (logo Boosha->boosha.it, scrollbar nascosta) e footer/copy allineati al ToV di Giada; versioni tool aggiornate (GPT Image 2, Sora 2, ecc.); matrice "cosa usare per cosa" ridisegnata a card; capitoli Claude Code 24 (Dynamic Workflows) e 25 (/goal) aggiunti al repo claude-code e sincronizzati; refresh dei restanti 8 concetti KB (tutti i 20 a 2026-06-01) + kb/README rigenerato |
| 2026-07-06 | Revisione editoriale completa: host OG corretto (aideepdive), naming sezioni uniforme (Confronto AI, Knowledge base), stat home data-driven, dead code rimosso, mentions_count eliminato (frontmatter KB + parser + prompt routine), brand map e stripLeadingH1 deduplicate, changelog radar renderizzato ("Novita recenti"), docs e prompt routine riallineati ai formati reali (body JSON risincronizzati — da riallineare sulle routine cloud) |
| 2026-07-06 | Nuova sezione "Fondamenti di AI": 28 capitoli in 7 parti da Russell & Norvig AIMA 4a ed. it. (fondamenti/ in root, route /fondamenti, lib/fondamenti.ts, cross-link bidirezionali KB<->capitoli, nav a 5 voci, stat e sezione in home). Generazione via workflow multi-agente con lettura integrale dei PDF; verifica adversariale completata su ~12 capitoli su 28 (lint deterministico ok su tutti; verifica fedelta/verbatim dei restanti da completare al rinnovo del budget agenti) |
