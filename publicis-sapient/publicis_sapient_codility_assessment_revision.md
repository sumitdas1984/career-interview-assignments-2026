# Publicis Sapient — Codility Assessment Follow-Up Documentation

> **Purpose:** Interview revision document for the follow-up rounds.  
> **Source:** Notes captured after the assessment. The source material describes two problems and their requirements, but it does **not** contain the exact code submitted during the assessment or a record of the candidate's exact implementation decisions. Therefore, the solution discussions below distinguish the documented requirements from recommended reasoning/implementation.

---

## 1. Assessment Overview

The assessment notes captured two coding problems:

1. **URL Shortener — FastAPI**
   - Python + FastAPI
   - REST API design
   - URL validation
   - Random short-key generation
   - Redirect handling
   - Visit-count tracking
   - Idempotency for repeated long URLs

2. **Count Preceding Divisors**
   - Array processing
   - Divisibility logic
   - Preserving index ordering
   - Complexity optimization from a straightforward `O(N²)` solution to an approach based on enumerating divisors

### What the assessment appears to test

Based on the captured requirements, the problems cover two different dimensions:

| Problem | Primary areas tested |
|---|---|
| URL Shortener | FastAPI, REST API design, validation, state management, idempotency, HTTP redirects |
| Count Preceding Divisors | Algorithmic reasoning, divisibility, complexity analysis, optimization |

---

# 2. Problem 1 — URL Shortener Using FastAPI

## 2.1 Problem Statement

Build a simple URL-shortening service using **Python + FastAPI**.

The service must accept a long URL, generate a random **5-character** key, and return a short URL.

Example request:

```json
{
  "url": "https://example.com/long/url"
}
```

Example response:

```json
{
  "short_url": "https://company.com/abc12"
}
```

The creation endpoint should return HTTP **201**.

The service must also:

- Redirect a short key to its original URL.
- Return **404** when the key does not exist.
- Increment the visit count on every successful redirect.
- Return visit information.
- Be idempotent for the same long URL.
- Reject invalid URLs.

---

## 2.2 API Requirements

### A. Create Short URL

```text
POST /
```

Input:

```json
{
  "url": "https://example.com/long/url"
}
```

Expected behavior:

1. Validate the supplied URL.
2. Check whether the long URL has already been shortened.
3. If it already exists, return the existing short URL.
4. Otherwise:
   - Generate a random 5-character key.
   - Associate the key with the long URL.
   - Initialize its visit count.
5. Return HTTP `201`.

Example:

```json
{
  "short_url": "https://company.com/abc12"
}
```

### B. Redirect

```text
GET /{key}
```

Expected behavior:

1. Look up the key.
2. If the key does not exist, return `404`.
3. If it exists:
   - Increment the visit count.
   - Redirect the client to the original URL.

### C. Visit Count

```text
GET /info/{key}
```

Example response:

```json
{
  "visits": 5
}
```

### D. Idempotency

If the same long URL is submitted repeatedly, the service must return the **same short URL**.

For example:

```text
POST https://example.com/a
→ https://company.com/abc12

POST https://example.com/a
→ https://company.com/abc12
```

It must not generate a new key for the same long URL.

### E. Validation

Invalid URLs must be rejected.

A FastAPI/Pydantic request model is a natural place to perform this validation.

---

# 3. Recommended Data Model / In-Memory Design

The assessment notes suggest two logical mappings:

```text
long URL → short key
short key → original URL + visit count
```

A practical in-memory representation would therefore use two structures:

```text
url_to_key
    long_url → short_key

key_to_url
    short_key → {
        url: original_url,
        visits: count
    }
```

### Why two mappings?

The two main operations have different lookup requirements.

#### Create operation

We need:

```text
long URL → existing short key?
```

This supports idempotency efficiently.

#### Redirect operation

We need:

```text
short key → original URL
```

This supports fast redirection.

Using only one mapping would make one of these operations unnecessarily expensive.

---

# 4. Solution Reasoning — URL Shortener

## 4.1 Step 1 — Validate Input

The request should be represented using a typed request model.

Conceptually:

```python
class URLRequest:
    url: validated URL
```

The important point for the interview is:

> URL validation should happen at the API boundary rather than allowing invalid data to enter the application state.

---

## 4.2 Step 2 — Check Idempotency

Before generating a key:

```text
Does url_to_key contain this URL?
```

If yes:

```text
return the existing short URL
```

This is important because generating the key first would violate the idempotency requirement.

### Interview explanation

> "I would first check whether the long URL already exists in the reverse mapping. If it does, I reuse the existing key. Only when the URL is new do I generate a short key."

---

