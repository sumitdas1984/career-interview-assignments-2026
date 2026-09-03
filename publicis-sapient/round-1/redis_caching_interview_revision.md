# Redis + Caching — Interview Revision

## 1. Why Caching?

Caching stores frequently accessed data in a faster layer so we don't repeatedly access a slower backend such as a database.

```text
Request
  ↓
Cache
  ↓
Database (only when needed)
```

### Benefits
- Lower latency
- Reduced database load
- Better scalability
- Faster responses

### Main trade-off

> **Performance vs freshness/consistency**

Cached data can become stale.

---

## 2. What is Redis?

**Redis is an in-memory data store** commonly used as an application-side cache.

```text
Client
  ↓
FastAPI
  ↓
Redis
  ↓
PostgreSQL
```

Redis can also be used for rate limiting, distributed locks, sessions, and counters. For this interview, focus mainly on caching.

---

## 3. Cache-Aside ⭐⭐⭐

The most important caching strategy for HLD.

The application manages the cache.

```text
Request
   ↓
Check Redis
   ↓
 ┌───────┴───────┐
 HIT             MISS
 ↓                ↓
Return          Database
                  ↓
                Redis
                  ↓
                Return
```

Typical flow:

```python
data = redis.get("user:123")

if data is None:
    data = db.get_user(123)
    redis.set("user:123", data)

return data
```

**Pros:** simple; application controls what gets cached.

**Main problem:** cache invalidation / stale data.

---

## 4. Other Cache Strategies

### Write-Through

```text
Application → Cache → Database
```

Cache is updated along with the database.

**Pros:** less chance of stale cache.  
**Cost:** writes go through the cache.

### Write-Behind / Write-Back

```text
Application → Cache → Database later
```

Fast writes, but higher risk if cached data is lost before reaching the database.

### Read-Through

```text
Application → Cache
                  ↓
              Database
```

The cache layer fetches data from the database on a miss.

### Quick comparison

| Strategy | Basic idea |
|---|---|
| **Cache-Aside** ⭐ | App handles cache + DB fallback |
| **Write-Through** | Update cache and DB together |
| **Write-Behind** | Cache first, DB later |
| **Read-Through** | Cache handles DB fetch on miss |

---

## 5. Cache Invalidation

Problem:

```text
Database:
User = "Sumit Das"

Redis:
User = "Sumit"
```

The cache is stale.

### TTL — Time To Live

```text
user:123
TTL = 10 minutes
```

After expiration:

```text
Cache MISS
   ↓
Database
   ↓
Fresh data → Redis
```

**Pros:** simple.  
**Cons:** data may remain stale until TTL expires.

### Explicit Invalidation

When data changes:

```text
Update Database
      ↓
Delete/update Redis entry
```

Next read fetches fresh data.

### Event-Based Invalidation

```text
User Service
    ↓
Database updated
    ↓
UserUpdated event
    ↓
Kafka
    ↓
Invalidate cache
```

---

## 6. How to Choose Invalidation

Ask:

> **How fresh does the data need to be?**

### Some staleness is acceptable

```text
Cache + TTL
```

Examples:
- Product catalog
- Configuration
- Frequently read metadata

### Stronger freshness is needed

Consider explicit invalidation or an event-based approach.

The more freshness you require, the more complexity you usually introduce.

---

## 7. Cache Stampede

A popular cache entry expires:

```text
Redis
document:123 → expired
```

Then 1,000 requests arrive simultaneously:

```text
1,000 requests
      ↓
Redis
      ↓
1,000 CACHE MISS
      ↓
Database
      ↓
💥 Huge DB spike
```

> **Popular key + expiration + many simultaneous requests → sudden database load.**

Possible solutions:
- Request coalescing / single-flight
- Distributed locking
- Staggered TTLs
- Background refresh

For HLD, recognize the problem and mention the general solutions.

---

## 8. Redis vs CDN

### CDN

Caches content **close to users**.

```text
User
 ↓
CDN
 ↓
Content
```

Good for images, CSS/JS, static files, videos, and some cacheable API responses.

### Redis

Caches data **close to the application**.

```text
Client
 ↓
FastAPI
 ↓
Redis
 ↓
Database
```

Good for application data, DB query results, sessions, counters, and short-lived state.

**Simple distinction:**

> **CDN → cache close to the user.**  
> **Redis → application-side cache.**

---

## 9. Redis + AI Application

Our document-processing system:

```text
User
 ↓
FastAPI
 ↓
Kafka
 ↓
Document Workers
 ↓
OCR → Chunking → Embedding → LLM
```

Redis can cache frequently accessed application data.

### Example: Document Status

Without Redis:

```text
GET /documents/123/status
        ↓
     FastAPI
        ↓
   PostgreSQL
```

With Redis:

```text
GET /documents/123/status
        ↓
     FastAPI
        ↓
      Redis
        ↓
status = PROCESSING
```

This reduces repeated database queries.

Redis could also cache expensive/reusable results where correctness, freshness, and user/context differences are carefully considered.

---

## 10. HLD Scenario

**Question:**  
"Our API is receiving 10× traffic and PostgreSQL is becoming the bottleneck. What would you do?"

**Strong answer:**

> "First I'd identify whether the workload is read-heavy and whether the data can tolerate some staleness. If yes, I'd introduce Redis using a cache-aside strategy. On a cache miss, we'd read from PostgreSQL and populate Redis. I'd use an appropriate TTL and potentially explicit invalidation when data changes. I'd monitor cache hit rate, latency, and database load."

Don't simply say:

> "Add Redis."

Explain why the data is suitable for caching and what freshness trade-off you're accepting.

---

## 11. Key Trade-offs

```text
Caching
  +
Fast responses
  +
Lower DB load
  +
Better scalability

  -
Stale data
  -
Invalidation complexity
  -
Memory/infrastructure cost
  -
Cache stampede risk
```

---

## 12. Last-Minute Cheat Sheet

```text
CACHE
→ Faster access to frequently used data

REDIS
→ In-memory application-side data store
→ Commonly used as a cache

CACHE-ASIDE ⭐
Request → Redis
            ↓ MISS
          Database
            ↓
          Redis

INVALIDATION
→ TTL
→ Explicit delete/update
→ Event-based invalidation

CACHE STAMPEDE
Popular key expires
→ many simultaneous misses
→ database spike

CDN
→ cache close to users

REDIS
→ cache close to application

HLD DECISION
Ask:
"How fresh does this data need to be?"
```

## Interview Principle

> **Don't add caching automatically. First determine whether the data is frequently read, expensive to retrieve, and safe to serve slightly stale. Then choose the caching and invalidation strategy based on the consistency requirement.**

### Status

**Redis + Caching → 🟢 Interview Ready**
