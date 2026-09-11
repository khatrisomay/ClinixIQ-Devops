"""
ClinixIQ - Webhook Idempotency & Replay Defense Service
"""

import logging
from typing import Set

from app.core.redis import redis_client

logger = logging.getLogger("clinixiq.billing.idempotency")


class IdempotencyGuard:
    def __init__(self):
        # In-memory fallback set if Redis is offline
        self._memory_processed_events: Set[str] = set()

    def _lock_key(self, event_id: str) -> str:
        return f"clinixiq:idempotency:stripe:{event_id}"

    def claim_event(self, event_id: str, ttl_seconds: int = 86400) -> bool:
        """
        Atomically claim an incoming event ID with a 24-hour TTL.
        Returns True if this is the first execution (claim acquired).
        Returns False if the event was already processed (duplicate detected).
        """
        if not event_id:
            return True

        if redis_client.is_connected() and redis_client.client:
            try:
                # Redis SET with NX=True (set if not exists) and EX=ttl_seconds
                acquired = redis_client.client.set(
                    self._lock_key(event_id), "processed", ex=ttl_seconds, nx=True
                )
                if acquired:
                    logger.debug(f"Idempotency claim acquired for Stripe event: {event_id}")
                    return True
                else:
                    logger.warning(f"Duplicate Stripe event rejected by Redis idempotency guard: {event_id}")
                    return False
            except Exception as exc:
                logger.warning(f"Redis error in IdempotencyGuard, falling back to memory: {exc}")

        # In-memory deduplication fallback
        if event_id in self._memory_processed_events:
            logger.warning(f"Duplicate Stripe event rejected by in-memory idempotency guard: {event_id}")
            return False

        self._memory_processed_events.add(event_id)
        return True

    def is_processed(self, event_id: str) -> bool:
        """Check if an event ID has already been recorded."""
        if not event_id:
            return False

        if redis_client.is_connected() and redis_client.client:
            try:
                return bool(redis_client.client.exists(self._lock_key(event_id)))
            except Exception as exc:
                logger.warning(f"Redis error in is_processed: {exc}")

        return event_id in self._memory_processed_events

    def clear(self) -> None:
        """Clear memory cache for test suite isolation."""
        self._memory_processed_events.clear()


idempotency_guard = IdempotencyGuard()
