"""
Feature tests for API serialization and enhanced FarmTractorResponse output.

This module tests the complete serialization workflow of the enhanced
FarmTractorResponse model, ensuring all robotic interface fields are
properly serialized and formatted for API consumption.
"""

import json

import pytest
from afs_fastapi.equipment.farm_tractors import FarmTractor, FieldMode


@pytest.fixture
def enhanced_tractor() -> FarmTractor:
    """
    Create a fully configured tractor with enhanced robotic features enabled.
    """
    tractor = FarmTractor("John Deere", "9RX", 2023, "https://deere.com/manual")

    # Configure basic operations
    tractor.start_engine()
    tractor.activate_hydraulics()
    tractor.change_gear(4)
    tractor.accelerate(15)

    # Configure GPS and navigation
    tractor.set_gps_position(40.123456, -85.654321)
    tractor.enable_auto_steer()
    tractor.add_waypoint(40.125000, -85.650000)
    tractor.add_waypoint(40.127000, -85.648000)
    tractor.set_heading(45.0)

    # Configure implement and field operations
    tractor.set_field_mode(FieldMode.PLANTING)
    tractor.lower_implement(8.0)
    tractor.set_implement_width(32.0)
    tractor.start_field_work()
    tractor.update_work_progress(1320)  # 1/4 mile

    # Enable autonomous features
    tractor.enable_autonomous_mode()

    return tractor


def test_api_response_serialization_basic_fields(enhanced_tractor: FarmTractor):
    """
    Test that basic tractor fields serialize correctly to API response format.
    """
    response = enhanced_tractor.to_response("tractor-001")

    # Validate core identification fields
    assert response.tractor_id == "tractor-001"
    assert response.make == "John Deere"
    assert response.model == "9RX"
    assert response.year == 2023
    assert response.manual_url == "https://deere.com/manual"

    # Validate engine and basic control fields
    assert response.engine_on is True
    assert response.speed == 15
    assert response.gear == 4
    assert response.power_takeoff is False  # Not engaged in this test
    assert response.hydraulics is True


def test_api_response_serialization_enhanced_fields(enhanced_tractor: FarmTractor):
    """
    Test that enhanced robotic interface fields serialize correctly.
    """
    response = enhanced_tractor.to_response("tractor-002")

    # GPS and Navigation
    assert response.gps_latitude == 40.123456
    assert response.gps_longitude == -85.654321
    assert response.auto_steer_enabled is True
    assert response.waypoint_count == 2
    assert response.current_heading == 45.0

    # Implement Controls
    assert response.implement_position == "lowered"
    assert response.implement_depth == 8.0
    assert response.implement_width == 32.0

    # Field Operations
    assert response.field_mode == "planting"
    assert response.work_rate > 0.0  # Should be calculated based on field work
    assert response.area_covered > 0.0  # Should have covered some area

    # Autonomous Features
    assert response.autonomous_mode is True
    assert response.obstacle_detection is True
    assert response.emergency_stop_active is False


def test_api_response_serialization_professional_fields(enhanced_tractor: FarmTractor):
    """
    Test that professional agricultural interface fields serialize correctly.
    """
    response = enhanced_tractor.to_response("tractor-003")

    # Engine and Fuel diagnostics
    assert response.engine_temp == 180.0  # Default engine temperature
    assert response.fuel_level == 100.0  # Default fuel level
    assert response.engine_rpm >= 0  # RPM should be non-negative

    # Hydraulic system
    assert response.hydraulic_pressure >= 0.0  # Should have non-negative pressure
    assert response.hydraulic_flow >= 0.0  # Should have flow rate data

    # Sensor data
    assert isinstance(response.wheel_slip, float)
    assert isinstance(response.ground_speed, float)
    assert isinstance(response.draft_load, float)

    # ISOBUS Communication
    assert response.isobus_address == 0x80  # Default ISOBUS address
    assert response.device_name == "John Deere_9RX_2023"

    # Safety Systems
    assert response.safety_system_active is True
    assert response.safety_level in ["PLc", "PLd", "PLe"]

    # Vision & Sensor Systems
    assert response.lidar_enabled is False  # Default state
    assert response.obstacle_count == 0  # No obstacles by default

    # Power Management
    assert response.regenerative_mode is False  # Default state


def test_api_response_json_serialization(enhanced_tractor: FarmTractor):
    """
    Test that the API response can be fully serialized to JSON.
    """
    response = enhanced_tractor.to_response("tractor-004")

    # Convert to JSON and back to ensure complete serializability
    json_data = response.model_dump()
    json_string = json.dumps(json_data, indent=2)
    parsed_data = json.loads(json_string)

    # Validate key fields in JSON
    assert parsed_data["tractor_id"] == "tractor-004"
    assert parsed_data["make"] == "John Deere"
    assert parsed_data["autonomous_mode"] is True
    assert parsed_data["waypoint_count"] == 2
    assert parsed_data["field_mode"] == "planting"
    assert parsed_data["safety_level"] in ["PLc", "PLd", "PLe"]

    # Ensure all enhanced fields are present
    enhanced_fields = [
        "waypoint_count",
        "current_heading",
        "implement_depth",
        "implement_width",
        "work_rate",
        "area_covered",
        "engine_temp",
        "hydraulic_flow",
        "wheel_slip",
        "ground_speed",
        "draft_load",
        "autonomous_mode",
        "obstacle_detection",
        "emergency_stop_active",
        "isobus_address",
        "device_name",
        "safety_system_active",
        "safety_level",
        "regenerative_mode",
        "lidar_enabled",
        "obstacle_count",
    ]

    for field in enhanced_fields:
        assert field in parsed_data, f"Enhanced field '{field}' missing from JSON output"


