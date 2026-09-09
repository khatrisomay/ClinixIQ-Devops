# ClinixIQ Observability, Telemetry & SRE Guide

## 📊 Telemetry Architecture

ClinixIQ implements a comprehensive telemetry pipeline grounding **Metrics**, **Logs**, and **Traces** (the three pillars of observability):

```
                     ┌──────────────────────┐
                     │   FastAPI Backend    │
                     └──────────┬───────────┘
                                │
          ┌─────────────────────┼─────────────────────┐
          │ (Prometheus /metrics)│ (Structured JSON)   │ (OTel Spans)
          ▼                     ▼                     ▼
┌───────────────────┐ ┌───────────────────┐ ┌───────────────────┐
│ Prometheus Scraper│ │ FluentBit / Loki  │ │ Jaeger / Tempo    │
│    (Port 9090)    │ │   (Audit Logs)    │ │ (Distributed Trace│
└─────────┬─────────┘ └───────────────────┘ └───────────────────┘
          │
          ▼
┌───────────────────┐
│ Grafana Dashboard │ (Port 3001)
│ Alertmanager      │ (Port 9093)
└───────────────────┘
```

---

## 📈 Prometheus Metrics Catalog

| Metric Identifier | Metric Type | Labels | Description |
| :--- | :--- | :--- | :--- |
| `http_requests_total` | Counter | `method`, `endpoint`, `status` | Total HTTP requests handled by the API |
| `http_request_duration_seconds` | Histogram | `method`, `endpoint` | End-to-end HTTP request latency distribution |
| `triage_predictions_total` | Counter | `condition`, `severity`, `emergency` | Total AI clinical evaluations categorized |
| `model_inference_duration_seconds` | Histogram | `model_version` | Pure machine learning inference computation duration |
| `active_triage_sessions` | Gauge | None | Number of concurrent active patient intakes |
| `cache_hits_total` | Counter | `cache_type` | Redis cache hits avoiding re-computation |
| `cache_misses_total` | Counter | `cache_type` | Cache misses requiring fresh inference |

---

## 🎯 Service Level Objectives (SLOs)

ClinixIQ commits to strict reliability standards for clinical availability:

| Service Level Indicator (SLI) | SLO Target | Evaluation Window | PromQL Formula |
| :--- | :--- | :--- | :--- |
| **API Availability** | **>= 99.9%** | Rolling 30 days | `(1 - (sum(rate(http_requests_total{status=~"5.."}[30d])) / sum(rate(http_requests_total[30d])))) * 100` |
| **P95 Latency** | **< 250ms** | Rolling 5 minutes | `histogram_quantile(0.95, sum(rate(http_request_duration_seconds_bucket[5m])) by (le))` |
| **P99 Latency** | **< 500ms** | Rolling 5 minutes | `histogram_quantile(0.99, sum(rate(http_request_duration_seconds_bucket[5m])) by (le))` |
| **Cache Efficiency** | **>= 60.0%** | Rolling 1 hour | `sum(rate(cache_hits_total[1h])) / (sum(rate(cache_hits_total[1h])) + sum(rate(cache_misses_total[1h]))) * 100` |

---

## 🔍 Essential PromQL Queries

### 1. Real-time Total Requests per Second (RPS)
```promql
sum(rate(http_requests_total[1m]))
```

### 2. Error Rate Percentage (5xx)
```promql
(sum(rate(http_requests_total{status=~"5.."}[2m])) / sum(rate(http_requests_total[2m]))) * 100
```

### 3. Top 5 Conditions by Triage Volume
```promql
topk(5, sum(rate(triage_predictions_total[10m])) by (condition))
```
