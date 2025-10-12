import unittest

from afs_fastapi.equipment.can_bus_manager import CanBusManager


class TestCanBusIntegration(unittest.TestCase):
    def test_virtual_can_bus_connection(self):
        """
        Tests that the CanBusManager can connect to a virtual CAN bus.
        """
        manager = CanBusManager(interface="virtual", channel="vcan0")
        manager.connect()
        self.assertIsNotNone(manager.bus)
        manager.disconnect()
        self.assertIsNone(manager.bus)


if __name__ == "__main__":
    unittest.main()
