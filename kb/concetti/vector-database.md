---
name: Vector database
aliases: [vector database, vector DB, vector store, database vettoriale, ANN index]
categoria: infrastruttura
created: 2026-04-28
last_updated: 2026-04-28
mentions_count: 0
---

# Vector database

## Cos'e

Un vector database e' un sistema di storage e ricerca specializzato per vettori densi ad alta dimensione (256-4096 dim tipicamente), che fornisce indicizzazione approssimata per nearest-neighbor search (ANN) su miliardi di vettori con latenza in millisecondi. La query restituisce i k vettori piu' simili a un vettore di interrogazione secondo una metrica di distanza (coseno, prodotto interno, euclidea L2). E' lo strato di persistenza che supporta gli [embedding](./embedding.md) nei sistemi di [RAG](./rag.md), recommendation, deduplicazione, anomaly detection.

L'idea di indicizzare vettori per ricerca approssimata e' antica: KD-tree (Bentley 1975), LSH (Indyk e Motwani 1998), product quantization (Jegou et al., 2010 con FAISS). La rilevanza esplode dopo il 2020 con la diffusione degli embedding e in modo massivo dal 2023 con il boom di RAG. Il mercato passa da una manciata di librerie (FAISS, Annoy, ScaNN) a un settore con decine di prodotti commerciali (Pinecone, Weaviate, Qdrant, Milvus, Vespa, Chroma, MongoDB Vector, Postgres pgvector, Elasticsearch dense_vector). Nel 2024-2026 la commoditizzazione spinge molti database tradizionali ad aggiungere supporto vettoriale (Postgres, MongoDB, Redis, Cassandra, DuckDB).

