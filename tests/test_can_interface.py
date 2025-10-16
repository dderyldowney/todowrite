from unittest.mock import MagicMock, patch

import can
import pytest

from afs_fastapi.equipment.can_bus_manager import CANBusConnectionManager, ConnectionPoolConfig
from afs_fastapi.equipment.physical_can_interface import InterfaceConfiguration


class TestCANBusConnectionManager:
    @pytest.fixture
    def pool_config(self):
        """Set up test fixtures."""
        return ConnectionPoolConfig(
            primary_interfaces=["can0", "can1"],
            backup_interfaces=["can2"],
            max_connections_per_interface=1,
            health_check_interval=5.0,
            failover_timeout=30.0,
            auto_recovery=True,
        )

    @pytest.mark.asyncio
    async def test_manager_initialization(self, pool_config):
        """Test successful manager initialization."""
        manager = CANBusConnectionManager(pool_config)

        # Mock the connection pool initialization
        with patch.object(manager.connection_pool, 'initialize', return_value=True):
            success = await manager.initialize()
            assert success is True

        await manager.shutdown()

    @pytest.mark.asyncio
    async def test_manager_initialization_failure(self, pool_config):
        """Test failed manager initialization."""
        manager = CANBusConnectionManager(pool_config)

        # Mock the connection pool initialization to fail
        with patch.object(manager.connection_pool, 'initialize', return_value=False):
            success = await manager.initialize()
            assert success is False

    @pytest.mark.asyncio
    async def test_send_message_legacy_api(self, pool_config):
        """Test sending a message using legacy API."""
        manager = CANBusConnectionManager(pool_config)

        # Create a mock interface with async send_message
        mock_interface = MagicMock()
        async def mock_send_message(msg):
            return True
        mock_interface.send_message = mock_send_message
        manager.physical_manager._interfaces["can0"] = mock_interface

        message = can.Message(arbitration_id=0x123, data=[1, 2, 3, 4])
        result = await manager.send_message("can0", message)
        assert result is True

    @pytest.mark.asyncio
    async def test_send_message_new_api(self, pool_config):
        """Test sending a message using new API with routing."""
        manager = CANBusConnectionManager(pool_config)

        # Mock connection pool to return active interfaces
        with patch.object(manager.connection_pool, 'get_active_interfaces', return_value=["can0", "can1"]):
            # Create mock interfaces with async send_message
            mock_interface0 = MagicMock()
            async def mock_send_message0(msg):
                return True
            mock_interface0.send_message = mock_send_message0

            mock_interface1 = MagicMock()
            async def mock_send_message1(msg):
                return True
            mock_interface1.send_message = mock_send_message1

            manager.physical_manager._interfaces["can0"] = mock_interface0
            manager.physical_manager._interfaces["can1"] = mock_interface1

            message = can.Message(arbitration_id=0x123, data=[1, 2, 3, 4])
            results = await manager.send_message(message)

            # Should return results for both interfaces
            assert isinstance(results, dict)
            assert all(results.values())

    def test_get_manager_status(self, pool_config):
        """Test getting manager status."""
        manager = CANBusConnectionManager(pool_config)
        status = manager.get_manager_status()

        assert isinstance(status, dict)
        assert "state" in status
        assert "statistics" in status
        assert "connection_pool" in status
        assert "routing" in status

    def test_get_active_interfaces(self, pool_config):
        """Test getting active interfaces."""
        manager = CANBusConnectionManager(pool_config)

        with patch.object(manager.connection_pool, 'get_active_interfaces', return_value=["can0"]):
            active = manager.get_active_interfaces()
            assert active == ["can0"]

    @pytest.mark.asyncio
    async def test_create_interface(self, pool_config):
        """Test creating a new interface."""
        manager = CANBusConnectionManager(pool_config)

        config = InterfaceConfiguration(
            interface_type="socketcan",
            channel="can0",
            bitrate=500000,
        )

        with patch.object(manager.physical_manager, 'create_interface', return_value=MagicMock()):
            success = await manager.create_interface("test_interface", config)
            assert success is True

    def test_message_callback_management(self, pool_config):
        """Test adding and removing message callbacks."""
        manager = CANBusConnectionManager(pool_config)

        def test_callback(decoded_message, interface_id):
            pass

        # Test adding callback
        manager.add_message_callback(test_callback)
        assert test_callback in manager._message_callbacks

        # Test removing callback
        manager.remove_message_callback(test_callback)
        assert test_callback not in manager._message_callbacks

