---
name: Mixture of Experts
aliases: [MoE, mixture-of-experts, mixture of experts, modello sparso, sparse model, expert routing]
categoria: architettura
created: 2026-06-01
last_updated: 2026-07-05
---

# Mixture of Experts

## Cos'e

Mixture of Experts (MoE) e' un'architettura di rete neurale in cui, invece di far passare ogni token attraverso tutti i parametri del modello, un router seleziona dinamicamente un piccolo sottoinsieme di sotto-reti specializzate — gli "expert" — da attivare per quel token. Il modello ha quindi un numero di parametri totali molto grande (la capacita' di memorizzazione e di specializzazione), ma un numero di parametri attivi molto piu' piccolo (il costo di calcolo per token). E' la principale tecnica usata nel 2026 per disaccoppiare la capacita' di un [LLM](./llm.md) dal suo costo di [inference](./inference.md).

L'idea ha radici lontane (Jacobs et al., 1991; il Sparsely-Gated MoE di Shazeer et al., 2017; Switch Transformer di Google, 2021), ma e' diventata lo standard de facto dei modelli frontier perche' risolve un problema economico preciso: per migliorare un modello denso bisogna aumentare i parametri, e il costo di inferenza cresce con essi. Con MoE si possono aggiungere expert — quindi capacita' — senza aumentare in proporzione il costo per token, perche' ogni token ne attiva solo alcuni.

Nei digest di maggio-giugno 2026 il MoE ricorre trasversalmente. TML-Interaction-Small di Thinking Machines Lab e' un MoE da 276 miliardi di parametri totali con 12 miliardi attivi. IBM Granite 4.0 includeva un 32B Mixture-of-Experts, superato da un 8B denso della generazione successiva — un dato istruttivo sui trade-off. LLaDA2.0-Uni usa un backbone MoE con masked diffusion per unificare comprensione e generazione multimodale. Microsoft pre-annuncia Project Polaris, modello di coding con architettura MoE in cui moduli specializzati coprono linguaggi e paradigmi distinti. La notazione "276B-A12B" o "30B-A3B" (parametri totali - parametri attivi) e' ormai standard nelle model card.

## Come funziona

Un layer MoE sostituisce il blocco feed-forward (MLP) di un transformer con N expert paralleli, piu' un router (gating network) che decide quali expert attivare per ciascun token.

Routing. Per ogni token, il router calcola un punteggio su tutti gli expert (tipicamente un piccolo layer lineare seguito da softmax) e seleziona i top-k (spesso k=1 o k=2). Solo gli expert selezionati elaborano il token; gli altri restano inattivi per quel token. L'output e' la somma pesata degli output degli expert attivi, con i pesi dati dal gating.

Sparsita'. La proprieta' chiave e' che il calcolo e' sparso: con 256 expert e top-2 routing, ogni token attiva 2/256 della capacita' del layer. Da qui la distinzione tra parametri totali (tutti gli expert, che occupano memoria) e parametri attivi (solo i k selezionati, che determinano i FLOP per token). Un MoE 276B-A12B occupa la memoria di un 276B ma costa, in compute, quanto un denso da ~12B.

Load balancing. Senza vincoli, il router tende a sovraccaricare pochi expert popolari lasciandone altri inutilizzati (expert collapse). Per evitarlo si aggiunge una auxiliary load-balancing loss che incentiva una distribuzione uniforme dei token tra gli expert, oppure si impone una capacita' massima per expert (token in eccesso vengono droppati o instradati altrove). Il bilanciamento e' una delle parti piu' delicate del training MoE.

Implicazioni di sistema. La memoria e' il vincolo dominante: tutti gli expert vanno tenuti in VRAM anche se per ogni token se ne usano pochi. Questo spinge verso il model parallelism (expert distribuiti su piu' GPU) e introduce comunicazione all-to-all tra device a ogni layer MoE — un costo di rete che a volte erode i guadagni di compute. La [tokenization](./tokenization.md) e il batching influenzano l'efficienza: token diversi nello stesso batch possono andare a expert diversi, complicando l'esecuzione efficiente.

Relazione con la quantizzazione. MoE e quantizzazione sono ortogonali e si combinano: un MoE puo' essere quantizzato (es. AWQ a 4 bit, tecnica al centro dell'acquisizione di Eigen AI da parte di Nebius) per ridurre l'impronta di memoria dei suoi molti expert. Il paper SOL ("Compute Where it Counts") mostra anche un asse adiacente: allocare dinamicamente il budget di compute per token, complementare al routing tra expert.

