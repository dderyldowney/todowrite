"""
Test suite for CAN frame encoding/decoding utilities.

Tests comprehensive J1939/ISOBUS message encoding and decoding for agricultural
equipment communication, following Test-First Development (TDD) methodology.
"""

from __future__ import annotations

import struct

import can
import pytest

from afs_fastapi.core.can_frame_codec import (
    CANFrameCodec,
    J1939DataType,
    J1939Decoder,
    J1939Encoder,
    PGNDefinition,
    SPNDefinition,
)


class TestSPNDefinition:
    """Test SPN definition and basic structures."""

    def test_spn_definition_creation(self) -> None:
        """Test creating SPN definition with agricultural parameters."""
        spn = SPNDefinition(
            spn=190,
            name="Engine Speed",
            description="Actual engine speed from ECU",
            data_type=J1939DataType.RPM,
            start_bit=24,
            bit_length=16,
            scale=0.125,
            units="rpm",
            min_value=0,
            max_value=8031.875,
            not_available_value=0xFFFF,
        )

        assert spn.spn == 190
        assert spn.name == "Engine Speed"
        assert spn.data_type == J1939DataType.RPM
        assert spn.scale == 0.125
        assert spn.units == "rpm"

    def test_pgn_definition_with_multiple_spns(self) -> None:
        """Test PGN definition containing multiple SPNs."""
        spns = [
            SPNDefinition(
                spn=190,
                name="Engine Speed",
                description="Engine RPM",
                data_type=J1939DataType.RPM,
                start_bit=24,
                bit_length=16,
                scale=0.125,
                units="rpm",
            ),
            SPNDefinition(
                spn=102,
                name="Manifold Pressure",
                description="Intake pressure",
                data_type=J1939DataType.PRESSURE,
                start_bit=8,
                bit_length=8,
                scale=2.0,
                units="kPa",
            ),
        ]

        pgn = PGNDefinition(
            pgn=0xF004,
            name="Electronic Engine Controller 1",
            description="Engine parameters",
            data_length=8,
            transmission_rate=50,
            spn_definitions=spns,
        )

        assert pgn.pgn == 0xF004
        assert len(pgn.spn_definitions) == 2
        assert pgn.data_length == 8


