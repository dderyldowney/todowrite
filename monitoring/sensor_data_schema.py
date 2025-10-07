class SensorDataSchema:
    """
    Conceptual standard data formats for agricultural sensor readings.
    This schema aims to provide a flexible structure for various sensor types,
    ensuring interoperability and efficient processing.
    """

    # Common fields for all sensor readings
    COMMON_FIELDS = {
        "timestamp": {
            "type": "string",
            "format": "date-time",
            "description": "ISO 8601 formatted timestamp of the sensor reading.",
        },
        "device_id": {"type": "string", "description": "Unique identifier for the sensor device."},
        "sensor_type": {
            "type": "string",
            "description": "Type of sensor (e.g., 'soil_moisture', 'air_temperature', 'pH').",
        },
        "value": {"type": "number", "description": "The measured value from the sensor."},
        "unit": {
            "type": "string",
            "description": "Unit of measurement for the sensor value (e.g., '%', '°C', 'pH').",
        },
    }

    # Example schema for a soil moisture sensor
    SOIL_MOISTURE_SCHEMA = {
        **COMMON_FIELDS,
        "metadata": {
            "type": "object",
            "properties": {
                "location": {
                    "type": "object",
                    "properties": {"latitude": {"type": "number"}, "longitude": {"type": "number"}},
                    "required": ["latitude", "longitude"],
                },
                "depth_cm": {
                    "type": "number",
                    "description": "Depth at which moisture was measured in cm.",
                },
            },
            "required": ["location"],
        },
    }

    # Example schema for an air temperature sensor
    AIR_TEMPERATURE_SCHEMA = {
        **COMMON_FIELDS,
        "metadata": {
            "type": "object",
            "properties": {
                "location": {
                    "type": "object",
                    "properties": {"latitude": {"type": "number"}, "longitude": {"type": "number"}},
                    "required": ["latitude", "longitude"],
                },
                "elevation_m": {
                    "type": "number",
                    "description": "Elevation above sea level in meters.",
                },
            },
            "required": ["location"],
        },
    }

    # You can add more sensor-specific schemas here

    @staticmethod
    def get_schema(sensor_type: str) -> dict:
        """
        Returns the schema for a given sensor type.
        """
        if sensor_type == "soil_moisture":
            return SensorDataSchema.SOIL_MOISTURE_SCHEMA
        elif sensor_type == "air_temperature":
            return SensorDataSchema.AIR_TEMPERATURE_SCHEMA
        else:
            # Default to common fields if no specific schema is defined
            return SensorDataSchema.COMMON_FIELDS


# Example Usage:
if __name__ == "__main__":
    soil_moisture_data = {
        "timestamp": "2025-10-07T10:00:00Z",
        "device_id": "SM-001",
        "sensor_type": "soil_moisture",
        "value": 0.45,
        "unit": "%",
        "metadata": {"location": {"latitude": 34.0522, "longitude": -118.2437}, "depth_cm": 15},
    }

    air_temperature_data = {
        "timestamp": "2025-10-07T10:00:00Z",
        "device_id": "AT-002",
        "sensor_type": "air_temperature",
        "value": 25.5,
        "unit": "°C",
        "metadata": {"location": {"latitude": 34.0522, "longitude": -118.2437}, "elevation_m": 100},
    }

    print("Soil Moisture Schema:")
    print(SensorDataSchema.get_schema("soil_moisture"))
    print("\nAir Temperature Schema:")
    print(SensorDataSchema.get_schema("air_temperature"))

    print("\nExample Soil Moisture Data:")
    print(soil_moisture_data)
    print("\nExample Air Temperature Data:")
    print(air_temperature_data)
