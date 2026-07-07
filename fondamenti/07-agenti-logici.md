---
titolo: Agenti logici
capitolo: 7
parte: 3
concetti: [agent, world-models, chain-of-thought, tool-use]
created: 2026-07-06
last_updated: 2026-07-06
---

# Agenti logici

Gli agenti risolutori di problemi visti nei capitoli precedenti sanno fare una cosa sola: cercare in uno spazio di stati atomici, senza alcuna nozione generale su come funziona il mondo. Il capitolo 7 introduce un salto qualitativo: agenti che possiedono una rappresentazione esplicita della conoscenza e la usano per ragionare, cioe' per derivare fatti nuovi da fatti noti e decidere cosa fare di conseguenza. La domanda di fondo e': come si costruisce un agente che "sa" delle cose, e come si garantisce che le conclusioni che trae siano corrette?

La risposta del capitolo passa per la logica come classe generale di linguaggi di rappresentazione. Il caso di studio e' la logica proposizionale: semplice, poco espressiva, ma sufficiente a illustrare tutti i concetti fondamentali — sintassi, semantica, conseguenza logica, inferenza corretta e completa — e supportata da tecnologie di inferenza mature (i risolutori SAT) che oggi affrontano problemi con milioni di variabili.

Conta anche il metodo: il capitolo mostra che un agente puo' essere descritto al livello della conoscenza (cosa sa e cosa vuole), indipendentemente da come quella conoscenza e' implementata. E' un'idea che precede di decenni il dibattito attuale su cosa "sappiano" davvero i modelli linguistici.

