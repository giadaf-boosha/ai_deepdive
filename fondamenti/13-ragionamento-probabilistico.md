---
titolo: Ragionamento probabilistico
capitolo: 13
parte: 4
volume: 1
pagine: "423-470"
concetti: [world-models, inference, agent, llm]
created: 2026-07-06
last_updated: 2026-07-06
---

# Ragionamento probabilistico

Un agente che opera in un mondo incerto ha bisogno di rappresentare probabilita' su molte variabili contemporaneamente. Il capitolo precedente mostra che la distribuzione congiunta completa risponde a qualsiasi domanda sul dominio, ma cresce in modo esponenziale con il numero di variabili: con 30 variabili booleane servirebbe piu' di un miliardo di numeri, e compilarli uno per uno e' impraticabile oltre che innaturale. La domanda del capitolo 13 e' quindi: come si rappresenta la conoscenza incerta in modo compatto, e come si ragiona su di essa in modo efficiente?

La risposta sono le reti bayesiane: grafi orientati aciclici in cui ogni nodo e' una variabile casuale e ogni arco codifica un'influenza diretta. Sfruttando le relazioni di indipendenza condizionale del dominio, una rete bayesiana puo' rappresentare la stessa distribuzione congiunta con una frazione minuscola dei parametri, e in molti casi rende l'inferenza trattabile. Il capitolo copre l'intero arco: sintassi e semantica delle reti, tecniche per specificare le distribuzioni locali, algoritmi di inferenza esatta e approssimata, e infine le reti causali, che permettono di distinguere tra osservare un evento e provocarlo.

## Un grafo che codifica l'indipendenza

Una rete bayesiana e' definita da tre elementi: un insieme di nodi, uno per ogni variabile casuale (discreta o continua); archi orientati che formano un DAG, dove un arco da X a Y indica che X influenza direttamente Y; e per ogni nodo una distribuzione condizionata dati i suoi genitori, tipicamente una tabella delle probabilita' condizionate (CPT) nel caso discreto.

L'esempio guida e' l'antifurto ideato da Judea Pearl: un allarme che puo' scattare per un'intrusione ma anche per un piccolo terremoto, e due vicini, John e Mary, che telefonano (in modo non del tutto affidabile) quando lo sentono. La topologia della rete cattura le ipotesi del dominio: le telefonate dipendono solo dall'allarme, non direttamente da intrusioni o terremoti. Tutto cio' che la rete non modella esplicitamente — batterie scariche, elicotteri di passaggio, la musica di Mary a tutto volume — resta riassunto nell'incertezza dei numeri nelle CPT. E' questo che consente a un agente piccolo di cavarsela in un mondo grande.

La semantica e' precisa: la probabilita' di un assegnamento completo di tutte le variabili e' il prodotto, su tutti i nodi, della probabilita' condizionata del valore del nodo dati i valori dei genitori. Da questa definizione discendono le proprieta' di indipendenza: ogni variabile e' condizionalmente indipendente dai suoi non discendenti dati i genitori, e piu' in generale e' indipendente da tutto il resto della rete data la sua coperta di Markov (genitori, figli e genitori dei figli). Il criterio di d-separazione permette di leggere direttamente dal grafo se due insiemi di variabili sono indipendenti dato un terzo insieme.

## Costruire bene la rete: l'ordine causale paga

La regola della catena mostra che qualsiasi ordinamento delle variabili produce una rete corretta, ma non tutte le reti corrette sono ugualmente buone. Il metodo di costruzione consiste nell'aggiungere le variabili una alla volta, collegando ogni nuova variabile solo all'insieme minimo di predecessori che la influenzano direttamente. Se si ordinano le variabili in senso causale — le cause prima degli effetti — la rete risulta compatta e i numeri richiesti sono giudizi naturali per un esperto. Con l'ordinamento causale l'antifurto richiede 10 parametri; con ordinamenti "diagnostici" infelici se ne arrivano a richiedere 13 o addirittura 31, quanti la distribuzione congiunta completa, e molti di essi corrispondono a giudizi probabilistici innaturali.

La compattezza deriva da una proprieta' generale dei sistemi localmente strutturati: se ogni variabile e' influenzata direttamente da al piu' k altre, la rete richiede circa n per 2 elevato a k numeri invece di 2 elevato a n. E' anche una garanzia di coerenza: una rete costruita cosi' non contiene probabilita' ridondanti, quindi non puo' violare gli assiomi della teoria della probabilita'.

## Distribuzioni locali compatte e variabili continue

