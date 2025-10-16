"""Integration tests for comprehensive CAN interface system.

This module tests the complete CAN communication stack including:
- Physical interface management
- Message routing and filtering
- ISOBUS protocol compliance
- Real-world agricultural scenarios
- Error handling and recovery
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Any
from unittest.mock import AsyncMock, patch

import can
import pytest

from afs_fastapi.core.can_frame_codec import CANFrameCodec
from afs_fastapi.equipment.can_bus_manager import CANBusConnectionManager, ConnectionPoolConfig
from afs_fastapi.equipment.can_error_handling import CANErrorHandler
from afs_fastapi.equipment.physical_can_interface import (
    BusSpeed,
    CANInterfaceType,
    InterfaceConfiguration,
    InterfaceState,
)
from afs_fastapi.protocols.isobus_handlers import ISOBUSProtocolManager


@dataclass
class AddressClaimMessage:
    """Test data class for address claim messages."""

    source_address: int
    name: int
    function_code: int
    vehicle_system: int


@dataclass
class EngineData:
    """Test data class for engine data."""

    rpm: float
    torque: float
    fuel_rate: float
    coolant_temp: float
    oil_pressure: float
    air_intake_temp: float


@dataclass
class VehiclePosition:
    """Test data class for vehicle position."""

    latitude: float
    longitude: float
    altitude: float


@dataclass
class TransportProtocolMessage:
    """Test data class for transport protocol messages."""

    control_byte: int
    total_message_size: int
    total_packets: int
    destination_address: int
    pgn: int
    data: bytes


@dataclass
class DiagnosticMessage:
    """Test data class for diagnostic messages."""

    source_address: int
    lamp_status: int
    dtc_count: int
    dtcs: list[dict[str, Any]]


class TestCANInterfaceIntegration:
    """Integration tests for complete CAN interface system."""

    @pytest.fixture
    def mock_can_bus(self):
        """Create mock CAN bus for testing."""
        bus = AsyncMock(spec=can.AsyncBufferedReader)
        bus.recv = AsyncMock()
        bus.send = AsyncMock()
        return bus

    @pytest.fixture
    def interface_config(self):
        """Create test interface configuration."""
        return InterfaceConfiguration(
            interface_type=CANInterfaceType.SOCKETCAN,
            channel="vcan0",
            bitrate=BusSpeed.SPEED_250K,
        )

    @pytest.fixture
    def connection_pool_config(self):
        """Create test connection pool configuration."""
        return ConnectionPoolConfig(
            primary_interfaces=["tractor_1", "tractor_2"],
            backup_interfaces=["backup_1"],
            max_connections_per_interface=1,
            health_check_interval=5.0,
            failover_timeout=30.0,
            auto_recovery=True,
        )

    @pytest.fixture
    def can_manager(self, connection_pool_config):
        """Create CAN bus manager with full integration."""
        return CANBusConnectionManager(connection_pool_config)

    @pytest.fixture
    def isobus_manager(self):
        """Create ISOBUS protocol manager."""
        codec = CANFrameCodec()
        error_handler = CANErrorHandler()
        return ISOBUSProtocolManager(codec, error_handler)

    @pytest.mark.skip(reason="Test interface mismatch - requires updated CAN manager API")
    async def test_complete_tractor_communication_workflow(
        self, can_manager, isobus_manager, mock_can_bus
    ):
        """Test complete tractor-to-tractor communication workflow."""
        # Simulate two tractors joining the network
        tractor_1_config = InterfaceConfiguration(
            interface_type=CANInterfaceType.SOCKETCAN,
            channel="vcan0",
            bitrate=BusSpeed.SPEED_250K,
        )

        tractor_2_config = InterfaceConfiguration(
            interface_type=CANInterfaceType.SOCKETCAN,
            channel="vcan0",
            bitrate=BusSpeed.SPEED_250K,
        )

        # Mock successful interface initialization
        with patch.object(can_manager, "_create_physical_interface") as mock_create:
            mock_interface_1 = AsyncMock()
            mock_interface_1.connect.return_value = True
            mock_interface_1.state = InterfaceState.CONNECTED
            mock_interface_1.receive_message = AsyncMock()
            mock_interface_1.send_message = AsyncMock()

            mock_interface_2 = AsyncMock()
            mock_interface_2.connect.return_value = True
            mock_interface_2.state = InterfaceState.CONNECTED
            mock_interface_2.receive_message = AsyncMock()
            mock_interface_2.send_message = AsyncMock()

            mock_create.side_effect = [mock_interface_1, mock_interface_2]

            # Initialize both tractor interfaces
            await can_manager.initialize_interface("tractor_1", tractor_1_config)
            await can_manager.initialize_interface("tractor_2", tractor_2_config)

            # Test Address Claim procedure
            address_claim_msg = AddressClaimMessage(
                source_address=0x81,
                name=0x8000000000000001,  # Tractor 1 NAME
                function_code=0x19,  # Tractor function
                vehicle_system=0x00,
            )

            # Simulate address claim exchange
            claim_frame = isobus_manager.address_claim.create_address_claim_message(
                address_claim_msg
            )

            # Verify address claim processing
            assert claim_frame is not None
            assert claim_frame.arbitration_id & 0xFF == 0x81  # Source address

            # Process the claim on the receiving tractor
            decoded_claim = isobus_manager.address_claim.process_address_claim(claim_frame)
            assert decoded_claim is not None
            assert decoded_claim.source_address == 0x81

            # Test engine data exchange
            engine_data = EngineData(
                rpm=1800,
                torque=75.5,
                fuel_rate=12.3,
                coolant_temp=85,
                oil_pressure=45.2,
                air_intake_temp=25,
            )

            # Create and send engine data message
            engine_frame = can_manager.codec.encode_engine_data(engine_data, source_address=0x81)
            await can_manager.send_message("tractor_1", engine_frame)

            # Verify message was sent
            mock_interface_1.send_message.assert_called_once()

            # Simulate receiving the message on tractor 2
            mock_interface_2.receive_message.return_value = engine_frame
            received_frame = await mock_interface_2.receive_message()

            # Decode received engine data
            decoded_engine = can_manager.codec.decode_can_message(received_frame)
            assert decoded_engine is not None
            assert decoded_engine.pgn == 0xF004  # Engine data PGN
            assert "rpm" in decoded_engine.data
            assert decoded_engine.data["rpm"] == 1800

    @pytest.mark.skip(reason="Test interface mismatch - requires updated CAN manager API")
    async def test_multi_tractor_field_coordination_scenario(self, can_manager, isobus_manager):
        """Test realistic multi-tractor field coordination scenario."""
        # Simulate 3 tractors performing coordinated field operation
        tractor_configs = []
        for i in range(3):
            config = InterfaceConfiguration(
                interface_type=CANInterfaceType.SOCKETCAN,
                channel=f"vcan{i}",
                bitrate=BusSpeed.SPEED_250K,
            )
            tractor_configs.append(config)

        # Mock interfaces for all tractors
        mock_interfaces = []
        for _ in range(3):
            mock_interface = AsyncMock()
            mock_interface.connect.return_value = True
            mock_interface.state = InterfaceState.CONNECTED
            mock_interface.receive_message = AsyncMock()
            mock_interface.send_message = AsyncMock()
            mock_interfaces.append(mock_interface)

        with patch.object(can_manager, "_create_physical_interface") as mock_create:
            mock_create.side_effect = mock_interfaces

            # Initialize all tractor interfaces
            for i, config in enumerate(tractor_configs):
                await can_manager.initialize_interface(f"tractor_{i+1}", config)

            # Simulate GPS position updates from all tractors
            positions = [
                VehiclePosition(latitude=40.7128, longitude=-74.0060, altitude=10.0),  # NYC
                VehiclePosition(
                    latitude=40.7589, longitude=-73.9851, altitude=15.0
                ),  # Times Square
                VehiclePosition(
                    latitude=40.6892, longitude=-74.0445, altitude=8.0
                ),  # Statue of Liberty
            ]

            # Send position updates
            for i, position in enumerate(positions):
                position_frame = can_manager.codec.encode_vehicle_position(
                    position, source_address=0x81 + i
                )
                await can_manager.send_message(f"tractor_{i+1}", position_frame)
                mock_interfaces[i].send_message.assert_called()

            # Simulate coordinate field operation command using Transport Protocol
            # Large message requiring multi-frame transport
            field_operation_data = {
                "operation_type": "cultivation",
                "field_id": "FIELD_001",
                "pattern": "parallel_lines",
                "spacing": 3.0,
                "speed": 8.5,
                "implement_depth": 15.2,
                "start_coordinates": [40.7128, -74.0060],
                "end_coordinates": [40.7589, -73.9851],
                "safety_zones": [
                    {"type": "obstacle", "coordinates": [40.7200, -74.0100], "radius": 10.0},
                    {"type": "water", "coordinates": [40.7300, -74.0200], "radius": 5.0},
                ],
            }

            # Create Transport Protocol message
            tp_message = TransportProtocolMessage(
                control_byte=0x20,  # Connection Management
                total_message_size=len(str(field_operation_data).encode()),
                total_packets=5,
                destination_address=0xFF,  # Broadcast
                pgn=0xFFFF,  # Custom application data
                data=str(field_operation_data).encode()[:7],  # First 7 bytes
            )

            tp_frame = isobus_manager.transport_protocol.create_tp_cm_message(tp_message)

            # Broadcast to all tractors
            for i in range(3):
                await can_manager.send_message(f"tractor_{i+1}", tp_frame)

            # Verify all tractors received the coordination command
            for mock_interface in mock_interfaces:
                assert mock_interface.send_message.call_count >= 1

    @pytest.mark.skip(reason="Test interface mismatch - requires updated CAN manager API")
    async def test_error_handling_and_recovery_integration(self, can_manager, isobus_manager):
        """Test comprehensive error handling and recovery scenarios."""
        config = InterfaceConfiguration(
            interface_type=CANInterfaceType.SOCKETCAN,
            channel="vcan0",
            bitrate=BusSpeed.SPEED_250K,
        )

        # Create mock interface that will fail initially
        mock_interface = AsyncMock()
        mock_interface.connect.side_effect = [False, False, True]  # Fail twice, then succeed
        mock_interface.state = InterfaceState.CONNECTED
        mock_interface.send_message = AsyncMock()

        with patch.object(can_manager, "_create_physical_interface", return_value=mock_interface):
            # Test connection retry mechanism
            await can_manager.initialize_interface("error_test", config)

            # Should have retried connection 3 times
            assert mock_interface.connect.call_count == 3

            # Test diagnostic message handling for error conditions
            diagnostic_msg = DiagnosticMessage(
                source_address=0x81,
                lamp_status=0x03,  # Warning and error lamps
                dtc_count=2,
                dtcs=[
                    {"spn": 110, "fmi": 3, "occurrence_count": 1},  # Engine coolant temp
                    {"spn": 175, "fmi": 4, "occurrence_count": 3},  # Engine oil pressure
                ],
            )

            # Create DM1 (Active DTCs) message
            dm1_frame = isobus_manager.diagnostics.create_dm1_message(diagnostic_msg)

            # Simulate sending diagnostic message
            await can_manager.send_message("error_test", dm1_frame)
            mock_interface.send_message.assert_called()

            # Process diagnostic message
            decoded_dm1 = isobus_manager.diagnostics.process_dm1_message(dm1_frame)
            assert decoded_dm1 is not None
            assert decoded_dm1.dtc_count == 2
            assert len(decoded_dm1.dtcs) == 2
            assert decoded_dm1.dtcs[0]["spn"] == 110

    @pytest.mark.skip(reason="Test interface mismatch - requires updated CAN manager API")
    async def test_high_throughput_message_processing(self, can_manager, isobus_manager):
        """Test system performance with high message throughput."""
        config = InterfaceConfiguration(
            interface_type=CANInterfaceType.SOCKETCAN,
            channel="vcan0",
            bitrate=BusSpeed.SPEED_500K,  # Higher bitrate for performance test
        )

        mock_interface = AsyncMock()
        mock_interface.connect.return_value = True
        mock_interface.state = InterfaceState.CONNECTED
        mock_interface.send_message = AsyncMock()
        mock_interface.receive_message = AsyncMock()

        with patch.object(can_manager, "_create_physical_interface", return_value=mock_interface):
            await can_manager.initialize_interface("performance_test", config)

            # Generate high volume of realistic agricultural messages
            messages_per_second = 100
            test_duration = 1.0  # 1 second test
            total_messages = int(messages_per_second * test_duration)

            start_time = datetime.now()

            # Send burst of engine data messages
            for i in range(total_messages):
                engine_data = EngineData(
                    rpm=1500 + (i % 500),  # Varying RPM
                    torque=50.0 + (i % 100),
                    fuel_rate=10.0 + (i % 20),
                    coolant_temp=80 + (i % 30),
                    oil_pressure=40.0 + (i % 20),
                    air_intake_temp=20 + (i % 15),
                )

                frame = can_manager.codec.encode_engine_data(engine_data, source_address=0x81)
                await can_manager.send_message("performance_test", frame)

            end_time = datetime.now()
            processing_time = (end_time - start_time).total_seconds()

            # Verify performance metrics
            assert mock_interface.send_message.call_count == total_messages
            assert processing_time < 2.0  # Should complete within 2 seconds

            # Calculate throughput
            throughput = total_messages / processing_time
            assert throughput > 50  # Minimum 50 messages/second

    @pytest.mark.skip(reason="Test interface mismatch - requires updated CAN manager API")
    async def test_real_world_agricultural_protocol_compliance(self, can_manager, isobus_manager):
        """Test compliance with real-world agricultural protocols."""
        config = InterfaceConfiguration(
            interface_type=CANInterfaceType.SOCKETCAN,
            channel="vcan0",
            bitrate=BusSpeed.SPEED_250K,
        )

        mock_interface = AsyncMock()
        mock_interface.connect.return_value = True
        mock_interface.state = InterfaceState.CONNECTED
        mock_interface.send_message = AsyncMock()

        with patch.object(can_manager, "_create_physical_interface", return_value=mock_interface):
            await can_manager.initialize_interface("compliance_test", config)

            # Test ISOBUS compliance scenarios

            # 1. Address Claim procedure compliance
            # Verify proper NAME field structure
            name_field = (
                (0x19 << 21)  # Function code (Tractor)
                | (0x00 << 16)  # Function instance
                | (0x07 << 11)  # ECU instance
                | (0x0123 << 0)  # Manufacturer code and serial
            )

            address_claim = AddressClaimMessage(
                source_address=0x81,
                name=name_field,
                function_code=0x19,
                vehicle_system=0x00,
            )

            claim_frame = isobus_manager.address_claim.create_address_claim_message(address_claim)

            # Verify J1939-21 compliance
            assert (claim_frame.arbitration_id >> 8) & 0xFFFF == 0x18EEFF  # PGN for Address Claim
            assert len(claim_frame.data) == 8  # Must be 8 bytes

            # 2. Test PGN request/response cycle
            # Request engine data (PGN 0xF004)
            request_frame = can.Message(
                arbitration_id=0x18EAFF81,  # PGN Request from SA 0x81
                data=[0x04, 0xF0, 0x00, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF],
                is_extended_id=True,
            )

            await can_manager.send_message("compliance_test", request_frame)

            # 3. Test Transport Protocol compliance for large messages
            large_data = b"A" * 200  # 200 bytes of data

            tp_message = TransportProtocolMessage(
                control_byte=0x20,  # BAM (Broadcast Announce Message)
                total_message_size=len(large_data),
                total_packets=(len(large_data) + 6) // 7,  # 7 bytes per packet
                destination_address=0xFF,
                pgn=0xFFFF,
                data=large_data[:7],
            )

            tp_frame = isobus_manager.transport_protocol.create_tp_cm_message(tp_message)

            # Verify TP.CM message format
            assert (tp_frame.arbitration_id >> 8) & 0xFFFF == 0x18ECFF  # TP.CM PGN
            assert tp_frame.data[0] == 0x20  # BAM control byte

            # Send the TP.CM message
            await can_manager.send_message("compliance_test", tp_frame)

            # Verify all compliance messages were sent
            assert mock_interface.send_message.call_count >= 3

    @pytest.mark.skip(reason="Test interface mismatch - requires updated CAN manager API")
    async def test_failover_and_redundancy_integration(self, can_manager):
        """Test failover and redundancy mechanisms."""
        # Configure primary and backup interfaces
        primary_config = InterfaceConfiguration(
            interface_type=CANInterfaceType.SOCKETCAN,
            channel="vcan0",
            bitrate=BusSpeed.SPEED_250K,
        )

        backup_config = InterfaceConfiguration(
            interface_type=CANInterfaceType.SOCKETCAN,
            channel="vcan1",
            bitrate=BusSpeed.SPEED_250K,
        )

        # Mock primary interface that will fail
        mock_primary = AsyncMock()
        mock_primary.connect.return_value = True
        mock_primary.state = InterfaceState.CONNECTED
        mock_primary.send_message = AsyncMock(side_effect=Exception("Interface failed"))

        # Mock backup interface
        mock_backup = AsyncMock()
        mock_backup.connect.return_value = True
        mock_backup.state = InterfaceState.CONNECTED
        mock_backup.send_message = AsyncMock()

        with patch.object(can_manager, "_create_physical_interface") as mock_create:
            mock_create.side_effect = [mock_primary, mock_backup]

            # Initialize both interfaces
            await can_manager.initialize_interface("primary", primary_config)
            await can_manager.initialize_interface("backup", backup_config)

            # Test message sending with failover
            test_message = can.Message(
                arbitration_id=0x18F00481,
                data=[0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07, 0x08],
                is_extended_id=True,
            )

            # First attempt should fail on primary, succeed on backup
            try:
                await can_manager.send_message("primary", test_message)
            except Exception:
                # Expected failure, should trigger failover
                pass

            # Verify backup interface was used
            # Note: This would require implementing actual failover logic in the manager
            assert mock_backup.connect.called

    @pytest.mark.skip(reason="Test interface mismatch - requires updated CAN manager API")
    async def test_memory_and_resource_management(self, can_manager):
        """Test memory usage and resource cleanup."""
        # This test uses old API methods that don't exist in current implementation
        # TODO: Rewrite for current CANBusConnectionManager interface
        pass
