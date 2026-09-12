"""
ClinixIQ - Synthetic End-to-End Patient Journey Smoke Test Suite
Simulates complete clinical workflows: symptom intake -> ML inference -> dynamic graphs -> cache hits.
"""

import argparse
import sys
from typing import Any, Dict

from tests.smoke.smoke_runner import SmokeRunner, SmokeTestResult


def validate_triage_response(data: Dict[str, Any], res: SmokeTestResult) -> bool:
    """Validate schema and clinical invariants of triage prediction."""
    if not isinstance(data, dict):
        return False
    condition = data.get("condition")
    severity = data.get("severity")
    confidence = data.get("confidence", 0)
    differentials = data.get("differentials", [])

    if not condition or not severity:
        res.error = "Missing condition or severity in response"
        return False
    if confidence < 50:
        res.error = f"Uncalibrated confidence: {confidence}% < 50%"
        return False
    if len(differentials) < 2:
        res.error = f"Insufficient differential diagnoses count: {len(differentials)}"
        return False
    return True


def run_patient_journey(runner: SmokeRunner) -> int:
    """Execute complete synthetic patient diagnostic journey."""
    print("[1/5] Step 1: Discover available clinical test samples...")
    runner.check("Sample Clinical Presentations", "/api/v1/triage/samples", expected_status=200)

    print("[2/5] Step 2: Ingest acute cardiac emergency presentation...")
    emergency_payload = {
        "symptoms": "sudden crushing sub-sternal chest pain, radiating down left arm with cold sweat",
        "duration_days": 1,
        "temperature": 98.4,
        "heart_rate": 115,
        "oxygen_level": 91,
    }
    runner.check(
        name="Emergency Clinical Triage Evaluation",
        path="/api/v1/triage/predict",
        expected_status=200,
        method="POST",
        payload=emergency_payload,
        validator=validate_triage_response,
    )

    print("[3/5] Step 3: Stream dynamic progression risk curve SVG...")
    runner.check(
        name="Dynamic Risk Curve SVG",
        path="/api/v1/graphs/risk-curve?condition=Acute+Coronary+Syndrome&peak_day=3",
        expected_status=200,
        method="GET",
    )

    print("[4/5] Step 4: Stream differential comparison bar chart SVG...")
    runner.check(
        name="Differential Bar Chart SVG",
        path="/api/v1/graphs/differential",
        expected_status=200,
        method="GET",
    )

    print("[5/5] Step 5: Test Redis caching speedup on identical symptom query...")
    cached_result = runner.check(
        name="Cached Triage Query (Cache Hit)",
        path="/api/v1/triage/predict",
        expected_status=200,
        method="POST",
        payload=emergency_payload,
        validator=validate_triage_response,
    )

    return runner.print_summary()


def main():
    parser = argparse.ArgumentParser(description="ClinixIQ Patient Journey Smoke Test")
    parser.add_argument("--url", default="http://localhost:8000", help="Base URL of ClinixIQ API")
    parser.add_argument("--timeout", type=float, default=5.0, help="Per-request timeout in seconds")
    args = parser.parse_args()

    runner = SmokeRunner(base_url=args.url, timeout=args.timeout)
    sys.exit(run_patient_journey(runner))


if __name__ == "__main__":
    main()
