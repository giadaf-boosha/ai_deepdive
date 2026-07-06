---
titolo: Ricerca in ambienti complessi
capitolo: 4
parte: 2
volume: 1
pagine: "115-150"
concetti: [agent, world-models, tool-use]
created: 2026-07-06
last_updated: 2026-07-06
---
# Ricerca in ambienti complessi

Il capitolo 3 di Russell e Norvig lavora sotto ipotesi comode: ambiente completamente osservabile, deterministico, statico e noto in anticipo. In quelle condizioni risolvere un problema significa calcolare una sequenza di azioni e poi eseguirla a occhi chiusi. Il capitolo 4 toglie queste stampelle una alla volta e si chiede: cosa succede quando all'agente interessa solo lo stato finale e non il cammino? Quando le variabili sono continue anziche' discrete? Quando le azioni hanno esiti imprevedibili, quando i sensori non bastano a sapere dove ci si trova, quando l'ambiente stesso e' sconosciuto e va esplorato?

La domanda di fondo e' come un agente possa comportarsi in modo razionale quando il mondo non collabora. Le risposte formano un repertorio che va dalla ricerca locale (algoritmi leggeri che tengono in memoria un solo stato o poco piu') ai piani condizionali con rami "se-allora", dagli stati-credenza che rappresentano l'incertezza come insieme di mondi possibili, fino agli agenti online che alternano azione e calcolo imparando strada facendo.

Conta perche' quasi nessun problema reale rispetta le ipotesi del capitolo 3. Un robot ha attuatori che slittano e sensori rumorosi; un sistema di scheduling industriale cerca una configurazione buona, non un percorso; un agente software opera in ambienti che scopre solo interagendovi. Gli strumenti concettuali introdotti qui — funzione obiettivo, piano condizionale, stato-credenza, ricerca online — sono il vocabolario minimo per ragionare su tutti questi casi.

