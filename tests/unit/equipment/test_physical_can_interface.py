"""
Test suite for physical CAN interface integration layer.

Tests comprehensive CAN interface abstraction for real-world tractor connectivity,
following Test-First Development (TDD) methodology for production agricultural systems.
"""

from __future__ import annotations

from unittest.mock import MagicMock, patch

import can
import pytest

from afs_fastapi.equipment.can_error_handling import CANErrorHandler
from afs_fastapi.equipment.physical_can_interface import (
    BusSpeed,
    CANInterfaceType,
    InterfaceConfiguration,
    InterfaceState,
    J1939Address,
    PhysicalCANManager,
    SocketCANInterface,
)


class TestInterfaceConfiguration:
    """Test CAN interface configuration structures."""

    def test_default_configuration_creation(self) -> None:
        """Test creating default interface configuration."""
        config = InterfaceConfiguration(
            interface_type=CANInterfaceType.SOCKETCAN,
            channel="can0",
            bitrate=BusSpeed.SPEED_250K,
        )

        assert config.interface_type == CANInterfaceType.SOCKETCAN
        assert config.channel == "can0"
        assert config.bitrate == BusSpeed.SPEED_250K
        assert config.fd_enabled is False
        assert config.auto_reset is True
        assert config.extended_frames is True

    def test_can_fd_configuration(self) -> None:
        """Test CAN FD configuration parameters."""
        config = InterfaceConfiguration(
            interface_type=CANInterfaceType.SOCKETCAN,
            channel="can1",
            bitrate=BusSpeed.SPEED_500K,
            fd_enabled=True,
            data_bitrate=2000000,
        )

        assert config.fd_enabled is True
        assert config.data_bitrate == 2000000


class TestJ1939Address:
    """Test J1939/ISOBUS address structure."""

    def test_basic_j1939_address_creation(self) -> None:
        """Test creating basic J1939 address."""
        address = J1939Address(
            source_address=0x25,  # Tractor ECU
            parameter_group_number=0xF004,  # Electronic Engine Controller 1
        )

        assert address.source_address == 0x25
        assert address.parameter_group_number == 0xF004
        assert address.destination_address == 0xFF  # Broadcast default
        assert address.priority == 6  # Default priority

    def test_directed_j1939_address(self) -> None:
        """Test J1939 address with specific destination."""
        address = J1939Address(
            source_address=0x25,
            parameter_group_number=0xEA00,  # Request PGN
            destination_address=0x26,  # Specific implement
            priority=3,  # High priority
        )

        assert address.destination_address == 0x26
        assert address.priority == 3


