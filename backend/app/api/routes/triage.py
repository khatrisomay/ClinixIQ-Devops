import hashlib
import time
from typing import Optional

from fastapi import APIRouter, Header, HTTPException, Response, status

from app.core.metrics import (
    CACHE_HITS_TOTAL,
    CACHE_MISSES_TOTAL,
    MODEL_INFERENCE_DURATION_SECONDS,
    TRIAGE_PREDICTIONS_TOTAL,
)
from app.core.redis import cache_manager
from app.ml.disease_predictor import predict_triage
from app.models.billing import PlanTier
from app.models.schemas import TriageRequest, TriageResponse
from app.services.billing_repository import billing_repository
from app.services.usage_meter import usage_meter

router = APIRouter(prefix="/api/v1/triage", tags=["Clinical Triage"])


def generate_cache_key(req: TriageRequest) -> str:
    key_raw = f"{req.symptoms.lower()}:{req.temperature}:{req.heart_rate}:{req.oxygen_level}:{req.duration_days}"
    return f"triage:{hashlib.sha256(key_raw.encode()).hexdigest()}"


@router.post(
    "/predict",
    response_model=TriageResponse,
    summary="Perform AI symptom triage and differential evaluation",
)
async def evaluate_symptoms(
    request: TriageRequest,
    response: Response,
    x_customer_id: Optional[str] = Header(None, alias="X-Customer-ID"),
):
    if not request.symptoms.strip():
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Symptoms string must not be empty",
        )

    # 1. Billing & Monthly Quota Verification
    customer_id = x_customer_id or "demo_user"
    sub = billing_repository.get_subscription(customer_id)
    tier = sub.plan_tier if sub else PlanTier.STARTER

    allowed, record = usage_meter.check_quota(customer_id, tier)
    if not allowed:
        raise HTTPException(
            status_code=status.HTTP_402_PAYMENT_REQUIRED,
            detail=(
                f"Monthly triage quota exceeded ({record.triage_evaluations_used}/{record.quota_limit} queries used). "
                "Please upgrade to Pro or Enterprise for additional capacity."
            ),
        )

    # Record usage
    updated_record = usage_meter.increment_usage(customer_id, tier)
    remaining = (
        "unlimited"
        if updated_record.quota_limit == -1
        else str(max(0, updated_record.quota_limit - updated_record.triage_evaluations_used))
    )
    response.headers["X-Plan-Tier"] = tier.value
    response.headers["X-Usage-Remaining"] = remaining

    # 2. Check cache for identical symptom presentation
    cache_key = generate_cache_key(request)
    cached_data = await cache_manager.get(cache_key)
    if cached_data:
        CACHE_HITS_TOTAL.labels(cache_type="triage_prediction").inc()
        return TriageResponse(**cached_data)

    CACHE_MISSES_TOTAL.labels(cache_type="triage_prediction").inc()

    # 3. Model Inference Execution
    start_infer = time.time()
    result = predict_triage(request)
    infer_duration = time.time() - start_infer

    MODEL_INFERENCE_DURATION_SECONDS.labels(model_version=result.model_version).observe(
        infer_duration
    )
    is_emergency = (
        "true" if "Emergency" in result.severity or "High Alert" in result.severity else "false"
    )
    TRIAGE_PREDICTIONS_TOTAL.labels(
        condition=result.condition,
        severity=result.severity,
        emergency=is_emergency,
    ).inc()

    await cache_manager.set(cache_key, result.model_dump(), ttl=1800)
    return result


@router.get("/samples", summary="Retrieve sample test cases")
async def get_samples():
    return {
        "samples": [
            {
                "label": "Cardiopulmonary Emergency",
                "symptoms": "severe chest tightness, shortness of breath, and palpitations",
            },
            {
                "label": "Standard Respiratory",
                "symptoms": "dry cough, sore throat, and mild fever for 2 days",
            },
            {
                "label": "Severe Infection / Meningeal",
                "symptoms": "stiff neck, high fever, unbearable headache and photophobia",
            },
            {
                "label": "Neurological Migraine",
                "symptoms": "throbbing headache on left temple with nausea and light sensitivity",
            },
        ]
    }
