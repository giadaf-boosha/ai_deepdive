---
name: Interaction Model
aliases: [interaction model, full-duplex AI, modello di interazione, full-duplex model]
categoria: architettura
created: 2026-05-13
last_updated: 2026-06-01
---

# Interaction Model

## Cos'e

Un interaction model e' una classe di modelli AI progettata per la conversazione in tempo reale attraverso un'architettura full-duplex: anziche' operare in cicli sequenziali (riceve input -> elabora -> produce output -> attende), il sistema percepisce e risponde in simultanea, mantenendo una "presenza" continua durante lo scambio. Il termine e' stato introdotto pubblicamente da Thinking Machines Lab (TML) nell'annuncio di TML-Interaction-Small (11-12 maggio 2026), ma la ricerca sul dialogo full-duplex e' attiva da anni, con il challenge ICASSP 2026 HumDial dedicato esplicitamente ai sistemi di dialogo full-duplex.

La differenza rispetto ai modelli audio/voice tradizionali e' strutturale. Un modello realtime come GPT-Realtime-2.0 o Gemini 3.1 Flash Live opera ancora secondo un modello half-duplex o quasi-full-duplex: attende che l'utente finisca (VAD, Voice Activity Detection) prima di elaborare e rispondere. Un interaction model vero riceve input in micro-turni da 200-500 ms durante la propria stessa generazione, e puo' interrompere se stesso, modulare il ritmo della propria risposta, o restare in silenzio al momento semanticamente opportuno: comportamenti impossibili con l'architettura sequenziale. La proprieta' chiave, secondo TML, e' che il full-duplex e' una caratteristica architetturale nativa (il modello e' addestrato da zero per percepire e generare in simultanea), non uno scaffolding esterno aggiunto sopra un LLM con un VAD e un dialog manager separati.

L'importanza pratica cresce con la penetrazione degli agenti vocali: un agente che interagisce con un cliente in una chiamata commerciale o in un'assistenza sanitaria deve essere percepito come un interlocutore naturale, non come un sistema che "pensa e poi parla". I benchmark emersi nel 2026 (FD-bench, TimeSpeak, CueSpeak) misurano precisamente queste capacita' di timing e sincronia che i benchmark precedenti ignoravano. Il tema e' rilevante anche al di fuori della voce: la stessa intuizione (un LLM che non puo' agire mentre legge ne' reagire mentre scrive) e' il bersaglio del filone di ricerca sui modelli multi-stream emerso nello stesso mese.

## Come funziona

L'architettura di un interaction model si differenzia da quella di un LLM autoregressive standard su piu' dimensioni.

**Micro-turn processing.** L'input non arriva come un blocco intero ma come uno stream continuo diviso in chunk temporali fissi (TML usa 200 ms). Ad ogni micro-turn il modello legge il chunk appena arrivato e decide se integrarlo nel contesto, se modificare la risposta in corso, o se intervenire con una interruzione. Questo richiede un meccanismo di routing del flusso utente (user-stream routing) nel modello durante la generazione, oggetto di ricerca specifica (arXiv:2605.10199, CUHK/SenseTime/Tsinghua).

**Architettura a due livelli (TML).** TML-Interaction-Small separa esplicitamente due componenti: un modello di interazione time-aware che gestisce il real-time (latenza sub-secondo, presenza, timing, interruzioni), e un modello asincrono in background che gestisce il ragionamento esteso, l'uso di tool e il lavoro a orizzonte lungo. I due livelli condividono il contesto ma operano su vincoli temporali diversi: il livello interattivo non puo' attendere che il livello di ragionamento completi un task; il livello di ragionamento puo' aggiornare il contesto del livello interattivo in modo asincrono. Concettualmente il layer asincrono e' un cugino dell'idea di [agente](./agent.md) con uso di [tool](./tool-use.md): mentre il layer realtime mantiene la conversazione, il layer di reasoning fa il lavoro pesante in background.

**Tokenizzazione dell'audio.** Per trattare audio, video e testo nello stesso stream, il sistema usa token discreti audio generati da un encoder vocale (TML usa una variante di CosyVoice 2). Questo permette di trattare la modalita' audio come sequenza di token, il che consente all'architettura transformer di gestirla con gli stessi meccanismi di attenzione del testo.

