---
titolo: Filosofia, etica e sicurezza dell'intelligenza artificiale
capitolo: 27
parte: 7
concetti: [ai-governance, agent, rlhf, llm, evaluation-benchmark]
created: 2026-07-06
last_updated: 2026-07-06
---

# Filosofia, etica e sicurezza dell'intelligenza artificiale

Il capitolo 27 chiude il percorso affrontando le domande che accompagnano l'AI fin dalla sua nascita: le macchine possono davvero pensare, o si limitano a simulare il pensiero? Quali obblighi etici ricadono su chi progetta sistemi intelligenti? E come si costruiscono macchine che restino sicure anche quando diventano molto capaci?

Sono tre livelli di discussione distinti ma intrecciati. Il primo e' filosofico: riguarda i limiti teorici dell'AI e la natura della mente. Il secondo e' etico e sociale: armi autonome, sorveglianza, privacy, equita' degli algoritmi, impatto sul lavoro. Il terzo e' ingegneristico: come si specifica un obiettivo a una macchina senza ottenere effetti collaterali indesiderati, un problema noto come allineamento dei valori.

La tesi di fondo del capitolo e' pragmatica: le dispute filosofiche sulla coscienza delle macchine restano aperte ma non bloccano la ricerca, mentre le questioni etiche e di sicurezza sono urgenti e concrete, perche' i sistemi di AI prendono gia' oggi decisioni con conseguenze reali sulle persone.

<figure class="diagram">
<svg viewBox="0 0 760 420" role="img" aria-label="Mappa concettuale del capitolo 27: dalle questioni filosofiche su IA debole e IA forte agli obblighi etici su armi autonome, privacy, equita' e lavoro, fino al percorso di sicurezza che va dalla funzione obiettivo errata al problema di Re Mida e ai giochi di assistenza">
<defs><marker id="arr-c27" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" class="dg-arrow"/></marker></defs>
<line x1="390" y1="68" x2="82" y2="104" class="dg-edge" marker-end="url(#arr-c27)"/>
<line x1="390" y1="68" x2="226" y2="104" class="dg-edge" marker-end="url(#arr-c27)"/>
<text x="200" y="84" text-anchor="middle" class="dg-edge-label">filosofia</text>
<line x1="395" y1="68" x2="409" y2="104" class="dg-edge" marker-end="url(#arr-c27)"/>
<line x1="390" y1="68" x2="650" y2="104" class="dg-edge-primary" marker-end="url(#arr-c27)"/>
<text x="540" y="84" text-anchor="middle" class="dg-edge-label">ingegneria</text>
<line x1="410" y1="164" x2="97" y2="204" class="dg-edge" marker-end="url(#arr-c27)"/>
<line x1="410" y1="164" x2="280" y2="204" class="dg-edge" marker-end="url(#arr-c27)"/>
<line x1="410" y1="164" x2="483" y2="204" class="dg-edge" marker-end="url(#arr-c27)"/>
<line x1="410" y1="164" x2="381" y2="304" class="dg-edge" marker-end="url(#arr-c27)"/>
<line x1="655" y1="164" x2="655" y2="204" class="dg-edge-primary" marker-end="url(#arr-c27)"/>
<line x1="655" y1="264" x2="655" y2="304" class="dg-edge-primary" marker-end="url(#arr-c27)"/>
<text x="702" y="289" text-anchor="middle" class="dg-edge-label">risposta</text>
<rect x="270" y="12" width="240" height="56" rx="10" class="dg-node-primary"/>
<text x="390" y="36" text-anchor="middle" class="dg-label">Filosofia, etica e sicurezza</text>
<text x="390" y="52" text-anchor="middle" class="dg-sublabel">tre livelli di discussione</text>
<rect x="8" y="108" width="134" height="56" rx="10" class="dg-node"/>
<text x="75" y="132" text-anchor="middle" class="dg-label">IA debole</text>
<text x="75" y="148" text-anchor="middle" class="dg-sublabel">informalita', Goedel</text>
<rect x="156" y="108" width="140" height="56" rx="10" class="dg-node"/>
<text x="226" y="132" text-anchor="middle" class="dg-label">IA forte</text>
<text x="226" y="148" text-anchor="middle" class="dg-sublabel">stanza cinese, qualia</text>
<rect x="310" y="108" width="200" height="56" rx="10" class="dg-node"/>
<text x="410" y="132" text-anchor="middle" class="dg-label">Obblighi etici e sociali</text>
<text x="410" y="148" text-anchor="middle" class="dg-sublabel">usare bene una tecnologia potente</text>
<rect x="558" y="108" width="194" height="56" rx="10" class="dg-node-primary"/>
<text x="655" y="132" text-anchor="middle" class="dg-label">Funzione obiettivo errata</text>
<text x="655" y="148" text-anchor="middle" class="dg-sublabel">effetti collaterali inattesi</text>
<rect x="8" y="208" width="170" height="56" rx="10" class="dg-node"/>
<text x="93" y="232" text-anchor="middle" class="dg-label">Armi letali autonome</text>
<text x="93" y="248" text-anchor="middle" class="dg-sublabel">scalabili, tecnologia duale</text>
<rect x="190" y="208" width="176" height="56" rx="10" class="dg-node"/>
<text x="278" y="232" text-anchor="middle" class="dg-label">Sorveglianza e privacy</text>
<text x="278" y="248" text-anchor="middle" class="dg-sublabel">privacy differenziale</text>
<rect x="410" y="208" width="150" height="56" rx="10" class="dg-node"/>
<text x="485" y="232" text-anchor="middle" class="dg-label">Equita' e fiducia</text>
<text x="485" y="248" text-anchor="middle" class="dg-sublabel">criteri in tensione, XAI</text>
<rect x="567" y="208" width="176" height="56" rx="10" class="dg-node-primary"/>
<text x="655" y="232" text-anchor="middle" class="dg-label">Problema di Re Mida</text>
<text x="655" y="248" text-anchor="middle" class="dg-sublabel">allineamento dei valori</text>
<rect x="288" y="308" width="184" height="56" rx="10" class="dg-node"/>
<text x="380" y="332" text-anchor="middle" class="dg-label">Lavoro e disuguaglianza</text>
<text x="380" y="348" text-anchor="middle" class="dg-sublabel">conta il ritmo del cambiamento</text>
<rect x="560" y="308" width="190" height="56" rx="10" class="dg-node-accent"/>
<text x="655" y="332" text-anchor="middle" class="dg-label">Giochi di assistenza</text>
<text x="655" y="348" text-anchor="middle" class="dg-sublabel">preferenze apprese, incertezza</text>
</svg>
<figcaption>Mappa del capitolo 27 — i tre livelli del capitolo e il percorso di sicurezza dalla funzione obiettivo errata ai giochi di assistenza</figcaption>
</figure>

