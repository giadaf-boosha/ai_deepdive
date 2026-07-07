---
titolo: Il futuro dell'intelligenza artificiale
capitolo: 28
parte: 7
concetti: [agent, world-models, rlhf, llm, ai-governance]
created: 2026-07-06
last_updated: 2026-07-06
---

# Il futuro dell'intelligenza artificiale

Il capitolo che chiude questo percorso si pone una domanda semplice da formulare e difficile da rispondere: dove sta andando l'IA e che cosa manca ancora? Il punto di partenza e' la definizione che attraversa tutto il percorso: l'IA come progettazione di agenti approssimativamente razionali, costruiti assemblando componenti diversi — percezione, rappresentazione, ragionamento logico e probabilistico, apprendimento, attuazione — e applicati a domini che vanno dalla medicina ai trasporti.

La maggior parte degli esperti si aspetta che i progressi continuino: le stime mediane collocano sistemi capaci di prestazioni "quasi umane" su un'ampia gamma di compiti in una finestra tra i 50 e i 100 anni, mentre l'impatto economico atteso gia' nel prossimo decennio si misura in migliaia di miliardi di dollari l'anno. Ma esistono anche voci critiche, secondo cui l'IA generale richiedera' secoli, e preoccupazioni etiche serie su equita', imparzialita' e potenziale pericolosita' dei sistemi.

Gli autori affrontano la domanda su due piani. Prima passano in rassegna i singoli componenti di un sistema di IA, chiedendosi per ciascuno se possa accelerare o frenare il progresso complessivo. Poi salgono di livello e ragionano sulle architetture: come combinare quei componenti in agenti che funzionino davvero nel mondo reale, sotto vincoli di tempo e di risorse computazionali.

