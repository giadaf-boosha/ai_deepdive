---
titolo: Visione artificiale
capitolo: 25
parte: 6
volume: 2
pagine: "239-282"
concetti: [world-models, evaluation-benchmark, embedding, agent]
created: 2026-07-06
last_updated: 2026-07-06
---
# Visione artificiale

Il capitolo affronta una domanda apparentemente banale e in realta' profonda: come si trasforma un flusso di pixel in una descrizione utile del mondo? Gli occhi sono organi costosi per un organismo — occupano spazio, consumano energia, si danneggiano facilmente — eppure quasi tutti gli animali li hanno, perche' vedere permette di anticipare il futuro: capire se un oggetto si avvicina, se il terreno regge, quanto dista un frutto. La visione artificiale prova a dare la stessa capacita' a un computer collegato a una fotocamera.

Il problema e' difficile perche' le immagini sono ambigue per costruzione. La proiezione da 3D a 2D butta via informazione: un oggetto piccolo e vicino produce la stessa immagine di uno grande e lontano, un oggetto bianco in penombra puo' apparire piu' scuro di uno nero sotto luce intensa. Russell e Norvig organizzano il capitolo attorno a due problemi fondamentali: la ricostruzione, cioe' costruire un modello del mondo a partire dalle immagini, e il riconoscimento, cioe' tracciare distinzioni tra gli oggetti osservati — che cosa sono, dove sono, che cosa stanno facendo.

Il percorso va dalla fisica alla semantica: prima la geometria e l'ottica della formazione delle immagini, poi le caratteristiche di basso livello estraibili dai pixel, quindi la classificazione e il rilevamento di oggetti con reti neurali convoluzionali, la ricostruzione del mondo tridimensionale e infine una rassegna di applicazioni, dalla guida autonoma alla generazione di immagini.

