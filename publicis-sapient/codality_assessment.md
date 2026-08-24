# Codility Practice Problems

## 1. URL Shortener — FastAPI

Build a simple URL shortener using **Python + FastAPI**.

### Requirements

1. **Create short URL**
   - `POST /`
   - Request JSON:
     ```json
     {"url": "https://example.com/long/url"}
     ```
   - Generate a random **5-character** key.
   - Return status **201**:
     ```json
     {"short_url": "https://company.com/abc12"}
     ```

2. **Redirect**
   - `GET /{key}`
   - Redirect to the original URL.
   - Return **404** if the key does not exist.
   - Increment the visit count on each successful redirect.

3. **Visit count**
   - `GET /info/{key}`
   - Return:
     ```json
     {"visits": 5}
     ```

4. **Idempotency**
   - Submitting the same long URL again must return the **same short URL**.

5. **Validation**
   - Reject invalid URLs.

### Suggested data

```text
long URL → short key
short key → original URL + visit count
```

---

## 2. Count Preceding Divisors

Given an integer array `A`, for every element count how many **previous elements divide it**.

Implement:

```python
def solution(A):
    ...
```

### Example

```text
A      = [2, 4, 3, 6]
Result = [0, 1, 0, 2]
```

Why?

```text
2 → nothing before it              → 0
4 → 2 divides 4                    → 1
3 → neither 2 nor 4 divides 3     → 0
6 → 2 and 3 divide 6              → 2
```

### Another example

```text
A      = [2, 2, 4]
Result = [0, 1, 2]
```

### Important

For each `A[k]`, count only elements at indexes:

```text
j < k
```

A simple solution checking every previous element is **O(N²)**.

A better approach is to keep previously seen values and check the **divisors of the current number**.

Typical complexity:

```text
Time:  O(N × √M)
Space: O(N)
```

where `M` is the maximum value in `A`.
