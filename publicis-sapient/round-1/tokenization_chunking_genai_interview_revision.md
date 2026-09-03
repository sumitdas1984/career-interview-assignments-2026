# Tokenization + Chunking — GenAI Interview Revision

## Core Difference

```text
Tokenization → How text becomes tokens for the model
Chunking     → How a large document becomes retrieval units
Embedding    → How chunks become vectors
```

## 1. Tokenization

LLMs process **tokens**, not raw text. A token can be a word, part of a word, punctuation, or whitespace-related text. Exact tokenization depends on the model/tokenizer.

### Why it matters

```text
System prompt
+ User query
+ Retrieved context
+ Conversation history
+ Output
----------------
≤ Context window
```

Token count affects:
- Context-window usage
- Cost
- Latency

> **Tokenization determines how text consumes the model's context budget.**

---

## 2. Tokenization in RAG

```text
User Query
+ Retrieved Chunks
+ Instructions
        ↓
      Tokens
        ↓
       LLM
```

Too much retrieved text means more tokens, cost, latency, and potentially more noise.

---

# 3. Chunking

A large document should usually be divided into smaller retrieval units.

```text
Document
   ↓
Chunks
 ├── Company History
 ├── Financial Results
 ├── AI Strategy
 ├── Risk Management
 └── HR Policies
```

Each chunk can have its own embedding and become a retrieval unit.

### Real purpose

> **Chunking creates retrieval units that are small enough for precise retrieval but large enough to preserve the context needed to answer a question.**

Treat chunking as a **retrieval optimization problem**, not simply "split every 500 tokens."

---

# 4. Chunk Size Trade-off

### Too Small

```text
Better precision
+
Less context
-
Important context may be split
```

### Too Large

```text
More context
+
Less precise retrieval
-
More irrelevant information
-
Higher token/cost/latency
```

> **There is no universally correct chunk size.**

Consider document structure, query patterns, embedding model, retrieval method, and context limits.

---

# 5. Chunk Overlap

Example:

```text
Chunk size = 500 tokens
Overlap    = 50 tokens
```

Overlap helps preserve context across boundaries.

### Trade-off

```text
More overlap
    ↓
More duplicated content
    ↓
More embeddings/storage
More retrieval candidates
Potentially more LLM tokens
```

> **Overlap improves boundary continuity but increases redundancy and cost.**

---

# 6. Fixed-Size Chunking

```text
Document
 ↓
500 tokens
 ↓
500 tokens
 ↓
500 tokens
```

### Pros
- Simple
- Predictable
- Easy to implement

### Cons
- Ignores document structure
- Can split paragraphs/sections unnaturally
- Can separate related information

---

# 7. Structure-Aware / Semantic Chunking

Use document structure instead of blindly splitting every N tokens.

```text
Document
 ├── Chapter
 │    ├── Section
 │    │    ├── Paragraph
 │    │    └── Paragraph
 │    └── Section
 └── Chapter
```

Try to preserve:

```text
Heading + related paragraphs
```

Useful for:
- Legal documents
- Technical documentation
- Financial reports
- Policies
- Research papers

For structured documents, this is often a better starting point than blind fixed-size splitting.

---

# 8. Hierarchical Chunking

```text
Document
   ↓
Sections
   ↓
Subsections
   ↓
Paragraphs
   ↓
Smaller retrieval chunks
```

Useful metadata:

```json
{
  "document_id": "annual_report_2025",
  "section": "AI Strategy",
  "page": 42,
  "chunk_id": "chunk_128"
}
```

Metadata helps with retrieval, filtering, citations, and context reconstruction.

---

# 9. Production Chunk Metadata

Consider storing:

```text
document_id
chunk_id
page_number
section
document_type
timestamp
access_permissions
```

Retrieval can combine:

```text
Semantic similarity
+
Metadata filtering
```

Example:

> Search only 2025 documents the current user is authorized to access.

---

# 10. How Tokenization and Chunking Connect

```text
Document
   ↓
Tokenizer / token-aware processing
   ↓
Tokens
   ↓
Chunking
   ↓
Retrieval Chunks
   ↓
Embedding
```

Prefer token-aware limits because models operate within token/context constraints.

---

# 11. Choosing Chunk Size — Interview Answer

> "I wouldn't choose a fixed size blindly. I'd consider the document structure, query patterns, embedding model and context window. I'd generally start with structure-aware chunks and a reasonable token limit, possibly with some overlap, and evaluate retrieval and answer quality. I'd then tune chunk size and overlap based on those results."

---

# 12. Chunking Is More Than Size

A production strategy may consider:

```text
Chunk size
Chunk overlap
Document structure
Semantic boundaries
Metadata
Parent-child relationships
Query patterns
Retrieval evaluation
```

Objective:

> **Retrieve the right information with enough context while minimizing unnecessary tokens.**

---

# 13. Interview Quick Answers

**What is tokenization?**

> "Tokenization converts text into tokens that the model processes. It affects context-window usage, cost and latency."

**Why chunk documents?**

> "To create focused retrieval units. The goal is to balance retrieval precision with enough context to answer the query."

**Why not one embedding per document?**

> "A large document can contain many unrelated topics. One embedding may represent too much mixed information and make precise retrieval harder."

**Why not very small chunks?**

> "They can improve precision but may lose surrounding context."

**Why not very large chunks?**

> "They preserve context but introduce irrelevant information and increase token, latency and cost."

**Why overlap?**

> "To preserve context across chunk boundaries, while accepting additional redundancy and cost."

**Fixed-size or semantic chunking?**

> "It depends on the document. Fixed-size is simple and predictable; structure-aware or semantic chunking is often better for structured documents. I'd validate the choice using retrieval and answer-quality metrics."

---

# Last-Minute Cheat Sheet

```text
TOKENIZATION
→ Text → Tokens
→ Model-dependent
→ Impacts context, cost, latency

CHUNKING
→ Document → Retrieval units
→ Goal: precision + sufficient context

SMALL CHUNKS
→ Precise, less context

LARGE CHUNKS
→ More context, more noise/cost

OVERLAP
→ Preserves boundary context
→ Adds redundancy/cost

FIXED-SIZE
→ Simple, may ignore structure

STRUCTURE-AWARE
→ Preserves headings/sections/semantic boundaries

METADATA
→ page, section, document_id, permissions, etc.

KEY PRINCIPLE
→ Chunking is a retrieval optimization problem
→ Evaluate and tune; no universal chunk size
```

## Core Interview Sentence

> **"I treat chunking as a retrieval optimization problem. The goal is to create semantically coherent chunks that are small enough for precise retrieval and efficient context usage, but large enough to preserve the context required to answer the query."**

### Status

**Tokenization + Chunking → 🟢 Interview Ready**
