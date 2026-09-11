"""
ClinixIQ - Comprehensive Unit Test Suite for Commercial Billing Engine
"""

import pytest
from fastapi.testclient import TestClient

from app.core.billing_config import billing_settings
from app.main import app
from app.models.billing import (
    BillingCycle,
    PlanTier,
    SubscriptionDetails,
    SubscriptionStatus,
)
from app.services.billing_repository import billing_repository
from app.services.stripe_service import stripe_service
from app.services.usage_meter import usage_meter

client = TestClient(app)


def test_list_plans_catalog():
    """Verify plan catalog returns Starter, Pro, and Enterprise configurations."""
    response = client.get("/api/billing/plans")
    assert response.status_code == 200
    plans = response.json()
    assert len(plans) == 3

    tiers = [p["tier"] for p in plans]
    assert "starter" in tiers
    assert "pro" in tiers
    assert "enterprise" in tiers

    pro_plan = next(p for p in plans if p["tier"] == "pro")
    assert pro_plan["price_monthly"] == 9.99
    assert pro_plan["triage_quota_monthly"] == -1
    assert pro_plan["priority_inference"] is True


def test_create_checkout_session_mock():
    """Verify Stripe Checkout Session initialization in offline mock mode."""
    payload = {
        "customer_email": "jane.doe@example.com",
        "plan_tier": "pro",
        "billing_cycle": "monthly",
    }
    response = client.post("/api/billing/create-checkout-session", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["session_id"].startswith("cs_")
    assert "checkout_url" in data
    assert data["plan_tier"] == "pro"
    assert data["billing_cycle"] == "monthly"


def test_create_starter_free_checkout():
    """Starter tier should return instant mock session without Stripe external charge."""
    payload = {
        "customer_email": "free.user@example.com",
        "plan_tier": "starter",
        "billing_cycle": "monthly",
    }
    response = client.post("/api/billing/create-checkout-session", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["session_id"].startswith("cs_free_")


def test_customer_portal_session_mock():
    """Verify Customer Billing Portal URL generation."""
    payload = {
        "customer_id": "cus_test_12345",
        "return_url": "http://localhost:3000/billing",
    }
    response = client.post("/api/billing/customer-portal", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "portal_url" in data
    assert "cus_test_12345" in data["portal_url"]


def test_billing_repository_crud():
    """Test subscription repository persistence and multi-index lookup."""
    test_sub = SubscriptionDetails(
        customer_id="cus_test_repo_user",
        customer_email="repo.user@clinixiq.health",
        subscription_id="sub_stripe_abc123",
        plan_tier=PlanTier.PRO,
        billing_cycle=BillingCycle.ANNUAL,
        status=SubscriptionStatus.ACTIVE,
    )

    # Save
    saved = billing_repository.save_subscription(test_sub)
    assert saved.customer_id == "cus_test_repo_user"

    # Get by ID
    fetched = billing_repository.get_subscription("cus_test_repo_user")
    assert fetched is not None
    assert fetched.plan_tier == PlanTier.PRO
    assert fetched.billing_cycle == BillingCycle.ANNUAL

    # Lookup by Email
    by_email = billing_repository.get_subscription_by_email("repo.user@clinixiq.health")
    assert by_email is not None
    assert by_email.customer_id == "cus_test_repo_user"

    # Lookup by Stripe Subscription ID
    by_sub_id = billing_repository.get_subscription_by_stripe_id("sub_stripe_abc123")
    assert by_sub_id is not None
    assert by_sub_id.customer_id == "cus_test_repo_user"

    # Update Status
    updated = billing_repository.update_status("cus_test_repo_user", SubscriptionStatus.CANCELED)
    assert updated.status == SubscriptionStatus.CANCELED

    # Delete
    deleted = billing_repository.delete_subscription("cus_test_repo_user")
    assert deleted is True
    assert billing_repository.get_subscription("cus_test_repo_user") is None


def test_usage_meter_quota_tracking():
    """Test usage metering, counter increments, and quota exceedance."""
    cust_id = "cus_usage_test_patient"
    usage_meter.reset_usage(cust_id)

    # Initial state
    record = usage_meter.get_usage(cust_id, PlanTier.STARTER)
    assert record.triage_evaluations_used == 0
    assert record.quota_limit == 5
    assert record.quota_exceeded is False

    # Increment 3 queries
    record = usage_meter.increment_usage(cust_id, PlanTier.STARTER, count=3)
    assert record.triage_evaluations_used == 3
    assert record.quota_exceeded is False

    # Check permission
    allowed, _ = usage_meter.check_quota(cust_id, PlanTier.STARTER)
    assert allowed is True

    # Increment past quota (reach 5)
    usage_meter.increment_usage(cust_id, PlanTier.STARTER, count=2)
    allowed, record = usage_meter.check_quota(cust_id, PlanTier.STARTER)
    assert allowed is False
    assert record.triage_evaluations_used == 5

    # Pro plan should be unlimited
    allowed_pro, pro_record = usage_meter.check_quota(cust_id, PlanTier.PRO)
    assert allowed_pro is True
    assert pro_record.quota_limit == -1


def test_triage_quota_guard_402_enforcement():
    """Verify HTTP 402 Payment Required is enforced on triage endpoint when quota exceeded."""
    guarded_customer = "cus_guarded_patient_99"
    usage_meter.reset_usage(guarded_customer)

    # Ensure customer is on Starter tier
    billing_repository.save_subscription(
        SubscriptionDetails(
            customer_id=guarded_customer,
            customer_email="guarded@clinixiq.health",
            plan_tier=PlanTier.STARTER,
            status=SubscriptionStatus.ACTIVE,
        )
    )

    # Saturate quota
    usage_meter.increment_usage(guarded_customer, PlanTier.STARTER, count=5)

    # Attempt triage evaluation
    payload = {
        "symptoms": "intermittent headache and eye strain",
        "duration_days": 2,
        "temperature": 98.6,
    }
    response = client.post(
        "/api/v1/triage/predict",
        json=payload,
        headers={"X-Customer-ID": guarded_customer},
    )
    assert response.status_code == 402
    assert "quota exceeded" in response.json()["detail"].lower()

    # Upgrade to Pro
    billing_repository.update_status(guarded_customer, SubscriptionStatus.ACTIVE, tier=PlanTier.PRO)

    # Retry triage evaluation with Pro tier
    retry_response = client.post(
        "/api/v1/triage/predict",
        json=payload,
        headers={"X-Customer-ID": guarded_customer},
    )
    assert retry_response.status_code == 200
    assert retry_response.headers.get("X-Plan-Tier") == "pro"
    assert retry_response.headers.get("X-Usage-Remaining") == "unlimited"
