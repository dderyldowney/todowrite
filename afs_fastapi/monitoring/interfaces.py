"""
Sensor backend interfaces and simple in-memory demo implementations.

These define the abstraction boundary between the API/domain models and
hardware or external sensor systems. Real implementations can plug in later
without changing API surfaces.
"""

from __future__ import annotations

from abc import ABC, abstractmethod


class SoilSensorBackend(ABC):
    """
    Abstract soil sensor backend.

    Implementations should communicate with hardware, gateways, or services
    to obtain current readings.
    """

    @abstractmethod
    def read(self, sensor_id: str) -> dict[str, float]:
        """Return current soil composition metrics for the given sensor."""


class WaterSensorBackend(ABC):
    """
    Abstract water sensor backend.

    Implementations should communicate with hardware, gateways, or services
    to obtain current readings.
    """

    @abstractmethod
    def read(self, sensor_id: str) -> dict[str, float]:
        """Return current water quality metrics for the given sensor."""


class DummySoilSensorBackend(SoilSensorBackend):
    """Default no-op soil backend returning neutral placeholder values."""

    def read(self, sensor_id: str) -> dict[str, float]:
        return {
            "nitrogen": 0.0,
            "phosphorus": 0.0,
            "potassium": 0.0,
            "ph": 7.0,
            "moisture": 0.0,
        }


class DummyWaterSensorBackend(WaterSensorBackend):
    """Default no-op water backend returning neutral placeholder values."""

    def read(self, sensor_id: str) -> dict[str, float]:
        return {
            "ph": 7.0,
            "dissolved_oxygen": 0.0,
            "temperature": 0.0,
            "conductivity": 0.0,
            "turbidity": 0.0,
        }
