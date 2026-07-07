---
titolo: Ricerca con avversari e giochi
capitolo: 5
parte: 2
concetti: [agent, multi-agent-orchestration, world-models, evaluation-benchmark]
created: 2026-07-06
last_updated: 2026-07-06
---

# Ricerca con avversari e giochi

Fin qui gli agenti hanno cercato soluzioni in ambienti che, al massimo, erano ostili per caso: labirinti, mappe, puzzle. Questo capitolo cambia le regole e introduce gli ambienti competitivi, dove esiste almeno un altro agente con obiettivi opposti ai nostri. La domanda diventa: come si pianifica quando qualcuno pianifica attivamente contro di noi? Non basta modellare l'avversario come rumore, come faremmo con la pioggia: la pioggia non vuole batterci, un avversario si.

Il banco di prova storico sono i giochi da tavolo: scacchi, Go, backgammon, poker. Per l'IA sono un laboratorio perfetto, perche' lo stato e' facile da rappresentare e le mosse legali sono poche e ben definite, a differenza del caos di un conflitto reale. Il capitolo parte dal caso piu' pulito — due giocatori, turni alternati, informazione completa, somma zero — e poi rilassa una condizione alla volta: prima aggiunge il caso (i dadi del backgammon), poi l'informazione nascosta (le carte del poker).

Il filo conduttore e' che il calcolo esatto della mossa ottima e' quasi sempre fuori portata: l'albero di gioco degli scacchi supera i 10^40 nodi. Tutta la disciplina consiste quindi nel decidere che cosa non calcolare — quali rami potare, quando fermarsi, come stimare cio' che non si e' esplorato.

<figure class="diagram">
<svg viewBox="0 0 760 496" role="img" aria-label="Mappa concettuale del capitolo 5: dal gioco a somma zero e dall'albero di gioco a minimax, potatura alfa-beta e funzione di valutazione, con le estensioni expectiminimax e stati-credenza, fino alla ricerca Monte Carlo e ad AlphaZero">
<defs><marker id="arr-c05" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" class="dg-arrow"/></marker></defs>
<line x1="290" y1="68" x2="290" y2="93" class="dg-edge" marker-end="url(#arr-c05)"/>
<line x1="404" y1="40" x2="630" y2="40" class="dg-edge"/>
<line x1="630" y1="40" x2="630" y2="93" class="dg-edge" marker-end="url(#arr-c05)"/>
<text x="517" y="32" text-anchor="middle" class="dg-edge-label">informazione nascosta</text>
<line x1="290" y1="152" x2="290" y2="177" class="dg-edge-primary" marker-end="url(#arr-c05)"/>
<line x1="290" y1="236" x2="290" y2="261" class="dg-edge-primary" marker-end="url(#arr-c05)"/>
<line x1="290" y1="320" x2="290" y2="345" class="dg-edge-primary" marker-end="url(#arr-c05)"/>
<line x1="290" y1="404" x2="290" y2="429" class="dg-edge" marker-end="url(#arr-c05)"/>
<text x="372" y="421" text-anchor="middle" class="dg-edge-label">se stimare e' difficile</text>
<line x1="390" y1="206" x2="512" y2="206" class="dg-edge" marker-end="url(#arr-c05)"/>
<text x="451" y="198" text-anchor="middle" class="dg-edge-label">con il caso</text>
<line x1="405" y1="376" x2="512" y2="376" class="dg-edge" marker-end="url(#arr-c05)"/>
<text x="458" y="368" text-anchor="middle" class="dg-edge-label">due patologie</text>
<line x1="405" y1="460" x2="512" y2="460" class="dg-edge" marker-end="url(#arr-c05)"/>
<text x="458" y="452" text-anchor="middle" class="dg-edge-label">+ reti neurali</text>
<rect x="176" y="12" width="228" height="56" rx="10" class="dg-node"/>
<text x="290" y="36" text-anchor="middle" class="dg-label">Gioco a somma zero</text>
<text x="290" y="52" text-anchor="middle" class="dg-sublabel">MAX contro MIN, turni alternati</text>
<rect x="195" y="96" width="190" height="56" rx="10" class="dg-node"/>
<text x="290" y="120" text-anchor="middle" class="dg-label">Albero di gioco</text>
<text x="290" y="136" text-anchor="middle" class="dg-sublabel">scacchi: oltre 10^40 nodi</text>
<rect x="515" y="96" width="230" height="56" rx="10" class="dg-node"/>
<text x="630" y="120" text-anchor="middle" class="dg-label">Stati-credenza</text>
<text x="630" y="136" text-anchor="middle" class="dg-sublabel">posizioni compatibili col percepito</text>
<rect x="190" y="180" width="200" height="56" rx="10" class="dg-node-primary"/>
<text x="290" y="204" text-anchor="middle" class="dg-label">Minimax</text>
<text x="290" y="220" text-anchor="middle" class="dg-sublabel">ottimo nel caso peggiore, O(b^m)</text>
<rect x="515" y="180" width="230" height="56" rx="10" class="dg-node"/>
<text x="630" y="204" text-anchor="middle" class="dg-label">Expectiminimax</text>
<text x="630" y="220" text-anchor="middle" class="dg-sublabel">nodi di casualita', valore atteso</text>
<rect x="182" y="264" width="216" height="56" rx="10" class="dg-node-primary"/>
<text x="290" y="288" text-anchor="middle" class="dg-label">Potatura alfa-beta</text>
<text x="290" y="304" text-anchor="middle" class="dg-sublabel">stessa mossa, meno nodi: O(b^(m/2))</text>
<rect x="175" y="348" width="230" height="56" rx="10" class="dg-node-primary"/>
<text x="290" y="372" text-anchor="middle" class="dg-label">Funzione di valutazione</text>
<text x="290" y="388" text-anchor="middle" class="dg-sublabel">fermarsi prima e stimare la posizione</text>
<rect x="515" y="348" width="230" height="56" rx="10" class="dg-node"/>
<text x="630" y="372" text-anchor="middle" class="dg-label">Patologie del taglio</text>
<text x="630" y="388" text-anchor="middle" class="dg-sublabel">quiescenza, effetto orizzonte</text>
<rect x="175" y="432" width="230" height="56" rx="10" class="dg-node"/>
<text x="290" y="456" text-anchor="middle" class="dg-label">Ricerca Monte Carlo (MCTS)</text>
<text x="290" y="472" text-anchor="middle" class="dg-sublabel">media di molte partite simulate</text>
<rect x="515" y="432" width="230" height="56" rx="10" class="dg-node-accent"/>
<text x="630" y="456" text-anchor="middle" class="dg-label">AlphaZero</text>
<text x="630" y="472" text-anchor="middle" class="dg-sublabel">MCTS + reti neurali in self-play</text>
</svg>
<figcaption>Mappa del capitolo 5 — decidere che cosa non calcolare: da minimax alla potatura alfa-beta e alla valutazione euristica, fino a MCTS e AlphaZero</figcaption>
</figure>

