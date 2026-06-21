---
name: World Models
aliases: [world model, world foundation model, WFM, modello del mondo, simulatore del mondo, physical AI world model]
categoria: architettura
created: 2026-06-09
last_updated: 2026-06-21
mentions_count: 10
---

# World Models

## Cos'e

Un world model e' un modello AI che apprende una rappresentazione interna della struttura e della dinamica di un ambiente per poter predire, pianificare e ragionare su cosa accadra' in futuro dato uno stato corrente e un'azione. La definizione operativa e' semplice: un agente con un world model non ha bisogno di interagire fisicamente con l'ambiente per valutare un'azione — puo' simularla internamente, osservare il risultato predetto, e scegliere in base a quello. La differenza rispetto a un modello che reagisce al presente e' la proiezione nel futuro: il world model mantiene uno stato interno che rappresenta il mondo e lo aggiorna con ogni nuova osservazione.

Il concetto ha radici nella psicologia cognitiva (Craik, 1943) e nella robotica classica, dove un "environmental model" era una mappa geometrica dello spazio. La svolta moderna e' l'abbandono delle rappresentazioni simboliche esplicite (mappe, grafi di stati) in favore di rappresentazioni neurali apprese dai dati: i world model attuali apprendono le dinamiche dell'ambiente direttamente da video, sensori o log di interazione, senza che un ingegnere definisca le regole fisiche a mano.

Il tema e' diventato centrale nel 2025-2026 per due ragioni convergenti. Primo, i modelli linguistici e multimodali hanno dimostrato capacita' di world modeling implicito: un LLM che risponde "se rilascio un oggetto cade" non ha mai visto un oggetto cadere, ma ha appreso la dinamica dalla distribuzione del linguaggio. Secondo, l'esigenza di addestrare sistemi robotici e di guida autonoma in ambienti virtuali sicuri prima del deployment fisico ha reso i world model per il physical AI la frontiera piu' attiva nel segmento.

Il punto di discontinuita' piu' recente e' NVIDIA Cosmos 3 (1 giugno 2026): il primo omnimodel aperto con reasoning fisico e generazione di azioni in un'unica architettura, basato su Mixture-of-Transformers e distribuito con pesi aperti su Hugging Face. Il lancio ha esplicitamente posizionato i world model come infrastruttura fondamentale per il physical AI — robotica, veicoli autonomi, smart spaces — e ha attirato attorno a Cosmos 3 una coalizione di partner (Cosmos Coalition) tra cui Generalist AI, Runway, Skild AI e Agile Robots.

## Come funziona

Un world model apprende a predire il prossimo stato del mondo dato lo stato corrente e un'azione. L'architettura tipica e' composta da tre moduli.

Encoder di stato. Trasforma l'input osservabile (frame video, dati sensoriali, testo) in una rappresentazione latente compressa. L'encoder apprende a estrarre le feature rilevanti per predire il futuro, ignorando il rumore. In modelli come Cosmos 3 l'encoder e' multimodale: processa testo, immagini, video e audio in un unico spazio latente.

Modello di transizione (core del world model). Prende lo stato corrente latente e l'azione (o il comando in linguaggio naturale) e predice lo stato futuro latente. In architetture recenti questo modulo e' il punto di innovazione principale: puo' essere autoregressivo (genera il futuro token per token, come un LLM che genera la descrizione del futuro), diffusion-based (genera il futuro come campione da una distribuzione appresa), o — nel caso di Cosmos 3 — un transformer di ragionamento che prima comprende la fisica della scena e poi produce la predizione. La distinzione "reason before generate" di Cosmos 3 e' rilevante: separare la fase di comprensione dalla fase di generazione permette di usare moduli specializzati per ciascuna, con il reasoning transformer che opera in spazio simbolico-latente e il generation transformer che opera in spazio percettivo.

Decoder di output. Riconverte lo stato latente predetto in output percettivi (frame video, sequenza di azioni, audio). Il decoder determina la qualita' perceptiva del video generato e la precisione fisica dell'azione prodotta.

