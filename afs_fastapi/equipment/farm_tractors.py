from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import ClassVar, Literal

from pydantic import BaseModel

# ==============================================================================
# ISOBUS Communication Interfaces (ISO 11783 Compliance)
# ==============================================================================


@dataclass
class ISOBUSMessage:
    """Standard ISOBUS message structure."""

    pgn: int  # Parameter Group Number
    source_address: int
    destination_address: int
    data: bytes
    timestamp: datetime


class ISOBUSDevice(ABC):
    """Abstract base class for ISOBUS-compatible devices."""

    @abstractmethod
    def get_device_name(self) -> str:
        """Return standardized device name."""
        pass

    @abstractmethod
    def send_message(self, message: ISOBUSMessage) -> bool:
        """Send ISOBUS message."""
        pass

    @abstractmethod
    def receive_message(self) -> ISOBUSMessage | None:
        """Receive ISOBUS message."""
        pass


# ==============================================================================
# Vision & Optical Sensor Interfaces
# ==============================================================================


@dataclass
class CameraConfig:
    """Camera system configuration."""

    resolution: tuple[int, int]  # width, height
    frame_rate: int
    field_of_view: float  # degrees
    exposure_mode: str
    color_space: str


@dataclass
class LiDARPoint:
    """3D point from LiDAR sensor."""

    x: float
    y: float
    z: float
    intensity: float
    timestamp: datetime


class VisionSensorInterface(ABC):
    """Abstract interface for vision sensors."""

    @abstractmethod
    def capture_frame(self) -> bytes | None:
        """Capture a single frame."""
        pass

    @abstractmethod
    def get_point_cloud(self) -> list[LiDARPoint]:
        """Get LiDAR point cloud data."""
        pass

    @abstractmethod
    def detect_obstacles(self, max_distance: float) -> list[tuple[float, float, float]]:
        """Detect obstacles within specified distance."""
        pass


# ==============================================================================
# Safety & Compliance Interfaces (ISO 18497 Series)
# ==============================================================================


class SafetyLevel(str, Enum):
    """ISO 18497 safety levels."""

    PERFORMANCE_LEVEL_C = "PLc"
    PERFORMANCE_LEVEL_D = "PLd"
    PERFORMANCE_LEVEL_E = "PLe"


@dataclass
class SafetyZone:
    """Defined safety zone around equipment."""

    zone_id: str
    boundary_points: list[tuple[float, float]]  # GPS coordinates
    safety_level: SafetyLevel
    max_speed: float  # mph
    detection_required: bool


class SafetySystemInterface(ABC):
    """Abstract interface for ISO 18497 safety systems."""

    @abstractmethod
    def emergency_stop(self) -> bool:
        """Trigger emergency stop per ISO 18497."""
        pass

    @abstractmethod
    def validate_safety_zone(self, position: tuple[float, float]) -> bool:
        """Validate position is within safe operating zone."""
        pass

    @abstractmethod
    def get_safety_status(self) -> dict[str, bool]:
        """Get comprehensive safety system status."""
        pass


# ==============================================================================
# Motor Control & Actuation Interfaces
# ==============================================================================


class MotorType(str, Enum):
    """Types of motor actuators."""

    BRUSHLESS_DC = "bldc"
    SERVO = "servo"
    STEPPER = "stepper"
    LINEAR_ACTUATOR = "linear"
    QDD_ACTUATOR = "qdd"


@dataclass
class MotorCommand:
    """Motor control command structure."""

    motor_id: str
    command_type: str  # position, velocity, torque
    target_value: float
    max_velocity: float | None = None
    max_acceleration: float | None = None


class MotorControlInterface(ABC):
    """Abstract interface for precision motor control."""

    @abstractmethod
    def send_motor_command(self, command: MotorCommand) -> bool:
        """Send command to specific motor."""
        pass

    @abstractmethod
    def get_motor_status(self, motor_id: str) -> dict[str, float]:
        """Get current motor status and position."""
        pass

    @abstractmethod
    def calibrate_motor(self, motor_id: str) -> bool:
        """Perform motor calibration sequence."""
        pass


