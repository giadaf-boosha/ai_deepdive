---
name: Agent harness
aliases: [agent harness, harness, scaffolding agentico, agent runtime]
categoria: infrastruttura
created: 2026-04-28
last_updated: 2026-06-29
---

# Agent harness

## Cos'e

Un agent harness e' lo strato software che incapsula un [LLM](./llm.md) e gli da la struttura per operare come [agent](./agent.md): gestione del loop di esecuzione, registrazione e dispatch dei tool, gestione del [context window](./context-window.md), tracing, error handling, persistenza, sicurezza, integrazione con UI o sistemi esterni. Il modello e' il motore; l'harness e' il telaio. Senza harness un LLM e' una funzione pura `messages -> messages`. Con un harness diventa un sistema software interagente.

Il termine "harness" si e' affermato nel 2024-2026 nella letteratura agentica, mutuato dal mondo del testing software (test harness). Anthropic, Cursor, OpenAI lo usano per descrivere la differenza tra "modello" e "prodotto agentico". Un esempio paradigmatico: Claude Code (l'harness con cui stiamo operando) non e' Claude, e' il sistema che orchestra Claude attraverso filesystem, git, bash, scheduling, tool MCP, monitoring. Lo stesso modello in due harness diversi (Claude Desktop vs Claude Code) ha capacita' operative molto diverse.

L'importanza dell'harness sta in un'asimmetria che la primavera 2026 ha reso ancora piu' netta: da un lato le capacita' base dei modelli si commoditizzano (la differenza Claude/GPT/Gemini su benchmark e' stretta); dall'altro, il design dell'harness fa la differenza tra agenti che funzionano in produzione e quelli che restano demo. Una formulazione diffusa nella community degli sviluppatori e' che costruire un agente e' "5% chiamare il modello in un loop e 95% context management, esecuzione tool, sandboxing ed error handling": il valore ingegneristico vive quasi interamente nell'harness, mentre il modello tende a diventare componente intercambiabile. Patterns di harness, telemetria, eval e robustezza sono il vero competitive moat per le aziende che costruiscono agenti.

Un dato di maggio 2026 conferma questa lettura su base empirica. Il paper "Is Grep All You Need? How Agent Harnesses Reshape Agentic Search" (arXiv 2605.15184, 14 maggio) ha misurato l'accuratezza di ricerca agentiva variando sia il metodo di retrieval (grep vs vector) sia l'harness (Chronos, Claude Code, OpenAI Codex CLI, Gemini CLI) sul dataset LongMemEval. Il risultato contro-intuitivo: la variabilita' di punteggio tra harness diversi, a parita' di metodo di retrieval e di dati, e' maggiore della variabilita' tra grep e vector retrieval all'interno dello stesso harness. In altre parole, su questi task la scelta e la configurazione dell'harness pesa quanto o piu' della scelta dell'algoritmo. Per chi progetta pipeline agentiche su corpus medio-grandi questo sposta esplicitamente l'attenzione dall'ottimizzazione del retrieval all'ingegneria dell'harness.

## Come funziona

Un harness include un set ricorrente di componenti.

Loop runtime. Esegue l'invariante centrale: ricevere stato, chiamare il modello, parsing dell'output (testo, tool call, end), eseguire azioni, aggiornare stato, decidere se continuare. Le decisioni includono budget (max step, max token, max wallclock), criteri di terminazione, retry su errori transienti. Un'osservazione architetturale emersa con forza nel 2026 e' che il loop agentico e l'ambiente di esecuzione dei tool sono concettualmente separabili: si puo' tenere il loop (orchestrazione, context management, error recovery) in un posto e spostare l'esecuzione dei tool altrove. E' esattamente la mossa di Anthropic con le self-hosted sandboxes (vedi sotto).