## Varianti / approcci

| Variante | Idea | Caratteristica |
|---|---|---|
| Sparsely-Gated MoE | Top-k routing classico (Shazeer 2017) | Base di tutte le varianti |
| Switch Transformer | top-1 routing, un solo expert per token | Massima sparsita', training semplificato |
| Fine-grained MoE | molti expert piccoli + shared expert | Granularita' fine, usato dai modelli recenti |
| MoE su diffusion backbone | expert dentro un masked diffusion LM | LLaDA2.0-Uni, multimodale |
| MoE per dominio | expert mappati a linguaggi/paradigmi | Project Polaris (coding) |
| Adaptive per-token compute | budget variabile oltre il routing | SOL, complementare al MoE |

Dense vs MoE. Un modello denso attiva tutti i parametri per ogni token: piu' semplice da addestrare, da quantizzare e da servire, ma il costo cresce con la capacita'. Un MoE separa capacita' e costo, ma e' piu' complesso (load balancing, comunicazione all-to-all, footprint di memoria). Il caso Granite 4.1 e' emblematico: un 8B denso che batte un 32B MoE della generazione precedente mostra che il MoE non e' sempre vincente — un modello denso ben addestrato puo' superare un MoE piu' grande, con il vantaggio aggiunto di essere piu' facile da [fine-tuning](./fine-tuning.md) in ambienti vincolati.

Granularita' degli expert. Pochi expert grandi vs molti expert piccoli e' un asse di design. La tendenza recente e' verso expert fine-grained (molti expert piccoli) piu' eventuali shared expert sempre attivi, che catturano la conoscenza comune mentre gli expert specializzati gestiscono i pattern di nicchia.

## Quando usarlo / quando no

Il MoE e' la scelta giusta quando si vuole massimizzare la capacita' del modello a parita' di budget di inferenza per token, quando si dispone di abbastanza memoria (VRAM o aggregata su piu' device) per tenere tutti gli expert, e quando il volume di training e' grande abbastanza da addestrare bene molti expert senza che restino sotto-allenati. E' la base architetturale dei modelli frontier proprio perche' permette di scalare la capacita' senza far esplodere il costo per richiesta.

E' la scelta sbagliata quando il vincolo dominante e' la memoria e non il compute (un MoE da 276B occupa la VRAM di un 276B anche se ne attiva 12B): in ambienti edge o single-GPU, un denso piu' piccolo e' spesso preferibile. E' sbagliata quando il budget di training e' limitato: con pochi dati, i molti expert restano sotto-addestrati e il modello rende meno di un denso equivalente in compute. E' sbagliata quando si vuole semplicita' operativa: servire un MoE richiede gestire routing, load balancing e comunicazione tra device.

Anti-pattern. Scegliere il MoE per il numero di parametri totali "da brochure" ignorando che il footprint di memoria scala con i totali, non con gli attivi. Trascurare il load balancing e ritrovarsi con expert collapse. Confrontare un MoE e un denso "a parita' di parametri totali" invece che a parita' di parametri attivi (il confronto equo per il costo di inferenza) o a parita' di costo di training.

## Esempi pratici

Esempio 1: full-duplex con capacita' alta e costo contenuto (TML-Interaction-Small). Un [interaction model](./interaction-model.md) realtime ha bisogno di latenza bassa, quindi di pochi parametri attivi, ma di molta conoscenza, quindi di tanti parametri totali. TML-Interaction-Small risolve il dilemma con un MoE 276B-A12B: 12B attivi tengono la latenza end-to-end a 0,40 s, i 276B totali forniscono la capacita'.

Esempio 2: il denso che batte il MoE (Granite 4.1). IBM ha mostrato che il Granite 4.1 8B instruct supera costantemente il Granite 4.0 32B Mixture-of-Experts sui benchmark principali, con un quarto dei parametri e un'architettura piu' semplice. La lezione: il MoE va giustificato, non assunto; un denso ben addestrato e piu' facile da quantizzare e da fine-tunare puo' vincere.

Esempio 3: expert per dominio nel coding (Project Polaris). Microsoft progetta Project Polaris come MoE in cui moduli specializzati coprono linguaggi e paradigmi distinti, con vantaggio marcato su Rust e Haskell. L'idea e' che expert dedicati a famiglie di linguaggi catturino meglio le idiosincrasie di ciascuno rispetto a un denso generalista.

