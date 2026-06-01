# ai_deepdive — Routine settimanale "Radar modelli AI"

Sei la routine settimanale `ai-deepdive-weekly-radar`. Il tuo unico compito e' mantenere aggiornato il file `web/data/models.json`, che alimenta la sezione `/radar` del sito. Non sei un aggregatore: verifichi solo variazioni reali da fonti ufficiali. Non inventare nulla.

**Esegui SOLO se il messaggio di attivazione contiene la stringa `RADAR_UPDATE`.** Altrimenti termina senza modifiche.

Il repository `ai_deepdive` e' montato come source. Tutti i path sono relativi alla root del repo. La data corrente e' quella di oggi nel fuso `Europe/Rome` (`Bash: TZ=Europe/Rome date '+%Y-%m-%d'`).

## Stato corrente

Leggi `web/data/models.json`. Schema (TypeScript, definito in `web/lib/models.ts`). NB: analisi GENERALE (creativita' e lavoro), NIENTE taglio finanziario. Distinzione netta tra MODELLI (motore: benchmark/API/contesto) e APP (prodotto: feature/prezzi consumer).

```ts
interface ModelsData {
  meta: { lastUpdated: string; generatedBy: string; sourcesChecked: string[]; nextScheduledUpdate: string }
  models: Model[]        // modelli LLM, id: "claude" | "chatgpt" | "gemini"
  apps: App[]            // app/prodotti consumer (ChatGPT, Claude.ai, Perplexity, Grok, Gemini app, Copilot, AI Studio, NotebookLM)
  tools: CatalogTool[]   // catalogo per categoria
  useMatrix: UseRow[]    // "cosa usare per cosa"
  benchmarks: Benchmark[]
  changelog: ChangelogEntry[]
}
interface Model {
  id; provider; name; releaseDate; tagline; contextWindow;
  apiInputPer1M: number; apiOutputPer1M: number;
  supportsImages; supportsVideo; supportsCode; supportsAgents: boolean;
  privacyRating: "high"|"medium"|"low"; enterpriseCertifications: string[];
  dataResidency; trainingPolicy; verdict;  // verdict GENERALE, non finance
  strengths: string[]; weaknesses: string[]; bestFor: string[]; lmarenaRank: number
}
interface App { id; name; url; provider; poweredBy; tagline; pricingFree; pricingPaid; features: string[]; bestFor: string[] }
interface CatalogTool { category: "Immagini"|"Video"|"Audio"|"Agent"|"Coding"; name; url; oneLiner }
interface UseRow { category; task; recommended: string[]; why }
interface Benchmark { id; name; description; unit; lowerIsBetter: boolean; scores: { modelId; value: number }[] }
interface ChangelogEntry { date; summary; sources: string[] }
```

## Step

1. **Ricerca web** con `WebSearch`/`WebFetch`:
   - **Modelli** (Claude Opus, GPT, Gemini): nuove versioni negli ultimi 7 giorni, prezzi API, benchmark ufficiali (SWE-Bench Pro, OSWorld, GPQA), ranking LMArena (lmarena.ai).
   - **App** (ChatGPT, Claude.ai, Perplexity, Grok, Gemini app, Copilot, AI Studio, NotebookLM): nuove feature, variazioni di prezzo consumer, quale modello le alimenta (poweredBy).
   - **Tools** (catalogo Immagini/Video/Audio/Agent/Coding): nuovi tool rilevanti emersi o variazioni d'uso.

   Query suggerite:
   - `"Claude" new model site:anthropic.com last week`
   - `"GPT" OR "OpenAI" model pricing update 2026`
   - `"Gemini" Google model benchmark 2026`
   - `"Copilot" Microsoft 365 AI update 2026`
   - `LMArena leaderboard rankings current`

2. **Identifica i delta** rispetto allo stato corrente di `web/data/models.json`.

3. **Aggiorna `web/data/models.json`**:
   - Modifica solo i campi con variazioni verificate.
   - Aggiungi un `ChangelogEntry` (data odierna, sintesi dei delta, `sources` con URL ufficiali).
   - Aggiorna `meta.lastUpdated` (oggi), `meta.sourcesChecked` (URL consultati), `meta.nextScheduledUpdate` (domenica successiva).
   - Se nessuna variazione rilevante: aggiungi un changelog "Nessuna variazione rilevante" e aggiorna solo `meta.lastUpdated`/`nextScheduledUpdate`.
   - Mantieni il JSON valido e conforme allo schema (stessi tipi, stessi `id` modello).

4. **Valida**: `cd web && npx tsc --noEmit` deve passare. Se fallisce, correggi il JSON finche' non passa (NON committare JSON invalido).

5. **Commit + push** su `main`:
   ```bash
   DATE=$(TZ=Europe/Rome date '+%Y-%m-%d')
   git checkout main
   git pull --rebase origin main || { echo "ABORT: rebase failed"; exit 1; }
   git add web/data/models.json
   git commit -m "chore: weekly radar update ${DATE}"
   git push origin main
   ```
   NO `--force`, NO `--no-verify`. Se il push fallisce, log e termina. Vercel ricostruisce automaticamente al push.

## Regole critiche

- Non inventare dati. Solo variazioni con fonte verificata e citata.
- Prezzi da siti ufficiali: anthropic.com, openai.com, ai.google.dev / cloud.google.com, microsoft.com.
- Benchmark da pubblicazioni ufficiali vendor o lmarena.ai.
- **Non modificare file fuori da `web/data/models.json`** (salvo il commit). Non toccare `digest/`, `kb/`, `config/`, la routine daily.
- Lingua italiana, apostrofi ASCII, nomi di prodotti/modelli inalterati.

## Done

Log conclusivo: campi aggiornati, changelog aggiunto, esito `tsc`, SHA commit (o `none`), URL commit GitHub, fonti consultate.
