---
name: Fine-tuning
aliases: [fine-tuning, fine tuning, SFT, supervised fine-tuning, adattamento di modello]
categoria: training
created: 2026-04-28
last_updated: 2026-06-01
mentions_count: 0
---

# Fine-tuning

## Cos'e

Il fine-tuning e' la procedura di addestramento aggiuntivo di un modello pre-addestrato su un dataset piu' ristretto, allo scopo di specializzarlo per uno stile, un compito, un dominio. Si parte da un checkpoint con pesi gia' utili, si esegue un training a learning rate bassi su esempi etichettati, si ottiene un modello che mantiene la capacita' generale del pre-training ma incorpora pattern specifici del nuovo dataset. Nel ciclo di addestramento di un [LLM](./llm.md) moderno il fine-tuning e' la fase post-pretraining, prima o in parallelo all'allineamento ([RLHF](./rlhf.md), DPO).

Il termine compare nel deep learning con la transfer learning su ImageNet (Yosinski et al., 2014), dove congelare i primi layer e ri-addestrare gli ultimi diventa pratica standard. Per NLP la pubblicazione di ULMFiT (Howard e Ruder, 2018) e poi BERT formalizza il pattern "pre-train then fine-tune". Con la scala dei modelli a centinaia di miliardi di parametri il fine-tuning full-weights diventa proibitivo, e nascono le tecniche parameter-efficient (PEFT): adapter, prefix tuning, e soprattutto LoRA (Hu et al., 2021) che e' oggi standard.

L'importanza del fine-tuning sta nel suo ruolo specifico nella pipeline. Dove il prompt engineering modifica l'input e [RAG](./rag.md) inietta conoscenza a runtime, il fine-tuning altera il comportamento del modello stesso: insegna stile, formato di output, accenti linguistici, riconoscimento di pattern di dominio che il prompt non riesce a indurre stabilmente. Per le aziende e' il modo per creare un asset proprietario sopra modelli open-weight (Llama, Mistral, Qwen, e dal maggio 2026 la famiglia IBM Granite 4.1 sotto licenza Apache 2.0) o per personalizzare modelli closed via fine-tuning API.

Nel 2026 il confine concettuale del fine-tuning si e' spostato. Per anni "fine-tuning" significava quasi esclusivamente SFT supervisionato; oggi il post-training include anche un secondo asse, il reinforcement learning con reward verificabili (RLVR) e i suoi algoritmi (GRPO, DPO, varianti), usato non piu' solo per allineamento ma per instillare capacita' di ragionamento. La ricetta che produce i modelli reasoning di frontiera e' diventata una sequenza fine-tuning + RL: lo si vede nettamente in SU-01 (curriculum-SFT poi RL in due stadi, maggio 2026) e nei modelli che lo precedono come DeepSeek R1 e o1. Capire il fine-tuning oggi significa quindi capire dove finisce l'SFT e dove inizia l'RL, e perche' la combinazione dei due e' diventata il default per i task verticali ad alto valore.

## Come funziona

Fine-tuning supervisionato (SFT) classico. Si prepara un dataset di esempi `(input, output)` o `(messages)` in formato chat. Si carica un checkpoint base. Si esegue un training loop con AdamW, learning rate dell'ordine di 1e-5 - 5e-5 (un ordine di grandezza piu' basso del pre-training), batch size piccolo, 1-3 epoche. La loss e' la cross-entropy sul next-token prediction, ma calcolata solo sui token di output (i token di input sono mascherati nella loss).

Considerazioni quantitative. Per un modello da 7B parametri, full fine-tuning su una singola GPU H100 80GB richiede gradient checkpointing e ottimizzazioni di memoria; con tecniche PEFT si scende a una singola A100 40GB. La VRAM necessaria scala con: parametri + ottimizzatore (AdamW = 2x parametri) + gradienti + activations. Per un 70B il full fine-tune richiede cluster multi-GPU.

