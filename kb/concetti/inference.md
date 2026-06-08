---
name: Inference
aliases: [inference, inferenza, serving, generation, decoding]
categoria: infrastruttura
created: 2026-04-28
last_updated: 2026-06-08
mentions_count: 28
---

# Inference

## Cos'e

L'inference e' la fase di esecuzione di un modello addestrato, in cui dato un input si calcolano le predizioni. Per un [LLM](./llm.md) e' il processo di generazione token-per-token: ad ogni passo, dato il prefisso, il modello produce una distribuzione di probabilita' sul vocabolario, si campiona un token, lo si aggiunge al prefisso, si ripete. L'inference si distingue dal training per due caratteristiche fondamentali: non si calcolano gradienti (no backpropagation), e si ottimizza per latenza e throughput, non per accuratezza di gradiente.

L'inference su LLM e' diventata una disciplina ingegneristica autonoma tra il 2022 e il 2026. I costi a regime di un sistema AI sono dominati dall'inference: il training si paga una volta, l'inference si paga per ogni richiesta, per ogni utente, per sempre. Greg Brockman ha rivelato in aula (processo Musk v. Altman) che OpenAI spende 50 miliardi di dollari in compute nel 2026 contro 30 milioni nel 2017, una crescita di oltre 1.600x in nove anni: una parte crescente di quella spesa e' inference a produzione, non training. Aziende dedicate (Together, Fireworks, Groq, Cerebras, SambaNova) e progetti open (vLLM, TensorRT-LLM, llama.cpp, MLC, SGLang) competono su throughput, latenza, costo per milione di token.

L'importanza pratica di capire l'inference e' triplice. Per chi costruisce: sapere come scegliere modello e provider in base a costi e SLA. Per chi opera: sapere come dimensionare GPU, batch size, quantizzazione. Per chi progetta prodotti: sapere quali UX sono economicamente sostenibili (es. streaming token in chat funziona, ma 100k token di output per ogni utente non e' viabile). Nella primavera 2026 il tema dominante e' il crollo del costo per token guidato dall'hardware: l'inferenza agentica, che genera ordini di grandezza piu' token di una chat, ha reso il costo per token la variabile competitiva piu' importante dell'intera industria.

## Come funziona

L'inference autoregressive ha due fasi tecnicamente distinte.

Prefill. Tutti i token dell'input (prompt + history) vengono processati in parallelo in un singolo forward pass. Si calcolano le rappresentazioni di tutti i token, e le K, V (key, value) per ogni layer vengono salvate nella KV cache. Il prefill e' compute-bound: scala con O(n^2) attention nel context size n, ma essendo parallelizzabile sulle GPU si esegue in centinaia di millisecondi anche su input lunghi.

Decode. Si genera un token alla volta in sequenza. Ogni step computa un singolo nuovo token: si calcolano Q, K, V per il nuovo token, l'attention sfrutta la KV cache (no ricalcolo), si applicano FFN, projection, softmax, sampling. Il decode e' memory-bound: l'overhead dominante e' leggere i pesi del modello (decine-centinaia di GB) dalla VRAM ad ogni step. Su una GPU H100 con un modello 70B in bfloat16, il throughput single-stream e' 30-80 token/s. Con batching e ottimizzazioni puo' superare 5000 token/s aggregati su molte query concorrenti. La natura memory-bound del decode e' la ragione per cui tutta l'innovazione hardware del 2026 punta a spostare i pesi piu' vicino alle unita' di calcolo (SRAM on-chip, in-memory compute, memoria unificata ad alta bandwidth).

KV cache. Memorizza key e value di tutti i token gia' processati per evitare di ricalcolarli. La sua dimensione e' `2 * num_layers * num_heads * head_dim * seq_len * dtype_size`. Per Llama 3 70B (80 layer, 64 heads, head_dim 128) con seq 4k in fp16: circa 5 GB. La KV cache e' la fonte primaria del consumo memoria a runtime e cresce linearmente con la lunghezza del context: con context da 1M token diventa proibitiva. Ottimizzazioni: GQA (Grouped Query Attention) e MQA condividono key/value tra heads, riducendo il KV; PagedAttention (vLLM) gestisce la KV cache come memoria virtuale paginata, eliminando frammentazione; prefix caching riusa la KV cache di prefissi condivisi (es. lo stesso system prompt).

