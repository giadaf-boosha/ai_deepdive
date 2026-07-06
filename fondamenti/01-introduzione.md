---
titolo: Introduzione
capitolo: 1
parte: 1
volume: 1
pagine: "3-38"
concetti: [agent, ai-governance, evaluation-benchmark]
created: 2026-07-06
last_updated: 2026-07-06
---

# Introduzione

Che cosa significa costruire una macchina intelligente? Il capitolo di apertura
di Russell e Norvig affronta la domanda da tre direzioni: una definizione
operativa di intelligenza artificiale, una ricostruzione delle discipline che le
hanno fornito idee e strumenti, e una storia del campo dalle origini al deep
learning. L'obiettivo dichiarato dell'AI non e' solo comprendere l'intelligenza,
ma costruire entita' capaci di agire in modo efficace e sicuro in situazioni
nuove.

Il punto di arrivo del capitolo e' una presa di posizione netta: tra i possibili
modi di definire l'AI, quello che ha vinto storicamente e' l'approccio degli
agenti razionali, cioe' sistemi che fanno "la cosa giusta" rispetto a un
obiettivo. Ma proprio questa definizione, avvertono gli autori, va corretta
quando le macchine diventano abbastanza potenti da operare nel mondo reale.

## Quattro modi di definire l'intelligenza artificiale

Le definizioni storiche di AI si dispongono lungo due assi: fedelta' al
comportamento umano contro razionalita' ideale, e processi di pensiero contro
comportamento osservabile. Ne escono quattro approcci.

Agire umanamente e' l'approccio del test di Turing: una macchina e'
intelligente se un esaminatore umano, dialogando per iscritto, non riesce a
distinguerla da una persona. Superare il test richiede interpretazione del
linguaggio naturale, rappresentazione della conoscenza, ragionamento automatico
e apprendimento automatico; la versione "totale" del test aggiunge visione
artificiale e robotica. E' notevole quanto questa lista del 1950 assomigli alle
capacita' dei sistemi AI di oggi. Gli autori pero' osservano che pochi
ricercatori hanno davvero inseguito il test: come l'aeronautica non cerca di
costruire macchine che volino "esattamente come piccioni", l'AI non ha bisogno
di imitare l'uomo per essere utile.

Pensare umanamente e' il territorio della modellazione cognitiva: costruire
programmi il cui ragionamento, passo per passo, ricalca quello osservato negli
esseri umani. E' il progetto delle scienze cognitive, nate dall'incontro tra AI
e psicologia sperimentale.

Pensare razionalmente e' la tradizione logicista, che discende dai sillogismi
di Aristotele: codificare le "leggi del pensiero" e derivare conclusioni
corrette da premesse certe. Il limite e' che la conoscenza del mondo reale e'
raramente certa; la teoria delle probabilita' colma la lacuna, ma un modello
del mondo, da solo, non genera comportamento.

Agire razionalmente e' l'approccio degli agenti razionali: un agente e'
qualcosa che agisce, e un agente razionale agisce per ottenere il miglior
risultato atteso rispetto a un obiettivo. Questo approccio e' piu' generale
(l'inferenza corretta e' solo uno dei meccanismi per la razionalita') e piu'
trattabile scientificamente (la razionalita' e' definita matematicamente, il
comportamento umano no). Russell e Norvig lo chiamano il modello standard
dell'AI, e notano che pervade anche teoria del controllo, ricerca operativa,
statistica ed economia. Un aggiustamento necessario: la razionalita' perfetta
e' impraticabile in ambienti complessi, e va sostituita dalla razionalita'
limitata — agire in modo appropriato quando non c'e' tempo per tutti i calcoli.

## Il problema dell'allineamento dei valori

Il modello standard presuppone che l'obiettivo fornito alla macchina sia
completo e corretto. Per gli scacchi funziona; per un'auto a guida autonoma no:
"arriva a destinazione in sicurezza" nasconde compromessi impossibili da
specificare a priori. Il divario tra le nostre reali preferenze e l'obiettivo
scritto nella macchina e' il problema di allineamento dei valori, e diventa
tanto piu' grave quanto piu' il sistema e' capace: una macchina che persegue un
obiettivo sbagliato con grande intelligenza produce conseguenze peggiori di una
maldestra.

La conclusione degli autori anticipa il resto dell'opera: non vogliamo macchine
che perseguono i loro obiettivi, ma i nostri — e se non sappiamo trasferirli in
modo perfetto, servono macchine che sanno di non conoscere l'obiettivo
completo, e per questo agiscono con cautela, chiedono il permesso, imparano le
preferenze osservando, accettano di essere spente. E' il programma delle
"macchine che portano benefici dimostrabili".

## Le discipline dietro l'AI

Il capitolo ricostruisce i contributi di otto discipline, ognuna guidata dalle
sue domande.

La filosofia ha fornito l'idea che la mente operi secondo regole: dai
sillogismi di Aristotele al dualismo di Cartesio, dall'empirismo di Bacon e
Locke al positivismo logico, fino al legame tra conoscenza e azione che rende
possibile giustificare razionalmente cio' che un agente fa. Anche l'etica
dell'AI ha radici qui: utilitarismo (giusto e' cio' che massimizza l'utilita'
attesa) contro deontologia (giusto e' cio' che rispetta regole universali).