LoRA (Low-Rank Adaptation). Invece di aggiornare tutti i pesi `W` di una matrice, si aggiunge una decomposizione a basso rango: `W' = W + alpha * (B A)`, dove `A` e' `r x d_in`, `B` e' `d_out x r`, e `r` e' tipicamente 8-64. Solo `A` e `B` vengono addestrati; il modello base resta congelato. La riduzione di parametri trainable e' di 100-10000x; in pratica si addestra lo 0.1-1% dei parametri totali recuperando il 90-95% della qualita' del full fine-tuning. Le adapter LoRA sono piccole (10-200 MB) e si possono caricare/scaricare a runtime, abilitando multi-tenancy: un modello base + N adapter per N clienti.

QLoRA (Dettmers et al., 2023). Combina LoRA con quantizzazione 4-bit del modello base. Permette di fine-tunare modelli 65B su una singola A100 80GB con perdita minima di qualita'. E' il setup di default per fine-tuning su consumer hardware. La quantizzazione e' diventata nel 2026 un asse economicamente centrale: a maggio Nebius ha acquisito Eigen AI (gli autori di AWQ, Activation-Aware Weight Quantization) per circa 643 milioni di dollari, segnale che lo strato di compressione dei pesi - lo stesso che rende fattibile QLoRA - e' considerato un asset strategico (vedi [inference](./inference.md)).

DPO (Direct Preference Optimization, Rafailov et al., 2023). Alternativa a [RLHF](./rlhf.md) per allineamento. Invece di addestrare un reward model e fare RL con PPO, si ottimizza direttamente una loss contrastiva closed-form che incorpora le preferenze pairwise `(prompt, chosen, rejected)`. Piu' semplice, stabile, computazionalmente leggero, senza l'instabilita' di PPO. Nel 2026 DPO e le sue discendenti (ORPO, IPO, KTO) sono il default di produzione per l'allineamento a preferenze nella maggior parte dei team, mentre RLHF-PPO resta confinato ai casi piu' avanzati.

GRPO e RLVR. Group Relative Policy Optimization (introdotto nel 2024, usato per addestrare DeepSeek R1) e' un algoritmo RL che rimuove il critic network di PPO: genera piu' completamenti per la stessa domanda e calcola l'advantage dai reward relativi del gruppo. Quando il reward e' deterministico e verificabile - correttezza di una soluzione matematica, esito di un test di codice, conformita' a un formato - si parla di Reinforcement Learning with Verifiable Rewards (RLVR), che sostituisce il reward model appreso con verifica diretta dell'output. E' il meccanismo con cui si fa "reasoning fine-tuning". La ricerca recente lavora sulla stabilita' e sul credit assignment di GRPO (es. GRPO-VPS, arXiv 2604.20659, che aggiunge una process supervision verificabile probando la fiducia del modello nella risposta corretta).

Continued pre-training (domain adaptation). Forma di fine-tuning su corpus non etichettato di dominio (es. testi medici, legali, codice di un linguaggio raro). Mantiene l'obiettivo next-token prediction ma su distribuzione spostata. Spesso si fa prima di SFT per innestare conoscenza di dominio.

Esempio numerico. Un dataset di 10.000 esempi con media 1500 token totali = 15M token. A 5e-5 learning rate, batch effettivo 64k token, 3 epoche, il training dura poche ore su una H100 con LoRA r=16. Costo ordine 50-200 euro su GPU cloud.

## Varianti / approcci

| Tecnica | Trainable params | Costo | Quando |
|---|---|---|---|
| Full fine-tuning | 100% | Alto | Massima qualita', risorse abbondanti |
| LoRA | 0.1-1% | Basso | Default per la maggior parte dei casi |
| QLoRA | 0.1-1% (base 4-bit) | Bassissimo | Hardware consumer |
| Adapter (Houlsby) | 1-3% | Medio-basso | Pre-LoRA, oggi raro |
| Prefix / prompt tuning | < 0.1% | Bassissimo | Task semplici, modelli piccoli |
| DPO / ORPO / KTO | LoRA o full | Medio | Allineamento a preferenze |
| GRPO / RLVR | LoRA o full | Medio-alto | Reasoning, reward verificabile |
| RLHF (PPO) | LoRA o full | Alto | Allineamento avanzato con reward model |
| Distillation | full di un modello piccolo | Medio | Comprimere un teacher in uno student |
| Mixture-of-LoRAs | piu' adapter + router | Medio | Specializzazione multi-dominio |