## Il gioco come problema formale

Un gioco a due giocatori si definisce con pochi ingredienti: uno stato iniziale, una funzione che dice a chi tocca muovere, l'insieme delle mosse legali in ogni stato, un modello di transizione che calcola lo stato successivo, un test che riconosce la fine della partita e una funzione di utilita' che assegna un punteggio agli stati terminali (per gli scacchi: vittoria, pareggio, sconfitta). Da questi ingredienti nasce l'albero di gioco: la radice e' la posizione corrente e ogni livello — ogni "strato" o ply — corrisponde alla mossa di un giocatore.

I giochi piu' studiati sono quelli a somma zero con informazione perfetta: entrambi vedono tutto e cio' che giova a uno danneggia l'altro nella stessa misura. Per convenzione i due giocatori si chiamano MAX e MIN: MAX cerca di massimizzare l'utilita' finale, MIN di minimizzarla. Questa simmetria ostile e' il cuore del problema: una strategia per MAX non e' una sequenza di mosse, ma un piano condizionale che prevede una risposta a ogni possibile contromossa di MIN.

## Minimax: assumere il peggio per scegliere il meglio

L'algoritmo minimax formalizza un ragionamento che ogni giocatore da tavolo conosce: "se muovo qui, lui rispondera' con la mossa che mi fa piu' male, e allora io...". Il valore minimax di uno stato e' l'utilita' che MAX puo' garantirsi assumendo che entrambi giochino in modo ottimo da li' in poi: nei nodi terminali e' l'utilita' del gioco, nei nodi MAX e' il massimo dei valori dei successori, nei nodi MIN il minimo. L'algoritmo scende in profondita' fino alle foglie e "riporta su" i valori; alla radice, la mossa migliore e' quella che porta al successore con valore piu' alto.

