---
name: Large Language Model
aliases: [LLM, modello linguistico di grandi dimensioni, foundation model]
categoria: architettura
created: 2026-04-28
last_updated: 2026-06-14
mentions_count: 17
---

# Large Language Model

## Cos'e

Un Large Language Model (LLM) e' un modello statistico di linguaggio basato su reti neurali profonde, addestrato su corpora testuali dell'ordine di centinaia di miliardi - migliaia di miliardi di token, con un numero di parametri che varia da qualche miliardo a oltre un trilione. L'obiettivo di addestramento canonico e' la previsione del token successivo: data una sequenza di simboli linguistici, il modello produce una distribuzione di probabilita' sul vocabolario per il token che verra' dopo. Questa formulazione apparentemente semplice, applicata su scala massiccia, fa emergere capacita' che non erano state programmate esplicitamente: traduzione, sintesi, ragionamento aritmetico elementare, generazione di codice, conversazione coerente.

La nascita degli LLM moderni si colloca tra il 2017 e il 2020. Il punto di svolta architetturale e' il paper "Attention Is All You Need" di Vaswani et al. (NeurIPS 2017), che introduce il transformer. Nel 2018 OpenAI pubblica GPT-1 (117 milioni di parametri), seguito da GPT-2 nel 2019 (1.5 miliardi). Google introduce BERT nel 2018, dimostrando l'efficacia del pre-training bidirezionale. Il salto di scala con GPT-3 nel 2020 (175 miliardi di parametri) rivela il fenomeno dell'in-context learning: il modello esegue compiti nuovi solo guardando esempi nel prompt, senza aggiornamento dei pesi. Da quel momento la classe dei "foundation model" (termine coniato dallo Stanford CRFM nel 2021) diventa il paradigma dominante della ricerca AI.

L'importanza degli LLM deriva da tre proprieta'. Sono general-purpose: la stessa rete e' usabile per task diversi cambiando solo il prompt. Sono economicamente leveraged: il costo di pre-training e' ammortizzato su milioni di applicazioni downstream. Sono compositi: si integrano con tool esterni, basi di conoscenza ([RAG](./rag.md)), agenti software ([agent](./agent.md)), formando sistemi piu' ampi. Per queste ragioni gli LLM sono diventati infrastruttura: cosi' come negli anni 2000 ogni applicazione web includeva un database relazionale, oggi una quota crescente di software include una chiamata a un LLM. Nel 2026 questa infrastruttura non e' piu' solo cloud: l'hardware consumer comincia a eseguire localmente modelli da decine di miliardi di parametri (vedi sezione Aggiornamenti, RTX Spark).

## Come funziona

Un LLM moderno e' un transformer decoder-only o encoder-decoder. Il flusso di calcolo a inference time, per un modello decoder-only generativo come la famiglia GPT o Llama, segue questi stadi.

Tokenizzazione. Il testo viene segmentato in token sub-word tramite [tokenization](./tokenization.md) BPE o SentencePiece. Un vocabolario tipico contiene 32k - 200k token. Ogni token e' mappato a un intero.

Embedding. Gli interi sono trasformati in vettori densi attraverso una matrice di [embedding](./embedding.md) `E` di dimensione `V x d`, dove `V` e' la cardinalita' del vocabolario e `d` la dimensione nascosta (es. 4096 in Llama 3 8B, 12288 in GPT-3 175B). A questi vettori si somma un'informazione posizionale: nei modelli moderni si usano rotary position embedding (RoPE) o ALiBi, che codificano la distanza relativa tra token. La gestione di questa informazione posizionale e' cio' che determina l'estensione massima del [context window](./context-window.md), salito nel 2026 a 1 milione di token nativi su diversi modelli frontier.

Stack di blocchi transformer. Una sequenza di N blocchi (N varia da 12 in modelli piccoli a 96-120 in modelli grandi) trasforma iterativamente le rappresentazioni. Ogni blocco ha due sottocomponenti: multi-head self-attention e feed-forward network (FFN). L'attention calcola, per ogni posizione i, una somma pesata dei valori delle altre posizioni, con pesi dati dal prodotto scalare query-key normalizzato softmax: `softmax(QK^T / sqrt(d_k)) V`. Il FFN e' una rete a due strati con attivazione GeLU o SwiGLU. Tra i sottocomponenti si applicano residual connection e layer normalization (RMSNorm nei modelli recenti).

