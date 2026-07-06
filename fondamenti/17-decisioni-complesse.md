---
titolo: Decisioni complesse
capitolo: 17
parte: 4
volume: 1
pagine: "573-608"
concetti: [agent, world-models, rlhf]
created: 2026-07-06
last_updated: 2026-07-06
---

# Decisioni complesse

Nel capitolo precedente l'agente doveva prendere una decisione alla volta: valutava le opzioni, sceglieva quella con la massima utilita' attesa, fine della storia. Qui il gioco cambia. La domanda diventa: come si decide oggi, sapendo che domani ci sara' un'altra decisione, e dopodomani un'altra ancora, e che ogni scelta modifica le condizioni di quelle successive? E' il territorio dei problemi di decisione sequenziali, dove l'utilita' non dipende da un singolo esito ma da un'intera storia di stati e azioni.

Il capitolo aggiunge un secondo ingrediente: l'incertezza. Le azioni non producono effetti garantiti; un robot che comanda "avanti" puo' slittare di lato, un investimento puo' rendere o meno. Il formalismo che tiene insieme sequenzialita' e stocasticita' e' il processo decisionale di Markov (MDP), uno degli strumenti concettuali piu' influenti di tutta l'AI: sta alla base del reinforcement learning e, per estensione, di molte tecniche con cui oggi si addestrano e si controllano gli agenti moderni.

Il percorso e' progressivo. Prima gli MDP completamente osservabili e gli algoritmi per risolverli; poi i problemi dei banditi, dove il dilemma e' quanto esplorare l'ignoto rispetto a sfruttare cio' che gia' funziona; infine i POMDP, in cui l'agente non sa nemmeno con certezza in quale stato si trova e deve ragionare su credenze invece che su fatti.

