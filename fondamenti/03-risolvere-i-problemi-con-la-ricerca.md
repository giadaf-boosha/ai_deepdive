---
titolo: Risolvere i problemi con la ricerca
capitolo: 3
parte: 2
volume: 1
pagine: "67-114"
concetti: [agent, world-models, chain-of-thought]
created: 2026-07-06
last_updated: 2026-07-06
---

# Risolvere i problemi con la ricerca

Cosa fa un agente quando la mossa giusta non e' ovvia? La risposta del capitolo 3 di Russell e Norvig e' semplice da enunciare e ricca di conseguenze: guarda avanti. L'agente immagina sequenze di azioni possibili, le simula dentro un modello del mondo e sceglie quella che lo porta a uno stato obiettivo. Questo processo computazionale si chiama ricerca, e l'agente che lo esegue e' un agente risolutore di problemi.

Il capitolo lavora in un mondo volutamente semplificato: ambienti a singolo agente, completamente osservabili, deterministici e noti. In queste condizioni la soluzione di un problema e' una sequenza fissa di azioni che l'agente puo' eseguire "a occhi chiusi", senza piu' consultare le percezioni: in teoria del controllo si parla di sistema ad anello aperto. Sembra un gioco accademico, ma e' il fondamento su cui poggiano navigatori stradali, pianificatori logistici, risolutori di puzzle e, come vedremo, parecchie idee che oggi ritroviamo negli agenti basati su LLM.

La domanda centrale del capitolo e' doppia. Primo: come si trasforma un obiettivo vago ("voglio arrivare a Bucarest") in un problema formale su cui un algoritmo puo' lavorare? Secondo: tra i tanti modi di esplorare le alternative, quali strategie trovano una soluzione, quali trovano la soluzione migliore, e a quale costo in tempo e memoria?

## Formulare il problema: stati, azioni e astrazione

Prima di cercare bisogna definire cosa si cerca. Un problema di ricerca e' descritto da cinque ingredienti: lo spazio degli stati (tutte le configurazioni possibili dell'ambiente), lo stato iniziale, le azioni disponibili in ogni stato, un modello di transizione che dice in quale stato si finisce applicando un'azione, e una funzione di costo che assegna un prezzo a ogni azione. Uno o piu' stati sono designati come obiettivo. Una sequenza di azioni forma un cammino; una soluzione e' un cammino dallo stato iniziale a un obiettivo, e la soluzione ottima e' quella di costo minimo.

L'esempio guida del libro e' un viaggio in Romania: le citta' sono gli stati, le strade sono le azioni, le distanze in miglia sono i costi. Ma la lezione piu' importante di questa sezione non riguarda la Romania: riguarda l'astrazione. Un vero viaggio in auto include il traffico, la radio, il meteo, i compagni di viaggio; il modello ignora tutto questo perche' irrilevante rispetto all'obiettivo. Scegliere il livello di astrazione giusto — abbastanza dettagliato da essere valido, abbastanza grossolano da essere trattabile — e' cio' che rende possibile risolvere problemi reali. Senza questa capacita' di semplificare, qualsiasi agente sarebbe schiacciato dalla complessita' del mondo.

Il capitolo passa in rassegna problemi standardizzati (mondi a griglia, rompicapo a 8 e 15 tasselli, sokoban, il curioso "problema del numero 4" di Knuth che genera uno spazio degli stati infinito) e problemi reali: itinerari stradali, pianificazione di voli, commesso viaggiatore, layout di circuiti VLSI, navigazione di robot, sequenze di montaggio automatico, fino alla progettazione di proteine. La struttura formale e' sempre la stessa; cambia solo cosa mettiamo dentro stati, azioni e costi.

## L'albero di ricerca e la frontiera

