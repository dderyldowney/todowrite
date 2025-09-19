import os

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from ..equipment.farm_tractors import FarmTractor, FarmTractorResponse
from ..monitoring.schemas import SoilReadingResponse, WaterQualityResponse
from ..monitoring.soil_monitor import SoilMonitor
from ..monitoring.water_monitor import WaterMonitor
from ..version import __version__

app = FastAPI(
    title="Automated Farming System API",
    description="API for controlling farm equipment and monitoring conditions",
    version=__version__,
)

# Optional CORS configuration via env var AFS_CORS_ORIGINS (comma-separated)
_cors_origins = os.getenv("AFS_CORS_ORIGINS")
if _cors_origins:
    origins = [o.strip() for o in _cors_origins.split(",") if o.strip()]
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


@app.get("/", tags=["meta"], summary="Welcome message")
async def read_root():
    """Root endpoint returning welcome message."""
    return {"message": "Welcome to the Agricultural Farm System API"}


@app.get("/health", tags=["meta"], summary="Health check")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}


@app.get("/version", tags=["meta"], summary="API version")
async def api_version():
    """Version information endpoint."""
    return {"version": __version__}


@app.get(
    "/equipment/tractor/{tractor_id}",
    response_model=FarmTractorResponse,
    response_model_exclude_none=True,
    tags=["equipment"],
    summary="Get tractor status",
)
async def get_tractor_status(tractor_id: str) -> FarmTractorResponse:
    """Get status of a specific tractor.

    Notes
    -----
    This returns a Pydantic model (`FarmTractorResponse`) suitable for API clients.
    """
    # Implementation would fetch actual tractor status
    tractor = FarmTractor("John Deere", "9RX", 2023)
    return tractor.to_response(tractor_id=tractor_id)


@app.get(
    "/monitoring/soil/{sensor_id}",
    response_model=SoilReadingResponse,
    response_model_exclude_none=True,
    tags=["monitoring"],
    summary="Get soil readings",
)
async def get_soil_status(sensor_id: str) -> SoilReadingResponse:
    """Get soil monitoring data from a specific sensor."""
    monitor = SoilMonitor(sensor_id)
    return SoilReadingResponse(sensor_id=sensor_id, readings=monitor.get_soil_composition())


@app.get(
    "/monitoring/water/{sensor_id}",
    response_model=WaterQualityResponse,
    response_model_exclude_none=True,
    tags=["monitoring"],
    summary="Get water readings",
)
async def get_water_status(sensor_id: str) -> WaterQualityResponse:
    """Get water quality data from a specific sensor."""
    monitor = WaterMonitor(sensor_id)
    return WaterQualityResponse(sensor_id=sensor_id, readings=monitor.get_water_quality())
