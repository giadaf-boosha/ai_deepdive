---
name: Chain of Thought / Reasoning
aliases: [chain of thought, CoT, catena di pensiero, reasoning, ragionamento esplicito, extended thinking]
categoria: tecnica
created: 2026-04-28
last_updated: 2026-06-27
mentions_count: 1
---

# Chain of Thought / Reasoning

## Cos'e

Chain of Thought (CoT) e' la tecnica con cui un [LLM](./llm.md) esplicita una sequenza di passi intermedi di ragionamento prima di produrre la risposta finale. Anziche' rispondere direttamente, il modello scrive "pensa": elenca sotto-problemi, fa calcoli intermedi, valuta alternative, infine sintetizza. La pratica nasce come tecnica di [prompt engineering](./prompt-engineering.md) (chiedere "ragiona passo per passo") e si evolve nel 2024-2025 in una proprieta' addestrata: i "reasoning model" (o1, o3, DeepSeek R1, Gemini Thinking, Claude con extended thinking) producono catene di pensiero come parte del loro comportamento normale, con token speciali che separano "thinking" da "answer".

Il paper fondatore e' "Chain-of-Thought Prompting Elicits Reasoning in Large Language Models" (Wei et al., Google Brain, NeurIPS 2022). Mostra che modelli sufficientemente grandi (>= 60B parametri allora) migliorano drasticamente su task di ragionamento aritmetico, simbolico, commonsense quando il prompt include esempi con catena di ragionamento. Kojima et al. (2022) dimostrano che la stessa cosa accade in zero-shot semplicemente aggiungendo "let's think step by step" al prompt. Da li parte una linea di ricerca: self-consistency (Wang et al., 2022), tree of thoughts (Yao et al., 2023), ReAct, Reflection, Reflexion, e infine i modelli reasoning addestrati con RL su task verificabili (DeepSeek R1, 2025).

L'importanza del reasoning sta nel fatto che cambia qualitativamente cio' che gli LLM possono fare. Su task di matematica olimpica, programmazione competitiva, dimostrazioni formali, il jump da modelli standard a reasoning model e' enorme: AIME 2024 da 13% (GPT-4o) a 83-90% (o1, Claude Sonnet 4 thinking, DeepSeek R1). La frontiera si e' spostata ulteriormente nel 2026: modelli reasoning general-purpose hanno raggiunto il livello medaglia d'oro su olimpiadi di matematica e fisica e in un caso documentato hanno disprovato una congettura aperta da 80 anni in geometria discreta (cfr. sezione Aggiornamenti). Allo stesso tempo il reasoning introduce trade-off (latenza, costo, leggibilita' e fedelta' della catena) che vanno gestiti, e la maturazione del 2026 sta spostando il discorso da "quanto pensare" a "quanto pensare in modo calibrato sul task".

## Come funziona

CoT come prompting (no training extra). Il prompt chiede al modello di esplicitare il ragionamento. Esempi di tecniche:

Few-shot CoT. Si forniscono 2-5 esempi (input, ragionamento, output) nel prompt. Il modello apprende il pattern in-context.

Zero-shot CoT. Aggiungere "ragioniamo passo per passo" o un equivalente. Funziona bene su modelli >= 7-13B parametri ben addestrati.

Self-consistency. Si campionano N catene (con temperature > 0), ognuna produce una risposta, si prende la maggioranza. Funziona quando la risposta finale e' un valore singolo (numero, scelta multipla). Migliora di 5-15 punti sopra greedy CoT.

Tree of Thoughts (ToT). Anziche' una catena lineare, si esplora un albero: ad ogni nodo si propongono N continuazioni, si valutano (con un altro prompt o con il modello stesso come critic), si espande il piu' promettente, si fa backtracking se serve. Costoso ma vince su problemi tipo Game of 24, crossword.

Reasoning come comportamento addestrato (reasoning model). I modelli "thinking" hanno una fase di training dedicata: SFT su catene di alta qualita' + RL con reward verificabili (test passati su problemi di matematica/coding). DeepSeek R1 ha mostrato che il reasoning behavior emerge anche da RL puro (senza SFT iniziale di ragionamenti) tramite GRPO (Group Relative Policy Optimization) con reward sui test verificabili. Il modello impara da solo a produrre catene piu' lunghe, a fare backtracking, a verificare le proprie risposte.

