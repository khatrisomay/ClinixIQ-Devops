"""
ClinixIQ - Chaos Engineering CLI Orchestrator
Executes resilience verification scenarios and outputs comprehensive MTTR benchmarks.
"""

import argparse
import json
import sys
from dataclasses import asdict
from typing import List

from chaos.chaos_engine import ChaosEngine, ChaosExecutionReport
from chaos.experiments.network_latency import NetworkLatencyExperiment
from chaos.experiments.redis_outage import RedisOutageExperiment
from chaos.experiments.traffic_spike import TrafficSpikeExperiment


def print_chaos_summary(reports: List[ChaosExecutionReport]) -> int:
    """Render formatted console summary table of chaos experiment outcomes."""
    print("
" + "=" * 78)
    print("  ClinixIQ Chaos Engineering & Resiliency Assessment Report")
    print("=" * 78)
    print(f"  {'Experiment Name':<44} | {'Status':<8} | {'MTTR (s)':<8} | {'Hypothesis'}")
    print("-" * 78)

    all_passed = True
    for r in reports:
        status_str = "PASSED ✔" if r.hypothesis_met else "FAILED ✘"
        hypo_str = "Met" if r.hypothesis_met else "Violated"
        if not r.hypothesis_met:
            all_passed = False
        print(f"  {r.experiment_name[:44]:<44} | {status_str:<8} | {r.mttr_seconds:<8} | {hypo_str}")

    print("=" * 78)
    total = len(reports)
    passed = sum(1 for r in reports if r.hypothesis_met)
    print(f"  Total Experiments: {total} | Passed: {passed} | Failed: {total - passed}")
    print("=" * 78 + "
")
    return 0 if all_passed else 1


def main():
    parser = argparse.ArgumentParser(description="ClinixIQ Chaos Engineering CLI")
    parser.add_argument(
        "--experiment",
        choices=["all", "redis", "latency", "spike"],
        default="all",
        help="Select specific chaos scenario to execute",
    )
    parser.add_argument(
        "--target-url",
        default="http://localhost:8000",
        help="Target base URL of ClinixIQ deployment",
    )
    parser.add_argument(
        "--duration",
        type=float,
        default=3.0,
        help="Duration in seconds for fault injection",
    )
    parser.add_argument(
        "--report",
        default=None,
        help="File path to save JSON chaos audit report",
    )
    args = parser.parse_args()

    engine = ChaosEngine()

    if args.experiment in ("all", "redis"):
        engine.register(
            RedisOutageExperiment(duration_seconds=args.duration, target_url=args.target_url)
        )
    if args.experiment in ("all", "latency"):
        engine.register(
            NetworkLatencyExperiment(duration_seconds=args.duration, target_url=args.target_url)
        )
    if args.experiment in ("all", "spike"):
        engine.register(
            TrafficSpikeExperiment(duration_seconds=args.duration, target_url=args.target_url)
        )

    reports = engine.run_all()

    if args.report:
        with open(args.report, "w", encoding="utf-8") as f:
            json.dump([asdict(r) for r in reports], f, indent=2)
        print(f"[INFO] Saved chaos audit report to {args.report}")

    sys.exit(print_chaos_summary(reports))


if __name__ == "__main__":
    main()
