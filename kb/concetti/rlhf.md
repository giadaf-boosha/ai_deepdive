---
name: Reinforcement Learning from Human Feedback
aliases: [RLHF, reinforcement learning from human feedback, allineamento RL, RLAIF]
categoria: training
created: 2026-04-28
last_updated: 2026-04-28
mentions_count: 0
---

# Reinforcement Learning from Human Feedback

## Cos'e

Reinforcement Learning from Human Feedback (RLHF) e' una procedura di addestramento in cui un modello di linguaggio viene affinato tramite reinforcement learning, usando come segnale di reward un modello (reward model) addestrato su preferenze umane. Lo scopo non e' insegnare nuove conoscenze ma allineare il comportamento: produrre output che gli umani giudicano utili, onesti, innocui, conformi a un set di norme. RLHF e' la fase canonica che separa un base model (puramente predittore di token) da un modello "chat" usabile in prodotto.

L'idea ha radici in Christiano et al. (OpenAI/DeepMind, NeurIPS 2017) "Deep Reinforcement Learning from Human Preferences", originariamente applicata a giochi Atari e simulazioni. Stiennon et al. (2020) la portano sulla sintesi di testo. Ouyang et al. (2022) "Training language models to follow instructions with human feedback" formalizzano la pipeline che diventa nota come InstructGPT, antenata di ChatGPT. Da quel momento RLHF e' parte essenziale di tutti i modelli frontier: GPT-4, Claude, Gemini, Llama 2/3, Qwen, Mistral.

L'importanza di RLHF deriva dal fatto che preferenze umane sono difficili da catturare con label classiche. Per uno stesso prompt, un'output puo' essere "tecnicamente corretto" ma non "utile". Il [fine-tuning](./fine-tuning.md) supervisionato cattura forma e formato; RLHF cattura giudizio. Senza un livello di allineamento, i base model tendono a generare testi pleonastici, evasivi, spesso tossici, e non seguono istruzioni complesse.

## Come funziona

La pipeline RLHF canonica (variante PPO) ha tre fasi distinte.

Fase 1: SFT iniziale. Si fa supervised [fine-tuning](./fine-tuning.md) del modello base su un dataset di esempi di alta qualita' (prompt + risposta scritta da umani o da modelli forti). L'output e' un modello "policy" pi-SFT che gia' segue istruzioni in modo accettabile.

Fase 2: training del reward model. Si raccolgono preferenze pairwise: per ogni prompt si generano N (tipicamente 4-9) risposte dalla policy SFT; annotatori umani le ordinano. Si costruiscono coppie (chosen, rejected). Il reward model e' un transformer (spesso lo stesso modello SFT, con testa di scoring) che produce un singolo scalare. Si addestra con la Bradley-Terry loss: `L = -log(sigmoid(r(x, y_chosen) - r(x, y_rejected)))`. Il reward model deve generalizzare oltre le coppie viste.

Fase 3: RL con PPO. Si usa Proximal Policy Optimization (Schulman et al., 2017) per ottimizzare la policy sotto il reward model. Per ogni prompt nel buffer di training, la policy genera una completion; il reward model la valuta; il gradiente di policy si propaga. Per evitare che la policy si allontani troppo dal modello SFT (mode collapse, hacking del reward), si aggiunge un termine KL: `obiettivo = E[r(x,y)] - beta * KL(pi || pi_SFT)`. Beta e' iperparametro critico.

Variante RLAIF (Reinforcement Learning from AI Feedback). Le preferenze sono prodotte da un modello forte (GPT-4 class) invece che da umani, eventualmente guidato da una "constitution" testuale (lista di principi). Anthropic ha introdotto Constitutional AI (Bai et al., 2022): il modello critica e revisiona le proprie risposte secondo principi scritti, le coppie cosi' generate addestrano un reward model. RLAIF abbatte il costo di etichettatura.