<figure class="diagram">
<svg viewBox="0 0 760 460" role="img" aria-label="Mappa concettuale del capitolo 28: l'IA come assemblaggio di componenti — selezione delle azioni, sensori e attuatori, rappresentazione del mondo, apprendimento — e il percorso dalle architetture di agenti al metaragionamento, all'ottimalita' limitata e all'IA generale">
<defs><marker id="arr-c28" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" class="dg-arrow"/></marker></defs>
<line x1="380" y1="68" x2="96" y2="97" class="dg-edge" marker-end="url(#arr-c28)"/>
<line x1="380" y1="68" x2="289" y2="97" class="dg-edge" marker-end="url(#arr-c28)"/>
<line x1="380" y1="68" x2="482" y2="97" class="dg-edge" marker-end="url(#arr-c28)"/>
<line x1="380" y1="68" x2="672" y2="97" class="dg-edge" marker-end="url(#arr-c28)"/>
<line x1="380" y1="68" x2="380" y2="197" class="dg-edge-primary" marker-end="url(#arr-c28)"/>
<text x="452" y="184" text-anchor="middle" class="dg-edge-label">come combinarli</text>
<line x1="96" y1="156" x2="96" y2="197" class="dg-edge" marker-end="url(#arr-c28)"/>
<text x="192" y="183" text-anchor="middle" class="dg-edge-label">che cosa ottimizzare?</text>
<line x1="672" y1="197" x2="672" y2="159" class="dg-edge" marker-end="url(#arr-c28)"/>
<text x="618" y="182" text-anchor="middle" class="dg-edge-label">alimentano</text>
<line x1="672" y1="256" x2="672" y2="297" class="dg-edge" marker-end="url(#arr-c28)"/>
<text x="612" y="282" text-anchor="middle" class="dg-edge-label">il vero salto</text>
<line x1="380" y1="256" x2="380" y2="297" class="dg-edge-primary" marker-end="url(#arr-c28)"/>
<text x="474" y="282" text-anchor="middle" class="dg-edge-label">metaragionamento</text>
<line x1="380" y1="356" x2="380" y2="387" class="dg-edge-primary" marker-end="url(#arr-c28)"/>
<text x="498" y="378" text-anchor="middle" class="dg-edge-label">oltre i compiti ristretti</text>
<rect x="280" y="12" width="200" height="56" rx="10" class="dg-node-primary"/>
<text x="380" y="36" text-anchor="middle" class="dg-label">Agenti razionali</text>
<text x="380" y="52" text-anchor="middle" class="dg-sublabel">assemblaggio di componenti</text>
<rect x="8" y="100" width="176" height="56" rx="10" class="dg-node"/>
<text x="96" y="124" text-anchor="middle" class="dg-label">Selezione delle azioni</text>
<text x="96" y="140" text-anchor="middle" class="dg-sublabel">orizzonti lunghi, gerarchie</text>
<rect x="206" y="100" width="166" height="56" rx="10" class="dg-node"/>
<text x="289" y="124" text-anchor="middle" class="dg-label">Sensori e attuatori</text>
<text x="289" y="140" text-anchor="middle" class="dg-sublabel">robotica come i PC anni '80</text>
<rect x="394" y="100" width="176" height="56" rx="10" class="dg-node"/>
<text x="482" y="124" text-anchor="middle" class="dg-label">Rappresentare il mondo</text>
<text x="482" y="140" text-anchor="middle" class="dg-sublabel">manca un formato generale</text>
<rect x="592" y="100" width="160" height="56" rx="10" class="dg-node"/>
<text x="672" y="124" text-anchor="middle" class="dg-label">Apprendimento</text>
<text x="672" y="140" text-anchor="middle" class="dg-sublabel">meno supervisione</text>
<rect x="8" y="200" width="176" height="56" rx="10" class="dg-node"/>
<text x="96" y="224" text-anchor="middle" class="dg-label">Preferenze incerte</text>
<text x="96" y="240" text-anchor="middle" class="dg-sublabel">rinforzo inverso, clic</text>
<rect x="285" y="200" width="190" height="56" rx="10" class="dg-node-primary"/>
<text x="380" y="224" text-anchor="middle" class="dg-label">Architetture di agenti</text>
<text x="380" y="240" text-anchor="middle" class="dg-sublabel">simbolico + connessionista</text>
<rect x="592" y="200" width="160" height="56" rx="10" class="dg-node"/>
<text x="672" y="224" text-anchor="middle" class="dg-label">Dati e calcolo</text>
<text x="672" y="240" text-anchor="middle" class="dg-sublabel">non il collo di bottiglia</text>
<rect x="285" y="300" width="190" height="56" rx="10" class="dg-node-primary"/>
<text x="380" y="324" text-anchor="middle" class="dg-label">Ottimalita' limitata</text>
<text x="380" y="340" text-anchor="middle" class="dg-sublabel">il miglior programma eseguibile</text>
<rect x="592" y="300" width="160" height="56" rx="10" class="dg-node"/>
<text x="672" y="324" text-anchor="middle" class="dg-label">Modelli condivisi</text>
<text x="672" y="340" text-anchor="middle" class="dg-sublabel">pre-addestrati via API</text>
<rect x="270" y="390" width="220" height="56" rx="10" class="dg-node-accent"/>
<text x="380" y="414" text-anchor="middle" class="dg-label">IA generale</text>
<text x="380" y="430" text-anchor="middle" class="dg-sublabel">manca maturita' ingegneristica</text>
</svg>
<figcaption>Mappa del capitolo 28 — dai componenti dell'agente alle architetture, fino all'ottimalita' limitata e all'IA generale</figcaption>
</figure>

## Il corpo dell'agente: sensori e attuatori maturano

Per decenni i sistemi di IA sono vissuti quasi solo nel software: input e output passavano comunque per mani umane, mentre la robotica restava confinata a compiti di basso livello. La ragione era duplice: costruire robot affidabili costava troppo, e ne' la potenza di calcolo ne' gli algoritmi erano in grado di digerire flussi percettivi ad alta larghezza di banda come il video.

La situazione e' cambiata rapidamente. Il costo di un lidar per auto a guida autonoma e' crollato di quasi due ordini di grandezza, esistono versioni a chip singolo da circa dieci euro, e i radar moderni hanno una sensibilita' un tempo impensabile. La tecnologia MEMS ha miniaturizzato accelerometri, giroscopi e attuatori fino a poterli montare su insetti volanti artificiali, mentre stampa 3D e biostampa hanno abbattuto i tempi di prototipazione. Gli autori paragonano lo stato della robotica a quello dei personal computer nei primi anni Ottanta: la tecnologia di base c'e', la diffusione capillare richiedera' ancora tempo, e arrivera' prima nell'industria — dove gli ambienti sono controllati e il ritorno dell'investimento e' misurabile — che nelle case.