Come si esplora concretamente uno spazio degli stati? Sovrapponendogli un albero di ricerca. La radice e' lo stato iniziale; espandere un nodo significa generare un figlio per ogni azione applicabile. I nodi generati ma non ancora espansi formano la frontiera, che separa la regione gia' esplorata da quella ancora sconosciuta: ogni cammino dallo stato iniziale verso l'esterno deve attraversarla.

Lo schema generale e' la ricerca best-first: a ogni passo si estrae dalla frontiera il nodo che minimizza una funzione di valutazione f(n) e lo si espande. Cambiando f si ottengono quasi tutti gli algoritmi del capitolo, il che rende questo schema una specie di stampo universale. La frontiera si implementa con una coda: con priorita' per best-first, FIFO per la ricerca in ampiezza, LIFO per quella in profondita'.

C'e' un'insidia strutturale: i cammini ridondanti. Lo stesso stato puo' essere raggiunto per vie diverse, e i cicli possono rendere infinito l'albero anche quando lo spazio degli stati e' minuscolo. Il libro condensa la questione in un aforisma: un algoritmo che non tiene memoria degli stati gia' visitati e' destinato a esplorarli di nuovo. Le contromisure sono tre: memorizzare tutti gli stati gia' raggiunti (ricerca su grafo), ignorare il problema quando la struttura del dominio lo consente (ricerca ad albero), o controllare solo i cicli risalendo la catena dei nodi padre. E' un trade-off puro tra memoria e tempo.

Per confrontare gli algoritmi servono quattro criteri: completezza (trova sempre una soluzione se esiste?), ottimalita' rispetto al costo, complessita' temporale e complessita' spaziale, misurate in funzione del fattore di ramificazione b e della profondita' d della soluzione.

## Cercare alla cieca: le strategie non informate

Un algoritmo non informato non sa quanto uno stato sia vicino all'obiettivo: puo' solo esplorare in modo ordinato. La ricerca in ampiezza espande i nodi per livelli di profondita' crescente: e' completa e trova sempre la soluzione con il minor numero di azioni, quindi e' ottima quando tutte le azioni costano uguale. Il prezzo e' brutale: tempo e memoria crescono come O(b^d), e la memoria e' il collo di bottiglia prima ancora del tempo.

Quando i costi variano, la generalizzazione giusta e' la ricerca a costo uniforme — l'algoritmo di Dijkstra, per l'informatica teorica — che espande sempre il nodo con costo di cammino minimo e si propaga per onde di costo crescente anziche' di profondita' crescente. E' completa e ottima rispetto al costo.

La ricerca in profondita' segue invece un cammino fino in fondo prima di tornare indietro. Non e' ne' completa in generale ne' ottima, ma ha un pregio enorme: memoria O(bm), lineare anziche' esponenziale. Problemi che richiederebbero exabyte in ampiezza si affrontano con pochi kilobyte in profondita'. La variante con backtracking scende addirittura a O(m), modificando lo stato corrente anziche' copiarlo: e' la tecnica alla base di constraint satisfaction e programmazione logica.

Il compromesso piu' elegante e' la ricerca ad approfondimento iterativo: si eseguono ricerche in profondita' con limite 0, 1, 2... finche' non si trova la soluzione. Sembra uno spreco rigenerare ogni volta i livelli superiori, ma la matematica assolve: in un albero la maggior parte dei nodi vive all'ultimo livello, quindi la complessita' temporale resta O(b^d) mentre la memoria resta lineare. E' il metodo non informato consigliato quando lo spazio e' troppo grande per la memoria e la profondita' della soluzione non e' nota. Chiude la rassegna la ricerca bidirezionale, che parte simultaneamente dallo stato iniziale e dall'obiettivo sperando di incontrarsi a meta': b^(d/2) + b^(d/2) e' molto meno di b^d.

## L'euristica cambia il gioco: greedy e A*

Tutto cambia quando l'agente dispone di una funzione euristica h(n): una stima del costo del cammino piu' economico dal nodo n a un obiettivo. Nel problema rumeno, la distanza in linea d'aria verso Bucarest e' un'euristica naturale: non deriva dalla definizione del problema, ma da conoscenza del dominio.