Cosa fa davvero l'RL. Una scoperta del 2026 (paper "Rethinking RL for LLM Reasoning", arXiv 2605.06241) ridimensiona la narrativa secondo cui l'RL "insegna" nuove capacita' di ragionamento. L'analisi token-level su piu' famiglie di modelli e algoritmi mostra che l'RL non espande le capacita' del modello base: redistribuisce probabilita' in modo sparso su un piccolo insieme di punti di decisione ad alta entropia, cioe' i token in cui il modello e' incerto su quale percorso di ragionamento prendere. Il footprint utile dell'RL e' concentrato nell'1-3% delle posizioni token e il token promosso cade quasi sempre tra le prime 5 alternative gia' presenti nel modello base. La catena di pensiero migliore, in altre parole, e' gia' latente nel modello pre-trainato: l'RL la rende piu' probabile in pochi punti critici. Questo ha conseguenze pratiche enormi sul costo del training (cfr. ReasonMaxxer nella tabella e in Aggiornamenti).

A inference time, i reasoning model emettono token "thinking" in un canale separato. OpenAI o1 nasconde i thinking token (ne mostra solo riassunti); Claude extended thinking li espone se l'API lo abilita; DeepSeek R1 li mostra interamente. I thinking token possono essere migliaia o decine di migliaia per problema complesso, con costi 5-50x rispetto a una risposta diretta. Su problemi di difficolta' olimpica i modelli reasoning 2026 generano stabilmente traiettorie che superano i 100K token (cfr. SU-01 in Aggiornamenti).

Test-time compute scaling. Una scoperta importante (OpenAI o1, 2024): la performance scala monotonamente con i token di thinking. Lasciar pensare il modello piu' a lungo (limite max_tokens nel canale thinking) migliora i risultati su task hard fino a un plateau. E' una nuova leva di scaling, ortogonale a parametri e dati di pretraining. Nel 2026 il test-time scaling (TTS) e' diventato una componente standard delle ricette reasoning: combinato con SFT a curriculum e RL a piu' stadi, sposta i modelli sopra le soglie da medaglia d'oro su benchmark di tipo olimpico anche a parametri contenuti.

Controllo del budget di ragionamento. La leva del test-time compute e' oggi esposta come parametro di prodotto. Claude extended thinking accetta un `budget_tokens` esplicito; OpenAI imposta il budget indirettamente via "reasoning effort". Nel 2026 la granularita' di questo controllo e' aumentata: alcuni modelli espongono livelli discreti di reasoning effort (per esempio minimal / low / medium / high / xhigh), e i prodotti consumer iniziano a offrire un pannello "Effort" per regolare quanto calcolo dedicare a una risposta. La direzione e' chiara: il reasoning diventa un dial che l'applicazione regola per task, non un comportamento fisso del modello.

Considerazioni quantitative. Su GSM8K (math problemi semplici), CoT prompting migliora un modello 175B da ~20% a ~57% accuracy (Wei 2022). Self-consistency a 40 campioni porta a ~74%. I reasoning model 2024-2025 superano 95%. Su AIME (matematica olimpica), o1 ha piu' che triplicato la performance di GPT-4o. Il cost per problema risolto puo' essere 10-100x maggiore con reasoning, ma il problema viene risolto. La tendenza 2026 e' duplice: da un lato si spinge la frontiera (olimpiadi, problemi aperti), dall'altro si lavora per abbattere il costo della stessa qualita' (training RL-free, fast mode, routing per difficolta').

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
| RL con reward verificabili | DeepSeek R1, o1, SU-01 | Math, coding |
| Test-time scaling (TTS) | Piu' campioni / catene piu' lunghe a inference | Spingere il solve rate su problemi hard |
| RL-free entropy-gated tuning | Contrastive loss solo sui token ad alta entropia | Replicare il beneficio RL a costo ~1000x inferiore |
| Reasoning effort dial | Livelli discreti di budget (minimal..xhigh) | Calibrare costo/qualita' per task |
| Mixture of reasoning depths | Chiama reasoning model solo se hard | Cost optimization |

