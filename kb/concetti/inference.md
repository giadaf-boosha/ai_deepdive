---
name: Inference
aliases: [inference, inferenza, serving, generation, decoding]
categoria: infrastruttura
created: 2026-04-28
last_updated: 2026-04-28
mentions_count: 0
---

# Inference

## Cos'e

L'inference e' la fase di esecuzione di un modello addestrato, in cui dato un input si calcolano le predizioni. Per un [LLM](./llm.md) e' il processo di generazione token-per-token: ad ogni passo, dato il prefisso, il modello produce una distribuzione, si campiona un token, lo si aggiunge al prefisso, si ripete. L'inference si distingue dal training per due caratteristiche: non si calcolano gradienti (no backpropagation), e si ottimizza per latenza e throughput, non per accuratezza di gradiente.

L'inference su LLM e' diventata una disciplina ingegneristica autonoma tra il 2022 e il 2026. I costi a regime di un sistema AI sono dominati dall'inference (training si paga una volta, inference si paga per ogni richiesta). Aziende dedicate (Together, Fireworks, Groq, Cerebras, SambaNova) e progetti open (vLLM, TensorRT-LLM, llama.cpp, MLC, SGLang) competono su throughput, latenza, costo per milione di token.

L'importanza pratica di capire l'inference e' triplice. Per chi costruisce: sapere come scegliere modello e provider in base ai costi/SLA. Per chi opera: sapere come dimensionare GPU, batch size, quantizzazione. Per chi progetta prodotti: sapere quali UX sono economicamente sostenibili (es. streaming token in chat funziona, ma 100k token output per ogni utente non e' viabile).

## Come funziona

L'inference autoregressive ha due fasi tecnicamente distinte.

Prefill. Tutti i token dell'input (prompt + history) vengono processati in parallelo in un singolo forward pass. Si calcolano le rappresentazioni di tutti i token, e le K, V (key, value) per ogni layer vengono salvate nella KV cache. Il prefill e' compute-bound: scala con O(n^2) attention nel context size n, ma essendo parallelizzabile sulle GPU si esegue in centinaia di millisecondi anche su input lunghi.

Decode. Si genera un token alla volta in sequenza. Ogni step computa un singolo nuovo token: si calcolano Q, K, V per il nuovo token, l'attention sfrutta la KV cache (no ricalcolo), si applicano FFN, projection, softmax, sampling. Il decode e' memory-bound: l'overhead dominante e' leggere i pesi del modello (decine-centinaia di GB) dalla VRAM ad ogni step. Su una GPU H100 con un modello 70B in bfloat16, il throughput single-stream e' 30-80 token/s. Con batching e ottimizzazioni puo' superare 5000 token/s aggregati su molte query concorrenti.

KV cache. Memorizza key e value di tutti i token gia' processati per evitare di ricalcolarli. La sua dimensione e' `2 * num_layers * num_heads * head_dim * seq_len * dtype_size`. Per Llama 3 70B (80 layer, 64 heads, head_dim 128) con seq 4k in fp16: ~5 GB. La KV cache e' la fonte primaria del consumo memoria a runtime. Ottimizzazioni: GQA (Grouped Query Attention) e MQA condividono key/value tra heads, riducendo il KV. PagedAttention (vLLM) gestisce la KV cache come memoria virtuale paginata, eliminando frammentazione.

