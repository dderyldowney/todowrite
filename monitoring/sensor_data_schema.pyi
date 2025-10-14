from typing import Any, Dict

class SensorDataSchema:
    COMMON_FIELDS: Dict[str, Any]
    SOIL_MOISTURE_SCHEMA: Dict[str, Any]
    AIR_TEMPERATURE_SCHEMA: Dict[str, Any]

    @staticmethod
    def get_schema(sensor_type: str) -> Dict[str, Any]: ...
