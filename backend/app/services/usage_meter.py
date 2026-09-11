"""
ClinixIQ - Monthly Quota Metering & Usage-Based Rate Limiting Service
"""

import logging
from datetime import datetime, timezone
from typing import Dict, Tuple

from app.core.billing_config import billing_settings
from app.core.redis import redis_client
from app.models.billing import PlanTier, UsageRecord

logger = logging.getLogger("clinixiq.billing.usage")


class UsageMeter:
    def __init__(self):
        # In-memory dictionary fallback: {(customer_id, month_key): count}
        self._memory_usage: Dict[Tuple[str, str], int] = {}
        self._memory_last_seen: Dict[Tuple[str, str], datetime] = {}

    def _get_current_month_key(self) -> str:
        return datetime.now(timezone.utc).strftime("%Y-%m")

    def _usage_key(self, customer_id: str, month_key: str) -> str:
        return f"clinixiq:usage:{customer_id}:{month_key}"

    def get_usage(self, customer_id: str, tier: PlanTier = PlanTier.STARTER) -> UsageRecord:
        """Fetch current monthly usage and evaluate against plan quota limits."""
        month_key = self._get_current_month_key()
        limit = billing_settings.TIER_QUOTAS.get(tier, 5)
        used = 0
        last_eval = None

        if redis_client.is_connected() and redis_client.client:
            try:
                val = redis_client.client.get(self._usage_key(customer_id, month_key))
                if val:
                    used = int(val)
            except Exception as exc:
                logger.warning(f"Redis get error in UsageMeter: {exc}")

        if used == 0:
            used = self._memory_usage.get((customer_id, month_key), 0)

        last_eval = self._memory_last_seen.get((customer_id, month_key))
        exceeded = (limit != -1) and (used >= limit)

        return UsageRecord(
            customer_id=customer_id,
            month_key=month_key,
            triage_evaluations_used=used,
            quota_limit=limit,
            quota_exceeded=exceeded,
            last_evaluated_at=last_eval,
        )

    def increment_usage(
        self, customer_id: str, tier: PlanTier = PlanTier.STARTER, count: int = 1
    ) -> UsageRecord:
        """Increment customer usage counter and refresh TTL."""
        month_key = self._get_current_month_key()
        limit = billing_settings.TIER_QUOTAS.get(tier, 5)
        now = datetime.now(timezone.utc)
        used = count

        # In-memory update
        mem_key = (customer_id, month_key)
        self._memory_usage[mem_key] = self._memory_usage.get(mem_key, 0) + count
        self._memory_last_seen[mem_key] = now
        used = self._memory_usage[mem_key]

        # Redis update
        if redis_client.is_connected() and redis_client.client:
            try:
                u_key = self._usage_key(customer_id, month_key)
                pipe = redis_client.client.pipeline()
                pipe.incrby(u_key, count)
                # 60 days TTL
                pipe.expire(u_key, 5184000)
                results = pipe.execute()
                used = int(results[0])
            except Exception as exc:
                logger.warning(f"Redis incr error in UsageMeter: {exc}")

        exceeded = (limit != -1) and (used > limit)
        return UsageRecord(
            customer_id=customer_id,
            month_key=month_key,
            triage_evaluations_used=used,
            quota_limit=limit,
            quota_exceeded=exceeded,
            last_evaluated_at=now,
        )

    def check_quota(
        self, customer_id: str, tier: PlanTier = PlanTier.STARTER
    ) -> Tuple[bool, UsageRecord]:
        """Check if customer is permitted to make another triage inference."""
        record = self.get_usage(customer_id, tier)
        if record.quota_limit == -1:
            return True, record  # Unlimited tier (Pro)
        if record.triage_evaluations_used >= record.quota_limit:
            return False, record  # Quota reached
        return True, record

    def reset_usage(self, customer_id: str) -> None:
        """Reset usage for test environments or new billing cycle."""
        month_key = self._get_current_month_key()
        self._memory_usage.pop((customer_id, month_key), None)
        self._memory_last_seen.pop((customer_id, month_key), None)
        if redis_client.is_connected() and redis_client.client:
            try:
                redis_client.client.delete(self._usage_key(customer_id, month_key))
            except Exception as exc:
                logger.warning(f"Redis delete error in reset_usage: {exc}")


usage_meter = UsageMeter()
