---
name: Tokenization
aliases: [tokenization, tokenizzazione, BPE, subword, byte-pair encoding]
categoria: tecnica
created: 2026-04-28
last_updated: 2026-06-01
---

# Tokenization

## Cos'e

La tokenization e' il processo che converte una stringa di testo in una sequenza di simboli atomici (token) appartenenti a un vocabolario fisso, usabili come input numerico per un [LLM](./llm.md). E' lo strato piu' basso, spesso invisibile ma decisivo, dell'intera pipeline. La scelta del tokenizer determina cosa il modello "vede": una parola? Un sotto-pezzo di parola? Un byte? E quindi influenza efficienza, capacita' multilingue, robustezza a typo, lunghezza effettiva del [context window](./context-window.md).

L'evoluzione storica e' chiara. Tokenizer word-level (un token per parola) erano comuni negli anni 2000 ma esplodevano in vocabolario per lingue morfologicamente ricche e fallivano su parole rare/nuove. I tokenizer character-level avevano vocabolari minuscoli ma sequenze enormi, rendendo il training inefficiente. Il compromesso vincente e' subword: pezzi di parola di lunghezza variabile, che bilanciano vocabolario e lunghezza sequenza. Le tre famiglie subword dominanti sono BPE (Byte-Pair Encoding, Sennrich et al. 2015 per traduzione neurale), WordPiece (BERT, Schuster e Nakajima 2012), Unigram LM (Kudo 2018, base di SentencePiece).

L'importanza pratica della tokenization e' spesso sottovalutata. Costo per chiamata, performance multilingue, qualita' su input strutturato (codice, JSON, numeri), capacita' di seguire instruction precise (es. contare parole o caratteri) sono tutte funzione del tokenizer. Un concetto chiave per ragionare quantitativamente sulla bonta' di un tokenizer e' la fertility: il numero medio di token prodotti per parola (o per byte) su un corpus dato. Fertility bassa significa sequenze piu' corte a parita' di testo, quindi meno costo, piu' margine nel context window e spesso latenza inferiore. La fertility di uno stesso tokenizer cambia drasticamente da lingua a lingua, ed e' la metrica che misura concretamente l'iniquita' multilingue (multilingual inequity) di cui si parla nella ricerca recente: lo stesso identico contenuto costa molto di piu' in alcune lingue solo per come e' segmentato.

## Come funziona

Byte-Pair Encoding (BPE) costruisce iterativamente il vocabolario. Si parte dai byte (256 simboli) o caratteri base. Si conta la frequenza di tutte le coppie adiacenti nel corpus, si fonde la coppia piu' frequente in un nuovo simbolo, si ripete. Si raggiunge un vocabolario target (es. 50.000 - 200.000 simboli). Le parole comuni diventano un singolo token; quelle rare si scompongono in sub-pezzi.

Esempio. Frasi: "tokenizer", "tokenizing", "token". Caratteri base. Coppie iniziali frequenti: "to" + "k", "ke" + "n". Dopo merge: "token" diventa un simbolo. "tokenizer" diventa "token" + "izer". "tokenizing" diventa "token" + "izing".

Byte-level BPE (GPT-2 in poi). Anziche' partire da caratteri, si parte dai byte. Cosi' qualunque stringa UTF-8 e' rappresentabile, anche caratteri non visti in training (emoji rari, alfabeti minoritari, byte invalidi). Il vocabolario base e' 256, le merge sono al livello byte. La maggior parte degli LLM moderni usa byte-level BPE.

WordPiece. Simile a BPE ma sceglie la merge che massimizza la probabilita' del corpus sotto un modello unigram, non solo la frequenza. Usato in BERT, ELECTRA. Token sub-word iniziano con `##` per indicare continuazione di parola.

Unigram LM (SentencePiece). Approccio probabilistico inverso. Si parte da un grande vocabolario candidato e si rimuovono iterativamente i token che riducono meno la log-likelihood del corpus. Ogni stringa ha multiple segmentazioni possibili; si sceglie quella di massima verosimiglianza con dynamic programming. Usato in T5, ALBERT, XLNet, molti modelli multilingual.

