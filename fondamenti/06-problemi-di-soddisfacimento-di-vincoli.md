---
titolo: Problemi di soddisfacimento di vincoli
capitolo: 6
parte: 2
volume: 1
pagine: "185-212"
concetti: [agent, world-models, chain-of-thought, inference]
created: 2026-07-06
last_updated: 2026-07-06
---

# Problemi di soddisfacimento di vincoli

Nei capitoli precedenti ogni stato del problema e' una scatola nera: la ricerca lo tratta come un punto atomico, senza guardarci dentro. Il capitolo 6 apre quella scatola. Uno stato diventa una rappresentazione fattorizzata: un insieme di variabili, ciascuna con un dominio di valori possibili, e un insieme di vincoli che dice quali combinazioni sono ammesse. Un problema formulato cosi' si chiama CSP, constraint satisfaction problem, e la soluzione e' un assegnamento completo di valori che non viola alcun vincolo.

La domanda di fondo del capitolo e': cosa guadagniamo quando smettiamo di trattare gli stati come atomi? La risposta e' duplice. Primo, molti problemi reali — colorare mappe, comporre orari, pianificare turni di fabbrica — si esprimono in modo naturale come vincoli su variabili. Secondo, e piu' importante, la struttura interna degli stati permette euristiche di uso generale, indipendenti dal dominio: un risolutore CSP puo' potare intere regioni dello spazio di ricerca appena scopre che un assegnamento parziale viola un vincolo, cosa che una ricerca su stati atomici non puo' fare.

Il capitolo costruisce l'intero arsenale: come si definisce formalmente un CSP, come l'inferenza propaga i vincoli riducendo i domini, come la ricerca con backtracking si combina con l'inferenza, come la ricerca locale attacca il problema da assegnamenti completi, e infine come la struttura del grafo dei vincoli determina quanto e' difficile il problema.

## Variabili, domini, vincoli: la grammatica dei CSP

Un CSP e' una tripla: variabili, domini, vincoli. Ogni vincolo specifica una relazione su una tupla di variabili, cioe' l'insieme delle combinazioni di valori che accetta. Un assegnamento che non viola nulla e' consistente; se copre tutte le variabili e' completo; una soluzione e' entrambe le cose.

L'esempio didattico del capitolo e' la colorazione della mappa dell'Australia: sette variabili (una per stato o territorio), dominio {rosso, verde, blu}, e un vincolo di disuguaglianza per ogni coppia di regioni confinanti. Il problema si visualizza come grafo dei vincoli, con le variabili come nodi e i vincoli binari come archi. La potenza del formalismo si vede subito: fissato SA = blu, le cinque regioni adiacenti perdono il blu dai loro domini e le combinazioni da esaminare crollano da 243 a 32.

