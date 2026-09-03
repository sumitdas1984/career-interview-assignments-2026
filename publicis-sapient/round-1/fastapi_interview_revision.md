# FastAPI — Interview Revision

## 1. What is FastAPI?
Python web framework for building APIs with:
- Async / await
- Request validation
- Dependency injection
- Automatic OpenAPI documentation
- Middleware
- Type hints

## 2. Routing
Maps HTTP method + URL to an endpoint.

```python
@app.get("/users/{id}")
async def get_user(id: int):
    return {"id": id}
```

`GET /users/10 → get_user()`

**Interview:** Routing maps incoming requests to the appropriate endpoint.

## 3. Request Validation
FastAPI uses **Pydantic** models.

```python
class User(BaseModel):
    name: str
    age: int

@app.post("/users")
async def create_user(user: User):
    return user
```

Invalid input is rejected before endpoint logic executes.

## 4. Dependency Injection
The endpoint declares what it needs; FastAPI provides it.

```python
def get_db():
    return create_db_connection()

@app.get("/users")
async def get_users(db = Depends(get_db)):
    return db.get_users()
```

Common uses: DB sessions, authentication/authorization, configuration, shared logic.

**Benefits:** reuse, separation of concerns, testability.

## 5. OpenAPI Documentation
FastAPI automatically generates an OpenAPI specification from routes, parameters, type hints, and Pydantic models.

```text
/docs  → Swagger UI
/redoc → ReDoc
```

**Interview:** Documentation stays aligned with the API definition.

## 6. Middleware
Runs around request/response processing.

```text
Request → Middleware → Endpoint → Middleware → Response
```

Uses: logging, CORS, authentication, timing, headers.

## 7. Async Support
FastAPI supports `async def` and `await`.

```python
@app.get("/users")
async def get_users():
    users = await database.fetch_users()
    return users
```

Useful for I/O-bound work such as HTTP, DB, Redis, and external APIs.

**Important:** `async def` does not automatically make blocking code non-blocking.

```python
async def bad():
    time.sleep(5)  # blocks event loop
```

## 8. Request Flow

```text
Client
  ↓
Middleware
  ↓
Routing
  ↓
Validation
  ↓
Dependency Injection
  ↓
Endpoint
  ↓
Response
```

## 9. Async Interview Points

Independent I/O:

```python
results = await asyncio.gather(
    get_user(),
    get_orders(),
    get_recommendations()
)
```

Blocking library with no async alternative:

```python
result = await asyncio.to_thread(blocking_function)
```

Production considerations:
- Timeouts
- Limited retries
- Exponential backoff + jitter
- Exception handling
- Cancellation
- Fallbacks
- Critical vs optional dependencies
- Observability

## 10. Common Questions

**Why FastAPI?**  
→ Lightweight, API-focused, type hints, validation, automatic docs, dependency injection, strong async support.

**Does FastAPI automatically make code async?**  
→ No. Blocking operations inside `async def` can block the event loop.

**When use async?**  
→ Mainly for I/O-bound workloads with async-compatible libraries.

**What is Dependency Injection?**  
→ The endpoint declares dependencies and FastAPI resolves/provides them.

**What is middleware?**  
→ Code that runs around request/response processing for cross-cutting concerns.

**What is Pydantic used for?**  
→ Data parsing and validation.

**What is OpenAPI?**  
→ A machine-readable API specification used by FastAPI to generate documentation.

## 11. FastAPI vs Full Framework

FastAPI is attractive for:

```text
API-centric
+ High I/O concurrency
+ Async workloads
+ Lightweight / flexible architecture
```

A full framework such as Django can be more suitable when an application needs many built-in web-application capabilities.

## Last-Minute Cheat Sheet

```text
FastAPI
  ├── Routing       → URL → endpoint
  ├── Validation    → Pydantic
  ├── DI            → Depends()
  ├── OpenAPI       → /docs, /redoc
  ├── Middleware    → request/response processing
  └── Async         → async/await for I/O concurrency

Async:
  independent I/O → gather()
  blocking code   → to_thread()
  production      → timeout + retry + backoff + fallback
```

### Status
**FastAPI → 🟢 Interview Ready**
