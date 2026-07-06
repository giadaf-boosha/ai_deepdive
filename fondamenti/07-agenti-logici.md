---
titolo: Agenti logici
capitolo: 7
parte: 3
volume: 1
pagine: "215-256"
concetti: [agent, world-models, chain-of-thought, tool-use]
created: 2026-07-06
last_updated: 2026-07-06
---

# Agenti logici

Gli agenti risolutori di problemi visti nei capitoli precedenti sanno fare una cosa sola: cercare in uno spazio di stati atomici, senza alcuna nozione generale su come funziona il mondo. Il capitolo 7 introduce un salto qualitativo: agenti che possiedono una rappresentazione esplicita della conoscenza e la usano per ragionare, cioe' per derivare fatti nuovi da fatti noti e decidere cosa fare di conseguenza. La domanda di fondo e': come si costruisce un agente che "sa" delle cose, e come si garantisce che le conclusioni che trae siano corrette?

La risposta del capitolo passa per la logica come classe generale di linguaggi di rappresentazione. Il caso di studio e' la logica proposizionale: semplice, poco espressiva, ma sufficiente a illustrare tutti i concetti fondamentali — sintassi, semantica, conseguenza logica, inferenza corretta e completa — e supportata da tecnologie di inferenza mature (i risolutori SAT) che oggi affrontano problemi con milioni di variabili.

Conta anche il metodo: il capitolo mostra che un agente puo' essere descritto al livello della conoscenza (cosa sa e cosa vuole), indipendentemente da come quella conoscenza e' implementata. E' un'idea che precede di decenni il dibattito attuale su cosa "sappiano" davvero i modelli linguistici.

## Sapere per agire: la base di conoscenza

Il cuore di un agente basato sulla conoscenza e' la knowledge base (KB): un insieme di formule espresse in un linguaggio di rappresentazione, dove ogni formula asserisce qualcosa sul mondo. L'agente interagisce con la KB attraverso due operazioni: Tell, per aggiungere informazione (per esempio una nuova percezione), e Ask, per interrogarla su quale azione convenga. Il ciclo e' sempre lo stesso: comunica la percezione, chiedi l'azione, registra l'azione eseguita, ripeti.

Il punto chiave e' che rispondere a un Ask puo' richiedere inferenza: la KB deve poter derivare formule nuove da quelle che contiene, e le risposte devono essere conseguenze di quanto le e' stato detto, non invenzioni. Questo approccio si chiama dichiarativo: si dice all'agente cosa e' vero, invece di programmare direttamente i comportamenti (approccio procedurale). Il dibattito tra i due campi ha animato gli anni Settanta e Ottanta; la posizione moderna e' che servono entrambi, e che la conoscenza dichiarativa puo' spesso essere compilata in codice piu' efficiente.

## Il mondo del wumpus come palestra

Per rendere concreti questi concetti il libro usa un ambiente giocattolo: una caverna a griglia 4x4 con un mostro (il wumpus), pozzi senza fondo e un mucchio d'oro. L'agente percepisce solo indizi locali — fetore vicino al wumpus, brezza vicino ai pozzi, scintillio dove c'e' l'oro — e deve recuperare l'oro senza morire. L'ambiente e' deterministico ma parzialmente osservabile: l'agente non vede dove sono i pericoli, deve dedurlo.

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

## Riferimenti

- Stuart J. Russell, Peter Norvig — *Intelligenza Artificiale: Un Approccio Moderno*, 4a edizione italiana, Pearson Italia, Vol. 1 (2021), Capitolo 7, pp. 215-256.