Sull'asse "prompt-only vs trained". Prompt CoT e' utile quando si lavora con modelli non reasoning. Reasoning model integrati superano CoT prompting ad ogni task hard, ma costano di piu'. Pattern produttivo: routing automatico - una prima chiamata classifica la difficolta', i casi facili vanno a un modello veloce, i casi hard a un reasoning model. Nel 2026 questo routing tende a essere interno al prodotto, esposto come un controllo di "effort" che l'utente o l'applicazione regolano.

Faithfulness della catena. Una preoccupazione storica: la catena scritta dal modello rispecchia davvero il "ragionamento interno" o e' una post-razionalizzazione? Lavori recenti (Anthropic 2023-2025) mostrano che la fedelta' e' parziale: a volte il modello arriva alla risposta in modi non corrispondenti alla catena scritta. La scoperta del 2026 sull'RL (token entropy-gated) rafforza questa lettura: se la catena di alta qualita' e' gia' latente nel modello base e l'RL si limita a renderla piu' probabile in pochi punti, la catena visibile e' un comportamento appreso che correla con la qualita' della risposta ma non e' garanzia del calcolo effettivo. La catena rimane utile per debugging e auditing ma non e' sempre rappresentazione del calcolo effettivo.

## Quando usarlo / quando no

CoT e' la scelta giusta su task che richiedono multi-step reasoning: matematica, programmazione, problemi logici, planning, calcoli su informazioni dal contesto, decomposizione di task complessi. E' utile in [agent](./agent.md) per esplicitare la pianificazione tra le tool call.

Reasoning model (versione addestrata) e' la scelta giusta quando: il task e' difficile e l'utente accetta latenza > 10s; la qualita' giustifica il costo (10-50x); il dominio ha verifica oggettiva (test, math). Buon use case: problemi STEM, debug di codice complesso, dimostrazioni, planning operations research. Nel 2026 il reasoning si trova anche in contesti prima impensabili, come i voice model real-time, dove un livello di ragionamento configurabile migliora l'instruction following senza rompere il ritmo della conversazione.

CoT e' la scelta sbagliata o sovrabbondante quando: il task e' semplice (classificazione, formattazione, lookup) - la catena rallenta senza migliorare; serve una risposta breve in chat conversazionale; la latenza e' critica (UI live); il task e' creativo (scrittura) - la catena puo' irrigidire. Una controtendenza dei modelli "instant" 2026 e' proprio l'ottimizzazione per velocita' e concisione anziche' per lunghezza di ragionamento: per molti task quotidiani la risposta diretta breve e' preferibile alla catena lunga.

