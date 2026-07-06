---
titolo: Pianificazione automatica
capitolo: 11
parte: 3
volume: 1
pagine: "353-394"
concetti: [agent, world-models, chain-of-thought, tool-use]
created: 2026-07-06
last_updated: 2026-07-06
---

# Pianificazione automatica

Come fa un agente a costruire in modo efficiente una sequenza di azioni che lo porti da dove si trova a dove vuole arrivare? E' la domanda al centro di questo capitolo. La ricerca nello spazio degli stati e la deduzione logica, viste nei capitoli precedenti, funzionano ma soffrono di due debolezze condivise: richiedono euristiche costruite a mano per ogni nuovo dominio e rappresentano gli stati in modo esplicito, con una crescita esponenziale che le rende impraticabili su problemi realistici.

La risposta della comunita' di ricerca e' una rappresentazione fattorizzata: invece di trattare ogni stato come un blocco atomico, lo si descrive come combinazione di proprieta' elementari, e le azioni come regole generali che leggono e modificano quelle proprieta'. Questa scelta, apparentemente solo notazionale, cambia tutto: rende possibile derivare automaticamente euristiche indipendenti dal dominio e comprimere spazi di ricerca enormi.

Il capitolo conta perche' la pianificazione e' il punto di incontro tra le due anime storiche dell'AI, la ricerca e la logica, e perche' i temi che tocca — scomporre obiettivi complessi in sottopassi, agire con informazione incompleta, monitorare l'esecuzione e correggere il tiro — sono esattamente quelli che oggi riemergono nella progettazione di sistemi agentici basati su LLM.

