# Architettura della conoscenza e della pubblicazione

Data decisione: 2026-08-23  
Principio: la conoscenza canonica e' privata; Notion e Substack sono proiezioni con finalita' diverse.

## Obiettivo

Trasformare il flusso quotidiano secondo la sequenza:

```text
osservare -> verificare -> comprendere -> collegare -> applicare -> insegnare -> pubblicare
```

Il sistema deve servire contemporaneamente aggiornamento operativo, studio entro 30 minuti al giorno, public speaking, formazione, strategia per Boosha/Parla e un futuro prodotto editoriale, senza confondere materiale privato con contenuto pubblicabile.

## Decisione a tre livelli

| Livello | Ruolo | Contenuto | Autorita' |
|---|---|---|---|
| Storage privato | Fonte canonica | Documenti, eventi, claim, evidenze, note, diritti, stato | Il sistema |
| Notion | Vista di lavoro | Reading queue, review, tesi, output, feedback | Sistema + Giada |
| Substack | Distribuzione pubblica | Articoli originali approvati | Giada |

Il repository pubblico contiene codice e output scelti esplicitamente per la pubblicazione. `AI_INTEL_DATA_DIR` deve essere esterna al repository; il contratto e' gia' applicato in `intelligence/config.py:57-94`.

## Modello della conoscenza

### Entita'

| Oggetto | Funzione | Campi indispensabili |
|---|---|---|
| `Source` | Identifica una fonte | id, nome, canale, autorita', access class |
| `Document` | Snapshot acquisito | id, URL canonico, hash, published_at, retrieved_at, source_id |
| `Event` | Fatto o sviluppo nel tempo | id, titolo canonico, type, occurred_at, status |
| `Claim` | Proposizione verificabile | id, testo, confidence, verification status |
| `Evidence` | Supporta o contraddice un claim | claim_id, document_id, relation, locator |
| `Entity` | Persona, azienda, modello, prodotto | id, canonical name, aliases |
| `Concept` | Idea durevole | id, definition, scope, lifecycle |
| `Bridge` | Connessione interdisciplinare | from, to, mechanism, break point |
| `Counterpoint` | Obiezione forte | claim/thesis id, evidence, status |
| `Application` | Implicazione operativa | target, problem, action, expected outcome |
| `ReadingNote` | Sintesi di una lettura integrale | thesis, evidence, objections, takeaways |
| `Thesis` | Idea originale in sviluppo | statement, confidence, evidence gaps, owner |
| `Output` | Articolo, talk, video, lezione, playbook | audience, thesis, format, status, source set |

### Relazioni essenziali

```text
Source 1--n Document
Document n--n Event
Document n--n Claim via Evidence
Event n--n Entity
Claim n--n Concept
Concept n--n Concept via Bridge
Claim/Thesis 1--n Counterpoint
Event/Concept/Thesis 1--n Application
ReadingNote n--n Document
Output n--n Claim/Thesis/ReadingNote
```

Un digest non e' un oggetto canonico: e' una proiezione di eventi selezionati. Una pagina Notion non e' un record canonico: e' una vista sincronizzata. Un articolo Substack non e' la KB: e' un output editoriale versionato.

## Lifecycle

### Claim

```text
unverified -> corroborated -> verified -> superseded | retracted
```

- `verified` richiede fonte primaria o evidenza indipendente sufficiente.
- `superseded` conserva il claim precedente e collega quello nuovo.
- Una correzione non sovrascrive silenziosamente la storia.

### Concept

```text
candidate -> active -> mature -> needs_review -> archived
```

Un concetto nasce quando e' necessario per capire piu' eventi o per sviluppare una tesi, non perche' il nome ricorre molte volte nello stesso ciclo di news.

### Output editoriale

```text
idea -> research -> outline -> draft -> fact_review -> rights_review
     -> ready_for_human -> scheduled -> published -> measured
```

`scheduled` e `published` richiedono sempre un'azione umana nella prima versione.

## Ranking per conoscenza e lettura

Lo score editoriale combina:

- rilevanza per le corsie tematiche;
- novita' rispetto alla conoscenza esistente;
- autorita' e prossimita' della fonte primaria;
- impatto potenziale;
- densita' informativa;
- applicabilita' a Giada, Boosha, Parla o Academy;
- `bridge potential`;
- costo di lettura;
- ridondanza.

