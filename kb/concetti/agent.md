---
name: AI Agent
aliases: [agent, AI agent, agente autonomo, autonomous agent]
categoria: paradigma
created: 2026-04-28
last_updated: 2026-05-28
mentions_count: 49
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

### 2026-05-01

Mistral lancia Vibe remote agents come prodotto companion di Mistral Medium 3.5: sessioni di coding asincrone che girano nel cloud, avviabili da CLI o da Le Chat, con connettori nativi per GitHub, Linear, Jira, Sentry e Slack. Il pattern e' rilevante perche' porta l'architettura agentica direttamente nel workspace dello sviluppatore senza richiedere un harness custom: orchestrazione, sandbox, tool calling e report sono gestiti dalla piattaforma. OpenAI lancio contestuale di GPT-5.5-Cyber, modello per difesa informatica con accesso ristretto via TAC program: primo esempio di agente specializzato per cybersecurity da un frontier lab, con governance di accesso separata dal modello consumer. [Digest 2026-05-01](../../digest/2026/05/01.md)

### 2026-05-02

Due segnali agentici nel digest di oggi. Claude Code v2.1.126 porta miglioramenti operativi all'harness piu' usato per coding agentico: project purge, OAuth in ambienti non-browser, model picker gateway-aware. Il Pentagon AI classified deal (7 aziende su IL6/IL7) segnala che i sistemi agentici entrano nei contesti piu' sensibili della difesa: AWS, Google, Microsoft, OpenAI, SpaceX, NVIDIA e Reflection ottengono accesso per analisi dati e decision-making su campo di battaglia, mentre Anthropic resta fuori per aver rifiutato di rinunciare ai guardrail. La dicotomia e' rilevante per chi progetta sistemi agentici enterprise: le restrizioni di deployment non sono solo tecniche ma politiche, e le scelte di policy del vendor di modelli impattano direttamente la disponibilita' del servizio in segmenti governativi. [Digest 2026-05-02](../../digest/2026/05/02.md)

### 2026-05-03

Microsoft porta Agent 365 in general availability: e' il primo prodotto di governance per agenti AI a raggiungere GA da un vendor hyperscaler. Il control plane unificato copre Windows endpoint, Azure, AWS Bedrock e Google Cloud, e introduce il concetto di "shadow AI discovery" — rilevamento automatico degli agenti non registrati nell'inventario centralizzato. Il pricing standalone ($15/utente/mese) o bundled in M365 E7 indica che la governance degli agenti diventa un costo operativo standard nelle aziende enterprise, analogo alla governance delle identita'. Il lancio posiziona Microsoft come fornitore dell'infrastruttura di controllo sulla quale le organizzazioni deployana agenti di tutti i vendor (inclusi OpenAI, Anthropic e agenti custom). [Digest 2026-05-03](../../digest/2026/05/03.md)

### 2026-05-04

Writer introduce trigger event-based per i propri agenti enterprise (30 aprile 2026): gli agenti ascoltano segnali di business in tempo reale — email, call, aggiornamenti documento, messaggi Slack — e avviano autonomamente i playbook corrispondenti senza che un utente inizi l'interazione. Il pattern si chiama "agente ambient" e rappresenta un cambio architetturale rispetto all'agente on-demand: invece di aspettare un prompt, l'agente e' sempre attivo in ascolto. Le integrazioni native coprono Gmail, Gong, Google Calendar, Google Drive, Microsoft SharePoint, Slack, Microsoft Teams. Il caso Writer si aggiunge a Microsoft Agent 365 (governance) e Mistral Vibe remote agents (coding asincrono) come segnale che il modello di deployment agentico si sta spostando da "tool invocato" a "processo continuo in background". [Digest 2026-05-04](../../digest/2026/05/04.md)

### 2026-05-05