<figure class="diagram">
<svg viewBox="0 0 760 400" role="img" aria-label="Mappa concettuale del capitolo 11: la pianificazione classica descritta con la rappresentazione fattorizzata PDDL, gli algoritmi di ricerca in avanti, all'indietro e SAT, le euristiche automatiche, le gerarchie HTN, gli stati-credenza, la pianificazione online e lo scheduling">
<defs><marker id="arr-c11" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" class="dg-arrow"/></marker></defs>
<line x1="385" y1="68" x2="385" y2="97" class="dg-edge-primary" marker-end="url(#arr-c11)"/>
<line x1="318" y1="68" x2="112" y2="97" class="dg-edge" marker-end="url(#arr-c11)"/>
<text x="215" y="76" text-anchor="middle" class="dg-edge-label">incertezza</text>
<path d="M490,32 L746,32 L746,320" class="dg-edge" marker-end="url(#arr-c11)"/>
<text x="630" y="24" text-anchor="middle" class="dg-edge-label">aggiunge tempo e risorse</text>
<line x1="515" y1="128" x2="569" y2="128" class="dg-edge" marker-end="url(#arr-c11)"/>
<text x="542" y="120" text-anchor="middle" class="dg-edge-label">estende</text>
<line x1="275" y1="156" x2="185" y2="321" class="dg-edge-primary" marker-end="url(#arr-c11)"/>
<line x1="350" y1="156" x2="329" y2="209" class="dg-edge" marker-end="url(#arr-c11)"/>
<line x1="420" y1="156" x2="505" y2="209" class="dg-edge" marker-end="url(#arr-c11)"/>
<line x1="500" y1="156" x2="655" y2="209" class="dg-edge" marker-end="url(#arr-c11)"/>
<text x="600" y="168" text-anchor="middle" class="dg-edge-label">proposizionalizza</text>
<line x1="98" y1="156" x2="98" y2="209" class="dg-edge" marker-end="url(#arr-c11)"/>
<text x="170" y="186" text-anchor="middle" class="dg-edge-label">durante l'esecuzione</text>
<line x1="240" y1="324" x2="315" y2="271" class="dg-edge" marker-end="url(#arr-c11)"/>
<text x="272" y="300" text-anchor="middle" class="dg-edge-label">rende praticabile</text>
<rect x="280" y="12" width="210" height="56" rx="10" class="dg-node"/>
<text x="385" y="36" text-anchor="middle" class="dg-label">Pianificazione classica</text>
<text x="385" y="52" text-anchor="middle" class="dg-sublabel">deterministico e osservabile</text>
<rect x="255" y="100" width="260" height="56" rx="10" class="dg-node-primary"/>
<text x="385" y="124" text-anchor="middle" class="dg-label">Rappresentazione fattorizzata</text>
<text x="385" y="140" text-anchor="middle" class="dg-sublabel">PDDL: fluenti e schemi di azione</text>
<rect x="8" y="100" width="180" height="56" rx="10" class="dg-node"/>
<text x="98" y="124" text-anchor="middle" class="dg-label">Stati-credenza</text>
<text x="98" y="140" text-anchor="middle" class="dg-sublabel">conformante e condizionale</text>
<rect x="572" y="100" width="164" height="56" rx="10" class="dg-node"/>
<text x="654" y="124" text-anchor="middle" class="dg-label">Gerarchica (HTN)</text>
<text x="654" y="140" text-anchor="middle" class="dg-sublabel">HLA e semantica angelica</text>
<rect x="8" y="212" width="180" height="56" rx="10" class="dg-node-accent"/>
<text x="98" y="236" text-anchor="middle" class="dg-label">Pianificazione online</text>
<text x="98" y="252" text-anchor="middle" class="dg-sublabel">monitora e ripianifica</text>
<rect x="250" y="212" width="158" height="56" rx="10" class="dg-node"/>
<text x="329" y="236" text-anchor="middle" class="dg-label">Ricerca in avanti</text>
<text x="329" y="252" text-anchor="middle" class="dg-sublabel">dallo stato iniziale</text>
<rect x="426" y="212" width="158" height="56" rx="10" class="dg-node"/>
<text x="505" y="236" text-anchor="middle" class="dg-label">Ricerca all'indietro</text>
<text x="505" y="252" text-anchor="middle" class="dg-sublabel">solo azioni rilevanti</text>
<rect x="604" y="212" width="136" height="56" rx="10" class="dg-node"/>
<text x="672" y="236" text-anchor="middle" class="dg-label">Codifica SAT</text>
<text x="672" y="252" text-anchor="middle" class="dg-sublabel">sistema SATPlan</text>
<rect x="60" y="324" width="240" height="56" rx="10" class="dg-node"/>
<text x="180" y="348" text-anchor="middle" class="dg-label">Euristiche automatiche</text>
<text x="180" y="364" text-anchor="middle" class="dg-sublabel">rilassamenti, astrazioni, scomposizione</text>
<rect x="560" y="324" width="192" height="56" rx="10" class="dg-node"/>
<text x="656" y="348" text-anchor="middle" class="dg-label">Scheduling</text>
<text x="656" y="364" text-anchor="middle" class="dg-sublabel">tempo, risorse, cammino critico</text>
</svg>
<figcaption>Mappa del capitolo 11 — la rappresentazione fattorizzata PDDL al centro: algoritmi di ricerca, euristiche automatiche, gerarchie, incertezza e scheduling</figcaption>
</figure>

## Descrivere il mondo a fattori: il linguaggio PDDL

La pianificazione classica assume un ambiente discreto, deterministico, statico e completamente osservabile. In questo quadro, il linguaggio PDDL (planning domain definition language) descrive uno stato come una congiunzione di fatti elementari ground (senza variabili), detti fluenti, con la convenzione che tutto cio' che non e' menzionato e' falso. Un problema di consegne, per esempio, si riduce a fatti come "il camion 1 e' a Melbourne" e "il pacco A e' sul camion 1".

