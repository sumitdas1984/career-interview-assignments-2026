# Part 3 — Indexing + Retrieval + Query Rewriting + Reranking

## Complete Retrieval Pipeline

```text
OFFLINE
Document → Parsing → Chunking → Embedding → Vector Index

ONLINE
User Query
   ↓
Query Rewriting / Decomposition
   ↓
Query Embedding
   ↓
Vector Search + BM25
   ↓
Hybrid Retrieval
   ↓
Top-K
   ↓
Reranker
   ↓
Top-N
   ↓
Context Construction
   ↓
LLM
```

## 1. Vector Index

A vector index makes nearest-neighbor search efficient.

Naive approach:

```text
Query → compare against every vector
```

At millions of vectors this is expensive.

> **Vector index = data structure/algorithm that makes vector similarity search efficient.**

---

## 2. ANN

**ANN = Approximate Nearest Neighbor**

Instead of comparing with every vector:

```text
Millions of vectors
      ↓
ANN index
      ↓
Promising candidates
      ↓
Top-K
```

Trade-off:

```text
Exact search → highest accuracy, more computation
ANN          → much faster, may sacrifice some recall
```

---

## 3. HNSW

**HNSW = Hierarchical Navigable Small World**

A graph-based ANN indexing algorithm.

Conceptually:

```text
Start
  ↓
Navigate through nearby vectors
  ↓
Move toward more similar vectors
  ↓
Find nearest candidates
```

Interview answer:

> "HNSW is a graph-based ANN index that enables efficient approximate nearest-neighbor search by navigating connections between vectors."

---

## 4. Vector Index vs Vector Database

### Vector Index
Search structure for efficient similarity search.

Examples:

```text
HNSW
IVF
PQ
```

### Vector Database
Manages:

```text
Vectors
+ Metadata
+ Indexes
+ Search APIs
```

> **The index is a component of the vector database.**

---

## 5. Metadata Filtering

Production retrieval often combines semantic search with metadata constraints.

Example:

```text
year = 2025
document_type = "audit_standard"
user_access = true
```

Benefits:

- Better relevance
- Smaller search space
- Security/access control

Important:

> **A semantically relevant document is not useful if the user is not authorized to see it.**

---

# 6. Vector Search

Uses embeddings to find semantically similar chunks.

Good for:

- Semantic similarity
- Paraphrased questions
- Different wording with similar meaning

Example:

```text
"How can we reduce audit risk?"
        ↓
Find chunks with similar meaning
```

---

# 7. BM25 / Keyword Search

BM25 is lexical/keyword-based retrieval.

Good for:

- Exact terminology
- IDs
- Acronyms
- Product names
- Legal references
- Technical terms

Example:

```text
"PCAOB AS 2201"
```

Exact terms can be very important.

---

# 8. Vector Search vs BM25

```text
Vector Search → semantic meaning
BM25          → lexical / exact terms
```

Example:

```text
"AI investment"
        ≈
"spending on artificial intelligence"
```

Vector search can capture this semantic relationship.

But:

```text
"PCAOB AS 2201"
```

may benefit strongly from BM25.

---

# 9. Hybrid Search

Combine both:

```text
                 Query
                   ↓
          ┌────────┴────────┐
          ↓                 ↓
    Vector Search         BM25
          ↓                 ↓
       Results            Results
          └────────┬────────┘
                   ↓
             Combine / Rank
                   ↓
               Reranker
                   ↓
                  Top-N
```

> **Hybrid retrieval combines semantic and lexical retrieval for more robust results.**

### Combining results

Weighted scoring:

```text
Final Score =
    α × Vector Score
  + β × BM25 Score
```

Or rank-based fusion.

**RRF = Reciprocal Rank Fusion** combines ranked result lists based on result positions.

No formula is required for the interview.

---

# 10. Top-K

If:

```text
Top-K = 20
```

retrieval returns 20 candidate chunks.

```text
Millions of chunks
       ↓
Retrieval
       ↓
Top 20
       ↓
Reranker
       ↓
Top 5
       ↓
LLM
```

Why not too small?

Relevant information may rank lower.

Why not too large?

More processing, reranking, context, latency, cost and noise.

> **Top-K is a recall vs latency/cost trade-off.**

---

# 11. Reranking

Initial retrieval is designed to be **fast and broad**.

It may not perfectly order results.

```text
Top 50 candidates
      ↓
Reranker
      ↓
Top 5–10
```

The reranker evaluates:

```text
Query + Candidate Chunk
```

and produces a more detailed relevance assessment.

Goal:

> **Improve precision and place the most relevant chunks near the top.**

---

# 12. Bi-Encoder vs Cross-Encoder

### Bi-Encoder

```text
Query → Vector
Chunk → Vector
       ↓
Compare vectors
```

Fast because document embeddings can be precomputed.

Used for:

> **Large-scale first-stage retrieval**

### Cross-Encoder

```text
Query + Chunk
      ↓
Reranker
      ↓
Relevance Score
```

More expensive but usually better at detailed query-document relevance.

Used for:

> **Reranking a relatively small candidate set**

Remember:

```text
Bi-encoder  → Fast + scalable
Cross-encoder → More accurate + expensive
```

---