### Bridge potential

Un ponte e' valido solo se specifica:

1. i due domini collegati;
2. il meccanismo realmente condiviso;
3. l'evidenza;
4. dove l'analogia smette di funzionare;
5. perche' il collegamento modifica una decisione o una spiegazione.

Esempi di assi prioritari:

- world models <-> filosofia della rappresentazione;
- spatial intelligence <-> neuroscienze della percezione;
- agentic AI <-> agency e intentionality;
- linguaggio come lossy representation <-> semantica e limiti degli LLM;
- simulation data <-> epistemologia;
- automation/augmentation <-> organizzazione del lavoro;
- valori embedded by design <-> leadership e governance.

Il bridge non deve premiare analogie suggestive ma non falsificabili.

## Reading budget

Il limite e' 30 minuti complessivi al giorno. Ogni contenuto riceve una decisione:

- `read_full`;
- `read_sections` con sezioni indicate;
- `tldr`;
- `reading_queue`;
- `ignore`.

L'allocazione sceglie i long read in ordine di score finche' resta budget; gli altri passano alla coda, come implementato in `intelligence/rendering.py:130-152`. Il sabato puo' consumare tempo accumulato soltanto se Giada lo decide esplicitamente: non si crea debito di lettura automatico.

## Nota di apprendimento e public speaking

Ogni lettura integrale utile produce:

- tesi in una frase;
- definizioni indispensabili;
- tre passaggi logici;
- evidenze e fonti;
- controargomento piu' forte;
- ponte interdisciplinare e suo limite;
- esempio concreto;
- implicazione pratica;
- versioni da 60 secondi, 5 minuti e 20 minuti;
- domande previste;
- frase memorabile originale;
- feedback di prova.

Il template iniziale vive in `intelligence/publishing.py:79-120`.

## Proiezione Notion

Notion serve come interfaccia operativa, non come storage dei documenti raw.

### Viste iniziali

1. **Radar & Reading**: eventi selezionati, score, tempo, decisione, stato di lettura.
2. **Claims to verify**: claim non verificati o contraddetti.
3. **Knowledge garden**: concept, bridge, counterpoint e review date.
4. **Applications**: Giada, Boosha, Parla, Academy.
5. **Editorial pipeline**: thesis e output dal research al ready-for-human.
6. **Speaking practice**: talk, durata, feedback, domande difficili.

### Ownership dei campi

- Il sistema possiede ID, titolo, URL, score, corsia, provenienza e timestamp.
- Giada possiede stato umano, note, letto/non letto, decisione editoriale e feedback di rehearsal.
- La sincronizzazione non sovrascrive i campi umani.

La proiezione bounded corrente e' definita in `intelligence/notion_export.py:9-35`. La Notion API tratta le righe di un data source come pagine e richiede uno schema coerente con le property del parent ([Notion Data Source API](https://developers.notion.com/reference/data-source)). Ogni integrazione deve salvare il `page_id` remoto per upsert idempotenti e usare una versione API fissata.

### Dati esclusi da Notion

- corpo raw di email e newsletter;
- copie integrali paywalled;
- cookie, token e credenziali;
- payload API non redatti;
- note personali non necessarie alla vista scelta.

## Pipeline pubblica e Substack

### Decisione

La prima versione genera un pacchetto offline, non crea draft su Substack e non usa endpoint privati. `intelligence/publishing.py:35-76` impone fact review, rights review, blocca la ripubblicazione raw e produce articolo, manifest SHA-256 e checklist.

Motivazione:

- i [Terms of Use di Substack](https://substack.com/tos) vietano crawling/scraping e reverse engineering;
- i [Developer API Terms](https://substack.com/api-tos) regolano dati pubblici autorizzati, ma non documentano un flusso ufficiale per creare e inviare newsletter;
- la guida ufficiale indica che i post sono salvati come draft nell'editor e che, per default, la pubblicazione puo' includere email e app inbox; l'opzione deve essere controllata manualmente ([Substack publishing guide](https://support.substack.com/hc/en-us/articles/360037831771-How-do-I-publish-a-new-post-on-Substack)).

### Flusso

```text
Output ready_for_human
  -> export article.md
  -> manifest.json con fonti/diritti/hash
  -> QA-CHECKLIST.md
  -> revisione Giada
  -> copia manuale in publication isolata senza iscritti
  -> preview desktop/mobile
  -> test email solo a Giada
  -> decisione manuale di scheduling/pubblicazione
```

`giadaf.substack.com` e i suoi circa 300 iscritti non vengono usati per test. Notes, invio email, scheduling e publish restano azioni manuali.

## Rights manifest

Ogni evidenza usata da un output pubblico registra:

```text
url
source
access_class: public | subscription | paywall | private
usage: link | paraphrase | short_quote | original_analysis | raw_republication
excerpt_words
license
rights_review_status
```

Regole:

- `raw_republication` blocca l'export;
- materiale paywalled puo' informare l'analisi privata, non essere ricostruito nel testo pubblico;
- quote ed estratti sono minimi e attribuiti;
- immagini richiedono licenza/permesso e alt text;
- la provenienza dei Fondamenti va revisionata prima di monetizzazione o rilascio con licenza.

## Benchmark e metriche

### Knowledge quality

| Metrica | Definizione | Soglia pilot proposta |
|---|---|---:|
| Claim traceability | Claim con evidence locator valido | 100% |
| Primary-source coverage | Claim verificati con fonte primaria | >= 90% |
| Contradiction coverage | Tesi con controargomento forte | >= 80% |
| Concept duplication | Concept duplicati/alias non risolti | <= 2% |
| Stale claim rate | Claim `needs_review` oltre SLA | <= 5% |
| Bridge acceptance | Bridge approvati dopo review umana | >= 60% |
| Application yield | Long read che produce applicazione concreta | >= 30% |

### Reading and reuse

| Metrica | Obiettivo |
|---|---:|
| Tempo selezionato quotidiano | <= 30 minuti |
| Long read completati / assegnati | >= 70% |
| Note riusate in talk/articolo/lezione entro 90 giorni | >= 25% |
| Corsie senza contenuti utili per 4 settimane | 0 senza review esplicita |

### Publishing

| Metrica | Obiettivo |
|---|---:|
| Pacchetti con fact + rights review | 100% |
| Claim pubblici con fonte | 100% |
| Invii accidentali agli iscritti in pilot | 0 |
| Pubblicazioni automatiche | 0 |
| Correzioni fattuali post-pubblicazione | < 1% dei claim |
| Tempo da research a draft revisionabile | Da misurare, non ottimizzare prima della qualita' |

Le soglie sono criteri proposti; il pilot deve registrare baseline e feedback umano prima di promuoverle a SLO.

## Rischi e controlli

| Rischio | Controllo |
|---|---|
| Notion diventa una seconda fonte di verita' | Sync unidirezionale per campi sistema; merge esplicito dei campi umani |
| Copie paywalled finiscono in output | Rights manifest e denylist dei campi raw |
| Tesi generata senza evidenza | Stato `candidate`, fact review obbligatoria |
| Bridge brillante ma falso | Campo `mechanism` + `break_point` + review umana |
| KB cresce senza manutenzione | Lifecycle e review date |
| Invio ai 300 iscritti | Publication isolata, allowlist email, manual-only |
| Cookie/API private Substack | Nessun uso nel target |
| Dati privati nel repo | Validazione hard di `AI_INTEL_DATA_DIR` |
| Modello sostituito | Record e contratti indipendenti dal provider |

## Sequenza di implementazione

1. Schema privato e migrazioni.
2. Import dei documenti con provenance.
3. Event/claim/evidence e deduplica.
4. Reading decision e note.
5. Concept/bridge/counterpoint/application.
6. Proiezione Notion con ownership dei campi.
7. Export editoriale offline con rights gate.
8. Publication di test isolata.
9. Pilot pubblico manuale soltanto dopo target e posizionamento.

## Fonti ufficiali

- [Notion Data Source API](https://developers.notion.com/reference/data-source)
- [Notion: working with databases](https://developers.notion.com/guides/data-apis/working-with-databases)
- [Notion token security](https://developers.notion.com/guides/get-started/quick-start)
- [Substack Terms of Use](https://substack.com/tos)
- [Substack Developer API Terms](https://substack.com/api-tos)
- [Substack publishing and drafts](https://support.substack.com/hc/en-us/articles/360037831771-How-do-I-publish-a-new-post-on-Substack)