## Rappresentare il mondo e tenerne traccia

Un agente deve mantenere una rappresentazione interna dello stato del mondo e aggiornarla man mano che percepisce. Il percorso ha mostrato molte tecniche per farlo: tracciamento di stati atomici, rappresentazioni fattorizzate, logica del primo ordine, filtraggio probabilistico in ambienti incerti, reti neurali ricorrenti che mantengono uno stato nel tempo. Il problema e' che ognuna di queste tecniche copre un pezzo del puzzle e nessuno sa ancora metterle insieme in modo organico.

Gli algoritmi attuali riconoscono bene oggetti e producono predicati semplici ("la tazza e' sul tavolo"), ma faticano con azioni di alto livello estese nel tempo, e comunque solo dopo addestramento su moltissimi dati; servira' una capacita' di generalizzare a situazioni mai viste senza dataset esaustivi. Il filtraggio approssimato scala su ambienti grandi ma ragiona per variabili, non per oggetti e relazioni, e la sua nozione di tempo e' un susseguirsi di passi discreti: predire dove sara' una pallina al passo successivo e' facile, rappresentare il concetto astratto "cio' che sale deve scendere" no. Il word embedding ha mostrato che si puo' catturare il significato senza definizioni rigide fatte di condizioni necessarie e sufficienti, ma il traguardo di formati di rappresentazione generali, riutilizzabili tra domini complessi, resta lontano.

## Agire su orizzonti lunghi e capire che cosa vogliamo davvero

Sulla selezione delle azioni, la difficolta' centrale e' la scala temporale. Un piano di vita reale — laurearsi in tre anni, per esempio — si compone di miliardi di passi primitivi, mentre gli algoritmi di ricerca gestiscono sequenze di decine o centinaia di azioni. Gli esseri umani ce la fanno perche' impongono una struttura gerarchica al comportamento, e tecniche come il reinforcement learning gerarchico vanno in quella direzione; ma questi metodi non coprono ancora il caso parzialmente osservabile, e soprattutto manca un modo per costruire automaticamente le gerarchie di stati e comportamenti, invece di riceverle gia' pronte dal progettista.

C'e' poi un problema piu' sottile: prima di ottimizzare serve sapere che cosa ottimizzare. In teoria basta dichiarare una funzione di utilita'; in pratica scrivere quella giusta e' un problema a se'. Le preferenze umane sono intrecciate, diverse da persona a persona, e un agente appena messo in campo non ha abbastanza esperienza per apprenderle: deve operare sotto incertezza sulle preferenze stesse. L'apprendimento per rinforzo inverso — dedurre gli obiettivi osservando un esperto che sa fare ma non sa spiegare — e' una risposta parziale. Gli autori notano che l'industria tecnologica ha gia' costruito una macchina potentissima per aggregare preferenze, i sistemi di raccomandazione basati sui clic, ma che questo feedback implicito ottimizza il breve termine e la cattura dell'attenzione, non gli interessi profondi delle persone: nessuna piattaforma suggerisce di spegnere il dispositivo e uscire a fare una passeggiata. Da qui l'interesse per movimenti come il "time well spent" e per l'idea di agenti personali che difendano gli obiettivi di lungo periodo dell'utente invece di quelli delle piattaforme.

## Apprendere con meno supervisione

Il deep learning ha trainato la rinascita dell'IA grazie a una confluenza di fattori: piu' dati via Internet, hardware piu' potente, e innovazioni algoritmiche come GAN, batch normalization, dropout e ReLU. Ma i sistemi attuali eccellono soprattutto quando i dati abbondano e sono etichettati; vanno in difficolta' con dati scarsi, apprendimento non supervisionato e rappresentazioni complesse.

Il capitolo delinea diverse strade per superare questi limiti. L'apprendimento per trasferimento riusa cio' che si e' imparato in un dominio per un dominio correlato. Un sistema ideale davanti a un problema nuovo — riconoscere modelli di automobili, per esempio — non dovrebbe pretendere milioni di immagini etichettate: dovrebbe sfruttare quello che gia' sa, cercare informazioni sul Web e conversare con un insegnante umano, capendo indicazioni come "questi due modelli si somigliano, ma uno ha la griglia piu' larga". Questo richiede un linguaggio di rappresentazione condiviso tra umani e macchine: nessun analista puo' modificare a mano un modello con milioni di pesi.

