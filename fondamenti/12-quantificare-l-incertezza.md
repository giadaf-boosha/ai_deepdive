---
titolo: Quantificare l'incertezza
capitolo: 12
parte: 4
volume: 1
pagine: "397-422"
concetti: [agent, world-models, inference, llm]
created: 2026-07-06
last_updated: 2026-07-06
---

# Quantificare l'incertezza

Il mondo reale non offre certezze a un agente: i sensori vedono solo una parte dell'ambiente, gli effetti delle azioni non sono deterministici, e a volte ci sono avversari di mezzo. Un agente puramente logico gestisce questa situazione con gli stati-credenza, cioe' insiemi di tutti gli stati possibili, ma il metodo scala male: costringe a considerare ogni spiegazione, anche la piu' remota, e a costruire piani condizionali che gonfiano senza limite. Peggio ancora, spesso nessun piano garantisce il risultato, eppure l'agente deve comunque scegliere.

Il capitolo 12 di Russell e Norvig affronta esattamente questa domanda: come si ragiona e si decide quando la conoscenza e' incompleta? La risposta proposta e' la teoria della probabilita', intesa come strumento per assegnare gradi numerici di credenza alle proposizioni, da 0 (certamente falsa) a 1 (certamente vera). L'esempio guida e' quotidiano: un taxi autonomo che deve portare un passeggero all'aeroporto non puo' dimostrare che partire 90 minuti prima "funzionera'", ma puo' stimare quanto e' probabile che funzioni, e confrontare quel piano con alternative piu' o meno prudenti.

La posta in gioco non e' solo rappresentare l'incertezza, ma agire razionalmente sotto incertezza. Il capitolo introduce cosi' anche il principio che collega credenze e scelte: un agente razionale seleziona l'azione con la massima utilita' attesa, combinando probabilita' degli esiti e preferenze su di essi.

