---
name: Vector database
aliases: [vector database, vector DB, vector store, database vettoriale, ANN index]
categoria: infrastruttura
created: 2026-04-28
last_updated: 2026-06-01
mentions_count: 0
---

# Vector database

## Cos'e

Un vector database e' un sistema di storage e ricerca specializzato per vettori densi ad alta dimensione (256-4096 dim tipicamente), che fornisce indicizzazione approssimata per nearest-neighbor search (ANN) su miliardi di vettori con latenza in millisecondi. La query restituisce i k vettori piu' simili a un vettore di interrogazione secondo una metrica di distanza (coseno, prodotto interno, euclidea L2). E' lo strato di persistenza che supporta gli [embedding](./embedding.md) nei sistemi di [RAG](./rag.md), recommendation, deduplicazione, anomaly detection e, sempre piu' nel 2026, memoria persistente per agenti.

L'idea di indicizzare vettori per ricerca approssimata e' antica: KD-tree (Bentley 1975), LSH (Indyk e Motwani 1998), product quantization (Jegou et al., 2010 con FAISS). La rilevanza esplode dopo il 2020 con la diffusione degli embedding e in modo massivo dal 2023 con il boom di RAG. Il mercato passa da una manciata di librerie (FAISS, Annoy, ScaNN) a un settore con decine di prodotti commerciali (Pinecone, Weaviate, Qdrant, Milvus, Vespa, Chroma, LanceDB, MongoDB Vector, Postgres pgvector, Elasticsearch dense_vector). Nel 2024-2026 la commoditizzazione spinge molti database tradizionali ad aggiungere supporto vettoriale (Postgres, MongoDB, Redis, Cassandra, DuckDB), e la tendenza dominante del 2026 e' chiara: invece di adottare un silos specializzato, molti team usano il database che hanno gia' in casa (in primis Postgres con pgvector) finche' la scala lo consente.

