import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.models.schemas import TriageRequest


@pytest.fixture(scope="session")
def client():
    """FastAPI TestClient fixture."""
    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture
def emergency_request():
    """Sample emergency cardiopulmonary presentation."""
    return TriageRequest(
        symptoms="severe substernal crushing chest pressure radiating to left arm and jaw",
        temperature=98.6,
        heart_rate=118,
        oxygen_level=88,
        duration_days=1,
    )


@pytest.fixture
def mild_uri_request():
    """Sample mild respiratory presentation."""
    return TriageRequest(
        symptoms="mild itchy throat, occasional dry cough, post-nasal drip",
        temperature=99.1,
        heart_rate=74,
        oxygen_level=99,
        duration_days=3,
    )