Tool registry. Mantiene la lista dei tool disponibili e i loro schemi, espone gli schemi al modello come parte del prompt (vedi [tool use](./tool-use.md)), valida gli argomenti delle chiamate, dispatcha all'implementazione, gestisce timeout, normalizza errori. Spesso si integra con [MCP](./mcp.md) per esporre tool da server esterni. La primavera 2026 ha visto l'MCP affermarsi come strato di tool standard production-grade: il 28 maggio Google ha pubblicato il Google Pay & Wallet Developer MCP Server (Public Preview) insieme a un programma di MCP server gestiti per le proprie API cloud, segnale che protocolli di tool prima usati per demo entrano nei workflow di pagamento reali.

Context manager. Costruisce il prompt ad ogni step: system prompt, knowledge persistente, history conversazionale, tool descriptions, eventuale RAG context. Quando la storia cresce verso il limite del [context window](./context-window.md), applica strategie di compaction: riassunti automatici di blocchi vecchi, eviction di tool result voluminosi, retrieval selettivo. La frontiera 2026 del context management e' spostare il coordinamento fuori dal context: con le Dynamic Workflows di Claude Opus 4.8 (28 maggio) il piano vive in uno script, i risultati intermedi nelle variabili dello script, e il context window dell'agente principale riceve solo la risposta finale, riducendo il rischio di overflow su task multi-step a scala di codebase.

Memory. Storage strutturato per: storia completa (per debug), riassunti compressi, knowledge persistente cross-session (preferenze utente, learned facts, snippet di codice ricorrenti). Backend tipici: file JSON locali, SQLite, vector store, KV store. Da notare che la memoria e' anche un vincolo di deployment: nelle self-hosted sandbox di Claude Managed Agents (public beta, maggio 2026) la feature Memory non e' supportata, un esempio di come scelte di isolamento e funzionalita' dell'harness si condizionino a vicenda.

Tracing e telemetria. Ogni step viene loggato in modo strutturato: input, output, tool calls, timing, costi token. Si esportano in OpenTelemetry, LangSmith, Helicone, Langfuse, Arize, Braintrust. Senza tracing, debug e regression detection sono praticamente impossibili. Il tracing e' la singola pratica piu' alto-leverage in un harness di produzione.

Sicurezza. Sandboxing dell'esecuzione tool (es. tool bash dentro container o VM), permission model (allowlist/denylist di comandi e path), human-in-the-loop su azioni distruttive, kill switch, rate limiting per utente, redaction di secrets nei log. Il 30 maggio 2026 Anthropic ha pubblicato la prima documentazione tecnica completa dell'isolamento di ogni prodotto Claude ("How we contain Claude across products"), rendendo questo livello dell'harness ispezionabile: Claude.ai esegue codice in container gVisor server-side con filesystem effimero per sessione; Claude Code, in locale sulla macchina dell'utente, usa Seatbelt su macOS e Bubblewrap su Linux per confinare il processo con capabilities minime; Claude Cowork gira dentro una VM completa (Apple Virtualization Framework su macOS, HCS su Windows). Il punto pratico per chi disegna un harness e' che il sandbox giusto dipende da dove gira l'agente: server-side, locale o emulazione full-OS.

Eval framework. Suite di task benchmark che si rilancia ad ogni modifica di harness o modello. Le metriche includono task success rate, costo medio per task, latenza, qualita' soggettiva valutata da reviewer. Gli eval si fanno offline (su task fissi) e in produzione (shadow mode, A/B test). E' significativo che alcuni harness incorporino l'eval nel loop stesso: Grok Build 0.1 (xAI, maggio 2026) introduce l'Arena Mode, in cui piu' agenti affrontano lo stesso problema e vengono classificati internamente prima che il risultato arrivi allo sviluppatore.

