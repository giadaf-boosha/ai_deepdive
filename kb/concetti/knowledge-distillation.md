---
name: Knowledge Distillation
aliases: [knowledge distillation, distillazione, model distillation, distillazione di modello, adversarial distillation, response distillation, student-teacher, distillazione avversariale]
categoria: training
created: 2026-06-25
last_updated: 2026-06-25
mentions_count: 6
---

# Knowledge Distillation

## Cos'e

La knowledge distillation e' una tecnica di training in cui un modello piu' piccolo ("student") apprende da un modello piu' grande e capace ("teacher"), usando gli output del teacher come supervision signal invece di — o in aggiunta a — i label originali del dataset. L'obiettivo e' trasferire le capacita' del teacher allo student a una frazione del costo di parametri e, di conseguenza, a un costo di inference significativamente inferiore.

Il concetto fu formalizzato da Hinton, Vinyals e Dean in "Distilling the Knowledge in a Neural Network" (2015, NeurIPS workshop), dove mostrano che le distribuzioni di probabilita' "soft" prodotte da un modello grande su un esempio contengono informazioni strutturali sul problema — le "dark knowledge" — che i label one-hot non catturano. Addestrare lo student a riprodurre queste distribuzioni soft trasferisce non solo la risposta corretta ma la relazione implicita tra le classi che il teacher ha appreso.

Nel contesto dei large language model, la distillation ha assunto forme diverse rispetto alla classificazione originale. La difficolta' principale e' che i LLM producono distribuzioni su un vocabolario da decine di migliaia di token: allineare le architetture teacher-student diventa complesso se differiscono nel vocabolario o nella struttura. Nella pratica del 2024-2026, la forma piu' comune e' la response distillation: lo student viene addestrato su conversazioni generate dal teacher tramite supervised fine-tuning, senza accesso ai logit interni del teacher. E' la forma piu' semplice e piu' diffusa perche' richiede solo accesso all'output del teacher, non ai suoi pesi o alle sue attivazioni interne.

## Come funziona

### Distillazione classica (logit-level)

Il teacher produce una distribuzione di probabilita' sull'output per ogni esempio. Lo student e' addestrato minimizzando la divergenza KL tra la propria distribuzione e quella del teacher, tipicamente con una temperatura T > 1 che "ammorbidisce" le distribuzioni rendendole piu' informative (Hinton et al. 2015). La loss totale e' una combinazione pesata della cross-entropy sui label duri (hard targets) e della KL divergence sulle distribuzioni soft (soft targets).

La temperatura T controlla il trade-off: T=1 equivale a standard softmax, T alto appiattisce le probabilita' rendendole piu' simili a distribuzioni uniformi, amplificando il segnale delle classi meno probabili ma comunque plausibili.

### Response distillation (output-level)

Il teacher genera risposte complete a un insieme di prompt. Le coppie prompt-risposta vengono usate per fare supervised fine-tuning dello student. Non e' necessario accedere ai pesi o ai logit del teacher: basta un'API o un endpoint che ritorna il testo generato. E' la tecnica usata dai dataset sintetici come Alpaca (GPT-3.5 come teacher), WizardLM, Orca (GPT-4 come teacher), e piu' in generale da qualsiasi pipeline che usa un modello frontier per generare dati di training per un modello minore.

### Feature distillation (layer-level)

Invece di distillare solo l'output finale, lo student apprende a replicare le attivazioni intermedie del teacher (hidden states, attention maps). Richiede una certa somiglianza architetturale tra teacher e student (stessa profondita' o meccanismo di proiezione) ed e' computazionalmente piu' esigente della response distillation. Produce studenti piu' efficienti in termini di numero di parametri necessari per raggiungere le stesse performance. Esempi: TinyBERT (Jiao et al. 2020) che distilla BERT a ogni layer; DistilBERT (Sanh et al. 2019) che usa una variante piu' semplice a layer alterni.

### Adversarial distillation (attacco)

La adversarial distillation e' la distillazione eseguita da un attore non autorizzato che accede sistematicamente all'API pubblica di un frontier model per raccogliere output e usarli per addestrare un modello concorrente senza sostenere i costi di R&D originali. Non e' una variante tecnica distinta — e' sempre response distillation dal punto di vista del training — ma si distingue per il contesto: l'accesso al teacher avviene tramite account fraudolenti in violazione dei termini di servizio, il volume di query e' anomalo (milioni di scambi in pochi mesi), e il fine e' il furto di capacita' competitive.

Il meccanismo e' semplice: creare account multipli per aggirare i rate limit e le policy di utilizzo accettabile, inviare un corpus di prompt progettato per elicitare le capacita' target del modello (coding, ragionamento, dominio specifico), raccogliere le risposte, filtrare le risposte di alta qualita' e usarle come dataset di training per il modello student. Il risultato e' un modello che approssima le capacita' del teacher a una frazione del costo di sviluppo.

## Varianti / approcci

| Variante | Accesso al teacher | Complessita' | Uso principale |
|---|---|---|---|
| Logit distillation | Logit completi | Alta | Classificazione, modelli custom |
| Response distillation | Solo testo output | Bassa | SFT su modelli open, dataset sintetici |
| Feature distillation | Attivazioni interne | Alta | Compressione architetturale |
| Adversarial distillation | API pubblica (non autorizzato) | Bassa (tecnicamente) | Furto di capacita' competitive |
| Self-distillation | Il modello e' teacher di se stesso | Media | Miglioramento senza dati aggiuntivi |

