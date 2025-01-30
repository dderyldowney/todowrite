# afs_fastapi/monitoring/__init__.py
from .soil_monitor import SoilMonitor
from .water_monitor import WaterMonitor

__all__ = ["SoilMonitor", "WaterMonitor"]
