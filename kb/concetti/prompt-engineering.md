---
name: Prompt engineering
aliases: [prompt engineering, ingegneria dei prompt, prompting]
categoria: tecnica
created: 2026-04-28
last_updated: 2026-04-28
mentions_count: 0
---

# Prompt engineering

## Cos'e

Il prompt engineering e' la disciplina che progetta e itera gli input testuali per indurre in un [LLM](./llm.md) il comportamento desiderato. E' la prima leva, la piu' rapida e a costo zero, per ottenere output utili: cambiare un prompt e' istantaneo, mentre [fine-tuning](./fine-tuning.md) richiede dati e tempo, e [RAG](./rag.md) richiede infrastruttura. Un buon prompt definisce ruolo, obiettivo, vincoli, formato, esempi, criteri di accettazione. Un cattivo prompt produce risposte vaghe, inconsistenti, fuori scopo.

Il termine emerge nel 2020-2021 con GPT-3 e l'osservazione che la qualita' degli output dipendeva fortemente da come si formulava la query. Brown et al. (2020) descrivono in-context learning e few-shot. Wei et al. (2022) introducono [chain of thought](./chain-of-thought.md). Si moltiplicano pubblicazioni: zero-shot CoT ("let's think step by step", Kojima 2022), self-consistency, tree of thoughts, ReAct, role prompting. Nel 2023-2024 il prompt engineering passa da arte folkloristica a pratica con guideline ufficiali pubblicate da OpenAI, Anthropic, Google, e a curricula formali.

L'importanza pratica e' enorme nei prodotti AI. Le differenze tra una soluzione mediocre e una eccellente, a parita' di modello, derivano spesso da prompt ben strutturati. Per applicazioni high-volume il prompt e' anche un asset economico: ridurre i token di sistema mantenendo la qualita' significa migliaia di euro al mese di risparmio.

## Come funziona

Un prompt efficace combina componenti standardizzabili.

System prompt. Istruzioni stabili che definiscono identita', ruolo, regole. Posizionato all'inizio della conversazione, viene tipicamente cached lato provider per ridurre costi. Buona pratica: descrivere il ruolo ("Sei un assistente legale specializzato in diritto societario italiano"), gli obiettivi ("Rispondi citando articoli del codice civile"), i vincoli ("Non dare consigli su contratti senza consultare un professionista"), il formato di output.

User message. La query attuale. Best practice: essere specifici sul deliverable ("scrivi un'email di max 100 parole, tono formale, rivolgendoti a un CFO"); separare contesto da istruzione (delimitatori XML, markdown, blocchi di codice); fornire input pulito.

Few-shot examples. Esempi (input, output) inclusi nel prompt. Il modello apprende il pattern in-context senza training. 2-5 esempi tipicamente bastano. Funziona meglio quando gli esempi coprono varianti dell'input atteso e quando il pattern e' formale (estrazione, classificazione, traduzione).

Chain of thought. Chiedere al modello di "ragionare passo per passo" prima di rispondere migliora task complessi. Vedi [chain of thought](./chain-of-thought.md).

Output format. Esprimere il formato come schema JSON, lista, tabella, markdown. Modelli moderni supportano structured outputs come feature dell'API; usarli e' piu' robusto che chiedere "rispondi in JSON".

Prompting tecniche avanzate. Self-consistency: campionare N risposte e prendere maggioranza. Tree of thoughts: il modello esplora rami alternativi, valuta, sceglie. Ensembling: chiamare il modello con N prompt diversi e combinare. Role play: assegnare un ruolo aiuta su task specialistici (debate, code review). Negative instructions: dichiarare cosa non fare e' meno efficace di dichiarare cosa fare. Constraint anchoring: ribadire vincoli critici a fine prompt funziona meglio che solo a inizio (recency bias dell'attention).

Esempio strutturale. Una struttura raccomandata Anthropic per prompt complessi:

```
[ruolo e contesto generale]

[istruzioni dettagliate, lista numerata]

<documents>
{documents}
</documents>

<examples>
{few_shot_examples}
</examples>

[query corrente]

[richiesta finale: "pensa passo passo, poi rispondi in formato JSON {schema}"]
```

L'uso di tag XML e' specificamente raccomandato per Claude perche' il training ha visto strutture XML in modo prominente; per GPT/Gemini funziona ugualmente ma anche markdown o JSON di delimitazione vanno bene.

Considerazioni sui costi. Prompt lunghi consumano token a ogni chiamata. Tecniche di mitigazione: prompt caching (vedi [context window](./context-window.md)), compressione del prompt (Microsoft LLMLingua, riducendo del 50-80% token con minima perdita), few-shot dynamic retrieval (selezionare gli esempi piu' rilevanti via [embedding](./embedding.md)).

## Varianti / approcci

| Tecnica | Quando | Nota |
|---|---|---|
| Zero-shot | Task semplici, o per testare il floor | Baseline |
| Few-shot | Pattern ben definito, formato ripetitivo | 2-5 esempi |
| Zero-shot CoT | Reasoning aritmetico, multi-step | "Let's think step by step" |
| Manual CoT | Quando il ragionamento ha forma specifica | Esempio with reasoning |
| Self-consistency | Task con risposta unica | Voting su N campioni |
| Tree of thoughts | Pianificazione, problem solving | Costoso |
| ReAct | Quando il modello deve usare tool | Vedi [tool use](./tool-use.md) |
| Reflection / self-critique | Migliora correttezza | Aggiunge un turno |
| Role prompting | Task specialistici | "Sei un esperto di X" |
| XML tagging | Prompt strutturati lunghi | Raccomandato per Claude |
| Constitutional prompting | Aggiungere principi di policy | Per controllo comportamentale |

Sull'asse "prompt engineering vs altre leve". Prompt engineering risolve problemi di formato, stile, ragionamento immediato. Per fatti aggiornati: [RAG](./rag.md). Per stile profondo o task verticali su volume: [fine-tuning](./fine-tuning.md). Per orchestrazione complessa: [agent](./agent.md). Per integrazione tool: [tool use](./tool-use.md). Spesso si combinano.

## Quando usarlo / quando no

Il prompt engineering e' il primo strumento da provare sempre. E' la scelta giusta in fase prototipale, per task one-off, per esperimenti rapidi, per costruire un baseline prima di investire in fine-tuning. E' essenziale anche quando si lavora su modelli closed senza accesso ai pesi.

E' insufficiente quando: il task richiede conoscenza fattuale che non sta nel modello (serve [RAG](./rag.md)); serve consistenza estrema su volume (serve fine-tuning o constrained decoding); il prompt diventa enorme e fragile (segnale che sta facendo cose che dovrebbero essere in pipeline esterna); le metriche di qualita' non migliorano oltre una soglia con prompt iteration (sintomo che il modello base non ha la capacita' richiesta).

Anti-pattern. Prompt da paragrafi prolissi senza struttura: rumorosi, inconsistenti. Iterazione senza eval: senza un dataset di test misurabile, "sembra meglio" e' soggettivo. Aggiungere istruzioni "non fare X" senza esempi positivi: il modello a volte le ignora. Mescolare lingue mid-prompt senza necessita'. Usare placeholder mai sostituiti (`{{user_name}}` lasciato grezzo): rotture in produzione. Trattare il prompt come specifica: il modello e' probabilistico, non deterministico, va validato.

## Esempi pratici

Esempio 1: estrazione strutturata. Da bozza zero-shot a prompt strutturato.

Brutto: "Estrai informazioni da questo testo".

Buono:

```
Sei un parser di curriculum. Estrai dal testo seguente le informazioni in formato JSON valido che rispetti questo schema:
{"name": str, "email": str, "years_experience": int, "skills": [str]}

Se un campo non e' presente, usa null. Non aggiungere campi non richiesti. Non includere testo prima o dopo il JSON.

<cv>
{cv_text}
</cv>
```

Differenza: ruolo, schema esplicito, gestione missing, vincolo di output. Tasso di errore di parsing scende da ~15% a < 1%.

Esempio 2: chain of thought su problema matematico.

```
Risolvi il problema seguente. Prima ragiona passo per passo dentro <thinking></thinking>, poi dai la risposta finale dentro <answer></answer>.

Problema: un negozio applica uno sconto del 20% su un articolo da 80 euro, poi una tassa del 22%. Quanto paga il cliente?
```

Risultato tipico: il modello scrive il calcolo intermedio (80 * 0.8 = 64; 64 * 1.22 = 78.08) e l'answer finale. Su benchmark GSM8K, CoT migliora la accuracy di 30+ punti rispetto a no-CoT su modelli pre-2024.

Esempio 3: role + few-shot per classificazione.

```
Sei un classificatore di intent per supporto clienti telco. Le categorie sono: BILLING, TECHNICAL, SALES, OTHER.

Esempi:
"Non riesco a connettermi alla rete" -> TECHNICAL
"Vorrei cambiare piano tariffario" -> SALES
"Perche' la mia bolletta e' raddoppiata?" -> BILLING

Classifica:
"Il modem mi sta lampeggiando rosso" ->
```

Senza esempi, il modello a volte produce categorie inventate o rispuegamenti. Con 3 esempi, si stabilizza al 95%+ di accuracy su un test set realistico.

## Letture

- Brown et al., "Language Models are Few-Shot Learners", 2020. https://arxiv.org/abs/2005.14165
- Wei et al., "Chain-of-Thought Prompting Elicits Reasoning in Large Language Models", 2022. https://arxiv.org/abs/2201.11903
- Kojima et al., "Large Language Models are Zero-Shot Reasoners", 2022. https://arxiv.org/abs/2205.11916
- Wang et al., "Self-Consistency Improves Chain of Thought Reasoning", 2022. https://arxiv.org/abs/2203.11171
- Yao et al., "Tree of Thoughts: Deliberate Problem Solving with Large Language Models", 2023. https://arxiv.org/abs/2305.10601
- Anthropic, "Prompt engineering overview". https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering
- OpenAI, "Prompt engineering guide". https://platform.openai.com/docs/guides/prompt-engineering
- "The Prompt Report", Schulhoff et al. 2024 (survey di 58 tecniche). https://arxiv.org/abs/2406.06608

## Note operative

Versionamento dei prompt. In produzione i prompt sono codice: vanno versionati, code-reviewati, testati. Tenere prompt in stringhe inline nei sorgenti e' un anti-pattern dopo la fase di prototipazione. Pattern raccomandato: file dedicati (prompts/extract.md, prompts/system.md), caricamento programmatico, hash del prompt loggato in telemetria per correlare risposte a versione.

Eval sui prompt. Senza eval, modificare un prompt e' una scommessa. Buona pratica: dataset di 50-200 esempi (input, output atteso o criterio di accettazione), funzione di scoring (exact match, regex, LLM-as-judge per task soggettivi), CI che gira ad ogni PR sul prompt. Su task con risposta unica, exact match basta; su generazione, LLM-as-judge con criteri espliciti e' robusto se il giudice e' di tier almeno pari.

Adattamento al modello. I prompt non sono universali. Un prompt che funziona su Claude puo' essere subottimale su GPT o Gemini, e viceversa. Anthropic raccomanda XML tagging, OpenAI predilige markdown, Gemini ha sue idiosincrasie. Quando si fa migrazione tra modelli, il porting del prompt deve essere accompagnato da retesting completo, non solo da ri-deploy.

## Aggiornamenti

Nessun aggiornamento dopo la creazione (2026-04-28).