<figure class="diagram">
<svg viewBox="0 0 760 496" role="img" aria-label="Mappa concettuale del capitolo 17: i problemi di decisione sequenziali si formalizzano come MDP, il fattore di sconto rende finite le utilita', l'equazione di Bellman porta a iterazione dei valori e delle politiche fino alla politica ottima; rami laterali per i banditi e per i POMDP con gli stati-credenza">
<defs><marker id="arr-c17" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" class="dg-arrow"/></marker></defs>
<line x1="360" y1="68" x2="360" y2="113" class="dg-edge-primary" marker-end="url(#arr-c17)"/>
<line x1="460" y1="40" x2="555" y2="40" class="dg-edge" marker-end="url(#arr-c17)"/>
<text x="508" y="32" text-anchor="middle" class="dg-edge-label">vincite ignote</text>
<line x1="178" y1="146" x2="275" y2="146" class="dg-edge" marker-end="url(#arr-c17)"/>
<text x="227" y="138" text-anchor="middle" class="dg-edge-label">utilita' finita</text>
<line x1="440" y1="146" x2="555" y2="146" class="dg-edge" marker-end="url(#arr-c17)"/>
<line x1="360" y1="174" x2="360" y2="219" class="dg-edge-primary" marker-end="url(#arr-c17)"/>
<line x1="250" y1="252" x2="225" y2="252" class="dg-edge" marker-end="url(#arr-c17)"/>
<line x1="320" y1="280" x2="288" y2="325" class="dg-edge" marker-end="url(#arr-c17)"/>
<line x1="430" y1="280" x2="492" y2="325" class="dg-edge" marker-end="url(#arr-c17)"/>
<line x1="300" y1="386" x2="343" y2="423" class="dg-edge" marker-end="url(#arr-c17)"/>
<line x1="480" y1="386" x2="418" y2="423" class="dg-edge" marker-end="url(#arr-c17)"/>
<line x1="652" y1="174" x2="652" y2="219" class="dg-edge" marker-end="url(#arr-c17)"/>
<text x="660" y="202" class="dg-edge-label">ragiona su</text>
<rect x="260" y="12" width="200" height="56" rx="10" class="dg-node"/>
<text x="360" y="36" text-anchor="middle" class="dg-label">Decisioni sequenziali</text>
<text x="360" y="52" text-anchor="middle" class="dg-sublabel">utilita' su intere storie</text>
<rect x="560" y="12" width="184" height="56" rx="10" class="dg-node"/>
<text x="652" y="36" text-anchor="middle" class="dg-label">Banditi con n braccia</text>
<text x="652" y="52" text-anchor="middle" class="dg-sublabel">esplorare vs sfruttare</text>
<rect x="8" y="118" width="170" height="56" rx="10" class="dg-node"/>
<text x="93" y="142" text-anchor="middle" class="dg-label">Fattore di sconto</text>
<text x="93" y="158" text-anchor="middle" class="dg-sublabel">gamma: il futuro pesa meno</text>
<rect x="280" y="118" width="160" height="56" rx="10" class="dg-node-primary"/>
<text x="360" y="142" text-anchor="middle" class="dg-label">MDP</text>
<text x="360" y="158" text-anchor="middle" class="dg-sublabel">transizioni e ricompense</text>
<rect x="560" y="118" width="184" height="56" rx="10" class="dg-node"/>
<text x="652" y="142" text-anchor="middle" class="dg-label">POMDP</text>
<text x="652" y="158" text-anchor="middle" class="dg-sublabel">parzialmente osservabile</text>
<rect x="40" y="224" width="185" height="56" rx="10" class="dg-node"/>
<text x="132" y="248" text-anchor="middle" class="dg-label">Funzione Q(s,a)</text>
<text x="132" y="264" text-anchor="middle" class="dg-sublabel">argmax da' la politica</text>
<rect x="250" y="224" width="220" height="56" rx="10" class="dg-node-primary"/>
<text x="360" y="248" text-anchor="middle" class="dg-label">Equazione di Bellman</text>
<text x="360" y="264" text-anchor="middle" class="dg-sublabel">ricompensa + futuro scontato</text>
<rect x="560" y="224" width="184" height="56" rx="10" class="dg-node"/>
<text x="652" y="248" text-anchor="middle" class="dg-label">Stato-credenza</text>
<text x="652" y="264" text-anchor="middle" class="dg-sublabel">distribuzione sugli stati</text>
<rect x="180" y="330" width="190" height="56" rx="10" class="dg-node"/>
<text x="275" y="354" text-anchor="middle" class="dg-label">Iterazione dei valori</text>
<text x="275" y="370" text-anchor="middle" class="dg-sublabel">convergenza per contrazione</text>
<rect x="400" y="330" width="210" height="56" rx="10" class="dg-node"/>
<text x="505" y="354" text-anchor="middle" class="dg-label">Iterazione delle politiche</text>
<text x="505" y="370" text-anchor="middle" class="dg-sublabel">valuta e migliora</text>
<rect x="290" y="428" width="180" height="56" rx="10" class="dg-node-accent"/>
<text x="380" y="452" text-anchor="middle" class="dg-label">Politica ottima</text>
<text x="380" y="468" text-anchor="middle" class="dg-sublabel">un'azione per ogni stato</text>
</svg>
<figcaption>Mappa concettuale del capitolo: dai problemi di decisione sequenziali agli MDP e all'equazione di Bellman fino alla politica ottima, con i rami dei banditi e dei POMDP.</figcaption>
</figure>

## Il mondo come processo di Markov

Un MDP e' definito da pochi elementi: un insieme di stati con uno stato iniziale, le azioni disponibili in ogni stato, un modello di transizione che assegna una probabilita' a ogni possibile esito di ogni azione, e una funzione di ricompensa che attribuisce un valore numerico a ogni transizione. L'ipotesi markoviana dice che la probabilita' di arrivare in uno stato dipende solo dallo stato corrente e dall'azione scelta, non da tutta la storia precedente: il presente riassume il passato.

