---
name: AI Agent
aliases: [agent, AI agent, agente autonomo, autonomous agent]
categoria: paradigma
created: 2026-04-28
last_updated: 2026-04-30
mentions_count: 10
---

# AI Agent

## Cos'e

Un AI agent e' un sistema software che usa un [LLM](./llm.md) come motore decisionale per perseguire un obiettivo attraverso una sequenza di azioni in un ambiente. La differenza rispetto a una singola chiamata LLM e' duplice: l'agente opera in loop (osserva, ragiona, agisce, osserva di nuovo), e ha accesso a strumenti esterni ([tool use](./tool-use.md)) che modificano l'ambiente o raccolgono informazioni. Il termine ha radici nella reinforcement learning e nella tradizione AI classica (Russell e Norvig definiscono l'agente come "qualunque entita' che percepisce l'ambiente attraverso sensori e agisce su di esso attraverso attuatori"); applicato agli LLM, indica sistemi in cui il piano d'azione e' generato linguisticamente.

I lavori seminali sono "ReAct: Synergizing Reasoning and Acting in Language Models" (Yao et al., 2022), che introduce l'alternanza thought-action-observation, e "Toolformer" (Schick et al., 2023), che insegna a un LLM ad invocare tool. Il 2023 vede l'esplosione di prototipi (AutoGPT, BabyAGI, AgentGPT) che dimostrano la fattibilita' di agenti loop-based ma anche i loro limiti: deviazione dall'obiettivo, allucinazioni cumulate, costi esplosivi. Tra il 2024 e il 2026 il paradigma matura: framework strutturati (LangGraph, OpenAI Agents SDK, Claude Agent SDK), pattern consolidati (orchestratore-worker, plan-execute-reflect), e protocolli standard come [MCP](./mcp.md) per l'integrazione di tool.

L'agente e' importante perche' sposta il modello da "predict the next token" a "esegui un compito". Le applicazioni pratiche includono assistenti di coding (Claude Code, Cursor agent mode, Codex), agenti di customer support che eseguono azioni nei sistemi aziendali, agenti di ricerca (Deep Research di OpenAI e Anthropic), agenti per browser e RPA. Nel 2026 il termine "agentic" e' diventato categoria di prodotto tracciata dagli analisti come Gartner.

## Come funziona

Un agente minimale opera secondo il loop ReAct:

```
loop:
  thought = LLM(history)        # ragionamento esplicito
  action = parse_action(thought)
  if action == "finish":
    return thought.answer
  observation = execute(action)
  history.append(thought, action, observation)
```

In dettaglio. Il prompt di sistema definisce il ruolo, gli obiettivi, i tool disponibili (con schema JSON), i vincoli (max iterazioni, budget). Ad ogni iterazione il modello riceve la storia accumulata e produce un blocco testuale che include un ragionamento e una chiamata a tool (function call) o un segnale di terminazione. Il framework esegue il tool e re-inserisce l'osservazione. Il loop si chiude quando il modello dichiara la conclusione o si raggiunge un limite.

Componenti architetturali. Planner: decide la sequenza di sotto-obiettivi (puo' essere implicito nelle thought o esplicito tramite un nodo dedicato). Executor: esegue i tool. Memory: storico conversazionale (short-term) e knowledge persistente (long-term, spesso via [RAG](./rag.md)). Reflector / critic: valuta il progresso, decide se cambiare strategia. Guardrail: validatori di output, controlli di policy, kill-switch su anomalie.

Pattern architetturali consolidati. Single-loop ReAct: un solo LLM, semplice e robusto fino a 20-30 step. Plan-and-execute: un planner produce piano alto livello, un executor esegue passo per passo. Orchestrator-workers: un coordinator delega sotto-task a sub-agent specializzati con tool ristretti. Multi-agent collaboration: piu' agenti con ruoli (es. researcher, writer, critic) interagiscono. Hierarchical / supervisor: gerarchia di agenti, ognuno con scope.

Considerazioni quantitative. Un task agentico tipico di coding consuma 50-500k token totali distribuiti su 10-100 step LLM. Il costo cresce in modo super-lineare se il context si gonfia (ogni step rilegge la storia). Le tecniche di compaction (riassunto periodico della storia per liberare context window) sono critiche per task lunghi.

Failure mode classici. Loop infiniti: il modello continua a chiamare lo stesso tool senza progresso. Hallucination cascading: un errore precoce contamina tutti gli step successivi. Tool misuse: chiamare il tool con argomenti sbagliati. Reward hacking: l'agente trova scorciatoie che soddisfano la metrica ma non l'intento (es. cancellare un test invece di farlo passare). Le mitigazioni includono budget hard, telemetria, validators sui tool output, fallback a human-in-the-loop.

## Varianti / approcci

| Pattern | Caratteristica | Esempio reale |
|---|---|---|
| ReAct loop | Thought-Action-Observation lineare | Claude Code, primi AutoGPT |
| Plan-and-execute | Piano statico + esecuzione | LangChain plan_and_execute |
| Orchestrator-workers | Coordinator + sub-agent specializzati | Anthropic's research multi-agent |
| Reflexion | Self-critique tra iterazioni | Shinn et al. 2023 |
| Tree-of-Thoughts agentic | Esplorazione ramificata di piani | Yao et al. 2023 |
| Computer-use / browser agent | Tool: screenshot + click + type | Claude Computer Use, OpenAI Operator |
| Coding agent | Tool: file edit + bash + test | Claude Code, Cursor agent, Codex CLI |
| Deep Research | Loop di search + read + write su orizzonte lungo | OpenAI Deep Research, Perplexity Deep Research |

Sull'asse autonomia: agenti supervisionati (ogni azione conferma da utente), semi-autonomi (azioni non distruttive auto, distruttive con conferma), autonomi (tutto in autopilot con guardrail). Sull'asse memoria: stateless per task, stateful con persistenza, learning-from-experience (l'agente aggiorna la propria base di conoscenza).

Una distinzione importante e' tra workflow e agent (Anthropic, "Building effective agents", 2024). Un workflow e' una pipeline LLM con flusso di controllo predefinito (chain, routing, parallelization). Un agent e' un sistema in cui l'LLM decide dinamicamente cosa fare. Workflow batte agent quando il problema e' ripetibile e mappabile; agent batte workflow quando c'e' incertezza sulla traiettoria.

## Quando usarlo / quando no

Un agente e' la scelta giusta quando il task richiede piu' chiamate LLM con stato condiviso, l'output dipende da informazioni che si raccolgono iterativamente, ci sono tool reali da invocare, e la traiettoria non e' nota a priori. Esempi: ricerca web multi-source con sintesi, debug di codice (riproduce, analizza, propone fix, verifica), processi di acquisto multi-step, navigazione UI per task ripetitivi.

Un agente e' la scelta sbagliata quando una catena lineare deterministica (workflow) sarebbe sufficiente, quando la latenza di 30+ secondi e' inaccettabile, quando l'errore di una singola azione ha costo elevato e non e' rollback-abile, quando la frequenza d'uso giustifica un sistema specializzato (un classificatore tradizionale per ticket invece di un agente che ragiona ogni volta).

Anti-pattern. "Agent-washing": chiamare agente quello che e' un workflow. Dare troppi tool: oltre 30-40 tool, la qualita' di selezione degrada. Mancanza di telemetria: senza tracing strutturato un agente e' inosservabile. Assenza di valutazione: bisogna avere task end-to-end con criterio di successo verificabile, non valutare solo step singoli. Trust troppo alto: lasciare un agente eseguire azioni distruttive (delete prod, send mail a clienti) senza human-in-the-loop nelle prime iterazioni.

## Esempi pratici

Esempio 1: agente coding minimale (pseudocodice).

```python
TOOLS = {"read_file": ..., "edit_file": ..., "run_bash": ...}
SYSTEM = "Sei un agente che modifica codice. Usa i tool per leggere, modificare, testare."

def agent_loop(task: str, max_steps: int = 30) -> str:
    history = [{"role": "system", "content": SYSTEM},
               {"role": "user", "content": task}]
    for _ in range(max_steps):
        resp = llm(history, tools=TOOLS)
        if resp.stop_reason == "end_turn":
            return resp.content
        for call in resp.tool_calls:
            obs = TOOLS[call.name](**call.args)
            history.append({"role": "tool", "tool_use_id": call.id, "content": obs})
        history.append({"role": "assistant", "content": resp.content})
    raise BudgetExceeded
```

Esempio 2: orchestrator-workers per ricerca. Un orchestrator riceve "scrivi un report sul mercato dei vector DB". Decompone in 5 sotto-domande, lancia 5 sub-agent paralleli, ognuno con tool web_search e read_url. I sub-agent restituiscono note strutturate; l'orchestrator scrive il report finale e cita le fonti. Il pattern e' analogo a quello descritto da Anthropic per il sistema "Research" lanciato nel 2025.

Esempio 3: agente operativo enterprise. Un agent customer support ha tool `get_order(id)`, `refund_order(id, amount)`, `escalate_to_human(reason)`. Policy: refund > 200 euro richiede `escalate_to_human`. L'agente esegue il loop ReAct, ma `refund_order` e' wrappato da un middleware che intercetta importi alti. La telemetria registra ogni tool call con argomenti, ID utente, esito.

## Letture

- Yao et al., "ReAct: Synergizing Reasoning and Acting in Language Models", 2022. https://arxiv.org/abs/2210.03629
- Schick et al., "Toolformer: Language Models Can Teach Themselves to Use Tools", 2023. https://arxiv.org/abs/2302.04761
- Shinn et al., "Reflexion: Language Agents with Verbal Reinforcement Learning", 2023. https://arxiv.org/abs/2303.11366
- Anthropic, "Building effective agents", 2024. https://www.anthropic.com/research/building-effective-agents
- Anthropic, "How we built our multi-agent research system", 2025. https://www.anthropic.com/engineering/built-multi-agent-research-system
- LangGraph documentation. https://langchain-ai.github.io/langgraph/
- OpenAI, "A practical guide to building agents", 2025. https://openai.com/research
- Russell e Norvig, "Artificial Intelligence: A Modern Approach", 4a ed., 2020.

## Note operative

Eval di un agente. Misurare un agente e' diverso dal misurare un LLM. Le metriche sono task-level: success rate (quanto spesso completa il task con criterio verificabile), efficiency (quanti step e quanti token usa), cost-per-success, latency end-to-end. Benchmark pubblici noti: SWE-bench (issue github), tau-bench (conversazioni con tool), GAIA (task generali), WebArena (browser). In produzione si costruisce un set "golden" di task ricorrenti del proprio dominio.

Pattern di rollout. Il deployment di agenti in azienda segue tipicamente tre fasi. Fase 1 - assistente: l'agente propone, l'umano approva ogni azione. Fase 2 - co-pilota: human-in-the-loop solo per azioni distruttive, le altre passano. Fase 3 - autonomo: l'agente esegue da solo, gli umani monitorano e rivedono campionariamente. Saltare le fasi e' rischioso; la maggior parte degli incidenti pubblicati di agenti in produzione (ordini sbagliati, mail inappropriate, dati cancellati) sono accaduti in deployment passati troppo presto a Fase 3.

Telemetria distribuita. Un agente che fa 50 step distribuiti tra LLM, database, API esterne genera traccia complessa. Standardizzare con OpenTelemetry, attributi span dedicati (model.name, tool.name, tokens.input, tokens.output, cost.usd), correlation id per sessione utente e per task. Senza questi, il debugging di un fail in produzione consuma ore; con essi, minuti.

## Aggiornamenti

### 2026-04-28

Tre voci del digest di oggi coinvolgono il concetto di agent. "From Skills to Talent" (huggingface.co/papers/2604.22446) propone un'architettura multi-agente ispirata alla gerarchia aziendale, con assegnazione task basata su skill matching. "ClawMark" (huggingface.co/papers/2604.23781) introduce un benchmark living-world per agenti persistenti multi-giorno, colmando il gap tra valutazione single-shot e use case operativi. Avoca AI chiude un Series B da $125M: prodotto interamente basato su agenti vocali per la gestione di chiamate in entrata nel settore servizi. Segnale convergente: l'architettura agentica si consolida sia come oggetto di ricerca accademica (benchmark, framework) sia come categoria di prodotto commerciale con metriche di business (volume prenotato). [Digest 2026-04-28](../../digest/2026/04/28.md)

### 2026-04-29

Tre segnali convergenti sul fronte agentico. Xiaomi MiMo-V2.5-Pro si valuta su Claw-Eval (benchmark agentico) e batte DeepSeek-V4-Pro: i benchmark agentici diventano il metro competitivo di riferimento anche per i modelli cinesi open source. OpenAI porta Codex su Amazon Bedrock come "Amazon Bedrock Managed Agents powered by OpenAI": la disponibilita' multi-cloud espande la superficie di deployment degli agenti basati su GPT-5.5. "The Reasoning Trap" (ICLR 2026, arXiv 2510.22977) documenta un trade-off strutturale che riguarda direttamente chi deploya agenti con tool calling: il RL di reasoning aumenta il task performance ma amplifica le tool hallucination in modo proporzionale, erodendo l'affidabilita' degli strumenti nei layer finali. [Digest 2026-04-29](../../digest/2026/04/29.md)

### 2026-04-30

Quattro segnali agentici nel digest di oggi. AutoResearchBench (arXiv 2604.25256, BAAI) documenta che anche i modelli frontier raggiungono meno del 10% su task di scoperta letteratura scientifica autonoma: il gap tra browsing generico e comprensione scientifica strutturata e' ora quantificato. GEPA (ICLR 2026 Oral) ottimizza compound AI systems (pipeline multi-modulo con piu' LLM e tool) via riflessione NL, battendo GRPO con 35x meno rollout: segnale che l'ottimizzazione di sistemi agentici non richiede RL costoso. Rogo chiude un Series D da $160M per "Felix", agente multi-step per investment banking: secondo round oltre $100M in due giorni per vertical AI agents (dopo Avoca AI $125M). Goldman Sachs rimuove l'accesso a Claude per i banker di Hong Kong: la governance per giurisdizione degli strumenti AI diventa pratica operativa nelle istituzioni finanziarie globali. [Digest 2026-04-30](../../digest/2026/04/30.md)