<figure class="diagram">
<svg viewBox="0 0 760 464" role="img" aria-label="Mappa concettuale del capitolo 12: dall'incertezza al fallimento dell'agente logico, alla teoria della probabilita' come gradi di credenza; la distribuzione congiunta completa e il suo muro esponenziale, compressa da indipendenza assoluta e condizionale; la regola di Bayes e il modello di Bayes ingenuo, il mondo del wumpus e la teoria delle decisioni con la massima utilita' attesa">
<defs><marker id="arr-c12" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" class="dg-arrow"/></marker></defs>
<line x1="233" y1="40" x2="272" y2="40" class="dg-edge" marker-end="url(#arr-c12)"/>
<line x1="380" y1="68" x2="380" y2="105" class="dg-edge-primary" marker-end="url(#arr-c12)"/>
<text x="470" y="90" text-anchor="middle" class="dg-edge-label">pigrizia e ignoranza</text>
<line x1="213" y1="136" x2="272" y2="136" class="dg-edge" marker-end="url(#arr-c12)"/>
<text x="242" y="128" text-anchor="middle" class="dg-edge-label">vincolano</text>
<line x1="635" y1="68" x2="635" y2="105" class="dg-edge" marker-end="url(#arr-c12)"/>
<line x1="488" y1="136" x2="527" y2="136" class="dg-edge-primary" marker-end="url(#arr-c12)"/>
<line x1="380" y1="164" x2="380" y2="201" class="dg-edge-primary" marker-end="url(#arr-c12)"/>
<text x="290" y="188" text-anchor="middle" class="dg-edge-label">inferenza per enumerazione</text>
<line x1="470" y1="164" x2="605" y2="201" class="dg-edge" marker-end="url(#arr-c12)"/>
<text x="560" y="178" text-anchor="middle" class="dg-edge-label">regola del prodotto</text>
<line x1="330" y1="260" x2="165" y2="297" class="dg-edge" marker-end="url(#arr-c12)"/>
<line x1="383" y1="260" x2="385" y2="297" class="dg-edge" marker-end="url(#arr-c12)"/>
<text x="460" y="282" text-anchor="middle" class="dg-edge-label">da O(2^n) a O(n)</text>
<line x1="635" y1="260" x2="635" y2="297" class="dg-edge" marker-end="url(#arr-c12)"/>
<line x1="498" y1="328" x2="527" y2="328" class="dg-edge" marker-end="url(#arr-c12)"/>
<line x1="385" y1="356" x2="385" y2="393" class="dg-edge" marker-end="url(#arr-c12)"/>
<text x="470" y="378" text-anchor="middle" class="dg-edge-label">solo la frontiera conta</text>
<rect x="20" y="12" width="210" height="56" rx="10" class="dg-node"/>
<text x="125" y="36" text-anchor="middle" class="dg-label">Incertezza</text>
<text x="125" y="52" text-anchor="middle" class="dg-sublabel">sensori parziali, esiti incerti</text>
<rect x="275" y="12" width="210" height="56" rx="10" class="dg-node"/>
<text x="380" y="36" text-anchor="middle" class="dg-label">Agente logico</text>
<text x="380" y="52" text-anchor="middle" class="dg-sublabel">stati-credenza: scala male</text>
<rect x="530" y="12" width="210" height="56" rx="10" class="dg-node"/>
<text x="635" y="36" text-anchor="middle" class="dg-label">Teoria dell'utilita'</text>
<text x="635" y="52" text-anchor="middle" class="dg-sublabel">preferenze sugli esiti</text>
<rect x="10" y="108" width="200" height="56" rx="10" class="dg-node"/>
<text x="110" y="132" text-anchor="middle" class="dg-label">Assiomi di Kolmogorov</text>
<text x="110" y="148" text-anchor="middle" class="dg-sublabel">violarli espone a perdite certe</text>
<rect x="275" y="108" width="210" height="56" rx="10" class="dg-node-primary"/>
<text x="380" y="132" text-anchor="middle" class="dg-label">Teoria della probabilita'</text>
<text x="380" y="148" text-anchor="middle" class="dg-sublabel">gradi di credenza da 0 a 1</text>
<rect x="530" y="108" width="210" height="56" rx="10" class="dg-node-accent"/>
<text x="635" y="132" text-anchor="middle" class="dg-label">Teoria delle decisioni</text>
<text x="635" y="148" text-anchor="middle" class="dg-sublabel">MEU: massima utilita' attesa</text>
<rect x="275" y="204" width="210" height="56" rx="10" class="dg-node"/>
<text x="380" y="228" text-anchor="middle" class="dg-label">Distribuzione congiunta</text>
<text x="380" y="244" text-anchor="middle" class="dg-sublabel">2^n valori: muro esponenziale</text>
<rect x="530" y="204" width="210" height="56" rx="10" class="dg-node"/>
<text x="635" y="228" text-anchor="middle" class="dg-label">Regola di Bayes</text>
<text x="635" y="244" text-anchor="middle" class="dg-sublabel">dal causale al diagnostico</text>
<rect x="20" y="300" width="210" height="56" rx="10" class="dg-node"/>
<text x="125" y="324" text-anchor="middle" class="dg-label">Indipendenza assoluta</text>
<text x="125" y="340" text-anchor="middle" class="dg-sublabel">fattorizza la congiunta</text>
<rect x="275" y="300" width="220" height="56" rx="10" class="dg-node"/>
<text x="385" y="324" text-anchor="middle" class="dg-label">Indipendenza condizionale</text>
<text x="385" y="340" text-anchor="middle" class="dg-sublabel">la causa separa gli effetti</text>
<rect x="530" y="300" width="210" height="56" rx="10" class="dg-node"/>
<text x="635" y="324" text-anchor="middle" class="dg-label">Bayes ingenuo</text>
<text x="635" y="340" text-anchor="middle" class="dg-sublabel">costo O(n), filtri antispam</text>
<rect x="275" y="396" width="220" height="56" rx="10" class="dg-node"/>
<text x="385" y="420" text-anchor="middle" class="dg-label">Mondo del wumpus</text>
<text x="385" y="436" text-anchor="middle" class="dg-sublabel">quantifica il rischio (31% vs 86%)</text>
</svg>
<figcaption>Mappa del capitolo 12 — la probabilita' come risposta all'incertezza e le indipendenze che rendono l'inferenza trattabile</figcaption>
</figure>

