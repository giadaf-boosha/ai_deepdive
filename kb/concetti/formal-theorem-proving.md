---
name: Formal theorem proving via LLM
aliases: [formal theorem proving, dimostrazione automatica di teoremi, formal verification via LLM, dimostrazione matematica formale, Lean proof, automated theorem proving]
categoria: paradigma
created: 2026-08-11
last_updated: 2026-08-11
---

# Formal theorem proving via LLM

## Cos'e

E' l'uso di un LLM per produrre dimostrazioni matematiche formali — verificate meccanicamente da un proof assistant come Lean 4, Coq o Isabelle — invece di dimostrazioni informali in linguaggio naturale. La differenza con la matematica "generata" da un chatbot e' categorica: una dimostrazione formale viene compilata da un kernel logico che accetta o rifiuta ogni singolo passo, per cui il verdetto finale (vero/falso, dimostrato/non dimostrato) non dipende dalla fiducia riposta nel modello che l'ha prodotta, ma dalla correttezza del kernel stesso — tipicamente uno dei componenti software piu' scrutinati e stabili nell'ecosistema dei linguaggi di dimostrazione.

Nel 2026 il formal theorem proving via LLM e' emerso come un canale distinto attraverso cui i laboratori frontier comunicano i progressi di modelli non ancora rilasciati pubblicamente. Invece di un benchmark (che puo' essere overfittato o "hackato", vedi `evaluation-benchmark.md`) o di una demo di prodotto, il laboratorio pubblica un risultato di ricerca matematica su un problema aperto, accompagnato da un certificato di verifica formale scaricabile ed eseguibile da chiunque abbia un installazione di Lean. Il segnale e' piu' difficile da falsificare di un punteggio benchmark: o il kernel accetta la dimostrazione, o non la accetta.

## Come funziona

Il flusso tipico osservato nei due casi finora documentati (OpenAI Astra, Anthropic Claude research) e' comune. Il modello riceve un problema aperto di matematica pura — spesso una congettura nota da anni o decenni nella comunita' — e lavora in modo agentico su larga scala: decine di subagenti, milioni di token di output, migliaia di comandi eseguiti (lettura di paper, calcoli simbolici, tentativi di dimostrazione, backtracking). Il modello produce sia un argomento in linguaggio naturale sia — passo cruciale — una traduzione della dimostrazione in un linguaggio di prova formale (Lean 4 nei due casi noti), che viene poi compilata dal kernel del proof assistant. Un "sorry count" pari a zero significa che nessun passo della dimostrazione formale resta non dimostrato/assunto: l'intera catena logica e' verificata meccanicamente.

Il laboratorio accompagna la pubblicazione con: un manoscritto tecnico esteso (centinaia di pagine nel caso OpenAI Astra), il codice della formalizzazione Lean su repository pubblico (GitHub), e una fase di revisione informale da parte di matematici di alto profilo — sia interni al laboratorio sia esterni, reclutati per validare la significativita' matematica del risultato (non solo la sua correttezza formale, gia' garantita dal kernel). Il risultato non passa per un processo di peer review accademico tradizionale prima della pubblicazione: la validazione "prima" e' quella dei revisori invitati dal laboratorio, la validazione "dopo" e' quella della comunita' matematica che esamina il preprint.

Un punto tecnico rilevante e' che il modello usato resta tipicamente non identificato o non rilasciato pubblicamente al momento dell'annuncio (Astra per OpenAI, un "modello di ricerca" non nominato per Anthropic): il risultato non e' quindi riproducibile end-to-end da terzi, a differenza della dimostrazione formale stessa che e' pubblica e ricompilabile da chiunque.

## Varianti / approcci

