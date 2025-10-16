import asyncio
import unittest
from unittest.mock import patch

from afs_fastapi.equipment.can_bus_manager import CANBusConnectionManager, ConnectionPoolConfig
from afs_fastapi.equipment.physical_can_interface import InterfaceConfiguration


class TestCanBusIntegration(unittest.TestCase):
    def setUp(self):
        """Set up test fixtures."""
        # Create minimal configuration for testing
        self.pool_config = ConnectionPoolConfig(
            primary_interfaces=["vcan0"],
            backup_interfaces=["vcan1"],
            max_connections_per_interface=1,
            health_check_interval=1.0,
            auto_recovery=True,
        )

    def test_can_bus_manager_initialization(self):
        """Test that the CAN bus manager can be initialized properly."""
        # Test manager creation
        manager = CANBusConnectionManager(pool_config=self.pool_config)

        # Verify manager is in initial state
        self.assertIsNotNone(manager)
        self.assertIsNotNone(manager.codec)
        self.assertIsNotNone(manager.physical_manager)
        self.assertIsNotNone(manager.connection_pool)
        self.assertIsNotNone(manager.message_router)

    @patch("afs_fastapi.equipment.physical_can_interface.PhysicalCANManager.connect_interface")
    def test_can_bus_manager_lifecycle(self, mock_connect):
        """Test the complete lifecycle of CAN bus manager."""

        async def run_test():
            # Mock successful interface connection within async context
            async def mock_connect_async(*args, **kwargs):
                return True

            mock_connect.side_effect = mock_connect_async

            manager = CANBusConnectionManager(pool_config=self.pool_config)

            # Test initialization
            success = await manager.initialize()
            self.assertTrue(success)

            # Test manager status
            status = manager.get_manager_status()
            self.assertIn("state", status)
            self.assertIn("statistics", status)
            self.assertIn("connection_pool", status)

            # Test shutdown
            await manager.shutdown()

        # Run the async test
        asyncio.run(run_test())

    def test_connection_pool_config_validation(self):
        """Test that connection pool configuration is properly validated."""
        # Test valid configuration
        valid_config = ConnectionPoolConfig(
            primary_interfaces=["can0", "can1"],
            backup_interfaces=["can2"],
            max_connections_per_interface=2,
        )

        manager = CANBusConnectionManager(pool_config=valid_config)
        self.assertEqual(manager.pool_config.primary_interfaces, ["can0", "can1"])
        self.assertEqual(manager.pool_config.backup_interfaces, ["can2"])
        self.assertEqual(manager.pool_config.max_connections_per_interface, 2)

    @patch("afs_fastapi.equipment.physical_can_interface.PhysicalCANManager.create_interface")
    def test_interface_creation(self, mock_create):
        """Test interface creation through manager."""

        async def run_test():
            # Mock successful interface creation within async context
            async def mock_create_async(*args, **kwargs):
                return True

            mock_create.side_effect = mock_create_async

            manager = CANBusConnectionManager(pool_config=self.pool_config)

            # Test interface creation
            config = InterfaceConfiguration(
                interface_type="virtual",
                channel="vcan0",
                bitrate=250000,
            )

            success = await manager.create_interface("test_interface", config)
            self.assertTrue(success)

        # Run the async test
        asyncio.run(run_test())


if __name__ == "__main__":
    unittest.main()
