# ClinixIQ - AI Health Triage & DevOps Platform

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Docker](https://img.shields.io/badge/Docker-Multi--stage-2496ED?logo=docker&logoColor=white)](https://www.docker.com/)
[![Kubernetes](https://img.shields.io/badge/Kubernetes-Orchestration-326CE5?logo=kubernetes&logoColor=white)](https://kubernetes.io/)
[![Jenkins](https://img.shields.io/badge/Jenkins-CI%2FCD-D24939?logo=jenkins&logoColor=white)](https://www.jenkins.io/)
[![React](https://img.shields.io/badge/React-18-61DAFB?logo=react&logoColor=black)](https://react.dev/)
[![FastAPI](https://img.shields.io/badge/FastAPI-Python-009688?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![Redis](https://img.shields.io/badge/Redis-Cache-DC382D?logo=redis&logoColor=white)](https://redis.io/)

**ClinixIQ** is an enterprise-grade, commercial AI-powered symptom triage and disease risk analytics platform. Designed to demonstrate a complete production DevOps lifecycle, ClinixIQ combines interactive clinical NLP triage with Python-generated diagnostic analytics, containerized with Docker, orchestrated via Kubernetes, and continuously delivered via automated Jenkins CI/CD pipelines.

---

## 🏗️ System Architecture

```
[ Client / Browser ] 
       │ (HTTPS / Ingress)
       ▼
[ Nginx Ingress Controller ]
       ├───────────────┬────────────────┐
       ▼               ▼                ▼
[ React Frontend ]  [ FastAPI Backend ] [ Prometheus / Grafana ]
  (Nginx Pods)        (Python Pods)        (Monitoring)
                       │
       ┌───────────────┴───────────────┐
       ▼                               ▼
[ ML Inference Engine ]     [ Redis Caching Layer ]
  (Scikit-Learn/XGBoost)      (Sub-millisecond Session State)
```

---

## 🐳 Local Docker Compose Quickstart

```bash
# Clone the repository
git clone https://github.com/khatrisomay/ClinixIQ-Devops.git
cd ClinixIQ-Devops

# Launch multi-container stack in background
docker compose up -d

# Verify services
docker compose ps
```

- **Frontend**: [http://localhost:3000](http://localhost:3000)
- **Backend API Docs**: [http://localhost:8000/docs](http://localhost:8000/docs)
- **Architecture Guide**: [docs/docker-compose-guide.md](docs/docker-compose-guide.md)

---

## 🛠️ DevOps Tech Stack

- **Containerization**: Multi-stage, non-root Docker builds for React (Vite/Nginx) and Python (FastAPI).
- **Orchestration**: Kubernetes manifests (Deployments, Services, Ingress, Horizontal Pod Autoscaler, ConfigMaps, Secrets).
- **CI/CD**: Declarative Jenkins pipeline with static linting, unit tests, Trivy vulnerability scanning, container registry publishing, and zero-downtime rolling updates.
- **Monitoring**: Prometheus metrics scrapers and Grafana dashboards tracking API latency, pod health, and ML inference duration.

---

## 📅 14-Day Delivery Roadmap
- **Day 1**: React.js Frontend, symptom triage UI, analytics dashboard, SaaS pricing, and Dockerfile. *(Complete)*
- **Day 2**: Python FastAPI backend, disease classification model, and Matplotlib/Plotly dynamic graph generator. *(Complete)*
- **Days 3–4**: Docker containerization, Docker Compose, Redis caching, and Kubernetes deployment manifests with HPA. *(In Progress)*
- **Days 5–6**: Jenkins declarative pipeline (Build, Lint, Trivy Scan, Helm/K8s Rolling Deploy).
- **Days 7–14**: Observability (Prometheus/Grafana), Stripe billing integration, and production verification.