Il secondo esempio e' industriale: la programmazione dei compiti nell'assemblaggio di un'auto. Qui le variabili sono i tempi di inizio dei compiti, e i vincoli sono aritmetici (un compito piu' la sua durata deve precedere il successivo) o disgiuntivi (due compiti che condividono uno strumento non possono sovrapporsi). Il formalismo si adatta poi a molte varianti: domini finiti o infiniti, discreti o continui (la programmazione lineare e' un CSP a dominio continuo), vincoli unari, binari, di ordine superiore, e vincoli globali come Tuttediverse, che impone valori tutti distinti a un gruppo arbitrario di variabili. Esistono anche vincoli di preferenza, che non proibiscono ma penalizzano: in quel caso si parla di problema di ottimizzazione di vincoli (COP).

## Propagazione: quando l'inferenza fa il lavoro della ricerca

L'idea distintiva dei CSP e' che si puo' ragionare sui vincoli prima ancora di cercare. La propagazione dei vincoli usa i vincoli per eliminare valori dai domini, il che a cascata puo' eliminare valori da altri domini. A volte la propagazione da sola risolve il problema; piu' spesso lo restringe abbastanza da rendere la ricerca molto piu' veloce.

Il concetto centrale e' la consistenza locale, in vari gradi di forza. La consistenza di nodo elimina i valori che violano i vincoli unari. La consistenza d'arco e' il livello successivo: una variabile e' arco-consistente rispetto a un'altra se per ogni suo valore esiste almeno un valore compatibile nell'altra. L'algoritmo classico e' AC-3: mantiene una coda di archi da controllare, e ogni volta che restringe un dominio rimette in coda gli archi dei vicini, perche' la riduzione puo' abilitare nuove riduzioni. Il costo nel caso peggiore e' O(cd^3) per c vincoli e domini di dimensione d. La consistenza di cammino sale di livello e ragiona su triple di variabili; la k-consistenza generalizza a insiemi di k variabili. Piu' il grado di consistenza e' forte, piu' inferenze si ottengono, ma il costo cresce esponenzialmente: in pratica si calcola quasi sempre la 2-consistenza, raramente oltre.

I vincoli globali meritano algoritmi dedicati. Per Tuttediverse basta un conteggio: se m variabili condividono complessivamente meno di m valori possibili, il vincolo e' insoddisfacibile — un controllo che scopre inconsistenze invisibili alla sola consistenza d'arco sui vincoli binari equivalenti. Per problemi su grandi intervalli numerici, come i posti sui voli di una compagnia aerea, si rappresentano i domini con i soli estremi e si propagano quelli.

Il Sudoku e' la palestra perfetta: 81 variabili, 27 vincoli Tuttediverse su righe, colonne e riquadri. La sola consistenza d'arco risolve gli schemi facili per intero, riducendo ogni dominio a un valore. Le strategie dei solutori umani, come le "naked triples", sono in realta' tecniche generali di propagazione travestite: nulla e' specifico del Sudoku, e questa e' la forza del formalismo.

## Backtracking piu' euristiche generali

Quando la propagazione non basta, serve la ricerca. Il backtracking per CSP e' una ricerca in profondita' su assegnamenti parziali: scegli una variabile non assegnata, prova un valore, ricorri; se nessun valore funziona, torna indietro. Un'osservazione chiave rende tutto trattabile: i CSP sono commutativi, l'ordine degli assegnamenti non conta, quindi a ogni nodo dell'albero basta considerare una sola variabile. Senza questa restrizione l'albero avrebbe n!·d^n foglie invece di d^n.

Il bello e' che le scelte dell'algoritmo si guidano con euristiche indipendenti dal dominio. Per la scelta della variabile, l'euristica MRV (minimum remaining values) preferisce quella con meno valori legali rimasti: e' una strategia fail-first, perche' se una variabile e' destinata a fallire conviene scoprirlo subito e potare l'albero. In caso di parita' aiuta l'euristica di grado, che sceglie la variabile coinvolta in piu' vincoli con variabili non ancora assegnate. Per la scelta del valore vale la logica opposta, fail-last: il valore meno vincolante, quello che toglie meno opzioni ai vicini, massimizza le probabilita' che il ramo corrente porti a una soluzione.

La ricerca si intreccia poi con l'inferenza. Il forward checking, dopo ogni assegnamento, cancella dai domini delle variabili adiacenti i valori incompatibili: se un dominio si svuota, si torna indietro subito. MAC (maintaining arc consistency) e' piu' aggressivo: dopo ogni assegnamento lancia AC-3 a partire dagli archi verso i vicini non assegnati, propagando ricorsivamente le riduzioni. MAC scopre inconsistenze che il forward checking non vede, perche' quest'ultimo non propaga oltre il primo livello.

## Tornare indietro con intelligenza

Il backtracking di base e' cronologico: al fallimento risale alla variabile assegnata piu' di recente. Ma quella variabile puo' non c'entrare nulla con il fallimento — cambiare colore alla Tasmania non risolve un conflitto nel continente. Il backjumping salta invece direttamente alla variabile piu' recente nell'insieme dei conflitti, cioe' tra quelle che hanno effettivamente ristretto i valori della variabile fallita. La versione piu' raffinata, il backjumping guidato dai conflitti, propaga gli insiemi dei conflitti all'indietro quando anche il salto fallisce, individuando il vero punto di decisione da rivedere. Curiosamente, il semplice backjumping e' ridondante se si usa gia' il forward checking: ogni ramo che il primo pota e' potato anche dal secondo.

L'idea complementare e' l'apprendimento dei vincoli: quando la ricerca incontra una contraddizione, estrae l'insieme minimo di assegnamenti responsabile del fallimento — un no-good — e lo registra, come nuovo vincolo o in una cache. Se la stessa combinazione si ripresenta altrove nell'albero, viene scartata senza rifare il lavoro. E' una delle tecniche chiave dei risolutori moderni, inclusi i SAT solver.

## Ricerca locale: aggiustare invece di costruire

L'approccio alternativo parte da un assegnamento completo, tipicamente pieno di violazioni, e lo ripara un passo alla volta. L'euristica min-conflicts sceglie a caso una variabile in conflitto e le assegna il valore che minimizza il numero di vincoli violati. Sul problema delle n regine il risultato e' sorprendente: il tempo di soluzione e' quasi indipendente dalla dimensione, e un milione di regine si sistema in una cinquantina di passi. Il metodo funziona anche su problemi reali difficili, come la pianificazione delle osservazioni del telescopio Hubble.

Il paesaggio di un CSP sotto min-conflicts e' pero' pieno di plateau: milioni di assegnamenti a un solo conflitto dalla soluzione. Le contromisure vengono dalla ricerca locale classica: mosse laterali, ricerca tabu' (una lista di stati visitati di recente in cui e' vietato tornare), simulated annealing, e il constraint weighting, che assegna pesi crescenti ai vincoli che restano violati, deformando la topografia e concentrando lo sforzo sui vincoli difficili. Un vantaggio pratico della ricerca locale e' l'uso online: se il maltempo invalida lo schedule dei voli, ripartire dallo schedule esistente produce una soluzione vicina all'originale con il minimo di cambiamenti, cosa che un backtracking da zero non garantisce.

## La forma del grafo decide la difficolta'

