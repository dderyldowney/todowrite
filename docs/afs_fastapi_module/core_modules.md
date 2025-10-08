# Core Modules and Classes

This section provides an overview of the core Python modules and classes within the `afs_fastapi` package. Understanding these fundamental components is crucial for developing with and extending the AFS FastAPI Agricultural Robotics Platform.

## 1. `afs_fastapi.equipment`

This module manages the interaction with various agricultural equipment, primarily focusing on tractors and implements. It provides abstractions for equipment state, control, and error handling.

### Key Classes:

*   **`FarmTractor`**: Represents a single agricultural tractor. It encapsulates properties like ID, model, manufacturer, serial number, current state (ON, OFF, MOVING), speed, fuel level, and error logs.
    *   **Methods**: `turn_on()`, `turn_off()`, `start_movement(speed)`, `stop_movement()`, `refuel(amount)`, `add_error(error)`, `clear_errors()`.
*   **`TractorState` (Enum)**: Defines the possible operational states of a tractor (e.g., `OFF`, `ON`, `MOVING`).
*   **`TractorError`**: A custom exception class for handling tractor-specific errors, including error codes and messages.

### Agricultural Context:

This module is central to controlling and monitoring the physical assets of an agricultural robotics fleet. It directly supports tasks such as autonomous plowing, planting, and harvesting by providing a programmatic interface to tractor operations. Its design considers the need for robust error reporting and state management in safety-critical field operations.

## 2. `afs_fastapi.monitoring`

The `monitoring` module is responsible for collecting, processing, and providing access to sensor data and system health information from agricultural equipment. It supports real-time data streams and historical data analysis.

### Key Classes:

*   **`SensorData`**: A data model for various sensor readings (e.g., GPS coordinates, soil moisture, temperature, fuel consumption).
*   **`MonitoringService`**: Manages the collection and aggregation of sensor data from multiple sources. Provides methods for querying current and historical data.

### Agricultural Context:

Accurate and timely monitoring is vital for precision agriculture. This module enables features like yield mapping, soil analysis, and predictive maintenance for agricultural machinery. It helps optimize resource usage (water, fertilizer) and ensures the efficient operation of robotic systems in the field.

## 3. `afs_fastapi.api`

This module defines the FastAPI endpoints that expose the platform's functionalities to external systems and user interfaces. It provides a RESTful interface for controlling equipment, retrieving monitoring data, and managing fleet operations.

### 3.1. API Endpoints

Here's a detailed reference of the available API endpoints:

*   **`GET /`**
    *   **Summary**: Welcome message
    *   **Description**: Root endpoint returning a welcome message.
    *   **Response Model**: `dict[str, str]` (e.g., `{"message": "Welcome to the Agricultural Farm System API"}`)

*   **`GET /health`**
    *   **Summary**: Health check
    *   **Description**: Health check endpoint.
    *   **Response Model**: `dict[str, str]` (e.g., `{"status": "healthy"}`)

*   **`GET /version`**
    *   **Summary**: API version
    *   **Description**: Version information endpoint.
    *   **Response Model**: `dict[str, str]` (e.g., `{"version": "1.0.0"}`)

*   **`GET /equipment/tractor/{tractor_id}`**
    *   **Summary**: Get tractor status
    *   **Description**: Get status of a specific tractor.
    *   **Path Parameters**: `tractor_id` (string)
    *   **Response Model**: `FarmTractorResponse`

*   **`GET /monitoring/soil/{sensor_id}`**
    *   **Summary**: Get soil readings
    *   **Description**: Get soil monitoring data from a specific sensor.
    *   **Path Parameters**: `sensor_id` (string)
    *   **Response Model**: `SoilReadingResponse`

*   **`GET /monitoring/water/{sensor_id}`**
    *   **Summary**: Get water readings
    *   **Description**: Get water quality data from a specific sensor.
    *   **Path Parameters**: `sensor_id` (string)
    *   **Response Model**: `WaterQualityResponse`

*   **`POST /ai/process`**
    *   **Summary**: Process text with AI optimization
    *   **Description**: Process text input with AI optimization pipeline. Applies sophisticated token optimization while preserving agricultural safety compliance and technical accuracy.
    *   **Request Body**: `AIProcessingRequest`
    *   **Response Model**: `AIProcessingResponse`