Esempi di harness reali. Claude Code: harness CLI/IDE per coding, integra filesystem, bash, git, MCP, hooks, sub-agent, schedule, e dalla v2.1.154 le Dynamic Workflows. Cursor: harness IDE-first con composer, agent mode, codebase indexing. OpenAI Codex CLI / Codex desktop: workflow simili, con Goal mode che persegue un obiettivo per ore o giorni. Google Antigravity 2.0: piattaforma agent-first standalone con CLI, SDK e Managed Agents nel Gemini API. xAI Grok Build 0.1: coding agent CLI proprietario con sub-agenti paralleli. AutoGPT, BabyAGI: harness di ricerca early. LangGraph: framework per costruire harness custom con grafi a stati. CrewAI, AutoGen: harness per multi-agent. Open Interpreter: harness desktop con tool=python sandbox. ARIS (arXiv 2605.03042): autonomous research harness open-source executor-agnostic.

Considerazioni quantitative. Un harness di produzione occupa tipicamente 5000-50000 righe di codice. La distribuzione del tempo per task agentico: 30-60% chiamate LLM (latenza inferenza), 20-40% esecuzione tool, 5-15% logica harness. Il costo dollari e' dominato dai token; ottimizzazioni harness (caching, compaction efficiente, tool result truncation, coordinamento fuori dal context) possono ridurre costi del 30-70%.

## Varianti / approcci

| Tipo harness | Esempi | Ottimizzato per |
|---|---|---|
| CLI / coding agent | Claude Code, Cursor agent, Codex CLI, Grok Build, Antigravity 2.0 | Sviluppatori, repo locali |
| Desktop assistant | Claude Desktop, ChatGPT desktop, Claude Cowork | Knowledge work generico |
| Browser / RPA | OpenAI Operator, Anthropic Computer Use, Browser Use | Automazione web GUI |
| Server / API agent | OpenAI Agents SDK, Claude Agent SDK, Antigravity SDK | Backend integrabile |
| Managed agent service | Claude Managed Agents, Gemini API Managed Agents | Deployment enterprise gestito |
| Multi-agent framework | LangGraph, CrewAI, AutoGen | Orchestrazione complessa |
| Voice / phone agent | Vapi, Retell | Conversazione vocale |
| Embedded in app | Cursor inline, Notion AI agents | Esperienze focalizzate |

Sull'asse "open vs proprietary". Open-source: LangGraph, Letta, OpenInterpreter, Continue.dev, ARIS. Proprietary: Claude Code, Cursor, Devin, Codex, Antigravity, Grok Build. La scelta dipende da estensibilita' richiesta vs UX out-of-the-box. Sempre piu' harness adottano [MCP](./mcp.md) come strato di tool standard, riducendo il lock-in; la primavera 2026 ha visto MCP diventare anche il canale di accesso alla rete privata enterprise (MCP tunnels, research preview).

Sull'asse "single-loop vs grafo a stati vs script orchestratore". Il single-loop classico (ReAct) e' semplice, robusto, sufficiente per la maggior parte dei task. I grafi a stati (LangGraph) modellano workflow piu' rigorosi con nodi tipizzati, edge condizionali, checkpointing. Vincono quando il flusso ha rami noti e si vuole controllo esplicito. Nel 2026 si e' aggiunta una terza modalita': lo script orchestratore generato dal modello stesso. Le Dynamic Workflows di Opus 4.8 fanno scrivere a Claude uno script JavaScript che coordina fino a 1.000 subagenti totali per run (16 in parallelo), eseguito in background mentre la sessione resta reattiva. Il caso d'uso dichiarato e' la migrazione completa di una codebase da kickoff a merge usando la test suite esistente come criterio di accettazione. E' una via di mezzo: piu' flessibile di un grafo statico, ma con il piano materializzato in codice ispezionabile invece che disperso nel context.

Sull'asse "managed vs self-hosted". Un harness puo' tenere tutto nella propria infrastruttura, oppure separare il loop (gestito dal vendor) dall'esecuzione dei tool (nell'infrastruttura del cliente). Le self-hosted sandboxes di Claude Managed Agents (public beta, 19 maggio 2026) implementano esattamente questa separazione: l'esecuzione dei tool si sposta su server propri o provider come Cloudflare, Daytona, Modal, Vercel, mentre orchestrazione, context management ed error recovery restano su Anthropic. File sensibili, package e servizi interni non lasciano il perimetro aziendale.

