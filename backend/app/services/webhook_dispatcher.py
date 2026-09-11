"""
ClinixIQ - Stripe Webhook Lifecycle Event Dispatcher
"""

import logging
from datetime import datetime, timezone
from typing import Any, Dict

from app.models.billing import (
    BillingCycle,
    PlanTier,
    SubscriptionDetails,
    SubscriptionStatus,
)
from app.services.billing_repository import billing_repository
from app.services.usage_meter import usage_meter

logger = logging.getLogger("clinixiq.billing.dispatcher")


class WebhookDispatcher:
    async def dispatch(self, event: Dict[str, Any]) -> bool:
        """Route incoming Stripe event to specialized lifecycle handler."""
        event_type = event.get("type", "")
        data_object = event.get("data", {}).get("object", {})

        # Optional idempotency check hook (wired in Commit 9)
        try:
            from app.core.idempotency import idempotency_guard
            event_id = event.get("id")
            if event_id and not idempotency_guard.claim_event(event_id):
                logger.info(f"Duplicate event {event_id} skipped via idempotency guard")
                return True
        except ImportError:
            pass

        handler_map = {
            "checkout.session.completed": self._handle_checkout_completed,
            "customer.subscription.created": self._handle_subscription_created,
            "customer.subscription.updated": self._handle_subscription_updated,
            "customer.subscription.deleted": self._handle_subscription_deleted,
            "invoice.payment_succeeded": self._handle_invoice_payment_succeeded,
            "invoice.payment_failed": self._handle_invoice_payment_failed,
        }

        handler = handler_map.get(event_type)
        if handler:
            try:
                await handler(data_object)
                logger.info(f"Successfully handled event: {event_type}")
                return True
            except Exception as exc:
                logger.error(f"Error handling event {event_type}: {exc}")
                return False
        else:
            logger.debug(f"Unhandled Stripe event type ignored: {event_type}")
            return True

    async def _handle_checkout_completed(self, session: Dict[str, Any]) -> None:
        customer_id = session.get("customer") or session.get("id")
        customer_email = session.get("customer_details", {}).get("email") or session.get("customer_email") or f"{customer_id}@clinixiq.local"
        subscription_id = session.get("subscription")

        metadata = session.get("metadata", {})
        plan_str = metadata.get("plan_tier", "pro")
        cycle_str = metadata.get("billing_cycle", "monthly")

        try:
            plan_tier = PlanTier(plan_str)
        except ValueError:
            plan_tier = PlanTier.PRO

        try:
            billing_cycle = BillingCycle(cycle_str)
        except ValueError:
            billing_cycle = BillingCycle.MONTHLY

        sub_details = SubscriptionDetails(
            customer_id=customer_id,
            customer_email=customer_email,
            subscription_id=subscription_id,
            plan_tier=plan_tier,
            billing_cycle=billing_cycle,
            status=SubscriptionStatus.ACTIVE,
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc),
        )

        billing_repository.save_subscription(sub_details)
        logger.info(f"Activated subscription for customer {customer_id} on {plan_tier.value}")

    async def _handle_subscription_created(self, sub_data: Dict[str, Any]) -> None:
        sub_id = sub_data.get("id")
        customer_id = sub_data.get("customer")
        status_str = sub_data.get("status", "active")

        sub = billing_repository.get_subscription(customer_id) or billing_repository.get_subscription_by_stripe_id(sub_id)
        if sub:
            sub.subscription_id = sub_id
            sub.status = SubscriptionStatus.ACTIVE if status_str == "active" else SubscriptionStatus.TRIALING
            billing_repository.save_subscription(sub)

    async def _handle_subscription_updated(self, sub_data: Dict[str, Any]) -> None:
        sub_id = sub_data.get("id")
        customer_id = sub_data.get("customer")
        status_str = sub_data.get("status", "active")
        cancel_at_period_end = sub_data.get("cancel_at_period_end", False)

        sub = billing_repository.get_subscription(customer_id) or billing_repository.get_subscription_by_stripe_id(sub_id)
        if sub:
            if status_str == "active":
                sub.status = SubscriptionStatus.ACTIVE
            elif status_str == "past_due":
                sub.status = SubscriptionStatus.PAST_DUE
            elif status_str in ("canceled", "unpaid"):
                sub.status = SubscriptionStatus.CANCELED

            sub.cancel_at_period_end = cancel_at_period_end
            billing_repository.save_subscription(sub)
            logger.info(f"Updated subscription {sub_id} status to {sub.status.value}")

    async def _handle_subscription_deleted(self, sub_data: Dict[str, Any]) -> None:
        sub_id = sub_data.get("id")
        customer_id = sub_data.get("customer")

        sub = billing_repository.get_subscription(customer_id) or billing_repository.get_subscription_by_stripe_id(sub_id)
        if sub:
            sub.status = SubscriptionStatus.CANCELED
            sub.plan_tier = PlanTier.STARTER
            billing_repository.save_subscription(sub)
            logger.info(f"Downgraded customer {customer_id} to STARTER following subscription deletion")

    async def _handle_invoice_payment_succeeded(self, invoice: Dict[str, Any]) -> None:
        customer_id = invoice.get("customer")
        if customer_id:
            # Payment successful, ensure active status and reset usage cycle
            sub = billing_repository.get_subscription(customer_id)
            if sub:
                sub.status = SubscriptionStatus.ACTIVE
                billing_repository.save_subscription(sub)
            usage_meter.reset_usage(customer_id)
            logger.info(f"Invoice payment succeeded for customer {customer_id}. Quota reset.")

    async def _handle_invoice_payment_failed(self, invoice: Dict[str, Any]) -> None:
        customer_id = invoice.get("customer")
        if customer_id:
            sub = billing_repository.get_subscription(customer_id)
            if sub:
                sub.status = SubscriptionStatus.PAST_DUE
                billing_repository.save_subscription(sub)
                logger.warning(f"Payment failed for customer {customer_id}. Status set to past_due.")


webhook_dispatcher = WebhookDispatcher()