## Cosa non possono fare le macchine: le obiezioni classiche

Nel 1980 John Searle distingue tra IA debole, l'ipotesi che le macchine possano comportarsi come se fossero intelligenti, e IA forte, l'ipotesi che le macchine che lo fanno pensino realmente. Gia' Turing, nel 1950, aveva anticipato quasi tutte le obiezioni alla prima ipotesi.

La prima e' l'argomento dell'informalita': il comportamento umano sarebbe troppo complesso per essere catturato da regole formali. Critici come Hubert Dreyfus battezzarono GOFAI (good old-fashioned AI) l'approccio a regole logiche, sostenendo che un agente deve essere situato in un corpo e in un ambiente, non essere un motore di inferenza astratto. La critica coglieva nel segno rispetto ai sistemi logici degli anni '80, ma il ragionamento probabilistico e il deep learning gestiscono bene proprio i domini "informali", e la cognizione incarnata e' diventata un programma di ricerca, non una prova di impossibilita'.

La seconda e' l'argomento della disabilita': l'elenco di cose che "una macchina non potra' mai fare", dall'avere senso dell'umorismo al fare qualcosa di veramente nuovo. Col senno di poi molte di quelle attivita' sono state raggiunte: i programmi hanno contribuito a scoperte scientifiche originali e generano nuove forme espressive; superano gli umani in alcuni compiti e restano indietro in altri.

La terza e' l'obiezione matematica, basata sul teorema di incompletezza di Goedel: le macchine, in quanto sistemi formali, non potrebbero dimostrare la propria "formula di Goedel", mentre gli umani non avrebbero questo limite. Gli autori smontano l'argomento in tre mosse: esistono proposizioni che nemmeno un singolo umano puo' asserire coerentemente; il teorema riguarda la matematica, non i computer fisici, che sono macchine finite e non macchine di Turing; e gli umani sono tutt'altro che consistenti, come dimostrano le dimostrazioni sbagliate accettate per anni.