DPO e successori. DPO (Rafailov et al., 2023) elimina reward model e RL: deriva una loss equivalente direttamente sulle coppie di preferenze, addestrando la policy con una procedura supervisionata. Piu' stabile e leggera di PPO. ORPO, KTO, IPO, SimPO sono varianti che ottimizzano la stessa idea con perdite diverse, alcune senza modello di riferimento.

Numeri tipici. La fase 1 SFT usa 10k - 100k esempi. La fase 2 reward model usa 50k - 500k coppie di preferenze. La fase 3 PPO consuma 10k - 100k step di training, con generazione online (la policy continua a produrre nuove risposte). Costo totale RLHF: 10-30% del costo di pre-training del modello, ordine di milioni di euro per un frontier model. Con DPO/RLAIF il costo scende di un ordine di grandezza.

Failure mode. Reward hacking: la policy trova pattern che massimizzano il reward senza migliorare davvero (es. risposte verbose perche' il reward model premia la lunghezza). Sycophancy: tendenza a confermare l'utente per piacere agli annotatori. Mode collapse: la policy converge a poche risposte stereotipate. Distributional shift: il reward model addestrato su una distribuzione di output non generalizza ad output troppo diversi.

## Varianti / approcci

| Tecnica | Reward source | Algoritmo | Caratteristica |
|---|---|---|---|
| InstructGPT-style RLHF | Umani (preferenze pairwise) | PPO | Originale, costoso, complesso |
| Constitutional AI / RLAIF | Modello AI con costituzione | PPO | Anthropic, scalable |
| DPO | Preferenze offline | Supervised loss | Stabile, semplice |
| KTO | Binary feedback (good/bad) | Kahneman-Tversky loss | Funziona con feedback non pairwise |
| ORPO | Preferenze | Loss combinata SFT+preferenze | Single-stage, niente reference model |
| Self-rewarding | Modello giudica se stesso | DPO iterativo | Yuan et al. 2024, scaling autonomo |
| Iterated RLHF | Loop di nuove preferenze su output recenti | PPO/DPO | Llama 2/3 chat |
| RL from verifiable rewards | Programma deterministico (test, math checker) | PPO/GRPO | Modelli reasoning o1, R1, R2 |

L'ultima riga merita attenzione. Per task verificabili (matematica, coding, logica) si puo' sostituire il reward model con un verificatore programmabile (un test runner, un math checker). E' la base dei modelli reasoning recenti: DeepSeek-R1 ha dimostrato che con GRPO (Group Relative Policy Optimization) e reward verificabili si possono produrre catene di [chain of thought](./chain-of-thought.md) sofisticate da un base model, anche senza SFT iniziale di alta qualita'.

## Quando usarlo / quando no

RLHF e i suoi successori sono la scelta giusta quando si costruisce un modello generalista chat-capable da deployare in prodotto, quando serve allineamento a policy organizzative complesse non esprimibili in regole, quando si ha budget e dati di preferenze, quando il modello deve gestire una distribuzione larga di intent. E' lo standard per qualunque modello pubblicato come "instruct" o "chat".

Sono la scelta sbagliata quando il task e' verticale e ben definito (un modello SFT senza RLHF basta), quando si fa fine-tuning di un modello gia' allineato per uno specifico tono (rischio di destabilizzare l'allineamento esistente), quando il volume di preferenze umane e' insufficiente (DPO ne richiede meno di PPO ma ne servono comunque migliaia), quando il task richiede precisione fattuale e RLHF puo' incoraggiare confidenza eccessiva.

Anti-pattern. Fare RL con un reward model debole: si amplificano i suoi bias. Saltare la fase SFT: il base model non sa rispondere e il segnale RL e' troppo rumoroso. Ottimizzare a oltranza il reward score: oltre una soglia il modello si rompe (overoptimization, Gao et al. 2022). Annotare preferenze senza guideline coerenti tra annotatori: si addestra rumore.

## Esempi pratici

Esempio 1: schema di pipeline DPO (sostituto pratico di PPO).

```python
from trl import DPOTrainer, DPOConfig

# dataset: lista di {"prompt", "chosen", "rejected"}
trainer = DPOTrainer(
    model=sft_model,
    ref_model=sft_model_frozen,
    args=DPOConfig(
        learning_rate=5e-7, beta=0.1,
        per_device_train_batch_size=2, gradient_accumulation_steps=8,
        num_train_epochs=1, output_dir="./dpo_out"
    ),
    train_dataset=preferences_dataset,
    tokenizer=tok,
)
trainer.train()
```

Esempio 2: Constitutional AI (semplificato). Si scrive una "costituzione" (lista di 10-30 principi: utilita', non danno, onesta', non diffamatorio, ...). Per ogni prompt il modello genera una risposta iniziale, poi un secondo passaggio in cui critica la risposta secondo un principio della costituzione e la riscrive. Le coppie (response_v1, response_v2_critiqued) diventano preferenze: v2 chosen, v1 rejected. Si addestra un reward model e si fa RL.

Esempio 3: caso enterprise. Un'azienda costruisce un assistente legale. Parte da un modello base 70B, fa SFT su 30k Q/A di studio, poi raccoglie 8k coppie di preferenze in cui senior partner annotano "risposta che useresti col cliente" vs "risposta scartata". DPO su queste coppie. Il modello finale produce risposte con tono e cautela conformi agli standard dello studio, riducendo il post-editing del 40% rispetto al baseline solo SFT.

## Letture

- Christiano et al., "Deep Reinforcement Learning from Human Preferences", NeurIPS 2017. https://arxiv.org/abs/1706.03741
- Stiennon et al., "Learning to summarize from human feedback", 2020. https://arxiv.org/abs/2009.01325
- Ouyang et al., "Training language models to follow instructions with human feedback" (InstructGPT), 2022. https://arxiv.org/abs/2203.02155
- Bai et al., "Constitutional AI: Harmlessness from AI Feedback", 2022. https://arxiv.org/abs/2212.08073
- Schulman et al., "Proximal Policy Optimization Algorithms", 2017. https://arxiv.org/abs/1707.06347
- Rafailov et al., "Direct Preference Optimization", NeurIPS 2023. https://arxiv.org/abs/2305.18290
- Gao et al., "Scaling Laws for Reward Model Overoptimization", 2022. https://arxiv.org/abs/2210.10760
- DeepSeek-AI, "DeepSeek-R1: Incentivizing Reasoning Capability in LLMs via Reinforcement Learning", 2025. https://arxiv.org/abs/2501.12948

## Note operative

Annotation guidelines. La qualita' delle preferenze dipende dalla coerenza tra annotatori. Senza linee guida scritte e calibrazione iniziale, gli annotatori divergono, il segnale diventa rumore, il modello apprende patterns spuri. Best practice: 5-10 pagine di guideline con esempi positivi e negativi, sessioni di calibrazione settimanali, agreement metric (Cohen's kappa) > 0.6 prima di iniziare la raccolta.

Reward model evaluation. Il reward model e' la fonte del segnale RL. Se il RM e' debole, l'RL amplifica i suoi bias. Misurarlo: accuracy su un test set di preferenze hold-out (target > 70% per un dominio generale, > 80% per dominio specializzato), out-of-distribution robustness, calibration. Senza RM eval, i fallimenti dell'RL sono inspiegabili.

Allineamento iterativo. I modelli frontier 2025-2026 non vengono allineati una volta sola. La pipeline e' iterativa: SFT + DPO/RLHF -> deploy -> raccolta feedback in produzione -> nuove preferenze -> nuovo training. Llama 3 chat e' stato addestrato in 5+ rounds. Ogni round si focalizza su problemi specifici (refusal eccessivi, allucinazioni su dominio X, stile su dominio Y). La capacita' di rispondere ai segnali di prodotto in iterazioni rapide e' competitive moat operativa.

## Aggiornamenti

Nessun aggiornamento dopo la creazione (2026-04-28).
