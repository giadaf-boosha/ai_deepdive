---
name: Large Language Model
aliases: [LLM, modello linguistico di grandi dimensioni, foundation model]
categoria: architettura
created: 2026-04-28
last_updated: 2026-05-23
mentions_count: 7
---

# Large Language Model

## Cos'e

Un Large Language Model (LLM) e' un modello statistico di linguaggio basato su reti neurali profonde, addestrato su corpora testuali dell'ordine di centinaia di miliardi - migliaia di miliardi di token, con un numero di parametri che varia da qualche miliardo a oltre un trilione. L'obiettivo di addestramento canonico e' la previsione del token successivo: data una sequenza di simboli linguistici, il modello produce una distribuzione di probabilita' sul vocabolario per il token che verra' dopo. Questa formulazione apparentemente semplice, applicata su scala massiccia, fa emergere capacita' che non erano state programmate esplicitamente: traduzione, sintesi, ragionamento aritmetico elementare, generazione di codice, conversazione coerente.

La nascita degli LLM moderni si colloca tra il 2017 e il 2020. Il punto di svolta architetturale e' il paper "Attention Is All You Need" di Vaswani et al. (NeurIPS 2017), che introduce il [transformer](./context-window.md). Nel 2018 OpenAI pubblica GPT-1 (117 milioni di parametri), seguito da GPT-2 nel 2019 (1.5 miliardi). Google introduce BERT nel 2018, dimostrando l'efficacia del pre-training bidirezionale. Il salto di scala con GPT-3 nel 2020 (175 miliardi di parametri) rivela il fenomeno dell'in-context learning: il modello esegue compiti nuovi solo guardando esempi nel prompt, senza aggiornamento dei pesi. Da quel momento la classe dei "foundation model" (termine coniato dallo Stanford CRFM nel 2021) diventa il paradigma dominante della ricerca AI.

L'importanza degli LLM deriva da tre proprieta'. Sono general-purpose: la stessa rete e' usabile per task diversi cambiando solo il prompt. Sono economicamente leveraged: il costo di pre-training e' ammortizzato su milioni di applicazioni downstream. Sono compositi: si integrano con tool esterni, basi di conoscenza ([RAG](./rag.md)), agenti software ([agent](./agent.md)), formando sistemi piu' ampi. Per queste ragioni gli LLM sono diventati infrastruttura: cosi' come negli anni 2000 ogni applicazione web includeva un database relazionale, oggi una quota crescente di software include una chiamata a un LLM.

## Come funziona

Un LLM moderno e' un transformer decoder-only o encoder-decoder. Il flusso di calcolo a inference time, per un modello decoder-only generativo come la famiglia GPT o Llama, segue questi stadi.

Tokenizzazione. Il testo viene segmentato in token sub-word tramite [tokenization](./tokenization.md) BPE o SentencePiece. Un vocabolario tipico contiene 32k - 200k token. Ogni token e' mappato a un intero.

Embedding. Gli interi sono trasformati in vettori densi attraverso una matrice di [embedding](./embedding.md) `E` di dimensione `V x d`, dove `V` e' la cardinalita' del vocabolario e `d` la dimensione nascosta (es. 4096 in Llama 3 8B, 12288 in GPT-3 175B). A questi vettori si somma un'informazione posizionale: nei modelli moderni si usano rotary position embedding (RoPE) o ALiBi, che codificano la distanza relativa tra token.

Stack di blocchi transformer. Una sequenza di N blocchi (N varia da 12 in modelli piccoli a 96-120 in modelli grandi) trasforma iterativamente le rappresentazioni. Ogni blocco ha due sottocomponenti: multi-head self-attention e feed-forward network (FFN). L'attention calcola, per ogni posizione i, una somma pesata dei valori delle altre posizioni, con pesi dati dal prodotto scalare query-key normalizzato softmax: `softmax(QK^T / sqrt(d_k)) V`. Il FFN e' una rete a due strati con attivazione GeLU o SwiGLU. Tra i sottocomponenti si applicano residual connection e layer normalization (RMSNorm nei modelli recenti).

Proiezione finale e softmax. L'ultima rappresentazione viene moltiplicata per la trasposta della matrice di embedding (weight tying) producendo un vettore di logit di dimensione V. Una softmax converte i logit in distribuzione di probabilita'.

Sampling. Per generare il token successivo si campiona dalla distribuzione: greedy (argmax), temperature sampling, top-k, top-p (nucleus). Il token campionato viene riaggiunto alla sequenza e il ciclo si ripete (autoregressivo).

