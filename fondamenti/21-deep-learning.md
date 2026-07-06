---
titolo: Deep learning
capitolo: 21
parte: 5
volume: 2
pagine: "103-140"
concetti: [llm, embedding, fine-tuning, inference]
created: 2026-07-06
last_updated: 2026-07-06
---

# Deep learning

Il capitolo 21 di Russell e Norvig affronta una domanda precisa: come si costruiscono e si addestrano ipotesi che non siano semplici funzioni lineari, ma circuiti algebrici profondi, con molti strati tra input e output? La regressione lineare o logistica calcola l'output in pochissimi passi e tratta ogni variabile di input in modo indipendente: questo limita drasticamente cio' che il modello puo' rappresentare. Il deep learning ribalta l'impostazione: si addestrano circuiti con cammini computazionali lunghi, in cui tutte le variabili di input possono interagire tra loro in modi complessi.

L'idea storica viene dai primi tentativi di modellare i neuroni come circuiti computazionali (McCulloch e Pitts, 1943), motivo per cui questi modelli si chiamano ancora reti neurali, anche se la somiglianza con il cervello resta superficiale. Il motivo pratico del successo e' un altro: su dati ad alta dimensionalita' come immagini, audio e testo, il deep learning supera ogni altro approccio di apprendimento automatico, ed e' oggi la base del riconoscimento visivo, della traduzione automatica, della sintesi vocale e di buona parte dell'apprendimento con rinforzo.

Il capitolo costruisce il quadro completo: dalle reti feedforward piu' semplici ai grafi computazionali generali, dalle reti convoluzionali per la visione alle reti ricorrenti per le sequenze, fino ai metodi non supervisionati e al transfer learning.

