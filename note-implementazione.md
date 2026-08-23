# Note di implementazione

## Contesto

Lavoro avviato dopo l'approvazione esplicita del piano riformalizzato per l'AI Intelligence System privato. La working copy e' separata dal clone locale preesistente per preservare due immagini non tracciate appartenenti all'utente.

## Decisioni confermate

- Digest privati dal lunedi' al venerdi' alle 07:00 e alle 21:00 Europe/Rome.
- Recap privato il sabato alle 09:00 Europe/Rome.
- Budget di lettura complessivo: 30 minuti al giorno.
- Codice pubblico separato da dati, email, credenziali e knowledge base privata.
- Notion come vista umana futura; Substack come livello editoriale draft-only nella prima versione.
- Nessun test o invio verso gli iscritti di `giadaf.substack.com`.
- Nessuna pubblicazione automatica.

## Deviazioni

- 2026-08-23 - Creata una working copy in `exec_bot/ai_deepdive` invece di modificare `/Users/giadafranceschini/code/ai_deepdive`: il clone preesistente contiene due file non tracciati dell'utente e si trova fuori dalla root scrivibile autorizzata.
- 2026-08-23 - Rimossa dall'architettura target l'automazione Substack tramite API private: i Terms of Use correnti vietano reverse engineering, scraping e crawling. La soluzione conservativa genera un draft package completo e mantiene manuali inserimento, preview, scheduling e pubblicazione nell'interfaccia ufficiale.
- 2026-08-23 - Rimossa la proposta di campionare automaticamente il feed X `For You` tramite browser: le regole X vietano l'automazione non-API del sito. La corsia conforme usa bookmark manuali acquisiti tramite Bookmarks API, affiancati da X API incrementale per la watchlist e xAI X Search per discovery semantica.
- 2026-08-23 - La working copy iniziale era ferma al commit `c0d86c7`, mentre `origin/main` era avanzato a `910c0e1`: e' stato eseguito un fetch read-only e il lavoro verra' riallineato sul remoto prima del push. I delta remoti riguardano digest, KB e radar e non sovrappongono i file v2.
- 2026-08-23 - La creazione del repository GitHub privato per lo stato non e' stata eseguita: `gh auth status` segnala credenziali GitHub non valide e, soprattutto, i dati raw non devono essere caricati neppure in un repo privato senza una decisione su cifratura e retention. L'MVP impone invece una directory privata locale/VM; il repo separato resta un'attivita' infrastrutturale esplicita.
- 2026-08-23 - Nessuna integrazione live, schedule o delivery e' stata attivata: mancano ancora credenziali e benchmark, e l'abilitazione prematura violerebbe i gate confermati. Sono stati implementati connettori, dry-run e istruzioni per il pilot.
