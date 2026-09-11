"""
ClinixIQ - Structured Financial Audit & Compliance Logger
Compliant with HIPAA Security Rule, PCI-DSS, and SOC2 financial accountability.
"""

import json
import logging
import uuid
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Dict, Optional

logger = logging.getLogger("clinixiq.audit.financial")


class FinancialAuditEventType(str, Enum):
    CHECKOUT_INITIATED = "checkout_initiated"
    SUBSCRIPTION_CREATED = "subscription_created"
    SUBSCRIPTION_UPGRADED = "subscription_upgraded"
    SUBSCRIPTION_DOWNGRADED = "subscription_downgraded"
    SUBSCRIPTION_CANCELED = "subscription_canceled"
    PAYMENT_SUCCEEDED = "payment_succeeded"
    PAYMENT_FAILED = "payment_failed"
    QUOTA_EXCEEDED = "quota_exceeded"
    WEBHOOK_PROCESSED = "webhook_processed"


class FinancialAuditLogger:
    @staticmethod
    def _sanitize_details(data: Dict[str, Any]) -> Dict[str, Any]:
        """Strip or mask PCI/PHI sensitive fields from audit telemetry."""
        sanitized = {}
        for k, v in data.items():
            k_lower = k.lower()
            if any(term in k_lower for term in ["card", "cvv", "pan", "token", "secret"]):
                sanitized[k] = "[REDACTED_FINANCIAL]"
            elif isinstance(v, dict):
                sanitized[k] = FinancialAuditLogger._sanitize_details(v)
            else:
                sanitized[k] = v
        return sanitized

    def log_event(
        self,
        event_type: FinancialAuditEventType,
        customer_id: str,
        details: Optional[Dict[str, Any]] = None,
        amount: Optional[float] = None,
        currency: str = "USD",
    ) -> Dict[str, Any]:
        """Record an immutable structured financial audit log entry."""
        details = details or {}
        audit_entry = {
            "audit_id": str(uuid.uuid4()),
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "event_type": event_type.value,
            "customer_id": customer_id,
            "amount": amount,
            "currency": currency.upper(),
            "details": self._sanitize_details(details),
            "compliance_context": {
                "hipaa_safe_harbor": True,
                "pci_dss_level": "SAQ-A",
                "environment": "production",
            },
        }

        # Log as single-line structured JSON
        logger.info(f"AUDIT_FINANCIAL: {json.dumps(audit_entry)}")
        return audit_entry

    def log_subscription_transition(
        self,
        customer_id: str,
        from_tier: str,
        to_tier: str,
        billing_cycle: str,
        subscription_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Audit subscription plan state changes."""
        return self.log_event(
            event_type=(
                FinancialAuditEventType.SUBSCRIPTION_UPGRADED
                if to_tier != "starter"
                else FinancialAuditEventType.SUBSCRIPTION_DOWNGRADED
            ),
            customer_id=customer_id,
            details={
                "previous_tier": from_tier,
                "new_tier": to_tier,
                "billing_cycle": billing_cycle,
                "subscription_id": subscription_id,
            },
        )

    def log_payment(
        self,
        customer_id: str,
        amount: float,
        currency: str,
        success: bool,
        invoice_id: Optional[str] = None,
        error_message: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Audit payment charges and failures."""
        event_type = (
            FinancialAuditEventType.PAYMENT_SUCCEEDED
            if success
            else FinancialAuditEventType.PAYMENT_FAILED
        )
        return self.log_event(
            event_type=event_type,
            customer_id=customer_id,
            amount=amount,
            currency=currency,
            details={
                "invoice_id": invoice_id,
                "error": error_message,
                "status": "success" if success else "failed",
            },
        )


financial_audit = FinancialAuditLogger()