<figure class="diagram">
<svg viewBox="0 0 760 470" role="img" aria-label="Mappa concettuale del capitolo 25: dalla formazione delle immagini al problema inverso della visione artificiale, i due problemi fondamentali di riconoscimento e ricostruzione, le caratteristiche di basso livello, le CNN con la svolta di ImageNet, il rilevamento di oggetti, la terza dimensione e le applicazioni finali">
<defs><marker id="arr-c25" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" class="dg-arrow"/></marker></defs>
<line x1="183" y1="40" x2="300" y2="40" class="dg-edge" marker-end="url(#arr-c25)"/>
<text x="241" y="32" text-anchor="middle" class="dg-edge-label">problema inverso</text>
<line x1="400" y1="68" x2="400" y2="110" class="dg-edge-primary" marker-end="url(#arr-c25)"/>
<line x1="470" y1="68" x2="630" y2="110" class="dg-edge-primary" marker-end="url(#arr-c25)"/>
<text x="455" y="92" text-anchor="middle" class="dg-edge-label">due problemi</text>
<line x1="95" y1="68" x2="95" y2="110" class="dg-edge" marker-end="url(#arr-c25)"/>
<text x="148" y="92" text-anchor="middle" class="dg-edge-label">dai pixel</text>
<line x1="204" y1="138" x2="302" y2="138" class="dg-edge" marker-end="url(#arr-c25)"/>
<line x1="400" y1="166" x2="400" y2="210" class="dg-edge" marker-end="url(#arr-c25)"/>
<text x="480" y="192" text-anchor="middle" class="dg-edge-label">classificatori appresi</text>
<line x1="652" y1="166" x2="652" y2="210" class="dg-edge" marker-end="url(#arr-c25)"/>
<line x1="204" y1="238" x2="302" y2="238" class="dg-edge" marker-end="url(#arr-c25)"/>
<text x="253" y="230" text-anchor="middle" class="dg-edge-label">svolta 2012</text>
<line x1="400" y1="266" x2="400" y2="310" class="dg-edge" marker-end="url(#arr-c25)"/>
<text x="455" y="292" text-anchor="middle" class="dg-edge-label">anche dove</text>
<line x1="400" y1="366" x2="400" y2="400" class="dg-edge" marker-end="url(#arr-c25)"/>
<line x1="650" y1="266" x2="470" y2="400" class="dg-edge" marker-end="url(#arr-c25)"/>
<rect x="8" y="12" width="175" height="56" rx="10" class="dg-node"/>
<text x="96" y="36" text-anchor="middle" class="dg-label">Dalla scena ai pixel</text>
<text x="96" y="52" text-anchor="middle" class="dg-sublabel">proiezione prospettica, luce</text>
<rect x="300" y="12" width="200" height="56" rx="10" class="dg-node-primary"/>
<text x="400" y="36" text-anchor="middle" class="dg-label">Visione artificiale</text>
<text x="400" y="52" text-anchor="middle" class="dg-sublabel">da pixel a descrizione del mondo</text>
<rect x="8" y="110" width="196" height="56" rx="10" class="dg-node"/>
<text x="106" y="134" text-anchor="middle" class="dg-label">Basso livello</text>
<text x="106" y="150" text-anchor="middle" class="dg-sublabel">bordi, texture, flusso, regioni</text>
<rect x="302" y="110" width="196" height="56" rx="10" class="dg-node"/>
<text x="400" y="134" text-anchor="middle" class="dg-label">Riconoscimento</text>
<text x="400" y="150" text-anchor="middle" class="dg-sublabel">che cosa, dove, che cosa fa</text>
<rect x="556" y="110" width="196" height="56" rx="10" class="dg-node"/>
<text x="654" y="134" text-anchor="middle" class="dg-label">Ricostruzione</text>
<text x="654" y="150" text-anchor="middle" class="dg-sublabel">modello del mondo dalle immagini</text>
<rect x="8" y="210" width="196" height="56" rx="10" class="dg-node"/>
<text x="106" y="234" text-anchor="middle" class="dg-label">ImageNet</text>
<text x="106" y="250" text-anchor="middle" class="dg-sublabel">14M immagini, dal 70% al 98%</text>
<rect x="302" y="210" width="196" height="56" rx="10" class="dg-node"/>
<text x="400" y="234" text-anchor="middle" class="dg-label">CNN</text>
<text x="400" y="250" text-anchor="middle" class="dg-sublabel">pattern locali appresi dai dati</text>
<rect x="548" y="210" width="204" height="56" rx="10" class="dg-node"/>
<text x="650" y="234" text-anchor="middle" class="dg-label">Terza dimensione</text>
<text x="650" y="250" text-anchor="middle" class="dg-sublabel">stereo, movimento, vista singola</text>
<rect x="295" y="310" width="210" height="56" rx="10" class="dg-node"/>
<text x="400" y="334" text-anchor="middle" class="dg-label">Rilevamento di oggetti</text>
<text x="400" y="350" text-anchor="middle" class="dg-sublabel">bounding box, objectness</text>
<rect x="300" y="400" width="200" height="56" rx="10" class="dg-node-accent"/>
<text x="400" y="424" text-anchor="middle" class="dg-label">Applicazioni</text>
<text x="400" y="440" text-anchor="middle" class="dg-sublabel">guida autonoma, captioning, GAN</text>
</svg>
<figcaption>Mappa del capitolo 25 — dal problema inverso della proiezione ai due compiti di riconoscimento e ricostruzione, fino alle applicazioni</figcaption>
</figure>

## Dalla scena ai pixel: geometria e luce

Tutto parte dal modello piu' semplice di fotocamera: una scatola con un foro (lo stenoscopio, o pinhole camera). Ogni punto della scena proietta un raggio attraverso il foro fino al piano immagine, e la geometria che ne risulta e' la proiezione prospettica: le coordinate immagine sono proporzionali a quelle della scena divise per la profondita' Z. Da qui discendono gli effetti che conosciamo dalle fotografie: gli oggetti lontani appaiono piccoli, le rette parallele convergono verso un punto di fuga, l'immagine e' invertita. Quando la profondita' degli oggetti varia poco rispetto alla distanza, si puo' usare un modello semplificato, la proiezione ortografica scalata, in cui il fattore prospettico diventa una costante.

Il foro piccolo pero' raccoglie poca luce: le fotocamere reali e gli occhi dei vertebrati usano lenti, che concentrano molta piu' luce su ogni punto del piano immagine al prezzo di una profondita' di campo limitata — solo gli oggetti entro un certo intervallo di distanze risultano a fuoco.