# ==============================================================================
# Data Management & Connectivity Interfaces
# ==============================================================================


@dataclass
class TaskData:
    """ISO XML task data structure."""

    task_id: str
    field_id: str
    operation_type: str
    prescription_map: dict[str, float] | None
    start_time: datetime
    end_time: datetime | None = None


class DataManagementInterface(ABC):
    """Abstract interface for agricultural data management."""

    @abstractmethod
    def export_iso_xml(self, task_data: TaskData) -> str:
        """Export data in ISO XML format."""
        pass

    @abstractmethod
    def import_prescription_map(self, map_data: bytes) -> dict[str, float]:
        """Import variable rate prescription map."""
        pass

    @abstractmethod
    def log_operation_data(self, data_point: dict[str, float]) -> bool:
        """Log operational data point."""
        pass


# ==============================================================================
# Power & Energy Management Interfaces
# ==============================================================================


@dataclass
class PowerSource:
    """Power source configuration."""

    source_type: str  # solar, fuel_cell, battery, grid
    voltage: float
    max_current: float
    efficiency: float


class PowerManagementInterface(ABC):
    """Abstract interface for power system management."""

    @abstractmethod
    def get_power_status(self) -> dict[str, float]:
        """Get comprehensive power system status."""
        pass

    @abstractmethod
    def set_power_priority(self, device_priorities: dict[str, int]) -> bool:
        """Set power allocation priorities."""
        pass

    @abstractmethod
    def enable_regenerative_mode(self) -> bool:
        """Enable energy recovery from motion."""
        pass


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
    waypoint_count : int
        Number of navigation waypoints.
    current_heading : float
        Current heading in degrees.
    implement_depth : float
        Working depth in inches.
    implement_width : float
        Working width in feet.
    work_rate : float
        Work rate in acres/hour.
    area_covered : float
        Total area covered in acres.
    engine_temp : float
        Engine temperature in Fahrenheit.
    hydraulic_flow : float
        Hydraulic flow in GPM.
    wheel_slip : float
        Wheel slip percentage.
    ground_speed : float
        Ground speed in mph.
    draft_load : float
        Draft load in pounds.
    autonomous_mode : bool
        Whether autonomous mode is enabled.
    obstacle_detection : bool
        Whether obstacle detection is active.
    emergency_stop_active : bool
        Whether emergency stop is active.
    isobus_address : int
        ISOBUS device address.
    device_name : str
        ISOBUS device name.
    safety_system_active : bool
        Whether safety system is active.
    safety_level : str
        Current safety performance level.
    regenerative_mode : bool
        Whether regenerative power mode is enabled.
    lidar_enabled : bool
        Whether LiDAR sensors are enabled.
    obstacle_count : int
        Number of detected obstacles.
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

    # Enhanced fields for robotic interfaces
    waypoint_count: int = 0
    current_heading: float = 0.0
    implement_depth: float = 0.0
    implement_width: float = 0.0
    work_rate: float = 0.0
    area_covered: float = 0.0
    engine_temp: float = 180.0
    hydraulic_flow: float = 0.0
    wheel_slip: float = 0.0
    ground_speed: float = 0.0
    draft_load: float = 0.0
    autonomous_mode: bool = False
    obstacle_detection: bool = True
    emergency_stop_active: bool = False
    isobus_address: int = 0x80
    device_name: str = ""
    safety_system_active: bool = True
    safety_level: Literal["PLc", "PLd", "PLe"] = "PLc"
    regenerative_mode: bool = False
    lidar_enabled: bool = False
    obstacle_count: int = 0

    status: str