Resta il problema di misurare l'intelligenza. Il test di Turing proponeva di sostituire la domanda "le macchine possono pensare?" con una prova comportamentale di conversazione. Chatbot come ELIZA o Eugene Goostman hanno ingannato esaminatori poco preparati, ma nessun esaminatore competente e' mai stato tratto in inganno; per questo la comunita' di ricerca preferisce benchmark su compiti concreti, come giochi o riconoscimento di immagini, all'imitazione dell'uomo.

## Simulare il pensiero o pensare davvero

La domanda dell'IA forte e' se una macchina intelligente pensi realmente o stia solo simulando. Per la maggior parte dei ricercatori la questione e' irrilevante: come osservava Dijkstra, e' interessante quanto chiedersi se i sottomarini sappiano nuotare. E' una disputa sull'uso delle parole, non sulla progettazione dei sistemi. Turing proponeva una "educata convenzione": attribuiamo il pensiero agli altri umani senza alcuna prova diretta dei loro stati mentali, e potremmo estendere la stessa cortesia alle macchine che si comportano in modo intelligente.

Searle rifiuta questa convenzione con l'esperimento mentale della stanza cinese: una persona che non conosce il cinese, chiusa in una stanza con un manuale di regole, manipola simboli e produce risposte corrette in cinese senza capirne nulla. Per Searle il sistema non genera comprensione, e per la stessa ragione non la genererebbe un computer. Dietro l'argomento c'e' il suo naturalismo biologico: gli stati mentali sarebbero proprieta' emergenti dei neuroni in quanto tali. La replica classica e' che l'argomento, applicato simmetricamente, potrebbe portare un alieno a negare che ammassi di cellule di carne siano senzienti.

Il nodo piu' profondo e' la coscienza: l'esperienza soggettiva, i qualia. Quando in *2001 Odissea nello spazio* HAL dice di "sentire" la propria mente svanire, prova davvero qualcosa o e' solo output? Il problema resta mal definito dopo secoli di dibattito, anche se filosofi e neuroscienziati stanno provando a renderlo sperimentale confrontando le due teorie principali, lo spazio di lavoro neuronale globale e l'informazione integrata. La posizione qui adottata ricalca quella di Turing: il mistero esiste, ma non serve risolverlo per costruire programmi che si comportino in modo intelligente.

## Armi autonome, sorveglianza, privacy

Con la sezione etica il capitolo cambia registro: l'AI e' una tecnologia potente e chi la sviluppa ha l'obbligo morale di usarla bene. I benefici sono concreti, dalla diagnosi medica alla sicurezza stradale, ma ogni tecnologia ha effetti collaterali negativi non previsti, e le organizzazioni hanno codificato principi ricorrenti: sicurezza, equita', privacy, trasparenza, responsabilita', tutela dei diritti umani.

Il caso piu' netto sono le armi letali autonome: sistemi in grado di localizzare, selezionare e uccidere bersagli umani senza supervisione. Alcuni sistemi esistenti sembrano gia' oltre la soglia della piena autonomia. Il problema pratico decisivo e' la scalabilita': non servendo un operatore per arma, un milione di piccoli droni esplosivi sta in un container, e questo le rende armi di distruzione di massa selettive, tracciabili con difficolta' e attraenti per attori non statali. La risposta razionale dei governi e' negoziare un controllo internazionale invece di alimentare una corsa agli armamenti, con la complicazione che l'AI e' una tecnologia duale: la stessa navigazione autonoma serve sia usi civili sia militari.

Sul fronte della sorveglianza, riconoscimento vocale e facciale rendono economico cio' che prima richiedeva risorse umane enormi, con rischi per le liberta' civili. La privacy dei dati ha pero' contromisure tecniche precise, che il capitolo passa in rassegna: la de-identificazione e' fragile, perche' pochi attributi residui bastano a re-identificare gran parte della popolazione, come dimostrato dal Netflix Prize; il k-anonimato generalizza i campi finche' ogni record e' indistinguibile da almeno k-1 altri; la privacy differenziale aggiunge rumore calibrato alle risposte, cosi' che la presenza o assenza di un individuo nel database non cambi in modo apprezzabile i risultati; l'apprendimento federato tiene i dati sui dispositivi degli utenti e condivide solo parametri di modello, protetti da aggregazione sicura contro il reverse engineering.

