from typing import Any

class SensorDataSchema:
    COMMON_FIELDS: dict[str, Any]
    SOIL_MOISTURE_SCHEMA: dict[str, Any]
    AIR_TEMPERATURE_SCHEMA: dict[str, Any]

    @staticmethod
    def get_schema(sensor_type: str) -> dict[str, Any]: ...