## Quando usarlo / quando no

Costruire o adottare un harness e' la scelta giusta quando si fa girare un agente in produzione, quando la singola chiamata LLM non basta, quando serve telemetria e debugging strutturato, quando si scalano molti utenti concorrenti. Non si puo' deployare un agente serio senza un harness.

E' overkill quando: si fa una single-call LLM dentro un endpoint stateless (uno script con SDK ufficiale basta); si fa prototipazione rapida (notebook + ciclo for); il "task" e' un workflow predefinito senza decisioni del modello (un pipeline data va con orchestrator data, non agent harness).

Una decisione 2026 ricorrente e' "build vs adopt vs managed". Adottare un harness esistente (Claude Code, Cursor, Codex, Antigravity) conviene quando l'80% dei casi e' coperto e si vuole UX out-of-the-box. Costruire custom conviene quando il dominio e' specifico e l'estensibilita' e' critica. La terza opzione, managed (Claude Managed Agents, Gemini Managed Agents), e' la risposta tipica degli ambienti regulated: si delega il loop al vendor ma si tiene il controllo su dati ed esecuzione. Per finanza, healthcare e legal, la combinazione self-hosted sandbox + MCP tunnels e' il pattern che ha sbloccato l'adozione enterprise nella primavera 2026, perche' rimuove i due blocchi piu' frequenti: il controllo sui dati e l'esposizione di sistemi interni a internet.

Anti-pattern. Costruire harness from scratch quando un framework esistente copre l'80% dei casi: si reinventa loop, retry, telemetria. Mancanza di tracing strutturato: ogni bug richiede ore di indagine. Tool con timeout illimitati: un tool bloccato congela l'agente. Stato persistente non versionato: aggiornamenti rompono memoria storica. Mescolare model selection in piu' luoghi senza un model router: difficile cambiare modello globalmente. Sottostimare costo eval: senza una suite di eval mantenuta, ogni cambio e' una scommessa. Affidarsi al modello base ignorando l'harness: il paper "Is Grep All You Need?" mostra che la stessa coppia modello+dati rende molto diversamente in harness diversi, quindi ottimizzare solo il prompt o solo il retrieval lascia performance sul tavolo. Orchestrare swarm di subagenti senza budget hard: con 1.000 subagenti per run il costo e il rischio di loop si moltiplicano se non c'e' un cap esplicito.

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

Esempio 3: orchestrazione fuori dal context con Dynamic Workflows (Claude Code v2.1.154+, Opus 4.8). Invece di tenere il piano nel context window, si chiede a Claude di scrivere uno script JavaScript che lancia subagenti paralleli (fino a 16 concorrenti, 1.000 totali). Ogni subagente ha context e sandbox propri; il parent riceve solo status update strutturati; il context principale riceve solo il risultato finale. Tipico per migrazioni a scala di codebase con test suite come criterio di accettazione. Il rovescio della medaglia e' la cost governance: serve un budget hard sul numero di subagenti e sui token, perche' lo swarm amplifica sia il throughput sia il rischio di consumo runaway.

Esempio 4: produzione enterprise regulated con managed agent. Una banca usa Claude Managed Agents con self-hosted sandbox su Modal: il loop agentico resta su Anthropic, ma i tool che leggono dati clienti girano nell'infrastruttura della banca; gli MCP server interni (core banking, KYC) sono raggiunti via MCP tunnel outbound-only, senza alcun endpoint pubblico esposto. Tracing su Datadog interno. Eval suite di 200 task gira in CI ad ogni deploy. SLO: P95 latenza < 30s, success rate > 85%. Vincolo noto: Memory cross-session non disponibile nelle sessioni self-hosted.