class TestJ1939Decoder:
    """Test J1939 message decoding functionality."""

    @pytest.fixture
    def decoder(self) -> J1939Decoder:
        """Create J1939 decoder for testing."""
        return J1939Decoder()

    def test_decoder_initialization_with_agricultural_pgns(self, decoder: J1939Decoder) -> None:
        """Test decoder initializes with standard agricultural PGNs."""
        # Check for key agricultural PGNs
        assert 0xF004 in decoder.pgn_definitions  # EEC1
        assert 0xFEF1 in decoder.pgn_definitions  # WVS
        assert 0xFEF3 in decoder.pgn_definitions  # VP
        assert 0xFEF2 in decoder.pgn_definitions  # LFE
        assert 0xF005 in decoder.pgn_definitions  # ETC1

        # Check for key SPNs
        assert 190 in decoder.spn_definitions  # Engine Speed
        assert 84 in decoder.spn_definitions  # Vehicle Speed
        assert 584 in decoder.spn_definitions  # Latitude
        assert 585 in decoder.spn_definitions  # Longitude

    def test_j1939_id_parsing(self, decoder: J1939Decoder) -> None:
        """Test parsing J1939 components from CAN ID."""
        # Test EEC1 message: Priority 3, PGN 0xF004, Source 0x00
        can_id = 0x18F00400
        result = decoder._parse_j1939_id(can_id)

        assert result is not None
        priority, data_page, pdu_format, pdu_specific, source_address = result

        assert priority == 6  # (0x18 >> 2) & 0x07 = 6
        assert data_page == 0
        assert pdu_format == 0xF0
        assert pdu_specific == 0x04
        assert source_address == 0x00

    def test_eec1_message_decoding(self, decoder: J1939Decoder) -> None:
        """Test decoding Electronic Engine Controller 1 message."""
        # Create EEC1 message with known values
        # Engine Speed: 1800 RPM = 1800/0.125 = 14400 = 0x3840
        # Manifold Pressure: 200 kPa = 200/2 = 100 = 0x64
        # Torque: 75% = 75+125 = 200 = 0xC8
        data = bytearray(8)
        data[3] = 0x40  # Engine speed low byte
        data[4] = 0x38  # Engine speed high byte
        data[1] = 0x64  # Manifold pressure
        data[2] = 0xC8  # Torque percent

        message = can.Message(
            arbitration_id=0x18F00400,  # EEC1 from engine ECU
            data=bytes(data),
            is_extended_id=True,
            timestamp=1234567890.0,
        )

        decoded = decoder.decode_can_message(message)

        assert decoded is not None
        assert decoded.pgn == 0xF004
        assert decoded.name == "Electronic Engine Controller 1"
        assert decoded.source_address == 0x00
        assert len(decoded.spn_values) == 3

        # Check engine speed
        engine_speed = next((spn for spn in decoded.spn_values if spn.spn == 190), None)
        assert engine_speed is not None
        assert engine_speed.is_valid
        assert abs(engine_speed.value - 1800.0) < 0.1

        # Check manifold pressure
        pressure = next((spn for spn in decoded.spn_values if spn.spn == 102), None)
        assert pressure is not None
        assert pressure.is_valid
        assert abs(pressure.value - 200.0) < 0.1

        # Check torque
        torque = next((spn for spn in decoded.spn_values if spn.spn == 61), None)
        assert torque is not None
        assert torque.is_valid
        assert abs(torque.value - 75.0) < 0.1

    def test_vehicle_speed_message_decoding(self, decoder: J1939Decoder) -> None:
        """Test decoding Wheel-Based Vehicle Speed message."""
        # Vehicle Speed: 25.5 km/h = 25.5/0.00390625 = 6528 = 0x1980
        data = bytearray(8)
        data[1] = 0x80  # Speed low byte
        data[2] = 0x19  # Speed high byte

        message = can.Message(
            arbitration_id=0x18FEF10B,  # WVS from transmission ECU
            data=bytes(data),
            is_extended_id=True,
        )

        decoded = decoder.decode_can_message(message)

        assert decoded is not None
        assert decoded.pgn == 0xFEF1
        assert decoded.name == "Wheel-Based Vehicle Speed"
        assert decoded.source_address == 0x0B

        # Check vehicle speed
        speed = next((spn for spn in decoded.spn_values if spn.spn == 84), None)
        assert speed is not None
        assert speed.is_valid
        assert abs(speed.value - 25.5) < 0.1

    def test_gps_position_message_decoding(self, decoder: J1939Decoder) -> None:
        """Test decoding Vehicle Position (GPS) message."""
        # Latitude: 40.7128° = 40.7128 * 10^7 = 407128000 = 0x184444E0
        # Longitude: -74.0060° = -74.0060 * 10^7 = -740060000 = 0xD3E13640
        data = bytearray(8)

        # Pack latitude (little-endian)
        lat_bytes = struct.pack("<I", 407128000)
        data[0:4] = lat_bytes

        # Pack longitude (little-endian)
        lon_bytes = struct.pack("<i", -740060000)  # Signed for negative
        data[4:8] = lon_bytes

        message = can.Message(
            arbitration_id=0x18FEF325,  # VP from GPS receiver
            data=bytes(data),
            is_extended_id=True,
        )

        decoded = decoder.decode_can_message(message)

        assert decoded is not None
        assert decoded.pgn == 0xFEF3
        assert decoded.name == "Vehicle Position"

        # Check latitude
        latitude = next((spn for spn in decoded.spn_values if spn.spn == 584), None)
        assert latitude is not None
        assert latitude.is_valid
        assert abs(latitude.value - 40.7128) < 0.0001

        # Check longitude
        longitude = next((spn for spn in decoded.spn_values if spn.spn == 585), None)
        assert longitude is not None
        assert longitude.is_valid
        assert abs(longitude.value - (-74.0060)) < 0.0001

    def test_not_available_value_handling(self, decoder: J1939Decoder) -> None:
        """Test handling of 'not available' values in SPN data."""
        # Create EEC1 message with engine speed = 0xFFFF (not available)
        data = bytearray(8)
        data[3] = 0xFF  # Engine speed low byte (not available)
        data[4] = 0xFF  # Engine speed high byte (not available)

        message = can.Message(
            arbitration_id=0x18F00400,
            data=bytes(data),
            is_extended_id=True,
        )

        decoded = decoder.decode_can_message(message)

        assert decoded is not None

        # Check engine speed is marked as not available
        engine_speed = next((spn for spn in decoded.spn_values if spn.spn == 190), None)
        assert engine_speed is not None
        assert not engine_speed.is_valid
        assert engine_speed.is_not_available
        assert engine_speed.value is None

    def test_unknown_pgn_handling(self, decoder: J1939Decoder) -> None:
        """Test handling of unknown PGN messages."""
        message = can.Message(
            arbitration_id=0x18DEAD25,  # Unknown PGN
            data=b"\x01\x02\x03\x04\x05\x06\x07\x08",
            is_extended_id=True,
        )

        decoded = decoder.decode_can_message(message)
        assert decoded is None

    def test_standard_frame_ignoring(self, decoder: J1939Decoder) -> None:
        """Test that standard (11-bit) CAN frames are ignored."""
        message = can.Message(
            arbitration_id=0x123,  # Standard frame
            data=b"\x01\x02\x03\x04",
            is_extended_id=False,
        )

        decoded = decoder.decode_can_message(message)
        assert decoded is None


