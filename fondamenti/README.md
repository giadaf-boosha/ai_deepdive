# Fondamenti di AI

> La teoria dell'intelligenza artificiale in italiano, capitolo per capitolo.
> Percorso in 7 parti e 28 capitoli basato su: Stuart J. Russell, Peter Norvig,
> *Intelligenza Artificiale: Un Approccio Moderno*, 4a edizione italiana,
> Pearson Italia (Volume 1, 2021, ISBN 9788891927484; Volume 2, 2022, ISBN 9788891927491).

Ogni capitolo e' una sintesi originale in italiano dei temi trattati nel capitolo
corrispondente dell'opera: prosa propria, nessuna riproduzione del testo Pearson,
riferimenti bibliografici (volume, capitolo, pagine) sempre citati in coda.

Esposto sul sito alla route `/fondamenti` (indice per parti) e `/fondamenti/<slug>`
(capitolo). Lo slug e' il nome file senza il prefisso numerico `NN-`.

## Struttura

| Parte | Titolo | Capitoli |
|---|---|---|
| 1 | Intelligenza artificiale | 1-2 |
| 2 | Risoluzione di problemi | 3-6 |
| 3 | Conoscenza, ragionamento e pianificazione | 7-11 |
| 4 | Conoscenza incerta e ragionamento in condizioni di incertezza | 12-18 |
| 5 | Apprendimento automatico | 19-22 |
| 6 | Comunicazione, percezione e azione | 23-26 |
| 7 | Conclusioni | 27-28 |

## Indice capitoli

Pagine stampate = numerazione del volume cartaceo (usata nelle citazioni).
Pagine PDF = posizione nel file PDF di lavoro (offset Vol. 1: +30, Vol. 2: +82).

| Cap | File | Volume | Pagine stampate | Pagine PDF |
|---|---|---|---|---|
| 1 | [01-introduzione.md](./01-introduzione.md) | 1 | 3-38 | 33-68 |
| 2 | [02-agenti-intelligenti.md](./02-agenti-intelligenti.md) | 1 | 39-64 | 69-94 |
| 3 | [03-risolvere-i-problemi-con-la-ricerca.md](./03-risolvere-i-problemi-con-la-ricerca.md) | 1 | 67-114 | 97-144 |
| 4 | [04-ricerca-in-ambienti-complessi.md](./04-ricerca-in-ambienti-complessi.md) | 1 | 115-150 | 145-180 |
| 5 | [05-ricerca-con-avversari-e-giochi.md](./05-ricerca-con-avversari-e-giochi.md) | 1 | 151-184 | 181-214 |
| 6 | [06-problemi-di-soddisfacimento-di-vincoli.md](./06-problemi-di-soddisfacimento-di-vincoli.md) | 1 | 185-212 | 215-242 |
| 7 | [07-agenti-logici.md](./07-agenti-logici.md) | 1 | 215-256 | 245-286 |
| 8 | [08-logica-del-primo-ordine.md](./08-logica-del-primo-ordine.md) | 1 | 257-286 | 287-316 |
| 9 | [09-inferenza-nella-logica-del-primo-ordine.md](./09-inferenza-nella-logica-del-primo-ordine.md) | 1 | 287-322 | 317-352 |
| 10 | [10-rappresentazione-della-conoscenza.md](./10-rappresentazione-della-conoscenza.md) | 1 | 323-352 | 353-382 |
| 11 | [11-pianificazione-automatica.md](./11-pianificazione-automatica.md) | 1 | 353-394 | 383-424 |
| 12 | [12-quantificare-l-incertezza.md](./12-quantificare-l-incertezza.md) | 1 | 397-422 | 427-452 |
| 13 | [13-ragionamento-probabilistico.md](./13-ragionamento-probabilistico.md) | 1 | 423-470 | 453-500 |
| 14 | [14-ragionamento-probabilistico-nel-tempo.md](./14-ragionamento-probabilistico-nel-tempo.md) | 1 | 471-510 | 501-540 |
| 15 | [15-programmazione-probabilistica.md](./15-programmazione-probabilistica.md) | 1 | 511-538 | 541-568 |
| 16 | [16-decisioni-semplici.md](./16-decisioni-semplici.md) | 1 | 539-572 | 569-602 |
| 17 | [17-decisioni-complesse.md](./17-decisioni-complesse.md) | 1 | 573-608 | 603-638 |
| 18 | [18-decisioni-multiagente.md](./18-decisioni-multiagente.md) | 1 | 609-658 | 639-688 |
| 19 | [19-apprendimento-da-esempi.md](./19-apprendimento-da-esempi.md) | 2 | 7-74 | 89-156 |
| 20 | [20-apprendimento-di-modelli-probabilistici.md](./20-apprendimento-di-modelli-probabilistici.md) | 2 | 75-102 | 157-184 |
| 21 | [21-deep-learning.md](./21-deep-learning.md) | 2 | 103-140 | 185-222 |
| 22 | [22-apprendimento-per-rinforzo.md](./22-apprendimento-per-rinforzo.md) | 2 | 141-176 | 223-258 |
| 23 | [23-elaborazione-del-linguaggio-naturale.md](./23-elaborazione-del-linguaggio-naturale.md) | 2 | 179-212 | 261-294 |
| 24 | [24-deep-learning-per-il-linguaggio-naturale.md](./24-deep-learning-per-il-linguaggio-naturale.md) | 2 | 213-238 | 295-320 |
| 25 | [25-visione-artificiale.md](./25-visione-artificiale.md) | 2 | 239-282 | 321-364 |
| 26 | [26-robotica.md](./26-robotica.md) | 2 | 283-338 | 365-420 |
| 27 | [27-filosofia-etica-e-sicurezza.md](./27-filosofia-etica-e-sicurezza.md) | 2 | 341-372 | 423-454 |
| 28 | [28-futuro-dell-ia.md](./28-futuro-dell-ia.md) | 2 | 373-384 | 455-466 |

Nota: i capitoli 1-2 compaiono in entrambi i volumi; qui si usa il Volume 1.
I capitoli 27-28 compaiono nel Volume 1 come "capitoli online" e nel Volume 2
a stampa; qui si usa il Volume 2.

## Format capitolo

```yaml
---
titolo: <Titolo capitolo>
capitolo: <N>
parte: <1-7>
volume: <1|2>
pagine: "<a-b>"        # pagine stampate del volume di riferimento
concetti: [<slug KB>]  # concetti correlati espliciti in kb/concetti/
created: YYYY-MM-DD
last_updated: YYYY-MM-DD
---
```

Corpo: inquadramento (2-3 paragrafi) -> 3-6 sezioni h2 tematiche -> `## Idee chiave`
(bullet) -> `## Perche conta oggi` (ponte alla pratica LLM/agenti, con link
`../kb/concetti/<slug>.md`) -> `## Riferimenti` (citazione completa).
Prosa originale, 1200-2500 parole, apostrofi ASCII, presente indicativo, no emoji.
