---
name: Embedding
aliases: [embedding, vector embedding, dense representation, rappresentazione densa]
categoria: tecnica
created: 2026-04-28
last_updated: 2026-04-28
mentions_count: 0
---

# Embedding

## Cos'e

Un embedding e' un vettore di numeri reali a dimensione fissa che rappresenta un oggetto (parola, frase, documento, immagine, audio, codice) in uno spazio metrico. La proprieta' chiave e' che oggetti semanticamente simili hanno embedding vicini, secondo una metrica come distanza coseno o euclidea. Un embedding tipico ha tra 256 e 4096 dimensioni; valori comuni nei modelli di produzione del 2025-2026 sono 1024, 1536, 3072.

L'idea ha radici negli anni '80 (rappresentazioni distribuite di Hinton), si concretizza con word2vec di Mikolov et al. (2013) per le parole, GloVe (Pennington et al., 2014) e fastText (Bojanowski et al., 2016). La svolta verso embedding contestuali avviene con ELMo (2018), ULMFiT, e soprattutto BERT (Devlin et al., 2018), che produce vettori dipendenti dal contesto della frase. Da quel momento gli embedding sono il connettore tra spazi simbolici e algoritmi numerici: ogni sistema di [RAG](./rag.md), [vector database](./vector-database.md), classificazione, clustering moderno passa per embedding.

L'importanza pratica e' enorme. Un embedding trasforma un problema di linguaggio in un problema geometrico: la similarita' diventa un prodotto scalare, la classificazione diventa un nearest neighbor, il clustering un k-means. Le applicazioni includono ricerca semantica, deduplicazione, raccomandazione, anomaly detection, evaluation di output LLM (judging tramite similarita' semantica), routing in sistemi multi-modello.

## Come funziona

Un modello di embedding produce per ogni input un vettore `v` in R^d. Per testi, l'architettura tipica e' un transformer encoder (BERT-like) o un decoder pooled. Il flusso:

Input testo. Tokenizzazione tramite [tokenization](./tokenization.md) BPE/WordPiece. Embedding di token e posizione, come in un [LLM](./llm.md).

Forward pass nell'encoder. Lo stack transformer produce una matrice di rappresentazioni token, dimensione `seq_len x d`.

Pooling. Riduce la matrice a un singolo vettore. Strategie: CLS pooling (si prende il vettore del token speciale `[CLS]`, tipico di BERT); mean pooling (media dei vettori token, mascherando padding); attention pooling (somma pesata con pesi appresi); last token pooling (negli encoder decoder-based).

Normalizzazione. Tipicamente si normalizza L2: `v / ||v||`. Cosi' la similarita' coseno coincide con il prodotto scalare, semplificando i calcoli a valle.

Training. La maggior parte dei modelli moderni di embedding e' addestrata con contrastive learning. Si costruiscono triplette (anchor, positive, negative) e si ottimizza una loss tipo InfoNCE: `L = -log(exp(sim(a,p)/tau) / sum_n exp(sim(a,n)/tau))`. La temperatura `tau` controlla la nettezza della distribuzione. I positive vengono da query-document veri (clickthrough, paraphrase, NLI entailment); i negative sono in-batch (gli altri esempi del batch) o "hard negatives" minati attivamente.

Le tecniche moderne includono Matryoshka Representation Learning (Kusupati et al., 2022), che addestra embedding in modo che i primi k componenti siano informativi anche da soli: si puo' troncare un vettore 1536-d a 256-d con perdita minore. text-embedding-3 di OpenAI e Voyage 3 implementano Matryoshka, permettendo trade-off costo/qualita' a runtime.

Geometria emergente. Negli embedding ben addestrati emergono direzioni semantiche: la celebre regolarita' word2vec `king - man + woman ~ queen` indica che certe relazioni sono lineari. Negli embedding di frase, cluster semantici corrispondono a topic, intent, lingua. Anisotropy (concentrazione dei vettori in un cono ristretto) e' un problema noto: tecniche come whitening o normalization migliorano la separazione.

