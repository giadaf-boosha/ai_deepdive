---
name: Context window
aliases: [context window, finestra di contesto, finestra contestuale, context length]
categoria: architettura
created: 2026-04-28
last_updated: 2026-06-29
---

# Context window

## Cos'e

Il context window (o finestra di contesto) e' la quantita' massima di token che un [LLM](./llm.md) puo' considerare in un singolo passo di inferenza, sommando input (system prompt, messaggi precedenti, documenti, esempi few-shot) e output generato. Si esprime in token e definisce un confine fisico: il modello non puo' ragionare su informazioni oltre la finestra, perche' non sono nelle sue rappresentazioni di attention. La finestra include sia testo "passato" della conversazione sia testo "futuro" che il modello sta producendo.

I primi transformer (GPT-2, BERT) avevano finestre di 512-1024 token. GPT-3 nel 2020 saliva a 2048. La traiettoria 2022-2026 e' di crescita esponenziale: GPT-4 8k/32k (2023), Claude 2 100k (2023), GPT-4 Turbo 128k (2023), Claude 2.1 200k (2023), Gemini 1.5 1M con sperimentazioni a 10M (2024), Claude 3.5/4 con 200k-1M (2024-2026), Gemini 2 standard 2M (2025). Nella primavera 2026 la finestra "di default" si e' stabilizzata su due fasce ricorrenti: 128k-256k per i modelli mid-tier e 1M token per i flagship agentici (Gemini 3.5 Flash, Qwen3.7-Max). L'estensione del context resta una feature competitiva centrale, ma il fronte si e' spostato: non basta dichiarare un milione di token, occorre dimostrare che il modello li usa davvero in task agentici lunghi.

L'importanza pratica e' duplice. Determina quanto puoi inserire in una singola chiamata: documenti interi, codebase, transcript di riunioni, base di conoscenza piccole. E determina la complessita' computazionale: l'attention e' O(n^2) sulla lunghezza, quindi raddoppiare il contesto piu' che raddoppia costi e latenza, a meno di ottimizzazioni. La gestione del context window e' tema centrale per progettare prompt, [agent](./agent.md), pipeline [RAG](./rag.md), e [fine-tuning](./fine-tuning.md). Con l'arrivo degli agenti che eseguono migliaia di tool call su sessioni lunghe (Qwen3.7-Max ha sostenuto run autonome fino a 35 ore con 1.000+ tool call), il context window e' passato da limite di "quanto testo posso incollare" a vincolo architetturale di "come distribuisco lo stato di un processo lungo tra finestra, storage esterno e sottoprocessi".

## Come funziona

Il limite del context viene definito a training time: si stabilisce una `max_position_embedding` o equivalente, e i positional encoding sono progettati per quella lunghezza. Il transformer applica la self-attention su una matrice n x n di score, dove n e' la lunghezza in token. Da qui derivano i due problemi cardinali: complessita' O(n^2) in tempo e memoria, e degradazione delle posizioni distanti.

Per estendere il context oltre il training nominale si usano diverse tecniche.

Position encoding migliorato. RoPE (Rotary Position Embedding, Su et al. 2021) codifica la posizione come rotazione complessa applicata a query e key, permettendo extrapolation oltre la lunghezza training tramite interpolation o YaRN scaling. ALiBi (Press et al. 2022) aggiunge bias lineari basati su distanza, naturalmente estensibili. NoPE elimina del tutto le encoding posizionali in alcune varianti. La finestra da 512k token di IBM Granite 4.1 (maggio 2026) non nasce da un trucco a inference time ma da un training in cinque fasi su circa 15 trilioni di token: e' il segnale che i lab puntano sempre piu' al long context "nativo" invece che a estensioni post-hoc.

Attention efficiente. FlashAttention (Dao et al. 2022) ricalcola l'attention in modo I/O-aware riducendo l'overhead memoria, abilitando training su context lunghi. Sliding window attention (Mistral): ogni token attende solo gli ultimi W token, rendendo l'attention O(nW). Sparse attention (Longformer, BigBird): pattern fissi di sparsita'. Linear attention / state space model (Mamba, RWKV): complessita' lineare in n, alternative al transformer. Una direzione emergente nel 2026 e' il compute adattivo per token: il paper "Compute Where it Counts" (Self Optimizing Language Models, maggio 2026) aggiunge a un modello base congelato una policy network leggera che, a ogni step di decode, regola dinamicamente sparsita' dell'attention, pruning delle attivazioni e bit-width della quantizzazione, comprimendo i token "facili" e riservando il budget pieno a quelli difficili. E' complementare alle tecniche statiche e mira proprio a rendere economicamente sostenibili le generazioni su finestre lunghe.

