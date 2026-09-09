def test_metrics_endpoint_exposition(client):
    """Verify that /metrics returns HTTP 200 with Prometheus text format."""
    response = client.get("/metrics")
    assert response.status_code == 200
    assert "text/plain" in response.headers["content-type"]
    text = response.text
    assert "http_requests_total" in text
    assert "http_request_duration_seconds" in text
    assert "triage_predictions_total" in text


def test_metrics_increment_on_triage(client, emergency_request):
    """Verify that making an inference records clinical metrics."""
    # Issue inference
    res = client.post("/api/v1/triage/predict", json=emergency_request.model_dump())
    assert res.status_code == 200

    # Scrape metrics
    metrics_res = client.get("/metrics")
    assert metrics_res.status_code == 200
    metrics_text = metrics_res.text
    assert "triage_predictions_total" in metrics_text
    assert "model_inference_duration_seconds_bucket" in metrics_text


def test_correlation_id_injection(client):
    """Verify X-Correlation-ID is generated and returned on API requests."""
    res = client.get("/api/v1/health")
    assert res.status_code == 200
    assert "X-Correlation-ID" in res.headers
    assert len(res.headers["X-Correlation-ID"]) > 10


def test_correlation_id_passthrough(client):
    """Verify existing X-Correlation-ID header is preserved."""
    custom_id = "test-clinixiq-trace-999"
    res = client.get("/api/v1/health", headers={"X-Correlation-ID": custom_id})
    assert res.status_code == 200
    assert res.headers["X-Correlation-ID"] == custom_id
