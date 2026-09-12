"""
Unit tests for ClinixIQ Chaos Engineering and Fault Injection Engine.
Validates experiment lifecycle, steady state probes, MTTR measurement, recovery, and cleanup hooks.
"""

import importlib.util
from pathlib import Path
import time
import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
chaos_path = REPO_ROOT / "chaos" / "chaos_engine.py"
spec = importlib.util.spec_from_file_location("chaos_engine_mod", str(chaos_path))
chaos_mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(chaos_mod)

ChaosFaultType = chaos_mod.ChaosFaultType
ExperimentStatus = chaos_mod.ExperimentStatus
SteadyStateMetrics = chaos_mod.SteadyStateMetrics
ChaosExecutionReport = chaos_mod.ChaosExecutionReport
ChaosExperiment = chaos_mod.ChaosExperiment
ChaosEngine = chaos_mod.ChaosEngine


class DummyPassingExperiment(ChaosExperiment):
    def __init__(self):
        super().__init__(
            name="Dummy Pass Test",
            description="Simulates successful fault injection and rapid recovery",
            fault_type=ChaosFaultType.ERROR_INJECTION,
            duration_seconds=0.1,
        )
        self.fault_active = False
        self.heal_called = False

    def inject_fault(self) -> None:
        self.fault_active = True

    def heal_fault(self) -> None:
        self.fault_active = False
        self.heal_called = True

    def probe_steady_state(self, phase: str) -> SteadyStateMetrics:
        if phase == "during_fault":
            return SteadyStateMetrics(
                phase=phase,
                timestamp=time.time(),
                availability_percent=90.0,
                p95_latency_ms=120.0,
                error_rate_percent=10.0,
                healthy=True,
            )
        return SteadyStateMetrics(
            phase=phase,
            timestamp=time.time(),
            availability_percent=100.0,
            p95_latency_ms=25.0,
            error_rate_percent=0.0,
            healthy=True,
        )


class UnhealthyBaselineExperiment(ChaosExperiment):
    def __init__(self):
        super().__init__(
            name="Unhealthy Baseline",
            description="Fails before fault injection due to degraded initial state",
            fault_type=ChaosFaultType.REDIS_DISCONNECT,
            duration_seconds=0.1,
        )

    def inject_fault(self) -> None:
        pass

    def heal_fault(self) -> None:
        pass

    def probe_steady_state(self, phase: str) -> SteadyStateMetrics:
        return SteadyStateMetrics(
            phase=phase,
            timestamp=time.time(),
            availability_percent=50.0,
            p95_latency_ms=999.0,
            error_rate_percent=50.0,
            healthy=False,
        )


class NeverRecoveringExperiment(ChaosExperiment):
    def __init__(self):
        super().__init__(
            name="Never Recovering",
            description="Fails because system does not heal post-fault",
            fault_type=ChaosFaultType.NETWORK_LATENCY,
            duration_seconds=0.1,
        )

    def inject_fault(self) -> None:
        pass

    def heal_fault(self) -> None:
        pass

    def probe_steady_state(self, phase: str) -> SteadyStateMetrics:
        if phase == "pre_fault":
            return SteadyStateMetrics(phase=phase, timestamp=time.time(), availability_percent=100.0, p95_latency_ms=20.0, error_rate_percent=0.0, healthy=True)
        return SteadyStateMetrics(phase=phase, timestamp=time.time(), availability_percent=20.0, p95_latency_ms=2000.0, error_rate_percent=80.0, healthy=False)


class FaultExceptionExperiment(ChaosExperiment):
    def __init__(self):
        super().__init__(
            name="Fault Crash",
            description="Ensures cleanup is executed even if fault injection explodes",
            fault_type=ChaosFaultType.TRAFFIC_SPIKE,
            duration_seconds=0.1,
        )
        self.cleanup_invoked = False

    def inject_fault(self) -> None:
        raise ValueError("Simulated fault injection failure")

    def heal_fault(self) -> None:
        self.cleanup_invoked = True

    def probe_steady_state(self, phase: str) -> SteadyStateMetrics:
        return SteadyStateMetrics(phase=phase, timestamp=time.time(), availability_percent=100.0, p95_latency_ms=10.0, error_rate_percent=0.0, healthy=True)


def test_chaos_enums_and_dataclasses():
    assert ChaosFaultType.REDIS_DISCONNECT.value == "redis_disconnect"
    assert ChaosFaultType.NETWORK_LATENCY.value == "network_latency"
    assert ChaosFaultType.TRAFFIC_SPIKE.value == "traffic_spike"
    assert ChaosFaultType.ERROR_INJECTION.value == "error_injection"

    assert ExperimentStatus.PENDING.value == "pending"
    assert ExperimentStatus.RUNNING.value == "running"
    assert ExperimentStatus.PASSED.value == "passed"
    assert ExperimentStatus.FAILED.value == "failed"

    metric = SteadyStateMetrics(
        phase="pre_fault",
        timestamp=1000.0,
        availability_percent=99.9,
        p95_latency_ms=18.5,
        error_rate_percent=0.1,
        healthy=True,
    )
    assert metric.phase == "pre_fault"
    assert metric.healthy is True


def test_successful_chaos_lifecycle():
    exp = DummyPassingExperiment()
    report = exp.execute()

    assert report.status == ExperimentStatus.PASSED
    assert report.hypothesis_met is True
    assert exp.heal_called is True
    assert len(report.steady_states) == 3  # pre, during, post
    assert report.mttr_seconds >= 0.0
    assert report.failure_reason is None


def test_unhealthy_baseline_abort():
    exp = UnhealthyBaselineExperiment()
    report = exp.execute()

    assert report.status == ExperimentStatus.FAILED
    assert report.hypothesis_met is False
    assert "Baseline steady state is unhealthy" in (report.failure_reason or "")
    assert len(report.steady_states) == 1


def test_fault_exception_triggers_cleanup():
    exp = FaultExceptionExperiment()
    report = exp.execute()

    assert report.status == ExperimentStatus.FAILED
    assert "Simulated fault injection failure" in (report.failure_reason or "")
    assert exp.cleanup_invoked is True


def test_chaos_engine_orchestration():
    engine = ChaosEngine()
    assert len(engine.experiments) == 0

    exp1 = DummyPassingExperiment()
    exp2 = FaultExceptionExperiment()

    engine.register(exp1)
    engine.register(exp2)
    assert len(engine.experiments) == 2

    reports = engine.run_all()
    assert len(reports) == 2
    assert reports[0].status == ExperimentStatus.PASSED
    assert reports[1].status == ExperimentStatus.FAILED
