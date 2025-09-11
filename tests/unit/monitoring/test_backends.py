from afs_fastapi.monitoring.interfaces import (
    SoilSensorBackend,
    WaterSensorBackend,
)
from afs_fastapi.monitoring.soil_monitor import SoilMonitor
from afs_fastapi.monitoring.water_monitor import WaterMonitor


class MySoilBackend(SoilSensorBackend):
    def read(self, sensor_id: str):
        # Echo sensor_id in a synthetic metric to ensure it flows through
        return {
            "ph": 6.7,
            "moisture": 0.33,
            "nitrogen": 1.2,
            "sensor": sensor_id,
        }


class MyWaterBackend(WaterSensorBackend):
    def read(self, sensor_id: str):
        return {
            "ph": 7.1,
            "turbidity": 0.9,
            "temperature": 18.0,
            "sensor": sensor_id,
        }


def test_soil_monitor_custom_backend():
    mon = SoilMonitor("SOIL001", backend=MySoilBackend())
    data = mon.get_soil_composition()
    assert data["ph"] == 6.7
    assert data["moisture"] == 0.33
    assert data["nitrogen"] == 1.2
    assert data["sensor"] == "SOIL001"


def test_water_monitor_custom_backend():
    mon = WaterMonitor("WTR001", backend=MyWaterBackend())
    data = mon.get_water_quality()
    assert data["ph"] == 7.1
    assert data["turbidity"] == 0.9
    assert data["temperature"] == 18.0
    assert data["sensor"] == "WTR001"
