# ClinixIQ - AI Health Triage & DevOps Platform

[![CI Pipeline](https://github.com/khatrisomay/ClinixIQ-Devops/actions/workflows/ci.yml/badge.svg)](https://github.com/khatrisomay/ClinixIQ-Devops/actions/workflows/ci.yml)
[![Terraform Audit](https://github.com/khatrisomay/ClinixIQ-Devops/actions/workflows/terraform.yml/badge.svg)](https://github.com/khatrisomay/ClinixIQ-Devops/actions/workflows/terraform.yml)
[![Security Audit](https://github.com/khatrisomay/ClinixIQ-Devops/actions/workflows/security.yml/badge.svg)](https://github.com/khatrisomay/ClinixIQ-Devops/actions/workflows/security.yml)
[![Secret Scan](https://github.com/khatrisomay/ClinixIQ-Devops/actions/workflows/secret-scan.yml/badge.svg)](https://github.com/khatrisomay/ClinixIQ-Devops/actions/workflows/secret-scan.yml)
[![Docker](https://img.shields.io/badge/Docker-Multi--stage-2496ED?logo=docker&logoColor=white)](https://www.docker.com/)
[![Kubernetes](https://img.shields.io/badge/Kubernetes-Orchestration-326CE5?logo=kubernetes&logoColor=white)](https://kubernetes.io/)
[![Terraform](https://img.shields.io/badge/Terraform-1.8.5%20IaC-844FBA?logo=terraform&logoColor=white)](https://www.terraform.io/)
[![AWS](https://img.shields.io/badge/AWS-EKS%20%7C%20ElastiCache-232F3E?logo=amazon-aws&logoColor=white)](https://aws.amazon.com/)
[![Jenkins](https://img.shields.io/badge/Jenkins-Declarative%20CI%2FCD-D24939?logo=jenkins&logoColor=white)](https://www.jenkins.io/)
[![Prometheus](https://img.shields.io/badge/Prometheus-Metrics%20Telemetry-E6522C?logo=prometheus&logoColor=white)](https://prometheus.io/)
[![Grafana](https://img.shields.io/badge/Grafana-SRE%20Dashboards-F46800?logo=grafana&logoColor=white)](https://grafana.com/)
[![Helm](https://img.shields.io/badge/Helm-3%20Package-0F1689?logo=helm&logoColor=white)](https://helm.sh/)

**ClinixIQ** is an enterprise-grade, commercial AI-powered symptom triage and disease risk analytics platform. Designed to demonstrate a complete production DevOps lifecycle, ClinixIQ combines interactive clinical NLP triage with Python-generated diagnostic analytics, containerized with Docker, orchestrated via Kubernetes, continuously delivered via automated Jenkins and GitHub Actions CI/CD pipelines, provisioned across multi-AZ AWS infrastructure via Terraform, and monitored with Prometheus & Grafana.

---

## 🏗️ Enterprise Cloud & Telemetry Architecture

```
                             [ Internet / User Traffic ]
                                          │
                                          │ HTTPS (TLS 1.3 / ACM Certificate)
                                          ▼
                         [ AWS Application Load Balancer ]
                           (Public Subnets across Multi-AZ)
                                          │
                  ┌───────────────────────┴───────────────────────┐
                  │ Path: /*                                      │ Path: /api/*, /metrics
                  ▼                                               ▼
         [ React Frontend UI ]                          [ FastAPI ML Microservice ]
           (Nginx Pods on EKS)                            (Python Pods with IRSA)
                                                                  │
                  ┌───────────────────────────────────────────────┼──────────────────────────────┐
                  ▼                                               ▼                              ▼
      [ ML Inference Engine ]                         [ ElastiCache Redis ]            [ Prometheus Server ]
        (Diagnostic Analytics)                          (Multi-AZ Replication)           (Port 9090 Telemetry)
                                                                  │                              │
                                                                  ▼                              ▼
                                                      [ KMS Envelope Encryption ]      [ Grafana Dashboard ]
                                                        (HIPAA Data Protection)          (Port 3001 SRE View)
```

---

## 📊 Observability & SRE Stack

- **Prometheus Telemetry**: Custom metrics tracking throughput, p95/p99 latency, disease classification distributions, and cache hit ratios on `/metrics`.
- **Pre-Configured Grafana Dashboard**: Automated datasource and dashboard provisioning located at `http://localhost:3001` (admin / `clinixiq-admin`).
- **SRE Alerting Rules**: Automated alerts for `HighInferenceLatency`, `HighErrorRate`, `ClinixIQServiceDown`, and `RedisCacheDown`.
- **OpenTelemetry & Structured Logging**: W3C distributed trace spans and HIPAA-compliant JSON audit logging with correlation ID propagation.

---

## ☁️ Cloud Infrastructure as Code (Terraform)

- **Multi-AZ VPC**: 3-tier networking (Public, Private Compute, and Isolated Database subnets) with redundant NAT Gateways and VPC Flow Logs.
- **Managed Amazon EKS**: Production-grade Kubernetes v1.30 with OIDC IAM Roles for Service Accounts (IRSA) and managed node groups.
- **AWS ElastiCache Redis**: Multi-AZ replication group with automated failover, TLS transit encryption, and KMS encryption at rest.
- **Secrets Management**: AWS Secrets Manager with least-privilege IAM policies and automated secret rotation.
- **Multi-Environment**: Tailored configurations for `dev` (cost-optimized) and `prod` (high-availability).

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

### 4. Validate Cloud Infrastructure (Terraform)
```bash
./scripts/tf-deploy.sh validate dev
```

---

## 📅 14-Day Delivery Roadmap
- **Day 1**: React.js Frontend, symptom triage UI, analytics dashboard, SaaS pricing, and Dockerfile. *(Complete)*
- **Day 2**: Python FastAPI backend, disease classification model, and Matplotlib/Plotly dynamic graph generator. *(Complete)*
- **Days 3–4**: Docker Compose, Redis caching, Gateway, Kubernetes manifests, Kustomize overlays, and Helm chart. *(Complete)*
- **Day 5**: Jenkins declarative 8-stage pipeline, GitHub Actions matrix CI/CD, Trivy container scanning, and Gitleaks. *(Complete)*
- **Day 6**: Full Observability stack (Prometheus metrics, Grafana dashboards, Alertmanager, and SRE runbooks). *(Complete)*
- **Day 7**: Cloud Infrastructure as Code (Terraform), AWS EKS cluster, ElastiCache Redis, ALB with ACM TLS, KMS encryption, Secrets Manager, and Disaster Recovery. *(Complete)*
- **Days 8–14**: Stripe commercial billing integration, end-to-end automated smoke testing, and production verification.
