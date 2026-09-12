"""
ClinixIQ - Automated Resilience & Recovery Benchmark Report Generator
Aggregates chaos experiment telemetry, computes MTTR, assesses SLA compliance,
and generates audit-ready Markdown and JSON resilience scorecards.
"""

import argparse
from datetime import datetime, timezone
import json
import logging
import os
import sys
from typing import Any, Dict, List, Optional

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("clinixiq.resilience.reporter")


class ResilienceAuditReporter:
    def __init__(self, raw_data: Optional[Dict[str, Any]] = None):
        self.data = raw_data or {}
        self.experiments = self.data.get("experiments", [])
        self.total_experiments = len(self.experiments)

    @classmethod
    def from_file(cls, filepath: str) -> "ResilienceAuditReporter":
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
        return cls(data)

    def calculate_resilience_grade(self) -> Dict[str, Any]:
        if not self.experiments:
            return {
                "grade": "N/A",
                "score_percent": 0.0,
                "passed_count": 0,
                "failed_count": 0,
                "avg_mttr_seconds": 0.0,
                "max_mttr_seconds": 0.0,
                "sla_target_met": False,
            }

        passed = sum(1 for e in self.experiments if e.get("status") == "passed" and e.get("hypothesis_met") is True)
        failed = self.total_experiments - passed
        score_percent = round((passed / self.total_experiments) * 100, 1)

        mttr_values = [float(e.get("mttr_seconds", 0.0)) for e in self.experiments if e.get("status") == "passed"]
        avg_mttr = round(sum(mttr_values) / len(mttr_values), 2) if mttr_values else 0.0
        max_mttr = round(max(mttr_values), 2) if mttr_values else 0.0

        # Enterprise MTTR SLA target is < 5.0 seconds
        sla_target_met = (failed == 0) and (max_mttr <= 5.0)

        if score_percent >= 99.0 and max_mttr <= 2.0:
            grade = "A+"
        elif score_percent >= 90.0 and max_mttr <= 5.0:
            grade = "A"
        elif score_percent >= 80.0:
            grade = "B"
        elif score_percent >= 70.0:
            grade = "C"
        else:
            grade = "F"

        return {
            "grade": grade,
            "score_percent": score_percent,
            "passed_count": passed,
            "failed_count": failed,
            "avg_mttr_seconds": avg_mttr,
            "max_mttr_seconds": max_mttr,
            "sla_target_met": sla_target_met,
        }

    def generate_markdown(self) -> str:
        resilience = self.calculate_resilience_grade()
        timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")

        lines = [
            "# ClinixIQ Enterprise Chaos Engineering & Resilience Benchmark Audit",
            f"**Audit Timestamp:** `{timestamp}`  ",
            f"**Platform Target:** `ClinixIQ Microservices Platform`  ",
            f"**Overall Resilience Grade:** `{resilience['grade']}` ({resilience['score_percent']}%)  ",
            f"**Disaster Recovery SLA Met (< 5s MTTR):** `{'PASS' if resilience['sla_target_met'] else 'FAIL'}`  ",
            "",
            "## 1. Executive Resilience Summary",
            "",
            "| Metric | Value | Baseline SLA Target | Status |",
            "| :--- | :--- | :--- | :--- |",
            f"| Total Chaos Scenarios | `{self.total_experiments}` | N/A | Evaluated |",
            f"| Scenarios Passed | `{resilience['passed_count']}` | 100% | {'✔' if resilience['failed_count'] == 0 else '✘'} |",
            f"| Scenarios Failed | `{resilience['failed_count']}` | 0 | {'✔' if resilience['failed_count'] == 0 else '✘'} |",
            f"| Average MTTR | `{resilience['avg_mttr_seconds']}s` | < 3.0s | {'✔' if resilience['avg_mttr_seconds'] <= 3.0 else 'WARN'} |",
            f"| Maximum MTTR Observed | `{resilience['max_mttr_seconds']}s` | < 5.0s | {'✔' if resilience['max_mttr_seconds'] <= 5.0 else 'FAIL'} |",
            f"| Resilience Score | `{resilience['score_percent']}%` | ≥ 95.0% | {'✔' if resilience['score_percent'] >= 95.0 else 'FAIL'} |",
            "",
            "## 2. Chaos Experiment Telemetry Breakdown",
            "",
            "| Experiment Name | Injected Fault Type | Status | Hypothesis Met | Duration (s) | MTTR (s) |",
            "| :--- | :--- | :--- | :--- | :--- | :--- |",
        ]

        for exp in self.experiments:
            name = exp.get("experiment_name", "Unknown")
            fault = exp.get("fault_type", "unknown")
            status = exp.get("status", "unknown").upper()
            hyp = "✔ True" if exp.get("hypothesis_met") else "✘ False"
            dur = exp.get("duration_seconds", 0.0)
            mttr = exp.get("mttr_seconds", 0.0)
            lines.append(f"| **{name}** | `{fault}` | `{status}` | {hyp} | `{dur}s` | `{mttr}s` |")

        lines.extend([
            "",
            "## 3. Steady State Observations & Latency Telemetry",
            "",
        ])

        for exp in self.experiments:
            name = exp.get("experiment_name", "Unknown")
            states = exp.get("steady_states", [])
            lines.append(f"### Scenario: {name}")
            if not states:
                lines.append("*(No steady state telemetry points captured)*")
                continue

            lines.append("| Phase | Availability | P95 Latency | Error Rate | System Healthy |")
            lines.append("| :--- | :--- | :--- | :--- | :--- |")
            for s in states:
                phase = s.get("phase", "n/a")
                avail = f"{s.get('availability_percent', 0.0)}%"
                p95 = f"{s.get('p95_latency_ms', 0.0)} ms"
                err = f"{s.get('error_rate_percent', 0.0)}%"
                healthy = "✔ Yes" if s.get("healthy") else "✘ No"
                lines.append(f"| `{phase}` | {avail} | {p95} | {err} | {healthy} |")
            lines.append("")

        lines.extend([
            "## 4. Architectural Resilience Recommendations",
            "- **Circuit Breakers:** Ensure Redis fallback and exponential retry backoffs remain active under connection storms.",
            "- **Autoscaling Policy:** Confirm Kubernetes HPA triggers when request duration P95 exceeds 500ms.",
            "- **Failover Routing:** Upstream ingress rate-limiting must prevent cascade 503s to critical clinical triage endpoints.",
            "",
            "---",
            "*Report auto-generated by ClinixIQ Resilience Verification Engine.*",
        ])

        return "