Sampling. Dato il vettore di logit, si campiona il token successivo. Strategie: greedy (argmax, deterministico), temperature scaling (`logits / T`), top-k (limita ai k token piu' probabili), top-p / nucleus (limita all'insieme la cui probabilita' cumulativa supera p), min-p, typical sampling, repetition penalty, beam search (esplora k sequenze in parallelo, raro per LLM moderni).

Speculative decoding (Leviathan et al. 2022, Chen et al. 2023). Un modello "draft" piccolo e veloce produce piu' token speculativi; il modello "target" grande li verifica in un singolo forward pass parallelo. Se la verifica conferma, si accettano molti token in un colpo. Speedup tipico 2-3x su workload generativi. Tecniche correlate: Medusa (head multiple), EAGLE (training congiunto draft-target).

Quantizzazione. Riduce la precisione dei pesi (e talvolta delle attivazioni) per ridurre memoria e aumentare throughput. Schemi: INT8 (peso 8-bit, qualita' quasi invariata), INT4 (peso 4-bit, perdita 1-3%), GPTQ, AWQ, GGUF (formato di llama.cpp), FP8 (Hopper, Blackwell), FP4/NVFP4 (Blackwell e Rubin, dove i Tensor Core supportano nativamente la precisione a 4 bit in floating point). Un modello 70B in INT4 entra in una singola H100 80GB invece di richiederne due in fp16. Il formato NVFP4 dei nuovi acceleratori Nvidia rende la quantizzazione a 4 bit un percorso hardware-nativo, non solo un trucco software.

Batching e continuous batching. Servire piu' richieste insieme aumenta l'utilizzo GPU. Continuous batching (vLLM, TGI) inserisce nuove request nel batch durante il decoding, senza aspettare che una request finisca. Throughput aggregato cresce di 5-20x rispetto a batching naive.

Distillation. Trasferimento da modello grande a modello piccolo. Un modello piccolo addestrato su dati prodotti da un modello grande puo' avvicinarne la qualita' a una frazione del costo di inferenza. IBM Granite 4.1 (rilasciato fine aprile 2026) e' un esempio della tendenza: il modello 8B instruct supera costantemente il Granite 4.0 32B MoE sui benchmark, con un quarto dei parametri, abbattendo i costi di serving a parita' di qualita'.

Hardware. Nvidia resta dominante (H100, H200, B100, B200, Blackwell, Rubin), con AMD MI300/MI325X, Google TPU, AWS Trainium e silicio custom degli hyperscaler (Microsoft MAIA 200). Gli acceleratori specializzati per inference puntano a eliminare il bottleneck memory-bound del decode: Groq LPU (low-latency, throughput record single-stream), Cerebras WSE-3 (intero wafer, 44 GB di SRAM on-chip), Fractile (in-memory compute). Vedi anche [mixture-of-experts](./mixture-of-experts.md) per l'inference sparsa.

Numeri. Tariffe medie per milione di token output, primavera 2026: frontier closed (Claude Opus 4, GPT-5) circa 30-75 $/M; mid-tier (Sonnet, GPT-5 mini, Gemini 3.1 Flash-Lite a 1,50 $/M output) circa 1-15 $/M; small open su provider (Llama 3 70B su Together, Fireworks) circa 0,5-2 $/M; self-hosted con quantizzazione e batching su H100 circa 0,1-0,5 $/M. La differenza di ordini di grandezza tra frontier e small fa scegliere i modelli in base al task. Le tariffe sono in caduta: Gemini 3.1 Flash-Lite costa 0,25 $/M in input con time-to-first-token 2,5x piu' rapido di 2.5 Flash, e i clienti GA riportano riduzioni di costo del 60% rispetto ai modelli "thinking-tier".

## Varianti / approcci

| Strategia | Idea | Trade-off |
|---|---|---|
| Quantizzazione | Pesi a 8/4/2 bit (INT4, AWQ, FP4) | Memoria/speed vs qualita' |
| KV cache compression | INT8 KV, eviction selettiva | Context lungo a bassa memoria |
| Speculative decoding | Draft + verify | Latency reduction, complessita' |
| Continuous batching | Batch dinamico | Throughput, latenza per-request stabile |
| Tensor parallel | Pesi splittati su piu' GPU | Modelli grandi, comunicazione overhead |
| Pipeline parallel | Layer su GPU diverse | Modelli grandi, latenza |
| MoE inference | Solo expert selezionati | Throughput x denso simile, infra complessa |
| Long context optimization | Sliding window, chunked prefill | 1M+ context realistico |
| Compilation | TorchCompile, TensorRT | 10-30% speedup |
| Disaggregated serving | Prefill workers + decode workers separati | Scaling indipendente |
| Linear attention / SSM | Stato ricorrente a dimensione fissa | Memoria costante nel decode, retrieval piu' debole |
| In-memory / wafer-scale HW | Pesi vicini al calcolo, SRAM on-chip | Token/s record, ecosistema immaturo |

Sulle architetture alternative al transformer puro per inference economica: state space model (Mamba, RWKV) con costo lineare in sequenza, ibridi (Jamba di AI21, Striped Hyena, Granite 4.x che mescola Mamba e attention), modelli MoE che attivano una frazione di parametri. La linear attention rimpiazza la KV cache con uno stato ricorrente di dimensione fissa, riducendo il decode a costo costante in memoria, al prezzo di una capacita' di retrieval a chiavi multiple piu' debole: e' la classe di architetture su cui si concentra la ricerca per rendere viabile il context da milioni di token senza esplosione della memoria.

## Quando usarlo / quando no

Self-hosting dell'inference e' la scelta giusta quando: il volume e' alto (ROI sui costi fissi GPU); ci sono requisiti di privacy/compliance (dati che non possono uscire); serve latenza ultra-bassa con hardware dedicato; il workload e' prevedibile. API managed e' la scelta giusta quando: volume basso o burst (paghi solo l'usato); si vogliono modelli frontier non self-hostable; non si ha team SRE/MLOps; le SLA del provider bastano. Una terza opzione cresce nel 2026: i neocloud token-as-a-service (GroqCloud, Together, Fireworks) che vendono token a prezzo aggressivo senza esporre la complessita' dell'infrastruttura, posizionandosi tra il managed dei lab e il self-hosting puro.

Anti-pattern. Self-hosting di un modello quando il volume mensile non copre il costo della GPU. Usare il modello frontier per task in cui un small model con [fine-tuning](./fine-tuning.md) basta. Ignorare il prompt caching: un'app che invia lo stesso system prompt di 10k token a ogni chiamata paga 10k token ogni volta invece di pagare 1k cached + delta. Non monitorare costo per request: i conti delle API LLM esplodono silenziosamente, e con i workload agentici (decine di chiamate per task) l'esplosione e' molto piu' rapida. Ignorare la latenza per UX: oltre 3 secondi senza streaming gli utenti percepiscono il sistema come rotto. Acquistare hardware di nicchia (LPU, wafer-scale) senza verificare maturita' dell'ecosistema software: il throughput record di un chip e' inutile se non supporta il modello o il framework che serve.

## Esempi pratici

Esempio 1: serving con vLLM.

```bash
pip install vllm
python -m vllm.entrypoints.openai.api_server \
  --model meta-llama/Meta-Llama-3-8B-Instruct \
  --gpu-memory-utilization 0.9 \
  --max-model-len 8192 \
  --enable-prefix-caching
```

Espone un endpoint OpenAI-compatible. Su una H100 si ottengono > 4000 token/s aggregati con batching, latenza P50 di pochi secondi per risposta tipica.

Esempio 2: quantizzazione con llama.cpp.

```bash
# converti
python convert.py /path/to/llama-3-70b
# quantizza a Q4_K_M
./quantize ggml-model-f16.gguf llama-3-70b-Q4_K_M.gguf Q4_K_M
# inference
./main -m llama-3-70b-Q4_K_M.gguf -p "Spiega la legge di Murphy"
```

Llama 3 70B Q4_K_M sta in circa 40 GB; gira su MacBook M3 Max (96 GB) a 5-10 tok/s, su una H100 a 50-80 tok/s. Con l'arrivo di SoC consumer a memoria unificata ad alta capacita' (Nvidia RTX Spark, 128 GB LPDDR5X a 300 GB/s, annunciato al Computex 2026) un laptop puo' caricare interamente in memoria modelli 70B-120B senza quantizzazione degradante, con context fino a 1M token: l'inference edge non quantizzata di modelli grandi diventa realistica.

Esempio 3: scelta architetturale di un'app SaaS. 100k richieste/giorno, prompt medio 2k token, output medio 500. Con GPT-5 (es. 5 $/M input + 15 $/M output): circa 2,0k$ + 0,75k$ = 2750 $/giorno. Con Claude Sonnet 4 a tariffe simili: stesso ordine. Con Llama 3.1 70B su Together (0,9 $/M): circa 320 $/giorno. Decisione: usare il modello frontier solo per le query dove serve, routing su small model per > 70% dei casi (classificazione, estrazione, risposte semplici). Cost reduction tipica: 60-80%.

## Letture

- Pope et al., "Efficiently Scaling Transformer Inference" (PaLM serving), 2022. https://arxiv.org/abs/2211.05102
- Kwon et al., "Efficient Memory Management for Large Language Model Serving with PagedAttention" (vLLM), 2023. https://arxiv.org/abs/2309.06180
- Leviathan et al., "Fast Inference from Transformers via Speculative Decoding", 2022. https://arxiv.org/abs/2211.17192
- Frantar et al., "GPTQ: Accurate Post-Training Quantization", 2022. https://arxiv.org/abs/2210.17323
- Lin et al., "AWQ: Activation-aware Weight Quantization", 2023. https://arxiv.org/abs/2306.00978
- "Efficient Streaming Language Models with Attention Sinks" (StreamingLLM), Xiao et al. 2023. https://arxiv.org/abs/2309.17453
- vLLM documentation. https://docs.vllm.ai
- "Artificial Analysis" inference benchmarks. https://artificialanalysis.ai

## Note operative

Streaming. L'inference autoregressiva permette di restituire i token man mano che vengono generati. Nelle UI conversazionali e' essenziale: senza streaming l'utente attende secondi guardando uno spinner; con streaming vede progressi immediati e percepisce sistema reattivo. Server-Sent Events o WebSocket sono i trasporti tipici. Il time-to-first-token (TTFT) e' la metrica chiave di UX, separata dal token-per-second.

Routing tra modelli. Un'app moderna spesso usa una flotta: small per classificazione e estrazione, medium per generazione standard, frontier per task hard, reasoning per problemi STEM. Un router (basato su classificatore o regola) sceglie il modello per ogni richiesta. Open-source come LiteLLM, RouteLLM, Martian semplificano l'orchestrazione. Risparmi tipici 40-70% rispetto a "tutto sul modello frontier".

Cold start e warm-up. Self-hosting con auto-scaling soffre di cold start: avviare un container con modello 70B richiede minuti per scaricare i pesi e riempire la KV cache iniziale. Pattern produttivi: pre-warm di repliche minime sempre attive, tier separati per richieste latency-critical vs batch, scaling reattivo basato su QPS osservato. I provider managed (Together, Fireworks, Bedrock, Vertex) gestiscono questo per te a costo di markup.

Inference agentica. I workload agentici (loop di [agent](./agent.md), [tool use](./tool-use.md), [multi-agent orchestration](./multi-agent-orchestration.md)) cambiano il profilo di carico dell'inference: una singola task utente puo' generare decine di chiamate LLM in sequenza, con context che cresce ad ogni step. Questo amplifica sia il costo per task sia la sensibilita' alla latenza per-chiamata, e rende il prompt/prefix caching e il context management decisivi. Anthropic con i Claude Managed Agents separa il loop agentico (su Anthropic) dall'esecuzione tool (in sandbox self-hosted del cliente): l'inference del modello resta centralizzata, l'esecuzione si distribuisce.

## Aggiornamenti

### 2026-05-03

Nebius Group acquisisce Eigen AI per $643 milioni, la piu' grande acquisizione mai registrata focalizzata esclusivamente sull'ottimizzazione dell'inferenza. La tecnologia chiave di Eigen AI e' AWQ (Activation-Aware Weight Quantization), sviluppata da Wei-Chen Wang (MIT HAN Lab, MLSys Best Paper 2024): quantizza i pesi LLM a 4 bit con attenzione selettiva ai canali piu' sensibili all'attivazione, riducendo la perdita di qualita' rispetto alla quantizzazione uniforme. Il risultato pratico: un modello che richiederebbe due GPU H100 in fp16 gira su una singola GPU in INT4. Eigen AI aveva gia' ottenuto i primi rank su Artificial Analysis per throughput di token output. L'acquisizione da $643M per 20 persone, circa $32M per ricercatore, segnala che lo strato di ottimizzazione dell'inferenza e' diventato l'asset piu' conteso nell'infrastruttura AI: la capacita' di "fare di piu' con le stesse GPU" vale quanto la GPU stessa. [Digest 2026-05-03](../../digest/2026/05/03.md)

### 2026-05-06

Due segnali convergenti sul costo dell'inferenza a produzione. Greg Brockman rivela in aula (processo Musk v. Altman) che OpenAI spende $50 miliardi in compute nel 2026, contro $30 milioni nel 2017: una crescita di oltre 1.600x in nove anni, superiore alle stime degli analisti e coerente con il superamento del target Stargate da 10 GW. Parallelamente, Allen Institute for AI pubblica MolmoAct2 (arXiv 2605.02881), modello open-source di action reasoning robotico che ottiene un throughput 2,42x superiore all'inference non ottimizzata del predecessore su task DROID con oggetti non visti: il risultato indica che ottimizzazioni architetturali specifiche per dominio (robot vs. chat) producono guadagni di latenza comparabili a quelli della quantizzazione generale. [Digest 2026-05-06](../../digest/2026/05/06.md)

### 2026-05-13

Tre segnali sull'inference. TML-Interaction-Small introduce il paradigma del micro-turn: invece di un ciclo prefill-decode lineare, il modello processa audio, video e testo in chunk da 200 ms in modo continuativo, leggendo l'input e producendo output in simultanea, una modalita' che richiede un'architettura di inference non autoregressive nel senso tradizionale, con streaming bidirezionale a bassa latenza come vincolo primario. SOL (arXiv:2605.10875) propone una policy network leggera che alloca dinamicamente il budget di compute per ogni token decodificato, controllando contemporaneamente sparsita' di attention, pruning nelle MLP e bit-width della quantizzazione, con i pesi del modello base congelati. Claude Platform on AWS raggiunge la general availability come primo hyperscaler con accesso nativo alla piattaforma Anthropic. [Digest 2026-05-13](../../digest/2026/05/13.md)

### 2026-05-14

Due segnali sul futuro dell'inference hardware e software. Fractile ($220M Series B, 13 maggio) porta l'in-memory-compute chip specializzato per AI inference: i calcoli avvengono direttamente in memoria, eliminando il collo di bottiglia di trasferimento pesi DRAM-chip che domina il costo del decode autoregressivo su GPU standard; le performance dichiarate sono 25x piu' veloci e 10x piu' economiche delle GPU correnti per workload di reasoning, con target di 1.200 token/secondo e primo silicio commerciale atteso nel 2027. Multi-Stream LLMs (arXiv 2605.12460, ELLIS/Tübingen) introduce un approccio complementare lato architetturale: stream paralleli di computazione dove ogni forward pass legge da piu' input stream e genera in piu' output stream simultaneamente. [Digest 2026-05-14](../../digest/2026/05/14.md)

### 2026-05-15

Due segnali convergenti sull'hardware. Cerebras debutta al Nasdaq il 14 maggio con un'IPO da $5,55 miliardi, la maggiore IPO tech USA del 2026, con apertura a $385 (+108% rispetto al prezzo di offerta di $185). Il core della tesi e' il WSE-3 (Wafer Scale Engine 3): un chip che corrisponde all'intero wafer di silicio invece dei die separati, con 4 trilioni di transistor e 44 GB di SRAM on-chip. L'SRAM on-chip elimina il principale bottleneck del decode autoregressivo su GPU (il trasferimento dei pesi da DRAM al chip a ogni step), con throughput dichiarato fino a 2.000 token/s su modelli 70B contro i 150-300 tipici di H100 in serving standard. L'IPO certifica che la tesi hardware alternativa alla GPU per l'inference LLM ha trovato validazione di mercato a scala. Parallelamente, Microsoft MDASH documenta il costo dell'inference agentica orchestrando 100+ agenti su un ensemble di modelli frontier e distillati. [Digest 2026-05-15](../../digest/2026/05/15.md)

### 2026-05-24

Gated DeltaNet-2 (arXiv 2605.22791, NVLabs, Ali Hatamizadeh, Yejin Choi, Jan Kautz) introduce un contributo rilevante all'inference su sequenze lunghe tramite linear attention con gate disaccoppiati. L'architettura standard di softmax attention scala come O(n^2) nella lunghezza della sequenza per il prefill e richiede una KV cache che cresce linearmente nel context size; la linear attention (Mamba, DeltaNet, RWKV) rimpiazza questa cache con uno stato ricorrente di dimensione fissa, riducendo il decode a costo costante in memoria ma sacrificando la capacita' di retrieval a chiavi multiple. Gated DeltaNet-2 risolve il trade-off con gate channel-wise separati per erase e write: a 1.3B parametri su 100B token FineWeb-Edu, supera Mamba-2, Mamba-3, Gated DeltaNet e KDA su linguaggio, ragionamento e retrieval, con il vantaggio piu' pronunciato sui benchmark RULER needle-in-a-haystack a chiavi multiple. Il risultato e' rilevante per scenari di inference con context window >1M token dove la KV cache cresce in modo proibitivo. Il codice e' open su GitHub (NVlabs/GatedDeltaNet-2). [Digest 2026-05-24](../../digest/2026/05/24.md)

### 2026-06-01

Il mese chiude con un tema dominante: il costo per token dell'inference e' diventato la variabile competitiva centrale dell'industria, e l'hardware e' la leva principale. Tre filoni emersi a fine maggio e inizio giugno.

Hardware Nvidia che ridefinisce il costo per token. Al Computex 2026 (1 giugno, Taipei) Nvidia conferma che Anthropic, OpenAI e SpaceX/xAI sono tra i primi grandi clienti del Vera CPU per datacenter, che affianca la Rubin GPU nella piattaforma Vera Rubin. La Vera Rubin NVL72 (unita' full-rack) dichiara 5x le prestazioni di inferenza rispetto a Blackwell e fino a 10x un costo per milione di token inferiore (un decimo del costo per token), con la Rubin GPU a 50 PFLOPs di inference NVFP4. Il fatto strutturale rilevante: i tre principali concorrenti frontier dipendono tutti dalla stessa roadmap hardware Nvidia, per cui ogni vantaggio differenziale di accesso ai chip (volumi, timing, pricing) si traduce direttamente in vantaggio sui costi di serving. Verificato anche via Tom's Hardware e Nvidia. [Digest 2026-06-01](../../digest/2026/06/01.md)

Inference edge non quantizzata. Sempre al Computex, Nvidia annuncia RTX Spark, il primo SoC Arm proprietario per PC (Grace CPU 20 core + Blackwell GPU 6144 CUDA core con FP4, 128 GB LPDDR5X unificata a 300 GB/s). La memoria unificata ad alta capacita' e' la discontinuita': per la prima volta un laptop consumer puo' caricare interamente in memoria modelli 70B-120B senza quantizzazione degradante, con context fino a 1M token per sessioni agentiche prolungate. Otto OEM (Dell, HP, Lenovo, Microsoft Surface, Asus, MSI) hanno confermato dispositivi per l'autunno 2026, in diretta competizione con Apple Silicon sulla fascia alta. Sposta in basso la soglia dell'inference locale di modelli grandi. [Digest 2026-06-01](../../digest/2026/06/01.md)

Il pivot di Groq da chip a neocloud. Groq raccoglie $650M (scoop Axios 28 maggio, confermato TechCrunch 29 maggio) per reinventarsi come AI inference neocloud dopo aver ceduto la tecnologia LPU a Nvidia per $20 miliardi (dicembre 2025). "Groq 2.0", guidata da Adam Winter (CEO) e Matt Eng (CFO), punta su GroqCloud come piattaforma token-as-a-service con circa 2 milioni di developer. Axios definisce la formula "un potenziale nuovo template di transazione" nei mercati privati AI: una startup di chip cede il suo IP hardware al monopolista (Nvidia) e si reinventa come cloud player usando quella liquidita'. Il segnale strategico: il valore si sposta dal silicio alla capacita' di vendere token a basso costo a scala. [Digest 2026-05-31](../../digest/2026/05/31.md)

Sul fronte silicio custom, Anthropic e Microsoft negoziano un accordo sul chip MAIA 200 (CNBC/Bloomberg 21 maggio), che sarebbe il primo deployment esterno del processore custom Microsoft (prestazioni dichiarate +30% nel fleet Azure): Anthropic diversifica la supply chain di compute, gia' distribuita tra AWS Trainium, Google TPU e GPU Nvidia via SpaceX. Sul fronte ricerca di base, fisici di Penn (25 maggio) dimostrano switching ottico a 4 attojoule con exciton-polaritons, tre ordini di grandezza sotto i transistor a silicio: non un chip pronto, ma un percorso verso acceleratori fotonici per l'inferenza ad altissimo volume, dove il consumo energetico e' uno dei tre colli di bottiglia sistemici (insieme a memory bandwidth e latenza inter-chip). [Digest 2026-05-25](../../digest/2026/05/25.md)

In sintesi, il filo conduttore del mese e' la convergenza: tutta l'innovazione (wafer-scale, in-memory, NVFP4, linear attention, memoria unificata edge, neocloud) attacca lo stesso bersaglio, ovvero il bottleneck memory-bound del decode e il costo per token che ne discende.

### 2026-06-03

OpenAI porta GPT-5.5, GPT-5.4 e Codex in GA su Amazon Bedrock il 2 giugno con stesso pricing per-token di direct OpenAI e governance enterprise nativa (IAM, PrivateLink, GuardRails, CloudTrail). Il caso rilevante per l'inference e' la convergenza: Bedrock diventa il layer di accesso neutro di fatto per i modelli frontier in produzione enterprise, con Anthropic Claude, Google Gemini (su Vertex) e OpenAI GPT tutti accessibili con governance enterprise nativa. La conseguenza pratica e' che la scelta del provider di inference per il deployment enterprise non e' piu' vincolata alla famiglia di modelli: un'organizzazione puo' usare Bedrock come unico layer di governance e scegliere il modello migliore per ogni task indipendentemente dal vendor, riducendo il vendor lock-in e semplificando i contratti. Sul fronte on-device, Microsoft Aion 1.0 Plan (14B, 32K context, in-box Windows) porta l'inference agentica completamente on-device su un sistema operativo mainstream: nessun round-trip cloud per la pianificazione, con il hardware RTX Spark come substrato per i workload piu' esigenti. [Digest 2026-06-03](../../digest/2026/06/03.md)

### 2026-06-05

Apple Private Cloud Compute (PCC) come architettura di inference per Siri rebuilt (annuncio atteso al WWDC 2026 dell'8 giugno, dettagli confermati il 4 giugno da TechCrunch e MacRumors). L'architettura: query dell'utente instradate verso server Apple con hardware-isolated enclaves dove i pesi di un modello Gemini customizzato da 1,2T parametri (partnership Apple-Google, gennaio 2026) girano in ambienti Apple-controllati; nessun dato utente condiviso con Google; i dati non vengono conservati dopo l'elaborazione. Il segnale per il concetto "inference" e' architetturale: PCC rappresenta un nuovo tier di inference che non e' ne' on-device ne' cloud pubblico tradizionale — e' confidential cloud computing, dove il vendor di modello (Google) fornisce i pesi ma non ha accesso agli input/output utente. Implica che per i modelli da 1T+ parametri, dove l'on-device e' praticabile solo in casi eccezionali (RTX Spark con 128GB unificata per modelli <120B), il confidential cloud computing diventa il template di riferimento per i vendor OS che vogliono preservare la privacy. Questa posizione intermedia — tra il on-device computing dove la privacy e' garantita fisicamente e il cloud tradizionale dove il vendor e' trusted per contratto — potrebbe diventare il pattern standard per OS-level AI inference. Vedi [digest 2026-06-05](../../digest/2026/06/05.md).

### 2026-06-04

Due segnali convergenti sull'economia dell'inference nel 2026. Alphabet raccoglie $80 miliardi (1 giugno, 5 fonti: abc.xyz, CNBC, Bloomberg, TechCrunch, Axios) con destinazione esplicita "AI compute infrastructure": la dimensione del fabbisogno di compute per l'inference di Google Cloud — backlog quasi raddoppiato a $460 miliardi trimestre su trimestre — richiede un'equity offering da record nella storia US per restare competitivi. Il capex dichiarato per il 2026 e' $180-190 miliardi, con il 2027 in ulteriore crescita: e' il segnale piu' concreto a oggi che il costo dell'inference a scala sistemica supera qualsiasi proiezione degli anni precedenti. MiniMax M3 (5 fonti, 1 giugno) introduce MiniMax Sparse Attention (MSA), un'architettura di attention sparsa che porta il decoding a 15,6x piu' veloce e il prefill a 9,7x piu' veloce rispetto al predecessore M2 su contesti da 1M token: un ottimizzazione architetturale specifica per il regime di inference a long context, dove il bottleneck memory-bound del decode diventa dominante. L'MSA e' un approccio diverso da GQA (condivisione key/value tra heads) e da PagedAttention (KV cache paginata): opera riducendo il numero di coppie key-value che ogni head di attention processa ad ogni step, mantenendo la qualita' su long-context a costo di throughput ridotto su context corto. Il risultato pratico rilevante per chi costruisce sistemi RAG o agenti a context lungo e' che l'ottimizzazione dell'inference su finestre da 500K-1M token e' ora una direzione di ricerca architetturale attiva, non solo un problema di hardware. [Digest 2026-06-04](../../digest/2026/06/04.md)

### 2026-06-07

KVarN (arXiv 2606.03458, Huawei CSL, 2 giugno, 5 fonti: arXiv + GitHub + NYU Shanghai AI + NVIDIA Developer Forums + HN 48399974) introduce il contributo piu' diretto al tema KV cache quantization comparso nei digest fino a oggi. Il paper risolve il problema dell'accumulo di errore in decode autoregressivo — ignorato dalle tecniche esistenti che valutano la KV cache quantization in setting prefill — con una pipeline Hadamard + dual-scaling variance normalization che porta la 2-bit quantization calibration-free a SOTA su MATH500, AIME24 e HumanEval, con throughput superiore a FP16 e accuratezza FP16-equivalente. Il risultato pratico e' un backend nativo vLLM (un singolo flag) che abilita 3-5x piu' sequenze parallele nella stessa memoria: un modello che richiedeva 4 H100 in FP16 per 100 sessioni concorrenti ne puo' servire 300-500 con KVarN a 2-bit. Il connettore con il filo conduttore inference economics della settimana e' diretto: ridurre la pressione sulla KV cache e' equivalente ad aumentare la capacita' di serving senza aggiungere hardware. [Digest 2026-06-07](../../digest/2026/06/07.md)

### 2026-06-08

Quattro segnali convergenti sull'economia dell'inference nel digest di oggi. Apple WWDC 2026 (8 fonti: MacRumors, Tom's Guide, CNBC, AppleInsider, Bloomberg, cryptobriefing, letsdatascience, heygotrade) introduce Private Cloud Compute (PCC) come terzo tier architetturale dell'inference: non on-device (come llama.cpp locale), non cloud pubblico tradizionale (come Bedrock o Vertex), ma confidential cloud computing — i pesi di Gemini 1,2T girano in enclave hardware-isolated su server Apple Silicon, con garanzia contrattuale che Google non puo' leggere gli input/output utente. Il pattern PCC risolve il trade-off tra modelli frontier (1T+ parametri, non portabili on-device) e privacy utente: delegare l'inference al vendor di modello (Google) ma eseguirla in ambiente fisicamente controllato dall'OS vendor (Apple). E' il segnale piu' concreto che il confidential cloud computing diventa prassi ingegneristica standard per l'inference AI nei contesti consumer. Google paga SpaceX $920M/mese ($30B totale, 8 fonti: TechCrunch, Bloomberg, CNBC, Yahoo Finance, Slashdot, cryptobriefing, PYMNTS, New Straits Times): l'economia dell'inference frontier e' talmente tesa che anche Google — $180-190B di capex nel 2026 — deve acquisire bridge compute da un concorrente per soddisfare la domanda di Gemini Enterprise. Il dato quantifica il valore di un singolo GPU cluster (110K GPU per $920M/mese): un'unita' di compute equivalente a quella affittata da Google genera piu' di $11 miliardi di ricavi annui da un singolo cliente. Anthropic raddoppia i limiti Claude Code (Anthropic official + 6 fonti): il deal SpaceX Colossus 1 (220K GPU, 300MW) porta la finestra di utilizzo di 5h al doppio e alza il rate limit API Opus da 30K a 500K token/minuto per Tier 1 (16x). L'aspetto inference e' la scarsita' come variabile operativa: la mossa risponde direttamente alla domanda degli utenti che scontravano blocchi peak-hour, e ogni raddoppio di limite equivale a un'espansione della capacita' di inference agentica disponibile per run complessi. [Digest 2026-06-08](../../digest/2026/06/08.md)

### 2026-06-06

ChatGPT Dreaming V3 (OpenAI, 4-5 giugno, 5 fonti) introduce un pattern rilevante per il concetto di inference: la sintesi di memoria e' un processo di inference asincrono persistente che gira in background indipendentemente dalla sessione attiva. Strutturalmente, Dreaming V3 e' un loop di inference continuo che processa lo storico delle conversazioni per aggiornare un representation compatta dello stato utente. La riduzione 5x del compute rispetto a V2 e' il fatto tecnico chiave: rende il deployment di questo loop di inference in background economicamente scalabile su centinaia di milioni di utenti Free. Il pattern e' architetturalmente diverso dall'inference standard (input -> output in una singola call): e' inference persistente, non sincrona con la sessione, su dati propri del sistema (le conversazioni passate). Il termine che OpenAI usa — "dreaming" — e' un riferimento esplicito ai sistemi biologici dove la consolidazione della memoria avviene off-line (durante il sonno). Come sistema di inference, Dreaming V3 aggiunge un terzo tier al continuum on-device / cloud standard: inference asincrona di sfondo per la manutenzione dello stato. [Digest 2026-06-06](../../digest/2026/06/06.md)
