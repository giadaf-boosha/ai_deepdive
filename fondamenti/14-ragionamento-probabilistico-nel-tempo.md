---
titolo: Ragionamento probabilistico nel tempo
capitolo: 14
parte: 4
volume: 1
pagine: "471-510"
concetti: [agent, world-models, inference]
created: 2026-07-06
last_updated: 2026-07-06
---

# Ragionamento probabilistico nel tempo

I capitoli precedenti trattano l'incertezza in mondi congelati: le variabili hanno un valore fisso e il problema e' solo scoprirlo. Molti problemi reali non funzionano cosi'. Il livello di glucosio di un paziente diabetico cambia di ora in ora, la posizione di un robot cambia a ogni passo, il significato di un segnale audio si costruisce nel tempo. Il capitolo 14 affronta la domanda centrale: come mantiene un agente una credenza probabilistica su uno stato del mondo che evolve, osservandolo solo attraverso sensori parziali e rumorosi?

La risposta combina due ingredienti gia' noti — lo stato-credenza e le reti bayesiane — con una struttura temporale: il mondo viene affettato in istanti discreti (time slice), e per ogni istante si definiscono variabili di stato non osservabili e variabili di evidenza osservabili. Il resto del capitolo costruisce, a partire da questa impostazione, una teoria dell'inferenza temporale sorprendentemente compatta: pochi algoritmi ricorsivi coprono filtraggio, predizione, smoothing e ricostruzione della sequenza piu' probabile, e tre famiglie di modelli (HMM, filtri di Kalman, reti bayesiane dinamiche) li specializzano per casi diversi.

Il capitolo e' anche una lezione di metodo: quando l'inferenza esatta diventa computazionalmente intrattabile, come accade appena lo stato ha molte variabili, si passa ad approssimazioni basate su campioni. Il particle filtering, che chiude il capitolo, e' uno degli algoritmi approssimati piu' usati in robotica e nel tracking.

## Un mondo a fette: stati, sensori e ipotesi di Markov

Il modello temporale di base ha tre componenti. Una distribuzione a priori sullo stato iniziale dice da dove si parte. Un modello di transizione specifica come lo stato evolve da un istante al successivo. Un modello sensoriale specifica quanto e' probabile ogni osservazione dato lo stato corrente. L'esempio conduttore del capitolo e' volutamente minimale: una guardia chiusa in un bunker vuole sapere se fuori piove, e la sua unica evidenza e' se il direttore arriva al mattino con o senza ombrello.

Il problema tecnico e' che la storia degli stati cresce senza limite: condizionare lo stato di oggi su tutta la storia passata e' impraticabile. Qui entra l'ipotesi di Markov: per predire lo stato presente basta una finestra limitata di passato, un orizzonte di ampiezza prefissata oltre il quale la storia piu' remota non aggiunge nulla. Nel caso del primo ordine, il presente rende il futuro indipendente dal passato — lo stato di oggi contiene gia' tutto cio' che serve per predire domani. Un'ipotesi analoga vale per i sensori: l'osservazione corrente dipende solo dallo stato corrente. Aggiungendo l'assunzione che le leggi del mondo non cambino nel tempo (omogeneita' temporale), bastano due tabelle di probabilita' condizionate per descrivere un processo di durata arbitraria.

L'ipotesi di Markov e' spesso solo approssimativamente vera, e il capitolo indica due rimedi: aumentare l'ordine del modello (far dipendere lo stato anche da istanti piu' remoti) oppure, in modo equivalente, arricchire l'insieme delle variabili di stato finche' non diventa "autosufficiente". Un robot la cui velocita' dipende dalla carica della batteria viola la proprieta' di Markov se la batteria non e' nello stato; includerla la ripristina. Modellare bene un processo significa in sostanza capire quale fisica lo governa.

## Le quattro domande che un agente pone al tempo

Definita la struttura, il capitolo elenca i compiti inferenziali fondamentali, tutti risolvibili con ricorsioni che costano tempo costante per passo.