<figure class="diagram">
<svg viewBox="0 0 760 300" role="img" aria-label="Albero di gioco minimax a due strati: la radice MAX A ha valore 3; i nodi MIN B, C e D hanno valori minimax 3, 2 e 2; le nove foglie terminali hanno utilita' 3, 12, 8, 2, 4, 6, 14, 5 e 2; la mossa migliore per MAX e' a1 e la risposta migliore per MIN e' b1">
<defs><marker id="arr-c05-b" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" class="dg-arrow"/></marker></defs>
<line x1="380" y1="82" x2="160" y2="137" class="dg-edge-primary" marker-end="url(#arr-c05-b)"/>
<text x="255" y="102" text-anchor="middle" class="dg-edge-label">a1</text>
<line x1="380" y1="82" x2="380" y2="137" class="dg-edge" marker-end="url(#arr-c05-b)"/>
<text x="392" y="112" text-anchor="middle" class="dg-edge-label">a2</text>
<line x1="380" y1="82" x2="600" y2="137" class="dg-edge" marker-end="url(#arr-c05-b)"/>
<text x="505" y="102" text-anchor="middle" class="dg-edge-label">a3</text>
<line x1="160" y1="192" x2="90" y2="237" class="dg-edge-primary" marker-end="url(#arr-c05-b)"/>
<text x="108" y="210" text-anchor="middle" class="dg-edge-label">b1</text>
<line x1="160" y1="192" x2="160" y2="237" class="dg-edge" marker-end="url(#arr-c05-b)"/>
<text x="172" y="218" text-anchor="middle" class="dg-edge-label">b2</text>
<line x1="160" y1="192" x2="230" y2="237" class="dg-edge" marker-end="url(#arr-c05-b)"/>
<text x="212" y="210" text-anchor="middle" class="dg-edge-label">b3</text>
<line x1="380" y1="192" x2="310" y2="237" class="dg-edge" marker-end="url(#arr-c05-b)"/>
<text x="328" y="210" text-anchor="middle" class="dg-edge-label">c1</text>
<line x1="380" y1="192" x2="380" y2="237" class="dg-edge" marker-end="url(#arr-c05-b)"/>
<text x="392" y="218" text-anchor="middle" class="dg-edge-label">c2</text>
<line x1="380" y1="192" x2="450" y2="237" class="dg-edge" marker-end="url(#arr-c05-b)"/>
<text x="432" y="210" text-anchor="middle" class="dg-edge-label">c3</text>
<line x1="600" y1="192" x2="530" y2="237" class="dg-edge" marker-end="url(#arr-c05-b)"/>
<text x="548" y="210" text-anchor="middle" class="dg-edge-label">d1</text>
<line x1="600" y1="192" x2="600" y2="237" class="dg-edge" marker-end="url(#arr-c05-b)"/>
<text x="612" y="218" text-anchor="middle" class="dg-edge-label">d2</text>
<line x1="600" y1="192" x2="670" y2="237" class="dg-edge" marker-end="url(#arr-c05-b)"/>
<text x="652" y="210" text-anchor="middle" class="dg-edge-label">d3</text>
<text x="45" y="62" text-anchor="middle" class="dg-label">MAX</text>
<text x="45" y="171" text-anchor="middle" class="dg-label">MIN</text>
<rect x="350" y="30" width="60" height="52" rx="10" class="dg-node-primary"/>
<text x="380" y="52" text-anchor="middle" class="dg-label">A</text>
<text x="380" y="68" text-anchor="middle" class="dg-sublabel">3</text>
<rect x="130" y="140" width="60" height="52" rx="10" class="dg-node-primary"/>
<text x="160" y="162" text-anchor="middle" class="dg-label">B</text>
<text x="160" y="178" text-anchor="middle" class="dg-sublabel">3</text>
<rect x="350" y="140" width="60" height="52" rx="10" class="dg-node"/>
<text x="380" y="162" text-anchor="middle" class="dg-label">C</text>
<text x="380" y="178" text-anchor="middle" class="dg-sublabel">2</text>
<rect x="570" y="140" width="60" height="52" rx="10" class="dg-node"/>
<text x="600" y="162" text-anchor="middle" class="dg-label">D</text>
<text x="600" y="178" text-anchor="middle" class="dg-sublabel">2</text>
<rect x="68" y="240" width="44" height="40" rx="10" class="dg-node-accent"/>
<text x="90" y="265" text-anchor="middle" class="dg-label">3</text>
<rect x="138" y="240" width="44" height="40" rx="10" class="dg-node"/>
<text x="160" y="265" text-anchor="middle" class="dg-label">12</text>
<rect x="208" y="240" width="44" height="40" rx="10" class="dg-node"/>
<text x="230" y="265" text-anchor="middle" class="dg-label">8</text>
<rect x="288" y="240" width="44" height="40" rx="10" class="dg-node"/>
<text x="310" y="265" text-anchor="middle" class="dg-label">2</text>
<rect x="358" y="240" width="44" height="40" rx="10" class="dg-node"/>
<text x="380" y="265" text-anchor="middle" class="dg-label">4</text>
<rect x="428" y="240" width="44" height="40" rx="10" class="dg-node"/>
<text x="450" y="265" text-anchor="middle" class="dg-label">6</text>
<rect x="508" y="240" width="44" height="40" rx="10" class="dg-node"/>
<text x="530" y="265" text-anchor="middle" class="dg-label">14</text>
<rect x="578" y="240" width="44" height="40" rx="10" class="dg-node"/>
<text x="600" y="265" text-anchor="middle" class="dg-label">5</text>
<rect x="648" y="240" width="44" height="40" rx="10" class="dg-node"/>
<text x="670" y="265" text-anchor="middle" class="dg-label">2</text>
</svg>
<figcaption>Albero di gioco a due strati: i valori minimax risalgono dalle foglie alla radice, la mossa migliore per MAX e' a1 e la risposta migliore per MIN e' b1.</figcaption>
</figure>

