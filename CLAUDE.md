# CLAUDE.md — ai_deepdive

> Istruzioni di progetto per le routine remote Claude Code che operano su questo repo.
> Identita' editoriale: italiano sempre, nomi tecnici inglesi inalterati, apostrofi ASCII,
> tono asciutto. Pochi segnali ad alto valore > coverage esaustiva.

Questo repo e' guidato da due routine:

- **`ai-deepdive-daily`** (ID `trig_01U38R2BbWd86ZSZvv9uv5Jy`, cron `0 5 * * *` UTC = 07:00 Europe/Rome) — il prompt completo e self-contained vive in [`automations/whats-new-daily-prompt.md`](./automations/whats-new-daily-prompt.md). NON modificarla da qui.
- **`ai-deepdive-weekly-radar`** (ID `trig_017UcxBB68S2FaiQGQWnNh39`, cron `0 6 * * 0` UTC = 08:00 Europe/Rome) — aggiorna `web/data/models.json`. Prompt in [`automations/weekly-radar-prompt.md`](./automations/weekly-radar-prompt.md). Task sintetico sotto.

---

## Task: Aggiornamento settimanale radar modelli AI

**Trigger**: domenica 08:00 (run solo se il messaggio di attivazione contiene "RADAR_UPDATE")

### Obiettivo
Aggiorna `web/data/models.json` con le novita' dell'ultima settimana sui principali modelli AI.

### Step

1. **Ricerca web** per ogni modello (Claude, ChatGPT/GPT, Gemini, Copilot):
   - Nuovi modelli o versioni rilasciate negli ultimi 7 giorni
   - Variazioni di prezzo API o abbonamenti
   - Nuovi benchmark pubblicati ufficialmente
   - Nuove funzionalita' rilevanti (agenti, multimodale, ecc.)
   - Variazioni ranking LMArena (lmarena.ai)

   Query suggerite:
   - `"Claude" new model site:anthropic.com last week`
   - `"GPT" OR "OpenAI" model pricing update 2026`
   - `"Gemini" Google model benchmark 2026`
   - `"Copilot" Microsoft 365 AI update 2026`
   - `LMArena leaderboard rankings current`

2. **Leggi** `web/data/models.json` per lo stato corrente
3. **Identifica delta** rispetto alla settimana precedente
4. **Aggiorna** `web/data/models.json`:
   - Modifica i campi aggiornati
   - Aggiungi `ChangelogEntry` con i delta trovati e fonti
   - Aggiorna `meta.lastUpdated`, `meta.sourcesChecked`, `meta.nextScheduledUpdate`
   - Se nessuna variazione rilevante: aggiungi entry "Nessuna variazione rilevante"
5. **Valida** con `cd web && npx tsc --noEmit`
6. **Commit**: `chore: weekly radar update [YYYY-MM-DD]`
7. **Push** su main -> Vercel ricostruisce automaticamente

### Regole critiche
- Non inventare dati. Solo variazioni con fonte verificata.
- Prezzi da siti ufficiali (anthropic.com, openai.com, ai.google.dev, microsoft.com).
- Benchmark da pubblicazioni ufficiali vendor o lmarena.ai.
- Non modificare file fuori da `web/data/models.json`.