class FarmTractor(
    ISOBUSDevice,
    SafetySystemInterface,
    MotorControlInterface,
    DataManagementInterface,
    PowerManagementInterface,
):
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
        self.waypoints: list[tuple[float, float]] = []
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

        # ISOBUS Communication
        self.isobus_address: int = 0x80  # Default address
        self.device_name: str = f"{make}_{model}_{year}"
        self.message_queue: list[ISOBUSMessage] = []

        # Vision & Sensor Systems
        self.camera_config: CameraConfig | None = None
        self.lidar_enabled: bool = False
        self.obstacle_list: list[tuple[float, float, float]] = []

        # Safety Systems (ISO 18497)
        self.safety_zones: list[SafetyZone] = []
        self.safety_level: SafetyLevel = SafetyLevel.PERFORMANCE_LEVEL_C
        self.safety_system_active: bool = True

        # Motor Control Systems
        self.motors: dict[str, dict[str, float]] = {
            "steer_motor": {"position": 0.0, "velocity": 0.0, "torque": 0.0},
            "throttle_motor": {"position": 0.0, "velocity": 0.0, "torque": 0.0},
            "implement_lift": {"position": 0.0, "velocity": 0.0, "torque": 0.0},
        }

        # Data Management
        self.operation_log: list[dict[str, float]] = []
        self.current_task: TaskData | None = None

        # Power Management
        self.power_sources: list[PowerSource] = [
            PowerSource("diesel_engine", 12.0, 200.0, 0.85),
            PowerSource("alternator", 12.0, 100.0, 0.90),
        ]
        self.power_consumption: dict[str, float] = {}
        self.regenerative_mode: bool = False

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
        except ValueError as e:
            raise ValueError("Invalid gear value") from e

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

    def reset_emergency_stop(self) -> str:
        """Reset emergency stop condition."""
        if not self.emergency_stop_active:
            raise ValueError("Emergency stop is not active")

        self.emergency_stop_active = False
        return "Emergency stop reset - Manual control restored"

    # Sensor Reading Methods
    def get_engine_diagnostics(self) -> dict[str, float]:
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

    def get_hydraulic_status(self) -> dict[str, float]:
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

    def get_ground_conditions(self) -> dict[str, float]:
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

    # ==============================================================================
    # ISOBUS Communication Interface Implementation
    # ==============================================================================

    def get_device_name(self) -> str:
        """Return standardized ISOBUS device name."""
        return self.device_name

    def send_message(self, message: ISOBUSMessage) -> bool:
        """Send ISOBUS message to network."""
        # TODO: Implement actual ISOBUS CAN transmission
        print(f"ISOBUS TX: PGN={message.pgn:04X} from {message.source_address:02X}")
        return True

    def receive_message(self) -> ISOBUSMessage | None:
        """Receive ISOBUS message from network."""
        # TODO: Implement actual ISOBUS CAN reception
        if self.message_queue:
            return self.message_queue.pop(0)
        return None

    def send_tractor_status(self) -> bool:
        """Send standardized tractor status via ISOBUS."""
        status_data = bytes(
            [
                self.gear,
                int(self.speed),
                int(self.engine_rpm / 10),
                int(self.fuel_level),
                0x01 if self.engine_on else 0x00,
            ]
        )

        message = ISOBUSMessage(
            pgn=0xFE48,  # Tractor status PGN
            source_address=self.isobus_address,
            destination_address=0xFF,  # Broadcast
            data=status_data,
            timestamp=datetime.now(),
        )

        return self.send_message(message)

    # ==============================================================================
    # Safety System Interface Implementation (ISO 18497)
    # ==============================================================================

    def emergency_stop(self) -> bool:
        """Trigger ISO 18497 compliant emergency stop."""
        self.emergency_stop_active = True
        self.speed = 0
        self.autonomous_mode = False
        self.auto_steer_enabled = False

        # Raise implement for safety
        if self.implement_position == ImplementPosition.LOWERED:
            self.implement_position = ImplementPosition.RAISED

        # Log safety event (using numeric codes: 999 = emergency_stop)
        self.log_operation_data(
            {
                "event_code": 999.0,  # Emergency stop event code
                "timestamp": datetime.now().timestamp(),
                "position_lat": self.gps_latitude or 0.0,
                "position_lon": self.gps_longitude or 0.0,
            }
        )

        print("ISO 18497 EMERGENCY STOP ACTIVATED")
        return True

    def validate_safety_zone(self, position: tuple[float, float]) -> bool:
        """Validate position is within defined safety zones."""
        if not self.safety_zones:
            return True  # No zones defined = unrestricted

        lat, lon = position
        for zone in self.safety_zones:
            # Simple point-in-polygon check (simplified)
            if self._point_in_polygon((lat, lon), zone.boundary_points):
                return True

        return False

    def _point_in_polygon(
        self, point: tuple[float, float], polygon: list[tuple[float, float]]
    ) -> bool:
        """Helper method for point-in-polygon calculation."""
        # Simplified implementation - would use proper geospatial library
        return True  # TODO: Implement proper geospatial checking

    def get_safety_status(self) -> dict[str, bool]:
        """Get comprehensive ISO 18497 safety status."""
        current_position = (self.gps_latitude or 0.0, self.gps_longitude or 0.0)

        return {
            "emergency_stop_active": self.emergency_stop_active,
            "safety_system_operational": self.safety_system_active,
            "position_safe": self.validate_safety_zone(current_position),
            "obstacle_detection_active": self.obstacle_detection,
            "speed_limit_compliant": self.speed <= 25,  # Example limit
            "operator_present": not self.autonomous_mode,
        }

    def add_safety_zone(self, zone: SafetyZone) -> str:
        """Add a safety zone for autonomous operation."""
        self.safety_zones.append(zone)
        return f"Safety zone {zone.zone_id} added with {len(zone.boundary_points)} boundary points"

    # ==============================================================================
    # Motor Control Interface Implementation
    # ==============================================================================

    def send_motor_command(self, command: MotorCommand) -> bool:
        """Send precision motor control command."""
        if command.motor_id not in self.motors:
            print(f"Warning: Motor {command.motor_id} not found")
            return False

        motor_status = self.motors[command.motor_id]

        # Update motor status based on command
        if command.command_type == "position":
            motor_status["position"] = command.target_value
        elif command.command_type == "velocity":
            motor_status["velocity"] = command.target_value
        elif command.command_type == "torque":
            motor_status["torque"] = command.target_value

        print(f"Motor {command.motor_id} {command.command_type} set to {command.target_value}")
        return True

    def get_motor_status(self, motor_id: str) -> dict[str, float]:
        """Get current motor status and position."""
        if motor_id not in self.motors:
            return {"error": -1.0}

        return self.motors[motor_id].copy()

    def calibrate_motor(self, motor_id: str) -> bool:
        """Perform motor calibration sequence."""
        if motor_id not in self.motors:
            return False

        # Simulate calibration
        self.motors[motor_id]["position"] = 0.0
        self.motors[motor_id]["velocity"] = 0.0
        self.motors[motor_id]["torque"] = 0.0

        print(f"Motor {motor_id} calibrated successfully")
        return True

    # ==============================================================================
    # Data Management Interface Implementation
    # ==============================================================================

    def export_iso_xml(self, task_data: TaskData) -> str:
        """Export agricultural data in ISO 11783-10 XML format."""
        # Simplified ISO XML generation
        xml_data = f"""<?xml version="1.0" encoding="UTF-8"?>
<ISO11783_TaskData>
    <TSK A="{task_data.task_id}" B="{task_data.operation_type}"
         C="{task_data.start_time.isoformat()}" D="1" E="{task_data.field_id}">
        <TLG A="{len(self.operation_log)}">
            <!-- Operation log data would be here -->
        </TLG>
    </TSK>
</ISO11783_TaskData>"""
        return xml_data

    def import_prescription_map(self, map_data: bytes) -> dict[str, float]:
        """Import variable rate prescription map."""
        # TODO: Implement proper map parsing
        # For now, return simulated prescription data
        return {
            "seed_rate": 32000.0,  # seeds per acre
            "fertilizer_rate": 150.0,  # lbs per acre
            "spray_rate": 20.0,  # gallons per acre
        }

    def log_operation_data(self, data_point: dict[str, float]) -> bool:
        """Log operational data point for analysis."""
        enhanced_data = data_point.copy()
        enhanced_data.update(
            {
                "timestamp": datetime.now().timestamp(),
                "speed": float(self.speed),
                "fuel_level": self.fuel_level,
                "engine_rpm": float(self.engine_rpm),
            }
        )

        self.operation_log.append(enhanced_data)
        return True

    def start_task_recording(self, task_id: str, field_id: str, operation_type: str) -> str:
        """Start recording a new field task."""
        self.current_task = TaskData(
            task_id=task_id,
            field_id=field_id,
            operation_type=operation_type,
            prescription_map=None,
            start_time=datetime.now(),
        )
        return f"Task recording started: {task_id}"

    def stop_task_recording(self) -> str:
        """Stop current task recording."""
        if self.current_task:
            self.current_task.end_time = datetime.now()
            task_id = self.current_task.task_id
            self.current_task = None
            return f"Task recording stopped: {task_id}"
        return "No active task to stop"

    # ==============================================================================
    # Power Management Interface Implementation
    # ==============================================================================

    def get_power_status(self) -> dict[str, float]:
        """Get comprehensive power system status."""
        total_available = sum(
            ps.voltage * ps.max_current * ps.efficiency for ps in self.power_sources
        )
        total_consumption = sum(self.power_consumption.values())

        return {
            "total_available_power": total_available,
            "total_consumption": total_consumption,
            "power_efficiency": (
                (total_available - total_consumption) / total_available
                if total_available > 0
                else 0.0
            ),
            "battery_level": self.fuel_level,  # Simplified
            "regenerative_active": float(self.regenerative_mode),
            "diesel_engine_load": float(self.engine_rpm / 2500.0) if self.engine_on else 0.0,
        }

    def set_power_priority(self, device_priorities: dict[str, int]) -> bool:
        """Set power allocation priorities for different systems."""
        # TODO: Implement actual power management logic
        print(f"Power priorities set: {device_priorities}")
        return True

    def enable_regenerative_mode(self) -> bool:
        """Enable energy recovery from hydraulic and motion systems."""
        if self.engine_on:
            self.regenerative_mode = True
            print("Regenerative energy recovery enabled")
            return True
        return False

    def disable_regenerative_mode(self) -> bool:
        """Disable energy recovery mode."""
        self.regenerative_mode = False
        print("Regenerative energy recovery disabled")
        return True

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
            # Enhanced robotic interface fields
            waypoint_count=len(self.waypoints),
            current_heading=self.current_heading,
            implement_depth=self.implement_depth,
            implement_width=self.implement_width,
            work_rate=self.work_rate,
            area_covered=self.area_covered,
            engine_temp=self.engine_temp,
            hydraulic_flow=self.hydraulic_flow,
            wheel_slip=self.wheel_slip,
            ground_speed=self.ground_speed,
            draft_load=self.draft_load,
            autonomous_mode=self.autonomous_mode,
            obstacle_detection=self.obstacle_detection,
            emergency_stop_active=self.emergency_stop_active,
            isobus_address=self.isobus_address,
            device_name=self.device_name,
            safety_system_active=self.safety_system_active,
            safety_level=self.safety_level.value,
            regenerative_mode=self.regenerative_mode,
            lidar_enabled=self.lidar_enabled,
            obstacle_count=len(self.obstacle_list),
            status=str(self),
        )