Proiezione finale e softmax. L'ultima rappresentazione viene moltiplicata per la trasposta della matrice di embedding (weight tying) producendo un vettore di logit di dimensione V. Una softmax converte i logit in distribuzione di probabilita'.

Sampling. Per generare il token successivo si campiona dalla distribuzione: greedy (argmax), temperature sampling, top-k, top-p (nucleus). Il token campionato viene riaggiunto alla sequenza e il ciclo si ripete (autoregressivo). Questo stadio e' il cuore dell'[inference](./inference.md): la natura autoregressiva implica che il costo cresce linearmente con la lunghezza dell'output e che la latenza e' dominata dal tempo per token, motivo per cui l'ottimizzazione del serving (KV cache, batching, quantizzazione, hardware dedicato) e' diventata un mercato a se'.

Il training segue tre fasi. Pre-training: ottimizzazione della cross-entropy sul next-token prediction su un corpus massiccio (es. 15 trilioni di token per Llama 3). Si usa AdamW con learning rate cosine schedule, batch effettivi nell'ordine di milioni di token, parallelismo tensor + pipeline + data su migliaia di GPU. Supervised fine-tuning (SFT): adattamento su dataset di istruzione-risposta curati. [RLHF](./rlhf.md) o DPO: allineamento alle preferenze umane.

Le leggi di scaling (Kaplan 2020, Hoffmann 2022 "Chinchilla") quantificano la relazione tra parametri, dati e loss: a budget di compute fissato, l'allocazione ottimale prevede circa 20 token di training per parametro. Modelli "compute-optimal" come Chinchilla 70B hanno mostrato performance superiori a Gopher 280B con un quarto dei parametri. Una tendenza chiave del 2025-2026 e' lo spostamento del baricentro dell'investimento di compute dal pre-training al post-training: reinforcement learning su task verificabili, curriculum SFT, process reward model. Il caso SU-01 (vedi Aggiornamenti, 2026-05-15) dimostra che un modello da 30 miliardi di parametri puo' raggiungere il livello medaglia d'oro olimpico in matematica e fisica con la sola ricetta di post-training, senza un backbone frontier proprietario.

## Varianti / approcci

Le architetture dominanti si distinguono per la struttura del transformer e per la procedura di training.

| Famiglia | Esempio | Caratteristica |
|---|---|---|
| Decoder-only autoregressivo | GPT-5.5, Claude Opus 4.8, Llama, Gemini 3.5, Mistral | Generativo, causal mask, scaling massiccio |
| Encoder-only | BERT, RoBERTa, DeBERTa | Bidirezionale, ottimo per classificazione e retrieval |
| Encoder-decoder | T5, BART, Flan-T5 | Forte su task seq2seq classici (traduzione, sintesi) |
| Mixture of Experts | Mixtral 8x7B, DeepSeek-V3, Project Polaris (riportato) | FFN sparso, attiva un sottoinsieme di esperti per token |
| State space / linear attention | Mamba-3, RWKV, Gated DeltaNet-2 | Costo lineare in sequenza, alternativa al transformer |

I modelli [Mixture of Experts](./mixture-of-experts.md) permettono di disaccoppiare parametri totali da parametri attivi: Mixtral 8x7B ha 47 miliardi di parametri totali ma ne attiva ~13 miliardi per token, con throughput simile a un denso 13B. DeepSeek-V3 (671B totali, 37B attivi) e' un esempio di MoE su scala estrema. Nel giugno 2026 Microsoft pre-annuncia Project Polaris, un modello di code understanding e generation con architettura MoE in cui moduli specializzati coprono linguaggi e paradigmi distinti (vedi Aggiornamenti): un segnale che il pattern MoE viene adottato anche per la specializzazione verticale (coding), non solo per la scalabilita' del modello generalista.

