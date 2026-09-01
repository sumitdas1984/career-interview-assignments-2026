# Kafka — High-Level Interview Revision

## 1. What is Kafka?

Kafka is a **distributed event streaming / messaging platform**.

For our interview, think of Kafka as:

> **A durable buffer between a producer and consumers that allows work/events to be processed asynchronously.**

Simple model:

```text
Producer → Kafka → Consumer
```

---

## 2. Why Do We Need Kafka?

Consider document processing.

Without Kafka:

```text
User
 ↓
FastAPI
 ↓
OCR
 ↓
Chunking
 ↓
Embedding
 ↓
LLM
 ↓
Response
```

The API request may stay open for a long time because document processing can take seconds or minutes.

This becomes problematic when many documents arrive together.

With Kafka:

```text
User
 ↓
FastAPI
 ↓
Kafka
 ↓
202 Accepted

Kafka
 ↓
Document Workers
 ↓
OCR → Chunking → Embedding → LLM
```

The API accepts the job quickly and the actual processing happens asynchronously.

---

# 3. Kafka in an AI Document Processing System

A realistic flow:

```text
                Upload Document
                       ↓
                    FastAPI
                       ↓
                 Store document
                   in S3/Storage
                       ↓
                Publish event
                       ↓
                    Kafka
                       ↓
              Document Worker(s)
                       ↓
             ┌─────────┼─────────┐
             ↓         ↓         ↓
            OCR     Chunking   Metadata
                       ↓
                   Embedding
                       ↓
                  Vector DB
                       ↓
                      LLM
                       ↓
                Processing Done
```

The Kafka message does **not** need to contain the entire document.

It can contain information needed by the worker:

```json
{
  "document_id": "doc123",
  "location": "s3://bucket/doc123.pdf"
}
```

The worker uses that information to retrieve and process the document.

---

# 4. Why Kafka is a Good Design Decision Here

### 1. Asynchronous processing

Document processing is long-running.

Instead of:

```text
API → wait 30 seconds → response
```

we can:

```text
API → Kafka → 202 Accepted
```

The worker processes the document in the background.

---

### 2. Handles traffic spikes

Suppose 10 documents arrive normally:

```text
Kafka
 ↓
Workers process normally
```

Suddenly 10,000 documents arrive:

```text
FastAPI
   ↓
 Kafka
   ↓
10,000 jobs waiting
   ↓
Workers process gradually
```

Kafka acts as a **buffer**.

The API does not need to process all 10,000 documents immediately.

---

### 3. Independent scaling

If document processing becomes the bottleneck:

```text
Kafka
 ↓
Worker 1
Worker 2
Worker 3
Worker 4
Worker 5
```

We can increase the number of workers without necessarily scaling the API layer by the same amount.

---

### 4. Failure isolation

Suppose the LLM service temporarily fails:

```text
FastAPI → Kafka → Worker → LLM ❌
```

The API can continue accepting new document requests while the processing side recovers, depending on the overall failure-handling design.

This prevents a slow/failing downstream processing component from directly blocking every upload request.

---

### 5. Decoupling

Without Kafka:

```text
FastAPI → Document Processor
```

The API directly depends on the processor.

With Kafka:

```text
FastAPI → Kafka → Document Processor
```

The API only needs to publish the processing request.

The processing system can evolve independently.

---

### 6. Multiple consumers

After a document is processed, multiple systems may be interested in the result:

```text
                 Kafka
                   ↓
          DocumentProcessed
                   ↓
        ┌──────────┼──────────┐
        ↓          ↓          ↓
   Notification  Search    Analytics
```

The document processor doesn't need to directly call every downstream system.

---

# 5. Kafka vs Direct API Call

### Direct synchronous call

```text
FastAPI → Document Worker
```

Good when:

- The result is needed immediately
- Processing is quick
- Simple request/response is sufficient

But the API becomes dependent on the worker's availability and latency.

### Kafka

```text
FastAPI → Kafka → Document Worker
```

Good when:

- Processing is long-running
- Work can happen asynchronously
- Traffic can arrive in bursts
- Workers need to scale independently
- Multiple systems need to react to events

### Key trade-off

```text
REST/direct call
→ simpler

Kafka
→ more resilient and scalable for asynchronous workflows
→ but adds architectural and operational complexity
```

**Do not use Kafka simply because it is popular.**

---

# 6. Event-Driven Thinking

An **event** represents something that happened.

Examples:

```text
DocumentUploaded
DocumentProcessed
DocumentFailed
OrderCreated
PaymentCompleted
```

For example:

```text
FastAPI
   ↓
DocumentUploaded
   ↓
Kafka
   ↓
Document Worker
```

The producer says:

> "A document was uploaded."

Consumers decide what they need to do in response.

This is the basic idea of **event-driven architecture**.

---

# 7. Minimal Kafka Concepts You Should Know

For this interview, remember only these:

### Producer

The application that publishes an event.

```text
FastAPI → Kafka
```

### Topic

A named stream/category where related events are published.

```text
document-events
```

### Consumer

The application that reads/processes events.

```text
Kafka → Document Worker
```

### Workers / Consumers

Multiple workers can process documents concurrently so the system can scale.

You do **not** need to go deep into Kafka internals for the current interview preparation.

---

# 8. When NOT to Use Kafka

Kafka can be unnecessary when:

- The operation is simple
- The result is needed immediately
- Traffic is small
- There is no asynchronous processing requirement
- A direct REST/gRPC call is sufficient

For example:

```text
GET /users/123
```

Usually:

```text
API → User Service
```

is better than introducing Kafka.

---

# 9. Interview Answers

### "Why Kafka?"

> "I would use Kafka when I need asynchronous processing, decoupling, buffering for traffic spikes, independent scaling, or multiple consumers reacting to events."

### "Why Kafka for document processing?"

> "Document processing is long-running and potentially bursty. Instead of keeping the API request open, I can publish a document-processing job to Kafka and return 202 Accepted. Workers consume the jobs asynchronously and can scale independently. Kafka also provides buffering and decouples the API from the processing pipeline."

### "Why not directly call the worker?"

> "A direct call creates runtime coupling. If the worker is slow or unavailable, the API is directly affected. Kafka allows the API to accept the work and lets processing happen asynchronously."

### "Why not use Kafka everywhere?"

> "Kafka adds complexity. For simple synchronous request/response interactions, REST or gRPC is usually simpler and more appropriate."

---

# Last-Minute Cheat Sheet

```text
Kafka
  ↓
Durable buffer / event stream
  ↓
Producer → Kafka → Consumer

Why?
  ├── Async processing
  ├── Buffer traffic spikes
  ├── Independent worker scaling
  ├── Failure isolation
  ├── Service decoupling
  └── Multiple consumers

AI Document Processing:

User
 ↓
FastAPI
 ↓
Kafka
 ↓
Document Workers
 ↓
OCR
 ↓
Chunking
 ↓
Embedding
 ↓
Vector DB / LLM

Key decision:

Quick + immediate result
→ REST/direct call

Long-running + async + bursty
→ Kafka is a strong option
```

### Status

**Kafka → 🟢 High-Level Interview Ready**
