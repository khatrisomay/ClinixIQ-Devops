import hashlib
from fastapi import APIRouter, HTTPException, status
from app.models.schemas import TriageRequest, TriageResponse
from app.ml.disease_predictor import predict_triage
from app.core.redis import cache_manager

router = APIRouter(prefix="/api/v1/triage", tags=["Clinical Triage"])

def generate_cache_key(req: TriageRequest) -> str:
    key_raw = f"{req.symptoms.lower()}:{req.temperature}:{req.heart_rate}:{req.oxygen_level}:{req.duration_days}"
    return f"triage:{hashlib.sha256(key_raw.encode()).hexdigest()}"

@router.post("/predict", response_model=TriageResponse, summary="Perform AI symptom triage and differential evaluation")
async def evaluate_symptoms(request: TriageRequest):
    if not request.symptoms.strip():
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Symptoms string must not be empty"
        )

    # Check cache for identical symptom presentation
    cache_key = generate_cache_key(request)
    cached_data = await cache_manager.get(cache_key)
    if cached_data:
        return TriageResponse(**cached_data)

    result = predict_triage(request)
    await cache_manager.set(cache_key, result.model_dump(), ttl=1800)
    return result

@router.get("/samples", summary="Retrieve sample test cases")
async def get_samples():
    return {
        "samples": [
            {"label": "Cardiopulmonary Emergency", "symptoms": "severe chest tightness, shortness of breath, and palpitations"},
            {"label": "Standard Respiratory", "symptoms": "dry cough, sore throat, and mild fever for 2 days"},
            {"label": "Severe Infection / Meningeal", "symptoms": "stiff neck, high fever, unbearable headache and photophobia"},
            {"label": "Neurological Migraine", "symptoms": "throbbing headache on left temple with nausea and light sensitivity"}
        ]
    }
