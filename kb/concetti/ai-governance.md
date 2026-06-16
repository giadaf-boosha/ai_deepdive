---
name: AI Governance
aliases: [AI governance, governance AI, export control AI, regolazione AI, AI regulation, AI policy, BIS AI, EAR AI models]
categoria: regolazione
created: 2026-06-14
last_updated: 2026-06-16
mentions_count: 13
---

# AI Governance

## Cos'e

AI governance e' l'insieme degli strumenti normativi, istituzionali e contrattuali che regolano lo sviluppo, la distribuzione e l'uso dei sistemi di intelligenza artificiale. La governance riguarda sia chi puo' accedere a un modello (export control, licensing), sia come il modello viene sviluppato (safety requirements, red-teaming obbligatorio), sia quali usi sono permessi o vietati (regolazione settoriale, AI Act europeo). Nel 2026 il perimetro si e' espanso rapidamente: dall'autoregolamentazione volontaria dei lab (policy interne, usage policy, responsible scaling policy) verso forme di intervento statale diretto che includono export control, audit obbligatori e — per la prima volta a giugno 2026 — direttive di sospensione di modelli gia' in produzione.

L'importanza della governance AI per i practitioner e' cresciuta in parallelo con la capacita' dei modelli. Fino al 2023, un'organizzazione poteva scegliere di adottare un LLM valutando quasi esclusivamente dimensioni tecniche (qualita', costo, latenza, privacy). A partire dal 2024, variabili di governance sono diventate fattori operativi: quale modello e' disponibile nella mia regione geografica, quali dati posso inviare al provider, il modello che sto usando oggi potrebbe essere rimosso domani per ragioni normative? Con la direttiva BIS del 13 giugno 2026 su Claude Fable 5 e Mythos 5 — prima sospensione di un LLM commerciale ordinata da un governo — queste domande hanno smesso di essere ipotetiche.

Il campo si articola in tre grandi aree. Export control regola chi puo' accedere a tecnologie AI sensibili in base alla nazionalita' o alla giurisdizione; la categoria e' tradizionalmente associata all'hardware (chip Nvidia con direttive EAR dal 2022) e si e' estesa nel 2026 ai modelli-software. Regolazione dei sistemi AI riguarda i requisiti che i sistemi devono soddisfare prima o durante il deployment: l'AI Act europeo (in vigore progressivo dal 2024) e' il framework piu' strutturato con una classificazione risk-based; negli USA il quadro e' ancora frammentato per settore (FDA per medical device AI, NIST AI RMF come linea guida volontaria, ordini esecutivi successivi). Safety e alignment governance riguarda i processi interni ai lab: responsible scaling policy (Anthropic, OpenAI, Google DeepMind) che condizionano il rilascio di nuove capacita' al superamento di soglie di sicurezza; red-teaming obbligatorio pre-rilascio; API trust and safety policies.

## Come funziona

### Export control

Gli export control statunitensi operano attraverso l'Export Administration Regulations (EAR), gestito dal Bureau of Industry and Security (BIS) del Dipartimento del Commercio. L'EAR classifica le tecnologie con una Commerce Control List (CCL): ogni tecnologia e' associata a un Export Control Classification Number (ECCN) che specifica a quali paesi e a quali usi la tecnologia puo' essere esportata o meno, e quali licenze sono necessarie.

Fino al 2022, i modelli di machine learning non erano esplicitamente nel perimetro EAR come categoria distinta: erano prodotti software ordinari. La prima applicazione sistematica degli export control al campo AI e' venuta dall'hardware: con le misure del 7 ottobre 2022, il Dipartimento del Commercio ha vietato l'esportazione verso la Cina di GPU Nvidia sopra certe soglie computazionali (H100, H800 e successive varianti). Le misure sono state aggiornate nel luglio 2023 (restrizioni su A100, A800 varianti cinesi) e nel novembre 2023 (divieto su qualsiasi GPU con A_100 pari o superiori a certi livelli in determinati paesi).

La direttiva BIS del 13 giugno 2026 su Claude Fable 5 e Mythos 5 rappresenta un salto categoriale: per la prima volta un'ordine di export control riguarda un modello-software come servizio, non l'hardware su cui gira. La base giuridica invocata nella direttiva sono le "national security authorities" dell'EAR; la specifica preoccupazione comunicata da Anthropic e' che il governo ritenesse il modello capace di essere usato per identificare vulnerabilita' software in modo che costituisce una minaccia alla sicurezza nazionale. Il meccanismo tecnico dell'ordine e' insolito: invece di vietare l'esportazione a paesi specifici (come avviene per i chip), la direttiva vieta l'accesso a qualsiasi "foreign national" ovunque si trovi, inclusi i dipendenti Anthropic con cittadinanza straniera. Questo perimetro ha reso impossibile la conformita' selettiva e ha costretto alla sospensione globale.

### AI Act europeo

L'AI Act dell'Unione Europea (Regolamento (UE) 2024/1689) e' il primo framework legislativo organico per i sistemi di IA al mondo. Classifica i sistemi AI in quattro categorie di rischio. Rischio inaccettabile: sistemi vietati (es. scoring sociale da parte dei governi, manipolazione psicologica subliminale). Alto rischio: sistemi soggetti a requisiti obbligatori di trasparenza, documentazione, audit e conformita' (es. AI in selezione del personale, credito, sistemi giudiziari, infrastrutture critiche). Rischio limitato: requisiti di trasparenza (es. chatbot che devono dichiarare di essere AI). Rischio minimo: senza requisiti specifici (es. filtri antispam). I "General Purpose AI Models" — categoria che include i frontier LLM — sono soggetti a requisiti trasversali come valutazione dei rischi sistemici, testing, red-teaming e reporting agli organi di vigilanza. Per i modelli con capacita' computazionali superiori a 10^25 FLOP (soglia che nel 2026 include tutti i modelli frontier), i requisiti diventano piu' stringenti. Il Colorado AI Act (SB 26-189, maggio 2026) negli USA e' un esempio di legislazione statale che introduce obblighi di trasparenza e disclosure per sistemi AI usati in decisioni consequenziali (impiego, credito, servizi essenziali), con effetto dal gennaio 2027.

### Responsible Scaling Policy

I principali lab AI hanno adottato framework interni che condizionano il rilascio di nuovi modelli al superamento di valutazioni di sicurezza. Anthropic ha la "Responsible Scaling Policy" (RSP): definisce "AI Safety Levels" (ASL) in analogia ai biosafety level, con requisiti di safety e interpretability che devono essere soddisfatti prima che un modello ASL-n possa essere sviluppato o distribuito. OpenAI ha il "Safety Readiness Framework"; Google DeepMind ha il "Frontier Safety Framework". Questi framework sono volontari ma vincolanti contrattualmente per le societa' che li hanno adottato; alcuni investitori istituzionali li richiedono come condizione di investimento.

## Varianti / approcci

| Meccanismo | Chi lo applica | Quando si attiva |
|---|---|---|
| Export control hardware (EAR/BIS) | US Dept of Commerce | Al trasferimento fisico o logico di tecnologia verso entita' straniere |
| Export control modelli (EAR/BIS) | US Dept of Commerce | Al momento dell'accesso via API o download da parte di foreign nationals |
| AI Act EU — high risk | European AI Office | Al deploy di sistemi in categorie regolamentate |
| Responsible Scaling Policy | Lab stesso | Pre-rilascio, sulla base di capability evaluations interne |
| API usage policy | Lab stesso | Enforcement retroattivo su account in violazione |
| Legislazione statale USA (es. CO SB 189) | Stato + AG | Per sistemi AI in decisioni consequenziali su consumatori |

## Quando usarlo / quando no

Il framework di AI governance piu' rilevante dipende dalla giurisdizione di deploy, dalla nazionalita' degli utenti e dalla categoria di rischio del caso d'uso.

Per chi distribuisce API AI a utenti internazionali: l'evento Fable 5 introduce un nuovo fattore di vendor risk. La domanda "il modello che uso oggi potrebbe essere sospeso domani per ragioni normative?" non e' piu' ipotetica. Implicazioni pratiche: avere un piano di fallback documentato (modello alternativo, provider alternativo) nei contratti enterprise; specificare nei SLA cosa avviene in caso di indisponibilita' del modello per causa di forza maggiore normativa; considerare multi-provider come pattern di resilienza.

Per chi costruisce sistemi AI in contesti ad alto rischio (selezione del personale, credito, healthcare): verificare se il sistema cade nelle categorie "high risk" dell'AI Act europeo e se gli utenti finali sono in UE. I requisiti di documentazione e audit sono obbligatori e la non conformita' espone a sanzioni fino al 3-6% del fatturato globale.

Per i lab che sviluppano modelli frontier: la direttiva BIS di giugno 2026 suggerisce che le valutazioni di sicurezza interne non sono sufficienti a garantire continuita' del servizio se il governo decide che un modello costituisce un rischio. Il precedente apre la questione di come strutturare il dialogo pre-rilascio con le autorita' regolatorie per ridurre la probabilita' di sospensioni improvvise.

## Esempi pratici

Esempio 1: multi-provider fallback dopo la sospensione Fable 5. Un team che usava `claude-fable-5` via API ha ricevuto errori di modello non disponibile nella serata del 13 giugno 2026. Un sistema con routing multi-provider (LiteLLM, OpenRouter) avrebbe potuto rilevare il 4xx/503 e dirottare automaticamente le richieste su un modello alternativo (Opus 4.8, GPT-5.5, Gemini 3.5 Flash). Il pattern di resilienza e': specificare modello principale e modello fallback nella configurazione del router; testare il fallback regolarmente; documentare nel runbook cosa fare quando il modello principale e' indisponibile.

Esempio 2: valutazione AI Act per un sistema di screening CV. Prima del deploy in Europa, verificare: il sistema prende decisioni consequenziali sull'impiego (si)? E' usato da un'organizzazione con sede o con impatto in UE (si)? Quindi ricade nella categoria high-risk. Requisiti obbligatori: documentazione tecnica dettagliata; log delle decisioni; testing su bias e discriminazione; meccanismo di supervisione umana; notifica all'autorita' competente. Il non rispetto espone a sanzioni e a impossibilita' di deploy.

Esempio 3: verifica della Responsible Scaling Policy prima di distribuire un modello fine-tuned. Se il fine-tuning amplia le capacita' di un modello su domini sensibili (biosicurezza, cyber offensivo), la RSP di Anthropic prevede valutazioni specifiche prima della distribuzione. Ignorarlo puo' portare al ritiro del modello dal marketplace o alla chiusura dell'account API.

## Letture

- European Commission, "Artificial Intelligence Act" (Regolamento UE 2024/1689). https://digital-strategy.ec.europa.eu/en/policies/regulatory-framework-ai
- US Department of Commerce / BIS, "Export Controls on Advanced Computing and Semiconductor Manufacturing Items" (ottobre 2022 e aggiornamenti). https://www.bis.doc.gov/
- NIST, "Artificial Intelligence Risk Management Framework (AI RMF 1.0)". https://www.nist.gov/system/files/documents/2023/01/26/NIST.AI.100-1.pdf
- Anthropic, "Responsible Scaling Policy". https://www.anthropic.com/news/responsible-scaling-policy
- Wilson Sonsini, "Colorado Legislature Repeals and Replaces Colorado AI Act: What SB 189 Means for Your Business" (maggio 2026). https://www.wsgr.com/en/insights/colorado-legislature-repeals-and-replaces-colorado-ai-act-what-sb-189-means-for-your-business.html

## Aggiornamenti

### 2026-06-14

Prima direttiva di export control nella storia per un LLM come modello-servizio. Il 13 giugno 2026, il Bureau of Industry and Security del Dipartimento del Commercio USA ha ordinato ad Anthropic la sospensione immediata dell'accesso a Claude Fable 5 e Mythos 5 per qualsiasi cittadino straniero. L'ambito dell'ordine — inclusi i dipendenti Anthropic con cittadinanza straniera — ha reso impossibile la conformita' selettiva e costretto alla disabilitazione globale. E' il primo caso documentato di un governo che ordina la sospensione di un LLM gia' in produzione commerciale. Anthropic ha rispettato l'ordine e contestualmente ha rilasciato una dichiarazione pubblica di disaccordo, sostenendo che il precedente implica un blocco sistemico per tutti i futuri lanci frontier USA. I modelli erano stati lanciati quattro giorni prima (9 giugno). [Digest 2026-06-14](../../digest/2026/06/14.md)

### 2026-06-15

Nuovi dettagli sul ban Fable 5/Mythos 5 chiariscono la dinamica causale: il trigger immediato e' stato Andy Jassy (CEO Amazon, principale investitore e cloud host di Anthropic) che ha personalmente allertato Treasury Secretary Scott Bessent il 12 giugno, dopo che ricercatori Amazon avevano estratto da Fable 5 informazioni su vulnerabilita' software offensive tramite una sequenza di prompt. La comunicazione Jassy-Bessent (Treasury) ha avviato l'escalation verso il Commerce (BIS/Lutnick) che ha prodotto la direttiva in 24 ore. Questo introduce un elemento strutturale nuovo: Amazon agisce simultaneamente come investitore di Anthropic ($8 miliardi impegnati), cloud host primario delle API Anthropic e origine della segnalazione che ha innescato il ban — un conflitto di interessi triplicato documentato pubblicamente. David Sacks (13-14 giugno) ha indicato che il ban puo' essere revocato se Anthropic implementa la correzione richiesta; Anthropic mantiene che il jailbreak non e' sistemico. Il caso consolida un pattern di governance AI inedito: attori privati in posizioni di co-interesse (investitore + cloud host) diventano segnalatori regolatori, con tempi di risposta governativa di ore anziche' mesi. [Digest 2026-06-15](../../digest/2026/06/15.md)

### 2026-06-16

Nuovi dettagli sulla crisi Fable 5 emergono nelle ultime 24 ore. Il vettore tecnico del jailbreak "Fix this code" e' ora documentato: una sequenza di prompt che inizia con una richiesta di debug di codice legittimo e introduce progressivamente codice contenente placeholder per vulnerabilita' offensive, sfruttando la tendenza del modello a completare pattern sintatticamente coerenti. Dario Amodei ha rifiutato pubblicamente l'ultimatum governativo — implementare una correzione entro 48 ore o affrontare un ban esteso — sostenendo che il jailbreak non e' sistemico ma situazionale e che una correzione forzata in 48 ore introduce rischi di regressione superiori al rischio originale. Il 15 giugno, un team di ingegneri Anthropic e' a Washington per incontri con BIS e con il team di David Sacks (OSTP): la negoziazione tecnica e' sulla soglia di accettazione della correzione, non sulla natura del problema. Il caso consolida il pattern emerso il 14 giugno: un attore privato in posizione di co-interesse (investitore + cloud host) innesca una risposta regolatoria in 24 ore, e il lab deve negoziare la revoca del ban in tempo reale mentre mantiene il servizio per gli utenti non-stranieri. La variabile critica e' la definizione di "correzione sufficiente": se il governo accetta patching contestuale, il ban potrebbe essere revocato in settimana; se richiede una garanzia sistemica, i tempi si allungano a una nuova versione del modello. [Digest 2026-06-16](../../digest/2026/06/16.md)
