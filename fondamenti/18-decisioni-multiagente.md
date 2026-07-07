---
titolo: Decisioni multiagente
capitolo: 18
parte: 4
concetti: [agent, multi-agent-orchestration, interaction-model, world-models]
created: 2026-07-06
last_updated: 2026-07-06
---

# Decisioni multiagente

Fino a questo punto del percorso l'agente e' solo: percepisce, pianifica e agisce come se il mondo contenesse un unico decisore. Il capitolo 18 rimuove questa semplificazione e chiede: che cosa cambia quando nell'ambiente operano altri agenti, ciascuno con i propri obiettivi? La risposta breve e' che cambia quasi tutto. Un agente razionale non puo' piu' limitarsi a modellare l'ambiente fisico: deve modellare il ragionamento altrui, sapendo che gli altri stanno facendo lo stesso con lui. Questo ragionamento ricorsivo — io penso a cosa pensi tu di cosa penso io — e' il territorio della teoria dei giochi, che sta alle decisioni multiagente come la teoria delle decisioni sta all'agente singolo.

Il capitolo copre un arco ampio: come pianificare quando piu' attori eseguono azioni in concorrenza, come analizzare giochi non cooperativi (strategie dominanti, equilibrio di Nash, giochi ripetuti e sequenziali), come formare coalizioni e spartirne il valore nei giochi cooperativi, e infine come progettare i meccanismi collettivi — aste, votazioni, contrattazioni — con cui gruppi di agenti prendono decisioni condivise. Due prospettive attraversano tutto il materiale: la progettazione di agenti (data la situazione, qual e' la strategia migliore?) e la progettazione di meccanismi (date le strategie razionali, quali regole del gioco producono il miglior esito collettivo?).

Conta perche' quasi nessun sistema di IA reale opera nel vuoto. Router che si contendono banda, veicoli a un incrocio, offerenti in un'asta pubblicitaria, robot che si dividono compiti in un magazzino: sono tutti sistemi multiagente, e senza gli strumenti di questo capitolo il comportamento collettivo resta imprevedibile o inefficiente.