Il training segue tre fasi. Pre-training: ottimizzazione della cross-entropy sul next-token prediction su un corpus massiccio (es. 15 trilioni di token per Llama 3). Si usa AdamW con learning rate cosine schedule, batch effettivi nell'ordine di milioni di token, parallelismo tensor + pipeline + data su migliaia di GPU. Supervised fine-tuning (SFT): adattamento su dataset di istruzione-risposta curati. [RLHF](./rlhf.md) o DPO: allineamento alle preferenze umane.

Le leggi di scaling (Kaplan 2020, Hoffmann 2022 "Chinchilla") quantificano la relazione tra parametri, dati e loss: a budget di compute fissato, l'allocazione ottimale prevede circa 20 token di training per parametro. Modelli "compute-optimal" come Chinchilla 70B hanno mostrato performance superiori a Gopher 280B con un quarto dei parametri.

## Varianti / approcci

Le architetture dominanti si distinguono per la struttura del transformer e per la procedura di training.

| Famiglia | Esempio | Caratteristica |
|---|---|---|
| Decoder-only autoregressivo | GPT-4, Claude, Llama, Gemini, Mistral | Generativo, causal mask, scaling massiccio |
| Encoder-only | BERT, RoBERTa, DeBERTa | Bidirezionale, ottimo per classificazione e retrieval |
| Encoder-decoder | T5, BART, Flan-T5 | Forte su task seq2seq classici (traduzione, sintesi) |
| Mixture of Experts | Mixtral 8x7B, GPT-4 (riportato), DeepSeek-V3 | FFN sparso, attiva un sottoinsieme di esperti per token |
| State space / linear attention | Mamba, RWKV | Costo lineare in sequenza, alternativa al transformer |

I modelli MoE permettono di disaccoppiare parametri totali da parametri attivi: Mixtral 8x7B ha 47 miliardi di parametri totali ma ne attiva ~13 miliardi per token, con throughput simile a un denso 13B. DeepSeek-V3 (671B totali, 37B attivi) e' un esempio recente di MoE su scala estrema.

Lungo l'asse della specializzazione si distinguono modelli base (solo pre-training), instruct (con SFT), chat (con RLHF), reasoning (con catene di pensiero esplicite e RL su task verificabili, vedi o1, o3, DeepSeek R1, Claude con extended thinking), e modelli multimodali nativi (GPT-4o, Gemini 2, Claude 4) che trattano testo, immagini, audio, video in un unico spazio di rappresentazione.

Sull'asse open vs closed: Llama (Meta), Mistral, Qwen (Alibaba), DeepSeek, Gemma (Google) rilasciano pesi scaricabili; OpenAI, Anthropic, Google rilasciano modelli di punta solo via API. La differenza di qualita' tra frontier closed e migliori open si e' ridotta a 6-12 mesi nel 2025-2026.

## Quando usarlo / quando no

Un LLM e' la scelta giusta quando il problema e' espresso bene in linguaggio naturale, l'output e' testuale o strutturabile come testo (JSON, codice, query), e l'errore atteso e' tollerabile o verificabile a valle. Buoni use case: estrazione di informazioni da documenti non strutturati, classificazione zero/few-shot in domini in cui non si hanno dataset, generazione di bozze (email, codice boilerplate, draft di documenti), interfacce conversazionali, [tool use](./tool-use.md) come orchestratore.

Un LLM e' la scelta sbagliata quando esistono soluzioni deterministiche affidabili (parsing strutturato, regex, query SQL), quando serve precisione numerica esatta su input grandi (un foglio Excel con migliaia di righe va elaborato con codice, non chiesto al modello), quando il dominio richiede garanzie verificabili (sicurezza critica, calcoli legali con responsabilita'), o quando il costo unitario del token rende l'operazione antieconomica rispetto a un classificatore tradizionale.

Anti-pattern comuni. Usare l'LLM come database: i modelli hallucinano fatti specifici, vanno integrati con [RAG](./rag.md). Usare l'LLM per calcoli: anche modelli reasoning sbagliano l'aritmetica oltre certe soglie, meglio delegare a un tool ([tool use](./tool-use.md)). Affidarsi al modello per logica multi-step senza catene esplicite di verifica: la performance degrada non linearmente con la profondita' del ragionamento. Trattare il prompt come specifica eseguibile: il prompt e' una guida probabilistica, non un programma.

## Esempi pratici