KV cache. A inference time, durante la generazione, si memorizzano key e value di tutti i token gia' processati per non ricalcolarli. La KV cache e' la fonte principale del consumo memoria a runtime. Per Llama 3 70B con context 8k, la KV cache occupa diversi GB. Su context 1M la KV cache puo' superare la memoria di una H100. Tecniche di compressione (PagedAttention come in vLLM, KV cache quantization, MQA/GQA che condividono key e value tra heads) riducono il problema. La pressione sulla KV cache spiega perche' lo strato di ottimizzazione dell'inferenza valga sempre di piu': l'acquisizione di Eigen AI da parte di Nebius per circa 643 milioni di dollari (maggio 2026), per un team di 20 persone autore della tecnica di quantizzazione AWQ, segnala che ridurre l'impronta memoria di un modello a 4 bit (dimezzando le GPU necessarie) e' diventato un asset strategico quanto lo stack applicativo.

Hardware e long context locale. La capacita' di tenere un milione di token in finestra dipende anche dalla memoria del dispositivo. Nvidia ha annunciato al Computex 2026 (1 giugno) RTX Spark, un SoC con 128 GB di memoria unificata LPDDR5X che, secondo Nvidia, consente di eseguire localmente su laptop modelli da 70B-120B parametri senza quantizzazione degradante e con context length fino a 1 milione di token per sessioni agentiche prolungate. E' il segnale che il long context sta scendendo dal datacenter al client.

Long-context retrieval. Anche con finestra estesa, modelli reali mostrano "lost in the middle" (Liu et al. 2023): performance peggiora per informazioni a meta' del contesto. Le valutazioni "needle in a haystack" misurano la capacita' di recuperare un'informazione precisa inserita a posizioni casuali. I modelli frontier 2025-2026 raggiungono 95%+ di recall su 1M token; quelli precedenti calano al 60-70%.

Numeri. 1 token ~ 4 caratteri o ~0.75 parole inglesi (italiano simile). 1k token = ~750 parole = ~1.5 pagine. 100k token = un libro corto. 1M token = ~2000 pagine.

## Varianti / approcci

Modelli del 2025-2026 con i loro context window:

| Modello | Context window | Note |
|---|---|---|
| Claude Opus 4.8 / Sonnet 4.x | 200k - 1M | 1M in beta o per Enterprise; Dynamic Workflows sposta lo stato fuori dal context |
| GPT-5 / GPT-4o | 128k - 256k | Variabile per tier |
| GPT-Realtime-2 | 128k | Voice model con reasoning GPT-5, salito da 32k |
| Gemini 3.5 Flash | 1M | Nativo multimodale, modello agentico Google I/O 2026 |
| Gemini 3.5 Pro | 2M | GA attesa giugno 2026; Deep Think per Ultra; la finestra piu' grande tra i frontier |
| Gemini 2 Pro | 2M | Standard, 10M sperimentale |
| MiniMax M3 | 1M | Open-weight (pesi su HuggingFace); MSA come tecnica per long-context inference economica; 59% SWE-Bench Pro |
| Qwen3.7-Max | 1M | Ottimizzato per CLI agent, run autonome fino a 35h |
| Mistral Medium 3.5 | 256k | 128B open-weights |
| IBM Granite 4.1 | 512k | Open-source Apache 2.0, long context nativo |
| Grok Build 0.1 | 256k | Coding agent CLI, cached $0,20/1M token |
| Llama 3.1 / 3.3 | 128k | Open weights |
| DeepSeek V3 | 128k | MoE open |

Sull'asse di tecnica per estendere il context: training nativo (modello addestrato direttamente su sequenze lunghe), continued pre-training su long context (estendere un modello base), position interpolation (NTK-aware, YaRN), retrieval-augmented (delegare a [RAG](./rag.md) la selezione, mantenere context piccolo).

Contrasto context-vs-RAG. Long context vince quando il corpus e' < 1-2M token, la query richiede sintesi globale, la latenza piu' alta e' tollerata. RAG vince per corpora vasti, query puntuali, costi bassi per richiesta. Pattern ibrido: RAG per filtrare al milione di token poi long context per ragionare globalmente.

