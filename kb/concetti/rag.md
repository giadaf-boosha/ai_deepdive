---
name: Retrieval-Augmented Generation
aliases: [RAG, retrieval augmented, generazione aumentata da retrieval]
categoria: paradigma
created: 2026-04-28
last_updated: 2026-04-28
mentions_count: 0
---

# Retrieval-Augmented Generation

## Cos'e

Retrieval-Augmented Generation (RAG) e' un paradigma architetturale in cui un [LLM](./llm.md) genera la risposta dopo aver recuperato, da una base di conoscenza esterna, frammenti di testo rilevanti per la query dell'utente. Il modello non si affida solo ai parametri congelati al momento del training; consulta una memoria esplicita, aggiornabile, ispezionabile. Il termine e' stato introdotto dal paper di Lewis et al. (Facebook AI, NeurIPS 2020) "Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks", che proponeva un sistema end-to-end in cui retriever e generator erano addestrati congiuntamente.

Nei sistemi industriali contemporanei il termine RAG ha assunto un significato piu' largo: indica qualunque pipeline in cui un retriever (tipicamente basato su [embedding](./embedding.md) e [vector database](./vector-database.md), spesso ibrido con BM25) seleziona documenti che vengono inseriti nel prompt del generatore prima della risposta. Non c'e' necessariamente joint training; spesso retriever e LLM sono off-the-shelf.

L'importanza di RAG deriva da quattro fattori. Riduce le allucinazioni: il modello cita fatti che ha sotto gli occhi invece di pescarli dalla memoria parametrica. Aggiorna la conoscenza: il knowledge cutoff dell'LLM diventa irrilevante per i fatti coperti dalla base. Permette personalizzazione: ogni organizzazione costruisce la propria base senza riaddestrare il modello. Rende la risposta auditabile: il sistema espone le fonti, l'utente verifica. Per applicazioni enterprise (knowledge base interna, supporto clienti, ricerca legale, documentazione tecnica) RAG e' lo schema di riferimento dal 2023.

## Come funziona

Una pipeline RAG canonica si articola in due fasi: indicizzazione (offline, batch) e query-time (online, per ogni richiesta).

Indicizzazione. I documenti sorgente (PDF, HTML, Markdown, transcript) vengono parsati ed estratti in testo pulito. Si applica chunking: il testo e' diviso in frammenti da 200-1500 token. Le strategie di chunking includono fixed-size con overlap (es. 512 token con overlap 64), semantic chunking (split su confini di paragrafo o sezione), sliding window. Per ogni chunk si calcola un [embedding](./embedding.md) tramite un modello dedicato (text-embedding-3, voyage-3, gte-large, bge-m3). L'embedding e i metadati (sorgente, sezione, timestamp) sono memorizzati in un [vector database](./vector-database.md).