**Architettura MoE per efficienza real-time.** TML-Interaction-Small e' un [Mixture-of-Experts](./mixture-of-experts.md) da 276 miliardi di parametri con 12 miliardi attivi per micro-turn: la struttura MoE consente di mantenere alta capacita' espressiva senza un costo computazionale proporzionale al totale dei parametri a ogni step, il che e' critico per un sistema che deve rispondere entro 200-400 ms. Sul piano dell'[inference](./inference.md) questo e' un paradigma diverso da quello batch/turn-based dei chat model: ogni 200 ms va prodotto un forward pass utile, il che impone un budget computazionale per micro-turn molto stringente.

**Stream paralleli (approccio multi-stream).** Un filone parallelo affronta lo stesso collo di bottiglia da un altro angolo. Invece di un singolo flusso sequenziale di token (in cui i ruoli system, user, assistant sono blocchi in serie), si addestra il modello a leggere e generare piu' stream di token in simultanea, ognuno dedicato a un ruolo (input utente, output, pensiero interno, system, tool call, audit). Ad ogni forward pass il modello legge da piu' stream di input e genera in piu' stream di output, mantenendo la dipendenza causale sugli step precedenti. Il punto rilevante e' che si tratta di un cambiamento a livello di dati di instruction-tuning, senza modificare l'architettura transformer: e' quindi realizzabile via [fine-tuning](./fine-tuning.md) di modelli esistenti e agnostico all'hardware. Questo lo rende complementare all'approccio TML, che invece addestra un modello dedicato da zero.

## Varianti / approcci

| Approccio | Caratteristica | Limite principale |
|---|---|---|
| VAD + half-duplex | Attende silenzio utente, poi elabora | Non permette interruzione; latenza percepita alta |
| Quasi-full-duplex con VAD predictivo | Inizia a generare prima del silenzio su segnali prosodici | Ancora fondamentalmente sequenziale; VAD failure |
| Full-duplex con user-stream routing | Legge input durante generazione; routing nel transformer | Complessita' architetturale; ricerca ancora aperta |
| TML micro-turn (200 ms chunk) | Chunk fissi, decisione per micro-turn, modello addestrato da zero | Richiede latenza infrastruttura sub-200 ms end-to-end |
| Two-level async + realtime (TML) | Separazione hard tra interazione e ragionamento | Coordinazione tra livelli aggiunge latenza al layer di reasoning |
| Multi-stream LLM (instruction-tuning) | Stream paralleli per ruolo, ottenuti via fine-tuning | Nessun benchmark conversazionale dedicato ancora pubblicato; maturita' di ricerca |
| Voice agent commerciale + ricerca parallela | Agente vocale che recupera info mid-sentence (es. Sesame) | Non e' full-duplex nativo nel senso TML; e' orchestrazione realtime sopra un voice stack |

I benchmark emergenti nel 2026 per questa categoria:

- **FD-bench v1.5**: misura qualita' complessiva dell'interazione full-duplex in scenari realistici di conversazione. TML-Interaction-Small: 77,8; Gemini 3.1 Flash Live: 54,3; GPT-Realtime-2.0: 46,8.
- **TimeSpeak**: capacita' del modello di iniziare a parlare a un momento specificato dall'utente (test di controllo temporale esplicito). TML: 64,7; prossimo competitore: 4,3.
- **CueSpeak**: capacita' di interrompere al momento semanticamente appropriato (test di comprensione contestuale del timing). TML: 81,7; prossimo competitore: 2,9.
- **Latenza end-to-end**: tempo dalla fine dell'utterance utente alla prima risposta audio. TML: 0,40 s; GPT-Realtime-2.0: 1,18 s; Gemini 3.1 Flash Live: 0,57 s.

Il distacco enorme su TimeSpeak (64,7 contro 4,3) e CueSpeak (81,7 contro 2,9) e' il segnale piu' interessante: i competitor realtime collassano su questi due test non perche' siano lenti, ma perche' la loro architettura half-duplex non concepisce affatto il controllo del timing dal lato del modello. Sono capacita' che un sistema VAD-based non puo' esprimere indipendentemente da quanto sia ottimizzato.

## Quando usarlo / quando no

Gli interaction model sono la scelta giusta per applicazioni in cui il timing conversazionale e' il fattore critico: assistenti vocali percepiti come "naturali", agenti per customer service telefonico, coaching linguistico in tempo reale, assistenti di presentazione o tutoring interattivo. La soglia di latenza percepita come naturale in una conversazione telefonica e' 200-400 ms; sistemi oltre 800-1000 ms sono percepiti come "lenti" e degradano l'esperienza.