## Letture

- Shazeer et al., "Outrageously Large Neural Networks: The Sparsely-Gated Mixture-of-Experts Layer", 2017. https://arxiv.org/abs/1701.06538
- Fedus, Zoph, Shazeer, "Switch Transformers", 2021. https://arxiv.org/abs/2101.03961
- Jacobs et al., "Adaptive Mixtures of Local Experts", 1991. https://doi.org/10.1162/neco.1991.3.1.79
- IBM Research, "Granite 4.1 foundation models", 2026. https://research.ibm.com/blog/granite-4-1-ai-foundation-models
- Thinking Machines Lab, "Interaction models" (TML-Interaction-Small), 2026. https://thinkingmachines.ai/blog/interaction-models/
- InclusionAI, "LLaDA2.0-Uni", arXiv 2604.20796, 2026. https://arxiv.org/abs/2604.20796
- Akhauri, Abdelfattah, "Compute Where it Counts: Self Optimizing Language Models", arXiv 2605.10875, 2026. https://arxiv.org/abs/2605.10875

## Note operative

Leggere la notazione "totali-attivi". Una model card che dichiara "276B-A12B" o "30B-A3B" indica parametri totali e parametri attivi: i totali governano la memoria da allocare, gli attivi governano il costo di calcolo per token e la latenza. Pianificare l'hardware sui totali, stimare il costo di servizio sugli attivi. Confondere i due numeri porta a sotto-dimensionare la VRAM o a sovrastimare il throughput.

Quando un denso e' la scelta migliore. Per deployment su singola GPU, su edge o in ambienti dove il fine-tuning deve essere semplice e prevedibile, un denso piu' piccolo e' spesso preferibile a un MoE piu' grande: meno memoria, niente load balancing, quantizzazione e [fine-tuning](./fine-tuning.md) piu' diretti. Il MoE paga quando si serve ad alto volume e il compute per token e' il vincolo economico dominante.