L'importanza pratica e' che senza vector database scalabili la ricerca semantica su corpora reali (milioni-miliardi di vettori) diventa impraticabile. Una scansione lineare per ogni query ha costo O(n*d), inaccettabile sopra qualche centinaia di migliaia di vettori. ANN index riducono il costo a O(log n) o O(sqrt(n)) accettando una piccola perdita di recall (qualita').

## Come funziona

Un vector DB ha tre livelli di responsabilita': storage (persistere vettori e metadati), index (struttura dati per ANN), query engine (esegue search filtrato).

Algoritmi di indice principali.

HNSW (Hierarchical Navigable Small World, Malkov e Yashunin 2016). E' lo standard de facto. Costruisce un grafo gerarchico multi-livello: il livello 0 contiene tutti i vertici, livelli superiori sono sottoinsiemi sempre piu' rarefatti. La search greedy parte dall'alto, scende, e converge sul vicino. Recall@10 > 95% con throughput migliaia di QPS per istanza, latency single-digit ms. Costo memoria: ~ 1.5x i vettori grezzi per i puntatori del grafo. Non e' compresso di default, ma combinazioni con quantization sono comuni.

IVF (Inverted File). Si fa k-means sul corpus, ottenendo c centroidi. Ogni vettore viene assegnato al centroide piu' vicino. La query confronta con i centroidi, sceglie i top-`nprobe`, scansiona linearmente i vettori in quei cluster. Trade-off: nprobe piccolo = veloce ma recall basso; nprobe grande = preciso ma lento.

Product Quantization (PQ). Comprime un vettore d-dim in una sequenza di m sub-codici, ognuno indice in un codebook k-means appreso su una sottosezione del vettore. Memoria scende drasticamente (es. 8 byte invece di 4096), con perdita 5-15% recall. PQ si combina con IVF (IVF-PQ) e HNSW (HNSW-PQ) per dataset enormi.

Scalar Quantization (SQ). Riduce ogni dimensione a int8 / int4 / binary, perdita di qualita' modesta. Sempre piu' usato (Pinecone, Qdrant, Vespa).

Filtered search. Le query reali non sono solo "k-NN", ma "k-NN dove `tenant_id = X` e `date > Y`". Implementazioni: pre-filter (filtra prima, poi ANN sul subset, perde efficienza HNSW), post-filter (ANN, poi filtra, rischia di non avere abbastanza risultati), hybrid (filtri integrati nell'index, vincolando l'esplorazione del grafo). I provider differiscono molto qui; i benchmark realistici devono includere filtered queries.

Hybrid retrieval. Combinazione di dense (ANN) + sparse (BM25). Reciprocal Rank Fusion combina rank list. Sistemi come Vespa, Weaviate, Elastic, Qdrant offrono hybrid built-in. Migliora il retrieval su query con identifier o terminologia tecnica.

Considerazioni quantitative. Un indice HNSW su 10 milioni di vettori a 1024 dim float32: ~60 GB. Con int8 quantization: ~15 GB. Con binary embedding (1 bit/dim): ~1.5 GB con perdita ~3-5%. Latenza P99 < 30 ms. Build time iniziale: minuti-ore. Update incrementale supportato, ma cancellazioni richiedono spesso compaction periodica.

Operazioni di scaling. Sharding orizzontale: il corpus viene partizionato; query fan-out a tutti gli shard, merge dei top-k. Replication: read replicas per QPS. Dimensioni reali in produzione: Pinecone serve indici da 100B+ vettori distribuiti; Vespa di Yahoo gestisce indici hybrid su petabyte.

## Varianti / approcci

| Categoria | Esempi | Quando |
|---|---|---|
| Pure vector SaaS | Pinecone, Weaviate Cloud, Qdrant Cloud | Workload focalizzato vector, gestione managed |
| Self-hostable open | Qdrant, Milvus, Weaviate, Chroma | Privacy, on-prem, costi controllati |
| Embedded / lightweight | Chroma, LanceDB, sqlite-vss, USearch, faiss | Prototipi, app desktop, in-process |
| Estensioni a DB tradizionali | pgvector (Postgres), Redis Vector, MongoDB Atlas, Elastic dense_vector | Stack esistente, no-new-store |
| Search engine + vector | Vespa, Elasticsearch, OpenSearch | Hybrid retrieval enterprise |
| Distributed analytical | Milvus, Vespa | Petascale corpora |

Per RAG di scala piccola-media (< 1M vettori) pgvector o Chroma sono spesso sufficienti. Per scale > 100M, soluzioni specializzate (Qdrant cluster, Vespa, Pinecone) danno vantaggi misurabili. Per ricerca enterprise complessa (multi-tenant, ACL fine-grained, hybrid, reranking), Vespa e Weaviate hanno feature ricche.

Asse di trade-off: recall vs latency vs costo. Tutti i sistemi scelgono un punto in questo triangolo. Benchmark indipendenti (ANN-Benchmarks, dbpedia, BEIR) misurano il fronte di Pareto.

## Quando usarlo / quando no

Un vector DB e' la scelta giusta quando il corpus supera ~100k vettori, quando si fanno query vector ad alta frequenza (chat, ricerca live), quando si serve multi-tenant con isolation, quando l'organizzazione ha gia' uno stack dati e vuole aggiungere capacita' vector. E' essenziale per [RAG](./rag.md) di produzione.

E' overkill quando: il corpus e' < 10k vettori (un array NumPy in memoria con cosine similarity batchata fa la stessa cosa); la latenza non conta (una scansione lineare e' piu' semplice); il dato non e' realmente vettoriale (per match esatto serve un B-tree, non ANN).

Anti-pattern. Sovra-indicizzare prima di benchmark: scegliere il DB con piu' feature senza misurare recall sul proprio dataset. Mescolare embedding di modelli diversi nello stesso indice (gli spazi non sono allineati). Ignorare la dimensione di metadati: alcuni provider fatturano sui metadata bytes. Non testare filtered queries: il calo di performance con filter e' provider-specifico e drammatico. Aggiornare l'embedding model senza re-indicizzare l'intero corpus: si distrugge consistenza.

Sicurezza. Vector embedding possono contenere informazioni invertibili (vector inversion attacks, Morris et al. 2023). Trattare embedding come dato sensibile, applicare access control per tenant, evitare di esporre indici pubblicamente.

## Esempi pratici

Esempio 1: setup Qdrant minimale.

```python
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct

client = QdrantClient(":memory:")
client.create_collection(
    collection_name="docs",
    vectors_config=VectorParams(size=1536, distance=Distance.COSINE),
)
client.upsert(
    collection_name="docs",
    points=[PointStruct(id=i, vector=emb, payload={"src": src})
            for i, (emb, src) in enumerate(zip(embeddings, sources))]
)
hits = client.search(collection_name="docs", query_vector=q_emb, limit=5)
```

Esempio 2: pgvector in Postgres.

```sql
CREATE EXTENSION IF NOT EXISTS vector;
CREATE TABLE docs (id bigserial primary key, content text, embedding vector(1024));
CREATE INDEX ON docs USING hnsw (embedding vector_cosine_ops) WITH (m = 16, ef_construction = 64);

-- query
SELECT id, content
FROM docs
WHERE tenant_id = $1
ORDER BY embedding <=> $2
LIMIT 10;
```

Per workload misti vector + relational, pgvector e' una scelta naturale. Performance HNSW su pgvector e' migliorata significativamente nel 2024-2025.

Esempio 3: scale-out con sharding. Un'azienda media servizio chat su 200M chunk di documenti. Setup: 4 nodi Qdrant in cluster, replication factor 2, sharding per tenant_id. Memoria totale: ~120 GB con int8 quantization. P95 latenza < 50 ms con filter su tenant. Costo infrastruttura: ~ 1500-3000 USD/mese su cloud comparabile.

## Letture

- Malkov e Yashunin, "Efficient and robust approximate nearest neighbor search using Hierarchical Navigable Small World graphs" (HNSW), 2016. https://arxiv.org/abs/1603.09320
- Jegou et al., "Product Quantization for Nearest Neighbor Search", IEEE TPAMI 2010.
- Johnson et al., "Billion-scale similarity search with GPUs" (FAISS), 2017. https://arxiv.org/abs/1702.08734
- Pan et al., "Vector Database Management Techniques and Systems", VLDB 2024. https://arxiv.org/abs/2310.14021
- Pinecone, "Learning Center" e blog tecnici. https://www.pinecone.io/learn
- Qdrant documentation. https://qdrant.tech/documentation/
- pgvector. https://github.com/pgvector/pgvector
- ANN-Benchmarks. https://ann-benchmarks.com/

## Note operative

Operazioni e backup. Un indice vector va trattato come un database: backup regolari, monitoring, alerting su latenza P99 e recall. La maggior parte dei sistemi moderni supporta snapshot e restore; Pinecone offre PITR su tier enterprise; pgvector eredita le procedure Postgres. Una pratica utile e' tenere un test set di Q/A "canary" e calcolare quotidianamente recall@10 in produzione: cali improvvisi indicano regressioni di indice o di modello upstream.

Costo totale. Il vector DB sembra economico al singolo store ma in produzione i costi includono: storage (proporzionale a vettori * dim * dtype), memoria RAM per indice (HNSW va in RAM per latenza bassa), CPU/GPU per query QPS, traffico in/out, ricostruzione periodica. Per corpora oltre 100M vettori, l'analisi di scelta tra managed (Pinecone, Weaviate Cloud) e self-hosted (Qdrant, Milvus su Kubernetes) deve includere costo del personale operativo, non solo bill cloud.

Anti-pattern di scelta. Pubblicare benchmark "il mio DB e' piu' veloce" su dataset sintetico (SIFT 1M, GIST 1M) e considerarlo predittivo del proprio caso reale: spesso non lo e'. La distribuzione dei vettori reali (non uniformi, cluster diseguali, presenza di outlier), la composizione delle query (filtered, hybrid, multi-vector), la concorrenza, sono tutte specifiche al carico. Conviene eseguire un benchmark sul proprio dato prima di decidere.

## Aggiornamenti

Nessun aggiornamento dopo la creazione (2026-04-28).
