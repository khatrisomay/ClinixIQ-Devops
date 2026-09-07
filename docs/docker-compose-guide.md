# ClinixIQ Docker Compose & Container Orchestration Guide

## 🐳 Architecture Overview

The local development environment uses Docker Compose to orchestrate three core microservices within an isolated bridge network (`clinixiq-network`):

```
                       [ Client / Web Browser ]
                                   │
                                   ▼
                   ┌───────────────────────────────┐
                   │    Nginx Gateway (Port 80)    │  (Production Mode)
                   └───────────────┬───────────────┘
                                   │
                   ┌───────────────┴───────────────┐
                   ▼                               ▼
       ┌──────────────────────┐        ┌──────────────────────┐
       │   React Frontend     │        │    FastAPI Backend   │
       │     (Port 3000)      │        │     (Port 8000)      │
       └──────────────────────┘        └───────────┬──────────┘
                                                   │
                                                   ▼
                                       ┌──────────────────────┐
                                       │   Redis 7.2 Cache    │
                                       │     (Port 6379)      │
                                       └──────────────────────┘
```

---

## 🚀 Quickstart Commands

### 1. Launch the Development Stack
```bash
# Clone and enter the repository
cd ClinixIQ-Devops

# Launch services in background
docker compose up -d

# Verify health status
docker compose ps
```

### 2. Service Endpoints
- **React Frontend**: [http://localhost:3000](http://localhost:3000)
- **FastAPI API & Swagger UI**: [http://localhost:8000/docs](http://localhost:8000/docs)
- **Kubernetes Liveness Probe**: [http://localhost:8000/healthz](http://localhost:8000/healthz)
- **Kubernetes Readiness Probe**: [http://localhost:8000/readyz](http://localhost:8000/readyz)

---

## 🔒 Security & Optimization Features
1. **Multi-Stage Builds**:
   - `frontend/Dockerfile`: Node 20 builder stage $\to$ Nginx unprivileged Alpine runtime.
   - `backend/Dockerfile`: Debian 12 builder stage $\to$ non-root `appuser` (UID 10001).
2. **Healthchecks**: Built-in container healthchecks guarantee that dependencies (Redis $\to$ Backend $\to$ Frontend) start in strict sequence.
3. **Resource Reservations**: Configured CPU and Memory limits prevent container runaway in production.
