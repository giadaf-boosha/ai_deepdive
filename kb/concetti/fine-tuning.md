---
name: Fine-tuning
aliases: [fine-tuning, fine tuning, SFT, supervised fine-tuning, adattamento di modello]
categoria: training
created: 2026-04-28
last_updated: 2026-04-28
mentions_count: 0
---

# Fine-tuning

## Cos'e

Il fine-tuning e' la procedura di addestramento aggiuntivo di un modello pre-addestrato su un dataset piu' ristretto, allo scopo di specializzarlo per uno stile, un compito, un dominio. Si parte da un checkpoint con pesi gia' utili, si esegue un training a learning rate bassi su esempi etichettati, si ottiene un modello che mantiene la capacita' generale del pre-training ma incorpora pattern specifici del nuovo dataset. Nel ciclo di addestramento di un [LLM](./llm.md) moderno il fine-tuning e' la fase post-pretraining, prima o in parallelo all'allineamento ([RLHF](./rlhf.md), DPO).

Il termine compare nel deep learning con la transfer learning su ImageNet (Yosinski et al., 2014), dove congelare i primi layer e ri-addestrare gli ultimi diventa pratica standard. Per NLP la pubblicazione di ULMFiT (Howard e Ruder, 2018) e poi BERT formalizza il pattern "pre-train then fine-tune". Con la scala dei modelli a centinaia di miliardi di parametri il fine-tuning full-weights diventa proibitivo, e nascono le tecniche parameter-efficient (PEFT): adapter, prefix tuning, e soprattutto LoRA (Hu et al., 2021) che e' oggi standard.

L'importanza del fine-tuning sta nel suo ruolo specifico nella pipeline. Dove il prompt engineering modifica l'input e [RAG](./rag.md) inietta conoscenza a runtime, il fine-tuning altera il comportamento del modello stesso: insegna stile, formato di output, accenti linguistici, riconoscimento di pattern di dominio che il prompt non riesce a indurre stabilmente. Per le aziende e' il modo per creare un asset proprietario sopra modelli open-weight (Llama, Mistral, Qwen) o per personalizzare modelli closed via fine-tuning API.

## Come funziona

Fine-tuning supervisionato (SFT) classico. Si prepara un dataset di esempi `(input, output)` o `(messages)` in formato chat. Si carica un checkpoint base. Si esegue un training loop con AdamW, learning rate dell'ordine di 1e-5 - 5e-5 (un ordine di grandezza piu' basso del pre-training), batch size piccolo, 1-3 epoche. La loss e' la cross-entropy sul next-token prediction, ma calcolata solo sui token di output (i token di input sono mascherati nella loss).

Considerazioni quantitative. Per un modello da 7B parametri, full fine-tuning su una singola GPU H100 80GB richiede gradient checkpointing e ottimizzazioni di memoria; con tecniche PEFT si scende a una singola A100 40GB. La VRAM necessaria scala con: parametri + ottimizzatore (AdamW = 2x parametri) + gradienti + activations. Per un 70B il full fine-tune richiede cluster multi-GPU.

LoRA (Low-Rank Adaptation). Invece di aggiornare tutti i pesi `W` di una matrice, si aggiunge una decomposizione a basso rango: `W' = W + alpha * (B A)`, dove `A` e' `r x d_in`, `B` e' `d_out x r`, e `r` e' tipicamente 8-64. Solo `A` e `B` vengono addestrati; il modello base resta congelato. La riduzione di parametri trainable e' di 100-10000x. Le adapter LoRA sono piccole (10-200 MB) e si possono caricare/scaricare a runtime, abilitando multi-tenancy: un modello base + N adapter per N clienti.

QLoRA (Dettmers et al., 2023). Combina LoRA con quantizzazione 4-bit del modello base. Permette di fine-tunare modelli 65B su una singola A100 80GB con perdita minima di qualita'. E' il setup di default per fine-tuning su consumer hardware.

DPO (Direct Preference Optimization, Rafailov et al., 2023). Alternativa a [RLHF](./rlhf.md) per allineamento. Invece di addestrare un reward model e fare RL, si ottimizza direttamente una loss che incorpora le preferenze pairwise `(prompt, chosen, rejected)`. Piu' semplice, stabile, computazionalmente leggero. ORPO, IPO, KTO sono varianti.

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
| DPO / ORPO | LoRA o full | Medio | Allineamento a preferenze |
| RLHF (PPO) | LoRA o full | Alto | Allineamento avanzato |
| Distillation | full di un modello piccolo | Medio | Comprimere un teacher in uno student |

