---
titolo: Agenti intelligenti
capitolo: 2
parte: 1
concetti: [agent, world-models, tool-use, multi-agent-orchestration]
created: 2026-07-06
last_updated: 2026-07-06
---

# Agenti intelligenti

Questo capitolo risponde a una domanda che il capitolo precedente lascia aperta: se l'AI e' la scienza della progettazione di agenti razionali, che cosa e' esattamente un agente, e che cosa significa che si comporta "bene"? La risposta e' una cornice concettuale sorprendentemente compatta, che regge ancora oggi buona parte del vocabolario con cui parliamo di sistemi AI: percezioni, azioni, ambienti, misura di prestazione, razionalita'.

Il valore del capitolo non sta in un algoritmo specifico, ma in un metodo di analisi. Prima di scrivere una riga di codice, il progettista deve descrivere il problema: cosa vede il sistema, cosa puo' fare, in che tipo di mondo opera, come si misura il successo. Solo dopo ha senso scegliere l'architettura interna. E' la stessa disciplina che oggi applichiamo quando definiamo il perimetro di un agente basato su LLM: quali tool ha a disposizione, quale contesto riceve, come valutiamo se ha svolto il compito.

Il capitolo introduce anche una tassonomia di architetture di agente — dal riflesso puro all'agente che pianifica massimizzando l'utilita' attesa — che funziona come una scala di complessita' crescente. Ogni gradino aggiunge una capacita' (memoria, previsione, preferenze, apprendimento) e ha un costo. Capire questa scala aiuta a leggere i sistemi moderni: molti prodotti "agentici" attuali sono combinazioni di questi schemi di base, non invenzioni radicalmente nuove.

<figure class="diagram">
<svg viewBox="0 0 760 496" role="img" aria-label="Mappa concettuale del capitolo 2: l'agente e' descritto dalla funzione agente e implementato dal programma agente; la misura di prestazione definisce l'agente razionale, che richiede la specifica PEAS; le proprieta' dell'ambiente determinano le quattro architetture, che possono tutte apprendere">
<defs><marker id="arr-c02" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" class="dg-arrow"/></marker></defs>
<line x1="290" y1="40" x2="226" y2="40" class="dg-edge" marker-end="url(#arr-c02)"/>
<text x="258" y="32" text-anchor="middle" class="dg-edge-label">descritto da</text>
<line x1="120" y1="68" x2="120" y2="112" class="dg-edge" marker-end="url(#arr-c02)"/>
<text x="128" y="94" text-anchor="start" class="dg-edge-label">implementata da</text>
<line x1="380" y1="68" x2="380" y2="112" class="dg-edge-primary" marker-end="url(#arr-c02)"/>
<text x="388" y="94" text-anchor="start" class="dg-edge-label">fa la cosa giusta</text>
<line x1="550" y1="144" x2="484" y2="144" class="dg-edge" marker-end="url(#arr-c02)"/>
<text x="517" y="136" text-anchor="middle" class="dg-edge-label">definisce</text>
<line x1="460" y1="172" x2="600" y2="218" class="dg-edge" marker-end="url(#arr-c02)"/>
<text x="545" y="214" text-anchor="end" class="dg-edge-label">richiede la specifica</text>
<line x1="647" y1="276" x2="646" y2="322" class="dg-edge" marker-end="url(#arr-c02)"/>
<line x1="540" y1="352" x2="484" y2="352" class="dg-edge" marker-end="url(#arr-c02)"/>
<text x="512" y="344" text-anchor="middle" class="dg-edge-label">determinano</text>
<line x1="380" y1="172" x2="380" y2="320" class="dg-edge-primary" marker-end="url(#arr-c02)"/>
<line x1="120" y1="172" x2="120" y2="216" class="dg-edge" marker-end="url(#arr-c02)"/>
<text x="128" y="198" text-anchor="start" class="dg-edge-label">rappresentano lo stato</text>
<line x1="380" y1="380" x2="380" y2="424" class="dg-edge" marker-end="url(#arr-c02)"/>
<text x="388" y="406" text-anchor="start" class="dg-edge-label">ogni tipo puo' apprendere</text>
<rect x="290" y="12" width="180" height="56" rx="10" class="dg-node-primary"/>
<text x="380" y="36" text-anchor="middle" class="dg-label">Agente</text>
<text x="380" y="52" text-anchor="middle" class="dg-sublabel">sensori e attuatori</text>
<rect x="20" y="12" width="200" height="56" rx="10" class="dg-node"/>
<text x="120" y="36" text-anchor="middle" class="dg-label">Funzione agente</text>
<text x="120" y="52" text-anchor="middle" class="dg-sublabel">sequenza percettiva -> azione</text>
<rect x="20" y="116" width="200" height="56" rx="10" class="dg-node"/>
<text x="120" y="140" text-anchor="middle" class="dg-label">Programma agente</text>
<text x="120" y="156" text-anchor="middle" class="dg-sublabel">implementazione concreta</text>
<rect x="280" y="116" width="200" height="56" rx="10" class="dg-node-primary"/>
<text x="380" y="140" text-anchor="middle" class="dg-label">Agente razionale</text>
<text x="380" y="156" text-anchor="middle" class="dg-sublabel">massimizza il risultato atteso</text>
<rect x="550" y="116" width="195" height="56" rx="10" class="dg-node"/>
<text x="647" y="140" text-anchor="middle" class="dg-label">Misura di prestazione</text>
<text x="647" y="156" text-anchor="middle" class="dg-sublabel">valuta gli stati dell'ambiente</text>
<rect x="20" y="220" width="210" height="56" rx="10" class="dg-node"/>
<text x="125" y="244" text-anchor="middle" class="dg-label">Rappresentazioni</text>
<text x="125" y="260" text-anchor="middle" class="dg-sublabel">atomica, fattorizzata, strutturata</text>
<rect x="550" y="220" width="195" height="56" rx="10" class="dg-node"/>
<text x="647" y="244" text-anchor="middle" class="dg-label">Specifica PEAS</text>
<text x="647" y="260" text-anchor="middle" class="dg-sublabel">descrivere l'ambiente operativo</text>
<rect x="280" y="324" width="200" height="56" rx="10" class="dg-node-primary"/>
<text x="380" y="348" text-anchor="middle" class="dg-label">Quattro architetture</text>
<text x="380" y="364" text-anchor="middle" class="dg-sublabel">dal riflesso all'utilita'</text>
<rect x="540" y="324" width="210" height="56" rx="10" class="dg-node"/>
<text x="645" y="348" text-anchor="middle" class="dg-label">Proprieta' dell'ambiente</text>
<text x="645" y="364" text-anchor="middle" class="dg-sublabel">osservabile? dinamico? ignoto?</text>
<rect x="280" y="428" width="200" height="56" rx="10" class="dg-node-accent"/>
<text x="380" y="452" text-anchor="middle" class="dg-label">Agente che apprende</text>
<text x="380" y="468" text-anchor="middle" class="dg-sublabel">migliora i propri componenti</text>
</svg>
<figcaption>Mappa del capitolo 2 — dall'agente alla razionalita', dalla specifica PEAS alle architetture che apprendono</figcaption>
</figure>

