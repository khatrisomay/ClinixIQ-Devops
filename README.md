# ClinixIQ - AI Health Triage & DevOps Platform

[![CI Pipeline](https://github.com/khatrisomay/ClinixIQ-Devops/actions/workflows/ci.yml/badge.svg)](https://github.com/khatrisomay/ClinixIQ-Devops/actions/workflows/ci.yml)
[![Security Audit](https://github.com/khatrisomay/ClinixIQ-Devops/actions/workflows/security.yml/badge.svg)](https://github.com/khatrisomay/ClinixIQ-Devops/actions/workflows/security.yml)
[![Secret Scan](https://github.com/khatrisomay/ClinixIQ-Devops/actions/workflows/secret-scan.yml/badge.svg)](https://github.com/khatrisomay/ClinixIQ-Devops/actions/workflows/secret-scan.yml)
[![Docker](https://img.shields.io/badge/Docker-Multi--stage-2496ED?logo=docker&logoColor=white)](https://www.docker.com/)
[![Kubernetes](https://img.shields.io/badge/Kubernetes-Orchestration-326CE5?logo=kubernetes&logoColor=white)](https://kubernetes.io/)
[![Jenkins](https://img.shields.io/badge/Jenkins-Declarative%20CI%2FCD-D24939?logo=jenkins&logoColor=white)](https://www.jenkins.io/)
[![Prometheus](https://img.shields.io/badge/Prometheus-Metrics%20Telemetry-E6522C?logo=prometheus&logoColor=white)](https://prometheus.io/)
[![Grafana](https://img.shields.io/badge/Grafana-SRE%20Dashboards-F46800?logo=grafana&logoColor=white)](https://grafana.com/)
[![Helm](https://img.shields.io/badge/Helm-3%20Package-0F1689?logo=helm&logoColor=white)](https://helm.sh/)

**ClinixIQ** is an enterprise-grade, commercial AI-powered symptom triage and disease risk analytics platform. Designed to demonstrate a complete production DevOps lifecycle, ClinixIQ combines interactive clinical NLP triage with Python-generated diagnostic analytics, containerized with Docker, orchestrated via Kubernetes, continuously delivered via automated Jenkins and GitHub Actions CI/CD pipelines, and monitored with Prometheus & Grafana.

---

## 🏗️ System & Telemetry Architecture

```
[ Client / Browser ] 
       │ (HTTPS / TLS 1.3)
       ▼
[ Nginx Ingress Controller ]
       ├───────────────┬────────────────┐
       ▼               ▼                ▼
[ React Frontend ]  [ FastAPI Backend ] [ Prometheus Server (9090) ]
  (Nginx Pods)        (Python Pods)        ├── Scrapes /metrics (10s)
                       │                   ├── Evaluates SRE Alert Rules
       ┌───────────────┴───────────────┐   └── Routes to Alertmanager (9093)
       ▼                               ▼                  │
[ ML Inference Engine ]     [ Redis Caching Layer ]       ▼
  (Scikit-Learn/XGBoost)      (Sub-millisecond State) [ Grafana Dashboard (3001) ]
```

---

## 📊 Observability & SRE Stack

- **Prometheus Telemetry**: Custom metrics tracking throughput, p95/p99 latency, disease classification distributions, and cache hit ratios on `/metrics`.
- **Pre-Configured Grafana Dashboard**: Automated datasource and dashboard provisioning located at `http://localhost:3001` (admin / `clinixiq-admin`).
- **SRE Alerting Rules**: Automated alerts for `HighInferenceLatency`, `HighErrorRate`, `ClinixIQServiceDown`, and `RedisCacheDown`.
- **OpenTelemetry & Structured Logging**: W3C distributed trace spans and HIPAA-compliant JSON audit logging with correlation ID propagation.

---

## 🐳 Quickstart Options

### 1. Launch Application Stack
```bash
docker compose up -d
# Frontend: http://localhost:3000 | API Docs: http://localhost:8000/docs
```

### 2. Launch Monitoring Stack (Prometheus & Grafana)
```bash
docker compose -f monitoring/docker-compose.monitoring.yml up -d
# Prometheus: http://localhost:9090 | Grafana: http://localhost:3001
```

### 3. Generate Synthetic Clinical Load
```bash
python scripts/generate-load.py --requests 200 --delay 0.05
```

---

## 📅 14-Day Delivery Roadmap
- **Day 1**: React.js Frontend, symptom triage UI, analytics dashboard, SaaS pricing, and Dockerfile. *(Complete)*
- **Day 2**: Python FastAPI backend, disease classification model, and Matplotlib/Plotly dynamic graph generator. *(Complete)*
- **Days 3–4**: Docker Compose, Redis caching, Gateway, Kubernetes manifests, Kustomize overlays, and Helm chart. *(Complete)*
- **Day 5**: Jenkins declarative 8-stage pipeline, GitHub Actions matrix CI/CD, Trivy container scanning, and Gitleaks. *(Complete)*
- **Day 6**: Full Observability stack (Prometheus metrics, Grafana dashboards, Alertmanager, and SRE runbooks). *(Complete)*
- **Days 7–14**: Cloud infrastructure, Stripe commercial billing integration, and production verification.