Tre segnali convergenti sul fronte del deployment agentico enterprise. Sierra chiude un Series E da $950 milioni a $15,8 miliardi di valutazione: e' il piu' grande round annunciato per un pure-play di agenti customer service, con Tiger Global e GV come lead. Anthropic lancia una nuova societa' standalone da $1,5 miliardi con Blackstone, Goldman Sachs, Hellman & Friedman e altri PE per embedded ingegneri Anthropic dentro le aziende clienti — il modello e' forward-deployed engineer, schema Palantir applicato agli agenti Claude. Lo stesso giorno OpenAI finalizza "The Deployment Company" (DeployCo) con $4 miliardi da 19 investitori PE a $10 miliardi di valutazione, stessa logica di integrazione profonda. Il segnale aggregato: la competizione tra lab frontier si sposta dall'architettura del modello all'integrazione nei processi operativi aziendali, con i fondi PE come canale di distribuzione primario. [Digest 2026-05-05](../../digest/2026/05/05.md)

### 2026-05-07

Cinque occorrenze agentiche nel digest di oggi, distribuite su tre aree distinte. Anthropic lancia 10 agent template per financial services (pitchbook, KYC, AML, ledger reconciliation) disponibili come plugin in Claude Cowork, Claude Code e Claude Managed Agents: primo set di template di dominio preconfigurati da un frontier lab per una vertical specifica, con benchmark di valutazione proprietario (Vals AI Finance Agent, Claude Opus 4.7 al 64,37%). FIS annuncia il Financial Crimes AI Agent sviluppato con Anthropic: comprime le investigazioni AML da giorni a minuti operando su piu' sistemi bancari in parallelo, con due banche (BMO, Amalgamated Bank) gia' in sviluppo e GA prevista per H2 2026. Al Code w/ Claude 2026 (San Francisco, 6 maggio), Anthropic lancia Code Review (revisione automatica del codice, in uso a ogni team interno) e Remote Agents (controllo del desktop dallo smartphone): due pattern agentici applicati al workflow dello sviluppatore. ARIS (arXiv 2605.03042) introduce l'adversarial multi-agent collaboration come meccanismo di assurance per la ricerca ML autonoma: un executor e un reviewer di famiglie di modelli diverse per intercettare errori correlati che il self-refinement mono-modello manca. [Digest 2026-05-07](../../digest/2026/05/07.md)

### 2026-05-13

Tre segnali agentici nel digest di oggi. Anthropic ricostruisce Thomson Reuters CoCounsel Legal interamente sul Claude Agent SDK: e' il primo sistema di ricerca giuridica commerciale ad alta scala (1M+ professionisti) che usa l'SDK come base operativa, con un'architettura multi-agente che pianifica l'inquiry, seleziona tool, recupera da Westlaw/Practical Law/KeyCite e si adatta mid-workflow via MCP. OpenAI lancia Daybreak, piattaforma agentica per la difesa informatica che usa Codex Security in loop per identificare attack path, testare vulnerabilita' in sandbox e proporre patch: 3.000+ problemi critici gia' corretti in 1.000+ progetti open source. Thinking Machines Lab presenta TML-Interaction-Small con un design a due livelli: un modello di interazione time-aware per il real-time (micro-turn da 200 ms) e un modello asincrono in background per il ragionamento esteso e l'uso di tool — una separazione esplicita tra il piano dell'interazione e il piano dell'execution che si avvicina al pattern orchestratore-worker applicato a un singolo sistema conversazionale. [Digest 2026-05-13](../../digest/2026/05/13.md)

### 2026-05-10

