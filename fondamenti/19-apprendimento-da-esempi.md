---
titolo: Apprendimento da esempi
capitolo: 19
parte: 5
volume: 2
pagine: "7-74"
concetti: [evaluation-benchmark, fine-tuning, embedding, vector-database, llm]
created: 2026-07-06
last_updated: 2026-07-06
---
# Apprendimento da esempi

Fino a questo punto del libro gli agenti ricevono la loro conoscenza dal progettista: regole, modelli del mondo, funzioni di utilita'. Il capitolo 19 ribalta la prospettiva e chiede: come puo' un agente migliorare da solo, osservando i dati? Quando l'agente e' un computer si parla di machine learning: il sistema osserva esempi e costruisce un modello che gli fa da teoria del mondo e, insieme, da modulo software riutilizzabile su problemi nuovi.

La motivazione e' pragmatica. I progettisti non possono anticipare tutte le situazioni che il sistema incontrera', e per molti compiti — riconoscere un volto, per esempio — nessun essere umano sa scrivere esplicitamente il programma giusto, perche' la competenza e' subconscia. L'apprendimento automatico e' ormai parte integrante dell'ingegneria del software: quasi ogni componente di un agente puo' essere appreso dai dati anziche' programmato a mano.

Il cuore del capitolo e' l'apprendimento supervisionato: partire da coppie input-output generate da una funzione ignota e trovare un'ipotesi che la approssimi bene anche su input mai visti. Attorno a questa idea si sviluppano le classi di modelli classiche — alberi di decisione, modelli lineari, metodi non parametrici, ensemble — e la teoria che spiega quando e perche' generalizzano.

## Indurre funzioni dai dati: ipotesi, bias e varianza

Il problema formale e' questo: dato un insieme di addestramento di N coppie (x, y) prodotte da una funzione ignota f, cercare una funzione h — l'ipotesi — che approssimi f. L'ipotesi vive in uno spazio delle ipotesi scelto dal progettista: rette, polinomi, alberi, reti. La misura che conta non e' l'aderenza ai dati di addestramento ma la capacita' di generalizzare, cioe' di predire correttamente su un insieme di test mai visto prima.

Due forze opposte governano la scelta dello spazio delle ipotesi. La distorsione (bias) e' la tendenza sistematica a deviare dal valore vero perche' lo spazio e' troppo ristretto: una retta non puo' catturare un andamento sinusoidale, e si parla di sottoadattamento. La varianza e' la sensibilita' dell'ipotesi alle fluttuazioni del campione: un polinomio di grado 12 passa perfettamente per 13 punti, ma cambia drasticamente se i punti cambiano di poco — e' il sovradattamento. Il compromesso distorsione-varianza e' il filo conduttore di tutto il capitolo, e il rasoio di Occam ne e' la versione filosofica: tra ipotesi compatibili con i dati, preferire la piu' semplice. Con una precisazione moderna importante: il numero di parametri da solo non misura la semplicita', visto che reti con miliardi di parametri spesso generalizzano bene.

C'e' anche un compromesso computazionale: uno spazio delle ipotesi molto espressivo (tutti i programmi possibili) rende intrattabile trovare una buona ipotesi al suo interno. Per questo la ricerca si e' concentrata su rappresentazioni semplici o, come nel deep learning, su rappresentazioni complesse il cui calcolo resta pero' limitato e prevedibile.

## Alberi di decisione: imparare regole leggibili

L'albero di decisione e' la prima classe di modelli trattata in dettaglio, sull'esempio ricorrente del capitolo: decidere se aspettare un tavolo al ristorante dati dieci attributi (affollamento, attesa stimata, fame, tipo di cucina e cosi' via). Un albero esegue una sequenza di test sugli attributi e arriva a una foglia che contiene la decisione. Ogni albero booleano equivale a una formula in forma normale disgiuntiva: e' logica proposizionale appresa dai dati.

L'algoritmo di apprendimento e' greedy e ricorsivo: a ogni nodo sceglie l'attributo "piu' importante" e suddivide gli esempi, ripetendo sui sottoinsiemi. L'importanza si misura con il guadagno informativo, cioe' la riduzione attesa di entropia — il concetto di Shannon che quantifica l'incertezza di una variabile casuale. Un attributo che separa nettamente esempi positivi e negativi ha guadagno alto e finisce vicino alla radice; uno che li mescola ha guadagno quasi nullo e viene ignorato. Il risultato notevole e' che dodici esempi bastano a produrre un albero piu' semplice di quello mentale della persona che li ha generati, e con pattern inattesi ma corretti.