class TestSocketCANInterface:
    """Test SocketCAN interface implementation."""

    @pytest.fixture
    def mock_error_handler(self) -> CANErrorHandler:
        """Create mock error handler."""
        return CANErrorHandler(enable_recovery=True)

    @pytest.fixture
    def socketcan_config(self) -> InterfaceConfiguration:
        """Create SocketCAN configuration."""
        return InterfaceConfiguration(
            interface_type=CANInterfaceType.SOCKETCAN,
            channel="vcan0",  # Virtual CAN for testing
            bitrate=BusSpeed.SPEED_250K,
        )

    @pytest.fixture
    def socketcan_interface(
        self,
        socketcan_config: InterfaceConfiguration,
        mock_error_handler: CANErrorHandler,
    ) -> SocketCANInterface:
        """Create SocketCAN interface for testing."""
        return SocketCANInterface(
            interface_id="test_socketcan",
            config=socketcan_config,
            error_handler=mock_error_handler,
        )

    def test_socketcan_interface_initialization(
        self,
        socketcan_interface: SocketCANInterface,
    ) -> None:
        """Test SocketCAN interface initialization."""
        assert socketcan_interface.interface_id == "test_socketcan"
        assert socketcan_interface.state == InterfaceState.DISCONNECTED
        assert socketcan_interface.config.interface_type == CANInterfaceType.SOCKETCAN

    @pytest.mark.asyncio
    async def test_socketcan_connection_lifecycle(
        self,
        socketcan_interface: SocketCANInterface,
    ) -> None:
        """Test SocketCAN connection and disconnection."""
        # Mock the CAN bus creation
        with patch("can.interface.Bus") as mock_bus:
            mock_bus_instance = MagicMock()
            mock_bus.return_value = mock_bus_instance

            # Test connection
            connection_result = await socketcan_interface.connect()

            assert connection_result is True
            assert socketcan_interface.state == InterfaceState.CONNECTED

            # Verify bus was created with correct parameters
            mock_bus.assert_called_once_with(
                interface="socketcan",
                channel="vcan0",
                bitrate=250000,
                fd=False,
                data_bitrate=2000000,
                can_filters=None,
            )

            # Test disconnection
            disconnection_result = await socketcan_interface.disconnect()

            assert disconnection_result is True
            assert socketcan_interface.state == InterfaceState.DISCONNECTED
            mock_bus_instance.shutdown.assert_called_once()

    @pytest.mark.asyncio
    async def test_socketcan_connection_failure(
        self,
        socketcan_interface: SocketCANInterface,
    ) -> None:
        """Test SocketCAN connection failure handling."""
        # Mock bus creation to raise exception
        with patch("can.interface.Bus", side_effect=Exception("Interface not found")):
            connection_result = await socketcan_interface.connect()

            assert connection_result is False
            assert socketcan_interface.state == InterfaceState.ERROR

    @pytest.mark.asyncio
    async def test_socketcan_message_sending(
        self,
        socketcan_interface: SocketCANInterface,
    ) -> None:
        """Test sending CAN message via SocketCAN."""
        # Set up connected state
        with patch("can.interface.Bus") as mock_bus:
            mock_bus_instance = MagicMock()
            mock_bus.return_value = mock_bus_instance

            await socketcan_interface.connect()

            # Create test message
            test_message = can.Message(
                arbitration_id=0x18F00425,  # J1939 message
                data=b"\x01\x02\x03\x04",
                is_extended_id=True,
            )

            # Test message sending
            send_result = await socketcan_interface.send_message(test_message)

            assert send_result is True
            mock_bus_instance.send.assert_called_once_with(test_message)
            assert socketcan_interface.status.messages_sent == 1

    @pytest.mark.asyncio
    async def test_socketcan_message_sending_failure(
        self,
        socketcan_interface: SocketCANInterface,
    ) -> None:
        """Test CAN message sending failure handling."""
        with patch("can.interface.Bus") as mock_bus:
            mock_bus_instance = MagicMock()
            mock_bus_instance.send.side_effect = can.CanError("Bus error")
            mock_bus.return_value = mock_bus_instance

            await socketcan_interface.connect()

            test_message = can.Message(arbitration_id=0x123, data=b"\x01\x02")
            send_result = await socketcan_interface.send_message(test_message)

            assert send_result is False
            assert socketcan_interface.status.errors_total == 1

    def test_socketcan_hardware_info(
        self,
        socketcan_interface: SocketCANInterface,
    ) -> None:
        """Test retrieving SocketCAN hardware information."""
        hardware_info = socketcan_interface.get_hardware_info()

        assert hardware_info["interface_type"] == "SocketCAN"
        assert hardware_info["channel"] == "vcan0"
        assert hardware_info["bitrate"] == 250000
        assert hardware_info["fd_enabled"] is False
        assert "driver" in hardware_info

    def test_socketcan_message_callbacks(
        self,
        socketcan_interface: SocketCANInterface,
    ) -> None:
        """Test message callback registration and execution."""
        received_messages = []

        def test_callback(message: can.Message, interface_id: str) -> None:
            received_messages.append((message, interface_id))

        # Register callback
        socketcan_interface.add_message_callback(test_callback)

        # Simulate received message
        test_message = can.Message(arbitration_id=0x123, data=b"\x01\x02")
        socketcan_interface._handle_received_message(test_message)

        assert len(received_messages) == 1
        assert received_messages[0][0] == test_message
        assert received_messages[0][1] == "test_socketcan"

        # Test callback removal
        socketcan_interface.remove_message_callback(test_callback)
        socketcan_interface._handle_received_message(test_message)

        # Should still be only 1 message (callback removed)
        assert len(received_messages) == 1