## I limiti della logica e i gradi di credenza

Provare a codificare un dominio come la diagnosi medica in regole logiche fallisce sistematicamente. Una regola che lega un sintomo a una causa non e' mai valida in senso stretto: lo stesso dolore puo' derivare da decine di condizioni diverse, e la stessa condizione non produce sempre il sintomo. Gli autori individuano tre ragioni del fallimento: la pigrizia (elencare tutte le eccezioni costa troppo), l'ignoranza teorica (nessuna teoria completa del dominio esiste) e l'ignoranza pratica (anche con la teoria, mancano i dati sul caso specifico).

La probabilita' risolve il problema riassumendo tutta questa incertezza in un numero. Dire che un paziente con mal di denti ha una carie con probabilita' 0,8 non descrive il mondo — nel mondo la carie c'e' o non c'e' — ma descrive lo stato di conoscenza dell'agente. Ogni nuova evidenza cambia legittimamente il numero: affermazioni fatte rispetto a insiemi di evidenze diversi non si contraddicono, sono semplicemente credenze condizionate su informazioni diverse.

Le credenze da sole pero' non bastano per decidere. Servono anche le preferenze sugli esiti, formalizzate dalla teoria dell'utilita'. La combinazione delle due e' la teoria delle decisioni, il cui cuore e' il principio della Massima Utilita' Attesa (MEU): tra tutte le azioni possibili, quella razionale e' quella la cui media degli esiti, pesata per le rispettive probabilita', e' massima. Un agente basato su questo principio mantiene uno stato-credenza probabilistico, predice gli esiti delle azioni e sceglie di conseguenza.

## Mondi possibili, variabili e assiomi

La semantica della probabilita' poggia sugli stessi mattoni della logica: i mondi possibili. Lo spazio campionario e' l'insieme di tutti i mondi, mutuamente esclusivi ed esaustivi; un modello di probabilita' assegna a ciascuno un numero tra 0 e 1, con somma totale pari a 1. Una proposizione corrisponde a un insieme di mondi, e la sua probabilita' e' la somma delle probabilita' dei mondi in cui vale.

Il linguaggio usa variabili casuali con un intervallo di valori: booleane, categoriali (per esempio le condizioni del tempo), oppure continue, per cui si passa dalle distribuzioni discrete alle funzioni di densita'. Si distinguono le probabilita' a priori, valide in assenza di altre informazioni, dalle probabilita' condizionate, aggiornate su un'evidenza: P(a|b) e' definita come P(a e b) / P(b). Riscritta come regola del prodotto, P(a e b) = P(a|b) P(b), questa definizione diventa il ferro del mestiere di tutte le derivazioni successive.

Gli assiomi di Kolmogorov vincolano i gradi di credenza tra proposizioni logicamente collegate. Non sono un capriccio matematico: l'argomentazione di de Finetti mostra che un agente le cui credenze violano gli assiomi puo' essere portato a perdere denaro in modo garantito da un avversario che gli propone scommesse coerenti con le sue stesse credenze dichiarate. In altre parole, credenze incoerenti producono comportamenti irrazionali, indipendentemente da come va il mondo.

## Inferenza per enumerazione e il muro esponenziale

Se si conosce la distribuzione congiunta completa — la probabilita' di ogni combinazione di valori di tutte le variabili — ogni interrogazione ha risposta meccanica: si individuano i mondi in cui la proposizione vale e si sommano le probabilita'. Da qui derivano due operazioni ricorrenti: la marginalizzazione, che elimina variabili sommando su tutti i loro valori, e il condizionamento, che ne e' la variante con la regola del prodotto.

Un trucco pratico importante e' la normalizzazione: quando si calcola una distribuzione condizionata, il denominatore comune puo' essere trattato come una costante alfa da fissare alla fine, imponendo che i valori sommino a 1. Questo evita di stimare probabilita' che non si conoscono direttamente e semplifica molti calcoli.

