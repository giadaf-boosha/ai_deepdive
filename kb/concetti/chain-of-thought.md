---
name: Chain of Thought / Reasoning
aliases: [chain of thought, CoT, catena di pensiero, reasoning, ragionamento esplicito, extended thinking]
categoria: tecnica
created: 2026-04-28
last_updated: 2026-04-28
mentions_count: 0
---

# Chain of Thought / Reasoning

## Cos'e

Chain of Thought (CoT) e' la tecnica con cui un [LLM](./llm.md) esplicita una sequenza di passi intermedi di ragionamento prima di produrre la risposta finale. Anziche' rispondere direttamente, il modello scrive "pensa": elenca sotto-problemi, fa calcoli intermedi, valuta alternative, infine sintetizza. La pratica nasce come tecnica di [prompt engineering](./prompt-engineering.md) (chiedere "ragiona passo per passo") e si evolve nel 2024-2025 in una proprieta' addestrata: i "reasoning model" (o1, o3, DeepSeek R1, Gemini Thinking, Claude con extended thinking) producono catene di pensiero come parte del loro comportamento normale, con token speciali che separano "thinking" da "answer".

Il paper fondatore e' "Chain-of-Thought Prompting Elicits Reasoning in Large Language Models" (Wei et al., Google Brain, NeurIPS 2022). Mostra che modelli sufficientemente grandi (>= 60B parametri allora) migliorano drasticamente su task di ragionamento aritmetico, simbolico, commonsense quando il prompt include esempi con catena di ragionamento. Kojima et al. (2022) dimostrano che la stessa cosa accade in zero-shot semplicemente aggiungendo "let's think step by step" al prompt. Da li parte una linea di ricerca: self-consistency (Wang et al., 2022), tree of thoughts (Yao et al., 2023), ReAct, Reflection, Reflexion, e infine i modelli reasoning addestrati con RL su task verificabili (DeepSeek R1, 2025).

L'importanza del reasoning sta nel fatto che cambia qualitativamente cio' che gli LLM possono fare. Su task di matematica olimpica, programmazione competitiva, dimostrazioni formali, il jump da modelli standard a reasoning model e' enorme: AIME 2024 da 13% (GPT-4o) a 83-90% (o1, Claude Sonnet 4 thinking, DeepSeek R1). Allo stesso tempo introduce trade-off (latenza, costo, leggibilita' della catena) che vanno gestiti.

## Come funziona

CoT come prompting (no training extra). Il prompt chiede al modello di esplicitare il ragionamento. Esempi di tecniche:

Few-shot CoT. Si forniscono 2-5 esempi (input, ragionamento, output) nel prompt. Il modello apprende il pattern in-context.

Zero-shot CoT. Aggiungere "ragioniamo passo per passo" o un equivalente. Funziona bene su modelli >= 7-13B parametri ben addestrati.

Self-consistency. Si campionano N catene (con temperature > 0), ognuna produce una risposta, si prende la maggioranza. Funziona quando la risposta finale e' un valore singolo (numero, scelta multipla). Migliora di 5-15 punti sopra greedy CoT.

Tree of Thoughts (ToT). Anziche' una catena lineare, si esplora un albero: ad ogni nodo si propongono N continuazioni, si valutano (con un altro prompt o con il modello stesso come critic), si espande il piu' promettente, si fa backtracking se serve. Costoso ma vince su problemi tipo Game of 24, crossword.

Reasoning come comportamento addestrato (reasoning model). I modelli "thinking" hanno una fase di training dedicata: SFT su catene di alta qualita' + RL con reward verificabili (test passati su problemi di matematica/coding). DeepSeek R1 ha mostrato che il reasoning behavior emerge anche da RL puro (senza SFT iniziale di ragionamenti) tramite GRPO (Group Relative Policy Optimization) con reward sui test verificabili. Il modello impara da solo a produrre catene piu' lunghe, a fare backtracking, a verificare le proprie risposte.