class TestJ1939Encoder:
    """Test J1939 message encoding functionality."""

    @pytest.fixture
    def encoder(self) -> J1939Encoder:
        """Create J1939 encoder for testing."""
        return J1939Encoder()

    def test_engine_data_encoding(self, encoder: J1939Encoder) -> None:
        """Test encoding engine data into EEC1 message."""
        message = encoder.encode_engine_data(
            source_address=0x00,
            engine_speed=1800.0,
            manifold_pressure=200.0,
            torque_percent=75.0,
        )

        assert message is not None
        assert message.arbitration_id == 0x18F00400
        assert message.is_extended_id
        assert len(message.data) == 8

        # Verify encoded values by decoding back
        decoder = J1939Decoder()
        decoded = decoder.decode_can_message(message)

        assert decoded is not None

        # Check engine speed
        engine_speed = next((spn for spn in decoded.spn_values if spn.spn == 190), None)
        assert engine_speed is not None
        assert abs(engine_speed.value - 1800.0) < 1.0  # Allow for rounding

    def test_vehicle_speed_encoding(self, encoder: J1939Encoder) -> None:
        """Test encoding vehicle speed data."""
        message = encoder.encode_vehicle_speed(
            source_address=0x0B,
            speed_kmh=25.5,
        )

        assert message is not None
        assert message.arbitration_id == 0x18FEF10B
        assert message.is_extended_id

        # Verify by decoding
        decoder = J1939Decoder()
        decoded = decoder.decode_can_message(message)

        assert decoded is not None
        speed = next((spn for spn in decoded.spn_values if spn.spn == 84), None)
        assert speed is not None
        assert abs(speed.value - 25.5) < 0.1

    def test_gps_position_encoding(self, encoder: J1939Encoder) -> None:
        """Test encoding GPS position data."""
        message = encoder.encode_gps_position(
            source_address=0x25,
            latitude=40.7128,
            longitude=-74.0060,
        )

        assert message is not None
        assert message.arbitration_id == 0x18FEF325
        assert message.is_extended_id

        # Verify by decoding
        decoder = J1939Decoder()
        decoded = decoder.decode_can_message(message)

        assert decoded is not None

        latitude = next((spn for spn in decoded.spn_values if spn.spn == 584), None)
        longitude = next((spn for spn in decoded.spn_values if spn.spn == 585), None)

        assert latitude is not None
        assert longitude is not None
        assert abs(latitude.value - 40.7128) < 0.001
        assert abs(longitude.value - (-74.0060)) < 0.001

    def test_custom_pgn_encoding(self, encoder: J1939Encoder) -> None:
        """Test encoding custom PGN with specific SPN values."""
        spn_values = {
            190: 2000.0,  # Engine speed
            102: 250.0,  # Manifold pressure
        }

        message = encoder.encode_pgn_message(
            pgn=0xF004,
            source_address=0x00,
            spn_values=spn_values,
            priority=3,
        )

        assert message is not None
        assert (message.arbitration_id >> 26) & 0x07 == 3  # Check priority

        # Verify encoding
        decoder = J1939Decoder()
        decoded = decoder.decode_can_message(message)

        assert decoded is not None
        assert decoded.priority == 3

        engine_speed = next((spn for spn in decoded.spn_values if spn.spn == 190), None)
        pressure = next((spn for spn in decoded.spn_values if spn.spn == 102), None)

        assert engine_speed is not None
        assert pressure is not None
        assert abs(engine_speed.value - 2000.0) < 1.0
        assert abs(pressure.value - 250.0) < 1.0

    def test_encoding_with_none_values(self, encoder: J1939Encoder) -> None:
        """Test encoding with None values (not available)."""
        spn_values = {
            190: None,  # Engine speed not available
            102: 180.0,  # Manifold pressure available
        }

        message = encoder.encode_pgn_message(
            pgn=0xF004,
            source_address=0x00,
            spn_values=spn_values,
        )

        assert message is not None

        # Verify encoding
        decoder = J1939Decoder()
        decoded = decoder.decode_can_message(message)

        assert decoded is not None

        engine_speed = next((spn for spn in decoded.spn_values if spn.spn == 190), None)
        pressure = next((spn for spn in decoded.spn_values if spn.spn == 102), None)

        assert engine_speed is not None
        assert engine_speed.is_not_available
        assert pressure is not None
        assert pressure.is_valid
        assert abs(pressure.value - 180.0) < 1.0

    def test_unknown_pgn_encoding_failure(self, encoder: J1939Encoder) -> None:
        """Test that encoding unknown PGN fails gracefully."""
        message = encoder.encode_pgn_message(
            pgn=0xDEAD,  # Unknown PGN
            source_address=0x00,
            spn_values={1234: 42.0},
        )

        assert message is None


