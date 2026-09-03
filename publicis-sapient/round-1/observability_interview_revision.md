# Observability — Interview Revision

## 1. What is Observability?

> **Observability = understanding the internal state/behavior of a system from the data it produces.**

It helps answer questions such as:

> "The application is slow. Which component is causing the problem?"

Example:

```text
User
 ↓
API Gateway
 ↓
FastAPI
 ↓
Kafka
 ↓
Worker
 ↓
LLM
 ↓
Database
```

---

# 2. Three Pillars

```text
              Observability
                    │
       ┌────────────┼────────────┐
       ↓            ↓            ↓
     Logs         Metrics       Traces
       ↓            ↓            ↓
 What happened?  How much?   Where/why?
```

## Logs

Tell you **what happened**.

Example:

```text
document_id=123
LLM request started

document_id=123
LLM request failed
timeout
```

Useful for investigating specific errors/events.

Good logs typically include:

```text
Timestamp
Service
Request/Correlation ID
Operation
Error
Latency
```

Avoid logging sensitive information.

---

## Metrics

Give numerical information about system behavior over time.

Examples:

```text
Request rate    → 1,000 req/sec
Error rate      → 2%
P95 latency     → 500 ms
CPU usage       → 75%
Memory usage    → 80%
Kafka lag       → increasing
```

For APIs, remember:

```text
Traffic
Errors
Latency
```

Often summarized as **RED**:

```text
Rate
Errors
Duration
```

---

## Traces

Show the journey of **one request across multiple services**.

Example:

```text
Request abc123

Gateway       10 ms
Order         20 ms
Payment      400 ms
Database      50 ms
--------------------
Total        480 ms
```

This helps identify where the request spent time.

---

# 3. Correlation / Request ID

A request can carry the same ID through multiple services:

```text
Request ID = abc123

Gateway
   ↓ abc123
FastAPI
   ↓ abc123
Kafka
   ↓ abc123
Worker
   ↓ abc123
LLM
```

You can then search logs for `abc123` and follow the request across the system.

This is especially useful in distributed systems.

---

# 4. Logs vs Metrics vs Traces

| Pillar | Main question |
|---|---|
| **Logs** | What happened? |
| **Metrics** | How much/how often/how bad? |
| **Traces** | Where did the request spend time? |

Example:

```text
API is slow

Metrics:
P95 latency → 300 ms → 2 sec

Trace:
LLM call → 1.6 sec

Logs:
LLM timeout/retry occurred
```

Together they help diagnose the problem.

---

# 5. Observability in an AI System

Consider:

```text
User
 ↓
FastAPI
 ↓
Kafka
 ↓
Document Worker
 ↓
OCR
 ↓
Embedding
 ↓
Vector DB
 ↓
LLM
```

Useful signals to monitor:

### API

```text
Request rate
Error rate
P95/P99 latency
```

### Kafka

```text
Messages produced
Messages processed
Consumer lag
```

### Worker

```text
Processing time
Failure rate
Queue backlog
```

### LLM

```text
Latency
Error rate
Token usage
Cost
```

### Vector DB

```text
Query latency
Error rate
```

AI systems need additional attention to **LLM latency, token usage, and cost**.

---

# 6. HLD Scenario

### Question

> "Users report that document processing has become slow. How would you investigate?"

### Strong answer

> "I'd start with metrics to determine whether latency or error rates have increased and identify which component is affected. Then I'd use distributed tracing to locate the slow component—for example OCR, embedding, vector search, or the LLM. Finally, I'd use correlated logs for that request/document ID to understand the specific failure or bottleneck."

Think:

```text
Metrics
  ↓
Is there a problem? How large?

Traces
  ↓
Where is the problem?

Logs
  ↓
Why is it happening?
```

---

# 7. Monitoring vs Observability

### Monitoring

> **Is something wrong?**

Example:

```text
P95 latency > 2 seconds
```

### Observability

> **Why is it wrong?**

Example:

```text
Trace → LLM call = 1.8 sec
Logs  → repeated LLM retries
```

---

# 8. Last-Minute Cheat Sheet

```text
OBSERVABILITY
→ Understand system behavior from emitted data

LOGS
→ What happened?

METRICS
→ How much/how often/how bad?

TRACES
→ Where did the request spend time?

CORRELATION ID
→ Follow one request across services

API metrics
→ Rate + Errors + Latency

AI system metrics
→ API + Kafka + Workers + LLM + Vector DB

Investigation flow
→ Metrics → Traces → Logs
```

## Interview Principle

> **Design observability into the system from the beginning. Don't wait for production problems to start collecting telemetry.**

### Status

**Observability → 🟢 Interview Ready**
