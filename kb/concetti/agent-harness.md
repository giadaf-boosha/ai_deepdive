---
name: Agent harness
aliases: [agent harness, harness, scaffolding agentico, agent runtime]
categoria: infrastruttura
created: 2026-04-28
last_updated: 2026-04-28
mentions_count: 0
---

# Agent harness

## Cos'e

Un agent harness e' lo strato software che incapsula un [LLM](./llm.md) e gli da la struttura per operare come [agent](./agent.md): gestione del loop di esecuzione, registrazione e dispatch dei tool, gestione del [context window](./context-window.md), tracing, error handling, persistenza, sicurezza, integrazione con UI o sistemi esterni. Il modello e' il motore; l'harness e' il telaio. Senza harness un LLM e' una funzione pura `messages -> messages`. Con un harness diventa un sistema software interagente.

Il termine "harness" si e' affermato nel 2024-2026 nella letteratura agentica, mutuato dal mondo del testing software (test harness). Anthropic, Cursor, OpenAI lo usano per descrivere la differenza tra "modello" e "prodotto agentico". Un esempio paradigmatico: Claude Code (l'harness con cui stiamo operando) non e' Claude, e' il sistema che orchestra Claude attraverso filesystem, git, bash, scheduling, tool MCP, monitoring. Lo stesso modello in due harness diversi (Claude Desktop vs Claude Code) ha capacita' operative molto diverse.

