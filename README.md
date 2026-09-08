# ClinixIQ - AI Health Triage & DevOps Platform

[![CI Pipeline](https://github.com/khatrisomay/ClinixIQ-Devops/actions/workflows/ci.yml/badge.svg)](https://github.com/khatrisomay/ClinixIQ-Devops/actions/workflows/ci.yml)
[![Security Audit](https://github.com/khatrisomay/ClinixIQ-Devops/actions/workflows/security.yml/badge.svg)](https://github.com/khatrisomay/ClinixIQ-Devops/actions/workflows/security.yml)
[![Secret Scan](https://github.com/khatrisomay/ClinixIQ-Devops/actions/workflows/secret-scan.yml/badge.svg)](https://github.com/khatrisomay/ClinixIQ-Devops/actions/workflows/secret-scan.yml)
[![Docker](https://img.shields.io/badge/Docker-Multi--stage-2496ED?logo=docker&logoColor=white)](https://www.docker.com/)
[![Kubernetes](https://img.shields.io/badge/Kubernetes-Orchestration-326CE5?logo=kubernetes&logoColor=white)](https://kubernetes.io/)
[![Jenkins](https://img.shields.io/badge/Jenkins-Declarative%20CI%2FCD-D24939?logo=jenkins&logoColor=white)](https://www.jenkins.io/)
[![Helm](https://img.shields.io/badge/Helm-3%20Package-0F1689?logo=helm&logoColor=white)](https://helm.sh/)

**ClinixIQ** is an enterprise-grade, commercial AI-powered symptom triage and disease risk analytics platform. Designed to demonstrate a complete production DevOps lifecycle, ClinixIQ combines interactive clinical NLP triage with Python-generated diagnostic analytics, containerized with Docker, orchestrated via Kubernetes, and continuously delivered via automated Jenkins and GitHub Actions CI/CD pipelines.

---

## 🏗️ System Architecture

```
[ Client / Browser ] 
       │ (HTTPS / TLS 1.3)
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

## 🔄 Dual CI/CD & DevSecOps Pipelines

ClinixIQ features enterprise dual-engine continuous integration and deployment:

- **Jenkins Multibranch Pipeline (`Jenkinsfile`)**: 8-stage declarative pipeline handling linting, dependency auditing, unit tests with coverage, multi-stage Docker compilation, Trivy container scanning, Helm deployment, and webhook notifications.
- **GitHub Actions (`.github/workflows/`)**:
  - `ci.yml`: Matrix testing across Python 3.11/3.12 and Node.js 18/20.
  - `security.yml`: Aqua Security Trivy filesystem and container CVE scanning.
  - `secret-scan.yml`: Gitleaks high-entropy secret detection.
  - `cd.yml`: Automated GHCR/Docker Hub multi-arch image publishing.

For detailed pipeline architecture, refer to [docs/cicd-pipeline-guide.md](docs/cicd-pipeline-guide.md).

---

## 🐳 Quickstart Options

### 1. Local Multi-Container Stack (Docker Compose)
```bash
docker compose up -d
# Frontend: http://localhost:3000 | API Docs: http://localhost:8000/docs
```

### 2. Local Kubernetes & Helm Deployment
```bash
# Validate and deploy via Helm
helm upgrade --install clinixiq ./helm/clinixiq --namespace clinixiq --create-namespace
```

### 3. Local Jenkins Controller
```bash
docker compose -f jenkins/docker-compose.jenkins.yml up -d
# Jenkins UI: http://localhost:8088 (admin / clinixiq-admin-pass)
```

---

## 📅 14-Day Delivery Roadmap
- **Day 1**: React.js Frontend, symptom triage UI, analytics dashboard, SaaS pricing, and Dockerfile. *(Complete)*
- **Day 2**: Python FastAPI backend, disease classification model, and Matplotlib/Plotly dynamic graph generator. *(Complete)*
- **Days 3–4**: Docker Compose, Redis caching, Gateway, Kubernetes manifests, Kustomize overlays, and Helm chart. *(Complete)*
- **Day 5**: Jenkins declarative 8-stage pipeline, GitHub Actions matrix CI/CD, Trivy container scanning, and Gitleaks. *(Complete)*
- **Days 6–7**: Observability stack (Prometheus metrics scrapers & Grafana dashboards).
- **Days 8–14**: Cloud infrastructure, Stripe commercial billing integration, and production verification.