Architettura Mixture-of-Transformers (MoT). Introdotta da Cosmos 3, la MoT abbina un reasoning transformer e un expert generation transformer. Il reasoning transformer elabora il prompt e costruisce la rappresentazione dell'intenzione (cosa deve succedere, in quale contesto fisico, con quali vincoli); l'expert generation transformer usa quella rappresentazione per produrre il video o la sequenza di azioni. Il routing tra gli expert del generation transformer avviene sulla base del tipo di output richiesto (video reale vs. simulato, breve vs. lungo, con o senza audio). La MoT condivide la filosofia della [Mixture of Experts](./mixture-of-experts.md) classica — separa la capacita' dalla densita' computazionale per token — applicandola a un problema multimodale con struttura temporale.

Addestramento. I world model si addestrano tipicamente in modo auto-supervisato su large-scale video data (YouTube, video industriali, simulatori), ottimizzando la predizione del frame successivo o di sequenze di frame. Il regime "robot data" richiede dati di interazione fisica: log di robot che eseguono compiti (DROID, Open X-Embodiment) dove l'azione e' annotata insieme all'osservazione. La quantita' di dati fisici reali e' il collo di bottiglia principale: generare dati sintetici plausibili con un world model stesso — auto-training loop — e' una delle promesse di Cosmos 3.

## Varianti / approcci

| Approccio | Meccanismo | Esempio nei digest |
|---|---|---|
| Video prediction | Genera frame futuri dato un contesto | VideoPoet, Cosmos 1-2 |
| Action-conditioned | Predice lo stato futuro dato un'azione | RT-2, Cosmos 3 |
| Reasoning + generation (MoT) | Comprende la fisica prima di generare | Cosmos 3 (2026) |
| Language-grounded | Usa descrizioni NL per condizionare la simulazione | Gemini for Science, Cosmos 3 |
| Latent imagination (RSSM) | Apprende dinamiche in spazio latente compresso per pianificazione | DreamerV3 (2023) |
| Formal verifier | Usa un oracolo di verifica (Lean) per garantire correttezza | AlphaProof Nexus (2026) |

World model implicito nei LLM. Un LLM non ha un modulo esplicito di simulazione fisica, ma impara world knowledge implicita dalla distribuzione del linguaggio: sa che gli oggetti cadono, che il fuoco brucia, che una chiave apre una serratura. Questo world modeling implicito e' limitato rispetto a un world model che ha visto effettivamente il mondo in video — il LLM non puo' generare il frame successivo di un video, solo descriverlo — ma e' gia' sufficiente per molti task di ragionamento di senso comune.

Differenza da un modello generativo video. Un modello video come Sora genera video plausibili ma non necessariamente fisicamente corretti: puo' generare un oggetto che attraversa un muro o che fluttua. Un world model fisico come Cosmos 3 e' vincolato a rispettare le leggi fisiche perche' e' stato addestrato su dati con annotazioni fisiche e sul feedback di simulatori. La differenza non e' solo qualitativa ma operativa: per addestrare un robot, serve un simulatore fisicamente corretto, non solo visivamente plausibile.

## Quando usarlo / quando no

I world model sono lo strumento appropriato quando si vuole addestrare un sistema fisico (robot, veicolo autonomo, drone) senza raccogliere milioni di ore di dati reali — la simulazione generata dal world model sostituisce parzialmente o completamente l'interazione con l'ambiente reale. Sono utili anche per la pianificazione: un agente con un world model puo' valutare mentalmente piu' alternative di azione prima di eseguirne una, riducendo il costo degli errori fisici.

Non sono lo strumento giusto per task puramente linguistici dove la fisica e' irrilevante, ne' per task che richiedono una verita' esatta sul mondo reale (il world model predice, non conosce lo stato esatto). L'allucinazione fisica — predire una dinamica sbagliata perche' il training data era parziale — e' il rischio principale; ogni deployment in produzione richiede un meccanismo di verifica indipendente (sensori reali, simulatori di fisica classica come IsaacSim) per intercettare le predizioni errate.

Soglia di utilita'. Per addestrare un robot a un nuovo task, la regola empirica e' che il world model riduce il fabbisogno di dati reali di un fattore 10-100x: con Cosmos 3, NVIDIA dichiara che i cicli di addestramento e valutazione si riducono da mesi a giorni. Questo non elimina il bisogno di dati fisici reali — i parametri del world model stesso devono venire da qualche parte — ma sposta il bottleneck dal dato fisico alla qualita' del world model.

## Esempi pratici

