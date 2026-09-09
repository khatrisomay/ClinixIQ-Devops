import time
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import graphs, triage
from app.core.config import settings
from app.core.logging_middleware import structured_logging_middleware
from app.core.metrics import get_metrics_response, prometheus_middleware
from app.core.redis import cache_manager
from app.models.schemas import HealthCheckResponse

START_TIME = time.time()


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    await cache_manager.connect()
    yield
    # Shutdown
    await cache_manager.disconnect()


app = FastAPI(
    title=settings.PROJECT_NAME,
    description="Production-grade AI disease prediction, triage classifier, and dynamic clinical graph generation service.",
    version=settings.VERSION,
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.middleware("http")(prometheus_middleware)
app.middleware("http")(structured_logging_middleware)

app.include_router(triage.router)
app.include_router(graphs.router)


@app.get("/metrics", summary="Prometheus Metrics Exposition Endpoint")
async def metrics():
    return get_metrics_response()


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
        version=settings.VERSION,
        cluster_role="ml-inference-worker",
        uptime_seconds=round(time.time() - START_TIME, 2),
    )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