Esempio 1: classificazione di ticket di supporto in zero-shot. Si fornisce al modello una lista di categorie e si chiede di assegnare il ticket. Confronto con un classificatore tradizionale: l'LLM funziona bene da subito senza dataset etichettato, ma costa di piu' per inferenza e ha latenza superiore. Soluzione ibrida: usare l'LLM per generare 5000 esempi etichettati, poi addestrare un modello piccolo (un encoder come MiniLM) per il deployment.

Esempio 2: chiamata API a un modello commerciale.

```python
from anthropic import Anthropic

client = Anthropic()
response = client.messages.create(
    model="claude-opus-4-5",
    max_tokens=1024,
    messages=[
        {"role": "user", "content": "Riassumi in 3 punti il paper 'Attention Is All You Need'."}
    ]
)
print(response.content[0].text)
```

Il flusso e': il SDK serializza il messaggio in JSON, lo invia all'endpoint HTTPS, il server esegue il forward pass, restituisce uno stream di token. Cost model tipico: tariffa per milione di token in input + tariffa per milione di token in output, con fattore 3-5x output/input.

Esempio 3: estrazione strutturata. Si chiede al modello di restituire JSON conforme a uno schema (function calling, structured outputs). Il modello e' guidato durante la generazione tramite constrained decoding o grammar-based sampling, riducendo gli errori di formato a quasi zero.

## Letture

- Vaswani et al., "Attention Is All You Need", NeurIPS 2017. https://arxiv.org/abs/1706.03762
- Brown et al., "Language Models are Few-Shot Learners" (GPT-3), NeurIPS 2020. https://arxiv.org/abs/2005.14165
- Hoffmann et al., "Training Compute-Optimal Large Language Models" (Chinchilla), 2022. https://arxiv.org/abs/2203.15556
- Kaplan et al., "Scaling Laws for Neural Language Models", 2020. https://arxiv.org/abs/2001.08361
- Bommasani et al., "On the Opportunities and Risks of Foundation Models", Stanford CRFM 2021. https://arxiv.org/abs/2108.07258
- Touvron et al., "Llama 2: Open Foundation and Fine-Tuned Chat Models", 2023. https://arxiv.org/abs/2307.09288
- Anthropic, "Claude documentation". https://docs.anthropic.com
- Hugging Face, "The Transformer Family v2". https://huggingface.co/blog/transformer-family

## Note operative

Scelta del modello. Nel 2026 l'ecosistema offre dozzine di opzioni viable. Criterio operativo: per ogni task, definire 3-5 esempi rappresentativi, testarli su 4-5 modelli candidati (frontier closed, frontier open, mid-tier closed, small open), confrontare qualita' percepita, latenza, costo. Spesso un Sonnet o GPT-5 mini risolve quanto Opus o GPT-5 al 20% del costo. Decidere a priori quale "tier" il task richiede e' meno efficace che misurare.

Knowledge cutoff. Ogni LLM ha una data oltre la quale non ha visto eventi. Modelli frontier 2026 tipicamente hanno cutoff a ottobre-dicembre 2025. Domande su eventi recenti vanno risolte con [RAG](./rag.md) o ricerca web tool, non con la memoria del modello. Ignorare il cutoff e' una causa comune di hallucination su fatti recenti.

Allucinazioni residue. Anche modelli ben allineati allucinano: invertire numeri, citare paper inesistenti, inventare API. Mitigazioni: chiedere al modello di citare fonti verificabili (RAG), avere validation a valle (es. eseguire il codice generato, controllare URL), preferire structured output per dati critici. Il livello accettabile di allucinazione dipende dal use case: in ricerca di marketing e' tollerabile, in informazioni mediche o legali no.

## Aggiornamenti

### 2026-05-20

Google I/O 2026 porta due nuovi modelli frontier. Gemini 3.5 Flash e' il nuovo modello di riferimento Google per task agentici e multimodali: supera Gemini 3.1 Pro su Terminal-Bench 2.1 (76,2%), GDPval-AA (1656 Elo) e CharXiv Reasoning (84,2%) con 4x la velocita' dei modelli comparabili, context window da 1M token e prezzo $1,50/$9,00 per 1M token in input/output. La disponibilita' immediata via Gemini API (AI Studio, Android Studio) lo rende il primo modello Google pensato esplicitamente per pipeline agentiche in produzione. Gemini Omni Flash e' la prima architettura Google che unifica reasoning testuale e generazione video in un singolo modello, senza pipeline separata tra LLM e video model: accetta in input testo, immagini, audio e video e genera clip fino a 10 secondi con coerenza fisica e SynthID watermarking. Il precedente piu' vicino nell'ecosistema era GPT-4o con image output; Gemini Omni Flash estende il concetto al video. Sul piano architetturale, entrambi i modelli segnalano la direzione del 2026 nei frontier model Google: la specializzazione per agentic use case (velocita', costo, multimodalita') e' esplicitata nei benchmark ufficiali, non piu' ricavabile solo dai test indipendenti. [Digest 2026-05-20](../../digest/2026/05/20.md)

