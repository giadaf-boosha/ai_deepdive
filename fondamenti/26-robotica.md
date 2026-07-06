---
titolo: Robotica
capitolo: 26
parte: 6
volume: 2
pagine: "283-338"
concetti: [agent, world-models, rlhf, multi-agent-orchestration]
created: 2026-07-06
last_updated: 2026-07-06
---

# Robotica

Un robot e' un agente con un corpo: percepisce il mondo fisico attraverso sensori e lo modifica attraverso attuatori. La domanda che attraversa tutto il capitolo e' come colmare l'enorme distanza tra i due estremi del problema: da un lato flussi grezzi di pixel e letture laser, dall'altro correnti elettriche da inviare ai motori, e in mezzo obiettivi di alto livello come "porta il pasto al paziente". Nessun capitolo del libro mette cosi' tanto alla prova, tutte insieme, le tecniche viste in precedenza: stima probabilistica dello stato, ricerca, MDP e POMDP, teoria dei giochi, apprendimento per rinforzo.

La robotica e' anche il banco di prova piu' severo per l'IA perche' il mondo reale non concede sconti. Gli ambienti sono parzialmente osservabili e stocastici, gli spazi di stati e azioni sono continui e ad alta dimensionalita', il tempo non si puo' accelerare come in simulazione e gli errori hanno costi fisici: un braccio che stringe troppo rompe la lampadina, un'auto che sbaglia una predizione mette in pericolo persone. Per questo i ricercatori scompongono il problema in strati (percezione, pianificazione, controllo, interazione) e poi lavorano per ricucirli, perche' ogni separazione semplifica ma sacrifica qualcosa.

## Corpi, sensori e attuatori

