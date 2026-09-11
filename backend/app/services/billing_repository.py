"""
ClinixIQ - Redis-Backed Subscription State & Customer Mapping Repository
"""

import json
import logging
from datetime import datetime, timezone
from typing import Dict, Optional

from app.core.redis import redis_client
from app.models.billing import (
    BillingCycle,
    PlanTier,
    SubscriptionDetails,
    SubscriptionStatus,
)

logger = logging.getLogger("clinixiq.billing.repository")


class BillingRepository:
    def __init__(self):
        # In-memory fallback dictionary if Redis is unreachable
        self._memory_subs: Dict[str, SubscriptionDetails] = {}
        self._memory_email_index: Dict[str, str] = {}
        self._memory_stripe_sub_index: Dict[str, str] = {}

    def _sub_key(self, customer_id: str) -> str:
        return f"clinixiq:sub:{customer_id}"

    def _email_key(self, email: str) -> str:
        return f"clinixiq:email_to_sub:{email.lower().strip()}"

    def _stripe_sub_key(self, stripe_sub_id: str) -> str:
        return f"clinixiq:sub_id_to_cust:{stripe_sub_id}"

    def save_subscription(self, sub: SubscriptionDetails) -> SubscriptionDetails:
        """Persist subscription details to Redis and update lookup indices."""
        sub.updated_at = datetime.now(timezone.utc)
        payload = sub.model_dump_json()

        # Update in-memory fallback
        self._memory_subs[sub.customer_id] = sub
        self._memory_email_index[sub.customer_email.lower().strip()] = sub.customer_id
        if sub.subscription_id:
            self._memory_stripe_sub_index[sub.subscription_id] = sub.customer_id

        # Update Redis
        if redis_client.is_connected() and redis_client.client:
            try:
                pipe = redis_client.client.pipeline()
                pipe.set(self._sub_key(sub.customer_id), payload)
                pipe.set(self._email_key(sub.customer_email), sub.customer_id)
                if sub.subscription_id:
                    pipe.set(self._stripe_sub_key(sub.subscription_id), sub.customer_id)
                pipe.execute()
            except Exception as exc:
                logger.warning(f"Redis write error during save_subscription: {exc}")

        return sub

    def get_subscription(self, customer_id: str) -> Optional[SubscriptionDetails]:
        """Fetch subscription details by customer_id."""
        if redis_client.is_connected() and redis_client.client:
            try:
                data = redis_client.client.get(self._sub_key(customer_id))
                if data:
                    raw = json.loads(data)
                    return SubscriptionDetails.model_validate(raw)
            except Exception as exc:
                logger.warning(f"Redis read error in get_subscription: {exc}")

        return self._memory_subs.get(customer_id)

    def get_subscription_by_email(self, email: str) -> Optional[SubscriptionDetails]:
        """Fetch subscription details using customer email."""
        cleaned_email = email.lower().strip()
        customer_id = None

        if redis_client.is_connected() and redis_client.client:
            try:
                customer_id = redis_client.client.get(self._email_key(cleaned_email))
            except Exception as exc:
                logger.warning(f"Redis read error in get_subscription_by_email: {exc}")

        if not customer_id:
            customer_id = self._memory_email_index.get(cleaned_email)

        if customer_id:
            return self.get_subscription(customer_id)
        return None

    def get_subscription_by_stripe_id(self, subscription_id: str) -> Optional[SubscriptionDetails]:
        """Fetch subscription details using Stripe subscription ID."""
        customer_id = None

        if redis_client.is_connected() and redis_client.client:
            try:
                customer_id = redis_client.client.get(self._stripe_sub_key(subscription_id))
            except Exception as exc:
                logger.warning(f"Redis read error in get_subscription_by_stripe_id: {exc}")

        if not customer_id:
            customer_id = self._memory_stripe_sub_index.get(subscription_id)

        if customer_id:
            return self.get_subscription(customer_id)
        return None

    def update_status(
        self,
        customer_id: str,
        status: SubscriptionStatus,
        tier: Optional[PlanTier] = None,
        billing_cycle: Optional[BillingCycle] = None,
    ) -> Optional[SubscriptionDetails]:
        """Update subscription status or tier for an existing customer."""
        sub = self.get_subscription(customer_id)
        if not sub:
            return None

        sub.status = status
        if tier:
            sub.plan_tier = tier
        if billing_cycle:
            sub.billing_cycle = billing_cycle

        return self.save_subscription(sub)

    def delete_subscription(self, customer_id: str) -> bool:
        """Remove subscription and indices."""
        sub = self.get_subscription(customer_id)
        if sub:
            self._memory_subs.pop(customer_id, None)
            self._memory_email_index.pop(sub.customer_email.lower().strip(), None)
            if sub.subscription_id:
                self._memory_stripe_sub_index.pop(sub.subscription_id, None)

            if redis_client.is_connected() and redis_client.client:
                try:
                    pipe = redis_client.client.pipeline()
                    pipe.delete(self._sub_key(customer_id))
                    pipe.delete(self._email_key(sub.customer_email))
                    if sub.subscription_id:
                        pipe.delete(self._stripe_sub_key(sub.subscription_id))
                    pipe.execute()
                except Exception as exc:
                    logger.warning(f"Redis delete error: {exc}")
            return True
        return False


billing_repository = BillingRepository()
