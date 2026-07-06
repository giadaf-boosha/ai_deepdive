---
titolo: Rappresentazione della conoscenza
capitolo: 10
parte: 3
volume: 1
pagine: "323-352"
concetti: [world-models, rag, agent, llm]
created: 2026-07-06
last_updated: 2026-07-06
---

# Rappresentazione della conoscenza

I capitoli precedenti spiegano come un agente logico ragiona a partire da una base di conoscenza. Questo capitolo affronta la domanda complementare, e per certi versi piu' difficile: che cosa mettere dentro quella base di conoscenza. Come si descrivono, in un linguaggio formale come la logica del primo ordine, le cose di cui e' fatto il mondo reale — oggetti, sostanze, misure, eventi, tempo, e perfino le credenze degli altri agenti?

La questione conta perche' nei domini giocattolo quasi ogni rappresentazione funziona, mentre nei domini reali — fare acquisti online, guidare nel traffico — servono schemi generali e flessibili, capaci di unificare aree di conoscenza diverse dentro un unico quadro coerente. Russell e Norvig chiamano questo lavoro ingegneria ontologica: progettare i concetti astratti che ricorrono in quasi tutti i domini, lasciando dei punti di aggancio dove inserire poi i dettagli specifici.

Il capitolo attraversa cosi' tre livelli: prima costruisce un'ontologia generale del mondo (categorie, parti, misure, sostanze, eventi, tempo, oggetti mentali), poi presenta i formalismi nati per ragionare in modo efficiente su queste strutture (reti semantiche e logiche descrittive), infine affronta il problema delle eccezioni e del ragionamento con informazione di default, dove la logica classica mostra i suoi limiti.

## Un'ontologia per (quasi) tutto

Rappresentare l'intero mondo e' impossibile, ma si puo' progettare uno scheletro concettuale generale — un'ontologia superiore — con i concetti piu' astratti in cima (Tutto, OggettiAstratti, EventiGeneralizzati) e le specializzazioni via via piu' concrete sotto. L'analogia proposta dal libro e' quella dei framework object-oriented: chi progetta una libreria grafica definisce il concetto generale di finestra, sapendo che altri lo specializzeranno in tipi concreti.

Un'ontologia generale ha due requisiti che la distinguono da una collezione di ontologie ad hoc: deve applicarsi a quasi ogni dominio senza soluzioni improvvisate, e deve permettere di combinare aree di conoscenza diverse nello stesso ragionamento — un robot che ripara circuiti ragiona insieme su collegamenti elettrici, disposizione spaziale, tempo e costi. Il bilancio storico e' pero' onesto: nessuna delle grandi applicazioni dell'AI usa davvero un'ontologia universale, e gli interessi divergenti degli stakeholder rendono difficile l'accordo. Le ontologie esistenti sono nate per quattro vie: team di esperti che scrivono assiomi a mano (CYC), importazione da database strutturati (DBpedia da Wikipedia), estrazione automatica da testi (TextRunner), e crowdsourcing di fatti di senso comune (OpenMind). Il Google Knowledge Graph, con decine di miliardi di fatti, e' un esempio industriale di approccio misto.

## Categorie, ereditarieta' e parti

Il mattone fondamentale e' la categoria: anche se il mondo e' fatto di oggetti individuali, gran parte del ragionamento avviene a livello di classi. Classificare un oggetto a partire dalle percezioni permette di predire proprieta' che non abbiamo osservato: se un frutto e' verde striato, ovale e con polpa rossa, concludiamo che e' un'anguria e da li' deduciamo tutto il resto.

In logica del primo ordine le categorie si esprimono come predicati oppure, tramite reificazione, come veri e propri oggetti su cui quantificare. Le relazioni chiave sono l'appartenenza (un oggetto e' membro di una categoria), la sottoclasse (una categoria e' inclusa in un'altra) e l'ereditarieta': se ogni cibo e' commestibile e le mele sono un tipo di frutta, che e' un tipo di cibo, ogni singola mela eredita la commestibilita' senza doverla affermare una per una. Le catene di sottoclassi formano gerarchie tassonomiche, uno strumento antichissimo (dalla biologia al sistema decimale Dewey) che l'AI formalizza. Concetti come categorie disgiunte, scomposizioni esaustive e partizioni permettono di dire con precisione come una categoria si divide nelle sue sottocategorie.

Accanto alla tassonomia c'e' la composizione fisica: la relazione ParteDi (transitiva e riflessiva) descrive gerarchie di parti — una citta' e' parte di una nazione, che e' parte di un continente. Gli oggetti composti si caratterizzano per la struttura delle loro parti; per aggregati senza struttura il libro introduce il concetto di mucchio, l'oggetto fisico composto da certi elementi, distinto dall'insieme matematico che quegli elementi contiene (un insieme non pesa due chili, un mucchio di mele si').

## Misure, cose e roba