Combinare gli assi di efficienza. MoE (sparsita' tra expert), quantizzazione (precisione ridotta dei pesi) e adaptive per-token compute (budget variabile) sono assi ortogonali e cumulabili. Un sistema di serving maturo li combina: un MoE quantizzato ad AWQ 4-bit con allocazione adattiva del compute per token e' lo stato dell'arte dell'ottimizzazione dell'inferenza nel 2026.

## Aggiornamenti

### 2026-06-05

MAI-Thinking-1, primo modello di ragionamento interno Microsoft (annunciato al Build 2026 il 2 giugno), e' un'architettura sparse MoE con 35 miliardi di parametri attivi e finestra di contesto da 256.000 token — addestrato senza distillazione da OpenAI o Anthropic. Conferma il pattern 2026: ogni nuova architettura di ragionamento frontier sceglie MoE per disaccoppiare capacita' e costo per token. Il dato operativo rilevante per chi pianifica il deployment: 35B attivi su un totale non dichiarato, con context 256K che implica un KV cache significativo — il servicing richiede istanze con memoria HBM adeguata al regime di long context. Vedi [digest 2026-06-05](../../digest/2026/06/05.md).

### 2026-06-01

Il MoE ricorre come scelta architetturale trasversale nei digest di maggio-giugno 2026. TML-Interaction-Small (Thinking Machines Lab, 11-12 maggio) e' un MoE 276B-A12B che combina capacita' alta e latenza bassa per il full-duplex (vedi [digest 2026-05-13](../../digest/2026/05/13.md)). LLaDA2.0-Uni (InclusionAI) usa un backbone MoE con masked diffusion per unificare understanding e generazione multimodale (vedi [digest 2026-05-03](../../digest/2026/05/03.md)). IBM Granite 4.1 fornisce il controesempio istruttivo: un 8B denso che batte un 32B MoE della generazione precedente (vedi [digest 2026-05-05](../../digest/2026/05/05.md)). Microsoft pre-annuncia Project Polaris come MoE per il coding con expert mappati a linguaggi e paradigmi distinti (vedi [digest 2026-06-01](../../digest/2026/06/01.md)). Sul fronte efficienza, il paper SOL (vedi [digest 2026-05-13](../../digest/2026/05/13.md)) e l'acquisizione di Eigen AI/AWQ da parte di Nebius (vedi [digest 2026-05-03](../../digest/2026/05/03.md)) mostrano assi complementari al routing tra expert. Il filo conduttore: separare capacita' (parametri totali) e costo (parametri attivi) e' la leva centrale dell'economia dell'inferenza frontier, ma non sostituisce un buon training — un denso ben fatto puo' ancora vincere.

### 2026-06-12

DiffusionGemma (Google, 10 giugno, 13+ fonti) introduce un nuovo caso d'uso del backbone MoE: utilizzato non per un LLM autoregressivo ma come base per un modello di text diffusion. Il backbone Gemma 4 26B MoE con 3,8B parametri attivi e' il fondamento su cui Google ha costruito la variante diffusiva: il MoE serve a garantire capacita' sufficiente (26B totali) con un footprint computazionale limitato per forward pass (3,8B attivi), essenziale per i passi di denoising iterativi dove ogni passo e' un forward pass completo. Il pattern "MoE come base per architetture non autoregressove" e' nuovo nel 2026: in precedenza il MoE era usato quasi esclusivamente in contesti autoregressivi (Mixtral, DeepSeek, Granite). DiffusionGemma dimostra che il beneficio di efficienza del MoE — costo attivo inferiore al costo totale — e' trasferibile a qualsiasi architettura che richieda piu' forward pass per produrre un output (diffusion, beam search, speculative decoding). [Digest 2026-06-12](../../digest/2026/06/12.md)

### 2026-07-05

LongCat-2.0 (Meituan, 30 giugno, missed coverage) introduce un nuovo caso d'uso rilevante per il MoE: primo modello frontier addestrato interamente su chip domestici cinesi senza alcun hardware NVIDIA. L'architettura e' un MoE da 1,6 trilioni di parametri totali con circa 48 miliardi attivi per token (range 33B-56B a seconda del routing), contesto nativo da 1 milione di token, licenza MIT. Il substrate hardware e' il dato strutturalmente nuovo: cluster da 50.000 chip Huawei Ascend 910, con parallelismi custom e libreria HCCL sviluppati da Meituan per scalare il training a questa dimensione. Prima del rilascio ufficiale, LongCat-2.0 era disponibile su OpenRouter come "Owl Alpha" e guidava i ranking per sviluppatori della piattaforma per circa due mesi. Benchmark al lancio: SWE-Bench Pro 59.5, Terminal-Bench 70.8 — in fascia competitiva con i modelli frontier non-flagship. Il caso e' rilevante per due ragioni: (1) dimostra empiricamente che un MoE a scala frontier puo' essere addestrato senza chip Nvidia, riducendo la dipendenza dal supply chain americano che le misure BIS del 2022-2026 intendevano creare; (2) il ratio active/total (48B/1.6T ≈ 1:33) e' piu' sparso dei modelli della generazione precedente (Kimi K2.7 1:10, GLM-5.2 1:18), un segnale che l'architettura MoE si sta spingendo verso una sparsita' piu' estrema per massimizzare la capacita' a parita' di costo di inferenza. Al momento del rilascio, i pesi non erano ancora scaricabili (repository in stato "coming soon"). [Digest 2026-07-05](../../digest/2026/07/05.md)

### 2026-06-20

Tre modelli open-weight per il coding agentico rilasciati nella settimana del ban Fable 5 confermano il MoE come architettura standard per disaccoppiare capacita' e costo di serving: Cohere North Mini Code (30B totali / 3B attivi via 128 expert, Apache 2.0, 256K context), Kimi K2.7-Code di Moonshot (1T totali / 32B attivi, 384 expert, Modified MIT, 256K context), GLM-5.2 di Zhipu/Z.ai (744B totali / 40B attivi, MIT, 1M context). I ratio active/total variano da 1:10 (Kimi K2.7-Code) a 1:18 (North Mini Code), un range piu' ampio rispetto ai modelli frontier della generazione precedente. Il pattern unificante e' la specializzazione degli expert per task di coding agentico: sia North Mini Code che K2.7-Code sono addestrati specificamente per agentic software engineering, mentre GLM-5.2 si posiziona come general-purpose con forte performance sul coding. Tutti e tre sono stati adottati da team enterprise come alternative a Fable 5 nel corso della stessa settimana del ban, documentando per la prima volta la velocita' con cui il mercato sostituisce un modello proprietario sospeso con modelli open-weight quando il gap di qualita' e' sufficientemente ridotto. Vedi [Digest 2026-06-20](../../digest/2026/06/20.md).