Il problema e' la scala. Con n variabili booleane la tabella congiunta ha 2^n elementi: con 100 variabili si arriva a circa 10^30 valori, impossibili da memorizzare e ancor prima da stimare dai dati. La distribuzione congiunta completa resta quindi un fondamento teorico — come le tabelle di verita' per la logica — ma non uno strumento operativo. Serve un modo per comprimerla.

## Indipendenza e regola di Bayes

La prima leva di compressione e' l'indipendenza assoluta: se due gruppi di variabili non si influenzano (i problemi dentali e il meteo, per dire), la congiunta si fattorizza nel prodotto di distribuzioni piu' piccole. Per n lanci di moneta indipendenti si passa da 2^n numeri a n distribuzioni a variabile singola. Il limite e' che l'indipendenza piena tra interi sottoinsiemi di variabili e' rara nei domini reali, dove quasi tutto e' collegato a quasi tutto, anche debolmente.

La seconda leva e' la regola di Bayes, ottenuta scrivendo la regola del prodotto in entrambe le direzioni: P(b|a) = P(a|b) P(b) / P(a). Sembra un giro a vuoto — servono tre numeri per calcolarne un quarto — ma e' preziosa perche' la conoscenza disponibile e' spesso orientata in senso causale, P(effetto|causa), mentre la domanda e' diagnostica, P(causa|effetto). L'esempio del libro e' clinico: la meningite causa torcicollo nel 70% dei casi, ma poiche' la meningite e' rarissima e il torcicollo comune, la probabilita' di meningite dato il torcicollo resta bassissima, intorno allo 0,14%. E' lo stesso errore di intuizione che si commette leggendo i risultati di un test medico molto sensibile per una malattia rara.

C'e' anche una ragione di robustezza per preferire la direzione causale: se scoppia un'epidemia, la probabilita' a priori della malattia cambia, ma il legame causale tra malattia e sintomo no. Un sistema costruito su conoscenza causale si aggiorna correttamente; uno costruito su statistiche diagnostiche dirette va ricalibrato da zero.

## Indipendenza condizionale e modelli di Bayes ingenui

Con piu' evidenze contemporanee, la regola di Bayes da sola torna a scalare male: le combinazioni di sintomi crescono esponenzialmente. La svolta e' l'indipendenza condizionale: due effetti della stessa causa possono essere indipendenti tra loro una volta nota la causa. Il mal di denti e la sonda del dentista che si incastra sono entrambi provocati dalla carie, ma dato che la carie c'e' (o non c'e'), sapere dell'uno non aggiunge nulla sull'altro. La causa "separa" i suoi effetti.

Questa proprieta' permette di scomporre la congiunta in una probabilita' a priori della causa e una condizionata per ciascun effetto: la rappresentazione cresce linearmente col numero di effetti, O(n) invece di O(2^n). Il libro presenta questa struttura come uno degli sviluppi piu' importanti della storia recente dell'AI, e il capitolo successivo la generalizza nelle reti bayesiane.

Il caso piu' semplice e' il modello di Bayes ingenuo (naive Bayes): una causa, molti effetti assunti condizionalmente indipendenti anche quando non lo sono davvero. L'inferenza e' immediata: si moltiplica la probabilita' a priori di ogni causa per le condizionate degli effetti osservati e si normalizza. L'applicazione classica e' la classificazione di testi: la categoria di un articolo e' la causa, la presenza delle singole parole chiave sono gli effetti. L'assunzione di indipendenza tra parole e' palesemente falsa — certe coppie di parole viaggiano insieme — e il modello risulta troppo sicuro delle proprie previsioni, ma l'ordinamento delle categorie resta spesso corretto. E' il motivo per cui i filtri antispam basati su questa idea hanno funzionato per anni.

## Il wumpus visto con occhi probabilistici

Il capitolo chiude tornando al mondo del wumpus, il dungeon a griglia del capitolo 7. Li' un agente logico, sentendo brezza in due caselle, restava bloccato: nessuna delle tre stanze candidate a contenere un pozzo era dimostrabilmente sicura, quindi la scelta era casuale. L'agente probabilistico fa di meglio: definisce una variabile per la presenza del pozzo in ogni stanza, sfrutta il fatto che ogni stanza ha probabilita' 0,2 di contenere un pozzo indipendentemente dalle altre, e calcola le probabilita' a posteriori date le percezioni.

