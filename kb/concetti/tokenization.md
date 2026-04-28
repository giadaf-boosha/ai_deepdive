---
name: Tokenization
aliases: [tokenization, tokenizzazione, BPE, subword, byte-pair encoding]
categoria: tecnica
created: 2026-04-28
last_updated: 2026-04-28
mentions_count: 0
---

# Tokenization

## Cos'e

La tokenization e' il processo che converte una stringa di testo in una sequenza di simboli atomici (token) appartenenti a un vocabolario fisso, usabili come input numerico per un [LLM](./llm.md). E' lo strato piu' basso, spesso invisibile ma decisivo, dell'intera pipeline. La scelta del tokenizer determina cosa il modello "vede": una parola? Un sotto-pezzo di parola? Un byte? E quindi influenza efficienza, capacita' multilingue, robustezza a typo, lunghezza effettiva del [context window](./context-window.md).

L'evoluzione storica e' chiara. Tokenizer word-level (un token per parola) erano comuni negli anni 2000 ma esplodevano in vocabolario per lingue morfologicamente ricche e fallivano su parole rare/nuove. I tokenizer character-level avevano vocabolari minuscoli ma sequenze enormi, rendendo il training inefficiente. Il compromesso vincente e' subword: pezzi di parola di lunghezza variabile, che bilanciano vocabolario e lunghezza sequenza. Le tre famiglie subword dominanti sono BPE (Byte-Pair Encoding, Sennrich et al. 2015 per traduzione neurale), WordPiece (BERT, Schuster e Nakajima 2012), Unigram LM (Kudo 2018, base di SentencePiece).

L'importanza pratica della tokenization e' spesso sottovalutata. Costo per chiamata, performance multilingue, qualita' su input strutturato (codice, JSON, numeri), capacita' di seguire instruction precise (es. contare parole o caratteri) sono tutte funzione del tokenizer.

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

Effetti misurabili. Lo stesso testo italiano in tokenizer GPT-2 vecchio richiede ~1.7x token rispetto allo stesso in inglese; con cl100k_base scende a ~1.3x; con Llama 3 a ~1.15x. Per testi cinesi/giapponesi/arabi, tokenizer poveri possono richiedere 3-4x token rispetto a inglese, con costi e context window peggiori. La scelta del modello con tokenizer adatto alla lingua dell'utente e' una leva di costo significativa.

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
| Tokenizer-free (ByT5) | No vocab, no OOV | Sequenze 4-5x lunghe, costoso |
| Vision tokenizer (patch + VQ) | Multimodalita' | Lossy |
| Audio tokenizer (Whisper, EnCodec) | Audio in LLM | Bitrate vs qualita' |

Una direzione di ricerca: tokenizer adattivi. T-FREE (2024), Megabyte (2023), BLT (2024) propongono modelli che operano su byte ma con grouping dinamico, riducendo il problema della lunghezza sequenza. Non ancora mainstream nei frontier model.

## Quando usarlo / quando no

Tutti gli LLM hanno un tokenizer; non si sceglie "se usarlo" ma "quale modello scegliere in base al tokenizer". La scelta esplicita rilevante e':

Per applicazioni multilingue: modelli con tokenizer ricco di token per le lingue target. Llama 3, Gemini, Qwen 2, Mistral hanno tokenizer migliori per non-inglese rispetto a modelli pre-2024.

Per applicazioni codice: modelli con tokenizer addestrato su codice. Gli ultimi GPT, Claude, Codex/Llama-Code hanno token efficienti per costrutti come `==`, `=>`, indentazione.

Per fine-tuning custom: serve attenzione. Aggiungere token speciali al tokenizer richiede embedding init e training; cambiare tokenizer di un modello pre-addestrato e' impraticabile.

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

Misurare il cost-per-language. Per applicazioni multilingue, il primo passo per il cost forecasting e' tokenizzare un campione rappresentativo nella propria lingua su tutti i modelli candidati. Stessi 1000 documenti tokenizzati in modelli A, B, C: il rapporto medio token/parola dice quanto pagheresti su quel modello. Spesso questa singola misura sposta del 30-60% la decisione finale di vendor.

Token speciali. I modelli chat hanno token speciali per delimitatori di ruolo (es. `<|user|>`, `<|assistant|>`, `<|system|>`, `<|tool_call|>`). Questi sono parte del template di chat e si interpongono tra i messaggi. Toccare manualmente o ri-iniettarli in stringhe utente puo' rompere il modello in modo silenzioso. Le librerie SDK ufficiali (Transformers, Anthropic, OpenAI) gestiscono il templating; usarle sempre invece che concatenare a mano.

Limiti su input strutturato. Il tokenizer puo' non comprimere bene formati JSON, XML, codice con molti delimitatori. Un JSON pretty-printed con indentazione spreca token in spazi e newline; un JSON minified ne usa meno. Per RAG con grandi quantita' di documenti, normalizzare formato (rimozione di whitespace ridondante, eliminazione di markup inutile) puo' ridurre il context del 10-20%.

## Aggiornamenti

Nessun aggiornamento dopo la creazione (2026-04-28).
