# Credit Acceptance — Technical Screen Preparation Tracker

**Target:** Technical Screen | Sept 7–11, 2026  
**Role:** Staff Machine Learning Engineer | Advanced Analytics

## Interview Signal

> **Primary focus: Applied ML + problem solving + system design + whiteboarding.**
>
> Advanced Analytics uses **Traditional ML + DL + GenAI depending on the business problem**. Strong traditional ML knowledge is important.

### Format
- [ ] Project deep dive
- [ ] ML problem solving
- [ ] Transformer / NLP
- [ ] AI / GenAI
- [ ] System design
- [ ] Whiteboard business problem
- [ ] No formal coding round

---

# 1. Priority Map

| Area | Priority | Done |
|---|---|---|
| Traditional ML | 🔴 Very High | ☐ |
| ML problem formulation | 🔴 Very High | ☐ |
| ML System Design | 🔴 Very High | ☐ |
| Causal inference | 🔴 Very High | ☐ |
| DL fundamentals | 🟠 High | ☐ |
| Transformer / NLP | 🟠 High | ☐ |
| GenAI / RAG / Agents | 🟠 High | ☐ |
| Evaluation / MLOps | 🟠 High | ☐ |
| Coding / LeetCode | 🟢 Low | ☐ |

---

# 2. Traditional ML

### Models
- [ ] Linear / Logistic Regression
- [ ] Decision Trees
- [ ] Random Forest
- [ ] Gradient Boosting / XGBoost
- [ ] Bias–variance
- [ ] Overfitting / underfitting
- [ ] Regularization — L1 / L2
- [ ] Feature engineering
- [ ] Data leakage
- [ ] Class imbalance

### Evaluation
- [ ] Precision / Recall / F1
- [ ] ROC-AUC vs PR-AUC
- [ ] Threshold selection
- [ ] Business-driven metrics

### Be able to explain
- [ ] XGBoost vs Logistic Regression
- [ ] XGBoost vs Random Forest
- [ ] Handling imbalanced data
- [ ] Preventing leakage
- [ ] Model interpretability
- [ ] Choosing the right metric

---

# 3. Applied ML / Business Problem Solving

### Core framework

```text
Business problem
      ↓
Clarify objective / target
      ↓
Understand + validate data
      ↓
Baseline
      ↓
Feature engineering
      ↓
Choose approach
      ↓
Evaluate
      ↓
Business impact
      ↓
Production + monitoring
```

### Practice
- [ ] Customer churn prediction
- [ ] Dealer / distributor churn
- [ ] Churn spike investigation
- [ ] Business KPI decline
- [ ] Customer behavior prediction
- [ ] Anomaly detection
- [ ] Segmentation
- [ ] Recommendation / intervention

**Key rule:** Don't jump straight to a model. First understand the business problem.

---

# 4. Causal Inference — Must Prepare

### Distinguish

**Prediction:** Who will churn?  
**Causality:** What caused churn?  
**Intervention:** What can reduce churn?

### Concepts
- [ ] Correlation vs causation
- [ ] Confounders
- [ ] Treatment / control
- [ ] Counterfactual
- [ ] Selection bias
- [ ] Treatment effect
- [ ] A/B testing
- [ ] ATE / CATE
- [ ] Propensity scores
- [ ] Difference-in-Differences
- [ ] Causal DAGs — conceptual
- [ ] Uplift / treatment-effect modeling

### Practice
> Churn increased 15%. How would you determine the cause and identify an effective mitigation?

---

# 5. Spike / Anomaly Analysis

### Prepare
- [ ] Trend vs seasonality
- [ ] Moving averages
- [ ] Baselines
- [ ] Anomaly detection
- [ ] Change-point detection
- [ ] Forecasting basics
- [ ] Root-cause analysis

### Practice
> Loan applications suddenly dropped 20%. How would you investigate?

```text
Detect → Validate data → When? → Where? → Who?
→ What changed? → Hypotheses → Statistical validation
→ Causal investigation → Mitigation
```

---

# 6. ML System Design — Must Prepare

### Generic architecture

```text
Data Sources
     ↓
Ingestion
     ↓
Feature Engineering / Feature Store
     ↓
Training Pipeline
     ↓
Model Registry
     ↓
Deployment
     ↓
Prediction Service
     ↓
Business Application
     ↓
Monitoring
```

### Discuss
- [ ] Batch vs real-time
- [ ] Feature freshness
- [ ] Training frequency
- [ ] Model versioning
- [ ] Data / model drift
- [ ] Retraining
- [ ] Explainability
- [ ] Latency
- [ ] Scalability
- [ ] Cost
- [ ] Security
- [ ] Observability

### Practice designs
- [ ] Customer churn system
- [ ] Dealer churn system
- [ ] Anomaly detection
- [ ] Recommendation system
- [ ] Real-time ML inference
- [ ] ML platform

---

# 7. Deep Learning

Keep it practical.
- [ ] Neural-network basics
- [ ] Forward / backpropagation
- [ ] Gradient descent
- [ ] Loss functions
- [ ] Overfitting
- [ ] Dropout
- [ ] Batch normalization
- [ ] CNN — conceptual
- [ ] RNN / LSTM — conceptual
- [ ] Transformers — deeper

### Practice
> When would you choose DL over traditional ML? When would DL be unnecessary?

---

# 8. Transformer / NLP

### Transformer
- [ ] Tokenization
- [ ] Embeddings
- [ ] Positional encoding
- [ ] Self-attention
- [ ] Query / Key / Value
- [ ] Multi-head attention
- [ ] Encoder vs Decoder
- [ ] Context window

