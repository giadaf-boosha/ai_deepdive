# implementation_plan.md — ai_deepdive

> Piano operativo. Suddivisione fasi, owner, deliverable, criteri di accettazione.
> Ultima revisione: 2026-04-28

## Fase 0 — Scaffold (locale)

**Owner**: Giada (lead)
**Stato**: in corso

- [x] Init repo locale `~/code/ai_deepdive` con `git init -b main` e remote `giadaf-boosha/ai_deepdive`
- [x] Struttura directory: `digest/2026/04/`, `kb/concetti/`, `config/`, `.github/workflows/`
- [x] `.gitignore` + `LICENSE` (MIT)
- [x] `spec.md` (questa specifica)
- [ ] `implementation_plan.md` (questo file)
- [ ] `README.md` (front page)

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
mentions_count: 0
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

## Criteri di accettazione (Done definition)

Il progetto è considerato live quando tutte queste condizioni sono vere:

1. ✅ Repo `giadaf-boosha/ai_deepdive` ha branch `main` con scaffold + KB seed + primo digest
2. ✅ `spec.md`, `implementation_plan.md`, `README.md` presenti e coerenti
3. ✅ `config/sources.yaml` con 17 newsletter + 40-60 X account documentati
4. ✅ `kb/concetti/` ha 15 file deep dive completi
5. ✅ `digest/2026/04/28.md` esiste con almeno 4 sezioni tematiche
6. ✅ Routine remota `whats-new-ai-deepdive` creata, abilitata, prossimo run schedulato
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