<figure class="diagram">
<svg viewBox="0 0 760 460" role="img" aria-label="Mappa concettuale del capitolo 21: dal deep learning come circuiti con cammini lunghi al grafo computazionale con pesi regolabili, addestrato con retropropagazione; ai lati le reti feedforward, convoluzionali e ricorrenti, in basso generalizzazione, apprendimento non supervisionato e transfer learning fino alle applicazioni">
<defs><marker id="arr-c21" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" class="dg-arrow"/></marker></defs>
<line x1="330" y1="68" x2="140" y2="101" class="dg-edge" marker-end="url(#arr-c21)"/>
<text x="235" y="80" text-anchor="middle" class="dg-edge-label">caso piu' semplice</text>
<line x1="380" y1="68" x2="380" y2="101" class="dg-edge-primary" marker-end="url(#arr-c21)"/>
<line x1="430" y1="68" x2="620" y2="101" class="dg-edge" marker-end="url(#arr-c21)"/>
<text x="535" y="82" text-anchor="middle" class="dg-edge-label">per le immagini</text>
<line x1="204" y1="132" x2="267" y2="132" class="dg-edge" marker-end="url(#arr-c21)"/>
<line x1="380" y1="160" x2="380" y2="193" class="dg-edge-primary" marker-end="url(#arr-c21)"/>
<text x="470" y="180" text-anchor="middle" class="dg-edge-label">discesa del gradiente</text>
<line x1="460" y1="160" x2="610" y2="193" class="dg-edge" marker-end="url(#arr-c21)"/>
<text x="535" y="176" text-anchor="middle" class="dg-edge-label">cicli con ritardo</text>
<line x1="270" y1="224" x2="207" y2="224" class="dg-edge" marker-end="url(#arr-c21)"/>
<text x="238" y="216" text-anchor="middle" class="dg-edge-label">problema</text>
<line x1="380" y1="252" x2="380" y2="285" class="dg-edge" marker-end="url(#arr-c21)"/>
<text x="470" y="272" text-anchor="middle" class="dg-edge-label">adattarsi non basta</text>
<line x1="380" y1="344" x2="380" y2="381" class="dg-edge" marker-end="url(#arr-c21)"/>
<line x1="140" y1="344" x2="295" y2="381" class="dg-edge" marker-end="url(#arr-c21)"/>
<line x1="610" y1="344" x2="465" y2="381" class="dg-edge" marker-end="url(#arr-c21)"/>
<text x="545" y="362" text-anchor="middle" class="dg-edge-label">meno etichette</text>
<rect x="270" y="12" width="220" height="56" rx="10" class="dg-node-primary"/>
<text x="380" y="36" text-anchor="middle" class="dg-label">Deep learning</text>
<text x="380" y="52" text-anchor="middle" class="dg-sublabel">circuiti con cammini lunghi</text>
<rect x="8" y="104" width="196" height="56" rx="10" class="dg-node"/>
<text x="106" y="128" text-anchor="middle" class="dg-label">Rete feedforward</text>
<text x="106" y="144" text-anchor="middle" class="dg-sublabel">somma pesata + attivazione</text>
<rect x="270" y="104" width="220" height="56" rx="10" class="dg-node-primary"/>
<text x="380" y="128" text-anchor="middle" class="dg-label">Grafo computazionale</text>
<text x="380" y="144" text-anchor="middle" class="dg-sublabel">pesi come manopole regolabili</text>
<rect x="546" y="104" width="206" height="56" rx="10" class="dg-node"/>
<text x="649" y="128" text-anchor="middle" class="dg-label">Reti convoluzionali</text>
<text x="649" y="144" text-anchor="middle" class="dg-sublabel">localita' e invarianza spaziale</text>
<rect x="8" y="196" width="196" height="56" rx="10" class="dg-node"/>
<text x="106" y="220" text-anchor="middle" class="dg-label">Scomparsa del gradiente</text>
<text x="106" y="236" text-anchor="middle" class="dg-sublabel">risolta dalle reti residuali</text>
<rect x="270" y="196" width="220" height="56" rx="10" class="dg-node-primary"/>
<text x="380" y="220" text-anchor="middle" class="dg-label">Retropropagazione</text>
<text x="380" y="236" text-anchor="middle" class="dg-sublabel">l'errore risale la rete</text>
<rect x="546" y="196" width="206" height="56" rx="10" class="dg-node"/>
<text x="649" y="220" text-anchor="middle" class="dg-label">Reti ricorrenti e LSTM</text>
<text x="649" y="236" text-anchor="middle" class="dg-sublabel">memoria per le sequenze</text>
<rect x="8" y="288" width="196" height="56" rx="10" class="dg-node"/>
<text x="106" y="312" text-anchor="middle" class="dg-label">Non supervisionato</text>
<text x="106" y="328" text-anchor="middle" class="dg-sublabel">autoencoder, VAE, GAN</text>
<rect x="270" y="288" width="220" height="56" rx="10" class="dg-node"/>
<text x="380" y="312" text-anchor="middle" class="dg-label">Generalizzazione</text>
<text x="380" y="328" text-anchor="middle" class="dg-sublabel">architettura, decadimento, dropout</text>
<rect x="546" y="288" width="206" height="56" rx="10" class="dg-node"/>
<text x="649" y="312" text-anchor="middle" class="dg-label">Transfer learning</text>
<text x="649" y="328" text-anchor="middle" class="dg-sublabel">preaddestra, poi regola finemente</text>
<rect x="255" y="384" width="250" height="56" rx="10" class="dg-node-accent"/>
<text x="380" y="408" text-anchor="middle" class="dg-label">Applicazioni</text>
<text x="380" y="424" text-anchor="middle" class="dg-sublabel">visione, linguaggio, RL deep</text>
</svg>
<figcaption>Mappa del capitolo 21 — dal circuito con pesi regolabili alla retropropagazione, fino alle applicazioni in visione, linguaggio e rinforzo</figcaption>
</figure>

## Reti come composizione di funzioni

Una rete feedforward e' un grafo aciclico orientato in cui ogni nodo, detto unita', calcola una somma pesata dei propri input e vi applica una funzione di attivazione non lineare. La non linearita' e' il punto cruciale: comporre funzioni lineari produce ancora una funzione lineare, mentre comporre unita' non lineari permette a reti abbastanza grandi di approssimare qualsiasi funzione continua (teorema di approssimazione universale, che vale gia' con due soli strati). Le attivazioni piu' usate sono la sigmoide, la ReLU (che restituisce il massimo tra zero e l'input), la sua versione smussata softplus e la tangente iperbolica.

