---
titolo: Pianificazione automatica
capitolo: 11
parte: 3
volume: 1
pagine: "353-394"
concetti: [agent, world-models, chain-of-thought, tool-use]
created: 2026-07-06
last_updated: 2026-07-06
---

# Pianificazione automatica

Come fa un agente a costruire in modo efficiente una sequenza di azioni che lo porti da dove si trova a dove vuole arrivare? E' la domanda al centro di questo capitolo. La ricerca nello spazio degli stati e la deduzione logica, viste nei capitoli precedenti, funzionano ma soffrono di due debolezze condivise: richiedono euristiche costruite a mano per ogni nuovo dominio e rappresentano gli stati in modo esplicito, con una crescita esponenziale che le rende impraticabili su problemi realistici.

La risposta della comunita' di ricerca e' una rappresentazione fattorizzata: invece di trattare ogni stato come un blocco atomico, lo si descrive come combinazione di proprieta' elementari, e le azioni come regole generali che leggono e modificano quelle proprieta'. Questa scelta, apparentemente solo notazionale, cambia tutto: rende possibile derivare automaticamente euristiche indipendenti dal dominio e comprimere spazi di ricerca enormi.

Il capitolo conta perche' la pianificazione e' il punto di incontro tra le due anime storiche dell'AI, la ricerca e la logica, e perche' i temi che tocca — scomporre obiettivi complessi in sottopassi, agire con informazione incompleta, monitorare l'esecuzione e correggere il tiro — sono esattamente quelli che oggi riemergono nella progettazione di sistemi agentici basati su LLM.

## Descrivere il mondo a fattori: il linguaggio PDDL

La pianificazione classica assume un ambiente discreto, deterministico, statico e completamente osservabile. In questo quadro, il linguaggio PDDL (planning domain definition language) descrive uno stato come una congiunzione di fatti elementari ground (senza variabili), detti fluenti, con la convenzione che tutto cio' che non e' menzionato e' falso. Un problema di consegne, per esempio, si riduce a fatti come "il camion 1 e' a Melbourne" e "il pacco A e' sul camion 1".