SentencePiece. Implementazione che tratta lo spazio come un carattere normale e non richiede pre-tokenization (split su spazi). Permette di addestrare tokenizer su lingue senza spazi (giapponese, cinese) in modo uniforme.

Differenze pratiche tra tokenizer.

| Tokenizer | Modello | Vocab size | Note |
|---|---|---|---|
| BPE byte-level | GPT-2, GPT-3 | 50.257 | Compatibile con tutto, ma poco efficiente su lingue non inglesi |
| tiktoken cl100k_base | GPT-3.5, GPT-4 | 100.256 | Aggiornato, migliori token su codice/multilingue |
| tiktoken o200k_base | GPT-4o, GPT-5 | ~200.000 | Ulteriore espansione, multilingual ricco |
| Llama 3 tokenizer | Llama 3 | 128.000 | Espanso rispetto a Llama 2 (32k), molto migliore su lingue diverse |
| SentencePiece (T5/Mistral) | Mistral, T5 | 32.000 - 128.000 | Unigram, robusto |
| Tekken | Mistral Large 2, Pixtral | ~131k | Tekkenized BPE, efficienza alta |

Effetti misurabili. Lo stesso testo italiano in tokenizer GPT-2 vecchio richiede ~1.7x token rispetto allo stesso in inglese; con cl100k_base scende a ~1.3x; con Llama 3 a ~1.15x. Per testi cinesi/giapponesi/arabi, tokenizer poveri possono richiedere 3-4x token rispetto a inglese, con costi e context window peggiori. La scelta del modello con tokenizer adatto alla lingua dell'utente e' una leva di costo significativa. La ricerca 2025-2026 sui tokenizer morphology-aware e multilingual va esattamente in questa direzione: ridurre il token-to-word ratio per le lingue penalizzate, con guadagni riportati intorno al 20% sui token consumati nei test sintetici e miglioramenti di throughput in inference quando la fertility scende.

Token su numeri e codice. I tokenizer trattano numeri come sequenze di digit token. Un numero come "12345" puo' essere "12" + "345" o "1" + "23" + "45" a seconda del tokenizer; questo influenza la performance aritmetica del modello, perche' la rappresentazione di "12345" cambia. Tokenizer recenti come o200k_base addestrano forzando ogni digit come token separato, migliorando il calcolo.

Effetti su instruction following. Chiedere "rispondi in esattamente 50 parole" sbaglia spesso: il modello non vede parole, vede token. Limiti in token sono piu' rispettabili. La famosa instruction "produci JSON valido" funziona meglio quando il tokenizer ha token speciali per `{`, `}`, `"`, riducendo gli stati ambigui.

## Varianti / approcci

| Approccio | Vantaggio | Svantaggio |
|---|---|---|
| Word-level | Intuitivo | Vocab esplosivo, OOV |
| Character-level | Vocab minimo | Sequenze lunghe |
| BPE byte-level | Robusto, universale | Bias verso inglese se training inglese-dominato |
| WordPiece | Prob-driven | Storicamente legato a BERT |
| SentencePiece Unigram | Multilingual | Implementation specifica |
| Byte-level con extra digit-split | Aritmetica migliore | Vocab leggermente piu' grande |
| Tokenizer-free (ByT5, BLT) | No vocab, no OOV | Sequenze 4-5x lunghe, costoso (mitigato da patching dinamico) |
| Vision tokenizer (patch + VQ) | Multimodalita' | Lossy |
| Audio tokenizer (Whisper, EnCodec) | Audio in LLM | Bitrate vs qualita' |
| Action tokenizer (robotica) | Azioni come token discreti per VLA | Mappatura azione-token lossy, dipendente dall'embodiment |

Una direzione di ricerca consolidata: tokenizer adattivi e architetture tokenizer-free. T-FREE (2024), Megabyte (2023) e in particolare BLT (Byte Latent Transformer, Pagnoni et al. 2024) propongono modelli che operano direttamente sui byte ma con grouping dinamico delle unita' di computazione. BLT in particolare non ha un vocabolario fisso: raggruppa i byte in "patch" di dimensione variabile, segmentate in base all'entropia del byte successivo, allocando piu' compute dove i dati sono piu' complessi. Questo attacca i difetti strutturali della tokenization classica: sensibilita' al rumore di input, mancanza di conoscenza ortografica (il modello non "vede" le lettere dentro un token), e l'iniquita' multilingue. Il limite storico di questi approcci era il costo: lavorare sui byte allunga le sequenze. Nel 2026 la ricerca si e' concentrata proprio su come rendere competitiva l'inference di queste architetture (vedi sezione Aggiornamenti). Restano comunque fuori dai frontier model in produzione, che continuano a usare BPE byte-level.

