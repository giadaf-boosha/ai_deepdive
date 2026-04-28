---
name: Context window
aliases: [context window, finestra di contesto, finestra contestuale, context length]
categoria: architettura
created: 2026-04-28
last_updated: 2026-04-28
mentions_count: 0
---

# Context window

## Cos'e

Il context window (o finestra di contesto) e' la quantita' massima di token che un [LLM](./llm.md) puo' considerare in un singolo passo di inferenza, sommando input (system prompt, messaggi precedenti, documenti, esempi few-shot) e output generato. Si esprime in token e definisce un confine fisico: il modello non puo' ragionare su informazioni oltre la finestra, perche' non sono nelle sue rappresentazioni di attention. La finestra include sia testo "passato" della conversazione sia testo "futuro" che il modello sta producendo.

I primi transformer (GPT-2, BERT) avevano finestre di 512-1024 token. GPT-3 nel 2020 saliva a 2048. La traiettoria 2022-2026 e' di crescita esponenziale: GPT-4 8k/32k (2023), Claude 2 100k (2023), GPT-4 Turbo 128k (2023), Claude 2.1 200k (2023), Gemini 1.5 1M con sperimentazioni a 10M (2024), Claude 3.5/4 con 200k-1M (2024-2026), Gemini 2 standard 2M (2025). L'estensione del context e' diventata feature competitiva centrale.

L'importanza pratica e' duplice. Determina quanto puoi inserire in una singola chiamata: documenti interi, codebase, transcript di riunioni, base di conoscenza piccole. E determina la complessita' computazionale: l'attention e' O(n^2) sulla lunghezza, quindi raddoppiare il contesto piu' che raddoppia costi e latenza, a meno di ottimizzazioni. La gestione del context window e' tema centrale per progettare prompt, [agent](./agent.md), pipeline [RAG](./rag.md), e [fine-tuning](./fine-tuning.md).

## Come funziona

Il limite del context viene definito a training time: si stabilisce una `max_position_embedding` o equivalente, e i positional encoding sono progettati per quella lunghezza. Il transformer applica la self-attention su una matrice n x n di score, dove n e' la lunghezza in token. Da qui derivano i due problemi cardinali: complessita' O(n^2) in tempo e memoria, e degradazione delle posizioni distanti.

Per estendere il context oltre il training nominale si usano diverse tecniche.

Position encoding migliorato. RoPE (Rotary Position Embedding, Su et al. 2021) codifica la posizione come rotazione complessa applicata a query e key, permettendo extrapolation oltre la lunghezza training tramite interpolation o YaRN scaling. ALiBi (Press et al. 2022) aggiunge bias lineari basati su distanza, naturalmente estensibili. NoPE elimina del tutto le encoding posizionali in alcune varianti.

Attention efficiente. FlashAttention (Dao et al. 2022) ricalcola l'attention in modo I/O-aware riducendo l'overhead memoria, abilitando training su context lunghi. Sliding window attention (Mistral): ogni token attende solo gli ultimi W token, rendendo l'attention O(nW). Sparse attention (Longformer, BigBird): pattern fissi di sparsita'. Linear attention / state space model (Mamba, RWKV): complessita' lineare in n, alternative al transformer.

KV cache. A inference time, durante la generazione, si memorizzano key e value di tutti i token gia' processati per non ricalcolarli. La KV cache e' la fonte principale del consumo memoria a runtime. Per Llama 3 70B con context 8k, la KV cache occupa diversi GB. Su context 1M la KV cache puo' superare la memoria di una H100. Tecniche di compressione (PagedAttention come in vLLM, KV cache quantization, MQA/GQA che condividono key e value tra heads) riducono il problema.

Long-context retrieval. Anche con finestra estesa, modelli reali mostrano "lost in the middle" (Liu et al. 2023): performance peggiora per informazioni a meta' del contesto. Le valutazioni "needle in a haystack" misurano la capacita' di recuperare un'informazione precisa inserita a posizioni casuali. I modelli frontier 2025-2026 raggiungono 95%+ di recall su 1M token; quelli precedenti calano al 60-70%.

Numeri. 1 token ~ 4 caratteri o ~0.75 parole inglesi (italiano simile). 1k token = ~750 parole = ~1.5 pagine. 100k token = un libro corto. 1M token = ~2000 pagine.

## Varianti / approcci

Modelli del 2025-2026 con i loro context window:

| Modello | Context window | Note |
|---|---|---|
| Claude Opus / Sonnet 4.x | 200k - 1M | 1M in beta o per Enterprise |
| GPT-5 / GPT-4o | 128k - 256k | Variabile per tier |
| Gemini 2 Pro | 2M | Standard, 10M sperimentale |
| Llama 3.1 / 3.3 | 128k | Open weights |
| Mistral Large 2 | 128k | |
| DeepSeek V3 | 128k | MoE open |
| Qwen 2.5 | 128k - 1M | Varianti |

Sull'asse di tecnica per estendere il context: training nativo (modello addestrato direttamente su sequenze lunghe), continued pre-training su long context (estendere un modello base), position interpolation (NTK-aware, YaRN), retrieval-augmented (delegare a [RAG](./rag.md) la selezione, mantenere context piccolo).

Contrasto context-vs-RAG. Long context vince quando il corpus e' < 1-2M token, la query richiede sintesi globale, la latenza piu' alta e' tollerata. RAG vince per corpora vasti, query puntuali, costi bassi per richiesta. Pattern ibrido: RAG per filtrare al milione di token poi long context per ragionare globalmente.