Un terzo approccio emerso nella primavera 2026 e' l'esternalizzazione dello stato fuori dal context. Le Dynamic Workflows di Claude Opus 4.8 (28 maggio 2026) ne sono l'esempio piu' netto: invece di tenere tutta la storia di un task multi-step a scala di codebase dentro la finestra, Claude scrive uno script JavaScript che orchestra fino a 1.000 subagenti totali (16 in parallelo); il piano vive nello script, i risultati intermedi nelle variabili, e il context riceve solo la risposta finale. E' una risposta diretta al problema dell'overflow: il context window non viene esteso, viene aggirato delegando il coordinamento a un'orchestrazione esterna.

## Quando usarlo / quando no

Sfruttare un context grande e' la scelta giusta quando: si analizza un documento intero (contratto, paper, codebase) che entra nella finestra; si fa long-form generation (un report lungo che richiede coerenza globale); si fanno chat lunghe con storia rilevante; si fa few-shot con molti esempi. E' anche utile per debugging di codice complesso, dove vedere l'intero modulo aiuta.

Non bisogna sfruttarlo quando: il task richiede solo un frammento (un chunk RAG di 500 token basta); il costo per chiamata diventa proibitivo (256k token in input a tariffa LLM frontier sono molti dollari per richiesta); la latenza diventa intollerabile (un context da 1M token aggiunge secondi); il "lost in the middle" degrada la qualita'.

