---
titolo: Logica del primo ordine
capitolo: 8
parte: 3
volume: 1
pagine: "257-286"
concetti: [agent, world-models, llm, chain-of-thought]
created: 2026-07-06
last_updated: 2026-07-06
---

# Logica del primo ordine

La logica proposizionale, vista nel capitolo precedente, dimostra che un agente puo' ragionare su un mondo a partire da fatti e regole. Ma paga un prezzo alto: ogni fatto e' un simbolo atomico e indivisibile, e per esprimere una regola generale come "le stanze adiacenti a un pozzo sono ventose" serve una formula separata per ogni stanza. Il capitolo 8 affronta esattamente questa domanda: come costruire un linguaggio di rappresentazione che parli di oggetti, delle loro proprieta' e delle relazioni tra loro, in modo conciso e con una semantica precisa.

La risposta e' la logica del primo ordine (FOL, first-order logic), il linguaggio formale piu' influente della storia dell'AI simbolica. La sua forza sta nel combinare il meglio di due mondi: dal linguaggio naturale prende l'idea che la realta' sia fatta di oggetti e relazioni, dalla logica proposizionale eredita una semantica dichiarativa, composizionale e non ambigua. Il risultato e' un linguaggio in cui una singola formula quantificata sostituisce intere famiglie di regole proposizionali.

Il capitolo non si limita alla teoria: mostra come usare la logica del primo ordine su domini concreti (parentela, numeri, insiemi, il mondo del wumpus) e chiude con una metodologia completa di ingegneria della conoscenza, applicata passo passo al dominio dei circuiti digitali. E' il ponte tra "avere un linguaggio logico" e "costruire una base di conoscenza che funziona davvero".

## Cosa manca ai linguaggi di programmazione (e al linguaggio naturale)

Il capitolo apre con un confronto illuminante. I linguaggi di programmazione come Python o Java sanno rappresentare fatti — una matrice puo' codificare la mappa del mondo del wumpus — ma non hanno un meccanismo generale per derivare fatti da altri fatti: ogni inferenza va programmata a mano, e la conoscenza del dominio resta intrecciata alla procedura che la usa. Inoltre non gestiscono bene l'informazione parziale: dire "c'e' un pozzo in [2,2] oppure in [3,1]" e' immediato in logica, macchinoso in un programma.

Il linguaggio naturale, all'estremo opposto, e' espressivo in modo straordinario, ma la visione moderna lo considera soprattutto un mezzo di comunicazione piu' che di rappresentazione: il significato di una frase dipende dal contesto in cui viene pronunciata, e l'ambiguita' e' ovunque. Il capitolo dedica spazio anche all'ipotesi di Sapir-Whorf — l'idea che la lingua parlata plasmi il pensiero — concludendo, dati sperimentali alla mano, che le persone ricordano il contenuto di cio' che leggono in forma non verbale, e che le differenze cognitive tra parlanti di lingue diverse esistono ma sono piccole.

La sintesi progettuale e' questa: prendere dalla logica proposizionale la semantica dichiarativa, composizionale e indipendente dal contesto, e dal linguaggio naturale gli elementi rappresentazionali di base — sostantivi per gli oggetti, verbi e aggettivi per le relazioni, e un caso speciale di relazione, le funzioni, che associano a ogni input esattamente un valore (come "padre di").

## Impegno ontologico: cosa esiste nel mondo secondo il linguaggio

La differenza profonda tra logiche non sta nella notazione ma nell'impegno ontologico: le ipotesi che ogni linguaggio fa sulla natura della realta'. La logica proposizionale assume che il mondo sia fatto di fatti, ciascuno vero o falso. La logica del primo ordine assume di piu': il mondo contiene oggetti e relazioni tra oggetti che possono valere o meno. Altre logiche spingono oltre: la logica temporale aggiunge i tempi, la logica fuzzy ammette gradi di verita' tra 0 e 1, le logiche di ordine superiore trattano le relazioni stesse come oggetti su cui quantificare.

Accanto all'impegno ontologico c'e' l'impegno epistemologico: quali stati di conoscenza un agente puo' avere rispetto a un fatto. In logica proposizionale e del primo ordine sono tre — vero, falso, sconosciuto — mentre la teoria della probabilita' permette qualunque grado di credenza tra 0 e 1. Il capitolo avverte di non confondere grado di credenza (incertezza dell'agente) e grado di verita' (vaghezza del fatto stesso): "Vienna e' una grande citta'" puo' essere vera al grado 0,8 in logica fuzzy, che e' cosa diversa dal credere con probabilita' 0,8 che il wumpus sia in una certa stanza.

## Modelli, termini e formule: la semantica in pratica

Un modello della logica del primo ordine e' un mondo possibile formalizzato: un dominio non vuoto di oggetti, relazioni come insiemi di tuple di oggetti, funzioni totali, e un'interpretazione che aggancia i simboli del linguaggio a questi elementi. L'esempio guida del libro usa cinque oggetti — Riccardo Cuor di Leone, Re Giovanni, le loro gambe sinistre e una corona — con relazioni come "fratello" (binaria) e "re" (unaria, una proprieta').

