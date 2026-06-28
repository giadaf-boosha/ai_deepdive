---
name: Agent sandboxing
aliases: [sandboxing, containment, isolamento agenti, agent containment, esecuzione isolata, sandbox]
categoria: infrastruttura
created: 2026-06-01
last_updated: 2026-06-28
mentions_count: 10
---

# Agent sandboxing

## Cos'e

L'agent sandboxing (o containment) e' l'insieme delle tecniche che isolano l'ambiente in cui un [agent](./agent.md) esegue codice e tool dal resto del sistema, in modo che un agente compromesso, manipolato o semplicemente in errore non possa danneggiare dati, infrastruttura o rete oltre un perimetro definito. Mentre il loop agentico (ragionamento, pianificazione, scelta dei tool) decide cosa fare, la sandbox e' il guscio dentro cui quelle azioni — eseguire un comando, scrivere un file, fare una richiesta di rete — accadono in modo confinato.

Il tema e' diventato centrale nel 2026 perche' gli agenti hanno smesso di essere demo e sono entrati in produzione, dove eseguono codice arbitrario generato dal modello stesso o influenzato da input non fidato. Un agente che riceve un documento via [tool use](./tool-use.md) puo' subire prompt injection; un agente che genera ed esegue codice puo' produrre un comando distruttivo; un agente con accesso alla rete puo' esfiltrare dati. La sandbox non risolve questi rischi a monte, ma ne limita il blast radius: definisce esattamente cosa puo' raggiungere un agente compromesso.

La documentazione di riferimento del periodo e' il post di ingegneria Anthropic "How we contain Claude across products" (fine maggio 2026, rilanciato da Simon Willison), prima descrizione pubblica completa di come ogni prodotto Claude isola l'esecuzione: tre architetture di sandbox distinte per tre prodotti distinti. In parallelo, Claude Managed Agents ha introdotto self-hosted sandboxes (l'esecuzione dei tool si sposta nell'infrastruttura del cliente) e MCP tunnels; Mistral Vibe esegue i remote agent in sandbox isolata nel cloud; il sistema di ricerca MOSS verifica i candidati di codice in worker effimeri prima di promuoverli in produzione.

## Come funziona

Il principio guida e' il least privilege: l'ambiente di esecuzione riceve solo le capabilities strettamente necessarie, e tutto il resto e' negato per default. Le tecniche si collocano su uno spettro di forza crescente.

Process-level isolation. Il livello piu' leggero confina un processo senza una macchina virtuale completa. Su macOS, Seatbelt (il sandbox di sistema) limita le syscall e gli accessi al filesystem; su Linux, Bubblewrap crea namespace isolati (mount, PID, network, user) con capabilities minime. Anthropic usa entrambi per Claude Code, che gira in locale sulla macchina dell'utente: il processo dell'agente e' confinato con capabilities minime, riducendo cosa puo' toccare sul sistema dell'utente.

Container con kernel isolation. Un gradino sopra, gVisor (un kernel applicativo userspace) intercetta le syscall del container e le serve in uno spazio isolato, riducendo la superficie d'attacco verso il kernel dell'host rispetto a un container Linux standard. Anthropic esegue il codice di Claude.ai in un container gVisor su infrastruttura isolata, con filesystem effimero per sessione e agente interamente server-side: ogni sessione parte pulita e non lascia stato persistente.

Virtual machine completa. Il livello piu' forte e' una VM che replica le condizioni di un computer reale, con un confine hardware-assistito tra guest e host. Claude Cowork gira dentro una VM completa — Apple Virtualization Framework su macOS, Hyper-V Container System su Windows. La VM e' la scelta quando l'agente deve avere l'illusione di un computer intero (eseguire app GUI, gestire piu' processi) ma l'isolamento dall'host deve restare forte.

Worker effimeri. Una variante orientata alla verifica e' eseguire ogni candidato di azione in un worker usa-e-getta che replica le condizioni reali, poi distruggerlo. MOSS verifica ogni candidato di modifica del codice in worker effimeri che replicano i failure di produzione raccolti, e promuove la versione vincente via container swap in-place con un rollback gate. L'effimerita' garantisce che un tentativo fallito non lasci residui.