Asse di scopo. Style fine-tuning: insegnare un tono, una voce di brand, un formato (es. JSON con campi precisi). Capability fine-tuning: insegnare a svolgere un task verticale (estrazione di entita' mediche, classificazione di intent). Reasoning fine-tuning: addestrare su catene di ragionamento corrette (CoT, recenti modelli reasoning come o1, DeepSeek R1, sono prodotti con SFT su ragionamenti + RL su task verificabili).

Asse di dato. Human-curated: piu' qualita', costoso. Synthetic data: generato da un modello forte come "teacher" (technique of distillation, used da Alpaca, Vicuna, e dalla maggior parte dei modelli open recenti). Mixed: bootstrap sintetico con curation umana spot-check.

## Quando usarlo / quando no

Il fine-tuning e' la scelta giusta quando: serve uno stile o formato che il prompt non garantisce stabilmente; c'e' un task ripetitivo ad alto volume con dataset etichettato (anche solo 200-1000 esempi gia' aiutano); si vuole ridurre latenza/costo passando a un modello piu' piccolo fine-tunato che eguaglia un grande prompt-engineered; si vuole proteggere conoscenza proprietaria (un competitor non puo' replicare il modello solo dal prompt); serve adattamento linguistico o di dominio profondo.

Il fine-tuning e' la scelta sbagliata quando: il problema e' di "conoscenza factuale" (i fatti vanno in [RAG](./rag.md), non nei pesi); il dataset e' minimo e di qualita' bassa (peggiora le cose); il modello base evolve rapidamente (ogni nuova versione richiede ri-fine-tuning); l'iterazione del prodotto e' veloce (il prompt si modifica in minuti, il fine-tune in giorni).

Anti-pattern. Fine-tunare prima di aver provato seriamente prompt engineering e few-shot: spesso il prompt risolve. Fine-tunare su dataset rumorosi o piccoli: catastrophic forgetting (il modello peggiora altrove). Misurare solo la loss di training: serve un eval set fuori distribuzione e benchmark di non-regressione. Mescolare style e factual nello stesso fine-tune (stile via fine-tune, fatti via RAG e' la separazione corretta). Usare un modello chat senza preservare il system prompt training format: si rompe la chat template.

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

Esempio 3: caso tipico in produzione. Un'azienda ha 50.000 ticket annotati con categoria. Fine-tuna un modello 7B in LoRA per classificazione. Confronto: GPT-4o con few-shot ottiene 92% accuracy a 8x costo per ticket; il modello fine-tunato self-hosted ottiene 91% a 1x. ROI evidente sopra il milione di ticket/anno.

## Letture

- Howard e Ruder, "Universal Language Model Fine-tuning for Text Classification" (ULMFiT), 2018. https://arxiv.org/abs/1801.06146
- Hu et al., "LoRA: Low-Rank Adaptation of Large Language Models", 2021. https://arxiv.org/abs/2106.09685
- Dettmers et al., "QLoRA: Efficient Finetuning of Quantized LLMs", NeurIPS 2023. https://arxiv.org/abs/2305.14314
- Rafailov et al., "Direct Preference Optimization", NeurIPS 2023. https://arxiv.org/abs/2305.18290
- Hu et al., "ORPO: Monolithic Preference Optimization without Reference Model", 2024. https://arxiv.org/abs/2403.07691
- Hugging Face PEFT documentation. https://huggingface.co/docs/peft
- "The Novice's LLM Training Guide" e i tutorial di Axolotl. https://github.com/OpenAccess-AI-Collective/axolotl
- OpenAI fine-tuning guide. https://platform.openai.com/docs/guides/fine-tuning

## Note operative

Qualita' del dato. La regola empirica e' che 1000 esempi di alta qualita' battono 50.000 esempi rumorosi. Curare il dataset (deduplicare, normalizzare formato, rimuovere outlier, bilanciare classi) ha ROI altissimo. Per task chat, ogni esempio dovrebbe rispettare il formato `messages` esatto del modello target (system, user, assistant, tool) - mismatch di template e' la prima causa di fine-tuning fallito.

Eval e regressioni. Senza un eval set fuori distribuzione, il fine-tuning ottimizza solo la training loss, che e' fuorviante. Buona pratica: suite di test in tre tier - in-distribution (esempi simili al training), out-of-distribution (variazioni realistiche), capability preservation (benchmark generali come MMLU, MT-Bench per assicurarsi che il modello non abbia perso capacita' generali). Misurare prima e dopo, comparare. Un fine-tune che migliora del 10% sul task ma peggiora del 20% su MMLU spesso non vale.

Iterazione modello base. Il modello base evolve. Llama 3 -> 3.1 -> 3.3 -> 4 in due anni. Fine-tune fatti su Llama 3 vanilla potrebbero non essere ottimali su 3.3, ma rifare il training costa risorse. Strategia: tenere il dataset versionato e ben documentato, automatizzare il pipeline di fine-tuning, ri-fare il training quando un nuovo base supera un threshold di miglioramento sui propri eval. La portabilita' dell'adapter LoRA tra versioni del base e' limitata - di solito serve ri-addestramento.

## Aggiornamenti

Nessun aggiornamento dopo la creazione (2026-04-28).