L'importanza di harness sta nel fatto che, da un lato, le capacita' base dei modelli si stanno commoditizzando (la differenza Claude/GPT/Gemini su benchmark e' stretta); dall'altro, il design dell'harness fa la differenza tra agenti che funzionano in produzione e quelli che restano demo. Patterns di harness, telemetria, eval, robustezza sono il vero competitive moat per le aziende che costruiscono agenti.

## Come funziona

Un harness include un set ricorrente di componenti.

Loop runtime. Esegue l'invariante centrale: ricevere stato, chiamare il modello, parsing dell'output (testo, tool call, end), eseguire azioni, aggiornare stato, decidere se continuare. Le decisioni includono budget (max step, max token, max wallclock), criteri di terminazione, retry su errori transienti.

Tool registry. Mantiene la lista dei tool disponibili e i loro schemi, espone gli schemi al modello come parte del prompt (vedi [tool use](./tool-use.md)), valida gli argomenti delle chiamate, dispatcha all'implementazione, gestisce timeout, normalizza errori. Spesso si integra con [MCP](./mcp.md) per esporre tool da server esterni.

Context manager. Costruisce il prompt ad ogni step: system prompt, knowledge persistente, history conversazionale, tool descriptions, eventuale RAG context. Quando la storia cresce verso il limite del [context window](./context-window.md), applica strategie di compaction: riassunti automatici di blocchi vecchi, eviction di tool result voluminosi, retrieval selettivo.

Memory. Storage strutturato per: storia completa (per debug), riassunti compressi, knowledge persistente cross-session (preferenze utente, learned facts, snippet di codice ricorrenti). Backend tipici: file JSON locali, SQLite, vector store, KV store.

Tracing e telemetria. Ogni step viene loggato in modo strutturato: input, output, tool calls, timing, costi token. Si esportano in OpenTelemetry, LangSmith, Helicone, Arize, Braintrust. Senza tracing, debug e regression detection sono praticamente impossibili. Il tracing e' la singola pratica piu' alto-leverage in un harness di produzione.

Sicurezza. Sandboxing dell'esecuzione tool (es. tool bash dentro container o Docker), permission model (allowlist/denylist di comandi e path), human-in-the-loop su azioni distruttive, kill switch, rate limiting per utente, redaction di secrets nei log.

Eval framework. Suite di task benchmark che si rilancia ad ogni modifica di harness o modello. Le metriche includono task success rate, costo medio per task, latenza, qualita' soggettiva valutata da reviewer. Gli eval si fanno offline (su task fissi) e in produzione (shadow mode, A/B test).

Esempi di harness reali. Claude Code: harness CLI/IDE per coding, integra filesystem, bash, git, MCP, hooks, sub-agent, schedule. Cursor: harness IDE-first con composer, agent mode, codebase indexing. OpenAI Codex CLI / Claude Code: workflow simili. AutoGPT, BabyAGI: harness di ricerca early. LangGraph: framework per costruire harness custom con grafi a stati. CrewAI, AutoGen: harness per multi-agent. Open Interpreter: harness desktop con tool=python sandbox.

Considerazioni quantitative. Un harness di produzione occupa tipicamente 5000-50000 righe di codice. La distribuzione del tempo per task agentico: 30-60% chiamate LLM (latenza inferenza), 20-40% esecuzione tool, 5-15% logica harness. Il costo dollari e' dominato dai token; ottimizzazioni harness (caching, compaction efficiente, tool result truncation) possono ridurre costi del 30-70%.

## Varianti / approcci

| Tipo harness | Esempi | Ottimizzato per |
|---|---|---|
| CLI / coding agent | Claude Code, Cursor agent, Codex CLI | Sviluppatori, repo locali |
| Desktop assistant | Claude Desktop, ChatGPT desktop | Knowledge work generico |
| Browser / RPA | OpenAI Operator, Anthropic Computer Use, Browser Use | Automazione web GUI |
| Server / API agent | OpenAI Agents SDK, Claude Agent SDK | Backend integrabile |
| Multi-agent framework | LangGraph, CrewAI, AutoGen | Orchestrazione complessa |
| Voice / phone agent | Vapi, Retell | Conversazione vocale |
| Embedded in app | Cursor inline, Notion AI agents | Esperienze focalizzate |

Sull'asse "open vs proprietary". Open-source: LangGraph, Letta, OpenInterpreter, Continue.dev. Proprietary: Claude Code, Cursor, Devin, Codex. La scelta dipende da estensibilita' richiesta vs UX out-of-the-box. Sempre piu' harness adottano [MCP](./mcp.md) come strato di tool standard, riducendo il lock-in.

Sull'asse "single-loop vs grafo a stati". Il single-loop classico (ReAct) e' semplice, robusto, sufficiente per la maggior parte dei task. I grafi a stati (LangGraph) modellano workflow piu' rigorosi con nodi tipizzati, edge condizionali, checkpointing. Vincono quando il flusso ha rami noti e si vuole controllo esplicito.

## Quando usarlo / quando no

Costruire o adottare un harness e' la scelta giusta quando si fa girare un agente in produzione, quando la singola chiamata LLM non basta, quando serve telemetria e debugging strutturato, quando si scalano molti utenti concorrenti. Non si puo' deployare un agente serio senza un harness.

E' overkill quando: si fa una single-call LLM dentro un endpoint stateless (uno script con SDK ufficiale basta); si fa prototipazione rapida (notebook + ciclo for); il "task" e' un workflow predefinito senza decisioni del modello (un pipeline data va con orchestrator data, non agent harness).

Anti-pattern. Costruire harness from scratch quando un framework esistente copre l'80% dei casi: si reinventa loop, retry, telemetria. Mancanza di tracing strutturato: ogni bug richiede ore di indagine. Tool con timeout illimitati: un tool bloccato congela l'agente. Stato persistente non versionato: aggiornamenti rompono memoria storica. Mescolare model selection in piu' luoghi senza un model router: difficile cambiare modello globalmente. Sottostimare costo eval: senza una suite di eval mantenuta, ogni cambio e' una scommessa.

## Esempi pratici

Esempio 1: harness minimale custom (300 righe Python).

```python
class Harness:
    def __init__(self, model, tools, system, max_steps=30, budget_usd=1.0):
        self.model, self.tools = model, tools
        self.system = system
        self.max_steps, self.budget = max_steps, budget_usd
        self.tracer = Tracer()

    def run(self, user_msg):
        history = [{"role": "user", "content": user_msg}]
        cost = 0.0
        for step in range(self.max_steps):
            with self.tracer.span(f"step_{step}"):
                resp = self.model.chat(
                    system=self.system,
                    messages=history,
                    tools=[t.schema for t in self.tools],
                )
                cost += resp.cost
                if cost > self.budget:
                    return "Budget exceeded"
                if resp.stop_reason == "end_turn":
                    return resp.text
                tool_results = []
                for call in resp.tool_calls:
                    tool = next(t for t in self.tools if t.name == call.name)
                    try:
                        out = tool.run(**call.args)
                    except Exception as e:
                        out = f"ERROR: {e}"
                    tool_results.append({"id": call.id, "output": out})
                history.append({"role": "assistant", "content": resp.content})
                history.append({"role": "user", "content": tool_results})
        return "Max steps reached"
```

Esempio 2: harness con LangGraph. Si definisce un grafo: nodo `agent` (chiama LLM), nodo `tools` (esegue tool calls), edge condizionale che torna a `agent` se ci sono altre tool calls o termina. Checkpointing automatico permette resume dopo crash. Threading di sessioni multi-utente.

Esempio 3: produzione enterprise. Un'azienda ha un harness custom basato su FastAPI + Postgres + Redis. Per ogni richiesta utente: crea sessione in Postgres, esegue loop agentico, ogni step viene salvato in Postgres per audit, tool result voluminosi messi in S3 e referenziati. Tracing su Datadog. Eval suite di 200 task gira in CI ad ogni deploy. SLO: P95 latenza < 30s, success rate > 85%.

## Letture

- Anthropic, "Building effective agents", 2024. https://www.anthropic.com/research/building-effective-agents
- Anthropic, "Claude Code best practices", 2025. https://docs.anthropic.com/en/docs/agents-and-tools/claude-code
- LangGraph documentation. https://langchain-ai.github.io/langgraph/
- OpenAI, "Agents SDK". https://github.com/openai/openai-agents-python
- "AutoGen: Enabling Next-Gen LLM Applications via Multi-Agent Conversation", Wu et al. 2023. https://arxiv.org/abs/2308.08155
- "Cognitive Architectures for Language Agents", Sumers et al. 2023. https://arxiv.org/abs/2309.02427
- Letta (formerly MemGPT). https://github.com/cpacker/MemGPT
- "SWE-bench: Can Language Models Resolve Real-World GitHub Issues?", Jimenez et al. 2023. https://arxiv.org/abs/2310.06770

## Note operative

Eval suite minima. Per un harness agentico in produzione serve almeno un set di 30-100 task end-to-end realistici, ognuno con criterio di successo automatico (un test, un check sulla output, un assertion sullo stato). La suite gira ad ogni cambio di prompt, modello, tool, configurazione harness. Senza questa misura, tutte le decisioni sono opinioni; con essa, i miglioramenti sono ingegnerizzabili. Dataset come SWE-bench (coding agent), tau-bench (tool use), AgentBench danno baseline pubblici, ma il vero eval e' sul proprio dominio.

Cost governance. In un harness multi-utente i costi possono esplodere. Un agent con bug puo' loopare consumando milioni di token in pochi minuti. Difese in profondita': budget hard per sessione, alerting su anomalie di consumo, rate limit per utente, kill-switch globale. Tracing dei token in tempo reale (es. via Helicone, Langfuse) e' indispensabile.

Sicurezza dei tool. La superficie d'attacco principale di un harness e' nei tool che modificano stato: shell, send-mail, db-write, file-write. Best practice: separare tool read-only da tool write; richiedere conferma utente per i write su prima esecuzione di una sessione; permission model dichiarativo (es. allowlist di comandi shell, denylist di path). Per agenti che eseguono codice, il sandbox (container, VM, gVisor) e' obbligatorio in qualunque deployment toccato da utenti finali.

## Aggiornamenti

Nessun aggiornamento dopo la creazione (2026-04-28).