Il filtraggio calcola la distribuzione sullo stato corrente date tutte le evidenze raccolte finora: e' la stima dello stato, cio' che serve per decidere adesso. Il risultato chiave del capitolo e' che questa stima si aggiorna in due mosse — proiettare in avanti la credenza attraverso il modello di transizione, poi correggerla con la nuova osservazione via regola di Bayes — senza mai riesaminare la storia. La credenza filtrata viaggia come un "messaggio in avanti" lungo la sequenza. Nell'esempio dell'ombrello, due giorni consecutivi di ombrello portano la probabilita' di pioggia oltre l'88 per cento, perche' la pioggia tende a persistere.

La predizione guarda avanti: e' un filtraggio senza nuove evidenze, in cui si applica solo il modello di transizione. Spingendo la predizione sempre piu' in la', la distribuzione converge a un punto fisso, la distribuzione stazionaria del processo: oltre un certo orizzonte (legato al tempo di mixing) il modello non sa piu' nulla di specifico sul futuro. E' un limite strutturale, non un difetto dell'algoritmo.

Lo smoothing guarda indietro: stima uno stato passato usando anche le evidenze arrivate dopo, e produce stime migliori del filtraggio perche' incorpora piu' informazione. Il calcolo combina il messaggio in avanti con un messaggio all'indietro che riassume le evidenze future; memorizzando i risultati del passaggio in avanti si regolarizza l'intera sequenza in tempo lineare. E' l'algoritmo forward-backward, fondamento computazionale di innumerevoli sistemi che elaborano sequenze rumorose.

Infine, la spiegazione piu' probabile cerca l'intera sequenza di stati che meglio giustifica le osservazioni. Non basta scegliere a ogni passo lo stato individualmente piu' probabile: la sequenza va valutata congiuntamente. L'algoritmo di Viterbi risolve il problema vedendo ogni sequenza come un cammino in un grafo di stati e sfruttando una ricorsione analoga al filtraggio, in cui la somma sugli stati precedenti diventa una massimizzazione. Il riconoscimento vocale classico e la decodifica di segnali su canali rumorosi sono applicazioni dirette.

## HMM: quando lo stato e' una sola variabile discreta

Il modello di Markov nascosto (HMM) e' il caso in cui lo stato e' una singola variabile discreta. Il vantaggio e' la concretezza: modello di transizione e modello sensoriale diventano matrici, e filtraggio e smoothing si riducono a prodotti matrice-vettore. Questa forma compatta abilita anche varianti raffinate, come uno smoothing che usa spazio costante indipendente dalla lunghezza della sequenza, o uno smoothing online a ritardo fisso con costo costante per aggiornamento.

L'esempio applicativo e' la localizzazione di un robot che si muove a caso in una griglia con sensori di ostacolo imprecisi. Anche con un tasso di errore per bit del 20 per cento — che rende sbagliata la maggior parte delle letture complessive — il robot riesce tipicamente a localizzarsi entro due caselle dopo una ventina di osservazioni, perche' l'inferenza integra le evidenze nel tempo e sfrutta i vincoli del modello di transizione. Nessuna singola lettura e' affidabile; la sequenza si'.

Il limite degli HMM e' rappresentazionale: lo stato e' atomico, senza struttura interna. Combinare piu' variabili in una "megavariabile" fa esplodere la matrice di transizione in modo esponenziale nel numero di variabili. Con 42 caselle e la possibilita' che ognuna sia sporca, gli stati diventano circa 1,8x10^14 (42 posizioni per 2^42 configurazioni di sporcizia) e la sola matrice di transizione richiederebbe oltre 10^29 valori di probabilita': serve un'altra rappresentazione.

## Filtri di Kalman: stato continuo e gaussiane

Se lo stato e' continuo — la posizione e la velocita' di un aereo su un radar, l'orbita di un pianeta — la variabile discreta non basta. Il filtro di Kalman gestisce questo caso assumendo che transizioni e osservazioni siano funzioni lineari dello stato piu' rumore gaussiano. La proprieta' magica delle gaussiane lineari e' la chiusura: se la credenza corrente e' gaussiana, dopo la proiezione in avanti e l'aggiornamento con l'osservazione resta gaussiana. La credenza e' quindi descritta per sempre da una media e una matrice di covarianza, senza crescita della rappresentazione — cosa che in generale, con altri modelli continui, non accade.

