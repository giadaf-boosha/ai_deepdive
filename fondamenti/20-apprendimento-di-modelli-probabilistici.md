---
titolo: Apprendimento di modelli probabilistici
capitolo: 20
parte: 5
concetti: [llm, fine-tuning, world-models, mixture-of-experts]
created: 2026-07-06
last_updated: 2026-07-06
---

# Apprendimento di modelli probabilistici

Un agente che opera nel mondo reale non conosce con certezza le regole che lo governano: deve ricavarle dall'esperienza. Questo capitolo affronta esattamente questa domanda: come si impara una teoria probabilistica del mondo a partire dai dati osservati? La risposta proposta e' elegante nella sua circolarita': l'apprendimento stesso puo' essere formulato come un problema di inferenza probabilistica. Osservare dati significa accumulare evidenza, e aggiornare le proprie credenze sulle ipotesi candidate e' un'applicazione diretta della regola di Bayes.

Questa prospettiva unifica temi che altrove appaiono separati: la scelta tra ipotesi in competizione, la stima di parametri numerici, il compromesso tra semplicita' del modello e aderenza ai dati, il sovradattamento. Il capitolo percorre una scala di difficolta' crescente: prima l'apprendimento bayesiano puro e le sue approssimazioni (MAP e massima verosimiglianza), poi la stima di parametri con dati completi, infine il caso piu' spinoso in cui alcune variabili non sono mai osservate, risolto dall'algoritmo expectation-maximization.

Il valore del capitolo sta nel mostrare che dietro tecniche apparentemente diverse — regressione lineare, classificatori bayesiani ingenui, clustering, modelli di Markov nascosti — c'e' un unico principio: trovare il modello che rende i dati osservati piu' plausibili, temperato da una preferenza a priori per la semplicita'.