## 4.3 Step 3 — Generate a Random 5-Character Key

The key must contain exactly five characters.

The key-generation logic should use a sufficiently large character set, for example:

```text
[a-zA-Z0-9]
```

Conceptually:

```text
generate random 5-character key
```

### Important issue: collision handling

A random key is not automatically unique.

For example:

```text
URL A → abc12
URL B → abc12
```

would create a collision.

Therefore, after generating a key, check:

```text
if key already exists:
    generate another key
```

The important invariant is:

```text
Every active short key maps to exactly one long URL.
```

---

# 5. Redirect Logic

For:

```text
GET /{key}
```

the lookup should be approximately:

```text
key
 ↓
key_to_url
 ↓
original URL + visit count
```

If not found:

```text
404 Not Found
```

If found:

```text
visits += 1
redirect(original_url)
```

### Important ordering

The visit count should be incremented only for a successful redirect.

So:

```text
unknown key → 404 → no visit increment
known key   → increment → redirect
```

---

# 6. Visit Count Endpoint

For:

```text
GET /info/{key}
```

the service looks up the key and returns its visit count.

If the key does not exist, a consistent API would return `404`.

Example:

```json
{
  "visits": 5
}
```

---

# 7. What Went Well — URL Shortener

Based on the requirements captured in the notes, the important design decisions to demonstrate in the follow-up discussion are:

### 1. Correct API decomposition

The problem naturally separates into:

```text
POST /          → create
GET /{key}      → redirect
GET /info/{key} → statistics
```

This is a clean REST-oriented decomposition.

### 2. Idempotency was explicitly handled

The requirement that the same long URL return the same short URL is easy to overlook.

The key design point is maintaining:

```text
long URL → short key
```

in addition to:

```text
short key → long URL
```

### 3. Collision handling matters

Random generation alone is insufficient.

A robust solution must verify that the generated key is not already present.

### 4. Visit counting is tied to successful redirects

The count should represent successful redirect activity, not arbitrary requests.

---

# 8. What Could Be Improved — URL Shortener

The source notes do not record the exact implementation submitted, so the following are **follow-up areas to verify/discuss**, rather than claims about what was done incorrectly.

## 8.1 Persistent storage

The captured problem describes logical mappings but does not specify a database.

For a coding assessment, in-memory dictionaries may be sufficient.

For production, however:

```text
FastAPI
   ↓
Database
   ↓
URL mappings
```

would be preferable.

Possible choices include:

- PostgreSQL
- Redis
- DynamoDB
- another persistent key-value/data store

---

## 8.2 Concurrency

The visit count introduces a concurrency consideration.

If multiple requests update the same counter simultaneously, a production implementation needs an atomic increment mechanism.

For example, with a database:

```text
UPDATE ... SET visits = visits + 1
```

rather than:

```text
read visits
increment in application
write visits
```

---

## 8.3 Key generation

For a real service, random 5-character keys have a finite keyspace.

With alphanumeric characters:

```text
62^5
```

possible combinations exist.

As the number of URLs grows, collision probability increases.

A production design might therefore consider:

- a larger key
- deterministic encoding of an ID
- a collision-resistant ID-generation strategy

---

## 8.4 URL normalization

A deeper follow-up question could be:

> Should two syntactically different but semantically equivalent URLs produce the same short URL?

For example, URL normalization can involve:

```text
scheme
host casing
default ports
trailing slash
query parameters
fragment
```

The assessment only requires "same long URL", so a simple exact-string comparison is sufficient unless normalization is explicitly required.

---

## 8.5 Abuse and security considerations

For a production system, additional controls could include:

- rate limiting
- malicious URL detection
- authentication/authorization if required
- expiration of short URLs
- maximum URL length
- monitoring
- audit logging

These are not stated assessment requirements and should therefore be presented as production extensions rather than part of the core solution.

---

# 9. Likely Follow-Up Questions — URL Shortener

### Q1. Why do you need two mappings?

**Answer:**

> "Because the create operation needs efficient lookup from long URL to short key for idempotency, while the redirect operation needs efficient lookup from short key to long URL. Two mappings give efficient lookup in both directions."

### Q2. What happens if the generated key already exists?

> "I check the key mapping after generation. If it already exists, I generate another key until I obtain an unused key."

### Q3. How would you make the visit counter safe under concurrency?

> "In production I would use an atomic increment at the persistence layer, such as a database atomic update or Redis INCR."

### Q4. Would you use random keys in production?

> "Possibly for a small system, but I would consider a larger keyspace or encoding a unique ID to control collision probability as the system grows."

### Q5. What would you change if the service had millions of URLs?

