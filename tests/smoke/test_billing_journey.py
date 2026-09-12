"""
ClinixIQ - Synthetic End-to-End Billing & Subscription Smoke Test Suite
Simulates SaaS lifecycle: catalog discovery -> checkout -> webhook -> entitlement -> customer portal.
"""

import argparse
import sys
import uuid
from typing import Any, Dict

from tests.smoke.smoke_runner import SmokeRunner, SmokeTestResult


def run_billing_journey(runner: SmokeRunner) -> int:
    """Execute complete synthetic commercial monetization journey."""
    test_id = uuid.uuid4().hex[:8]
    customer_email = f"patient_{test_id}@clinixiq-test.health"
    customer_id = f"cus_smoke_{test_id}"

    print(f"[1/6] Step 1: Discover SaaS plans catalog...")
    runner.check("Fetch SaaS Plans Catalog", "/api/billing/plans", expected_status=200)

    print(f"[2/6] Step 2: Initialize Stripe Checkout for customer: {customer_email}...")
    checkout_payload = {
        "customer_email": customer_email,
        "customer_id": customer_id,
        "plan_tier": "pro",
        "billing_cycle": "monthly",
    }
    checkout_res = runner.check(
        name="Create Stripe Checkout Session",
        path="/api/billing/create-checkout-session",
        expected_status=200,
        method="POST",
        payload=checkout_payload,
    )

    print(f"[3/6] Step 3: Dispatch synthetic checkout.session.completed webhook...")
    webhook_event = {
        "id": f"evt_smoke_comp_{test_id}",
        "type": "checkout.session.completed",
        "data": {
            "object": {
                "id": f"cs_smoke_{test_id}",
                "customer": customer_id,
                "customer_email": customer_email,
                "subscription": f"sub_smoke_{test_id}",
                "metadata": {"plan_tier": "pro", "billing_cycle": "monthly"},
            }
        },
    }
    runner.check(
        name="Stripe Webhook Event Processing",
        path="/api/webhooks/stripe",
        expected_status=200,
        method="POST",
        payload=webhook_event,
        headers={"stripe-signature": "smoke_test_sig"},
    )

    print(f"[4/6] Step 4: Verify subscription state synchronization...")
    runner.check(
        name="Verify Subscription Entitlement",
        path=f"/api/billing/subscription/{customer_id}",
        expected_status=200,
        method="GET",
    )

    print(f"[5/6] Step 5: Verify monthly usage metering...")
    runner.check(
        name="Check Monthly Quota Usage",
        path=f"/api/billing/usage/{customer_id}?tier=pro",
        expected_status=200,
        method="GET",
    )

    print(f"[6/6] Step 6: Generate Stripe Customer Billing Portal session...")
    portal_payload = {"customer_id": customer_id}
    runner.check(
        name="Customer Billing Portal Session",
        path="/api/billing/customer-portal",
        expected_status=200,
        method="POST",
        payload=portal_payload,
    )

    return runner.print_summary()


def main():
    parser = argparse.ArgumentParser(description="ClinixIQ Billing Journey Smoke Test")
    parser.add_argument("--url", default="http://localhost:8000", help="Base URL of ClinixIQ API")
    parser.add_argument("--timeout", type=float, default=5.0, help="Per-request timeout in seconds")
    args = parser.parse_args()

    runner = SmokeRunner(base_url=args.url, timeout=args.timeout)
    sys.exit(run_billing_journey(runner))


if __name__ == "__main__":
    main()