<figure class="diagram">
<svg viewBox="0 0 760 380" role="img" aria-label="Mappa concettuale del capitolo 4: dagli ambienti complessi partono cinque risposte — ricerca locale con hill climbing, simulated annealing e algoritmi evolutivi, ottimizzazione negli spazi continui, piani condizionali, stati-credenza e ricerca online che con LRTA* porta all'apprendimento">
<defs><marker id="arr-c04" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" class="dg-arrow"/></marker></defs>
<line x1="270" y1="68" x2="74" y2="112" class="dg-edge" marker-end="url(#arr-c04)"/>
<line x1="330" y1="68" x2="220" y2="112" class="dg-edge" marker-end="url(#arr-c04)"/>
<text x="275" y="90" text-anchor="middle" class="dg-edge-label">variabili continue</text>
<line x1="390" y1="68" x2="374" y2="112" class="dg-edge" marker-end="url(#arr-c04)"/>
<text x="382" y="102" text-anchor="middle" class="dg-edge-label">esiti imprevedibili</text>
<line x1="450" y1="68" x2="521" y2="112" class="dg-edge" marker-end="url(#arr-c04)"/>
<text x="478" y="90" text-anchor="middle" class="dg-edge-label">sensori insufficienti</text>
<line x1="505" y1="68" x2="675" y2="112" class="dg-edge-primary" marker-end="url(#arr-c04)"/>
<text x="622" y="96" text-anchor="middle" class="dg-edge-label">ambiente sconosciuto</text>
<line x1="55" y1="168" x2="103" y2="212" class="dg-edge" marker-end="url(#arr-c04)"/>
<line x1="95" y1="168" x2="295" y2="212" class="dg-edge" marker-end="url(#arr-c04)"/>
<line x1="125" y1="168" x2="492" y2="212" class="dg-edge" marker-end="url(#arr-c04)"/>
<line x1="675" y1="168" x2="678" y2="212" class="dg-edge-primary" marker-end="url(#arr-c04)"/>
<text x="676" y="196" text-anchor="middle" class="dg-edge-label">aggiunge memoria</text>
<line x1="678" y1="268" x2="645" y2="310" class="dg-edge-primary" marker-end="url(#arr-c04)"/>
<rect x="230" y="12" width="300" height="56" rx="10" class="dg-node-primary"/>
<text x="380" y="36" text-anchor="middle" class="dg-label">Ambienti complessi</text>
<text x="380" y="52" text-anchor="middle" class="dg-sublabel">il mondo non collabora</text>
<rect x="8" y="112" width="132" height="56" rx="10" class="dg-node"/>
<text x="74" y="136" text-anchor="middle" class="dg-label">Ricerca locale</text>
<text x="74" y="152" text-anchor="middle" class="dg-sublabel">solo lo stato finale</text>
<rect x="152" y="112" width="136" height="56" rx="10" class="dg-node"/>
<text x="220" y="136" text-anchor="middle" class="dg-label">Spazi continui</text>
<text x="220" y="152" text-anchor="middle" class="dg-sublabel">discesa del gradiente</text>
<rect x="300" y="112" width="148" height="56" rx="10" class="dg-node"/>
<text x="374" y="136" text-anchor="middle" class="dg-label">Piano condizionale</text>
<text x="374" y="152" text-anchor="middle" class="dg-sublabel">rami if-then-else</text>
<rect x="456" y="112" width="130" height="56" rx="10" class="dg-node"/>
<text x="521" y="136" text-anchor="middle" class="dg-label">Stato-credenza</text>
<text x="521" y="152" text-anchor="middle" class="dg-sublabel">mondi possibili</text>
<rect x="598" y="112" width="154" height="56" rx="10" class="dg-node-primary"/>
<text x="675" y="136" text-anchor="middle" class="dg-label">Ricerca online</text>
<text x="675" y="152" text-anchor="middle" class="dg-sublabel">alterna calcolo e azione</text>
<rect x="8" y="212" width="190" height="56" rx="10" class="dg-node"/>
<text x="103" y="236" text-anchor="middle" class="dg-label">Hill climbing</text>
<text x="103" y="252" text-anchor="middle" class="dg-sublabel">massimi locali, creste, plateau</text>
<rect x="210" y="212" width="170" height="56" rx="10" class="dg-node"/>
<text x="295" y="236" text-anchor="middle" class="dg-label">Simulated annealing</text>
<text x="295" y="252" text-anchor="middle" class="dg-sublabel">accetta mosse peggiorative</text>
<rect x="392" y="212" width="200" height="56" rx="10" class="dg-node"/>
<text x="492" y="236" text-anchor="middle" class="dg-label">Algoritmi evolutivi</text>
<text x="492" y="252" text-anchor="middle" class="dg-sublabel">popolazione, crossover, mutazione</text>
<rect x="604" y="212" width="148" height="56" rx="10" class="dg-node-primary"/>
<text x="678" y="236" text-anchor="middle" class="dg-label">LRTA*</text>
<text x="678" y="252" text-anchor="middle" class="dg-sublabel">impara dall'esperienza</text>
<rect x="524" y="310" width="228" height="56" rx="10" class="dg-node-accent"/>
<text x="638" y="334" text-anchor="middle" class="dg-label">Apprendimento</text>
<text x="638" y="350" text-anchor="middle" class="dg-sublabel">ponte verso il reinforcement learning</text>
</svg>
<figcaption>Mappa del capitolo 4 — cinque risposte agli ambienti che non collaborano, dalla ricerca locale alla ricerca online che apre all'apprendimento</figcaption>
</figure>

## Quando conta la destinazione, non il viaggio

In molti problemi la soluzione e' uno stato, non un cammino: nel rompicapo delle 8 regine interessa la configurazione finale della scacchiera, non la sequenza di mosse per costruirla. Lo stesso vale per il layout di circuiti integrati, il job-shop scheduling, la gestione di portafogli. Qui entra la ricerca locale: si parte da uno stato e ci si sposta tra stati vicini senza tenere traccia del percorso. Il prezzo e' la perdita di sistematicita' (nessuna garanzia di esplorare tutto lo spazio), il guadagno e' una memoria minima e la capacita' di lavorare in spazi enormi o infiniti.

L'immagine guida e' quella di un paesaggio dello spazio degli stati in cui l'altezza di ogni punto e' il valore della funzione obiettivo. L'algoritmo hill climbing sale sempre verso il vicino migliore, come uno scalatore nella nebbia che tasta solo il terreno immediato. Funziona spesso e in fretta, ma resta intrappolato da tre nemici: i massimi locali (picchi inferiori a quello globale), le creste (sequenze di massimi locali difficili da percorrere) e i plateau (zone piatte in cui nessuna mossa migliora nulla). Sulle 8 regine la versione base si blocca l'86% delle volte; concedere qualche mossa laterale sui plateau porta il tasso di successo al 94%.