def test_api_response_field_types_and_validation(enhanced_tractor: FarmTractor):
    """
    Test that API response fields have correct types and pass Pydantic validation.
    """
    response = enhanced_tractor.to_response("tractor-005")

    # Integer fields
    assert isinstance(response.waypoint_count, int)
    assert isinstance(response.engine_rpm, int)
    assert isinstance(response.isobus_address, int)
    assert isinstance(response.obstacle_count, int)

    # Float fields
    assert isinstance(response.current_heading, float)
    assert isinstance(response.implement_depth, float)
    assert isinstance(response.implement_width, float)
    assert isinstance(response.work_rate, float)
    assert isinstance(response.area_covered, float)
    assert isinstance(response.engine_temp, float)

    # Boolean fields
    assert isinstance(response.autonomous_mode, bool)
    assert isinstance(response.obstacle_detection, bool)
    assert isinstance(response.emergency_stop_active, bool)
    assert isinstance(response.safety_system_active, bool)
    assert isinstance(response.regenerative_mode, bool)
    assert isinstance(response.lidar_enabled, bool)

    # String/Literal fields
    assert response.implement_position in ["raised", "lowered", "transport"]
    assert response.field_mode in [
        "transport",
        "tillage",
        "planting",
        "spraying",
        "harvesting",
        "maintenance",
    ]
    assert response.safety_level in ["PLc", "PLd", "PLe"]


def test_api_response_emergency_stop_serialization():
    """
    Test API response serialization during emergency stop conditions.
    """
    tractor = FarmTractor("Case IH", "Magnum", 2024)
    tractor.start_engine()
    tractor.set_gps_position(40.0, -85.0)  # Set GPS position
    tractor.enable_auto_steer()  # Enable auto-steer first
    tractor.add_waypoint(40.1, -85.1)  # Add waypoint for autonomous mode
    tractor.enable_autonomous_mode()

    # Trigger emergency stop
    tractor.emergency_stop()

    response = tractor.to_response("emergency-test")

    # Validate emergency stop affects serialized state
    assert response.emergency_stop_active is True
    assert response.autonomous_mode is False  # Should be disabled
    assert response.speed == 0  # Should be stopped

    # Ensure other fields remain intact
    assert response.make == "Case IH"
    assert response.model == "Magnum"
    assert response.year == 2024


def test_api_response_comprehensive_field_coverage():
    """
    Test that all 40 expected API response fields are present and serializable.
    """
    tractor = FarmTractor("New Holland", "T7", 2025)
    response = tractor.to_response("comprehensive-test")

    # Count all fields that should be in the response
    expected_fields = {
        # Core Identification (5)
        "tractor_id",
        "make",
        "model",
        "year",
        "manual_url",
        # Engine and Basic Controls (5)
        "engine_on",
        "speed",
        "gear",
        "power_takeoff",
        "hydraulics",
        # GPS and Navigation (5)
        "gps_latitude",
        "gps_longitude",
        "auto_steer_enabled",
        "waypoint_count",
        "current_heading",
        # Implement Controls (3)
        "implement_position",
        "implement_depth",
        "implement_width",
        # Field Operations (3)
        "field_mode",
        "work_rate",
        "area_covered",
        # Engine and Fuel (3)
        "fuel_level",
        "engine_rpm",
        "engine_temp",
        # Hydraulics (2)
        "hydraulic_pressure",
        "hydraulic_flow",
        # Sensors (3)
        "wheel_slip",
        "ground_speed",
        "draft_load",
        # Autonomous Features (3)
        "autonomous_mode",
        "obstacle_detection",
        "emergency_stop_active",
        # ISOBUS Communication (2)
        "isobus_address",
        "device_name",
        # Safety Systems (2)
        "safety_system_active",
        "safety_level",
        # Vision & Sensor Systems (2)
        "lidar_enabled",
        "obstacle_count",
        # Power Management (1)
        "regenerative_mode",
        # System Status (1)
        "status",
    }

    # Validate all expected fields are present
    response_dict = response.model_dump()
    actual_fields = set(response_dict.keys())

    missing_fields = expected_fields - actual_fields
    extra_fields = actual_fields - expected_fields

    assert not missing_fields, f"Missing fields: {missing_fields}"
    assert not extra_fields, f"Unexpected extra fields: {extra_fields}"
    assert len(actual_fields) == 40, f"Expected 40 fields, got {len(actual_fields)}"