Anche gli alberi sovradattano: crescendo, catturano rumore. Il rimedio e' la potatura: si genera l'albero completo e poi si eliminano i test che un test statistico di significativita' giudica irrilevanti (potatura chi-quadro). Il capitolo mostra anche come estendere gli alberi a dati mancanti, attributi continui (test su punti di suddivisione) e output numerici (alberi di regressione, famiglia CART). Il pregio degli alberi e' la comprensibilita'; il limite e' l'instabilita': un solo esempio in piu' puo' cambiare la radice e quindi l'intero albero.

## Valutare e selezionare: dalla convalida incrociata alla teoria PAC

Come si sceglie tra modelli candidati senza barare? La regola d'oro e' tenere davvero separato l'insieme di test: si addestra sull'insieme di addestramento, si confrontano modelli e iperparametri su un insieme di validazione e si valuta il modello finale, una sola volta, sul test set. Quando i dati scarseggiano, la convalida incrociata k-volte fa servire ogni esempio sia all'addestramento sia alla validazione, in turni distinti.

Il tasso di errore non basta: non tutti gli errori pesano uguale. Classificare come spam la mail della mamma e' peggio che lasciar passare uno spam. La funzione di perdita generalizza il conteggio degli errori assegnando un costo a ogni tipo di sbaglio; la perdita di generalizzazione e' il valore atteso sulla distribuzione vera degli esempi, e in pratica si stima con la perdita empirica sul campione. Un'alternativa alla selezione via validazione e' la regolarizzazione: minimizzare perdita empirica piu' un termine di complessita' pesato da un iperparametro, penalizzando esplicitamente le ipotesi complicate. La messa a punto degli iperparametri stessa diventa un problema di ricerca: a mano, su griglia, casuale, oppure con ottimizzazione bayesiana o addestramento basato sulla popolazione.

La teoria dell'apprendimento computazionale da' fondamento a tutto questo. L'idea PAC (probably approximately correct) e' che un'ipotesi seriamente sbagliata viene smascherata con alta probabilita' da pochi esempi, perche' prima o poi predice male. Da qui si ricava un limite sul numero di esempi necessari, che cresce con il logaritmo della dimensione dello spazio delle ipotesi: spazi ristretti come le liste di decisione con test corti sono apprendibili con un numero di esempi polinomiale, mentre lo spazio di tutte le funzioni booleane richiederebbe di vedere praticamente tutti gli input possibili.

## Modelli lineari: regressione, percettrone, regressione logistica

La classe delle funzioni lineari e' usata da secoli e resta il punto di partenza. Nella regressione lineare univariata si cercano i due pesi della retta che minimizzano la perdita quadratica; la soluzione esiste in forma chiusa. Il caso multivariato si risolve con l'equazione normale, oppure — ed e' il metodo generale — con la discesa del gradiente: si parte da pesi qualsiasi e ci si sposta iterativamente nella direzione che riduce la perdita, con passo dato dal tasso di apprendimento. La variante stocastica (SGD) aggiorna i pesi su minibatch di esempi anziche' sull'intero data set: e' molto piu' veloce e, con un tasso di apprendimento decrescente, converge. E' lo stesso motore che oggi addestra le reti neurali. La regolarizzazione dei pesi merita una nota: quella L1 tende a produrre modelli sparsi, azzerando i pesi degli attributi irrilevanti, mentre la L2 no.

Per la classificazione, una funzione lineare passata attraverso una soglia rigida definisce un confine di decisione: e' il percettrone, con la sua regola di aggiornamento dei pesi che converge se i dati sono linearmente separabili ma oscilla senza fine altrimenti. Sostituendo la soglia rigida con la funzione logistica — la sigmoide — si ottiene la regressione logistica: l'output diventa una probabilita' di appartenenza alla classe, il modello e' differenziabile ovunque e la discesa del gradiente si comporta in modo prevedibile anche su dati rumorosi. Non a caso e' una delle tecniche di classificazione piu' usate in medicina, marketing e credito.

## Memoria, distanze e kernel: i modelli non parametrici

