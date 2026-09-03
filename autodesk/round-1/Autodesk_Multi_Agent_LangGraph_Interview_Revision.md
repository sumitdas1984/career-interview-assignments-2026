# Autodesk — Multi-Agent LangGraph Interview Revision

## 1. Core Mental Model

A multi-agent system uses multiple specialized agents that collaborate to complete a task.

**LangGraph mental mapping**
- Agent → Node
- State → Shared information/context
- Edge → Next step
- Conditional Edge → Dynamic routing
- Parallel branches → Concurrent execution
- Checkpoint → Saved execution state
- Interrupt → Human-in-the-loop pause

**Principal principle:** Start with the workflow and dependencies—not the framework.

---

# 2. Seven Main Patterns

## 2.1 Supervisor

**Idea:** One central agent acts as a manager and decides which specialized agent should work next.

**Example:** Supervisor → Research Agent / Finance Agent / Writer Agent

**Best for:** Dynamic routing and centralized coordination.

**Pros:** Centralized control, clear responsibilities.

**Cons:** Supervisor bottleneck, extra LLM calls, routing errors.

**Interview one-liner:**  
> “A central agent orchestrates specialized agents and decides which agent should execute next based on the current state.”

---

## 2.2 Sequential

**Idea:** Agents execute one after another.

`Agent A → Agent B → Agent C`

**Example:** Document Extraction → Analysis → Summary.

**Best for:** Clear dependencies and deterministic workflows.

**Pros:** Simple, predictable, easy to debug.

**Cons:** Latency accumulates; one slow step delays everything downstream.

**Interview one-liner:**  
> “Sequential orchestration is appropriate when there are explicit dependencies between stages.”

---

## 2.3 Parallel

**Idea:** Independent agents execute simultaneously and their results are combined.

```text
          → Agent A →
Task  →   → Agent B → Aggregator
          → Agent C →
```

**Example:** Finance + Market Research + Competitor Analysis → Final Report.

**Best for:** Independent tasks where latency matters.

**Pros:** Lower latency, good resource utilization.

**Cons:** Concurrency, aggregation, timeouts, and partial-failure handling become important.

**Interview one-liner:**  
> “If tasks are independent, I would execute them in parallel and aggregate the results.”

---

## 2.4 Planner–Executor

**Idea:** A planner creates a plan; executor agents perform the planned tasks.

`User Task → Planner → Plan → Executors → Result`

**Example:** Trip planner creates tasks for flights, hotel, transport, and itinerary.

**Best for:** Complex tasks where steps are not known upfront.

**Key distinction:**
- Planner = **what needs to happen**
- Executor = **perform the assigned task**

**Pros:** Handles complex, dynamic workflows.

**Cons:** Bad plans, extra LLM calls, higher latency/cost. Plans should be validated.

**Interview one-liner:**  
> “Planner–executor is useful when the task is complex and the sequence of work needs to be determined dynamically.”

---

## 2.5 Peer-to-Peer

**Idea:** Agents communicate directly without a central supervisor.

`Requirements ↔ Architecture ↔ Coding ↔ Testing`

**Best for:** Decentralized collaboration.

**Pros:** Flexible, no central coordinator bottleneck.

**Cons:** Harder debugging/observability, possible loops, harder governance and cost control.

**Interview one-liner:**  
> “Peer-to-peer orchestration enables direct agent collaboration but increases coordination and observability complexity.”

---

## 2.6 Critic–Reviewer

**Idea:** One agent generates an output; another independently reviews or improves it.

`Generator → Critic → Improved Result`

**Examples:**
- Coding Agent → Code Review Agent
- RAG QA Agent → Fact-check Agent

**Best for:** Quality-critical tasks.

**Pros:** Better validation, catches errors/hallucinations.

**Cons:** Extra inference cost and latency.

**Interview one-liner:**  
> “I introduce a critic when the cost of an incorrect output justifies additional inference for independent validation.”

---

## 2.7 Human-in-the-Loop (HITL)

**Idea:** Agent works autonomously until a critical/high-risk step, then pauses for human approval.

`Agent → Critical Action → Human Approval → Resume`

**Examples:** Financial transaction, production deployment, legal decision, deleting important data.

**Important:** HITL does not mean the human performs the entire workflow. Human intervention happens at predefined risk points.

**LangGraph connection:** Interrupt/pause → human review → approve/reject → resume.

**Best for:** High-risk, sensitive, irreversible, or compliance-sensitive actions.

**Interview one-liner:**  
> “I keep the agent autonomous for routine work, but introduce human approval at high-risk or irreversible decision points.”

