"""
Pydantic response schemas for monitoring endpoints.

These are transport-layer models used by the API to expose sensor readings
with a stable, JSON-serializable shape. They intentionally sit separate from
backend integrations and domain monitors.
"""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel


class SoilReadingResponse(BaseModel):
    """
    Soil sensor reading response payload.

    Parameters
    ----------
    sensor_id : str
        Identifier of the soil sensor.
    readings : Dict[str, Any]
        Key-value mapping of soil metrics (e.g., ph, moisture, nutrients).
        Values may be numeric or strings depending on backend representation.
    """

    sensor_id: str
    readings: dict[str, Any]


class WaterQualityResponse(BaseModel):
    """
    Water sensor reading response payload.

    Parameters
    ----------
    sensor_id : str
        Identifier of the water sensor.
    readings : Dict[str, Any]
        Key-value mapping of water metrics (e.g., ph, turbidity, temperature).
        Values may be numeric or strings depending on backend representation.
    """

    sensor_id: str
    readings: dict[str, Any]
