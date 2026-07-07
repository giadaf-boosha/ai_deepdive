---
titolo: Elaborazione del linguaggio naturale
capitolo: 23
parte: 6
concetti: [tokenization, embedding, llm, evaluation-benchmark]
created: 2026-07-06
last_updated: 2026-07-06
---

# Elaborazione del linguaggio naturale

Il linguaggio e' il tratto che piu' di ogni altro distingue la nostra specie, e non a caso Turing lo scelse come terreno del suo test: chi parla pianifica un messaggio per trasmettere conoscenza e raggiungere un obiettivo, chi ascolta percepisce e inferisce il significato inteso. Questo capitolo affronta la domanda di fondo del natural language processing (NLP): come possa una macchina servirsi della lingua per dialogare con le persone e per attingere al sapere sterminato che l'umanita' ha depositato nei testi scritti.

Il problema e' che le lingue naturali non si comportano come i linguaggi formali. Non esiste una definizione netta di frase corretta, i giudizi dei parlanti divergono e cambiano nel tempo, le espressioni sono ambigue e vaghe, e la corrispondenza tra parole e cose non e' fissata da nessuna specifica. La risposta del capitolo e' pragmatica: se non possiamo tracciare un confine booleano tra frasi grammaticali e non grammaticali, possiamo almeno assegnare a ogni stringa una probabilita'. Da qui nasce l'idea di modello di linguaggio, una distribuzione di probabilita' sulle sequenze di parole, che si rivela lo strumento centrale per quasi tutti i compiti linguistici: completamento del testo, correzione ortografica, traduzione, risposta a domande.

Il capitolo percorre una scala di modelli sempre piu' espressivi: dai conteggi di parole isolate, agli n-grammi, alle grammatiche probabilistiche con parsing, fino alle grammatiche aumentate con semantica logica. Chiude con le complicazioni del linguaggio reale e con una rassegna dei compiti applicativi. E' il ponte concettuale tra l'AI classica e i modelli neurali del capitolo successivo.

