from typing import Optional, List, Dict
from pydantic import BaseModel, Field

class TriageRequest(BaseModel):
    symptoms: str = Field(..., description="Free-form natural language symptoms description")
    age: Optional[int] = Field(default=30, ge=0, le=120, description="Patient age in years")
    gender: Optional[str] = Field(default="unspecified", description="Gender (male, female, other, unspecified)")
    duration_days: Optional[int] = Field(default=2, ge=1, le=365, description="Duration of symptoms in days")
    temperature: Optional[float] = Field(default=None, description="Body temperature in Fahrenheit")
    heart_rate: Optional[int] = Field(default=None, description="Resting heart rate in bpm")
    oxygen_level: Optional[int] = Field(default=None, description="Oxygen saturation SpO2 %")

class DifferentialMatch(BaseModel):
    condition: str
    probability: int
    risk: str
    category: str

class TriageResponse(BaseModel):
    condition: str
    confidence: int
    severity: str
    triage_color: str
    action: str
    differentials: List[DifferentialMatch]
    extracted_symptoms: List[str]
    vitals_assessment: Dict[str, str]
    model_version: str
    inference_latency_ms: float
    timestamp: str

class HealthCheckResponse(BaseModel):
    status: str
    service: str
    version: str
    cluster_role: str
    uptime_seconds: float
