# ClinixIQ - AI Health Triage & DevOps Platform

[![CI Pipeline](https://github.com/khatrisomay/ClinixIQ-Devops/actions/workflows/ci.yml/badge.svg)](https://github.com/khatrisomay/ClinixIQ-Devops/actions/workflows/ci.yml)
[![Terraform Audit](https://github.com/khatrisomay/ClinixIQ-Devops/actions/workflows/terraform.yml/badge.svg)](https://github.com/khatrisomay/ClinixIQ-Devops/actions/workflows/terraform.yml)
[![Chaos Engineering](https://img.shields.io/badge/Chaos%20Engineering-Resilience%20Verified-00C853?logo=target&logoColor=white)](chaos/)
[![Security Audit](https://github.com/khatrisomay/ClinixIQ-Devops/actions/workflows/security.yml/badge.svg)](https://github.com/khatrisomay/ClinixIQ-Devops/actions/workflows/security.yml)
[![Secret Scan](https://github.com/khatrisomay/ClinixIQ-Devops/actions/workflows/secret-scan.yml/badge.svg)](https://github.com/khatrisomay/ClinixIQ-Devops/actions/workflows/secret-scan.yml)
[![Docker](https://img.shields.io/badge/Docker-Multi--stage-2496ED?logo=docker&logoColor=white)](https://www.docker.com/)
[![Kubernetes](https://img.shields.io/badge/Kubernetes-Orchestration-326CE5?logo=kubernetes&logoColor=white)](https://kubernetes.io/)
[![Terraform](https://img.shields.io/badge/Terraform-1.8.5%20IaC-844FBA?logo=terraform&logoColor=white)](https://www.terraform.io/)
[![AWS](https://img.shields.io/badge/AWS-EKS%20%7C%20ElastiCache-232F3E?logo=amazon-aws&logoColor=white)](https://aws.amazon.com/)
[![Stripe](https://img.shields.io/badge/Stripe-SaaS%20Billing-635BFF?logo=stripe&logoColor=white)](https://stripe.com/)
[![Jenkins](https://img.shields.io/badge/Jenkins-Declarative%20CI%2FCD-D24939?logo=jenkins&logoColor=white)](https://www.jenkins.io/)
[![Prometheus](https://img.shields.io/badge/Prometheus-Metrics%20Telemetry-E6522C?logo=prometheus&logoColor=white)](https://prometheus.io/)
[![Grafana](https://img.shields.io/badge/Grafana-SRE%20Dashboards-F46800?logo=grafana&logoColor=white)](https://grafana.com/)
[![Helm](https://img.shields.io/badge/Helm-3%20Package-0F1689?logo=helm&logoColor=white)](https://helm.sh/)

**ClinixIQ** is an enterprise-grade, commercial AI-powered symptom triage and disease risk analytics platform. Designed to demonstrate a complete production DevOps lifecycle, ClinixIQ combines interactive clinical NLP triage with Python-generated diagnostic analytics, containerized with Docker, orchestrated via Kubernetes, continuously delivered via automated Jenkins and GitHub Actions CI/CD pipelines, provisioned across multi-AZ AWS infrastructure via Terraform, monetized via Stripe subscriptions, continuously verified through automated chaos engineering & smoke testing, and monitored with Prometheus & Grafana.

---

## 🏗️ Enterprise Cloud, Resilience & Telemetry Architecture

```
                             [ Internet / User Traffic ]
                                          │
                                          │ HTTPS (TLS 1.3 / ACM Certificate)
                                          ▼
                         [ AWS Application Load Balancer ]
                           (Public Subnets across Multi-AZ)
                                          │
                  ┌───────────────────────┼───────────────────────┐
                  │ Path: /*              │ Path: /api/*, /metrics│ Synthetic Health Probes
                  ▼                       ▼                       ▼
         [ React Frontend UI ]  [ FastAPI ML & Billing ]  [ Automated Smoke Runner ]
           (Nginx Pods on EKS)    (Python Pods with IRSA)  (Exponential Backoff E2E)
                                          │                       │
                  ┌───────────────────────┼───────────────────────┴──────────────────────┐
                  ▼                       ▼                       ▼                      ▼
      [ ML Inference Engine ]  [ ElastiCache Redis ]   [ Prometheus Server ]   [ Chaos Mesh Engine ]
        (Diagnostic Analytics)   (Multi-AZ Replication)  (Port 9090 Telemetry)  (Fault Injection & MTTR)
                                          │                       │                      │
                  ┌───────────────────────┼───────────────────────┘                      │
                  ▼                       ▼                       ▼                      ▼
      [ Stripe Payment Gateway ][ KMS HIPAA Protection ] [ Grafana Dashboard ] [ Resilience Audit Report ]
        (Checkout & Webhooks)    (Envelope Encryption)    (Port 3001 SRE View)   (Automated Scorecard)
```

---

## ⚡ Chaos Engineering & Resilience Verification

- **Automated Fault Injection Engine**: Python framework for executing Redis disconnects, upstream latency injection, and traffic saturation.
- **Steady State Hypothesis Verification**: Continuous probing of P95 latency and availability with MTTR (Mean Time To Recovery) measurement.
- **Enterprise Smoke Runner**: Zero-dependency cross-platform runner (`tests/smoke/smoke_runner.py`) with exponential backoff validating patient and billing journeys.
- **Kubernetes Resilience Manifests**: Declarative Chaos Mesh CRDs (`PodChaos`, `NetworkChaos`) and automated pod disruption scripts.
- **Resilience Scorecard Generator**: CI/CD audit reporter calculating SLA compliance (< 5s MTTR target) and generating Markdown/JSON scorecards.

---

## 💳 Commercial Monetization & Stripe Billing Engine

- **Self-Service Subscriptions**: Seamless Stripe Checkout Sessions supporting Starter ($0), Pro ($9.99/mo), and Enterprise ($149/mo) tiers with automated 20% annual discounts.
- **Cryptographic Webhooks**: Real-time asynchronous state synchronization verified via HMAC-SHA256 signatures on `/api/webhooks/stripe`.
- **Distributed Idempotency Defense**: Atomic Redis `SET NX` locks with 24-hour TTL preventing duplicate webhook execution and replay attacks.
- **Clinical Quota Metering**: Tier-based monthly query rate-limiting with automated HTTP 402 Payment Required enforcement on `/api/v1/triage/predict`.
- **Customer Billing Portal**: Self-service subscription management, invoice downloads, and card updates via Stripe Billing Portal.

---

## 📊 Observability & SRE Stack

- **Prometheus Telemetry**: Custom metrics tracking throughput, p95/p99 latency, disease classification distributions, active subscriptions, MRR, and cache hit ratios on `/metrics`.
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

### 3. Run Automated Smoke Test Suite
```bash
python tests/smoke/smoke_runner.py --url http://localhost:8000 --retries 3
```

### 4. Execute Chaos Engineering Resilience Drills
```bash
python chaos/run_chaos.py --experiment all --duration 3.0
```

### 5. Run Full Automated Test Suite
```bash
pytest backend/tests/ -v
```

---

## 📅 14-Day Delivery Roadmap
- **Day 1**: React.js Frontend, symptom triage UI, analytics dashboard, SaaS pricing, and Dockerfile. *(Complete)*
- **Day 2**: Python FastAPI backend, disease classification model, and Matplotlib/Plotly dynamic graph generator. *(Complete)*
- **Days 3–4**: Docker Compose, Redis caching, Gateway, Kubernetes manifests, Kustomize overlays, and Helm chart. *(Complete)*
- **Day 5**: Jenkins declarative 8-stage pipeline, GitHub Actions matrix CI/CD, Trivy container scanning, and Gitleaks. *(Complete)*
- **Day 6**: Full Observability stack (Prometheus metrics, Grafana dashboards, Alertmanager, and SRE runbooks). *(Complete)*
- **Day 7**: Cloud Infrastructure as Code (Terraform), AWS EKS cluster, ElastiCache Redis, ALB with ACM TLS, KMS encryption, Secrets Manager, and Disaster Recovery. *(Complete)*
- **Day 8**: Commercial Monetization, Stripe Checkout, Webhooks, Subscription Management, and Quota Metering. *(Complete)*
- **Day 9**: End-to-End Automated Smoke Testing, Chaos Engineering, Fault Injection, System Resilience Verification, and Health Check Probes. *(Complete)*
- **Days 10–14**: GitOps Continuous Deployment (ArgoCD), Advanced Security Auditing, Performance Benchmarking, and Final Production Hardening.