<figure class="diagram">
<svg viewBox="0 0 760 400" role="img" aria-label="Mappa concettuale del capitolo 23: dal linguaggio naturale al modello di linguaggio come distribuzione di probabilita', la scala di modelli da borsa di parole a n-grammi, PCFG e grammatiche aumentate, con POS tagging, semantica composizionale, ambiguita' e disambiguazione, fino al ponte verso i word embedding del capitolo 24">
<defs><marker id="arr-c23" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" class="dg-arrow"/></marker></defs>
<line x1="116" y1="68" x2="116" y2="118" class="dg-edge-primary" marker-end="url(#arr-c23)"/>
<line x1="224" y1="118" x2="300" y2="68" class="dg-edge" marker-end="url(#arr-c23)"/>
<text x="330" y="100" text-anchor="middle" class="dg-edge-label">strumento centrale</text>
<line x1="646" y1="68" x2="646" y2="118" class="dg-edge" marker-end="url(#arr-c23)"/>
<line x1="224" y1="146" x2="540" y2="146" class="dg-edge" marker-end="url(#arr-c23)"/>
<text x="382" y="138" text-anchor="middle" class="dg-edge-label">una delle 4 fonti</text>
<line x1="116" y1="174" x2="88" y2="224" class="dg-edge-primary" marker-end="url(#arr-c23)"/>
<line x1="168" y1="252" x2="200" y2="252" class="dg-edge-primary" marker-end="url(#arr-c23)"/>
<line x1="360" y1="252" x2="392" y2="252" class="dg-edge-primary" marker-end="url(#arr-c23)"/>
<line x1="552" y1="252" x2="584" y2="252" class="dg-edge-primary" marker-end="url(#arr-c23)"/>
<line x1="230" y1="280" x2="110" y2="330" class="dg-edge" marker-end="url(#arr-c23)"/>
<text x="130" y="300" text-anchor="middle" class="dg-edge-label">dare struttura</text>
<line x1="310" y1="280" x2="375" y2="330" class="dg-edge" marker-end="url(#arr-c23)"/>
<text x="420" y="300" text-anchor="middle" class="dg-edge-label">niente generalizzazione</text>
<line x1="668" y1="280" x2="654" y2="330" class="dg-edge" marker-end="url(#arr-c23)"/>
<rect x="8" y="12" width="216" height="56" rx="10" class="dg-node"/>
<text x="116" y="36" text-anchor="middle" class="dg-label">Linguaggio naturale</text>
<text x="116" y="52" text-anchor="middle" class="dg-sublabel">nessun confine grammaticale netto</text>
<rect x="288" y="12" width="190" height="56" rx="10" class="dg-node"/>
<text x="383" y="36" text-anchor="middle" class="dg-label">Compiti applicativi</text>
<text x="383" y="52" text-anchor="middle" class="dg-sublabel">traduzione, speech, QA</text>
<rect x="540" y="12" width="212" height="56" rx="10" class="dg-node"/>
<text x="646" y="36" text-anchor="middle" class="dg-label">Ambiguita' pervasiva</text>
<text x="646" y="52" text-anchor="middle" class="dg-sublabel">lessicale, sintattica, semantica</text>
<rect x="8" y="118" width="216" height="56" rx="10" class="dg-node-primary"/>
<text x="116" y="142" text-anchor="middle" class="dg-label">Modello di linguaggio</text>
<text x="116" y="158" text-anchor="middle" class="dg-sublabel">probabilita' sulle sequenze</text>
<rect x="540" y="118" width="212" height="56" rx="10" class="dg-node"/>
<text x="646" y="142" text-anchor="middle" class="dg-label">Disambiguazione</text>
<text x="646" y="158" text-anchor="middle" class="dg-sublabel">interpretazione piu' probabile</text>
<rect x="8" y="224" width="160" height="56" rx="10" class="dg-node"/>
<text x="88" y="248" text-anchor="middle" class="dg-label">Borsa di parole</text>
<text x="88" y="264" text-anchor="middle" class="dg-sublabel">Bayes ingenuo</text>
<rect x="200" y="224" width="160" height="56" rx="10" class="dg-node"/>
<text x="280" y="248" text-anchor="middle" class="dg-label">N-grammi</text>
<text x="280" y="264" text-anchor="middle" class="dg-sublabel">catena di Markov</text>
<rect x="392" y="224" width="160" height="56" rx="10" class="dg-node"/>
<text x="472" y="248" text-anchor="middle" class="dg-label">PCFG e parsing</text>
<text x="472" y="264" text-anchor="middle" class="dg-sublabel">alberi sintattici, CYK</text>
<rect x="584" y="224" width="168" height="56" rx="10" class="dg-node"/>
<text x="668" y="248" text-anchor="middle" class="dg-label">Grammatiche aumentate</text>
<text x="668" y="264" text-anchor="middle" class="dg-sublabel">caso, teste lessicali</text>
<rect x="8" y="330" width="170" height="56" rx="10" class="dg-node"/>
<text x="93" y="354" text-anchor="middle" class="dg-label">POS tagging</text>
<text x="93" y="370" text-anchor="middle" class="dg-sublabel">HMM o regressione logistica</text>
<rect x="290" y="330" width="200" height="56" rx="10" class="dg-node-accent"/>
<text x="390" y="354" text-anchor="middle" class="dg-label">Word embedding</text>
<text x="390" y="370" text-anchor="middle" class="dg-sublabel">verso i modelli neurali (cap. 24)</text>
<rect x="548" y="330" width="204" height="56" rx="10" class="dg-node"/>
<text x="650" y="354" text-anchor="middle" class="dg-label">Semantica composizionale</text>
<text x="650" y="370" text-anchor="middle" class="dg-sublabel">dalla frase alla forma logica</text>
</svg>
<figcaption>Mappa del capitolo 23 — dal modello di linguaggio alla scala di modelli sempre piu' espressivi, fino al ponte verso i word embedding</figcaption>
</figure>

## Contare le parole: borsa di parole e n-grammi

Il modello piu' semplice tratta un testo come una borsa di parole: per classificare una frase in una categoria (business, meteo, spam) basta guardare quali parole contiene, ignorando completamente l'ordine. E' il modello di Bayes ingenuo riletto come modello di linguaggio generativo: immaginiamo una borsa per categoria, piena di foglietti con le parole, ed estraiamo parole a caso. L'assunzione di indipendenza tra le parole e' palesemente falsa, eppure il modello classifica con buona accuratezza: "azioni" e "guadagni" segnalano un testo finanziario, "pioggia" e "nuvoloso" uno meteorologico. I parametri si stimano contando le occorrenze in un corpus etichettato, e gia' qui emerge un dettaglio non banale: decidere che cosa sia una parola (come spezzare "c'e'"?) richiede un processo di tokenizzazione.

