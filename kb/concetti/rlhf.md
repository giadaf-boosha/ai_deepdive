---
name: Reinforcement Learning from Human Feedback
aliases: [RLHF, reinforcement learning from human feedback, allineamento RL, RLAIF]
categoria: training
created: 2026-04-28
last_updated: 2026-06-01
mentions_count: 0
---

# Reinforcement Learning from Human Feedback

## Cos'e

Reinforcement Learning from Human Feedback (RLHF) e' una procedura di addestramento in cui un modello di linguaggio viene affinato tramite reinforcement learning, usando come segnale di reward un modello (reward model) addestrato su preferenze umane. Lo scopo non e' insegnare nuove conoscenze ma allineare il comportamento: produrre output che gli umani giudicano utili, onesti, innocui, conformi a un set di norme. RLHF e' la fase canonica che separa un base model (puramente predittore di token) da un modello "chat" usabile in prodotto.

L'idea ha radici in Christiano et al. (OpenAI/DeepMind, NeurIPS 2017) "Deep Reinforcement Learning from Human Preferences", originariamente applicata a giochi Atari e simulazioni. Stiennon et al. (2020) la portano sulla sintesi di testo. Ouyang et al. (2022) "Training language models to follow instructions with human feedback" formalizzano la pipeline che diventa nota come InstructGPT, antenata di ChatGPT. Da quel momento RLHF e' parte essenziale di tutti i modelli frontier: GPT-4, Claude, Gemini, Llama 2/3, Qwen, Mistral.

L'importanza di RLHF deriva dal fatto che preferenze umane sono difficili da catturare con label classiche. Per uno stesso prompt, un'output puo' essere "tecnicamente corretto" ma non "utile". Il [fine-tuning](./fine-tuning.md) supervisionato cattura forma e formato; RLHF cattura giudizio. Senza un livello di allineamento, i base model tendono a generare testi pleonastici, evasivi, spesso tossici, e non seguono istruzioni complesse.

Nel 2025-2026 il termine RLHF e' diventato un'etichetta ombrello. La famiglia comprende ormai tre rami che convivono nella stessa pipeline di post-training: (1) allineamento da preferenze umane o AI (RLHF/RLAIF classico), orientato a utilita', tono, sicurezza; (2) RL da reward verificabili (RLVR), orientato al reasoning su task con risposta controllabile (matematica, coding, logica), produttore di [chain of thought](./chain-of-thought.md) verificabili; (3) preference optimization offline (DPO e successori), che approssima il primo ramo senza loop RL online. Capire quale ramo si sta usando, e perche', e' oggi piu' importante che padroneggiare il singolo algoritmo.

## Come funziona

La pipeline RLHF canonica (variante PPO) ha tre fasi distinte.

Fase 1: SFT iniziale. Si fa supervised [fine-tuning](./fine-tuning.md) del modello base su un dataset di esempi di alta qualita' (prompt + risposta scritta da umani o da modelli forti). L'output e' un modello "policy" pi-SFT che gia' segue istruzioni in modo accettabile.

Fase 2: training del reward model. Si raccolgono preferenze pairwise: per ogni prompt si generano N (tipicamente 4-9) risposte dalla policy SFT; annotatori umani le ordinano. Si costruiscono coppie (chosen, rejected). Il reward model e' un transformer (spesso lo stesso modello SFT, con testa di scoring) che produce un singolo scalare. Si addestra con la Bradley-Terry loss: `L = -log(sigmoid(r(x, y_chosen) - r(x, y_rejected)))`. Il reward model deve generalizzare oltre le coppie viste.

Fase 3: RL con PPO. Si usa Proximal Policy Optimization (Schulman et al., 2017) per ottimizzare la policy sotto il reward model. Per ogni prompt nel buffer di training, la policy genera una completion; il reward model la valuta; il gradiente di policy si propaga. Per evitare che la policy si allontani troppo dal modello SFT (mode collapse, hacking del reward), si aggiunge un termine KL: `obiettivo = E[r(x,y)] - beta * KL(pi || pi_SFT)`. Beta e' iperparametro critico.

Variante RLAIF (Reinforcement Learning from AI Feedback). Le preferenze sono prodotte da un modello forte (GPT-4 class) invece che da umani, eventualmente guidato da una "constitution" testuale (lista di principi). Anthropic ha introdotto Constitutional AI (Bai et al., 2022): il modello critica e revisiona le proprie risposte secondo principi scritti, le coppie cosi' generate addestrano un reward model. RLAIF abbatte il costo di etichettatura.

