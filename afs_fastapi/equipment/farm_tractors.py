from datetime import datetime
from enum import Enum
from typing import ClassVar, Dict, List, Literal, Optional, Tuple

from pydantic import BaseModel


class ImplementPosition(str, Enum):
    """Implement position states."""

    RAISED = "raised"
    LOWERED = "lowered"
    TRANSPORT = "transport"


class FieldMode(str, Enum):
    """Field operation modes."""

    TRANSPORT = "transport"
    TILLAGE = "tillage"
    PLANTING = "planting"
    SPRAYING = "spraying"
    HARVESTING = "harvesting"
    MAINTENANCE = "maintenance"


class FarmTractorResponse(BaseModel):
    """
    Representation of a tractor state suitable for API responses.

    Parameters
    ----------
    make : str
        Manufacturer name.
    model : str
        Model name.
    year : int
        Year of manufacture.
    manual_url : str | None, optional
        URL to the operator's manual, by default None.
    engine_on : bool
        Whether the engine is currently running.
    speed : int
        Current speed in mph.
    gear : int
        Current gear (0–10).
    power_takeoff : bool
        Whether the PTO is engaged.
    hydraulics : bool
        Whether hydraulics are activated.
    gps_latitude : float | None
        Current GPS latitude coordinate.
    gps_longitude : float | None
        Current GPS longitude coordinate.
    auto_steer_enabled : bool
        Whether auto-steer is active.
    implement_position : str
        Current implement position (raised/lowered/transport).
    field_mode : str
        Current field operation mode.
    """

    tractor_id: str | None = None
    make: str
    model: str
    year: int
    manual_url: str | None = None
    engine_on: bool
    speed: int
    gear: int
    power_takeoff: bool
    hydraulics: bool
    gps_latitude: float | None = None
    gps_longitude: float | None = None
    auto_steer_enabled: bool = False
    implement_position: Literal["raised", "lowered", "transport"] = "raised"
    field_mode: Literal[
        "transport", "tillage", "planting", "spraying", "harvesting", "maintenance"
    ] = "transport"
    fuel_level: float = 100.0
    engine_rpm: int = 0
    hydraulic_pressure: float = 0.0
    status: str