Il passo successivo reintroduce l'ordine. Far dipendere ogni parola da tutte le precedenti sarebbe corretto in linea di principio ma intrattabile: con centomila parole di vocabolario e frasi di quaranta parole i parametri esplodono. Il compromesso e' la catena di Markov: nel modello a n-grammi ogni parola dipende solo dalle n-1 precedenti. Bigrammi e trigrammi bastano per compiti come il rilevamento dello spam, l'analisi del sentiment o l'attribuzione d'autore. Esistono varianti utili: i modelli di caratteri, che prevedono il carattere successivo e identificano la lingua di un testo con accuratezza superiore al 99%, e gli skip-gram, che contano coppie di parole vicine saltandone una in mezzo.

I conteggi grezzi hanno pero' due difetti. Gli n-grammi rari producono stime ad alta varianza, e le parole mai viste nel corpus (fuori vocabolario) riceverebbero probabilita' zero, azzerando la probabilita' dell'intera frase. Le soluzioni sono la sostituzione delle parole rare con simboli speciali come UNK e la regolarizzazione (smoothing): dalla regola di Laplace, che aggiunge uno a ogni conteggio, ai modelli di backoff con interpolazione lineare, che combinano trigrammi, bigrammi e unigrammi pesati. L'obiettivo comune e' ridurre la varianza del modello riservando un po' di massa di probabilita' agli eventi mai osservati.

Il limite strutturale resta la mancanza di generalizzazione: per un modello a n-grammi ogni parola e' un atomo senza struttura interna. Aver visto "un gatto nero" non fornisce alcuna evidenza a favore di "il gattino giocoso", mentre un parlante riconosce in entrambi lo stesso schema articolo-sostantivo-aggettivo. Rappresentazioni piu' ricche — dizionari strutturati come WordNet, o i word embedding trattati nel capitolo 24 — servono esattamente a colmare questo divario.

## Etichettare le parole: POS tagging

Un primo modo di dare struttura al testo e' assegnare a ogni parola la sua parte del discorso (POS, part of speech): sostantivo, verbo, aggettivo e cosi' via. Il riferimento pratico e' il Penn Treebank, un corpus inglese di oltre tre milioni di parole annotate con 45 tag. Il POS tagging non e' interessante di per se', ma e' un passo preparatorio per traduzione, risposta a domande e perfino sintesi vocale, dove serve sapere se "capitano" e' un sostantivo o un verbo per pronunciarlo correttamente.

Il capitolo confronta due famiglie di approcci. Il modello di Markov nascosto (HMM) tratta le parole come osservazioni e i tag come stati nascosti; l'algoritmo di Viterbi recupera la sequenza di tag piu' probabile con accuratezza intorno al 97%. E' un modello generativo semplice, ma poco flessibile: non c'e' un modo naturale di esprimere regolarita' come "le parole che finiscono in -oso sono probabilmente aggettivi". La regressione logistica, modello discriminativo, permette invece di definire caratteristiche arbitrarie sulla parola e sul contesto — suffissi, maiuscole, presenza di cifre, tag della parola precedente — e apprende i pesi con la discesa del gradiente. Per gestire la sequenza si usa una ricerca greedy, che decide tag per tag senza tornare indietro, oppure una ricerca beam che mantiene i b candidati migliori, bilanciando velocita' e accuratezza. In generale i modelli discriminativi ottengono errori piu' bassi, mentre quelli generativi convergono prima e reggono meglio quando i dati di addestramento scarseggiano.

## Grammatiche probabilistiche e parsing

Per catturare la struttura gerarchica delle frasi servono le grammatiche. Il formalismo di riferimento e' la grammatica non contestuale probabilistica (PCFG): un insieme di regole di riscrittura, ciascuna con una probabilita', che generano alberi sintattici con categorie come sintagma nominale (NP) e sintagma verbale (VP). Gli autori ne definiscono una minima per un frammento di inglese ambientato nel mondo del wumpus, e mostrano subito i suoi due difetti tipici: sovragenera (accetta frasi che nessun parlante accetterebbe) e sottogenera (rifiuta frasi legittime).

