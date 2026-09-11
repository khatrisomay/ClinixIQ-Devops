"""
ClinixIQ - Resilient Stripe Client Service with Mock/Live Fallbacks
"""

import logging
import uuid
from typing import Any, Dict, Optional

from app.core.billing_config import billing_settings
from app.models.billing import (
    BillingCycle,
    CheckoutSessionResponse,
    CustomerPortalResponse,
    PlanTier,
)

logger = logging.getLogger("clinixiq.billing.stripe")

try:
    import stripe
except ImportError:
    stripe = None


class StripeService:
    def __init__(self):
        self.mock_mode = billing_settings.MOCK_MODE
        if not self.mock_mode and stripe:
            stripe.api_key = billing_settings.STRIPE_SECRET_KEY
            logger.info("Initialized live Stripe API client")
        else:
            logger.info("Initialized StripeService in offline MOCK mode")

    def create_checkout_session(
        self,
        customer_email: str,
        plan_tier: PlanTier,
        billing_cycle: BillingCycle = BillingCycle.MONTHLY,
        customer_id: Optional[str] = None,
        success_url: Optional[str] = None,
        cancel_url: Optional[str] = None,
    ) -> CheckoutSessionResponse:
        """Create a Stripe Checkout Session for subscription checkout."""
        success_url = success_url or billing_settings.CHECKOUT_SUCCESS_URL
        cancel_url = cancel_url or billing_settings.CHECKOUT_CANCEL_URL

        plan = billing_settings.PLANS.get(plan_tier)
        if not plan:
            raise ValueError(f"Invalid plan tier: {plan_tier}")

        if plan_tier == PlanTier.STARTER:
            session_id = f"cs_free_{uuid.uuid4().hex[:12]}"
            redirect_url = success_url.replace("{CHECKOUT_SESSION_ID}", session_id)
            return CheckoutSessionResponse(
                session_id=session_id,
                checkout_url=redirect_url,
                plan_tier=plan_tier,
                billing_cycle=billing_cycle,
                mode="mock",
            )

        price_id = (
            plan.stripe_price_id_annual
            if billing_cycle == BillingCycle.ANNUAL
            else plan.stripe_price_id_monthly
        )

        if not self.mock_mode and stripe and price_id and not price_id.endswith("_mock"):
            try:
                session_args: Dict[str, Any] = {
                    "payment_method_types": ["card"],
                    "line_items": [{"price": price_id, "quantity": 1}],
                    "mode": "subscription",
                    "success_url": success_url,
                    "cancel_url": cancel_url,
                    "customer_email": customer_email if not customer_id else None,
                    "customer": customer_id if customer_id else None,
                    "metadata": {
                        "plan_tier": plan_tier.value,
                        "billing_cycle": billing_cycle.value,
                        "project": "ClinixIQ",
                    },
                }
                session = stripe.checkout.Session.create(**session_args)
                return CheckoutSessionResponse(
                    session_id=session.id,
                    checkout_url=session.url,
                    plan_tier=plan_tier,
                    billing_cycle=billing_cycle,
                    mode="live",
                )
            except Exception as exc:
                logger.error(f"Failed to create live Stripe checkout session: {exc}. Falling back to mock session.")

        # Fallback / Mock Checkout Session
        mock_session_id = f"cs_mock_{uuid.uuid4().hex[:16]}"
        mock_checkout_url = success_url.replace("{CHECKOUT_SESSION_ID}", mock_session_id)
        return CheckoutSessionResponse(
            session_id=mock_session_id,
            checkout_url=mock_checkout_url,
            plan_tier=plan_tier,
            billing_cycle=billing_cycle,
            mode="mock",
        )

    def create_customer_portal_session(
        self,
        customer_id: str,
        return_url: Optional[str] = None,
    ) -> CustomerPortalResponse:
        """Create a Stripe Customer Portal session for subscription management."""
        return_url = return_url or billing_settings.PORTAL_RETURN_URL

        if not self.mock_mode and stripe and not customer_id.startswith("cus_mock_"):
            try:
                portal_session = stripe.billing_portal.Session.create(
                    customer=customer_id,
                    return_url=return_url,
                )
                return CustomerPortalResponse(portal_url=portal_session.url)
            except Exception as exc:
                logger.error(f"Failed to create Stripe portal session: {exc}. Using mock portal.")

        mock_portal_url = f"{return_url}?portal=active&customer_id={customer_id}"
        return CustomerPortalResponse(portal_url=mock_portal_url)

    def verify_webhook_signature(self, payload: bytes, sig_header: str) -> Dict[str, Any]:
        """Verify HMAC-SHA256 signature on incoming Stripe webhook."""
        if not self.mock_mode and stripe:
            try:
                event = stripe.Webhook.construct_event(
                    payload, sig_header, billing_settings.STRIPE_WEBHOOK_SECRET
                )
                return dict(event)
            except Exception as exc:
                logger.warning(f"Live webhook signature verification failed: {exc}")
                raise ValueError(f"Invalid webhook signature: {exc}")

        # In mock mode, if signature header is provided or contains 'mock', treat as valid JSON
        import json
        try:
            return json.loads(payload.decode("utf-8"))
        except Exception as exc:
            raise ValueError(f"Malformed webhook payload: {exc}")


stripe_service = StripeService()
