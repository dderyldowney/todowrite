from unittest.mock import MagicMock
from afs_fastapi.equipment.farm_tractors import FarmTractor


def get_mock_farm_tractor():
    mock_tractor = MagicMock(spec=FarmTractor)
    mock_tractor.make = "John Deere"
    mock_tractor.model = "9RX"
    mock_tractor.year = 2023
    mock_tractor.manual_url = "https://example.com/manual"
    mock_tractor.engine_on = False
    mock_tractor.speed = 0
    mock_tractor.gear = "Neutral"
    mock_tractor.power_takeoff = False
    mock_tractor.hydraulics = False
    return mock_tractor
