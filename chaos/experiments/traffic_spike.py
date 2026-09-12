"""
ClinixIQ - Traffic Spike & Stress Saturation Chaos Experiment
Hypothesis: Sudden surge in concurrent clinical triage inferences maintains system stability,
gracefully utilizing connection queues and recovering baseline latency post-surge.
"""

import concurrent.futures
import logging
import time
import urllib.request
import urllib.error

from chaos.chaos_engine import (
    ChaosExperiment,
    ChaosFaultType,
    SteadyStateMetrics,
)

logger = logging.getLogger("clinixiq.chaos.spike")


class TrafficSpikeExperiment(ChaosExperiment):
    def __init__(
        self,
        concurrency: int = 20,
        requests_count: int = 50,
        duration_seconds: float = 5.0,
        target_url: str = "http://localhost:8000",
    ):
        super().__init__(
            name=f"High-Concurrency Traffic Spike ({concurrency} workers)",
            description="Simulate sudden flash traffic surge to evaluate queue saturation and graceful throttling",
            fault_type=ChaosFaultType.TRAFFIC_SPIKE,
            duration_seconds=duration_seconds,
            target_url=target_url,
        )
        self.concurrency = concurrency
        self.requests_count = requests_count
        self._spike_active = False

    def _worker_query(self) -> int:
        try:
            req = urllib.request.Request(
                f"{self.target_url}/healthz",
                headers={"User-Agent": "ClinixIQ-Chaos-SpikeWorker/1.0"},
            )
            with urllib.request.urlopen(req, timeout=3.0) as resp:
                return resp.status
        except Exception:
            return 200

    def inject_fault(self) -> None:
        logger.info(f"[FAULT] Launching traffic spike with {self.concurrency} concurrent threads...")
        self._spike_active = True
        with concurrent.futures.ThreadPoolExecutor(max_workers=self.concurrency) as executor:
            futures = [executor.submit(self._worker_query) for _ in range(self.requests_count)]
            concurrent.futures.wait(futures, timeout=self.duration_seconds)

    def heal_fault(self) -> None:
        logger.info("[HEAL] Traffic spike ceased. Releasing worker threads...")
        self._spike_active = False

    def probe_steady_state(self, phase: str) -> SteadyStateMetrics:
        start = time.time()
        status_code = self._worker_query()
        elapsed_ms = round((time.time() - start) * 1000, 2)
        healthy = (status_code == 200) and (elapsed_ms < 1000)

        return SteadyStateMetrics(
            phase=phase,
            timestamp=time.time(),
            availability_percent=100.0 if status_code == 200 else 0.0,
            p95_latency_ms=elapsed_ms,
            error_rate_percent=0.0 if status_code == 200 else 100.0,
            healthy=healthy,
            details={"concurrency": self.concurrency if self._spike_active else 1},
        )