L'importanza pratica e' che senza vector database scalabili la ricerca semantica su corpora reali (milioni-miliardi di vettori) diventa impraticabile. Una scansione lineare per ogni query ha costo O(n*d), inaccettabile sopra qualche centinaia di migliaia di vettori. ANN index riducono il costo a O(log n) o O(sqrt(n)) accettando una piccola perdita di recall (qualita'). Va pero' segnalato un controcanto emerso con forza nel 2026 nei contesti agentici: per corpora gestiti da agenti con accesso a strumenti, la ricerca lessicale (grep) puo' battere la ricerca vettoriale su molti task, e la scelta del vector DB non e' sempre la leva piu' importante (vedi sotto, sezione Aggiornamenti).

## Come funziona

Un vector DB ha tre livelli di responsabilita': storage (persistere vettori e metadati), index (struttura dati per ANN), query engine (esegue search filtrato).

Algoritmi di indice principali.

HNSW (Hierarchical Navigable Small World, Malkov e Yashunin 2016). E' lo standard de facto. Costruisce un grafo gerarchico multi-livello: il livello 0 contiene tutti i vertici, livelli superiori sono sottoinsiemi sempre piu' rarefatti. La search greedy parte dall'alto, scende, e converge sul vicino. Recall@10 > 95% con throughput migliaia di QPS per istanza, latency single-digit ms. Costo memoria: ~ 1.5x i vettori grezzi per i puntatori del grafo. Non e' compresso di default, ma combinazioni con quantization sono comuni.

IVF (Inverted File). Si fa k-means sul corpus, ottenendo c centroidi. Ogni vettore viene assegnato al centroide piu' vicino. La query confronta con i centroidi, sceglie i top-`nprobe`, scansiona linearmente i vettori in quei cluster. Trade-off: nprobe piccolo = veloce ma recall basso; nprobe grande = preciso ma lento.

DiskANN. Famiglia di indici a grafo (Vamana) progettati per tenere la maggior parte dei vettori su SSD invece che in RAM, riducendo il costo per vettore. E' la base di pgvectorscale (Timescale/Tiger Data) e di alcune offerte managed; combinato con quantizzazione consente recall alto a frazione del costo memoria di HNSW puro in RAM. E' uno degli approcci che nel 2026 hanno spostato il fronte di Pareto costo/recall su Postgres.

Product Quantization (PQ). Comprime un vettore d-dim in una sequenza di m sub-codici, ognuno indice in un codebook k-means appreso su una sottosezione del vettore. Memoria scende drasticamente (es. 8 byte invece di 4096), con perdita 5-15% recall. PQ si combina con IVF (IVF-PQ) e HNSW (HNSW-PQ) per dataset enormi.

Scalar Quantization (SQ) e Binary Quantization (BQ). SQ riduce ogni dimensione a int8 / int4, perdita di qualita' modesta. BQ porta ogni dimensione a 1 bit, con compressione estrema (32x rispetto a float32) e perdita recuperabile via reranking sui candidati. Sempre piu' usato (Pinecone, Qdrant, Vespa). Una variante che ha avuto trazione nel 2026 e' la Statistical Binary Quantization usata da pgvectorscale, che calibra le soglie di binarizzazione sulla distribuzione del dato per limitare la perdita. Il pattern tipico e' quantization aggressiva per il primo passo di candidate retrieval + reranking con vettori a precisione piena (o con un modello cross-encoder) sui top-k.

Filtered search. Le query reali non sono solo "k-NN", ma "k-NN dove `tenant_id = X` e `date > Y`". Implementazioni: pre-filter (filtra prima, poi ANN sul subset, perde efficienza HNSW), post-filter (ANN, poi filtra, rischia di non avere abbastanza risultati), hybrid (filtri integrati nell'index, vincolando l'esplorazione del grafo). I provider differiscono molto qui; i benchmark realistici devono includere filtered queries. La gestione dei filtri selettivi su HNSW e' stata storicamente un punto debole: algoritmi come ACORN (adottato da Qdrant) hanno reso competitive le query molto selettive che prima degradavano drasticamente recall o latenza.

Hybrid retrieval. Combinazione di dense (ANN) + sparse (BM25). Reciprocal Rank Fusion combina rank list. Sistemi come Vespa, Weaviate, Elastic, Qdrant offrono hybrid built-in. Migliora il retrieval su query con identifier o terminologia tecnica. Il supporto a sparse vector come cittadino di prima classe e' in espansione anche su pgvector.

Considerazioni quantitative. Un indice HNSW su 10 milioni di vettori a 1024 dim float32: ~60 GB. Con int8 quantization: ~15 GB. Con binary embedding (1 bit/dim): ~1.5 GB con perdita ~3-5% (recuperabile con reranking). Latenza P99 < 30 ms. Build time iniziale: minuti-ore. Update incrementale supportato, ma cancellazioni richiedono spesso compaction periodica.

Operazioni di scaling. Sharding orizzontale: il corpus viene partizionato; query fan-out a tutti gli shard, merge dei top-k. Replication: read replicas per QPS. Dimensioni reali in produzione: Pinecone serve indici da 100B+ vettori distribuiti; Vespa di Yahoo gestisce indici hybrid su petabyte.

## Varianti / approcci

| Categoria | Esempi | Quando |
|---|---|---|
| Pure vector SaaS | Pinecone, Weaviate Cloud, Qdrant Cloud | Workload focalizzato vector, gestione managed |
| Self-hostable open | Qdrant, Milvus, Weaviate, Chroma | Privacy, on-prem, costi controllati |
| Embedded / lightweight | Chroma, LanceDB, sqlite-vss, USearch, faiss | Prototipi, app desktop, in-process |
| Estensioni a DB tradizionali | pgvector / pgvectorscale (Postgres), Redis Vector, MongoDB Atlas, Elastic dense_vector | Stack esistente, no-new-store |
| Search engine + vector | Vespa, Elasticsearch, OpenSearch | Hybrid retrieval enterprise |
| Distributed analytical | Milvus, Vespa | Petascale corpora |

Per RAG di scala piccola-media (< 1M vettori) pgvector o Chroma sono spesso sufficienti. Una regola pratica diffusa nel 2026 e' che pgvector copre bene la grande maggioranza dei workload sotto i ~10M vettori, specie quando servono filtri SQL ricchi, multi-tenant e persistenza durevole nello stesso DB transazionale. Per scale > 100M, soluzioni specializzate (Qdrant cluster, Vespa, Pinecone, Milvus) danno vantaggi misurabili. Per ricerca enterprise complessa (multi-tenant, ACL fine-grained, hybrid, reranking), Vespa e Weaviate hanno feature ricche; Qdrant si distingue per filtered search e quantization su singolo binario Rust.

Asse di trade-off: recall vs latency vs costo. Tutti i sistemi scelgono un punto in questo triangolo. Benchmark indipendenti (ANN-Benchmarks, dbpedia, BEIR) misurano il fronte di Pareto, ma vanno presi con cautela (vedi Note operative): i dataset classici a bassa dimensione (SIFT, GIST) non rappresentano gli embedding LLM moderni ne' i carichi reali con scritture continue, filtri e picchi di concorrenza.

## Quando usarlo / quando no

Un vector DB e' la scelta giusta quando il corpus supera ~100k vettori, quando si fanno query vector ad alta frequenza (chat, ricerca live), quando si serve multi-tenant con isolation, quando l'organizzazione ha gia' uno stack dati e vuole aggiungere capacita' vector. E' essenziale per [RAG](./rag.md) di produzione e per la memoria di lungo periodo degli agenti, dove servono filtri metadata-rich e isolamento per utente o sessione.

E' overkill quando: il corpus e' < 10k vettori (un array NumPy in memoria con cosine similarity batchata fa la stessa cosa); la latenza non conta (una scansione lineare e' piu' semplice); il dato non e' realmente vettoriale (per match esatto serve un B-tree, non ANN). Un caso emergente da considerare: per agenti che lavorano su un corpus navigabile con strumenti (codebase, file system, knowledge base con struttura), la ricerca lessicale via grep puo' superare la ricerca vettoriale su molti task, evitando del tutto il costo di indicizzazione e re-embedding.

Anti-pattern. Sovra-indicizzare prima di benchmark: scegliere il DB con piu' feature senza misurare recall sul proprio dataset. Mescolare embedding di modelli diversi nello stesso indice (gli spazi non sono allineati). Ignorare la dimensione di metadati: alcuni provider fatturano sui metadata bytes. Non testare filtered queries: il calo di performance con filter e' provider-specifico e drammatico. Aggiornare l'embedding model senza re-indicizzare l'intero corpus: si distrugge consistenza. Adottare un vector DB specializzato per default quando lo stack Postgres esistente reggerebbe la scala attuale.

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

Per workload misti vector + relational, pgvector e' una scelta naturale. Performance HNSW su pgvector e' migliorata significativamente nel 2024-2025; nel 2026 pgvector 0.9 ha aggiunto miglioramenti a IVFFlat, supporto a sparse vector e ulteriori ottimizzazioni di velocita', mentre l'estensione pgvectorscale (DiskANN + Statistical Binary Quantization) ha portato il throughput di Postgres a livelli competitivi con i vector DB specializzati su decine di milioni di vettori. Va ricordato che questi numeri provengono da benchmark di vendor e vanno verificati sul proprio carico.

Esempio 3: scale-out con sharding. Un'azienda media servizio chat su 200M chunk di documenti. Setup: 4 nodi Qdrant in cluster, replication factor 2, sharding per tenant_id. Memoria totale: ~120 GB con int8 quantization. P95 latenza < 50 ms con filter su tenant. Costo infrastruttura: ~ 1500-3000 USD/mese su cloud comparabile.

## Letture

- Malkov e Yashunin, "Efficient and robust approximate nearest neighbor search using Hierarchical Navigable Small World graphs" (HNSW), 2016. https://arxiv.org/abs/1603.09320
- Jegou et al., "Product Quantization for Nearest Neighbor Search", IEEE TPAMI 2010.
- Johnson et al., "Billion-scale similarity search with GPUs" (FAISS), 2017. https://arxiv.org/abs/1702.08734
- Pan et al., "Vector Database Management Techniques and Systems", VLDB 2024. https://arxiv.org/abs/2310.14021
- Sen et al., "Is Grep All You Need? How Agent Harnesses Reshape Agentic Search", 2026. https://arxiv.org/abs/2605.15184
- Pinecone, "Learning Center" e blog tecnici. https://www.pinecone.io/learn
- Qdrant documentation. https://qdrant.tech/documentation/
- pgvector. https://github.com/pgvector/pgvector
- ANN-Benchmarks. https://ann-benchmarks.com/

## Note operative

Operazioni e backup. Un indice vector va trattato come un database: backup regolari, monitoring, alerting su latenza P99 e recall. La maggior parte dei sistemi moderni supporta snapshot e restore; Pinecone offre PITR su tier enterprise; pgvector eredita le procedure Postgres. Una pratica utile e' tenere un test set di Q/A "canary" e calcolare quotidianamente recall@10 in produzione: cali improvvisi indicano regressioni di indice o di modello upstream.

Costo totale. Il vector DB sembra economico al singolo store ma in produzione i costi includono: storage (proporzionale a vettori * dim * dtype), memoria RAM per indice (HNSW va in RAM per latenza bassa; DiskANN sposta parte del costo su SSD), CPU/GPU per query QPS, traffico in/out, ricostruzione periodica. Per corpora oltre 100M vettori, l'analisi di scelta tra managed (Pinecone, Weaviate Cloud) e self-hosted (Qdrant, Milvus su Kubernetes) deve includere costo del personale operativo, non solo bill cloud.

Anti-pattern di scelta. Pubblicare benchmark "il mio DB e' piu' veloce" su dataset sintetico (SIFT 1M, GIST 1M) e considerarlo predittivo del proprio caso reale: spesso non lo e'. I dataset classici hanno dimensionalita' bassa e non riflettono gli embedding LLM ad alta dimensione; le leaderboard premiano condizioni statiche, mentre la produzione deve sopravvivere a scritture continue, filtri su metadati e picchi di concorrenza. La distribuzione dei vettori reali (non uniformi, cluster diseguali, presenza di outlier), la composizione delle query (filtered, hybrid, multi-vector), la concorrenza, sono tutte specifiche al carico. Conviene eseguire un benchmark sul proprio dato prima di decidere.

## Aggiornamenti

Nessun aggiornamento dopo la creazione (2026-04-28).

### 2026-06-01

Nel mese non emergono lanci dirompenti di nuovi prodotti, ma si consolidano due tendenze. Sul fronte engine, pgvector/pgvectorscale (DiskANN + Statistical Binary Quantization) e tecniche di binary quantization con reranking spostano il fronte costo/recall, rafforzando il pattern "usa il Postgres che hai gia'" per la maggior parte dei workload sotto ~10M vettori. Sul fronte retrieval, il paper "Is Grep All You Need?" (arXiv:2605.15184, in listing 15 maggio) mostra empiricamente che nella ricerca agentiva grep batte spesso la ricerca vettoriale e che la varianza dovuta all'harness CLI supera quella dovuta all'algoritmo di retrieval; ridimensiona quindi il vector DB come leva primaria nei contesti agentici (vedi [../../digest/2026/05/16.md](../../digest/2026/05/16.md)). Si segnala anche, sul tema correlato della quantizzazione di modelli, l'acquisizione di Eigen AI da parte di Nebius ([../../digest/2026/05/03.md](../../digest/2026/05/03.md)), indicatore del valore attribuito allo strato di ottimizzazione.