## Letture

- Anthropic, "Building effective agents", 2024. https://www.anthropic.com/research/building-effective-agents
- Anthropic, "Claude Code best practices", 2025. https://docs.anthropic.com/en/docs/agents-and-tools/claude-code
- Anthropic Engineering, "How we contain Claude across products", 2026. https://www.anthropic.com/engineering/how-we-contain-claude
- Anthropic, "Orchestrate subagents at scale with dynamic workflows", Claude Code Docs, 2026. https://code.claude.com/docs/en/workflows
- "Is Grep All You Need? How Agent Harnesses Reshape Agentic Search", arXiv 2605.15184, 2026. https://arxiv.org/abs/2605.15184
- "ARIS: Auto-Research-in-Sleep", arXiv 2605.03042, 2026. https://arxiv.org/abs/2605.03042
- LangGraph documentation. https://langchain-ai.github.io/langgraph/
- OpenAI, "Agents SDK". https://github.com/openai/openai-agents-python
- "AutoGen: Enabling Next-Gen LLM Applications via Multi-Agent Conversation", Wu et al. 2023. https://arxiv.org/abs/2308.08155
- "Cognitive Architectures for Language Agents", Sumers et al. 2023. https://arxiv.org/abs/2309.02427
- Letta (formerly MemGPT). https://github.com/cpacker/MemGPT
- "SWE-bench: Can Language Models Resolve Real-World GitHub Issues?", Jimenez et al. 2023. https://arxiv.org/abs/2310.06770

## Note operative

Eval suite minima. Per un harness agentico in produzione serve almeno un set di 30-100 task end-to-end realistici, ognuno con criterio di successo automatico (un test, un check sulla output, un assertion sullo stato). La suite gira ad ogni cambio di prompt, modello, tool, configurazione harness. Senza questa misura, tutte le decisioni sono opinioni; con essa, i miglioramenti sono ingegnerizzabili. Dataset come SWE-bench (coding agent), tau-bench (tool use), AgentBench, LongMemEval (memoria/ricerca agentiva) danno baseline pubblici, ma il vero eval e' sul proprio dominio. Da tenere a mente il finding di "Is Grep All You Need?": un eval va girato sull'harness completo, non solo sul modello, perche' lo stesso modello rende diversamente a seconda di come l'harness gli serve il context e i tool result (inline vs su file).

Cost governance. In un harness multi-utente i costi possono esplodere. Un agent con bug puo' loopare consumando milioni di token in pochi minuti, e gli harness 2026 con orchestrazione di swarm (fino a 1.000 subagenti per run) alzano sia il throughput sia la superficie di rischio. Difese in profondita': budget hard per sessione e per swarm, cap sul numero di subagenti, alerting su anomalie di consumo, rate limit per utente, kill-switch globale. Tracing dei token in tempo reale (es. via Helicone, Langfuse) e' indispensabile. Opzioni di pricing come il Fast Mode di Opus 4.8 (2.5x la velocita' a un terzo del costo) e il pannello Effort permettono di calibrare costo e latenza per classe di task direttamente dall'harness.

Sicurezza dei tool. La superficie d'attacco principale di un harness e' nei tool che modificano stato: shell, send-mail, db-write, file-write. Best practice: separare tool read-only da tool write; richiedere conferma utente per i write su prima esecuzione di una sessione; permission model dichiarativo (es. allowlist di comandi shell, denylist di path). Per agenti che eseguono codice, il sandbox e' obbligatorio in qualunque deployment toccato da utenti finali; la documentazione Anthropic del 30 maggio 2026 mostra che la scelta del meccanismo dipende dal contesto di esecuzione (gVisor server-side, Seatbelt/Bubblewrap in locale, VM full-OS per ambienti desktop emulati). In ambito enterprise, separare il loop dall'esecuzione dei tool (self-hosted sandbox) e accedere ai sistemi interni via gateway outbound-only (MCP tunnel) e' il pattern di riferimento per non esporre il perimetro aziendale.

