---
name: Multi-agent orchestration
aliases: [multi-agent, sistema multi-agente, orchestrazione di agenti, agent swarm, subagenti, sub-agent orchestration]
categoria: paradigma
created: 2026-06-01
last_updated: 2026-06-01
mentions_count: 8
---

# Multi-agent orchestration

## Cos'e

La multi-agent orchestration e' il paradigma in cui piu' istanze di [agent](./agent.md) — non un singolo loop agentico — collaborano, in parallelo o in pipeline, per risolvere un task troppo grande, troppo lungo o troppo eterogeneo per un agente solo. Un componente coordinatore (orchestrator, project coordinator, meta-agente) decompone il problema, assegna i sotto-task a worker specializzati, raccoglie i risultati parziali e li integra in un output finale. La differenza rispetto a un agente singolo non e' solo quantitativa: cambia il modo in cui il lavoro viene strutturato e, soprattutto, dove vive lo stato.

Il tema e' diventato centrale nella primavera 2026 perche' i provider hanno trasformato l'orchestrazione multi-agente da pattern di ricerca a feature di prodotto. xAI ha lanciato Grok Build 0.1 con un'architettura che spawna fino a otto sub-agenti concorrenti su un workflow plan-search-build, piu' "Arena Mode" in cui piu' agenti affrontano lo stesso problema e vengono classificati prima che il risultato arrivi allo sviluppatore. Anthropic ha pubblicato Claude Opus 4.8 con Dynamic Workflows, in cui Claude scrive uno script JavaScript che orchestra fino a 1.000 subagenti totali per run (16 in parallelo) eseguiti in background. Microsoft ha pre-annunciato la Copilot Agent Mode, dove Copilot diventa un meta-agente che progetta e orchestra swarm di sub-agenti da descrizioni in linguaggio naturale. Sul lato ricerca, l'AI Co-Mathematician di Google DeepMind e MDASH di Microsoft hanno mostrato sistemi con decine o centinaia di agenti specializzati in produzione.

Il valore dell'orchestrazione multi-agente e' triplice. Primo, parallelismo: sotto-task indipendenti girano simultaneamente, riducendo la latenza wall-clock. Secondo, specializzazione: agenti diversi possono usare modelli, tool e prompt diversi, ciascuno ottimizzato per il proprio compito (un frontier model per il ragionamento pesante, modelli distillati come "debater" ad alto volume, un modello di una famiglia diversa come reviewer indipendente). Terzo, gestione del [context window](./context-window.md): il coordinamento vive fuori dal contesto del modello principale, evitando l'overflow su task multi-step a scala di codebase.

## Come funziona

Lo schema generale prevede tre ruoli, che possono essere svolti da modelli diversi o dallo stesso modello con prompt diversi.

Orchestrator. Riceve l'obiettivo di alto livello, lo decompone in sotto-task, decide la topologia (sequenziale, parallela, gerarchica), assegna i sotto-task ai worker e gestisce dipendenze ed errori. Nelle Dynamic Workflows di Anthropic l'orchestrazione e' codice: il modello scrive uno script che lancia subagenti, mette i risultati intermedi in variabili dello script e passa al context solo la risposta finale. Questo e' un punto architetturale chiave — sposta il coordinamento dal linguaggio naturale (fragile, costoso in token) al codice (deterministico, ispezionabile).

Worker (subagenti). Ogni worker e' un'istanza agentica con il proprio loop, i propri tool e, spesso, il proprio [agent-harness](./agent-harness.md). Lavora su un sotto-task circoscritto, con un contesto ridotto e mirato. La specializzazione puo' essere per fase (plan, search, build), per dominio (un agente per il kernel networking, uno per l'authentication stack, come nei plugin di dominio di MDASH) o per ruolo (executor vs reviewer).

Aggregator / verifier. Raccoglie gli output dei worker e li integra. Spesso include un passo di verifica: in ARIS l'assurance pipeline e' a tre stadi (integrity check, result-to-claim mapping, claim audit); in MDASH un modello frontier separato fornisce una verifica indipendente; nell'AI Co-Mathematician un agente reviewer ha identificato un errore in una dimostrazione prima che venisse promossa.

Topologie ricorrenti. La pipeline sequenziale incatena agenti in cui l'output di uno e' l'input del successivo (plan -> search -> build). Il fan-out parallelo lancia N worker indipendenti sullo stesso sotto-problema o su sotto-problemi disgiunti, poi aggrega. La gerarchia annida orchestratori: un coordinatore di alto livello delega a coordinatori di sotto-dominio, che a loro volta gestiscono worker. L'arena / debate mette piu' agenti in competizione o contraddittorio sullo stesso task, selezionando la soluzione migliore (Arena Mode di Grok Build, debater di MDASH, adversarial collaboration cross-model di ARIS).

Adversarial collaboration cross-model. Un pattern emerso con forza e' usare un executor di una famiglia di modelli e un reviewer di una famiglia diversa, per intercettare errori correlati che il self-refinement mono-modello manca sistematicamente. ARIS usa Claude Code come executor e un modello di altra famiglia come reviewer; MDASH alterna frontier model per il ragionamento e un frontier model separato per la verifica.

