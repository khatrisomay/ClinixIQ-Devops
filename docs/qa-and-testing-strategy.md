# ClinixIQ Quality Assurance & Testing Strategy

This guide outlines the holistic testing strategy, test pyramid taxonomy, automated smoke runner architecture, and continuous quality gates protecting the ClinixIQ clinical microservices platform.

---

## 1. ClinixIQ Testing Pyramid Architecture

```
                 /\
                /  \
               / E2E \             <- Synthetic Smoke Probes & Chaos Drills (10%)
              /-------\
             /  Integ  \           <- Service-to-Service, DB, Redis & Webhooks (25%)
            /-----------\
           /  Unit Tests \         <- Model Inferences, Schemas, Quota Guards (65%)
          /---------------
```

### Layer Breakdown

| Testing Layer | Tools & Frameworks | Target Coverage | Execution Frequency |
| :--- | :--- | :--- | :--- |
| **Unit Testing** | `pytest`, `pytest-cov`, `unittest.mock` | >= 70% code coverage | Every PR & local git commit |
| **Integration Testing** | `httpx`, `FastAPI TestClient`, `fakeredis` | Critical routing contracts | Every PR build |
| **Synthetic Smoke Probes** | `SmokeRunner`, exponential backoff HTTP client | 100% core endpoints | Post-deployment & staging |
| **Chaos Engineering** | `ChaosEngine`, Chaos Mesh, LitmusChaos | MTTR < 5.0s SLA | Weekly and on release cuts |

---

## 2. Automated Smoke Testing Engine

ClinixIQ features a lightweight, zero-dependency Python smoke test harness located at `tests/smoke/smoke_runner.py`.

### Key Features
- **Exponential Backoff:** Configurable retries (`--retries 3`) with doubling delay intervals to absorb transient network blips during pod rolling updates.
- **Custom Assertion Validators:** Supports functional response payload assertions in addition to HTTP status code verification.
- **Structured JSON Reporting:** Generates timestamped CI/CD test summaries containing pass rates, failed checks, and millisecond latency profiles.

### Running Smoke Tests Locally
```bash
# Verify local API server
python tests/smoke/smoke_runner.py --url http://localhost:8000 --timeout 5.0 --report reports/smoke.json

# Execute synthetic patient clinical journey
python tests/smoke/test_patient_journey.py --url http://localhost:8000

# Execute commercial billing checkout & webhook journey
python tests/smoke/test_billing_journey.py --url http://localhost:8000
```

---

## 3. Test Suite Inventory

### Backend Unit & Integration Tests (`backend/tests/`)
1. `test_triage.py`: Clinical ML prediction validation, symptom extraction, emergency escalation logic, and SVG chart generation.
2. `test_metrics.py`: Prometheus `/metrics` exposition, counter increments, and correlation ID tracing propagation.
3. `test_billing.py`: Plan catalogs, customer portal sessions, quota enforcement, and tier-based rate limiting (HTTP 402).
4. `test_webhooks.py`: Stripe webhook idempotency, signature verification, and subscription lifecycle events.
5. `test_smoke_runner.py`: Smoke engine retries, custom validators, and summary exit codes.
6. `test_chaos_engine.py`: Steady state hypothesis testing, fault injection lifecycle, and MTTR calculations.

### Executing Backend Tests
```bash
cd backend
pytest tests/ -v --cov=app --cov-report=xml
```

---

## 4. CI/CD Quality Gates & Release Verification

| Workflow File | Trigger | Quality Gate Policy |
| :--- | :--- | :--- |
| `.github/workflows/ci.yml` | Pull Request / Push | Linting, unit tests, coverage verification, frontend build. |
| `.github/workflows/smoke-test.yml` | Deployment Complete | Liveness, readiness, triage API, and billing endpoint smoke probes. |
| `.github/workflows/chaos.yml` | Schedule / Dispatch | Fault injection scenarios, MTTR benchmarking, resilience scorecard generation. |
| `security.yml` (DevSecOps) | Pull Request / Push | Gitleaks secret detection and Trivy container vulnerability scanning. |

---

## 5. Failure Escalation & Rollback Thresholds

- **Smoke Test Failure:** If any post-deployment smoke probe returns non-zero exit codes, the deployment pipeline halts immediately and initiates an automated rollback to the previous stable release.
- **Flaky Test Elimination:** Tests exhibiting non-deterministic behavior are isolated with `@pytest.mark.flaky` and addressed within 48 hours.