Esempio numerico. Un modello a 1024 dim con 4 byte per dimensione (float32) produce vettori da 4 KB. Un milione di documenti = 4 GB. Con float16: 2 GB. Con quantizzazione int8: 1 GB. Con binary embedding (1 bit per dim): 128 MB. Le scelte di precisione impattano costo storage e velocita' di ricerca, con perdita di qualita' tipicamente 1-5% NDCG.

## Varianti / approcci

| Famiglia | Esempi | Caratteristica |
|---|---|---|
| Static word embedding | word2vec, GloVe, fastText | Un vettore per parola, no contesto |
| Encoder-based contextual | BERT, RoBERTa, MiniLM, MPNet | Vettori dipendono dal contesto |
| Sentence-tuned | Sentence-BERT, MPNet sentence | Contrastive su coppie di frasi |
| Multilingue | LaBSE, multilingual-e5, BGE-M3 | Allineamento cross-lingual |
| Long-context | jina-embeddings-v3, voyage-3 | Supporto fino a 32k+ token |
| Matryoshka | text-embedding-3, voyage-3, NV-Embed | Troncabili a piu' dimensioni |
| Multimodali | CLIP, SigLIP, ImageBind | Allineano modalita' diverse |
| Code | OpenAI text-embedding-3 con dataset code, Voyage code-2 | Tuned per codice |
| Bi-encoder vs cross-encoder | BGE bi-encoder, BGE reranker | Bi: fast retrieval; cross: precise reranking |

I bi-encoder calcolano un embedding per query e uno per documento separatamente; il match e' il prodotto scalare. Sono veloci ma meno precisi. I cross-encoder ricevono `[query, document]` insieme e producono uno score; piu' precisi ma O(n) per ranking. Pipeline tipica: bi-encoder per retrieval di k=100, cross-encoder per reranking del top-k.

I modelli leader nei benchmark MTEB nel 2025-2026: famiglia Voyage, Cohere embed v4, OpenAI text-embedding-3-large, BGE-M3, NV-Embed-v2, jina-embeddings-v3, gte-Qwen2.

## Quando usarlo / quando no

Gli embedding sono la scelta giusta per ricerca semantica, [RAG](./rag.md), clustering, deduplicazione fuzzy, classificazione k-NN, similarity-based recommendation, drift detection, valutazione automatica di output testuali, grouping di feedback utente, semantic cache di chiamate LLM.