Sono la scelta sbagliata per applicazioni in cui la profondita' del ragionamento e' piu' importante del timing (analisi documenti, generazione di codice, ricerca multi-step) e per deployment dove la latenza infrastrutturale non puo' garantire round-trip sub-200 ms (es. connessioni mobili 4G instabili, regioni geografiche con latenza alta verso i datacenter del provider). In questi casi un modello realtime tradizionale o un agente testuale con [tool-use](./tool-use.md) e' sufficiente, e l'overhead architetturale del full-duplex non si ripaga.

La complessita' dell'architettura a due livelli comporta anche un costo di integrazione piu' alto rispetto a un'API realtime tradizionale: chi costruisce su TML deve gestire due canali asincroni con semantiche diverse, il che richiede un SDK dedicato o un [agent harness](./agent-harness.md) che astragga la coordinazione. Va inoltre considerato lo stato di maturita': a giugno 2026 TML-Interaction-Small e' ancora una research preview riservata a un gruppo ristretto di ricercatori, l'approccio multi-stream e' un paper con codice ma senza prodotto, e i deployment commerciali (Sesame e simili) usano orchestrazione realtime sopra stack vocali piu' tradizionali piuttosto che full-duplex nativo. Chi deve spedire qualcosa in produzione oggi lavora ancora prevalentemente con API realtime quasi-full-duplex.

## Esempi pratici

**Agente di customer service telefonico.** Un interaction model sostituisce un IVR tradizionale in una chiamata in entrata. L'utente dice "Devo disdire il mio abbonamento". Invece di attendere che finisca e poi rispondere con "Vuole procedere con la disdetta?", il modello ha gia' riconosciuto l'intent a meta' frase, ha attivato il layer di reasoning in background per recuperare i dettagli dell'account, e quando l'utente smette sta gia' producendo la risposta personalizzata. Il tempo percepito tra fine utterance e risposta: < 400 ms.

**Tutoring linguistico.** Un interaction model coach di pronuncia reagisce in tempo reale agli errori articolatori, interrompendo gentilmente con correzioni al momento giusto, non alla fine della frase, quando la forma motoria e' gia' consolidata. Questo richiede CueSpeak alto: interrompere troppo presto e' invasivo, troppo tardi e' inutile.

**Voice agent consumer con ricerca mid-sentence.** L'app iOS di Sesame (preview pubblica fine maggio 2026) mostra una versione commerciale dell'idea: durante la conversazione l'agente vocale esegue in parallelo piu' ricerche web mentre parla, integrando informazioni fresche a meta' frase, e mantiene quattro personalita' con memoria persistente. Non e' full-duplex nativo nel senso stretto TML, ma e' il caso d'uso che spiega perche' il timing e la concorrenza tra percezione, ragionamento e parola contino: l'obiettivo dichiarato e' costruire un'abitudine d'uso quotidiana, e un agente che si blocca per cercare sul web rompe l'illusione di naturalezza.

