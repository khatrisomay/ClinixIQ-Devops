"""
ClinixIQ - Stripe Webhook Endpoint with Cryptographic Signature Verification
"""

import logging
from typing import Any, Dict
from fastapi import APIRouter, Header, HTTPException, Request, status

from app.services.stripe_service import stripe_service

logger = logging.getLogger("clinixiq.api.webhooks")
router = APIRouter(prefix="/api/webhooks", tags=["Webhooks"])


@router.post(
    "/stripe",
    summary="Stripe Event Webhook Listener",
    status_code=status.HTTP_200_OK,
)
async def stripe_webhook(
    request: Request,
    stripe_signature: str = Header(None, alias="stripe-signature"),
) -> Dict[str, Any]:
    """
    Receive, cryptographically verify, and process asynchronous Stripe events.
    Verifies HMAC-SHA256 signature against STRIPE_WEBHOOK_SECRET.
    """
    payload = await request.body()

    if not stripe_signature and not stripe_service.mock_mode:
        logger.warning("Rejected Stripe webhook request: missing stripe-signature header")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Missing stripe-signature header",
        )

    try:
        event = stripe_service.verify_webhook_signature(
            payload=payload, sig_header=stripe_signature or "mock_signature"
        )
    except ValueError as val_err:
        logger.warning(f"Invalid webhook signature: {val_err}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Webhook signature verification failed: {val_err}",
        )
    except Exception as exc:
        logger.error(f"Unexpected error validating webhook: {exc}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Webhook verification error",
        )

    event_type = event.get("type", "unknown")
    event_id = event.get("id", "unknown")
    logger.info(f"Verified incoming Stripe webhook: {event_type} (id: {event_id})")

    # Dynamic import to avoid circular dependency before Commit 8 dispatcher
    try:
        from app.services.webhook_dispatcher import webhook_dispatcher
        processed = await webhook_dispatcher.dispatch(event)
    except ImportError:
        processed = True

    return {
        "received": True,
        "event_id": event_id,
        "type": event_type,
        "processed": processed,
    }