La luminosita' di un pixel dipende poi da come le superfici riflettono la luce. La maggior parte delle superfici e' diffusa (riflette in tutte le direzioni, come tessuti e pietra), altre sono speculari (riflettono in un lobo stretto, come metalli e superfici bagnate). Per una superficie diffusa illuminata da una sorgente lontana vale la legge del coseno di Lambert: l'intensita' e' proporzionale all'albedo e al coseno dell'angolo tra luce e normale alla superficie. E' per questo che l'ombreggiatura e' un indizio di forma: pixel chiari suggeriscono superfici rivolte verso la luce, pixel scuri superfici illuminate di taglio. Il colore, infine, si riduce quasi sempre a tre numeri per pixel (RGB), perche' il principio della tricromia dice che tre componenti primari bastano a riprodurre qualsiasi colore percepito da un osservatore umano.

## Bordi, texture, movimento: le caratteristiche di basso livello

Un'immagine da dodici milioni di pixel contiene troppa informazione grezza. Il primo passo e' estrarre rappresentazioni compatte, e il capitolo ne individua quattro particolarmente generali: bordi, texture, flusso ottico e regioni.

I bordi sono curve nel piano immagine dove la luminosita' cambia bruscamente. Possono nascere da una discontinuita' di profondita', da un cambio di orientamento della superficie, da un cambio di riflettanza o da un'ombra — e il rilevatore di bordi non sa distinguere tra queste cause. L'algoritmo classico calcola il gradiente dell'immagine dopo averla lisciata con un filtro gaussiano (le due operazioni si combinano in una sola convoluzione) e marca come bordi i punti in cui il modulo del gradiente e' un massimo locale sopra una soglia. Lo smoothing serve a eliminare i picchi spuri dovuti al rumore, che altrimenti verrebbero scambiati per bordi veri.

La texture descrive un pattern che si ripete su un'area — le finestre di un palazzo, i ciottoli di una spiaggia, le macchie di un leopardo. Una rappresentazione tipica e' un istogramma degli orientamenti dei gradienti in un'area: robusto ai cambi di illuminazione, sensibile alle rotazioni. Serve sia a riconoscere oggetti (zebra e cavallo hanno forma simile ma texture diverse) sia a mettere in corrispondenza aree di immagini diverse.

Il flusso ottico e' il movimento apparente dei pixel tra un fotogramma e il successivo di un video. Si misura cercando, per ogni blocco di pixel, il blocco piu' simile nel fotogramma seguente (per esempio minimizzando la somma dei quadrati delle differenze). Codifica informazione preziosa: gli oggetti vicini si muovono apparentemente piu' in fretta di quelli lontani, e le parti in movimento di una scena si distinguono da quelle ferme.

La segmentazione, infine, raggruppa i pixel in regioni coerenti per luminosita', colore e texture. Si puo' affrontare come classificazione dei confini appresa da esempi annotati da umani, oppure come partizionamento di un grafo di pixel simili. Nessun metodo basato solo su proprieta' locali trova i confini "giusti" degli oggetti: per questo una strategia diffusa e' la sovrasegmentazione in superpixel, che riduce la complessita' senza perdere confini reali.

## Classificare immagini: perche' le CNN funzionano

Per decidere che cosa raffigura un'immagine, i sistemi moderni usano l'aspetto — colore e texture — e devono essere robusti a variazioni enormi: illuminazione, scorcio, punto di vista, occlusione, deformazione. Un gatto ripreso da angolazioni diverse produce immagini radicalmente differenti, e nessuna regola scritta a mano copre tutti i casi. La risposta moderna e' apprendere classificatori da grandi quantita' di dati con reti neurali convoluzionali (CNN).

Il capitolo spiega perche' questa architettura e' adatta alle immagini partendo dal data set MNIST di cifre scritte a mano. Il valore di un singolo pixel dice poco, perche' la stessa cifra puo' essere traslata, ruotata, ingrandita; sono i pattern locali a essere informativi — cerchi, incroci, estremita' di linee — insieme alle loro relazioni spaziali. Una convoluzione seguita da una ReLU e' esattamente un rilevatore di pattern locali: kernel diversi trovano pattern diversi, e impilando strati la rete costruisce pattern di pattern, su finestre sempre piu' ampie. Il punto decisivo e' che questi rilevatori vengono appresi dai dati, non progettati da un ricercatore: e' la garanzia che le caratteristiche siano davvero utili al compito.