<figure class="diagram">
<svg viewBox="0 0 760 280" role="img" aria-label="Rete neurale feedforward con due input x1 e x2, uno strato nascosto di due unita' (3 e 4) e una unita' di output (5) che produce l'output y previsto; sui collegamenti i pesi w1,3 w1,4 w2,3 w2,4 w3,5 w4,5">
<defs><marker id="arr-c21-b" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" class="dg-arrow"/></marker></defs>
<line x1="170" y1="78" x2="326" y2="78" class="dg-edge" marker-end="url(#arr-c21-b)"/>
<text x="250" y="70" text-anchor="middle" class="dg-edge-label">w1,3</text>
<line x1="170" y1="98" x2="326" y2="200" class="dg-edge" marker-end="url(#arr-c21-b)"/>
<text x="200" y="135" text-anchor="middle" class="dg-edge-label">w1,4</text>
<line x1="170" y1="198" x2="326" y2="96" class="dg-edge" marker-end="url(#arr-c21-b)"/>
<text x="200" y="168" text-anchor="middle" class="dg-edge-label">w2,3</text>
<line x1="170" y1="218" x2="326" y2="218" class="dg-edge" marker-end="url(#arr-c21-b)"/>
<text x="250" y="236" text-anchor="middle" class="dg-edge-label">w2,4</text>
<line x1="450" y1="92" x2="586" y2="136" class="dg-edge" marker-end="url(#arr-c21-b)"/>
<text x="505" y="98" text-anchor="middle" class="dg-edge-label">w3,5</text>
<line x1="450" y1="204" x2="586" y2="160" class="dg-edge" marker-end="url(#arr-c21-b)"/>
<text x="505" y="200" text-anchor="middle" class="dg-edge-label">w4,5</text>
<line x1="710" y1="148" x2="744" y2="148" class="dg-edge" marker-end="url(#arr-c21-b)"/>
<rect x="60" y="50" width="110" height="56" rx="10" class="dg-node"/>
<text x="115" y="74" text-anchor="middle" class="dg-label">x1</text>
<text x="115" y="90" text-anchor="middle" class="dg-sublabel">input</text>
<rect x="60" y="190" width="110" height="56" rx="10" class="dg-node"/>
<text x="115" y="214" text-anchor="middle" class="dg-label">x2</text>
<text x="115" y="230" text-anchor="middle" class="dg-sublabel">input</text>
<rect x="330" y="50" width="120" height="56" rx="10" class="dg-node-primary"/>
<text x="390" y="74" text-anchor="middle" class="dg-label">3</text>
<text x="390" y="90" text-anchor="middle" class="dg-sublabel">strato nascosto</text>
<rect x="330" y="190" width="120" height="56" rx="10" class="dg-node-primary"/>
<text x="390" y="214" text-anchor="middle" class="dg-label">4</text>
<text x="390" y="230" text-anchor="middle" class="dg-sublabel">strato nascosto</text>
<rect x="590" y="120" width="120" height="56" rx="10" class="dg-node-accent"/>
<text x="650" y="144" text-anchor="middle" class="dg-label">5</text>
<text x="650" y="160" text-anchor="middle" class="dg-sublabel">output y previsto</text>
</svg>
<figcaption>Rete neurale con due input, uno strato nascosto di due unita' e una unita' di output — schema ripreso dalla figura 21.3 del cap. 21, AIMA 4a ed.</figcaption>
</figure>

Il modo piu' generale di guardare una rete e' come grafo computazionale: un circuito in cui ogni nodo rappresenta un'operazione elementare e i pesi sono parametri regolabili, manopole che decidono quanto ogni nodo "ascolta" i suoi predecessori. L'apprendimento consiste nel ruotare queste manopole finche' l'output della rete si avvicina ai valori osservati nei dati di addestramento.

La codifica di input e output segue schemi ricorrenti. Gli attributi categorici si rappresentano con la codifica one-hot, per evitare che la rete attribuisca significato a un'adiacenza numerica che non esiste (un ristorante thai non e' "vicino" a un fast-food solo perche' i codici 3 e 4 sono contigui). In uscita, per la classificazione multiclasse si usa uno strato softmax che trasforma i valori grezzi in una distribuzione di probabilita', e come funzione di perdita si minimizza l'entropia incrociata, cioe' la verosimiglianza logaritmica negativa dei dati. Per la regressione si usa tipicamente uno strato di output lineare, equivalente a una regressione lineare sulle caratteristiche costruite dagli strati precedenti.

