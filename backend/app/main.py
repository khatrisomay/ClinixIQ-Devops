import time
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.models.schemas import HealthCheckResponse
from app.api.routes import triage, graphs

START_TIME = time.time()

app = FastAPI(
    title="ClinixIQ Healthcare ML & Triage Platform",
    description="Production-grade AI disease prediction, triage classifier, and dynamic clinical graph generation service.",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Enable CORS for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API Routers
app.include_router(triage.router)
app.include_router(graphs.router)

# Kubernetes Health Probes
@app.get("/healthz", summary="Liveness Probe for Kubernetes")
async def liveness():
    return {"status": "healthy", "service": "clinixiq-backend"}

@app.get("/readyz", summary="Readiness Probe for Kubernetes")
async def readiness():
    return {"status": "ready", "service": "clinixiq-backend"}

@app.get("/api/v1/health", response_model=HealthCheckResponse, summary="Detailed System Status")
async def system_health():
    return HealthCheckResponse(
        status="operational",
        service="clinixiq-backend-api",
        version="1.0.0",
        cluster_role="ml-inference-worker",
        uptime_seconds=round(time.time() - START_TIME, 2)
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
