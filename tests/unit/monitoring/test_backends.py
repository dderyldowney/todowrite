from afs_fastapi.monitoring.interfaces import SoilSensorBackend, WaterSensorBackend
from afs_fastapi.monitoring.soil_monitor import SoilMonitor
from afs_fastapi.monitoring.water_monitor import WaterMonitor


class MySoilBackend(SoilSensorBackend):
    def read(self, sensor_id: str):
        # Return numeric-only readings matching the interface
        return {"ph": 6.7, "moisture": 0.33, "nitrogen": 1.2}


class MyWaterBackend(WaterSensorBackend):
    def read(self, sensor_id: str):
        return {"ph": 7.1, "turbidity": 0.9, "temperature": 18.0}


def test_soil_monitor_custom_backend():
    mon = SoilMonitor("SOIL001", backend=MySoilBackend())
    data = mon.get_soil_composition()
    assert data["ph"] == 6.7
    assert data["moisture"] == 0.33
    assert data["nitrogen"] == 1.2
    # backend returns numeric readings only per interface


def test_water_monitor_custom_backend():
    mon = WaterMonitor("WTR001", backend=MyWaterBackend())
    data = mon.get_water_quality()
    assert data["ph"] == 7.1
    assert data["turbidity"] == 0.9
    assert data["temperature"] == 18.0
    # backend returns numeric readings only per interface