Sampling. Dato il vettore di logit, si campiona il token successivo. Strategie: greedy (argmax, deterministico), temperature scaling (`logits / T`), top-k (limita ai k token piu' probabili), top-p / nucleus (limita all'insieme la cui probabilita' cumulativa supera p), min-p, typical sampling, repetition penalty, beam search (esplora k sequenze in parallelo, raro per LLM moderni).

Speculative decoding (Leviathan et al. 2022, Chen et al. 2023). Un modello "draft" piccolo e veloce produce piu' token speculativi; il modello "target" grande li verifica in un singolo forward pass parallelo. Se la verifica conferma, si accettano molti token in un colpo. Speedup tipico 2-3x su workload generativi. Tecniche correlate: Medusa (head multiple), EAGLE (training congiunto draft-target).

Quantizzazione. Riduce la precisione dei pesi (e talvolta delle attivazioni) per ridurre memoria e aumentare throughput. Schemi: INT8 (peso 8-bit, qualita' quasi invariata), INT4 (peso 4-bit, perdita 1-3%), GPTQ, AWQ, GGUF (formato di llama.cpp), FP8 (Hopper, Blackwell). Un modello 70B in INT4 entra in una singola H100 80GB invece di richiederne due in fp16.

Batching e continuous batching. Servire piu' richieste insieme aumenta utilizzo GPU. Continuous batching (vLLM, TGI) inserisce nuove request nel batch durante il decoding, senza aspettare che una request finisca. Throughput aggregato cresce di 5-20x rispetto a batching naive.

Distillation. Trasferimento da modello grande a modello piccolo. Un Phi 3 mini di 3.8B parametri puo' avvicinare la qualita' di GPT-3.5 grazie a training su dati prodotti da modelli grandi.

Hardware. GPU NVIDIA dominanti (H100, H200, B100, B200). AMD MI300/MI325X, Google TPU v5p/v6, Trainium di AWS, acceleratori specializzati come Groq LPU (low-latency, throughput record per token-per-secondo single-stream), Cerebras WSE (memoria enorme, per modelli molto grandi single-chip).

Numeri. Tariffe medie per milione di token output, primavera 2026: frontier closed (Claude Opus 4, GPT-5) ~30-75 $/M; mid-tier (Sonnet, GPT-5 mini) ~5-15 $/M; small open su provider (Llama 3 70B su Together, Fireworks) ~0.5-2 $/M; self-hosted con quantizzazione e batching su H100: ~0.1-0.5 $/M. La differenza ordini di grandezza tra frontier e small fa scegliere i modelli in base al task.

## Varianti / approcci

| Strategia | Idea | Trade-off |
|---|---|---|
| Quantizzazione | Pesi a 8/4/2 bit | Memoria/speed vs qualita' |
| KV cache compression | INT8 KV, eviction selettiva | Context lungo a bassa memoria |
| Speculative decoding | Draft + verify | Latency reduction, complessita' |
| Continuous batching | Batch dinamico | Throughput, latenza per-request stabile |
| Tensor parallel | Pesi splittati su piu' GPU | Modelli grandi, comunicazione overhead |
| Pipeline parallel | Layer su GPU diverse | Modelli grandi, latenza |
| MoE inference | Solo expert selezionati | Throughput x denso simile, infra complessa |
| Long context optimization | Sliding window, chunked prefill | 1M+ context realistico |
| Compilation | TorchCompile, TensorRT | 10-30% speedup |
| Disaggregated serving | Prefill workers + decode workers separati | Scaling indipendente |

Sulle architetture alternative al transformer puro per inference economica: state space model (Mamba, RWKV) con costo lineare in sequenza, ibridi (Jamba di AI21, Striped Hyena), modelli MoE che attivano una frazione di parametri.

## Quando usarlo / quando no

Self-hosting dell'inference e' la scelta giusta quando: il volume e' alto (ROI sui costi fissi GPU); ci sono requisiti di privacy/compliance (dati che non possono uscire); serve latenza ultra-bassa con hardware dedicato; il workload e' prevedibile. API managed e' la scelta giusta quando: volume basso o burst (paghi solo l'usato); si vogliono modelli frontier non self-hostable; non si ha team SRE/MLOps; le SLA del provider bastano.

Anti-pattern. Self-hosting di un modello quando il volume mensile non copre il costo della GPU. Usare il modello frontier per task in cui un small model con [fine-tuning](./fine-tuning.md) basta. Ignorare il prompt caching: un'app che invia lo stesso system prompt di 10k token a ogni chiamata paga 10k token ogni volta invece di pagare 1k cached + delta. Non monitorare costo per request: i conti delle API LLM esplodono silenziosamente. Ignorare la latenza per UX: oltre 3 secondi senza streaming gli utenti percepiscono il sistema come rotto.

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

Llama 3 70B Q4_K_M sta in circa 40 GB; gira su MacBook M3 Max (96 GB) a 5-10 tok/s, su una H100 a 50-80 tok/s.

Esempio 3: scelta architetturale di un'app SaaS. 100k richieste/giorno, prompt medio 2k token, output medio 500. Con GPT-5 (es. 5 $/M input + 15 $/M output): ~ 2.0k$ + 0.75k$ = 2750 $/giorno. Con Claude Sonnet 4 a tariffe simili: stesso ordine. Con Llama 3.1 70B su Together (0.9 $/M): ~ 320 $/giorno. Decisione: usare il modello frontier solo per le query dove serve, routing su small model per > 70% dei casi (classificazione, estrazione, risposte semplici). Cost reduction tipica: 60-80%.

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

## Aggiornamenti

Nessun aggiornamento dopo la creazione (2026-04-28).