> "I would move the state from process memory to persistent storage, introduce horizontal scaling, and use a shared datastore. I would also consider caching popular short-key lookups."

---

# 10. Problem 2 — Count Preceding Divisors

## 10.1 Problem Statement

Given an integer array `A`, for every element count how many **previous elements divide it**.

Implement:

```python
def solution(A):
    ...
```

Only elements at earlier indexes are considered:

```text
j < k
```

---

## 10.2 Example 1

Input:

```text
A = [2, 4, 3, 6]
```

Output:

```text
[0, 1, 0, 2]
```

Reasoning:

```text
2 → no previous elements → 0

4 → 2 divides 4 → 1

3 → neither 2 nor 4 divides 3 → 0

6 → 2 divides 6
     3 divides 6
     → 2
```

Therefore:

```text
[0, 1, 0, 2]
```

---

## 10.3 Example 2

Input:

```text
A = [2, 2, 4]
```

Output:

```text
[0, 1, 2]
```

Reasoning:

```text
2 → no previous element → 0

2 → previous 2 divides it → 1

4 → previous 2 divides it
     previous 2 divides it
     → 2
```

The second example highlights an important point:

> Duplicate values at different previous indexes must each be counted.

---

# 11. Straightforward Solution

The simplest solution is to examine every previous element.

For each position `k`:

```text
for every j < k:
    if A[k] % A[j] == 0:
        count += 1
```

### Complexity

There can be approximately:

```text
N × (N - 1) / 2
```

comparisons.

Therefore:

```text
Time:  O(N²)
Space: O(N)
```

The result array itself requires `O(N)` space.

---

# 12. Optimized Approach

The notes identify a better approach:

> Keep previously seen values and check the **divisors of the current number**.

Instead of asking:

```text
Which previous values divide A[k]?
```

we reverse the question:

```text
What are the divisors of A[k]?
Which of those divisors have appeared previously?
```

---

## 12.1 Example

Consider:

```text
A = [2, 4, 3, 6]
```

At:

```text
A[k] = 6
```

the divisors are:

```text
1, 2, 3, 6
```

The previously seen values are:

```text
2, 4, 3
```

Among the divisors of `6`:

```text
2 → seen
3 → seen
```

Therefore:

```text
count = 2
```

---

# 13. Important Detail: Count Frequencies, Not Just Presence

The second example makes this especially important.

```text
A = [2, 2, 4]
```

When processing `4`, its divisor `2` has appeared **twice**.

Therefore:

```text
count = 2
```

A simple set is not enough:

```text
seen = {2}
```

would only tell us that `2` exists.

We need frequency information:

```text
frequency[2] = 2
```

Then:

```text
frequency[2]
```

correctly contributes `2` to the answer for `4`.

---

# 14. Optimized Algorithm

Maintain a frequency map of previously seen values.

For each value `x`:

### Step 1

Find all divisors of `x`.

A divisor pair can be found efficiently by iterating:

```text
d = 1 ... sqrt(x)
```

If:

```text
x % d == 0
```

then:

```text
d
x // d
```

are both divisors.

### Step 2

For each divisor, look up its frequency among previously seen values.

### Step 3

Add those frequencies to the result.

### Step 4

After calculating the answer for `x`, increment:

```text
frequency[x] += 1
```

This ordering is critical.

The current element must **not** count itself.

---

# 15. Why the Ordering Matters

Suppose:

```text
A = [2]
```

When processing `2`, the answer must be:

```text
0
```

not `1`.

Therefore:

```text
calculate answer
        ↓
add current value to frequency map
```

must happen in that order.

If we add the current value first, the current element could incorrectly become its own preceding divisor.

---

# 16. Complexity

Let:

```text
M = maximum value in A
```

For each element, divisor enumeration takes approximately:

```text
O(sqrt(A[k]))
```

Therefore the notes characterize the typical complexity as:

```text
Time:  O(N × √M)
Space: O(N)
```

The space is `O(N)` for storing frequencies/results in the general case.

This is substantially better than:

```text
O(N²)
```

when the values are not extremely large.

---

# 17. What Went Well — Divisor Problem

The strongest algorithmic insight is the transformation from:

```text
check all previous elements
```

to:

```text
enumerate divisors of current element
+
look them up among previous values
```

This changes the problem from an index-oriented scan into a value/frequency lookup problem.

### Key strengths to communicate

1. **Correctly respected `j < k`.**
2. **Recognized the naive `O(N²)` approach.**
3. **Used divisors of the current value to reduce unnecessary comparisons.**
4. **Used frequencies rather than only presence**, which handles duplicates correctly.
5. **Avoided counting the current element** by updating the frequency map after computing its result.

---

