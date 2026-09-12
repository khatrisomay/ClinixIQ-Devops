"""
ClinixIQ - Automated Production Smoke Testing Engine
Validates critical API endpoints, health probes, and contracts with exponential backoff.
"""

import argparse
import json
import logging
import sys
import time
from dataclasses import asdict, dataclass, field
from typing import Any, Callable, Dict, List, Optional
import urllib.request
import urllib.error

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("clinixiq.smoke")


@dataclass
class SmokeTestResult:
    name: str
    endpoint: str
    method: str
    status: str  # "PASS" | "FAIL" | "SKIPPED"
    status_code: Optional[int] = None
    duration_ms: float = 0.0
    error: Optional[str] = None
    details: Dict[str, Any] = field(default_factory=dict)


class SmokeRunner:
    def __init__(
        self,
        base_url: str = "http://localhost:8000",
        timeout: float = 10.0,
        retries: int = 3,
        retry_delay: float = 1.0,
    ):
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.retries = retries
        self.retry_delay = retry_delay
        self.results: List[SmokeTestResult] = []

    def check(
        self,
        name: str,
        path: str,
        expected_status: int = 200,
        method: str = "GET",
        payload: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
        validator: Optional[Callable[[Dict[str, Any], SmokeTestResult], bool]] = None,
    ) -> SmokeTestResult:
        """Execute a single smoke test check with exponential backoff retries."""
        url = f"{self.base_url}{path}"
        req_headers = {"User-Agent": "ClinixIQ-SmokeRunner/1.0", "Accept": "application/json"}
        if headers:
            req_headers.update(headers)

        data = None
        if payload is not None:
            data = json.dumps(payload).encode("utf-8")
            req_headers["Content-Type"] = "application/json"

        last_error = None
        status_code = None
        duration_ms = 0.0

        for attempt in range(1, self.retries + 1):
            start_time = time.time()
            try:
                req = urllib.request.Request(url, data=data, headers=req_headers, method=method)
                with urllib.request.urlopen(req, timeout=self.timeout) as response:
                    status_code = response.status
                    duration_ms = round((time.time() - start_time) * 1000, 2)
                    body_bytes = response.read()
                    parsed_json = {}
                    try:
                        parsed_json = json.loads(body_bytes.decode("utf-8"))
                    except Exception:
                        pass

                    if status_code == expected_status:
                        result = SmokeTestResult(
                            name=name,
                            endpoint=path,
                            method=method,
                            status="PASS",
                            status_code=status_code,
                            duration_ms=duration_ms,
                            details={"attempt": attempt, "response": parsed_json},
                        )

                        if validator:
                            try:
                                if not validator(parsed_json, result):
                                    result.status = "FAIL"
                                    result.error = "Custom assertion validator failed"
                            except Exception as val_err:
                                result.status = "FAIL"
                                result.error = f"Validator exception: {val_err}"

                        self.results.append(result)
                        logger.info(f"✔ [{result.status}] {name} ({path}) - {status_code} in {duration_ms}ms")
                        return result

            except urllib.error.HTTPError as http_err:
                status_code = http_err.code
                duration_ms = round((time.time() - start_time) * 1000, 2)
                if status_code == expected_status:
                    # Expected failure status code (e.g. 402, 422)
                    result = SmokeTestResult(
                        name=name,
                        endpoint=path,
                        method=method,
                        status="PASS",
                        status_code=status_code,
                        duration_ms=duration_ms,
                        details={"attempt": attempt},
                    )
                    self.results.append(result)
                    logger.info(f"✔ [PASS] {name} ({path}) - Expected {status_code} in {duration_ms}ms")
                    return result
                last_error = f"HTTP {http_err.code}: {http_err.reason}"
            except Exception as exc:
                last_error = str(exc)

            if attempt < self.retries:
                sleep_time = self.retry_delay * (2 ** (attempt - 1))
                time.sleep(sleep_time)

        # If loop exits without returning, test failed
        result = SmokeTestResult(
            name=name,
            endpoint=path,
            method=method,
            status="FAIL",
            status_code=status_code,
            duration_ms=duration_ms,
            error=last_error or "Retries exhausted",
            details={"attempts": self.retries},
        )
        self.results.append(result)
        logger.error(f"✘ [FAIL] {name} ({path}) - Error: {result.error}")
        return result

    def get_summary(self) -> Dict[str, Any]:
        total = len(self.results)
        passed = sum(1 for r in self.results if r.status == "PASS")
        failed = sum(1 for r in self.results if r.status == "FAIL")
        skipped = sum(1 for r in self.results if r.status == "SKIPPED")
        avg_latency = (
            round(sum(r.duration_ms for r in self.results) / total, 2) if total > 0 else 0.0
        )
        return {
            "total": total,
            "passed": passed,
            "failed": failed,
            "skipped": skipped,
            "pass_rate_percent": round((passed / total) * 100, 1) if total > 0 else 0.0,
            "avg_latency_ms": avg_latency,
            "results": [asdict(r) for r in self.results],
        }

    def print_summary(self) -> int:
        summary = self.get_summary()
        print("\n" + "=" * 60)
        print("  ClinixIQ Production Smoke Testing Summary")
        print("=" * 60)
        print(f"  Target Base URL : {self.base_url}")
        print(f"  Total Checks    : {summary['total']}")
        print(f"  Passed          : {summary['passed']} ✔")
        print(f"  Failed          : {summary['failed']} ✘")
        print(f"  Pass Rate       : {summary['pass_rate_percent']}%")
        print(f"  Average Latency : {summary['avg_latency_ms']} ms")
        print("=" * 60 + "\n")
        return 0 if summary["failed"] == 0 else 1


def main():
    parser = argparse.ArgumentParser(description="ClinixIQ Smoke Test Runner")
    parser.add_argument("--url", default="http://localhost:8000", help="Base URL of ClinixIQ API")
    parser.add_argument("--timeout", type=float, default=5.0, help="Per-request timeout in seconds")
    parser.add_argument("--retries", type=int, default=3, help="Max retry attempts")
    parser.add_argument("--report", default=None, help="File path to save JSON smoke report")
    args = parser.parse_args()

    runner = SmokeRunner(base_url=args.url, timeout=args.timeout, retries=args.retries)

    # Core Smoke Probe Suite
    runner.check("Liveness Probe", "/healthz", expected_status=200)
    runner.check("Readiness Probe", "/readyz", expected_status=200)
    runner.check("System Health Status", "/api/v1/health", expected_status=200)
    runner.check("Prometheus Telemetry", "/metrics", expected_status=200)
    runner.check("SaaS Pricing Catalog", "/api/billing/plans", expected_status=200)

    if args.report:
        with open(args.report, "w", encoding="utf-8") as f:
            json.dump(runner.get_summary(), f, indent=2)
        logger.info(f"Saved smoke test report to {args.report}")

    sys.exit(runner.print_summary())


if __name__ == "__main__":
    main()
