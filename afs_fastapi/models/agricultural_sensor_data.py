"""
Agricultural sensor data models with ISOBUS integration.

This module provides data structures for agricultural sensor information
that integrates with the established ISOBUS communication infrastructure
for real-world tractor and implement data collection.

Implementation follows Test-First Development (TDD) GREEN phase.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from enum import Enum

from afs_fastapi.equipment.farm_tractors import ISOBUSMessage


class SensorType(str, Enum):
    """Agricultural sensor types for comprehensive farm monitoring."""

    # Soil monitoring sensors
    SOIL_MOISTURE = "soil_moisture"
    SOIL_TEMPERATURE = "soil_temperature"
    SOIL_PH = "soil_ph"

    # Crop monitoring sensors
    YIELD_MONITOR = "yield_monitor"
    CROP_HEIGHT = "crop_height"

    # Environmental sensors
    GPS_POSITION = "gps_position"
    WEATHER_STATION = "weather_station"

    # Equipment sensors
    FUEL_LEVEL = "fuel_level"
    ENGINE_TEMPERATURE = "engine_temperature"


@dataclass
class AgriculturalSensorData:
    """Agricultural sensor data with ISOBUS message traceability.

    Provides time-series agricultural sensor data linked to ISOBUS
    communication for multi-tractor field operations and analytics.
    """

    timestamp: datetime
    tractor_id: str
    isobus_source: ISOBUSMessage
    sensor_type: SensorType
    value: float
    unit: str
    field_coordinates: tuple[float, float]  # (latitude, longitude)

    def __post_init__(self) -> None:
        """Validate agricultural sensor data after initialization."""
        if not self.tractor_id:
            raise ValueError("Tractor ID must not be empty")

        if not isinstance(self.sensor_type, SensorType):
            raise ValueError(f"Invalid sensor type: {self.sensor_type}")

        if not self.unit:
            raise ValueError("Unit must not be empty")

        # Validate GPS coordinates
        lat, lon = self.field_coordinates
        if not (-90 <= lat <= 90):
            raise ValueError(f"Invalid latitude: {lat}")
        if not (-180 <= lon <= 180):
            raise ValueError(f"Invalid longitude: {lon}")


@dataclass
class TractorTelemetryData:
    """Tractor telemetry data for fleet coordination and monitoring.

    Captures critical tractor operational parameters from ISOBUS
    communication for safety monitoring and fleet management.
    """

    timestamp: datetime
    tractor_id: str
    isobus_source: ISOBUSMessage
    vehicle_speed: float  # km/h
    fuel_level: float  # percent (0-100)
    engine_temperature: float  # celsius
    gps_coordinates: tuple[float, float]  # (latitude, longitude)
    operational_mode: str

    def __post_init__(self) -> None:
        """Validate tractor telemetry data for safety compliance."""
        if not self.tractor_id:
            raise ValueError("Tractor ID must not be empty")

        # Safety validation for vehicle speed
        if self.vehicle_speed < 0:
            raise ValueError("Vehicle speed must be non-negative")

        # Safety validation for fuel level
        if not (0 <= self.fuel_level <= 100):
            raise ValueError("Fuel level must be between 0 and 100 percent")

        # Validate GPS coordinates
        lat, lon = self.gps_coordinates
        if not (-90 <= lat <= 90):
            raise ValueError(f"Invalid latitude: {lat}")
        if not (-180 <= lon <= 180):
            raise ValueError(f"Invalid longitude: {lon}")

        if not self.operational_mode:
            raise ValueError("Operational mode must not be empty")

    def get_safety_status(self) -> str:
        """Get safety status based on telemetry parameters.

        Returns
        -------
        str
            Safety status: "normal", "warning", or "critical"
        """
        # Critical safety conditions
        if self.fuel_level < 5.0:
            return "critical"
        if self.engine_temperature > 110.0:
            return "critical"

        # Warning conditions
        if self.fuel_level < 15.0:
            return "warning"
        if self.engine_temperature > 95.0:
            return "warning"

        return "normal"

    def is_moving(self) -> bool:
        """Check if tractor is currently moving.

        Returns
        -------
        bool
            True if vehicle speed indicates movement (>0.1 km/h)
        """
        return self.vehicle_speed > 0.1


@dataclass
class YieldMonitorData:
    """Yield monitoring data for agricultural analytics and reporting.

    Captures harvest yield information from combine harvesters with
    ISOBUS integration for comprehensive field performance analysis.
    """

    timestamp: datetime
    tractor_id: str
    isobus_source: ISOBUSMessage
    crop_type: str
    yield_volume: float  # tons per hectare
    moisture_content: float  # percent
    field_coordinates: tuple[float, float]  # (latitude, longitude)
    harvest_width: float  # meters
    harvest_speed: float  # km/h

    def __post_init__(self) -> None:
        """Validate yield monitoring data for agricultural analytics."""
        if not self.tractor_id:
            raise ValueError("Tractor ID must not be empty")

        if not self.crop_type:
            raise ValueError("Crop type must not be empty")

        if self.yield_volume < 0:
            raise ValueError("Yield volume must be non-negative")

        if not (0 <= self.moisture_content <= 100):
            raise ValueError("Moisture content must be between 0 and 100 percent")

        if self.harvest_width <= 0:
            raise ValueError("Harvest width must be positive")

        if self.harvest_speed < 0:
            raise ValueError("Harvest speed must be non-negative")

        # Validate GPS coordinates
        lat, lon = self.field_coordinates
        if not (-90 <= lat <= 90):
            raise ValueError(f"Invalid latitude: {lat}")
        if not (-180 <= lon <= 180):
            raise ValueError(f"Invalid longitude: {lon}")

    def calculate_yield_per_minute(self) -> float:
        """Calculate yield harvest rate per minute.

        Returns
        -------
        float
            Yield harvest rate in tons per minute
        """
        # Calculate area covered per minute in hectares
        area_per_minute = (
            self.harvest_width  # meters
            * (self.harvest_speed * 1000 / 60)  # meters per minute
            / 10000  # convert square meters to hectares
        )

        # Calculate yield per minute
        return self.yield_volume * area_per_minute

    def calculate_coverage_hectares_per_hour(self) -> float:
        """Calculate field coverage rate in hectares per hour.

        Returns
        -------
        float
            Field coverage rate in hectares per hour
        """
        # Calculate area covered per hour in hectares
        return (
            self.harvest_width  # meters
            * (self.harvest_speed * 1000)  # meters per hour
            / 10000  # convert square meters to hectares
        )

    def get_adjusted_yield(self, target_moisture: float = 15.0) -> float:
        """Calculate moisture-adjusted yield for standardized reporting.

        Parameters
        ----------
        target_moisture : float, default 15.0
            Target moisture content for yield adjustment

        Returns
        -------
        float
            Moisture-adjusted yield in tons per hectare
        """
        # Standard moisture adjustment formula for agricultural reporting
        moisture_factor = (100 - self.moisture_content) / (100 - target_moisture)
        return self.yield_volume * moisture_factor

    def is_harvest_quality_acceptable(self, max_moisture: float = 20.0) -> bool:
        """Check if harvest quality meets standards.

        Parameters
        ----------
        max_moisture : float, default 20.0
            Maximum acceptable moisture content

        Returns
        -------
        bool
            True if harvest quality is acceptable
        """
        return (
            self.moisture_content <= max_moisture
            and self.yield_volume > 0
            and self.harvest_speed > 0.5  # Minimum harvest speed for quality
        )