Google DeepMind pubblica l'AI Co-Mathematician (arXiv 2605.06651), il primo sistema multi-agente documentato ad affrontare matematica frontier con collaborazione umana verificata. L'architettura e' un workspace statefulness e asincrono in cui un agente "project coordinator" orchestra in parallelo piu' research workstream (ideazione, ricerca bibliografica, esplorazione computazionale, dimostrazione di teoremi, scrittura LaTeX). Il pattern e' rilevante per il concetto di agent perche' estende l'architettura orchestratore-worker a un dominio ad alta struttura formale — la matematica — in cui la verifica degli output (dimostrazioni) e' oggettiva e il costo di un errore propagato e' elevato. Risultato di sistema: 48% su FrontierMath Tier 4, nuovo record. Caso documentato: Marc Lackenby (Oxford) ha usato il sistema per risolvere il problema 21.10 del Kourovka Notebook; il reviewer-agent ha individuato un errore nella prima dimostrazione, e Lackenby ha trovato la correzione. Il caveat centrale rimane valido anche in questo contesto: il sistema opera senza cap di token o chiamate, rendendo il confronto con altri benchmark non direttamente comparabile in termini di costo. [Digest 2026-05-10](../../digest/2026/05/10.md)

### 2026-05-15

Microsoft MDASH (multi-model agentic scanning harness) entra in produzione come sistema di sicurezza: piu' di 100 agenti AI specializzati orchestrati su una pipeline a cinque stadi (prepare, scan, validate, dedup, prove) per la scoperta autonoma di vulnerabilita' in codebase complessi come Windows. In produzione, MDASH ha trovato 16 delle falle corrette nel Patch Tuesday di maggio 2026, incluse 4 RCE critiche. Il pattern architetturale e' rilevante: agenti specializzati per classe di vulnerabilita', un modello frontier per il ragionamento pesante, modelli distillati come debater ad alto volume, un secondo frontier per verifica indipendente, plugin di dominio per contesto non inferibile dai pesi. Il risultato (88,45% su CyberGym, primo posto) e' il primo caso documentato di un sistema multi-agente che raggiunge prestazioni di produzione in security research — un campo storicamente resistente all'AI per la necessita' di exploit proof-of-concept verificabili. [Digest 2026-05-15](../../digest/2026/05/15.md)

### 2026-05-20

Google I/O 2026 introduce due sistemi agentici di rilievo. Gemini Spark e' il primo agente Google progettato per girare 24/7 su virtual machine cloud-side indipendenti dal dispositivo dell'utente: accede a Gmail, Docs, Slides, Calendar e completa task multi-step in background (sintetizzare note di riunione, redigere email, costruire documenti) senza richiedere un prompt attivo. Il pattern e' l'agente ambient a livello di produttivita' — lo stesso che Writer e Microsoft Agent 365 hanno esplorato in ambienti enterprise — applicato ora all'ecosistema consumer Google. La disponibilita' e' scaglionata: beta per trusted tester questa settimana, AI Ultra subscriber la settimana successiva. Google Antigravity 2.0 introduce un livello di astrazione piu' alto per gli sviluppatori: una desktop app standalone, un CLI e un SDK per orchestrare piu' agenti in parallelo, con Managed Agents nel Gemini API come ambiente Linux isolato di execution. Il modello di default e' Gemini 3.5 Flash. I due sistemi convergono sullo stesso punto: l'unita' di deployment AI si sposta dal singolo LLM call all'agente persistente con stato, memoria e capacita' di azione su sistemi esterni. [Digest 2026-05-20](../../digest/2026/05/20.md)

### 2026-05-14

Google presenta Gemini Intelligence all'Android Show 2026 come esempio di sistema agentico a scala OS: Gemini si muove tra applicazioni, comprende cio' che e' sullo schermo e completa task cross-app in modo autonomo (prenotazioni, costruzione carrelli, recupero email, navigazione siti) senza che l'utente passi manualmente da un'app all'altra. Il pattern architetturale rilevante e' l'agente ambient a livello di sistema operativo: l'agente non e' invocato per singole richieste ma e' sempre presente come strato di orchestrazione sul dispositivo, accede al contesto multi-app in tempo reale e agisce su screen state. Il rollout inizia estate 2026 su Pixel e Galaxy; si espande a watch, auto, occhiali e laptop. L'annuncio segnala che il paradigma agentico si estende ora al livello di OS consumer, oltre che all'enterprise software. [Digest 2026-05-14](../../digest/2026/05/14.md)