".join(lines) + "
"

    def export_report(self, markdown_path: Optional[str] = None, json_path: Optional[str] = None) -> None:
        if markdown_path:
            os.makedirs(os.path.dirname(os.path.abspath(markdown_path)), exist_ok=True)
            with open(markdown_path, "w", encoding="utf-8") as f:
                f.write(self.generate_markdown())
            logger.info(f"Generated Markdown resilience audit report at: {markdown_path}")

        if json_path:
            os.makedirs(os.path.dirname(os.path.abspath(json_path)), exist_ok=True)
            payload = {
                "audit_timestamp": datetime.now(timezone.utc).isoformat(),
                "summary": self.calculate_resilience_grade(),
                "raw_report": self.data,
            }
            with open(json_path, "w", encoding="utf-8") as f:
                json.dump(payload, f, indent=2)
            logger.info(f"Generated JSON resilience scorecard at: {json_path}")


def main():
    parser = argparse.ArgumentParser(description="ClinixIQ Resilience Report Generator")
    parser.add_argument("--input", required=True, help="Input raw JSON chaos execution file")
    parser.add_argument("--markdown", default=None, help="Target markdown audit file path")
    parser.add_argument("--json", default=None, help="Target JSON scorecard file path")
    args = parser.parse_args()

    reporter = ResilienceAuditReporter.from_file(args.input)
    reporter.export_report(markdown_path=args.markdown, json_path=args.json)


if __name__ == "__main__":
    main()