La linea di ricerca su linear attention e state space model continua a maturare come alternativa al transformer per il problema del costo quadratico dell'attention. Gated DeltaNet-2 (NVLabs, maggio 2026) introduce gate separati e channel-wise per le operazioni di cancellazione e scrittura nella memoria ricorrente, battendo Mamba-2, Mamba-3 e il Gated DeltaNet originale su linguaggio, reasoning e retrieval a 1.3 miliardi di parametri. Il vantaggio e' piu' marcato sui benchmark needle-in-a-haystack a chiavi multiple, dove la dimensione fissa dello stato ricorrente penalizzava tradizionalmente i modelli lineari.

Lungo l'asse della specializzazione si distinguono modelli base (solo pre-training), instruct (con SFT), chat (con RLHF), reasoning (con catene di pensiero esplicite e RL su task verificabili, vedi o-series, DeepSeek R1, Claude con extended thinking), e modelli multimodali nativi (GPT-4o, Gemini 3.5, Claude 4) che trattano testo, immagini, audio, video in un unico spazio di rappresentazione. Gemini Omni Flash (maggio 2026) estende il concetto unificando reasoning testuale e generazione video in un singolo modello senza pipeline separata. Si affermano inoltre modelli verticali specializzati per dominio: GPT-Rosalind (life science, ragionamento su molecole, proteine, geni) e GPT-5.5-Cyber (cybersecurity) sono esempi di varianti derivate dalla stessa architettura base e distribuite via "trusted access" su domini ad alto rischio.

Sull'asse open vs closed: Llama (Meta), Mistral, Qwen (Alibaba), DeepSeek, Gemma (Google), Kimi (Moonshot AI) rilasciano pesi scaricabili; OpenAI, Anthropic, Google rilasciano modelli di punta solo via API. La differenza di qualita' tra frontier closed e migliori open si e' ridotta a 6-12 mesi nel 2025-2026. Un fenomeno emergente e' il post-training proprietario su pesi open: Cursor Composer 2.5 e' costruito sopra Kimi K2.5 ma dedica l'85% del budget di compute a reinforcement learning su task sintetici, raggiungendo parita' di benchmark coding con modelli frontier closed a circa un decimo del costo (vedi Aggiornamenti). Questo sposta la competizione dal modello base all'harness, al post-training specializzato e all'esperienza di prodotto.

## Quando usarlo / quando no

Un LLM e' la scelta giusta quando il problema e' espresso bene in linguaggio naturale, l'output e' testuale o strutturabile come testo (JSON, codice, query), e l'errore atteso e' tollerabile o verificabile a valle. Buoni use case: estrazione di informazioni da documenti non strutturati, classificazione zero/few-shot in domini in cui non si hanno dataset, generazione di bozze (email, codice boilerplate, draft di documenti), interfacce conversazionali, [tool use](./tool-use.md) come orchestratore, agenti che eseguono task complessi su sessioni lunghe (1000+ tool call).

Un LLM e' la scelta sbagliata quando esistono soluzioni deterministiche affidabili (parsing strutturato, regex, query SQL), quando serve precisione numerica esatta su input grandi (un foglio Excel con migliaia di righe va elaborato con codice, non chiesto al modello), quando il dominio richiede garanzie verificabili (sicurezza critica, calcoli legali con responsabilita'), o quando il costo unitario del token rende l'operazione antieconomica rispetto a un classificatore tradizionale.

Anti-pattern comuni. Usare l'LLM come database: i modelli hallucinano fatti specifici, vanno integrati con [RAG](./rag.md). Usare l'LLM per calcoli: anche modelli reasoning sbagliano l'aritmetica oltre certe soglie, meglio delegare a un tool ([tool use](./tool-use.md)). Affidarsi al modello per logica multi-step senza catene esplicite di verifica: la performance degrada non linearmente con la profondita' del ragionamento (vedi [chain-of-thought](./chain-of-thought.md)). Trattare il prompt come specifica eseguibile: il prompt e' una guida probabilistica, non un programma. Un anti-pattern emerso con la diffusione degli agenti e' valutare un modello solo su benchmark sintetici: TerminalWorld (maggio 2026), benchmark costruito da registrazioni terminale reali, mostra un pass rate massimo del 62,5% tra otto modelli frontier su workflow autentici, contro percentuali ben piu' alte sui task sintetici.