Risolvere un CSP e' NP-completo in generale, ma la struttura del grafo dei vincoli puo' cambiare radicalmente il quadro. Se il grafo ha componenti connesse separate, i sottoproblemi sono indipendenti e il costo diventa lineare nel numero di componenti: dividere 100 variabili booleane in quattro blocchi indipendenti trasforma un tempo cosmologico in meno di un secondo.

Il caso trattabile per eccellenza e' l'albero: un CSP il cui grafo e' un albero si risolve in tempo lineare. Basta ordinare le variabili topologicamente da una radice, imporre la consistenza d'arco orientato dalle foglie verso la radice, e poi assegnare i valori scendendo senza mai fare backtracking.

Per i grafi generici esistono due strategie di riduzione ad albero. Il condizionamento con insieme di taglio individua un sottoinsieme di variabili (il cycle cutset) la cui rimozione rende il grafo un albero: si enumera ogni assegnamento del cutset e si risolve l'albero residuo, con costo O(d^c · (n−c)d^2) per un cutset di dimensione c. La scomposizione ad albero raggruppa invece le variabili in nodi sovrapposti che formano un albero di sottoproblemi; il parametro critico e' la larghezza d'albero w del grafo, e il costo e' O(nd^(w+1)): i CSP con larghezza d'albero limitata sono risolvibili in tempo polinomiale, anche se trovare la scomposizione ottima e' a sua volta NP-difficile. Il trade-off pratico: il cutset richiede solo memoria lineare, la scomposizione ad albero e' spesso piu' veloce ma esponenziale in memoria.

Infine c'e' la struttura nei valori: se le soluzioni sono equivalenti a meno di permutazioni (i colori di una mappa sono intercambiabili), un vincolo di rottura della simmetria — per esempio un ordinamento alfabetico arbitrario tra tre variabili — riduce lo spazio di ricerca di un fattore fattoriale.

## Idee chiave

- Un CSP rappresenta lo stato come coppie variabile/valore e la soluzione come soddisfacimento di un insieme di vincoli; moltissimi problemi pratici si formulano cosi' in modo naturale.
- L'inferenza per propagazione (consistenza di nodo, d'arco con AC-3, di cammino, k-consistenza) elimina valori impossibili prima e durante la ricerca, a volte risolvendo il problema da sola.
- Il metodo di ricerca standard e' il backtracking, una ricerca in profondita' su assegnamenti parziali che sfrutta la commutativita' dei CSP per considerare una sola variabile per nodo.
- Le euristiche MRV, di grado e del valore meno vincolante sono generali, non specifiche del dominio: variabili fail-first, valori fail-last.
- Il backjumping guidato dai conflitti risale alla vera causa del fallimento, e l'apprendimento dei vincoli registra i no-good per non ripetere gli stessi errori.
- La ricerca locale con min-conflicts e' straordinariamente efficace: sul problema delle n regine il tempo e' quasi indipendente dalla dimensione.
- La struttura del grafo dei vincoli governa la complessita': alberi in tempo lineare, grafi generici trattabili via cutset conditioning o scomposizione ad albero se la larghezza d'albero e' piccola.
- Rompere le simmetrie di valore riduce lo spazio di ricerca di fattori fattoriali.

## Perche conta oggi

I CSP sono il primo punto del libro in cui l'AI smette di usare conoscenza specifica del dominio e inizia a sfruttare la struttura della rappresentazione: euristiche generali che funzionano su qualunque problema formulato nel linguaggio giusto. E' la stessa scommessa che regge un [llm](../kb/concetti/llm.md) moderno, che applica un meccanismo unico a qualunque compito espresso come testo. E le tecniche del capitolo non sono archeologia: i solver di vincoli e i SAT solver, diretti discendenti di backtracking con apprendimento dei no-good, girano oggi dentro compilatori, sistemi di scheduling e verifica formale, e sono esattamente il tipo di strumento esterno che un [agent](../kb/concetti/agent.md) basato su LLM richiama via [tool-use](../kb/concetti/tool-use.md) quando il problema richiede garanzie di correttezza che la generazione statistica non offre.

C'e' anche un parallelismo metodologico. La propagazione dei vincoli e' una forma di [inference](../kb/concetti/inference.md) che riduce lo spazio delle possibilita' prima di decidere, cosi' come la scomposizione di un problema in sottoproblemi piu' semplici — il cuore di cutset conditioning e tree decomposition — riecheggia nelle strategie di [chain-of-thought](../kb/concetti/chain-of-thought.md), dove il modello affronta un problema complesso un passaggio verificabile alla volta. Chi progetta sistemi ibridi LLM + solver oggi sta di fatto ricombinando i due paradigmi: il modello linguistico formula il problema in variabili e vincoli, il risolutore CSP lo chiude con la sistematicita' che il capitolo 6 ha codificato quarant'anni fa.

## Riferimenti

- Stuart J. Russell, Peter Norvig — *Intelligenza Artificiale: Un Approccio Moderno*, 4a edizione italiana, Pearson Italia, Vol. 1 (2021), Capitolo 6, pp. 185-212.