Un modello parametrico riassume i dati in un numero fisso di parametri e poi li dimentica. Un modello non parametrico tiene i dati con se': con milioni di esempi conviene lasciar parlare i dati anziche' costringerli in pochi numeri. Il metodo simbolo e' k-nearest-neighbors: per classificare un nuovo punto si guardano i k esempi piu' vicini e si prende il voto di maggioranza (o la media, per la regressione). Il k regola il compromesso: k = 1 sovradatta, k grande sottoadatta, e la convalida incrociata sceglie il valore.

"Piu' vicino" richiede una metrica di distanza (Minkowski, euclidea, Manhattan) e una normalizzazione delle dimensioni. E qui compare la maledizione della dimensionalita': in spazi ad alta dimensione i vicini piu' prossimi non sono affatto vicini, e quasi tutti i punti diventano outlier. Per rendere veloce la ricerca dei vicini su grandi data set servono strutture dedicate: alberi k-d per poche dimensioni, hashing sensibile alla localita' (LSH) per molte — proiezioni casuali multiple che con alta probabilita' mettono punti vicini nello stesso bucket, con velocizzazioni di migliaia di volte rispetto alla ricerca esaustiva.

Le macchine a vettori di supporto (SVM) chiudono la sezione: cercano il separatore con massimo margine, cioe' il confine piu' lontano possibile dagli esempi, il che favorisce la generalizzazione. Il separatore dipende solo da pochi esempi critici, i vettori di supporto. Il trucco del kernel permette poi di trovare separatori lineari in spazi di caratteristiche ad altissima dimensione senza mai calcolarli esplicitamente: basta sostituire il prodotto scalare con una funzione kernel. Dati non separabili nello spazio originale diventano separabili nello spazio trasformato, e il confine, riportato indietro, puo' essere quanto di piu' non lineare.

## Piu' modelli sono meglio di uno: l'ensemble learning

L'ensemble learning combina le predizioni di piu' ipotesi base, di solito con un voto. I benefici sono due: piu' espressivita' (tre classificatori lineari votanti delimitano una regione triangolare che nessuna retta singola rappresenta) e meno varianza (se i classificatori sbagliano in modo almeno parzialmente scorrelato, la maggioranza sbaglia meno di ciascuno).

Il bagging addestra K modelli su campioni con reinserimento dello stesso data set e ne media le predizioni; funziona bene proprio con modelli instabili come gli alberi. Le foreste casuali aggiungono casualita' nella scelta degli attributi a ogni suddivisione, decorrelando gli alberi: sono robuste al sovradattamento anche senza potatura e sono state per anni il metodo vincente nelle competizioni di data science. Lo stacking impila un modello ensemble sopra modelli base di classi diverse, addestrandolo sulle loro predizioni. Il boosting procede in sequenza: ogni nuova ipotesi si concentra sugli esempi che le precedenti hanno sbagliato, aumentandone il peso; AdaBoost puo' trasformare un apprendimento appena migliore del caso in un classificatore perfetto sui dati di addestramento, e — sorprendentemente — le prestazioni sul test continuano a migliorare anche dopo l'interpolazione. Il boosting del gradiente, implementato in pacchetti come XGBoost, applica l'idea seguendo il gradiente della perdita ed e' oggi lo standard per i dati tabellari. Infine, l'apprendimento online abbandona l'assunzione che i dati siano i.i.d.: algoritmi come la maggioranza pesata randomizzata aggregano pareri di esperti e garantiscono un rimpianto limitato rispetto al migliore di essi, anche contro sequenze avversarie.

## Costruire sistemi che funzionano davvero

L'ultima parte del capitolo passa dalla teoria alla pratica di progetto. Prima viene la formulazione del problema: quale compito, quale funzione di perdita, quale tipo di apprendimento (supervisionato, per rinforzo, semi-supervisionato quando le etichette sono poche, debolmente supervisionato quando sono rumorose). Poi i dati, che sono la parte dominante del lavoro: raccolta e provenienza, privacy, data augmentation quando scarseggiano, classi squilibrate da ricampionare, outlier da trattare, feature engineering guidato dalla conoscenza del dominio — per Domingos e' il fattore che piu' distingue i progetti riusciti — e analisi esplorativa con visualizzazioni come t-SNE.

