# Docker + Kubernetes — Interview Revision

## 1. Docker → Kubernetes: Why?

Docker and Kubernetes solve different problems.

### Docker

Docker helps package and run an application as a container:

```text
FastAPI Code
     ↓
Docker Image
     ↓
Container
```

Good for running individual/containerized applications.

### The production problem

Imagine:

```text
FastAPI
 ├── Container 1
 ├── Container 2
 ├── Container 3
 └── ... 50 containers
```

Now we need to handle:

- Container failures/restarts
- Scaling
- Traffic distribution
- Deploying new versions
- Health management
- Running many application instances

### Kubernetes

Kubernetes is a **container orchestration platform**.

> **Docker → Containerization**  
> **Kubernetes → Orchestration and management of containers at scale**

Think:

```text
Docker:
"Run my application."

Kubernetes:
"Run and manage my application reliably at scale."
```

Kubernetes does not simply replace Docker; it manages containerized applications.

---

# 2. Ingress

Ingress is an **external HTTP/HTTPS routing layer** in Kubernetes.

Instead of exposing every service directly:

```text
Internet
   ↓
User Service
Order Service
Payment Service
```

use:

```text
                    Internet
                       ↓
                    Ingress
                 /      |                       ↓       ↓        ↓
             User     Order    Payment
            Service   Service   Service
```

The Ingress looks at the incoming request and routes it to the appropriate Kubernetes Service.

Example:

```text
api.company.com/users
        ↓
      Ingress
        ↓
    User Service
```

```text
api.company.com/orders
        ↓
      Ingress
        ↓
    Order Service
```

### Common responsibilities

- External HTTP/HTTPS routing
- Host/path-based routing
- TLS/HTTPS termination

### Important distinction

```text
Internet
   ↓
Ingress       → external traffic routing
   ↓
Service       → stable access to Pods
   ↓
Pods
```

---

# 3. Helm

Helm is a **package manager / templating tool for Kubernetes**.

Without Helm, an application may have multiple Kubernetes configuration files:

```text
deployment.yaml
service.yaml
configmap.yaml
ingress.yaml
secret.yaml
```

Managing these separately across environments can become repetitive.

Helm packages Kubernetes resources into a **Chart**:

```text
                Helm Chart
                    │
        ┌───────────┼───────────┐
        ↓           ↓           ↓
   Deployment    Service     Ingress
```

The same Chart can be reused with different configuration for:

```text
Development
Staging
Production
```

### Simple analogy

```text
Kubernetes YAML files = ingredients

Helm Chart = packaged recipe
```

### Helm vs Kubernetes

> **Kubernetes runs and manages the application.**

> **Helm packages, templates, and helps deploy/manage Kubernetes resources.**

Helm does not replace Kubernetes.

---

# 4. How They Fit Together

For a FastAPI application:

```text
Developer
    ↓
   Git
    ↓
 Docker Image
    ↓
  Registry
    ↓
   Helm
    ↓
Kubernetes Cluster
    ↓
Deployment
    ↓
  Pods
    ↓
 Service
    ↑
 Ingress
    ↑
Internet
```

Remember the responsibilities:

| Technology | Main purpose |
|---|---|
| **Docker** | Package/run application as containers |
| **Kubernetes** | Manage containers at scale |
| **Deployment** | Manage Pods/replicas |
| **Service** | Stable endpoint for Pods |
| **Ingress** | External HTTP/HTTPS routing |
| **Helm** | Package/template/deploy Kubernetes resources |

---

# 5. Interview Quick Answers

### Why Kubernetes if we already have Docker?

> "Docker solves containerization, but once we have many containers in production, we need orchestration—health management, scaling, service discovery, traffic routing, and rolling deployments. Kubernetes provides these capabilities."

### What is Ingress?

> "Ingress is an external HTTP/HTTPS routing layer in Kubernetes. It routes incoming requests to the appropriate Kubernetes Service based on things such as host or path."

### What is Helm?

> "Helm is a package and templating tool for Kubernetes. It lets us package resources such as Deployments, Services and Ingress into reusable Charts and manage environment-specific configuration."

---

# Last-Minute Mental Model

```text
Docker
  ↓
Container

Kubernetes
  ↓
Manage containers
  ↓
Deployment → Pods
  ↓
Service → stable access
  ↓
Ingress → external routing

Helm
  ↓
Package/template Kubernetes resources
```

### Status

**Docker + Kubernetes → 🟢 Interview Ready**
