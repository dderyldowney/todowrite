"""Soil Moisture Monitoring for Agricultural Equipment.

REFACTOR PHASE: Enhanced implementation with improved code quality.
This module provides soil moisture monitoring capabilities for precision agriculture
and multi-tractor coordination scenarios.
"""

from __future__ import annotations

import time
from dataclasses import dataclass

# Agricultural moisture monitoring constants
MOISTURE_MIN_VALID = 0.0
MOISTURE_MAX_VALID = 100.0
CRITICAL_DRY_THRESHOLD = 5.0
MILLISECOND_CONVERSION = 1000


@dataclass
class MoistureReading:
    """Soil moisture reading with validation status.

    Agricultural Context: Represents a single soil moisture measurement
    from field sensors used in precision agriculture irrigation systems.
    """

    moisture_percentage: float
    is_valid: bool
    status: str
    requires_immediate_irrigation: bool = False
    processing_time_ms: float = 0.0


@dataclass
class MoistureAlert:
    """Agricultural alert for critical moisture conditions.

    Agricultural Context: Alerts generated for multi-tractor coordination
    when soil moisture requires immediate irrigation intervention.
    """

    alert_type: str
    field_section: str
    requires_immediate_action: bool
    recommended_action: str


class SoilMoistureMonitor:
    """Soil moisture monitoring component for agricultural equipment.

    REFACTOR PHASE: Enhanced implementation with improved constants and typing.
    Provides soil moisture validation and alert generation for precision
    agriculture and multi-tractor field coordination.
    """

    def __init__(self, sensor_id: str, field_section: str) -> None:
        """Initialize soil moisture monitor for agricultural equipment.

        Args:
            sensor_id: Unique identifier for the soil moisture sensor
            field_section: Field section identifier for multi-tractor coordination

        """
        self.sensor_id = sensor_id
        self.field_section = field_section
        self._alerts: list[MoistureAlert] = []

    def process_reading(self, moisture_value: float) -> MoistureReading:
        """Process soil moisture sensor reading with agricultural validation.

        Args:
            moisture_value: Raw moisture percentage from sensor (0-100%)

        Returns:
            MoistureReading with validation status and agricultural context

        """
        start_time = time.time()

        # Validate moisture reading range
        if moisture_value < MOISTURE_MIN_VALID or moisture_value > MOISTURE_MAX_VALID:
            processing_time = (time.time() - start_time) * MILLISECOND_CONVERSION
            return MoistureReading(
                moisture_percentage=moisture_value,
                is_valid=False,
                status="sensor_error",
                processing_time_ms=processing_time,
            )

        # Check for critical dry conditions requiring irrigation
        if moisture_value <= CRITICAL_DRY_THRESHOLD:
            processing_time = (time.time() - start_time) * MILLISECOND_CONVERSION
            # Generate alert for critical moisture condition
            alert = MoistureAlert(
                alert_type="critical_moisture",
                field_section=self.field_section,
                requires_immediate_action=True,
                recommended_action="Immediate irrigation required",
            )
            self._alerts.append(alert)

            return MoistureReading(
                moisture_percentage=moisture_value,
                is_valid=True,
                status="critical_dry",
                requires_immediate_irrigation=True,
                processing_time_ms=processing_time,
            )

        # Normal moisture reading
        processing_time = (time.time() - start_time) * MILLISECOND_CONVERSION
        return MoistureReading(
            moisture_percentage=moisture_value,
            is_valid=True,
            status="normal",
            processing_time_ms=processing_time,
        )

    def get_generated_alerts(self) -> list[MoistureAlert]:
        """Get list of generated agricultural alerts.

        Returns:
            List of moisture alerts for multi-tractor coordination

        """
        return self._alerts.copy()
