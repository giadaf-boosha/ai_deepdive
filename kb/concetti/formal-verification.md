---
name: Formal Verification / Theorem Proving assistito da LLM
aliases: [formal verification, theorem proving, dimostrazione formale, formalizzazione matematica, Lean proof, autoformalizzazione, computer-checked proof, theorem formalization]
categoria: tecnica
created: 2026-09-12
last_updated: 2026-09-12
---

# Formal Verification / Theorem Proving assistito da LLM

## Cos'e

La formal verification (verifica formale) in matematica e' il processo di esprimere una dimostrazione in un linguaggio logico completamente rigoroso — un proof assistant come Lean, Coq, Isabelle o Agda — cosi' che un programma (il kernel del proof assistant) possa controllare meccanicamente, passo per passo, che ogni inferenza sia corretta secondo le regole della logica sottostante. A differenza di una dimostrazione scritta in linguaggio naturale su una rivista matematica, che viene validata da revisori umani e puo' contenere lacune o errori non rilevati per anni, una dimostrazione formalizzata e verificata al computer non lascia margine di ambiguita': se il kernel accetta la prova, la prova e' corretta rispetto agli assiomi dichiarati, punto.

Il "theorem proving" assistito da LLM e' l'applicazione dei modelli linguistici di grandi dimensioni (vedi `./llm.md`) a questo processo: invece di un matematico che scrive a mano migliaia di righe di codice Lean, un LLM (o piu' istanze di un LLM in orchestrazione, vedi `./multi-agent-orchestration.md`) genera il codice della dimostrazione formale, lo sottopone al kernel del proof assistant, osserva l'esito (accettato, rifiutato con errore specifico, o "goal" residuo da chiudere) e itera fino a convergenza. Il campo e' distinto ma imparentato con il "reasoning" generico dei LLM (vedi `./chain-of-thought.md`): mentre il reasoning informale produce testo plausibile ma non verificato, il theorem proving formale produce artefatti verificabili meccanicamente, eliminando per costruzione la classe di errori piu' insidiosa del reasoning matematico assistito da AI, cioe' la dimostrazione che "sembra" corretta ma non lo e'.

L'interesse per il tema e' cresciuto rapidamente nel 2025-2026 in parallelo ai progressi dei modelli su benchmark matematici a livello di competizione (IMO, USAMO — vedi `./evaluation-benchmark.md`, aggiornamento MaxProof 2026-06-15) e alla disponibilita' di proof assistant piu' maturi e di corpora di allenamento (Mathlib per Lean, il piu' grande repository comunitario di matematica formalizzata). Il salto qualitativo del 2026 e' stato passare da dimostrazioni di singoli teoremi o lemmi isolati a formalizzazioni di interi risultati storici di grande complessita', di cui la dimostrazione dell'Ultimo Teorema di Fermat completata da Claude (Anthropic, annunciata il 4 settembre 2026) e' finora l'esempio piu' ampio reso pubblico: oltre 13 milioni di righe di codice Lean e circa 29.500 teoremi intermedi verificati.

## Come funziona

### Il ciclo di autoformalizzazione

Il processo tipico di theorem proving assistito da LLM segue un ciclo iterativo:

```
1. Il sistema riceve l'enunciato del teorema da dimostrare (spesso gia' formalizzato a mano da un esperto, o tradotto dal linguaggio naturale)
2. L'LLM genera una bozza di dimostrazione o di un passo intermedio nel linguaggio del proof assistant (es. tattiche Lean 4)
3. Il codice viene sottoposto al kernel del proof assistant
4. Il kernel restituisce: accettato / rifiutato con errore di sintassi o di tipo / "goal" (sotto-obiettivo) ancora aperto
5. In caso di rifiuto o goal aperto, l'LLM riceve il feedback e genera un tentativo corretto o un passo successivo
6. Il ciclo si ripete finche' il teorema completo e' dimostrato (nessun goal aperto, kernel soddisfatto)
```

Questo schema e' concettualmente simile al tool use (vedi `./tool-use.md`): il proof assistant funge da "tool" che fornisce un segnale di verita' oggettivo e non ambiguo — a differenza della maggior parte dei domini in cui un LLM opera, dove il feedback (una review umana, un test unitario incompleto) e' parziale o rumoroso. Questa proprieta' rende il theorem proving un dominio particolarmente adatto al reinforcement learning (vedi `./rlhf.md` per il concetto di segnale di reward, qui applicato senza feedback umano ma con verifica automatica): il reward e' binario e verificabile a costo computazionale contenuto (l'esecuzione del kernel), permettendo cicli di generazione-verifica-correzione ad altissimo volume senza intervento umano nel loop.

### Decomposizione e scala

Per teoremi di grande complessita' come l'Ultimo Teorema di Fermat, la dimostrazione completa non e' un singolo passaggio ma un albero di migliaia di lemmi intermedi, ciascuno dei quali va formalizzato e dimostrato separatamente prima di poter essere composto nella dimostrazione finale. Questo introduce un problema di orchestrazione (vedi `./multi-agent-orchestration.md`): serve un meccanismo che tenga traccia di quali sotto-teoremi sono gia' dimostrati, quali dipendono da altri non ancora completati, e che distribuisca il lavoro di dimostrazione dei singoli lemmi a istanze di modello che possono lavorare in parallelo su rami indipendenti dell'albero delle dipendenze. Nel caso della dimostrazione di Fermat, Anthropic ha riportato l'uso dello strumento open-source Prove2Me e di "dozzine" di istanze Claude che hanno generato in aggregato circa 6 miliardi di token nell'arco di 11 giorni — un volume di calcolo che rende esplicito come la fattibilita' di questo tipo di impresa dipenda tanto dall'infrastruttura di orchestrazione e dal budget di calcolo quanto dalla capacita' di reasoning del singolo modello.

### Il ruolo di Mathlib e delle librerie di matematica formalizzata

Un fattore abilitante spesso sottovalutato e' l'esistenza di librerie di matematica gia' formalizzata (Mathlib per Lean e' la piu' estesa, con contributi di migliaia di matematici e informatici nel corso di un decennio). Una nuova dimostrazione non parte da zero: puo' richiamare migliaia di lemmi, definizioni e teoremi gia' verificati nella libreria, analogamente a come un programmatore richiama funzioni di libreria invece di riscrivere tutto da capo. La qualita' e la copertura di queste librerie condizionano direttamente la fattibilita' pratica di formalizzare un nuovo risultato: un teorema che richiede aree della matematica poco coperte da Mathlib (geometria algebrica avanzata, teoria dei numeri di frontiera) rimane molto piu' difficile da formalizzare anche con un LLM molto capace, perche' mancano i mattoni di base su cui costruire.

## Varianti / approcci

| Approccio | Cosa fa | Esempio |
|---|---|---|
| Autoformalizzazione diretta | L'LLM traduce un enunciato o una dimostrazione in linguaggio naturale direttamente in codice del proof assistant | Traduzione di risultati da paper esistenti |
| Neural theorem proving con ricerca | L'LLM propone tattiche/passi, un algoritmo di ricerca (es. best-first search) esplora l'albero dei goal aperti | Sistemi tipo GPT-f, Lean Copilot, DeepSeek-Prover |
| Generative verifier + test-time scaling | Piu' tentativi generati in parallelo, un verificatore (il kernel stesso, o un modello ausiliario) seleziona i migliori | MaxProof (vedi `./evaluation-benchmark.md`, aggiornamento 2026-06-15) applicato a IMO/USAMO |
| Orchestrazione multi-agente su larga scala | Decomposizione di un teorema in migliaia di lemmi, dimostrati in parallelo da istanze multiple e ricomposti | Dimostrazione Fermat (Anthropic/Claude, Prove2Me, settembre 2026) |
| Formalizzazione assistita interattiva | Un matematico umano guida il processo passo-passo, l'LLM propone i singoli passi (autocomplete) | Lean Copilot e strumenti IDE-integrati |

La distinzione piu' rilevante per chi valuta questi sistemi e' tra dimostrare teoremi nuovi (research-level, dove l'enunciato stesso e' un contributo originale) e formalizzare teoremi gia' noti e dimostrati in linguaggio naturale (dove il contributo e' "solo" tradurre in un linguaggio verificabile meccanicamente una dimostrazione la cui correttezza matematica e' gia' accettata dalla comunita'). Il caso Fermat rientra nella seconda categoria: il teorema era gia' dimostrato da Andrew Wiles nel 1994, il contributo di Claude e' stato produrre una versione della dimostrazione verificabile meccanicamente riga per riga, non scoprire una dimostrazione nuova. Questo non ne riduce il valore ingegneristico e metodologico, ma va tenuto distinto — anche nella comunicazione editoriale — dal caso, concettualmente piu' ambizioso e non ancora dimostrato pubblicamente su questa scala, di un LLM che dimostra un teorema originale mai provato prima da nessuno.

## Quando usarlo / quando no

La formalizzazione assistita da LLM ha senso quando la correttezza assoluta e verificabile e' un requisito non negoziabile: matematica pura di alto valore (risultati storici, congetture aperte), verifica di algoritmi critici per la sicurezza, certificazione di componenti software o hardware dove un bug ha conseguenze gravi (vedi il collegamento concettuale con l'evaluation di sistemi agentici in ambienti ad alto rischio, `./evaluation-benchmark.md`). E' anche uno strumento utile come "second check" indipendente su dimostrazioni gia' pubblicate ma mai formalizzate, per scovare eventuali lacune sfuggite alla revisione umana tradizionale.