Le varianti attaccano il problema da angoli diversi. L'hill climbing stocastico sceglie a caso tra le mosse in salita; quello con riavvio casuale rilancia la ricerca da punti iniziali diversi finche' non trova un obiettivo, ed e' completo con probabilita' 1. Il simulated annealing, ispirato alla tempra dei metalli, accetta anche mosse peggiorative con una probabilita' che decresce con l'entita' del peggioramento e con una "temperatura" che cala nel tempo: all'inizio si esplora in modo turbolento, poi ci si assesta. Se il raffreddamento e' abbastanza lento, la probabilita' di finire su un massimo globale tende a 1. La ricerca local beam mantiene k stati in parallelo e concentra le risorse dove si vedono progressi: non sono k ricerche indipendenti, perche' l'informazione passa da un thread all'altro.

Gli algoritmi evolutivi portano questa idea all'estremo con la metafora della selezione naturale: una popolazione di stati, una funzione di fitness, genitori che si ricombinano tramite crossover e figli soggetti a mutazione casuale. Il crossover paga quando esistono "blocchi" di soluzione che hanno senso da soli e possono essere ricombinati; se la rappresentazione e' scelta male, il vantaggio svanisce. Gli algoritmi genetici trovano applicazione in problemi strutturati complessi, dalla configurazione di circuiti fino, in tempi recenti, alla ricerca di architetture per reti neurali deep.

## Ottimizzare nel continuo

Quando le variabili sono numeri reali — per esempio le coordinate di tre aeroporti da posizionare in modo da minimizzare le distanze dalle citta' — il fattore di ramificazione diventa infinito e gli algoritmi discreti non si applicano direttamente. Una prima via e' discretizzare: sovrapporre una griglia con passo delta e muoversi tra i punti della griglia, oppure campionare successori casuali e misurare il progresso con il gradiente empirico.

La via piu' potente sfrutta il calcolo differenziale: il gradiente della funzione obiettivo indica la direzione di massima pendenza, e l'aggiornamento iterativo dello stato lungo il gradiente (con una dimensione del passo da calibrare: troppo piccola e servono troppi passi, troppo grande e si supera il massimo) e' l'antenato diretto delle tecniche con cui oggi si addestrano le reti neurali. Il metodo Newton-Raphson usa anche le derivate seconde, raccolte nella matrice Hessiana, per convergere piu' in fretta, al costo di calcoli che crescono con il quadrato delle dimensioni. Anche nel continuo massimi locali, creste e plateau restano un problema, e riavvii casuali e simulated annealing restano rimedi utili. Chiude il quadro l'ottimizzazione vincolata: quando i vincoli sono disuguaglianze lineari e l'obiettivo e' lineare si parla di programmazione lineare, caso speciale della piu' generale ottimizzazione convessa, risolvibile in tempo polinomiale anche con migliaia di variabili.

## Pianificare quando le azioni tradiscono

Se le azioni hanno esiti multipli possibili, una sequenza fissa non basta piu'. Il libro usa un aspirapolvere "erratico": l'azione di aspirazione a volte pulisce anche la casella adiacente, a volte sporca un tappeto pulito. La generalizzazione formale sostituisce la funzione che restituisce un singolo stato risultante con una funzione che restituisce un insieme di stati possibili. La soluzione diventa un piano condizionale: una struttura con rami if-then-else che dice cosa fare a seconda di cio' che l'agente osservera' durante l'esecuzione. E' la stessa logica per cui si guida guardando la strada invece di memorizzare in anticipo ogni sterzata.

Lo strumento per trovare questi piani e' l'albero di ricerca AND-OR. Nei nodi OR l'agente sceglie quale azione compiere; nei nodi AND e' l'ambiente a "scegliere" l'esito, e il piano deve coprire ogni ramo. Una soluzione e' un sottoalbero con un obiettivo in ogni foglia, una sola azione per ogni nodo OR e tutti i rami coperti in ogni nodo AND. L'algoritmo ricorsivo che esplora questi grafi taglia i cicli: se lo stato corrente coincide con uno gia' presente sul cammino dalla radice, quel ramo fallisce, il che garantisce la terminazione negli spazi finiti.

