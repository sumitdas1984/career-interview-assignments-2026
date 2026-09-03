# CI/CD with GitHub Actions — Interview Revision

## 1. CI vs CD

### CI — Continuous Integration

Goal:

> **Whenever code changes, automatically verify that the change is safe to merge.**

Typical flow:

```text
Developer
   ↓
Git Push / Pull Request
   ↓
GitHub Actions
   ↓
Build
   ↓
Tests
   ↓
Lint / Quality / Security Checks
   ↓
✅ Pass → Merge
❌ Fail  → Fix
```

Key idea:

> **Frequent integration + automated validation.**

---

### CD — Continuous Delivery / Deployment

After CI passes, deliver the application to an environment.

```text
Code
 ↓
CI
 ↓
Docker Image
 ↓
Container Registry
 ↓
Kubernetes / Cloud
```

### Continuous Delivery

Code is automatically prepared for production, but production deployment may require approval.

```text
CI → Staging → Validation → Approval → Production
```

### Continuous Deployment

Every change that passes the pipeline is automatically deployed.

```text
CI → Staging → Validation → Production
```

No manual production approval.

---

# 2. GitHub Actions Mental Model

Remember:

```text
Workflow
   ↓
Jobs
   ↓
Steps
   ↓
Runner
```

- **Workflow** → complete automation pipeline
- **Job** → logical unit of work
- **Step** → individual action/command
- **Runner** → machine/environment executing the job

For interviews, understand the concepts rather than memorizing YAML syntax.

---

# 3. Production Pipeline

For a FastAPI / AI application:

```text
Developer
    ↓
GitHub
    ↓
GitHub Actions
    │
    ├── Unit Tests
    ├── Lint / Quality
    ├── Security Checks
    ↓
Build Docker Image
    ↓
Container Registry
    ↓
Deploy to Kubernetes
    ↓
Staging
    ↓
Health / Smoke Tests
    ↓
Approval*
    ↓
Production
    ↓
Rolling Deployment
    ↓
Monitor
```

`*` Approval depends on whether the organization uses Continuous Delivery or Continuous Deployment.

---

# 4. Docker + Registry + Kubernetes

The important relationship:

```text
GitHub
   ↓
GitHub Actions
   ↓
Docker Image
   ↓
Container Registry
   ↓
Kubernetes
   ↓
Pods
```

### Why push to a registry?

Kubernetes needs access to the application image.

The registry acts as the central place to store/version Docker images.

Use **versioned/immutable image tags**, preferably tied to a commit or release.

Example:

```text
my-api:commit-a82f31
```

This makes deployments traceable and rollback easier.

---

# 5. Deployment Strategy

### Rolling Deployment ⭐

Gradually replace old application instances with the new version.

```text
Before:

v1  v1  v1  v1

During:

v1  v1  v2  v2

After:

v2  v2  v2  v2
```

Benefits:

- Minimal/no downtime
- Gradual rollout
- Old version can continue serving traffic while new version starts

---

# 6. Health Checks

A deployment should not be considered successful just because Kubernetes accepted the new Pods.

Use:

```text
Deploy
  ↓
Health / Smoke Checks
  ↓
Healthy?
 ├── Yes → Continue
 └── No  → Stop / Rollback
```

Health checks and observability are important parts of safe deployment.

---

# 7. Rollback

If the new version causes problems:

```text
v1 → v2
      ↓
    Problem
      ↓
   Rollback
      ↓
v1
```

This is why keeping versioned container images is important.

A good deployment pipeline should make rollback **quick and predictable**.

---

# 8. Environments

A common enterprise flow is:

```text
Development
     ↓
   Staging
     ↓
 Production
```

The same application artifact/image should ideally move through environments rather than rebuilding different images for each environment.

Configuration can vary by environment.

Example:

```text
Development → dev database
Staging     → staging database
Production  → production database
```

---

# 9. Secrets

Never hard-code credentials in source code or workflow files.

Examples:

```text
Database password
API keys
Cloud credentials
Deployment credentials
```

Use appropriate secret management such as:

- GitHub Secrets
- Cloud secret management
- Kubernetes Secrets

The important interview principle:

> **Credentials should be injected securely at runtime rather than stored in source code.**

---

# 10. Failure Handling

Consider failures at each stage:

```text
Tests fail
   ↓
Stop pipeline

Docker build fails
   ↓
Stop deployment

Deployment fails
   ↓
Do not promote

Health check fails
   ↓
Rollback / stop rollout

Production issue
   ↓
Monitor + rollback
```

CI/CD should be a **quality gate**, not just an automated deployment script.

---

# 11. HLD Interview Scenario

### Question

> "A developer pushes code. Walk me through how you would deploy the new version to production."

### Strong answer

> "When the developer pushes code or raises a pull request, GitHub Actions triggers CI. I would check out the code, install dependencies, run unit tests, linting, quality and security checks. If CI passes, I would build a Docker image and push it to a container registry using a versioned tag tied to the commit or release.
>
> For CD, I'd deploy that image to staging and run health or smoke tests. Depending on the organization's process, production deployment can require an approval gate. In production, I'd use a rolling deployment so the new version is gradually introduced while the old version continues serving traffic. I'd monitor the deployment and have a rollback path if health checks or production metrics indicate a problem."

---

# 12. SDM-Level Follow-up Points

If the interviewer probes further:

### "Why GitHub Actions?"

> "It integrates naturally with our GitHub repository and supports automated CI/CD workflows. The important part is the pipeline design; Jenkins and other tools can implement similar stages."

### "Why Docker?"

> "It packages the application and its dependencies into a consistent artifact that can move across environments."

### "Why a container registry?"

> "It provides a centralized, versioned location from which deployment environments can pull application images."

### "Why rolling deployment?"

> "It reduces downtime and allows gradual replacement of the old version."

### "What if deployment fails?"

> "Stop or pause the rollout, investigate using health checks and observability, and rollback to the previous known-good image if necessary."

### "How do you prevent bad code from reaching production?"

> "Use CI as a quality gate: automated tests, linting, security/quality checks, followed by staging validation before production."

---

# 13. Last-Minute Cheat Sheet

```text
CI
→ Build + Test + Quality/Security checks

CD
→ Deliver/deploy validated application

GitHub Actions
→ Workflow → Jobs → Steps → Runner

Pipeline
→ GitHub
→ CI
→ Docker Image
→ Registry
→ Staging
→ Health Checks
→ Production
→ Rolling Deployment
→ Monitor / Rollback

Key practices
→ Versioned images
→ Environment separation
→ Secure secrets
→ Automated quality gates
→ Health checks
→ Observability
→ Fast rollback
```

## Interview Principle

> **A good CI/CD pipeline doesn't just deploy code. It validates the change, produces a traceable artifact, deploys it safely, verifies the deployment, monitors it, and provides a reliable rollback path.**

### Status

**CI/CD + GitHub Actions → 🟢 Interview Ready**