*   **`POST /ai/equipment/optimize`**
    *   **Summary**: Optimize equipment communication
    *   **Description**: Optimize equipment communication messages for ISOBUS and safety protocols. Uses conservative optimization to ensure safety-critical equipment communication remains accurate and compliant.
    *   **Request Body**: `EquipmentOptimizationRequest`
    *   **Response Model**: `AIProcessingResponse`

*   **`POST /ai/monitoring/optimize`**
    *   **Summary**: Optimize monitoring data
    *   **Description**: Optimize monitoring data processing for sensor readings and analysis. Uses standard optimization for soil quality, water monitoring, and environmental sensor data.
    *   **Request Body**: `MonitoringOptimizationRequest`
    *   **Response Model**: `AIProcessingResponse`

*   **`POST /ai/fleet/optimize`**
    *   **Summary**: Optimize fleet coordination
    *   **Description**: Optimize fleet coordination messages and multi-tractor commands. Uses aggressive optimization for routine fleet coordination.
    *   **Request Body**: `FleetOptimizationRequest`
    *   **Response Model**: `AIProcessingResponse`

*   **`GET /ai/statistics`**
    *   **Summary**: Get AI processing statistics
    *   **Description**: Get comprehensive AI processing pipeline statistics.
    *   **Response Model**: `PlatformStatisticsResponse`

*   **`GET /ai/health`**
    *   **Summary**: AI processing health check
    *   **Description**: Perform comprehensive AI processing pipeline health check.
    *   **Response Model**: `HealthCheckResponse`

### 3.2. Pydantic Models (from `ai_processing_schemas.py`)

This section details the Pydantic models used for request and response validation in the API.

*   **`OptimizationLevelEnum`**
    *   **Description**: AI processing optimization intensity levels.
    *   **Values**: `CONSERVATIVE`, `STANDARD`, `AGGRESSIVE`, `ADAPTIVE`

*   **`TargetFormatEnum`**
    *   **Description**: Target output format for AI processing.
    *   **Values**: `STANDARD`, `BRIEF`, `BULLET_POINTS`

*   **`AIProcessingRequest`**
    *   **Description**: Request model for AI processing pipeline operations.
    *   **Fields**:
        *   `user_input` (str): Input text to process (required, min_length=1, max_length=10000).
        *   `service_name` (str | None): Calling service name for tracking and configuration (default: "platform").
        *   `optimization_level` (OptimizationLevelEnum | None): Optimization intensity (defaults to service configuration).
        *   `target_format` (TargetFormatEnum | None): Desired output format (default: `STANDARD`).
        *   `token_budget` (int | None): Maximum token budget for processing (ge=100, le=8000).
        *   `context_data` (dict[str, Any] | None): Additional context for agricultural operations.

*   **`AIProcessingResponse`**
    *   **Description**: Response model for AI processing pipeline operations.
    *   **Fields**:
        *   `final_output` (str): Optimized output text.
        *   `total_tokens_saved` (int): Total tokens saved through optimization (ge=0).
        *   `stages_completed` (int): Number of pipeline stages completed (ge=0, le=4).
        *   `agricultural_compliance_maintained` (bool): Whether agricultural safety compliance was preserved.
        *   `optimization_level` (OptimizationLevelEnum): Applied optimization level.
        *   `optimization_applied` (bool): Whether optimization was successfully applied.
        *   `estimated_tokens` (int): Estimated token count of final output (ge=0).
        *   `budget_exceeded` (bool): Whether token budget was exceeded.
        *   `fallback_used` (bool): Whether fallback processing was used.
        *   `metrics` (dict[str, Any]): Detailed processing metrics.

*   **`EquipmentOptimizationRequest`**
    *   **Description**: Request model for equipment communication optimization.
    *   **Fields**:
        *   `message` (str): Equipment communication message (required, min_length=1, max_length=5000).
        *   `equipment_id` (str | None): Equipment identifier for tracking.
        *   `priority` (str | None): Message priority level (default: "high").