Il libro usa un mondo giocattolo, una griglia 4x3 con due uscite (una buona, una cattiva) e movimenti inaffidabili: l'azione voluta riesce con probabilita' 0,8, ma nel 20% dei casi l'agente scivola di lato. In un ambiente cosi' una sequenza fissa di mosse non basta, perche' l'agente puo' ritrovarsi ovunque. La soluzione deve dire cosa fare in ogni stato raggiungibile: si chiama politica, e si indica con la lettera greca pi. Una politica ottima e' quella che massimizza l'utilita' attesa sulle possibili storie che genera. Un dettaglio istruttivo: la forma della politica ottima cambia radicalmente al variare della ricompensa dei passi intermedi. Se ogni passo costa molto, l'agente corre verso l'uscita piu' vicina anche se e' quella cattiva; se ogni passo produce una piccola ricompensa positiva, l'agente evita entrambe le uscite e vaga per sempre. Il design della ricompensa e' gia' design del comportamento.

<figure class="diagram">
<svg viewBox="0 0 760 300" role="img" aria-label="Il mondo a griglia 4x3 del capitolo 17: stati terminali +1 in (4,3) e -1 in (4,2), muro in (2,2), partenza INIZIO in (1,1); a destra il modello di transizione, con probabilita' 0,8 nella direzione voluta e 0,1 per ciascuna direzione ortogonale">
<defs><marker id="arr-c17-b" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" class="dg-arrow"/></marker></defs>
<line x1="600" y1="125" x2="600" y2="74" class="dg-edge-primary" marker-end="url(#arr-c17-b)"/>
<text x="600" y="64" text-anchor="middle" class="dg-edge-label">0,8</text>
<line x1="560" y1="156" x2="510" y2="156" class="dg-edge" marker-end="url(#arr-c17-b)"/>
<text x="535" y="148" text-anchor="middle" class="dg-edge-label">0,1</text>
<line x1="640" y1="156" x2="690" y2="156" class="dg-edge" marker-end="url(#arr-c17-b)"/>
<text x="665" y="148" text-anchor="middle" class="dg-edge-label">0,1</text>
<rect x="70" y="50" width="85" height="62" rx="4" class="dg-node"/>
<rect x="155" y="50" width="85" height="62" rx="4" class="dg-node"/>
<rect x="240" y="50" width="85" height="62" rx="4" class="dg-node"/>
<rect x="325" y="50" width="85" height="62" rx="4" class="dg-node-accent"/>
<text x="367" y="86" text-anchor="middle" class="dg-label">+1</text>
<rect x="70" y="112" width="85" height="62" rx="4" class="dg-node"/>
<rect x="155" y="112" width="85" height="62" rx="4" class="dg-node"/>
<line x1="162" y1="119" x2="233" y2="167" class="dg-edge"/>
<line x1="233" y1="119" x2="162" y2="167" class="dg-edge"/>
<rect x="240" y="112" width="85" height="62" rx="4" class="dg-node"/>
<rect x="325" y="112" width="85" height="62" rx="4" class="dg-node"/>
<text x="367" y="148" text-anchor="middle" class="dg-label">-1</text>
<rect x="70" y="174" width="85" height="62" rx="4" class="dg-node"/>
<text x="112" y="209" text-anchor="middle" class="dg-sublabel">INIZIO</text>
<rect x="155" y="174" width="85" height="62" rx="4" class="dg-node"/>
<rect x="240" y="174" width="85" height="62" rx="4" class="dg-node"/>
<rect x="325" y="174" width="85" height="62" rx="4" class="dg-node"/>
<text x="52" y="85" text-anchor="middle" class="dg-sublabel">3</text>
<text x="52" y="147" text-anchor="middle" class="dg-sublabel">2</text>
<text x="52" y="209" text-anchor="middle" class="dg-sublabel">1</text>
<text x="112" y="256" text-anchor="middle" class="dg-sublabel">1</text>
<text x="197" y="256" text-anchor="middle" class="dg-sublabel">2</text>
<text x="282" y="256" text-anchor="middle" class="dg-sublabel">3</text>
<text x="367" y="256" text-anchor="middle" class="dg-sublabel">4</text>
<text x="240" y="282" text-anchor="middle" class="dg-sublabel">(a) ambiente 4x3</text>
<rect x="560" y="125" width="80" height="62" rx="4" class="dg-node"/>
<text x="600" y="212" text-anchor="middle" class="dg-sublabel">modello di transizione</text>
<text x="600" y="282" text-anchor="middle" class="dg-sublabel">(b)</text>
</svg>
<figcaption>Il mondo 4x3: terminali +1 e -1, muro in (2,2), partenza in (1,1); l'azione voluta riesce con probabilita' 0,8, con 0,1 si scivola di lato e le altre transizioni valgono -0,04 — schema ripreso dalla figura 17.1 del cap. 17, AIMA 4a ed.</figcaption>
</figure>

