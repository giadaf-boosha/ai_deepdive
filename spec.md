# AI Intelligence System — specifica

> Sorgente di verita' per scope, requisiti e decisioni. Revisione: 2026-08-23.

## 1. Contesto e obiettivo

`ai_deepdive` nasce come routine editoriale Claude Code: cerca notizie, genera Markdown, aggiorna una KB pubblica e invia un'email. L'audit 2026-08-23 mostra che il prototipo ha valore editoriale, ma non offre acquisizione incrementale, copertura misurabile, deduplicazione persistente o separazione tra dati privati e output pubblici.

L'obiettivo v2 e' un sistema personale di intelligence, progettato fin dall'inizio per team, Academy e lettori esterni. Deve:

1. aggregare fonti ufficiali, newsletter, stampa, ricerca, X e input manuali;
2. conservare un solo record per documento e un solo evento per fatto;
3. distinguere fatto, inferenza, opinione e rumor;
4. produrre due digest privati feriali e un recap del sabato;
5. scegliere cosa leggere entro 30 minuti al giorno;
6. costruire conoscenza persistente, tesi e ponti interdisciplinari verificabili;
7. preparare output per Notion, public speaking e Substack senza pubblicarli automaticamente;
8. restare indipendente dal modello e dal tool di esecuzione.

## 2. Confini della prima implementazione

In scope:

- codice pubblico e privo di dati personali;
- database SQLite e file operativi in una directory privata esterna;
- connettori deterministici e incrementali;
- deduplicazione documento/evento, ranking, reading queue, digest e audit trail;
- adapter editoriale sostituibile, con baseline offline;
- email all'indirizzo personale tramite allowlist e flag esplicito di invio;
- export controllato per Notion;
- pacchetto Substack manuale con fact/rights gate;
- test offline e benchmark X definito prima dell'attivazione a pagamento.

Fuori scope:

- organizzazione degli altri filoni di lavoro;
- replica automatica del feed X For You;
- scraping del sito X via browser;
- API private o reverse engineering di Substack;
- pubblicazione o invio alla mailing list esistente;
- import automatico di testo integrale paywalled in output pubblici;
- migrazione automatica dei digest/KB storici, che restano dataset di eval non verificato.

## 3. Separazione pubblico/privato

Il repository pubblico contiene codice, configurazioni di esempio, documentazione e contenuti legacy. La variabile obbligatoria `AI_INTEL_DATA_DIR` deve puntare fuori dal repository. L'applicazione rifiuta l'avvio se la directory e' interna al repo.

Nel data store privato vivono database, body email/newsletter, note, claim, bridge, reading history, outbox e credenziali indirette. I segreti vivono solo in environment variables o secret manager della VM.

Ogni record ha una visibility fra `private`, `team`, `public_candidate` e `public_approved`. Solo `public_approved`, dopo fact review e rights review, puo' entrare in un pacchetto pubblico.

## 4. Modello dati canonico

```text
Source -> Document -> Event -> Claim -> Evidence
                         |        |
                         |        +-> Concept / Bridge / Thesis
                         +-> ReadingDecision -> Digest / ReadingNote
                                                |
                                                +-> Application / Output
```

Entita' minime:

- `Source`: identita', tipo, priorita', access class e stato.
- `Document`: URL canonico/fingerprint, titolo, estratto o raw reference privata, data e provenance.
- `Event`: fatto deduplicato che puo' riunire piu' documenti.
- `EventDocument`: ruolo `primary`, `confirmation` o `analysis`.
- `Claim`: tipo `fact`, `inference`, `opinion` o `rumor`, confidenza e stato di verifica.
- `ClaimEvidence`: supporto o contraddizione con citazione precisa.
- `Concept`: conoscenza durevole, separata dalla frequenza della notizia.
- `Bridge`: relazione interdisciplinare con meccanismo, evidenza, controevidenza e rischio dell'analogia.
- `ReadingDecision` e `ReadingNote`: decisione, minuti, esito e note.
- `Application`: implicazione per Giada, Boosha, Parla o Academy.
- `Thesis`: posizione argomentabile e versionata.
- `Output`: digest, talk, lezione o articolo con audience e gate.
- `RightsRecord`, `SyncRecord`, `Run`, `Delivery`, `Watermark`: compliance e operabilita'.

## 5. Acquisizione

### Fonti web, ricerca e newsletter

- RSS/Atom prima scelta, parser locale e watermark per fonte.
- IMAP per iCloud e Gmail; message ID come identita' primaria.
- HTML autenticato solo tramite integrazione conforme e contenuto mantenuto privato.
- articoli dei provider AI e paper sempre collegati alla fonte primaria.
- import JSONL come porta controllata per acquisizioni manuali o connector esterni.