class TestPhysicalCANManager:
    """Test physical CAN manager for multiple interfaces."""

    @pytest.fixture
    def can_manager(self) -> PhysicalCANManager:
        """Create CAN manager for testing."""
        return PhysicalCANManager()

    @pytest.fixture
    def test_config(self) -> InterfaceConfiguration:
        """Create test configuration."""
        return InterfaceConfiguration(
            interface_type=CANInterfaceType.SOCKETCAN,
            channel="vcan0",
            bitrate=BusSpeed.SPEED_250K,
        )

    @pytest.mark.asyncio
    async def test_interface_creation_and_management(
        self,
        can_manager: PhysicalCANManager,
        test_config: InterfaceConfiguration,
    ) -> None:
        """Test creating and managing CAN interfaces."""
        # Create interface
        interface = await can_manager.create_interface("test_if", test_config)

        assert interface.interface_id == "test_if"
        assert interface.config == test_config

        # Test duplicate creation
        with pytest.raises(ValueError, match="Interface test_if already exists"):
            await can_manager.create_interface("test_if", test_config)

    @pytest.mark.asyncio
    async def test_interface_connection_management(
        self,
        can_manager: PhysicalCANManager,
        test_config: InterfaceConfiguration,
    ) -> None:
        """Test connecting and disconnecting interfaces."""
        # Create interface
        await can_manager.create_interface("test_if", test_config)

        # Mock CAN bus for connection
        with patch("can.interface.Bus"):
            # Test connection
            connection_result = await can_manager.connect_interface("test_if")
            assert connection_result is True

            # Test status tracking
            status = can_manager.get_interface_status("test_if")
            assert status is not None
            assert status.state == InterfaceState.CONNECTED

            # Test disconnection
            disconnection_result = await can_manager.disconnect_interface("test_if")
            assert disconnection_result is True

    @pytest.mark.asyncio
    async def test_connect_all_interfaces(
        self,
        can_manager: PhysicalCANManager,
        test_config: InterfaceConfiguration,
    ) -> None:
        """Test connecting all configured interfaces."""
        # Create multiple interfaces
        await can_manager.create_interface("if1", test_config)
        await can_manager.create_interface("if2", test_config)

        with patch("can.interface.Bus"):
            results = await can_manager.connect_all()

            assert len(results) == 2
            assert results["if1"] is True
            assert results["if2"] is True

    @pytest.mark.asyncio
    async def test_broadcast_message(
        self,
        can_manager: PhysicalCANManager,
        test_config: InterfaceConfiguration,
    ) -> None:
        """Test broadcasting message to all active interfaces."""
        # Create and connect interfaces
        await can_manager.create_interface("if1", test_config)
        await can_manager.create_interface("if2", test_config)

        with patch("can.interface.Bus") as mock_bus:
            mock_bus_instances = [MagicMock(), MagicMock()]
            mock_bus.side_effect = mock_bus_instances

            await can_manager.connect_all()

            # Test broadcast
            test_message = can.Message(arbitration_id=0x123, data=b"\x01\x02")
            results = await can_manager.broadcast_message(test_message)

            assert len(results) == 2
            assert results["if1"] is True
            assert results["if2"] is True

            # Verify both interfaces received the message
            for mock_instance in mock_bus_instances:
                mock_instance.send.assert_called_once_with(test_message)

    def test_global_message_callbacks(
        self,
        can_manager: PhysicalCANManager,
    ) -> None:
        """Test global message callbacks applied to all interfaces."""
        received_messages = []

        def global_callback(message: can.Message, interface_id: str) -> None:
            received_messages.append((message, interface_id))

        # Add global callback
        can_manager.add_global_callback(global_callback)

        # Verify callback list
        assert len(can_manager._global_callbacks) == 1

    def test_j1939_message_creation(
        self,
        can_manager: PhysicalCANManager,
    ) -> None:
        """Test J1939/ISOBUS message creation."""
        address = J1939Address(
            source_address=0x25,
            parameter_group_number=0xF004,
            priority=3,
        )

        test_data = b"\x12\x34\x56\x78\x9A\xBC\xDE\xF0"
        message = can_manager.create_j1939_message(address, test_data)

        assert message.is_extended_id is True
        assert message.data == test_data
        assert len(message.data) == 8

        # Verify CAN ID construction (simplified check)
        assert (message.arbitration_id & 0xFF) == 0x25  # Source address