## Percepire e agire: la definizione minima di agente

Un agente e' qualunque sistema che riceve informazioni dall'ambiente tramite sensori e interviene su di esso tramite attuatori. La definizione e' volutamente larga: copre un umano (occhi e mani), un robot (telecamere e motori), ma anche un puro software che legge file e pacchetti di rete e risponde scrivendo dati o mostrando informazioni. L'ambiente non e' "il mondo intero": e' la porzione di mondo che influenza cio' che l'agente percepisce e che le sue azioni possono modificare.

<figure class="diagram">
<svg viewBox="0 0 760 300" role="img" aria-label="Schema dell'interazione agente-ambiente: l'agente riceve percezioni dall'ambiente tramite i sensori, il programma agente (il punto interrogativo) sceglie l'azione e gli attuatori agiscono sull'ambiente">
<defs><marker id="arr-c02-b" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" class="dg-arrow"/></marker></defs>
<rect x="70" y="25" width="320" height="250" rx="10" class="dg-node-primary"/>
<text x="135" y="58" text-anchor="middle" class="dg-label">agente</text>
<rect x="600" y="25" width="140" height="250" rx="10" class="dg-node"/>
<text x="670" y="155" text-anchor="middle" class="dg-label">ambiente</text>
<line x1="600" y1="58" x2="374" y2="58" class="dg-edge" marker-end="url(#arr-c02-b)"/>
<text x="480" y="50" text-anchor="middle" class="dg-edge-label">percezioni</text>
<line x1="370" y1="242" x2="596" y2="242" class="dg-edge" marker-end="url(#arr-c02-b)"/>
<text x="480" y="234" text-anchor="middle" class="dg-edge-label">azioni</text>
<line x1="310" y1="76" x2="310" y2="112" class="dg-edge" marker-end="url(#arr-c02-b)"/>
<line x1="310" y1="185" x2="310" y2="221" class="dg-edge" marker-end="url(#arr-c02-b)"/>
<rect x="250" y="40" width="120" height="36" rx="10" class="dg-node"/>
<text x="310" y="62" text-anchor="middle" class="dg-label">sensori</text>
<rect x="260" y="115" width="100" height="70" rx="10" class="dg-node"/>
<text x="310" y="158" text-anchor="middle" class="dg-label">?</text>
<rect x="250" y="224" width="120" height="36" rx="10" class="dg-node"/>
<text x="310" y="246" text-anchor="middle" class="dg-label">attuatori</text>
</svg>
<figcaption>Gli agenti interagiscono con l'ambiente attraverso sensori e attuatori.</figcaption>
</figure>