<figure class="diagram">
<svg viewBox="0 0 760 460" role="img" aria-label="Mappa concettuale del capitolo 20: l'apprendimento bayesiano puro viene approssimato dall'ipotesi MAP, il cui prior realizza il rasoio di Occam; con prior uniforme si arriva alla massima verosimiglianza, che con dati completi si riduce a frequenze (naive Bayes), con pochi dati e' corretta dai prior coniugati e con dati incompleti porta alle variabili nascoste, risolte dall'algoritmo EM applicato a miscele di gaussiane e HMM">
<defs><marker id="arr-c20" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" class="dg-arrow"/></marker></defs>
<line x1="380" y1="68" x2="380" y2="104" class="dg-edge-primary" marker-end="url(#arr-c20)"/>
<text x="298" y="90" text-anchor="middle" class="dg-edge-label">approssimazione</text>
<line x1="470" y1="116" x2="600" y2="68" class="dg-edge" marker-end="url(#arr-c20)"/>
<text x="545" y="82" text-anchor="middle" class="dg-edge-label">il prior penalizza</text>
<line x1="380" y1="160" x2="380" y2="196" class="dg-edge-primary" marker-end="url(#arr-c20)"/>
<text x="298" y="182" text-anchor="middle" class="dg-edge-label">prior uniforme</text>
<line x1="450" y1="224" x2="545" y2="224" class="dg-edge" marker-end="url(#arr-c20)"/>
<text x="497" y="216" text-anchor="middle" class="dg-edge-label">pochi dati</text>
<line x1="300" y1="252" x2="165" y2="288" class="dg-edge" marker-end="url(#arr-c20)"/>
<text x="195" y="262" text-anchor="middle" class="dg-edge-label">dati completi</text>
<line x1="383" y1="252" x2="385" y2="288" class="dg-edge-primary" marker-end="url(#arr-c20)"/>
<text x="475" y="272" text-anchor="middle" class="dg-edge-label">dati incompleti</text>
<line x1="125" y1="344" x2="125" y2="380" class="dg-edge" marker-end="url(#arr-c20)"/>
<text x="175" y="366" text-anchor="middle" class="dg-edge-label">esempio</text>
<line x1="385" y1="344" x2="385" y2="380" class="dg-edge-primary" marker-end="url(#arr-c20)"/>
<text x="460" y="366" text-anchor="middle" class="dg-edge-label">risolte da</text>
<line x1="490" y1="408" x2="530" y2="408" class="dg-edge" marker-end="url(#arr-c20)"/>
<rect x="280" y="12" width="200" height="56" rx="10" class="dg-node-primary"/>
<text x="380" y="36" text-anchor="middle" class="dg-label">Apprendimento bayesiano</text>
<text x="380" y="52" text-anchor="middle" class="dg-sublabel">predizione ottima ma intrattabile</text>
<rect x="520" y="12" width="225" height="56" rx="10" class="dg-node"/>
<text x="632" y="36" text-anchor="middle" class="dg-label">Rasoio di Occam / MDL</text>
<text x="632" y="52" text-anchor="middle" class="dg-sublabel">l'apprendimento come compressione</text>
<rect x="290" y="104" width="180" height="56" rx="10" class="dg-node-primary"/>
<text x="380" y="128" text-anchor="middle" class="dg-label">Ipotesi MAP</text>
<text x="380" y="144" text-anchor="middle" class="dg-sublabel">la piu' probabile dati i dati</text>
<rect x="260" y="196" width="190" height="56" rx="10" class="dg-node-primary"/>
<text x="355" y="220" text-anchor="middle" class="dg-label">Massima verosimiglianza</text>
<text x="355" y="236" text-anchor="middle" class="dg-sublabel">MAP con prior uniforme</text>
<rect x="545" y="196" width="205" height="56" rx="10" class="dg-node"/>
<text x="647" y="220" text-anchor="middle" class="dg-label">Prior coniugati (beta)</text>
<text x="647" y="236" text-anchor="middle" class="dg-sublabel">iperparametri = contatori virtuali</text>
<rect x="20" y="288" width="210" height="56" rx="10" class="dg-node"/>
<text x="125" y="312" text-anchor="middle" class="dg-label">Stima con dati completi</text>
<text x="125" y="328" text-anchor="middle" class="dg-sublabel">parametri = frequenze osservate</text>
<rect x="290" y="288" width="190" height="56" rx="10" class="dg-node-primary"/>
<text x="385" y="312" text-anchor="middle" class="dg-label">Variabili nascoste</text>
<text x="385" y="328" text-anchor="middle" class="dg-sublabel">mai osservate, meno parametri</text>
<rect x="20" y="380" width="210" height="56" rx="10" class="dg-node"/>
<text x="125" y="404" text-anchor="middle" class="dg-label">Naive Bayes</text>
<text x="125" y="420" text-anchor="middle" class="dg-sublabel">indipendenza data la classe</text>
<rect x="280" y="380" width="210" height="56" rx="10" class="dg-node-accent"/>
<text x="385" y="404" text-anchor="middle" class="dg-label">Algoritmo EM</text>
<text x="385" y="420" text-anchor="middle" class="dg-sublabel">alterna passo E e passo M</text>
<rect x="530" y="380" width="215" height="56" rx="10" class="dg-node"/>
<text x="637" y="404" text-anchor="middle" class="dg-label">Miscele di gaussiane, HMM</text>
<text x="637" y="420" text-anchor="middle" class="dg-sublabel">clustering, forward-backward</text>
</svg>
<figcaption>Mappa concettuale del capitolo 20: dall'apprendimento bayesiano puro, attraverso le approssimazioni MAP e di massima verosimiglianza, fino alle variabili nascoste e all'algoritmo EM.</figcaption>
</figure>

## Imparare e' aggiornare credenze: la visione bayesiana

L'esempio conduttore e' volutamente giocoso: sacchetti di caramelle con proporzioni ignote di due gusti, ciliegia e lime, incartate in modo indistinguibile. Cinque ipotesi possibili descrivono la composizione del sacchetto, dal 100% ciliegia al 100% lime. Ogni caramella scartata e' un dato; il compito e' predire il gusto della prossima.

