# Fondamenti di AI

> La teoria dell'intelligenza artificiale in italiano, capitolo per capitolo.
> Percorso originale in 7 parti e 28 capitoli, dal test di Turing al futuro dell'AI.

Ogni capitolo e' una sintesi originale in italiano: prosa propria, taglio
divulgativo, ponte costante verso la pratica di LLM e agenti.

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

| Cap | File |
|---|---|
| 1 | [01-introduzione.md](./01-introduzione.md) |
| 2 | [02-agenti-intelligenti.md](./02-agenti-intelligenti.md) |
| 3 | [03-risolvere-i-problemi-con-la-ricerca.md](./03-risolvere-i-problemi-con-la-ricerca.md) |
| 4 | [04-ricerca-in-ambienti-complessi.md](./04-ricerca-in-ambienti-complessi.md) |
| 5 | [05-ricerca-con-avversari-e-giochi.md](./05-ricerca-con-avversari-e-giochi.md) |
| 6 | [06-problemi-di-soddisfacimento-di-vincoli.md](./06-problemi-di-soddisfacimento-di-vincoli.md) |
| 7 | [07-agenti-logici.md](./07-agenti-logici.md) |
| 8 | [08-logica-del-primo-ordine.md](./08-logica-del-primo-ordine.md) |
| 9 | [09-inferenza-nella-logica-del-primo-ordine.md](./09-inferenza-nella-logica-del-primo-ordine.md) |
| 10 | [10-rappresentazione-della-conoscenza.md](./10-rappresentazione-della-conoscenza.md) |
| 11 | [11-pianificazione-automatica.md](./11-pianificazione-automatica.md) |
| 12 | [12-quantificare-l-incertezza.md](./12-quantificare-l-incertezza.md) |
| 13 | [13-ragionamento-probabilistico.md](./13-ragionamento-probabilistico.md) |
| 14 | [14-ragionamento-probabilistico-nel-tempo.md](./14-ragionamento-probabilistico-nel-tempo.md) |
| 15 | [15-programmazione-probabilistica.md](./15-programmazione-probabilistica.md) |
| 16 | [16-decisioni-semplici.md](./16-decisioni-semplici.md) |
| 17 | [17-decisioni-complesse.md](./17-decisioni-complesse.md) |
| 18 | [18-decisioni-multiagente.md](./18-decisioni-multiagente.md) |
| 19 | [19-apprendimento-da-esempi.md](./19-apprendimento-da-esempi.md) |
| 20 | [20-apprendimento-di-modelli-probabilistici.md](./20-apprendimento-di-modelli-probabilistici.md) |
| 21 | [21-deep-learning.md](./21-deep-learning.md) |
| 22 | [22-apprendimento-per-rinforzo.md](./22-apprendimento-per-rinforzo.md) |
| 23 | [23-elaborazione-del-linguaggio-naturale.md](./23-elaborazione-del-linguaggio-naturale.md) |
| 24 | [24-deep-learning-per-il-linguaggio-naturale.md](./24-deep-learning-per-il-linguaggio-naturale.md) |
| 25 | [25-visione-artificiale.md](./25-visione-artificiale.md) |
| 26 | [26-robotica.md](./26-robotica.md) |
| 27 | [27-filosofia-etica-e-sicurezza.md](./27-filosofia-etica-e-sicurezza.md) |
| 28 | [28-futuro-dell-ia.md](./28-futuro-dell-ia.md) |

## Format capitolo

```yaml
---
titolo: <Titolo capitolo>
capitolo: <N>
parte: <1-7>
concetti: [<slug KB>]  # concetti correlati espliciti in kb/concetti/
created: YYYY-MM-DD
last_updated: YYYY-MM-DD
---
```

Corpo: inquadramento (2-3 paragrafi) -> 3-6 sezioni h2 tematiche -> `## Idee chiave`
(bullet) -> `## Perche conta oggi` (ponte alla pratica LLM/agenti, con link
`../kb/concetti/<slug>.md`). Prosa originale, 1200-2500 parole, apostrofi ASCII,
presente indicativo, no emoji.

## Attribuzione

I capitoli sono sintesi originali in italiano dei temi trattati nell'opera di
riferimento: Stuart J. Russell, Peter Norvig, *Intelligenza Artificiale: Un
Approccio Moderno*, 4a edizione, Pearson Italia (Vol. 1, 2021; Vol. 2, 2022).
