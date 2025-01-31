# afs_fastapi/stations/station_types.py
from enum import Enum


class StationType(Enum):
    MASTER = "master"
    DIAGNOSTIC = "diagnostic"
    SERVICE_DISPATCH = "service_dispatch"
    MONITORING = "monitoring"
    DROID_DISPATCH = "droid_dispatch"
    REPAIR_SERVICE = "repair_service"


def get_station_type(station_type_str: str) -> StationType:
    try:
        return StationType(station_type_str.lower())
    except ValueError:
        raise ValueError(f"Invalid station type: {station_type_str}")


class MasterStation:
    def __init__(self, station_id: int, system: str):
        self.station_id = station_id
        self.system = system

    def activate(self):
        return f"Master station {self.station_id} for {self.system} system is activated."

    def deactivate(self):
        return f"Master station {self.station_id} for {self.system} system is deactivated."