Asse di scopo. Style fine-tuning: insegnare un tono, una voce di brand, un formato (es. JSON con campi precisi). Capability fine-tuning: insegnare a svolgere un task verticale (estrazione di entita' mediche, classificazione di intent). Reasoning fine-tuning: addestrare su catene di ragionamento corrette (CoT, vedi [chain-of-thought](./chain-of-thought.md)). I modelli reasoning come o1, DeepSeek R1 e SU-01 (30B-A3B, maggio 2026) sono prodotti con una sequenza SFT su ragionamenti + RL su task verificabili: SU-01 usa SFT con curriculum reverse-perplexity su circa 340K traiettorie, poi RL in due stadi (prima reward verificabili, poi "proof-level RL"), poi test-time scaling, raggiungendo il livello medaglia d'oro su IMO 2025, USAMO 2026 e IPhO senza modifiche architetturali.

Asse di dato. Human-curated: piu' qualita', costoso. Synthetic data: generato da un modello forte come "teacher" (tecnica di distillation, usata da Alpaca, Vicuna, e dalla maggior parte dei modelli open recenti). La distillation e' tornata sotto i riflettori a maggio 2026 quando Elon Musk ha ammesso sotto cross-examination, nel processo Musk v. Altman, che xAI ha usato modelli OpenAI come teacher per addestrare Grok - episodio che illustra quanto la generazione di dati sintetici da un modello forte sia ormai pratica diffusa, e i nodi legali che ne derivano. Mixed: bootstrap sintetico con curation umana spot-check.

Mixture-of-LoRAs e routing. Una linea di ricerca 2026 estende LoRA instradando ogni input attraverso un piccolo pool di adapter per layer, abilitando specializzazione su distribuzioni di input diverse. Approcci come ReMix (Reinforcement routing for mixtures of LoRAs, arXiv 2603.10160) applicano RL per ottimizzare il routing tra piu' adapter LoRA. E' un'evoluzione utile quando un singolo adapter non basta a coprire piu' sotto-domini eterogenei.

## Quando usarlo / quando no

Il fine-tuning e' la scelta giusta quando: serve uno stile o formato che il prompt non garantisce stabilmente; c'e' un task ripetitivo ad alto volume con dataset etichettato (anche solo 200-1000 esempi gia' aiutano); si vuole ridurre latenza/costo passando a un modello piu' piccolo fine-tunato che eguaglia un grande prompt-engineered; si vuole proteggere conoscenza proprietaria (un competitor non puo' replicare il modello solo dal prompt); serve adattamento linguistico o di dominio profondo; serve instillare capacita' di ragionamento su un dominio con reward verificabile (in questo caso la leva e' RLVR/GRPO sopra l'SFT, non l'SFT da solo).

Il fine-tuning e' la scelta sbagliata quando: il problema e' di "conoscenza factuale" (i fatti vanno in [RAG](./rag.md), non nei pesi); il dataset e' minimo e di qualita' bassa (peggiora le cose); il modello base evolve rapidamente (ogni nuova versione richiede ri-fine-tuning); l'iterazione del prodotto e' veloce (il prompt si modifica in minuti, il fine-tune in giorni).

