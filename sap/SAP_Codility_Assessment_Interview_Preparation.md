# SAP Codility Assessment — Interview Prep

## Task 1 — Giant Slalom / Gate Problem

### High-level approach
- Process the gates sequentially from top to bottom.
- Maintain the required state while traversing instead of repeatedly scanning the input.
- Avoid unnecessary nested loops.

**Complexity:** `O(N)` time; `O(1)` or small auxiliary space depending on the required state.

### Interview answer
> "I processed the gates sequentially and maintained the relevant state during traversal, avoiding repeated comparisons and keeping the solution linear."

### Discuss edge cases
- Minimum/empty input if allowed
- One gate
- Already-valid ordering
- Duplicate/equal positions if allowed
- Boundary positions

---

# Task 2 — Smart Support Router

## Requirement

This was a **two-stage LangChain workflow**, not just classification.

```text
Email
  ↓
1. Classification
  ↓
category + confidence
  ↓
RunnableBranch
  ├── Technical Support
  ├── Billing
  └── General Feedback
          ↓
     Department LLM
          ↓
    routed_response
```

Function:

```python
def classify_and_route_email(
    email_content: str,
    mock_llm_func
) -> EmailClassification:
```

## Output

```python
class EmailClassification(BaseModel):
    category: Literal[
        "Technical Support",
        "Billing",
        "General Feedback"
    ]
    confidence: float
    routed_response: str
```

During classification, `routed_response` must initially be `""`.

---

## Step 1 — Classification

Required:

- `PromptTemplate`
- `PydanticOutputParser`
- `RunnableLambda`

Classification prompt must:

1. contain **"classify"**
2. include the email
3. include:

```python
parser.get_format_instructions()
```

Conceptually:

```text
Classify this customer email.

Email:
{email_content}

Return:
{format_instructions}
```

First LLM call returns:

```python
EmailClassification(
    category="Billing",
    confidence=0.9,
    routed_response=""
)
```

---

## Step 2 — Routing & Response

Create department-specific chains.

### Technical Support
Prompt contains:

```text
You are a technical support specialist
```

### Billing
Prompt contains:

```text
You are a billing specialist
```

### General Feedback
Prompt contains:

```text
You are a customer service representative
```

Each prompt includes the original email.

Use `RunnableBranch` to select the chain based on `classification.category`.

Use `RunnableLambda` to wrap normal Python/LLM functions as LangChain runnables.

Second LLM call generates the department response.

Then:

```python
classification.routed_response = department_response
return classification
```

---

## LangChain Components

| Component | Purpose |
|---|---|
| `PromptTemplate` | Build structured prompts |
| `PydanticOutputParser` | Parse/validate LLM output |
| `RunnableLambda` | Wrap Python functions as runnables |
| `RunnableBranch` | Category-based routing |
| `BaseModel` | Structured validated result |

**Important:** The assessment explicitly required these instead of manual `if/elif/else` routing or manual string parsing.

---

## 30-Second Answer

> "Task 2 was a two-stage LangChain pipeline. First, I used a PromptTemplate and PydanticOutputParser to classify the email into Technical Support, Billing, or General Feedback and get a confidence score. Then I used RunnableBranch to route the classification to the appropriate department chain. That chain called the mock LLM again to generate the response, which I stored in routed_response before returning the final EmailClassification."

---

## Likely Questions

**Why PydanticOutputParser?**  
Structured, validated output instead of manually parsing an LLM string.

**Why is `routed_response` initially empty?**  
Classification and response generation are separate stages.

**Why RunnableBranch?**  
It makes category routing part of the LangChain pipeline rather than manual conditionals.

**Why RunnableLambda?**  
It adapts normal Python/LLM functions into LangChain Runnable components.

**How many LLM calls?**  
Two: classification + department response.

**Refund?** → Billing  
**Crash/error?** → Technical Support  
**Suggestion/compliment?** → General Feedback

---

## Production Improvements

If asked what you would improve:

- Confidence threshold + human fallback
- Structured-output/retry handling
- LLM evaluation dataset
- Prompt/version management
- Observability and tracing
- Latency/error monitoring
- Async processing
- PII/security controls
- Retry/dead-letter handling

---

# Final 8-Point Revision

- [ ] Task 1 → sequential processing
- [ ] Task 1 → complexity + edge cases
- [ ] Task 2 → **two LLM calls**
- [ ] Classification → `PromptTemplate` + `PydanticOutputParser`
- [ ] Functions → `RunnableLambda`
- [ ] Routing → `RunnableBranch`
- [ ] Final object → `category + confidence + routed_response`
- [ ] Explain **why** each LangChain component is used

## Mental Model

```text
Email
  ↓
LLM #1
  ↓
Classification
(category, confidence)
  ↓
RunnableBranch
  ↓
Department Chain
  ↓
LLM #2
  ↓
routed_response
  ↓
Final EmailClassification
```