La matematica ha reso formali logica e probabilita' e ha creato la teoria
della computazione: la logica booleana e del primo ordine, la regola di Bayes,
il teorema di incompletezza di Godel, la nozione di computabilita' di Turing e
la distinzione tra problemi trattabili e intrattabili (NP-completezza). Il
monito pratico: una crescita esponenziale dei tempi di calcolo non si batte con
hardware piu' veloce.

L'economia ha formalizzato la decisione razionale: utilita' (Bernoulli),
teoria delle decisioni, teoria dei giochi (von Neumann e Morgenstern), processi
decisionali di Markov (Bellman) e la soddisfazione di Herbert Simon — decisioni
"abbastanza buone" come descrizione realistica del comportamento umano.

Le neuroscienze hanno mostrato che un insieme di cellule semplici puo'
produrre pensiero: il neurone come unita', le tecniche di imaging, il confronto
quantitativo tra cervello e computer. La lezione degli autori e' prudente:
senza la teoria giusta, macchine piu' veloci forniscono solo risposte sbagliate
piu' rapidamente.

La psicologia ha dato il modello dell'agente basato sulla conoscenza: stimolo
tradotto in rappresentazione interna, rappresentazioni manipolate da processi
cognitivi, e da queste le azioni (Craik). Dalla psicologia cognitiva discende
la scienza cognitiva, e dall'interazione uomo-computer l'idea di intelligenza
aumentata: computer che amplificano le capacita' umane invece di sostituirle.

L'ingegneria informatica ha fornito la macchina: dai primi computer di guerra
alla legge di Moore, fino all'hardware specializzato per l'AI (GPU, TPU) e
all'aumento vertiginoso della potenza di calcolo dedicata all'addestramento
dopo il 2012.

La teoria del controllo e la cibernetica hanno studiato artefatti che si
autoregolano tramite retroazione, minimizzando l'errore rispetto a uno stato
desiderato (Wiener). L'AI nasce in parte per superare i limiti della matematica
del controllo: logica e computazione simbolica permettono di trattare
linguaggio, visione e pianificazione.

La linguistica, con la critica di Chomsky al behaviorismo, ha mostrato che il
linguaggio e' creativo e non riducibile ad associazioni stimolo-risposta; da
qui la linguistica computazionale e l'elaborazione del linguaggio naturale.

## Settant'anni di storia in otto fasi

La storia del campo alterna entusiasmi e cadute. La gestazione (1943-1956) va
dal primo modello di neuroni artificiali di McCulloch e Pitts, all'apprendimento
hebbiano, fino al workshop di Dartmouth del 1956, dove McCarthy conia il
termine "intelligenza artificiale". Nei primi anni di grandi aspettative
(1952-1969) arrivano Logic Theorist e General Problem Solver di Newell e Simon,
l'ipotesi del sistema fisico di simboli, il Lisp e l'Advice Taker di McCarthy,
i micromondi come il mondo dei blocchi, il percettrone di Rosenblatt.

La dose di realta' (1966-1973) smonta l'ottimismo: i sistemi funzionano su
esempi giocattolo ma non scalano, per due ragioni di fondo — l'introspezione
informata non sostituisce l'analisi del problema, e l'esplosione combinatoria
rende inutile la potenza bruta. Il libro Perceptrons di Minsky e Papert
congela i fondi alle reti neurali. Seguono i sistemi esperti (1969-1986):
conoscenza di dominio potente e specifica al posto dei "metodi deboli"
generali, da DENDRAL a MYCIN a R1, fino al boom industriale e al successivo
"inverno dell'AI", quando le promesse stravaganti non vengono mantenute.

