# Strategia di retrieval da X

Data decisione: 2026-08-23  
Stato: strategia target da validare con benchmark, non autorizzazione a eseguire chiamate reali.

## Decisione

X viene trattato come un sottosistema con quattro corsie differenti:

1. **Watchlist controllata**: X API ufficiale, incrementale, per gli account `alert-si`.
2. **Discovery semantica**: xAI API con `x_search`, per trovare segnali fuori dalla watchlist e cluster conversazionali.
3. **Serendipity personale**: bookmark manuale dei post interessanti nel vero `For You`, poi acquisizione tramite Bookmarks API ufficiale.
4. **Audit editoriale**: Grok.com usato manualmente su query campione per confrontare cio' che una ricerca consumer trova rispetto alla pipeline.

Grok Bot non e' il motore X predefinito. E' un ambiente persistente di orchestrazione; l'accesso a X deve comunque passare da un meccanismo autorizzato e misurabile. L'automazione browser del `For You` non entra nel target.

## Perche' non esiste un unico canale

- La watchlist richiede recall, finestre temporali e post ID riproducibili.
- La discovery richiede ricerca semantica e puo' accettare recall non deterministica.
- Il `For You` e' personale, volatile e non ricostruibile a posteriori.
- Grok.com puo' decidere se cercare o meno nei post pubblici di X; X lo descrive come una decisione del prodotto, non come una garanzia di copertura ([About Grok](https://help.x.com/en/using-x/about-grok)).
- Grok Bot ha VM, browser, filesystem e login persistenti, condivisi tra tutti i Bot dello stesso utente; non costituisce un isolamento di credenziali tra Bot ([Grok Bot overview](https://docs.x.ai/grok-bot/overview)).

## Matrice dei canali

| Canale | Punto di forza | Limite | Ruolo |
|---|---|---|---|
| X API | Output strutturato, post ID, author ID, timestamp, paginazione | Costo per risorsa e policy X | Fonte canonica watchlist/bookmark |
| xAI `x_search` | Keyword, semantic, user e thread search con citazioni | Ricerca agentica non esaustiva; costi token + tool | Discovery e controprova |
| Grok.com | Accesso consumer rapido a X e web incluso nel prodotto | Non schedulabile, non deterministico, export debole | Benchmark manuale |
| Grok Bot | Routine persistenti e integrazione multi-app | Login condivisi; browser non equivale ad API X | Orchestrazione non-X, se utile |
| Browser sul `For You` | Feed personale reale | Fragile, non riproducibile, rischio di non conformita' | Escluso dall'automazione |
| Bookmark manuali + API | Giudizio umano sul vero feed, acquisizione strutturata | Richiede gesto manuale | Corsia serendipity consigliata |

## Watchlist controllata

### Input

- account sempre inclusi;
- account `alert-si`, suddivisi per `labs_org`, `people_research`, `product_agent_stack`, `press_strategy`;
- watermark per account o endpoint;
- limite hard di post e dollari per run.

### Output minimo per post

```text
platform_post_id
author_id
author_handle
created_at
canonical_url
text_hash
conversation_id
referenced_post_ids
retrieved_at
retrieval_channel
raw_payload_pointer
cost_usd
```

I record vengono deduplicati per `platform_post_id`; quote, reply e repost restano relazioni, non copie indipendenti della stessa notizia.

### Regola editoriale

Un post non diventa automaticamente un evento. Deve contenere almeno uno tra:

- annuncio originale;
- evidenza tecnica verificabile;
- collegamento a fonte primaria;
- interpretazione unica di una persona nella watchlist;
- segnale che merita verifica fuori da X.

Rumor e claim senza conferma restano `unverified` e non entrano nel digest come fatto.

## Discovery con xAI X Search

La documentazione ufficiale dichiara keyword search, semantic search, user search e thread fetch. `allowed_x_handles` accetta al massimo 20 handle e puo' essere combinato con una finestra `from_date`/`to_date`; una watchlist di circa 59 account richiede quindi almeno tre gruppi logici per una sweep completa ([xAI X Search](https://docs.x.ai/developers/tools/x-search)).

Impostazione proposta:

- massimo 3 chiamate per i tre gruppi watchlist quando serve una controprova;
- massimo 3 chiamate aperte per discovery tematica;
- `max_turns` basso e conteggio delle chiamate effettivamente riuscite;
- salvataggio di citazioni, query, filtri, modello, token e tool usage;
- nessuna sostituzione silenziosa della fonte primaria con la sintesi di Grok.

xAI applica costo token e costo per invocazione; al 23 agosto 2026 `x_search` e' indicato a 5 USD per 1.000 chiamate riuscite, oltre ai token ([xAI pricing](https://docs.x.ai/developers/pricing)). Il modello puo' effettuare piu' tool call nella stessa richiesta: il ledger deve usare `server_side_tool_usage`, non il numero di richieste HTTP ([tool usage details](https://docs.x.ai/developers/tools/tool-usage-details)).

## Corsia `For You`

### Decisione conservativa

Non automatizzare scrolling, parsing DOM o scraping del feed. Giada salva manualmente i post rilevanti nei bookmark o in una cartella bookmark dedicata; il sistema li importa via API.

La [Bookmarks API](https://docs.x.com/x-api/posts/bookmarks/introduction) rende i bookmark privati e disponibili soltanto all'utente autenticato. Richiede OAuth user context. Questo percorso non replica tutto il `For You`, ma conserva esattamente il segnale che Giada ha giudicato interessante.

### Misura del blind spot

Una volta a settimana Giada valuta un campione del feed per 10 minuti e marca:

- post gia' acquisito dalla watchlist;
- post trovato da discovery;
- post nuovo salvato come bookmark;
- rumore.

Il rapporto `nuovi bookmark rilevanti / post rilevanti osservati` misura il valore marginale del `For You`. Se scende stabilmente sotto il 10%, il campione puo' essere ridotto; se supera il 30%, si amplia la discovery, non lo scraping.

## Cost model e guardrail

La X API e' pay-per-use. La documentazione del 23 agosto 2026 indica 0,005 USD per Post letto; gli owned reads dell'utente autenticato, inclusi i bookmark, costano 0,001 USD per risorsa. La deduplicazione di billing entro il giorno UTC e' dichiarata una soft guarantee ([X API pricing](https://docs.x.com/x-api/getting-started/pricing)).

Con 11 run settimanali, 300 post per run costerebbero al massimo teorico circa:

```text
300 * 0,005 USD * 11 * 4,33 = 71,45 USD/mese
```

Il valore `x_max_posts_per_run = 300` e' soltanto un tetto tecnico, non una quota spendibile a ogni run. La CLI registra reservation e costi stimati in un ledger mensile SQLite, calcola il limite effettivo dal budget residuo e blocca atomicamente la chiamata se non resta almeno una pagina minima. In questo modo run manuali o concorrenti non possono aggirare `x_monthly_budget_usd = 25`.

Guardrail obbligatori:

- budget mensile e giornaliero hard-stop;
- reservation atomica preflight prima della chiamata e riconciliazione dopo il risultato;
- contatore per risorsa e per endpoint;
- niente auto-recharge durante pilot;
- degradazione esplicita `coverage_gap`, mai fallback nascosto;
- nessuna chiamata X API durante test unitari;
- fixture sanitizzate con post ID sintetici.

## Benchmark comparativo

### Dataset

- 14 giorni storici con almeno 30 eventi X rilevanti annotati manualmente;
- equilibrio tra annunci, paper, prodotto, strategia e segnali interdisciplinari;
- fonte primaria e timestamp per ogni evento;
- set separato di almeno 50 post di rumore.

### Candidati

1. X API watchlist.
2. xAI X Search con handle e date.
3. Grok.com manuale con prompt fisso.
4. Vecchia routine WebSearch `site:x.com` come baseline negativa.

Grok Bot viene valutato solo se usa uno dei canali autorizzati sopra; non ottiene una categoria separata per il solo fatto di avere un browser.

### Metriche

| Metrica | Definizione |
|---|---|
| Event recall | Eventi gold trovati / eventi gold |
| Post precision | Post utili / post recuperati |
| Alert recall | Eventi degli account `alert-si` trovati / eventi gold alert |
| Discovery lift | Eventi unici trovati fuori watchlist |
| Primary-link rate | Eventi collegati a fonte ufficiale |
| Duplicate rate | Post/eventi gia' acquisiti riproposti |
| Median latency | Tempo tra pubblicazione e acquisizione |
| Cost per accepted event | Costo totale / eventi entrati nel radar |
| Reproducibility | Stessa query/finestra con risultati confrontabili |
| Citation integrity | URL citati che risolvono al post corretto |
| Policy fit | Pass/fail rispetto ai termini applicabili |

### Criteri di scelta

- X API resta il canale canonico se `alert recall >= 95%` nel gold set e il costo rientra nel cap.
- xAI Search resta discovery se aggiunge almeno il 10% di eventi utili con precisione >= 60%.
- Grok.com resta audit manuale se non offre un export riproducibile.
- Qualsiasi opzione che richieda scraping browser non passa il policy gate.

Le soglie sono ipotesi di pilot da validare, non risultati misurati.

## Failure modes

| Caso | Comportamento |
|---|---|
| Crediti X esauriti | Chiudi la corsia, registra gap, non comprare automaticamente |
| HTTP 429 | Rispetta reset, nessun retry aggressivo |
| Post cancellato | Mantieni ID e stato `unavailable`; non ripubblicare testo |
| Claim solo su X | Stato `unverified`, cerca fonte indipendente |
| xAI senza citazioni | Scarta l'output dalla pipeline fattuale |
| Grok.com trova evento assente | Aggiungi al dataset eval, non al digest senza verifica |
| Bookmark privato | Resta nello storage privato e non viene esposto in Notion pubblico/Substack |

## Fonti ufficiali

- [X API pricing](https://docs.x.com/x-api/getting-started/pricing)
- [X API rate limits](https://docs.x.com/x-api/fundamentals/rate-limits)
- [X Bookmarks API](https://docs.x.com/x-api/posts/bookmarks/introduction)
- [X Developer Policy](https://docs.x.com/developer-terms/policy)
- [xAI X Search](https://docs.x.ai/developers/tools/x-search)
- [xAI pricing](https://docs.x.ai/developers/pricing)
- [xAI tool usage details](https://docs.x.ai/developers/tools/tool-usage-details)
- [Grok.com](https://x.ai/grok)
- [About Grok on X](https://help.x.com/en/using-x/about-grok)
- [Grok Bot overview](https://docs.x.ai/grok-bot/overview)