L'apprendimento bayesiano non sceglie un'ipotesi: le mantiene tutte. Per ciascuna calcola la probabilita' a posteriori, proporzionale al prodotto tra la probabilita' a priori dell'ipotesi e la verosimiglianza dei dati sotto quell'ipotesi. Le predizioni sono medie pesate delle predizioni di tutte le ipotesi, con pesi pari alle rispettive probabilita' a posteriori. Il risultato notevole e' che questa predizione e' ottima: nessun altro metodo, in media, fa meglio, e con l'accumularsi dei dati la probabilita' delle ipotesi false tende a zero, cosi' che la predizione bayesiana finisce per coincidere con l'ipotesi vera.

Il prezzo di questa ottimalita' e' computazionale: quando lo spazio delle ipotesi e' enorme o continuo, sommare (o integrare) su tutte diventa intrattabile. Da qui la necessita' di approssimazioni.

## MAP, massima verosimiglianza e il rasoio di Occam

La prima approssimazione e' predire in base alla singola ipotesi piu' probabile dati i dati: l'ipotesi massima a posteriori, o MAP. E' una scommessa piu' rischiosa della media bayesiana, ma trasforma una sommatoria in un problema di ottimizzazione, in genere molto piu' abbordabile. Con l'aumentare dei dati, le due predizioni convergono.

Il ruolo della distribuzione a priori merita attenzione: penalizza la complessita'. Le ipotesi molto espressive si adattano a qualsiasi insieme di dati, ma sono tante e ciascuna parte con probabilita' a priori bassa; le ipotesi semplici partono avvantaggiate. Il compromesso tra complessita' e adattamento diventa esplicito passando ai logaritmi: massimizzare la probabilita' a posteriori equivale a minimizzare i bit necessari a codificare l'ipotesi piu' i bit necessari a codificare i dati data l'ipotesi. E' il principio della minima lunghezza della descrizione (MDL), una versione formale del rasoio di Occam: l'apprendimento come compressione.

Se si assume una distribuzione a priori uniforme — nessuna ragione per preferire un'ipotesi all'altra — MAP si riduce a scegliere l'ipotesi che massimizza la sola verosimiglianza dei dati: la massima verosimiglianza (ML), il metodo standard della statistica classica. Funziona bene con molti dati, quando l'evidenza sommerge qualsiasi prior; con pochi dati mostra i suoi limiti, come vedremo.

## Stimare parametri con dati completi

Quando la struttura del modello e' fissata e ogni osservazione contiene valori per tutte le variabili, il compito si chiama stima di densita' con dati completi. La ricetta di massima verosimiglianza e' meccanica: si scrive la verosimiglianza dei dati in funzione dei parametri, si passa al logaritmo per trasformare prodotti in somme, si deriva rispetto a ciascun parametro e si azzera la derivata.

Per una rete bayesiana con tabelle di probabilita' condizionata il risultato e' rassicurante: il problema si spezza in un sottoproblema indipendente per parametro, e la stima ottima di ogni probabilita' condizionata e' semplicemente la frequenza osservata nei dati. Se il 60% delle caramelle scartate e' alla ciliegia, la stima ML della proporzione e' 0,6. Lo stesso schema vale nel continuo: per una gaussiana, media e deviazione standard di massima verosimiglianza coincidono con media e scarto dei campioni. E la regressione lineare classica, che minimizza la somma dei quadrati degli errori, si rivela essere esattamente la stima ML sotto l'ipotesi che i dati siano generati da una retta piu' rumore gaussiano a varianza fissa: la perdita quadratica non e' una scelta arbitraria, e' una conseguenza del modello di rumore.

Il capitolo dedica spazio al modello bayesiano ingenuo (naive Bayes), la rete piu' usata nel machine learning classico: una variabile di classe come radice e gli attributi come foglie, assunti condizionalmente indipendenti data la classe. L'assunzione e' quasi sempre falsa, eppure il classificatore funziona sorprendentemente bene, scala su problemi enormi (con n attributi booleani i parametri sono solo 2n+1), tollera dati rumorosi o mancanti e non richiede alcuna ricerca per l'addestramento. Il difetto tipico e' l'eccesso di sicurezza: predizioni con probabilita' schiacciate verso 0 o 1.

