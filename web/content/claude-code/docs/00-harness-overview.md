---
title: "00 — Agent Harness Overview"
slug: 00-harness-overview
order: "000"
source: https://github.com/giadaf-boosha/claude-code/blob/main/docs/00-harness-overview.md
---
---

## 0.1 Perche' questo capitolo esiste

Nel 2023 si parlava di **prompt engineering** ("come scrivere il prompt giusto").
Nel 2024 si e' iniziato a parlare di **context engineering** ("come dare all'LLM il contesto giusto").
Nel **febbraio 2026** Mitchell Hashimoto (creatore di HashiCorp, Vagrant, Ghostty) ha messo un nome al livello successivo: **harness engineering**.

Il post fondativo, "[We Need to Talk About 'Agent Harnesses'](https://mitchellh.com/writing/agent-harnesses)" del 5 febbraio 2026, ha consolidato un'osservazione che molti facevano da mesi:

> **Agent = LLM + Harness**
>
> Il modello e' la materia prima. L'**harness** e' tutto cio' che gli sta intorno: contesto, tool, memoria, orchestrazione, guardrail, error recovery. **L'80% della qualita' di un agent dipende dall'harness, non dal modello.**

Sei giorni dopo, **OpenAI ha rivelato che 1M di righe di codice del progetto Codex erano state generate dall'agent — zero scritte manualmente** (5 mesi). Il messaggio: a parita' di modello, l'harness fa la differenza.

> Fonte: dossier-conceptual-harness.md sintesi.

Questo capitolo definisce che cos'e' un harness, perche' e' importante e come Claude Code e' un'incarnazione concreta di questo paradigma.

---

## 0.2 Definizione

> "An agent harness is the orchestration layer that surrounds a language model and turns it into something that can do work."
> — Mitchell Hashimoto, 5 feb 2026

In termini operativi:

```
Agent = LLM + Harness

dove Harness =
  Context layer       (cosa il modello vede)
+ Tool layer          (cosa il modello puo' fare)
+ Memory layer        (cosa il modello ricorda)
+ Orchestration       (chi decide cosa, quando)
+ Guardrails          (cosa NON puo' fare)
+ State persistence   (cosa sopravvive al crash)
+ Error recovery      (cosa fare quando qualcosa rompe)
```

