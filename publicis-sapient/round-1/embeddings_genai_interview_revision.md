# Part 2 — Embeddings: GenAI Interview Revision

## Core Idea

> **An embedding is a numerical representation of text that captures semantic information.**

```text
Text
 ↓
Embedding Model
 ↓
Vector
[0.21, -0.43, 0.87, ...]
```

Semantically similar text tends to be close in embedding space.

---

## 1. Why Embeddings?

Keyword search can miss semantic relationships:

```text
"reduce insurance premium"
        ≈
"lower insurance rates"
```

Embeddings enable **semantic search** by comparing vectors rather than relying only on exact words.

---

## 2. Embeddings in RAG

### Ingestion

```text
Document
 ↓
Chunking
 ↓
Embedding Model
 ↓
Vectors
 ↓
Vector DB / Index
```

### Query

```text
User Query
 ↓
Embedding Model
 ↓
Query Vector
 ↓
Vector Search
 ↓
Relevant Chunks
```

The query and document vectors should normally come from the **same/compatible embedding space**.

---

## 3. Similarity Measures

Common choices:

- Cosine similarity
- Dot product / inner product
- Euclidean distance

### Cosine Similarity

Measures the angle/direction between vectors.

> **Focuses on direction rather than magnitude.**

Typical interpretation:

```text
+1 → same direction
 0 → orthogonal
-1 → opposite direction
```

Higher cosine similarity generally means greater semantic similarity.

### Dot Product

```text
A · B
```

Considers direction and magnitude.

Important:

> For **L2-normalized vectors**, dot product and cosine similarity produce the same ranking.

### Euclidean Distance

Measures straight-line distance.

```text
A ●────────● B
```

Smaller distance = closer.

---

## 4. Embedding Dimension

A 768-dimensional embedding is:

```text
[x1, x2, x3, ... x768]
```

Higher dimension does **not automatically mean better**.

Trade-off:

```text
Higher dimension
   +
Potentially richer representation
   -
More memory
   -
More computation
   -
Larger vector index
```

---

## 5. Choosing an Embedding Model

Don't choose only from generic benchmarks.

Consider:

### Retrieval quality
Does it retrieve the correct chunks?

### Domain fit
How well does it handle legal, financial, technical, etc. terminology?

### Latency
Important for ingestion and especially query-time embedding.

### Cost
Consider document volume + query volume + inference cost.

### Dimension
Higher dimensions increase storage/index cost.

### Language support
Important for multilingual systems.

---

## 6. Offline vs Online Embeddings

### Document embeddings

Usually generated during ingestion:

```text
Document
 ↓
Chunk
 ↓
Embedding
 ↓
Vector DB
```

Can be generated asynchronously/batch-wise.

### Query embeddings

Generated at query time:

```text
User Query
 ↓
Embedding
 ↓
Search
```

Therefore query embedding latency directly affects user-facing latency.

---

## 7. Embedding Quality ≠ RAG Quality

A good embedding model alone does not guarantee good RAG.

```text
Parsing
  ↓
Chunking
  ↓
Embedding
  ↓
Indexing
  ↓
Retrieval
  ↓
Reranking
  ↓
Context Construction
  ↓
LLM
```

Example:

```text
Good embedding
+
Poor chunking
=
Poor retrieval
```

Evaluate embeddings within the complete retrieval pipeline.

---

## 8. Dense Embeddings vs Keyword Search

Traditional search:

```text
BM25 / Keyword Search
```

primarily relies on lexical matching.

Embedding search captures semantic relationships:

```text
"AI investment"
        ≈
"spending on artificial intelligence"
```

Modern RAG systems often use:

```text
Keyword Search
      +
Vector Search
      ↓
Hybrid Retrieval
```

---

## 9. Domain-Specific Embeddings

Specialized domains have terminology with specific meanings.

Example:

```text
Legal:
going concern
material misstatement
audit evidence
professional judgment
```

A domain-adapted embedding model may perform better.

But:

> **Domain-specific does not automatically mean better. Benchmark it on your actual data and queries.**

---

## 10. Fine-Tuning Embeddings

If generic embeddings consistently perform poorly:

