# REST + GraphQL — Interview Revision

## 1. REST

REST is an architectural style for designing APIs around **resources**.

```text
/users
/orders
/products
/payments
```

Typical operations:

```text
GET    /users/123
POST   /orders
GET    /orders/456
PUT    /orders/456
DELETE /orders/456
```

Core idea:

> **Resources + HTTP methods + stateless requests**

REST is a strong default because it is simple, well understood, and works naturally with HTTP infrastructure.

---

# 2. REST Limitations

## Over-fetching

Client needs:

```text
name
profile_picture
```

but the API returns:

```json
{
  "id": 123,
  "name": "Sumit",
  "email": "...",
  "address": "...",
  "phone": "...",
  "preferences": "...",
  "orders": [...],
  "profile_picture": "..."
}
```

> **Over-fetching = receiving more data than the client needs.**

One possible REST solution:

```text
GET /users/123?fields=name,profile_picture
```

But the API now needs to support and maintain field-selection behavior.

---

## Under-fetching

A UI needs:

```text
User
 ├── Profile
 ├── Orders
 └── Recommendations
```

With REST, the client may need multiple calls:

```text
GET /users/123
GET /users/123/orders
GET /users/123/recommendations
```

> **Under-fetching = one API response does not provide enough data, so the client needs multiple requests.**

---

# 3. Why GraphQL?

GraphQL lets the **client specify exactly which fields it wants**.

Example:

```graphql
query {
  user(id: 123) {
    name
    profilePicture
  }
}
```

Response:

```json
{
  "user": {
    "name": "Sumit",
    "profilePicture": "..."
  }
}
```

Fundamental difference:

> **REST → server determines the response shape.**

> **GraphQL → client specifies the fields it wants.**

---

# 4. When GraphQL Is Useful

Choose GraphQL when:

- Clients need flexible data selection
- REST has significant over-fetching
- REST has significant under-fetching
- A client needs data from multiple backend services
- Different clients need different subsets of data

Example:

```text
                    GraphQL API
                         ↓
              ┌──────────┼──────────┐
              ↓          ↓          ↓
            User       Orders     Payment
           Service     Service     Service
```

The GraphQL layer can aggregate the data and return one response to the client.

---

# 5. REST vs GraphQL

| REST | GraphQL |
|---|---|
| Resource-oriented endpoints | Query-based API |
| Server determines response shape | Client specifies response fields |
| Can over-fetch | Reduces over-fetching |
| Can under-fetch | Can fetch related data together |
| Simple HTTP model | Query language + schema |
| HTTP caching is straightforward | Caching can be more complex |
| Simpler operational model | More API/platform complexity |

Do not say:

> "GraphQL is better than REST."

Instead:

> **Choose based on the application's requirements and trade-offs.**

---

# 6. GraphQL Trade-offs

GraphQL provides flexibility, but introduces additional complexity.

### Query complexity

Clients can potentially request very deep or expensive queries.

```text
User
 └── Orders
      └── Products
           └── Reviews
                └── Users
```

Need controls such as:

- Query depth/complexity limits
- Rate limiting

### N+1 Problem

A query for many users may cause:

```text
1 query → users

+ 100 queries → orders for each user
```

This is the **N+1 problem**.

Batching/data-loader approaches can help.

### Caching

REST works naturally with HTTP caching.

GraphQL often has one endpoint with many possible queries, so traditional HTTP caching can be more complicated.

### Other complexity

Also consider:

- Schema management
- Authorization
- Observability

---

# 7. Why Choose GraphQL Over REST?

### Strong interview answer

> **"I would choose GraphQL when clients need flexibility in the data they request, especially when we're seeing significant over-fetching or under-fetching with REST. It's also useful when a client needs to aggregate data from multiple backend services into a single response."**
>
> **"The trade-off is that GraphQL introduces additional complexity. We need to manage the schema, control expensive or deeply nested queries, handle issues such as the N+1 problem, and caching can be more complicated than with REST. There can also be additional complexity around authorization and observability."**
>
> **"So I wouldn't replace REST with GraphQL by default. If our APIs are simple and stable, REST is usually a better choice. I'd introduce GraphQL when the flexibility and aggregation benefits justify the additional complexity."**

---

# 8. Concrete Example

Mobile UI needs:

```text
User
 ├── name
 ├── profile picture
 └── last 3 orders
```

REST might require:

```text
GET /users/123
GET /users/123/orders
```

GraphQL:

```graphql
query {
  user(id: 123) {
    name
    profilePicture
    orders(limit: 3) {
      id
      total
    }
  }
}
```

The client gets exactly the required data through one API request.

---

# 9. REST → GraphQL Migration

Don't rewrite the entire REST system immediately.

A safer approach:

```text
                    Client
                       ↓
                  GraphQL Layer
                  /                            ↓             ↓
          Existing REST      New APIs
              APIs
```

The GraphQL layer initially acts as a **facade/aggregation layer** over existing REST services.

Example:

```graphql
query {
  customer(id: 123) {
    name
    orders {
      id
      total
    }
  }
}
```

Internally it might call:

```text
GET /users/123
GET /users/123/orders
```

The client doesn't need to know that.

Then migrate capabilities incrementally based on actual needs.

> **Don't rewrite everything at once.**

---

# 10. HLD Decision Framework

When deciding between REST and GraphQL, ask:

```text
Are APIs simple and stable?
        ↓
       Yes
        ↓
      REST

Are clients suffering from:
  → over-fetching?
  → under-fetching?
  → many API calls?
  → need for flexible responses?
  → data aggregation?
        ↓
       Yes
        ↓
    Consider GraphQL
```

---

# 11. Last-Minute Cheat Sheet

```text
REST
→ Resource-oriented
→ Simple HTTP API
→ Good default

REST problems
→ Over-fetching
→ Under-fetching
→ Multiple calls for aggregated data

GraphQL
→ Client specifies required fields
→ Flexible response shape
→ Useful for aggregation

GraphQL costs
→ Query complexity
→ N+1 problem
→ More complicated caching
→ Schema/authorization/observability complexity

Migration
→ Add GraphQL facade
→ Reuse existing REST APIs
→ Migrate incrementally

Decision
→ Don't choose GraphQL because it is newer
→ Choose it when its flexibility/aggregation benefits justify the complexity
```

## Key Interview Sentence

> **GraphQL gives clients more flexibility and reduces over/under-fetching, but transfers more complexity to the API platform.**

### Status

**REST + GraphQL → 🟢 Interview Ready**
