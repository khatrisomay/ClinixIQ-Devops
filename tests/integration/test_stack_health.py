import pytest
import httpx

BACKEND_BASE_URL = "http://localhost:8000"
GATEWAY_BASE_URL = "http://localhost:80"

@pytest.mark.asyncio
async def test_backend_liveness():
    """Verify backend liveness probe."""
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            res = await client.get(f"{BACKEND_BASE_URL}/healthz")
            assert res.status_code == 200
            assert res.json().get("status") == "healthy"
    except httpx.ConnectError:
        pytest.skip("Local container stack not running; skipping live network test.")

@pytest.mark.asyncio
async def test_backend_readiness():
    """Verify backend readiness probe."""
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            res = await client.get(f"{BACKEND_BASE_URL}/readyz")
            assert res.status_code == 200
            assert res.json().get("status") == "ready"
    except httpx.ConnectError:
        pytest.skip("Local container stack not running; skipping live network test.")

@pytest.mark.asyncio
async def test_live_triage_inference():
    """Test full inference pipeline with emergency condition."""
    payload = {
        "symptoms": "sharp crushing chest pressure and sudden dyspnea",
        "temperature": 99.2,
        "oxygen_level": 89
    }
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            res = await client.post(f"{BACKEND_BASE_URL}/api/v1/triage/predict", json=payload)
            assert res.status_code == 200
            data = res.json()
            assert "condition" in data
            assert data["confidence"] >= 65
            assert "Emergency" in data["severity"] or "High Alert" in data["severity"]
            assert data["inference_latency_ms"] < 150
    except httpx.ConnectError:
        pytest.skip("Local container stack not running; skipping live network test.")

@pytest.mark.asyncio
async def test_dynamic_graph_svg_stream():
    """Test streaming vector SVG endpoint."""
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            res = await client.get(f"{BACKEND_BASE_URL}/api/v1/graphs/risk-curve?condition=Viral+URI")
            assert res.status_code == 200
            assert "image/svg+xml" in res.headers["content-type"]
            assert "<svg" in res.text
            assert "</svg>" in res.text
    except httpx.ConnectError:
        pytest.skip("Local container stack not running; skipping live network test.")
