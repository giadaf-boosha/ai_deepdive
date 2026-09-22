---
name: System One Models
aliases: [System One model, decision model, modello di decisione, Jev, TypeSafe AI Jev, non-autoregressive decision model]
categoria: architettura
created: 2026-09-22
last_updated: 2026-09-22
---

# System One Models

## Cos'e

I "System One Models" sono una categoria di modelli proposta da TypeSafe AI a settembre 2026 con il lancio di Jev, il primo esempio pubblico della classe. Il nome richiama la distinzione psicologica di Daniel Kahneman tra "System 1" (pensiero rapido, automatico, intuitivo) e "System 2" (pensiero lento, deliberato, sequenziale): un [LLM](./llm.md) generalista che ragiona passo per passo — con o senza [chain of thought](./chain-of-thought.md) esplicito — si comporta come un System 2, mentre un System One Model e' pensato per rispondere a domande strutturate e ripetitive con la stessa immediatezza di un riflesso, senza deliberazione token-per-token.

Tecnicamente, un System One Model non e' un LLM generalista compresso o distillato per essere piu' veloce: e' un tipo di modello diverso, costruito per un compito diverso. Non genera testo libero. Prende in ingresso uno stato non strutturato — testo, ma anche stato di un programma, di un documento, di una conversazione — e restituisce in uscita decisioni tipizzate: un numero in virgola mobile associato a una categoria, la risposta a una domanda si/no, un punteggio di rating, un punteggio di confidenza calibrato. L'output non e' "generato" nel senso in cui lo e' l'output di un LLM autoregressivo: e' selezionato tra un insieme di risposte possibili definito in anticipo dallo schema del task, il che garantisce per costruzione che l'output sia conforme allo schema, invece di essere conforme "quasi sempre" come accade con un LLM generalista vincolato a un output strutturato tramite grammar constraint o JSON mode.

Il caso d'uso previsto non e' generare contenuto, ma prendere decisioni ad alto volume su uno stato condiviso, dove le risposte possibili sono note in anticipo: instradamento di richieste (routing), moderazione e rilevamento spam, assegnazione di priorita' e ranking, classificazione di ticket di supporto, valutazione di conformita' a una policy, scoring di lead commerciali. Sono compiti che oggi vengono spesso risolti con un LLM generalista usato come classificatore — un uso tecnicamente possibile ma economicamente e architetturalmente sproporzionato, perche' un LLM da centinaia di miliardi di parametri che genera token uno alla volta per produrre alla fine un singolo "si" o "no" sta spendendo capacita' di generazione libera per un compito che non ne richiede.

## Come funziona

### Non-autoregressivita' e parallel sampling

La differenza architetturale piu' rilevante rispetto a un LLM generalista e' che Jev non e' autoregressivo. Un LLM standard genera un token alla volta, condizionando ogni nuovo token sui token precedenti: la latenza cresce con la lunghezza dell'output, e generare N risposte a N domande diverse sullo stesso contesto richiede in linea di principio N passaggi in avanti separati (o un batching che comunque non elimina il costo per query). Jev inverte lo schema: ingerisce lo stato del programma o del documento una sola volta, poi valuta in parallelo tutte le domande poste su quello stato, e restituisce tutte le risposte in un unico passaggio, con una latenza dichiarata compresa tra 70 e 500 millisecondi indipendentemente dal numero di domande poste sullo stesso contesto.

Il meccanismo che rende possibile questa parallelizzazione e' un "parallel sampler": invece di campionare token da una distribuzione di probabilita' su un intero vocabolario per poi decodificarli in testo, il sistema enumera in anticipo l'insieme finito di risposte possibili per ciascuna domanda (definito dallo schema del task — le categorie di una classificazione, le opzioni di un si/no, i bucket di un punteggio) e assegna direttamente una probabilita' calibrata a ciascuna opzione. Questo e' concettualmente piu' vicino a un modello di classificazione probabilistica con un head specializzato per ogni tipo di domanda che a un modello generativo di linguaggio nel senso classico: la "generazione" e' sostituita da una selezione vincolata, e la conformita' allo schema di output e' garantita per costruzione (non puo' emettere una categoria che non esiste), invece di essere ottenuta a posteriori con un parser che scarta o ritenta le risposte malformate come accade tipicamente con lo structured output di un LLM generalista.

### Calibrazione della confidenza