L'hardware determina cosa un robot puo' fare. Le due grandi famiglie sono i manipolatori (bracci robotici, dalle celle industriali ai bracci montati su carrozzine per l'assistenza) e i robot mobili: veicoli su ruote, droni quadricottero, veicoli subacquei autonomi, rover planetari, robot con gambe per terreni impraticabili.

I sensori si dividono in passivi, come le fotocamere, che si limitano a raccogliere segnali gia' presenti nell'ambiente, e attivi, come sonar e lidar, che emettono energia e ne misurano il ritorno. Tre categorie contano piu' di tutte: i telemetri (sonar, videocamere a tempo di volo, lidar, radar) per misurare distanze; i sensori di posizione, come il GPS all'aperto o i segnalatori radio al chiuso; i sensori propriocettivi, che informano il robot del suo stesso corpo, dai trasduttori angolari sui giunti all'odometria delle ruote, notoriamente imprecisa perche' le ruote slittano. Sensori di forza e torsione completano il quadro quando il robot maneggia oggetti fragili.

Sul fronte degli attuatori, motori elettrici, idraulici o pneumatici muovono giunti rotanti o prismatici. Per afferrare, la pinza a due ganasce parallele resta lo standard per la sua semplicita'; le mani antropomorfe con decine di attuatori offrono molta piu' destrezza, ma controllarle e' proporzionalmente piu' difficile.

## Percepire: sapere dove sono le cose (e dove sono io)

La percezione robotica trasforma misurazioni rumorose in una rappresentazione interna utile a decidere. Il quadro formale e' quello del filtraggio: mantenere uno stato-credenza, cioe' una distribuzione di probabilita' sugli stati possibili, aggiornata a ogni passo combinando un modello di movimento (come le azioni cambiano lo stato) e un modello sensoriale (come lo stato genera le osservazioni). Rispetto al caso discreto visto nei capitoli precedenti, qui le variabili sono continue e l'aggiornamento usa integrali invece di sommatorie.

Il problema simbolo e' la localizzazione: capire dove si trova il robot su una mappa nota. Due famiglie di algoritmi dominano. La localizzazione Monte Carlo usa il particle filtering: una nuvola di ipotesi campionate che all'inizio copre tutta la mappa, si addensa nelle zone compatibili con le misurazioni e alla fine collassa sulla posizione vera. Il filtro di Kalman esteso (EKF) rappresenta invece la credenza come una gaussiana e linearizza i modelli non lineari con un'espansione di Taylor: funziona bene quando i riferimenti spaziali (landmark) sono facili da identificare, mentre in presenza di ambiguita' la distribuzione diventa multimodale e le particelle tornano preferibili.

Quando la mappa non esiste, il robot affronta un problema uovo-e-gallina: localizzarsi rispetto a una mappa che sta costruendo mentre si muove. E' lo SLAM (simultaneous localization and mapping), risolto con estensioni dell'EKF, metodi a grafo ed expectation-maximization; e' una delle tecnologie abilitanti di aspirapolvere robot e veicoli autonomi. Il machine learning entra in gioco anche qui: con la riduzione dimensionale per comprimere percezioni multidimensionali, e con approcci auto-supervisionati in cui un sensore affidabile a corto raggio etichetta automaticamente i dati per addestrare un classificatore che opera a lungo raggio, come nel veicolo autonomo che impara a riconoscere la superficie transitabile.

## Lo spazio delle configurazioni e la pianificazione del movimento

Per pianificare un movimento conviene cambiare punto di vista: invece di ragionare su tutti i punti del corpo del robot nello spazio di lavoro, si rappresenta l'intero robot come un singolo punto in uno spazio astratto, lo spazio delle configurazioni (spazio C), con una dimensione per ogni grado di liberta'. Un braccio con due giunti vive in uno spazio a due angoli; gli ostacoli fisici, anche semplici, assumono in questo spazio forme sorprendentemente contorte. Le funzioni di cinematica diretta e inversa traducono tra configurazioni e posizioni nel mondo. In pratica lo spazio C non si costruisce mai esplicitamente: lo si sonda con un rilevatore di collisioni che dice se una data configurazione e' libera.

La pianificazione del movimento cerca un cammino continuo nello spazio libero da una configurazione di partenza a una obiettivo, il classico "problema dei trasportatori di pianoforti". Le strategie principali sono quattro. I grafi di visibilita' collegano i vertici degli ostacoli poligonali e garantiscono il cammino piu' breve, che pero' rasenta gli ostacoli. I diagrammi di Voronoi fanno l'opposto, mantenendo il robot il piu' lontano possibile da tutto. La scomposizione in celle discretizza lo spazio in una griglia e applica ricerca su grafo, ma soffre della maledizione della dimensionalita' e produce cammini a scalini (varianti come A* ibrido tengono conto dello stato continuo per generare traiettorie percorribili). Infine i metodi randomizzati: le roadmap probabilistiche (PRM) campionano configurazioni libere a caso e le collegano, mentre gli alberi RRT crescono incrementalmente da partenza e arrivo fino a incontrarsi. Non sono completi in senso stretto ma probabilisticamente completi, e scalano bene in molte dimensioni.

Un approccio complementare e' l'ottimizzazione delle traiettorie: si parte da un cammino semplice ma in collisione (per esempio una linea retta) e lo si deforma minimizzando un funzionale di costo che combina efficienza e distanza dagli ostacoli, con la discesa del gradiente guidata dal calcolo delle variazioni. Si trova un ottimo locale, non globale, ma nella pratica funziona.

## Dal piano al motore: il controllo

Avere un cammino non basta: bisogna eseguirlo. Il controllo a ciclo aperto usa la dinamica inversa per calcolare quali coppie applicare ai motori, ma qualsiasi imprecisione nel modello (masse, inerzie, attriti) fa accumulare errori. Il controllo a ciclo chiuso confronta continuamente posizione desiderata e reale e corregge. Il controllore proporzionale (P) applica una forza proporzionale all'errore, ma tende a oscillare come una molla attorno al riferimento; aggiungere un termine derivativo (PD) smorza le oscillazioni; il termine integrale (PID) elimina gli errori sistematici di lungo periodo. Il PID e' il cavallo di battaglia dell'industria. Il controllo a coppia calcolata combina un componente feedforward, che usa il modello per anticipare la coppia necessaria, con un feedback che corregge il residuo.

Il controllo ottimo unifica pianificazione e inseguimento: si ottimizza direttamente sulla sequenza di controlli, rispettando i vincoli della dinamica. Quando il costo e' quadratico e la dinamica lineare, il regolatore lineare quadratico (LQR) fornisce la politica ottima risolvendo un'equazione di Riccati; per i sistemi reali si usa l'ILQR, che linearizza iterativamente attorno alla soluzione corrente.

L'incertezza cambia le regole: servono politiche, non piani rigidi. Il controllo predittivo basato su modello (MPC) pianifica su un orizzonte breve, esegue la prima azione e ripianifica a ogni passo, incorporando le nuove informazioni. E quando l'informazione stessa e' scarsa, il robot puo' compiere azioni deliberate di raccolta di informazioni, come i movimenti controllati che sfruttano il contatto con una superficie per ridurre l'incertezza: la strategia che centra un buco stretto non mirando al centro, ma appoggiandosi a un lato e facendosi guidare dalla geometria.

## Imparare a muoversi e a stare tra le persone

Quando il modello dinamico non e' scrivibile a mano, entra il reinforcement learning. Il collo di bottiglia e' l'efficienza campionaria: il mondo reale gira a velocita' reale e i fallimenti rompono cose. Le risposte sono diverse: apprendimento basato su modello, che alterna stima dei parametri fisici e miglioramento della politica; trasferimento sim-to-real, addestrando in simulazione politiche robuste grazie alla randomizzazione del dominio (variare attriti, masse, illuminazione tra le simulazioni); primitive di movimento parametrizzate al posto di comandi di basso livello; meta-apprendimento e apprendimento per trasferimento per riusare esperienza tra compiti; esplorazione sicura, che vincola le azioni per evitare stati pericolosi.

La maggior parte dei robot, pero', non lavora in isolamento: opera attorno a persone e per persone. Il coordinamento si puo' formulare come un gioco a informazione incompleta tra robot e umano, dove ciascuno ha i propri obiettivi e le azioni di ciascuno influenzano l'altro. La scomposizione pratica e' predire le azioni umane, assumendo che le persone siano agenti "rumorosamente razionali" rispetto a obiettivi che il robot inferisce osservandole, e poi agire date le predizioni; le versioni piu' sofisticate tengono conto anche dell'influenza delle azioni del robot su quelle umane, come l'auto autonoma che si inserisce in corsia confidando in un fisiologico rallentamento altrui.

La seconda sfida e' capire cosa vogliono le persone. Due strade: apprendere la funzione di costo da dimostrazioni umane (se guidi in modo prudente, il robot inferisce che pesi la sicurezza piu' dell'efficienza) oppure imitare direttamente la politica, la clonazione comportamentale, che pero' generalizza male fuori dalla distribuzione delle dimostrazioni; tecniche iterative come DAgger raccolgono nuove etichette umane sugli stati che la politica corrente incontra davvero. Accanto alla visione deliberativa esiste quella reattiva: controllori semplici, come le macchine a stati aumentate dell'architettura di sussunzione, che fanno camminare un esapode su terreno accidentato senza alcun modello del mondo, ma che scalano male verso compiti complessi.

## Idee chiave

- Un robot combina sensori e attuatori in ambienti stocastici, parzialmente osservabili e popolati da altri agenti: MDP, POMDP e teoria dei giochi sono i formalismi naturali, complicati da spazi continui ad alta dimensionalita' e dall'impossibilita' di "annullare" gli errori fisici.
- Risolvere tutto il problema end-to-end e' oggi troppo difficile: la pratica scompone in percezione, pianificazione del movimento, controllo e interazione, accettando la suboptimalita' della separazione.
- La percezione mantiene uno stato-credenza con filtri probabilistici (particle filtering, filtri di Kalman); localizzazione e SLAM ne sono le applicazioni cardine.
- Lo spazio delle configurazioni riduce il robot a un punto; il movimento si pianifica con grafi di visibilita', diagrammi di Voronoi, scomposizione in celle, metodi randomizzati (PRM, RRT) o ottimizzazione delle traiettorie.
- I cammini si eseguono con controllori a ciclo chiuso (PID, coppia calcolata); il controllo ottimo (LQR, ILQR) unisce pianificazione e controllo ottimizzando direttamente sulle azioni.
- Sotto incertezza servono politiche: ripianificazione online in stile MPC e azioni esplicite di raccolta di informazioni.
- Il reinforcement learning robotico punta tutto sull'efficienza campionaria: modelli, sim-to-real con randomizzazione del dominio, primitive di movimento, esplorazione sicura.
- Interagire con le persone richiede predizione dei comportamenti umani, apprendimento delle preferenze da dimostrazioni e correzioni, e comportamenti leggibili che rendano il robot prevedibile.

## Perche conta oggi

Il capitolo descrive, con vent'anni di anticipo sul lessico attuale, l'anatomia di qualsiasi [agente](../kb/concetti/agent.md) che opera in un ambiente reale: percepire, mantenere una credenza sullo stato, pianificare gerarchicamente, agire, ripianificare quando le cose cambiano. Il ciclo MPC (pianifica su orizzonte breve, esegui la prima azione, osserva, ripianifica) e' esattamente il loop di un agente LLM che alterna ragionamento e [tool use](../kb/concetti/tool-use.md) dentro un [agent harness](../kb/concetti/agent-harness.md), e la separazione tra pianificazione dei compiti, pianificazione del movimento e controllo prefigura le architetture a piu' livelli con cui oggi si orchestrano sotto-agenti specializzati in un sistema di [multi-agent orchestration](../kb/concetti/multi-agent-orchestration.md).

Anche i temi di apprendimento sono attualissimi. L'apprendimento delle preferenze da dimostrazioni e correzioni umane e' l'antenato diretto di [RLHF](../kb/concetti/rlhf.md): il problema di fondo, inferire cio' che l'utente vuole davvero invece di ottimizzare una ricompensa scritta male, e' identico. E il trasferimento sim-to-real, con la sua dipendenza da simulatori fedeli della dinamica, anticipa il ruolo dei [world models](../kb/concetti/world-models.md) nell'addestrare agenti (robotici e non) in ambienti sintetici prima di esporli al mondo reale, dove oggi i modelli fondazionali per la robotica (vision-language-action) stanno riportando queste idee al centro della scena.

## Riferimenti

- Stuart J. Russell, Peter Norvig — *Intelligenza Artificiale: Un Approccio Moderno*, 4a edizione italiana, Pearson Italia, Vol. 2 (2022), Capitolo 26, pp. 283-338.