class TestCANFrameCodec:
    """Test complete CAN frame codec functionality."""

    @pytest.fixture
    def codec(self) -> CANFrameCodec:
        """Create CAN frame codec for testing."""
        return CANFrameCodec()

    def test_codec_round_trip_engine_data(self, codec: CANFrameCodec) -> None:
        """Test complete encode/decode round trip for engine data."""
        # Original data
        original_spn_values = {
            190: 1850.0,  # Engine speed
            102: 220.0,  # Manifold pressure
            61: 80.0,  # Torque percent
        }

        # Encode
        encoded_message = codec.encode_message(
            pgn=0xF004,
            source_address=0x00,
            spn_values=original_spn_values,
        )

        assert encoded_message is not None

        # Decode
        decoded_message = codec.decode_message(encoded_message)

        assert decoded_message is not None
        assert decoded_message.pgn == 0xF004
        assert len(decoded_message.spn_values) == 3

        # Verify values within tolerance
        for spn_value in decoded_message.spn_values:
            original_value = original_spn_values[spn_value.spn]
            assert abs(spn_value.value - original_value) < 1.0

    def test_codec_pgn_definition_access(self, codec: CANFrameCodec) -> None:
        """Test accessing PGN and SPN definitions."""
        # Test PGN definition access
        eec1_def = codec.get_pgn_definition(0xF004)
        assert eec1_def is not None
        assert eec1_def.name == "Electronic Engine Controller 1"
        assert len(eec1_def.spn_definitions) >= 3

        # Test SPN definition access
        engine_speed_def = codec.get_spn_definition(190)
        assert engine_speed_def is not None
        assert engine_speed_def.name == "Engine Speed"
        assert engine_speed_def.units == "rpm"

        # Test unknown definitions
        assert codec.get_pgn_definition(0xDEAD) is None
        assert codec.get_spn_definition(99999) is None

    def test_codec_supported_pgns_and_spns(self, codec: CANFrameCodec) -> None:
        """Test listing supported PGNs and SPNs."""
        supported_pgns = codec.list_supported_pgns()
        supported_spns = codec.list_supported_spns()

        assert len(supported_pgns) >= 5  # At least 5 agricultural PGNs
        assert len(supported_spns) >= 10  # At least 10 SPNs

        # Check for key agricultural PGNs
        assert 0xF004 in supported_pgns  # EEC1
        assert 0xFEF1 in supported_pgns  # WVS
        assert 0xFEF3 in supported_pgns  # VP

        # Check for key SPNs
        assert 190 in supported_spns  # Engine Speed
        assert 84 in supported_spns  # Vehicle Speed
        assert 584 in supported_spns  # Latitude


