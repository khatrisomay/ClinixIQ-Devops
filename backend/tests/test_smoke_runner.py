"""
Unit tests for ClinixIQ Automated Smoke Testing Runner.
Validates HTTP probing, retries, exponential backoff, assertion validators, and metrics calculation.
"""

import importlib.util
import io
import json
import sys
from pathlib import Path
from unittest.mock import patch
import urllib.error

import pytest

# Load smoke_runner module directly by filepath to avoid namespace collisions with backend/tests
REPO_ROOT = Path(__file__).resolve().parent.parent.parent
smoke_path = REPO_ROOT / "tests" / "smoke" / "smoke_runner.py"
spec = importlib.util.spec_from_file_location("smoke_runner_mod", str(smoke_path))
smoke_mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(smoke_mod)

SmokeRunner = smoke_mod.SmokeRunner
SmokeTestResult = smoke_mod.SmokeTestResult


class MockHTTPResponse:
    def __init__(self, status: int, body: dict):
        self.status = status
        self._body = json.dumps(body).encode("utf-8")

    def read(self):
        return self._body

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass


def test_smoke_test_result_dataclass():
    res = SmokeTestResult(
        name="Health Probe",
        endpoint="/healthz",
        method="GET",
        status="PASS",
        status_code=200,
        duration_ms=12.5,
        details={"attempt": 1},
    )
    assert res.name == "Health Probe"
    assert res.endpoint == "/healthz"
    assert res.status == "PASS"
    assert res.status_code == 200
    assert res.error is None
    assert res.duration_ms == 12.5


def test_smoke_runner_initialization():
    runner = SmokeRunner(base_url="http://testapi.local:8000/", timeout=3.5, retries=5, retry_delay=0.1)
    assert runner.base_url == "http://testapi.local:8000"
    assert runner.timeout == 3.5
    assert runner.retries == 5
    assert runner.retry_delay == 0.1
    assert runner.results == []


@patch("urllib.request.urlopen")
def test_smoke_runner_successful_check(mock_urlopen):
    mock_urlopen.return_value = MockHTTPResponse(200, {"status": "ok", "service": "clinixiq"})

    runner = SmokeRunner(base_url="http://localhost:8000", retries=2, retry_delay=0.01)
    result = runner.check("Liveness", "/healthz", expected_status=200)

    assert result.status == "PASS"
    assert result.status_code == 200
    assert result.error is None
    assert result.details["attempt"] == 1
    assert result.details["response"] == {"status": "ok", "service": "clinixiq"}
    assert len(runner.results) == 1


@patch("urllib.request.urlopen")
def test_smoke_runner_custom_validator(mock_urlopen):
    mock_urlopen.return_value = MockHTTPResponse(200, {"version": "2.4.0", "healthy": True})
    runner = SmokeRunner(retries=1)

    # Passing validator
    res_pass = runner.check(
        "Version Check",
        "/version",
        validator=lambda data, res: data.get("healthy") is True,
    )
    assert res_pass.status == "PASS"

    # Failing validator
    res_fail = runner.check(
        "Version Check Fail",
        "/version",
        validator=lambda data, res: data.get("version") == "1.0.0",
    )
    assert res_fail.status == "FAIL"
    assert "Custom assertion validator failed" in res_fail.error

    # Exception in validator
    res_exc = runner.check(
        "Version Check Exc",
        "/version",
        validator=lambda data, res: data["non_existent_key"]["sub"],
    )
    assert res_exc.status == "FAIL"
    assert "Validator exception" in res_exc.error


@patch("urllib.request.urlopen")
def test_smoke_runner_expected_http_error(mock_urlopen):
    mock_urlopen.side_effect = urllib.error.HTTPError(
        url="http://localhost:8000/protected",
        code=401,
        msg="Unauthorized",
        hdrs={},
        fp=io.BytesIO(b"{}"),
    )

    runner = SmokeRunner(retries=1)
    result = runner.check("Auth Guard", "/protected", expected_status=401)
    assert result.status == "PASS"
    assert result.status_code == 401


@patch("urllib.request.urlopen")
def test_smoke_runner_retry_backoff_recovery(mock_urlopen):
    responses = [
        urllib.error.URLError("Connection reset"),
        MockHTTPResponse(200, {"status": "recovered"}),
    ]
    mock_urlopen.side_effect = responses

    runner = SmokeRunner(retries=3, retry_delay=0.01)
    result = runner.check("Resilience Test", "/api/retry", expected_status=200)

    assert result.status == "PASS"
    assert result.details["attempt"] == 2
    assert mock_urlopen.call_count == 2


@patch("urllib.request.urlopen")
def test_smoke_runner_exhausted_retries_fail(mock_urlopen):
    mock_urlopen.side_effect = urllib.error.URLError("Connection refused")

    runner = SmokeRunner(retries=2, retry_delay=0.01)
    result = runner.check("Failed Service", "/api/down", expected_status=200)

    assert result.status == "FAIL"
    assert result.status_code is None
    assert "Connection refused" in result.error
    assert result.details["attempts"] == 2


def test_smoke_runner_summary_and_exit_code():
    runner = SmokeRunner()
    runner.results = [
        SmokeTestResult("T1", "/p1", "GET", "PASS", 200, 10.0),
        SmokeTestResult("T2", "/p2", "GET", "PASS", 200, 20.0),
        SmokeTestResult("T3", "/p3", "GET", "FAIL", 500, 30.0, error="Server Error"),
    ]

    summary = runner.get_summary()
    assert summary["total"] == 3
    assert summary["passed"] == 2
    assert summary["failed"] == 1
    assert summary["pass_rate_percent"] == 66.7
    assert summary["avg_latency_ms"] == 20.0
    assert runner.print_summary() == 1

    # Only pass
    runner.results = [SmokeTestResult("T1", "/p1", "GET", "PASS", 200, 10.0)]
    assert runner.print_summary() == 0
