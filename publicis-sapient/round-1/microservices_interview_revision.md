# Microservices — Last-Minute Interview Revision

## Core Mental Model

Microservices are mainly about:
- Splitting a system into services
- Service communication
- Failure handling
- Distributed data/consistency
- Independent scaling/deployment

**Key principle:** High cohesion within a service, low coupling between services.

## 1. Service Boundaries

Prefer boundaries around **business capabilities / bounded contexts**.

```text
Customer | Order | Payment | Inventory | Shipping
```

A good service has:
- Clear business responsibility
- High internal cohesion
- Low dependency on other services
- Independent deployability/scaling

Avoid creating a separate service for every small entity.

## 2. Database per Service

```text
User Service    → User DB
Order Service   → Order DB
Payment Service → Payment DB
```

**Benefits:** loose coupling, independent scaling, schema evolution.

**Costs:** distributed transactions, consistency challenges, operational complexity.

## 3. Service Communication

### Synchronous

```text
Order → HTTP/REST/gRPC → Payment → Response
```

Use when the caller needs the result immediately.

**Pros:** simple, immediate response.

**Cons:** runtime coupling; downstream latency/failure affects caller.

### Asynchronous

```text
Order → Kafka → Payment
```

Use when processing does not need to finish before the caller continues.

**Pros:** loose coupling, resilience, buffering, independent processing.

**Costs:** eventual consistency, duplicates, ordering issues, harder debugging.

## 4. API Gateway

```text
Client
  ↓
API Gateway
  ↓
User / Order / Payment / Inventory
```

Common responsibilities:
- Authentication
- Routing
- Rate limiting
- TLS termination
- Logging
- API aggregation

**Trade-off:** Don't put complex business logic in the gateway; otherwise it can become a bottleneck/new monolith.

## 5. Service Discovery

Microservice instances are dynamic, so avoid hard-coded IPs.

> **Service Discovery = mechanism for dynamically finding the network location of another service.**

Two approaches:

```text
Client-side:
Order → Registry → choose Payment instance

Server-side:
Order → Load Balancer → Payment instance
```

### Kubernetes connection

Kubernetes runs applications in **Pods**. Pod IPs can change.

A Kubernetes **Service** provides a stable network identity for a group of Pods:

```text
Order
  ↓
payment-service
  ↓
Pod 1 / Pod 2 / Pod 3
```

Kubernetes DNS can resolve the service name.

Important:

```text
Service Discovery → find service instances
Load Balancing    → distribute traffic among instances
```

## 6. Resilience Patterns

### Timeout
Maximum time we're willing to wait for a dependency.

### Retry
Retry transient failures only.

Use:
- Limited retries
- Exponential backoff
- Jitter

### Circuit Breaker

Protects against repeated dependency failures/cascading failure.

```text
CLOSED → repeated failures → OPEN
OPEN → cooldown → HALF-OPEN
HALF-OPEN → success → CLOSED
HALF-OPEN → failure → OPEN
```

- **CLOSED:** normal traffic
- **OPEN:** fail fast / block calls
- **HALF-OPEN:** allow test calls

**Retry vs Circuit Breaker:**

```text
Retry            → "Try again; failure may be temporary."
Circuit Breaker  → "Dependency looks unhealthy; stop calling it."
```

### Bulkhead

Isolates resources so one dependency/workload cannot consume everything.

```text
Payment         → limited resources
Inventory       → limited resources
Recommendations → limited resources
```

**Circuit Breaker:** stop calling unhealthy dependency.

**Bulkhead:** isolate resources between workloads.

### Fallback

If an optional dependency fails, return degraded/partial functionality instead of failing the entire request.

First decide whether the dependency is **critical or optional**.

## 7. Saga

Problem: one business transaction spans multiple services/databases.

```text
Create Order → Charge Payment → Reserve Inventory
```

Each service performs a local transaction.

If a later step fails, perform compensating actions:

```text
Order created       ✅
Payment charged     ✅
Inventory reserve   ❌
       ↓
Refund Payment
       ↓
Cancel Order
```

> **Saga = sequence of local transactions + compensating actions.**

Two approaches:
- **Choreography:** services react to events
- **Orchestration:** central Saga coordinator

## 8. Idempotency

Prevents duplicate side effects when requests/messages are retried.

Example:

```text
Request 1 → payment succeeds
Response lost
Request 2 → client retries
```

Use an idempotency key:

```http
POST /payments
Idempotency-Key: abc123
```

Remember:

```text
abc123 → transaction #789 → SUCCESS
```

Repeated request with the same key returns the existing result instead of charging again.

> **Same operation + same idempotency key → same effect.**

Important for:
- Payments
- Order creation
- Retries
- Message processing
- Kafka consumers

## 9. Failure Handling

```text
Request
  ↓
Timeout
  ↓
Retryable?
 ├─ Yes → Limited retry → still failing?
 │                         ↓
 │                    Fallback / error
 └─ No  → Fail
```

Also consider:
- Circuit breaker
- Bulkhead
- Cancellation
- Idempotency
- Critical vs optional dependency

## 10. Architecture Mental Model

```text
                    API Gateway
                         ↓
          ┌──────────────┼──────────────┐
          ↓              ↓              ↓
      User Service   Order Service   Payment Service
          ↓              ↓              ↓
       User DB        Order DB       Payment DB

Communication:
  Sync  → REST / gRPC
  Async → Kafka / events

Resilience:
  Timeout → Retry → Circuit Breaker / Fallback
  Bulkhead → resource isolation
  Idempotency → duplicate protection

Distributed transaction:
  Saga

Dynamic instances:
  Service Discovery
```

## 11. Interview Quick Answers

**Why microservices?**  
→ Independent deployment/scaling, clear business boundaries, team autonomy, and failure isolation.

**What makes a good service boundary?**  
→ A clear business capability with high cohesion and low coupling.

**Why database per service?**  
→ Avoids tight coupling through a shared database, but introduces distributed consistency challenges.

**REST or Kafka?**  
→ REST/gRPC when an immediate response is needed; Kafka when asynchronous processing, decoupling, buffering, or event propagation is valuable.

**Circuit Breaker?**  
→ Stops repeated calls to an unhealthy dependency and helps prevent cascading failures.

**Bulkhead?**  
→ Isolates resources so one workload/dependency cannot take down the entire service.

**Saga?**  
→ Local transactions + compensating actions for distributed business workflows.

**Idempotency?**  
→ Repeating an operation doesn't create unintended additional side effects.

**Service Discovery?**  
→ Dynamically locates available service instances.

**API Gateway?**  
→ Common entry point for routing and cross-cutting concerns such as authentication and rate limiting.

## 12. Pattern Cheat Sheet

| Problem | Pattern |
|---|---|
| Dependency too slow | Timeout |
| Temporary failure | Retry |
| Dependency repeatedly failing | Circuit Breaker |
| One workload consumes resources | Bulkhead |
| Graceful degradation | Fallback |
| Duplicate request/message | Idempotency |
| Multi-service transaction | Saga |
| Dynamic service locations | Service Discovery |
| Common client entry point | API Gateway |
| Async communication | Kafka / Event-driven |

## 13. SDM-Level Framework

When designing a microservices system:

```text
Business capabilities
        ↓
Service boundaries
        ↓
Data ownership
        ↓
Sync vs async
        ↓
Failure handling
        ↓
Consistency requirements
        ↓
Scaling
        ↓
Observability
        ↓
Deployment
```

**Interview principle:**

> Don't name a pattern first. Identify the problem first, then choose the pattern and explain its trade-off.

### Status

**Microservices → 🟢 Interview Ready**