Un dettaglio spesso trascurato: giocare la mossa minimax contro un avversario debole garantisce almeno il risultato calcolato, ma non e' sempre la scelta piu' redditizia. Contro un giocatore che difficilmente trovera' l'unica confutazione, una mossa "rischiosa" con nove esiti favorevoli su dieci puo' valere piu' di un pareggio certo. Il minimax e' ottimo nel senso del caso peggiore, non del valore atteso.

Il problema e' il costo: con fattore di ramificazione b e profondita' m, minimax esplora O(b^m) nodi. Per gli scacchi, con circa 35 mosse legali per posizione e partite da 80 strati, parliamo di circa 10^123 stati: l'algoritmo puro e' inservibile. Esiste anche un'estensione ai giochi con piu' di due giocatori — si sostituisce il valore scalare con un vettore di utilita', una per giocatore — che fa emergere fenomeni nuovi come le alleanze: se due giocatori deboli attaccano il piu' forte, la cooperazione nasce da puro egoismo, senza bisogno di accordi espliciti.

## Alfa-beta: l'arte di non guardare

La potatura alfa-beta calcola esattamente la stessa decisione di minimax esaminando molti meno nodi. L'idea: se durante la ricerca scopriamo che un ramo porta a un esito peggiore di un'alternativa gia' verificata, e' inutile continuare a esplorarlo, perche' un giocatore razionale non ci passera' mai. L'algoritmo mantiene due limiti lungo il cammino corrente: alfa, il miglior valore gia' garantito a MAX ("almeno"), e beta, il miglior valore gia' garantito a MIN ("al piu'"). Appena il valore di un nodo esce da questa finestra, il resto dei suoi figli viene ignorato.

Il guadagno dipende in modo cruciale dall'ordine di esame delle mosse: se si provano prima quelle buone, si pota molto di piu'. Con ordinamento perfetto la complessita' scende a O(b^(m/2)), il che equivale a dimezzare l'esponente: a parita' di tempo si guarda due volte piu' in profondita', e negli scacchi il fattore di ramificazione effettivo cala da 35 a 6. Euristiche pratiche come provare prima le catture, ricordare le "mosse killer" che hanno funzionato in posizioni simili, e sfruttare l'approfondimento iterativo per ordinare le mosse dello strato successivo avvicinano molto questo limite. Un'altra ottimizzazione chiave e' la tabella delle trasposizioni: sequenze diverse di mosse che sfociano nella stessa posizione vengono valutate una volta sola, con effetti notevoli sulla profondita' raggiungibile.

## Fermarsi prima della fine: funzioni di valutazione

