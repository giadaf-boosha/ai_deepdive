---
titolo: Inferenza nella logica del primo ordine
capitolo: 9
parte: 3
concetti: [inference, embedding, chain-of-thought, rag]
created: 2026-07-06
last_updated: 2026-07-06
---

# Inferenza nella logica del primo ordine

Il capitolo 8 ha mostrato come la logica del primo ordine permetta di descrivere il mondo con oggetti, relazioni e quantificatori. Il capitolo 9 affronta la domanda successiva, quella operativa: come si costruisce un algoritmo che, data una base di conoscenza scritta in questo linguaggio, risponda a qualsiasi domanda per cui esiste una risposta? Non basta che la logica sia espressiva; serve una procedura meccanica di deduzione che sia corretta (non deriva mai falsita') e, dove possibile, completa (trova ogni conseguenza logica).

La risposta del capitolo si articola in un percorso preciso. Prima si dimostra che l'inferenza del primo ordine si puo' ridurre a quella proposizionale, al prezzo di un'esplosione combinatoria. Poi si introduce l'unificazione, il meccanismo che evita quell'esplosione e permette di ragionare direttamente sulle formule con variabili. Su questa base si costruiscono tre grandi famiglie di algoritmi: la concatenazione in avanti, la concatenazione all'indietro (da cui nasce il Prolog) e la risoluzione, l'unica procedura completa per basi di conoscenza arbitrarie.

Il capitolo contiene anche uno dei risultati piu' profondi di tutta l'informatica teorica: la conseguenza logica nel primo ordine e' semidecidibile. Esistono algoritmi che confermano ogni formula che segue davvero dalla base di conoscenza, ma nessun algoritmo puo' rispondere "no" in tutti i casi in cui la formula non segue. E' un limite strutturale, non un difetto ingegneristico, e condiziona il design di ogni sistema di ragionamento automatico.

<figure class="diagram">
<svg viewBox="0 0 760 470" role="img" aria-label="Mappa concettuale del capitolo 9: l'inferenza nel primo ordine si affronta prima con la proposizionalizzazione, che porta alla semidecidibilita', poi con l'unificazione, da cui derivano il Modus Ponens generalizzato, le concatenazioni in avanti e all'indietro con Datalog e Prolog, e la risoluzione su formule in CNF, unica procedura completa">
<defs><marker id="arr-c09" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" class="dg-arrow"/></marker></defs>
<line x1="320" y1="68" x2="140" y2="107" class="dg-edge" marker-end="url(#arr-c09)"/>
<text x="217" y="80" text-anchor="middle" class="dg-edge-label">forza bruta</text>
<line x1="380" y1="68" x2="380" y2="107" class="dg-edge-primary" marker-end="url(#arr-c09)"/>
<line x1="115" y1="166" x2="115" y2="207" class="dg-edge" marker-end="url(#arr-c09)"/>
<text x="123" y="192" class="dg-edge-label">teorema di Herbrand</text>
<line x1="380" y1="166" x2="380" y2="207" class="dg-edge-primary" marker-end="url(#arr-c09)"/>
<text x="390" y="192" class="dg-edge-label">lifting</text>
<line x1="475" y1="155" x2="612" y2="307" class="dg-edge" marker-end="url(#arr-c09)"/>
<text x="560" y="290" text-anchor="middle" class="dg-edge-label">letterali complementari</text>
<line x1="650" y1="166" x2="650" y2="307" class="dg-edge" marker-end="url(#arr-c09)"/>
<line x1="295" y1="266" x2="145" y2="307" class="dg-edge" marker-end="url(#arr-c09)"/>
<line x1="380" y1="266" x2="380" y2="307" class="dg-edge" marker-end="url(#arr-c09)"/>
<line x1="115" y1="366" x2="115" y2="397" class="dg-edge" marker-end="url(#arr-c09)"/>
<text x="123" y="386" class="dg-edge-label">senza funzioni</text>
<line x1="380" y1="366" x2="380" y2="397" class="dg-edge" marker-end="url(#arr-c09)"/>
<rect x="270" y="12" width="220" height="56" rx="10" class="dg-node-primary"/>
<text x="380" y="36" text-anchor="middle" class="dg-label">Inferenza nel primo ordine</text>
<text x="380" y="52" text-anchor="middle" class="dg-sublabel">procedura meccanica di deduzione</text>
<rect x="22" y="110" width="186" height="56" rx="10" class="dg-node"/>
<text x="115" y="134" text-anchor="middle" class="dg-label">Proposizionalizzazione</text>
<text x="115" y="150" text-anchor="middle" class="dg-sublabel">istanziare i quantificatori</text>
<rect x="280" y="110" width="200" height="56" rx="10" class="dg-node-primary"/>
<text x="380" y="134" text-anchor="middle" class="dg-label">Unificazione</text>
<text x="380" y="150" text-anchor="middle" class="dg-sublabel">sostituzione piu' generale (MGU)</text>
<rect x="560" y="110" width="180" height="56" rx="10" class="dg-node"/>
<text x="650" y="134" text-anchor="middle" class="dg-label">CNF e skolemizzazione</text>
<text x="650" y="150" text-anchor="middle" class="dg-sublabel">funzioni di Skolem</text>
<rect x="30" y="210" width="170" height="56" rx="10" class="dg-node"/>
<text x="115" y="234" text-anchor="middle" class="dg-label">Semidecidibilita'</text>
<text x="115" y="250" text-anchor="middle" class="dg-sublabel">nessun 'no' garantito</text>
<rect x="275" y="210" width="210" height="56" rx="10" class="dg-node-primary"/>
<text x="380" y="234" text-anchor="middle" class="dg-label">Modus Ponens generalizzato</text>
<text x="380" y="250" text-anchor="middle" class="dg-sublabel">regola per clausole definite</text>
<rect x="17" y="310" width="196" height="56" rx="10" class="dg-node"/>
<text x="115" y="334" text-anchor="middle" class="dg-label">Concatenazione in avanti</text>
<text x="115" y="350" text-anchor="middle" class="dg-sublabel">dai fatti al punto fisso</text>
<rect x="273" y="310" width="214" height="56" rx="10" class="dg-node"/>
<text x="380" y="334" text-anchor="middle" class="dg-label">Concatenazione all'indietro</text>
<text x="380" y="350" text-anchor="middle" class="dg-sublabel">ricerca AND/OR sugli obiettivi</text>
<rect x="560" y="310" width="180" height="56" rx="10" class="dg-node-accent"/>
<text x="650" y="334" text-anchor="middle" class="dg-label">Risoluzione</text>
<text x="650" y="350" text-anchor="middle" class="dg-sublabel">completa per refutazione</text>
<rect x="40" y="400" width="150" height="56" rx="10" class="dg-node"/>
<text x="115" y="424" text-anchor="middle" class="dg-label">Datalog</text>
<text x="115" y="440" text-anchor="middle" class="dg-sublabel">decidibile e polinomiale</text>
<rect x="300" y="400" width="160" height="56" rx="10" class="dg-node"/>
<text x="380" y="424" text-anchor="middle" class="dg-label">Prolog</text>
<text x="380" y="440" text-anchor="middle" class="dg-sublabel">incompleto senza tabling</text>
</svg>
<figcaption>Mappa concettuale del capitolo: l'unificazione e il lifting collegano la proposizionalizzazione alle tre famiglie di algoritmi, fino alla risoluzione, unica procedura completa.</figcaption>
</figure>

## Dai quantificatori alle proposizioni: la via forza bruta

Il primo approccio e' quasi ingenuo: eliminare i quantificatori sostituendo le variabili con termini concreti. La regola di istanziazione universale dice che da una formula valida per ogni x si puo' derivare la stessa formula con x rimpiazzato da qualunque termine ground, cioe' privo di variabili. Se la base di conoscenza afferma che ogni re avido e' malvagio, posso istanziarla su Giovanni, su Riccardo, sul padre di Giovanni e cosi' via. La regola di istanziazione esistenziale funziona in modo speculare: una formula che afferma "esiste un x tale che" viene sostituita da una singola istanza con un nuovo simbolo di costante, mai usato prima, detto costante di Skolem. E' l'atto di dare un nome a un oggetto di cui si sa solo che esiste.

Applicando sistematicamente queste regole, ogni base di conoscenza del primo ordine si trasforma in una base proposizionale, su cui girano gli algoritmi gia' visti nel capitolo 7. Questa tecnica si chiama proposizionalizzazione. Il problema e' che, appena la base contiene un simbolo di funzione, i termini ground diventano infiniti: da Padre si generano Padre(Giovanni), Padre(Padre(Giovanni)) e cosi' via senza fine. Il teorema di Herbrand (1930) salva la situazione a meta': se una formula segue logicamente dalla base, allora esiste una dimostrazione che usa solo un sottoinsieme finito delle istanziazioni. Si puo' quindi procedere per livelli crescenti di profondita' dei termini, con la garanzia di trovare prima o poi la dimostrazione, se esiste. Se non esiste, pero', la ricerca puo' non terminare mai: e' esattamente la semidecidibilita' citata sopra, imparentata con il problema della terminazione delle macchine di Turing.

## Unificazione: far combaciare formule con variabili

La proposizionalizzazione genera montagne di istanziazioni inutili. L'osservazione chiave del capitolo e' che spesso serve una sola sostituzione, quella giusta. Se so che ogni re avido e' malvagio, che Giovanni e' re e che tutti sono avidi, mi basta trovare una sostituzione che renda le premesse della regola identiche a fatti gia' noti: in questo caso legare sia la x della regola sia la y del fatto universale a Giovanni.

Il processo che calcola queste sostituzioni si chiama unificazione. L'algoritmo UNIFY prende due espressioni e restituisce, se esiste, un unificatore: una sostituzione che le rende identiche. Tra i tanti unificatori possibili, ne esiste sempre uno "piu' generale" (MGU), quello che impone il minimo di vincoli sulle variabili; e' il risultato canonico dell'algoritmo. Due dettagli pratici meritano attenzione. Primo, la standardizzazione separata: prima di unificare due formule occorre rinominare le variabili di una delle due, altrimenti collisioni puramente sintattiche di nomi fanno fallire unificazioni legittime. Secondo, il controllo di occorrenza: una variabile non puo' essere unificata con un termine che la contiene (x con F(x)), pena inferenze scorrette; molti sistemi Prolog lo omettono per velocita', accettando il rischio.

Sull'unificazione si costruisce il Modus Ponens generalizzato: se le premesse di un'implicazione unificano, tramite una sostituzione condivisa, con fatti presenti nella base di conoscenza, allora si puo' asserire il conseguente con quella stessa sostituzione applicata. Questo passaggio si chiama lifting: prendere una regola di inferenza proposizionale e "sollevarla" al primo ordine, facendole eseguire solo le sostituzioni davvero necessarie. Tutto il resto del capitolo e' lifting applicato ad algoritmi noti. Il capitolo discute anche il problema, molto concreto, di recuperare in fretta i fatti unificabili con una query dentro basi di conoscenza enormi: indicizzazione per predicato, chiavi combinate predicato-argomento, reticoli di sussunzione. E' il punto in cui la logica incontra l'ingegneria dei database.

## Concatenazione in avanti: dai fatti verso le conclusioni

La prima famiglia di algoritmi lavora su clausole definite: implicazioni con una congiunzione di letterali positivi come antecedente e un singolo letterale positivo come conseguente, con i quantificatori universali lasciati impliciti. Il capitolo le illustra con un esempio diventato classico: dalle premesse che vendere armi a nazioni ostili e' un crimine per un americano, che lo stato di Nono possiede missili venduti dal colonnello West e che Nono e' nemico dell'America, l'algoritmo deriva in due iterazioni che West e' un criminale.

La concatenazione in avanti parte dai fatti noti e fa scattare ogni regola le cui premesse sono soddisfatte, aggiungendo le conclusioni alla base, finche' non emergono piu' fatti nuovi: la base raggiunge allora un punto fisso. L'algoritmo e' corretto (ogni passo e' Modus Ponens generalizzato) e completo per le clausole definite. Per il caso Datalog — clausole definite senza simboli di funzione, il formalismo dei database deduttivi — la terminazione e' garantita e il costo e' polinomiale nel numero di fatti.

La versione ingenua e' pero' inefficiente per tre motivi, e per ciascuno il capitolo presenta il rimedio. Il matching tra premesse di una regola e fatti noti e' in generale NP-difficile (ogni CSP si puo' codificare come una singola clausola definita), ma le regole reali sono piccole e ordinamenti euristici dei congiunti aiutano molto. La ricontrollazione di tutte le regole a ogni iterazione si evita con la concatenazione incrementale: ogni fatto nuovo deve derivare da almeno un fatto inferito nell'iterazione precedente, quindi basta considerare le regole toccate da quei fatti; l'algoritmo Rete porta l'idea al limite, mantenendo in una rete le corrispondenze parziali tra regole e fatti, ed e' il cuore dei sistemi di produzioni come XCON e delle architetture cognitive come SOAR. Infine, per non derivare fatti irrilevanti rispetto all'obiettivo, la tecnica dei magic set riscrive le regole aggiungendo vincoli ricavati da una pre-analisi all'indietro dell'interrogazione.

## Concatenazione all'indietro e la nascita del Prolog

La seconda famiglia ribalta la direzione: si parte dall'obiettivo e si cercano regole il cui conseguente unifica con esso, trasformando le premesse in nuovi sotto-obiettivi, fino ad arrivare a fatti noti. E' una ricerca AND/OR in profondita': OR perche' l'obiettivo puo' essere dimostrato da regole diverse, AND perche' tutte le premesse di una regola scelta vanno dimostrate insieme, propagando la sostituzione accumulata.

Questo schema e' l'anima della programmazione logica, sintetizzata dall'equazione di Kowalski "algoritmi = logica + controllo": esprimi la conoscenza in forma dichiarativa e lascia che l'inferenza risolva il problema. Il linguaggio di riferimento e' il Prolog, dove una clausola come criminale(X) :- americano(X), arma(Y), vende(X,Y,Z), ostile(Z) si legge all'indietro rispetto all'implicazione logica. Un aspetto elegante: un predicato Prolog descrive una relazione, non una funzione, quindi lo stesso programma che concatena due liste puo' anche enumerare tutti i modi di spezzare una lista in due.

Il Prolog paga la sua efficienza con alcune deviazioni dalla logica pura: semantica dei database con ipotesi di mondo chiuso e nomi unici, aritmetica predefinita, predicati con effetti collaterali, niente controllo di occorrenza. Soprattutto, la ricerca in profondita' senza memoria lo rende incompleto: basta scrivere due clausole ricorsive nell'ordine "sbagliato" perche' il sistema si perda in un albero di dimostrazione infinito, anche quando la risposta esiste. La concatenazione all'indietro soffre inoltre di calcoli ridondanti sugli stessi sotto-obiettivi. La programmazione logica con tabelle risolve entrambi i problemi memorizzando i risultati intermedi, combinando l'orientamento all'obiettivo del backward chaining con la garanzia di terminazione (su Datalog) del forward chaining: e' l'analogo logico della programmazione dinamica. Il capitolo accenna anche alla programmazione logica a vincoli, in cui le variabili non vengono legate a valori ma vincolate, e la risposta a una query puo' essere un vincolo come "1 < Z < 7".

## Risoluzione: la procedura completa

Le prime due famiglie funzionano solo su clausole definite. La risoluzione e' la procedura generale: funziona su qualsiasi base di conoscenza del primo ordine. Il prerequisito e' convertire tutto in forma normale congiuntiva (CNF), una congiunzione di disgiunzioni di letterali. La conversione segue passi meccanici — eliminare le implicazioni, spingere le negazioni verso l'interno, standardizzare le variabili — piu' un passo specifico del primo ordine: la skolemizzazione, che elimina i quantificatori esistenziali sostituendoli con funzioni di Skolem i cui argomenti sono le variabili universali che li racchiudono. Il dettaglio e' cruciale: "esiste qualcuno che ama x" diventa Ama(G(x), x), dove G(x) dipende da x, perche' persone diverse possono essere amate da persone diverse; usare una costante fissa cambierebbe il significato.

La regola di risoluzione e' il lifting della sua versione proposizionale: due clausole si risolvono eliminando una coppia di letterali complementari, dove nel primo ordine "complementari" significa che uno unifica con la negazione dell'altro. La dimostrazione procede per refutazione: per provare che una formula segue dalla base, si aggiunge la sua negazione e si applicano risoluzioni finche' non emerge la clausola vuota, cioe' una contraddizione. Il capitolo dimostra la completezza per refutazione con una catena in tre mosse: il teorema di Herbrand garantisce un sottoinsieme finito di istanze ground insoddisfacibile, la risoluzione proposizionale trova la contraddizione su quelle istanze, e il lemma di lifting di Robinson trasporta la dimostrazione ground al primo ordine. Un riquadro collega questi risultati al teorema di incompletezza di Godel: estendendo il linguaggio con l'induzione matematica, per qualunque sistema di assiomi (coerente) esistono formule aritmetiche vere che quel sistema non puo' dimostrare.

Restano due questioni pratiche. L'uguaglianza non e' gestita nativamente: si puo' assiomatizzare (costoso), oppure trattare con regole dedicate come demodulazione e paramodulazione, che riscrivono termini uguali dentro le clausole. E lo spazio di ricerca va domato con strategie di controllo: preferenza per le clausole unitarie, insieme di supporto (ogni risoluzione deve coinvolgere una clausola derivata dalla query negata), risoluzione di input e lineare, eliminazione per sussunzione delle clausole piu' specifiche di altre gia' presenti. E' interessante che la concatenazione all'indietro si riveli un caso particolare di risoluzione con una specifica strategia di controllo. Il capitolo chiude segnalando che i dimostratori moderni si fanno aiutare dall'apprendimento: sistemi come DeepHOL usano reti neurali per stimare quali premesse e quali passi hanno piu' probabilita' di portare a una dimostrazione. Le applicazioni di punta sono la verifica e la sintesi di hardware e software: CPU verificate formalmente, algoritmi crittografici certificati, software spaziale controllato con model checker.

## Idee chiave

- L'inferenza del primo ordine si puo' ridurre a quella proposizionale tramite istanziazione dei quantificatori, ma la proposizionalizzazione genera troppe istanze inutili e diventa lenta appena il dominio cresce.
- L'unificazione calcola la sostituzione minima che rende identiche due formule con variabili; e' il componente che permette di fare solo le istanziazioni necessarie.
- Il Modus Ponens generalizzato, ottenuto per lifting, e' la regola su cui poggiano concatenazione in avanti e all'indietro, entrambe limitate alle clausole definite.
- La conseguenza logica nel primo ordine e' semidecidibile: si puo' sempre confermare cio' che segue dalla base, ma non sempre riconoscere cio' che non segue. Datalog, senza simboli di funzione, e' invece decidibile.
- La concatenazione in avanti alimenta database deduttivi e sistemi di produzioni; su Datalog e' completa e polinomiale nel numero di fatti.
- La concatenazione all'indietro e' orientata all'obiettivo e sta alla base della programmazione logica; il Prolog la implementa con scelte pragmatiche (mondo chiuso, niente occur check, ricerca in profondita') che lo rendono veloce ma incompleto senza tabling.
- La risoluzione, applicata a formule in CNF dopo la skolemizzazione, e' una procedura di dimostrazione completa per refutazione per l'intera logica del primo ordine.
- Uguaglianza (demodulazione, paramodulazione) e strategie di controllo (clausole unitarie, insieme di supporto, sussunzione) sono cio' che rende la risoluzione usabile in pratica; i dimostratori efficienti hanno prodotto risultati matematici nuovi e verificato hardware e software reali.

