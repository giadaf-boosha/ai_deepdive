# Audit dello stato corrente di `ai_deepdive`

Data dell'audit: 2026-08-23  
Modalita': read-only  
Perimetro: repository, app, prompt, configurazione, digest, knowledge base, deploy e routine accessibili.

## Executive summary

`ai_deepdive` e' un prototipo editoriale funzionante, con un patrimonio di contenuti e un frontend statico riutilizzabile. Non e' ancora un AI Intelligence System affidabile: l'acquisizione, la deduplicazione, la selezione editoriale, l'aggiornamento della KB, Git e l'email sono affidati a un unico prompt, senza uno stato strutturato che renda ogni passaggio osservabile e verificabile.

La decisione e' quindi:

- conservare sito, corpus storico, configurazione delle fonti e convenzioni editoriali;
- congelare la routine corrente come baseline di confronto;
- costruire la nuova pipeline accanto a essa, con dati privati fuori dal repository pubblico;
- non estendere il prompt monolitico e non aggiungere nuove schedule prima di un pilot misurato.

## Confini dell'evidenza

L'audit ha distinto tre stati:

1. **Checkout locale preesistente**: `/Users/giadafranceschini/code/ai_deepdive`, HEAD `c0d86c7` del 7 luglio 2026, con due PNG non tracciati dell'utente.
2. **Repository remoto pubblico**: `main` a `910c0e1` del 23 agosto 2026. Al momento della verifica conteneva 85 digest, ultimo `digest/2026/08/22.md`, e 25 concetti KB.
3. **Deploy pubblico**: [aideepdive.vercel.app](https://aideepdive.vercel.app/) rispondeva HTTP 200; il radar live riportava verifica 23 agosto 2026 e prossimo aggiornamento 30 agosto 2026.

Il codice applicativo e i prompt non risultavano cambiati tra il checkout del 7 luglio e HEAD remoto; i delta erano digest, nove file KB e `web/data/models.json`.

## Struttura e comportamento osservato

```text
config/sources.yaml
        |
        v
routine Claude Code giornaliera
  scrape/search -> filtro -> digest -> KB -> commit/push -> email/draft
        |
        +--> digest/YYYY/MM/DD.md
        +--> kb/concetti/*.md
        +--> build statico Next.js su Vercel

routine Claude Code settimanale
  web search -> web/data/models.json -> commit/push -> Vercel
```

La struttura promessa e' descritta in `README.md:15-46`; il comportamento daily effettivo e' interamente specificato in `automations/whats-new-daily-prompt.md:7-247`; il frontend legge Markdown a build time tramite `web/lib/content-paths.ts:3-8`.

## Risultati quantitativi della baseline

I numeri seguenti sono misure dell'archivio locale di 67 digest, dal 28 aprile al 6 luglio 2026, salvo dove indicato diversamente.

| Metrica | Risultato | Interpretazione |
|---|---:|---|
| Digest locali | 67 | Tre date mancanti nel periodo locale |
| Digest su remoto | 85 | Solo 18 nuovi digest tra 9 luglio e 22 agosto: routine intermittente |
| Fonti consultate medie | 22,84 | Definizione non stabile tra run |
| Fonti fallite medie | 20,55 | Failure rate strutturalmente alto |
| Run con fallimenti oltre meta' copertura | 59/67 | L'edge case `>50%` e' la normalita', non l'eccezione |
| Run con fallite > consultate | 36/67 | Metriche non mutuamente coerenti |
| Voci medie per digest | 4,63 | Compatibile con un brief stretto |
| Domini linkati distinti | 431 | Il fallback ha ampliato il perimetro oltre la config |
| Link diretti a post X | 3 | Copertura X sostanzialmente assente |

Esempio di incoerenza operativa: `digest/2026/06/25.md:34-36` dichiara 21 fonti consultate e 29 fallite. In `digest/2026/07/06.md:35`, X non viene tentato perche' il blocco 403 e' considerato consolidato.

## Gap verificati

### Acquisizione

- La config contiene 19 newsletter e 59 account X (`config/sources.yaml:12-494`), ma la routine non dispone di connettori dedicati e testabili.
- I feed canonici falliscono spesso; WebSearch e' diventato il meccanismo principale e introduce fonti non governate.
- Mancano iCloud IMAP, Gmail, account/newsletter Substack, feed dei provider ufficiali, arXiv per categoria, GitHub Trending, Hacker News AI e le fonti strategy richieste.
- Il contratto del prompt usa `newsletter` e paywall `none|partial|full` (`automations/whats-new-daily-prompt.md:11-16`); il file reale usa `newsletters` e `false|partial|full` (`config/sources.yaml:9-12`).

### Stato, deduplicazione e affidabilita'

- La deduplicazione rilegge soltanto sette digest (`automations/whats-new-daily-prompt.md:29-35`): non esistono canonical URL, hash del documento o identita' persistente dell'evento.
- La finestra `YESTERDAY 00:00` (`automations/whats-new-daily-prompt.md:18-27`) dura circa 31 ore nel run delle 07:00 e non supporta due run incrementali al giorno.
- Mancano watermark, idempotency key, lock del job, stato di retry, correzioni e aggiornamenti di un evento gia' pubblicato.
- Il push e' diretto su `main`; lo snippet non implementa il controllo `git diff --cached --quiet` che il testo dichiara (`automations/whats-new-daily-prompt.md:159-188`).

### Scheduling e delivery

- `0 5 * * *` equivale alle 07:00 in CEST e alle 06:00 in CET; la limitazione e' gia' documentata in `automations/README.md:63-69`.
- Non esistono run serale e recap del sabato.
- L'esito email non e' persistito in un ledger e la routine puo' creare un draft invece di inviare (`automations/whats-new-daily-prompt.md:190-214`).

### Knowledge base

- Il trigger 3 fonti oggi/5 menzioni in sette giorni e la generazione immediata di 1.500-3.000 parole (`automations/whats-new-daily-prompt.md:101-157`) premiano la ripetizione, non il valore durevole.
- Mancano oggetti distinti per claim, evidenza, controargomento, bridge interdisciplinare, reading note, thesis e application.
- Digest, KB e contenuto editoriale sono pubblici; non possono ospitare note personali, materiale paywalled o implicazioni riservate per Boosha e Parla.

### Frontend

- Il parser riconosce solo bullet con titolo in grassetto (`web/lib/digest.ts:67-94`); quattro digest locali hanno un formato che produce zero titoli estratti pur dichiarando voci nel frontmatter.
- Le note di produzione sono nascoste nella singola pagina (`web/app/digest/[date]/page.tsx:38-41`) ma restano nel testo full-text serializzato per la ricerca (`web/app/digest/page.tsx:11-19`).
- `rehypeRaw` e' abilitato senza sanitizzazione (`web/components/MarkdownContent.tsx:41-44`), ampliando il rischio se Markdown generato dall'agente contiene HTML inatteso.
- Non risultano test o workflow CI per parser, schema contenuti e build.

### Documentazione e diritti

- `README.md:100-109` dichiara il radar attivo; `automations/README.md:35-39` dice ancora che deve essere creato.
- Due PDF di Russell e Norvig provenienti da Anna's Archive sono presenti localmente e ignorati da Git. I 28 capitoli Fondamenti sono dichiarati sintesi originali con una singola attribuzione (`spec.md:121-129`), mentre il repository applica licenza MIT. La monetizzazione richiede una revisione separata di provenienza, diritti e licensing.

## Rischi prioritizzati

| Livello | Rischio | Effetto | Controllo richiesto |
|---|---|---|---|
| Critico | Claim non verificato o fonte secondaria debole | Perdita di fiducia editoriale | Claim-evidence ledger e fonte primaria obbligatoria |
| Critico | Dati privati nel repo/sito pubblico | Esposizione di email, note o paywall | `AI_INTEL_DATA_DIR` esterna e privata |
| Alto | Run duplicato o finestra sovrapposta | Doppioni e doppio invio | Watermark, lock, idempotency key |
| Alto | X assente o troppo costoso | Blind spot su una fonte centrale | Strategia X a corsie e budget hard-stop |
| Alto | Pubblicazione/invio accidentale Substack | Impatto sui circa 300 iscritti | Export offline e approvazione manuale |
| Medio | HTML non sanitizzato | Content injection nel sito | Renderer escapato/sanitizzato |
| Medio | KB che cresce senza revisione | Conoscenza stale e ridondante | Lifecycle, stato dei claim e review cadence |

## Asset riutilizzabili

- Gli 85 digest remoti come dataset storico per eval, dopo fact-checking a campione.
- `config/sources.yaml` come seed del registry, non come schema definitivo.
- I 25 concetti KB e i 28 Fondamenti come materiale da revisionare.
- Il frontend Next.js/Vercel come vista pubblica di output deliberatamente pubblicabili.
- Le convenzioni editoriali: italiano, tono asciutto, link diretto, massimo dieci segnali.
- La pipeline Substack esistente come riferimento di conversione, non come canale autorizzato di pubblicazione automatica.

## Benchmark di uscita dalla baseline

Il pilot deve usare un gold set di almeno 100 eventi storici, annotati manualmente con fonte primaria, rilevanza e decisione di lettura. Il confronto baseline/nuovo sistema deve misurare:

| Asse | Metrica | Soglia pilot proposta |
|---|---|---:|
| Retrieval | Recall degli eventi critici | >= 90% |
| Editoriale | Precision@10 | >= 80% |
| Deduplica | Cluster duplicati residui | <= 2% |
| Provenienza | Voci con fonte primaria | >= 90% |
| Tracciabilita' | Claim con evidenza risolvibile | 100% |
| Reading | Tempo selezionato | <= 30 min/giorno |
| Operazioni | Run senza intervento | >= 95% nel pilot |
| Delivery | Invii duplicati | 0 |
| Privacy | Record privati nel repo pubblico | 0 |

Le soglie sono criteri di accettazione proposti, non risultati gia' raggiunti.

## Decisioni conseguenti

1. Il repository pubblico resta il luogo del codice e degli output intenzionalmente pubblici.
2. Documenti acquisiti, email, database, KB privata, reading notes e outbox vivono fuori dal repository.
3. L'acquisizione produce record strutturati prima di invocare un modello editoriale.
4. Digest, reading queue, Notion e Substack sono proiezioni, non fonti di verita'.
5. Nessuna pubblicazione automatica e nessun test sulla publication esistente.
6. La routine corrente resta una baseline finche' il nuovo sistema supera il benchmark.

## Riferimenti ufficiali esterni

- [X Developer Policy](https://docs.x.com/developer-terms/policy)
- [X API pricing](https://docs.x.com/x-api/getting-started/pricing)
- [xAI X Search](https://docs.x.ai/developers/tools/x-search)
- [Grok Bot overview](https://docs.x.ai/grok-bot/overview)
- [Notion data source API](https://developers.notion.com/reference/data-source)
- [Substack Terms of Use](https://substack.com/tos)
- [Substack: pubblicare e salvare draft](https://support.substack.com/hc/en-us/articles/360037831771-How-do-I-publish-a-new-post-on-Substack)