C'e' pero' un caso interessante: il mondo "scivoloso" in cui i movimenti a volte falliscono lasciando l'agente fermo. Nessun piano aciclico funziona, ma esiste una soluzione ciclica: riprovare l'azione finche' non riesce. Vale come soluzione se ogni fallimento e' davvero indipendente dal precedente; se invece il non determinismo nasconde una causa persistente non osservata (una cinghia di trasmissione rotta), insistere non serve, e conviene riformulare il problema come parzialmente osservabile.

## Agire senza vedere: gli stati-credenza

Quando i sensori non determinano lo stato esatto, l'agente ragiona su uno stato-credenza: l'insieme degli stati fisici in cui potrebbe trovarsi. Il caso estremo e' il problema senza sensori (o conformante), in cui le percezioni non danno alcuna informazione. Sorprendentemente e' spesso risolvibile: nell'aspirapolvere deterministico a 8 stati, la sequenza giusta di azioni "forza" il mondo verso lo stato obiettivo da qualunque punto di partenza, senza mai osservare nulla. E a volte un piano senza sensori e' preferibile anche quando i sensori ci sarebbero: un antibiotico ad ampio spettro evita i costi e i rischi dell'attesa delle analisi.

Il trucco concettuale e' elegante: si trasforma il problema fisico in un problema di ricerca nello spazio degli stati-credenza, che e' completamente osservabile per definizione, perche' l'agente conosce sempre cio' che crede. Su questo spazio girano gli algoritmi classici del capitolo 3, con potature specifiche: se uno stato-credenza risolvibile e' sottoinsieme di un altro, il soprainsieme e' superfluo. Il limite e' l'esplosione combinatoria (con N stati fisici gli stati-credenza sono 2 elevato a N), mitigabile con rappresentazioni compatte o con la ricerca incrementale che costruisce una soluzione valida stato per stato.