<figure class="diagram">
<svg viewBox="0 0 760 500" role="img" aria-label="Mappa concettuale del capitolo 7: l'agente basato sulla conoscenza usa una knowledge base espressa in logica proposizionale; la conseguenza logica si calcola con model checking, risoluzione e clausole di Horn, fino ai risolutori SAT, all'agente ibrido per il wumpus e al passaggio alla logica del primo ordine">
<defs><marker id="arr-c07" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" class="dg-arrow"/></marker></defs>
<line x1="380" y1="68" x2="380" y2="93" class="dg-edge-primary" marker-end="url(#arr-c07)"/>
<line x1="310" y1="68" x2="150" y2="93" class="dg-edge" marker-end="url(#arr-c07)"/>
<text x="218" y="73" text-anchor="middle" class="dg-edge-label">banco di prova</text>
<line x1="380" y1="152" x2="380" y2="177" class="dg-edge-primary" marker-end="url(#arr-c07)"/>
<text x="432" y="168" text-anchor="middle" class="dg-edge-label">linguaggio</text>
<line x1="380" y1="236" x2="380" y2="261" class="dg-edge-primary" marker-end="url(#arr-c07)"/>
<path d="M480,208 L725,208 L725,429" class="dg-edge" marker-end="url(#arr-c07)"/>
<text x="600" y="200" text-anchor="middle" class="dg-edge-label">non scala</text>
<line x1="300" y1="320" x2="135" y2="345" class="dg-edge" marker-end="url(#arr-c07)"/>
<line x1="360" y1="320" x2="352" y2="345" class="dg-edge" marker-end="url(#arr-c07)"/>
<line x1="455" y1="320" x2="570" y2="345" class="dg-edge" marker-end="url(#arr-c07)"/>
<text x="540" y="330" text-anchor="middle" class="dg-edge-label">forma ristretta</text>
<line x1="105" y1="404" x2="105" y2="429" class="dg-edge" marker-end="url(#arr-c07)"/>
<line x1="350" y1="404" x2="353" y2="429" class="dg-edge" marker-end="url(#arr-c07)"/>
<rect x="260" y="12" width="240" height="56" rx="10" class="dg-node-primary"/>
<text x="380" y="36" text-anchor="middle" class="dg-label">Agente basato sulla conoscenza</text>
<text x="380" y="52" text-anchor="middle" class="dg-sublabel">rappresenta la conoscenza e ragiona</text>
<rect x="30" y="96" width="200" height="56" rx="10" class="dg-node"/>
<text x="130" y="120" text-anchor="middle" class="dg-label">Mondo del wumpus</text>
<text x="130" y="136" text-anchor="middle" class="dg-sublabel">griglia 4x4, pericoli da dedurre</text>
<rect x="280" y="96" width="200" height="56" rx="10" class="dg-node-primary"/>
<text x="380" y="120" text-anchor="middle" class="dg-label">Knowledge base (KB)</text>
<text x="380" y="136" text-anchor="middle" class="dg-sublabel">Tell/Ask, approccio dichiarativo</text>
<rect x="280" y="180" width="200" height="56" rx="10" class="dg-node-primary"/>
<text x="380" y="204" text-anchor="middle" class="dg-label">Logica proposizionale</text>
<text x="380" y="220" text-anchor="middle" class="dg-sublabel">simboli e cinque connettivi</text>
<rect x="270" y="264" width="220" height="56" rx="10" class="dg-node-primary"/>
<text x="380" y="288" text-anchor="middle" class="dg-label">Conseguenza logica</text>
<text x="380" y="304" text-anchor="middle" class="dg-sublabel">alfa |= beta: vera in ogni modello</text>
<rect x="15" y="348" width="180" height="56" rx="10" class="dg-node"/>
<text x="105" y="372" text-anchor="middle" class="dg-label">Model checking</text>
<text x="105" y="388" text-anchor="middle" class="dg-sublabel">enumera i modelli, costo 2^n</text>
<rect x="255" y="348" width="190" height="56" rx="10" class="dg-node"/>
<text x="350" y="372" text-anchor="middle" class="dg-label">Risoluzione (CNF)</text>
<text x="350" y="388" text-anchor="middle" class="dg-sublabel">corretta e completa</text>
<rect x="495" y="348" width="200" height="56" rx="10" class="dg-node"/>
<text x="595" y="372" text-anchor="middle" class="dg-label">Clausole di Horn</text>
<text x="595" y="388" text-anchor="middle" class="dg-sublabel">concatenazione avanti/indietro</text>
<rect x="15" y="432" width="180" height="56" rx="10" class="dg-node"/>
<text x="105" y="456" text-anchor="middle" class="dg-label">Risolutori SAT</text>
<text x="105" y="472" text-anchor="middle" class="dg-sublabel">DPLL, WalkSAT, SATPlan</text>
<rect x="245" y="432" width="220" height="56" rx="10" class="dg-node"/>
<text x="355" y="456" text-anchor="middle" class="dg-label">Agente ibrido per il wumpus</text>
<text x="355" y="472" text-anchor="middle" class="dg-sublabel">inferenza logica + ricerca A*</text>
<rect x="520" y="432" width="220" height="56" rx="10" class="dg-node-accent"/>
<text x="630" y="456" text-anchor="middle" class="dg-label">Logica del primo ordine</text>
<text x="630" y="472" text-anchor="middle" class="dg-sublabel">capitolo 8: piu' espressiva</text>
</svg>
<figcaption>Mappa dei concetti del capitolo 7: dall'agente basato sulla conoscenza ai metodi di inferenza proposizionale e ai loro limiti.</figcaption>
</figure>

## Sapere per agire: la base di conoscenza

Il cuore di un agente basato sulla conoscenza e' la knowledge base (KB): un insieme di formule espresse in un linguaggio di rappresentazione, dove ogni formula asserisce qualcosa sul mondo. L'agente interagisce con la KB attraverso due operazioni: Tell, per aggiungere informazione (per esempio una nuova percezione), e Ask, per interrogarla su quale azione convenga. Il ciclo e' sempre lo stesso: comunica la percezione, chiedi l'azione, registra l'azione eseguita, ripeti.

Il punto chiave e' che rispondere a un Ask puo' richiedere inferenza: la KB deve poter derivare formule nuove da quelle che contiene, e le risposte devono essere conseguenze di quanto le e' stato detto, non invenzioni. Questo approccio si chiama dichiarativo: si dice all'agente cosa e' vero, invece di programmare direttamente i comportamenti (approccio procedurale). Il dibattito tra i due campi ha animato gli anni Settanta e Ottanta; la posizione moderna e' che servono entrambi, e che la conoscenza dichiarativa puo' spesso essere compilata in codice piu' efficiente.

## Il mondo del wumpus come palestra

Per rendere concreti questi concetti consideriamo un ambiente giocattolo: una caverna a griglia 4x4 con un mostro (il wumpus), pozzi senza fondo e un mucchio d'oro. L'agente percepisce solo indizi locali — fetore vicino al wumpus, brezza vicino ai pozzi, scintillio dove c'e' l'oro — e deve recuperare l'oro senza morire. L'ambiente e' deterministico ma parzialmente osservabile: l'agente non vede dove sono i pericoli, deve dedurlo.