# 18. What Could Be Improved — Divisor Problem

The source notes do not preserve the exact submitted implementation, so these should be treated as areas for follow-up discussion rather than claims about the submitted code.

## 18.1 Be explicit about duplicate values

The example:

```text
[2, 2, 4] → [0, 1, 2]
```

is particularly useful in an interview.

It demonstrates why:

```text
set
```

is insufficient and why:

```text
frequency map
```

is needed.

---

## 18.2 Handle divisor pairs carefully

When enumerating divisors up to `sqrt(x)`, a perfect square needs special handling.

For example:

```text
x = 16
```

When:

```text
d = 4
```

both calculated divisors are:

```text
4 and 4
```

They must not be counted twice.

---

## 18.3 Clarify assumptions about input values

The captured notes say the input consists of integers but do not specify constraints such as:

- whether values can be zero
- whether values can be negative
- maximum value
- whether values are bounded

The `O(N × √M)` divisor approach naturally assumes positive values.

If asked in an interview, a good response is:

> "I would first confirm the input constraints, particularly whether zero or negative values are allowed, because the divisor-enumeration approach and complexity depend on those assumptions."

---

# 19. Likely Follow-Up Questions — Divisor Problem

### Q1. Why not use `O(N²)`?

> "The straightforward approach checks every previous element for every current element. That gives `O(N²)`. Since the question is specifically about divisibility, I can enumerate the divisors of the current value and use a frequency map to determine which divisors have occurred before."

### Q2. Why do you need a frequency map instead of a set?

> "Because duplicate previous values count separately. For `[2, 2, 4]`, both occurrences of `2` divide `4`, so the answer is `2`. A set would only record one occurrence."

### Q3. Why enumerate only up to the square root?

> "Divisors occur in pairs. If `d` divides `x`, then `x // d` is also a divisor. Once I check up to `sqrt(x)`, I can discover both members of each pair."

### Q4. How do you avoid counting the same divisor twice for a perfect square?

> "When `d * d == x`, the two members of the divisor pair are identical, so I add that divisor only once."

### Q5. How do you prevent the current element from counting itself?

> "I calculate its answer using the frequency map of previous elements first, and only then add the current value to the map."

---

# 20. Overall Assessment Reflection

Based on the captured notes, the two problems exercised complementary skills.

### Problem 1

Primarily tested:

```text
API design
FastAPI
state management
validation
idempotency
HTTP behavior
```

### Problem 2

Primarily tested:

```text
algorithmic reasoning
complexity
divisibility
frequency counting
optimization
```

This combination is useful preparation for a follow-up interview because the interviewer can probe both:

- **implementation-level decisions**, and
- **reasoning/complexity trade-offs**.

---

# 21. Key Lessons to Retain for the Follow-Up Interview

## URL Shortener

Remember this mental model:

```text
                 ┌── url_to_key ──→ short key
long URL ────────┤
                 └── key_to_url ──→ URL + visits
```

Core points:

```text
validate
  ↓
check idempotency
  ↓
generate unique key if new
  ↓
store both mappings
  ↓
return 201
```

Redirect:

```text
key
 ↓
lookup
 ↓
404 if missing
 ↓
increment visits
 ↓
redirect
```

## Divisor Problem

Remember this transformation:

```text
Naive:
current element
    ↓
check every previous value
    ↓
O(N²)

Optimized:
current element
    ↓
enumerate its divisors
    ↓
frequency lookup among previous values
    ↓
O(N × √M)
```

And the three critical details:

```text
frequency map, not set
calculate before inserting current value
avoid double-counting sqrt divisor
```

---

# 22. 60-Second Interview Summary

If asked to summarize the assessment:

> "The assessment covered two problems. The first was a FastAPI URL shortener where the important parts were API design, URL validation, random 5-character key generation, redirect handling, visit counting, and idempotency. I would use mappings in both directions so that repeated long URLs return the same short URL while short-key lookups remain efficient. I would also explicitly handle key collisions.
>
> The second problem was to count how many preceding array elements divide each current element. The straightforward solution is `O(N²)`, but the better approach is to maintain frequencies of previously seen values and enumerate the divisors of the current number up to its square root. That gives approximately `O(N × √M)` time and `O(N)` space. Duplicate values are important because each occurrence counts separately, so a frequency map is required rather than a set."

---

## Source Boundary

This document is based on the post-assessment notes supplied for this preparation exercise. The notes specify the requirements, examples, and intended complexity of the two problems, but **do not preserve the exact code submitted during the assessment**. Consequently, the sections discussing "what could be improved" and implementation details are framed as interview-preparation guidance rather than retrospective claims about the exact submission.