Il comportamento dell'agente si descrive matematicamente con la funzione agente: una corrispondenza che associa a ogni possibile storia di percezioni (la sequenza percettiva) un'azione. In linea di principio la si potrebbe scrivere come una tabella gigantesca; in pratica la tabella e' astrazione pura, e cio' che gira davvero dentro la macchina e' il programma agente, un'implementazione concreta e finita di quella funzione. La distinzione tra descrizione esterna (funzione) e implementazione interna (programma) e' uno dei punti concettuali piu' utili del capitolo.

Gli autori usano un esempio minuscolo per rendere tutto tangibile: un aspirapolvere robotico in un mondo di due riquadri, ciascuno pulito o sporco. L'agente percepisce dove si trova e se c'e' sporco, e puo' spostarsi o aspirare. Anche in un mondo cosi' ridotto emergono subito le domande vere: tra i tanti modi di riempire la tabella percezione-azione, qual e' quello giusto? Cosa distingue un agente buono da uno stupido?

## Razionalita': fare la cosa giusta, non la cosa perfetta

La risposta passa dal consequenzialismo: un agente si giudica dalle conseguenze delle sue azioni sull'ambiente, misurate da una misura di prestazione che valuta la sequenza di stati attraversati. Un agente razionale e', per ogni sequenza percettiva possibile, quello che sceglie l'azione che massimizza il valore atteso di quella misura, date le informazioni disponibili.

Due dettagli della definizione hanno conseguenze pratiche enormi. Primo: la misura va definita sull'effetto desiderato nell'ambiente, non sul comportamento che immaginiamo debba avere l'agente. Se premio l'aspirapolvere per la quantita' di sporco aspirato, un agente razionale puo' scoprire che conviene aspirare, rovesciare lo sporco e riaspirarlo all'infinito. Meglio premiare i pavimenti puliti, magari con penalita' per consumo e rumore. E' la versione da manuale di quello che oggi chiamiamo reward hacking o specification gaming.

Secondo: razionalita' non significa onniscienza. L'agente razionale massimizza il risultato atteso, non quello effettivo; se attraverso la strada dopo aver guardato bene e mi cade addosso un portellone da un aereo, non sono stato irrazionale, solo sfortunato. Da qui discendono due comportamenti che un agente razionale deve avere: raccogliere informazioni (information gathering) quando le percezioni disponibili non bastano — guardare prima di attraversare, esplorare un ambiente sconosciuto — e apprendere dall'esperienza per correggere una conoscenza iniziale parziale o sbagliata. Un agente che si affida solo a cio' che il progettista gli ha cablato dentro manca di autonomia; un esempio classico e' lo scarabeo stercorario e la vespa sphex, insetti i cui rituali rigidi collassano appena un entomologo dispettoso viola le assunzioni su cui sono costruiti.

## Descrivere il problema prima della soluzione: PEAS

Prima di progettare l'agente bisogna specificare l'ambiente operativo, riassunto dall'acronimo PEAS: Performance, Environment, Actuators, Sensors. Per un taxi a guida autonoma, ad esempio: prestazione (viaggio sicuro, veloce, legale, confortevole, redditizio), ambiente (strade, traffico, pedoni, clienti, meteo), attuatori (sterzo, acceleratore, freni, clacson, schermo), sensori (telecamere, radar, GPS, tachimetro, microfoni). Alcuni obiettivi sono in tensione tra loro — velocita' contro sicurezza contro profitto — e la specifica deve esplicitare il compromesso.

Lo schema vale identico per agenti puramente software: un sistema di diagnosi medica, un tutor per lo studio di una lingua, un softbot che opera su siti web hanno tutti la loro descrizione PEAS. E ambienti virtuali possono essere complessi quanto quelli fisici.

## Le dimensioni che rendono un ambiente facile o difficile

Gli ambienti operativi si classificano lungo poche dimensioni, e ogni dimensione sposta radicalmente il progetto dell'agente:

- **Completamente vs parzialmente osservabile**: i sensori danno accesso a tutto lo stato rilevante o solo a una parte? Con osservabilita' parziale serve memoria interna.
- **Agente singolo vs multiagente**: ci sono altre entita' che massimizzano una loro misura di prestazione in funzione del mio comportamento? Gli scacchi sono competitivi; il traffico e' in parte cooperativo e in parte competitivo. In ambienti competitivi anche il comportamento casuale puo' essere razionale, perche' rende imprevedibili.
- **Deterministico vs non deterministico**: lo stato successivo e' completamente determinato da stato corrente e azione? Il mondo reale, per scopi pratici, quasi mai. "Stocastico" e' il caso in cui l'incertezza e' quantificata con probabilita' esplicite.
- **Episodico vs sequenziale**: ogni decisione e' indipendente dalle precedenti (classificare pezzi difettosi su un nastro) o ogni scelta condiziona quelle future (scacchi, guida)?
- **Statico vs dinamico**: l'ambiente cambia mentre l'agente delibera? Se si', non decidere e' esso stesso una decisione.
- **Discreto vs continuo**: si applica a stati, tempo, percezioni e azioni.
- **Noto vs ignoto**: l'agente conosce le "leggi" dell'ambiente (gli esiti delle azioni) oppure deve scoprirle? Non coincide con l'osservabilita': il solitario e' noto ma parzialmente osservabile, un videogioco nuovo puo' essere osservabile ma ignoto.

Il caso peggiore combina tutto: parzialmente osservabile, multiagente, non deterministico, sequenziale, dinamico, continuo, ignoto. La guida di un taxi ci va molto vicino.

## Quattro architetture, una scala di complessita'

Il programma agente e' cio' che, eseguito su un'architettura fisica dotata di sensori e attuatori, implementa la funzione agente: agente = architettura + programma. L'approccio a tabella esplicita e' irrealizzabile — per un'ora di guida servirebbero piu' righe di quanti atomi contenga l'universo osservabile — e la sfida dell'AI e' proprio produrre comportamento razionale con poco codice invece che con una tabella enorme, come il metodo di Newton ha sostituito le tavole delle radici quadrate. Il capitolo delinea quattro schemi base.

**Agenti reattivi semplici.** Scelgono l'azione guardando solo la percezione corrente, tramite regole condizione-azione del tipo "se la macchina davanti frena, inizia a frenare". Sono compatti e veloci, ma funzionano solo se la decisione corretta e' ricavabile dalla singola percezione, cioe' in ambienti completamente osservabili. Con osservabilita' parziale cadono in cicli infiniti, che a volte si spezzano solo randomizzando le scelte.

**Agenti reattivi basati su modello.** La cura per l'osservabilita' parziale e' uno stato interno che tiene traccia della parte di mondo non visibile ora. Aggiornarlo richiede due tipi di conoscenza: un modello di transizione (come evolve il mondo e che effetto hanno le mie azioni) e un modello sensoriale (come lo stato del mondo si riflette nelle percezioni). Lo stato interno e' spesso una "migliore ipotesi", non una certezza: l'agente decide comunque.

**Agenti basati su obiettivi.** Sapere com'e' il mondo non basta a decidere: a un incrocio il taxi puo' girare in ogni direzione, e la scelta giusta dipende dalla destinazione. L'agente combina il modello del mondo con una descrizione esplicita di stati desiderabili e proietta le azioni nel futuro: "cosa succede se faccio cosi'? mi avvicina all'obiettivo?". Ricerca e pianificazione sono i campi dell'AI dedicati a trovare queste sequenze di azioni. Il vantaggio rispetto al reattivo e' la flessibilita': cambiare destinazione significa cambiare un dato, non riscrivere tutte le regole.

**Agenti basati sull'utilita'.** Gli obiettivi sono binari — raggiunto o no — mentre spesso servono gradazioni: molte rotte portano a destinazione, ma alcune sono piu' sicure, rapide o economiche. Una funzione di utilita' internalizza la misura di prestazione e permette di bilanciare obiettivi in conflitto e di confrontare obiettivi incerti pesando probabilita' e importanza. In condizioni di incertezza l'agente razionale massimizza l'utilita' attesa. Non e' gratis: servono modelli del mondo, ragionamento e algoritmi non banali, e la razionalita' perfetta resta computazionalmente fuori portata.

## Imparare a migliorarsi