<figure class="diagram">
<svg viewBox="0 0 760 440" role="img" aria-label="Il mondo del wumpus: griglia 4x4 con l'agente in [1,1] rivolto a est, il wumpus in [1,3], l'oro in [2,3] e pozzi in [3,1], [3,3] e [4,4]; fetore nelle stanze adiacenti al wumpus e brezza in quelle adiacenti ai pozzi">
<defs><marker id="arr-c07-b" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" class="dg-arrow"/></marker></defs>
<rect x="160" y="16" width="92" height="92" rx="10" class="dg-node"/>
<text x="206" y="66" text-anchor="middle" class="dg-sublabel">fetore</text>
<rect x="256" y="16" width="92" height="92" rx="10" class="dg-node"/>
<rect x="352" y="16" width="92" height="92" rx="10" class="dg-node"/>
<text x="398" y="66" text-anchor="middle" class="dg-sublabel">brezza</text>
<rect x="448" y="16" width="92" height="92" rx="10" class="dg-node"/>
<text x="494" y="66" text-anchor="middle" class="dg-label">POZZO</text>
<rect x="160" y="112" width="92" height="92" rx="10" class="dg-node"/>
<text x="206" y="162" text-anchor="middle" class="dg-label">WUMPUS</text>
<rect x="256" y="112" width="92" height="92" rx="10" class="dg-node-accent"/>
<text x="302" y="148" text-anchor="middle" class="dg-label">ORO</text>
<text x="302" y="166" text-anchor="middle" class="dg-sublabel">brezza</text>
<text x="302" y="182" text-anchor="middle" class="dg-sublabel">fetore</text>
<rect x="352" y="112" width="92" height="92" rx="10" class="dg-node"/>
<text x="398" y="162" text-anchor="middle" class="dg-label">POZZO</text>
<rect x="448" y="112" width="92" height="92" rx="10" class="dg-node"/>
<text x="494" y="162" text-anchor="middle" class="dg-sublabel">brezza</text>
<rect x="160" y="208" width="92" height="92" rx="10" class="dg-node"/>
<text x="206" y="258" text-anchor="middle" class="dg-sublabel">fetore</text>
<rect x="256" y="208" width="92" height="92" rx="10" class="dg-node"/>
<rect x="352" y="208" width="92" height="92" rx="10" class="dg-node"/>
<text x="398" y="258" text-anchor="middle" class="dg-sublabel">brezza</text>
<rect x="448" y="208" width="92" height="92" rx="10" class="dg-node"/>
<rect x="160" y="304" width="92" height="92" rx="10" class="dg-node-primary"/>
<text x="206" y="338" text-anchor="middle" class="dg-label">AGENTE</text>
<text x="206" y="354" text-anchor="middle" class="dg-sublabel">start</text>
<line x1="186" y1="370" x2="224" y2="370" class="dg-edge-primary" marker-end="url(#arr-c07-b)"/>
<rect x="256" y="304" width="92" height="92" rx="10" class="dg-node"/>
<text x="302" y="354" text-anchor="middle" class="dg-sublabel">brezza</text>
<rect x="352" y="304" width="92" height="92" rx="10" class="dg-node"/>
<text x="398" y="354" text-anchor="middle" class="dg-label">POZZO</text>
<rect x="448" y="304" width="92" height="92" rx="10" class="dg-node"/>
<text x="494" y="354" text-anchor="middle" class="dg-sublabel">brezza</text>
<text x="142" y="66" text-anchor="middle" class="dg-sublabel">4</text>
<text x="142" y="162" text-anchor="middle" class="dg-sublabel">3</text>
<text x="142" y="258" text-anchor="middle" class="dg-sublabel">2</text>
<text x="142" y="354" text-anchor="middle" class="dg-sublabel">1</text>
<text x="206" y="420" text-anchor="middle" class="dg-sublabel">1</text>
<text x="302" y="420" text-anchor="middle" class="dg-sublabel">2</text>
<text x="398" y="420" text-anchor="middle" class="dg-sublabel">3</text>
<text x="494" y="420" text-anchor="middle" class="dg-sublabel">4</text>
<text x="560" y="150" text-anchor="start" class="dg-label">Percezioni</text>
<text x="560" y="172" text-anchor="start" class="dg-sublabel">fetore: wumpus adiacente</text>
<text x="560" y="190" text-anchor="start" class="dg-sublabel">brezza: pozzo adiacente</text>
<text x="560" y="208" text-anchor="start" class="dg-sublabel">scintillio: oro nella stanza</text>
<text x="560" y="234" text-anchor="start" class="dg-sublabel">agente in [1,1], rivolto a est</text>
</svg>
<figcaption>Un tipico mondo del wumpus.</figcaption>
</figure>