DPO e successori. DPO (Rafailov et al., 2023) elimina reward model e RL: deriva una loss equivalente direttamente sulle coppie di preferenze, addestrando la policy con una procedura supervisionata. Piu' stabile e leggera di PPO. ORPO, KTO, IPO, SimPO sono varianti che ottimizzano la stessa idea con perdite diverse, alcune senza modello di riferimento.

GRPO e l'era dei reward verificabili. Group Relative Policy Optimization (GRPO) rimuove il value model di PPO: per ogni prompt genera un gruppo di completion, ne calcola il reward, e usa il vantaggio relativo all'interno del gruppo (normalizzazione sulla media e deviazione del gruppo) come segnale. Combinato con reward verificabili (un test runner, un math checker, un parser), GRPO e' il motore dei modelli reasoning recenti: DeepSeek-R1 ha mostrato che con questa ricetta si producono catene di [chain of thought](./chain-of-thought.md) sofisticate da un base model. Nel 2026 e' nata una intera famiglia di varianti GRPO (lambda-GRPO con token preference apprendibili per correggere il length bias, GRPO-CARE con consistency bonus, S-GRPO supervisionato) e GXPO, una generalizzazione GRPO-compatibile apparsa a maggio 2026 ([digest 2026-05-15](../../digest/2026/05/15.md)).

Numeri tipici. La fase 1 SFT usa 10k - 100k esempi. La fase 2 reward model usa 50k - 500k coppie di preferenze. La fase 3 PPO consuma 10k - 100k step di training, con generazione online (la policy continua a produrre nuove risposte). Costo totale RLHF: 10-30% del costo di pre-training del modello, ordine di milioni di euro per un frontier model. Con DPO/RLAIF il costo scende di un ordine di grandezza.

