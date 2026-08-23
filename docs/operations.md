# Operations runbook

Stato: MVP pronto per shadow run; nessuna schedule o delivery live attivata.

## Runtime scelto

Un solo ambiente principale mantiene il progetto: una VM Linux persistente con Python 3.11+, timezone `Europe/Rome`, repository del codice in `/srv/ai-deepdive` e dati privati in `/var/lib/ai-intelligence`. Il modello editoriale e' un adapter, non l'orchestratore dell'infrastruttura. Codex o Claude Code possono modificare il codice, ma la produzione esegue la CLI versionata.

Grok.com resta ricerca manuale; Grok Bot non e' parte del runtime. X usa esclusivamente API ufficiali.

## Installazione VM

Eseguire come utente di servizio non-root dedicato:

```bash
git clone https://github.com/giadaf-boosha/ai_deepdive.git /srv/ai-deepdive
cd /srv/ai-deepdive
python3 -m venv .venv
.venv/bin/pip install -e .
install -d -m 700 /var/lib/ai-intelligence
export AI_INTEL_DATA_DIR=/var/lib/ai-intelligence
.venv/bin/ai-intel --config config/intelligence.example.toml init
```

Il secret manager o l'environment file leggibile solo dall'utente di servizio contiene, quando abilitati:

```text
AI_INTEL_DATA_DIR
ICLOUD_IMAP_USERNAME
ICLOUD_IMAP_PASSWORD
GMAIL_IMAP_USERNAME
GMAIL_IMAP_PASSWORD
X_BEARER_TOKEN
X_USER_ACCESS_TOKEN
SMTP_USERNAME
SMTP_PASSWORD
EDITORIAL_PROVIDER_TOKEN
```

`X_USER_ID` non e' un segreto, ma va configurato come dato operativo. Nessun valore deve essere inserito nel repository.

## Acquisizione manuale del pilot

### RSS/Atom

```bash
ai-intel --config config/intelligence.example.toml ingest-rss \
  --source-id simon-willison \
  --url https://simonwillison.net/atom/everything/
```

Ogni fonte ha stato ETag, Last-Modified e ID gia' visti nel data dir privato.

### iCloud e Gmail

```bash
ai-intel --config config/intelligence.example.toml ingest-imap \
  --source-id icloud-ai-top \
  --host imap.mail.me.com \
  --mailbox Newsletter/AI_TOP \
  --username-env ICLOUD_IMAP_USERNAME \
  --password-env ICLOUD_IMAP_PASSWORD

ai-intel --config config/intelligence.example.toml ingest-imap \
  --source-id gmail-newsletters \
  --host imap.gmail.com \
  --mailbox INBOX \
  --username-env GMAIL_IMAP_USERNAME \
  --password-env GMAIL_IMAP_PASSWORD
```

IMAP usa `UIDVALIDITY` e UID incrementali. Il raw body resta privato; il connector estrae un link HTTPS editoriale quando presente.

### X watchlist

```bash
ai-intel --config config/intelligence.example.toml ingest-x \
  --handle karpathy \
  --handle ylecun \
  --handle swyx \
  --handle simonw \
  --handle jeremyphoward \
  --handle _akhaliq
```

La CLI aggrega gli handle, usa `since_id`, conserva la paginazione incompleta e prenota atomicamente nel ledger il costo massimo della run. Dopo il risultato riconcilia la reservation con le risorse ricevute. Il hard cap rispetta quindi sia `x_max_posts_per_run` sia il budget mensile residuo, anche con run manuali o concorrenti. Il pilot parte dai sei account sempre-inclusi; l'espansione alla watchlist completa avviene soltanto dopo il benchmark.

### For You

Giada salva i post interessanti in una cartella bookmark X. La pipeline importa i bookmark con OAuth user context:

```bash
ai-intel --config config/intelligence.example.toml ingest-x-bookmarks \
  --user-id "$X_USER_ID"
```

Non esiste scrolling automatico del feed.

## Curazione e preview

```bash
ai-intel --config config/intelligence.example.toml curate
ai-intel --config config/intelligence.example.toml render \
  --slot am \
  --at 2026-08-24T07:00:00+02:00
```

Senza gateway configurato viene usata la baseline deterministica e la confidenza resta `low`. Il digest, HTML e `.eml` vengono scritti nell'outbox privata. Non viene eseguito alcun invio.

Un gateway editoriale model-independent puo' essere collegato con `--provider-endpoint` solo dopo che esiste un endpoint HTTPS reale e autenticato. Non viene indicato un URL fittizio: il gateway non e' ancora stato deployato. Il sistema valida completezza, event ID, enum e minuti prima di usare la risposta.

## Gate prima dell'invio

Per cinque giorni lavorativi:

1. acquisizione e render manuali;
2. zero `--send`;
3. confronto con fonti primarie e gold set;
4. verifica doppioni, copertura, tempi di lettura e costo;
5. approvazione esplicita della qualita' dei digest.

Solo dopo il gate, un invio personale usa:

```bash
ai-intel --config config/intelligence.example.toml render --slot am --send
```

La recipient allowlist contiene solo `giada.f@me.com`. Un destinatario diverso viene bloccato prima della connessione SMTP.

## Schedule target

Il scheduler deve essere timezone-aware, non un cron UTC fisso:

```text
Mon..Fri 07:00:00 Europe/Rome  -> acquisizione, curate, render am, eventuale send
Mon..Fri 21:00:00 Europe/Rome  -> acquisizione, curate, render pm, eventuale send
Sat      09:00:00 Europe/Rome  -> curate, render weekly, eventuale send
```

Ogni job deve avere lock esclusivo e idempotency key. L'attivazione systemd viene fatta sulla VM soltanto dopo gli shadow run, perche' percorso dell'utente di servizio, secret manager e comando di acquisizione batch dipendono dall'ambiente reale.

## Backup e osservabilita'

- backup cifrato giornaliero del database e degli state file;
- retention raw definita per access class;
- alert per run mancante, connector fallito, coverage gap e budget >=80%;
- nessun auto-recharge X nel pilot;
- log senza body email, token o contenuti paywalled;
- restore testato prima di abilitare la delivery.

## Riconciliazione dei casi ambigui

SMTP non offre una idempotency key end-to-end. Il sistema prenota quindi la delivery prima della connessione. Se il processo cade dopo l'accettazione del server ma prima del salvataggio, la delivery resta `PENDING` o viene marcata `BLOCKED`: non viene ritentata automaticamente.

```bash
ai-intel --config config/intelligence.example.toml delivery-status
ai-intel --config config/intelligence.example.toml resolve-delivery \
  --id delivery_ID \
  --outcome sent
```

Dopo aver verificato la mailbox:

- `sent` chiude la delivery;
- `failed` dichiara che l'email non e' stata inviata e consente un retry;
- `blocked` mantiene il blocco.

Analogamente, una chiamata X interrotta dopo una o piu' pagine conserva la reservation massima, per non sottostimare il costo. Confrontare la Developer Console prima di riconciliarla:

```bash
ai-intel --config config/intelligence.example.toml cost-status
ai-intel --config config/intelligence.example.toml reconcile-cost \
  --reservation-key RESERVATION_KEY \
  --actual-usd 0.125
```

Usare `--release` soltanto quando la console conferma costo zero.

## Rollback

La v2 vive accanto alla routine legacy. In caso di errore si disabilita la nuova schedule; non si cancella il database e non si riattiva automaticamente alcuna pubblicazione. La vecchia routine resta baseline finche' la v2 non supera i criteri in `spec.md`.