Un elemento distintivo dichiarato per la classe System One e' che l'output non e' solo una decisione ma una decisione accompagnata da un punteggio di confidenza calibrato: il modello non dice solo "categoria A", ma "categoria A con probabilita' 0,82". La calibrazione — la proprieta' per cui, tra tutte le previsioni a cui il modello assegna una confidenza dell'80%, effettivamente circa l'80% risulta corretta — e' un requisito tecnico distinto dall'accuratezza pura: un modello puo' essere molto accurato ma mal calibrato (sempre troppo sicuro di se', o troppo cauto), il che lo rende inaffidabile come input per una decisione automatizzata a valle che usa la confidenza come soglia (es. "processa automaticamente solo le decisioni con confidenza sopra 0,9, il resto va a revisione umana"). Il valore pratico dichiarato di un System One Model rispetto a un LLM generalista usato come classificatore ad-hoc e' proprio questo: un output pensato dall'inizio per essere consumato da codice a valle, non da un lettore umano, con la confidenza come parte integrante del contratto di output.

### Pricing asimmetrico

Jev e' prezzato solo sull'input — $0,042 per milione di token — con l'output gratuito. Questo schema di pricing e' coerente con l'architettura: se l'output non e' testo generato token per token ma una selezione tra un numero finito di opzioni predefinite, il costo marginale di produrre la risposta e' vicino a zero rispetto al costo di elaborare il contesto in ingresso, e la struttura tariffaria riflette questa asimmetria invece di ricalcare lo schema input/output separatamente prezzato tipico dei LLM generalisti.

## Varianti / approcci

La categoria System One Models e', a settembre 2026, rappresentata pubblicamente da un solo prodotto (Jev), quindi non esistono ancora varianti concorrenti direttamente comparabili. E' utile pero' collocare l'approccio rispetto alle alternative gia' esistenti per lo stesso tipo di compito:

| Approccio | Come produce la decisione | Costo/latenza tipici | Limite principale |
|---|---|---|---|
| LLM generalista come classificatore (prompt + parsing) | Genera testo libero, poi un parser esterno estrae la categoria | Alto: genera token anche per un output minimo, spesso richiede retry su output malformato | Overkill computazionale; conformita' allo schema non garantita |
| LLM generalista con structured output / JSON mode | Vincola la generazione a una grammatica che forza uno schema JSON valido | Migliore del caso precedente ma ancora autoregressivo, un passaggio per query | Costo e latenza scalano con il volume di query, non pensato per batch di domande sullo stesso stato |
| Modello di classificazione classico (es. un classificatore BERT-style fine-tuned) | Head di classificazione dedicato, addestrato su un task specifico | Molto basso, ma un modello per ogni task | Non generalizza a task nuovi senza retraining; nessuna comprensione di linguaggio naturale libero in input |
| System One Model (Jev) | Parallel sampler non-autoregressivo su uno stato condiviso, schema di output tipizzato definito a runtime | Dichiarato molto basso (decine-centinaia di ms, prezzo solo-input) | Categoria nuova, benchmark solo vendor-side, non generalista: non produce testo libero |

L'asse di differenziazione piu' rilevante e' "generalita' del compito vs. efficienza per un compito vincolato". Un LLM generalista puo' in teoria fare tutto, incluso classificare, ma paga in costo e latenza la generalita' che non sta usando quando il compito e' in realta' una decisione ristretta. Un classificatore tradizionale e' efficiente ma rigido, va riaddestrato per ogni nuovo task. Un System One Model si propone come via di mezzo: comprende input in linguaggio naturale non strutturato come un LLM (non serve retraining per un nuovo schema di classi, basta definire lo schema a runtime), ma restituisce solo decisioni vincolate con l'efficienza di un classificatore dedicato.

## Quando usarlo / quando no

Ha senso considerare un System One Model quando ricorrono insieme tre condizioni: il volume di decisioni e' alto e ripetuto (migliaia o milioni di chiamate sullo stesso tipo di domanda), l'insieme delle risposte possibili e' noto e vincolato in anticipo (non serve testo libero in output), e la latenza o il costo per decisione di un LLM generalista sono un collo di bottiglia concreto nel sistema. Esempi tipici: moderazione di contenuti in tempo reale su un flusso ad alto volume, routing di richieste in ingresso verso il worker o il modello corretto, scoring e prioritizzazione continua di un flusso di ticket o lead, valutazione automatica di conformita' a regole esplicite.

Non ha senso quando il task richiede genuinamente generazione di testo libero (scrittura, sintesi, spiegazione, conversazione), quando le categorie di risposta non sono note in anticipo o cambiano di continuo in modi che richiedono comprensione contestuale profonda, o quando il volume di decisioni e' basso e il costo di un LLM generalista e' comunque trascurabile rispetto al valore della singola decisione (es. una valutazione una tantum ad alto stakes, dove vale la pena pagare il costo di un modello di ragionamento esplicito). Un errore di categoria da evitare e' considerare un System One Model come un sostituto economico di un LLM generalista per compiti di ragionamento multi-step: non lo e', perche' l'intera architettura rinuncia deliberatamente alla generazione sequenziale che il ragionamento step-by-step richiede.

