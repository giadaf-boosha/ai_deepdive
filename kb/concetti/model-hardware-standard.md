---
name: Model Hardware Standard
aliases: [MHS, Model Hardware Standard, standard hardware per agenti, driver hardware per AI]
categoria: infrastruttura
created: 2026-09-01
last_updated: 2026-09-01
---

# Model Hardware Standard

## Cos'e

Il Model Hardware Standard (MHS) e' una specifica aperta presentata da Anthropic in research preview il 27-28 agosto 2026, che fa per i dispositivi fisici quello che il [Model Context Protocol](./mcp.md) ha fatto per i tool software: definisce un'interfaccia comune con cui un agente AI puo' scoprire, leggere lo stato e comandare hardware programmabile — robot da laboratorio, microscopi, liquid handler, bracci robotici, laser, strumenti di manifattura — senza che ogni fornitore di dispositivi debba essere integrato con codice ad-hoc.

Il problema che MHS affronta e' distinto da quello risolto da MCP. MCP normalizza l'accesso a tool e dati digitali (API, database, servizi cloud): il "dispositivo" e' sempre un endpoint software con un contratto ragionevolmente esplicito. Gli strumenti fisici di laboratorio e manifattura, al contrario, espongono tipicamente interfacce proprietarie e frammentate — protocolli seriali, SDK vendor-specific, driver scritti per un singolo modello di macchina — e le loro caratteristiche operative (limiti di sicurezza, parametri regolabili, tolleranze meccaniche) esistono spesso solo in manuali cartacei o nella conoscenza tacita di un tecnico specializzato. Integrare un nuovo strumento in un workflow automatizzato ha richiesto finora settimane di lavoro di integrazione manuale per dispositivo. MHS punta a comprimere questo lavoro a ore, con un driver standardizzato e un file di riferimento leggibile sia da umani sia da agenti.

Lo standard e' nato dentro Anthropic ma e' dichiaratamente model-agnostic: non richiede Claude specificamente, e qualunque sistema AI compatibile con la specifica puo' in teoria operare lo stesso hardware una volta che il dispositivo espone un driver MHS. Anthropic ha dichiarato l'intenzione di rendere la specifica open source una volta completato il lavoro di hardening sulla sicurezza; al momento del lancio resta un research preview riservato a un primo gruppo selezionato di laboratori scientifici e produttori avanzati, tra cui Genentech e la Carnegie Mellon University.

## Come funziona

MHS si inserisce concettualmente tra l'harness dell'agente e l'hardware fisico attraverso due strati.

Il primo strato e' il driver device-specific: un componente software che gestisce la traduzione di basso livello verso qualunque interfaccia il produttore del dispositivo espone effettivamente — che sia un protocollo seriale proprietario, un'API REST del vendor, o un bus di campo industriale. Il driver espone verso l'alto un set minimo di primitive comuni a qualunque hardware programmabile: read (leggere un valore, es. una temperatura o una posizione), write (impostare un valore, es. una nuova temperatura o un comando di movimento), e discovery (annunciarsi sulla rete cosi' che un agente possa trovare il dispositivo senza conoscerne in anticipo l'indirizzo o il modello).

Il secondo strato e' il livello di protocollo standard, che rende quei driver raggiungibili da qualunque agente. Questo strato non reinventa un trasporto proprio: si appoggia a MCP, cosi' che un agente gia' equipaggiato con un client MCP puo' raggiungere un dispositivo MHS come raggiungerebbe qualunque altro MCP server, oltre a poter usare un'interfaccia a riga di comando o file di codice che incatenano comandi su piu' dispositivi in sequenza. In questo senso MHS non e' un'alternativa a MCP ma un'estensione del suo dominio d'uso: MCP resta il trasporto e il protocollo di interazione, MHS aggiunge la semantica e le garanzie necessarie per l'hardware fisico, dove un comando eseguito male ha conseguenze irreversibili nel mondo reale (un braccio robotico che urta un ostacolo, un liquid handler che versa un reagente nel contenitore sbagliato) invece che un errore recuperabile in memoria.

La parte piu' distintiva dello standard e' la descrizione del dispositivo. Ogni device MHS espone, insieme alle primitive read/write, una descrizione discoverable delle proprie caratteristiche fisiche: cosa puo' misurare, quali parametri sono regolabili e quali limiti di sicurezza vanno rispettati (peso massimo, range di temperatura, velocita' di movimento consentita). Questa descrizione non deve necessariamente essere scritta a mano in un formato tecnico: gli utenti possono inserire le caratteristiche del dispositivo in linguaggio naturale — incluse informazioni fisiche non deducibili dal solo codice sorgente o dal firmware del dispositivo, come la fragilita' di un componente o una procedura di calibrazione — e il driver le trasforma in un file di riferimento strutturato che l'agente consulta prima di agire. E' l'equivalente, per l'hardware, del `description` dello schema di un tool MCP: la qualita' di questa descrizione determina quanto in sicurezza e con quanta autonomia un agente puo' operare il dispositivo.

## Varianti / approcci