## Aggiornamenti

### 2026-05-02

Claude Code v2.1.126 (rilasciato 1 maggio 2026) introduce miglioramenti significativi al harness: `claude project purge` per la gestione del ciclo di vita dei progetti, model picker che interroga `/v1/models` di gateway compatibili, OAuth via incolla in terminale per ambienti WSL2/SSH/container, e risoluzione del rilevamento PowerShell 7 su Windows. I progressi evidenziano come il harness di produzione evolva lungo tre assi: gestione dello stato persistente (project state lifecycle), integrazione con infrastrutture ibride (gateway, Bedrock service tier), e robustezza su ambienti non standard (WSL2, container, cloud IDE). [Digest 2026-05-02](../../digest/2026/05/02.md)

### 2026-06-11

Claude Managed Agents: Scheduled Deployments e Credential Vaults in public beta (Anthropic, 9 giugno, 5 fonti). Due funzionalita' infrastrutturali che risolvono la coppia di blocchi piu' frequente nel deployment di harness agentico in produzione. Scheduled Deployments: l'operatore assegna un cron schedule a un harness specifico (es. `0 5 * * *` per ogni giorno alle 5 UTC); la piattaforma Anthropic avvia la sessione, esegue il task e la chiude, senza che il team gestisca nessun scheduler esterno (nessun cron job server, Lambda, Airflow). L'harness diventa indistinguibile da un processo di sistema pianificato. Credential Vaults: le API key, i token OAuth e le password di database necessarie ai tool che l'harness usa non passano mai in chiaro nel prompt o nella history della sessione; vengono archiviate crittografate nella piattaforma e iniettate nell'ambiente di esecuzione al momento dell'avvio, come variabili d'ambiente. Insieme, le due funzionalita' risolvono la domanda "chi attiva l'agente quando non c'e' un umano, e come si autentica" che tiene la maggior parte dei progetti agentici fermi in pilota. Caso documentato: Rakuten usa scheduled deployments per analizzare dati e produrre report su base settimanale o mensile. La routine ai_deepdive di questo repo usa esattamente questo pattern (cron schedule + credenziali ambiente). [Digest 2026-06-11](../../digest/2026/06/11.md)

### 2026-06-01

Maggio 2026 e' stato un mese denso e sostanziale per il concetto di harness, su quattro fronti distinti, tutti con riscontro nei digest e in fonti web verificabili.