Il parsing e' la ricerca dell'albero sintattico di una frase, e puo' procedere dall'alto (dal simbolo di frase alle parole) o dal basso. Fatto in modo ingenuo, ripete lavoro: la programmazione dinamica lo evita registrando i risultati parziali in una struttura chiamata chart. L'algoritmo CYK, il parser di chart descritto nel capitolo, richiede la grammatica in forma normale di Chomsky e trova l'albero piu' probabile in tempo O(n^3) rispetto alla lunghezza della frase. Poiche' i linguaggi naturali si sono evoluti per essere capiti in tempo reale, ci si puo' spingere verso O(n) accettando qualche rischio: ricerca A* con euristiche apprese, ricerca beam, o il parsing deterministico shift-reduce che scorre la frase parola per parola gestendo uno stack di costituenti.

Accanto alla struttura sintagmatica esiste la grammatica delle dipendenze, che descrive la frase come relazioni binarie tra parole senza costituenti intermedi; le due notazioni sono in gran parte interconvertibili, e la seconda risulta piu' naturale per lingue a ordine libero delle parole. Soprattutto, le grammatiche non si scrivono piu' a mano: da un treebank come il Penn Treebank si inducono regole e probabilita' contando i sottoalberi, e dove gli alberi annotati mancano si ricorre ad apprendimento semisupervisionato o non supervisionato, sfruttando perfino i tag HTML delle pagine web come parentesizzazione parziale.

## Dalla sintassi al significato: grammatiche aumentate

Una PCFG pura non sa che "Io mangiai una banana" funziona mentre "Me mangiai una banana" no: tratta tutti i pronomi allo stesso modo. Le grammatiche aumentate sostituiscono i simboli atomici con rappresentazioni strutturate che portano con se' caso grammaticale, persona, numero e testa lessicale del sintagma. Una PCFG lessicalizzata condiziona le probabilita' sulle parole di testa: puo' cosi' apprendere che il verbo "mangiare" si combina volentieri con un oggetto commestibile, e che un verbo transitivo e' seguito da un NP molto piu' spesso di un verbo intransitivo.

Lo stesso meccanismo di aumento apre la porta alla semantica. Seguendo il principio di composizionalita' — il significato di una frase e' funzione del significato delle sue parti — ogni regola grammaticale viene arricchita con un'annotazione che costruisce la rappresentazione logica. I verbi diventano predicati in notazione lambda: "ama" e' una funzione che, applicata a "Bruno" e poi ad "Alice", produce la formula Ama(Alice, Bruno). L'esempio didattico delle espressioni aritmetiche rende l'idea: l'albero sintattico di "3 + (4 / 2)" ha come radice direttamente il valore 5. Poiche' annotare frasi con forme logiche richiede esperti, i sistemi piu' pratici imparano grammatiche semantiche da coppie domanda/risposta raccolte dal web, facendo emergere la forma logica intermedia come variabile latente.

## Il linguaggio reale non collabora

L'ultima parte del capitolo elenca cio' che rende il linguaggio umano ostico per qualsiasi grammatica formale. La quantificazione: "ogni agente sente una brezza" ammette due letture logiche, una brezza per tutti o una ciascuno. La pragmatica: espressioni indexical come "io" e "oggi" si risolvono solo conoscendo la situazione, e l'intento del parlante (domanda, comando, promessa) va decodificato come atto linguistico. Le dipendenze a lunga distanza spostano pezzi di frase lontano dal punto in cui la grammatica li richiede. Il tempo verbale richiede di rappresentare la collocazione temporale degli eventi.

E poi l'ambiguita', che pervade tutto: lessicale (una parola, molti significati), sintattica (una frase, molti alberi), semantica, fino alle figure retoriche come metonimia e metafora, che gli umani interpretano senza accorgersene. I titoli di giornale ambigui sono l'eccezione che fa ridere; la regola e' che quasi ogni frase ha decine di analisi possibili, di cui i parlanti ne percepiscono una sola. La disambiguazione e' quindi un problema di scelta dell'interpretazione piu' probabile, e richiede di combinare quattro fonti di evidenza: un modello del mondo (che cosa e' verosimile), un modello mentale del parlante (che cosa vuole comunicare), un modello del linguaggio (che cosa si dice di solito) e, nel parlato, un modello acustico.