### Models
- [ ] BERT
- [ ] GPT
- [ ] BART
- [ ] Pretraining vs fine-tuning

### NLP
- [ ] Classification
- [ ] NER
- [ ] Semantic similarity
- [ ] Embeddings
- [ ] Summarization
- [ ] Information extraction
- [ ] Document QA

**My strongest real-world example:** BART summarization + transformer NLP + LLM fine-tuning at Thomson Reuters.

---

# 9. GenAI

## RAG
- [ ] Chunking
- [ ] Embeddings
- [ ] Vector search
- [ ] Hybrid retrieval
- [ ] Reranking
- [ ] Query expansion
- [ ] Contextual compression
- [ ] Groundedness
- [ ] RAG evaluation
- [ ] Hallucination mitigation

## Agents
- [ ] Agent vs deterministic workflow
- [ ] Multi-agent architecture
- [ ] Routing
- [ ] State management
- [ ] Tool use
- [ ] Evaluation
- [ ] Failure handling

## Fine-tuning
- [ ] PEFT
- [ ] LoRA
- [ ] QLoRA
- [ ] RAG vs fine-tuning
- [ ] Evaluation

---

# 10. Choosing the Right Approach

```text
Structured prediction       → Traditional ML
Complex patterns / data     → DL
Text understanding          → Transformer / LLM
Private / changing knowledge→ RAG
Domain adaptation           → Fine-tuning
"What caused this?"         → Causal inference
"What intervention works?" → Treatment effect / uplift
Complex multi-step workflow → Agent / GenAI
```

For every choice, explain **why** using:
- Accuracy
- Data availability
- Explainability
- Latency
- Cost
- Complexity
- Maintainability
- Business impact

---

# 11. Probable Whiteboard Problems

### 🔴 Highest probability
- [ ] Customer churn prediction
- [ ] Dealer / distributor churn
- [ ] Churn spike investigation
- [ ] Business KPI decline / root cause
- [ ] ML system for churn
- [ ] Intervention effectiveness

### 🟠 Medium probability
- [ ] Customer segmentation
- [ ] Recommendation
- [ ] Anomaly detection
- [ ] Enterprise GenAI assistant
- [ ] ML + GenAI hybrid solution

---

# 12. One Hybrid Problem to Master

> Some customers are likely to churn. Build an AI system to identify them and recommend what Credit Acceptance should do.

```text
Customer data
     ↓
Churn prediction
     ↓
High-risk customers
     ↓
Causal / uplift analysis
     ↓
Best intervention
     ↓
Recommendation
     ↓
GenAI explanation / assistant
     ↓
Business user
```

Demonstrates: **ML + causal inference + GenAI + system design + business thinking**

---

# 13. Project Deep Dives

## Bosch — MiDAS
- [ ] Business problem
- [ ] Architecture
- [ ] My contribution
- [ ] GenAI components
- [ ] LLMOps / Langfuse
- [ ] RAG
- [ ] Design decisions / trade-offs
- [ ] Challenges
- [ ] Production considerations
- [ ] ~$650K projected annual impact

## Thomson Reuters — Conversational AI
- [ ] Business problem
- [ ] Document QA / RAG
- [ ] Summarization
- [ ] LLM architecture
- [ ] Evaluation
- [ ] Productionization
- [ ] ~$100K projected annual impact

## Thomson Reuters — LLM Fine-tuning
- [ ] Why fine-tuning?
- [ ] Dataset
- [ ] Unsloth
- [ ] LoRA / QLoRA / PEFT
- [ ] Evaluation
- [ ] Deployment

## Manhattan — Traditional ML
- [ ] Shipment ETA prediction
- [ ] Random Forest / XGBoost
- [ ] Features
- [ ] Evaluation
- [ ] Batch vs real-time
- [ ] Production architecture

---

# 14. Whiteboard Answer Framework

1. **Clarify business objective**
2. **Define target + success metric**
3. **Understand data**
4. **Establish baseline**
5. **Choose ML / DL / GenAI / causal approach**
6. **Explain why**
7. **Evaluate**
8. **Consider causal analysis**
9. **Design production architecture**
10. **Monitoring / feedback loop**
11. **Business impact**

---

# 15. Preparation Roadmap

## Phase 1 — ML Foundation
- [ ] ML fundamentals
- [ ] XGBoost
- [ ] Evaluation
- [ ] DL basics
- [ ] Transformer / NLP

## Phase 2 — Applied ML
- [ ] Churn
- [ ] Spike / anomaly
- [ ] Root-cause analysis
- [ ] Causal inference
- [ ] Experimentation
- [ ] Uplift modeling

## Phase 3 — Architecture
- [ ] ML system design
- [ ] Production inference
- [ ] MLOps
- [ ] Monitoring
- [ ] Trade-offs

## Phase 4 — GenAI
- [ ] RAG
- [ ] Agents
- [ ] Fine-tuning
- [ ] Evaluation
- [ ] LLMOps

## Phase 5 — Final Practice
- [ ] 5–10 whiteboard problems
- [ ] 2–3 project deep dives
- [ ] Mock technical interview
- [ ] Review weak areas
- [ ] Practice concise explanations

---

# 16. Final Mental Model

> **Business problem → formulate → choose Traditional ML / DL / GenAI / causal approach → design → evaluate → productionize → measure business impact.**

### The interview is NOT primarily:
> "Show me how much GenAI terminology you know."

### It is more likely:
> **"Here's a business problem. How would you think about it, solve it, and build it?"**
