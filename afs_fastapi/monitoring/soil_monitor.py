from datetime import datetime
from typing import Any, Dict

from .interfaces import DummySoilSensorBackend, SoilSensorBackend


class SoilMonitor:
    def __init__(self, sensor_id: str, backend: SoilSensorBackend | None = None):
        self.sensor_id = sensor_id
        self.backend: SoilSensorBackend = backend or DummySoilSensorBackend()
        self.last_reading: Dict[str, Any] = {}

    def get_soil_composition(self) -> Dict[str, float]:
        """Get soil composition readings via the configured backend."""
        return self.backend.read(self.sensor_id)

    def log_reading(self) -> None:
        """Log current soil readings with timestamp."""
        self.last_reading = {
            "timestamp": datetime.now(),
            "readings": self.get_soil_composition(),
        }