Le azioni sono definite tramite schemi: un nome con variabili, una precondizione (cosa deve valere per poter agire) e un effetto (quali fluenti l'azione aggiunge e quali elimina). Un unico schema "Vola(aereo, da, a)" cattura tutte le possibili tratte di tutti gli aerei; e' questa compattezza che manca alle rappresentazioni atomiche. Il risultato di un'azione si calcola con una regola meccanica: si tolgono dallo stato i fluenti negati dall'effetto e si aggiungono quelli affermati.

Il libro illustra il formalismo con tre domini che sono diventati classici: il trasporto aereo di merci (caricare, scaricare, volare), il cambio di una ruota bucata e il mondo dei blocchi, dove un braccio robotico impila cubi su un tavolo. Sono esempi giocattolo, ma mostrano anche le insidie della modellazione: definire correttamente cosa significa "libero" per un blocco o per il tavolo richiede piu' attenzione di quanto sembri, e un modello impreciso produce piani sbagliati o spazi di ricerca inutilmente grandi.

## Cercare un piano: in avanti, all'indietro, o come formula logica

Dato un problema PDDL, la strada piu' diretta e' la ricerca in avanti (progressione): si parte dallo stato iniziale e si applicano azioni finche' non si raggiunge l'obiettivo. Il problema e' il fattore di ramificazione: in un dominio di trasporto con decine di aerei e centinaia di pacchi, ogni stato puo' avere migliaia di azioni applicabili, e anche istanze concettualmente banali diventano intrattabili senza una buona euristica.

L'alternativa e' la ricerca all'indietro (regressione): si parte dall'obiettivo e si applicano le azioni "al contrario", chiedendosi quali stati precedenti porterebbero a quello desiderato. Il vantaggio e' che si considerano solo le azioni rilevanti, cioe' quelle i cui effetti contribuiscono all'obiettivo, e il fattore di ramificazione crolla. Un esempio efficace: per l'obiettivo "possedere il libro con un certo ISBN", la ricerca in avanti dovrebbe enumerare miliardi di possibili acquisti, quella all'indietro unifica direttamente l'obiettivo con l'effetto dell'unica azione utile. Lo svantaggio e' che si lavora con insiemi di stati descritti da formule con variabili, e su questi e' piu' difficile definire euristiche accurate: per questo la maggior parte dei sistemi moderni preferisce la ricerca in avanti.

Una terza via traduce il problema in soddisfacibilita' booleana: si "proposizionalizzano" azioni e obiettivi su un orizzonte temporale fissato e si affida tutto a un risolutore SAT, come fa il sistema SATPlan. La formula risultante e' molto piu' lunga della descrizione PDDL originale, ma i risolutori moderni la gestiscono. Esistono poi approcci storici come Graphplan (basato su un grafo di pianificazione) e la pianificazione con ordinamento parziale, che rappresenta il piano come grafo di azioni con soli i vincoli di precedenza davvero necessari: oggi non e' piu' competitiva in velocita', ma resta usata dove gli umani devono leggere e validare i piani, per esempio nelle operazioni dei veicoli spaziali.

## Euristiche gratis: il dividendo della rappresentazione fattorizzata

Il vero guadagno della rappresentazione fattorizzata e' che le euristiche si possono derivare automaticamente, rilassando il problema in modi sistematici. Ignorare le precondizioni rende ogni azione sempre applicabile e trasforma la stima del costo in un problema di copertura di insiemi; ignorare le liste di eliminazioni (gli effetti negativi) produce un problema in cui nessuna azione disfa il lavoro di un'altra, quindi il progresso verso l'obiettivo e' monotono e una semplice hill climbing trova soluzioni senza vicoli ciechi. Rimuovere precondizioni selezionate da uno schema di azione genera meccanicamente euristiche note, come la distanza Manhattan per il gioco del quindici.

Un secondo asse di attacco e' l'astrazione di stato: si ignorano fluenti irrilevanti per il problema specifico, mappando molti stati concreti su uno astratto e riducendo lo spazio di ordini di grandezza. Un terzo e' la scomposizione: si divide l'obiettivo in sottoinsiemi, si risolve ciascuno indipendentemente e si combinano le stime — sommandole si ottiene un'euristica accurata e ammissibile quando i sotto-obiettivi sono davvero indipendenti. A questi si aggiungono potature indipendenti dal dominio, come la riduzione simmetrica (tra stati equivalenti a meno di una permutazione se ne esplora uno solo) e lo sfruttamento dei sotto-obiettivi serializzabili, che si possono raggiungere in un ordine tale da non dover mai disfare quelli gia' completati: e' il trucco che ha permesso al pianificatore Remote Agent della NASA di controllare in tempo reale la sonda Deep Space One. Il sistema FF (FastForward), vincitore di gare internazionali, combina ricerca in avanti, euristica che ignora le eliminazioni e una hill climbing potenziata.

## Pianificare per livelli: gerarchie di azioni

Pianificare una vacanza in termini di comandi motori richiederebbe miliardi di azioni. Gli umani ragionano per livelli di astrazione, e la pianificazione gerarchica (HTN, hierarchical task network) formalizza questa intuizione: accanto alle azioni primitive esistono azioni di alto livello (HLA), come "vai all'aeroporto", ciascuna con uno o piu' raffinamenti possibili in sequenze di azioni piu' fini (guidare e parcheggiare, oppure prendere un taxi). Il beneficio computazionale e' potenzialmente esponenziale: con una libreria di raffinamenti piccola e ben fatta, il costo della ricerca puo' passare da esponenziale a quasi lineare nella lunghezza della soluzione.

L'algoritmo di base sostituisce ripetutamente una HLA con uno dei suoi raffinamenti finche' il piano diventa tutto primitivo e raggiunge l'obiettivo. Ma raffinare fino alle azioni primitive per verificare un piano tradisce lo spirito dell'astrazione: vorremmo poter certificare un piano di alto livello senza scendere nei dettagli. Qui il libro introduce la semantica angelica: poiche' e' l'agente stesso (non un avversario) a scegliere quale implementazione eseguire, a ogni HLA si associa un insieme raggiungibile di stati, e un piano astratto funziona se tale insieme interseca gli stati obiettivo. Con descrizioni approssimate — ottimistiche e pessimistiche — si possono scartare subito i piani che certamente falliscono e adottare con fiducia quelli che certamente funzionano, rimandando il raffinamento solo ai casi ambigui. E' un modello fedele di come deliberiamo noi: decidiamo "due settimane alle Hawaii" e lasciamo i dettagli dei voli a dopo.

## Quando il mondo non collabora: incertezza, percezione, ripianificazione

La pianificazione classica assume di sapere tutto. Il capitolo la estende in tre direzioni, usando come filo conduttore un problema semplice: verniciare una sedia e un tavolo dello stesso colore senza conoscere i colori di partenza.

La pianificazione senza sensori (o conformante) cerca un piano che funzioni qualunque sia lo stato reale: l'agente ragiona su stati-credenza, insiemi di mondi possibili rappresentati come formule logiche. La mossa vincente e' aprire un barattolo e verniciare entrambi i mobili con quello, costringendo il mondo nell'obiettivo anche senza mai osservarlo. Il capitolo mostra che, se lo stato-credenza resta una congiunzione di letterali, l'aggiornamento e' quasi identico al caso osservabile e la rappresentazione resta compatta; gli effetti condizionali delle azioni, pero', possono farla esplodere, e allora servono approssimazioni conservative o il calcolo pigro via risolutore SAT.

La pianificazione condizionale genera piani con ramificazioni basate sulle percezioni: PDDL viene esteso con schemi di percezione che descrivono cosa l'agente osservera' e quando. Il piano diventa un albero di if-then-else: osserva i colori, e vernicia solo se serve.

La pianificazione online, infine, accetta che nessun piano sopravvive intatto al contatto con la realta': l'agente monitora l'esecuzione e ripianifica quando qualcosa va storto. Il monitoraggio puo' riguardare la singola azione (le precondizioni valgono ancora?), il piano residuo (porta ancora all'obiettivo? cosi' si rileva presto il fallimento e, in caso di aiuto esterno inatteso, anche la serendipita' di un obiettivo gia' raggiunto) o gli obiettivi stessi (ne e' comparso uno migliore?). La ripianificazione ripara il piano cercando il ricongiungimento piu' economico con quello originale. Il limite di fondo resta il modello: se un'azione fallisce sempre per una causa che l'agente non rappresenta (un barattolo vuoto), riprovare all'infinito non serve; la via d'uscita e' apprendere un modello migliore dai fallimenti.

## Tempo, scadenze e risorse limitate

La pianificazione classica dice cosa fare e in che ordine, non quanto dura ne' quando. Lo scheduling aggiunge durate, vincoli temporali e risorse: consumabili (i bulloni) o riusabili (un ispettore, occupato durante il compito ma poi di nuovo disponibile), rappresentate come quantita' aggregate anziche' come individui, il che riduce drasticamente la combinatoria. L'approccio tipico e' "prima pianifica, poi schedula".

Senza vincoli di risorse, minimizzare la durata totale (makespan) e' facile: il metodo del cammino critico calcola per ogni azione la finestra tra inizio piu' precoce e piu' tardivo; le azioni senza margine formano il cammino critico che determina la durata dell'intero piano. Ma appena le risorse impongono che due azioni non si sovrappongano, i vincoli diventano disgiuntivi e il problema NP-difficile: si ricorre a branch-and-bound, ricerca tabu' o a euristiche greedy come quella del margine minimo, che funzionano bene in pratica pur senza garanzie. Quando lo scheduling risulta troppo difficile, conviene integrare le due fasi e considerare durate e sovrapposizioni gia' durante la costruzione del piano.

## Idee chiave

- Rappresentare stati e azioni in forma fattorizzata (PDDL) invece che atomica e' la mossa che rende la pianificazione scalabile: consente schemi di azione compatti ed euristiche derivabili automaticamente.
- La ricerca di un piano puo' procedere in avanti dallo stato iniziale o all'indietro dall'obiettivo; la regressione riduce il fattore di ramificazione, ma la ricerca in avanti domina perche' su stati concreti le euristiche sono piu' accurate.
- Problemi rilassati (ignorare precondizioni o effetti negativi), astrazioni di stato e scomposizione in sotto-obiettivi generano euristiche efficaci senza conoscenza specifica del dominio.
- Un problema di pianificazione si puo' anche codificare come soddisfacibilita' booleana o come CSP e delegare a risolutori generici molto ottimizzati.
- La pianificazione gerarchica (HTN) incapsula conoscenza esperta in azioni di alto livello con raffinamenti; la semantica angelica permette di certificare piani astratti senza esplorarne le implementazioni, con risparmi potenzialmente esponenziali.
- In ambienti parzialmente osservabili o non deterministici si ragiona su stati-credenza: la pianificazione conformante trova piani robusti senza percezioni, quella condizionale ramifica sulle osservazioni.
- Un agente online monitora azione, piano e obiettivi durante l'esecuzione e ripianifica quando il mondo devia dal modello; i fallimenti ricorrenti segnalano che va appreso un modello migliore, non ritentato lo stesso piano.
- Tempo e risorse si gestiscono con lo scheduling: il cammino critico risolve i vincoli temporali puri in tempo polinomiale, ma i vincoli di risorse rendono il problema NP-difficile.

## Perche conta oggi

I sistemi agentici costruiti sugli LLM stanno riscoprendo, spesso senza citarlo, il vocabolario di questo capitolo. Un [agente](../kb/concetti/agent.md) che scompone un compito in sottotask sta facendo pianificazione gerarchica informale: le "azioni di alto livello" sono i passi di un ragionamento [chain-of-thought](../kb/concetti/chain-of-thought.md), e i raffinamenti sono le chiamate concrete a strumenti esterni via [tool use](../kb/concetti/tool-use.md). Il ciclo pianifica-esegui-monitora-ripianifica descritto nel Paragrafo 11.5 e' esattamente il loop operativo di un [agent harness](../kb/concetti/agent-harness.md) moderno: osservare il risultato di un'azione, confrontarlo con l'atteso, riparare il piano.

Le differenze sono altrettanto istruttive. La pianificazione classica offre garanzie formali (un piano trovato e' corretto rispetto al modello) al prezzo di un modello del mondo esplicito e fragile; un [LLM](../kb/concetti/llm.md) pianifica in modo flessibile su descrizioni in linguaggio naturale, ma senza garanzie e con [world models](../kb/concetti/world-models.md) impliciti e imperfetti. Le lezioni del capitolo restano attuali proprio per questo: gli stati-credenza ricordano che un agente deve rappresentare la propria incertezza, la semantica angelica che conviene validare i piani al livello di astrazione giusto, e il monitoraggio dell'esecuzione che nessun sistema autonomo e' affidabile se si fida ciecamente del proprio modello. Non a caso le architetture ibride che accoppiano LLM e pianificatori simbolici sono una delle direzioni piu' studiate per dare affidabilita' agli agenti.

## Riferimenti

- Stuart J. Russell, Peter Norvig — *Intelligenza Artificiale: Un Approccio Moderno*, 4a edizione italiana, Pearson Italia, Vol. 1 (2021), Capitolo 11, pp. 353-394.