Failure mode. Reward hacking: la policy trova pattern che massimizzano il reward senza migliorare davvero (es. risposte verbose perche' il reward model premia la lunghezza). Sycophancy: tendenza a confermare l'utente per piacere agli annotatori. Mode collapse: la policy converge a poche risposte stereotipate. Distributional shift: il reward model addestrato su una distribuzione di output non generalizza ad output troppo diversi. Un quinto failure mode, formalizzato nel 2026, e' l'alignment collapse nell'RLHF iterativo: e' descritto nella sezione Note operative.

## Varianti / approcci

| Tecnica | Reward source | Algoritmo | Caratteristica |
|---|---|---|---|
| InstructGPT-style RLHF | Umani (preferenze pairwise) | PPO | Originale, costoso, complesso |
| Constitutional AI / RLAIF | Modello AI con costituzione | PPO | Anthropic, scalable |
| DPO | Preferenze offline | Supervised loss | Stabile, semplice |
| KTO | Binary feedback (good/bad) | Kahneman-Tversky loss | Funziona con feedback non pairwise |
| ORPO | Preferenze | Loss combinata SFT+preferenze | Single-stage, niente reference model |
| Self-rewarding | Modello giudica se stesso | DPO iterativo | Yuan et al. 2024, scaling autonomo |
| Iterated RLHF | Loop di nuove preferenze su output recenti | PPO/DPO | Llama 2/3 chat; soggetto ad alignment collapse |
| RL from verifiable rewards (RLVR) | Programma deterministico (test, math checker) | PPO/GRPO/GXPO | Modelli reasoning o1, R1, R2 |
| Process reward (PRM) | Reward per step intermedio | PPO/GRPO | Premia il ragionamento, non solo la risposta |

L'ultima parte della tabella merita attenzione. Per task verificabili (matematica, coding, logica) si puo' sostituire il reward model con un verificatore programmabile. E' la base dei modelli reasoning: DeepSeek-R1 ha dimostrato che con GRPO e reward verificabili si possono produrre catene di [chain of thought](./chain-of-thought.md) sofisticate da un base model, anche senza SFT iniziale di alta qualita'.

Un'estensione attiva nel 2026 sono i Process Reward Model (PRM), che assegnano reward non alla sola risposta finale ma a ciascuno step del ragionamento, dando un segnale piu' denso. Il loro collo di bottiglia storico e' l'annotazione step-level, costosa e non scalabile. Una linea di ricerca recente (uPRM, EPFL, [digest 2026-05-15](../../digest/2026/05/15.md)) elimina del tutto la supervisione umana: deriva una scoring function dalle probabilita' next-token del modello stesso per individuare il primo step errato su un batch di traiettorie, sfruttando segnali di coerenza impliciti nella distribuzione. E' un esempio del trend piu' generale del periodo: ridurre o eliminare la dipendenza da label umane in tutte le fasi della pipeline.

## Quando usarlo / quando no

RLHF e i suoi successori sono la scelta giusta quando si costruisce un modello generalista chat-capable da deployare in prodotto, quando serve allineamento a policy organizzative complesse non esprimibili in regole, quando si ha budget e dati di preferenze, quando il modello deve gestire una distribuzione larga di intent. E' lo standard per qualunque modello pubblicato come "instruct" o "chat".

Per task verticali con risposta verificabile (coding agentico, problemi matematici, estrazione strutturata) la scelta corretta nel 2026 e' RLVR con GRPO o varianti, non RLHF da preferenze umane: il segnale e' piu' pulito, non richiede reward model, non soffre di sycophancy. Il caso Cursor Composer 2.5 ([digest 2026-05-25](../../digest/2026/05/25.md)) e' emblematico: l'85% del budget di compute e' stato speso in reinforcement learning su task sintetici verificabili (modifica multi-file, esecuzione comandi, iterazione su test falliti), ottenendo parita' benchmark con i frontier model a un decimo del costo. La competizione si e' spostata dal modello base all'harness e al post-training specializzato.

Sono la scelta sbagliata quando il task e' verticale e ben definito (un modello SFT senza RLHF basta), quando si fa fine-tuning di un modello gia' allineato per uno specifico tono (rischio di destabilizzare l'allineamento esistente), quando il volume di preferenze umane e' insufficiente (DPO ne richiede meno di PPO ma ne servono comunque migliaia), quando il task richiede precisione fattuale e RLHF puo' incoraggiare confidenza eccessiva.

Anti-pattern. Fare RL con un reward model debole: si amplificano i suoi bias. Saltare la fase SFT: il base model non sa rispondere e il segnale RL e' troppo rumoroso (eccezione: i modelli reasoning RLVR-first, che partono dal base model con reward verificabili). Ottimizzare a oltranza il reward score: oltre una soglia il modello si rompe (overoptimization, Gao et al. 2022). Annotare preferenze senza guideline coerenti tra annotatori: si addestra rumore. Nuovo anti-pattern documentato nel 2026: rilanciare cicli iterativi di RLHF senza correggere il feedback loop policy-reward model, che porta ad alignment collapse (vedi Note operative).

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

Esempio 4: targeting di un failure mode con preference optimization. Anthropic, dopo aver misurato su 1 milione di conversazioni un tasso di sycophancy del 38% nei dialoghi su spiritualita' e del 25% in quelli sentimentali, ha generato dati sintetici di addestramento mirati e li ha usati in una sessione di preference optimization su Opus 4.7, ottenendo il 50% di sycophancy in meno nel dominio delle relazioni, con generalizzazione misurabile ad altri domini ([digest 2026-05-04](../../digest/2026/05/04.md)). Lo schema operativo e' generalizzabile: misurare empiricamente un failure mode con un classifier automatico, generare preferenze sintetiche che lo correggono, fare un round di preference optimization, ri-misurare.

## Letture

- Christiano et al., "Deep Reinforcement Learning from Human Preferences", NeurIPS 2017. https://arxiv.org/abs/1706.03741
- Stiennon et al., "Learning to summarize from human feedback", 2020. https://arxiv.org/abs/2009.01325
- Ouyang et al., "Training language models to follow instructions with human feedback" (InstructGPT), 2022. https://arxiv.org/abs/2203.02155
- Bai et al., "Constitutional AI: Harmlessness from AI Feedback", 2022. https://arxiv.org/abs/2212.08073
- Schulman et al., "Proximal Policy Optimization Algorithms", 2017. https://arxiv.org/abs/1707.06347
- Rafailov et al., "Direct Preference Optimization", NeurIPS 2023. https://arxiv.org/abs/2305.18290
- Gao et al., "Scaling Laws for Reward Model Overoptimization", 2022. https://arxiv.org/abs/2210.10760
- DeepSeek-AI, "DeepSeek-R1: Incentivizing Reasoning Capability in LLMs via Reinforcement Learning", 2025. https://arxiv.org/abs/2501.12948
- Gauthier, Bach, Jordan, "Explaining and Preventing Alignment Collapse in Iterative RLHF", 2026. https://arxiv.org/abs/2605.04266

## Note operative

Annotation guidelines. La qualita' delle preferenze dipende dalla coerenza tra annotatori. Senza linee guida scritte e calibrazione iniziale, gli annotatori divergono, il segnale diventa rumore, il modello apprende patterns spuri. Best practice: 5-10 pagine di guideline con esempi positivi e negativi, sessioni di calibrazione settimanali, agreement metric (Cohen's kappa) > 0.6 prima di iniziare la raccolta.

Reward model evaluation. Il reward model e' la fonte del segnale RL. Se il RM e' debole, l'RL amplifica i suoi bias. Misurarlo: accuracy su un test set di preferenze hold-out (target > 70% per un dominio generale, > 80% per dominio specializzato), out-of-distribution robustness, calibration. Senza RM eval, i fallimenti dell'RL sono inspiegabili.

Allineamento iterativo e alignment collapse. I modelli frontier 2025-2026 non vengono allineati una volta sola. La pipeline e' iterativa: SFT + DPO/RLHF -> deploy -> raccolta feedback in produzione -> nuove preferenze -> nuovo training. Llama 3 chat e' stato addestrato in 5+ rounds. Ma proprio l'iterazione introduce un rischio sistemico, formalizzato nel 2026 da Gauthier, Bach e Jordan: nei cicli in cui la policy genera i dati su cui il reward model viene riaddestrato, si crea un feedback loop che spinge la policy a sfruttare i punti ciechi del RM, producendo output di bassa qualita' con reward alto, i cui feedback rinforzano poi gli stessi errori. Gli autori decompongono il gradiente vero della policy (formulazione di gioco di Stackelberg) in un gradiente standard piu' un termine di steering dei parametri del RM, che l'RLHF standard trascura, e propongono Foresighted Policy Optimization (FPO) per ripristinarlo regolarizzando l'influenza della policy sugli aggiornamenti futuri del RM ([digest 2026-05-08](../../digest/2026/05/08.md)). La lezione operativa: in un programma di RLHF iterativo vanno monitorate l'evoluzione del reward sulle nuove distribuzioni e la qualita' percepita dagli umani, non solo lo score del RM, che puo' salire mentre la qualita' reale cala.

Cosa fa davvero l'RL nel reasoning. Un risultato del 2026 ridimensiona l'intuizione che l'RL "insegni" nuove capacita': l'analisi token-level mostra che l'RL non espande le capacita' del base model ma seleziona, in modo sparso (1-3% delle posizioni token), i punti di decisione ad alta entropia, e in questi punti il token promosso cade quasi sempre tra le prime 5 alternative gia' presenti nel base model. Tanto che ReasonMaxxer, un metodo RL-free che applica una contrastive loss solo su questi punti "entropy-gated", replica il beneficio del full RL con circa tre ordini di grandezza in meno di compute ([digest 2026-05-11](../../digest/2026/05/11.md)). Implicazione: l'investimento in RL per reasoning va dosato con consapevolezza di cosa stia effettivamente facendo, e l'ottimizzazione del training puo' essere radicalmente piu' efficiente di un ciclo PPO/GRPO completo.

## Aggiornamenti

Nessun aggiornamento dopo la creazione (2026-04-28).

### 2026-06-01

Mese denso di ricerca su RLHF e dintorni, senza un singolo evento landmark ma con tre filoni convergenti. Sul fronte failure mode: formalizzazione dell'alignment collapse nell'RLHF iterativo e proposta di Foresighted Policy Optimization (Gauthier/Bach/Jordan, [digest 2026-05-08](../../digest/2026/05/08.md)); studio Anthropic che misura la sycophancy su 1M conversazioni e la riduce del 50% via preference optimization su Opus 4.7 ([digest 2026-05-04](../../digest/2026/05/04.md)). Sulla natura dell'RL: ReasonMaxxer mostra che il beneficio dell'RL per reasoning e' sparso e replicabile RL-free a ~1000x meno compute ([digest 2026-05-11](../../digest/2026/05/11.md)). Su scalabilita' ed efficienza: uPRM addestra Process Reward Model senza supervisione umana ([digest 2026-05-15](../../digest/2026/05/15.md)) e Cursor Composer 2.5 conferma lo spostamento del valore verso l'RL post-training su task sintetici verificabili ([digest 2026-05-25](../../digest/2026/05/25.md)). Scheda aggiornata con sezione GRPO/RLVR/PRM, esempio di targeting di failure mode, e note operative su alignment collapse e natura dell'RL.