### 2026-05-15

Due contributi distinti sull'estensione delle capacita' degli LLM. SU-01 (arXiv 2605.13301) dimostra che un modello 30B-A3B e' sufficiente per raggiungere il livello medaglia d'oro a IMO 2025, USAMO 2026 e IPhO 2024/2025: la ricetta e' curriculum SFT con reverse-perplexity su 340K traiettorie + RL a due stadi (verifiable reward poi proof-level RL) + test-time scaling. Il risultato principale e' metodologico: non serve un modello frontier proprietario o una modifica architetturale per raggiungere performance olimpica in matematica e fisica, basta una ricetta di addestramento sistematica applicata a un backbone competitivo gia' disponibile. uPRM (arXiv 2605.10158, EPFL) affronta il problema del training dei Process Reward Model: le annotazioni step-level da esperti umani sono il principale collo di bottiglia alla scalabilita' dei PRM, che sono lo strumento principale per guidare il ragionamento degli LLM step-by-step. uPRM elimina questa dipendenza usando la distribuzione next-token dell'LLM stesso come segnale di supervisione, identificando il primo step errato in un batch di traiettorie senza alcuna label esterna. I due paper si inseriscono in un filone convergente: la frontiera della capacita' degli LLM si sposta sempre piu' verso il post-training (RL, PRM, curriculum) piuttosto che verso la scala del pre-training. [Digest 2026-05-15](../../digest/2026/05/15.md)

### 2026-05-11

Un paper su arXiv (2605.06241) riformula il ruolo del reinforcement learning nel training LLM per il reasoning: RL non insegna strategie nuove ai modelli, ma redistribuisce massa di probabilita' su un sottoinsieme sparso (1-3% delle posizioni token) in cui il modello base e' gia' incerto. Il token promosso cade sempre tra le prime 5 alternative del modello base. Traduzione pratica: gli autori introducono ReasonMaxxer, metodo RL-free che applica contrastive loss solo ai punti di decisione ad alta entropia, replicando le performance del full RL con circa tre ordini di grandezza meno compute. [Digest 2026-05-11](../../digest/2026/05/11.md)

### 2026-05-06

OpenAI rilascia GPT-5.5 Instant come nuovo modello di default di ChatGPT, sostituendo GPT-5.3 Instant. Il modello registra il 52,5% di affermazioni allucinatorie in meno su prompt ad alta posta rispetto al predecessore e risposte il 30,2% piu' brevi. E' il primo modello default di ChatGPT a integrare la ricerca nelle conversazioni passate e nei file dell'utente per personalizzazione contestuale. La mossa consolida il trend emerso a fine aprile 2026 — GPT-5.5 originale il 23 aprile, GPT-5.5-Cyber il 30 aprile — verso varianti specializzate derivate dalla stessa architettura di base. [Digest 2026-05-06](../../digest/2026/05/06.md)

### 2026-05-23

Alibaba lancia Qwen3.7-Max al Cloud Summit di Hangzhou (20-21 maggio): modello flagship per l'era degli agenti con context window nativa da 1 milione di token, extended thinking mode e ottimizzazione nativa per i principali CLI agent framework. In termini architetturali, il modello affronta i task agentici con orizzonte lungo (1.000+ tool call, 35 ore di esecuzione autonoma in un test interno) in modo che i modelli frontier precedenti non documentavano in produzione. Contestualmente Alibaba presenta il chip Zhenwu M890 e afferma che Qwen3.7-Max e' stato usato per scrivere autonomamente il firmware ottimizzato del chip stesso, in un loop di validazione software-hardware integrato. Questa notizia si inserisce nella traiettoria degli ultimi mesi: dalla settimana scorsa (Gemini 3.5 Flash per agentic, Gemini Omni Flash come modello unificato testo-video) il 2026 registra un'accelerazione verso modelli progettati esplicitamente per sessioni agentiche lunghe, non solo per singole inference. [Digest 2026-05-23](../../digest/2026/05/23.md)