Qui compare anche una distinzione concettuale importante: i modelli generativi apprendono la distribuzione completa di ogni classe e possono generare esempi sintetici; i modelli discriminativi (regressione logistica, alberi di decisione) apprendono direttamente il confine tra le classi. Con molti dati i discriminativi tendono a vincere, con pochi dati spesso vincono i generativi.

## Prior, distribuzioni coniugate e incertezza sui parametri

La massima verosimiglianza ha un difetto serio con campioni piccoli: dopo una sola caramella alla ciliegia conclude che il sacchetto e' ciliegia al 100%, e assegna probabilita' zero a eventi mai osservati. L'antidoto bayesiano e' trattare i parametri stessi come variabili casuali con una distribuzione a priori, da aggiornare man mano che i dati arrivano.

Per un parametro compreso tra 0 e 1 la famiglia naturale e' quella delle distribuzioni beta, governate da due iperparametri a e b. La proprieta' chiave e' la coniugazione: se il prior e' una beta, anche il posterior dopo ogni osservazione resta una beta, con a incrementato per ogni ciliegia e b per ogni lime. Gli iperparametri agiscono da contatori virtuali: partire da Beta(a, b) equivale ad aver gia' visto a-1 successi e b-1 insuccessi. Con dati abbondanti il posterior si stringe attorno al valore vero e l'approccio bayesiano converge a quello di massima verosimiglianza; con dati scarsi, il prior evita conclusioni assurde.

L'idea si estende con naturalezza: assumendo l'indipendenza dei parametri, ogni parametro di una rete bayesiana riceve il suo prior, e l'intero processo di apprendimento diventa un problema di inferenza in una rete piu' grande in cui parametri e dati sono tutti nodi. In questa formulazione esiste un solo algoritmo di apprendimento: l'inferenza bayesiana, tipicamente approssimata via MCMC. La regressione lineare bayesiana illustra il beneficio pratico: invece di una singola retta, si ottiene una distribuzione sulle rette, e l'incertezza della predizione cresce allontanandosi dai dati osservati — esattamente il comportamento che il buon senso richiede e che la regressione classica non offre.

Il capitolo tocca anche due estensioni: l'apprendimento della struttura della rete (una ricerca nello spazio dei grafi, guidata da test di indipendenza o da punteggi che penalizzano la complessita') e la stima di densita' non parametrica, dove il modello e' l'insieme dei dati stessi, interrogato via k vicini piu' prossimi o funzioni kernel; in entrambi i casi la granularita' giusta si sceglie con la convalida incrociata.

## Variabili nascoste e l'algoritmo EM

Molti domini reali contengono variabili latenti che non compaiono mai nei dati: una cartella clinica registra sintomi e terapie, quasi mai la malattia in se'. Perche' non eliminarle? Perche' le variabili nascoste possono ridurre drasticamente il numero di parametri: nell'esempio del capitolo, togliere il nodo latente da una piccola rete diagnostica fa esplodere i parametri da 78 a 708. Meno parametri significa meno dati necessari.

Il problema e' circolare: se conoscessimo i valori delle variabili nascoste, stimare i parametri sarebbe banale conteggio; se conoscessimo i parametri, potremmo inferire i valori nascosti. L'algoritmo expectation-maximization (EM) rompe il circolo fingendo di conoscere i parametri: nel passo E usa il modello corrente per calcolare la distribuzione a posteriori delle variabili nascoste (i "conteggi attesi"); nel passo M ricalcola i parametri massimizzando la verosimiglianza come se quei conteggi fossero osservazioni reali. Si itera fino alla convergenza, e si dimostra che ogni iterazione aumenta la verosimiglianza dei dati.

Le applicazioni mostrate sono tre. Nel clustering non supervisionato con miscele di gaussiane, EM alterna l'assegnamento probabilistico dei punti alle componenti e il ricalcolo di medie, covarianze e pesi: partendo da 500 punti senza etichette, ricostruisce un modello quasi indistinguibile da quello generatore. Nelle reti bayesiane con variabili nascoste, i conteggi attesi si ottengono come sottoprodotto dell'inferenza standard. Nei modelli di Markov nascosti (HMM), la complicazione e' che le probabilita' di transizione sono condivise nel tempo, e i conteggi attesi si calcolano con l'algoritmo forward-backward, usando lo smoothing e non il semplice filtraggio.