**Reasoning concorrente alla lettura (multi-stream).** Negli esperimenti sui modelli multi-stream il modello viene addestrato a compiti come "solving-while-reading" (risolvere mentre legge l'input) e "auditing-while-solving" (verificare uno stream di soluzione mentre viene generato), valutati su benchmark come GSM8K, MATH500 e SQuAD. E' un esempio non vocale dello stesso principio: separare i concern in stream paralleli sblocca comportamenti che il formato sequenziale non permette, con il beneficio collaterale di uno stream di "pensiero" separato e ispezionabile a fini di monitorabilita'.

## Letture

- Thinking Machines Lab, "Interaction Models: A Scalable Approach to Human-AI Collaboration", 2026. https://thinkingmachines.ai/blog/interaction-models/
- arXiv:2605.10199 "How Should LLMs Listen While Speaking? A Study of User-Stream Routing in Full-Duplex Spoken Dialogue", CUHK / SenseTime / Tsinghua, 2026. https://arxiv.org/abs/2605.10199
- arXiv:2604.21406 "Full-Duplex Interaction in Spoken Dialogue Systems: A Comprehensive Study from the ICASSP 2026 HumDial Challenge", 2026. https://arxiv.org/abs/2604.21406
- arXiv:2605.12460 "Multi-Stream LLMs: Unblocking Language Models with Parallel Streams of Thoughts, Inputs and Outputs", Su / Yang / Li / Geiping (Max Planck IS, ELLIS Tübingen, ETH Zurich), 2026. https://arxiv.org/abs/2605.12460 — codice: https://github.com/seal-rg/streaming
- TechCrunch, "Thinking Machines wants to build an AI that actually listens while it talks", maggio 2026. https://techcrunch.com/2026/05/11/thinking-machines-wants-to-build-an-ai-that-actually-listens-while-it-talks/
- VentureBeat, "Thinking Machines shows off preview of near-realtime AI voice and video conversation with new 'interaction models'", maggio 2026. https://venturebeat.com/technology/thinking-machines-shows-off-preview-of-near-realtime-ai-voice-and-video-conversation-with-new-interaction-models
- TechCrunch, "Sesame, the conversational AI startup from Oculus founders, launches its iOS app", maggio 2026. https://techcrunch.com/2026/05/28/sesame-the-conversational-ai-startup-from-oculus-founders-launches-its-ios-app/

## Aggiornamenti

### 2026-05-13

Thinking Machines Lab (Mira Murati) annuncia TML-Interaction-Small, il primo modello pubblico nella categoria "interaction model": architettura MoE 276B/12B attivi, micro-turn da 200 ms, latenza end-to-end di 0,40 s, FD-bench v1.5 a 77,8 (vs 54,3 Gemini e 46,8 GPT-Realtime-2.0). Research preview a gruppo ristretto, distribuzione piu' ampia attesa nel 2026. Il lancio introduce anche tre nuovi benchmark verticali per la valutazione dei sistemi full-duplex: FD-bench, TimeSpeak, CueSpeak. [Digest 2026-05-13](../../digest/2026/05/13.md)

### 2026-06-01

Mese ricco di sviluppi sostanziali sul tema full-duplex, su tre fronti distinti.

1. **Multi-Stream LLMs (paper, 14 maggio).** Su, Yang, Li e Geiping (Max Planck IS, ELLIS Tübingen, ETH Zurich, Universita' di Tübingen) pubblicano arXiv:2605.12460 con codice su GitHub (seal-rg/streaming). E' un secondo angolo di attacco al collo di bottiglia sequenziale che motiva anche TML: invece di addestrare un modello dedicato da zero, propongono di fare instruction-tuning con stream di token paralleli (uno per ruolo: input, output, thought, system, tool, audit), un cambiamento solo a livello di dati di training, agnostico all'hardware e applicabile a modelli esistenti. Esperimenti su "solving-while-reading" e "auditing-while-solving" valutati su GSM8K, MATH500, SQuAD e altri. Aggiunto come variante "multi-stream" nella tabella approcci e come esempio non-vocale. [Digest 2026-05-14](../../digest/2026/05/14.md)

2. **Sesame iOS (prodotto, 28-30 maggio).** La startup dei co-fondatori di Oculus apre la preview pubblica di un'app di voice agent con quattro personalita' a memoria persistente e ricerca web parallela mid-sentence. Non e' full-duplex nativo in senso TML, ma e' la prima validazione commerciale di scala del perche' il timing e la concorrenza percezione/ragionamento/parola contino in un agente vocale consumer. Aggiunto come riga nella tabella approcci e come terzo esempio pratico. [Digest 2026-05-30](../../digest/2026/05/30.md)

3. **Conferma fonti primarie.** Verificato via WebSearch lo stato di TML-Interaction-Small (research preview ancora ristretta, co-fondatrice Lilian Weng oltre a Mira Murati, addestramento full-duplex nativo senza VAD esterno) e l'esistenza del paper multi-stream. Nessuna revisione dei numeri di benchmark: i dati FD-bench/TimeSpeak/CueSpeak/latenza restano quelli del lancio.

Oltre all'aggiunta dei due sviluppi, la scheda e' stata migliorata in chiarezza: esplicitata la distinzione tra full-duplex nativo (TML) e orchestrazione realtime sopra stack tradizionali (Sesame, API realtime), aggiunto un commento sull'interpretazione del distacco su TimeSpeak/CueSpeak, e una nota sullo stato di maturita' nella sezione "quando usarlo / quando no".
