# ClinixIQ Chaos Engineering & Resilience Runbook

This document defines the enterprise Chaos Engineering principles, Game Day standard operating procedures (SOP), automated failure injection protocols, and emergency blast radius containment mechanisms for the ClinixIQ microservices ecosystem.

---

## 1. Principles of ClinixIQ Chaos Engineering

ClinixIQ facilitates safety-critical clinical triage and multi-tier commercial SaaS billing. System availability, stateful idempotency, and automated recovery are paramount.

1. **Hypothesize About Steady State:** Every chaos experiment begins with measurable quantitative definitions of baseline health (HTTP 200 pass rate >= 99.9%, P95 latency <= 250ms, active error budget consumption <= 0.01%).
2. **Simulate Real-World Failures:** Faults mirror production incidents: Redis broker eviction, network latency degradation, pod node evictions, and traffic surges.
3. **Automate Continuous Verification:** Run chaos experiments programmatically in staging pipelines and on weekly schedules rather than waiting for production outages.
4. **Minimize Blast Radius:** All chaos experiments incorporate automated health gates, execution timeouts, and unconditional self-healing cleanup handlers.

---

## 2. Game Day Standard Operating Procedure (SOP)

### Team Roles & Responsibilities

| Role | Designee | Responsibilities |
| :--- | :--- | :--- |
| **Chaos Commander** | Staff DevOps / SRE Lead | Authorizes experiment commencement, calls aborts if blast radius exceeds limits, tracks timeline. |
| **Telemetry Lead** | Observability Engineer | Monitors Grafana dashboards, Prometheus alerts, and P95 latency metrics in real time. |
| **Chaos Injector** | Chaos Engineer / QA | Triggers CLI chaos scripts or Chaos Mesh CRDs against target staging clusters. |
| **Scribe** | QA / Technical Writer | Logs all timestamps, behavioral anomalies, MTTR timings, and post-experiment action items. |

### Game Day Execution Checklist

1. **Pre-Flight Verification:**
   - Ensure all baseline Kubernetes pods (`backend`, `frontend`, `redis`) report `1/1 Running`.
   - Confirm Prometheus and Grafana telemetry scraping is active with zero active alerts.
   - Run the smoke test suite: `python tests/smoke/smoke_runner.py --url http://localhost:8000`.
2. **Execution Phase:**
   - Execute targeted scenario via CLI: `python chaos/run_chaos.py --experiment redis --duration 10.0`.
   - Telemetry lead validates that Alertmanager alerts fire within SLA thresholds.
3. **Recovery Phase (MTTR Measurement):**
   - Injector terminates fault.
   - Scribe logs the exact recovery timestamp when steady state metrics return to baseline.
4. **Post-Mortem & Resilience Audit:**
   - Run `python chaos/resilience_reporter.py --input reports/chaos/resilience_audit.json --markdown reports/chaos/audit.md`.
   - Archive report artifacts and file Jira/GitHub issues for any remediation actions.

---

## 3. Chaos Experiment Catalog

### Experiment 1: Redis Invalidation & Cache Broker Severance
- **Fault Type:** `redis_disconnect`
- **Hypothesis:** When the Redis caching layer becomes unavailable, the FastAPI backend will degrade gracefully by executing fresh ML model inferences directly without dropping requests or throwing HTTP 500s.
- **Verification:** Run `python chaos/run_chaos.py --experiment redis`.
- **Target MTTR:** `< 3.0 seconds`.

### Experiment 2: Network Latency & Jitter Degradation
- **Fault Type:** `network_latency`
- **Hypothesis:** Adding 300ms network delay with 50ms jitter across API endpoints must not trigger cascading connection pool exhaustion or timeout failures in downstream callers.
- **Verification:** Run `python chaos/run_chaos.py --experiment latency`.
- **Target MTTR:** `< 2.0 seconds`.

### Experiment 3: High-Concurrency Traffic Spike Saturation
- **Fault Type:** `traffic_spike`
- **Hypothesis:** Flooding the triage pipeline with concurrent clinical submissions must engage rate limiting and queuing gracefully while maintaining liveness and readiness probe availability.
- **Verification:** Run `python chaos/run_chaos.py --experiment spike`.
- **Target MTTR:** `< 4.0 seconds`.

### Experiment 4: Kubernetes Pod Disruption & Eviction
- **Fault Type:** `pod-kill`
- **Hypothesis:** Random termination of a backend microservice pod will be seamlessly absorbed by Kubernetes ReplicaSets and Service endpoints without dropping ongoing customer transactions.
- **Verification:** Run `./scripts/test-pod-disruption.sh`.
- **Target MTTR:** `< 5.0 seconds`.

---

## 4. Emergency Blast Radius Containment & Abort Procedures

If an experiment causes unexpected systemic degradation, any team member is empowered to declare an immediate abort.

### Hard Abort Triggers
- End-to-end API error rate exceeds **5.0%** for more than 15 seconds.
- P95 latency exceeds **3,000ms** on critical clinical triage endpoints.
- Unhandled HTTP 500 exceptions surge on payment or checkout routes.

### Emergency Kill Commands

#### Native CLI Scenarios
Press `Ctrl+C` or execute process termination:
```bash
# Terminate Python chaos orchestrators
pkill -f "run_chaos.py"
```

#### Kubernetes Chaos Mesh Resources
Delete all active chaos CRDs immediately:
```bash
kubectl delete -k k8s/chaos/
kubectl delete podchaos,networkchaos --all -n clinixiq
```

---

## 5. Automated CI/CD Chaos Pipeline

Chaos engineering is automated in GitHub Actions via `.github/workflows/chaos.yml`.
- Runs automatically on weekly schedules (Sundays at 03:00 UTC).
- Executed on every pull request that modifies `chaos/**`.
- Produces downloadable JSON and Markdown audit artifacts (`reports/chaos/resilience_audit.json`).