Le azioni sono definite tramite schemi: un nome con variabili, una precondizione (cosa deve valere per poter agire) e un effetto (quali fluenti l'azione aggiunge e quali elimina). Un unico schema "Vola(aereo, da, a)" cattura tutte le possibili tratte di tutti gli aerei; e' questa compattezza che manca alle rappresentazioni atomiche. Il risultato di un'azione si calcola con una regola meccanica: si tolgono dallo stato i fluenti negati dall'effetto e si aggiungono quelli affermati.

<figure class="diagram">
<svg viewBox="0 0 760 260" role="img" aria-label="Schema di azione PDDL Vola: la precondizione elenca i fluenti che devono valere nello stato, l'effetto i fluenti eliminati e aggiunti, e sostituendo le variabili con costanti si ottiene l'azione ground Vola P1 SFO JFK">
<defs><marker id="arr-c11-b" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" class="dg-arrow"/></marker></defs>
<line x1="198" y1="100" x2="287" y2="100" class="dg-edge" marker-end="url(#arr-c11-b)"/>
<text x="242" y="92" text-anchor="middle" class="dg-edge-label">se vale in s</text>
<line x1="470" y1="100" x2="557" y2="100" class="dg-edge" marker-end="url(#arr-c11-b)"/>
<text x="513" y="92" text-anchor="middle" class="dg-edge-label">risultato</text>
<line x1="380" y1="128" x2="380" y2="187" class="dg-edge" marker-end="url(#arr-c11-b)"/>
<text x="475" y="162" text-anchor="middle" class="dg-edge-label">istanzia le variabili</text>
<rect x="8" y="48" width="190" height="104" rx="10" class="dg-node"/>
<text x="103" y="72" text-anchor="middle" class="dg-label">Precondizione</text>
<text x="103" y="90" text-anchor="middle" class="dg-sublabel">Posizione(p, da)</text>
<text x="103" y="106" text-anchor="middle" class="dg-sublabel">Aereo(p)</text>
<text x="103" y="122" text-anchor="middle" class="dg-sublabel">Aeroporto(da)</text>
<text x="103" y="138" text-anchor="middle" class="dg-sublabel">Aeroporto(a)</text>
<rect x="290" y="72" width="180" height="56" rx="10" class="dg-node-primary"/>
<text x="380" y="96" text-anchor="middle" class="dg-label">Azione</text>
<text x="380" y="112" text-anchor="middle" class="dg-sublabel">Vola(p, da, a)</text>
<rect x="560" y="64" width="192" height="72" rx="10" class="dg-node"/>
<text x="656" y="88" text-anchor="middle" class="dg-label">Effetto</text>
<text x="656" y="106" text-anchor="middle" class="dg-sublabel">¬Posizione(p, da)</text>
<text x="656" y="122" text-anchor="middle" class="dg-sublabel">Posizione(p, a)</text>
<rect x="270" y="190" width="220" height="56" rx="10" class="dg-node"/>
<text x="380" y="214" text-anchor="middle" class="dg-label">Azione ground</text>
<text x="380" y="230" text-anchor="middle" class="dg-sublabel">Vola(P1, SFO, JFK)</text>
</svg>
<figcaption>Schema di azione Vola in PDDL — precondizione, effetto e istanza ground; schema ripreso dal Paragrafo 11.1 e dalla Figura 11.1 del cap. 11, AIMA 4a ed.</figcaption>
</figure>

Il libro illustra il formalismo con tre domini che sono diventati classici: il trasporto aereo di merci (caricare, scaricare, volare), il cambio di una ruota bucata e il mondo dei blocchi, dove un braccio robotico impila cubi su un tavolo. Sono esempi giocattolo, ma mostrano anche le insidie della modellazione: definire correttamente cosa significa "libero" per un blocco o per il tavolo richiede piu' attenzione di quanto sembri, e un modello impreciso produce piani sbagliati o spazi di ricerca inutilmente grandi.

## Cercare un piano: in avanti, all'indietro, o come formula logica

Dato un problema PDDL, la strada piu' diretta e' la ricerca in avanti (progressione): si parte dallo stato iniziale e si applicano azioni finche' non si raggiunge l'obiettivo. Il problema e' il fattore di ramificazione: in un dominio di trasporto con decine di aerei e centinaia di pacchi, ogni stato puo' avere migliaia di azioni applicabili, e anche istanze concettualmente banali diventano intrattabili senza una buona euristica.

L'alternativa e' la ricerca all'indietro (regressione): si parte dall'obiettivo e si applicano le azioni "al contrario", chiedendosi quali stati precedenti porterebbero a quello desiderato. Il vantaggio e' che si considerano solo le azioni rilevanti, cioe' quelle i cui effetti contribuiscono all'obiettivo, e il fattore di ramificazione crolla. Un esempio efficace: per l'obiettivo "possedere il libro con un certo ISBN", la ricerca in avanti dovrebbe enumerare miliardi di possibili acquisti, quella all'indietro unifica direttamente l'obiettivo con l'effetto dell'unica azione utile. Lo svantaggio e' che si lavora con insiemi di stati descritti da formule con variabili, e su questi e' piu' difficile definire euristiche accurate: per questo la maggior parte dei sistemi moderni preferisce la ricerca in avanti.

Una terza via traduce il problema in soddisfacibilita' booleana: si "proposizionalizzano" azioni e obiettivi su un orizzonte temporale fissato e si affida tutto a un risolutore SAT, come fa il sistema SATPlan. La formula risultante e' molto piu' lunga della descrizione PDDL originale, ma i risolutori moderni la gestiscono. Esistono poi approcci storici come Graphplan (basato su un grafo di pianificazione) e la pianificazione con ordinamento parziale, che rappresenta il piano come grafo di azioni con soli i vincoli di precedenza davvero necessari: oggi non e' piu' competitiva in velocita', ma resta usata dove gli umani devono leggere e validare i piani, per esempio nelle operazioni dei veicoli spaziali.

## Euristiche gratis: il dividendo della rappresentazione fattorizzata

Il vero guadagno della rappresentazione fattorizzata e' che le euristiche si possono derivare automaticamente, rilassando il problema in modi sistematici. Ignorare le precondizioni rende ogni azione sempre applicabile e trasforma la stima del costo in un problema di copertura di insiemi; ignorare le liste di eliminazioni (gli effetti negativi) produce un problema in cui nessuna azione disfa il lavoro di un'altra, quindi il progresso verso l'obiettivo e' monotono e una semplice hill climbing trova soluzioni senza vicoli ciechi. Rimuovere precondizioni selezionate da uno schema di azione genera meccanicamente euristiche note, come la distanza Manhattan per il gioco del quindici.

Un secondo asse di attacco e' l'astrazione di stato: si ignorano fluenti irrilevanti per il problema specifico, mappando molti stati concreti su uno astratto e riducendo lo spazio di ordini di grandezza. Un terzo e' la scomposizione: si divide l'obiettivo in sottoinsiemi, si risolve ciascuno indipendentemente e si combinano le stime — sommandole si ottiene un'euristica accurata e ammissibile quando i sotto-obiettivi sono davvero indipendenti. A questi si aggiungono potature indipendenti dal dominio, come la riduzione simmetrica (tra stati equivalenti a meno di una permutazione se ne esplora uno solo) e lo sfruttamento dei sotto-obiettivi serializzabili, che si possono raggiungere in un ordine tale da non dover mai disfare quelli gia' completati: e' il trucco che ha permesso al pianificatore Remote Agent della NASA di controllare in tempo reale la sonda Deep Space One. Il sistema FF (FastForward), vincitore di gare internazionali, combina ricerca in avanti, euristica che ignora le eliminazioni e una hill climbing potenziata.

## Pianificare per livelli: gerarchie di azioni

Pianificare una vacanza in termini di comandi motori richiederebbe miliardi di azioni. Gli umani ragionano per livelli di astrazione, e la pianificazione gerarchica (HTN, hierarchical task network) formalizza questa intuizione: accanto alle azioni primitive esistono azioni di alto livello (HLA), come "vai all'aeroporto", ciascuna con uno o piu' raffinamenti possibili in sequenze di azioni piu' fini (guidare e parcheggiare, oppure prendere un taxi). Il beneficio computazionale e' potenzialmente esponenziale: con una libreria di raffinamenti piccola e ben fatta, il costo della ricerca puo' passare da esponenziale a quasi lineare nella lunghezza della soluzione.

L'algoritmo di base sostituisce ripetutamente una HLA con uno dei suoi raffinamenti finche' il piano diventa tutto primitivo e raggiunge l'obiettivo. Ma raffinare fino alle azioni primitive per verificare un piano tradisce lo spirito dell'astrazione: vorremmo poter certificare un piano di alto livello senza scendere nei dettagli. Qui il libro introduce la semantica angelica: poiche' e' l'agente stesso (non un avversario) a scegliere quale implementazione eseguire, a ogni HLA si associa un insieme raggiungibile di stati, e un piano astratto funziona se tale insieme interseca gli stati obiettivo. Con descrizioni approssimate — ottimistiche e pessimistiche — si possono scartare subito i piani che certamente falliscono e adottare con fiducia quelli che certamente funzionano, rimandando il raffinamento solo ai casi ambigui. E' un modello fedele di come deliberiamo noi: decidiamo "due settimane alle Hawaii" e lasciamo i dettagli dei voli a dopo.

## Quando il mondo non collabora: incertezza, percezione, ripianificazione

La pianificazione classica assume di sapere tutto. Il capitolo la estende in tre direzioni, usando come filo conduttore un problema semplice: verniciare una sedia e un tavolo dello stesso colore senza conoscere i colori di partenza.

La pianificazione senza sensori (o conformante) cerca un piano che funzioni qualunque sia lo stato reale: l'agente ragiona su stati-credenza, insiemi di mondi possibili rappresentati come formule logiche. La mossa vincente e' aprire un barattolo e verniciare entrambi i mobili con quello, costringendo il mondo nell'obiettivo anche senza mai osservarlo. Il capitolo mostra che, se lo stato-credenza resta una congiunzione di letterali, l'aggiornamento e' quasi identico al caso osservabile e la rappresentazione resta compatta; gli effetti condizionali delle azioni, pero', possono farla esplodere, e allora servono approssimazioni conservative o il calcolo pigro via risolutore SAT.

La pianificazione condizionale genera piani con ramificazioni basate sulle percezioni: PDDL viene esteso con schemi di percezione che descrivono cosa l'agente osservera' e quando. Il piano diventa un albero di if-then-else: osserva i colori, e vernicia solo se serve.

La pianificazione online, infine, accetta che nessun piano sopravvive intatto al contatto con la realta': l'agente monitora l'esecuzione e ripianifica quando qualcosa va storto. Il monitoraggio puo' riguardare la singola azione (le precondizioni valgono ancora?), il piano residuo (porta ancora all'obiettivo? cosi' si rileva presto il fallimento e, in caso di aiuto esterno inatteso, anche la serendipita' di un obiettivo gia' raggiunto) o gli obiettivi stessi (ne e' comparso uno migliore?). La ripianificazione ripara il piano cercando il ricongiungimento piu' economico con quello originale. Il limite di fondo resta il modello: se un'azione fallisce sempre per una causa che l'agente non rappresenta (un barattolo vuoto), riprovare all'infinito non serve; la via d'uscita e' apprendere un modello migliore dai fallimenti.

## Tempo, scadenze e risorse limitate

La pianificazione classica dice cosa fare e in che ordine, non quanto dura ne' quando. Lo scheduling aggiunge durate, vincoli temporali e risorse: consumabili (i bulloni) o riusabili (un ispettore, occupato durante il compito ma poi di nuovo disponibile), rappresentate come quantita' aggregate anziche' come individui, il che riduce drasticamente la combinatoria. L'approccio tipico e' "prima pianifica, poi schedula".

Senza vincoli di risorse, minimizzare la durata totale (makespan) e' facile: il metodo del cammino critico calcola per ogni azione la finestra tra inizio piu' precoce e piu' tardivo; le azioni senza margine formano il cammino critico che determina la durata dell'intero piano. Ma appena le risorse impongono che due azioni non si sovrappongano, i vincoli diventano disgiuntivi e il problema NP-difficile: si ricorre a branch-and-bound, ricerca tabu' o a euristiche greedy come quella del margine minimo, che funzionano bene in pratica pur senza garanzie. Quando lo scheduling risulta troppo difficile, conviene integrare le due fasi e considerare durate e sovrapposizioni gia' durante la costruzione del piano.

## Idee chiave

- Rappresentare stati e azioni in forma fattorizzata (PDDL) invece che atomica e' la mossa che rende la pianificazione scalabile: consente schemi di azione compatti ed euristiche derivabili automaticamente.
- La ricerca di un piano puo' procedere in avanti dallo stato iniziale o all'indietro dall'obiettivo; la regressione riduce il fattore di ramificazione, ma la ricerca in avanti domina perche' su stati concreti le euristiche sono piu' accurate.
- Problemi rilassati (ignorare precondizioni o effetti negativi), astrazioni di stato e scomposizione in sotto-obiettivi generano euristiche efficaci senza conoscenza specifica del dominio.
- Un problema di pianificazione si puo' anche codificare come soddisfacibilita' booleana o come CSP e delegare a risolutori generici molto ottimizzati.
- La pianificazione gerarchica (HTN) incapsula conoscenza esperta in azioni di alto livello con raffinamenti; la semantica angelica permette di certificare piani astratti senza esplorarne le implementazioni, con risparmi potenzialmente esponenziali.
- In ambienti parzialmente osservabili o non deterministici si ragiona su stati-credenza: la pianificazione conformante trova piani robusti senza percezioni, quella condizionale ramifica sulle osservazioni.
- Un agente online monitora azione, piano e obiettivi durante l'esecuzione e ripianifica quando il mondo devia dal modello; i fallimenti ricorrenti segnalano che va appreso un modello migliore, non ritentato lo stesso piano.
- Tempo e risorse si gestiscono con lo scheduling: il cammino critico risolve i vincoli temporali puri in tempo polinomiale, ma i vincoli di risorse rendono il problema NP-difficile.

## Perche conta oggi

I sistemi agentici costruiti sugli LLM stanno riscoprendo, spesso senza citarlo, il vocabolario di questo capitolo. Un [agente](../kb/concetti/agent.md) che scompone un compito in sottotask sta facendo pianificazione gerarchica informale: le "azioni di alto livello" sono i passi di un ragionamento [chain-of-thought](../kb/concetti/chain-of-thought.md), e i raffinamenti sono le chiamate concrete a strumenti esterni via [tool use](../kb/concetti/tool-use.md). Il ciclo pianifica-esegui-monitora-ripianifica descritto nel Paragrafo 11.5 e' esattamente il loop operativo di un [agent harness](../kb/concetti/agent-harness.md) moderno: osservare il risultato di un'azione, confrontarlo con l'atteso, riparare il piano.

Le differenze sono altrettanto istruttive. La pianificazione classica offre garanzie formali (un piano trovato e' corretto rispetto al modello) al prezzo di un modello del mondo esplicito e fragile; un [LLM](../kb/concetti/llm.md) pianifica in modo flessibile su descrizioni in linguaggio naturale, ma senza garanzie e con [world models](../kb/concetti/world-models.md) impliciti e imperfetti. Le lezioni del capitolo restano attuali proprio per questo: gli stati-credenza ricordano che un agente deve rappresentare la propria incertezza, la semantica angelica che conviene validare i piani al livello di astrazione giusto, e il monitoraggio dell'esecuzione che nessun sistema autonomo e' affidabile se si fida ciecamente del proprio modello. Non a caso le architetture ibride che accoppiano LLM e pianificatori simbolici sono una delle direzioni piu' studiate per dare affidabilita' agli agenti.

## Riferimenti

- Stuart J. Russell, Peter Norvig — *Intelligenza Artificiale: Un Approccio Moderno*, 4a edizione italiana, Pearson Italia, Vol. 1 (2021), Capitolo 11, pp. 353-394.
