# ClinixIQ SRE Incident Response Runbooks & On-Call Matrix

## 🚨 Incident Severity Levels

| Severity | Definition | Target Response SLA | Target Resolution SLA |
| :--- | :--- | :--- | :--- |
| **P1 - Critical** | Complete service outage, emergency triage API unreachable, or >5% 5xx errors. | **< 15 minutes** | **< 2 hours** |
| **P2 - Major** | Degraded inference latency (p95 > 1s), Redis cache failure, or telemetry drop. | **< 30 minutes** | **< 4 hours** |
| **P3 - Minor** | Single pod restart, non-critical metrics scrape failure, or minor cosmetic UI defect. | **< 2 hours** | **< 24 hours** |
| **P4 - Low** | Planned maintenance, non-blocking warning alerts, documentation updates. | **< 24 hours** | Next sprint |

---

## 📞 On-Call Escalation Matrix

1. **Primary On-Call SRE**: Investigates incoming Alertmanager paging alerts.
2. **Secondary DevOps Lead**: Engaged if incident is unacknowledged within 15 minutes.
3. **Clinical / ML Engineering Lead**: Engaged if model output exhibits classification drift or anomalous confidence distributions.

---

## 🛠️ Operational Runbooks

### Runbook 1: `ClinixIQServiceDown`
**Alert Trigger**: `up{job="clinixiq-backend"} == 0` for > 1m.

#### Diagnostic Steps:
```bash
# 1. Check pod status in Kubernetes
kubectl get pods -n clinixiq -l app.kubernetes.io/component=backend

# 2. Inspect pod termination reasons (OOMKilled, CrashLoopBackOff)
kubectl describe pod -l app.kubernetes.io/component=backend -n clinixiq

# 3. View recent crash logs
kubectl logs -l app.kubernetes.io/component=backend -n clinixiq --tail=100 --previous
```

#### Remediation Actions:
1. If pods are in `CrashLoopBackOff` following a deployment, execute an immediate zero-downtime rollback:
   ```bash
   kubectl rollout undo deployment/clinixiq-backend -n clinixiq
   ```
2. If pods were `OOMKilled`, scale memory limits in `k8s/base/backend-deployment.yaml` or restart the deployment:
   ```bash
   kubectl rollout restart deployment/clinixiq-backend -n clinixiq
   ```

---

### Runbook 2: `HighP95InferenceLatency`
**Alert Trigger**: `histogram_quantile(0.95, rate(model_inference_duration_seconds_bucket[5m])) > 0.5s`

#### Diagnostic Steps:
```bash
# 1. Check current HPA scaling status
kubectl get hpa clinixiq-backend-hpa -n clinixiq

# 2. Check CPU and memory utilization across backend nodes
kubectl top pods -n clinixiq
```

#### Remediation Actions:
1. Trigger manual replica expansion if HPA is near maxReplicas:
   ```bash
   kubectl scale deployment/clinixiq-backend -n clinixiq --replicas=6
   ```
2. Verify Redis cache hit ratio on Grafana (`http://localhost:3001/d/clinixiq-overview`). If cache miss rate is high, investigate key invalidation patterns.

---

### Runbook 3: `RedisCacheDown`
**Alert Trigger**: `redis_up == 0` for > 1m.

#### Remediation Actions:
FastAPI backend automatically degrades to in-memory caching. To restore Redis:
```bash
# 1. Restart Redis container / pod
docker compose restart redis
# Or in Kubernetes:
kubectl rollout restart deployment/clinixiq-redis -n clinixiq

# 2. Verify Redis ping
docker exec -it clinixiq-redis redis-cli ping
```