Considerazioni quantitative. Il parallelismo riduce la latenza ma non il costo: 1.000 subagenti consumano i token di 1.000 esecuzioni. La gestione del fallimento si complica: con N worker, la probabilita' che almeno uno fallisca cresce con N, e l'orchestrator deve gestire retry, rollback e risultati parziali. Oltre una certa scala, il coordinamento stesso diventa il collo di bottiglia — ragione per cui spostarlo in codice (Dynamic Workflows) o in uno script di routing esplicito (i cinque workflow di ARIS) e' preferibile a coordinare via prompt in linguaggio naturale.

## Varianti / approcci

| Approccio | Topologia | Coordinamento | Esempio nei digest |
|---|---|---|---|
| Sub-agenti paralleli | Fan-out su fasi | Workflow fisso plan-search-build | Grok Build 0.1 (8 sub-agenti) |
| Subagenti orchestrati da codice | Gerarchica, fino a 1.000 | Script JavaScript, stato fuori dal context | Opus 4.8 Dynamic Workflows |
| Swarm da NL | Dinamica | Meta-agente progetta lo swarm | Copilot Agent Mode |
| Ensemble di modelli specializzati | Pipeline 5-stage | Plugin di dominio + verifica indipendente | MDASH (100+ agenti) |
| Research workstream paralleli | Coordinatore stateful asincrono | Project coordinator | AI Co-Mathematician |
| Adversarial cross-model | Executor + reviewer | Routing al modello reviewer | ARIS |

L'asse "coordinamento in NL vs in codice". Coordinare via linguaggio naturale (l'orchestrator descrive a parole cosa fare) e' flessibile ma fragile e costoso: ogni passaggio rigenera contesto. Coordinare via codice (l'orchestrator scrive uno script che chiama i worker) e' piu' rigido ma deterministico, ispezionabile e mantiene lo stato fuori dal context window. Dynamic Workflows e' l'esempio piu' netto del secondo approccio.

L'asse "stesso modello vs modelli eterogenei". Usare la stessa famiglia per tutti i ruoli e' semplice ma soffre di errori correlati. Usare modelli eterogenei (frontier per il reasoning, distillati per il volume, una famiglia diversa per il review) e' il differenziatore di ARIS e MDASH: la diversita' delle distribuzioni di errore aumenta la probabilita' di intercettare gli sbagli.

## Quando usarlo / quando no

La multi-agent orchestration e' la scelta giusta quando il task e' decomponibile in sotto-task parallelizzabili (esplorare piu' ipotesi, scansionare piu' moduli), quando l'orizzonte e' lungo e satura il [context window](./context-window.md) di un singolo agente (migrazione di una codebase da centinaia di migliaia di righe), quando la verifica indipendente aggiunge affidabilita' (security, dimostrazioni matematiche), o quando la specializzazione per dominio batte un generalista.

E' la scelta sbagliata quando il task e' intrinsecamente sequenziale e non si decompone — l'orchestrazione aggiunge solo overhead di coordinamento. E' sbagliata quando il budget e' stretto: N agenti costano N volte. E' sbagliata quando un singolo loop agentico con buon [tool use](./tool-use.md) basta — il principio di parsimonia vale anche qui: non introdurre un'orchestra dove serve un solista.

Anti-pattern. Orchestrazione via prompt in linguaggio naturale su task lunghi: il contesto si gonfia, i risultati intermedi si perdono. Fan-out senza aggregazione robusta: N risposte parziali che nessuno integra. Assenza di verifica: piu' agenti che propagano lo stesso errore con piu' confidenza. Mancanza di rollback: un container swap senza gate (come invece previsto in MOSS) puo' promuovere una regressione in produzione. Nessuna osservabilita': uno swarm senza tracciamento di chi ha fatto cosa e' indebuggabile.

Sicurezza. Ogni subagente eredita i rischi del singolo agente — prompt injection via [tool use](./tool-use.md), azioni distruttive — moltiplicati per il numero di agenti e amplificati dalla concorrenza. Per questo l'orchestrazione multi-agente in produzione va accoppiata a [agent-sandboxing](./agent-sandboxing.md): ogni worker gira in un ambiente isolato, e il loop di coordinamento resta su infrastruttura controllata.

## Esempi pratici

Esempio 1: migrazione di codebase con Dynamic Workflows. Per migrare centinaia di migliaia di righe da un framework all'altro, Claude Opus 4.8 scrive uno script che lancia subagenti — ciascuno su un modulo — usando la test suite esistente come criterio di accettazione. Lo script raccoglie i diff, ritenta i moduli falliti e, a convergenza, restituisce al context solo il riepilogo finale. Il context dell'utente non vede mai i mille passaggi intermedi.

Esempio 2: scansione di sicurezza con ensemble (MDASH). Una pipeline a cinque fasi (prepare, scan, validate, dedup, prove) orchestra oltre 100 agenti: frontier model per il ragionamento sulle vulnerabilita', modelli distillati come debater ad alto volume, un frontier model separato per la verifica indipendente, plugin di dominio che iniettano convenzioni del kernel e invarianti dei lock. In produzione il sistema ha identificato 16 vulnerabilita' corrette in un Patch Tuesday, incluse 4 RCE critiche.