# 13. Two-Stage Retrieval

Important production pattern:

```text
Millions of chunks
       ↓
Fast retrieval
       ↓
Top 50–100
       ↓
Expensive reranker
       ↓
Top 5–10
       ↓
LLM
```

First stage:

> **Maximize recall**

Second stage:

> **Maximize precision**

---

# 14. Query Rewriting

The original query may not be ideal for retrieval.

Example:

```text
User:
"What about the exceptions?"
```

Rewrite to:

```text
"What exceptions did the audit committee identify
regarding revenue recognition?"
```

> **Query rewriting improves or clarifies the search query before retrieval.**

---

# 15. Query Expansion / Multi-Query

Example:

```text
"AI investment"
```

becomes:

```text
"artificial intelligence investment"
"AI spending"
"AI infrastructure investment"
```

Then:

```text
Multiple Queries
      ↓
Multiple Searches
      ↓
Merge Results
      ↓
Rerank
```

Potential benefit:

> Higher recall.

Trade-offs:

> More search operations, latency, cost and potentially more noise.

---

# 16. Query Decomposition

Complex questions can be split into sub-questions.

Example:

```text
"Compare Bosch and Siemens' AI investments in 2024."
```

Could become:

```text
Bosch AI investment 2024
Siemens AI investment 2024
Compare investment levels
```

Useful for:

- Complex questions
- Multi-hop retrieval
- Comparative questions

---

# 17. Query Rewriting vs Reranking

Very important:

```text
Query Rewriting
→ Improves the QUERY
→ Before retrieval
→ "How should I search?"

Reranking
→ Improves the RESULTS
→ After retrieval
→ "Which retrieved results are most relevant?"
```

---

# 18. When Query Rewriting Can Hurt

Rewriting introduces another model decision.

Example:

```text
Original:
"What is AS 2201?"
```

An incorrect rewrite could change the user's intent.

Therefore:

> **Query rewriting can improve retrieval but can also introduce errors or alter intent.**

For simple, well-formed queries, it may provide little value.

---

# 19. Important HLD Trade-offs

### Recall vs Latency

```text
Higher K
→ Better chance of finding relevant chunks
→ More processing
```

### Precision vs Recall

```text
Broad retrieval
→ Higher recall + more noise

Aggressive filtering
→ Higher precision + risk of missing relevant information
```

### Reranking Quality vs Latency

```text
More powerful reranker
→ Better ranking
→ More latency/cost
```

### Hybrid Search

```text
Vector + BM25
→ More robust retrieval
→ More system complexity
```

### Query Rewriting

```text
Better query
→ Potentially better retrieval
→ Additional latency/cost
→ Risk of changing intent
```

---

# 20. Why Not Send 100 Chunks to the LLM?

More context does not necessarily mean better context.

```text
100 chunks
   ↓
More tokens
   ↓
Higher cost
Higher latency
More noise
Potentially worse answer
```

Goal:

> **High-quality, relevant context — not maximum context.**

---

# 21. If RAG Retrieval Is Poor

Don't immediately replace the embedding model.

Investigate:

```text
Poor Retrieval
     ↓
Document parsing
Chunking
Embedding model
Similarity metric
Top-K
Metadata filters
Hybrid search
Query rewriting
Reranking
```

Evaluate retrieval separately before changing the LLM.

Useful metrics:

```text
Recall@K
Precision@K
MRR
NDCG
```

---

# 22. HLD Question — Large-Scale Retrieval

### "Your RAG system has 100 million chunks. How would you make retrieval efficient?"

Strong answer:

> "I wouldn't perform brute-force comparison across all vectors. I'd use an approximate nearest-neighbor index such as HNSW, combined with metadata filtering to reduce the search space. I'd use a fast first-stage retrieval to generate a candidate set and then apply a more expensive reranker to that smaller set. I'd tune the retrieval parameters based on latency and recall requirements."

---

# 23. HLD Question — Why Not Rerank Everything?

> "A cross-encoder evaluates the query and candidate document together, so applying it to millions of documents would be extremely expensive. I'd first use fast ANN/BM25 retrieval to generate a smaller candidate set and then rerank only those candidates."

---

# 24. HLD Question — Poor RAG Answers

> "I'd first determine whether the issue is retrieval or generation. For retrieval, I'd inspect chunking, embedding quality, index configuration, Top-K, metadata filters, hybrid search, query rewriting and reranking. I'd evaluate retrieval using metrics such as Recall@K and NDCG before changing the LLM."

---

# 25. Final Mental Model

```text
INDEXING
→ Make large-scale vector search efficient

QUERY REWRITING
→ Improve / clarify the search query

VECTOR SEARCH
→ Semantic similarity

BM25
→ Exact lexical matching

HYBRID SEARCH
→ Semantic + lexical retrieval

TOP-K
→ Broad candidate set

RERANKING
→ More accurate ordering

TOP-N
→ Best context for the LLM

LLM
→ Generate final answer
```

## Core Architecture Principle

> **Use a fast first-stage retrieval to maximize recall, then use a more expensive reranker to maximize precision before sending a small, high-quality context to the LLM.**

### Status

**Indexing + Retrieval + Query Rewriting + Reranking → 🟢 Interview Ready**