Anti-pattern. Riempire il context "per sicurezza" con tutto il possibile: piu' rumore peggiora le risposte. Ignorare il prompt caching: le finestre grandi sono economiche solo se il prefisso e' cached (Anthropic prompt caching, OpenAI prompt caching; Grok Build 0.1 espone token cached a $0,20/1M contro $1/1M dei token freschi, un fattore 5 che cambia l'economia di un workflow). Non gestire il contesto di un agent: in [agent](./agent.md) lunghi la storia cresce, va periodicamente riassunta (compaction) o spostata fuori dal context con un'orchestrazione esterna (vedi Dynamic Workflows), altrimenti la finestra esplode. Confondere context window e knowledge cutoff: la finestra e' "quanto puoi mostrare al modello in una chiamata", non "quanto sa".

## Esempi pratici

Esempio 1: analisi di documento lungo. Si carica un PDF di 200 pagine (~80k token). Si chiede al modello di sintetizzare i 5 punti chiave e identificare contraddizioni. Senza long context bisognerebbe spezzare in chunk, riassumere ognuno, poi sintetizzare i riassunti (pipeline map-reduce). Con un context da 200k il task e' single-shot, qualita' superiore perche' il modello vede tutto contemporaneamente.

Esempio 2: prompt caching. Anthropic e OpenAI consentono di marcare prefissi del prompt come cache-able. Una applicazione che invia la stessa codebase di 100k token a ogni domanda paga il prezzo pieno solo la prima volta; le richieste successive (entro 5 minuti per Anthropic standard) hanno costo input ridotto del 90%. Sfruttare il caching e' essenziale per workflow long-context economicamente sostenibili.

Esempio 3: gestione context in agente. Un agente coding che lavora 30 step accumula history. A 100k token il prompt diventa pesante. Tecnica: ogni 20 step l'agent invoca una "summarize_history" che condensa gli step vecchi in un sommario di 2k token, mantenendo dettagli solo per gli ultimi 5. Il context resta gestibile, le metriche di task completion non peggiorano in modo significativo.

Esempio 4: orchestrazione fuori dal context. Per una migrazione su centinaia di migliaia di righe di codice, tenere ogni file modificato e ogni risultato di test nella finestra porterebbe rapidamente all'overflow. Con un'architettura tipo Dynamic Workflows si scrive uno script che lancia subagenti in parallelo, ciascuno con il proprio context fresco su un sottoinsieme di file; lo script accumula gli esiti nelle sue variabili e restituisce al context principale solo lo stato di avanzamento e la risposta finale. La test suite esistente funge da criterio di accettazione. Il context principale resta leggero mentre il lavoro effettivo gira su molte finestre indipendenti.

## Letture

- Vaswani et al., "Attention Is All You Need", 2017. https://arxiv.org/abs/1706.03762
- Su et al., "RoFormer: Enhanced Transformer with Rotary Position Embedding", 2021. https://arxiv.org/abs/2104.09864
- Press et al., "Train Short, Test Long: Attention with Linear Biases" (ALiBi), 2022. https://arxiv.org/abs/2108.12409
- Dao et al., "FlashAttention: Fast and Memory-Efficient Exact Attention", 2022. https://arxiv.org/abs/2205.14135
- Liu et al., "Lost in the Middle: How Language Models Use Long Contexts", 2023. https://arxiv.org/abs/2307.03172
- Peng et al., "YaRN: Efficient Context Window Extension of Large Language Models", 2023. https://arxiv.org/abs/2309.00071
- Gemini 1.5 Technical Report, Google DeepMind 2024. https://arxiv.org/abs/2403.05530
- Akhauri & Abdelfattah, "Compute Where it Counts: Self Optimizing Language Models", 2026. https://arxiv.org/abs/2605.10875
- Anthropic, "Prompt caching documentation". https://docs.anthropic.com/en/docs/build-with-claude/prompt-caching

## Note operative

Misurare il context realmente usato. Spesso si riempie il prompt senza misurare. Strumenti come tiktoken (OpenAI) o gli SDK Anthropic permettono di contare i token prima di inviare la richiesta. Una buona pratica e' loggare per ogni chiamata `input_tokens`, `output_tokens`, `cache_read_tokens`, `cache_write_tokens`. Sopra l'80% del context window dichiarato la qualita' degrada e i costi diventano sproporzionati: meglio progettare l'app perche' resti sotto questa soglia.

Lost in the middle. Quando si comporre un prompt con piu' chunk recuperati via [RAG](./rag.md), l'ordine importa. Mettere i chunk piu' rilevanti all'inizio o alla fine del contesto, non al centro, migliora la performance. Per query agentiche, ridurre la verbosita' dei tool result (es. troncare output di file > 5k token, paginare elenchi lunghi) preserva attenzione del modello.

Caching budget. Anthropic permette fino a 4 cache breakpoint per richiesta. La granularita' importa: mettere un breakpoint dopo il system prompt e uno dopo i documenti immutabili massimizza il riuso. Cambiare anche un solo carattere prima del breakpoint invalida la cache. Per workflow ad alta variabilita', conviene strutturare il prompt come "stable prefix + variabile suffix", non mescolare.

Pattern di compaction. Per agenti long-running serve una strategia di riassunto. Schema tipico: ogni N step l'agent invoca un sub-task "riassumi gli ultimi M step in massimo K token", il riassunto sostituisce gli step originali nella history. Si tengono integri solo gli ultimi 2-3 step. La storia completa viene archiviata fuori-context su disco o database, recuperabile su richiesta esplicita.

Esternalizzazione dello stato. Quando il task supera per sua natura qualsiasi finestra (migrazioni su intere codebase, run agentiche di molte ore), la compaction non basta: conviene spostare il coordinamento fuori dal context con un'orchestrazione esplicita. Lo stato vive in uno script o in un layer applicativo, i sottoprocessi ricevono context freschi e mirati, e la finestra principale mantiene solo il sommario di avanzamento. E' un cambio di mentalita': il context window non e' la memoria dell'agente, e' solo la sua memoria di lavoro immediata.

## Aggiornamenti

### 2026-06-15

MiniMax M3 pesi open pubblicati (~11 giugno): primo modello open-weight con contesto da 1M token nativo al livello di qualita' frontier (59% SWE-Bench Pro). Il rapporto tecnico arXiv:2606.13392 documenta MiniMax Sparse Attention (MSA) come la tecnica che abilita il 1M token context a un costo di inference gestibile. Prima della pubblicazione dei pesi di M3, i modelli open-weight con 1M di contesto erano tutti significativamente inferiori ai modelli frontier per qualita' (gap di 15-25 punti su SWE-Bench Pro); M3 riduce il gap a zero su quel benchmark e lo rende disponibile per auto-hosting e fine-tuning. Aggiornata la tabella modelli nella sezione Varianti / approcci per includere MiniMax M3. [Digest 2026-06-15](../../digest/2026/06/15.md)

### 2026-06-20

Tre nuovi modelli con finestre di contesto rilevanti. GLM-5.2 (Zhipu/Z.ai, pesi MIT su Hugging Face dal 17 giugno) introduce un contesto da 1M token open-weight su un'architettura MoE a 744B/40B attivi — secondo modello open-weight (dopo MiniMax M3, coperto 15 giugno) a raggiungere questa soglia con qualita' frontier. Kimi K2.7-Code (Moonshot, 12 giugno) e Cohere North Mini Code (9 giugno) operano su 256K token, che rimane la fascia standard per i modelli di coding agentico. Grok 4.3, disponibile in GA su Amazon Bedrock dal 15 giugno, aggiunge 1M token in un contesto enterprise con serving su Mantle (nuovo inference engine Bedrock). Il pattern che emerge: nel segmento coding agentico open-weight il context standard si assesta su 256K (sufficiente per codebase di media taglia), mentre i modelli general-purpose con 1M token si moltiplicano. [Digest 2026-06-20](../../digest/2026/06/20.md).

### 2026-06-07

Google conferma (TechTimes 6 giugno + 3 fonti secondarie: codersera.com, ofox.ai, aimlapi.com) che Gemini 3.5 Pro avra' una finestra di contesto da 2 milioni di token — la piu' grande annunciata per qualsiasi modello frontier a oggi — con GA attesa entro fine giugno 2026. Il modello e' gia' in limited preview per enterprise selezionati su Vertex. La finestra da 2M token ridisegna la soglia di utilizzo del RAG per i corpus sotto quella dimensione: una codebase di media taglia (~500k token, ~2M caratteri), una base documentale aziendale o un anno di transcript di meeting entrano in singola call senza preprocessing. Aggiornata la tabella modelli nella sezione Varianti / approcci. [Digest 2026-06-07](../../digest/2026/06/07.md)

### 2026-06-01

Mese intenso di rilasci che confermano il long context come terreno competitivo. Sul fronte modelli: Mistral Medium 3.5 (256k, [01.md](../../digest/2026/05/01.md)), IBM Granite 4.1 con 512k token nativi ([05.md](../../digest/2026/05/05.md)), GPT-Realtime-2 salito da 32k a 128k ([08.md](../../digest/2026/05/08.md)), Gemini 3.5 Flash con 1M token nativo a Google I/O ([20.md](../../digest/2026/05/20.md)), Qwen3.7-Max con 1M token e run autonome fino a 35 ore con 1.000+ tool call ([23.md](../../digest/2026/05/23.md)), Grok Build 0.1 (256k, cached $0,20/1M, [26.md](../../digest/2026/05/26.md)). Due novita' strutturali oltre i numeri di finestra: le Dynamic Workflows di Claude Opus 4.8, che spostano il coordinamento di task multi-step fuori dal context via orchestrazione di subagenti ([29.md](../../digest/2026/05/29.md)), e l'hardware per il long context locale con Nvidia RTX Spark (128 GB unificati, context fino a 1M su laptop, [06/01.md](../../digest/2026/06/01.md)). Sul lato efficienza: il paper SOL sul compute adattivo per token ([13.md](../../digest/2026/05/13.md)) e l'acquisizione di Eigen AI (AWQ) da parte di Nebius ([03.md](../../digest/2026/05/03.md)). Aggiornati tabella modelli, sezioni Come funziona e Varianti, aggiunto Esempio 4 e una nota operativa sull'esternalizzazione dello stato.

### 2026-06-29

CompressKV (arXiv:2606.24467, 23 giugno, 5 fonti: arXiv abs/HTML/OpenReview/Semantic Scholar/moonlight.io) affronta il problema dell'esplosione della KV cache su context lunghi con un approccio basato su Semantic Retrieval Heads: le teste di attenzione che eseguono retrieval semantico vengono identificate e mantenute con KV cache completa; le altre vengono compresse o eliminate. Il risultato misurato e' 97% di qualita' con 3% della dimensione originale della KV cache — riduzione di oltre 30x. Per il concetto di context window, l'implicazione e' diretta: la barriera pratica all'utilizzo di contesti da 1M token non e' solo il limite dichiarato del modello ma la memoria GPU richiesta dalla KV cache a runtime (vedi sezione Come funziona). CompressKV riduce questa barriera di un ordine di grandezza, avvicinando il context window lungo nominalmente dichiarato alla finestra effettivamente usabile in produzione senza hardware dedicato. Il paper si inserisce in un filone di ottimizzazione della KV cache che include GQA (condivisione key/value tra heads), PagedAttention (vLLM, gestione paginata), KVarN (quantizzazione 2-bit, coperto digest 07 giugno) e MiniMax MSA (sparsita' blockwise, coperto digest 15 giugno): CompressKV aggiunge la dimensione della selezione strutturale per testa, invece di applicare la stessa compressione uniformemente a tutte le posizioni. [Digest 2026-06-29](../../digest/2026/06/29.md)
