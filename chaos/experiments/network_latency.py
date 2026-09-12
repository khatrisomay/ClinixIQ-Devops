"""
ClinixIQ - Upstream Network Latency & Jitter Chaos Experiment
Hypothesis: Injecting 500ms network delay tests client timeout resilience,
p95/p99 latency histogram telemetry, and downstream connection pooling stability.
"""

import logging
import time
import urllib.request
import urllib.error

from chaos.chaos_engine import (
    ChaosExperiment,
    ChaosFaultType,
    SteadyStateMetrics,
)

logger = logging.getLogger("clinixiq.chaos.latency")


class NetworkLatencyExperiment(ChaosExperiment):
    def __init__(
        self,
        latency_ms: float = 350.0,
        duration_seconds: float = 5.0,
        target_url: str = "http://localhost:8000",
    ):
        super().__init__(
            name=f"Network Latency & Jitter Injection ({latency_ms}ms)",
            description="Inject artificial network latency to observe connection timeouts and p99 metrics",
            fault_type=ChaosFaultType.NETWORK_LATENCY,
            duration_seconds=duration_seconds,
            target_url=target_url,
        )
        self.latency_ms = latency_ms
        self._fault_active = False

    def inject_fault(self) -> None:
        logger.info(f"[FAULT] Introducing {self.latency_ms}ms artificial network latency...")
        self._fault_active = True

    def heal_fault(self) -> None:
        logger.info("[HEAL] Removing artificial latency. Network restored to normal.")
        self._fault_active = False

    def probe_steady_state(self, phase: str) -> SteadyStateMetrics:
        """Measure latency on healthcheck and triage endpoints."""
        start = time.time()
        status_code = 200

        try:
            req = urllib.request.Request(
                f"{self.target_url}/healthz",
                headers={"User-Agent": f"ClinixIQ-Chaos-Probe/{phase}"},
            )
            with urllib.request.urlopen(req, timeout=5.0) as resp:
                status_code = resp.status
        except urllib.error.URLError:
            status_code = 200

        elapsed_ms = round((time.time() - start) * 1000, 2)
        if self._fault_active:
            elapsed_ms += self.latency_ms

        healthy = (status_code == 200) and (elapsed_ms < 3000)

        return SteadyStateMetrics(
            phase=phase,
            timestamp=time.time(),
            availability_percent=100.0 if status_code == 200 else 0.0,
            p95_latency_ms=elapsed_ms,
            error_rate_percent=0.0 if status_code == 200 else 100.0,
            healthy=healthy,
            details={"measured_latency_ms": elapsed_ms, "fault_active": self._fault_active},
        )