Le proprieta' quantitative — lunghezza, massa, prezzo — si rappresentano con funzioni di unita' applicate a numeri, cosi' che la stessa grandezza abbia nomi diversi in unita' diverse e la conversione sia un semplice assioma di uguaglianza. Il punto piu' interessante riguarda le grandezze senza scala naturale, come la difficolta' di un esercizio o la bellezza di una poesia: non serve inventare numeri arbitrari, basta poterle ordinare. Relazioni monotone tra misure bastano per molte decisioni, ed e' l'idea alla base della fisica qualitativa.

C'e' poi una distinzione ontologica profonda, quella tra cose e roba (stuff). Alcune porzioni di realta' resistono all'individuazione in oggetti distinti: tagliando a meta' un formichiere non otteniamo due formichieri, ma tagliando a meta' del burro otteniamo ancora burro. Il linguaggio naturale lo riflette nella differenza tra sostantivi numerabili e non numerabili. La chiave formale sta nelle proprieta' intrinseche, che sopravvivono alla suddivisione (densita', colore, punto di fusione), contro quelle estrinseche, che non vi sopravvivono (peso, forma, lunghezza): una categoria definita solo da proprieta' intrinseche e' una sostanza, una che include anche una sola proprieta' estrinseca e' un oggetto numerabile.

## Eventi, tempo e cambiamento

Per rappresentare azioni continue, simultanee o estese nel tempo, il capitolo introduce il calcolo degli eventi. Gli ingredienti sono eventi, fluenti (aspetti del mondo che cambiano, come la posizione di una persona) e istanti temporali. Reificare gli eventi come oggetti permette di attaccare loro quantita' arbitrarie di informazione — chi viaggia, da dove, verso dove, se il volo e' stato turbolento — cosa impossibile con predicati a numero fisso di argomenti. Predicati come T (il fluente vale in un intervallo), Accade, Inizia e Termina, insieme ad assiomi generali di persistenza, catturano l'idea che un fluente resta vero finche' un evento non lo termina.