Orchestrazione fuori dal context. Il 28 maggio Anthropic rilascia Claude Opus 4.8 con Dynamic Workflows (research preview su Claude Code v2.1.154+): Claude scrive uno script JavaScript che orchestra fino a 1.000 subagenti totali per run (16 in parallelo), eseguito in background; il piano e i risultati intermedi vivono nelle variabili dello script, il context principale riceve solo la risposta finale. E' una nuova modalita' di harness — lo script orchestratore generato dal modello — accanto al single-loop e al grafo a stati. Aggiunte anche il pannello Effort e il Fast Mode (2.5x velocita' a un terzo del costo). Sezioni aggiornate: Come funziona, Varianti, Esempi (nuovo Esempio 3), Note operative. [Digest 2026-05-29](../../digest/2026/05/29.md)

Separazione loop/esecuzione per l'enterprise. Annunciate il 19 maggio a Code with Claude London, le self-hosted sandboxes di Claude Managed Agents (public beta) spostano l'esecuzione dei tool nell'infrastruttura del cliente mantenendo il loop su Anthropic; gli MCP tunnels (research preview) danno accesso outbound-only a MCP server in rete privata. E' il pattern che ha sbloccato l'adozione in finanza, healthcare e legal. Aggiunto un asse "managed vs self-hosted" e un nuovo Esempio 4. [Digest 2026-05-28](../../digest/2026/05/28.md)

Documentazione dell'isolamento. Il 30 maggio Anthropic pubblica "How we contain Claude across products", prima descrizione tecnica completa dei tre sandbox (gVisor per Claude.ai, Seatbelt/Bubblewrap per Claude Code, VM full-OS per Claude Cowork). Rafforzata la sezione Sicurezza e la nota operativa sui tool. [Digest 2026-05-31](../../digest/2026/05/31.md)

Evidenza empirica sul peso dell'harness. Il paper "Is Grep All You Need?" (arXiv 2605.15184, 14 maggio) mostra che la varianza di accuratezza tra harness diversi supera quella tra metodi di retrieval a parita' di modello e dati. Integrato in Cos'e, negli anti-pattern e nella nota operativa sull'eval. [Digest 2026-05-16](../../digest/2026/05/16.md)

Contesto competitivo e MCP production-grade. Aggiornata la mappa degli harness con Grok Build 0.1 (sub-agenti paralleli + Arena Mode, [Digest 2026-05-26](../../digest/2026/05/26.md)), Cursor Composer 2.5 ([Digest 2026-05-25](../../digest/2026/05/25.md)), Codex Goal mode ([Digest 2026-05-24](../../digest/2026/05/24.md)), Google Antigravity 2.0 con CLI/SDK/Managed Agents ([Digest 2026-05-20](../../digest/2026/05/20.md)), e ARIS come research harness open-source ([Digest 2026-05-07](../../digest/2026/05/07.md)). MCP entra nei workflow production con il Google Pay & Wallet MCP Server ([Digest 2026-05-29](../../digest/2026/05/29.md)).

### 2026-06-13

Claude Code v2.1.172 (10 giugno, 6 fonti) rimuove il vincolo che impediva ai subagenti di avviare propri subagenti. L'harness gestisce ora alberi di sessioni fino a 5 livelli di profondita': ogni nodo e' un'istanza harness completa con context window, system prompt e selezione di modello propri; il parent riceve solo il riepilogo del figlio. Dal punto di vista dell'harness la novita' e' strutturale: il loop agentico non e' piu' una struttura a due livelli (orchestratore + worker piatti) ma una gerarchia ricorsiva. Il context manager del parent e' parzialmente esonerato dal tenere traccia dello stato dei sotto-task profondi, che restano confinati nel context del nodo figlio. Il rovescio e' che la cost governance si complica: ogni nodo della gerarchia consuma token indipendentemente e il costo totale del run e' la somma dei costi dell'intero albero, senza visibilita' diretta dal nodo radice. [Digest 2026-06-13](../../digest/2026/06/13.md)

### 2026-06-16

Claude Agent SDK (Anthropic, 15 giugno, 6 fonti) introduce pool di crediti separati per uso non-interattivo (CLI -p, GitHub Actions, agenti di terze parti): $20/mese Piano Pro, $100 Max 5x, $200 Max 20x, senza rollover mensile. Dal punto di vista dell'harness, la novita' e' la separazione finanziaria come primitiva di architettura: i run autonomi pianificati — cronjob, pipeline CI/CD, agenti embedded in prodotti di terze parti — consumano da un budget dedicato, separato dal budget dell'utente interattivo. Il costo di un harness in produzione diventa una linea di spesa configurabile e monitorabile indipendentemente dall'uso manuale. Le implicazioni pratiche per il design dell'harness: il pool di crediti e' il limite naturale per il rate limiting dei run autonomi (un harness che supera il budget mensile si blocca, non degrada silenziosamente); l'assenza di rollover impone di dimensionare correttamente il budget mensile al momento della sottoscrizione, non a consuntivo. Il pattern si inserisce nel piu' ampio movimento verso harness con cost governance esplicita: dopo la visibilita' sui costi per nodo introdotta con la gerarchia multi-livello (13 giugno), il pool dedicato introduce una frontiera finanziaria tra uso umano e uso agentico. [Digest 2026-06-16](../../digest/2026/06/16.md)

### 2026-06-17

A partire dal 23 giugno 2026, l'accesso a Fable 5 esce dai piani Pro/Max/Team/Enterprise e richiede un pool di crediti prepagati a tariffe API ($10/M input, $50/M output — circa 2,0 crediti/1k input e 10 crediti/1k output). Sommato al pool separato introdotto il 15 giugno per l'uso non-interattivo del Claude Agent SDK, un harness in produzione su piano Pro o Max deve ora tracciare due budget paralleli con semantiche diverse: il pool del 15 giugno copre `claude -p`, GitHub Actions e SDK headless (reset mensile); il pool del 23 giugno copre l'uso di Fable 5 via subscription indipendentemente dalla modalita'. Il pattern che emerge e' un'architettura di billing a strati: uso interattivo (incluso nel piano), uso agentico automatizzato (pool Agent SDK), uso del modello premium (pool Fable 5). Per chi progetta harness, questo implica monitoraggio separato dei tre canali di consumo, configurazione di alert per ciascun pool, e scelta deliberata del modello per minimizzare il costo del layer premium. [Digest 2026-06-17](../../digest/2026/06/17.md)

### 2026-06-19

CORREZIONE ai digest del 16 e 17 giugno: il pool di crediti separato per Agent SDK non e' mai entrato in vigore. Anthropic ha sospeso il cambiamento il 15 giugno 2026 — stesso giorno previsto per l'entrata in vigore — comunicandolo via email agli utenti ("nothing changes for now"). Agent SDK, `claude -p` e GitHub Actions continuano a drenare dal pool standard della subscription senza pool separato. Le entry del 16 e 17 giugno in questa sezione descrivevano uno stato che non e' mai diventato operativo. Le cause della retromarcia: pressione developer (il pool a tariffe API avrebbe aumentato i costi per gli heavy user rispetto alla subscription flat), price war con OpenAI (che mantiene la propria subscription inclusiva dell'Agent SDK), e contesto pre-IPO. Il segnale per chi progetta harness e' che il modello finanziario del layer agentico rimane in corso di definizione; qualsiasi progettazione di cost governance per harness su subscription dovrebbe essere considerata provvisoria fino a conferma ufficiale. [Digest 2026-06-19](../../digest/2026/06/19.md)