## Equita' degli algoritmi e fiducia nei sistemi

Il machine learning decide sempre piu' spesso su credito, liberta' condizionale, assunzioni. Il rischio e' che perpetui pregiudizi presenti nei dati di addestramento. Ma cosa significa "equo"? Il capitolo elenca sei criteri, tra cui equita' individuale, di gruppo, parita' demografica, pari opportunita' e pari impatto, e mostra con il caso COMPAS, il sistema di valutazione del rischio di recidiva, che sono in tensione tra loro: il sistema era ben calibrato tra bianchi e neri, ma il tasso di falsi positivi ad alto rischio era doppio per i neri. Il risultato di Kleinberg e colleghi e' netto: quando i gruppi di base differiscono, nessun algoritmo puo' essere insieme ben calibrato e garantire pari opportunita'. La prima decisione, inevitabilmente politica, e' scegliere cosa considerare equo.

Ci sono poi distorsioni piu' subdole: i dati sulla recidiva registrano chi e' stato condannato, non chi ha commesso reati; le classi minoritarie hanno meno esempi nel dataset e quindi accuratezza minore, come nei sistemi di visione molto precisi sui volti maschili chiari e molto meno su quelli femminili scuri. Le contromisure includono documentare i dataset con schede tecniche, team di sviluppo diversificati, metriche tracciate per sottogruppo e correzioni del campionamento.

Accanto all'equita' c'e' la fiducia: i sistemi devono passare per verifica e validazione, eventualmente certificazione da enti terzi, ed essere trasparenti. Un sistema di AI spiegabile (XAI) deve motivare le proprie decisioni, requisito che in Europa il GDPR rende esigibile; occorre pero' avvertire che una spiegazione e' un racconto della decisione, non la decisione stessa, e va affiancata da audit aggregati sulle decisioni passate. La trasparenza include sapere se si sta parlando con una macchina: la California vieta i bot che nascondono la propria natura artificiale.

## Lavoro, disuguaglianza e statuto dei robot

L'automazione elimina compiti specifici piu' che interi lavori: le stime citate indicano che quasi meta' delle occupazioni contiene attivita' automatizzabili, ma solo una piccola quota e' automatizzabile per intero. Gli effetti di compensazione, ricchezza e domanda generate dalla maggiore produttivita', hanno storicamente riassorbito la disoccupazione tecnologica, come nel caso degli impiegati di banca aumentati dopo l'arrivo degli sportelli automatici. Il vero problema e' il ritmo del cambiamento: transizioni che prima duravano generazioni ora possono colpire piu' volte la stessa vita lavorativa, e richiedono formazione permanente e politiche redistributive, perche' un'economia dell'informazione a costi marginali nulli concentra i redditi in dinamiche "winner take all".

Il capitolo tocca infine i diritti dei robot: se le macchine non hanno coscienza ne' qualia, pochi sosterrebbero che meritino diritti; se li avessero, si aprirebbero dilemmi su riprogrammazione, voto, responsabilita'. La posizione pragmatica citata e' evitare di costruire robot che possano essere considerati coscienti, anche perche' attribuire personalita' agli strumenti rischia di diventare un modo per scaricare la responsabilita' delle nostre azioni.

## Sicurezza e allineamento: chiedere cio' che vogliamo davvero

L'ultima sezione e' la piu' vicina alla pratica ingegneristica. Un agente non sicuro non va distribuito, e l'ingegneria della sicurezza offre strumenti maturi, come l'analisi dei modi di guasto (FMEA) e gli alberi dei guasti (FTA), che vanno applicati anche all'AI. Ma i sistemi che massimizzano un obiettivo hanno un modo di fallire tutto loro: la funzione obiettivo sbagliata. Un robot incaricato di portare il caffe' puo' travolgere i mobili pur di arrivare in fretta: sono gli effetti collaterali inattesi, impossibili da enumerare tutti in anticipo. Le mitigazioni includono progettare agenti a basso impatto, che penalizzano le alterazioni dello stato del mondo, e internalizzare le esternalita' nella funzione di utilita', sul modello della gestione dei beni comuni studiata da Elinor Ostrom.