## Esempi pratici

Esempio 1: classificazione di ticket di supporto in zero-shot. Si fornisce al modello una lista di categorie e si chiede di assegnare il ticket. Confronto con un classificatore tradizionale: l'LLM funziona bene da subito senza dataset etichettato, ma costa di piu' per inferenza e ha latenza superiore. Soluzione ibrida: usare l'LLM per generare 5000 esempi etichettati, poi addestrare un modello piccolo (un encoder come MiniLM) per il deployment.

Esempio 2: chiamata API a un modello commerciale.

```python
from anthropic import Anthropic

client = Anthropic()
response = client.messages.create(
    model="claude-opus-4-8",
    max_tokens=1024,
    messages=[
        {"role": "user", "content": "Riassumi in 3 punti il paper 'Attention Is All You Need'."}
    ]
)
print(response.content[0].text)
```

Il flusso e': il SDK serializza il messaggio in JSON, lo invia all'endpoint HTTPS, il server esegue il forward pass, restituisce uno stream di token. Cost model tipico: tariffa per milione di token in input + tariffa per milione di token in output, con fattore 3-5x output/input. Alcuni provider offrono modalita' "fast" che aumentano il throughput a costo ridotto (Claude Opus 4.8 Fast Mode: 2.5x la velocita' standard a un terzo del costo) o tariffe ridotte sui token cached.

Esempio 3: estrazione strutturata. Si chiede al modello di restituire JSON conforme a uno schema (function calling, structured outputs). Il modello e' guidato durante la generazione tramite constrained decoding o grammar-based sampling, riducendo gli errori di formato a quasi zero.

Esempio 4: esecuzione locale. Con l'arrivo di hardware come Nvidia RTX Spark (128 GB di memoria unificata, giugno 2026), e' possibile caricare interamente in memoria un modello da 70B-120B parametri su un laptop consumer senza quantizzazione degradante, con context fino a 1 milione di token. Questo abilita pipeline agentiche locali in cui i dati non lasciano la macchina, rilevante per scenari con vincoli di privacy o compliance.

## Letture

- Vaswani et al., "Attention Is All You Need", NeurIPS 2017. https://arxiv.org/abs/1706.03762
- Brown et al., "Language Models are Few-Shot Learners" (GPT-3), NeurIPS 2020. https://arxiv.org/abs/2005.14165
- Hoffmann et al., "Training Compute-Optimal Large Language Models" (Chinchilla), 2022. https://arxiv.org/abs/2203.15556
- Kaplan et al., "Scaling Laws for Neural Language Models", 2020. https://arxiv.org/abs/2001.08361
- Bommasani et al., "On the Opportunities and Risks of Foundation Models", Stanford CRFM 2021. https://arxiv.org/abs/2108.07258
- Touvron et al., "Llama 2: Open Foundation and Fine-Tuned Chat Models", 2023. https://arxiv.org/abs/2307.09288
- Hatamizadeh et al., "Gated DeltaNet-2" (NVLabs), arXiv 2605.22791, maggio 2026. https://arxiv.org/abs/2605.22791
- Anthropic, "Claude documentation". https://docs.anthropic.com
- Hugging Face, "The Transformer Family v2". https://huggingface.co/blog/transformer-family

## Note operative

Scelta del modello. Nel 2026 l'ecosistema offre dozzine di opzioni viable. Criterio operativo: per ogni task, definire 3-5 esempi rappresentativi, testarli su 4-5 modelli candidati (frontier closed, frontier open, mid-tier closed, small open), confrontare qualita' percepita, latenza, costo. Spesso un Sonnet o GPT-5 mini risolve quanto Opus o GPT-5 al 20% del costo. Decidere a priori quale "tier" il task richiede e' meno efficace che misurare. Per task agentici, valutare anche l'orizzonte: modelli ottimizzati per sessioni lunghe (Qwen3.7-Max, Gemini 3.5 Flash) reggono migliaia di tool call meglio di modelli ottimizzati per singola inference.

