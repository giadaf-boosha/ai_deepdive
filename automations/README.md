# automations/

Routine remote Claude Code per ai_deepdive.

## A cosa serve

Ogni mattina alle 07:00 (Europe/Rome) — corrispondenti a `0 5 * * *` UTC — una routine Claude Code remota:

1. Scarica gli aggiornamenti delle ultime 24 ore dalle newsletter e dagli account X elencati in `config/sources.yaml`.
2. Filtra in modo editoriale stretto (max 10 voci, 4 sezioni).
3. Genera un digest in italiano in `digest/YYYY/MM/DD.md`.
4. Aggiorna la knowledge base in `kb/concetti/` (deep dive italiani 1500-3000 parole) e `kb/README.md`.
5. Committa e pusha su `main`.
6. Invia (o crea draft di) un'email a `giada.f@me.com` via Gmail MCP.

Spec di riferimento: [`../spec.md`](../spec.md). Piano: [`../implementation_plan.md`](../implementation_plan.md).

## File in questa cartella

- `whats-new-daily-prompt.md` — prompt completo, self-contained, eseguito dalla routine giornaliera. Single source of truth per il comportamento giornaliero.
- `routine-body.json` — body JSON della routine giornaliera, pronto per `RemoteTrigger create` / `update`. Embedda il prompt nel campo `events[0].data.message.content`.
- `weekly-radar-prompt.md` — prompt completo della routine settimanale `ai-deepdive-weekly-radar` (aggiorna `web/data/models.json`).
- `weekly-radar-body.json` — body JSON della routine settimanale, pronto per `RemoteTrigger create`.
- `README.md` — questo file.

## Routine settimanale: ai-deepdive-weekly-radar

Aggiorna `web/data/models.json` (sezione `/radar` del sito) ogni domenica alle 08:00 Europe/Rome.

- **Cron**: `0 6 * * 0` (UTC) = 08:00 Europe/Rome in CEST, 07:00 in CET.
- **Guard**: il body embedda la stringa `RADAR_UPDATE` in testa al messaggio; il prompt esegue solo se quella stringa e' presente nell'attivazione.
- **Tool**: `Bash`, `Read`, `Write`, `Edit`, `Glob`, `Grep`, `WebFetch`, `WebSearch`. Nessun MCP (no email).
- **Effetto**: commit `chore: weekly radar update YYYY-MM-DD` su `main` -> Vercel ricostruisce il sito.

### Come crearla (da fare una volta)

La routine NON e' ancora creata sul cloud. Per crearla, da claude.ai/code/routines (o via `RemoteTrigger create`) passa il body `weekly-radar-body.json`. Verifica l'`environment_id` (riusa quello della daily: `env_011CUioy7aASAFi9ucxkS4pA`) e che il git source punti a `giadaf-boosha/ai_deepdive`. Dopo la creazione, un run manuale di test verifica che `web/data/models.json` venga aggiornato e committato.

Modifiche al prompt: edita `weekly-radar-prompt.md`, poi rigenera il body (stesso schema dello snippet Python sopra, leggendo `weekly-radar-prompt.md` e anteponendo `RADAR_UPDATE\n\n` al contenuto) e aggiorna la routine con `RemoteTrigger update`.

## Come modificare la routine

Workflow standard:

1. Edita `whats-new-daily-prompt.md`.
2. Rigenera `routine-body.json` (rebuilding embedda il prompt aggiornato e rigenera lo `uuid` dell'evento):
   ```bash
   cd automations
   python3 - <<'PY'
   import json, uuid, pathlib
   prompt = pathlib.Path("whats-new-daily-prompt.md").read_text(encoding="utf-8")
   body = json.loads(pathlib.Path("routine-body.json").read_text(encoding="utf-8"))
   ev = body["job_config"]["ccr"]["events"][0]["data"]
   ev["message"]["content"] = prompt
   ev["uuid"] = str(uuid.uuid4()).lower()
   pathlib.Path("routine-body.json").write_text(json.dumps(body, indent=2, ensure_ascii=False), encoding="utf-8")
   PY
   ```
3. Valida JSON: `python3 -c "import json; json.load(open('routine-body.json'))"`.
4. Aggiorna la routine remota con `RemoteTrigger update` passando il nuovo body (oppure ricrea con `RemoteTrigger create` se non esiste ancora).
5. Commit di `automations/` su `main`.

Modifiche allo schedule: cambia `cron_expression` in `routine-body.json`. Tieni a mente che il cron e' in UTC; `0 5 * * *` corrisponde alle 07:00 Europe/Rome durante l'ora legale (CEST) e alle 06:00 in solare (CET). Se vuoi 07:00 fisse anno tutto, valuta una doppia routine o accetta lo shift stagionale.

## Schedule corrente

- Cron: `0 5 * * *` (UTC).
- Equivalente locale: 07:00 Europe/Rome in CEST, 06:00 in CET.
- `enabled: true`.

## Connettori MCP usati

- **Gmail** (`connector_uuid: 1f477cb1-7cd7-41e6-a246-b63a8a0cdef7`): per inviare l'email mattutina o creare un draft. La routine usa `mcp__claude_ai_Gmail__create_draft` come fallback se l'invio diretto non e' disponibile.

Tool standard abilitati nel context della routine: `Bash`, `Read`, `Write`, `Edit`, `Glob`, `Grep`, `WebFetch`, `WebSearch`. Nessun tool destruttivo aggiuntivo.

## Come testarla manualmente

Trigger manuale fuori schedule:

```
RemoteTrigger run --name ai-deepdive-daily
```

(o l'equivalente UI) — esegue una sola iterazione subito. Verifica:

- Nuovo file `digest/YYYY/MM/DD.md` creato con la struttura attesa.
- File in `kb/concetti/` aggiornati o creati per i concetti che superano la soglia.
- Commit `feat(daily): ai_deepdive YYYY-MM-DD` presente su `main`.
- Email/draft con subject `AI Deepdive — YYYY-MM-DD` in inbox.

In caso di run manuale "dry" (senza commit), eseguila in locale invocando lo stesso prompt da Claude Code CLI puntando al repo, prima di toccare la routine remota.

## Troubleshooting

- **Repo non clean al run**: la routine fa ABORT. Pulisci o stash i cambi non di routine.
- **WebFetch 402/403 su X**: il prompt prevede fallback `WebSearch`. Se anche quello fallisce, la fonte va in `failed_sources` e finisce nelle Note di produzione del digest.
- **Gmail MCP error**: il commit resta valido, l'email salta. Riesegui manualmente il comando di invio o crea draft a mano.
- **Conflitto rebase**: ABORT. Risolvi a mano poi rilancia.

## Note di sicurezza

- Nessun secret embedded nei file di questa cartella.
- Nessun `--force` o `--no-verify` nei comandi git del prompt.
- Tool destruttivi non inclusi nella allowlist.