Robot arm manipulation. Un world model addestrato su video di manipolazione di oggetti impara le dinamiche di afferrare, spostare, rilasciare. Un robot che deve imparare un nuovo grasping pattern non deve provare milioni di volte: genera la sequenza di azioni nel simulatore interno, seleziona quella con la predizione di successo piu' alta, esegue fisicamente solo quella. Questo e' il loop fondamentale di Cosmos 3 per robotica.

Autonomous driving. I veicoli autonomi usano world model per predire la traiettoria di altri veicoli, pedoni e oggetti nelle prossime 2-5 secondi. Il world model non sostituisce i sensori (lidar, radar, camera), ma li integra: laddove un sensore non vede (occlusion), il world model predice cosa c'e' dall'altra parte basandosi sul contesto. Cos3 Super e' il modello di scala per la generazione di scenari sintetici di guida.

Addestramento da video YouTube. Cosmos 3 e' stato preaddestrato su grandi corpus video publici per apprendere le dinamiche fisiche del mondo. Il risultato e' un foundation model che puo' essere fine-tuned su dati robotici specifici dell'utente — un gripper, un ambiente di magazzino, un tipo di oggetto — con un volume di dati nettamente inferiore a quello necessario per addestrare da zero.

## Letture

- Hafner et al., "Mastering Diverse Domains through World Models" (DreamerV3), 2023. https://arxiv.org/abs/2301.04104
- Ha e Schmidhuber, "Recurrent World Models Facilitate Policy Evolution", NeurIPS 2018. https://arxiv.org/abs/1809.01999
- Zidan et al., "World Models: A Comprehensive Survey of Architectures, Methodologies, Reasoning Paradigms, and Applications", arXiv 2606.00133, 2026. https://arxiv.org/abs/2606.00133
- NVIDIA, "NVIDIA Cosmos 3 Technical Report", 2026. https://research.nvidia.com/labs/cosmos-lab/cosmos3/technical-report.pdf
- NVIDIA Blog, "How Cosmos 3 Helps Physical AI Think Before It Acts", 2026. https://blogs.nvidia.com/blog/cosmos-3-physical-ai-open-world-foundation-model/
- Anthropic, "MolmoAct2 and robot action reasoning", arXiv 2605.02881, 2026. https://arxiv.org/abs/2605.02881

## Aggiornamenti

### 2026-06-21

DreamX-World 1.0 (AMAP-ML/Alibaba AutoNavi, arXiv:2606.16993, 15 giugno 2026): primo world model interattivo general-purpose open-source con benchmark superiori ai sistemi closed-source comparabili. Architettura basata su Wan2.2-T2V-5B, controllo camera a 6 DoF, risoluzione 704x1280 a 7,5 secondi per clip. Camera-control score 73.75 e overall score 84.76 su WorldTest, sopra HY-WorldPlay 1.5 (80.79) e LingBot-World (80.45). Pesi, codice e pipeline open-source su GitHub (AMAP-ML/DreamX-World). Il differenziale rispetto all'ecosistema esistente: WoRLD (Google) e WorldMaker (Meta) restano closed-source; DreamX-World 1.0 e' il primo world model navigabile general-purpose con pesi pubblici e benchmark verificabili da terze parti. [Digest 2026-06-21](../../digest/2026/06/21.md)

### 2026-06-09

NVIDIA lancia Cosmos 3 (1 giugno 2026, missed coverage): il primo world foundation model aperto per physical AI con architettura Mixture-of-Transformers, cinque modalita' native (testo, immagini, video, audio, azioni), pesi open-weight su Hugging Face (Nano 16B, Super 64B). L'approccio "reason before generate" — un reasoning transformer comprende la fisica della scena prima che un expert generation transformer produca output — e' il contributo architetturale principale rispetto ai generatori video classici (Cosmos 1-2, VideoPoet, Sora) che non hanno un modulo di ragionamento fisico esplicito. La Cosmos Coalition (Agile Robots, Black Forest Labs, Generalist AI, LTX, Runway, Skild AI) segnala che l'ecosistema attorno ai world model per robotica si sta strutturando come consorzio, non come competizione tra vendor. 8 fonti indipendenti: NVIDIA Newsroom, NVIDIA Blog, Hugging Face Blog/NVIDIA, HPCwire/AIwire, GlobeNewswire, ARC Advisory Group, explainx.ai, NVIDIA Research Technical Report. [Digest 2026-06-09](../../digest/2026/06/09.md)