Knowledge cutoff. Ogni LLM ha una data oltre la quale non ha visto eventi. Modelli frontier 2026 tipicamente hanno cutoff a ottobre-dicembre 2025 o successivo. Domande su eventi recenti vanno risolte con [RAG](./rag.md) o ricerca web tool, non con la memoria del modello. Ignorare il cutoff e' una causa comune di hallucination su fatti recenti.

Allucinazioni residue. Anche modelli ben allineati allucinano: invertire numeri, citare paper inesistenti, inventare API. I modelli recenti riducono il tasso (GPT-5.5 Instant registra il 52,5% di affermazioni allucinatorie in meno su prompt ad alta posta rispetto al predecessore) ma non lo azzerano. Mitigazioni: chiedere al modello di citare fonti verificabili (RAG), avere validation a valle (es. eseguire il codice generato, controllare URL), preferire structured output per dati critici. Una variante robusta della verifica e' il loop generatore-verificatore formale: AlphaProof Nexus (DeepMind, maggio 2026) usa Gemini come motore generativo e Lean come proof assistant che certifica ogni passo, ottenendo risultati matematicamente garantiti anziche' plausibili. Il livello accettabile di allucinazione dipende dal use case: in ricerca di marketing e' tollerabile, in informazioni mediche o legali no.

## Aggiornamenti

### 2026-05-06

OpenAI rilascia GPT-5.5 Instant come nuovo modello di default di ChatGPT, sostituendo GPT-5.3 Instant. Il modello registra il 52,5% di affermazioni allucinatorie in meno su prompt ad alta posta rispetto al predecessore e risposte il 30,2% piu' brevi. E' il primo modello default di ChatGPT a integrare la ricerca nelle conversazioni passate e nei file dell'utente per personalizzazione contestuale. La mossa consolida il trend emerso a fine aprile 2026 — GPT-5.5 originale il 23 aprile, GPT-5.5-Cyber il 30 aprile — verso varianti specializzate derivate dalla stessa architettura di base. [Digest 2026-05-06](../../digest/2026/05/06.md)

### 2026-05-11

Un paper su arXiv (2605.06241) riformula il ruolo del reinforcement learning nel training LLM per il reasoning: RL non insegna strategie nuove ai modelli, ma redistribuisce massa di probabilita' su un sottoinsieme sparso (1-3% delle posizioni token) in cui il modello base e' gia' incerto. Il token promosso cade sempre tra le prime 5 alternative del modello base. Traduzione pratica: gli autori introducono ReasonMaxxer, metodo RL-free che applica contrastive loss solo ai punti di decisione ad alta entropia, replicando le performance del full RL con circa tre ordini di grandezza meno compute. [Digest 2026-05-11](../../digest/2026/05/11.md)

### 2026-05-15

Due contributi distinti sull'estensione delle capacita' degli LLM. SU-01 (arXiv 2605.13301) dimostra che un modello 30B-A3B e' sufficiente per raggiungere il livello medaglia d'oro a IMO 2025, USAMO 2026 e IPhO 2024/2025: la ricetta e' curriculum SFT con reverse-perplexity su 340K traiettorie + RL a due stadi (verifiable reward poi proof-level RL) + test-time scaling. Il risultato principale e' metodologico: non serve un modello frontier proprietario o una modifica architetturale per raggiungere performance olimpica in matematica e fisica, basta una ricetta di addestramento sistematica applicata a un backbone competitivo gia' disponibile. uPRM (arXiv 2605.10158, EPFL) affronta il problema del training dei Process Reward Model: le annotazioni step-level da esperti umani sono il principale collo di bottiglia alla scalabilita' dei PRM, che sono lo strumento principale per guidare il ragionamento degli LLM step-by-step. uPRM elimina questa dipendenza usando la distribuzione next-token dell'LLM stesso come segnale di supervisione, identificando il primo step errato in un batch di traiettorie senza alcuna label esterna. I due paper si inseriscono in un filone convergente: la frontiera della capacita' degli LLM si sposta sempre piu' verso il post-training (RL, PRM, curriculum) piuttosto che verso la scala del pre-training. [Digest 2026-05-15](../../digest/2026/05/15.md)