EM non e' una bacchetta magica: converge a massimi locali, puo' degenerare (una gaussiana che collassa su un singolo punto porta la verosimiglianza a infinito), rallenta molto vicino alla soluzione — motivo per cui in pratica lo si combina con metodi basati sul gradiente. E c'e' un limite piu' profondo, l'identificabilita': con variabili mai osservate, modelli diversi possono spiegare i dati esattamente allo stesso modo (basta scambiare le etichette dei due sacchetti), e nessuna quantita' di dati puo' distinguerli.

## Idee chiave

- L'apprendimento bayesiano tratta l'apprendimento come inferenza: mantiene tutte le ipotesi e le pesa per la probabilita' a posteriori. E' la predizione ottima, ma diventa intrattabile su spazi di ipotesi grandi.
- L'ipotesi MAP approssima l'approccio bayesiano scegliendo la singola ipotesi piu' probabile; il prior penalizza la complessita' e realizza in pratica il rasoio di Occam, in forma equivalente al principio MDL.
- La massima verosimiglianza e' MAP con prior uniforme: con dati completi e reti bayesiane, la stima si decompone parametro per parametro e coincide con le frequenze osservate.
- Con pochi dati la massima verosimiglianza fallisce (probabilita' zero per eventi non visti); i prior coniugati come la famiglia beta correggono il problema con "conteggi virtuali".
- Il classificatore bayesiano ingenuo e' semplice, scalabile e robusto nonostante l'assunzione di indipendenza quasi sempre violata.
- Quando ci sono variabili nascoste, EM alterna inferenza sui valori latenti (passo E) e massimizzazione dei parametri (passo M), aumentando la verosimiglianza a ogni iterazione; si applica a miscele di gaussiane, reti bayesiane e HMM.
- Apprendere la struttura di una rete e' un problema di selezione di modelli: una ricerca discreta nello spazio delle strutture, con penalizzazione della complessita' per evitare reti completamente connesse.
- I modelli non parametrici (nearest-neighbors, kernel) rappresentano la distribuzione direttamente con i dati, senza fissare in anticipo il numero di parametri.

## Perche conta oggi

Le idee di questo capitolo sono il substrato concettuale su cui poggia l'addestramento dei modelli moderni. Un [LLM](../kb/concetti/llm.md) e' a tutti gli effetti un gigantesco stimatore di massima verosimiglianza: il pre-training minimizza la log-loss sul token successivo, che e' esattamente la verosimiglianza logaritmica negativa dei dati sotto il modello. Il compromesso tra complessita' e adattamento discusso via MAP e MDL riappare ovunque si parli di regolarizzazione e sovradattamento, incluso il [fine-tuning](../kb/concetti/fine-tuning.md), dove pochi dati specifici devono aggiornare un modello senza fargli dimenticare il prior implicito acquisito in pre-training — una dinamica che ricorda da vicino l'aggiornamento bayesiano con conteggi virtuali.

Anche i concetti architetturali hanno eredi diretti. Le distribuzioni miscela, cuore del clustering con EM, sono l'antenato concettuale dei [mixture-of-experts](../kb/concetti/mixture-of-experts.md), dove una variabile latente (quale esperto attivare) governa la generazione. E la distinzione tra modelli generativi e discriminativi e' tornata centrale: i modelli generativi hanno vinto la scala, e l'idea che un agente debba apprendere una distribuzione completa sul mondo per predire e decidere e' la tesi di fondo dei [world models](../kb/concetti/world-models.md). Chi lavora oggi con l'incertezza delle predizioni — calibrazione, confidenza, quando un modello dovrebbe dire "non lo so" — sta riproponendo, su scala diversa, il passaggio dalla stima puntuale alla distribuzione a posteriori che questo capitolo motiva con una manciata di caramelle.
