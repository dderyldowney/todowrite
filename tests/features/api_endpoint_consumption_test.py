"""
Feature tests for API endpoint consumption and enhanced FarmTractorResponse integration.

This module tests the complete API workflow from endpoint requests through
response serialization, ensuring all enhanced robotic interface fields are
properly exposed and consumable via HTTP API.
"""

import json
from typing import Any

import pytest
from fastapi.testclient import TestClient

from afs_fastapi.api.main import app


@pytest.fixture
def client() -> TestClient:
    """
    Create a FastAPI test client for API endpoint testing.
    """
    return TestClient(app)


def test_tractor_endpoint_basic_connectivity(client: TestClient):
    """
    Test basic connectivity to the tractor status endpoint.
    """
    response = client.get("/equipment/tractor/test-001")

    assert response.status_code == 200
    assert response.headers["content-type"] == "application/json"

    data = response.json()
    assert "tractor_id" in data
    assert data["tractor_id"] == "test-001"


def test_tractor_endpoint_enhanced_response_structure(client: TestClient):
    """
    Test that the tractor endpoint returns all enhanced robotic interface fields.
    """
    response = client.get("/equipment/tractor/robotic-test")

    assert response.status_code == 200
    data = response.json()

    # Core Identification fields
    assert "tractor_id" in data
    assert "make" in data
    assert "model" in data
    assert "year" in data
    # Note: manual_url may be excluded if None due to response_model_exclude_none=True

    # Enhanced GPS and Navigation fields
    assert "waypoint_count" in data
    assert "current_heading" in data
    assert "auto_steer_enabled" in data

    # Enhanced Implement Controls
    assert "implement_depth" in data
    assert "implement_width" in data
    assert "implement_position" in data

    # Enhanced Field Operations
    assert "work_rate" in data
    assert "area_covered" in data
    assert "field_mode" in data

    # Enhanced Autonomous Features
    assert "autonomous_mode" in data
    assert "obstacle_detection" in data
    assert "emergency_stop_active" in data

    # Enhanced ISOBUS Communication
    assert "isobus_address" in data
    assert "device_name" in data

    # Enhanced Safety Systems
    assert "safety_system_active" in data
    assert "safety_level" in data

    # Enhanced Vision & Sensor Systems
    assert "lidar_enabled" in data
    assert "obstacle_count" in data

    # Enhanced Power Management
    assert "regenerative_mode" in data


def test_tractor_endpoint_field_types_validation(client: TestClient):
    """
    Test that API endpoint returns correctly typed fields.
    """
    response = client.get("/equipment/tractor/type-test")

    assert response.status_code == 200
    data = response.json()

    # Integer fields
    assert isinstance(data["waypoint_count"], int)
    assert isinstance(data["engine_rpm"], int)
    assert isinstance(data["isobus_address"], int)
    assert isinstance(data["obstacle_count"], int)
    assert isinstance(data["year"], int)

    # Float fields
    assert isinstance(data["current_heading"], int | float)
    assert isinstance(data["implement_depth"], int | float)
    assert isinstance(data["implement_width"], int | float)
    assert isinstance(data["work_rate"], int | float)
    assert isinstance(data["area_covered"], int | float)
    assert isinstance(data["engine_temp"], int | float)

    # Boolean fields
    assert isinstance(data["autonomous_mode"], bool)
    assert isinstance(data["obstacle_detection"], bool)
    assert isinstance(data["emergency_stop_active"], bool)
    assert isinstance(data["safety_system_active"], bool)
    assert isinstance(data["regenerative_mode"], bool)
    assert isinstance(data["lidar_enabled"], bool)
    assert isinstance(data["engine_on"], bool)

    # String fields
    assert isinstance(data["make"], str)
    assert isinstance(data["model"], str)
    assert isinstance(data["device_name"], str)
    assert isinstance(data["status"], str)

    # Literal/enum fields
    assert data["implement_position"] in ["raised", "lowered", "transport"]
    assert data["field_mode"] in [
        "transport",
        "tillage",
        "planting",
        "spraying",
        "harvesting",
        "maintenance",
    ]
    assert data["safety_level"] in ["PLc", "PLd", "PLe"]