Sopra questa base si costruisce una teoria del tempo: momenti di durata zero e intervalli estesi, una scala temporale assoluta, e la classica algebra degli intervalli di Allen — le relazioni possibili tra due intervalli (uno precede l'altro, sono consecutivi, si sovrappongono, uno e' durante l'altro, iniziano o finiscono insieme) espresse con confronti tra istanti di inizio e fine. Un'idea elegante che ne discende e' trattare gli stessi oggetti fisici come eventi generalizzati, cioe' pezzi di spazio-tempo: gli Stati Uniti sono un "evento" iniziato nel 1776, e il termine Presidente(StatiUniti) denota un unico oggetto che consiste di persone diverse in periodi diversi.

## Ragionare sulle credenze: oggetti mentali e logica modale

Un agente sofisticato deve poter ragionare non solo sul mondo, ma sulla conoscenza — propria e altrui. Qui la logica del primo ordine incontra un ostacolo: il ragionamento sull'uguaglianza e' integrato nella logica (trasparenza referenziale), quindi se Superman e Clark Kent sono la stessa persona, tutto cio' che vale per uno vale per l'altro. Ma Lois puo' sapere che Superman vola senza sapere che Clark vola: per le attitudini proposizionali come credere e conoscere, i termini usati contano.

La logica modale risolve il problema con operatori che accettano formule come argomenti (K_A P: "A conosce P") e una semantica a mondi possibili collegati da relazioni di accessibilita': un agente conosce P se P e' vera in tutti i mondi compatibili con cio' che sa. Il formalismo permette conoscenza annidata (Lois sa che Clark sa qualcosa che lei non sa) e distingue letture ambigue dei quantificatori. Ha pero' un difetto strutturale, l'onniscienza logica: assume che ogni agente conosca tutte le conseguenze dei propri assiomi, un'idealizzazione lontana dagli agenti reali. Il paragrafo accenna anche ad altre modalita', come la logica temporale lineare con operatori sul futuro, usata per specificare proprieta' di sistemi.

## Reti semantiche, logiche descrittive e ragionamento di default

Per ragionare in modo efficiente sulle categorie sono nate due famiglie di formalismi imparentate. Le reti semantiche rappresentano oggetti e categorie come nodi e le relazioni come archi etichettati; l'ereditarieta' diventa un algoritmo che risale i collegamenti di appartenenza e sottoinsieme fino a trovare la proprieta' cercata. La semplicita' e' il loro punto di forza e il loro limite: gli archi esprimono solo relazioni binarie (le asserzioni n-arie richiedono reificazione), e la piena potenza della logica del primo ordine si perde. Le logiche descrittive come CLASSIC formalizzano le stesse idee con un'algebra di costruttori di concetti; i compiti inferenziali centrali sono la sussunzione (una categoria e' inclusa in un'altra?) e la classificazione (un oggetto appartiene a una categoria?), con un'attenzione esplicita alla trattabilita' computazionale: si rinuncia a negazione e disgiunzione piene in cambio di inferenze prevedibilmente efficienti.

Le reti semantiche gestiscono con naturalezza i valori di default: tutte le persone hanno due gambe, salvo informazione piu' specifica che sovrascrive il valore. Questo pero' viola la monotonicita' della logica classica, dove aggiungere assiomi non puo' mai ritirare conclusioni. Le logiche non monotone nascono per dare una semantica a questo modo di ragionare, onnipresente nel senso comune: vedendo un'auto parcheggiata assumiamo che abbia quattro ruote, salvo ritrattare se emerge il contrario. La circoscrizione minimizza predicati di "anormalita'" (gli uccelli volano, a meno che non siano anormali), preferendo i modelli con meno eccezioni; la logica di default formula regole con prerequisito, giustificazioni e conclusione, e definisce le estensioni come insiemi massimali di conclusioni coerenti. Il "rombo di Nixon" — quacchero, quindi pacifista per default; repubblicano, quindi non pacifista per default — illustra i conflitti tra default e i meccanismi di priorita' per risolverli.

Infine, se le conclusioni di default possono rivelarsi sbagliate, serve un modo efficiente di ritrattarle: e' il compito dei sistemi di mantenimento della verita' (TMS). Un JTMS annota ogni formula con le sue giustificazioni, cosi' che ritirare una premessa cancelli solo cio' che dipendeva esclusivamente da essa; un ATMS tiene traccia, per ogni formula, degli insiemi di assunzioni che la renderebbero vera, permettendo di confrontare rapidamente scenari ipotetici alternativi e di generare spiegazioni. Il problema resta NP-difficile, ma usati con criterio i TMS rendono gestibili ambienti e ipotesi complesse.

## Idee chiave

- Rappresentare conoscenza su larga scala richiede un'ontologia generale che organizzi e colleghi domini diversi; costruirla e' un progetto tuttora aperto, nonostante infrastrutture ormai solide.
- L'ontologia superiore del capitolo si fonda su categorie ed eventi, e copre sottocategorie, parti, misure, sostanze, tempo, cambiamento e credenze.
- L'ereditarieta' lungo le gerarchie di categorie e' una forma di inferenza potente ed economica: le proprieta' si deducono dall'appartenenza, non si elencano oggetto per oggetto.
- I tipi naturali (pomodori, sedie) non ammettono definizioni logiche complete; si puo' pero' rappresentare cio' che vale per le loro istanze tipiche.
- Il calcolo degli eventi rende trattabili azioni continue, simultanee ed estese nel tempo, permettendo a un agente di prevedere gli effetti di sequenze di azioni.
- Reti semantiche e logiche descrittive scambiano espressivita' con efficienza e leggibilita'; le logiche descrittive puntano esplicitamente a inferenze di sussunzione trattabili.
- L'ipotesi del mondo chiuso e i valori di default sono scorciatoie preziose ma non monotone: circoscrizione e logica di default ne catturano la semantica.
- I sistemi di mantenimento della verita' gestiscono in modo efficiente revisione delle credenze e ritrattazione delle inferenze quando arrivano informazioni nuove.

## Perche conta oggi

Gli [LLM](../kb/concetti/llm.md) sembrano aver scavalcato il problema: la conoscenza sta nei pesi della rete, non in assiomi scritti a mano. Ma le domande del capitolo sono tornate intatte sotto altre forme. Un modello linguistico ha conoscenza implicita, opaca e non ritrattabile — esattamente cio' che i TMS e le logiche non monotone volevano evitare — e la risposta pratica dell'industria e' stata reintrodurre conoscenza esplicita e aggiornabile accanto al modello: il [RAG](../kb/concetti/rag.md) e i [vector database](../kb/concetti/vector-database.md) fanno oggi il lavoro che le basi di conoscenza strutturate facevano ieri, con gli [embedding](../kb/concetti/embedding.md) al posto dei predicati come meccanismo di indicizzazione semantica. I knowledge graph in stile DBpedia, citati nel capitolo, restano infrastruttura viva nei motori di ricerca e nei sistemi enterprise.

Anche il resto dell'ontologia di Russell e Norvig riemerge nella pratica degli [agenti](../kb/concetti/agent.md): un agente che pianifica azioni con effetti nel tempo, ritratta conclusioni davanti a errori e ragiona su cio' che sa e non sa sta affrontando eventi, fluenti, default e oggetti mentali, anche se lo fa in linguaggio naturale invece che in logica del primo ordine. La ricerca sui [world models](../kb/concetti/world-models.md) ripropone la domanda centrale del capitolo in forma neurale: quale rappresentazione interna del mondo serve per predire e agire bene? Le note storiche del capitolo osservavano gia' che non conosciamo ancora il modo migliore di unire i vantaggi delle reti neurali e della semantica logica: e' precisamente il fronte su cui il campo si muove oggi.

## Riferimenti

- Stuart J. Russell, Peter Norvig — *Intelligenza Artificiale: Un Approccio Moderno*, 4a edizione italiana, Pearson Italia, Vol. 1 (2021), Capitolo 10, pp. 323-352.