### 2026-05-20

Google I/O 2026 porta due nuovi modelli frontier. Gemini 3.5 Flash e' il nuovo modello di riferimento Google per task agentici e multimodali: supera Gemini 3.1 Pro su Terminal-Bench 2.1 (76,2%), GDPval-AA (1656 Elo) e CharXiv Reasoning (84,2%) con 4x la velocita' dei modelli comparabili, context window da 1M token e prezzo $1,50/$9,00 per 1M token in input/output. La disponibilita' immediata via Gemini API (AI Studio, Android Studio) lo rende il primo modello Google pensato esplicitamente per pipeline agentiche in produzione. Gemini Omni Flash e' la prima architettura Google che unifica reasoning testuale e generazione video in un singolo modello, senza pipeline separata tra LLM e video model: accetta in input testo, immagini, audio e video e genera clip fino a 10 secondi con coerenza fisica e SynthID watermarking. Il precedente piu' vicino nell'ecosistema era GPT-4o con image output; Gemini Omni Flash estende il concetto al video. Sul piano architetturale, entrambi i modelli segnalano la direzione del 2026 nei frontier model Google: la specializzazione per agentic use case (velocita', costo, multimodalita') e' esplicitata nei benchmark ufficiali, non piu' ricavabile solo dai test indipendenti. [Digest 2026-05-20](../../digest/2026/05/20.md)

### 2026-05-23

Alibaba lancia Qwen3.7-Max al Cloud Summit di Hangzhou (20-21 maggio): modello flagship per l'era degli agenti con context window nativa da 1 milione di token, extended thinking mode e ottimizzazione nativa per i principali CLI agent framework. In termini architetturali, il modello affronta i task agentici con orizzonte lungo (1.000+ tool call, 35 ore di esecuzione autonoma in un test interno) in modo che i modelli frontier precedenti non documentavano in produzione. Contestualmente Alibaba presenta il chip Zhenwu M890 e afferma che Qwen3.7-Max e' stato usato per scrivere autonomamente il firmware ottimizzato del chip stesso, in un loop di validazione software-hardware integrato. Questa notizia si inserisce nella traiettoria degli ultimi mesi: dalla settimana scorsa (Gemini 3.5 Flash per agentic, Gemini Omni Flash come modello unificato testo-video) il 2026 registra un'accelerazione verso modelli progettati esplicitamente per sessioni agentiche lunghe, non solo per singole inference. [Digest 2026-05-23](../../digest/2026/05/23.md)

### 2026-05-29

Anthropic rilascia Claude Opus 4.8 (28 maggio), nuovo modello flagship con miglioramenti su coding, reasoning, financial analysis e knowledge work. Prezzo invariato rispetto a Opus 4.7. Fast Mode disponibile come opzione separata: 2.5x la velocita' standard a un terzo del costo. Disponibile su Claude.ai, API e GitHub Copilot (GA dalla stessa data). Anthropic conferma che i Mythos-class models — il livello di capacita' superiore, finora disponibile solo a partner di sicurezza selezionati tramite Project Glasswing — restano "in the coming weeks" senza data specifica. Il lancio consolida la cadenza di aggiornamento Anthropic nel 2026: Opus 4.7 a febbraio, Sonnet 4.6 ad aprile, Opus 4.8 a maggio — aggiornamenti del modello flagship ogni 2-3 mesi con prezzi stabili e miglioramenti incrementali di capability. [Digest 2026-05-29](../../digest/2026/05/29.md)

### 2026-06-01

Mese ricco di sviluppi convergenti su tre direttrici: specializzazione architetturale per il coding, post-training su pesi open, esecuzione locale di modelli grandi. Le novita' principali emerse nei digest di fine maggio e inizio giugno.

