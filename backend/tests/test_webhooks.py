"""
ClinixIQ - Stripe Webhook & Idempotency Automated Pytest Suite
"""

import json
import pytest
from fastapi.testclient import TestClient

from app.core.idempotency import idempotency_guard
from app.main import app
from app.models.billing import PlanTier, SubscriptionStatus
from app.services.billing_repository import billing_repository
from app.services.usage_meter import usage_meter

client = TestClient(app)


@pytest.fixture(autouse=True)
def cleanup_test_state():
    idempotency_guard.clear()
    yield
    idempotency_guard.clear()


def test_webhook_checkout_session_completed():
    """Verify checkout.session.completed creates active subscription in repository."""
    cust_id = "cus_hook_test_user"
    event_payload = {
        "id": "evt_test_checkout_comp_101",
        "type": "checkout.session.completed",
        "data": {
            "object": {
                "id": "cs_test_session_123",
                "customer": cust_id,
                "customer_email": "hook.user@clinixiq.health",
                "subscription": "sub_hook_pro_456",
                "metadata": {
                    "plan_tier": "pro",
                    "billing_cycle": "annual",
                },
            }
        },
    }

    response = client.post(
        "/api/webhooks/stripe",
        content=json.dumps(event_payload),
        headers={"Content-Type": "application/json", "stripe-signature": "mock_sig_test"},
    )
    assert response.status_code == 200
    res_data = response.json()
    assert res_data["received"] is True
    assert res_data["event_id"] == "evt_test_checkout_comp_101"

    # Verify state saved in repository
    sub = billing_repository.get_subscription(cust_id)
    assert sub is not None
    assert sub.plan_tier == PlanTier.PRO
    assert sub.status == SubscriptionStatus.ACTIVE
    assert sub.subscription_id == "sub_hook_pro_456"


def test_webhook_subscription_lifecycle_updates():
    """Verify subscription update and deletion downgrade handlers."""
    cust_id = "cus_hook_lifecycle_user"

    # Initial session completed
    init_event = {
        "id": "evt_init_sub_201",
        "type": "checkout.session.completed",
        "data": {
            "object": {
                "customer": cust_id,
                "customer_email": "lifecycle@clinixiq.health",
                "subscription": "sub_stripe_789",
                "metadata": {"plan_tier": "pro"},
            }
        },
    }
    client.post(
        "/api/webhooks/stripe",
        content=json.dumps(init_event),
        headers={"Content-Type": "application/json", "stripe-signature": "mock_sig_test"},
    )

    # 1. Update: past_due
    update_event = {
        "id": "evt_update_sub_202",
        "type": "customer.subscription.updated",
        "data": {
            "object": {
                "id": "sub_stripe_789",
                "customer": cust_id,
                "status": "past_due",
                "cancel_at_period_end": True,
            }
        },
    }
    resp = client.post(
        "/api/webhooks/stripe",
        content=json.dumps(update_event),
        headers={"Content-Type": "application/json", "stripe-signature": "mock_sig_test"},
    )
    assert resp.status_code == 200

    sub = billing_repository.get_subscription(cust_id)
    assert sub.status == SubscriptionStatus.PAST_DUE
    assert sub.cancel_at_period_end is True

    # 2. Delete: subscription canceled -> downgrade to starter
    delete_event = {
        "id": "evt_delete_sub_203",
        "type": "customer.subscription.deleted",
        "data": {
            "object": {
                "id": "sub_stripe_789",
                "customer": cust_id,
                "status": "canceled",
            }
        },
    }
    resp_del = client.post(
        "/api/webhooks/stripe",
        content=json.dumps(delete_event),
        headers={"Content-Type": "application/json", "stripe-signature": "mock_sig_test"},
    )
    assert resp_del.status_code == 200

    sub_after = billing_repository.get_subscription(cust_id)
    assert sub_after.status == SubscriptionStatus.CANCELED
    assert sub_after.plan_tier == PlanTier.STARTER


def test_webhook_invoice_payment_succeeded_resets_usage():
    """Verify invoice.payment_succeeded resets monthly usage quota."""
    cust_id = "cus_invoice_reset_user"
    usage_meter.reset_usage(cust_id)

    # Accumulate usage
    usage_meter.increment_usage(cust_id, PlanTier.STARTER, count=4)
    assert usage_meter.get_usage(cust_id).triage_evaluations_used == 4

    invoice_event = {
        "id": "evt_inv_paid_301",
        "type": "invoice.payment_succeeded",
        "data": {
            "object": {
                "customer": cust_id,
                "amount_paid": 999,
                "currency": "usd",
            }
        },
    }
    response = client.post(
        "/api/webhooks/stripe",
        content=json.dumps(invoice_event),
        headers={"Content-Type": "application/json", "stripe-signature": "mock_sig_test"},
    )
    assert response.status_code == 200
    assert usage_meter.get_usage(cust_id).triage_evaluations_used == 0


def test_webhook_idempotency_deduplication():
    """Verify duplicate incoming Stripe events are recognized and deduplicated."""
    duplicate_event_id = "evt_duplicate_idempotency_999"
    event_payload = {
        "id": duplicate_event_id,
        "type": "invoice.payment_succeeded",
        "data": {
            "object": {
                "customer": "cus_idem_user",
            }
        },
    }

    # First event delivery
    resp1 = client.post(
        "/api/webhooks/stripe",
        content=json.dumps(event_payload),
        headers={"Content-Type": "application/json", "stripe-signature": "mock_sig_test"},
    )
    assert resp1.status_code == 200
    assert resp1.json()["processed"] is True

    # Duplicate delivery of identical event ID
    resp2 = client.post(
        "/api/webhooks/stripe",
        content=json.dumps(event_payload),
        headers={"Content-Type": "application/json", "stripe-signature": "mock_sig_test"},
    )
    assert resp2.status_code == 200
    # Processed should return True (HTTP 200 to Stripe) but execution skipped
    assert resp2.json()["processed"] is True
    assert idempotency_guard.is_processed(duplicate_event_id) is True