---

# 3. Quick Comparison

| Pattern | Core Idea | Best For |
|---|---|---|
| Supervisor | Manager assigns work | Dynamic centralized routing |
| Sequential | A → B → C | Fixed dependencies |
| Parallel | A + B + C | Independent tasks |
| Planner–Executor | Plan → Execute | Complex dynamic tasks |
| Peer-to-Peer | Direct collaboration | Decentralized collaboration |
| Critic–Reviewer | Generate → Review | Quality-critical output |
| HITL | Agent → Human → Resume | High-risk decisions |

---

# 4. How to Choose

Start with the **workflow**:

- Deterministic dependencies → **Sequential**
- Independent tasks → **Parallel**
- Dynamic centralized routing → **Supervisor**
- Unknown/complex steps → **Planner–Executor**
- Decentralized collaboration → **Peer-to-Peer**
- Quality is critical → add **Critic–Reviewer**
- High-risk/irreversible action → add **HITL**

---

# 5. Patterns Can Be Combined

These patterns are **not mutually exclusive**.

A production system could be:

`Supervisor → Planner → Parallel Executors → Critic → Human Approval → Final Result`

**Principal-level point:**  
> “I treat these as architectural building blocks. A production agentic system can combine them based on task dependencies, autonomy requirements, quality, and risk.”

---

# 6. Common Interview Questions

### Supervisor vs Planner–Executor
> “A supervisor decides which specialized agent should work next. A planner creates an explicit plan or sequence of tasks that executors perform.”

### Sequential vs Parallel
> “Sequential is for dependent tasks; parallel is for independent tasks where reducing latency is important.”

### Supervisor vs Peer-to-Peer
> “Supervisor centralizes orchestration through a manager. Peer-to-peer removes that central coordinator and allows direct agent collaboration.”

### Why use a Critic?
> “To independently validate correctness, safety, or quality when the benefit justifies extra latency and cost.”

### Why use HITL?
> “When the agent reaches a high-risk, sensitive, or irreversible action requiring human judgment or approval.”

### How would you choose an architecture?
> “I first analyze workflow dependencies. I use sequential for deterministic dependencies, parallel for independent tasks, supervisor for dynamic routing, and planner–executor when the steps are unknown upfront. I add critics for quality-critical outputs and HITL for high-risk actions. I then optimize for reliability, latency, cost, observability, and security.”

---

# 7. Principal-Level Trade-offs

Always consider:

- **Latency** — Number of sequential LLM calls
- **Cost** — Number of agents/inference calls
- **Reliability** — Agent/tool failure handling
- **Scalability** — Independent scaling
- **Observability** — End-to-end tracing
- **State** — Shared/durable state management
- **Security** — Agent/tool permissions
- **Guardrails** — Constrain agent behavior
- **Human oversight** — Approval boundaries
- **Idempotency** — Safe retries
- **Timeouts** — Slow agent/tool handling
- **Fallbacks** — Model/tool failure strategy
- **Loop control** — Prevent runaway agent interactions

---

# 8. LangGraph Mental Model

Think of LangGraph as a **stateful workflow/agent orchestration graph**.

```text
              State
                |
              Agent
             (Node)
                |
              Edge
                |
          Next Action
```

**Parallel:**
```text
              → Agent A →
Task ─────────→ Agent B → Aggregator
              → Agent C →
```

**HITL:**
```text
Agent → Critical Step → INTERRUPT
                           |
                     Human Review
                      /       \
                  Reject      Approve
                               |
                             Resume
```

---

# 9. 5-Minute Final Drill

Be able to answer instantly:

1. **Supervisor?** Central agent dynamically routes work.
2. **Sequential?** Dependent tasks execute one after another.
3. **Parallel?** Independent tasks execute concurrently.
4. **Planner–Executor?** Planner creates the plan; executors perform it.
5. **Peer-to-Peer?** Agents collaborate directly without a central supervisor.
6. **Critic–Reviewer?** One generates; another validates/improves.
7. **HITL?** Agent pauses for human approval at critical points.
8. **How choose?** Dependencies + autonomy + quality + risk + latency + cost.
9. **Principal mindset?** Choose the simplest architecture that provides the required autonomy and reliability.

---

# 10. One Sentence to Remember

> **“Choose orchestration based on workflow dependencies and risk: sequential for dependent work, parallel for independent work, supervisor for dynamic routing, planner–executor for dynamic plans, peer-to-peer for decentralized collaboration, critic for quality, and HITL for high-risk decisions.”**