*   **`MonitoringOptimizationRequest`**
    *   **Description**: Request model for monitoring data optimization.
    *   **Fields**:
        *   `sensor_data` (str): Sensor reading or monitoring data (required, min_length=1, max_length=5000).
        *   `sensor_id` (str | None): Sensor identifier for tracking.
        *   `data_type` (str | None): Type of monitoring data (default: "general").

*   **`FleetOptimizationRequest`**
    *   **Description**: Request model for fleet coordination optimization.
    *   **Fields**:
        *   `coordination_message` (str): Fleet coordination message or command (required, min_length=1, max_length=5000).
        *   `fleet_operation` (str | None): Type of fleet operation (default: "coordination").
        *   `tractor_count` (int | None): Number of tractors involved (ge=1, le=20).

*   **`PlatformStatisticsResponse`**
    *   **Description**: Response model for platform AI processing statistics.
    *   **Fields**:
        *   `global_stats` (dict[str, Any]): Global processing statistics.
        *   `service_stats` (dict[str, Any]): Per-service processing statistics.
        *   `configuration` (dict[str, Any]): Current platform configuration.
        *   `pipeline_health` (dict[str, Any]): Pipeline health indicators.

*   **`HealthCheckResponse`**
    *   **Description**: Response model for AI processing health check.
    *   **Fields**:
        *   `status` (str): Overall health status.
        *   `pipeline_operational` (bool): Whether AI processing pipeline is operational.
        *   `services_registered` (int): Number of registered services (ge=0).
        *   `total_requests_processed` (int): Total requests processed since startup (ge=0).
        *   `test_processing_success` (bool): Whether test processing succeeded.
        *   `agricultural_safety_mode` (bool): Whether agricultural safety mode is enabled.
        *   `error` (str | None): Error message if unhealthy.

### 3.3. Code Examples

#### Example 1: Get Tractor Status

This example demonstrates how to retrieve the status of a specific tractor using the `GET /equipment/tractor/{tractor_id}` endpoint.

```python
import requests

BASE_URL = "http://localhost:8000"  # Replace with your API base URL

def get_tractor_status(tractor_id: str):
    response = requests.get(f"{BASE_URL}/equipment/tractor/{tractor_id}")
    response.raise_for_status()  # Raise an exception for HTTP errors
    return response.json()

if __name__ == "__main__":
    tractor_id = "tractor-1"
    status = get_tractor_status(tractor_id)
    print(f"Status for {tractor_id}:")
    print(status)
```

#### Example 2: Get Soil Readings

This example demonstrates how to retrieve soil monitoring data from a specific sensor using the `GET /monitoring/soil/{sensor_id}` endpoint.

```python
import requests

BASE_URL = "http://localhost:8000"  # Replace with your API base URL

def get_soil_readings(sensor_id: str):
    response = requests.get(f"{BASE_URL}/monitoring/soil/{sensor_id}")
    response.raise_for_status()
    return response.json()

if __name__ == "__main__":
    sensor_id = "soil-sensor-1"
    readings = get_soil_readings(sensor_id)
    print(f"Soil readings for {sensor_id}:")
    print(readings)
```

#### Example 3: Process Text with AI Optimization

This example demonstrates how to send text for AI optimization using the `POST /ai/process` endpoint.

```python
import requests
import json

BASE_URL = "http://localhost:8000"  # Replace with your API base URL

def process_text_with_ai(user_input: str, optimization_level: str = "standard"):
    headers = {"Content-Type": "application/json"}
    payload = {
        "user_input": user_input,
        "optimization_level": optimization_level,
        "service_name": "platform"
    }
    response = requests.post(f"{BASE_URL}/ai/process", headers=headers, data=json.dumps(payload))
    response.raise_for_status()
    return response.json()

if __name__ == "__main__":
    text_to_optimize = "Coordinate the three tractors for simultaneous planting in field sector Alpha."
    optimized_output = process_text_with_ai(text_to_optimize, "aggressive")
    print("Optimized Output:")
    print(optimized_output)
```

---

## 4. Other Key Modules*   **`afs_fastapi.core`**: Contains foundational utilities, configuration management, and common data models used across the application.
*   **`afs_fastapi.services`**: Implements the business logic and orchestrates interactions between different modules (e.g., `FleetCoordinationService` for multi-tractor operations).
*   **`afs_fastapi.config`**: Handles application-wide configuration settings.