Gli strati nascosti sono il cuore dell'ipotesi che spiega perche' il deep learning funziona: la trasformazione complessiva da input a output (dall'immagine alla categoria "giraffa") viene scomposta in tante trasformazioni semplici, ognuna appresa con aggiornamenti locali. Ogni strato produce una nuova rappresentazione dell'input, e spesso queste rappresentazioni intermedie catturano strutture significative — bordi, angoli, occhi, facce — anche se non sempre risultano interpretabili per un essere umano.

## Retropropagazione: l'errore che risale la rete

L'addestramento usa la discesa del gradiente: si calcola quanto la perdita cambia al variare di ciascun peso e si aggiornano i pesi nella direzione che la riduce. Per i pesi vicini all'output il calcolo e' diretto; per quelli negli strati nascosti serve applicare ripetutamente la regola della catena. Il risultato e' un'intuizione potente: ogni unita' riceve un "errore percepito" che e' l'errore dell'unita' successiva moltiplicato per i pesi del cammino che le collega. L'errore misurato in uscita viene cosi' retrocesso strato per strato, da cui il nome retropropagazione.

Il capitolo generalizza il meccanismo a qualsiasi grafo computazionale: durante il passaggio in avanti ogni nodo calcola il suo valore, durante quello all'indietro raccoglie i messaggi di gradiente dai successori, li somma e li propaga ai predecessori. Il costo e' lineare nel numero di nodi, i messaggi possono essere tensori elaborati in parallelo su GPU o TPU, e il rovescio della medaglia e' la memoria: i valori intermedi del passaggio in avanti vanno conservati per quello all'indietro.

In pratica nessuno deriva i gradienti a mano: i pacchetti software moderni usano la differenziazione automatica, che applica meccanicamente le regole del calcolo a qualsiasi programma numerico. Questo ha reso possibile l'apprendimento end-to-end, in cui un sistema complesso viene addestrato per intero da coppie input/output, senza che il progettista debba specificare cosa deve fare ogni sottosistema.

Un problema strutturale emerge subito: le derivate locali delle attivazioni possono essere quasi zero, e moltiplicandosi lungo molti strati i segnali di errore si estinguono. E' la scomparsa del gradiente, che affligge le reti molto profonde. Le reti residuali la aggirano con un cambio di prospettiva: ogni strato non sostituisce la rappresentazione precedente ma la perturba, aggiungendo un residuo appreso. Se il residuo e' nullo, lo strato lascia passare l'informazione inalterata: la rete propaga i segnali per default, invece di dover imparare a farlo.

## Convoluzioni: geometria dentro la rete

Trattare un'immagine come un vettore piatto di pixel butta via un'informazione essenziale: i pixel adiacenti sono correlati. Una rete completamente connessa su un'immagine da un megapixel avrebbe migliaia di miliardi di pesi e nessuna nozione di vicinanza. Le reti convoluzionali (CNN) iniettano nella struttura della rete due conoscenze a priori sulle immagini: la localita' (ogni unita' guarda solo una piccola regione dell'input) e l'invarianza spaziale (un occhio ha lo stesso aspetto in qualunque punto dell'immagine, quindi lo stesso rilevatore di caratteristiche puo' essere replicato ovunque).

Lo strumento e' il kernel: un piccolo pattern di pesi condivisi che viene fatto scorrere sull'immagine calcolando un prodotto scalare a ogni posizione (l'operazione si chiama convoluzione). Con d kernel distinti il numero di parametri diventa indipendente dalla dimensione dell'immagine, e ogni kernel produce una feature map che indica dove la sua caratteristica appare. Il passo (stride) controlla il sottocampionamento, e gli strati di pooling riassumono regioni adiacenti con la media o con il massimo, riducendo la risoluzione e facilitando il riconoscimento a scale diverse. Il campo recettivo delle unita' cresce con la profondita': gli strati alti "vedono" porzioni sempre piu' ampie dell'input, il che spiega perche' la profondita' serve a comporre caratteristiche locali in oggetti interi.

Tutto questo si esprime elegantemente come operazioni su tensori, array multidimensionali che le librerie compilano in codice ottimizzato per GPU e TPU, elaborando minibatch di immagini in parallelo.

## Addestrare bene e generalizzare

Le reti moderne si addestrano quasi sempre con la discesa stocastica del gradiente (SGD): a ogni passo si stima il gradiente su un minibatch casuale di esempi. La stocasticita' aiuta a sfuggire ai minimi locali, il costo per passo resta costante, e accorgimenti come il momento (una media mobile dei gradienti recenti) e la riduzione progressiva del tasso di apprendimento migliorano la convergenza. La normalizzazione batch stabilizza ulteriormente l'addestramento riscalando i valori interni della rete rispetto a media e varianza del minibatch.

Adattarsi ai dati di addestramento pero' non basta: l'obiettivo e' generalizzare a dati mai visti. Il capitolo indica tre leve. La prima e' la scelta dell'architettura, che codifica assunzioni sul dominio: e' un risultato empirico centrale che, a parita' di numero di pesi, una rete piu' profonda generalizza meglio di una piu' larga. Poiche' mancano linee guida definitive, la selezione dell'architettura viene spesso automatizzata (ricerca dell'architettura neurale, con algoritmi evolutivi, apprendimento con rinforzo o funzioni di valutazione apprese). La seconda leva e' il decadimento del peso, una penalita' sui pesi grandi che equivale a un apprendimento con massimo a posteriori con prior gaussiano. La terza e' il dropout: durante l'addestramento si disattivano a caso unita' della rete, costringendo il modello a non dipendere mai da una sola caratteristica — ogni input deve restare riconoscibile anche quando parte della rete e' spenta.

Il capitolo segnala anche un limite inquietante: gli esempi ostili (adversarial examples). Bastano perturbazioni impercettibili di pochi pixel per far classificare un cane come un'ostrica, e questi attacchi spesso si trasferiscono tra reti con architetture e dati diversi. E' un indizio che le reti riconoscono gli oggetti in modi profondamente differenti dal sistema visivo umano.

## Sequenze e memoria: RNN e LSTM

Per dati sequenziali le reti feedforward hanno un difetto strutturale: possono guardare solo una finestra di lunghezza fissa. Le reti ricorrenti (RNN) introducono cicli con ritardo nel grafo computazionale, dando alla rete uno stato interno — una memoria — che riassume gli input precedenti. Addestrarle equivale a "srotolare" la rete lungo i passi temporali e applicare la retropropagazione nel tempo, con i pesi condivisi tra tutti i passi.

La condivisione dei pesi, pero', rende il gradiente un prodotto di molti fattori simili: se il peso ricorrente e' minore di uno il gradiente svanisce, se e' maggiore esplode. L'architettura LSTM (long short-term memory) risolve il problema con una cella di memoria che viene copiata, non moltiplicata, da un passo al successivo, e con unita' di porta apprese — forget gate, input gate, output gate — che decidono in modo "morbido" cosa ricordare, cosa aggiornare e cosa esporre. Le LSTM sono state le prime RNN realmente utilizzabili su larga scala, con ottimi risultati nel riconoscimento vocale e nell'elaborazione del linguaggio.

## Imparare senza etichette e trasferire conoscenza

L'apprendimento supervisionato richiede enormi quantita' di dati etichettati, mentre a un bambino basta una giraffa per riconoscerle tutte. Da qui l'interesse per paradigmi meno dipendenti dalle etichette. L'apprendimento non supervisionato lavora su soli input e persegue due obiettivi: apprendere nuove rappresentazioni e apprendere modelli generativi da cui campionare dati nuovi. Il capitolo presenta una progressione di modelli: il PCA probabilistico come generativo minimale; gli autoencoder, che comprimono l'input in una rappresentazione e lo ricostruiscono; gli autoencoder variazionali (VAE), che rendono trattabile l'inferenza massimizzando un limite inferiore variazionale (ELBO) sulla verosimiglianza; i modelli autoregressivi deep, che predicono ogni elemento di una sequenza dai precedenti senza variabili latenti (WaveNet per la sintesi vocale ne e' l'esempio piu' noto); e le GAN, coppie generatore-discriminatore addestrate in competizione, capaci di produrre volti fotorealistici di persone mai esistite.

L'apprendimento per trasferimento sfrutta l'esperienza su un compito per impararne meglio un altro: in pratica si copiano i pesi di un modello preaddestrato (ResNet-50 per la visione, RoBERTa per il linguaggio) e li si regola finemente sul nuovo compito, spesso congelando i primi strati che fungono da estrattori di caratteristiche generali. Una variante cruciale e' il trasferimento dalla simulazione al mondo reale, per esempio nella guida autonoma. L'apprendimento multitask spinge oltre: addestrare simultaneamente su molti obiettivi forza il modello a costruire rappresentazioni comuni piu' profonde.

## Dove il deep learning ha vinto

Il capitolo chiude con le applicazioni. Nella visione, la svolta e' AlexNet a ImageNet 2012: tasso di errore del 15,3% contro il 25% del secondo classificato, cinque strati convoluzionali, ReLU e GPU; nel giro di pochi anni l'errore e' sceso sotto il 2%, meglio di un umano addestrato. Nel linguaggio naturale, la traduzione end-to-end ha ridotto gli errori del 60% rispetto ai sistemi a fasi, e i word embedding — parole rappresentate come vettori in uno spazio ad alta dimensionalita', dove termini usati in contesti simili finiscono vicini — si sono rivelati la chiave della generalizzazione linguistica. Nell'apprendimento per rinforzo deep, agenti come DQN hanno imparato a giocare ai videogiochi Atari da pixel grezzi e segnali di punteggio, e AlphaGo ha battuto i campioni umani di Go; restano pero' fragilita' quando l'ambiente differisce anche poco dall'addestramento.

## Idee chiave

- Le reti neurali rappresentano funzioni non lineari complesse componendo unita' semplici: somma pesata piu' attivazione non lineare, organizzate in grafi computazionali con pesi regolabili.
- La retropropagazione e' discesa del gradiente nello spazio dei pesi: l'errore misurato in uscita risale la rete via regola della catena, e la differenziazione automatica la rende disponibile per qualsiasi architettura.
- La profondita' paga: a parita' di parametri, reti piu' profonde generalizzano meglio, perche' scompongono trasformazioni complesse in passi semplici e componibili.
- Le reti convoluzionali codificano localita' e invarianza spaziale, e per questo dominano sui dati con topologia a griglia come le immagini.
- Le reti ricorrenti aggiungono memoria per i dati sequenziali; le LSTM, con cella di memoria copiata e porte apprese, evitano scomparsa ed esplosione del gradiente.
- Generalizzare richiede piu' leve insieme: architettura adatta al dominio, decadimento del peso, dropout (che impedisce alla rete di affidarsi a una singola caratteristica) — ma gli esempi ostili mostrano che la robustezza resta un problema aperto.
- Autoencoder variazionali, modelli autoregressivi e GAN permettono di apprendere da dati non etichettati e di generare dati nuovi.
- Il transfer learning — preaddestrare su un compito ricco di dati e regolare finemente sul compito target — riduce drasticamente il fabbisogno di etichette.

## Perche conta oggi

Questo capitolo descrive, senza nominarli, i mattoni degli attuali [LLM](../kb/concetti/llm.md): i modelli autoregressivi deep che predicono l'elemento successivo di una sequenza sono esattamente il principio generativo di GPT e Claude, i word [embedding](../kb/concetti/embedding.md) sono l'antenato diretto delle rappresentazioni vettoriali su cui si fondano ricerca semantica e RAG, e l'apprendimento per trasferimento con modelli preaddestrati e' diventato il paradigma dominante del [fine-tuning](../kb/concetti/fine-tuning.md). Anche i problemi indicati come aperti nel 2021 sono ancora attuali: gli esempi ostili prefigurano i jailbreak e le prompt injection, e la finestra fissa delle reti feedforward e' il limite che oggi chiamiamo [context window](../kb/concetti/context-window.md).

Colpisce, in retrospettiva, cio' che il capitolo non contiene: il Transformer viene rimandato ai capitoli sul linguaggio, e LSTM e CNN occupano il centro della scena. Eppure la meccanica di fondo — grafi computazionali, SGD su minibatch, retropropagazione, normalizzazione, hardware parallelo — e' identica a quella con cui si addestrano e si eseguono i modelli di frontiera: capire questi fondamenti significa capire cosa succede davvero durante l'addestramento e l'[inference](../kb/concetti/inference.md) di qualsiasi sistema AI moderno.

## Riferimenti

- Stuart J. Russell, Peter Norvig — *Intelligenza Artificiale: Un Approccio Moderno*, 4a edizione italiana, Pearson Italia, Vol. 2 (2022), Capitolo 21, pp. 103-140.