Ed e' proprio qui che il ragionamento paga. Se in una stanza non si sente brezza, nessuna stanza adiacente contiene un pozzo; se in un'altra si sente fetore ma le stanze gia' escluse non possono ospitare il wumpus, la posizione del mostro resta univocamente determinata. Combinando percezioni raccolte in momenti e luoghi diversi, l'agente identifica stanze sicure che nessuna singola osservazione garantirebbe. La proprieta' cruciale: se le premesse sono vere, le conclusioni del ragionamento logico sono garantite vere. Non e' una euristica, e' una garanzia.

## Sintassi, semantica e conseguenza logica

Ogni logica e' definita da due cose. La sintassi stabilisce quali formule sono ben formate. La semantica definisce la verita' di ogni formula rispetto a ogni mondo possibile; quando serve precisione si parla di modelli, astrazioni matematiche che fissano un valore di verita' per ogni formula.

Su queste basi si definisce la relazione centrale del capitolo, la conseguenza logica: una formula alfa ha come conseguenza beta (si scrive alfa |= beta) se beta e' vera in tutti i modelli in cui alfa e' vera. Un'immagine utile: le conseguenze della KB sono un pagliaio, la formula che ci interessa e' un ago; la conseguenza logica dice che l'ago e' nel pagliaio, l'inferenza e' l'atto di trovarlo.

Un algoritmo di inferenza e' corretto se deriva solo conseguenze logiche, completo se le deriva tutte. Il metodo piu' diretto e' il model checking: enumerare tutti i modelli e verificare che la formula valga in ognuno di quelli che soddisfano la KB. Nel mondo del wumpus, con tre stanze incerte ci sono 8 modelli possibili; controllandoli tutti si conclude, per esempio, che una certa stanza non contiene pozzi. Funziona, ma il numero di modelli cresce come 2^n nel numero di simboli: serviranno metodi migliori.

Resta la questione del grounding: cosa garantisce che la KB sia vera nel mondo reale? Per le formule percettive rispondono i sensori; per le regole generali risponde l'apprendimento, che non e' infallibile ma, con buone procedure, da' ragioni per essere ottimisti.

## La logica proposizionale e le sue regole del gioco

La logica proposizionale costruisce formule a partire da simboli atomici (ciascuno vero o falso) e cinque connettivi: negazione, congiunzione, disgiunzione, implicazione e bicondizionale. La semantica e' definita ricorsivamente da tavole di verita'. Un dettaglio che sorprende sempre: l'implicazione non richiede alcun nesso causale tra premessa e conclusione, ed e' vera ogni volta che la premessa e' falsa. Va letta come "se la premessa e' vera, sostengo che lo e' anche la conclusione; altrimenti non affermo nulla".

Con questo linguaggio si scrive una KB per il wumpus: simboli come P(x,y) per "c'e' un pozzo in [x,y]" e B(x,y) per "c'e' brezza in [x,y]", piu' regole bicondizionali che collegano la brezza alla presenza di pozzi nelle stanze adiacenti. Tre concetti completano il quadro: l'equivalenza logica (due formule vere negli stessi modelli), la validita' (formule vere in ogni modello, le tautologie) e la soddisfacibilita' (esiste almeno un modello che rende vera la formula). Il problema SAT — decidere la soddisfacibilita' di una formula proposizionale — e' stato il primo problema dimostrato NP-completo, e la conseguenza logica proposizionale e' co-NP-completa: ogni algoritmo noto e' esponenziale nel caso peggiore. Un legame prezioso: alfa |= beta se e solo se (alfa AND NOT beta) e' insoddisfacibile, che e' la classica dimostrazione per assurdo.

## Dimostrare invece di enumerare

