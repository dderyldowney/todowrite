# afs_fastapi/__init__.py
from .equipment.farm_tractors import FarmTractor
from .consoles.console_types import CommandConsole

__all__ = ["FarmTractor", "CommandConsole"]