Metriche distinte: `attempted`, `acquired`, `failed`, `cited`, `primary`.

### X

X e' diviso in tre corsie:

1. watchlist canonica tramite X Recent Search, query aggregate, `since_id`, cache e tetto rigido;
2. discovery semantica tramite xAI X Search, misurata come complemento e non come enumerazione;
3. vero For You tramite gesto umano bookmark e successiva acquisizione con Bookmarks API.

Grok.com resta uno strumento manuale di esplorazione. Grok Bot puo' orchestrare processi, ma non automatizza il browser X. X MCP e' solo un adapter della stessa API e non aggira costi o limiti.

## 6. Deduplicazione e ranking

Tre livelli:

1. identita' esatta per source ID, message ID o post ID;
2. documento per URL canonico e fingerprint del contenuto;
3. evento per similarita' deterministica di titolo/entita' e conferma editoriale.

Il ranking considera novita', autorita' e prossimita' della fonte primaria, impatto, rilevanza per le corsie, evidenza, ponte interdisciplinare, applicabilita' e costo di lettura. Non tutte le corsie devono apparire in ogni digest; la copertura viene bilanciata su base settimanale.

Corsie: ricerca tecnica; agenti e coding; prodotto; business dei lab; strategia aziendale; marketing; formazione; filosofia; neuroscienze; linguistica e semantica; matematica; management e leadership; spatial intelligence ed embodied AI.

Un bridge e' valido solo se esplicita il meccanismo condiviso e dove l'analogia smette di reggere.

## 7. Output e tempo

- lunedi-venerdi, 07:00 Europe/Rome: novita' dalla precedente esecuzione riuscita;
- lunedi-venerdi, 21:00: novita' del giorno non gia' inviate;
- sabato, 09:00: top 10 eventi della settimana e long read per il weekend.

Ogni voce contiene titolo, TLDR, perche' conta, corsia, confidenza, decisione di lettura, minuti, fonti e bridge se validato. La somma delle letture complete selezionate non supera 30 minuti al giorno; il resto va in coda.

Le finestre partono dal watermark dell'ultima esecuzione riuscita, non da formule come "ultime 24 ore", quindi non si sovrappongono e non lasciano buchi.

## 8. Knowledge e pubblicazione

La KB non nasce da una soglia di menzioni. Un aggiornamento durevole richiede almeno un claim con evidenza, una definizione del delta e una decisione umana o un gate editoriale.

Notion e' una proiezione umana controllata: campi system-owned in uscita e campi human-owned in rientro, hash e conflict log. L'integrazione va limitata alle sole pagine condivise.

Substack e' una destinazione editoriale manuale. Il sistema produce `article.md`, manifest dei diritti e checklist; Giada incolla, verifica preview/test email e decide la pubblicazione. Non vengono usate API private.

Per il public speaking ogni tesi puo' generare una struttura con audience, hook, definizioni, tre passaggi, evidenze, controargomento, bridge, esempio, so-what, versioni 60 secondi/5 minuti/20 minuti, domande e feedback.

## 9. Sicurezza

- contenuto esterno trattato come dato non fidato, mai come istruzione;
- output strutturato del modello validato prima della persistenza;
- rendering HTML con escaping;
- raw paywalled e newsletter solo privati;
- invio email disabilitato senza flag esplicito, credenziali e recipient allowlist;
- nessuna delivery a Substack;
- limiti per post, pagine, tool call e budget mensile;
- idempotency key per run e delivery;
- nessun segreto o database nel repository pubblico.

## 10. Criteri di accettazione MVP

- run ripetuta sugli stessi input: zero documenti/eventi/output duplicati;
- 100% delle voci ha almeno un link diretto e provenance;
- watchlist X raggiunge event recall >=95% nel benchmark controllato;
- xAI Search entra in produzione solo con rumore <=20% e discovery incrementale utile;
- reading queue rispetta 30 minuti;
- finestre AM/PM/weekly corrette in Europe/Rome;
- nessun test esegue rete, API a pagamento, invio o pubblicazione;
- pacchetto pubblico bloccato senza fact e rights review;
- tutte le deviazioni dal piano sono registrate in `note-implementazione.md`.

## 11. Baseline legacy

`digest/`, `kb/`, `fondamenti/`, `web/` e le routine Claude Code restano temporaneamente intatti. Non sono la fonte canonica della v2 e non vanno estesi prima di una settimana di run manuali affidabili. La vecchia automazione Substack non deve essere eseguita; la sostituzione supportata e' l'export manuale della v2.
