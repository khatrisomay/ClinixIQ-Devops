"""
ClinixIQ - Commercial Billing & Subscription Pydantic Schemas
"""

from datetime import datetime, timezone
from enum import Enum
from typing import List, Optional
from pydantic import BaseModel, ConfigDict, Field


class PlanTier(str, Enum):
    STARTER = "starter"
    PRO = "pro"
    ENTERPRISE = "enterprise"


class BillingCycle(str, Enum):
    MONTHLY = "monthly"
    ANNUAL = "annual"


class SubscriptionStatus(str, Enum):
    ACTIVE = "active"
    PAST_DUE = "past_due"
    CANCELED = "canceled"
    TRIALING = "trialing"
    INCOMPLETE = "incomplete"
    NONE = "none"


class PlanInfo(BaseModel):
    tier: PlanTier
    name: str
    price_monthly: float
    price_annual_monthly_rate: float
    triage_quota_monthly: int  # -1 represents unlimited
    features: List[str]
    priority_inference: bool
    stripe_price_id_monthly: Optional[str] = None
    stripe_price_id_annual: Optional[str] = None


class CheckoutSessionRequest(BaseModel):
    customer_email: str
    plan_tier: PlanTier
    billing_cycle: BillingCycle = BillingCycle.MONTHLY
    customer_id: Optional[str] = None
    success_url: Optional[str] = None
    cancel_url: Optional[str] = None


class CheckoutSessionResponse(BaseModel):
    session_id: str
    checkout_url: str
    plan_tier: PlanTier
    billing_cycle: BillingCycle
    mode: str = "mock"  # "mock" or "live"
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class CustomerPortalRequest(BaseModel):
    customer_id: str
    return_url: Optional[str] = None


class CustomerPortalResponse(BaseModel):
    portal_url: str


class SubscriptionDetails(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    customer_id: str
    customer_email: str
    plan_tier: PlanTier = PlanTier.STARTER
    billing_cycle: BillingCycle = BillingCycle.MONTHLY
    status: SubscriptionStatus = SubscriptionStatus.ACTIVE
    subscription_id: Optional[str] = None
    current_period_start: Optional[datetime] = None
    current_period_end: Optional[datetime] = None
    cancel_at_period_end: bool = False
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class UsageRecord(BaseModel):
    customer_id: str
    month_key: str
    triage_evaluations_used: int = 0
    quota_limit: int = 5
    quota_exceeded: bool = False
    last_evaluated_at: Optional[datetime] = None