Anti-pattern. Fine-tunare prima di aver provato seriamente prompt engineering e few-shot: spesso il prompt risolve. Fine-tunare su dataset rumorosi o piccoli: catastrophic forgetting (il modello peggiora altrove). Misurare solo la loss di training: serve un eval set fuori distribuzione e benchmark di non-regressione (vedi [evaluation-benchmark](./evaluation-benchmark.md)). Mescolare style e factual nello stesso fine-tune (stile via fine-tune, fatti via RAG e' la separazione corretta). Usare un modello chat senza preservare il system prompt training format: si rompe la chat template. Per il reasoning fine-tuning, un anti-pattern emerso nel 2026 e' assumere che serva sempre un ciclo RL completo: il paper ReasonMaxxer (arXiv 2605.06241) mostra che il beneficio dell'RL per il reasoning e' concentrato nell'1-3% delle posizioni token (i punti di decisione ad alta entropia), e replicabile con una contrastive loss mirata a costo radicalmente inferiore - prima di lanciare un costoso ciclo RL conviene verificare se basta un intervento sparso.

## Esempi pratici

Esempio 1: fine-tuning con LoRA su Llama 3 8B per generazione di email in stile aziendale.

```python
from peft import LoraConfig, get_peft_model
from transformers import AutoModelForCausalLM, AutoTokenizer, Trainer, TrainingArguments

base = "meta-llama/Meta-Llama-3-8B-Instruct"
model = AutoModelForCausalLM.from_pretrained(base, torch_dtype="bfloat16")
tok = AutoTokenizer.from_pretrained(base)

cfg = LoraConfig(r=16, lora_alpha=32, target_modules=["q_proj", "v_proj", "o_proj"],
                 lora_dropout=0.05, bias="none", task_type="CAUSAL_LM")
model = get_peft_model(model, cfg)

# Dataset: 1500 email aziendali (input: brief, output: email finale)
trainer = Trainer(model=model, args=TrainingArguments(
    output_dir="./out", learning_rate=2e-4, num_train_epochs=3,
    per_device_train_batch_size=4, gradient_accumulation_steps=4,
    bf16=True, logging_steps=20, save_strategy="epoch"
), train_dataset=dataset)
trainer.train()
model.save_pretrained("./adapter")
```

Esempio 2: fine-tuning hosted via API (OpenAI, Anthropic, Together). Si carica un JSONL con messages, si lancia un job, si ottiene un model id. Latenza tipica del job: 30 minuti - 4 ore. Costo per token di training visibile a prezzario. Inference sul modello fine-tunato ha tariffa maggiorata rispetto al base.

Esempio 3: caso tipico in produzione. Un'azienda ha 50.000 ticket annotati con categoria. Fine-tuna un modello 7B in LoRA per classificazione. Confronto: un modello frontier prompt-engineered con few-shot ottiene 92% accuracy a 8x costo per ticket; il modello fine-tunato self-hosted ottiene 91% a 1x. ROI evidente sopra il milione di ticket/anno.

Esempio 4: reasoning fine-tuning con reward verificabile. Per un task di soluzione di problemi matematici, si parte da un backbone reasoning, si fa SFT su un set di traiettorie di ragionamento corrette, poi si applica GRPO con reward binario (soluzione corretta vs errata, verificata da un checker deterministico). E' la struttura della ricetta SU-01: nessuna modifica al transformer, solo SFT con curriculum + RL a stadi + test-time scaling. Toolchain 2026: Unsloth per velocita' su hardware consumer, Axolotl per pipeline guidate da YAML, TRL per gli obiettivi RL avanzati (DPO, GRPO).

## Letture

- Howard e Ruder, "Universal Language Model Fine-tuning for Text Classification" (ULMFiT), 2018. https://arxiv.org/abs/1801.06146
- Hu et al., "LoRA: Low-Rank Adaptation of Large Language Models", 2021. https://arxiv.org/abs/2106.09685
- Dettmers et al., "QLoRA: Efficient Finetuning of Quantized LLMs", NeurIPS 2023. https://arxiv.org/abs/2305.14314
- Rafailov et al., "Direct Preference Optimization", NeurIPS 2023. https://arxiv.org/abs/2305.18290
- Hu et al., "ORPO: Monolithic Preference Optimization without Reference Model", 2024. https://arxiv.org/abs/2403.07691
- "GRPO-VPS: Enhancing Group Relative Policy Optimization with Verifiable Process Supervision", 2026. https://arxiv.org/abs/2604.20659
- "ReMix: Reinforcement routing for mixtures of LoRAs in LLM finetuning", 2026. https://arxiv.org/pdf/2603.10160
- Hugging Face PEFT documentation. https://huggingface.co/docs/peft
- Axolotl, framework di fine-tuning. https://github.com/OpenAccess-AI-Collective/axolotl
- Unsloth, fine-tuning guide. https://unsloth.ai/docs/get-started/fine-tuning-llms-guide
- OpenAI fine-tuning guide. https://platform.openai.com/docs/guides/fine-tuning

## Note operative

Qualita' del dato. La regola empirica e' che 1000 esempi di alta qualita' battono 50.000 esempi rumorosi. Curare il dataset (deduplicare, normalizzare formato, rimuovere outlier, bilanciare classi) ha ROI altissimo. Per task chat, ogni esempio dovrebbe rispettare il formato `messages` esatto del modello target (system, user, assistant, tool) - mismatch di template e' la prima causa di fine-tuning fallito.

Eval e regressioni. Senza un eval set fuori distribuzione, il fine-tuning ottimizza solo la training loss, che e' fuorviante. Buona pratica: suite di test in tre tier - in-distribution (esempi simili al training), out-of-distribution (variazioni realistiche), capability preservation (benchmark generali come MMLU, MT-Bench per assicurarsi che il modello non abbia perso capacita' generali). Misurare prima e dopo, comparare. Un fine-tune che migliora del 10% sul task ma peggiora del 20% su MMLU spesso non vale.