Sul fronte multimodale, la nozione di "tokenization" si e' estesa ben oltre il testo. I vision tokenizer trasformano immagini in patch quantizzate; gli audio tokenizer (EnCodec, codec neurali) discretizzano il segnale; e nella robotica i VLA (vision-language-action model) usano action tokenization per rappresentare comandi continui di attuatori come sequenze di token discreti, riusando la stessa macchineria autoregressiva degli LLM. La qualita' di questi tokenizer non-testuali e' una leva di performance esattamente come per il testo.

## Quando usarlo / quando no

Tutti gli LLM hanno un tokenizer; non si sceglie "se usarlo" ma "quale modello scegliere in base al tokenizer". La scelta esplicita rilevante e':

Per applicazioni multilingue: modelli con tokenizer ricco di token per le lingue target. Llama 3, Gemini, Qwen 2, Mistral hanno tokenizer migliori per non-inglese rispetto a modelli pre-2024. Quando il volume in una lingua penalizzata e' alto, conviene misurare la fertility effettiva (token/parola) per ciascun candidato, perche' e' li' che si concentra la differenza di costo.

Per applicazioni codice: modelli con tokenizer addestrato su codice. Gli ultimi GPT, Claude, Codex/Llama-Code hanno token efficienti per costrutti come `==`, `=>`, indentazione.

Per fine-tuning custom: serve attenzione. Aggiungere token speciali al tokenizer richiede embedding init e training; cambiare tokenizer di un modello pre-addestrato e' impraticabile. Esiste pero' una linea di ricerca su tokenizer "universali" e su tecniche di transfer cross-tokenizer (vedi Aggiornamenti) che mira ad attenuare proprio questo vincolo di rigidita'.

Anti-pattern. Stimare costo a "parole" senza convertire in token: sbagli del 30-200%. Comparare due modelli su lunghezza prompt senza tokenizer-specific count. Assumere che `len(text) / 4` sia il numero di token: e' una stima inglese-only, in italiano si sbaglia di 10-20%, in lingue CJK del 50-100%. Aggiungere padding manuale: i tokenizer moderni gestiscono padding e attention mask, non manipolare a mano.

## Esempi pratici

Esempio 1: contare token con tiktoken (OpenAI).

```python
import tiktoken
enc = tiktoken.encoding_for_model("gpt-4o")
testo = "Buongiorno, come posso aiutarti oggi?"
ids = enc.encode(testo)
print(len(ids), ids)
print([enc.decode([i]) for i in ids])
```

Output tipico: 9 token per la frase. La decode mostra come gli spazi siano associati al token successivo (`" come"` non `"come"`).

Esempio 2: stimare costo di una richiesta.

```python
prompt_tokens = enc.encode(prompt)
sys_tokens = enc.encode(system)
total_in = len(sys_tokens) + len(prompt_tokens)
expected_out = 800
cost_in = total_in / 1e6 * 5.0      # 5 USD/M input (esempio)
cost_out = expected_out / 1e6 * 15.0
print(f"Stimato: {cost_in + cost_out:.4f} USD")
```

Esempio 3: ottimizzazione per lingua. Un'app italiana misura: con GPT-3.5 vecchio cl100k il prompt italiano medio e' 1300 token; con Llama 3 70B (tokenizer 128k aggiornato) e' 1100 token; con un modello cinese con tokenizer non-italiano sale a 2500 token. Su volume mensile la scelta cambia il costo del 50-100%. Conviene benchmarkare la tokenizzazione, non solo la qualita'.

Esempio 4: misurare la fertility su un corpus reale. Per scegliere il vendor su base quantitativa, si tokenizza lo stesso campione con piu' encoder e si calcola token/parola.

