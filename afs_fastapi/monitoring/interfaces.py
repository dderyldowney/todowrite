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
        # Use sensor_id to create slight variations for testing
        sensor_hash = hash(sensor_id) % 100
        return {
            "nitrogen": 0.0 + (sensor_hash % 10) * 0.1,
            "phosphorus": 0.0 + (sensor_hash % 5) * 0.05,
            "potassium": 0.0 + (sensor_hash % 8) * 0.08,
            "ph": 7.0 + (sensor_hash % 20 - 10) * 0.1,
            "moisture": 0.0 + (sensor_hash % 50) * 0.01,
        }


class DummyWaterSensorBackend(WaterSensorBackend):
    """Default no-op water backend returning neutral placeholder values."""

    def read(self, sensor_id: str) -> dict[str, float]:
        # Use sensor_id to create slight variations for testing
        sensor_hash = hash(sensor_id) % 100
        return {
            "ph": 7.0 + (sensor_hash % 20 - 10) * 0.05,
            "dissolved_oxygen": 8.0 + (sensor_hash % 10) * 0.1,
            "temperature": 20.0 + (sensor_hash % 15) * 0.5,
            "conductivity": 0.2 + (sensor_hash % 5) * 0.01,
            "turbidity": 1.0 + (sensor_hash % 8) * 0.1,
        }