Resta da definire l'utilita' di una storia infinita. La risposta standard e' lo sconto: le ricompense future vengono moltiplicate per un fattore gamma tra 0 e 1 elevato al tempo, cosi' che il futuro remoto pesi sempre meno. Lo sconto ha giustificazioni economiche (un euro oggi vale piu' di un euro domani), probabilistiche (equivale a una piccola probabilita' di terminazione a ogni passo) e matematiche: rende finita la somma di una sequenza infinita di ricompense, ed e' l'unica forma di aggregazione coerente con preferenze stazionarie nel tempo. C'e' anche un risultato elegante sul reward shaping: aggiungere alla ricompensa un termine a forma di gradiente di potenziale non cambia la politica ottima, il che consente di "aiutare" l'agente con segnali intermedi senza distorcere l'obiettivo. E' esattamente cio' che fa un addestratore di animali con i piccoli premi lungo il percorso.

## L'equazione che lega presente e futuro

Il cuore matematico del capitolo e' l'equazione di Bellman: l'utilita' di uno stato e' la ricompensa attesa per la prossima transizione piu' l'utilita' scontata dello stato in cui si finisce, assumendo che l'agente scelga sempre l'azione migliore. E' una definizione ricorsiva: il valore di un punto del mondo dipende dai valori dei suoi vicini. Con n stati si ottengono n equazioni in n incognite, e la loro soluzione unica e' proprio la funzione di utilita' della politica ottima.

Accanto all'utilita' di stato c'e' la funzione Q, che misura l'utilita' attesa di una specifica coppia stato-azione. E' una quantita' apparentemente minore ma dal futuro luminoso: conoscere Q permette di ricavare la politica ottima con un semplice argmax, senza nemmeno bisogno del modello di transizione. Chi ha sentito parlare di Q-learning nel reinforcement learning ritrova qui l'origine del nome.

Per problemi realistici la rappresentazione tabellare degli stati esplode. Il capitolo mostra come le reti di decisione dinamiche (DDN) fattorizzino lo stato in variabili — per un robot mobile: posizione, velocita', carica della batteria, stato di ricarica — ottenendo rappresentazioni esponenzialmente piu' compatte. L'esempio del Tetris rende l'idea della scala: circa 10 alla 62 stati, eppure descrivibile con una manciata di variabili.

## Tre modi per trovare la politica ottima

Il primo algoritmo e' l'iterazione dei valori: si parte da utilita' arbitrarie e si applica ripetutamente l'aggiornamento di Bellman, ricalcolando il valore di ogni stato dai valori correnti dei vicini. La garanzia di convergenza viene da un argomento di contrazione: ogni applicazione dell'aggiornamento riduce la distanza dalla soluzione vera di un fattore almeno gamma, quindi il processo converge esponenzialmente all'unico punto fisso. Un fatto pratico importante: la politica derivata dalle stime diventa spesso ottima molto prima che le stime stesse siano accurate. All'agente non serve conoscere i valori esatti, gli basta che l'ordinamento delle azioni sia giusto.