MHS si posiziona in un campo dove esistevano gia' approcci parziali, ciascuno con un ambito piu' stretto.

| Approccio | Ambito | Limite rispetto a MHS |
|---|---|---|
| SDK proprietario del produttore | Un solo modello/famiglia di dispositivo | Nessuna interoperabilita' tra vendor; richiede integrazione ad-hoc per ogni nuovo device |
| Protocolli industriali (OPC-UA, Modbus) | Automazione industriale, PLC | Pensati per sistemi di controllo tradizionali, non per un agente AI che deve scoprire e ragionare sulle capacita' di un dispositivo sconosciuto |
| ROS (Robot Operating System) | Robotica, principalmente ricerca e prototipazione | Framework completo per orchestrare un robot, non uno standard leggero di interfacciamento pensato per essere consumato da un modello linguistico |
| MCP puro (senza MHS) | Tool e dati software | Non definisce semantica per hardware fisico: nessun concetto nativo di limiti di sicurezza, calibrazione, o descrizione fisica di un dispositivo |
| MHS | Hardware fisico programmabile, raggiungibile via MCP | Aggiunge la semantica fisica (limiti, calibrazione, descrizione in linguaggio naturale) mancante in MCP, restando compatibile con l'ecosistema MCP esistente |

La scelta architetturale di appoggiarsi a MCP come trasporto, invece di definire un protocollo di rete nuovo, e' coerente con il pattern gia' osservato nell'ecosistema agentico nel 2025-2026: piuttosto che frammentare ulteriormente lo strato di interoperabilita', i nuovi domini applicativi (pagamenti, dati finanziari, e ora hardware fisico) si innestano su MCP come strato di trasporto comune, aggiungendo sopra di esso la semantica specifica del dominio.

## Quando usarlo

MHS e' rilevante per organizzazioni che gestiscono parchi di strumenti fisici eterogenei e vogliono renderli operabili da agenti AI senza commissionare un'integrazione custom per ogni dispositivo: laboratori di ricerca biologica o chimica con liquid handler, robot da laboratorio, plate reader e microscopi di produttori diversi; strutture di manifattura avanzata con bracci robotici e strumenti di misura; contesti in cui il collo di bottiglia per automatizzare un workflow scientifico o produttivo e' storicamente il tempo di integrazione ingegneristica per-dispositivo, non la capacita' di ragionamento del modello che dovrebbe orchestrare il processo.

Non e' la scelta giusta per un singolo dispositivo isolato gestito da un solo team con un'integrazione gia' funzionante e stabile — l'overhead di adottare uno standard nuovo (ancora in research preview, non finalizzato) supera il beneficio quando non c'e' necessita' di scoprire o orchestrare piu' dispositivi eterogenei. Va inoltre trattato con la stessa cautela di sicurezza gia' nota per MCP quando applicata a un dominio con conseguenze fisiche irreversibili: fino a quando lo standard non e' maturo e pubblicamente auditabile, affidare ad agenti autonomi il controllo diretto di hardware costoso o pericoloso (senza supervisione umana su azioni ad alto rischio) resta un compromesso da valutare caso per caso.

## Esempi pratici

Genentech ha usato un primo deployment di MHS per automatizzare un protocollo di saggio proteico che richiedeva il coordinamento sequenziale di tre strumenti — un liquid handler per dosare i reagenti, un braccio robotico per spostare le piastre tra le stazioni, un plate reader per la lettura finale — un workflow che in precedenza richiedeva script di integrazione separati e sincronizzati manualmente per ciascuno dei tre dispositivi.

Un team della Carnegie Mellon University ha usato MHS per esperimenti di drug discovery, raggiungendo una curva dose-risposta completa in circa otto ore di lavoro effettivo, contro le settimane tipicamente necessarie per integrare manualmente la stessa sequenza di strumenti in un workflow automatizzato — la differenza attribuita al tempo di integrazione eliminato dal driver comune, non a un cambiamento nella velocita' fisica degli strumenti stessi.

## Letture

- Anthropic — Previewing the Model Hardware Standard. https://www.anthropic.com/news/model-hardware-standard-research-preview
- MarkTechPost — Anthropic Opens a Research Preview of the Model Hardware Standard (MHS). https://www.marktechpost.com/2026/08/29/anthropic-opens-a-research-preview-of-the-model-hardware-standard-mhs-a-shared-specification-for-ai-agents-to-safely-operate-physical-devices/
- Qz — Anthropic Model Hardware Standard connects AI to lab equipment. https://qz.com/anthropic-model-hardware-standard-ai-robots-lab-equipment-082826
- MLQ News — Anthropic previews a hardware standard for AI-controlled robots and lab equipment. https://mlq.ai/news/anthropic-previews-a-hardware-standard-for-ai-controlled-robots-and-lab-equipment/

## Aggiornamenti

### 2026-09-01

Prima menzione nel digest: Anthropic apre il research preview del Model Hardware Standard (27-28 agosto, coperta come missed coverage in questa run). [Digest 2026-09-01](../../digest/2026/09/01.md)