## Quando usarlo / quando no

Sfruttare un context grande e' la scelta giusta quando: si analizza un documento intero (contratto, paper, codebase) che entra nella finestra; si fa long-form generation (un report lungo che richiede coerenza globale); si fanno chat lunghe con storia rilevante; si fa few-shot con molti esempi. E' anche utile per debugging di codice complesso, dove vedere l'intero modulo aiuta.

Non bisogna sfruttarlo quando: il task richiede solo un frammento (un chunk RAG di 500 token basta); il costo per chiamata diventa proibitivo (256k token in input a tariffa LLM frontier sono molti dollari per richiesta); la latenza diventa intollerabile (un context da 1M token aggiunge secondi); il "lost in the middle" degrada la qualita'.

Anti-pattern. Riempire il context "per sicurezza" con tutto il possibile: piu' rumore peggiora le risposte. Ignorare il prompt caching: le finestre grandi sono economiche solo se il prefisso e' cached (Anthropic prompt caching, OpenAI prompt caching). Non gestire il contesto di un agent: in [agent](./agent.md) lunghi la storia cresce, va periodicamente riassunta (compaction) altrimenti il context esplode. Confondere context window e knowledge cutoff: la finestra e' "quanto puoi mostrare al modello in una chiamata", non "quanto sa".

## Esempi pratici

Esempio 1: analisi di documento lungo. Si carica un PDF di 200 pagine (~80k token). Si chiede al modello di sintetizzare i 5 punti chiave e identificare contraddizioni. Senza long context bisognerebbe spezzare in chunk, riassumere ognuno, poi sintetizzare i riassunti (pipeline map-reduce). Con un context da 200k il task e' single-shot, qualita' superiore perche' il modello vede tutto contemporaneamente.

Esempio 2: prompt caching. Anthropic e OpenAI consentono di marcare prefissi del prompt come cache-able. Una applicazione che invia la stessa codebase di 100k token a ogni domanda paga il prezzo pieno solo la prima volta; le richieste successive (entro 5 minuti per Anthropic standard) hanno costo input ridotto del 90%. Sfruttare il caching e' essenziale per workflow long-context economicamente sostenibili.

Esempio 3: gestione context in agente. Un agente coding che lavora 30 step accumula history. A 100k token il prompt diventa pesante. Tecnica: ogni 20 step l'agent invoca una "summarize_history" che condensa gli step vecchi in un sommario di 2k token, mantenendo dettagli solo per gli ultimi 5. Il context resta gestibile, le metriche di task completion non peggiorano in modo significativo.

## Letture

- Vaswani et al., "Attention Is All You Need", 2017. https://arxiv.org/abs/1706.03762
- Su et al., "RoFormer: Enhanced Transformer with Rotary Position Embedding", 2021. https://arxiv.org/abs/2104.09864
- Press et al., "Train Short, Test Long: Attention with Linear Biases" (ALiBi), 2022. https://arxiv.org/abs/2108.12409
- Dao et al., "FlashAttention: Fast and Memory-Efficient Exact Attention", 2022. https://arxiv.org/abs/2205.14135
- Liu et al., "Lost in the Middle: How Language Models Use Long Contexts", 2023. https://arxiv.org/abs/2307.03172
- Peng et al., "YaRN: Efficient Context Window Extension of Large Language Models", 2023. https://arxiv.org/abs/2309.00071
- Gemini 1.5 Technical Report, Google DeepMind 2024. https://arxiv.org/abs/2403.05530
- Anthropic, "Prompt caching documentation". https://docs.anthropic.com/en/docs/build-with-claude/prompt-caching

## Note operative

Misurare il context realmente usato. Spesso si riempie il prompt senza misurare. Strumenti come tiktoken (OpenAI) o gli SDK Anthropic permettono di contare i token prima di inviare la richiesta. Una buona pratica e' loggare per ogni chiamata `input_tokens`, `output_tokens`, `cache_read_tokens`, `cache_write_tokens`. Sopra l'80% del context window dichiarato la qualita' degrada e i costi diventano sproporzionati: meglio progettare l'app perche' resti sotto questa soglia.

Lost in the middle. Quando si comporre un prompt con piu' chunk recuperati via [RAG](./rag.md), l'ordine importa. Mettere i chunk piu' rilevanti all'inizio o alla fine del contesto, non al centro, migliora la performance. Per query agentiche, ridurre la verbosita' dei tool result (es. troncare output di file > 5k token, paginare elenchi lunghi) preserva attenzione del modello.

Caching budget. Anthropic permette fino a 4 cache breakpoint per richiesta. La granularita' importa: mettere un breakpoint dopo il system prompt e uno dopo i documenti immutabili massimizza il riuso. Cambiare anche un solo carattere prima del breakpoint invalida la cache. Per workflow ad alta variabilita', conviene strutturare il prompt come "stable prefix + variabile suffix", non mescolare.

Pattern di compaction. Per agenti long-running serve una strategia di riassunto. Schema tipico: ogni N step l'agent invoca un sub-task "riassumi gli ultimi M step in massimo K token", il riassunto sostituisce gli step originali nella history. Si tengono integri solo gli ultimi 2-3 step. La storia completa viene archiviata fuori-context su disco o database, recuperabile su richiesta esplicita.

## Aggiornamenti

Nessun aggiornamento dopo la creazione (2026-04-28).