Il modo piu' ingenuo di usarla e' la ricerca best-first greedy: espandi sempre il nodo che sembra piu' vicino all'obiettivo, cioe' f(n) = h(n). Spesso e' velocissima — nell'esempio rumeno trova un cammino senza mai deviare — ma la sua "golosita'" non da' garanzie: puo' restituire soluzioni peggiori di quelle trovate con piu' cautela.

L'algoritmo simbolo del capitolo e' la ricerca A*, che combina passato e futuro: f(n) = g(n) + h(n), dove g(n) e' il costo gia' speso per arrivare a n e h(n) la stima di quanto manca. Se l'euristica e' ammissibile — non sovrastima mai il costo residuo, cioe' e' sistematicamente ottimista — A* e' completa e ottima rispetto al costo. Una proprieta' un po' piu' forte, la consistenza (una forma di disuguaglianza triangolare), garantisce inoltre che il primo cammino con cui si raggiunge uno stato sia gia' quello ottimo. Con euristica consistente, A* e' anche ottimamente efficiente: nessun algoritmo che usa la stessa euristica puo' espandere meno nodi certamente necessari. La sua arma e' la potatura: interi sottoalberi vengono scartati senza nemmeno essere esaminati, un'idea che attraversa tutta l'IA.

Il rovescio della medaglia e' che, per molti problemi, anche A* espande un numero di nodi esponenziale. Se si accettano soluzioni "sufficientemente buone" (satisficing), si puo' gonfiare deliberatamente l'euristica: la ricerca A* pesata usa f(n) = g(n) + W x h(n) con W > 1, esplora molti meno stati e garantisce un costo entro un fattore W dall'ottimo. E' istruttivo notare che una sola formula unifica tutto: W = 0 da' la ricerca a costo uniforme, W = 1 da' A*, W = infinito da' la greedy.

Restano i problemi di memoria, per cui esistono varianti dedicate: la ricerca beam tiene solo i k nodi migliori della frontiera (veloce, ma incompleta e subottima); IDA* applica l'approfondimento iterativo al costo f; RBFS e SMA* usano la memoria disponibile in modo piu' furbo, ricordando i valori di backup dei sottoalberi dimenticati per poterli rigenerare solo se necessario. La morale e' sottile: la scarsita' di memoria puo' rendere un problema intrattabile dal punto di vista del tempo, e l'unica via d'uscita e' rinunciare all'ottimalita'.

## Da dove vengono le buone euristiche

Se la qualita' dell'euristica decide le prestazioni, come si inventano euristiche buone? Il capitolo misura la qualita' con il fattore di ramificazione effettivo: sul rompicapo a 8 tasselli, la distanza Manhattan (somma delle distanze di ogni tassello dalla sua casella finale) batte nettamente il semplice conteggio dei tasselli fuori posto, e un'euristica con valori piu' alti — purche' ammissibile — domina e non espande mai piu' nodi.

La ricetta piu' generale e' il problema rilassato: si tolgono vincoli alle azioni e si usa il costo esatto della soluzione del problema semplificato come stima per quello originale. Se i tasselli potessero volare ovunque, il costo esatto sarebbe "tasselli fuori posto"; se potessero scivolare anche su caselle occupate, sarebbe la distanza Manhattan. Il costo ottimo di un problema rilassato e' sempre un'euristica ammissibile e consistente per il problema vero, e il processo si puo' automatizzare partendo da una descrizione formale delle azioni.