L'aggiornamento ha una lettura intuitiva: la nuova media e' una media pesata tra osservazione e predizione, dove il peso (la matrice dei guadagni di Kalman) stabilisce quanta fiducia accordare all'evidenza appena arrivata rispetto a cio' che il modello aveva anticipato. Se il sensore e' rumoroso si crede di piu' al modello; se il processo e' imprevedibile si crede di piu' al sensore. Curiosamente, la sequenza delle varianze non dipende dalle osservazioni e converge in fretta: si puo' calcolare offline.

Le ipotesi di linearita' e gaussianita' sono pero' stringenti. Un uccello che vola verso un tronco non prosegue dritto in media: scarta a destra o a sinistra, e una singola gaussiana centrata sul tronco e' una pessima predizione. Il filtro di Kalman esteso (EKF) linearizza localmente i sistemi non lineari; il filtro a commutazione fa girare piu' filtri in parallelo, ciascuno con un modello diverso del comportamento, pesandone le predizioni.

## Reti bayesiane dinamiche: fattorizzare lo stato

Le reti bayesiane dinamiche (DBN) estendono le reti bayesiane ai processi temporali: ogni time slice e' una copia della stessa sottorete, con archi che collegano un istante al successivo. Ogni HMM e ogni filtro di Kalman e' una DBN particolare, ma la direzione interessante e' l'inversa: scomponendo lo stato nelle sue variabili costitutive, la DBN sfrutta la sparsita' delle dipendenze. Dove l'HMM richiede tabelle esponenziali nel numero di variabili, la DBN cresce linearmente se ogni variabile ha pochi genitori. E a differenza del filtro di Kalman, una DBN puo' rappresentare distribuzioni arbitrarie — utile quando la credenza e' multimodale, come per delle chiavi che possono essere in tasca, sul comodino o nella porta, ma quasi certamente non a mezz'aria in giardino.

Una parte istruttiva del capitolo riguarda la modellazione dei sensori che falliscono. Un modello di errore gaussiano ingenuo, davanti a una lettura assurda (batteria a zero dopo venti letture a cinque), conclude che la batteria e' davvero scarica. Aggiungere una piccola probabilita' di lettura completamente sbagliata (modello di fallimento transitorio) da' alla credenza un'inerzia che assorbe i glitch. Per i guasti permanenti serve di piu': una variabile di stato aggiuntiva che rappresenta la salute del sensore, con un arco di persistenza che ricorda che un sensore rotto resta rotto. La morale e' generale: un sistema gestisce correttamente il fallimento dei sensori solo se il suo modello sensoriale contempla la possibilita' del fallimento.

Sul fronte inferenziale la notizia e' agrodolce. Srotolare la DBN e applicare gli algoritmi esatti funziona, e con l'eliminazione delle variabili in ordine temporale si ottengono aggiornamenti a costo costante; ma quel costo e' in generale esponenziale nel numero di variabili di stato, perche' la distribuzione a posteriori congiunta non resta fattorizzata. Rappresentare in modo compatto non implica ragionare in modo efficiente ed esatto.

## Particelle: approssimare il posterior con una popolazione di campioni

La via d'uscita e' l'approssimazione. La likelihood weighting applicata alla rete srotolata fallisce: le variabili di stato vengono campionate senza tener conto delle evidenze, e la frazione di campioni con peso significativo crolla esponenzialmente con la lunghezza della sequenza. Il particle filtering aggiunge il passo che cambia tutto: il ricampionamento. A ogni istante ogni campione viene propagato in avanti col modello di transizione, pesato con la verosimiglianza della nuova evidenza, e poi la popolazione viene ricampionata proporzionalmente ai pesi. I campioni improbabili muoiono, quelli plausibili si moltiplicano, e la popolazione si concentra dove il posterior e' alto. L'algoritmo e' consistente (converge alla distribuzione corretta al crescere dei campioni) e in pratica mantiene un buon posterior con un numero costante di particelle.

