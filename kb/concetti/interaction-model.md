---
name: Interaction Model
aliases: [interaction model, full-duplex AI, modello di interazione, full-duplex model]
categoria: architettura
created: 2026-05-13
last_updated: 2026-05-13
mentions_count: 5
---

# Interaction Model

## Cos'e

Un interaction model e' una classe di modelli AI progettata per la conversazione in tempo reale attraverso un'architettura full-duplex: anziche' operare in cicli sequenziali (riceve input → elabora → produce output → attende), il sistema percepisce e risponde in simultanea, mantenendo una "presenza" continua durante lo scambio. Il termine e' stato introdotto pubblicamente da Thinking Machines Lab (TML) nell'annuncio di TML-Interaction-Small (11-12 maggio 2026), ma la ricerca sul dialogo full-duplex e' attiva da anni, con il challenge ICASSP 2026 HumDial dedicato esplicitamente ai sistemi di dialogo full-duplex.

La differenza rispetto ai modelli audio/voice tradizionali e' strutturale. Un modello realtime come GPT-Realtime-2.0 o Gemini Flash Live opera ancora secondo un modello half-duplex o quasi-full-duplex: attende che l'utente finisca (VAD — Voice Activity Detection) prima di elaborare e rispondere. Un interaction model vero riceve input in micro-turni da 200-500 ms durante la propria stessa generazione, e puo' interrompere se stesso, modulare il ritmo della propria risposta, o restare in silenzio al momento semanticamente opportuno — comportamenti impossibili con l'architettura sequenziale.

L'importanza pratica cresce con la penetrazione degli agenti vocali: un agente che interagisce con un cliente in una chiamata commerciale o in un'assistenza sanitaria deve essere percepito come un interlocutore naturale, non come un sistema che "pensa e poi parla". I benchmark emersi nel 2026 (FD-bench, TimeSpeak, CueSpeak) misurano precisamente queste capacita' di timing e sincronia che i benchmark precedenti ignoravano.

## Come funziona

L'architettura di un interaction model si differenzia da quella di un LLM autoregressive standard su piu' dimensioni.

**Micro-turn processing.** L'input non arriva come un blocco intero ma come uno stream continuo diviso in chunk temporali fissi (TML usa 200 ms). Ad ogni micro-turn il modello legge il chunk appena arrivato e decide se integrarlo nel contesto, se modificare la risposta in corso, o se intervenire con una interruzione. Questo richiede un meccanismo di routing del flusso utente (user-stream routing) nel modello durante la generazione — oggetto di ricerca specifica (arXiv:2605.10199, CUHK/SenseTime/Tsinghua).

**Architettura a due livelli (TML).** TML-Interaction-Small separa esplicitamente due componenti: un modello di interazione time-aware che gestisce il real-time (latenza sub-secondo, presenza, timing, interruzioni), e un modello asincrono in background che gestisce il ragionamento esteso, l'uso di tool e il lavoro a orizzonte lungo. I due livelli comunicano ma operano su vincoli temporali diversi: il livello interattivo non puo' attendere che il livello di ragionamento completi un task; il livello di ragionamento puo' aggiornare il contesto del livello interattivo in modo asincrono.

**Tokenizzazione dell'audio.** Per trattare audio, video e testo nello stesso stream, il sistema usa token discreti audio generati da un encoder vocale (TML usa una variante di CosyVoice 2). Questo permette di trattare la modalita' audio come sequenza di token, il che consente all'architettura transformer di gestirla con gli stessi meccanismi di attenzione del testo.

**Architettura MoE per efficienza real-time.** TML-Interaction-Small e' un MoE da 276 miliardi di parametri con 12 miliardi attivi per micro-turn: la struttura MoE consente di mantenere alta capacita' espressiva senza un costo computazionale proporzionale al totale dei parametri a ogni step, il che e' critico per un sistema che deve rispondere entro 200-400 ms.

## Varianti / approcci

| Approccio | Caratteristica | Limite principale |
|---|---|---|
| VAD + half-duplex | Attende silenzio utente, poi elabora | Non permette interruzione; latenza percepita alta |
| Quasi-full-duplex con VAD predictivo | Inizia a generare prima del silenzio su segnali prosodici | Ancora fondamentalmente sequenziale; VAD failure |
| Full-duplex con user-stream routing | Legge input durante generazione; routing nel transformer | Complessita' architetturale; ricerca ancora aperta |
| TML micro-turn (200 ms chunk) | Chunk fissi, decisione per micro-turn | Richiede latenza infrastruttura sub-200 ms end-to-end |
| Two-level async + realtime (TML) | Separazione hard tra interazione e ragionamento | Coordinazione tra livelli aggiunge latenza al layer di reasoning |

I benchmark emergenti nel 2026 per questa categoria:

- **FD-bench v1.5**: misura qualita' complessiva dell'interazione full-duplex in scenari realistici di conversazione. TML-Interaction-Small: 77,8; Gemini 3.1 Flash Live: 54,3; GPT-Realtime-2.0: 46,8.
- **TimeSpeak**: capacita' del modello di iniziare a parlare a un momento specificato dall'utente (test di controllo temporale esplicito). TML: 64,7; prossimo competitore: 4,3.
- **CueSpeak**: capacita' di interrompere al momento semanticamente appropriato (test di comprensione contestuale del timing). TML: 81,7; prossimo competitore: 2,9.
- **Latenza end-to-end**: tempo dalla fine dell'utterance utente alla prima risposta audio. TML: 0,40 s; GPT-Realtime-2.0: 1,18 s; Gemini 3.1 Flash Live: 0,57 s.

## Quando usarlo / quando no

Gli interaction model sono la scelta giusta per applicazioni in cui il timing conversazionale e' il fattore critico: assistenti vocali percepiti come "naturali", agenti per customer service telefonico, coaching linguistico in tempo reale, assistenti di presentazione o tutoring interattivo. La soglia di latenza percepita come naturale in una conversazione telefonica e' 200-400 ms; sistemi oltre 800-1000 ms sono percepiti come "lenti" e degradano l'esperienza.

Sono la scelta sbagliata per applicazioni in cui la profondita' del ragionamento e' piu' importante del timing (analisi documenti, generazione di codice, ricerca multi-step) e per deployment dove la latenza infrastrutturale non puo' garantire round-trip sub-200 ms (es. connessioni mobili 4G instabili, regioni geografiche con latenza alta verso i datacenter del provider).

La complessita' dell'architettura a due livelli comporta anche un costo di integrazione piu' alto rispetto a un'API realtime tradizionale: chi costruisce su TML deve gestire due canali asincroni con semantiche diverse, il che richiede un SDK dedicato o un harness che astragga la coordinazione.

## Esempi pratici

**Agente di customer service telefonico.** Un interaction model sostituisce un IVR tradizionale in una chiamata in entrata. L'utente dice "Devo disdire il mio abbonamento". Invece di attendere che finisca e poi rispondere con "Vuole procedere con la disdetta?", il modello ha gia' riconosciuto l'intent a meta' frase, ha attivato il layer di reasoning in background per recuperare i dettagli dell'account, e quando l'utente smette sta gia' producendo la risposta personalizzata. Il tempo percepito tra fine utterance e risposta: < 400 ms.

**Tutoring linguistico.** Un interaction model coach di pronuncia reagisce in tempo reale agli errori articolatori, interrompendo gentilmente con correzioni al momento giusto — non alla fine della frase, quando la forma motoria e' gia' consolidata. Questo richiede CueSpeak alto: interrompere troppo presto e' invasivo, troppo tardi e' inutile.

## Letture

- Thinking Machines Lab, "Interaction Models: A Scalable Approach to Human-AI Collaboration", 2026. https://thinkingmachines.ai/blog/interaction-models/
- arXiv:2605.10199 "How Should LLMs Listen While Speaking? A Study of User-Stream Routing in Full-Duplex Spoken Dialogue", CUHK / SenseTime / Tsinghua, 2026. https://arxiv.org/abs/2605.10199
- arXiv:2604.21406 "Full-Duplex Interaction in Spoken Dialogue Systems: A Comprehensive Study from the ICASSP 2026 HumDial Challenge", 2026. https://arxiv.org/abs/2604.21406
- TechCrunch, "Thinking Machines wants to build an AI that actually listens while it talks", maggio 2026. https://techcrunch.com/2026/05/11/thinking-machines-wants-to-build-an-ai-that-actually-listens-while-it-talks/
- VentureBeat, "Thinking Machines shows off preview of near-realtime AI voice and video conversation with new 'interaction models'", maggio 2026. https://venturebeat.com/technology/thinking-machines-shows-off-preview-of-near-realtime-ai-voice-and-video-conversation-with-new-interaction-models

## Aggiornamenti

### 2026-05-13

Thinking Machines Lab (Mira Murati) annuncia TML-Interaction-Small, il primo modello pubblico nella categoria "interaction model": architettura MoE 276B/12B attivi, micro-turn da 200 ms, latenza end-to-end di 0,40 s, FD-bench v1.5 a 77,8 (vs 54,3 Gemini e 46,8 GPT-Realtime-2.0). Research preview a gruppo ristretto, distribuzione piu' ampia attesa nel 2026. Il lancio introduce anche tre nuovi benchmark verticali per la valutazione dei sistemi full-duplex: FD-bench, TimeSpeak, CueSpeak. [Digest 2026-05-13](../../digest/2026/05/13.md)
