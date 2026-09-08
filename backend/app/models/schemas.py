from pydantic import BaseModel, Field


class TriageRequest(BaseModel):
    symptoms: str = Field(..., description="Free-form natural language symptoms description")
    age: int | None = Field(default=30, ge=0, le=120, description="Patient age in years")
    gender: str | None = Field(
        default="unspecified", description="Gender (male, female, other, unspecified)"
    )
    duration_days: int | None = Field(
        default=2, ge=1, le=365, description="Duration of symptoms in days"
    )
    temperature: float | None = Field(default=None, description="Body temperature in Fahrenheit")
    heart_rate: int | None = Field(default=None, description="Resting heart rate in bpm")
    oxygen_level: int | None = Field(default=None, description="Oxygen saturation SpO2 %")


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
    differentials: list[DifferentialMatch]
    extracted_symptoms: list[str]
    vitals_assessment: dict[str, str]
    model_version: str
    inference_latency_ms: float
    timestamp: str


class HealthCheckResponse(BaseModel):
    status: str
    service: str
    version: str
    cluster_role: str
    uptime_seconds: float
