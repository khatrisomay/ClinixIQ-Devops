# ClinixIQ - AI Health Triage & DevOps Platform

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Docker](https://img.shields.io/badge/Docker-Multi--stage-2496ED?logo=docker&logoColor=white)](https://www.docker.com/)
[![Kubernetes](https://img.shields.io/badge/Kubernetes-Orchestration-326CE5?logo=kubernetes&logoColor=white)](https://kubernetes.io/)
[![Jenkins](https://img.shields.io/badge/Jenkins-CI%2FCD-D24939?logo=jenkins&logoColor=white)](https://www.jenkins.io/)
[![React](https://img.shields.io/badge/React-18-61DAFB?logo=react&logoColor=black)](https://react.dev/)
[![FastAPI](https://img.shields.io/badge/FastAPI-Python-009688?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)

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
[ ML Inference Engine ]     [ Analytics / Graph Gen ]
  (Scikit-Learn/XGBoost)      (Matplotlib / Plotly)
```

---

## 🛠️ DevOps Tech Stack

- **Containerization**: Multi-stage, non-root Docker builds for React (Vite/Nginx) and Python (FastAPI).
- **Orchestration**: Kubernetes manifests (Deployments, Services, Ingress, Horizontal Pod Autoscaler, ConfigMaps, Secrets).
- **CI/CD**: Declarative Jenkins pipeline with static linting, unit tests, Trivy vulnerability scanning, container registry publishing, and zero-downtime rolling updates.
- **Monitoring**: Prometheus metrics scrapers and Grafana dashboards tracking API latency, pod health, and ML inference duration.

---

## 💼 Commercial SaaS Strategy
1. **Free Triage**: Basic AI symptom evaluation & differential diagnoses.
2. **Pro Patient ($9.99/mo)**: Unlimited evaluations, chronic symptom tracking, exportable PDF doctor referral summaries, and longitudinal risk graphs.
3. **Enterprise Clinic API ($149/mo)**: High-throughput API access for telehealth providers with dedicated Kubernetes ingress and HIPAA-aligned data pipelines.

---

## 📅 14-Day Delivery Roadmap
- **Days 1–3**: React.js Frontend, symptom triage UI, analytics dashboard, SaaS pricing, and Dockerfile. *(Current Phase)*
- **Days 4–6**: Python FastAPI backend, disease classification model, and Matplotlib/Plotly dynamic graph generator.
- **Days 7–9**: Docker containerization, Docker Compose, and Kubernetes deployment manifests with HPA.
- **Days 10–12**: Jenkins declarative pipeline (Build, Lint, Trivy Scan, Helm/K8s Rolling Deploy).
- **Days 13–14**: Prometheus/Grafana observability dashboards, Stripe billing integration, and production verification.
