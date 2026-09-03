from fastapi import APIRouter, HTTPException, status
from app.models.schemas import TriageRequest, TriageResponse
from app.ml.disease_predictor import predict_triage

router = APIRouter(prefix="/api/v1/triage", tags=["Clinical Triage"])

@router.post("/predict", response_model=TriageResponse, summary="Perform AI symptom triage and differential evaluation")
async def evaluate_symptoms(request: TriageRequest):
    """
    Consumes unstructured symptom text and patient vitals, extracts clinical features,
    and calculates differential diagnosis probabilities, triage urgency, and care plans.
    """
    if not request.symptoms.strip():
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Symptoms string must not be empty"
        )
    return predict_triage(request)

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