Con osservazioni parziali il modello di transizione tra stati-credenza si scompone in tre fasi: predizione (dove porta l'azione), enumerazione delle percezioni possibili, aggiornamento (quali stati sono coerenti con cio' che si e' percepito). Il ciclo predizione-aggiornamento e' il cuore del mantenimento dello stato-credenza durante l'esecuzione, noto anche come monitoraggio, filtro o stima dello stato. L'esempio canonico e' la localizzazione: un robot con sensori affidabili ma movimento erratico, piazzato in un labirinto ignoto della propria posizione, restringe l'insieme delle posizioni compatibili a ogni nuova percezione, spesso convergendo in pochi passi a un punto singolo. Le azioni non deterministiche allargano lo stato-credenza; le percezioni lo restringono.

## Imparare esplorando: la ricerca online

Tutti gli approcci precedenti sono offline: prima si calcola la soluzione completa, poi la si esegue. La ricerca online alterna invece calcolo e azione: l'agente esegue una mossa, osserva il risultato, decide la successiva. E' l'unica opzione in ambienti sconosciuti (il problema classico della costruzione di mappe) e conviene anche in ambienti dinamici o fortemente non deterministici, perche' concentra il calcolo sulle contingenze che si verificano davvero anziche' su tutte quelle possibili.

Le prestazioni si misurano con il rapporto di competitivita': il costo del cammino effettivamente percorso rispetto al cammino ottimo che si sarebbe seguito conoscendo l'ambiente. Nessun algoritmo puo' garantire un rapporto limitato in generale: i vicoli ciechi e le azioni irreversibili possono intrappolare qualsiasi esploratore, come mostra l'argomentazione dell'avversario che costruisce il labirinto apposta contro l'agente. Ci si limita quindi agli spazi esplorabili in modo sicuro, dove da ogni stato raggiungibile si puo' sempre arrivare a un obiettivo.

Un agente online deve espandere solo nodi che occupa fisicamente, il che rende naturale la ricerca in profondita' con backtracking fisico: si torna sui propri passi nel mondo reale, e serve quindi che le azioni siano reversibili. Il random walk e' completo negli spazi finiti sicuri ma puo' impiegare un numero esponenziale di passi. La mossa vincente e' aggiungere memoria: LRTA* (learning real-time A*) mantiene per ogni stato visitato una stima aggiornabile del costo verso l'obiettivo e la corregge man mano che l'esperienza smentisce l'euristica iniziale, "riempiendo" cosi' i minimi locali fino a uscirne. Il suo ottimismo in condizioni di incertezza — assumere che le azioni mai provate portino al meglio — spinge l'agente a esplorare cammini nuovi. Piu' in generale, la ricerca online e' una palestra di apprendimento: l'agente impara la mappa dell'ambiente memorizzando gli esiti delle azioni e affina le stime di valore degli stati, un ponte diretto verso il reinforcement learning trattato piu' avanti nel libro.

## Idee chiave

- La ricerca locale (hill climbing e varianti) tiene in memoria pochissimi stati e affronta problemi di ottimizzazione in cui conta lo stato finale, non il cammino; il suo tallone d'Achille sono massimi locali, creste e plateau.
- Il simulated annealing accetta mosse peggiorative con probabilita' decrescente nel tempo e, con un raffreddamento adeguato, converge verso l'ottimo globale.
- Gli algoritmi evolutivi sono ricerca beam stocastica arricchita da mutazione e crossover su una popolazione di stati; funzionano bene quando la rappresentazione cattura blocchi di soluzione riutilizzabili.
- Negli spazi continui si ottimizza con il gradiente (analitico o empirico), con Newton-Raphson quando le derivate seconde sono trattabili, e la programmazione lineare e l'ottimizzazione convessa offrono garanzie polinomiali sotto vincoli di forma.
- In ambienti non deterministici la soluzione e' un piano condizionale, trovato con la ricerca su alberi AND-OR; i piani ciclici del tipo "riprova finche' funziona" sono legittimi se i fallimenti sono indipendenti.
- Con osservabilita' parziale l'agente ragiona su stati-credenza; il problema fisico si riformula come problema completamente osservabile nello spazio degli stati-credenza, su cui girano gli algoritmi standard.
- Il ciclo predizione-aggiornamento mantiene lo stato-credenza durante l'esecuzione ed e' il meccanismo alla base di monitoraggio, filtri e localizzazione.
- Negli ambienti sconosciuti la ricerca online alterna azione e calcolo; agenti come LRTA* sfuggono ai minimi locali aggiornando le stime euristiche con l'esperienza, prima forma di apprendimento incontrata nel libro.

## Perche conta oggi

Questo capitolo e' una miniera di concetti che l'era degli LLM ha reso di nuovo centrali. Un [agente](../kb/concetti/agent.md) moderno basato su un [LLM](../kb/concetti/llm.md) opera esattamente nelle condizioni descritte qui: ambiente parzialmente osservabile (vede solo cio' che gli strumenti restituiscono), azioni non deterministiche (una chiamata API puo' fallire o dare esiti imprevisti), spazio in gran parte sconosciuto da esplorare online. Il pattern "agisci, osserva, aggiorna, decidi" degli agenti che usano il [tool use](../kb/concetti/tool-use.md) e' la ricerca online del paragrafo 4.5 con altri panni; i piani condizionali con retry sono la versione formale dei loop "prova, verifica, riprova" che ogni [agent harness](../kb/concetti/agent-harness.md) implementa; lo stato-credenza e' l'antenato concettuale dei [world models](../kb/concetti/world-models.md) con cui i sistemi attuali mantengono una rappresentazione interna dell'ambiente.

Anche il versante ottimizzazione e' tutt'altro che archeologia: la discesa del gradiente descritta per il problema degli aeroporti e' lo stesso principio che addestra ogni rete neurale, e gli algoritmi evolutivi sono tornati attuali per la ricerca di architetture deep. Persino l'ottimismo in condizioni di incertezza di LRTA* riecheggia nelle strategie di esplorazione del reinforcement learning che sta dietro a tecniche come [RLHF](../kb/concetti/rlhf.md). Leggere questo capitolo significa riconoscere che molti pattern degli agenti moderni hanno fondamenta teoriche vecchie di decenni, con proprieta' e limiti gia' studiati.

## Riferimenti

- Stuart J. Russell, Peter Norvig — *Intelligenza Artificiale: Un Approccio Moderno*, 4a edizione italiana, Pearson Italia, Vol. 1 (2021), Capitolo 4, pp. 115-150.