- **Problemi aperti in teoria dei numeri/algebra** (Anthropic, 10 agosto 2026): innalzamento di un lower bound dimostrato su una proprieta' quantitativa nota (percentuale di zeri della zeta di Riemann sulla retta critica), non una dimostrazione completa della congettura di fondo.
- **Batch di problemi aperti eterogenei** (OpenAI Astra, 1 agosto 2026): dieci risultati distinti in teoria dei gruppi, algebre di von Neumann, geometria ad alta dimensione, complessita' quantistica, crittografia su reticoli, combinatoria estremale — inclusa la prima costruzione esplicita di un gruppo non-sofico, questione aperta dal 1999.
- **Verifica formale come garanzia epistemica**: in entrambi i casi il laboratorio usa esplicitamente la formalizzazione Lean come argomento per elevare la credibilita' del risultato rispetto a un claim puramente testuale del modello, in un contesto (matematica avanzata) dove la verifica umana indipendente e' costosa e lenta.

## Quando usarlo

Il pattern e' rilevante per chi valuta l'affidabilita' dei claim di capacita' di un laboratorio frontier su un modello non ancora accessibile pubblicamente: a differenza di un benchmark auto-riportato, un certificato Lean pubblico e' verificabile da terzi con strumenti standard (l'installazione di Lean e la compilazione del certificato), anche se la significativita' matematica del contributo e la sua novita' rispetto alla letteratura restano da valutare con competenza di dominio. E' un segnale utile per distinguere "il modello sa rispondere bene a domande di matematica da benchmark" da "il modello ha contribuito un risultato nuovo, verificato meccanicamente, alla ricerca matematica" — due claim di capacita' molto diversi, spesso confusi nella copertura mediatica generalista.

Va usato con cautela come proxy di capacita' generale: entrambi i casi noti riguardano aree di matematica pura molto specifiche, con un run costruito ad hoc (decine di subagenti, milioni di token, guidato da matematici del laboratorio) — non e' evidenza diretta di capacita' di ricerca autonoma trasferibile ad altri domini scientifici.

## Esempi pratici

- Anthropic, 10 agosto 2026: un modello Claude di ricerca non rilasciato dimostra che almeno il 67,250% degli zeri non banali della funzione zeta di Riemann sono semplici e sulla retta critica (contro il 41,6% del precedente miglior risultato umano), con un run da 31 milioni di token di output, circa 60 subagenti, 2.400 comandi shell, lettura di 54 paper arXiv. Formalizzazione Lean su GitHub (`anthropics/zeta-23-lean`), revisione di matematici interni (Levent Alpoge, Ralph Furman) ed esterni (Brian Conrey, Dan Goldston). Non e' una dimostrazione dell'ipotesi di Riemann completa.
- OpenAI, 1 agosto 2026: il modello Astra (non ancora rilasciato) produce dieci dimostrazioni verificate in Lean 4 su problemi aperti da almeno un decennio, con "sorry count" zero su tutte, accompagnate da un manoscritto tecnico di 249 pagine. Il vincitore della medaglia Fields Timothy Gowers dichiara che raccomanderebbe una delle dimostrazioni per una rivista di primo livello senza esitazione.

## Letture

- [Anthropic — Learning more about Claude's mathematical capabilities](https://www.anthropic.com/research/riemann-zeta)
- [GitHub — anthropics/zeta-23-lean](https://github.com/anthropics/zeta-23-lean)
- [SiliconANGLE — OpenAI's Astra solves 10 long-open math problems and publishes the proofs](https://siliconangle.com/2026/08/02/openais-astra-solves-10-long-open-math-problems-publishes-proofs/)

## Aggiornamenti

### 2026-08-11

Prima scheda del concetto, creata in seguito alla seconda istanza in dieci giorni di un laboratorio frontier che comunica i progressi di un modello non rilasciato tramite un risultato di matematica pura formalizzato in Lean: OpenAI Astra (1 agosto, dieci dimostrazioni) e Anthropic Claude research (10 agosto, lower bound Riemann zeta dal 41,6% al 67,2%). Vedi [digest 2026-08-11](../../digest/2026/08/11.md); il caso OpenAI Astra era gia' stato coperto nel [digest 2026-08-03](../../digest/2026/08/03.md) ma allora valutato sotto soglia per una scheda KB dedicata.