<figure class="diagram">
<svg viewBox="0 0 760 380" role="img" aria-label="Mappa concettuale del capitolo 18: dalle decisioni multiagente alla pianificazione multiattuatore e alla teoria dei giochi, con equilibrio di Nash, dilemma del prigioniero, giochi ripetuti, forma estesa, giochi cooperativi e progettazione di meccanismi, fino ai giochi di assistenza">
<defs><marker id="arr-c18" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" class="dg-arrow"/></marker></defs>
<line x1="350" y1="68" x2="128" y2="101" class="dg-edge" marker-end="url(#arr-c18)"/>
<text x="235" y="79" text-anchor="middle" class="dg-edge-label">stesso obiettivo</text>
<line x1="380" y1="68" x2="380" y2="101" class="dg-edge-primary" marker-end="url(#arr-c18)"/>
<text x="452" y="88" text-anchor="middle" class="dg-edge-label">preferenze divergenti</text>
<line x1="315" y1="160" x2="82" y2="201" class="dg-edge" marker-end="url(#arr-c18)"/>
<line x1="360" y1="160" x2="267" y2="201" class="dg-edge" marker-end="url(#arr-c18)"/>
<line x1="405" y1="160" x2="485" y2="201" class="dg-edge" marker-end="url(#arr-c18)"/>
<line x1="455" y1="160" x2="686" y2="201" class="dg-edge" marker-end="url(#arr-c18)"/>
<line x1="79" y1="232" x2="97" y2="306" class="dg-edge" marker-end="url(#arr-c18)"/>
<line x1="194" y1="340" x2="297" y2="340" class="dg-edge" marker-end="url(#arr-c18)"/>
<text x="245" y="331" text-anchor="middle" class="dg-edge-label">se ripetuto</text>
<line x1="689" y1="232" x2="640" y2="306" class="dg-edge" marker-end="url(#arr-c18)"/>
<text x="580" y="272" text-anchor="middle" class="dg-edge-label">l'umano sceglie per primo</text>
<rect x="280" y="12" width="200" height="56" rx="10" class="dg-node-primary"/>
<text x="380" y="36" text-anchor="middle" class="dg-label">Decisioni multiagente</text>
<text x="380" y="52" text-anchor="middle" class="dg-sublabel">piu' agenti, obiettivi propri</text>
<rect x="8" y="104" width="230" height="56" rx="10" class="dg-node"/>
<text x="123" y="128" text-anchor="middle" class="dg-label">Pianificazione multiattuatore</text>
<text x="123" y="144" text-anchor="middle" class="dg-sublabel">coordinamento, convenzioni</text>
<rect x="290" y="104" width="180" height="56" rx="10" class="dg-node-primary"/>
<text x="380" y="128" text-anchor="middle" class="dg-label">Teoria dei giochi</text>
<text x="380" y="144" text-anchor="middle" class="dg-sublabel">ragionamento ricorsivo</text>
<rect x="4" y="204" width="150" height="56" rx="10" class="dg-node"/>
<text x="79" y="228" text-anchor="middle" class="dg-label">Equilibrio di Nash</text>
<text x="79" y="244" text-anchor="middle" class="dg-sublabel">deviare non conviene</text>
<rect x="186" y="204" width="162" height="56" rx="10" class="dg-node"/>
<text x="267" y="228" text-anchor="middle" class="dg-label">Giochi cooperativi</text>
<text x="267" y="244" text-anchor="middle" class="dg-sublabel">nucleo e valore di Shapley</text>
<rect x="380" y="204" width="210" height="56" rx="10" class="dg-node"/>
<text x="485" y="228" text-anchor="middle" class="dg-label">Progettazione di meccanismi</text>
<text x="485" y="244" text-anchor="middle" class="dg-sublabel">aste, voto, contrattazione</text>
<rect x="622" y="204" width="134" height="56" rx="10" class="dg-node"/>
<text x="689" y="228" text-anchor="middle" class="dg-label">Forma estesa</text>
<text x="689" y="244" text-anchor="middle" class="dg-sublabel">induzione a ritroso</text>
<rect x="4" y="312" width="190" height="56" rx="10" class="dg-node"/>
<text x="99" y="336" text-anchor="middle" class="dg-label">Dilemma del prigioniero</text>
<text x="99" y="352" text-anchor="middle" class="dg-sublabel">equilibrio non Pareto-ottimo</text>
<rect x="300" y="312" width="190" height="56" rx="10" class="dg-node"/>
<text x="395" y="336" text-anchor="middle" class="dg-label">Giochi ripetuti</text>
<text x="395" y="352" text-anchor="middle" class="dg-sublabel">cooperazione via folk theorem</text>
<rect x="510" y="312" width="242" height="56" rx="10" class="dg-node-accent"/>
<text x="631" y="336" text-anchor="middle" class="dg-label">Giochi di assistenza</text>
<text x="631" y="352" text-anchor="middle" class="dg-sublabel">IA incerta sugli obiettivi umani</text>
</svg>
<figcaption>Mappa del capitolo 18 — dalla pianificazione con piu' attori alla teoria dei giochi, fino a coalizioni, meccanismi e giochi di assistenza</figcaption>
</figure>

## Piu' attori nello stesso ambiente: coordinare i piani

