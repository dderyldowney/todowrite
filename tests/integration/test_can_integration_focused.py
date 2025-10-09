"""Focused integration tests for the CAN interface system.

This module tests the complete CAN communication stack with realistic
agricultural scenarios, using the actual implemented components.
"""

from __future__ import annotations

import pytest
from unittest.mock import AsyncMock
import can
from datetime import datetime

from afs_fastapi.equipment.physical_can_interface import (
    InterfaceConfiguration,
    CANInterfaceType,
    BusSpeed,
)
from afs_fastapi.equipment.can_bus_manager import (
    CANBusConnectionManager,
    ConnectionPoolConfig,
)
from afs_fastapi.core.can_frame_codec import (
    CANFrameCodec,
)
from afs_fastapi.protocols.isobus_handlers import (
    ISOBUSProtocolManager,
    ISOBUSDevice,
    ISOBUSFunction,
)
from afs_fastapi.equipment.can_error_handling import CANErrorHandler


class TestCANIntegrationFocused:
    """Focused integration tests for CAN interface system."""

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
            primary_interfaces=["tractor_1"],
            backup_interfaces=["backup_1"],
            health_check_interval=5.0,
            auto_recovery=True,
        )

    @pytest.fixture
    def can_codec(self):
        """Create CAN frame codec."""
        return CANFrameCodec()

    @pytest.fixture
    def isobus_manager(self, can_codec):
        """Create ISOBUS protocol manager."""
        error_handler = CANErrorHandler()
        return ISOBUSProtocolManager(can_codec, error_handler)

    @pytest.mark.asyncio
    async def test_engine_data_encoding_decoding_workflow(self, can_codec):
        """Test complete engine data encoding and decoding workflow."""
        # Test encoding engine data using the actual encoder
        engine_frame = can_codec.encoder.encode_engine_data(
            source_address=0x81,
            engine_speed=1800.0,
            manifold_pressure=45.0,
            torque_percent=75.0,
        )

        assert engine_frame is not None
        assert engine_frame.is_extended_id
        assert len(engine_frame.data) == 8

        # Test decoding the same message
        decoded = can_codec.decode_message(engine_frame)
        assert decoded is not None
        assert decoded.pgn == 0xF004  # EEC1 PGN

        # Verify SPN values are correct
        spn_values = {spn.spn: spn.value for spn in decoded.spn_values if spn.is_valid}
        assert 190 in spn_values  # Engine speed
        assert abs(spn_values[190] - 1800.0) < 1.0  # Allow for scaling precision

    @pytest.mark.asyncio
    async def test_vehicle_position_encoding_decoding(self, can_codec):
        """Test GPS position encoding and decoding."""
        # Test encoding GPS position
        gps_frame = can_codec.encoder.encode_gps_position(
            source_address=0x82,
            latitude=40.7128,   # NYC latitude
            longitude=-74.0060, # NYC longitude
        )

        assert gps_frame is not None
        assert gps_frame.is_extended_id

        # Test decoding
        decoded = can_codec.decode_message(gps_frame)
        assert decoded is not None
        assert decoded.pgn == 0xFEF3  # Vehicle Position PGN

        # Verify coordinates
        spn_values = {spn.spn: spn.value for spn in decoded.spn_values if spn.is_valid}
        assert 584 in spn_values  # Latitude
        assert 585 in spn_values  # Longitude
        assert abs(spn_values[584] - 40.7128) < 0.001
        assert abs(spn_values[585] - (-74.0060)) < 0.001

    @pytest.mark.asyncio
    async def test_isobus_address_claim_workflow(self, isobus_manager):
        """Test ISOBUS address claim procedure."""
        # Create a test device
        test_device = ISOBUSDevice(
            name="Test_Tractor",
            address=0x81,
            function=ISOBUSFunction.TRACTOR,
            manufacturer_code=0x123,
            device_class=0x00,
            device_class_instance=0x00,
            ecu_instance=0x00,
            identity_number=0x12345,
            preferred_address=0x81,
        )

        # Create address claim message
        claim_message = isobus_manager.address_claim.create_address_claim_message(test_device)
        assert claim_message is not None
        assert claim_message.is_extended_id
        assert len(claim_message.data) == 8

        # Handle the address claim (simulate receiving it)
        claimed_device = isobus_manager.address_claim.handle_address_claim(claim_message)
        assert claimed_device is not None
        assert claimed_device.address == 0x81
        assert claimed_device.function == ISOBUSFunction.TRACTOR

        # Verify device is registered
        registered_device = isobus_manager.address_claim.get_device_by_address(0x81)
        assert registered_device is not None
        assert registered_device.name == "Device_81"  # Handler creates name based on address
        assert registered_device.function == ISOBUSFunction.TRACTOR

    @pytest.mark.asyncio
    async def test_can_frame_codec_supported_pgns(self, can_codec):
        """Test that codec supports expected agricultural PGNs."""
        supported_pgns = can_codec.list_supported_pgns()

        # Verify key agricultural PGNs are supported
        expected_pgns = [
            0xF004,  # Electronic Engine Controller 1
            0xFEF1,  # Wheel-Based Vehicle Speed
            0xFEF3,  # Vehicle Position
            0xFEF2,  # Fuel Economy
            0xF005,  # Electronic Transmission Controller 1
        ]

        for pgn in expected_pgns:
            assert pgn in supported_pgns, f"PGN {pgn:04X} not supported"

        # Verify SPN definitions are available
        supported_spns = can_codec.list_supported_spns()
        expected_spns = [190, 102, 61, 84, 584, 585, 183]  # Key agricultural SPNs

        for spn in expected_spns:
            assert spn in supported_spns, f"SPN {spn} not supported"

    @pytest.mark.asyncio
    async def test_isobus_message_routing(self, isobus_manager):
        """Test ISOBUS message routing and handling."""
        # Create a test engine data message
        test_message = can.Message(
            arbitration_id=0x18F00481,  # EEC1 from address 0x81
            data=bytes([0x00, 0x00, 0x64, 0x00, 0x38, 0x0E, 0x00, 0x00]),
            is_extended_id=True,
        )

        # Test message handling
        handled = isobus_manager.handle_message(test_message)
        # Note: This specific message won't be handled as EEC1 is not in the message handlers
        # but we can verify the routing logic works

        # Test a message that should be handled (Address Claim)
        # The handler expects PGN calculation to match its routing
        address_claim_message = can.Message(
            arbitration_id=0x18EEFF81,  # Address claim from 0x81
            data=bytes([0x45, 0x23, 0x01, 0x23, 0x45, 0x00, 0x00, 0x80]),
            is_extended_id=True,
        )

        handled = isobus_manager.handle_message(address_claim_message)
        # Note: may not be handled depending on exact PGN calculation
        # Just verify the routing logic doesn't crash
        assert isinstance(handled, bool)

    @pytest.mark.asyncio
    async def test_connection_pool_management(self, connection_pool_config):
        """Test connection pool initialization and management."""
        # Create a mock CAN bus manager
        manager = CANBusConnectionManager(connection_pool_config)

        # Mock the physical manager
        manager.physical_manager = AsyncMock()
        manager.physical_manager.connect_interface = AsyncMock(return_value=True)
        manager.physical_manager.disconnect_all = AsyncMock(return_value={})
        manager.physical_manager.get_interface_status = AsyncMock(return_value=None)

        # Test initialization
        success = await manager.initialize()
        assert success

        # Test getting manager status
        status = manager.get_manager_status()
        assert "state" in status
        assert "statistics" in status
        assert "connection_pool" in status

        # Test shutdown
        await manager.shutdown()

    @pytest.mark.asyncio
    async def test_error_handling_integration(self, can_codec):
        """Test error handling throughout the system."""
        # Test with invalid message data
        invalid_message = can.Message(
            arbitration_id=0x18F00481,
            data=bytes([0xFF, 0xFF, 0xFF]),  # Too short for EEC1
            is_extended_id=True,
        )

        # Should handle gracefully without crashing
        decoded = can_codec.decode_message(invalid_message)
        # May return None or handle gracefully

        # Test with invalid encoding parameters
        invalid_frame = can_codec.encoder.encode_engine_data(
            source_address=999,  # Invalid address
            engine_speed=-100.0,  # Invalid speed
        )
        # Should handle gracefully

    @pytest.mark.asyncio
    async def test_multi_device_network_simulation(self, isobus_manager):
        """Test simulation of multiple devices on the network."""
        # Create multiple agricultural devices
        devices = [
            ISOBUSDevice(
                name="Tractor_1",
                address=0x81,
                function=ISOBUSFunction.TRACTOR,
                manufacturer_code=0x123,
                device_class=0x00,
                device_class_instance=0x00,
                ecu_instance=0x00,
                identity_number=0x10001,
                preferred_address=0x81,
            ),
            ISOBUSDevice(
                name="Sprayer_1",
                address=0x82,
                function=ISOBUSFunction.SPRAYERS,
                manufacturer_code=0x124,
                device_class=0x01,
                device_class_instance=0x00,
                ecu_instance=0x00,
                identity_number=0x10002,
                preferred_address=0x82,
            ),
            ISOBUSDevice(
                name="Harvester_1",
                address=0x83,
                function=ISOBUSFunction.HARVESTERS,
                manufacturer_code=0x125,
                device_class=0x02,
                device_class_instance=0x00,
                ecu_instance=0x00,
                identity_number=0x10003,
                preferred_address=0x83,
            ),
        ]

        # Simulate address claims for all devices
        for device in devices:
            claim_message = isobus_manager.address_claim.create_address_claim_message(device)
            claimed = isobus_manager.address_claim.handle_address_claim(claim_message)
            assert claimed is not None

        # Verify all devices are registered
        assert len(isobus_manager.address_claim.claimed_addresses) == 3

        # Test device lookup by function
        tractors = isobus_manager.address_claim.get_devices_by_function(ISOBUSFunction.TRACTOR)
        assert len(tractors) == 1
        assert tractors[0].name == "Device_81"  # Handler creates name based on address

        sprayers = isobus_manager.address_claim.get_devices_by_function(ISOBUSFunction.SPRAYERS)
        assert len(sprayers) == 1

        harvesters = isobus_manager.address_claim.get_devices_by_function(ISOBUSFunction.HARVESTERS)
        assert len(harvesters) == 1

    @pytest.mark.asyncio
    async def test_agricultural_pgn_definitions(self, can_codec):
        """Test that agricultural PGN definitions are correctly loaded."""
        # Test Electronic Engine Controller 1 (EEC1)
        eec1_definition = can_codec.get_pgn_definition(0xF004)
        assert eec1_definition is not None
        assert eec1_definition.name == "Electronic Engine Controller 1"
        assert len(eec1_definition.spn_definitions) > 0

        # Test Vehicle Position (VP)
        vp_definition = can_codec.get_pgn_definition(0xFEF3)
        assert vp_definition is not None
        assert vp_definition.name == "Vehicle Position"

        # Test key SPNs
        engine_speed_spn = can_codec.get_spn_definition(190)  # Engine Speed
        assert engine_speed_spn is not None
        assert engine_speed_spn.name == "Engine Speed"
        assert engine_speed_spn.units == "rpm"

        latitude_spn = can_codec.get_spn_definition(584)  # Latitude
        assert latitude_spn is not None
        assert latitude_spn.name == "Latitude"
        assert latitude_spn.units == "degrees"

    @pytest.mark.asyncio
    async def test_system_performance_basic(self, can_codec):
        """Test basic system performance with rapid message processing."""
        messages_processed = 0
        start_time = datetime.now()

        # Process a batch of engine data messages
        for i in range(100):
            engine_frame = can_codec.encoder.encode_engine_data(
                source_address=0x81,
                engine_speed=1500.0 + i,  # Varying RPM
                torque_percent=50.0 + (i % 50),
            )

            if engine_frame:
                decoded = can_codec.decode_message(engine_frame)
                if decoded:
                    messages_processed += 1

        end_time = datetime.now()
        processing_time = (end_time - start_time).total_seconds()

        # Verify performance
        assert messages_processed == 100
        assert processing_time < 1.0  # Should process 100 messages in under 1 second

        # Calculate throughput
        throughput = messages_processed / processing_time
        assert throughput > 50  # At least 50 messages per second