Non ha senso per la stragrande maggioranza del lavoro matematico quotidiano: la formalizzazione completa di un risultato richiede un investimento di calcolo e di tempo ordini di grandezza superiore alla dimostrazione informale equivalente (11 giorni e miliardi di token per un teorema gia' noto da 30 anni), e resta impraticabile per la matematica esplorativa dove l'enunciato stesso e' ancora in evoluzione. E' anche inadatta come sostituto della revisione tra pari per risultati nuovi il cui enunciato potrebbe essere sbagliato o mal posto: il kernel verifica che la dimostrazione sia logicamente valida rispetto agli assiomi dati, non che l'enunciato formalizzato catturi correttamente l'intuizione matematica originale — un errore di traduzione tra linguaggio naturale e formalizzazione ("formalizzare la cosa sbagliata") non viene rilevato dal processo di verifica in se'.

## Esempi pratici

Esempio 1: la dimostrazione Fermat (Anthropic, 4 settembre 2026). Obiettivo: produrre una versione Lean, verificabile al kernel, della dimostrazione dell'Ultimo Teorema di Fermat (dimostrato informalmente da Wiles nel 1994). Approccio: decomposizione in circa 29.500 teoremi intermedi, dozzine di istanze Claude che lavorano in parallelo sui singoli lemmi usando lo strumento Prove2Me per l'orchestrazione e il tracciamento delle dipendenze, circa 6 miliardi di token generati in aggregato su 11 giorni, oltre 13 milioni di righe di codice Lean risultanti. Il criterio di successo e' binario e oggettivo: il kernel Lean accetta l'intera catena di dimostrazioni senza errori.

Esempio 2 (per contrasto metodologico, gia' coperto in `./evaluation-benchmark.md`): MaxProof applica generative verification e test-time scaling per portare MiniMax M3 da 27/42 a 35/42 su IMO 2025 e da 26/42 a 36/42 su USAMO 2026 — qui il target non e' una formalizzazione completa in un proof assistant ma una soluzione corretta a un problema di competizione, valutata da un verificatore, senza necessariamente produrre una prova Lean end-to-end. La distinzione illustra due obiettivi diversi sotto l'etichetta comune "AI e matematica formale": risolvere problemi (competition math) vs. formalizzare dimostrazioni (proof formalization).

Esempio 3: uso pratico per chi costruisce sistemi di verifica software. Un'organizzazione che deve certificare la correttezza di un algoritmo critico (es. un protocollo crittografico) puo' usare lo stesso schema ciclo-genera-verifica-correggi per produrre una specifica formale dell'algoritmo e una dimostrazione della sua correttezza rispetto alla specifica, riducendo — ma non eliminando, per il limite descritto sopra sulla traduzione enunciato-formalizzazione — il rischio di bug logici non rilevati dal testing tradizionale.

## Letture

- Anthropic, "Formalizing Fermat's Last Theorem", settembre 2026. https://www.anthropic.com/research/formalizing-fermats-last-theorem
- The Mathlib Community, "The Lean Mathematical Library", 2020. https://leanprover-community.github.io/
- Polu, Sutskever, "Generative Language Modeling for Automated Theorem Proving" (GPT-f), 2020. https://arxiv.org/abs/2009.03393
- MiniMax, "MaxProof: population-level test-time scaling per il ragionamento matematico", giugno 2026 — vedi `./evaluation-benchmark.md`, aggiornamento 2026-06-15.

## Aggiornamenti

### 2026-09-12

Prima voce di questa scheda, appena creata. Claude (Anthropic) completa la prima dimostrazione formale nota, verificata al computer in Lean, dell'Ultimo Teorema di Fermat: oltre 13 milioni di righe di codice e 29.500 teoremi intermedi verificati in 11 giorni, contro gli anni stimati per una formalizzazione umana equivalente, usando lo strumento open-source Prove2Me e dozzine di istanze Claude in parallelo per circa 6 miliardi di token complessivi. L'annuncio risale al 4 settembre 2026 mai coperto in un digest per assenza di run tra il 4 e l'11 settembre; recuperato come missed coverage nel digest del 12 settembre. [Digest 2026-09-12](../../digest/2026/09/12.md)