Il primo passo e' distinguere gli scenari. Se c'e' un solo decisore che pianifica per piu' attori esecutori (ipotesi dell'agente benevolo), il problema e' di pianificazione multiattuatore o multibody: serve gestire la sincronizzazione delle azioni congiunte, ma la mente e' una sola. Se invece ogni attore decide per se', abbiamo veri decisori multipli: quando condividono l'obiettivo, il problema centrale e' il coordinamento; quando le preferenze divergono, serve l'apparato completo della teoria dei giochi.

Sul piano tecnico, il nodo e' la concorrenza: i piani di agenti diversi vengono eseguiti insieme, e occorre un modello di come le azioni interagiscono. Si esaminano tre approcci — l'esecuzione interleaved (tutte le possibili alternanze delle azioni atomiche, corretta ma esponenziale), l'ordinamento parziale e la sincronizzazione perfetta su un orologio globale, che e' il modello adottato per la sua semantica semplice. Gli schemi d'azione vengono estesi con vincoli di azione concorrente: alcune azioni falliscono se eseguite insieme (due tennisti che colpiscono la stessa palla), altre riescono solo se eseguite insieme (due persone che trasportano un oggetto pesante).

Anche con obiettivi e conoscenze condivisi, resta il problema che possono esistere piu' piani congiunti ugualmente validi ma incompatibili tra loro: se ognuno ne sceglie uno diverso, il risultato e' il fallimento. Le vie d'uscita sono le convenzioni (vincoli condivisi sulla scelta, come "si guida a destra"; quando diffuse diventano norme sociali), la comunicazione esplicita, oppure il riconoscimento del piano: osservare le prime mosse dell'altro e dedurne il piano congiunto che sta seguendo.

## Ragionare contro chi ragiona: equilibri e dilemmi

Il modello base della teoria dei giochi non cooperativi e' il gioco in forma normale: giocatori, azioni disponibili e una funzione di payoff che assegna un'utilita' a ogni combinazione di scelte. Il primo concetto di soluzione e' la strategia dominante: una strategia migliore di ogni alternativa qualunque cosa facciano gli altri. Il dilemma del prigioniero mostra il suo lato oscuro: per entrambi i sospettati tradire domina, ma l'esito in cui entrambi tradiscono e' peggiore per tutti e due rispetto al silenzio reciproco. Una soluzione individualmente inattaccabile puo' essere collettivamente pessima.

Quando le strategie dominanti non esistono, il concetto di riferimento e' l'equilibrio di Nash: un profilo di strategie da cui nessun giocatore ha interesse a deviare unilateralmente. Nash dimostro' che, ammettendo strategie miste (scelte randomizzate), ogni gioco ne possiede almeno uno. Il capitolo tratta anche il punto di vista opposto, quello del benessere sociale: la Pareto ottimalita' (nessuno puo' migliorare senza che qualcun altro peggiori), la somma delle utilita' (benessere utilitaristico) e i criteri egualitari. Il dilemma del prigioniero e' un dilemma proprio perche' l'unico equilibrio non e' Pareto-ottimo.

Sul fronte computazionale, per i giochi a somma zero funziona la tecnica maximin di von Neumann: la strategia mista ottima si trova con la programmazione lineare, e il valore del gioco e' garantito contro qualsiasi avversario razionale. Nei giochi a somma non zero il calcolo degli equilibri e' molto piu' costoso, e in pratica si usano euristiche come la miglior risposta iterata, che converge a un equilibrio quando converge.

## Il tempo cambia il gioco: ripetizione e sequenzialita'

Se il dilemma del prigioniero viene giocato piu' volte, la cooperazione puo' emergere — ma solo a certe condizioni. Con un numero di ripetizioni fisso e noto, l'induzione a ritroso la distrugge: l'ultima partita e' un gioco singolo, quindi si tradisce; ma allora anche la penultima, e cosi' via fino alla prima. Con ripetizioni infinite, invece, strategie rappresentabili come macchine a stati finiti — la celebre tit-for-tat, che coopera e poi copia l'ultima mossa altrui, o la piu' spietata "inflessibile", che punisce per sempre alla prima defezione — rendono la cooperazione un equilibrio di Nash. E' il contenuto del folk theorem: la minaccia credibile di ritorsione sostiene esiti cooperativi che nel gioco singolo sarebbero irraggiungibili. Curiosamente, anche limitare la memoria degli agenti (macchine con meno stati delle mosse residue) puo' favorire la cooperazione: non poter contare le ripetizioni equivale a giocare all'infinito.

Per i giochi con turni si usa la forma estesa, un albero di gioco con eventuale giocatore "Caso" per gli eventi aleatori. Con informazione perfetta, l'induzione a ritroso calcola gli equilibri in tempo polinomiale nella dimensione dell'albero; il raffinamento dell'equilibrio perfetto nei sottogiochi elimina gli equilibri basati su minacce non credibili. Con informazione imperfetta (poker, non scacchi) le cose si complicano: gli insiemi informativi raggruppano stati indistinguibili per un giocatore, la conversione in forma normale esplode esponenzialmente, e servono la forma sequenziale di Koller e soprattutto l'astrazione — raggruppare stati e azioni equivalenti — che ha permesso a programmi come Libratus e Pluribus di battere i campioni umani di poker riducendo 10^18 stati a dimensioni trattabili.

Una sezione particolarmente attuale riguarda i giochi di assistenza: un umano e un robot condividono la stessa funzione di payoff, ma solo l'umano ne conosce i parametri. Nel gioco delle graffette, l'umano sceglie per primo e la sua scelta diventa un segnale: il robot ne inferisce le preferenze quanto basta per agire bene, senza che nessuno abbia programmato esplicitamente "insegnare" o "dedurre". E' la formalizzazione dell'IA con benefici dimostrabili: la macchina resta utile proprio perche' e' incerta sugli obiettivi umani e li apprende dall'interazione.

## Coalizioni: chi si allea con chi, e come si divide il valore

La teoria dei giochi cooperativi assume che gli accordi vincolanti siano possibili. Un gioco e' descritto da una funzione caratteristica che assegna a ogni coalizione di giocatori il valore che otterrebbe cooperando. Le due domande centrali sono la stabilita' e l'equita'. Alla prima risponde il nucleo: l'insieme delle distribuzioni di payoff tali che nessuna coalizione guadagnerebbe a staccarsi dalla grande coalizione. Il nucleo puo' essere vuoto (nessuna spartizione e' stabile) o contenere distribuzioni percepite come inique.

Alla seconda domanda risponde il valore di Shapley: a ciascun giocatore spetta il suo contributo marginale medio su tutti i possibili ordini di ingresso nella coalizione. E' l'unica ripartizione che soddisfa quattro assiomi di equita' (efficienza, giocatore fittizio, simmetria, additivita'). Il problema e' computazionale: rappresentare la funzione caratteristica per esteso richiede spazio esponenziale, e verificare che il nucleo non sia vuoto e' spesso co-NP-completo. Rappresentazioni compatte come le reti di contributi marginali permettono pero' di calcolare il valore di Shapley in tempo polinomiale, e la ricerca nel grafo delle strutture di coalizioni offre garanzie di approssimazione per il problema NP-difficile di massimizzare il benessere sociale complessivo.

## Progettare le regole: aste, voto e contrattazione

L'ultima parte rovescia la prospettiva: invece di chiedersi come giocare, si progetta il gioco. Un meccanismo definisce le strategie ammissibili, un centro che raccoglie le scelte e una regola che assegna i payoff. Il contract net protocol e' il decano dell'area: un agente annuncia un compito, gli altri fanno offerte, il migliore lo prende in appalto — lo schema, di fatto, dietro ogni piattaforma di matching tra domanda e offerta.

Per allocare risorse scarse ci sono le aste. L'asta al rialzo (inglese) e' efficiente ma costosa in comunicazione e vulnerabile alla collusione, come mostra il caso storico dell'asta tedesca di frequenze del 1999, in cui due operatori si spartirono i lotti segnalandosi le intenzioni tramite le offerte stesse. L'asta di Vickrey (a busta chiusa, al secondo prezzo) ha la proprieta' preziosa di essere rivelatrice: offrire la propria vera valutazione e' strategia dominante, il che elimina il calcolo strategico ed e' il motivo per cui varianti di questo schema muovono la pubblicita' sui motori di ricerca. La generalizzazione VCG estende l'idea a beni collettivi ed esternalita' — ogni vincitore paga la perdita che la sua presenza impone agli altri — e affronta problemi come la tragedia dei beni comuni, dove la strategia dominante individuale (inquinare) produce il disastro collettivo.

Per aggregare preferenze c'e' il voto. Il paradosso di Condorcet mostra che con tre candidati le preferenze collettive possono essere cicliche; il teorema di Arrow dimostra che nessuna funzione di benessere sociale soddisfa insieme quattro condizioni ragionevoli (Pareto, vincitore di Condorcet, indipendenza dalle alternative irrilevanti, assenza di dittatura); il teorema di Gibbard-Satterthwaite aggiunge che ogni procedura non dittatoriale e' manipolabile con dichiarazioni non veritiere. Non e' la fine della democrazia, ma il promemoria che ogni sistema di voto ha casi patologici.

Infine la contrattazione: nel protocollo a offerte alternate di Rubinstein, con agenti impazienti (fattore di sconto), l'accordo di equilibrio si raggiunge al primo turno e premia il giocatore piu' paziente. Nei domini orientati ai compiti, il protocollo di concessione monotona e la strategia di Zeuthen — concede chi ha piu' da perdere dal conflitto (la minore propensione al rischio), e concede il minimo per invertire i ruoli — producono accordi Pareto-ottimi e individualmente razionali.

## Idee chiave

- Quando nell'ambiente operano altri agenti, la pianificazione richiede coordinamento: piani congiunti corretti non bastano, serve accordarsi su quale eseguire (convenzioni, comunicazione, riconoscimento del piano).
- La teoria dei giochi e' per le decisioni multiagente cio' che la teoria delle decisioni e' per l'agente singolo: descrive il comportamento razionale quando ogni giocatore deve modellare il ragionamento degli altri.
- I concetti di soluzione (strategia dominante, equilibrio di Nash, maximin) caratterizzano gli esiti raggiungibili tra agenti razionali; il dilemma del prigioniero mostra che l'equilibrio puo' non essere Pareto-ottimo.
- La ripetizione cambia gli incentivi: nei giochi iterati all'infinito il folk theorem rende sostenibile la cooperazione tramite minacce credibili di ritorsione.
- Nei giochi in forma estesa l'induzione a ritroso calcola equilibri perfetti nei sottogiochi; con informazione imperfetta servono forma sequenziale e astrazione, le tecniche dietro i programmi che hanno battuto i campioni di poker.
- Nei giochi cooperativi il nucleo identifica le coalizioni stabili e il valore di Shapley e' l'unico modo di dividere il valore che rispetta gli assiomi di equita'.
- La progettazione di meccanismi ribalta il problema: aste rivelatrici (Vickrey, VCG), procedure di voto e protocolli di contrattazione allineano gli incentivi individuali con l'esito collettivo desiderato.
- I teoremi di impossibilita' (Arrow, Gibbard-Satterthwaite) fissano i limiti: nessuna procedura di scelta sociale ragionevole e' insieme completa e immune da manipolazione.
- I giochi di assistenza formalizzano un'IA che resta utile perche' incerta sugli obiettivi umani: l'apprendimento delle preferenze emerge come strategia di equilibrio, non come regola imposta.

## Perche conta oggi

I sistemi costruiti attorno agli [LLM](../kb/concetti/llm.md) stanno rendendo questo capitolo improvvisamente operativo. Le architetture di [multi-agent orchestration](../kb/concetti/multi-agent-orchestration.md) — un agente coordinatore che delega sottocompiti ad agenti specializzati — sono contract net protocol in forma moderna: annuncio del compito, valutazione delle capacita', aggiudicazione. I problemi che il capitolo formalizza (concorrenza tra piani, azioni che interferiscono, necessita' di convenzioni condivise) sono esattamente quelli che un [agent](../kb/concetti/agent.md) incontra quando piu' istanze lavorano sullo stesso codebase o sulla stessa risorsa, e che gli [agent harness](../kb/concetti/agent-harness.md) devono gestire con lock, code e protocolli di comunicazione.

C'e' poi un filo piu' profondo. I giochi di assistenza sono il fondamento teorico dell'allineamento moderno: l'idea che la macchina debba restare incerta sulle preferenze umane e apprenderle dall'interazione e' la stessa che motiva [RLHF](../kb/concetti/rlhf.md) e il design dei [interaction model](../kb/concetti/interaction-model.md) tra utente e assistente. E la progettazione di meccanismi — regole che rendono la strategia onesta quella dominante — e' una lente utile per la [AI governance](../kb/concetti/ai-governance.md): quando piu' attori (aziende, agenti autonomi, piattaforme) interagiscono, non basta chiedere comportamenti virtuosi; bisogna progettare incentivi per cui la virtu' sia l'equilibrio.