Su questo fronte vanno riportate le posizioni dei protagonisti del deep learning. LeCun propone di sostituire il termine con "programmazione differenziabile": rendere differenziabile — e quindi ottimizzabile automaticamente — non solo il modello, ma l'intero sistema software che lo circonda. LeCun e Hinton sostengono inoltre che l'enfasi sull'apprendimento supervisionato non e' sostenibile: il futuro e' l'apprendimento debolmente supervisionato e quello che LeCun chiama apprendimento predittivo, in cui il sistema costruisce un modello del mondo e impara a prevederne gli stati futuri. Hinton, nel 2017, si e' spinto a dire che occorre ripartire da zero sulle specifiche delle architetture e sulla retropropagazione, pur restando fedele all'idea di fondo dell'apprendimento per regolazione di parametri.

## Dati, calcolo e il passaggio ai modelli condivisi

Le risorse non sembrano il collo di bottiglia. Il Web produce oltre 10^18 byte al giorno di materiale utilizzabile, esistono centinaia di dataset di qualita', e il crowdsourcing permette di etichettare cio' che manca. L'hardware specializzato — GPU, TPU, FPGA — e' centinaia di volte piu' veloce delle CPU per l'addestramento: un modello su ImageNet che nel 2014 richiedeva un giorno intero nel 2018 si addestrava in due minuti, e tra il 2012 e il 2018 il calcolo dedicato all'addestramento dei modelli di punta e' cresciuto di un fattore 2 ogni 3,5 mesi. I computer quantistici restano una promessa lontana: esistono algoritmi quantistici per l'algebra lineare, ma nessuna macchina in grado di eseguirli su problemi di dimensioni reali.

Il cambiamento piu' significativo e' pero' qualitativo: il passaggio dai dati condivisi ai modelli condivisi. I grandi provider cloud competono offrendo via API modelli pre-addestrati per visione, riconoscimento vocale e traduzione, utilizzabili cosi' come sono o personalizzabili con i propri dati. Una previsione plausibile: avviare un progetto di machine learning da zero diventera' insolito quanto scrivere un'applicazione web senza librerie. Vista dal 2026, e' una delle previsioni piu' azzeccate del capitolo.

## Architetture, metaragionamento e la strada verso l'IA generale

Quale architettura di agente scegliere? La risposta e' "tutte": risposte reattive dove il tempo stringe, deliberazione basata su conoscenza dove si puo' pianificare, apprendimento dove i dati abbondano o il dominio e' poco compreso. La sfida storica e' fondere sistemi simbolici — capaci di lunghe catene di ragionamento e rappresentazioni espressive — e sistemi connessionisti, capaci di riconoscere pattern in dati rumorosi; la combinazione di programmazione probabilistica e deep learning e' una delle linee di ricerca in questa direzione, ancora acerba.

Un agente reale deve inoltre controllare le proprie deliberazioni: decidere quanto pensare prima di agire. Poiche' i domini si fanno sempre piu' complessi, ogni problema diventa un problema in tempo reale in cui la soluzione esatta e' fuori portata. Servono metodi generali: gli algoritmi anytime, la cui risposta migliora gradualmente e resta utilizzabile a ogni interruzione, e il metaragionamento basato sulla teoria delle decisioni, che valuta ogni calcolo pesandone il costo in ritardo contro il beneficio in qualita' della decisione. Generalizzando si arriva alle architetture riflessive, capaci di deliberare sulle proprie attivita' computazionali. La lezione di fondo: la forza bruta non basta. Anche una macchina fisicamente al limite (10^51 operazioni al secondo) enumererebbe in un anno solo le frasi di 11 parole, mentre un piano di vita umano conta miliardi di attuazioni. Meglio allora un obiettivo normativo raggiungibile, l'ottimalita' limitata: fissata l'architettura, cercare il miglior programma agente che quella architettura puo' eseguire.