### 2026-05-23

Due contributi rilevanti per il concetto di agent. MOSS (arxiv 2605.22794, HKUST/Tsinghua/Alibaba DAMO, submission 21 maggio) introduce la prima architettura documentata di auto-evoluzione agentica tramite riscrittura del codice sorgente in produzione: l'agente accumula failure di produzione, genera candidati di fix delegando l'editing a un coding-agent CLI esterno, verifica in worker effimeri e si aggiorna via container swap in-place. Su OpenClaw, il punteggio medio su quattro task sale da 0.25 a 0.60 in un singolo ciclo evolutivo senza supervisione umana. Il contributo metodologico e' la distinzione tra scope di adattamento: MOSS sostiene che la riscrittura del source code e' l'unico meccanismo Turing-completo, deterministico e immune al context drift — una posizione rilevante per chi progetta agenti a lunga durata di vita in produzione. Qwen3.7-Max (Alibaba Cloud Summit, 20-21 maggio) e' il nuovo modello frontier per agenti di Alibaba: 1M token di context, extended thinking, ottimizzato esplicitamente per i principali CLI agent framework (OpenClaw, Claude Code, Hermes Agent). In un test interno ha sostenuto esecuzione autonoma per 35 ore con 1.000+ tool call su un task complesso. Entrambe le notizie convergono sullo stesso segnale: il design degli agenti si sta spostando dall'orizzonte di pochi minuti (singolo task) verso sessioni di ore/giorni, con conseguenti esigenze di persistenza di stato, tolleranza al fallimento e auto-correzione. [Digest 2026-05-23](../../digest/2026/05/23.md)

### 2026-05-24

