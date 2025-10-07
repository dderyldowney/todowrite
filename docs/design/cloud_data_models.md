# Data Models for Cloud-Integrated Agricultural Data

## Overview

This document defines the data models for agricultural data that will be exchanged and stored in cloud platforms. These models ensure consistency, facilitate data processing, and support interoperability with various agricultural applications.

## Core Data Entities

1.  **Telemetry Data Model**:
    *   **Purpose**: Represents real-time sensor readings and equipment status.
    *   **Fields**:
        *   `robot_id` (string): Unique identifier for the robotic system.
        *   `timestamp` (datetime): UTC timestamp of the data reading.
        *   `location` (GeoJSON Point): Current GPS coordinates.
        *   `sensor_readings` (object): Key-value pairs for various sensor data (e.g., `soil_moisture`, `air_temp`, `humidity`).
        *   `equipment_status` (object): Key-value pairs for equipment-specific metrics (e.g., `engine_rpm`, `fuel_level`, `implement_state`).
    *   **Example (JSON)**:
        ```json
        {
            "robot_id": "R1",
            "timestamp": "2025-10-07T12:30:00Z",
            "location": {"type": "Point", "coordinates": [-118.2437, 34.0522]},
            "sensor_readings": {"soil_moisture": 0.45, "air_temp": 22.5},
            "equipment_status": {"engine_rpm": 2000, "fuel_level": 0.75}
        }
        ```

2.  **Field Boundary Data Model**:
    *   **Purpose**: Represents the geographical boundaries of agricultural fields.
    *   **Fields**:
        *   `field_id` (string): Unique identifier for the field.
        *   `farm_id` (string): Identifier for the farm.
        *   `name` (string): Human-readable name of the field.
        *   `geometry` (GeoJSON Polygon): The geographical shape of the field.
        *   `area_acres` (float): Calculated area of the field in acres.
    *   **Example (GeoJSON)**:
        ```json
        {
            "type": "Feature",
            "geometry": {
                "type": "Polygon",
                "coordinates": [[[-118.25, 34.05], [-118.24, 34.05], [-118.24, 34.06], [-118.25, 34.06], [-118.25, 34.05]]]
            },
            "properties": {
                "field_id": "F001",
                "farm_id": "FarmA",
                "name": "North Field",
                "area_acres": 100.5
            }
        }
        ```

3.  **Command Data Model**:
    *   **Purpose**: Represents commands sent from the cloud to robotic systems.
    *   **Fields**:
        *   `command_id` (string): Unique identifier for the command.
        *   `robot_id` (string): Target robotic system.
        *   `timestamp` (datetime): UTC timestamp when the command was issued.
        *   `type` (string): Type of command (e.g., `MOVE`, `SPRAY`, `HARVEST`).
        *   `parameters` (object): Command-specific parameters (e.g., `target_location`, `application_rate`).
    *   **Example (JSON)**:
        ```json
        {
            "command_id": "CMD001",
            "robot_id": "R1",
            "timestamp": "2025-10-07T12:35:00Z",
            "type": "MOVE",
            "parameters": {"target_location": {"type": "Point", "coordinates": [-118.245, 34.055]}}
        }
        ```

## Data Validation and Schema Enforcement

*   JSON schemas will be defined and enforced to ensure data integrity and consistency.
*   Data validation will occur at ingestion points and before data persistence.
