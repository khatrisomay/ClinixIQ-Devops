import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.ml.symptom_extractor import extract_symptoms
from app.ml.disease_predictor import predict_triage
from app.models.schemas import TriageRequest

client = TestClient(app)

def test_liveness_probe():
    response = client.get("/healthz")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

def test_readiness_probe():
    response = client.get("/readyz")
    assert response.status_code == 200
    assert response.json()["status"] == "ready"

def test_system_health():
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "operational"
    assert data["service"] == "clinixiq-backend-api"

def test_symptom_extraction():
    text = "Patient presenting with high fever, severe chest tightness, and hacking dry cough for 3 days."
    symptoms = extract_symptoms(text)
    assert "fever" in symptoms
    assert "chest_pain" in symptoms
    assert "cough" in symptoms

def test_emergency_triage_escalation():
    req = TriageRequest(
        symptoms="sudden onset of crushing chest pain and severe shortness of breath",
        temperature=98.6,
        oxygen_level=89
    )
    result = predict_triage(req)
    assert "Emergency" in result.severity or "High Alert" in result.severity
    assert result.confidence > 70
    assert len(result.differentials) >= 3

def test_mild_triage_prediction():
    req = TriageRequest(
        symptoms="mild sore throat and occasional cough with low energy",
        temperature=99.1
    )
    result = predict_triage(req)
    assert any(term in result.condition for term in ["Viral", "Respiratory", "Bronchitis", "Allergic"])
    assert result.confidence >= 60

def test_predict_api_endpoint():
    payload = {
        "symptoms": "throbbing headache, nausea, and sensitivity to light",
        "duration_days": 1,
        "temperature": 98.4
    }
    response = client.post("/api/v1/triage/predict", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "condition" in data
    assert "confidence" in data
    assert "differentials" in data
    assert len(data["differentials"]) > 0

def test_dynamic_graph_risk_curve_svg():
    response = client.get("/api/v1/graphs/risk-curve?condition=Influenza+Type+A&peak_day=4")
    assert response.status_code == 200
    assert "image/svg+xml" in response.headers["content-type"]
    assert "<svg" in response.text
    assert "</svg>" in response.text

def test_dynamic_differential_bar_chart_svg():
    response = client.get("/api/v1/graphs/differential")
    assert response.status_code == 200
    assert "image/svg+xml" in response.headers["content-type"]
    assert "<svg" in response.text
