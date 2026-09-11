"""
ClinixIQ - Stripe & Commercial Billing Configuration
"""

import os
from typing import Dict
from app.models.billing import PlanInfo, PlanTier


class BillingSettings:
    def __init__(self):
        self.STRIPE_SECRET_KEY: str = os.getenv("STRIPE_SECRET_KEY", "")
        self.STRIPE_PUBLISHABLE_KEY: str = os.getenv("STRIPE_PUBLISHABLE_KEY", "pk_test_clinixiq_mock_public_key")
        self.STRIPE_WEBHOOK_SECRET: str = os.getenv("STRIPE_WEBHOOK_SECRET", "whsec_clinixiq_mock_webhook_secret")
        self.CURRENCY: str = os.getenv("STRIPE_CURRENCY", "usd").lower()

        # Mock mode auto-detection: enabled if live key is absent or placeholder
        self.MOCK_MODE: bool = (
            not self.STRIPE_SECRET_KEY
            or self.STRIPE_SECRET_KEY.startswith("clinixiq")
            or self.STRIPE_SECRET_KEY.startswith("sk_test_mock")
            or os.getenv("STRIPE_MOCK_MODE", "true").lower() == "true"
        )

        # Plan Price IDs (Stripe catalog mappings)
        self.PRICE_PRO_MONTHLY: str = os.getenv("STRIPE_PRICE_PRO_MONTHLY", "price_pro_monthly_mock")
        self.PRICE_PRO_ANNUAL: str = os.getenv("STRIPE_PRICE_PRO_ANNUAL", "price_pro_annual_mock")
        self.PRICE_ENTERPRISE_MONTHLY: str = os.getenv("STRIPE_PRICE_ENT_MONTHLY", "price_ent_monthly_mock")
        self.PRICE_ENTERPRISE_ANNUAL: str = os.getenv("STRIPE_PRICE_ENT_ANNUAL", "price_ent_annual_mock")

        # Frontend Return URLs
        self.CHECKOUT_SUCCESS_URL: str = os.getenv(
            "STRIPE_SUCCESS_URL", "http://localhost:3000/?session_id={CHECKOUT_SESSION_ID}&status=success"
        )
        self.CHECKOUT_CANCEL_URL: str = os.getenv(
            "STRIPE_CANCEL_URL", "http://localhost:3000/?canceled=true"
        )
        self.PORTAL_RETURN_URL: str = os.getenv(
            "STRIPE_PORTAL_RETURN_URL", "http://localhost:3000/"
        )

        # Quota limits by tier (-1 represents unlimited)
        self.TIER_QUOTAS: Dict[PlanTier, int] = {
            PlanTier.STARTER: 5,
            PlanTier.PRO: -1,
            PlanTier.ENTERPRISE: 10000,
        }

        # Canonical Plan Catalog
        self.PLANS: Dict[PlanTier, PlanInfo] = {
            PlanTier.STARTER: PlanInfo(
                tier=PlanTier.STARTER,
                name="Starter Triage",
                price_monthly=0.00,
                price_annual_monthly_rate=0.00,
                triage_quota_monthly=5,
                features=[
                    "5 AI symptom triage assessments / month",
                    "Top 3 differential disease matches",
                    "Standard home-care triage guidance",
                    "Community support access",
                ],
                priority_inference=False,
                stripe_price_id_monthly=None,
                stripe_price_id_annual=None,
            ),
            PlanTier.PRO: PlanInfo(
                tier=PlanTier.PRO,
                name="Pro Patient & Care",
                price_monthly=9.99,
                price_annual_monthly_rate=7.99,
                triage_quota_monthly=-1,
                features=[
                    "Unlimited AI triage queries",
                    "Exportable PDF doctor summaries",
                    "Python biomarker & risk trend curves",
                    "Priority ML inference queue (<50ms)",
                    "Chronic symptom tracking calendar",
                ],
                priority_inference=True,
                stripe_price_id_monthly=self.PRICE_PRO_MONTHLY,
                stripe_price_id_annual=self.PRICE_PRO_ANNUAL,
            ),
            PlanTier.ENTERPRISE: PlanInfo(
                tier=PlanTier.ENTERPRISE,
                name="Clinic / Telehealth API",
                price_monthly=149.00,
                price_annual_monthly_rate=119.00,
                triage_quota_monthly=10000,
                features=[
                    "10,000 API triage evaluations / month",
                    "Dedicated Kubernetes ingress endpoint",
                    "HIPAA-aligned anonymization pipeline",
                    "Custom disease probability weighting",
                    "99.9% uptime SLA & priority engineer support",
                ],
                priority_inference=True,
                stripe_price_id_monthly=self.PRICE_ENTERPRISE_MONTHLY,
                stripe_price_id_annual=self.PRICE_ENTERPRISE_ANNUAL,
            ),
        }


billing_settings = BillingSettings()