### 2026-06-29

Google chiude Gemini CLI (copertura mancata dal 18 giugno, 6 fonti: The Register, The New Stack, aibuilderclub, byteiota, TechTimes, cloudnews.tech): il progetto open-source Apache 2.0, con 6.000 pull request aperte da contributor esterni, viene rimpiazzato da Antigravity CLI, un fork closed-source scritto in Go senza partecipazione della community. L'episodio e' rilevante per il concetto di harness per due ragioni. Prima, il pattern open/closed-source nelle CLI agentiche: Gemini CLI aveva lanciato il 25 maggio come CLI agentica open-source, generando 6.000 PR di community in tre settimane; la chiusura del repo e il lancio di Antigravity CLI senza migrare nessuna delle 6.000 PR e' un caso documentato di "bait-and-switch" (The Register), che solleva la questione del rischio per chi investe in contribuzioni a harness open-source di grandi vendor. Seconda, il pattern architetturale: Antigravity CLI in Go e' distinto dall'SDK Python/TypeScript di Google Antigravity 2.0 (lanciato il 20 maggio, coperto digest 05-20); Google gestisce ora tre harness separati (Antigravity CLI, Antigravity SDK, Vertex AI Agent Builder) con gradi di apertura diversi, illustrando la tensione tra harness di sviluppo open e harness di produzione closed. La decisione di non migrare le PR aperte conferma su scala di prodotto il finding del paper "Is Grep All You Need?": l'harness specifico — non solo il modello — e' la variabile che il vendor vuole controllare. [Digest 2026-06-29](../../digest/2026/06/29.md)
