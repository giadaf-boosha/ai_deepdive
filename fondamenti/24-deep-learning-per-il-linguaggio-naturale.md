---
titolo: Deep learning per l'elaborazione del linguaggio naturale
capitolo: 24
parte: 6
volume: 2
pagine: "213-238"
concetti: [embedding, llm, fine-tuning, context-window, tokenization]
created: 2026-07-06
last_updated: 2026-07-06
---

# Deep learning per l'elaborazione del linguaggio naturale

Il capitolo 23 mostra come trattare il linguaggio con grammatiche, parsing e analisi semantica. Funziona, ma fino a un certo punto: i fenomeni linguistici reali sono troppo vari e sfumati per essere catturati da regole scritte a mano. Il capitolo 24 parte da una constatazione pratica: esiste una quantita' enorme di testo leggibile dalle macchine, e conviene chiedersi se un approccio guidato dai dati, basato sulle reti neurali profonde del capitolo 21, possa fare meglio dei sistemi costruiti manualmente.

La risposta del capitolo e' un percorso in cinque tappe: rappresentare le parole come vettori densi invece che come simboli atomici; usare reti ricorrenti per tenere traccia del contesto mentre si legge una sequenza; trasformare una sequenza in un'altra, come richiede la traduzione automatica; sostituire la ricorrenza con l'auto-attenzione dell'architettura transformer; e infine preaddestrare modelli su corpus giganteschi non etichettati per poi adattarli a compiti specifici.

E' il capitolo che descrive la genealogia diretta dei modelli linguistici odierni: word embedding, seq2seq, attention, transformer, preaddestramento. Chi vuole capire da dove arrivano GPT e i suoi successori trova qui i pezzi fondamentali, nell'ordine in cui la ricerca li ha messi insieme.

## Le parole diventano punti in uno spazio

Una rete neurale lavora con numeri, quindi la prima domanda e' come codificare una parola. Il vettore one-hot — un 1 nella posizione della parola e 0 altrove — e' la soluzione ingenua, ma tratta ogni parola come un'isola: "gatto" e "gattino" risultano distanti quanto "gatto" e "carburatore". L'alternativa segue l'intuizione del linguista John Firth: una parola si riconosce dalle parole che la accompagnano. Comprimendo le statistiche di co-occorrenza in un vettore denso di poche centinaia di dimensioni si ottiene un word embedding, una rappresentazione appresa dai dati in cui parole simili finiscono vicine nello spazio.

Gli embedding mostrano una proprieta' sorprendente: certe relazioni semantiche diventano differenze vettoriali. Il vettore che separa Athens da Greece assomiglia a quello che separa Oslo da Norway, e la stessa aritmetica funziona per capitali, valute, plurali, superlativi, tempi verbali. Non c'e' garanzia che un algoritmo di embedding catturi una particolare relazione, ma come rappresentazione di partenza per compiti a valle — classificazione, traduzione, risposta a domande — i vettori densi battono nettamente le codifiche discrete. Si possono usare vettori preaddestrati pronti (WORD2VEC, GloVe, FASTTEXT) oppure addestrarli insieme al modello del compito: un embedding appreso durante il POS tagging, per esempio, tendera' a enfatizzare le caratteristiche grammaticali delle parole.

## Ricordare il contesto: le reti ricorrenti