La svolta storica e' misurabile su ImageNet, il data set con oltre 14 milioni di immagini che ha alimentato una competizione annuale: nel 2010 nessun sistema superava il 70% di accuratezza sulle 5 migliori ipotesi; con l'arrivo delle CNN nel 2012 e i raffinamenti successivi si e' arrivati al 98%, oltre le prestazioni umane. Tra le tecniche pratiche che aiutano c'e' l'aumento del data set: copiare gli esempi di addestramento applicando piccole traslazioni, rotazioni o variazioni di tonalita' per simulare la varieta' del mondo reale.

## Trovare gli oggetti: dalle finestre alle bounding box

Il classificatore dice che cosa c'e' nell'immagine; il rilevatore di oggetti dice anche dove, assegnando una bounding box a ogni oggetto trovato. L'idea di base e' far scorrere una finestra sull'immagine e classificare il contenuto di ogni finestra, ma le finestre possibili sono troppe: in un'immagine n per n sono dell'ordine di n alla quarta. Serve un filtro a monte, un punteggio di objectness che stimi quanto e' probabile che un box contenga un oggetto qualsiasi.

L'architettura Faster RCNN, descritta nel capitolo come riferimento, organizza il lavoro in una pipeline: una rete propone regioni candidate valutando box di ancoraggio di varie dimensioni e proporzioni centrati su una griglia di punti; le regioni di interesse vengono standardizzate con il ROI pooling e passate a un classificatore; la soppressione dei non massimi elimina i box quasi duplicati che si sovrappongono sullo stesso oggetto; la regressione della bounding box raffina la posizione finale. La valutazione di questi sistemi richiede test set annotati da umani e metriche che bilancino recall (trovare tutti gli oggetti presenti) e precisione (non inventarne di inesistenti).

## Recuperare la terza dimensione

Le immagini sono 2D ma il mondo e' 3D, e il capitolo mostra quanti indizi permettono di recuperare la profondita'. Con due viste della stessa scena si puo' triangolare: e' la stereoscopia binoculare, in cui la disparita' — lo spostamento orizzontale di un punto tra immagine sinistra e destra — e' inversamente legata alla profondita'. La geometria dice che la disparita' cresce con la baseline (la distanza tra le due fotocamere) e decresce con il quadrato della distanza: per l'uomo, con una baseline di circa 6 cm, questo si traduce nella capacita' di distinguere differenze di profondita' di frazioni di millimetro a 30 cm.

Una fotocamera in movimento produce lo stesso tipo di informazione: il flusso ottico generato dal moto rivela la struttura della scena a meno di un fattore di scala, e il rapporto tra profondita' e velocita' di avvicinamento — il tempo al contatto — e' direttamente stimabile, tanto che molti animali lo usano per atterrare o evitare collisioni.