### Riserve metodologiche

Le prestazioni dichiarate per Jev — fino a 193,6 volte piu' veloce e 444,6 volte piu' economico rispetto a LLM generalisti su task System One, circa 68% di accuratezza sul benchmark interno a quattro workflow di TypeSafe, vicino a modelli mid-tier come GPT-5.6 Terra — sono al momento benchmark del vendor stesso, non risultati indipendenti. TypeSafe AI ha dichiarato pubblicamente alcune limitazioni della propria valutazione: le misurazioni di latenza sono state condotte dai propri laptop sulla costa ovest degli Stati Uniti (non rappresentative di condizioni di rete generiche), l'azienda non puo' escludere che il pricing sia sovvenzionato nella fase di lancio, e i workflow usati per il benchmark, pur dichiarati assenti dal training set del modello, sono stati costruiti dallo stesso team che ha sviluppato il modello. Chi valuta l'adozione di questa categoria di modelli per un caso d'uso in produzione dovrebbe quindi trattare i numeri di velocita' e costo come limiti superiori ottimistici, non come garanzie, e condurre una propria valutazione comparativa sul proprio workload prima di sostituire una pipeline di classificazione esistente.

## Esempi pratici

Esempio 1: moderazione di contenuti su un flusso ad alto volume. Un servizio che riceve migliaia di messaggi al minuto e deve classificarli in tempo reale come spam/non-spam, con un punteggio di confidenza che decide se il messaggio va bloccato automaticamente, marcato per revisione umana o lasciato passare. Con un LLM generalista, ogni messaggio richiederebbe un passaggio autoregressivo completo con prompt di sistema, generazione e parsing dell'output; con un System One Model, lo stato (il messaggio, eventualmente insieme al contesto della conversazione) viene ingerito una volta e la decisione spam/non-spam con relativa confidenza viene restituita in un unico passaggio a bassa latenza, rendendo fattibile il filtro in tempo reale sul volume completo del traffico.

Esempio 2: routing di richieste verso worker specializzati in un sistema multi-agente (vedi [multi-agent orchestration](./multi-agent-orchestration.md)). Un orchestratore che riceve richieste eterogenee e deve instradarle rapidamente al worker o al modello giusto (un task di coding vs. un task di ricerca vs. un task di scrittura) puo' usare un System One Model come classificatore di routing a monte, riservando l'uso di un LLM generalista piu' costoso solo al worker effettivamente selezionato, invece di usare un LLM generalista anche per la decisione di instradamento stessa.

Esempio 3: scoring continuo di lead commerciali. Un sistema CRM che riceve informazioni su nuovi contatti e deve assegnare un punteggio di priorita' aggiornato ogni volta che arriva nuova informazione (una email, un'interazione, un dato firmografico) puo' usare un System One Model per ricalcolare il punteggio a ogni evento con latenza sub-secondo, invece di accumulare eventi e rivalutare periodicamente con un LLM generalista piu' lento e costoso.

## Letture

- Simon Willison, "Jev introduces a new shape of LLM — System One, aka Decision Models", 21 settembre 2026. https://simonwillison.net/2026/Sep/21/jev/
- TypeSafe AI, "Introducing System One Models & Jev", settembre 2026. https://typesafe.ai/blog/introducing-system-one-models-and-jev
- Tom's Hardware, "TypeSafe AI's Jev offers an alternative to LLMs that claims to be 193x faster and 445x cheaper", settembre 2026. https://www.tomshardware.com/tech-industry/artificial-intelligence/typesafe-ais-jev-offers-an-alternative-to-llms-that-claims-to-be-193x-faster-and-445x-cheaper-system-one-type-model-is-bespoke-for-probabilistic-decision-making
- MarkTechPost, "TypeSafe AI Releases Jev: A System One Model That Returns Typed, Calibrated Decisions Instead of Text", 19 settembre 2026. https://www.marktechpost.com/2026/09/19/typesafe-ai-releases-jev/
- DataCamp, "Jev: TypeSafe's System One Model That Never Hallucinates", settembre 2026. https://www.datacamp.com/blog/system-one-models-jev

## Aggiornamenti

### 2026-09-22

Prima voce di questa scheda, appena creata. TypeSafe AI lancia Jev il 15 settembre 2026, accompagnato da 40 milioni di dollari di funding; il modello — opera di Diogo Almeida, ex OpenAI e co-autore delle tecniche di training originarie di ChatGPT — diventa la storia AI piu' discussa su Hacker News il 21 settembre in seguito a un'analisi tecnica di Simon Willison, che ne battezza la sintesi "System One, aka Decision Models". [Digest 2026-09-22](../../digest/2026/09/22.md)
