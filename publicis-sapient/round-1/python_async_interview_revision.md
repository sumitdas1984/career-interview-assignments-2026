# Python `asyncio` — Last-Minute Interview Revision

## 1. Core Idea

**Async is mainly for I/O-bound work.**

Instead of blocking while waiting for I/O, the event loop can run other async tasks.

```text
Task A → waiting for I/O
             ↓
        Event Loop
             ↓
         Task B runs
```

- **Concurrency:** multiple tasks make progress by switching between them.
- **Parallelism:** multiple tasks execute at the same time, typically using multiple cores/threads/processes.
- Async ≠ parallelism.

## 2. Key Concepts

### `async def`
Defines a **coroutine function**.

```python
async def foo():
    ...
```

Calling it creates a **coroutine object**.

### `await`
Waits for an async operation and gives the event loop an opportunity to run other tasks.

```python
result = await foo()
```

### Task
Schedules a coroutine under the event loop.

```python
task = asyncio.create_task(foo())
```

Use when you need control over the task lifecycle or want to start work before awaiting it.

## 3. Sequential vs Concurrent

### Sequential

```python
a = await get_a()
b = await get_b()
c = await get_c()
```

If each takes 2 seconds:

```text
2s + 2s + 2s ≈ 6s
```

### Concurrent

For independent operations:

```python
a, b, c = await asyncio.gather(
    get_a(),
    get_b(),
    get_c()
)
```

Approximately:

```text
max(2s, 2s, 2s) ≈ 2s
```

**Rule:** Don't make dependent operations concurrent just because async is available.

## 4. `gather()` vs `create_task()`

### `asyncio.gather()`

Use when you have multiple operations and want their results.

```python
results = await asyncio.gather(
    get_user(),
    get_orders(),
    get_recommendations()
)
```

Think:

> **Run these together → wait for results.**

### `asyncio.create_task()`

Use when you want to schedule a coroutine as a task and manage it separately.

```python
task = asyncio.create_task(get_data())

# do other async work

result = await task
```

Think:

> **Start/schedule this work → decide when to await/control it.**

## 5. Blocking Code — Common Interview Trap

Bad:

```python
async def get_data():
    return requests.get(url)
```

`requests.get()` is synchronous/blocking and can block the event loop.

Prefer an async library:

```python
async def get_data():
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
    return response
```

If unavoidable:

```python
result = await asyncio.to_thread(blocking_function)
```

Remember:

```text
Async I/O        → await it
Blocking I/O     → don't block event loop
Cannot replace?  → consider to_thread()
CPU-heavy Python → consider processes/workers
```

## 6. Timeouts

Never allow a downstream call to wait indefinitely.

```python
result = await asyncio.wait_for(
    get_orders(),
    timeout=3
)
```

Modern alternative:

```python
async with asyncio.timeout(3):
    result = await get_orders()
```

Concept:

```text
Call → wait → timeout → stop/cancel → handle timeout
```

## 7. Retries

Retry **transient** failures, not everything.

Potentially retryable:
- Timeout
- Temporary connection failure
- Some 5xx errors

Usually not worth retrying:
- 400
- 401
- 403
- 404

Good retry strategy:

```text
Limited retries
      +
Exponential backoff
      +
Jitter
```

Why jitter?

> Prevent many clients from retrying at exactly the same time.

## 8. Exception Handling

```python
try:
    result = await get_orders()
except asyncio.TimeoutError:
    # handle timeout
    ...
```

Avoid blindly swallowing all exceptions.

### `gather()` failures

By default:

```python
await asyncio.gather(...)
```

propagates an exception from a failing awaitable.

Important:

> If one child raises, `gather()` does **not automatically cancel the other awaitables** merely because one failed.

For partial results:

```python
results = await asyncio.gather(
    get_user(),
    get_orders(),
    get_recommendations(),
    return_exceptions=True
)
```

Then inspect individual results.

**Important:** Partial failure handling is a business/design decision.

## 9. Cancellation

A task can be cancelled:

```python
task.cancel()
```

Cancellation requests that the coroutine stop.

Use `finally` for cleanup:

```python
async def work():
    try:
        return await do_work()
    finally:
        await cleanup()
```

Do not accidentally swallow `CancelledError`.

Cancellation matters when a client disconnects or work is no longer needed.

## 10. Critical vs Optional Dependencies

Example:

```text
User Service             → Critical
Orders Service           → Critical
Recommendations Service  → Optional
```

If Recommendations fails:

```text
Return partial response
```

If Orders fails:

```text
Possibly fail the request
```

**First decide business criticality, then choose the technical handling.**

## 11. FastAPI Connection

Good:

```python
@app.get("/dashboard")
async def dashboard():
    user, orders, recommendations = await asyncio.gather(
        get_user(),
        get_orders(),
        get_recommendations()
    )

    return {
        "user": user,
        "orders": orders,
        "recommendations": recommendations
    }
```

This works well when downstream calls are independent, I/O-bound, and async-compatible.

Bad:

```python
@app.get("/dashboard")
async def dashboard():
    time.sleep(5)
```

`async def` does **not** automatically make blocking code asynchronous.

## 12. SDM-Level Mental Model

```text
          FastAPI
             ↓
      Independent calls
             ↓
      asyncio.gather()
             ↓
    ┌────────┼─────────┐
    ↓        ↓         ↓
   User    Orders    Reco
    ↓        ↓         ↓
 timeout  timeout   timeout
    ↓        ↓         ↓
 retry?   retry?    fallback?
    ↓        ↓         ↓
 success  success   optional
```

Think about:
- Concurrency
- Timeouts
- Retry policy
- Backoff + jitter
- Exception handling
- Cancellation
- Critical vs optional dependencies
- Resource cleanup
- Observability
- Downstream capacity

## 13. Interview Quick Answers

**Does async make CPU-bound Python faster?**  
→ No. Async is primarily useful for I/O-bound work.

**Does `async def` automatically make code non-blocking?**  
→ No. Blocking calls inside `async def` can still block the event loop.

**When use `gather()`?**  
→ Independent async operations where you want their results concurrently.

**When use `create_task()`?**  
→ When you want to schedule/manage an individual coroutine as a task.

**Why use `to_thread()`?**  
→ To run unavoidable blocking synchronous work without blocking the event-loop thread.

**Why timeout?**  
→ Prevent indefinite waiting and protect service resources.

**Why retry?**  
→ Recover from transient failures.

**Why exponential backoff + jitter?**  
→ Reduce retry storms and give an unhealthy dependency time to recover.

**What if one `gather()` operation fails?**  
→ By default, its exception propagates; other awaitables aren't automatically cancelled merely because one failed.

**What if the client disconnects?**  
→ Cancellation may propagate; unnecessary work should be cancelled and resources cleaned up.

## Final Mental Model

```text
async def
   ↓
Coroutine
   ↓
await / Task
   ↓
Event Loop
   ↓
Efficient I/O concurrency

Production:
Timeout → Retry → Backoff/Jitter
              ↓
        Exception/Fallback
              ↓
          Cancellation
              ↓
           Cleanup
```

### Status

**Python Async → 🟢 Interview Ready**