Altre strade: i database di pattern memorizzano i costi esatti di sottoproblemi precalcolati (con le versioni disgiunte si sommano stime senza perdere l'ammissibilita', accelerando il rompicapo a 15 tasselli di un fattore 10.000); i punti di riferimento (landmark) precalcolano cammini ottimi verso pochi vertici scelti, ed e' cosi' che i servizi di mappe online rispondono in millisecondi su grafi con decine di milioni di nodi; infine si puo' imparare l'euristica dall'esperienza, addestrando un modello su coppie stato-costo tratte da soluzioni ottime di istanze passate, tipicamente a partire da caratteristiche (feature) dello stato. Qui il libro getta un ponte esplicito verso il machine learning: perfino il "cercare meglio" puo' essere appreso, ragionando in uno spazio degli stati di metalivello i cui stati sono gli alberi di ricerca stessi.

## Idee chiave

- Prima dell'algoritmo viene la formulazione: stato iniziale, azioni, modello di transizione, stati obiettivo e costi definiscono il problema, e la scelta del livello di astrazione decide se sara' trattabile.
- Una soluzione e' un cammino nello spazio degli stati; in ambienti deterministici, osservabili e noti e' una sequenza di azioni eseguibile senza guardare le percezioni.
- Quasi tutti gli algoritmi del capitolo sono istanze di best-first con una diversa funzione di valutazione f(n); la frontiera e la gestione degli stati gia' raggiunti sono la meccanica comune.
- Gli algoritmi si giudicano su quattro assi: completezza, ottimalita' rispetto al costo, tempo e memoria; nella ricerca in ampiezza il vero limite e' la memoria, non il tempo.
- Tra i metodi non informati, l'approfondimento iterativo combina il meglio dei due mondi: tempo paragonabile all'ampiezza, memoria lineare come la profondita'.
- A* con euristica ammissibile e' completa e ottima rispetto al costo; con euristica consistente e' anche ottimamente efficiente e il primo cammino verso ogni stato e' gia' quello migliore.
- Rinunciare all'ottimalita' e' spesso un buon affare: A* pesata, ricerca beam e le varianti a memoria limitata (IDA*, RBFS, SMA*) scambiano garanzie per velocita' o spazio.
- Le euristiche migliori nascono da problemi rilassati, database di pattern, landmark precalcolati o apprendimento dall'esperienza; un'euristica dominante riduce direttamente i nodi espansi.

## Perche conta oggi

La ricerca nello spazio degli stati sembra archeologia dell'IA, ma descrive esattamente il ciclo con cui lavora un [agent](../kb/concetti/agent.md) moderno costruito attorno a un [llm](../kb/concetti/llm.md): formulare l'obiettivo, generare azioni candidate, valutare dove portano, scegliere, eventualmente tornare sui propri passi. Tecniche come Tree of Thoughts o il sampling di piu' catene di ragionamento sono, in sostanza, ricerca best-first su uno spazio di stati testuali, dove il modello stesso fa da funzione euristica; il [chain-of-thought](../kb/concetti/chain-of-thought.md) lineare corrisponde a una ricerca in profondita' senza backtracking, con gli stessi rischi di incompletezza che il capitolo mette in fila. E il vincolo che domina il capitolo — la memoria esponenziale della frontiera — ha un parallelo diretto nel [context-window](../kb/concetti/context-window.md) limitato entro cui un agente deve tenere lo stato della propria esplorazione.

Anche la lezione sulla formulazione resta attuale: definire stati, azioni ammissibili e costi e' il lavoro che oggi si fa progettando il [tool-use](../kb/concetti/tool-use.md) di un agente e il suo modello dell'ambiente, cioe' i suoi [world-models](../kb/concetti/world-models.md) impliciti. Le idee di potatura, satisficing e ricerca bidirezionale riappaiono ogni volta che si bilancia qualita' della soluzione e budget di calcolo o di token. Il capitolo insegna il vocabolario con cui ragionare su questi trade-off, e mostra che erano gia' tutti sul tavolo decenni prima dei transformer.

## Riferimenti

- Stuart J. Russell, Peter Norvig — *Intelligenza Artificiale: Un Approccio Moderno*, 4a edizione italiana, Pearson Italia, Vol. 1 (2021), Capitolo 3, pp. 67-114.