def test_tractor_endpoint_professional_agriculture_fields(client: TestClient):
    """
    Test that professional agricultural fields are exposed correctly via API.
    """
    response = client.get("/equipment/tractor/pro-ag-test")

    assert response.status_code == 200
    data = response.json()

    # Validate ISOBUS communication fields
    assert "isobus_address" in data
    assert data["isobus_address"] == 128  # 0x80 in decimal
    assert "device_name" in data
    assert "John Deere_9RX_2023" in data["device_name"]

    # Validate safety system compliance
    assert "safety_system_active" in data
    assert data["safety_system_active"] is True
    assert "safety_level" in data
    assert data["safety_level"] == "PLc"  # Default performance level

    # Validate sensor and diagnostic data
    assert "engine_temp" in data
    assert data["engine_temp"] == 180.0  # Default engine temperature
    assert "hydraulic_pressure" in data
    assert "hydraulic_flow" in data
    assert "wheel_slip" in data
    assert "ground_speed" in data
    assert "draft_load" in data

    # Validate autonomous capabilities
    assert "obstacle_detection" in data
    assert data["obstacle_detection"] is True
    assert "obstacle_count" in data
    assert data["obstacle_count"] == 0  # Default no obstacles


def test_tractor_endpoint_multiple_requests_consistency(client: TestClient):
    """
    Test that multiple requests to the tractor endpoint return consistent structure.
    """
    tractor_ids = ["consistency-1", "consistency-2", "consistency-3"]
    responses: list[dict[str, Any]] = []

    for tractor_id in tractor_ids:
        response = client.get(f"/equipment/tractor/{tractor_id}")
        assert response.status_code == 200
        response_data: dict[str, Any] = response.json()
        responses.append(response_data)

    # Verify all responses have the same structure
    first_response_keys = set(responses[0].keys())

    for i, response_data in enumerate(responses[1:], 1):
        response_keys = set(response_data.keys())
        assert response_keys == first_response_keys, f"Response {i} has different structure"

        # Verify tractor_id is correctly set
        assert response_data["tractor_id"] == tractor_ids[i]

    # Verify all responses have the expected number of fields (37 when None fields are excluded)
    assert len(first_response_keys) == 37, f"Expected 37 fields, got {len(first_response_keys)}"


def test_tractor_endpoint_json_schema_compliance(client: TestClient):
    """
    Test that the API endpoint response complies with expected JSON schema.
    """
    response = client.get("/equipment/tractor/schema-test")

    assert response.status_code == 200
    data = response.json()

    # Test that the response can be serialized and deserialized
    json_string = json.dumps(data)
    parsed_data = json.loads(json_string)

    assert parsed_data == data, "JSON serialization/deserialization failed"

    # Validate specific schema requirements
    required_fields = [
        "tractor_id",
        "make",
        "model",
        "year",
        "engine_on",
        "speed",
        "gear",
        "waypoint_count",
        "current_heading",
        "implement_depth",
        "implement_width",
        "autonomous_mode",
        "safety_level",
        "device_name",
        "status",
    ]

    for field in required_fields:
        assert field in data, f"Required field '{field}' missing from response"


def test_tractor_endpoint_enhanced_navigation_data(client: TestClient):
    """
    Test that enhanced navigation and GPS data is properly exposed via API.
    """
    response = client.get("/equipment/tractor/nav-test")

    assert response.status_code == 200
    data = response.json()

    # GPS coordinate fields (may be excluded if None due to response_model_exclude_none=True)
    # These fields will only be present if GPS is set
    # Either both should be present or both should be absent

    # Navigation status fields
    assert "auto_steer_enabled" in data
    assert isinstance(data["auto_steer_enabled"], bool)

    # Waypoint management
    assert "waypoint_count" in data
    assert data["waypoint_count"] >= 0

    # Heading information
    assert "current_heading" in data
    assert isinstance(data["current_heading"], int | float)
    assert 0.0 <= data["current_heading"] < 360.0