Il secondo e' l'iterazione delle politiche, che sfrutta proprio questa osservazione. Alterna due passi: valutare la politica corrente (calcolare le utilita' che produrrebbe) e migliorarla (scegliere in ogni stato l'azione migliore rispetto a quelle utilita'). La valutazione e' piu' facile della soluzione completa perche', con l'azione fissata dalla politica, le equazioni diventano lineari. L'algoritmo termina quando il passo di miglioramento non cambia piu' nulla, e a quel punto la politica e' ottima. Esistono varianti che valutano in modo approssimato o aggiornano solo sottoinsiemi di stati, fino all'iterazione asincrona, che concentra il calcolo dove serve davvero.

Il terzo approccio riformula il problema come programmazione lineare, il che dimostra che gli MDP sono risolvibili in tempo polinomiale, anche se in pratica i risolutori PL raramente battono la programmazione dinamica. Tutti e tre sono metodi offline: calcolano l'intera soluzione prima di agire. Per spazi di stati enormi si passa agli algoritmi online, che ragionano solo dallo stato corrente: alberi expectimax a profondita' limitata, campionamento nei nodi di casualita' per domare il fattore di ramificazione, e metodi Monte Carlo come UCT, che simula molte partite in avanti per stimare il valore delle mosse. E' la stessa famiglia di idee che ha reso possibile AlphaGo.

## Esplorare o sfruttare: i banditi

Immaginate una fila di slot machine, ognuna con una probabilita' di vincita fissa ma ignota. A ogni gettone dovete scegliere: la macchina che finora ha pagato meglio, o una mai provata che potrebbe essere migliore? E' il problema del bandito con n braccia, il modello formale del compromesso tra sfruttamento ed esplorazione. La struttura riaffiora ovunque: quale cura sperimentare, dove allocare un budget pubblicitario, quale variante di un prodotto testare.

Il risultato teorico centrale e' l'indice di Gittins: a ogni braccio si puo' associare un numero che dipende solo dalla storia di quel braccio, e la politica ottima consiste semplicemente nel tirare sempre il braccio con l'indice piu' alto. Il problema, in apparenza intrecciato, si scompone in valutazioni indipendenti. Gli indici pero' sono costosi da calcolare, e in pratica si usano strategie quasi ottime piu' semplici: l'euristica UCB (upper confidence bound), che sceglie il braccio con il limite superiore di confidenza piu' alto, premiando cosi' sia il valore stimato sia l'incertezza; e il campionamento di Thompson, che sceglie ogni braccio con la probabilita' che sia il migliore date le osservazioni raccolte. Entrambe garantiscono un rimpianto che cresce solo in modo logaritmico, il minimo teorico possibile.

Il capitolo distingue con cura i banditi dai problemi di selezione (dove i test non costano ricompensa reale e conta solo scegliere bene alla fine, e non esiste alcuna funzione indice) e li generalizza ai superprocessi, in cui ogni braccio e' un MDP completo: il modello formale del multitasking, con la lezione controintuitiva che risolvere ottimamente ogni singolo compito non produce la politica globalmente ottima.

## Decidere al buio: i POMDP

Fin qui l'agente sapeva sempre dove si trovava. Nei POMDP (MDP parzialmente osservabili) questa certezza cade: al posto dell'accesso diretto allo stato c'e' un modello sensoriale che fornisce osservazioni rumorose. L'agente non puo' piu' applicare una politica del tipo "nello stato s fai a", perche' non conosce s.

L'idea risolutiva e' lo stato-credenza: una distribuzione di probabilita' su tutti gli stati possibili, aggiornata a ogni azione e osservazione con un'operazione di filtraggio bayesiano. Il colpo di scena concettuale e' che la politica ottima dipende solo dallo stato-credenza, e che un POMDP equivale a un MDP osservabile nello spazio degli stati-credenza. Il prezzo e' alto: quello spazio e' continuo e ad alta dimensionalita'. Ne segue anche una proprieta' comportamentale nuova: siccome le azioni cambiano cio' che l'agente sa, oltre a dove si trova, le politiche ottime nei POMDP includono spontaneamente azioni di raccolta di informazioni. Guardare prima di attraversare non e' una regola aggiunta a mano, emerge dalla matematica.

Gli algoritmi esatti rappresentano la funzione di utilita' come massimo di una collezione di iperpiani, uno per ogni piano condizionale, ed eliminano quelli dominati; ma il numero di piani cresce in modo doppiamente esponenziale e il problema generale e' PSPACE-difficile. In pratica si usano metodi approssimati e online: ricerca in avanti su alberi di stati-credenza, particle filtering per rappresentare le credenze, e la combinazione con UCT nota come POMCP, applicabile in linea di principio a POMDP grandi e realistici. Il limite residuo, ammesso onestamente dal libro, e' l'orizzonte temporale: senza pianificazione gerarchica, le simulazioni casuali non arrivano a compiti che richiedono milioni di azioni elementari.

## Idee chiave

- Un problema di decisione sequenziale in ambiente stocastico si formalizza come MDP: stati, azioni, modello di transizione probabilistico e funzione di ricompensa.
- La soluzione di un MDP non e' un piano ma una politica: una mappa da ogni stato all'azione da eseguire, robusta per costruzione agli esiti imprevisti.
- Lo sconto esponenziale delle ricompense rende trattabili gli orizzonti infiniti ed e' l'unica aggregazione coerente con preferenze stazionarie.
- L'equazione di Bellman lega il valore di uno stato a quello dei vicini; iterazione dei valori e iterazione delle politiche la risolvono con garanzie di convergenza, e la politica diventa spesso ottima ben prima che i valori siano precisi.
- La forma della funzione di ricompensa determina il comportamento: il teorema dello shaping dice quali modifiche sono innocue e quali no.
- Nei problemi dei banditi il nodo e' bilanciare esplorazione e sfruttamento; l'indice di Gittins da' la soluzione ottima, UCB e Thompson sampling quella pratica con rimpianto logaritmico.
- Nei POMDP l'agente ragiona su stati-credenza, distribuzioni di probabilita' sugli stati possibili; un POMDP e' un MDP sullo spazio continuo delle credenze.
- Il valore dell'informazione entra nella struttura stessa del problema: le politiche ottime dei POMDP includono azioni fatte apposta per ridurre l'incertezza.

## Perche conta oggi

Questo capitolo e' la grammatica formale con cui oggi si descrive qualsiasi [agent](../kb/concetti/agent.md) che opera in piu' passi: stato, azione, osservazione, ricompensa, politica. Quando un agente basato su [llm](../kb/concetti/llm.md) pianifica una sequenza di chiamate a strumenti tramite [tool-use](../kb/concetti/tool-use.md), sta di fatto navigando un POMDP: non osserva mai lo stato completo del mondo (il contenuto vero di un filesystem, l'esito reale di un'API), mantiene una credenza implicita e compie azioni di raccolta di informazioni — leggere prima di scrivere, verificare prima di procedere — esattamente come prescrive la teoria. Anche il ruolo del modello di transizione riecheggia nella ricerca attuale sui [world-models](../kb/concetti/world-models.md): un agente che sa prevedere le conseguenze delle proprie azioni puo' pianificare invece di limitarsi a reagire.

Il legame piu' diretto e' con l'addestramento. Il [rlhf](../kb/concetti/rlhf.md) e le tecniche successive trattano la generazione di testo come un MDP in cui la politica e' il modello stesso e la ricompensa viene da un modello di preferenze: le trappole discusse nel capitolo — ricompense mal disegnate che producono comportamenti degeneri, l'importanza dello shaping — sono gli stessi problemi di reward hacking che affliggono l'allineamento dei modelli. E il dilemma dei banditi vive una seconda vita nei sistemi in produzione, dall'A/B testing con Thompson sampling alla scelta di quale modello o prompt servire a ciascun utente dentro un [agent-harness](../kb/concetti/agent-harness.md).

## Riferimenti

- Stuart J. Russell, Peter Norvig — *Intelligenza Artificiale: Un Approccio Moderno*, 4a edizione italiana, Pearson Italia, Vol. 1 (2021), Capitolo 17, pp. 573-608.