Anche il particle filtering ha punti deboli: se il modello di transizione e' deterministico su alcune variabili (la sporcizia che non si sposta mai), le ipotesi iniziali delle particelle non vengono mai corrette e l'algoritmo collassa su una mappa sbagliata. Quando pero' il problema ha struttura di indipendenza condizionale — nello SLAM, dati i percorsi del robot, le caselle sono indipendenti tra loro — il particle filter di Rao-Blackwell combina campionamento (sulla traiettoria) e inferenza esatta (su ogni casella), recuperando accuratezza dove il campionamento puro fallirebbe.

## Idee chiave

- Un mondo che cambia si modella replicando le variabili di stato e di evidenza per ogni istante temporale discreto.
- L'ipotesi di Markov (il futuro dipende dal passato solo attraverso il presente) e l'omogeneita' temporale rendono la rappresentazione finita e compatta: bastano un modello di transizione e un modello sensoriale.
- Filtraggio, predizione, smoothing e spiegazione piu' probabile sono i quattro compiti inferenziali di base; tutti ammettono algoritmi ricorsivi lineari nella lunghezza della sequenza, con aggiornamenti a costo costante per passo.
- Il forward-backward combina un messaggio in avanti e uno all'indietro per stimare gli stati passati; Viterbi sostituisce la somma con il massimo per trovare la sequenza di stati globalmente piu' probabile.
- Gli HMM (stato discreto singolo) riducono tutto ad algebra di matrici; i filtri di Kalman (stato continuo, dinamica gaussiana lineare) mantengono per sempre una credenza gaussiana descritta da media e covarianza.
- Le DBN fattorizzano lo stato in piu' variabili e rappresentano in modo compatto processi che farebbero esplodere un HMM; includono HMM e filtri di Kalman come casi speciali.
- Salvo casi speciali come i modelli gaussiani lineari, l'inferenza esatta con molte variabili di stato e' intrattabile: rappresentare compattamente non basta a ragionare efficientemente.
- Il particle filtering — propagazione, pesatura, ricampionamento — e' la famiglia di algoritmi approssimati di riferimento; la variante di Rao-Blackwell mescola campioni e inferenza esatta dove la struttura lo consente.

## Perche conta oggi

Le architetture agentiche moderne rimettono al centro esattamente il problema di questo capitolo: un [agente](../kb/concetti/agent.md) che opera per molti passi in un ambiente parzialmente osservabile deve mantenere una stima di stato aggiornabile in modo incrementale, senza rileggere ogni volta l'intera storia. Il messaggio in avanti del filtraggio — una sintesi a costo costante di tutto il passato rilevante — e' concettualmente lo stesso vincolo che spinge gli agenti basati su [LLM](../kb/concetti/llm.md) a comprimere la memoria di lavoro invece di accumulare trascrizioni illimitate in una [context window](../kb/concetti/context-window.md) finita. E l'idea di un modello di transizione appreso che permette predizione e smoothing e' l'antenata diretta dei [world models](../kb/concetti/world-models.md) con cui oggi si addestrano agenti capaci di simulare le conseguenze delle proprie azioni.

Anche le lezioni operative restano attuali. Il principio per cui un sistema robusto deve modellare il fallimento dei propri sensori si traduce, nella pratica degli agenti con [tool use](../kb/concetti/tool-use.md), nel trattare gli output degli strumenti come evidenza fallibile e non come verita'. E il trade-off tra inferenza esatta intrattabile e approssimazioni campionarie efficienti e' lo stesso che governa ogni scelta di [inference](../kb/concetti/inference.md) su modelli di grandi dimensioni: la qualita' della stima si compra con il calcolo, e gli algoritmi che vincono sono quelli che concentrano il calcolo dove la probabilita' e' alta.

## Riferimenti

- Stuart J. Russell, Peter Norvig — *Intelligenza Artificiale: Un Approccio Moderno*, 4a edizione italiana, Pearson Italia, Vol. 1 (2021), Capitolo 14, pp. 471-510.