Esempio 3: ricerca matematica collaborativa (AI Co-Mathematician). Un project coordinator orchestra in parallelo workstream di ideazione, ricerca bibliografica, esplorazione computazionale e dimostrazione, gestendo esplicitamente l'incertezza e le ipotesi fallite. Un agente reviewer ha intercettato un errore in una dimostrazione, permettendo a un matematico umano di colmarlo: il sistema ha raggiunto il 48% su FrontierMath Tier 4 (vedi [evaluation-benchmark](./evaluation-benchmark.md)).

## Letture

- Anthropic, "Claude Opus 4.8" (Dynamic Workflows), 2026. https://www.anthropic.com/news/claude-opus-4-8
- xAI, "Grok Build CLI", 2026. https://x.ai/news/grok-build-cli
- Microsoft Security Blog, "Defense at AI speed" (MDASH), 2026. https://www.microsoft.com/en-us/security/blog/2026/05/12/defense-at-ai-speed-microsofts-new-multi-model-agentic-security-system-tops-leading-industry-benchmark/
- Yang, Li, Li, "ARIS: Auto-Research-in-Sleep", arXiv 2605.03042, 2026. https://arxiv.org/abs/2605.03042
- Google DeepMind, "AI Co-Mathematician", arXiv 2605.06651, 2026. https://arxiv.org/abs/2605.06651
- Anthropic, "Building effective agents", 2024. https://www.anthropic.com/research/building-effective-agents
- Wu et al., "AutoGen: Enabling Next-Gen LLM Applications via Multi-Agent Conversation", 2023. https://arxiv.org/abs/2308.08155

## Note operative

Coordinamento fuori dal context. La lezione architetturale piu' robusta del 2026 e' che lo stato di coordinamento non deve vivere nel context window del modello orchestratore. Metterlo in codice (variabili di uno script) o in uno store esterno (wiki di ricerca persistente, come in ARIS) evita che il contesto si saturi e rende il sistema scalabile a centinaia o migliaia di subagenti. Quando il coordinamento e' inline nel prompt, la scala massima e' di pochi agenti prima che il contesto degeneri.

Eterogeneita' dei modelli. Se l'obiettivo e' affidabilita' (non solo throughput), usare modelli di famiglie diverse per executor e reviewer e' una scelta deliberata e ben supportata: gli errori dei due modelli sono meno correlati, quindi il reviewer cattura sbagli che il self-refinement mono-modello lascerebbe passare. Questo ha un costo (piu' provider, piu' integrazioni) che va messo a budget.

Parallelismo non e' gratis. Il fan-out riduce la latenza percepita ma il costo in token e in chiamate scala linearmente con il numero di worker. Un benchmark valutato "senza cap al numero di chiamate o token" (come nel caveat dell'AI Co-Mathematician) non e' comparabile a parita' di costo con un sistema vincolato: nel valutare sistemi multi-agente, fissare il budget di inferenza e' parte della metodologia, non un dettaglio.

## Aggiornamenti

### 2026-06-01

La multi-agent orchestration e' passata da pattern di ricerca a feature di prodotto in poche settimane. Grok Build 0.1 (xAI, 14-20 maggio) introduce 8 sub-agenti paralleli e Arena Mode (vedi [digest 2026-05-26](../../digest/2026/05/26.md)). Claude Opus 4.8 (Anthropic, 28 maggio) introduce Dynamic Workflows con orchestrazione di fino a 1.000 subagenti via script JavaScript, spostando il coordinamento fuori dal context window (vedi [digest 2026-05-29](../../digest/2026/05/29.md)). Microsoft pre-annuncia la Copilot Agent Mode con swarm di sub-agenti generati da descrizioni in linguaggio naturale (vedi [digest 2026-06-01](../../digest/2026/06/01.md)). Sul lato ricerca, MDASH (Microsoft) orchestra 100+ agenti su un ensemble di modelli frontier e distillati per la scoperta di vulnerabilita' (vedi [digest 2026-05-15](../../digest/2026/05/15.md)), l'AI Co-Mathematician (Google DeepMind) usa un project coordinator stateful asincrono raggiungendo il 48% su FrontierMath Tier 4 (vedi [digest 2026-05-10](../../digest/2026/05/10.md)), e ARIS formalizza l'adversarial collaboration cross-model con executor e reviewer di famiglie diverse (vedi [digest 2026-05-07](../../digest/2026/05/07.md)). Anche MOSS (vedi [digest 2026-05-23](../../digest/2026/05/23.md)) e Google Antigravity 2.0 (vedi [digest 2026-05-20](../../digest/2026/05/20.md)) rientrano nel tema. Il filo conduttore tecnico: spostare lo stato di coordinamento fuori dal contesto, usare modelli eterogenei per la verifica, e accoppiare l'orchestrazione a [agent-sandboxing](./agent-sandboxing.md) per il deployment sicuro.
