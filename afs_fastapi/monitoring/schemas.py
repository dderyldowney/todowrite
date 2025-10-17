"""
Pydantic response schemas for monitoring endpoints.

These are transport-layer models used by the API to expose sensor readings
with a stable, JSON-serializable shape. They intentionally sit separate from
backend integrations and domain monitors.

Agricultural Context:
Defines data structures for real-time agricultural monitoring including
soil quality, water management, and environmental sensor data for precision
farming operations and autonomous equipment guidance.
"""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field


class SoilReadingResponse(BaseModel):
    """
    Soil sensor reading response payload for precision agriculture monitoring.

    Provides real-time soil condition data for agricultural equipment navigation,
    crop management decisions, and field optimization strategies.
    """

    sensor_id: str = Field(
        ...,
        description="Unique identifier of the soil sensor in the field monitoring network",
        examples=["SOIL_001", "FIELD_A_SECTOR_2_SOIL"],
    )

    readings: dict[str, Any] = Field(
        ...,
        description="Soil metrics including pH, moisture, nutrient levels, and temperature",
        examples=[
            {
                "ph": 6.8,
                "moisture_percent": 34.2,
                "nitrogen_ppm": 120,
                "phosphorus_ppm": 45,
                "potassium_ppm": 180,
                "temperature_celsius": 22.1,
                "electrical_conductivity": 2.4,
                "organic_matter_percent": 3.8,
            }
        ],
    )


class WaterQualityResponse(BaseModel):
    """
    Water sensor reading response payload for irrigation and drainage management.

    Provides water quality measurements for irrigation systems, drainage monitoring,
    and environmental compliance in agricultural operations.
    """

    sensor_id: str = Field(
        ...,
        description="Unique identifier of the water quality sensor",
        examples=["WATER_001", "IRRIGATION_MAIN_01", "DRAINAGE_WEST_02"],
    )

    readings: dict[str, Any] = Field(
        ...,
        description="Water quality metrics including pH, turbidity, temperature, and chemical levels",
        examples=[
            {
                "ph": 7.2,
                "turbidity_ntu": 12.5,
                "temperature_celsius": 18.7,
                "dissolved_oxygen_ppm": 8.4,
                "nitrate_ppm": 5.2,
                "phosphate_ppm": 0.8,
                "electrical_conductivity": 680,
                "total_dissolved_solids": 340,
            }
        ],
    )