Query-time. La query dell'utente viene trasformata. Spesso si applica query rewriting (l'LLM riscrive la query per renderla autonoma rispetto al contesto conversazionale) e query expansion (HyDE: generare una risposta ipotetica e usarne l'embedding). La query trasformata viene embeddata. Si esegue ricerca approssimata k-nearest-neighbor nel vector database: viene restituita una lista di k chunk con score di similarita' coseno o prodotto scalare. K tipico: 20-100 candidati.

Reranking. I candidati vengono passati a un cross-encoder (es. Cohere Rerank, BGE reranker) che valuta query e chunk congiuntamente, producendo score piu' accurati di quelli del bi-encoder iniziale. Si seleziona top-N (3-10) per il contesto finale.

Augmented generation. Il prompt finale include istruzioni di sistema, i chunk selezionati come contesto, la query. L'LLM genera la risposta condizionata. Si chiede tipicamente di citare le fonti (es. con marker `[1]`, `[2]`) e di rifiutarsi se il contesto non contiene la risposta, per ridurre allucinazioni.

Formula di scoring. La similarita' cosseno tra embedding query `q` e chunk `c` e': `sim(q,c) = (q . c) / (||q|| ||c||)`. Nei sistemi ibridi si combina con BM25 (sparse, basato su term frequency) tramite reciprocal rank fusion: `RRF(d) = sum_i 1/(k + rank_i(d))`, con k tipicamente 60.

Esempio numerico. Una knowledge base aziendale con 500.000 documenti, chunk di 500 token con overlap 50, produce circa 2-4 milioni di chunk. Embedding a 1024 dimensioni in float16 occupano ~8 GB. Un indice HNSW su questa scala risponde in 5-30 ms per query. Il costo dominante e' la latenza dell'LLM nella fase finale (1-5 secondi per risposta completa), non il retrieval.

## Varianti / approcci

| Variante | Idea | Quando |
|---|---|---|
| Naive RAG | Embedding + similarity search + LLM | Prototipo, base di conoscenza piccola |
| Hybrid retrieval | Dense + sparse (BM25) con RRF | Documenti tecnici con identifier o codici |
| Reranking | Cross-encoder dopo bi-encoder | Quando precision e' critica |
| HyDE | Embedding di una risposta ipotetica | Query corte e ambigue |
| Multi-query | LLM genera N riformulazioni, si fa retrieval su ognuna | Query complesse |
| Step-back prompting | LLM astrae un concetto piu' generale prima di cercare | Domande puntuali su domini ampi |
| GraphRAG (Microsoft, 2024) | Costruisce un grafo di entita' e community summary | Domande globali su corpus, non lookup puntuali |
| Agentic RAG | Un [agent](./agent.md) decide se e cosa cercare | Query miste fact-finding + reasoning |
| Self-RAG (Asai et al., 2023) | Il modello emette token di controllo che decidono retrieval | Trade-off automatico tra costo e precisione |
| Long-context only | Inserire l'intero corpus nel [context window](./context-window.md) | Corpora < ~2M token, latenza accettabile |

L'asse "retrieval vs long context" e' diventato centrale: con context window da 1-10M token (Gemini 2, Claude con 1M), per knowledge base piccole l'inserimento intero del corpus diventa praticabile e a volte preferibile, anche se costoso e con degrado di attention al crescere della lunghezza.

## Quando usarlo / quando no

RAG e' la scelta giusta quando: la conoscenza e' specifica all'organizzazione e cambia frequentemente; l'utente si aspetta citazioni e tracciabilita'; il corpus e' troppo grande per il context window o per essere economico inserirlo per ogni query; serve aggiornabilita' incrementale (aggiungere un documento senza riaddestrare). Domini tipici: knowledge base IT, documentazione di prodotto, ricerca legale, compliance, supporto clienti, customer success, onboarding interno.

RAG e' la scelta sbagliata quando: la domanda richiede sintesi globale del corpus (in tal caso GraphRAG o long context vincono); il dato e' tabellare e una query SQL e' piu' adatta; serve [fine-tuning](./fine-tuning.md) per insegnare uno stile o un formato di output (RAG inietta fatti, non comportamento); la base di conoscenza e' minima (100-1000 frammenti) e il long-context e' piu' semplice; serve real-time su feed in millisecondi (RAG aggiunge 50-300 ms di latenza retrieval).

Anti-pattern frequenti. Chunk troppo grandi: il modello fatica a localizzare. Chunk troppo piccoli: si perde contesto. Embedding di qualita' bassa (modelli piccoli generici su dominio tecnico): il retrieval restituisce rumore. Mancanza di metadata filtering: si recuperano chunk obsoleti. Assenza di evaluation: senza ground truth (set di Q/A annotato) e' impossibile capire se il retrieval funziona.

## Esempi pratici

Esempio 1: pipeline minima con LangChain (pseudocodice).

```python
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.vectorstores import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter

# Indicizzazione
docs = load_documents("docs/")
splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
chunks = splitter.split_documents(docs)
vectorstore = Chroma.from_documents(chunks, OpenAIEmbeddings(model="text-embedding-3-small"))

# Query
def answer(question: str) -> str:
    retrieved = vectorstore.similarity_search(question, k=5)
    context = "\n\n".join(d.page_content for d in retrieved)
    prompt = f"Contesto:\n{context}\n\nDomanda: {question}\nRispondi citando le fonti."
    return ChatOpenAI(model="gpt-4o").invoke(prompt).content
```

Esempio 2: RAG con reranker. Dopo `similarity_search(k=50)` si invia la lista a un cross-encoder che restituisce score query-document. Si tiene il top-5. Il guadagno tipico in NDCG@5 e' 10-30 punti rispetto al puro bi-encoder, su benchmark come BEIR.

Esempio 3: scenario reale di assistente legale. Il corpus e' una raccolta di 200.000 sentenze. Si usa hybrid retrieval (BM25 per match esatto su numeri di sentenza + dense per concetti giuridici), reranker fine-tuned su giurisprudenza, citazioni obbligatorie nel prompt. La metrica di successo non e' BLEU ma "percentuale di risposte verificate da un avvocato come correttamente fondate".

## Letture

- Lewis et al., "Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks", NeurIPS 2020. https://arxiv.org/abs/2005.11401
- Gao et al., "Retrieval-Augmented Generation for Large Language Models: A Survey", 2023. https://arxiv.org/abs/2312.10997
- Asai et al., "Self-RAG: Learning to Retrieve, Generate, and Critique through Self-Reflection", 2023. https://arxiv.org/abs/2310.11511
- Edge et al., "From Local to Global: A Graph RAG Approach to Query-Focused Summarization" (Microsoft GraphRAG), 2024. https://arxiv.org/abs/2404.16130
- Gao et al., "Precise Zero-Shot Dense Retrieval without Relevance Labels" (HyDE), 2022. https://arxiv.org/abs/2212.10496
- Anthropic, "Contextual Retrieval", 2024. https://www.anthropic.com/news/contextual-retrieval
- Pinecone Learning Center. https://www.pinecone.io/learn/
- "BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information Retrieval Models", Thakur et al. 2021. https://arxiv.org/abs/2104.08663

## Note operative

Evaluation. Senza misura un sistema RAG e' una scommessa. Suite minima: dataset di 100-300 (query, ground-truth-answer, ground-truth-chunk-ids). Metriche: retrieval (recall@k, MRR, NDCG sui chunk), generation (faithfulness misurata da LLM-as-judge, answer correctness). Tool noti: Ragas, Trulens, DeepEval, ARES. Pipeline tipica: misurare retrieval e generation separatamente per sapere dove intervenire quando le metriche calano.

Aggiornamento incrementale. La base di conoscenza cambia. Pattern: ETL incrementale che rileva nuovi/modificati documenti via webhook o polling, ri-genera embedding solo per chunk affetti, upsert nel vector DB con versioning. Tombstone dei chunk obsoleti, cleanup periodico. Per documenti volatili (CRM, ticket aperti) si arriva a refresh ogni minuti; per knowledge base statica anche giornaliero basta.

Sicurezza e provenance. In contesti regolati, le citazioni non bastano: serve catena auditabile da risposta -> chunk -> documento sorgente -> autore -> data. Conviene persistere ogni chunk con identificativi tracciabili e timestamp, e includere nelle risposte i chunk_id grezzi (anche internamente) cosi' che un audit possa risalire alla fonte esatta usata. Mai concatenare documenti senza demarcatori - rende impossibile attribuire fatti a sorgenti.

Contextual retrieval. Una tecnica recente (Anthropic, 2024): prima di embeddare un chunk, lo si arricchisce con un breve riassunto del documento da cui proviene, generato da un LLM. Cosi' un chunk isolato ("la temperatura era 22 gradi") porta con se' contesto ("estratto del rapporto annuale 2024 di sezione meteo") che migliora il retrieval. Combinato con BM25 e reranker, riduce gli errori di retrieval del 49% nei benchmark Anthropic.

## Aggiornamenti

Nessun aggiornamento dopo la creazione (2026-04-28).
