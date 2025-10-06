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

### Key Components:

*   **FastAPI Routers**: Organize API endpoints into logical groups (e.g., `/equipment`, `/monitoring`, `/fleet`).
*   **Pydantic Models**: Used for request and response validation, ensuring data integrity and clear API contracts.
*   **Dependency Injection**: Manages dependencies for API endpoints, such as database connections or service instances.

### Agricultural Context:

The API layer is the gateway for integrating the AFS FastAPI platform with farm management software, mobile applications for field operators, and other robotic control systems. It allows for remote control of tractors, real-time visualization of field data, and automated task assignment, all critical for modern agricultural operations.

## 4. Other Key Modules

*   **`afs_fastapi.core`**: Contains foundational utilities, configuration management, and common data models used across the application.
*   **`afs_fastapi.services`**: Implements the business logic and orchestrates interactions between different modules (e.g., `FleetCoordinationService` for multi-tractor operations).
*   **`afs_fastapi.config`**: Handles application-wide configuration settings.