Infine, l'IA generale. I progressi recenti sono figli di competizioni su compiti ristretti — guida autonoma, ImageNet, Go — ciascuno con un sistema addestrato da zero, mentre un agente davvero intelligente dovrebbe saper fare molte cose diverse. Gli autori difendono l'equilibrio attuale tra esplorazione e sfruttamento con un'analogia: nessuno avrebbe detto ai fratelli Wright nel 1903 di abbandonare l'aereo a singolo compito per progettare direttamente una macchina di "volo generale artificiale"; ma sarebbe stato altrettanto sbagliato limitarsi a gare annuali per perfezionare biplani di legno. Segnali di "diversita' di comportamento" gia' esistono: sistemi di traduzione unici per cento lingue, modelli congiunti multi-compito, i language model transformer come apripista di nuovi campi di ricerca. Manca pero' la maturita' ingegneristica: strumenti e pratiche che consentano anche a chi non e' un esperto di livello mondiale di costruire sistemi che funzionano, come accadde alla programmazione con la nascita dell'ingegneria del software. Il capitolo si chiude senza profezie: l'IA, come stampa, idraulica e aviazione, portera' benefici e effetti collaterali da gestire — con una differenza, il rischio unico che pone alla supremazia del genere umano — e con le parole di Turing del 1950: vediamo solo un breve tratto di strada, ma basta a capire quanto resta da fare.

## Idee chiave

- L'IA e' un assemblaggio di componenti — percezione, rappresentazione, decisione, apprendimento, attuazione — e il progresso complessivo dipende dal componente piu' arretrato, non da quello piu' brillante.
- Sensori e attuatori sono maturati piu' in fretta del previsto: la robotica e' oggi dove erano i personal computer nei primi anni Ottanta.
- Manca un formato di rappresentazione del mondo generale e riusabile: le tecniche esistenti (logiche, probabilistiche, neurali) coprono ciascuna un pezzo e non si integrano ancora.
- Le decisioni su orizzonti lunghi richiedono gerarchie di comportamento; il problema aperto e' costruirle automaticamente invece di riceverle dal progettista.
- Specificare gli obiettivi e' difficile quanto perseguirli: l'agente deve operare sotto incertezza sulle preferenze umane, e il feedback implicito dei clic ottimizza l'attenzione a breve termine, non il benessere.
- Il futuro dell'apprendimento e' meno supervisione: transfer learning, programmazione differenziabile, apprendimento predittivo basato su modelli del mondo.
- Dati e calcolo abbondano; il vero salto e' il passaggio dai dati condivisi ai modelli condivisi offerti come servizio.
- L'obiettivo realistico non e' la razionalita' perfetta ma l'ottimalita' limitata: il miglior programma agente eseguibile su un'architettura data, con metaragionamento per decidere quanto pensare.

## Perche conta oggi

Riletto a distanza di anni, questo capitolo e' un elenco di previsioni in gran parte confermate. I "modelli condivisi" offerti via API sono diventati gli [LLM](../kb/concetti/llm.md) che oggi fanno da fondazione a interi ecosistemi applicativi; l'apprendimento debolmente supervisionato e predittivo auspicato da LeCun e Hinton e' esattamente il pre-training su testo non annotato, e l'idea di [world models](../kb/concetti/world-models.md) appresi per predizione e' tornata al centro della ricerca. Il problema di "decidere che cosa si vuole" — specificare obiettivi sotto incertezza sulle preferenze umane — e' il nucleo concettuale di [RLHF](../kb/concetti/rlhf.md) e dell'allineamento moderno, discendente diretto dell'apprendimento per rinforzo inverso.

Anche la parte architetturale parla al presente: un [agent](../kb/concetti/agent.md) basato su LLM che pianifica, chiama strumenti esterni tramite [tool use](../kb/concetti/tool-use.md) e decide quanto ragionare prima di rispondere e' un'incarnazione pratica del metaragionamento e dell'ottimalita' limitata descritti nel capitolo. E la preoccupazione per piattaforme che ottimizzano l'attenzione anziche' gli interessi degli utenti, insieme al richiamo agli investimenti per ridurre gli impatti negativi, anticipa i temi oggi presidiati dalla [governance dell'AI](../kb/concetti/ai-governance.md). La strada indicata da Turing resta la stessa: se ne vede solo un tratto, ma abbastanza per sapere che il lavoro non e' finito.