Turing gia' nel 1950 suggeriva che, invece di programmare a mano le macchine intelligenti, convenisse costruire macchine capaci di apprendere e poi addestrarle. Qualsiasi tipo di agente puo' essere reso capace di apprendere. Lo schema generale ha quattro componenti: l'elemento esecutivo (l'agente come descritto finora, che sceglie le azioni), l'elemento di apprendimento (che modifica l'esecutivo per migliorarlo), l'elemento critico (che confronta il comportamento con uno standard di prestazione fissato dall'esterno e produce feedback) e il generatore di problemi (che propone azioni esplorative, subottimali nel breve ma informative — come gli esperimenti di Galileo). Alcune percezioni funzionano da ricompense o penalita' dirette: la mancia negata al tassista brusco e' un segnale sulla qualita' della guida. Il tema unificante: apprendere significa modificare un componente dell'agente perche' si accordi meglio con il feedback disponibile.

Un ultimo asse riguarda come i componenti rappresentano l'ambiente: rappresentazioni atomiche (ogni stato e' una scatola nera indivisibile), fattorizzate (uno stato e' un vettore di attributi con valori) e strutturate (oggetti espliciti e relazioni tra loro), in ordine di espressivita' crescente. Piu' la rappresentazione e' espressiva, piu' e' concisa — ma piu' ragionamento e apprendimento si complicano.

## Idee chiave

- Un agente e' qualsiasi sistema che percepisce un ambiente e agisce su di esso; il suo comportamento e' descritto dalla funzione agente, che mappa sequenze percettive in azioni, e realizzato da un programma agente.
- La razionalita' e' relativa: dipende dalla misura di prestazione, dalla conoscenza pregressa, dalle azioni disponibili e dalle percezioni ricevute fino a quel momento. Massimizza il risultato atteso, non quello reale.
- La misura di prestazione va definita sugli effetti desiderati nell'ambiente, non sui comportamenti attesi dell'agente: altrimenti l'agente ottimizza la metrica invece del compito.
- Progettare un agente comincia dalla specifica PEAS dell'ambiente operativo, la piu' dettagliata possibile.
- Le proprieta' dell'ambiente — osservabilita', numero di agenti, determinismo, episodicita', dinamicita', discretezza, conoscenza delle regole — determinano quale architettura di agente e' adeguata.
- Le quattro architetture base (reattivo semplice, reattivo con modello, a obiettivi, a utilita') formano una scala: ogni gradino aggiunge memoria, previsione o preferenze graduate, in cambio di piu' complessita'.
- Se la misura di prestazione e' incerta o difficile da specificare, il progetto deve incorporare quell'incertezza, altrimenti l'agente rischia di ottimizzare l'obiettivo sbagliato.
- Ogni architettura puo' essere estesa con l'apprendimento, che migliora i componenti dell'agente sulla base del feedback e permette di operare in ambienti inizialmente ignoti.

## Perche conta oggi

Il vocabolario di questo capitolo del 1995-2021 e' diventato, quasi senza modifiche, il vocabolario degli [agenti](../kb/concetti/agent.md) basati su LLM. Un agente moderno che legge una codebase, chiama API e scrive file e' esattamente il classico "softbot": le percezioni sono l'output dei tool e il contesto, gli attuatori sono le chiamate a funzioni esterne — cio' che oggi chiamiamo [tool use](../kb/concetti/tool-use.md) — e l'ambiente operativo e' parzialmente osservabile, dinamico e spesso ignoto. Anche la struttura pratica che circonda il modello, l'[agent harness](../kb/concetti/agent-harness.md), e' la versione contemporanea dell'"architettura" su cui gira il programma agente; e lo stato interno che l'agente mantiene per compensare l'osservabilita' parziale trova il suo limite fisico nella [context window](../kb/concetti/context-window.md) del modello.

Anche le lezioni concettuali reggono. Il monito sulla misura di prestazione mal specificata e' il cuore dei problemi di allineamento e di reward hacking, e tecniche come [RLHF](../kb/concetti/rlhf.md) sono tentativi di apprendere le preferenze umane invece di cablarle — proprio come il tassista che aggiorna la sua funzione di utilita' osservando le reazioni dei passeggeri. La distinzione tra ambienti a singolo agente e multiagente anticipa i sistemi di [orchestrazione multi-agente](../kb/concetti/multi-agent-orchestration.md) attuali, dove piu' agenti cooperano suddividendosi un compito. E l'idea che un agente competente debba mantenere modelli di transizione e sensoriali del proprio ambiente riecheggia nel dibattito sui [world models](../kb/concetti/world-models.md) degli LLM: quanto del mondo un modello linguistico rappresenta davvero, e quanto gli basta per agire in modo razionale.