**Cosa NON e' un harness**:
- Non e' un wrapper di prompt template (quello e' prompt engineering, livello 1)
- Non e' solo "context window management" (quello e' context engineering, livello 2)
- Non e' un'API call sequence (quello e' un workflow scriptato)

**Un harness include un'agent loop** (vedi [14b — ReAct + agent loop](/claude-code/14b-agent-loop-react)) che decide a runtime quale tool chiamare, quando memorizzare, quando chiedere conferma all'utente.

---

## 0.3 Tre analogie didattiche

### Analogia 1 — Cavallo e redini
- **Cavallo** = LLM. Forza bruta, ma senza direzione cammina dove vuole.
- **Redini** = Harness. Permettono al cavaliere (utente) di indirizzare la forza in modo controllato.
- Senza redini, il cavallo va o non va a seconda dell'umore. Con le redini, l'utente puo' usare il cavallo per arare un campo, fare consegne, vincere una corsa.

### Analogia 2 — OS / CPU / RAM
- **CPU** = LLM. Esegue il calcolo.
- **OS** = Harness. Gestisce risorse, schedula task, fornisce librerie, coordina I/O.
- **RAM** = Context window. Veloce ma limitata.
- **Disk** = Memory persistente (CLAUDE.md, auto-memory).
- L'utente non programma direttamente la CPU: lo fa attraverso l'OS. Stessa cosa per LLM via harness.

### Analogia 3 — Ponteggi (scaffolding)
- **L'edificio** = il software finale.
- **Operai** = LLM. Lavorano in altezza, producono.
- **Ponteggi** = Harness. Permettono agli operai di muoversi in sicurezza, hanno reti di sicurezza, ascensori, percorsi definiti.
- Senza ponteggi, gli operai cadono o lavorano lentamente. Con ponteggi, cantieri da grattacielo.

> Fonte: dossier-conceptual-harness.md, derivata da `01b-harness/00-guida.md` (tufano).

---

## 0.4 Il framework IMPACT

Hashimoto e altri hanno consolidato 5 pilastri che ogni harness completo deve avere. L'acronimo (italianizzato) e':

| Lettera | Componente | Cosa fa | Esempi in Claude Code |
|---|---|---|---|
| **I** | **Intent** | Goal + constraints + acceptance criteria | CLAUDE.md, README progetto, prompt iniziale dettagliato |
| **M** | **Memory** | Stato persistente cross-turn / cross-session | auto-memory `~/.claude/projects/.../memory/`, `.claude/rules/`, plans directory |
| **P** | **Planning** | Design pre-esecuzione, riflessione | plan mode, `/ultraplan`, Opus 4.7 reasoning |
| **A** | **Authority** | Cosa puo' fare l'agent, chi approva, guardrail | permission rules (allow/ask/deny), sandbox, hooks, managed settings |
| **C** | **Control flow** | Come l'agent esegue il loop reason→act→observe | `/loop`, Monitor tool, hooks lifecycle, auto mode classifier |

> Vedi diagramma mermaid sotto.

```mermaid
flowchart TD
    USR[Utente / Task]
    LLM{LLM Claude}

    subgraph HARNESS["Harness IMPACT"]
        I[Intent<br/>CLAUDE.md, prompt]
        M[Memory<br/>auto-memory, plans]
        P[Planning<br/>plan mode, /ultraplan]
        A[Authority<br/>permissions, sandbox, hooks]
        C[Control flow<br/>/loop, Monitor, hooks lifecycle]
    end

    USR -->|Task| I
    I --> P
    P --> LLM
    LLM -->|Tool call| A
    A -->|Allow / Deny / Ask| C
    C --> M
    M -.->|Restore on next turn| I
    LLM -->|Output| USR
```

---

## 0.5 8 componenti architetturali (drill-down)

L'IMPACT framework descrive **a che livello** l'harness lavora. Sotto, ogni harness completo si articola in 8 componenti tecnici:

| # | Componente | Cosa fa | Doc Claude Code |
|---|---|---|---|
| 1 | **Context layer** | Decide cosa l'LLM vede ad ogni turn | [00b](/claude-code/00b-context-engineering), [06](/claude-code/06-claude-md-memory) |
| 2 | **Tool layer** | Espone capabilities (bash, edit, search, web) | [03](/claude-code/03-slash-commands), [10](/claude-code/10-mcp) |
| 3 | **Memory** | Persistenza cross-turn (auto-memory) e cross-session (plans) | [06](/claude-code/06-claude-md-memory), [06b](/claude-code/06b-memory-architecture) |
| 4 | **Orchestration** | Quale strategia (single agent, subagent, team) | [08](/claude-code/08-subagents), [12](/claude-code/12-agent-teams) |
| 5 | **Guardrails** | Limiti hard (sandbox, deny rules, hooks block) | [04](/claude-code/04-modalita-permessi), [04b](/claude-code/04b-authority-model), [07](/claude-code/07-hooks) |
| 6 | **State** | Snapshot e ripristino (checkpoints) | [04](/claude-code/04-modalita-permessi) sez. 4.5 |
| 7 | **Error recovery** | Cosa fare quando un tool fallisce / context corrotto | [07](/claude-code/07-hooks), [04](/claude-code/04-modalita-permessi) |
| 8 | **Intent capture** | Tradurre goal vago in goal eseguibile | [06](/claude-code/06-claude-md-memory), plan mode, `/ultraplan` |

> Nota: la fonte primaria (tufano `01b-harness`) elenca 7 componenti tecnici; "Intent capture" e' aggiunto come ottavo per coerenza con IMPACT. Vedi `_research/dossier-conceptual-harness.md` sez. 13 per trasparenza.

---

## 0.6 Tre case study fondativi

### Case 1 — OpenAI Codex (5 mesi, 1M righe generate)

OpenAI ha rivelato (11 feb 2026) che il progetto Codex aveva accumulato **circa 1 milione di righe di codice generate dall'agent, zero scritte manualmente** in 5 mesi di sviluppo. Stesso modello disponibile a tutti — la differenza era nel harness interno (orchestrazione multi-agent, retrieval mirato, eval automatici).

Lezione: l'harness puo' moltiplicare la produttivita' di un team a parita' di modello.

### Case 2 — Hashline experiment

Sperimento citato in fonti tufano: a parita' di modello, **cambiare solo l'harness** (context engineering + memory + planning) ha portato un'improvement misurato significativo su benchmark interni.

> ⚠️ Nota trasparenza: il numero specifico citato in alcune fonti ("+919%") **non e' verificato** nei dossier raccolti per questa repo. Lo riportiamo come aneddoto direzionale, non come dato. Vedi `_research/dossier-conceptual-context.md` sez. 2.

Lezione: il margine di miglioramento via harness, anche con LLM stagnante, e' enorme.

### Case 3 — Manus (acquisizione $2B per harness, non per modello)

[Manus](https://manus.im), startup AI agent, e' stata acquistata per ~$2B. Il punto chiave: Manus **non aveva un modello proprio** — usava modelli di terzi (Claude, GPT, Gemini). Il valore acquisito era nell'harness: orchestrazione multi-modello, computer use, memory architecture.

Lezione: il mercato remunera l'harness anche piu' del modello. Il modello e' commodity, l'harness e' moat.

> Fonti citate in `_research/dossier-conceptual-harness.md` con riferimenti X.

---

## 0.7 Claude Code IS un harness — mapping completo

Ogni feature di Claude Code corrisponde a un componente harness. Questo mapping e' la chiave per "vedere" Claude Code:

| Feature Claude Code | Componente harness | IMPACT | Doc |
|---|---|---|---|
| **CLAUDE.md** | Intent + Memory persistente | I + M | [06](/claude-code/06-claude-md-memory) |
| **`/init`** | Intent capture iniziale | I | [06](/claude-code/06-claude-md-memory) |
| **auto-memory** | Memory cross-session learned | M | [06b](/claude-code/06b-memory-architecture) |
| **`.claude/rules/`** | Memory path-specific | M | [06](/claude-code/06-claude-md-memory) |
| **plan mode** | Planning explicit | P | [04](/claude-code/04-modalita-permessi) |
| **`/ultraplan`** | Planning cloud-scale | P | [15](/claude-code/15-ultraplan-ultrareview) |
| **`/batch`** | Planning + Orchestration parallela | P + O | [03](/claude-code/03-slash-commands) |
| **permission rules** | Authority dichiarativa | A | [04](/claude-code/04-modalita-permessi), [04b](/claude-code/04b-authority-model) |
| **sandbox** | Authority OS-level | A | [04](/claude-code/04-modalita-permessi) |
| **managed settings** | Authority enterprise | A | [18](/claude-code/18-settings-auth) |
| **hooks** | Control flow + Authority | C + A | [07](/claude-code/07-hooks) |
| **`/loop`** | Control flow ricorsivo | C | [14](/claude-code/14-loop-monitor) |
| **Monitor tool** | Control flow event-driven | C | [14](/claude-code/14-loop-monitor) |
| **auto mode** | Control flow classifier-based | C | [04](/claude-code/04-modalita-permessi) |
| **subagents** | Orchestration single-thread | Orch | [08](/claude-code/08-subagents) |
| **agent teams** | Orchestration multi-thread | Orch | [12](/claude-code/12-agent-teams) |
| **checkpoints** | State + Error recovery | State | [04](/claude-code/04-modalita-permessi) sez. 4.5 |
| **`/rewind`** | State restoration | State | [04](/claude-code/04-modalita-permessi) |
| **MCP** | Tool layer extensibile | Tool | [10](/claude-code/10-mcp) |
| **plugins** | Tool + Skills + Hooks bundle | Tool | [11](/claude-code/11-plugins-marketplace) |
| **skills** | Tool layer behavior packs | Tool | [09](/claude-code/09-skills) |
| **`/ultrareview`** | Guardrails pre-merge | Guard | [15](/claude-code/15-ultraplan-ultrareview) |
| **`/security-review`** | Guardrails sicurezza | Guard | [03](/claude-code/03-slash-commands) |
| **`/compact`** | State + Memory compression | State + M | [03](/claude-code/03-slash-commands) |

> Risultato: quando leggi una nuova feature di Claude Code, chiediti "che componente harness amplifica?". La risposta sara' sempre una colonna di questa tabella.

---

## 0.8 I tre pilastri dell'harness engineering

Da `_research/dossier-conceptual-harness.md`:

1. **Determinismo dichiarativo** — Le regole non negoziabili (sicurezza, compliance, naming) si scrivono una volta nel harness (CLAUDE.md, hooks, sandbox), non in ogni prompt. L'LLM non puo' aggirarle.
2. **Composabilita'** — Skill / hook / subagent / MCP sono "Lego" combinabili. L'harness emerge dalla composizione, non da un monolite.
3. **Osservabilita'** — Ogni iterazione lascia traccia (auto-memory, transcript, hook logs, checkpoints). Il sistema e' debuggabile, riproducibile, recuperabile.

---

## 0.9 Quando "non ti serve l'harness"

Per task one-shot semplici (estrarre 3 entita' da un PDF, riassumere un email) un'API call diretta basta. L'harness ha overhead.

L'harness **paga** quando:
- Task multi-step (3+ tool call)
- Cross-session continuity (riprendere domani)
- Multi-utente (team che condividono regole)
- Compliance (audit log, RBAC, sandbox obbligatoria)
- Iterazione fitta (il context vale piu' del prompt)

In tutti gli altri casi, considera un wrapper SDK leggero (vedi [16 — Headless & Agent SDK](/claude-code/16-headless-agent-sdk) `--bare` mode).

---

## 0.10 Glossario veloce

| Termine | Definizione 1-frase |
|---|---|
| **Agent** | LLM + Harness che esegue un task autonomamente |
| **Harness** | Strato di orchestrazione attorno al modello (context, tool, memory, guardrail) |
| **IMPACT** | 5 pilastri harness: Intent, Memory, Planning, Authority, Control flow |
| **Context layer** | Cosa il modello vede ad ogni turn (CLAUDE.md, output tool, history) |
| **Memory layer** | Cosa sopravvive cross-turn (auto-memory, plans, checkpoints) |
| **Authority layer** | Cosa l'agent puo' fare (permission rules, sandbox, hooks) |
| **Compound engineering** | Pattern architetturali a livello harness (vedi [22](/claude-code/22-compound-engineering)) |

Glossario completo: [23 — Glossario](/claude-code/23-glossario).

---

## 0.11 Letture di approfondimento

- [Mitchell Hashimoto, "We Need to Talk About 'Agent Harnesses'"](https://mitchellh.com/writing/agent-harnesses) (5 feb 2026, post fondativo)
- [00b — Context engineering](/claude-code/00b-context-engineering) — il livello immediatamente sotto l'harness
- [14b — Agent loop ReAct](/claude-code/14b-agent-loop-react) — come l'harness fa girare il modello
- [22 — Compound engineering](/claude-code/22-compound-engineering) — pattern architetturali
- [21 — Guide per target user](/claude-code/21-guide-target-user) — come l'harness cambia per profilo
- `_research/dossier-conceptual-harness.md` — dossier interno dettagliato

---

← Precedente: [README](/claude-code) · Successivo → [00b — Context engineering](/claude-code/00b-context-engineering)