Coding model con MoE verticale. Microsoft pre-annuncia Project Polaris (embargo rilasciato prima del keynote Build 2026 del 2 giugno): modello di code understanding e generation con architettura mixture-of-experts in cui moduli specializzati coprono linguaggi e paradigmi distinti, destinato a GitHub Copilot con GA ad agosto 2026. Nelle misurazioni interne supera GPT-4 Turbo su HumanEval e MBPP, con vantaggio marcato su Rust e Haskell, e include una Code Content Guarantee che indemnizza i clienti da claim di proprieta' intellettuale sul codice generato. E' la prima riduzione strutturale della dipendenza di Microsoft da OpenAI per i prodotti developer. [Digest 2026-06-01](../../digest/2026/06/01.md)

Esecuzione locale di LLM 120B. Nvidia annuncia RTX Spark al Computex 2026 (1 giugno): primo SoC Arm proprietario per PC, con Grace CPU a 20 core, Blackwell GPU da 6144 CUDA core e 128 GB di memoria unificata LPDDR5X a 300 GB/s. La memoria unificata ad alta capacita' e' la discontinuita' tecnica: per la prima volta un laptop consumer puo' caricare interamente in memoria modelli da 70B-120B parametri senza quantizzazione degradante, con context fino a 1 milione di token per sessioni agentiche prolungate. Otto produttori hanno confermato dispositivi per l'autunno 2026. Sul fronte datacenter, Bloomberg riporta che Anthropic, OpenAI e SpaceX/xAI sono tra i primi utenti del Vera CPU Nvidia: i tre principali lab frontier convergono sulla stessa roadmap hardware. [Digest 2026-06-01](../../digest/2026/06/01.md)

Post-training proprietario su pesi open. Cursor rilascia Composer 2.5 sopra Kimi K2.5 (Moonshot AI), dedicando l'85% del budget di compute al post-training proprietario (RL su 25x piu' task sintetici del predecessore): 79,8% su SWE-Bench Multilingual contro l'80,5% di Claude Opus 4.7, a circa un decimo del costo. xAI lancia Grok Build 0.1, coding agent CLI con 8 sub-agenti paralleli e context 256k token (70,8% su SWE-Bench Verified). Il pattern: la competizione si sposta dal modello base all'harness, al post-training specializzato e all'esperienza di prodotto. [Digest 2026-05-25](../../digest/2026/05/25.md), [Digest 2026-05-26](../../digest/2026/05/26.md)

Architetture alternative al transformer. Gated DeltaNet-2 (NVLabs, arXiv 2605.22791) introduce gate separati e channel-wise per cancellazione e scrittura nella memoria ricorrente lineare, battendo Mamba-2, Mamba-3 e Gated DeltaNet a 1.3B parametri su linguaggio, reasoning e retrieval, con vantaggio marcato sui benchmark RULER a chiavi multiple. La linea state space / linear attention continua a presentarsi come alternativa al costo quadratico dell'attention. [Digest 2026-05-24](../../digest/2026/05/24.md)

Modelli verticali e capacita' di frontiera. Claude Mythos Preview (Project Glasswing) registra 93,9% su SWE-bench Verified, 82,0% su Terminal-Bench 2.0 e 97,6% su USAMO 2026, ma resta in accesso ristretto per ragioni di governance piu' che tecniche. OpenAI apre Rosalind Biodefense, programma di trusted access a GPT-Rosalind (modello life-science specializzato), consolidando il pattern dei modelli verticali derivati dalla stessa architettura base e distribuiti in modo controllato su domini ad alto rischio. AlphaProof Nexus (DeepMind, arXiv 2605.22763) combina Gemini 3.1 Pro con verifica formale Lean per risolvere 9 problemi aperti di Erdos: prima dimostrazione che un sistema basato su LLM contribuisce risultati originali alla matematica di ricerca, con verifica certificata anziche' plausibile. [Digest 2026-05-27](../../digest/2026/05/27.md), [Digest 2026-05-30](../../digest/2026/05/30.md), [Digest 2026-05-31](../../digest/2026/05/31.md)