Anche una singola immagine e' sorprendentemente ricca: l'occlusione ordina gli oggetti in profondita', il gradiente di texture rivela l'inclinazione delle superfici (i ciottoli lontani appaiono piu' piccoli), l'ombreggiatura suggerisce la forma, la posizione dei piedi di un pedone rispetto all'orizzonte ne stima la distanza. I metodi moderni non ragionano esplicitamente su questa matematica: addestrano reti a predire mappe di profondita' — la profondita' di ogni pixel — direttamente dalle immagini, e funzionano bene perche' molte scene hanno struttura regolare.

## Che cosa ci si fa: dalle persone alla guida autonoma

L'ultima parte del capitolo passa in rassegna gli usi. Capire che cosa fanno le persone: stimare le articolazioni del corpo e ricostruirne la posa 3D da una singola immagine funziona molto bene; classificare le azioni e' piu' difficile, perche' la stessa azione appare in modi diversissimi, azioni diverse si somigliano, e il nome giusto dipende dalla scala temporale (un fotogramma mostra "aprire il frigorifero", il video lungo mostra "prepararsi uno spuntino").

Collegare immagini e parole: dai sistemi di tagging al captioning (una CNN per rappresentare l'immagine accoppiata a un modello sequenziale per generare la frase) fino al visual question answering, che smaschera i sistemi che "indovinano" dalle statistiche del data set invece di guardare davvero l'immagine.

Ricostruzione da piu' viste: gli algoritmi structure-from-motion ricostruiscono modelli 3D di interi edifici o citta' da collezioni di fotografie, con applicazioni dalla realta' virtuale al monitoraggio dei cantieri con droni.

Generazione e trasformazione di immagini: reti addestrate su coppie (foto aerea, mappa stradale) imparano a tradurre un dominio nell'altro; con il vincolo di coerenza del ciclo si puo' fare anche senza coppie (cavalli in zebre); il trasferimento di stile combina il contenuto di una foto con lo stile di un dipinto sfruttando il fatto che nei primi strati di una CNN profonda vive lo stile e negli ultimi il contenuto. Le GAN producono immagini fotorealistiche, con usi legittimi (data set sintetici che proteggono la privacy dei pazienti in radiologia) e problematici (i deepfake).

Infine il controllo del movimento: un'auto a guida autonoma deve mantenere la corsia, tenere la distanza di sicurezza, evitare ostacoli e rispettare la segnaletica, costruendo un modello del mondo a partire da fotocamere spesso integrate con lidar, radar e microfoni. I robot mobili scompongono la navigazione in costruzione della mappa (SLAM) e pianificazione del percorso.

## Idee chiave

- La percezione visiva sembra facile solo perche' il cervello la svolge senza sforzo apparente: in realta' richiede un'elaborazione sofisticata, e il suo scopo e' estrarre l'informazione che serve ad agire — manipolare, navigare, riconoscere.
- La direzione grafica (da descrizione 3D a immagine) e' geometria ben compresa; la direzione visione (da immagine a descrizione 3D) e' il problema inverso, molto piu' difficile perche' la proiezione distrugge informazione.
- Bordi, texture, flusso ottico e regioni sono le rappresentazioni di basso e medio livello che forniscono indizi sui confini degli oggetti e sulle corrispondenze tra immagini.
- Le CNN classificano immagini con grande accuratezza perche' apprendono dai dati gerarchie di rilevatori di pattern locali, invece di usare caratteristiche progettate a mano; resta difficile predire quando falliranno, perche' i dati di test possono differire da quelli di addestramento in modi rilevanti.
- Un rilevatore di oggetti si costruisce sopra un classificatore: una rete propone box con alto punteggio di objectness, un'altra li classifica, e passi come la soppressione dei non massimi e la regressione della bounding box ripuliscono l'output.
- Con piu' viste di una scena si ricostruisce la struttura 3D per triangolazione; in molti casi la geometria e' ricavabile anche da una vista sola, grazie a indizi come occlusione, texture, ombreggiatura e oggetti familiari.
- I metodi di visione, pur imperfetti, sono abbastanza accurati da sostenere un'enorme varieta' di applicazioni pratiche, dal captioning alla guida autonoma alla generazione di immagini.

## Perche conta oggi

Le idee di questo capitolo sono il ponte tra la visione classica e i sistemi multimodali attuali. Le gerarchie di caratteristiche apprese dalle CNN sono l'antenato diretto degli [embedding](../kb/concetti/embedding.md) visivi con cui gli [LLM](../kb/concetti/llm.md) multimodali oggi "vedono": un'immagine viene trasformata in vettori che il modello linguistico tratta come token, e il captioning e il visual question answering descritti nel capitolo — allora fragili e propensi a indovinare — sono diventati capacita' standard dei modelli di frontiera. La lezione di ImageNet, per cui data set grandi e competizioni pubbliche accelerano il progresso, e' la stessa logica che governa gli attuali [benchmark di valutazione](../kb/concetti/evaluation-benchmark.md); e il monito del capitolo sulla distanza tra dati di addestramento e dati di test resta il cuore del problema di robustezza anche per i modelli di oggi.

Il secondo filo che porta al presente e' la ricostruzione: mappe di profondita', structure-from-motion, SLAM e stima della posa sono i mattoni con cui un [agente](../kb/concetti/agent.md) incarnato — un robot, un'auto autonoma, un drone — costruisce e mantiene una rappresentazione interna dell'ambiente in cui deve agire. E' la stessa esigenza che motiva la ricerca sui [world models](../kb/concetti/world-models.md): passare da pixel a un modello del mondo abbastanza affidabile da poterci pianificare sopra. Il capitolo mostra che questo passaggio non e' mai gratuito, e che ogni sistema che "vede" sta risolvendo, in qualche forma, il problema inverso della proiezione.

## Riferimenti
- Stuart J. Russell, Peter Norvig — *Intelligenza Artificiale: Un Approccio Moderno*, 4a edizione italiana, Pearson Italia, Vol. 2 (2022), Capitolo 25, pp. 239-282.