Anche con alfa-beta, arrivare agli stati terminali di una partita di scacchi e' impossibile. La soluzione, gia' delineata da Claude Shannon nel 1950, e' interrompere la ricerca a una certa profondita' e stimare le posizioni non terminali con una funzione di valutazione euristica: al posto dell'utilita' vera, un numero che approssima la probabilita' di vincere da quello stato. La forma classica e' una somma pesata di caratteristiche della posizione — negli scacchi il conteggio del materiale, dove per convenzione un pedone vale 1, cavallo e alfiere 3, la torre 5, la regina 9 — anche se i programmi moderni preferiscono combinazioni non lineari, e i pesi possono essere appresi automaticamente invece che fissati a mano.

Tagliare la ricerca a profondita' fissa crea pero' due patologie. La prima: valutare posizioni "agitate", dove e' in corso uno scambio di pezzi, produce stime senza senso; serve una ricerca di quiescenza che prosegue finche' la posizione non si calma. La seconda e' l'effetto orizzonte: un danno inevitabile (un pezzo condannato) puo' essere spinto oltre la profondita' di ricerca con mosse dilatorie, per esempio una serie di scacchi inutili, e il programma crede di averlo evitato. Le estensioni singole — approfondire la ricerca quando una mossa e' chiaramente superiore alle alternative — mitigano il problema.

A queste tecniche i motori aggiungono la potatura in avanti (tagliare rami che sembrano cattivi senza la garanzia che lo siano, come fanno ProbCut o la ricerca beam) e le tabelle precalcolate: librerie di aperture derivate dall'esperienza umana e da statistiche su milioni di partite, e tavole dei finali costruite con ricerca retrograda che risolvono perfettamente tutte le posizioni fino a sette pezzi. Il risultato complessivo e' un motore come Stockfish, che cerca a 30 strati di profondita' e supera qualsiasi umano.

## Monte Carlo: valutare simulando

Per il Go l'approccio alfa-beta fallisce due volte: il fattore di ramificazione parte da 361, e nessuno e' riuscito a scrivere una buona funzione di valutazione, perche' il valore del materiale conta poco e la situazione resta fluida fino alla fine. La risposta e' la ricerca ad albero Monte Carlo (MCTS): invece di stimare uno stato con una formula, si giocano da quello stato molte partite complete simulate (playout o rollout) e si usa la percentuale di vittorie come valore.

