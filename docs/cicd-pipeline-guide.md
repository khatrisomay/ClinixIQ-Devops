# ClinixIQ Enterprise CI/CD & DevSecOps Architecture Guide

## 🚀 Dual Pipeline Architecture

ClinixIQ implements a dual pipeline strategy supporting both **GitHub Actions** (cloud-native automated PR verification) and **Jenkins** (enterprise-grade self-hosted multibranch orchestration).

```
                            [ Git Push / Pull Request ]
                                         │
                    ┌────────────────────┴────────────────────┐
                    ▼                                         ▼
        [ GitHub Actions CI/CD ]                     [ Jenkins Controller ]
        ├── Matrix Tests (Py 3.11/3.12, Node 20)      ├── 1. Checkout & Log Scm
        ├── Gitleaks Secret Scanning                  ├── 2. Parallel Lint (Ruff/ESLint)
        ├── Trivy Vulnerability Audit                 ├── 3. Dependency CVE Audit
        └── GHCR Container Publishing                 ├── 4. Pytest & Coverage
                                                      ├── 5. Docker Build & Tag
                                                      ├── 6. Trivy Container Audit
                                                      ├── 7. Helm Dry-Run & K8s Deploy
                                                      └── 8. Webhook Notification
```

---

## 🏗️ Jenkins 8-Stage Declarative Pipeline

| Stage | Action | Tooling | Quality Gate |
| :--- | :--- | :--- | :--- |
| **1. Checkout** | Clones repo, validates commit hash | Git SCM | Clean checkout |
| **2. Quality & Lint** | Parallel Python & React static analysis | Ruff, ESLint | 0 fatal lint errors |
| **3. Security Audit** | Scans Python and Node dependencies | `pip-audit`, `npm audit` | Flags known CVEs |
| **4. Unit Tests** | Executes 9+ clinical triage tests | `pytest`, `pytest-cov` | 100% test pass rate |
| **5. Container Build** | Multi-stage Docker image compilation | Docker CLI | Successful build |
| **6. Trivy Scan** | Audits built container layers | Aqua Security Trivy | Fails on CRITICAL |
| **7. Helm Deploy** | Deploys release to Kubernetes | Helm 3, `kubectl` | Valid manifest rollout |
| **8. Verify & Notify** | Runs smoke check & sends webhook | Shell script, Webhooks | HTTP 200 on `/healthz` |

---

## 🐳 Running Jenkins Locally

To spin up the dedicated Jenkins Controller with pre-installed DevOps tools:

```bash
# Launch Jenkins with configuration-as-code
docker compose -f jenkins/docker-compose.jenkins.yml up -d

# Check startup status
docker compose -f jenkins/docker-compose.jenkins.yml ps
```

Access the Jenkins Dashboard at: [http://localhost:8088](http://localhost:8088)
- **Username**: `admin`
- **Password**: `clinixiq-admin-pass`

---

## 🔄 Automated Zero-Downtime Rollback

If a container enters `CrashLoopBackOff` or fails the initial HTTP `/healthz` probe during continuous deployment:

```bash
# Automated rollback script
./scripts/verify-deployment.sh clinixiq http://localhost:8000/healthz 60
```
This automatically triggers `kubectl rollout undo deployment/clinixiq-backend` to restore the previously healthy cluster revision without downtime.