class TestAgriculturalMessageScenarios:
    """Test real-world agricultural messaging scenarios."""

    @pytest.fixture
    def codec(self) -> CANFrameCodec:
        """Create codec for testing."""
        return CANFrameCodec()

    def test_tractor_field_operation_messages(self, codec: CANFrameCodec) -> None:
        """Test typical message sequence during field operations."""
        # Engine ECU reporting operational data
        engine_msg = codec.encode_message(
            pgn=0xF004,
            source_address=0x00,  # Engine ECU
            spn_values={
                190: 2100.0,  # Engine RPM at PTO speed
                102: 180.0,  # Manifold pressure under load
                61: 85.0,  # High torque demand
            },
        )

        # Transmission reporting vehicle movement
        speed_msg = codec.encode_message(
            pgn=0xFEF1,
            source_address=0x03,  # Transmission ECU
            spn_values={84: 12.5},  # Field working speed
        )

        # GPS receiver reporting position
        gps_msg = codec.encode_message(
            pgn=0xFEF3,
            source_address=0x25,  # GPS receiver
            spn_values={
                584: 42.3601,  # Farm latitude
                585: -71.0589,  # Farm longitude
            },
        )

        # Fuel system reporting consumption
        fuel_msg = codec.encode_message(
            pgn=0xFEF2,
            source_address=0x17,  # Fuel system ECU
            spn_values={
                183: 25.5,  # Current fuel rate L/h
                184: 2.1,  # Fuel economy km/L
            },
        )

        # Verify all messages encode successfully
        assert engine_msg is not None
        assert speed_msg is not None
        assert gps_msg is not None
        assert fuel_msg is not None

        # Decode and verify each message
        decoded_engine = codec.decode_message(engine_msg)
        decoded_speed = codec.decode_message(speed_msg)
        decoded_gps = codec.decode_message(gps_msg)
        decoded_fuel = codec.decode_message(fuel_msg)

        assert decoded_engine is not None
        assert decoded_speed is not None
        assert decoded_gps is not None
        assert decoded_fuel is not None

        # Verify source addresses match expected ECUs
        assert decoded_engine.source_address == 0x00
        assert decoded_speed.source_address == 0x03
        assert decoded_gps.source_address == 0x25
        assert decoded_fuel.source_address == 0x17

    def test_precision_agriculture_data_encoding(self, codec: CANFrameCodec) -> None:
        """Test encoding high-precision agricultural data."""
        # High-precision GPS coordinates (6 decimal places)
        precision_coords = {
            584: 40.123456,  # Precision latitude
            585: -74.987654,  # Precision longitude
        }

        gps_msg = codec.encode_message(pgn=0xFEF3, source_address=0x25, spn_values=precision_coords)

        assert gps_msg is not None

        # Decode and check precision retention
        decoded = codec.decode_message(gps_msg)
        assert decoded is not None

        lat_spn = next((spn for spn in decoded.spn_values if spn.spn == 584), None)
        lon_spn = next((spn for spn in decoded.spn_values if spn.spn == 585), None)

        assert lat_spn is not None
        assert lon_spn is not None

        # Check precision within J1939 latitude/longitude resolution (10^-7 degrees)
        assert abs(lat_spn.value - 40.123456) < 1e-6
        assert abs(lon_spn.value - (-74.987654)) < 1e-6

    def test_extreme_operating_conditions(self, codec: CANFrameCodec) -> None:
        """Test encoding data at extreme operating conditions."""
        # High-performance engine at maximum rated conditions
        extreme_engine = {
            190: 3000.0,  # Maximum engine RPM
            102: 300.0,  # High boost pressure
            61: 100.0,  # Maximum torque output
        }

        # High-speed transport conditions
        extreme_speed = {
            84: 80.0,  # High road speed km/h
        }

        engine_msg = codec.encode_message(0xF004, 0x00, extreme_engine)
        speed_msg = codec.encode_message(0xFEF1, 0x03, extreme_speed)

        assert engine_msg is not None
        assert speed_msg is not None

        # Verify extreme values are handled correctly
        decoded_engine = codec.decode_message(engine_msg)
        decoded_speed = codec.decode_message(speed_msg)

        assert decoded_engine is not None
        assert decoded_speed is not None

        # Check that extreme values are within valid ranges
        engine_speed = next((spn for spn in decoded_engine.spn_values if spn.spn == 190), None)
        vehicle_speed = next((spn for spn in decoded_speed.spn_values if spn.spn == 84), None)

        assert engine_speed is not None
        assert vehicle_speed is not None
        assert engine_speed.is_valid
        assert vehicle_speed.is_valid

    def test_mixed_valid_and_invalid_data(self, codec: CANFrameCodec) -> None:
        """Test handling mixed valid and invalid SPN data."""
        mixed_data = {
            190: 1800.0,  # Valid engine speed
            102: None,  # Not available manifold pressure
            61: 65.0,  # Valid torque
        }

        message = codec.encode_message(0xF004, 0x00, mixed_data)
        assert message is not None

        decoded = codec.decode_message(message)
        assert decoded is not None

        # Check that valid and invalid data are handled correctly
        engine_speed = next((spn for spn in decoded.spn_values if spn.spn == 190), None)
        pressure = next((spn for spn in decoded.spn_values if spn.spn == 102), None)
        torque = next((spn for spn in decoded.spn_values if spn.spn == 61), None)

        assert engine_speed is not None and engine_speed.is_valid
        assert pressure is not None and pressure.is_not_available
        assert torque is not None and torque.is_valid