La sintassi si costruisce a strati. I termini denotano oggetti: simboli di costante come Giovanni, variabili, oppure termini complessi come GambaSinistra(Giovanni) — che non e' una chiamata di funzione che "calcola" qualcosa, ma semplicemente un nome per un oggetto di cui potremmo non conoscere altro. Le formule atomiche affermano fatti applicando un predicato a dei termini: Fratello(Riccardo, Giovanni). I connettivi logici della proposizionale compongono formule complesse. Il simbolo di uguaglianza permette di dire che due termini denotano lo stesso oggetto, o — negato — che ne denotano due distinti, cosa essenziale per contare: "Riccardo ha almeno due fratelli" richiede proprio un vincolo di disuguaglianza tra le variabili.

Un dettaglio importante: nulla obbliga che ogni oggetto abbia un nome, ne' che due nomi diversi indichino oggetti diversi. Per contesti in cui questa liberta' complica la vita — tipicamente i database — esiste una semantica alternativa, la semantica dei database, che adotta l'ipotesi dei nomi unici (ogni costante denota un oggetto distinto), l'ipotesi del mondo chiuso (cio' che non e' affermato e' falso) e la chiusura del dominio (esistono solo gli oggetti nominati). La lezione di fondo e' pragmatica: non esiste una semantica "giusta" in assoluto, esiste quella che rende naturali le cose che vogliamo dire.

## Quantificatori: il salto espressivo

I quantificatori sono cio' che rende la FOL davvero potente. Il quantificatore universale (per ogni x) permette leggi generali; quello esistenziale (esiste un x) permette asserzioni su oggetti anonimi. Il capitolo insiste su due errori classici, cosi' frequenti da meritare attenzione.

Primo: con il quantificatore universale il connettivo naturale e' l'implicazione, non la congiunzione. "Tutti i re sono persone" si scrive con "se x e' un re allora x e' una persona": l'implicazione e' vera anche per tutti gli oggetti che non sono re, che e' esattamente cio' che vogliamo. Usare la congiunzione affermerebbe invece che ogni oggetto del dominio e' un re ed e' una persona — corone e gambe incluse.

Secondo, speculare: con l'esistenziale il connettivo naturale e' la congiunzione. Un'implicazione quantificata esistenzialmente e' quasi sempre troppo debole, perche' basta un solo oggetto che non soddisfa la premessa a renderla vera per vacuita'.

Con quantificatori annidati l'ordine conta: "ognuno ama qualcuno" e "c'e' qualcuno amato da tutti" si distinguono solo per l'ordine dei quantificatori. Infine, universale ed esistenziale sono legati dalla negazione secondo le leggi di De Morgan: "a nessuno piacciono i broccoli" e "tutti non gradiscono i broccoli" sono la stessa formula, scritta in due modi. In linea di principio basterebbe un solo quantificatore; se ne usano due per leggibilita'.

## Tre domini alla prova: parentela, numeri, wumpus

La seconda meta' del capitolo mette il linguaggio al lavoro. L'interfaccia con la base di conoscenza resta TELL/ASK: si asseriscono formule e si pongono query, con la variante ASKVARS che restituisce le sostituzioni di variabili che rendono vera la query.

Il dominio della parentela mostra come si assiomatizza una rete di relazioni familiari: la madre come genitore femmina, il nonno come genitore di un genitore, la consanguineita' come condivisione di un genitore. Emerge la distinzione tra assiomi (informazione di base) e teoremi (formule derivabili dagli assiomi: logicamente ridondanti, ma preziose per abbattere il costo computazionale delle derivazioni). Non tutti gli assiomi sono definizioni complete: di un predicato come Persona possiamo dare solo specifiche parziali, e la FOL lo consente senza problemi.

Il dominio dei numeri naturali e' un esempio di economia estrema: con una costante (0), una funzione (successore), un predicato e quattro assiomi in stile Peano si definiscono i naturali e l'addizione, e da li' — per addizioni ripetute — moltiplicazione, potenze e tutta la teoria dei numeri. Il capitolo introduce qui lo zucchero sintattico: notazioni comode come la scrittura infissa m + 0, che non aggiungono nulla alla semantica. Seguono gli assiomi per insiemi e liste.

Il mondo del wumpus, infine, chiude il cerchio con il capitolo 7: dove la logica proposizionale richiedeva una regola per ogni stanza e una copia di ogni formula per ogni istante di tempo, la FOL cattura tutto con singoli assiomi quantificati su spazio e tempo — una regola sola dice che una stanza e' ventosa se e solo se una stanza adiacente contiene un pozzo, e un solo assioma di stato successore per predicato tiene traccia di cio' che cambia nel tempo.

## Ingegneria della conoscenza: dal dominio alla base di conoscenza

Costruire una base di conoscenza reale e' un processo di progettazione, non un atto di trascrizione. Il capitolo lo articola in sette passi: identificare le domande a cui la KB dovra' rispondere; raccogliere la conoscenza rilevante dagli esperti del dominio (acquisizione della conoscenza); definire un vocabolario di costanti, predicati e funzioni — e' l'ontologia del dominio, e le scelte di stile qui pesano quanto quelle di un'architettura software; codificare gli assiomi generali; codificare l'istanza specifica del problema; interrogare la KB tramite la procedura di inferenza; fare debugging e valutazione.

Il caso di studio e' un sommatore a un bit: porte logiche, morsetti, segnali e collegamenti diventano oggetti e relazioni, dodici assiomi generali descrivono il comportamento di AND, OR, XOR e NOT, e una manciata di formule atomiche codifica il circuito specifico. A quel punto la stessa procedura di inferenza risponde sia a query di verifica ("con quali input la somma vale 0 e il riporto 1?") sia a interrogazioni strutturali, senza scrivere alcun algoritmo dedicato. Il debugging e' istruttivo: un assioma sbagliato e' una formula falsa rispetto al mondo, riconoscibile in isolamento — al contrario di una riga di codice errata, che si giudica solo nel suo contesto. E il capitolo ammonisce: finito il debugging apparente, serve una valutazione misurata con query di prova, perche' e' troppo facile convincersi che il lavoro sia completo.

## Idee chiave

- Un buon linguaggio di rappresentazione e' dichiarativo, composizionale, espressivo, indipendente dal contesto e non ambiguo: i linguaggi di programmazione e il linguaggio naturale falliscono ciascuno su assi diversi.
- Le logiche si distinguono per impegno ontologico (cosa esiste nel mondo) ed epistemologico (quali stati di credenza sono ammessi): la FOL si impegna su fatti, oggetti e relazioni.
- Un modello FOL e' un dominio di oggetti piu' un'interpretazione che collega costanti a oggetti, predicati a relazioni e simboli di funzione a funzioni; verita' e conseguenza logica si definiscono su tutti i modelli possibili, che sono infiniti.
- Una formula atomica e' vera quando la relazione denotata dal predicato vale tra gli oggetti denotati dai termini; le interpretazioni estese danno significato alle variabili quantificate.
- La coppia di regole d'oro dei quantificatori: implicazione con il quantificatore universale, congiunzione con quello esistenziale; invertirle produce formule troppo forti o troppo deboli.
- L'uguaglianza permette di identificare e distinguere oggetti; la semantica dei database (nomi unici, mondo chiuso, dominio chiuso) e' un'alternativa comoda quando si conoscono tutti i fatti.
- Sia la logica proposizionale sia la FOL restano inadatte a proposizioni vaghe, il che ne limita l'uso in domini che richiedono giudizi sfumati.
- Sviluppare una base di conoscenza e' un processo iterativo in sette passi: analisi del dominio, scelta del vocabolario (ontologia), codifica di assiomi e istanze, interrogazione e debugging.

## Perche conta oggi

La logica del primo ordine non e' il motore degli attuali sistemi di AI generativa, ma le domande che pone sono tornate centrali. Ogni [LLM](../kb/concetti/llm.md) che ragiona su entita' e relazioni — chi possiede cosa, cosa e' collegato a cosa — sta affrontando in forma statistica lo stesso problema che la FOL risolve in forma simbolica; e quando un modello sbaglia una quantificazione ("tutti" contro "qualcuno") sta inciampando esattamente sulle distinzioni che questo capitolo formalizza. Le tecniche di [chain-of-thought](../kb/concetti/chain-of-thought.md) rendono espliciti passi di derivazione che una KB logica produrrebbe per inferenza, e la costruzione di [world models](../kb/concetti/world-models.md) ripropone la questione dell'impegno ontologico: quali oggetti e relazioni il sistema assume esistano nel mondo.

Il parallelo piu' diretto e' pero' con la pratica degli agenti. Il processo di ingegneria della conoscenza — identificare le domande, scegliere un vocabolario, codificare regole generali e istanze specifiche, interrogare, fare debugging — e' strutturalmente identico a come oggi si progetta un [agent](../kb/concetti/agent.md): definire gli strumenti e il loro schema e' scegliere un'ontologia, e il [tool use](../kb/concetti/tool-use.md) con schemi tipati eredita proprio la disciplina di predicati e funzioni con arita' fissata. Anche il [prompt engineering](../kb/concetti/prompt-engineering.md) di sistema, quando enumera regole e vincoli per il modello, e' una forma informale di codifica degli assiomi del dominio — con lo stesso rischio, ben noto agli ingegneri della conoscenza: assiomi mancanti o troppo deboli producono risposte sbagliate difficili da diagnosticare.

## Riferimenti

- Stuart J. Russell, Peter Norvig — *Intelligenza Artificiale: Un Approccio Moderno*, 4a edizione italiana, Pearson Italia, Vol. 1 (2021), Capitolo 8, pp. 257-286.
