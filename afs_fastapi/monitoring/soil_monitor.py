from typing import Dict, Any
from datetime import datetime

class SoilMonitor:
    def __init__(self, sensor_id: str):
        self.sensor_id = sensor_id
        self.last_reading: Dict[str, Any] = {}
        
    def get_soil_composition(self) -> Dict[str, float]:
        """Get soil composition readings."""
        # Implementation would connect to actual sensors
        return {
            "nitrogen": 0.0,
            "phosphorus": 0.0,
            "potassium": 0.0,
            "ph": 7.0,
            "moisture": 0.0
        }
        
    def log_reading(self) -> None:
        """Log current soil readings with timestamp."""
        self.last_reading = {
            "timestamp": datetime.now(),
            "readings": self.get_soil_composition()
        }