```text
Generic Embedding Model
        ↓
Domain-specific training data
        ↓
Fine-tuned Embedding Model
```

Training data may contain:

```text
Query → Relevant Chunk
```

or:

```text
Query → Positive Chunk
       → Hard Negative Chunk
```

For interviews, understand the purpose rather than training mechanics.

---

## 11. Normalization

L2 normalization makes vector length equal to 1.

Example:

```text
Before: [3, 4]
After:  [0.6, 0.8]
```

For normalized vectors:

```text
Dot Product ≈ Cosine Similarity
```

Whether to normalize depends on the embedding model and vector database configuration. Don't blindly normalize everything.

---

## 12. Storage at Scale

Example:

```text
10 million chunks
768 dimensions
32-bit floats
```

Approximate raw vector storage:

```text
10M × 768 × 4 bytes
≈ 30.7 GB
```

This excludes:

- Index overhead
- Metadata
- Replicas
- Database overhead

Therefore vector dimension and indexing strategy affect infrastructure cost.

---

## 13. Multilingual Embeddings

For multilingual systems, the model should place semantically equivalent text into a useful shared space.

```text
"How do I reset my password?"
            ≈
"Wie setze ich mein Passwort zurück?"
```

Choose a model that performs well for the required languages.

---

## 14. If Retrieval Is Poor

Don't immediately replace the embedding model.

Investigate:

```text
Poor Retrieval
     ↓
 ┌─────────────────────────┐
 │ Document parsing        │
 │ Chunking                │
 │ Embedding model         │
 │ Similarity metric       │
 │ Top-K                   │
 │ Metadata filters        │
 │ Hybrid search           │
 │ Reranking               │
 └─────────────────────────┘
```

This demonstrates system-level thinking.

---

## 15. Evaluating an Embedding Model

Use representative queries with known relevant chunks:

```text
Queries + Relevant Chunks
          ↓
       Retrieval
          ↓
   Retrieval Metrics
```

Useful metrics:

- Recall@K
- Precision@K
- MRR
- NDCG

### MMR

**Maximal Marginal Relevance**

A retrieval technique balancing:

```text
Relevance + Diversity
```

It reduces redundant results.

### NDCG

**Normalized Discounted Cumulative Gain**

A ranking evaluation metric that rewards highly relevant results near the top.

```text
MMR  → Retrieval technique
NDCG → Evaluation metric
```

---

## 16. HLD Interview Question

### "How would you choose an embedding model for production RAG?"

Strong answer:

> "I'd evaluate it on representative queries and documents from our actual domain rather than relying only on generic benchmarks. I'd consider retrieval quality, domain and language support, latency, cost, vector dimensionality and infrastructure requirements. I'd validate the choice using retrieval metrics such as Recall@K and NDCG and ultimately measure downstream answer quality."

---

# Last-Minute Cheat Sheet

```text
EMBEDDING
→ Numerical representation of semantic meaning
→ Creates a semantic vector space

RAG
Document → Chunk → Embedding → Vector DB

Query
→ Same/compatible embedding space
→ Query vector
→ Similarity search
→ Relevant chunks

SIMILARITY
→ Cosine
→ Dot product
→ Euclidean distance

COSINE
→ Direction

DOT PRODUCT
→ Direction + magnitude
→ Normalized vectors ≈ cosine

DIMENSION
→ Number of vector values
→ Higher ≠ automatically better
→ More dimensions → more storage/computation

MODEL SELECTION
→ Quality
→ Domain fit
→ Language support
→ Latency
→ Cost
→ Dimension

PRODUCTION
→ Document embeddings usually offline/batch
→ Query embeddings online

IMPORTANT
→ Embedding quality alone ≠ RAG quality
→ Evaluate the complete retrieval pipeline

MMR
→ Maximal Marginal Relevance
→ Relevance + diversity

NDCG
→ Normalized Discounted Cumulative Gain
→ Ranking quality
```

## Core Interview Sentence

> **"I would select an embedding model based not only on benchmark quality but on retrieval performance for our actual domain, along with latency, cost, dimensionality, and language requirements. I'd evaluate it using representative queries and retrieval metrics such as Recall@K and NDCG."**

### Status

**Embeddings → 🟢 Interview Ready**