Una finestra fissa di poche parole basta per compiti locali come il POS tagging, ma il linguaggio e' pieno di dipendenze a lungo raggio: per risolvere un pronome puo' servire l'inizio della frase. Le reti neurali ricorrenti (RNN) elaborano il testo una parola alla volta mantenendo uno stato nascosto che viene passato al passo successivo. Questo risolve tre problemi delle reti feedforward: il numero di parametri non cresce con la lunghezza dell'input, i pesi sono condivisi tra le posizioni (niente asimmetria: cio' che il modello impara sulla decima parola vale anche per la ventesima), e in linea di principio qualsiasi informazione puo' viaggiare nello stato nascosto per un numero arbitrario di passi.

In pratica, pero', l'informazione si degrada passo dopo passo, come in un gioco del telefono: e' la versione temporale del problema della scomparsa del gradiente. Le LSTM lo mitigano con unita' a porte che decidono esplicitamente cosa ricordare e cosa dimenticare: possono trasportare intatta una caratteristica come il numero del soggetto lungo una frase piena di incisi, dove una RNN semplice si confonderebbe. Per la classificazione servono altri accorgimenti: una RNN bidirezionale combina una lettura da sinistra a destra con una da destra a sinistra, perche' spesso cio' che segue una parola e' decisivo quanto cio' che la precede; per giudizi sull'intera frase, come l'analisi del sentiment, si aggrega lo stato nascosto finale o la media di tutti gli stati (average pooling).

Un modello di linguaggio RNN, addestrato a predire la parola successiva, puo' anche generare testo: si campiona una parola dalla distribuzione di output e la si reimmette come input successivo. Gia' con modelli piccoli addestrati su Shakespeare il risultato e' localmente fluido, anche se privo di coerenza globale.

## Tradurre e' trasformare una sequenza in un'altra

La traduzione automatica non e' un tagging parola per parola: le lingue riordinano, fondono e spezzano le parole. Serve leggere l'intera frase di origine e generare la frase di destinazione un pezzo alla volta, condizionando ogni parola generata sia sull'origine sia su quanto gia' prodotto. Il modello sequenza-sequenza di base fa esattamente questo con due RNN: la prima codifica la frase di origine, e il suo stato nascosto finale inizializza la seconda, che genera la traduzione. L'approccio ha ridotto drasticamente gli errori rispetto ai metodi statistici precedenti, ma soffre di tre limiti: lo stato nascosto privilegia il contesto recente e sbiadisce quello lontano, l'intera frase deve stare in un vettore di dimensione fissa, e l'elaborazione strettamente sequenziale sfrutta male l'hardware parallelo.

Il meccanismo di attenzione attacca i primi due limiti. Invece di comprimere tutto nell'ultimo stato, il decoder calcola a ogni passo un punteggio di affinita' tra il proprio stato corrente e ciascuno stato dell'encoder, lo normalizza con una softmax e usa i pesi risultanti per costruire una media pesata degli stati di origine: un riassunto dinamico, ricalcolato parola per parola. L'attenzione non ha pesi propri e funziona con sequenze di lunghezza qualsiasi; il modello impara da solo dove guardare, e nelle traduzioni i pesi di attenzione ricalcano spesso gli allineamenti parola-parola che farebbe un traduttore umano — una rara isola di interpretabilita' nelle reti neurali.

Resta il problema di come generare la frase finale. La decodifica greedy sceglie a ogni passo la parola piu' probabile, ma una scelta localmente ottima puo' compromettere la frase intera senza possibilita' di correzione. La ricerca beam mantiene le k ipotesi migliori a ogni passo e le espande in parallelo, avvicinandosi alla sequenza globalmente piu' probabile; con modelli piu' accurati bastano beam piu' piccoli.

## Il transformer: attenzione senza ricorrenza

L'architettura transformer, introdotta dall'articolo "Attention is all you need", elimina del tutto la ricorrenza: il contesto, vicino e lontano, viene modellato solo con l'auto-attenzione, in cui ogni parola di una sequenza presta attenzione a tutte le altre parole della stessa sequenza. Per evitare che ogni parola presti attenzione soprattutto a se stessa, l'input viene proiettato in tre rappresentazioni distinte tramite matrici apprese: query (chi guarda), chiave (chi viene guardato) e valore (il contenuto trasmesso). I punteggi query-chiave, scalati per stabilita' numerica e normalizzati con una softmax, pesano la combinazione dei valori. Tutto si riduce a moltiplicazioni di matrici calcolabili in parallelo per tutte le posizioni: e' questo che rende i transformer addestrabili in modo efficiente su GPU e TPU, e quindi scalabili a dimensioni prima impraticabili.

Uno strato transformer combina auto-attenzione, una rete feedforward applicata in modo identico a ogni posizione e connessioni residuali contro la scomparsa del gradiente; i modelli reali ne impilano almeno sei. L'attenzione multi-headed suddivide la rappresentazione in piu' teste che imparano a guardare aspetti diversi della frase. Poiche' l'auto-attenzione ignora l'ordine delle parole, si aggiunge a ogni posizione un embedding posizionale. L'architettura completa distingue un codificatore, adatto a compiti di classificazione, e un decodificatore, quasi identico ma con attenzione mascherata alle sole parole precedenti, perche' il testo viene generato da sinistra a destra.

## Preaddestrare su tutto il web, raffinare sul compito

Etichettare testo richiede competenze linguistiche e costa; il testo grezzo, invece, abbonda: ogni giorno Internet cresce di miliardi di parole. Il preaddestramento sfrutta questa asimmetria: si addestra un modello generico su un corpus enorme non etichettato e lo si adatta poi al compito specifico con pochi dati — e' la declinazione linguistica dell'apprendimento per trasferimento. Il capitolo la sviluppa in tre gradini.

Il primo sono i word embedding preaddestrati non supervisionati: GloVe parte dai conteggi di co-occorrenza e arriva al vincolo per cui il prodotto scalare tra due vettori approssima il logaritmo della loro probabilita' di comparire insieme. L'addestramento e' economico e i vettori catturano conoscenza reale del dominio: un modello addestrato su abstract di scienza dei materiali risolveva analogie tra composti chimici e proprieta' fisiche, arrivando a indicare materiali termoelettrici anni prima che la letteratura li confermasse.

Il secondo gradino nasce da un limite: una parola polisemica come "salita" (pendenza, oppure participio di salire) non puo' essere rappresentata da un unico vettore. Le rappresentazioni contestuali producono un embedding diverso per ogni occorrenza, in funzione delle parole circostanti; si ottengono addestrando un modello di linguaggio a predire la parola successiva e riusando i suoi stati interni.

Il terzo gradino e' il modello di linguaggio con maschera (MLM): invece di predire solo in avanti, si nascondono parole a caso nella frase e si chiede a un modello bidirezionale — o a un transformer — di ricostruirle, usando il contesto in entrambe le direzioni. La frase e' l'etichetta di se stessa: niente annotazione manuale. Preaddestrato su un corpus ampio, un MLM produce rappresentazioni che si trasferiscono bene a traduzione, risposta a domande, riepilogo e giudizi grammaticali. E' la ricetta di BERT e derivati.

## Il punto della situazione, visto dal 2020

Il capitolo fotografa il campo al momento della svolta: nel 2018 un commentatore parlo' del "momento ImageNet" dell'elaborazione del linguaggio naturale, per analogia con la svolta della visione artificiale del 2012. Il motore e' proprio il trasferimento: da allora quasi ogni progetto NLP parte da un transformer preaddestrato da scaricare, non da un modello da addestrare da zero. GPT-2, con 1,5 miliardi di parametri addestrati su 40 GB di testo, genera completamenti sorprendentemente fluidi e affronta compiti diversi senza messa a punto dedicata — pur con fallimenti evidenti, come loop di ripetizioni. T5 riformula ogni compito come testo-a-testo, preaddestrandosi su 35 miliardi di parole del corpus C4. Il sistema ARISTO supera con il 91,6% un esame di scienze a scelta multipla, e il solo RoBERTa arriva all'88,2%. Sui benchmark GLUE e SuperGLUE i modelli superano il riferimento umano su alcuni compiti.

Gli autori chiudono con una domanda onesta: perche' i modelli puramente guidati dai dati battono i sistemi grammaticali del capitolo 23? La risposta pragmatica e' che sono piu' facili da sviluppare e rendono meglio sui benchmark; forse stanno apprendendo internamente rappresentazioni latenti simili a grammatiche e semantica, forse qualcosa di completamente diverso — non lo sappiamo. E i limiti restano: contesto di poche centinaia di parole, prestazioni ancora sotto quelle umane su molti compiti, e un'efficienza dei dati imbarazzante rispetto a quanto legge un essere umano in una vita intera.

## Idee chiave

- Rappresentare le parole come vettori continui appresi dai dati (word embedding) e' piu' robusto delle codifiche atomiche, e si puo' fare senza etichette.
- Le RNN mantengono il contesto in uno stato nascosto con un numero di parametri indipendente dalla lunghezza dell'input; le LSTM proteggono l'informazione a lungo raggio con unita' a porte.
- Il modello sequenza-sequenza — encoder piu' decoder — copre la traduzione automatica e in generale i problemi di generazione condizionata di testo.
- L'attenzione sostituisce il collo di bottiglia del vettore di stato fisso con un riassunto dinamico dell'origine, ricalcolato a ogni parola generata, ed e' spesso interpretabile.
- Il transformer usa solo auto-attenzione (query, chiave, valore) piu' embedding posizionali: modella contesto vicino e lontano e sfrutta al massimo il parallelismo dell'hardware.
- La generazione richiede una strategia di decodifica: la ricerca beam batte la scelta greedy perche' ottimizza la probabilita' dell'intera sequenza, non della singola parola.
- Il preaddestramento su corpus non etichettati, seguito da una messa a punto sul dominio di destinazione, permette di costruire modelli competitivi con pochi dati specifici: i modelli mascherati tipo BERT sono l'esempio canonico.
- I modelli guidati dai dati battono i sistemi a regole sui benchmark, ma non sappiamo se apprendano davvero strutture linguistiche o qualcos'altro.

## Perche conta oggi

Questo capitolo descrive, con qualche anno di anticipo, esattamente la pila su cui poggiano gli [LLM](../kb/concetti/llm.md) attuali: [embedding](../kb/concetti/embedding.md) come rappresentazione di base, transformer come architettura, preaddestramento su scala web come strategia. Cio' che il libro chiama messa a punto per il dominio di destinazione e' oggi il [fine-tuning](../kb/concetti/fine-tuning.md), arricchito da tecniche come RLHF che il capitolo non poteva anticipare. Anche i limiti segnalati sono profetici: il vincolo delle poche centinaia di parole di contesto e' diventato la corsa alla [context window](../kb/concetti/context-window.md), passata da centinaia di token a milioni, e la domanda su cosa succederebbe aggiungendo immagini e video ai dati di addestramento ha trovato risposta nei modelli multimodali.

Rileggere il capitolo aiuta anche a non dare per scontate le scelte di design: la [tokenization](../kb/concetti/tokenization.md) moderna discende dal dilemma tra modelli a livello di parole e di caratteri discusso qui; la tensione tra decodifica greedy e ricerca beam e' ancora il compromesso che regola temperatura e campionamento nella [inference](../kb/concetti/inference.md) di ogni API. E l'ammissione finale degli autori — non sappiamo se questi modelli apprendano grammatiche latenti o qualcosa di del tutto diverso — resta la domanda aperta al centro dell'interpretabilita' dei modelli attuali.

## Riferimenti

- Stuart J. Russell, Peter Norvig — *Intelligenza Artificiale: Un Approccio Moderno*, 4a edizione italiana, Pearson Italia, Vol. 2 (2022), Capitolo 24, pp. 213-238.
