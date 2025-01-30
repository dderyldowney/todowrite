from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, Any

from ..equipment.farm_tractors import FarmTractor
from ..monitoring.soil_monitor import SoilMonitor
from ..monitoring.water_monitor import WaterMonitor

app = FastAPI(
    title="Automated Farming System API",
    description="API for controlling farm equipment and monitoring conditions",
    version="0.1.0"
)

@app.get("/")
async def read_root():
    """Root endpoint returning welcome message."""
    return {"message": "Welcome to the Agricultural Farm System API"}

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}

@app.get("/version")
async def api_version():
    """Version information endpoint."""
    return {"version": "0.1.0"}

@app.get("/equipment/tractor/{tractor_id}")
async def get_tractor_status(tractor_id: str) -> Dict[str, Any]:
    """Get status of a specific tractor."""
    # Implementation would fetch actual tractor status
    tractor = FarmTractor("John Deere", "9RX", 2023)
    return {"tractor_id": tractor_id, "status": str(tractor)}

@app.get("/monitoring/soil/{sensor_id}")
async def get_soil_status(sensor_id: str) -> Dict[str, Any]:
    """Get soil monitoring data from a specific sensor."""
    monitor = SoilMonitor(sensor_id)
    return {"sensor_id": sensor_id, "readings": monitor.get_soil_composition()}

@app.get("/monitoring/water/{sensor_id}")
async def get_water_status(sensor_id: str) -> Dict[str, Any]:
    """Get water quality data from a specific sensor."""
    monitor = WaterMonitor(sensor_id)
    return {"sensor_id": sensor_id, "readings": monitor.get_water_quality()}