Anti-pattern. Forzare CoT su modelli piccoli (< 7B): la catena si auto-confonde, peggiora la risposta. Lasciare il thinking visibile in prodotti consumer senza UX dedicata: gli utenti vengono distratti. Affidarsi alla catena come "spiegazione affidabile" del ragionamento: e' un proxy, non il ground truth. Pagare per reasoning model su task in cui un modello standard 1/10 del costo basta. Tenere il reasoning effort sempre al massimo "per sicurezza": oltre il plateau si spende senza guadagnare, e per task facili si peggiora latenza e a volte qualita'.

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
    model="claude-opus-4-8",
    max_tokens=16000,
    thinking={"type": "enabled", "budget_tokens": 8000},
    messages=[{"role": "user", "content": "Dimostra che la radice di 2 e' irrazionale."}]
)
```

Il response include un blocco `thinking` con la catena (centinaia o migliaia di token) e un blocco `text` con la risposta finale. Il budget thinking e' parametrico: piu' alto = qualita' maggiore su task hard, piu' costo. In Opus 4.8 il controllo del calcolo dedicato a una risposta e' esposto anche lato prodotto tramite un pannello Effort.

Esempio 3: routing per cost optimization. Pipeline: una prima call con un modello small classifica la query in {easy, medium, hard}. Easy -> small model (1x cost). Medium -> standard model con CoT prompt (3x). Hard -> reasoning model (30x). Distribuzione tipica: 70% easy, 25% medium, 5% hard. Cost medio per query si abbatte del 60-80% rispetto a "tutto sul reasoning model" mantenendo qualita' equivalente sui casi che ne hanno bisogno. Il "dial" di reasoning effort esposto dai modelli 2026 e' una variante nativa di questo routing: invece di cambiare modello si cambia il livello di sforzo sullo stesso modello.

Esempio 4: test-time scaling su problema hard. Su un problema di difficolta' olimpica, una singola generazione diretta puo' restare sotto la soglia di soluzione; aumentare il budget di thinking e/o campionare piu' traiettorie con selezione (TTS) alza il solve rate. Nei risultati 2026 su SU-01 il passaggio da generazione diretta a TTS sposta IMO-ProofBench da circa 57,6% a 70,2%, oltre la gold line IMO. Il prezzo e' una latenza e un consumo di token sostanziali: il TTS si attiva solo quando il valore del risultato lo giustifica.

## Letture

- Wei et al., "Chain-of-Thought Prompting Elicits Reasoning in Large Language Models", NeurIPS 2022. https://arxiv.org/abs/2201.11903
- Kojima et al., "Large Language Models are Zero-Shot Reasoners", NeurIPS 2022. https://arxiv.org/abs/2205.11916
- Wang et al., "Self-Consistency Improves Chain of Thought Reasoning", 2022. https://arxiv.org/abs/2203.11171
- Yao et al., "Tree of Thoughts: Deliberate Problem Solving with Large Language Models", 2023. https://arxiv.org/abs/2305.10601
- OpenAI, "Learning to Reason with LLMs" (o1), 2024. https://openai.com/index/learning-to-reason-with-llms/
- DeepSeek-AI, "DeepSeek-R1: Incentivizing Reasoning Capability in LLMs via RL", 2025. https://arxiv.org/abs/2501.12948
- Snell et al., "Scaling LLM Test-Time Compute Optimally", 2024. https://arxiv.org/abs/2408.03314
- Anthropic, "Tracing the thoughts of a large language model", 2025. https://www.anthropic.com/news/tracing-thoughts-language-model
- "Rethinking RL for LLM Reasoning" (ReasonMaxxer), arXiv 2605.06241, 2026. https://arxiv.org/abs/2605.06241
- Li et al., "Achieving Gold-Medal-Level Olympiad Reasoning via Simple and Unified Scaling" (SU-01), arXiv 2605.13301, 2026. https://arxiv.org/abs/2605.13301

## Note operative

Quando rendere visibile la catena. In molte UI la catena thinking e' un dettaglio tecnico, non un valore per l'utente. Mostrarla puo' confondere o esporre ragionamenti errati che minano la fiducia. Pattern preferibile: mostrare solo la risposta finale come default, con un toggle "mostra ragionamento" per utenti tecnici. In contesti di expert review (medicina, legale) la catena diventa invece centrale: serve come traccia auditabile.

Costi di reasoning. Il thinking e' fatturato ai prezzi output, e puo' essere voluminoso. Su Claude extended thinking il budget va impostato in funzione del task: 1024 token bastano per math semplice, 8000 per math hard, 16000+ per olimpiadi. Su o1, o3 il budget e' impostato indirettamente via "reasoning effort", e i modelli 2026 espongono livelli discreti (per esempio minimal..xhigh) per calibrare costo e qualita'. Esiste una soglia oltre la quale aumentare il budget non migliora piu' la qualita' (plateau): conviene calibrare con un campione di task target.

Reasoning + tool. Combinare reasoning model con [tool use](./tool-use.md) e' particolarmente potente: il modello pensa, decide di chiamare un tool, integra il risultato nel pensiero. Pattern emerso nel 2025 in modelli "agentic reasoning". Cura: se il tool restituisce errore o output non utile, il modello reasoning puo' avviare loop di tentativi prolungati, consumando budget. Mettere limiti rigorosi su numero di iterazioni di reasoning + tool per task.

Costo del training del reasoning. Il risultato 2026 sui token entropy-gated suggerisce che non e' sempre necessario un ciclo RL completo per ottenere il comportamento reasoning: tecniche che applicano una correzione mirata solo ai pochi punti di decisione incerti possono replicare gran parte del beneficio a una frazione del compute. Per chi addestra o fine-tuna modelli reasoning interni, vale la pena valutare queste ricette RL-free prima di impegnare budget GPU in un ciclo RL completo.

## Aggiornamenti

### 2026-06-27

"The Deterministic Horizon: When Extended Reasoning Fails and Tool Delegation Becomes Necessary" (Guo, Wu, Yiu — arXiv:2606.00376, accettato ICML 2026) stabilisce il primo bound teorico formale sul limite del CoT puro in compiti di state-tracking. Il teorema dell'Attention Bottleneck dimostra che nei decoder-only transformer la capacita' di state-tracking e' limitata in modo determinato dalla profondita' del contesto; un modello di errore context-dipendente ne quantifica il decadimento. Il Deterministic Horizon d* — la soglia oltre la quale l'accuratezza crolla super-esponenzialmente — e' empiricamente stimato tra 19 e 31 step su 12 modelli e 8 task domain (SWE-bench, WebArena, SQL-Multi tra gli altri). Oltre quella soglia, il tool-integrated reasoning (reasoning + tool deterministici) ottiene 86-94% contro il 24-42% del CoT puro. Il contributo teorico e' che il limite non e' una questione di scala del modello o di dimensione del contesto, ma di capacita' intrinseca dei decoder-only transformer a mantenere stato deterministico su sequenze lunghe. Il contributo pratico e' una guida operativa: per task che richiedono state-tracking beyond d* — refactoring su codebase grandi, query SQL multi-step, navigazione web multi-hop — il tool use non e' un'ottimizzazione ma una necessita' strutturale. Il paper fornisce anche un metodo per stimare d* su un task specifico senza benchmark formali: tracciare la curva di accuratezza al variare della lunghezza della sequenza e identificare il punto di curvatura. Aggiornate di conseguenza le sezioni Note operative (aggiunto paragrafo su stima di d* per routing), Letture (aggiunto arXiv:2606.00376) e Varianti (aggiunto "tool-integrated reasoning" come variante distinta dal reasoning puro). [Digest 2026-06-27](../../digest/2026/06/27.md)

### 2026-06-01

Mese ricco di sviluppi sul reasoning. Sul fronte training, il paper "Rethinking RL for LLM Reasoning" (arXiv 2605.06241) mostra che l'RL non insegna nuove strategie ma redistribuisce probabilita' su un 1-3% di token ad alta entropia gia' presenti nel modello base; il metodo RL-free ReasonMaxxer replica il beneficio con circa 1000x meno compute ([07/05, digest 11](../../digest/2026/05/11.md)). Sul fronte capacita', SU-01 (arXiv 2605.13301), un 30B-A3B con ricetta SFT a curriculum + RL a due stadi + test-time scaling, raggiunge il livello medaglia d'oro su IMO 2025, USAMO 2026 e IPhO, generando traiettorie oltre 100K token ([14/05, digest 15](../../digest/2026/05/15.md)). Un modello reasoning general-purpose di OpenAI ha inoltre disprovato una congettura di Erdős aperta da 80 anni, verifica firmata Tim Gowers ([20/05, digest 23](../../digest/2026/05/23.md)). Lato prodotto, il reasoning effort diventa un dial: GPT-Realtime-2 espone cinque livelli (minimal..xhigh) in un voice model ([07/05, digest 08](../../digest/2026/05/08.md)) e Claude Opus 4.8 aggiunge un pannello Effort ([28/05, digest 29](../../digest/2026/05/29.md)); in controtendenza, GPT-5.5 Instant e' ottimizzato per concisione anziche' lunghezza di ragionamento ([05/05, digest 06](../../digest/2026/05/06.md)). Aggiornate di conseguenza le sezioni Come funziona, Varianti, Quando usarlo e Note operative.