Separazione del loop dall'esecuzione. Un pattern architetturale chiave del 2026 e' separare dove vive il loop agentico da dove avviene l'esecuzione dei tool. Con i self-hosted sandboxes di Claude Managed Agents, il loop agentico (orchestrazione, context management, error recovery) resta su infrastruttura Anthropic, mentre l'esecuzione dei tool si sposta nell'ambiente del cliente (server propri o provider come Cloudflare, Daytona, Modal, Vercel). File sensibili, package e servizi interni non escono dal perimetro aziendale. Gli MCP tunnels completano il quadro: gli agenti raggiungono [MCP](./mcp.md) server nella rete privata via un gateway outbound-only, senza regole di firewall inbound ne' endpoint pubblici esposti, con traffico cifrato end-to-end.

## Varianti / approcci

| Tecnica | Forza isolamento | Costo overhead | Esempio nei digest |
|---|---|---|---|
| Seatbelt (macOS) / Bubblewrap (Linux) | Process-level | Basso | Claude Code (locale) |
| gVisor | Kernel userspace | Medio | Claude.ai (server-side) |
| VM completa | Hardware-assisted | Alto | Claude Cowork |
| Worker effimeri | Per-tentativo, usa-e-getta | Medio | MOSS (verifica candidati) |
| Self-hosted sandbox | Perimetro del cliente | Operativo | Claude Managed Agents |
| Sandbox cloud isolata | Provider-managed | Operativo | Mistral Vibe remote agents |

L'asse "forza vs overhead". Process-level isolation e' leggero e adatto a un agente locale che gira sulla macchina dell'utente; la VM e' la piu' forte ma costa in risorse e tempo di avvio. La scelta dipende dal modello di minaccia: un agente che esegue codice di terze parti o influenzato da input non fidato merita isolamento piu' forte di uno che esegue solo codice fidato in un perimetro controllato.

L'asse "dove vive il loop". Tutto server-side (Claude.ai) e' semplice ma i dati escono dal perimetro del cliente. Loop su provider + esecuzione self-hosted (Claude Managed Agents) tiene i dati sensibili in casa al costo di maggiore complessita' operativa. La scelta e' guidata dalla compliance: in finanza, healthcare e legal il controllo sui dati e la non-esposizione dei sistemi interni sono spesso vincolanti.

## Quando usarlo / quando no

La sandbox e' obbligatoria — non opzionale — quando l'agente esegue codice generato dal modello, quando elabora input non fidato (documenti, pagine web, tool result che possono contenere prompt injection), quando ha accesso a rete o filesystem, e quando opera in ambienti regolamentati dove il modello di minaccia va documentato. In pratica: qualunque agente in produzione che faccia [tool use](./tool-use.md) reale.

La sandbox e' sovradimensionata quando l'agente non esegue nulla di esterno — un assistente puramente conversazionale che genera solo testo non ha un ambiente di esecuzione da isolare. Una VM completa e' eccessiva quando basta un process-level confinement: imporre l'isolamento piu' forte ovunque introduce overhead di avvio e risorse senza guadagno di sicurezza proporzionato.

Anti-pattern. Eseguire codice generato dall'agente direttamente sull'host senza isolamento ("tanto e' solo uno script"): e' la via piu' diretta a un incidente. Concedere all'agente capabilities ampie per comodita' di sviluppo e dimenticarsi di restringerle in produzione. Trattare il tool result come fidato: un risultato di tool puo' contenere istruzioni di prompt injection, e va trattato come dato pubblico, mai come istruzione (vedi le note operative di [tool-use](./tool-use.md)). Promuovere in produzione una modifica generata dall'agente senza un rollback gate, come invece fa MOSS.

Sicurezza. La sandbox e' un controllo di contenimento, non di prevenzione: limita il danno di un agente compromesso, non impedisce che lo diventi. Va combinata con human-in-the-loop sulle azioni sensibili, con un controllo di policy separato dal modello, e con logging completo dei tool call per l'osservabilita'. Quando si orchestrano molti agenti (vedi [multi-agent-orchestration](./multi-agent-orchestration.md)), ogni worker eredita questi rischi moltiplicati: ciascuno va sandboxato, e il loop di coordinamento resta su infrastruttura controllata.

## Esempi pratici

Esempio 1: tre prodotti, tre sandbox (Anthropic). Claude.ai esegue codice in un container gVisor server-side con filesystem effimero per sessione; Claude Code, in locale, usa Seatbelt (macOS) o Bubblewrap (Linux) per confinare il processo con capabilities minime; Claude Cowork gira in una VM completa (Apple Virtualization Framework / Hyper-V Container System) che replica un computer reale. La scelta del livello segue il modello di minaccia di ciascun prodotto: piu' l'agente e' autonomo e potente, piu' forte e' l'isolamento.