Il ritorno delle reti neurali (dal 1986) riparte dalla retropropagazione e dai
modelli connessionisti, piu' adatti alla confusione del mondo reale dei
concetti definiti assiomaticamente. Con il ragionamento probabilistico e
l'apprendimento automatico (dal 1987) l'AI diventa scienza matura: reti
bayesiane di Pearl, modelli nascosti di Markov, benchmark condivisi,
riunificazione con statistica e controllo. I big data (dal 2001) mostrano che,
oltre una certa scala, piu' dati battono algoritmi migliori. Infine il deep
learning (dal 2011): la vittoria su ImageNet nel 2012 innesca la rinascita che
porta ad AlphaGo e ai sistemi attuali, al prezzo di enormi risorse di calcolo e
di dati.

## Stato dell'arte, rischi e opportunita'

Il capitolo fotografa (al 2019-2020) un campo in accelerazione: pubblicazioni,
studenti e investimenti in crescita di un ordine di grandezza; sistemi pari o
superiori all'uomo in giochi, riconoscimento di oggetti e ambiti diagnostici
ristretti; applicazioni mature in guida autonoma, traduzione, riconoscimento
vocale, raccomandazioni. Sul futuro dell'AI a livello umano gli esperti si
dividono tra pochi decenni e "mai" — e gli autori ricordano, con Tetlock, che
nel prevedere gli esperti non battono i dilettanti.

I rischi elencati sono concreti e attuali: armi autonome letali, sorveglianza e
persuasione su scala industriale, decisioni distorte da bias nei dati, impatto
sull'occupazione, sistemi critici per la sicurezza, cybersicurezza. Da qui
l'importanza di governance e regolamentazione. Sul lungo periodo il tema e' il
controllo di sistemi superintelligenti: il "problema del gorilla" (creare
qualcosa di piu' intelligente di noi e perdere il controllo del nostro futuro)
e il "problema di Re Mida" (ottenere esattamente cio' che si e' chiesto, non
cio' che si voleva). La risposta proposta non e' fermare l'AI ma riprogettarla:
agenti incerti sull'obiettivo umano, che apprendono le preferenze
dall'osservazione.

## Idee chiave

- L'AI si definisce lungo due assi (umano/razionale, pensiero/comportamento);
  l'approccio vincente e' quello degli agenti razionali che "fanno la cosa
  giusta" — il modello standard.
- La razionalita' perfetta e' computazionalmente impraticabile: serve
  razionalita' limitata.
- Il modello standard presuppone obiettivi completi e corretti; nel mondo reale
  questo genera il problema di allineamento dei valori.
- Otto discipline hanno costruito le fondamenta: filosofia, matematica,
  economia, neuroscienze, psicologia, ingegneria informatica, teoria del
  controllo, linguistica.
- La storia dell'AI e' ciclica: entusiasmo, promesse eccessive, inverno,
  rinascita su basi piu' solide — dai sistemi esperti al deep learning.
- Piu' dati e piu' calcolo hanno spostato il campo dalla conoscenza artigianale
  all'apprendimento dai dati; senza la teoria giusta, pero', macchine piu'
  veloci danno solo risposte sbagliate piu' in fretta.
- I rischi dell'AI (bias, sorveglianza, armi autonome, sicurezza) sono gia'
  attuali e richiedono governance; il controllo di sistemi superintelligenti
  richiede di ripensare il modello standard.

## Perche conta oggi

Il vocabolario di questo capitolo e' il vocabolario del dibattito corrente. I
sistemi basati su [LLM](../kb/concetti/llm.md) vengono valutati con benchmark
condivisi — la pratica nata negli anni '90 raccontata qui, oggi al centro di
[evaluation e benchmark](../kb/concetti/evaluation-benchmark.md). L'approccio
dell'agente razionale e' il fondamento teorico degli
[AI agent](../kb/concetti/agent.md) moderni, e la razionalita' limitata descrive
bene i compromessi di latenza e costo con cui gli agenti reali operano. Il
problema di allineamento dei valori e' diventato disciplina ingegneristica con
[RLHF](../kb/concetti/rlhf.md) e con il filone safety; le questioni di rischio e
regolamentazione trattate in chiusura sono oggi materia di
[AI governance](../kb/concetti/ai-governance.md). Rileggere la storia dei cicli
di hype e inverno aiuta a calibrare le aspettative anche sull'ondata attuale.

## Riferimenti

- Stuart J. Russell, Peter Norvig — *Intelligenza Artificiale: Un Approccio
  Moderno*, 4a edizione italiana, Pearson Italia, Vol. 1 (2021), Capitolo 1,
  pp. 3-38.