class TestIntegrationScenarios:
    """Test real-world tractor connectivity scenarios."""

    @pytest.mark.asyncio
    async def test_multi_tractor_field_coordination_setup(self) -> None:
        """Test setting up CAN communication for multi-tractor coordination."""
        manager = PhysicalCANManager()

        # Create interfaces for different tractors
        tractor_configs = [
            InterfaceConfiguration(
                interface_type=CANInterfaceType.SOCKETCAN,
                channel="can0",  # Primary field network
                bitrate=BusSpeed.SPEED_250K,
            ),
            InterfaceConfiguration(
                interface_type=CANInterfaceType.SOCKETCAN,
                channel="can1",  # Secondary implement network
                bitrate=BusSpeed.SPEED_500K,
            ),
        ]

        with patch("can.interface.Bus"):
            # Create interfaces
            _ = await manager.create_interface("field_network", tractor_configs[0])
            _ = await manager.create_interface("implement_network", tractor_configs[1])

            # Connect all interfaces
            connection_results = await manager.connect_all()

            assert all(connection_results.values())
            assert len(manager._active_interfaces) == 2

            # Test emergency broadcast capability
            emergency_message = manager.create_j1939_message(
                J1939Address(
                    source_address=0x25,
                    parameter_group_number=0xE001,  # Emergency stop
                    priority=0,  # Highest priority
                ),
                b"\xFF\xFF\xFF\xFF\x00\x00\x00\x00",  # Emergency stop signal
            )

            broadcast_results = await manager.broadcast_message(emergency_message)
            assert all(broadcast_results.values())

    @pytest.mark.asyncio
    async def test_isobus_compliance_validation(self) -> None:
        """Test ISOBUS protocol compliance in message handling."""
        manager = PhysicalCANManager()

        config = InterfaceConfiguration(
            interface_type=CANInterfaceType.SOCKETCAN,
            channel="vcan0",
            bitrate=BusSpeed.SPEED_250K,  # ISOBUS standard
            extended_frames=True,  # Required for J1939
        )

        with patch("can.interface.Bus"):
            interface = await manager.create_interface("isobus_test", config)
            await manager.connect_interface("isobus_test")

            # Test standard ISOBUS message types
            standard_messages = [
                # Electronic Engine Controller 1 (EEC1)
                (J1939Address(source_address=0x00, parameter_group_number=0xF004), b"\x00" * 8),
                # Wheel-Based Vehicle Speed (WVS)
                (J1939Address(source_address=0x0B, parameter_group_number=0xFE48), b"\x00" * 8),
                # Vehicle Position (VP)
                (J1939Address(source_address=0x25, parameter_group_number=0xFEF3), b"\x00" * 8),
            ]

            for address, data in standard_messages:
                message = manager.create_j1939_message(address, data)

                # Verify extended ID format
                assert message.is_extended_id is True

                # Verify data length compliance
                assert len(message.data) <= 8  # Standard CAN frame limit

                # Test message sending
                send_result = await interface.send_message(message)
                assert send_result is True

    @pytest.mark.asyncio
    async def test_error_recovery_during_field_operations(self) -> None:
        """Test error recovery mechanisms during active field operations."""
        error_handler = CANErrorHandler(enable_recovery=True)
        manager = PhysicalCANManager(error_handler=error_handler)

        config = InterfaceConfiguration(
            interface_type=CANInterfaceType.SOCKETCAN,
            channel="vcan0",
            bitrate=BusSpeed.SPEED_250K,
        )

        with patch("can.interface.Bus") as mock_bus:
            # First connection succeeds
            mock_bus_instance = MagicMock()
            mock_bus.return_value = mock_bus_instance

            interface = await manager.create_interface("field_ops", config)
            connection_result = await manager.connect_interface("field_ops")
            assert connection_result is True

            # Simulate message sending failure
            mock_bus_instance.send.side_effect = can.CanError("Bus off")

            test_message = manager.create_j1939_message(
                J1939Address(source_address=0x25, parameter_group_number=0xF004),
                b"\x01\x02\x03\x04\x05\x06\x07\x08",
            )

            send_result = await interface.send_message(test_message)
            assert send_result is False
            assert interface.status.errors_total > 0

            # Verify error was logged
            assert error_handler.total_errors_handled > 0