Sono la scelta sbagliata per match esatto su stringhe (un indice invertito BM25 o un B-tree e' piu' veloce e accurato), per query con identifier strutturati (codici prodotto, sigle), per task che richiedono ragionamento composizionale (gli embedding catturano similarita' semantica ma non logica), per dati con cardinalita' bassa (un semplice one-hot funziona).

Anti-pattern. Usare un modello generico su dominio specialistico: un text-embedding-3-small su sentenze giuridiche italiane perde rispetto a un modello multilingual fine-tunato su dominio. Mescolare embedding di modelli diversi nello stesso indice: gli spazi non sono allineati. Usare embedding senza normalizzazione e poi confrontare con coseno: errore frequente. Calcolare embedding solo a query time (no caching): costo esplode.

## Esempi pratici

Esempio 1: similarita' tra due frasi.

```python
from openai import OpenAI
import numpy as np

client = OpenAI()
def embed(text: str) -> np.ndarray:
    r = client.embeddings.create(model="text-embedding-3-small", input=text)
    return np.array(r.data[0].embedding)

a = embed("Il gatto dorme sul divano.")
b = embed("Un felino riposa sul sofa'.")
cos = float(a @ b)  # gia' normalizzati
print(cos)  # tipicamente > 0.85
```

Esempio 2: deduplicazione di feedback. 50.000 commenti utente vengono embeddati. Si calcola la matrice di similarita' approssimata (HNSW + soglia 0.92). Cluster di duplicati semantici emergono automaticamente. Riduzione tipica: 40% dei commenti aggregabili, accelera l'analisi qualitativa.

Esempio 3: semantic cache. Prima di chiamare un LLM costoso per una domanda, si embedda la query e si cerca in cache. Se trovi un hit > 0.97 con stessa categoria utente, restituisci la risposta cached. Risparmi anche 30-60% di chiamate su workload con domande ricorrenti.

## Letture

- Mikolov et al., "Efficient Estimation of Word Representations in Vector Space" (word2vec), 2013. https://arxiv.org/abs/1301.3781
- Reimers e Gurevych, "Sentence-BERT", EMNLP 2019. https://arxiv.org/abs/1908.10084
- Karpukhin et al., "Dense Passage Retrieval for Open-Domain Question Answering", 2020. https://arxiv.org/abs/2004.04906
- Kusupati et al., "Matryoshka Representation Learning", NeurIPS 2022. https://arxiv.org/abs/2205.13147
- Wang et al., "Text Embeddings by Weakly-Supervised Contrastive Pre-training" (E5), 2022. https://arxiv.org/abs/2212.03533
- Chen et al., "BGE M3-Embedding", 2024. https://arxiv.org/abs/2402.03216
- Hugging Face MTEB leaderboard. https://huggingface.co/spaces/mteb/leaderboard
- OpenAI, "New embedding models and API updates", 2024. https://openai.com/index/new-embedding-models-and-api-updates/

## Note operative

Scelta di un modello di embedding nel 2025-2026. Per inglese e ricerca semantica generica, text-embedding-3-large di OpenAI o voyage-3 sono solidi out-of-the-box. Per multilingue forte (italiano incluso), bge-m3 e multilingual-e5 large hanno qualita' competitiva con costo zero (open weights). Per code, voyage-code-2 e jina-embeddings-v2-code battono i generici. Per dominio fortemente specializzato (legale, medico, finanziario), il fine-tuning di un encoder come gte-large su poche migliaia di triplette interne porta a guadagni 5-15 punti NDCG a costi modesti.

Privacy degli embedding. Gli embedding non sono "anonimi": ricerche recenti mostrano che da un embedding di frase si puo' ricostruire una parafrasi del testo originale con accuracy elevata (vector inversion attack, Morris et al. 2023). Trattarli come dati sensibili significa applicare gli stessi controlli di accesso del testo sorgente, evitare di inviare embedding di dato regolato a servizi esterni non conformi, e considerare encryption-at-rest per indici contenenti PII.

Manutenzione di un indice di embedding. Il modello evolve: ogni 6-18 mesi conviene valutare l'upgrade. Rebuilding dell'indice e' un'operazione lenta e da pianificare con dual-write durante la migrazione (l'indice vecchio resta servito mentre il nuovo si popola). Il versioning del modello di embedding deve essere persistito nei metadata, altrimenti negli anni nessuno sa piu' chi ha prodotto cosa. Le valutazioni offline (NDCG@10, MRR) su un set di Q/A ground-truth devono essere automatizzate in CI per detectare regressioni.

Embedding multimodali. Modelli come CLIP (Radford et al., OpenAI 2021) e successori (SigLIP, ImageBind, Voyage multimodal-3) producono embedding allineati tra modalita' (testo, immagini, audio). Una stessa query testuale puo' recuperare immagini semanticamente correlate. Use case: ricerca prodotti su catalogo e-commerce, content moderation, organizzazione di librerie media. La sfida e' che gli spazi multimodali sono piu' rumorosi di quelli text-only, e la qualita' del retrieval cross-modal richiede modelli di riferimento aggiornati ed eval set dedicato.

## Aggiornamenti

Nessun aggiornamento dopo la creazione (2026-04-28).
