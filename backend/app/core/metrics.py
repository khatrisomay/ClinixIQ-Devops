import time
from collections.abc import Callable

from fastapi import Request, Response
from prometheus_client import (
    CONTENT_TYPE_LATEST,
    REGISTRY,
    Counter,
    Gauge,
    Histogram,
    generate_latest,
)

# Core HTTP Metrics
HTTP_REQUESTS_TOTAL = Counter(
    "http_requests_total",
    "Total count of HTTP requests processed by ClinixIQ API",
    ["method", "endpoint", "status"],
)

HTTP_REQUEST_DURATION_SECONDS = Histogram(
    "http_request_duration_seconds",
    "HTTP request latency in seconds",
    ["method", "endpoint"],
    buckets=[0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1.0, 2.5, 5.0],
)

# Clinical Triage Domain Metrics
TRIAGE_PREDICTIONS_TOTAL = Counter(
    "triage_predictions_total",
    "Total AI clinical triage predictions evaluated",
    ["condition", "severity", "emergency"],
)

MODEL_INFERENCE_DURATION_SECONDS = Histogram(
    "model_inference_duration_seconds",
    "Duration of pure ML model triage inference in seconds",
    ["model_version"],
    buckets=[0.005, 0.01, 0.025, 0.05, 0.1, 0.25, 0.5],
)

ACTIVE_TRIAGE_SESSIONS = Gauge(
    "active_triage_sessions", "Current number of in-flight active clinical triage sessions"
)

# Caching & Infrastructure Metrics
CACHE_HITS_TOTAL = Counter(
    "cache_hits_total", "Total Redis cache hits for clinical inferences", ["cache_type"]
)

CACHE_MISSES_TOTAL = Counter(
    "cache_misses_total", "Total Redis cache misses requiring fresh ML evaluation", ["cache_type"]
)

# Commercial Monetization & Billing Metrics
ACTIVE_SUBSCRIPTIONS_TOTAL = Gauge(
    "active_subscriptions_total",
    "Current count of active paying subscriptions by tier",
    ["tier"],
)

MONTHLY_RECURRING_REVENUE_DOLLARS = Gauge(
    "monthly_recurring_revenue_dollars",
    "Estimated Monthly Recurring Revenue in USD by plan tier",
    ["tier"],
)

STRIPE_WEBHOOK_EVENTS_TOTAL = Counter(
    "stripe_webhook_events_total",
    "Total incoming Stripe webhook events evaluated",
    ["event_type", "status"],
)

STRIPE_CHECKOUT_SESSIONS_TOTAL = Counter(
    "stripe_checkout_sessions_total",
    "Total initiated Stripe checkout sessions",
    ["tier", "billing_cycle"],
)



async def prometheus_middleware(request: Request, call_next: Callable) -> Response:
    """Middleware collecting HTTP traffic metrics for Prometheus scraping."""
    endpoint = request.url.path
    # Group dynamic paths to prevent cardinality explosion
    if endpoint.startswith("/api/v1/graphs/"):
        endpoint = "/api/v1/graphs/{type}"
    elif endpoint == "/metrics" or endpoint.startswith("/docs") or endpoint.startswith("/openapi"):
        endpoint = "system"

    method = request.method
    start_time = time.time()

    if request.url.path == "/api/v1/triage/predict":
        ACTIVE_TRIAGE_SESSIONS.inc()

    try:
        response = await call_next(request)
        status = str(response.status_code)
    except Exception:
        status = "500"
        raise
    finally:
        duration = time.time() - start_time
        HTTP_REQUESTS_TOTAL.labels(method=method, endpoint=endpoint, status=status).inc()
        HTTP_REQUEST_DURATION_SECONDS.labels(method=method, endpoint=endpoint).observe(duration)
        if request.url.path == "/api/v1/triage/predict":
            ACTIVE_TRIAGE_SESSIONS.dec()

    return response


def get_metrics_response() -> Response:
    """Exposes Prometheus text exposition format."""
    return Response(content=generate_latest(REGISTRY), media_type=CONTENT_TYPE_LATEST)
