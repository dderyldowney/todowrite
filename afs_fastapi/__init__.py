# afs_fastapi/__init__.py
from .equipment.farm_tractors import FarmTractor
from .stations.station_types import MasterStation

__all__ = ["FarmTractor", "MasterStation"]