Il calcolo diretto sommerebbe su tutte le configurazioni delle stanze sconosciute — migliaia di termini — ma l'indipendenza condizionale salva di nuovo la situazione: le brezze osservate dipendono solo dalle stanze di frontiera, quelle adiacenti alle caselle gia' visitate, e tutto il resto della mappa sparisce nella costante di normalizzazione. Il risultato e' netto: due stanze hanno circa il 31% di probabilita' di contenere un pozzo, la terza circa l'86%. La logica sapeva solo dire "non e' sicuro"; la probabilita' dice quanto non e' sicuro, e l'agente puo' scegliere il rischio minore.

## Idee chiave

- L'incertezza non e' un incidente ma la condizione normale degli ambienti complessi, parzialmente osservabili o non deterministici; nasce da pigrizia e ignoranza, e la probabilita' serve a riassumerla.
- Le probabilita' misurano le credenze dell'agente rispetto alle evidenze disponibili, non proprieta' oggettive del singolo caso: cambiano legittimamente quando cambia l'informazione.
- Decidere richiede piu' che credere: la teoria delle decisioni unisce probabilita' e utilita', e l'azione razionale e' quella che massimizza l'utilita' attesa.
- Gli assiomi della probabilita' vincolano tra loro le credenze su proposizioni collegate; chi li viola puo' essere sfruttato sistematicamente (argomento di de Finetti).
- La distribuzione congiunta completa risponde in linea di principio a ogni interrogazione, ma la sua dimensione esponenziale la rende inutilizzabile in pratica come rappresentazione diretta.
- L'indipendenza assoluta fattorizza la congiunta in blocchi separati; l'indipendenza condizionale, legata alle relazioni causali, e' molto piu' comune e altrettanto potente.
- La regola di Bayes converte conoscenza causale in conclusioni diagnostiche ed e' il fondamento dell'inferenza probabilistica moderna; il modello di Bayes ingenuo la applica a molti effetti con costo lineare.
- Nel mondo del wumpus l'agente probabilistico batte quello logico: quantifica il rischio delle mosse invece di limitarsi a dichiararle non sicure.

## Perche conta oggi

Tutto lo stack dell'AI generativa e' probabilistico fin nelle fondamenta: un [LLM](../kb/concetti/llm.md) e' letteralmente una distribuzione condizionata sul token successivo dato il contesto, e la fase di [inference](../kb/concetti/inference.md) e' un campionamento ripetuto da quella distribuzione. Anche la temperatura di generazione, il sampling top-p e la calibrazione delle confidenze sono concetti che discendono direttamente dal vocabolario di questo capitolo. Il fenomeno del naive Bayes "troppo sicuro di se'" per assunzioni di indipendenza violate e' un antenato diretto del problema di calibrazione dei modelli attuali, misurato oggi con [benchmark dedicati](../kb/concetti/evaluation-benchmark.md).

Il salto concettuale dall'agente logico all'agente che massimizza l'utilita' attesa e' anche il salto che serve per capire gli [agent](../kb/concetti/agent.md) moderni: operano in ambienti parzialmente osservabili (un repository, il web, un browser), dove nessuna azione ha esito garantito, e devono continuamente pesare rischio e beneficio — ritentare una chiamata, chiedere conferma, scegliere tra piani alternativi. La lezione del wumpus si ripropone identica: mantenere una stima esplicita di cio' che non si sa, incorporata in [world models](../kb/concetti/world-models.md) piu' o meno formali, distingue un agente che sceglie a caso da uno che sceglie il rischio minore. E la distinzione tra conoscenza causale robusta e correlazioni diagnostiche fragili resta uno dei criteri piu' utili per giudicare quando fidarsi di un sistema appreso dai dati.

## Riferimenti

- Stuart J. Russell, Peter Norvig — *Intelligenza Artificiale: Un Approccio Moderno*, 4a edizione italiana, Pearson Italia, Vol. 1 (2021), Capitolo 12, pp. 397-422.