Anche una CPT puo' diventare ingombrante se un nodo ha molti genitori. Il capitolo presenta diverse scorciatoie. I nodi deterministici hanno un valore fissato esattamente da una funzione dei genitori. L'indipendenza specifica del contesto cattura i casi in cui una dipendenza vale solo per certi valori di altre variabili (il danno di un'auto dipende dalla sua robustezza solo se c'e' stato un incidente). Il modello di OR rumoroso descrive un effetto con piu' cause indipendenti, ognuna delle quali puo' essere inibita con una certa probabilita': bastano k parametri invece di 2 elevato a k, e su reti mediche reali il risparmio e' di quattro ordini di grandezza.

Per le variabili continue si puo' discretizzare, oppure usare famiglie parametriche di distribuzioni. Nelle reti ibride, con variabili discrete e continue insieme, il caso tipico e' la gaussiana lineare: un figlio continuo ha distribuzione normale con media che varia linearmente nel valore del genitore. Per un figlio discreto con genitore continuo (compro la frutta se il costo e' basso) si usano funzioni a soglia morbida come i modelli probit ed expit, quest'ultimo basato sulla funzione logistica, onnipresente anche nel machine learning. Il caso di studio della polizza di assicurazione auto mostra come si progetta una rete realistica, con variabili nascoste come l'avversione al rischio del cliente che non si osservano mai ma tengono sparsa la struttura.

## Inferenza esatta: sommare in modo intelligente

Il compito centrale e' calcolare la distribuzione a posteriori di una variabile di query, date le variabili di evidenza osservate. L'approccio piu' diretto, l'inferenza per enumerazione, somma i prodotti di probabilita' condizionate su tutti i valori delle variabili nascoste: corretto, ma con costo temporale esponenziale nel numero di variabili.

L'algoritmo di eliminazione delle variabili migliora la situazione con una forma di programmazione dinamica: valuta l'espressione da destra a sinistra, memorizza i risultati intermedi come fattori (matrici indicizzate dai valori delle variabili) e combina i fattori con due sole operazioni, il prodotto puntuale e il summing out di una variabile. Si possono inoltre potare in anticipo tutte le variabili irrilevanti: qualsiasi variabile che non sia antenata di una variabile di query o di evidenza non incide sul risultato. Sull'esempio assicurativo il guadagno e' di circa mille volte rispetto all'enumerazione.

Quanto costa in generale? Dipende dalla struttura. Nei polialberi (reti in cui tra due nodi esiste al piu' un cammino non orientato) l'inferenza esatta e' lineare nella dimensione della rete. Nelle reti a connessioni multiple, invece, il problema e' NP-difficile — anzi #P-difficile, perche' l'inferenza bayesiana contiene come caso speciale il conteggio degli assegnamenti soddisfacenti di una formula proposizionale. Gli algoritmi di clustering (o ad albero di join) raggruppano nodi in meganodi per trasformare la rete in un polialbero e calcolare le probabilita' a posteriori di tutte le variabili in un solo passaggio, ma nel caso pessimo i meganodi diventano esponenzialmente grandi: l'intrattabilita' non sparisce, si sposta.

## Quando l'esatto non basta: campionare

Per reti grandi si passa ai metodi Monte Carlo, che stimano le probabilita' generando eventi casuali e contando. Il campionamento diretto genera ogni evento seguendo l'ordine topologico della rete, campionando ogni variabile condizionatamente ai valori gia' estratti per i suoi genitori. Il campionamento di rigetto adatta l'idea alle query condizionate: scarta i campioni incompatibili con l'evidenza. Funziona, ma la frazione di campioni utili crolla esponenzialmente col numero di variabili di evidenza, come se per stimare un evento raro si dovesse aspettare che accada davvero.

La pesatura di verosimiglianza e' un caso di campionamento di importanza: fissa le variabili di evidenza ai valori osservati, campiona solo le altre, e corregge attribuendo a ogni campione un peso pari al prodotto delle probabilita' condizionate delle evidenze. Nessun campione va sprecato, ma se le evidenze compaiono tardi nell'ordinamento i campioni diventano "allucinazioni" poco somiglianti alla realta' suggerita dalle evidenze, e la maggior parte dei pesi diventa trascurabile.

Gli algoritmi MCMC (Monte Carlo per catene di Markov) cambiano prospettiva: invece di generare ogni campione da zero, modificano casualmente uno stato corrente. Il campionamento di Gibbs ricampiona una variabile non di evidenza alla volta, condizionatamente alla sua coperta di Markov: si dimostra che la distribuzione stazionaria della catena e' esattamente la distribuzione a posteriori cercata, purche' la catena sia ergodica (cosa che le CPT con probabilita' 0 o 1 possono compromettere). Metropolis-Hastings generalizza: propone un nuovo stato da una distribuzione qualsiasi e lo accetta con una probabilita' che dipende dal rapporto tra le probabilita' a posteriori, garantendo la convergenza per qualsiasi proposta ragionevole. Un'osservazione pratica chiude la sezione: compilare la rete in codice di campionamento specifico per il modello, invece di interpretarla come struttura dati, accelera l'inferenza di due o tre ordini di grandezza.

## Dalle correlazioni alle cause

Una rete bayesiana con la freccia Fuoco verso Fumo e una con la freccia invertita rappresentano la stessa distribuzione congiunta, eppure sappiamo che spegnere il fuoco ferma il fumo e non viceversa. Le reti causali sono la sottoclasse di reti bayesiane in cui la direzione delle frecce riflette il meccanismo del mondo: ogni variabile e' determinata da un'equazione strutturale funzione dei suoi genitori e di un disturbo esogeno, un meccanismo stabile che resta invariante ai cambiamenti locali dell'ambiente.

Questa scelta ripaga quando si vogliono prevedere gli effetti degli interventi. L'operatore do del do-calculus formalizza la differenza tra osservare e agire: osservare che l'irrigatore e' acceso abbassa la probabilita' che il cielo sia coperto, ma accenderlo noi dall'esterno non cambia il meteo. L'intervento do si modella "mutilando" la rete, cioe' rimuovendo gli archi entranti nella variabile manipolata e fissandone il valore; la formula di correzione calcola poi l'effetto su qualunque altra variabile. Quando le distribuzioni necessarie non sono note, il criterio back-door indica quali variabili condizionare per bloccare i cammini spuri che risalgono attraverso le cause comuni. E' il fondamento della moderna teoria dell'inferenza causale, che consente di trarre conclusioni causali anche da dati non sperimentali, senza dover sempre ricorrere a esperimenti controllati.

## Idee chiave

- Una rete bayesiana e' un DAG con una distribuzione condizionata per ogni nodo dati i suoi genitori: una rappresentazione della conoscenza incerta con un ruolo paragonabile a quello della logica proposizionale per la conoscenza certa.
- La rete codifica in forma concisa le relazioni di indipendenza condizionale del dominio, leggibili dal grafo tramite non-discendenti, coperta di Markov e d-separazione.
- La rete definisce una distribuzione congiunta completa come prodotto delle distribuzioni locali, ed e' spesso esponenzialmente piu' piccola della congiunta enumerata; ordinare le variabili in senso causale massimizza la compattezza.
- Distribuzioni canoniche (nodi deterministici, OR rumoroso, gaussiane lineari, probit/expit) e reti ibride permettono di specificare in modo compatto anche nodi con molti genitori o variabili continue.
- L'inferenza esatta calcola le probabilita' a posteriori valutando somme di prodotti; l'eliminazione delle variabili evita i calcoli ripetuti ed e' lineare nei polialberi, ma il problema generale e' NP-difficile (anzi #P-difficile).
- Quando l'esatto e' fuori portata, il campionamento fornisce stime consistenti: pesatura di verosimiglianza e metodi MCMC come Gibbs e Metropolis-Hastings scalano a reti che gli algoritmi esatti non possono trattare.
- Le reti causali aggiungono alle reti bayesiane il vincolo dell'ordinamento causale e, con l'operatore do e il criterio back-door, permettono di predire gli effetti degli interventi e non solo delle osservazioni.

## Perche conta oggi

Le reti bayesiane restano il linguaggio di riferimento per costruire [world models](../kb/concetti/world-models.md) espliciti e interpretabili: ogni numero ha un significato preciso, ogni indipendenza e' dichiarata, e si puo' verificare perche' il sistema ha tratto una conclusione. E' un contrasto istruttivo con gli [LLM](../kb/concetti/llm.md), che comprimono le regolarita' del mondo in pesi opachi: molte delle domande aperte sulla loro affidabilita' — quando una correlazione appresa e' anche una relazione causale, quanto e' calibrata una risposta — sono esattamente le domande che questo capitolo affronta in forma esplicita. La distinzione tra osservare e intervenire, formalizzata dal do-calculus, e' oggi centrale anche nel dibattito su cosa i modelli linguistici capiscono davvero dei meccanismi che descrivono.

Sul piano algoritmico, l'eredita' e' diretta. Il campionamento e la stima di distribuzioni a posteriori sono il cuore dell'[inference](../kb/concetti/inference.md) moderna, e i metodi MCMC del capitolo sono tuttora la colonna portante della statistica bayesiana usata per valutare e calibrare i modelli. Per un [agent](../kb/concetti/agent.md) che deve decidere sotto incertezza — quale tool invocare, quanto fidarsi di un'osservazione, se un'azione causera' l'effetto voluto — il ragionamento probabilistico strutturato e' il complemento naturale delle capacita' generative: architetture che combinano LLM con modelli probabilistici espliciti, ad esempio in pipeline di [tool use](../kb/concetti/tool-use.md) con stime di confidenza, riprendono precisamente questa divisione dei compiti.

## Riferimenti

- Stuart J. Russell, Peter Norvig — *Intelligenza Artificiale: Un Approccio Moderno*, 4a edizione italiana, Pearson Italia, Vol. 1 (2021), Capitolo 13, pp. 423-470.
