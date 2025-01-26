import unittest
from tests.mocks.mock_farm_tractor import get_mock_farm_tractor


class TestFarmTractor(unittest.TestCase):
    def setUp(self):
        self.mock_tractor = get_mock_farm_tractor()

    def test_start_engine(self):
        self.mock_tractor.start_engine.return_value = "Engine started."
        result = self.mock_tractor.start_engine()
        self.assertEqual(result, "Engine started.")
        self.mock_tractor.start_engine.assert_called_once()

    def test_stop_engine(self):
        self.mock_tractor.stop_engine.return_value = "Engine stopped."
        result = self.mock_tractor.stop_engine()
        self.assertEqual(result, "Engine stopped.")
        self.mock_tractor.stop_engine.assert_called_once()

    def test_change_gear(self):
        self.mock_tractor.change_gear.return_value = "Gear changed to 1."
        result = self.mock_tractor.change_gear("1")
        self.assertEqual(result, "Gear changed to 1.")
        self.mock_tractor.change_gear.assert_called_once_with("1")

    def test_accelerate(self):
        self.mock_tractor.accelerate.return_value = (
            "Speed increased to 10 km/h."
        )
        result = self.mock_tractor.accelerate(10)
        self.assertEqual(result, "Speed increased to 10 km/h.")
        self.mock_tractor.accelerate.assert_called_once_with(10)

    def test_brake(self):
        self.mock_tractor.brake.return_value = "Speed decreased to 0 km/h."
        result = self.mock_tractor.brake(10)
        self.assertEqual(result, "Speed decreased to 0 km/h.")
        self.mock_tractor.brake.assert_called_once_with(10)

    def test_engage_power_takeoff(self):
        self.mock_tractor.engage_power_takeoff.return_value = (
            "Power takeoff engaged."
        )
        result = self.mock_tractor.engage_power_takeoff()
        self.assertEqual(result, "Power takeoff engaged.")
        self.mock_tractor.engage_power_takeoff.assert_called_once()

    def test_disengage_power_takeoff(self):
        self.mock_tractor.disengage_power_takeoff.return_value = (
            "Power takeoff disengaged."
        )
        result = self.mock_tractor.disengage_power_takeoff()
        self.assertEqual(result, "Power takeoff disengaged.")
        self.mock_tractor.disengage_power_takeoff.assert_called_once()

    def test_activate_hydraulics(self):
        self.mock_tractor.activate_hydraulics.return_value = (
            "Hydraulics activated."
        )
        result = self.mock_tractor.activate_hydraulics()
        self.assertEqual(result, "Hydraulics activated.")
        self.mock_tractor.activate_hydraulics.assert_called_once()

    def test_deactivate_hydraulics(self):
        self.mock_tractor.deactivate_hydraulics.return_value = (
            "Hydraulics deactivated."
        )
        result = self.mock_tractor.deactivate_hydraulics()
        self.assertEqual(result, "Hydraulics deactivated.")
        self.mock_tractor.deactivate_hydraulics.assert_called_once()


if __name__ == "__main__":
    unittest.main()