def test_tractor_endpoint_field_operations_data(client: TestClient):
    """
    Test that field operations data is properly exposed via API.
    """
    response = client.get("/equipment/tractor/field-ops-test")

    assert response.status_code == 200
    data = response.json()

    # Field mode validation
    assert "field_mode" in data
    assert data["field_mode"] in [
        "transport",
        "tillage",
        "planting",
        "spraying",
        "harvesting",
        "maintenance",
    ]

    # Work tracking fields
    assert "work_rate" in data
    assert isinstance(data["work_rate"], int | float)
    assert data["work_rate"] >= 0.0

    assert "area_covered" in data
    assert isinstance(data["area_covered"], int | float)
    assert data["area_covered"] >= 0.0

    # Implement status
    assert "implement_position" in data
    assert data["implement_position"] in ["raised", "lowered", "transport"]

    assert "implement_depth" in data
    assert isinstance(data["implement_depth"], int | float)
    assert data["implement_depth"] >= 0.0

    assert "implement_width" in data
    assert isinstance(data["implement_width"], int | float)
    assert data["implement_width"] >= 0.0


def test_api_endpoint_error_handling(client: TestClient):
    """
    Test API endpoint error handling for invalid requests.
    """
    # Test with empty tractor ID
    response = client.get("/equipment/tractor/")
    assert response.status_code == 404  # Not Found - missing path parameter

    # Test with special characters in tractor ID (should still work)
    response = client.get("/equipment/tractor/test-special-chars-123")
    assert response.status_code == 200


def test_api_endpoint_performance_and_response_time(client: TestClient):
    """
    Test API endpoint performance and response time characteristics.
    """
    import time

    start_time = time.time()
    response = client.get("/equipment/tractor/performance-test")
    end_time = time.time()

    assert response.status_code == 200

    # Response should be reasonably fast (under 1 second for this simple case)
    response_time = end_time - start_time
    assert response_time < 1.0, f"Response took too long: {response_time:.3f} seconds"

    # Response should have reasonable size (not too large)
    data = response.json()
    json_size = len(json.dumps(data))
    assert json_size < 10000, f"Response too large: {json_size} bytes"  # Reasonable limit


def test_api_endpoint_comprehensive_integration(client: TestClient):
    """
    Comprehensive integration test covering full API workflow.
    """
    # Test the complete workflow from request to response
    tractor_id = "integration-test-001"
    response = client.get(f"/equipment/tractor/{tractor_id}")

    # Validate HTTP response
    assert response.status_code == 200
    assert "application/json" in response.headers["content-type"]

    # Parse and validate JSON response
    data = response.json()
    assert data["tractor_id"] == tractor_id

    # Validate that all enhanced robotic interface categories are represented
    categories = {
        "core": ["make", "model", "year"],
        "engine": ["engine_on", "engine_rpm", "engine_temp"],
        "navigation": ["waypoint_count", "current_heading", "auto_steer_enabled"],
        "implements": ["implement_position", "implement_depth", "implement_width"],
        "field_ops": ["field_mode", "work_rate", "area_covered"],
        "autonomous": ["autonomous_mode", "obstacle_detection", "emergency_stop_active"],
        "isobus": ["isobus_address", "device_name"],
        "safety": ["safety_system_active", "safety_level"],
        "sensors": ["lidar_enabled", "obstacle_count"],
        "power": ["regenerative_mode"],
    }

    for category, fields in categories.items():
        for field in fields:
            assert field in data, f"Category '{category}' field '{field}' missing from API response"

    # Validate that the response represents a complete, professional agricultural system
    assert data["make"] == "John Deere"
    assert data["model"] == "9RX"
    assert data["safety_system_active"] is True
    assert data["device_name"] == "John Deere_9RX_2023"
    assert data["obstacle_detection"] is True