## Quando usarlo / quando no

**Usare la distillation per:**
- Ridurre i costi di inference mantenendo qualita' accettabile: un modello 8B addestrato su output di un 70B puo' avvicinarsi al 70B su task specifici con un quarto del costo di serving.
- Adattare un frontier model a un dominio senza accesso ai suoi pesi: response distillation tramite API e' la sola opzione disponibile per i modelli closed.
- Accelerare il fine-tuning di un modello student su dati scarsi: i dati sintetici generati dal teacher ampliano il training set su distribuzioni difficili da raccogliere manualmente.
- Creare modelli specializzati per deployment edge o on-device dove la dimensione del modello e' il vincolo primario.

**Non usare la distillation quando:**
- Si ha accesso ai pesi del teacher: il fine-tuning diretto o il pruning sono spesso piu' efficienti.
- Il task richiede capacita' che il teacher non possiede: la distillation trasferisce capacita' presenti nel teacher, non capacita' assenti.
- La qualita' del teacher non e' verificata sul task target: "garbage in, garbage out" si amplifica nella distillation perche' gli errori sistematici del teacher diventano pattern nello student.
- I termini di servizio del provider vietano la distillation: la maggior parte dei termini di uso accettabile dei frontier model (Anthropic, OpenAI, Google) vietano esplicitamente l'uso degli output per addestrare modelli concorrenti. Violare questi termini configura la adversarial distillation come violazione contrattuale e, potenzialmente, di norme sugli export control.

## Esempi pratici

**Pipeline di response distillation autorizzata.** Un team vuole un modello di customer support specializzato per il proprio dominio, piu' economico da servire di GPT-5. Il processo: (1) raccogliere 5.000 conversazioni reali con cliente; (2) generare risposte con GPT-5 (o Claude Opus) tramite API ufficiale su ogni conversazione, rispettando i rate limit; (3) filtrare le risposte sotto una soglia di qualita' valutata con LLM-as-a-judge; (4) fare SFT di Llama 3 70B sul dataset filtrato con 3 epoche e learning rate 2e-5; (5) valutare con MT-Bench e con un golden set proprietario. Il modello risultante gira su una singola H100 a 1/10 del costo dell'API frontier, con qualita' comparabile sui task in-distribution.

**Segnali di anomalia per chi gestisce API.** Un provider di API che vuole rilevare adversarial distillation osserva: volume di query anomalamente alto per un singolo account o cluster di account correlati; prompt sintetici o semi-sintetici con distribuzioni molto diverse dall'uso organico; sampling sistematico su aree di capacita' specifiche (coding, ragionamento matematico) con prompt costruiti per coprire il dominio; mancanza di sessioni interattive (nessun multi-turn, nessuna correzione, solo query isolated). La correlazione tra questi segnali identifica il pattern con alta specificita'.

## Letture

- Hinton, Vinyals, Dean, "Distilling the Knowledge in a Neural Network", 2015. https://arxiv.org/abs/1503.02531
- Sanh et al., "DistilBERT, a distilled version of BERT: smaller, faster, cheaper and lighter", 2019. https://arxiv.org/abs/1910.01108
- Jiao et al., "TinyBERT: Distilling BERT for Natural Language Understanding", 2020. https://arxiv.org/abs/1909.10351
- Mukherjee et al., "Orca: Progressive Learning from Complex Explanation Traces of GPT-4", 2023. https://arxiv.org/abs/2306.02707
- Taori et al., "Alpaca: A Strong, Replicable Instruction-Following Model" (Stanford CRFM, 2023). https://crfm.stanford.edu/2023/03/13/alpaca.html

## Aggiornamenti

### 2026-06-25

Anthropic ha reso pubblica il 24 giugno una lettera al Senate Banking Committee (senatori Tim Scott ed Elizabeth Warren, datata 10 giugno 2026) che documenta il piu' grande caso accertato di adversarial distillation nella storia dei frontier model. Tra il 22 aprile e il 5 giugno 2026, circa 25.000 account fraudolenti hanno condotto 28,8 milioni di scambi con i modelli Anthropic — in modo specifico Mythos Preview nelle aree di software engineering e ragionamento agentico — con il fine di estrarre output da usare nel training di un modello concorrente riconducibile ad Alibaba. La risposta tecnica di Anthropic ha incluso il ban degli account e l'identificazione dei pattern anomali (volume, sistematicita', correlazione temporale); la risposta politica e' la lettera al Congresso con richiesta di nuove misure legislative. Il caso e' rilevante per la governance della distillation per due ragioni. Prima, introduce per la prima volta la tesi che la distillazione sistematica di un frontier model via API fraudolenta debba essere classificata come violazione degli export control (EAR) oltre che dei termini di servizio — equiparando l'estrazione delle capacita' di un modello all'esportazione non autorizzata della tecnologia sottostante. Se la tesi trovasse riscontro legislativo, il quadro normativo della distillation cambierebbe significativamente: non piu' solo responsabilita' contrattuale, ma potenzialmente sanzioni federali. Seconda, la scala dell'attacco (28,8M scambi in 45 giorni) quantifica per la prima volta il volume necessario per una distillation efficace su capacita' frontier di coding e ragionamento: e' un dato di riferimento per chi disegna sistemi di rilevamento delle anomalie API. [Digest 2026-06-25](../../digest/2026/06/25.md)