A inference time, i reasoning model emettono token "thinking" in un canale separato. OpenAI o1 nasconde i thinking token (ne mostra solo riassunti); Claude extended thinking li espone se l'API lo abilita; DeepSeek R1 li mostra interamente. I thinking token possono essere migliaia o decine di migliaia per problema complesso, con costi 5-50x rispetto a una risposta diretta.

Test-time compute scaling. Una scoperta importante (OpenAI o1, 2024): la performance scala monotonamente con i token di thinking. Lasciar pensare il modello piu' a lungo (limite max_tokens nel canale thinking) migliora i risultati su task hard fino a un plateau. E' una nuova leva di scaling, ortogonale a parametri e dati di pretraining.

Considerazioni quantitative. Su GSM8K (math problemi semplici), CoT prompting migliora un modello 175B da ~20% a ~57% accuracy (Wei 2022). Self-consistency a 40 campioni porta a ~74%. I reasoning model 2024-2025 superano 95%. Su AIME (matematica olimpica), o1 ha piu' che triplicato la performance di GPT-4o. Il cost per problema risolto puo' essere 10-100x maggiore con reasoning, ma il problema viene risolto.

## Varianti / approcci

| Tecnica | Idea | Quando |
|---|---|---|
| Few-shot CoT | Esempi con ragionamento in prompt | Pattern specifico di reasoning |
| Zero-shot CoT | "Ragiona passo per passo" | Default semplice |
| Self-consistency | N campioni + voto | Risposte discrete |
| Tree of Thoughts | Esplorazione albero | Pianificazione, problemi puzzle |
| Least-to-most prompting | Decompose -> solve | Problemi gerarchici |
| Self-refine / Reflection | Critica e revisione | Code, scritti |
| Verification | Modello verifica la propria risposta | Task con verificatore esterno |
| Process Reward Model | RM sui passi intermedi, non solo output | Training reasoning robusto |
| RL con reward verificabili | DeepSeek R1, o1 | Math, coding |
| Mixture of reasoning depths | Chiama reasoning model solo se hard | Cost optimization |

Sull'asse "prompt-only vs trained". Prompt CoT e' utile quando si lavora con modelli non reasoning. Reasoning model integrati superano CoT prompting ad ogni task hard, ma costano di piu'. Pattern produttivo: routing automatico - una prima chiamata classifica la difficolta', i casi facili vanno a un modello veloce, i casi hard a un reasoning model.

Faithfulness della catena. Una preoccupazione storica: la catena scritta dal modello rispecchia davvero il "ragionamento interno" o e' una post-razionalizzazione? Lavori recenti (Anthropic 2023-2025) mostrano che la fedelta' e' parziale: a volte il modello arriva alla risposta in modi non corrispondenti alla catena scritta. La catena rimane utile per debugging e auditing ma non e' sempre rappresentazione del calcolo effettivo.

## Quando usarlo / quando no

CoT e' la scelta giusta su task che richiedono multi-step reasoning: matematica, programmazione, problemi logici, planning, calcoli su informazioni dal contesto, decomposizione di task complessi. E' utile in [agent](./agent.md) per esplicitare la pianificazione tra le tool call.

Reasoning model (versione addestrata) e' la scelta giusta quando: il task e' difficile e l'utente accetta latenza > 10s; la qualita' giustifica il costo (10-50x); il dominio ha verifica oggettiva (test, math). Buon use case: problemi STEM, debug di codice complesso, dimostrazioni, planning operations research.

CoT e' la scelta sbagliata o sovrabbondante quando: il task e' semplice (classificazione, formattazione, lookup) - la catena rallenta senza migliorare; serve una risposta breve in chat conversazionale; la latenza e' critica (UI live); il task e' creativo (scrittura) - la catena puo' irrigidire.

Anti-pattern. Forzare CoT su modelli piccoli (< 7B): la catena si auto-confonde, peggiora la risposta. Lasciare il thinking visibile in prodotti consumer senza UX dedicata: gli utenti vengono distratti. Affidarsi alla catena come "spiegazione affidabile" del ragionamento: e' un proxy, non il ground truth. Pagare per reasoning model su task in cui un modello standard 1/10 del costo basta.

## Esempi pratici

Esempio 1: zero-shot CoT prompt.