Esempio 2: tenere i dati in casa (Claude Managed Agents). Una banca vuole usare agenti Claude ma non puo' far uscire file sensibili e sistemi interni dal proprio perimetro. Con i self-hosted sandboxes, l'esecuzione dei tool avviene su infrastruttura della banca mentre il loop agentico resta su Anthropic; gli MCP tunnels permettono agli agenti di raggiungere MCP server interni via gateway outbound-only, senza esporre endpoint pubblici. I due blocchi storici all'adozione enterprise (controllo dei dati, esposizione dei sistemi interni) cadono.

Esempio 3: verifica prima della promozione (MOSS). Un sistema di auto-evoluzione agentica raccoglie i failure di produzione, genera candidati di modifica del codice, e li verifica in worker effimeri che replicano i failure raccolti. Solo il candidato che supera la verifica viene promosso, via container swap in-place con rollback gate. La sandbox effimera garantisce che un candidato difettoso non contamini la produzione.

## Letture

- Anthropic Engineering, "How we contain Claude across products", 2026. https://www.anthropic.com/engineering/how-we-contain-claude
- Simon Willison, "How we contain Claude", 2026. https://simonwillison.net/2026/May/30/how-we-contain-claude/
- Anthropic, "Claude Managed Agents updates" (self-hosted sandboxes, MCP tunnels), 2026. https://claude.com/blog/claude-managed-agents-updates
- gVisor project documentation. https://gvisor.dev/docs/
- Bubblewrap (containers/bubblewrap). https://github.com/containers/bubblewrap
- MOSS, arXiv 2605.22794, 2026. https://arxiv.org/abs/2605.22794
- Mistral AI, "Vibe remote agents", 2026. https://mistral.ai/news/vibe-remote-agents-mistral-medium-3-5

## Note operative

Scegliere il livello sul modello di minaccia. Non esiste un livello "giusto" in assoluto: Seatbelt/Bubblewrap bastano per un agente locale che esegue codice fidato; gVisor e' adatto a esecuzione server-side multi-tenant; la VM serve quando l'agente deve avere un computer intero ma l'isolamento dall'host resta critico. La domanda operativa e' sempre: cosa puo' raggiungere un agente compromesso in questo ambiente, e ce ne andiamo bene?

Loop e esecuzione vanno disaccoppiati per la compliance. Il pattern "loop su provider, esecuzione self-hosted" e' la risposta del 2026 ai requisiti di settori regolamentati. Tiene i dati sensibili nel perimetro del cliente senza rinunciare all'orchestrazione gestita. Va valutato per i suoi limiti dichiarati: ad esempio i self-hosted sandbox di Claude non erano disponibili su Claude Platform su AWS e la Memory non era supportata nelle sessioni self-hosted al lancio.

La sandbox non sostituisce gli altri controlli. Contenimento, human-in-the-loop sulle azioni sensibili, controllo di policy separato dal modello e logging completo sono livelli complementari. Un agente sandboxato ma senza approvazione umana sulle azioni distruttive, o senza tracciamento dei tool call, e' ancora un rischio operativo. La sandbox limita il danno; gli altri controlli riducono la probabilita' che il danno si verifichi.

## Aggiornamenti

### 2026-06-28

Tenet Security divulga il 3 giugno la classe di attacco "Agentjacking" (CSA research note 12-14 giugno, 6 fonti): un singolo report di errore Sentry falsificato e' sufficiente per reindirizzare Claude Code, Cursor o Codex verso un server controllato dall'attaccante, che esegue codice arbitrario sulla macchina del developer. L'attacco sfrutta il fatto che gli agenti di coding consumano automaticamente l'output degli strumenti di error tracking (Sentry MCP) senza trattarlo come input non fidato — identica famiglia del prompt injection, ma con un vettore specifico: l'error tracking e' un canale considerato "safe" dall'agente, che lo eredita dall'ecosistema degli strumenti developer tradizionali dove un report di errore non puo' eseguire codice. Tenet ha identificato 2388 organizzazioni con DSN Sentry esposti; il tasso di successo nei test controllati e' stato dell'85% sui principali agenti di mercato. Sentry ha definito il problema "technically not defensible" e ha attivato un filtro su un payload specifico senza fix strutturale. L'Agentjacking aggiunge un vettore concreto allo spazio dei rischi di sandboxing: mentre il contenimento a livello OS (gVisor, Seatbelt, Bubblewrap, VM) limita il blast radius di codice arbitrario una volta eseguito, il vettore Sentry bypassa la sandbox agendo prima dell'esecuzione — influenzando la scelta del codice che l'agente decide di eseguire. La mitigazione pratica e' aggiungere un passaggio di revisione umana tra l'output degli strumenti di error tracking e qualsiasi agente a esecuzione autonoma, e trattare tutto l'output di questi strumenti come input non fidato anche se proviene dall'interno del perimetro aziendale. [Digest 2026-06-28](../../digest/2026/06/28.md)