L'alternativa al model checking e' la dimostrazione di teoremi: applicare regole di inferenza direttamente alle formule, costruendo una catena di passi che porta alla conclusione. Il Modus Ponens (da "alfa implica beta" e "alfa" si inferisce "beta") e l'eliminazione degli and sono gli esempi base; ogni equivalenza logica standard puo' fungere da regola. La ricerca di una dimostrazione puo' battere l'enumerazione perche' ignora le proposizioni irrilevanti, per quante siano. Vale inoltre la monotonicita': aggiungere formule alla KB non invalida mai le conclusioni gia' tratte.

La regola che cambia tutto e' la risoluzione: prende due clausole (disgiunzioni di letterali) che contengono una coppia di letterali complementari e produce la clausola con tutti gli altri letterali. Da sola, accoppiata a un algoritmo di ricerca completo, da' una procedura di inferenza completa per l'intera logica proposizionale. Il trucco e' che ogni formula e' convertibile in forma normale congiuntiva (CNF, congiunzione di clausole); per dimostrare che KB implica alfa si converte (KB AND NOT alfa) in CNF e si risolve finche' o non emerge la clausola vuota (contraddizione: alfa e' dimostrata) o non si genera piu' nulla di nuovo (alfa non segue).

Molte KB pratiche non richiedono tutta questa potenza. Le clausole di Horn — al piu' un letterale positivo — si leggono come implicazioni "se corpo allora testa" e ammettono inferenza in tempo lineare tramite concatenazione in avanti (dai fatti verso le conclusioni, ragionamento guidato dai dati) o all'indietro (dalla query verso i fatti che la sostengono, ragionamento guidato dagli obiettivi). E' la base della programmazione logica, e i due stili anticipano una distinzione ancora attualissima tra elaborazione reattiva delle informazioni in ingresso e ricerca mirata a rispondere a una domanda.

## Risolutori SAT: il model checking diventa pratico

Il capitolo dedica ampio spazio a come rendere efficiente la verifica di soddisfacibilita'. L'algoritmo DPLL raffina l'enumerazione ricorsiva con tre idee: terminazione anticipata (una formula puo' risultare vera o falsa gia' su un modello parziale), euristica del simbolo puro (un simbolo che compare con un solo segno puo' essere assegnato senza rischi) e propagazione delle clausole unitarie (una clausola ridotta a un solo letterale forza un assegnamento, che a cascata ne forza altri). I risolutori moderni aggiungono analisi di componenti, ordinamento intelligente di variabili, backtracking guidato dai conflitti con apprendimento di clausole, riavvii casuali e indicizzazione dinamica: cosi' si gestiscono problemi con decine di milioni di variabili, con ricadute enormi su verifica dell'hardware e dei protocolli.

L'approccio complementare e' la ricerca locale: WalkSAT parte da un assegnamento casuale e inverte simboli, alternando passi greedy e passi casuali. Trova modelli in fretta quando esistono, ma non puo' mai certificare l'insoddisfacibilita': per un agente significa che va bene per trovare soluzioni, non per dimostrare che una stanza e' sicura. Interessante anche la geografia dei problemi SAT casuali: quelli sotto-vincolati (poche clausole) e sovra-vincolati (molte) sono facili; i problemi davvero duri si concentrano vicino a una soglia critica del rapporto clausole/simboli, intorno a 4,3 per le formule 3-CNF.

## Dal ragionamento all'azione: fluenti, frame e piani

L'ultima parte del capitolo costruisce un agente completo per il wumpus. Il mondo cambia nel tempo, quindi i simboli che descrivono aspetti mutevoli — i fluenti — vanno indicizzati con il passo temporale. Scrivere assiomi di effetto ("se al tempo t fai questa azione, al tempo t+1 vale quest'altro") non basta: non dicono nulla su cio' che resta invariato, e l'agente dimentica di avere ancora la freccia dopo essersi mosso. E' il celebre problema del frame. La soluzione elegante sono gli assiomi di stato successore, uno per fluente: un fluente e' vero al tempo t+1 se e solo se un'azione al tempo t lo ha reso vero, oppure era gia' vero e nessuna azione lo ha reso falso. Restano limiti di principio, come il problema della qualificazione: elencare davvero tutte le precondizioni di un'azione nel mondo reale e' impossibile, e la logica pura non offre una via d'uscita completa.