```
Risolvi il problema seguente. Pensa passo per passo dentro <thinking></thinking>.
Dai la risposta finale dentro <answer></answer>.

Problema: una scatola contiene 12 sfere rosse e 8 blu. Estraendo 3 sfere senza reimmissione, qual e' la probabilita' che siano tutte rosse?
```

Risultato tipico: il modello calcola 12/20 * 11/19 * 10/18 = 1320/6840 ≈ 0.193. Senza CoT i modelli pre-reasoning sbagliavano sistematicamente questa categoria.

Esempio 2: extended thinking con Claude.

```python
client.messages.create(
    model="claude-opus-4-5",
    max_tokens=16000,
    thinking={"type": "enabled", "budget_tokens": 8000},
    messages=[{"role": "user", "content": "Dimostra che la radice di 2 e' irrazionale."}]
)
```

Il response include un blocco `thinking` con la catena (centinaia o migliaia di token) e un blocco `text` con la risposta finale. Il budget thinking e' parametrico: piu' alto = qualita' maggiore su task hard, piu' costo.

Esempio 3: routing per cost optimization. Pipeline: una prima call con un modello small classifica la query in {easy, medium, hard}. Easy -> small model (1x cost). Medium -> standard model con CoT prompt (3x). Hard -> reasoning model (30x). Distribuzione tipica: 70% easy, 25% medium, 5% hard. Cost medio per query si abbatte del 60-80% rispetto a "tutto sul reasoning model" mantenendo qualita' equivalente sui casi che ne hanno bisogno.

## Letture

- Wei et al., "Chain-of-Thought Prompting Elicits Reasoning in Large Language Models", NeurIPS 2022. https://arxiv.org/abs/2201.11903
- Kojima et al., "Large Language Models are Zero-Shot Reasoners", NeurIPS 2022. https://arxiv.org/abs/2205.11916
- Wang et al., "Self-Consistency Improves Chain of Thought Reasoning", 2022. https://arxiv.org/abs/2203.11171
- Yao et al., "Tree of Thoughts: Deliberate Problem Solving with Large Language Models", 2023. https://arxiv.org/abs/2305.10601
- OpenAI, "Learning to Reason with LLMs" (o1), 2024. https://openai.com/index/learning-to-reason-with-llms/
- DeepSeek-AI, "DeepSeek-R1: Incentivizing Reasoning Capability in LLMs via RL", 2025. https://arxiv.org/abs/2501.12948
- Snell et al., "Scaling LLM Test-Time Compute Optimally", 2024. https://arxiv.org/abs/2408.03314
- Anthropic, "Tracing the thoughts of a large language model", 2025. https://www.anthropic.com/news/tracing-thoughts-language-model

## Note operative

Quando rendere visibile la catena. In molte UI la catena thinking e' un dettaglio tecnico, non un valore per l'utente. Mostrarla puo' confondere o esporre ragionamenti errati che minano la fiducia. Pattern preferibile: mostrare solo la risposta finale come default, con un toggle "mostra ragionamento" per utenti tecnici. In contesti di expert review (medicina, legale) la catena diventa invece centrale: serve come traccia auditabile.

Costi di reasoning. Il thinking e' fatturato ai prezzi output, e puo' essere voluminoso. Su Claude extended thinking il budget va impostato in funzione del task: 1024 token bastano per math semplice, 8000 per math hard, 16000+ per olimpiadi. Su o1, o3 il budget e' impostato indirettamente via "reasoning effort". Esiste una soglia oltre la quale aumentare il budget non migliora piu' la qualita' (plateau): convene calibrare con un campione di task target.

Reasoning + tool. Combinare reasoning model con [tool use](./tool-use.md) e' particolarmente potente: il modello pensa, decide di chiamare un tool, integra il risultato nel pensiero. Pattern emerso nel 2025 in modelli "agentic reasoning". Cura: se il tool restituisce errore o output non utile, il modello reasoning puo' avviare loop di tentativi prolungati, consumando budget. Mettere limiti rigorosi su numero di iterazioni di reasoning + tool per task.

## Aggiornamenti

Nessun aggiornamento dopo la creazione (2026-04-28).
