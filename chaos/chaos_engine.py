"""
ClinixIQ - Chaos Engineering & Resilience Validation Framework
Orchestrates automated hypothesis testing, fault injection, and recovery validation.
"""

import abc
import logging
import time
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("clinixiq.chaos")


class ChaosFaultType(str, Enum):
    REDIS_DISCONNECT = "redis_disconnect"
    NETWORK_LATENCY = "network_latency"
    TRAFFIC_SPIKE = "traffic_spike"
    ERROR_INJECTION = "error_injection"


class ExperimentStatus(str, Enum):
    PENDING = "pending"
    RUNNING = "running"
    PASSED = "passed"
    FAILED = "failed"


@dataclass
class SteadyStateMetrics:
    phase: str  # "pre_fault" | "during_fault" | "post_heal"
    timestamp: float
    availability_percent: float
    p95_latency_ms: float
    error_rate_percent: float
    healthy: bool
    details: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ChaosExecutionReport:
    experiment_name: str
    fault_type: ChaosFaultType
    status: ExperimentStatus
    hypothesis_met: bool
    duration_seconds: float
    mttr_seconds: float  # Mean Time To Recovery
    steady_states: List[SteadyStateMetrics] = field(default_factory=list)
    failure_reason: Optional[str] = None


class ChaosExperiment(abc.ABC):
    def __init__(
        self,
        name: str,
        description: str,
        fault_type: ChaosFaultType,
        duration_seconds: float = 10.0,
        target_url: str = "http://localhost:8000",
    ):
        self.name = name
        self.description = description
        self.fault_type = fault_type
        self.duration_seconds = duration_seconds
        self.target_url = target_url.rstrip("/")
        self.status = ExperimentStatus.PENDING

    @abc.abstractmethod
    def inject_fault(self) -> None:
        """Apply active fault injection to target subsystem."""
        pass

    @abc.abstractmethod
    def heal_fault(self) -> None:
        """Teardown fault injection and restore baseline state."""
        pass

    @abc.abstractmethod
    def probe_steady_state(self, phase: str) -> SteadyStateMetrics:
        """Evaluate Steady State Hypothesis metrics (latency, error rate)."""
        pass

    def execute(self) -> ChaosExecutionReport:
        """Execute full chaos lifecycle: probe baseline -> inject -> observe -> heal -> verify."""
        logger.info(f"=== Starting Chaos Experiment: {self.name} ===")
        self.status = ExperimentStatus.RUNNING
        steady_states: List[SteadyStateMetrics] = []
        start_time = time.time()
        mttr_seconds = 0.0

        try:
            # 1. Probe Baseline Steady State
            logger.info("Phase 1: Probing baseline steady state before fault injection...")
            pre_metrics = self.probe_steady_state(phase="pre_fault")
            steady_states.append(pre_metrics)
            if not pre_metrics.healthy:
                raise RuntimeError("Baseline steady state is unhealthy prior to experiment.")

            # 2. Inject Fault
            logger.info(f"Phase 2: Injecting fault [{self.fault_type.value}] for {self.duration_seconds}s...")
            fault_start = time.time()
            self.inject_fault()

            # Observe system during active fault
            time.sleep(min(self.duration_seconds, 2.0))
            during_metrics = self.probe_steady_state(phase="during_fault")
            steady_states.append(during_metrics)

            remaining_sleep = max(0.0, self.duration_seconds - (time.time() - fault_start))
            if remaining_sleep > 0:
                time.sleep(remaining_sleep)

            # 3. Heal Fault
            logger.info("Phase 3: Healing fault and measuring system recovery...")
            heal_start = time.time()
            self.heal_fault()

            # Poll for recovery (MTTR)
            recovery_deadline = time.time() + 15.0
            recovered = False
            while time.time() < recovery_deadline:
                post_metrics = self.probe_steady_state(phase="post_heal")
                if post_metrics.healthy:
                    mttr_seconds = round(time.time() - heal_start, 2)
                    steady_states.append(post_metrics)
                    recovered = True
                    break
                time.sleep(0.5)

            if not recovered:
                steady_states.append(self.probe_steady_state(phase="post_heal"))
                raise RuntimeError("System failed to recover steady state within timeout.")

            total_duration = round(time.time() - start_time, 2)
            self.status = ExperimentStatus.PASSED
            logger.info(f"✔ Experiment PASSED: {self.name} (MTTR: {mttr_seconds}s)")

            return ChaosExecutionReport(
                experiment_name=self.name,
                fault_type=self.fault_type,
                status=self.status,
                hypothesis_met=True,
                duration_seconds=total_duration,
                mttr_seconds=mttr_seconds,
                steady_states=steady_states,
            )

        except Exception as exc:
            self.status = ExperimentStatus.FAILED
            total_duration = round(time.time() - start_time, 2)
            logger.error(f"✘ Experiment FAILED: {self.name} - Reason: {exc}")
            # Ensure healing even upon exception
            try:
                self.heal_fault()
            except Exception:
                pass

            return ChaosExecutionReport(
                experiment_name=self.name,
                fault_type=self.fault_type,
                status=self.status,
                hypothesis_met=False,
                duration_seconds=total_duration,
                mttr_seconds=mttr_seconds,
                steady_states=steady_states,
                failure_reason=str(exc),
            )


class ChaosEngine:
    def __init__(self):
        self.experiments: List[ChaosExperiment] = []
        self.reports: List[ChaosExecutionReport] = []

    def register(self, experiment: ChaosExperiment) -> None:
        self.experiments.append(experiment)

    def run_all(self) -> List[ChaosExecutionReport]:
        self.reports.clear()
        for exp in self.experiments:
            report = exp.execute()
            self.reports.append(report)
        return self.reports


chaos_engine = ChaosEngine()
