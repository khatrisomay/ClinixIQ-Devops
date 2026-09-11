"""
ClinixIQ - Commercial Billing & Subscription API Routes
"""

import logging
from typing import Dict, List, Optional
from fastapi import APIRouter, HTTPException, status

from app.core.billing_config import billing_settings
from app.models.billing import (
    CheckoutSessionRequest,
    CheckoutSessionResponse,
    CustomerPortalRequest,
    CustomerPortalResponse,
    PlanInfo,
    PlanTier,
    SubscriptionDetails,
    SubscriptionStatus,
    UsageRecord,
)
from app.services.billing_repository import billing_repository
from app.services.stripe_service import stripe_service
from app.services.usage_meter import usage_meter

logger = logging.getLogger("clinixiq.api.billing")
router = APIRouter(prefix="/api/billing", tags=["Commercial Billing"])


@router.get("/plans", response_model=List[PlanInfo], summary="List all SaaS pricing tiers")
async def list_plans() -> List[PlanInfo]:
    """Retrieve catalog of available clinical tiers, pricing, and quota limits."""
    return list(billing_settings.PLANS.values())


@router.post(
    "/create-checkout-session",
    response_model=CheckoutSessionResponse,
    summary="Create Stripe Checkout Session",
)
async def create_checkout_session(payload: CheckoutSessionRequest) -> CheckoutSessionResponse:
    """Initialize a Stripe Checkout Session for subscription purchase."""
    try:
        session_resp = stripe_service.create_checkout_session(
            customer_email=payload.customer_email,
            plan_tier=payload.plan_tier,
            billing_cycle=payload.billing_cycle,
            customer_id=payload.customer_id,
            success_url=payload.success_url,
            cancel_url=payload.cancel_url,
        )
        return session_resp
    except ValueError as val_err:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(val_err)
        )
    except Exception as exc:
        logger.error(f"Error creating checkout session: {exc}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to initialize checkout session",
        )


@router.post(
    "/customer-portal",
    response_model=CustomerPortalResponse,
    summary="Access Stripe Customer Billing Portal",
)
async def customer_portal(payload: CustomerPortalRequest) -> CustomerPortalResponse:
    """Generate authenticated URL to manage billing, payment methods, and invoices."""
    try:
        portal_resp = stripe_service.create_customer_portal_session(
            customer_id=payload.customer_id,
            return_url=payload.return_url,
        )
        return portal_resp
    except Exception as exc:
        logger.error(f"Error accessing customer portal: {exc}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to access customer billing portal",
        )


@router.get(
    "/subscription/{customer_id}",
    response_model=SubscriptionDetails,
    summary="Get customer subscription status",
)
async def get_subscription(customer_id: str) -> SubscriptionDetails:
    """Fetch active subscription tier and billing status for a customer."""
    sub = billing_repository.get_subscription(customer_id)
    if not sub:
        # Default fallback to Starter free tier
        return SubscriptionDetails(
            customer_id=customer_id,
            customer_email=f"{customer_id}@clinixiq.local",
            plan_tier=PlanTier.STARTER,
            status=SubscriptionStatus.ACTIVE,
        )
    return sub


@router.get(
    "/usage/{customer_id}",
    response_model=UsageRecord,
    summary="Get current monthly usage quota status",
)
async def get_usage(customer_id: str, tier: Optional[PlanTier] = None) -> UsageRecord:
    """Inspect triage query consumption against monthly tier quota."""
    if not tier:
        sub = billing_repository.get_subscription(customer_id)
        tier = sub.plan_tier if sub else PlanTier.STARTER

    return usage_meter.get_usage(customer_id, tier)