## I compiti applicativi

La rassegna finale copre i grandi compiti dell'NLP. Il riconoscimento vocale, dove le reti neurali deep hanno abbattuto il tasso di errore di circa il 30% dopo il 2011 portandolo vicino a quello umano, e la sintesi vocale sul percorso inverso. La traduzione automatica, passata dagli n-grammi ai modelli neurali sequenza-sequenza e poi ai meccanismi di attenzione dei transformer, con qualita' prossima a quella umana su alcune coppie di lingue. L'estrazione di informazioni, che trasforma testo libero in record strutturati. L'information retrieval dei motori di ricerca e la risposta a domande, che invece di restituire documenti deve produrre la risposta effettiva. Il capitolo mostra anche i primi modelli di linguaggio neurali generativi: i campioni di GPT-2 sono fluenti e pertinenti al prompt, ma non avanzano verso una tesi coerente — un'istantanea preziosa dello stato dell'arte al 2020.

## Idee chiave

- Un modello di linguaggio e' una distribuzione di probabilita' sulle stringhe: rinunciare al confine netto tra frasi corrette e scorrette e' la mossa che rende trattabile il linguaggio naturale.
- I modelli a n-grammi, pur semplicistici, estraggono molta informazione e reggono compiti reali come identificazione della lingua, sentiment analysis e classificazione, purche' si regolarizzino le stime per gli eventi rari.
- Conviene progettare modelli che sfruttino bene i dati disponibili, anche se sembrano troppo semplici; i word embedding offrono poi una rappresentazione delle parole piu' ricca dei conteggi atomici.
- Le grammatiche a struttura sintagmatica (PCFG) e le grammatiche delle dipendenze catturano la gerarchia delle frasi; un parser di chart come CYK analizza in O(n^3), e con una piccola perdita di accuratezza beam search e shift-reduce scendono verso il tempo lineare.
- Un treebank permette di apprendere grammatica e probabilita' dai dati invece di scriverle a mano.
- Aumentare la grammatica con caso, concordanza e teste lessicali, e poi con annotazioni semantiche composizionali, trasforma il parsing in interpretazione: dalla frase alla forma logica.
- Quantificatori, pragmatica, dipendenze a lunga distanza, tempo verbale e soprattutto ambiguita' a ogni livello rendono il linguaggio reale irriducibile a una grammatica formale completa.
- La disambiguazione e' selezione dell'interpretazione piu' probabile, combinando modello del mondo, modello mentale, modello del linguaggio e modello acustico.

## Perche conta oggi

Questo capitolo e' la genealogia diretta degli [LLM](../kb/concetti/llm.md). L'idea fondante — un modello di linguaggio come distribuzione di probabilita' sulla parola successiva — e' esattamente cio' che un transformer moderno ottimizza; e' cambiata la rappresentazione, non la domanda. La [tokenizzazione](../kb/concetti/tokenization.md), qui liquidata come dettaglio ("che cosa e' una parola?"), e' oggi una scelta di progetto che condiziona costi, multilinguismo e persino le capacita' aritmetiche dei modelli. Il limite degli n-grammi — parole atomiche, zero generalizzazione — e' precisamente il problema che gli [embedding](../kb/concetti/embedding.md) risolvono, ed e' il filo che porta al capitolo 24.

Anche i temi apparentemente datati hanno eredi diretti. La finestra di n-1 parole degli n-grammi e' l'antenata della [context window](../kb/concetti/context-window.md), e la tensione tra contesto piu' lungo e parametri piu' numerosi non e' mai sparita. Il problema della disambiguazione tramite modello del mondo e modello mentale del parlante riemerge ogni volta che si scrive un prompt: gran parte del [prompt engineering](../kb/concetti/prompt-engineering.md) consiste nel fornire al modello il contesto pragmatico che il capitolo attribuiva all'ascoltatore umano. E l'osservazione che i modelli si confrontano su compiti condivisi per misurare i progressi anticipa la pratica moderna degli [evaluation benchmark](../kb/concetti/evaluation-benchmark.md). Ironia della storia: le pipeline esplicite di parsing e semantica composizionale sono state in gran parte assorbite dai modelli end-to-end, ma i concetti — struttura, ambiguita', composizionalita', atti linguistici — restano il vocabolario con cui si diagnosticano i fallimenti degli LLM.