class FarmTractor:
    """
    A class representing a farm tractor with various functionalities,
    such as engine control, gear changes, and hydraulic systems.
    """

    MAX_SPEED: ClassVar[int] = 40  # Maximum speed limit for the tractor.
    MIN_GEAR: ClassVar[int] = 0  # Minimum gear value (e.g., reverse support can be added here).
    MAX_GEAR: ClassVar[int] = 10  # Maximum gear value.

    def __init__(self, make: str, model: str, year: int, manual_url: str | None = None) -> None:
        """
        Initializes a FarmTractor instance.

        Args:
            make (str): The manufacturer of the tractor.
            model (str): The model of the tractor.
            year (int): The manufacturing year of the tractor.
            manual_url (str | None): Optional URL for accessing the tractor's manual.
        """
        self.make: str = make
        self.model: str = model
        self.year: int = year
        self.manual_url: str | None = manual_url
        self.engine_on: bool = False
        self.speed: int = 0
        self.gear: int = 0
        self.power_takeoff: bool = False
        self.hydraulics: bool = False

        # GPS and Navigation
        self.gps_latitude: float | None = None
        self.gps_longitude: float | None = None
        self.auto_steer_enabled: bool = False
        self.waypoints: List[Tuple[float, float]] = []
        self.current_heading: float = 0.0  # degrees

        # Implement Controls
        self.implement_position: ImplementPosition = ImplementPosition.RAISED
        self.implement_depth: float = 0.0  # inches
        self.implement_width: float = 0.0  # feet

        # Field Operations
        self.field_mode: FieldMode = FieldMode.TRANSPORT
        self.work_rate: float = 0.0  # acres/hour
        self.area_covered: float = 0.0  # acres

        # Engine and Fuel
        self.fuel_level: float = 100.0  # percentage
        self.engine_rpm: int = 0
        self.engine_temp: float = 180.0  # fahrenheit

        # Hydraulics
        self.hydraulic_pressure: float = 0.0  # psi
        self.hydraulic_flow: float = 0.0  # gpm

        # Sensors
        self.wheel_slip: float = 0.0  # percentage
        self.ground_speed: float = 0.0  # mph
        self.draft_load: float = 0.0  # lbs

        # Autonomous Features
        self.autonomous_mode: bool = False
        self.obstacle_detection: bool = True
        self.emergency_stop_active: bool = False

    def start_engine(self) -> str:
        if self.engine_on:
            raise ValueError("Engine is already running.")
        self.engine_on = True
        return "Engine started."

    def stop_engine(self) -> str:
        if not self.engine_on:
            raise ValueError("Engine is already off.")
        self.engine_on = False
        self.speed = 0  # Reset speed when engine is stopped.
        self.gear = 0  # Return to neutral gear.
        self.power_takeoff = False  # Disengage PTO.
        self.hydraulics = False  # Deactivate hydraulics.
        return "Engine stopped. Tractor is now reset."

    def change_gear(self, gear: int | str) -> str:
        """
        Change the tractor's gear.
        Args:
            gear: The gear to change to (int or string)
        Returns:
            str: Status message
        Raises:
            ValueError: If engine is off or invalid gear
        """
        if not self.engine_on:
            raise ValueError("Cannot change gears while the engine is off.")

        # Convert gear to int if it's a string
        try:
            gear = int(gear)
        except ValueError:
            raise ValueError("Invalid gear value")

        if not 0 <= gear <= 10:
            raise ValueError("Gear must be between 0 and 10.")

        self.gear = gear
        return f"Gear changed to {gear}."

    def accelerate(self, increase: int) -> str:
        if not self.engine_on:
            raise ValueError("Cannot accelerate while the engine is off.")
        if increase < 0:
            raise ValueError("Acceleration must be a positive value.")
        self.speed = min(self.speed + increase, self.MAX_SPEED)  # Limit speed to MAX_SPEED.
        return f"Speed increased to {self.speed} mph."

    def brake(self, decrease: int) -> str:
        if not self.engine_on:
            raise ValueError("Cannot brake while the engine is off.")
        if decrease < 0:
            raise ValueError("Brake reduction must be a positive value.")
        self.speed = max(0, self.speed - decrease)  # Ensure speed is not negative.
        return f"Speed decreased to {self.speed} mph."

    def engage_power_takeoff(self) -> str:
        if not self.engine_on:
            raise ValueError("Cannot engage PTO while the engine is off.")
        if self.power_takeoff:
            raise ValueError("PTO is already engaged.")
        self.power_takeoff = True
        return "Power Take-Off (PTO) engaged."

    def disengage_power_takeoff(self) -> str:
        if not self.power_takeoff:
            raise ValueError("PTO is already disengaged.")
        self.power_takeoff = False
        return "Power Take-Off (PTO) disengaged."

    def activate_hydraulics(self) -> str:
        if not self.engine_on:
            raise ValueError("Cannot activate hydraulics while the engine is off.")
        if self.hydraulics:
            raise ValueError("Hydraulics are already activated.")
        self.hydraulics = True
        return "Hydraulics activated."

    def deactivate_hydraulics(self) -> str:
        if not self.hydraulics:
            raise ValueError("Hydraulics are already deactivated.")
        self.hydraulics = False
        return "Hydraulics deactivated."

    # GPS and Navigation Controls
    def set_gps_position(self, latitude: float, longitude: float) -> str:
        """Set current GPS coordinates."""
        if not (-90 <= latitude <= 90):
            raise ValueError("Latitude must be between -90 and 90 degrees")
        if not (-180 <= longitude <= 180):
            raise ValueError("Longitude must be between -180 and 180 degrees")

        self.gps_latitude = latitude
        self.gps_longitude = longitude
        return f"GPS position set to {latitude:.6f}, {longitude:.6f}"

    def enable_auto_steer(self) -> str:
        """Enable GPS auto-steer system."""
        if not self.engine_on:
            raise ValueError("Cannot enable auto-steer while engine is off")
        if self.gps_latitude is None or self.gps_longitude is None:
            raise ValueError("GPS position must be set before enabling auto-steer")
        if self.auto_steer_enabled:
            raise ValueError("Auto-steer is already enabled")

        self.auto_steer_enabled = True
        return "Auto-steer enabled"

    def disable_auto_steer(self) -> str:
        """Disable GPS auto-steer system."""
        if not self.auto_steer_enabled:
            raise ValueError("Auto-steer is already disabled")

        self.auto_steer_enabled = False
        return "Auto-steer disabled"

    def add_waypoint(self, latitude: float, longitude: float) -> str:
        """Add a waypoint to the navigation route."""
        if not (-90 <= latitude <= 90):
            raise ValueError("Latitude must be between -90 and 90 degrees")
        if not (-180 <= longitude <= 180):
            raise ValueError("Longitude must be between -180 and 180 degrees")

        self.waypoints.append((latitude, longitude))
        return f"Waypoint added: {latitude:.6f}, {longitude:.6f}. Total waypoints: {len(self.waypoints)}"

    def clear_waypoints(self) -> str:
        """Clear all navigation waypoints."""
        waypoint_count = len(self.waypoints)
        self.waypoints.clear()
        return f"Cleared {waypoint_count} waypoints"

    def set_heading(self, heading: float) -> str:
        """Set current heading in degrees (0-359)."""
        if not (0 <= heading < 360):
            raise ValueError("Heading must be between 0 and 359 degrees")

        self.current_heading = heading
        return f"Heading set to {heading:.1f} degrees"

    # Implement Controls
    def raise_implement(self) -> str:
        """Raise the attached implement."""
        if not self.engine_on:
            raise ValueError("Cannot raise implement while engine is off")
        if self.implement_position == ImplementPosition.RAISED:
            raise ValueError("Implement is already raised")

        self.implement_position = ImplementPosition.RAISED
        self.implement_depth = 0.0
        return "Implement raised"

    def lower_implement(self, depth: float = 6.0) -> str:
        """Lower the implement to working position."""
        if not self.engine_on:
            raise ValueError("Cannot lower implement while engine is off")
        if not self.hydraulics:
            raise ValueError("Hydraulics must be activated to lower implement")
        if depth < 0 or depth > 24:
            raise ValueError("Implement depth must be between 0 and 24 inches")

        self.implement_position = ImplementPosition.LOWERED
        self.implement_depth = depth
        return f"Implement lowered to {depth:.1f} inch depth"

    def set_transport_position(self) -> str:
        """Set implement to transport position."""
        if not self.engine_on:
            raise ValueError("Cannot change implement position while engine is off")

        self.implement_position = ImplementPosition.TRANSPORT
        self.implement_depth = 0.0
        return "Implement set to transport position"

    def set_implement_width(self, width: float) -> str:
        """Set the working width of the implement."""
        if width < 0 or width > 80:
            raise ValueError("Implement width must be between 0 and 80 feet")

        self.implement_width = width
        return f"Implement width set to {width:.1f} feet"

    # Field Operation Controls
    def set_field_mode(self, mode: FieldMode) -> str:
        """Set the current field operation mode."""
        if not self.engine_on:
            raise ValueError("Cannot change field mode while engine is off")

        self.field_mode = mode
        return f"Field mode set to {mode.value}"

    def start_field_work(self) -> str:
        """Begin field work operations."""
        if not self.engine_on:
            raise ValueError("Engine must be running to start field work")
        if self.field_mode == FieldMode.TRANSPORT:
            raise ValueError("Must set field mode before starting work")
        if self.implement_position != ImplementPosition.LOWERED:
            raise ValueError("Implement must be lowered to start field work")

        self.area_covered = 0.0
        self.work_rate = self.speed * self.implement_width / 8.25  # rough calculation
        return f"Field work started in {self.field_mode.value} mode"

    def update_work_progress(self, distance: float) -> str:
        """Update work progress based on distance covered."""
        if distance < 0:
            raise ValueError("Distance must be positive")

        if self.implement_width > 0:
            area_increment = (distance * self.implement_width) / 43560  # convert to acres
            self.area_covered += area_increment

        return f"Work progress updated. Total area covered: {self.area_covered:.2f} acres"

    # Autonomous Operation Controls
    def enable_autonomous_mode(self) -> str:
        """Enable autonomous operation mode."""
        if not self.engine_on:
            raise ValueError("Engine must be running for autonomous mode")
        if not self.auto_steer_enabled:
            raise ValueError("Auto-steer must be enabled for autonomous mode")
        if len(self.waypoints) == 0:
            raise ValueError("Waypoints must be set for autonomous mode")
        if self.autonomous_mode:
            raise ValueError("Autonomous mode is already enabled")

        self.autonomous_mode = True
        return "Autonomous mode enabled"

    def disable_autonomous_mode(self) -> str:
        """Disable autonomous operation mode."""
        if not self.autonomous_mode:
            raise ValueError("Autonomous mode is already disabled")

        self.autonomous_mode = False
        return "Autonomous mode disabled"

    def emergency_stop(self) -> str:
        """Trigger emergency stop - halt all operations."""
        self.emergency_stop_active = True
        self.speed = 0
        self.autonomous_mode = False
        self.auto_steer_enabled = False
        if self.implement_position == ImplementPosition.LOWERED:
            self.implement_position = ImplementPosition.RAISED
        return "EMERGENCY STOP ACTIVATED - All operations halted"

    def reset_emergency_stop(self) -> str:
        """Reset emergency stop condition."""
        if not self.emergency_stop_active:
            raise ValueError("Emergency stop is not active")

        self.emergency_stop_active = False
        return "Emergency stop reset - Manual control restored"

    # Sensor Reading Methods
    def get_engine_diagnostics(self) -> Dict[str, float]:
        """Get current engine diagnostic readings."""
        if self.engine_on:
            self.engine_rpm = 1800 + (self.speed * 25)  # simulate RPM based on speed
            self.engine_temp = min(220, 180 + (self.engine_rpm / 100))  # simulate temp
        else:
            self.engine_rpm = 0

        return {
            "rpm": self.engine_rpm,
            "temperature": self.engine_temp,
            "fuel_level": self.fuel_level,
            "oil_pressure": 45.0 if self.engine_on else 0.0,
        }

    def get_hydraulic_status(self) -> Dict[str, float]:
        """Get current hydraulic system status."""
        if self.hydraulics and self.engine_on:
            self.hydraulic_pressure = 2500.0
            self.hydraulic_flow = 25.0
        else:
            self.hydraulic_pressure = 0.0
            self.hydraulic_flow = 0.0

        return {
            "pressure": self.hydraulic_pressure,
            "flow_rate": self.hydraulic_flow,
            "temperature": 140.0 if self.hydraulics else 80.0,
        }

    def get_ground_conditions(self) -> Dict[str, float]:
        """Get current ground and traction conditions."""
        # Simulate realistic values based on current state
        if self.engine_on and self.speed > 0:
            self.wheel_slip = min(15.0, self.speed * 0.3)  # More slip at higher speeds
            self.ground_speed = self.speed * (1 - self.wheel_slip / 100)
            self.draft_load = (
                self.implement_depth * 500
                if self.implement_position == ImplementPosition.LOWERED
                else 0
            )
        else:
            self.wheel_slip = 0.0
            self.ground_speed = 0.0
            self.draft_load = 0.0

        return {
            "wheel_slip": self.wheel_slip,
            "ground_speed": self.ground_speed,
            "draft_load": self.draft_load,
            "soil_compaction": 2.5 if self.implement_position == ImplementPosition.LOWERED else 1.0,
        }

    def __str__(self) -> str:
        """
        Returns a string representation of the FarmTractor object.

        Returns:
            str: A string summarizing the tractor's details.
        """
        engine_status = "On" if self.engine_on else "Off"
        manual_info = self.manual_url if self.manual_url else "No manual available"
        gps_info = (
            f"GPS: {self.gps_latitude:.6f}, {self.gps_longitude:.6f}"
            if self.gps_latitude
            else "GPS: Not Set"
        )
        return (
            f"Tractor {self.make} {self.model} ({self.year})\n"
            f"Engine: {engine_status}\n"
            f"Speed: {self.speed} mph\n"
            f"Gear: {self.gear}\n"
            f"PTO: {'Engaged' if self.power_takeoff else 'Disengaged'}\n"
            f"Hydraulics: {'Activated' if self.hydraulics else 'Deactivated'}\n"
            f"{gps_info}\n"
            f"Auto-Steer: {'Enabled' if self.auto_steer_enabled else 'Disabled'}\n"
            f"Field Mode: {self.field_mode.value}\n"
            f"Implement: {self.implement_position.value}\n"
            f"Autonomous: {'Active' if self.autonomous_mode else 'Inactive'}\n"
            f"Manual URL: {manual_info}"
        )

    def to_response(self, tractor_id: str | None = None) -> FarmTractorResponse:
        """
        Convert the current tractor state to a Pydantic response model.

        Returns
        -------
        FarmTractorResponse
            A serializable snapshot of the tractor's current state.
        """
        return FarmTractorResponse(
            tractor_id=tractor_id,
            make=self.make,
            model=self.model,
            year=self.year,
            manual_url=self.manual_url,
            engine_on=self.engine_on,
            speed=self.speed,
            gear=self.gear,
            power_takeoff=self.power_takeoff,
            hydraulics=self.hydraulics,
            gps_latitude=self.gps_latitude,
            gps_longitude=self.gps_longitude,
            auto_steer_enabled=self.auto_steer_enabled,
            implement_position=self.implement_position.value,
            field_mode=self.field_mode.value,
            fuel_level=self.fuel_level,
            engine_rpm=self.engine_rpm,
            hydraulic_pressure=self.hydraulic_pressure,
            status=str(self),
        )