```python
import tiktoken
corpus = open("campione_it.txt", encoding="utf-8").read()
parole = len(corpus.split())
for model in ["gpt-4o", "gpt-3.5-turbo"]:
    enc = tiktoken.encoding_for_model(model)
    n_tok = len(enc.encode(corpus))
    print(f"{model}: fertility = {n_tok / parole:.2f} token/parola")
```

Una fertility di 1.8 contro 1.3 significa, a parita' di tutto il resto, quasi il 40% di costo input in piu' su quel modello per quella lingua.

## Letture

- Sennrich et al., "Neural Machine Translation of Rare Words with Subword Units" (BPE), 2015. https://arxiv.org/abs/1508.07909
- Kudo, "Subword Regularization: Improving Neural Network Translation Models with Multiple Subword Candidates", 2018. https://arxiv.org/abs/1804.10959
- Kudo e Richardson, "SentencePiece: A simple and language independent subword tokenizer", 2018. https://arxiv.org/abs/1808.06226
- Radford et al., "Language Models are Unsupervised Multitask Learners" (GPT-2 byte-level BPE), 2019.
- Hugging Face Tokenizers documentation. https://huggingface.co/docs/tokenizers
- OpenAI tiktoken. https://github.com/openai/tiktoken
- "Tokenization: A Survey", Mielke et al. 2021. https://arxiv.org/abs/2112.10508
- "Byte Latent Transformer: Patches Scale Better Than Tokens", Pagnoni et al. 2024. https://arxiv.org/abs/2412.09871

## Note operative

Misurare il cost-per-language. Per applicazioni multilingue, il primo passo per il cost forecasting e' tokenizzare un campione rappresentativo nella propria lingua su tutti i modelli candidati. Stessi 1000 documenti tokenizzati in modelli A, B, C: il rapporto medio token/parola (la fertility) dice quanto pagheresti su quel modello. Spesso questa singola misura sposta del 30-60% la decisione finale di vendor.

Token speciali. I modelli chat hanno token speciali per delimitatori di ruolo (es. `<|user|>`, `<|assistant|>`, `<|system|>`, `<|tool_call|>`). Questi sono parte del template di chat e si interpongono tra i messaggi. Toccare manualmente o ri-iniettarli in stringhe utente puo' rompere il modello in modo silenzioso. Le librerie SDK ufficiali (Transformers, Anthropic, OpenAI) gestiscono il templating; usarle sempre invece che concatenare a mano.

Limiti su input strutturato. Il tokenizer puo' non comprimere bene formati JSON, XML, codice con molti delimitatori. Un JSON pretty-printed con indentazione spreca token in spazi e newline; un JSON minified ne usa meno. Per RAG con grandi quantita' di documenti, normalizzare formato (rimozione di whitespace ridondante, eliminazione di markup inutile) puo' ridurre il context del 10-20%.

## Aggiornamenti

Nessun aggiornamento dopo la creazione (2026-04-28).

### 2026-06-01

Mese senza svolte strutturali sulla tokenization testuale dei frontier model (BPE byte-level resta lo standard di produzione), ma due segnali confermano l'estensione del concetto oltre il testo e gli sforzi per superare la rigidita' del vocabolario fisso. In robotica, MolmoAct2 di Ai2 adotta un sistema di action tokenization aperto per i modelli VLA (vedi [../../digest/2026/05/06.md](../../digest/2026/05/06.md)); sul fronte training, il framework TIDE introduce un obiettivo cross-tokenizer per distillare modelli autoregressivi in diffusion LLM con vocabolari diversi (vedi [../../digest/2026/05/02.md](../../digest/2026/05/02.md)). In parallelo, fonte web verificabile: l'11 maggio 2026 ricercatori di Meta, Stanford e University of Washington presentano un "Fast Byte Latent Transformer" che riduce la memory bandwidth in inference di oltre il 50% senza tokenizer (MarkTechPost, https://www.marktechpost.com/2026/05/11/meta-and-stanford-researchers-propose-fast-byte-latent-transformer-that-reduces-inference-memory-bandwidth-by-over-50-without-tokenization/), affrontando il principale limite storico delle architetture tokenizer-free. Aggiornata la scheda con i concetti di fertility, multilingual inequity, action tokenizer e un esempio per misurare la fertility per lingua.