Scelta del modello base. La scelta del base condiziona costo ed efficacia del fine-tune. Il trend 2026 e' verso modelli piccoli ma fortemente competitivi: IBM Granite 4.1 8B (rilasciato a fine aprile 2026, Apache 2.0) supera il precedente Granite 4.0 32B MoE sui benchmark principali con un quarto dei parametri e un'architettura piu' semplice che facilita il fine-tuning in ambienti vincolati. Per molti task verticali un 7-8B ben scelto fine-tunato in LoRA e' la soluzione con il miglior rapporto qualita'/costo, e va preferito a un fine-tune di un modello molto piu' grande.

Iterazione modello base. Il modello base evolve. Fine-tune fatti su una release vanilla potrebbero non essere ottimali su una successiva, ma rifare il training costa risorse. Strategia: tenere il dataset versionato e ben documentato, automatizzare il pipeline di fine-tuning, ri-fare il training quando un nuovo base supera un threshold di miglioramento sui propri eval. La portabilita' dell'adapter LoRA tra versioni del base e' limitata - di solito serve ri-addestramento.

## Aggiornamenti

Nessun aggiornamento dopo la creazione (2026-04-28).

### 2026-06-01
Il mese di maggio 2026 ha consolidato lo spostamento del post-training verso la combinazione SFT + RL: SU-01 mostra una ricetta curriculum-SFT poi RL a due stadi che raggiunge il livello olimpico senza modifiche architetturali ([15.md](../../digest/2026/05/15.md)), mentre ReasonMaxxer dimostra che il beneficio dell'RL e' sparso (1-3% dei token) e replicabile a costo molto inferiore ([11.md](../../digest/2026/05/11.md)). Su RLHF la ricerca documenta l'alignment collapse iterativo e propone FPO ([08.md](../../digest/2026/05/08.md)). La distillation da modelli forti torna centrale (ammissione xAI nel processo Musk v. Altman, [02.md](../../digest/2026/05/02.md)), e la quantizzazione che abilita QLoRA si conferma asset strategico con l'acquisizione di Eigen AI/AWQ da parte di Nebius ([03.md](../../digest/2026/05/03.md)). Aggiunte le voci GRPO/RLVR, Mixture-of-LoRAs e la nota sui base model piccoli (Granite 4.1).