Con questi assiomi l'agente ibrido del capitolo combina inferenza logica (per stabilire quali stanze sono sicure) e ricerca A* (per pianificare i percorsi), secondo priorita' decrescenti: afferra l'oro se scintilla, esplora stanze sicure non visitate, prova a uccidere il wumpus con la freccia, al limite rischia o rinuncia. Per evitare che il costo delle inferenze cresca con la storia, lo stato-credenza si approssima con una congiunzione di letterali dimostrabili (1-CNF): un involucro conservativo che include tutti gli stati davvero possibili.

Infine SATPlan mostra che perfino la pianificazione si riduce a soddisfacibilita': si codificano stato iniziale, assiomi di transizione e obiettivo a un tempo t in un'unica formula, e ogni modello trovato da un risolutore SAT e' un piano. Servono pero' accorgimenti istruttivi: assiomi di precondizione (niente frecce scoccate senza freccia) e assiomi di esclusione tra azioni simultanee incompatibili. Il capitolo chiude con un'ammissione onesta: la logica proposizionale non scala, perche' non sa dire "per ogni stanza" o "per ogni tempo" e costringe a moltiplicare le formule. Serve un linguaggio piu' espressivo, la logica del primo ordine, tema del capitolo successivo.

## Idee chiave

- Un agente basato sulla conoscenza separa cosa sa (la KB, formule in un linguaggio di rappresentazione) da come lo usa (il meccanismo di inferenza): puo' essere descritto al livello della conoscenza, senza dettagli implementativi.
- Sintassi e semantica definiscono una logica; la conseguenza logica (beta vera in tutti i modelli in cui la KB e' vera) e' il criterio che rende affidabile il ragionamento.
- Un algoritmo di inferenza corretto deriva solo conseguenze logiche; uno completo le deriva tutte. La risoluzione su formule in CNF e' corretta e completa per la logica proposizionale.
- Con un vocabolario finito il model checking e' sempre possibile ma esponenziale; DPLL e la ricerca locale tipo WalkSAT lo rendono pratico su problemi enormi, anche se la ricerca locale non certifica mai l'insoddisfacibilita'.
- Le clausole di Horn ammettono inferenza in tempo lineare con concatenazione in avanti (guidata dai dati) o all'indietro (guidata dagli obiettivi).
- Per ambienti che cambiano servono fluenti indicizzati nel tempo e assiomi di stato successore, che risolvono il problema del frame specificando come ogni fluente evolve.
- La pianificazione puo' essere ridotta a SAT: ogni modello della formula che codifica stato iniziale, transizioni e obiettivo e' un piano valido (in ambienti completamente osservabili).
- La logica proposizionale non regge ambienti di dimensione arbitraria: manca la potenza espressiva per parlare in modo conciso di oggetti, tempo e regole universali — motivazione diretta per la logica del primo ordine.

## Perche conta oggi

Il vocabolario di questo capitolo e' il vocabolario con cui oggi si progettano e si valutano gli [agenti](../kb/concetti/agent.md) basati su LLM. Il ciclo Tell/Ask della KB e' l'antenato concettuale del loop percezione-ragionamento-azione di un agent harness moderno; la distinzione tra livello della conoscenza e livello dell'implementazione e' esattamente la lente con cui ci si chiede se un [LLM](../kb/concetti/llm.md) "sappia" qualcosa o si limiti a manipolare token. E il problema del grounding — come garantire che la KB rifletta il mondo reale — riappare identico quando si aggancia un modello a fonti esterne con la [RAG](../kb/concetti/rag.md) o a sensori e API tramite il [tool use](../kb/concetti/tool-use.md).

C'e' anche un contrasto istruttivo. L'inferenza logica offre garanzie (correttezza, completezza, monotonicita') che il ragionamento in linguaggio naturale di un LLM non ha: una catena di [chain-of-thought](../kb/concetti/chain-of-thought.md) somiglia a una dimostrazione, ma nessun teorema ne assicura la validita'. Per questo i sistemi neuro-simbolici e i verificatori formali (i discendenti diretti dei risolutori SAT del capitolo) tornano di moda come complemento dei modelli generativi: il modello propone, la logica verifica. Anche la stima dello stato con approssimazioni conservative e gli assiomi di stato successore prefigurano i [world models](../kb/concetti/world-models.md) con cui gli agenti attuali tengono traccia di ambienti parzialmente osservabili.
