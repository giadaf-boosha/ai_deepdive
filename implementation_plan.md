# AI Intelligence System — implementation plan

> Revisione: 2026-08-23. Le parti piu' instabili sono intenzionalmente in cima.

## 1. Decisioni, modello e interfacce — MVP completato

- [x] Separare codice pubblico e stato privato tramite `AI_INTEL_DATA_DIR` obbligatoria.
- [x] Definire modello `Source -> Document -> Event -> Claim/Evidence` e record knowledge/output.
- [x] Separare X watchlist, discovery semantica e For You personale.
- [x] Sostituire l'API privata Substack con pacchetto manuale e rights gate.
- [x] Definire adapter editoriale indipendente dal modello con baseline offline.
- [ ] Eseguire una settimana di run manuali e calibrare soglie/ranking.
- [ ] Decidere il provider editoriale di produzione solo dopo eval comparativa.

## 2. Flussi utente e decisioni — MVP completato

- [x] Digest AM/PM e weekly basati su watermark.
- [x] Budget lettura massimo 30 minuti/giorno.
- [x] Template public speaking e bridge interdisciplinari.
- [x] Export Notion con ownership esplicita dei campi.
- [x] Email protetta da allowlist e flag di invio.
- [ ] Validare con Giada un campione reale di 3 digest e 10 decisioni di lettura.
- [ ] Creare le viste Notion solo dopo la validazione del modello informativo.

## 3. Acquisizione — connector completati, attivazione pending

- [x] Connector RSS/Atom e IMAP testabili offline.
- [x] Import JSONL per input controllati.
- [x] X Recent Search con `since_id`, pagination e hard cap.
- [x] X Bookmarks come ponte dal For You.
- [ ] Configurare credenziali su VM/secret manager.
- [ ] Auditare usage X precedente da Developer Console.
- [ ] Eseguire benchmark X documentato senza superare il budget approvato.
- [ ] Aggiungere xAI X Search solo se supera i criteri di accettazione.

## 4. Curation, knowledge e output — MVP completato

- [x] Canonicalizzazione, fingerprint e clustering evento deterministico.
- [x] Ranking editoriale multi-corsia e reading queue.
- [x] Rendering Markdown/HTML con escaping.
- [x] Export Substack offline con manifest e checklist.
- [x] Proiezione Notion limitata.
- [ ] Aggiungere feedback umano al ciclo di ranking dopo i primi run.
- [ ] Promuovere claim/concept/bridge solo tramite review.

## 5. Validazione e rollout — da eseguire

1. [ ] Importare fixture reali private senza committarle.
2. [ ] Eseguire pipeline manualmente due volte e verificare idempotenza.
3. [ ] Eseguire shadow run AM/PM per cinque giorni senza invio.
4. [ ] Confrontare con digest legacy e gold set umano.
5. [ ] Abilitare email solo a `giada.f@me.com` per una settimana.
6. [ ] Configurare schedule locale Europe/Rome su VM persistente.
7. [ ] Solo dopo stabilita', valutare Notion live e publication Substack isolata a zero iscritti.

## 6. Infrastruttura e lavoro meccanico — da eseguire

- [ ] Creare repository GitHub privato separato per eventuali config/stato non-secret; mai raw content.
- [ ] Configurare backup cifrato del database privato.
- [ ] Configurare health check e alert su run mancanti, costo e copertura.
- [ ] Deprecare formalmente la routine daily legacy dopo il parallel run.
- [ ] Rimuovere `python-substack` e `publish.py` legacy in una modifica separata dopo verifica di non utilizzo.
- [ ] Valutare la sanitizzazione `rehypeRaw` del frontend legacy in una modifica separata.

## Definition of done della prima implementazione

- test offline verdi;
- documentazione e audit aggiornati;
- nessuna chiamata a pagamento o delivery esterna durante QA;
- commit e push su `main` senza sovrascrivere modifiche utente;
- deviazioni annotate;
- istruzioni riproducibili per init, ingest, curate, render e dry-run delivery.