MCTS costruisce un albero di ricerca iterando quattro passi: selezione (si scende nell'albero scegliendo le mosse secondo una politica di selezione), espansione (si aggiunge un nuovo nodo foglia), simulazione (si gioca una partita fino in fondo secondo una politica di playout) e retropropagazione (il risultato aggiorna le statistiche di tutti i nodi sul cammino). La politica di selezione piu' nota, UCT, usa la formula UCB1 per bilanciare sfruttamento delle mosse che hanno vinto spesso ed esplorazione di quelle provate poche volte: il termine di esplorazione cresce per i nodi trascurati e svanisce all'aumentare delle simulazioni.

Il vantaggio strutturale di MCTS e' la robustezza: alfa-beta puo' essere deviata da un singolo errore di valutazione su un nodo, mentre una media su migliaia di simulazioni assorbe gli errori individuali. Inoltre il costo di una simulazione e' lineare nella profondita', non esponenziale, e il metodo funziona anche su giochi nuovi di cui si conoscono solo le regole. Il rovescio della medaglia: essendo una potatura di tipo B, puo' non esplorare mai la singola linea di gioco decisiva, e fatica dove una mossa e' "ovviamente" vincente per un umano ma richiede molte simulazioni per emergere. AlphaZero ha mostrato che la combinazione di MCTS e reti neurali che apprendono giocando contro se stesse vale anche per gli scacchi, dove alfa-beta sembrava insuperabile.

## Dadi, carte coperte e il valore del bluff

I giochi stocastici come il backgammon aggiungono all'albero i nodi di casualita': tra una mossa e l'altra c'e' un lancio di dadi con esiti pesati per probabilita'. Il valore minimax si generalizza in expectiminimax: nei nodi di casualita' si calcola il valore atteso, cioe' la media dei valori dei figli pesata per la probabilita' di ciascun esito. Due conseguenze pratiche: la complessita' esplode (guardare lontano diventa quasi inutile, perche' le sequenze future si diluiscono nelle probabilita') e la funzione di valutazione deve restituire valori proporzionali alla probabilita' di vincere, non un ordinamento qualsiasi — una trasformazione che preserva l'ordine delle foglie puo' cambiare la mossa scelta.

I giochi parzialmente osservabili sono un'altra categoria ancora. In Kriegspiel, variante degli scacchi in cui i pezzi avversari sono invisibili, il giocatore ragiona su stati-credenza — l'insieme delle posizioni compatibili con cio' che ha percepito — e una strategia vincente deve dare scacco matto in ogni stato dello stato-credenza. Emergono concetti impossibili nei giochi osservabili, come lo scacco matto probabilistico, che riesce con probabilita' 1 grazie a mosse randomizzate. Nei giochi di carte come bridge e poker, l'approssimazione comune e' la "media sulla chiaroveggenza": si campionano le distribuzioni possibili delle carte e si media il risultato come se poi il gioco fosse osservabile. Funziona spesso, ma ha un difetto concettuale profondo: un agente che assume di conoscere presto tutto non compie mai azioni per ottenere informazioni, non nasconde le proprie e non bluffa mai. La soluzione corretta passa per gli equilibri della teoria dei giochi, ed e' la strada che ha portato Libratus e Pluribus a battere i campioni umani di poker.

## Idee chiave

- Un gioco si formalizza con stato iniziale, mosse legali, modello di transizione, test di terminazione e funzione di utilita' sugli stati finali; da qui nasce l'albero di gioco.
- Nei giochi deterministici a due giocatori, a somma zero e con informazione perfetta, minimax calcola la strategia ottima esplorando l'albero in profondita' e riportando su i valori.
- La potatura alfa-beta restituisce la stessa decisione di minimax scartando i sottoalberi che non possono influenzare il risultato; con un buon ordinamento delle mosse dimezza di fatto l'esponente della ricerca.
- Poiche' l'albero completo resta intrattabile, si taglia la ricerca a una certa profondita' e si stima il valore degli stati con una funzione di valutazione euristica, gestendo quiescenza ed effetto orizzonte.
- La ricerca ad albero Monte Carlo sostituisce la valutazione euristica con la media di molte simulazioni complete, bilanciando esplorazione e sfruttamento (UCT/UCB1); e' la scelta preferita quando la ramificazione e' alta o la valutazione difficile.
- Tabelle di aperture e di finali permettono di consultare mosse precalcolate invece di cercare, alle due estremita' della partita.
- Il caso si gestisce con expectiminimax, che aggiunge nodi di casualita' valutati come media pesata per probabilita'; l'informazione nascosta richiede di ragionare su stati-credenza, e le scorciatoie che ignorano il valore dell'informazione non sanno bluffare.
- I programmi superano i campioni umani in scacchi, dama, Go, Othello e poker; l'evoluzione recente (AlphaZero, MuZero) sostituisce la conoscenza umana codificata a mano con l'apprendimento tramite gioco contro se stessi.

## Perche conta oggi

Le idee di questo capitolo sono il prototipo di come un [agente](../kb/concetti/agent.md) moderno ragiona sotto vincoli di calcolo: non si valuta tutto, si decide dove spendere il budget di computazione. Il "metaragionamento" che il capitolo indica come limite degli algoritmi classici — ragionare sul valore del calcolo stesso — e' esattamente il problema di un sistema di [inference](../kb/concetti/inference.md) che deve dosare quanti token di ragionamento dedicare a un problema, o di una catena di [chain-of-thought](../kb/concetti/chain-of-thought.md) che esplora piu' linee di soluzione e ne scarta la maggior parte: tecniche come tree-of-thought e la best-of-N sampling sono, in sostanza, ricerca su albero con potatura e funzioni di valutazione apprese.

Il secondo lascito e' l'idea, resa concreta da MCTS e AlphaZero, che simulare traiettorie future dentro un modello del mondo batte la valutazione statica: e' la stessa intuizione dietro i [world-models](../kb/concetti/world-models.md) e dietro il self-play che oggi genera dati di addestramento per il reasoning dei modelli. Infine, appena piu' agenti LLM operano nello stesso ambiente — in cooperazione o in competizione — riemergono i temi dei giochi multiplayer e dell'informazione nascosta: alleanze che nascono dall'interesse, valore strategico dell'imprevedibilita', equilibri invece di ottimi individuali. Sono le fondamenta teoriche della [multi-agent-orchestration](../kb/concetti/multi-agent-orchestration.md), e il motivo per cui valutare questi sistemi richiede [benchmark](../kb/concetti/evaluation-benchmark.md) che misurano il comportamento contro avversari reali, non solo su casi statici.