Valutazione su task reali. TerminalWorld (arXiv 2605.22535) costruisce un benchmark agentico da 1530 task derivati da registrazioni terminale reali: il pass rate massimo tra otto modelli frontier e' 62,5%, contro percentuali ben piu' alte sui benchmark sintetici, evidenziando il gap tra prestazioni dichiarate e workflow autentici da developer. [Digest 2026-06-01](../../digest/2026/06/01.md)

### 2026-06-10

Claude Fable 5 e Mythos 5 (Anthropic, 9 giugno, 14+ fonti) marcano una discontinuita' nella roadmap dei modelli Anthropic. Fable 5 e' il primo modello della famiglia Fable reso pubblicamente disponibile: pricing a $10/$50 per milione di token input/output, accesso gratuito su tutti i piani fino al 22 giugno, disponibile su AWS Bedrock, Google Cloud Vertex, GitHub Copilot e Microsoft AI Foundry dall'9 giugno. Mythos 5 — stessa architettura di base con guardrail rimossi per partner cyber autorizzati — e' il primo modello Mythos-class ad essere reso pubblicamente disponibile, seppur in modalita' restricted. Il pattern e' rilevante per il concetto LLM come categoria: la distinzione Fable/Mythos codifica la scelta dei guardrail come prodotto, non come prerequisito — primo caso in cui un frontier lab commercializza esplicitamente due varianti dello stesso modello con politiche di sicurezza differenti. La disponibilita' multi-cloud (AWS, Google Cloud, GitHub, Microsoft) al lancio e' il nuovo standard di rilascio per i modelli frontier: non piu' accesso progressivo ma distribuzione simultanea su tutti i principali provider enterprise. [Digest 2026-06-10](../../digest/2026/06/10.md)

### 2026-06-14

Claude Fable 5 e Mythos 5 diventano il primo caso documentato di LLM soggetti a direttiva di export control. Il 13 giugno 2026, il Bureau of Industry and Security (BIS) del Dipartimento del Commercio USA ha ordinato ad Anthropic la sospensione immediata dell'accesso ai modelli per qualsiasi cittadino straniero — inclusi i dipendenti Anthropic con cittadinanza non statunitense. I modelli erano stati lanciati quattro giorni prima (9 giugno). L'ordine, basato sulle "national security authorities" dell'EAR, ha reso impossibile la conformita' selettiva per giurisdizione e ha costretto alla disabilitazione globale. Il precedente rilevante per il concetto LLM come categoria: per la prima volta un governo classifica un modello-software-come-servizio come tecnologia soggetta a export control, non solo l'hardware (chip) su cui gira. Anthropic ha rispettato l'ordine e contestualmente ha rilasciato una dichiarazione pubblica di disaccordo. Claude Opus 4.8 rimane il modello frontier Anthropic disponibile a livello globale. [Digest 2026-06-14](../../digest/2026/06/14.md)

### 2026-06-12

DiffusionGemma (Google, 10 giugno, 13+ fonti) arricchisce il panorama degli LLM open con la prima architettura di text diffusion da un lab frontier. Il modello e' distinto dagli LLM autoregressivi convenzionali: usa attention bidirezionale invece di causale e genera testo tramite denoising iterativo parallelo anziche' decodifica sequenziale. Il suo posizionamento nel landscape degli LLM open e' come alternativa di throughput (4x piu' veloce) con compromesso di qualita' (gap di 19 punti su AIME 2026 rispetto a Gemma 4 autoregressivo). OpenAI estende la distribuzione dei propri modelli frontier alla piattaforma Oracle OCI (10 giugno, 7 fonti): con questo accordo, tutti i principali hyperscaler cloud (AWS, Google Cloud Vertex, Azure, Oracle OCI) ospitano modelli frontier OpenAI, consolidando il pattern di distribuzione multi-cloud diventato standard di rilascio nel 2026. Il landscape degli LLM open a giugno 2026 include ora un nuovo paradigma architetturale (text diffusion) accanto a MoE sparse (MiniMax M3, Mixtral) e dense (LLaMA 4, Qwen3). [Digest 2026-06-12](../../digest/2026/06/12.md)
