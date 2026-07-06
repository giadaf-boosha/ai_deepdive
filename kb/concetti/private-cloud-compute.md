---
name: Private Cloud Compute
aliases: [PCC, Private Cloud Compute, confidential cloud computing, confidential inference, Apple PCC, confidential cloud, TEE cloud inference]
categoria: infrastruttura
created: 2026-06-08
last_updated: 2026-06-08
---

# Private Cloud Compute

## Cos'e

Private Cloud Compute (PCC) e' un'architettura di inference cloud progettata da Apple per eseguire modelli AI di grandi dimensioni su server remoti garantendo che il vendor del modello non abbia accesso agli input e agli output dell'utente. Introdotto pubblicamente al WWDC 2026 (8 giugno 2026) come infrastruttura per Siri 2.0 — alimentata da un modello Gemini a 1,2 trilioni di parametri sviluppato con Google DeepMind — PCC colma il vuoto architetturale tra l'inferenza on-device (privacy garantita fisicamente, ma limitata dai parametri del modello portabili sul dispositivo) e il cloud computing tradizionale (modelli frontier accessibili, ma con input utente che transitano nell'infrastruttura del vendor).

Il problema che PCC risolve e' concreto: i modelli da 1T+ parametri non sono portabili su dispositivi consumer nemmeno con la memoria unificata piu' capiente disponibile (RTX Spark da 128 GB abilita al massimo ~120B parametri senza quantizzazione degradante). Per offrire Siri con le capacita' di un modello frontier multimodale, Apple deve eseguirlo su server remoti. Il classico cloud computing creerebbe un conflitto irrisolvibile: Google vedrebbe ogni query e ogni risposta di ogni utente iPhone. PCC risolve questo eseguendo il modello Gemini in enclave hardware-isolated su server Apple Silicon, in un ambiente fisicamente e logicamente controllato da Apple — non da Google.

## Come funziona

L'architettura PCC ha tre componenti principali.

**Hardware Apple Silicon dedicato.** I server PCC usano chip Apple Silicon (la stessa famiglia di M-series usata negli iPhone e nei Mac consumer), non hardware Nvidia o AMD tipico dei datacenter. Apple Silicon integra la Secure Enclave — un processore crittografico isolato dal main processor — e il Secure Boot chain: ogni nodo PCC viene avviato con un'immagine software verificata crittograficamente prima di ricevere traffico.

**Isolamento del modello.** I pesi del modello Gemini vengono caricati nell'enclave. L'architettura garantisce che il software che gira nell'enclave non possa comunicare verso l'esterno se non attraverso i canali esplicitamente definiti nell'immagine verificata. In pratica: Google fornisce i pesi del modello, Apple controlla l'ambiente di esecuzione. Il vendor del modello non ha un canale per leggere gli input/output processati.

**Elaborazione stateless ed effimera.** Ogni query viene processata in modo stateless: non viene salvata dopo l'elaborazione, non e' disponibile per il training futuro del modello Gemini, non e' accessibile ad Apple o Google per altri scopi. Apple dichiara che questa proprieta' e' garantita architetturalmente (non solo contrattualmente) dal fatto che il software PCC non include meccanismi di logging o storage persistente degli input. La verifica e' parzialmente resa possibile da audit tecnici del software dell'immagine del nodo.

**Routing selettivo.** Non tutta la computazione di Siri 2.0 passa per PCC. Le query piu' semplici (lookup locale, timer, riconoscimento vocale di base) restano on-device. Le query che richiedono le capacita' del modello frontier (ragionamento multi-step, generazione di testo, cross-app context) vengono instradate verso PCC. La logica di routing e' locale al dispositivo e non richiede invio di dati al server per decidere.

## La posizione nel panorama architetturale

PCC introduce un terzo tier nell'ecosistema dell'inference AI, tra i due poli tradizionali.

**On-device inference.** Modelli small-medium (7B-70B parametri, quantizzati) girano direttamente sul dispositivo. Privacy garantita fisicamente: nessun dato lascia il dispositivo. Vincoli: qualita' del modello limitata dalla memoria del chip (attualmente fino a ~120B su RTX Spark, molto meno su iPhone), latenza variabile, consumo energetico del dispositivo.

**Cloud inference tradizionale.** Modelli frontier (100B-1T+ parametri) girano su GPU nel datacenter del vendor. Massima qualita', latenza network-bound. Privacy: l'utente si fida del vendor per contratto; in pratica, gli input transitano nell'infrastruttura del vendor.

**Confidential cloud inference (PCC).** Modelli frontier girano su server cloud, ma in enclave hardware-isolated controllate dall'OS vendor (Apple), non dal vendor del modello (Google). Privacy parzialmente garantita architetturalmente: il vendor del modello non accede agli input, ma l'OS vendor (Apple) ha accesso fisico ai server. L'utente si fida dell'OS vendor, non del vendor del modello.

Il pattern PCC risponde a una distinzione importante nella struttura di fiducia: la maggior parte degli utenti si fida di Apple con i propri dati (ha gia' dato accesso a tutti i propri file, foto, email) ma non vuole che Google — un concorrente con un modello di business pubblicitario — veda le proprie query AI. PCC sfrutta questa asimmetria di fiducia.

## Varianti e approcci analoghi

**Intel TDX e AMD SEV.** I principali produttori di CPU per datacenter offrono Trusted Execution Environment (TEE) hardware per il cloud: Intel Trust Domain Extensions e AMD Secure Encrypted Virtualization. Questi meccanismi consentono di eseguire VM con memoria crittografata, inaccessibile al cloud provider. PCC e' un'implementazione proprietaria dello stesso principio su Apple Silicon, con garanzie aggiuntive legate al Secure Boot chain e all'immagine software verificabile.

**Confidential computing per AI di terze parti.** Il pattern PCC si distingue dai TEE standard perche' il software che gira nell'enclave (il modello) appartiene a un vendor (Google) diverso da chi controlla l'hardware (Apple). Questa separazione — vendor modello vs. vendor hardware — e' la caratteristica distintiva: in un TEE standard il cloud provider controlla il software, mentre in PCC il vendor del modello fornisce i pesi ma non controlla l'ambiente.

**Apple Secure Enclave storica.** Apple usa la Secure Enclave nei propri dispositivi dal 2013 (iPhone 5S) per proteggere chiavi crittografiche e biometria. PCC estende il principio al cloud per la prima volta: dalla Secure Enclave del chip alla Secure Enclave del server.

## Quando usarlo / quando no

PCC e' rilevante come template architetturale per chi deve costruire sistemi AI con le seguenti caratteristiche:

**Casi d'uso in cui PCC e' il pattern corretto:**
- Modelli frontier (>100B parametri) che non possono girare on-device.
- Dati utente sensibili che non devono essere accessibili al vendor del modello.
- Contesti in cui l'utente si fida dell'OS vendor / hardware vendor ma non del vendor del modello.
- Deployment su piattaforme consumer dove la privacy percepita dall'utente e' un fattore di adozione critico.

**Quando PCC non e' la scelta giusta:**
- Modelli che possono girare on-device con qualita' sufficiente: PCC aggiunge latenza network e complessita' operativa.
- Contesti in cui anche l'OS vendor (chi controlla i server) e' un soggetto non trusted: PCC non garantisce privacy verso chi controlla fisicamente i server.
- Ambienti dove la verifica dell'immagine software dell'enclave non e' possibile: la garanzia di PCC dipende dalla capacita' di audit dell'immagine.
- Sistemi che richiedono logging degli input per compliance (es. alcuni contesti regolati): PCC e' progettato per essere stateless, incompatibile con log mandatori.

## Esempi pratici

**Apple + Google (WWDC 2026).** Siri 2.0 esegue le query che richiedono Gemini 1.2T su PCC. Apple dice a Google: "ecco i tuoi pesi, ti paghiamo $1 miliardo l'anno, ma non puoi vedere cosa chiedono i nostri utenti". Apple dice ai propri utenti: "Gemini gira su nostri server, in un ambiente che solo noi controlliamo, e i dati non vengono conservati". Il contratto con Google include esplicitamente il divieto di usare le query PCC per il training futuro.

**Il pattern preannunciato.** Il digest del 5 giugno 2026 aveva identificato PCC come "un'architettura di confidential cloud computing che potrebbe diventare un template per i vendor OS": un OS vendor che non vuole (o non puo') addestrare e servire un modello frontier puo' licenziare i pesi dal vendor specializzato (OpenAI, Anthropic, Google) ed eseguirli in un ambiente che il vendor del modello non controlla. Il WWDC 2026 ha trasformato questa ipotesi in prodotto con miliardi di utenti.

## Letture

- Apple, "Private Cloud Compute: A new frontier for AI privacy in the cloud", 2024. https://security.apple.com/blog/private-cloud-compute/ (annuncio iniziale del pattern PCC)
- MacRumors, "WWDC 2026 — Apple reveals Gemini-powered Siri", 8 giugno 2026. https://www.macrumors.com/guide/wwdc-2026-what-to-expect/
- AppleInsider, "iOS 27, macOS 27, Siri: What to expect to launch at WWDC 2026", 5 giugno 2026. https://appleinsider.com/articles/26/06/05/ios-27-macos-27-siri-what-to-expect-to-launch-at-wwdc-2026
- Macworld, "Apple to use Google servers with Nvidia hardware for the new Siri", giugno 2026. https://www.macworld.com/article/3156959/apple-to-use-google-servers-with-nvidia-hardware-for-the-new-siri.html
- Intel, "Intel Trust Domain Extensions (Intel TDX)", 2022. https://www.intel.com/content/www/us/en/developer/articles/technical/intel-trust-domain-extensions.html
- AMD, "AMD Secure Encrypted Virtualization (AMD SEV)", 2022. https://developer.amd.com/sev/

## Aggiornamenti

### 2026-06-08

Concetto documentato per la prima volta. Apple svela Siri 2.0 al WWDC 2026 (8 giugno) con PCC come architettura di inference per il modello Gemini 1.2T (8+ fonti indipendenti: MacRumors, Tom's Guide, CNBC, AppleInsider, Bloomberg, cryptobriefing, letsdatascience, heygotrade). E' la prima implementazione su larga scala (miliardi di dispositivi) del pattern confidential cloud computing per AI, dove il vendor del modello (Google) e il vendor dell'hardware/OS (Apple) sono soggetti distinti. Il pattern era stato anticipato nel digest del 5 giugno 2026 come "un'architettura che potrebbe diventare un template per i vendor OS". Il WWDC 2026 ne conferma la maturita' come prodotto. [Digest 2026-06-08](../../digest/2026/06/08.md)