Due aggiornamenti sul paradigma agentico. OpenAI porta Goal mode di Codex alla stabilita' (21 maggio): l'agente di coding puo' ora perseguire un obiettivo complesso per ore o giorni senza supervisione attiva, e' disponibile nell'app, nell'IDE extension e nella CLI. La funzionalita' era in beta da aprile; la promozione a stabile segnala che OpenAI ritiene il pattern affidabile per uso continuativo. L'aggiunta di Appshots (contesto visuale dall'app in primo piano via doppio Command) e del controllo remoto con Mac bloccato completa la transizione di Codex da co-pilota interattivo ad agente semi-autonomo persistente. Jack Clark (co-fondatore Anthropic) ha previsto alla 2026 Cosmos Lecture di Oxford (20 maggio) che le prime aziende gestite interamente da AI — senza management umano — genereranno milioni di dollari di ricavi entro 18 mesi. La previsione e' la prima affermazione pubblica con timeline specifica da un fondatore di lab frontier sull'emergere di "agent-only companies" come categoria di business autonoma; si posiziona piu' vicina alla concretezza rispetto ad analoghe previsioni di Altman e Hassabis sullo stesso tema. [Digest 2026-05-24](../../digest/2026/05/24.md)

### 2026-05-25

Cursor lancia Composer 2.5, un coding agent basato su Kimi K2.5 con post-training proprietario (RL su 25x piu' task sintetici del predecessore): raggiunge 79,8% su SWE-Bench Multilingual — essenzialmente a parita' con Claude Opus 4.7 (80,5%) — a un decimo del costo. Il modello opera esclusivamente come agente inside l'IDE e CLI Cursor: legge e modifica piu' file in parallelo, esegue comandi in terminale, itera su test falliti senza input umano. Il lancio segnala che il paradigma "agente di coding specializzato" ha raggiunto parita' con i modelli frontier generalisti sulle metriche chiave, rendendo la specializzazione post-training su open-weight la strategia di default per i tool builder. [Digest 2026-05-25](../../digest/2026/05/25.md)

### 2026-05-27

Due segnali agentici nel digest di oggi. Anthropic pubblica il primo update di Project Glasswing (25-26 maggio): Claude Mythos Preview — il modello piu' avanzato di Anthropic con 93,9% su SWE-bench Verified — ha operato autonomamente come agente di security scanning su 1.000+ progetti open source, trovando 6.202 vulnerabilita' high/critical in scansione non presidiata. Il comportamento documentato (raccolta automatica di target, esecuzione di analisi iterativa, classificazione per severita') e' un esempio di agente autonomo specializzato su un task di lunga durata con output verificabile. In parallelo, il sighting del toggle "claude-mythos-1-preview" in Claude Code pubblico il 25 maggio segnala che Anthropic sta preparando l'integrazione di Mythos nell'harness di coding agent piu' usato — un'espansione dell'architettura agentica di Claude Code verso capacita' di security research. L'ostacolo dichiarato al rilascio e' di governance, non tecnico: la velocita' di discovery supera la capacita' di patching dell'ecosistema. [Digest 2026-05-27](../../digest/2026/05/27.md)

### 2026-05-28

Tre segnali agentici nel digest di oggi. Anthropic rilascia Claude Managed Agents con self-hosted sandboxes (public beta) e MCP tunnels (research preview): il loop agentico — orchestrazione, context management, error recovery — rimane su Anthropic, mentre l'esecuzione dei tool si sposta nell'infrastruttura del cliente o di provider come Cloudflare, Daytona, Modal, Vercel. I MCP tunnels permettono agli agenti di raggiungere server MCP nella rete privata dell'azienda senza esporre endpoint pubblici. La coppia di funzionalita' rimuove i due principali blocchi all'adozione enterprise degli agenti in ambienti regulated (healthcare, legal, finance): il controllo dei dati e l'esposizione dei sistemi interni. KPMG e PwC, i due Big Four che hanno siglato global alliance con Anthropic nella settimana del 14-19 maggio, prevedono entrambi deployment di workflow agentici come caso d'uso primario: KPMG menziona esplicitamente "agentic workflows in real time" come funzionalita' core di Digital Gateway. I tre segnali convergono su un tema comune: il paradigma agentico e' passato dalla fase di prototipazione alla fase di infrastruttura enterprise, con richieste specifiche di governance (sandbox isolato, rete privata, certificazioni) che i frontier lab stanno soddisfacendo con architetture dedicate. [Digest 2026-05-28](../../digest/2026/05/28.md)

### 2026-05-26

Tre segnali agentici nel digest di oggi. xAI lancia Grok Build 0.1 (20 maggio), il primo coding agent CLI proprietario di xAI: 8 sub-agenti paralleli, Arena Mode (piu' agenti competono sullo stesso task e vengono classificati automaticamente prima che il risultato raggiunga lo sviluppatore), architettura local-first, 256K context, 70,8% SWE-Bench Verified. La mossa porta xAI nel segmento coding agentico dove il valore si misura su task completion, non su chat quality. Google apre gradualmente Gemini for Science, la piattaforma annunciata a I/O 2026 che unifica tre moduli agentici — Literature Insights (NotebookLM), Hypothesis Generation (Co-Scientist) e Computational Discovery (AlphaEvolve+ERA) — per la ricerca scientifica. Computational Discovery in particolare e' un agente evolutivo che genera e valuta in parallelo migliaia di varianti di codice, estendendo il paradigma agentico dal dominio engineering al dominio della scoperta scientifica strutturata. Il pattern aggregato della settimana e' coerente con il trend tracciato nei digest precedenti: il paradigma agentico si sta frammentando in specializzazioni verticali — coding (Claude Code, Cursor, Codex, Grok Build), ricerca scientifica (Gemini for Science, AI Co-Mathematician), manifattura (Mistral/Emmi AI LEMs) — con architetture diverse per ciascun dominio e benchmark di valutazione sempre piu' verticali. [Digest 2026-05-26](../../digest/2026/05/26.md)
