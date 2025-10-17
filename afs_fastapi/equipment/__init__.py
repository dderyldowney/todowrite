# afs_fastapi/equipment/__init__.py
from .can_bus_manager import CANBusConnectionManager
from .farm_tractors import FarmTractor, FarmTractorResponse

__all__ = ["FarmTractor", "FarmTractorResponse", "CANBusConnectionManager"]