### 2026-06-23

Google DeepMind pubblica il 18 giugno l'AI Control Roadmap (blog post Rohin Shah e Four Flynn, deepmind.google/blog/securing-the-future-of-ai-agents/): un framework defense-in-depth per agenti in produzione che assume il misalignment come scenario possibile da progettare, non da escludere. Le tre primitivi operative introdotte ampliano il vocabolario del sandboxing: (1) Supervisor Agent asincrono — un agente separato che monitora in tempo reale le traiettorie di esecuzione degli agenti operativi e scalata verso revisori umani in caso di comportamento anomalo, senza bloccare il flusso; (2) firma crittografica delle azioni, che rende ogni tool call auditabile e ricostruibile post-incident; (3) kill switch che interrompe un agente in esecuzione con serializzazione corretta dello stato. La tassonomia delle minacce e' derivata da MITRE ATT&CK adattato al contesto agentico AI (privilege escalation, data exfiltration tramite tool, prompt injection, persistenza via file di configurazione). Il sistema e' gia' in produzione su ~1 milione di task di coding agent interni a Google. Il contributo al campo del sandboxing e' concettuale oltre che tecnico: sposta la prospettiva da "costruire agenti allineati" a "costruire sistemi di controllo che funzionino anche se l'alignment e' imperfetto" — la stessa premessa che aveva portato Anthropic a descrivere le proprie sandbox di prodotto come "contenimento", non come "prevenzione". Il framework DeepMind e' il primo documento pubblico che sistematizza queste idee in una roadmap con componenti implementabili. [Digest 2026-06-23](../../digest/2026/06/23.md)

### 2026-06-07

Simon Willison rilascia micropython-wasm (6 giugno, alpha, github.com/simonw/micropython-wasm) e il plugin datasette-agent-micropython: una sandbox WASM leggera per esecuzione di Python da un agente, senza container o VM completa. Il contributo tecnico principale e' la gestione dello stato persistente nell'istanza MicroPython: il build WASM standard termina l'interprete dopo ogni chiamata, rendendo impossibile il riuso di variabili tra step agentici successivi; micropython-wasm mantiene l'istanza in vita. Il livello di isolamento e' process-level via WebAssembly (sotto gVisor e VM completa sullo spettro di forza), adatto a agenti locali trusted. Il test di sandbox escape con GPT-5.5 non ha prodotto breakout. L'HN thread (48425347) conferma la trazione. Il pattern e' trasferibile a qualsiasi framework che richieda un'opzione sandboxing piu' leggera dei container, in particolare per CLI agent e Datasette Agent ma non solo. [Digest 2026-06-07](../../digest/2026/06/07.md)

### 2026-06-01

L'agent sandboxing emerge come tema infrastrutturale ricorrente nei digest di maggio 2026. Anthropic pubblica "How we contain Claude across products", prima documentazione pubblica completa dell'isolamento di ogni prodotto Claude: gVisor per Claude.ai, Seatbelt/Bubblewrap per Claude Code, VM completa per Claude Cowork (vedi [digest 2026-05-31](../../digest/2026/05/31.md)). Claude Managed Agents introduce self-hosted sandboxes e MCP tunnels, disaccoppiando il loop agentico (su Anthropic) dall'esecuzione dei tool (nel perimetro del cliente) per sbloccare l'adozione in ambienti regolamentati (vedi [digest 2026-05-28](../../digest/2026/05/28.md)). Mistral Vibe esegue i remote agent in sandbox isolata nel cloud (vedi [digest 2026-05-01](../../digest/2026/05/01.md)). Il sistema di ricerca MOSS verifica i candidati di codice in worker effimeri con rollback gate prima della promozione in produzione (vedi [digest 2026-05-23](../../digest/2026/05/23.md)). Il filo conduttore: con gli agenti in produzione, il containment passa da dettaglio implementativo a requisito di prodotto e di compliance, ed e' la controparte difensiva necessaria della [multi-agent-orchestration](./multi-agent-orchestration.md).