Segue la selezione del modello con strumenti come curva ROC e matrice di confusione per gestire il compromesso tra falsi positivi e falsi negativi. La fiducia nel sistema richiede pratiche da ingegneria del software (versioning, test, revisione, monitoraggio, accountability) piu' due proprieta' specifiche: interpretabilita' (capire il modello ispezionandolo, come per un albero) e spiegabilita' (un processo separato, come LIME, che spiega le singole predizioni anche di un modello scatola nera). Infine la manutenzione: il mondo non e' stazionario, gli utenti e gli avversari cambiano comportamento, e il modello va monitorato e riaddestrato con un processo il piu' possibile automatizzato.

## Idee chiave

- L'apprendimento supervisionato consiste nel trovare, in uno spazio di ipotesi scelto a priori, una funzione che concordi con gli esempi e generalizzi a dati futuri: l'equilibrio tra aderenza ai dati e semplicita' dell'ipotesi e' il problema centrale.
- Gli alberi di decisione rappresentano qualsiasi funzione booleana e si apprendono con un'euristica greedy basata sul guadagno informativo; sono leggibili ma instabili.
- La qualita' di un modello si misura su dati mai visti: insiemi di test separati, convalida incrociata e curve di apprendimento sono gli strumenti standard, e la funzione di perdita specifica quanto costa ogni tipo di errore.
- La teoria dell'apprendimento computazionale (PAC) lega il numero di esempi necessari alla complessita' dello spazio delle ipotesi: piu' lo spazio e' espressivo, piu' dati servono e piu' difficile e' la ricerca.
- I modelli lineari si addestrano in forma chiusa o con la discesa del gradiente; la versione stocastica su minibatch e' il metodo di ottimizzazione generale, applicabile ben oltre la regressione. La regressione logistica sostituisce la soglia rigida del percettrone con una sigmoide e funziona anche su dati non separabili.
- I modelli non parametrici (nearest-neighbors, regressione pesata localmente) usano tutti i dati per ogni predizione; le SVM massimizzano il margine e con il trucco del kernel trovano separatori lineari in spazi impliciti ad alta dimensione.
- I metodi ensemble — bagging, foreste casuali, stacking, boosting — combinano modelli per ridurre distorsione e varianza e spesso battono ogni modello singolo; l'apprendimento online gestisce dati la cui distribuzione cambia nel tempo.
- Un buon sistema di machine learning non e' solo un algoritmo: richiede formulazione del problema, cura dei dati, valutazione onesta, interpretabilita' e manutenzione continua in esercizio.

## Perche conta oggi

Questo capitolo e' la grammatica di base con cui leggere gli [LLM](../kb/concetti/llm.md) moderni. Il compromesso distorsione-varianza, la separazione tra addestramento, validazione e test, la discesa stocastica del gradiente su minibatch, la regolarizzazione: sono esattamente i concetti che governano il pre-training e il [fine-tuning](../kb/concetti/fine-tuning.md) dei grandi modelli, con la differenza che oggi la scala ha rimescolato alcune intuizioni (il capitolo stesso nota che modelli con miliardi di parametri possono generalizzare bene dopo l'interpolazione, come gia' si osservava con il boosting). La disciplina della valutazione su dati tenuti da parte e' l'antenata diretta degli [evaluation benchmark](../kb/concetti/evaluation-benchmark.md) con cui si confrontano i modelli, incluso il problema — gia' descritto da Russell e Norvig — del sovradattamento agli insiemi di validazione riusati troppe volte.

Anche i metodi apparentemente datati hanno eredi diretti. La ricerca dei vicini piu' prossimi con hashing sensibile alla localita' e' il cuore dei [vector database](../kb/concetti/vector-database.md) che alimentano le pipeline [RAG](../kb/concetti/rag.md), dove i punti sono [embedding](../kb/concetti/embedding.md) di testi e la maledizione della dimensionalita' e' un vincolo di progetto quotidiano. E la sezione sullo sviluppo di sistemi — provenienza dei dati, monitoraggio, non stazionarieta', spiegabilita' — descrive gia' nel 2021 quello che oggi chiamiamo MLOps e che qualsiasi team che mette in produzione modelli, generativi o meno, deve presidiare.

## Riferimenti

- Stuart J. Russell, Peter Norvig — *Intelligenza Artificiale: Un Approccio Moderno*, 4a edizione italiana, Pearson Italia, Vol. 2 (2022), Capitolo 19, pp. 7-74.