## Perche conta oggi

Gli LLM ragionano in modo statistico, non deduttivo, e proprio per questo i temi del capitolo tornano attuali come contrappeso. Quando un modello scompone un problema passo per passo con il [chain-of-thought](../kb/concetti/chain-of-thought.md), sta imitando in linguaggio naturale la struttura di una concatenazione all'indietro: obiettivo, sotto-obiettivi, fatti di appoggio — ma senza le garanzie di correttezza di un motore di [inference](../kb/concetti/inference.md) logica. Le pipeline neuro-simboliche piu' solide usano l'LLM per tradurre il problema in forma formale e delegano la deduzione a un solver o a un dimostratore, esattamente la divisione dei ruoli che il capitolo anticipa parlando di DeepHOL, dove [embedding](../kb/concetti/embedding.md) neurali guidano la selezione delle premesse dentro un dimostratore classico.

Anche l'ingegneria intorno agli LLM ricalca schemi del capitolo. Il problema di FETCH — recuperare in fretta i fatti unificabili con una query da una base enorme, con indici e reticoli di sussunzione — e' l'antenato simbolico del retrieval che alimenta i sistemi [RAG](../kb/concetti/rag.md). E un [agent](../kb/concetti/agent.md) moderno che decide quale strumento invocare tramite [tool-use](../kb/concetti/tool-use.md), verifica precondizioni e concatena i risultati sta eseguendo, di fatto, un ciclo di forward chaining su regole apprese anziche' scritte a mano. La semidecidibilita' resta il monito di fondo: qualunque sistema che ragiona su conoscenza espressiva deve accettare che alcune domande non ammettono un "no" garantito, e progettare timeout, euristiche e fallback di conseguenza.