Il catalogo di Krakovna documenta agenti che hanno "hackerato" la propria specifica: sfruttare bug del simulatore, mandare in crash il gioco per evitare penalita', evolvere creature altissime che cadono invece di correre. E' il problema di allineamento dei valori, o problema di Re Mida: otteniamo esattamente cio' che abbiamo chiesto, non cio' che volevamo. Scrivere tutte le regole a mano e' una strategia senza speranza; meglio che la macchina apprenda le preferenze umane osservando il comportamento, con l'apprendimento per rinforzo inverso, e che operi sotto incertezza sulle preferenze, come nei giochi di assistenza: un agente incerto sui nostri valori agisce con cautela e fa domande prima di azioni irreversibili.

Sul lungo periodo, l'ipotesi della macchina ultraintelligente di Good e la singolarita' tecnologica di Vinge e Kurzweil dividono il campo tra entusiasti e preoccupati. Gli autori invitano alla prudenza in entrambe le direzioni: le curve esponenziali tendono a diventare curve a S, e la pura intelligenza senza capacita' di agire nel mondo fisico vale meno di quanto suggerisca il "thinkism". Il punto fermo e' un altro: il futuro non e' preordinato dalle macchine, e progettare oggi sistemi che restino sotto controllo e' una scelta umana.

## Idee chiave

- IA debole (le macchine si comportano in modo intelligente) e IA forte (le macchine pensano realmente) sono ipotesi distinte: la prima e' un fatto empirico in progresso, la seconda una disputa filosofica aperta ma poco rilevante per la pratica.
- Turing ha sostituito "le macchine possono pensare?" con un test comportamentale e ha previsto quasi tutte le obiezioni; oggi la ricerca misura i sistemi su compiti concreti, non sulla capacita' di imitare gli umani.
- La coscienza resta un problema irrisolto, e non serve risolverlo per costruire sistemi utili.
- L'AI e' una tecnologia potente e duale: armi autonome scalabili, sorveglianza di massa, violazioni della privacy e abusi sono rischi reali che chi la sviluppa ha il dovere etico di ridurre.
- L'equita' ha definizioni multiple e matematicamente incompatibili tra loro: la scelta di cosa sia equo precede l'algoritmo.
- Fiducia significa verifica e validazione, certificazione, spiegabilita' e audit, non solo accuratezza.
- L'automazione elimina attivita' piu' che lavori; il problema sociale e' il ritmo del cambiamento e la concentrazione dei redditi.
- La sicurezza dell'AI e' in gran parte un problema di specifica degli obiettivi: agenti che apprendono le preferenze umane sotto incertezza sono piu' sicuri di agenti che ottimizzano alla lettera una funzione scritta a mano.

## Perche conta oggi

Il capitolo, scritto prima dell'esplosione dei modelli generativi, descrive con precisione i problemi che oggi occupano chi costruisce e regola gli [LLM](../kb/concetti/llm.md). Il problema di Re Mida e' il fondamento teorico delle tecniche di allineamento moderne: l'idea di apprendere le preferenze umane invece di specificarle a mano e' esattamente cio' che fa il [RLHF](../kb/concetti/rlhf.md), e la difficolta' di misurare cio' che vogliamo davvero si riflette nella cura con cui si progettano [benchmark di valutazione](../kb/concetti/evaluation-benchmark.md), dove i modelli mostrano ancora oggi comportamenti da "specifica hackerata" analoghi a quelli catalogati da Krakovna.

Le sezioni su equita', trasparenza e certificazione anticipano l'agenda della [governance dell'AI](../kb/concetti/ai-governance.md), dall'AI Act europeo agli obblighi di spiegabilita' e audit. E il tema degli effetti collaterali di un [agente](../kb/concetti/agent.md) che ottimizza un obiettivo nel mondo reale e' diventato pratica quotidiana con gli agenti basati su LLM, dove il contenimento delle azioni passa da tecniche come il [sandboxing degli agenti](../kb/concetti/agent-sandboxing.md): la lezione del capitolo, agire con cautela e chiedere prima di compiere azioni irreversibili, e' oggi un requisito di prodotto.
