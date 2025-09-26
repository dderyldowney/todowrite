# Automated Farming System API

[![AFS Testing](https://github.com/dderyldowney/afs_fastapi/actions/workflows/afs-testing.yml/badge.svg)](https://github.com/dderyldowney/afs_fastapi/actions/workflows/afs-testing.yml)

![Automated Farming System API logo](resources/static/images/afs_fastapi-logo.jpg)

## Project Outline

### 1. Project Purpose

The [AFS-FastAPI Project](https://github.com/dderyldowney/afs_fastapi) aims to harness Machine Learning (ML) and robotics to automate essential farming processes, including
operating farm equipment, maintaining soil health, and managing water quality. By integrating data-driven insights with
advanced automation, the project seeks to enhance farming efficiency, sustainability, and productivity.

The system provides a robust set of API interfaces, using [FastAPI](https://fastapi.tiangolo.com), to support diverse
use cases, ranging from controlling robotic devices and physical farm equipment to monitoring environmental factors such
as soil, water, and air quality. The APIs are designed to serve a wide range of consumers, including AI agents managing
autonomous operations and humans overseeing the overall system or specific subsystems.

---

### 2. Locating Operational Manuals for Farm Equipment

**Objective:** Identify and utilize online resources that provide operational manuals for farm equipment. These manuals
will guide the adaptation of current robotics to operate agricultural machines for automation purposes.

**FarmTractor Class:**
The `FarmTractor` is a plain Python class used in the project to represent a farm tractor. It includes attributes such as
`make`, `model`, `year`, and `manual_url` to store the URL of the operational manual for the tractor. This class is used
to demonstrate core equipment behaviors and to provide a structured way to manage tractor data within the system.

API responses that expose tractor state use a dedicated Pydantic model (`FarmTractorResponse`) to provide a stable, JSON-serializable schema without mixing API concerns into the core class.

**FarmTractor Class Attributes:**

**Core Identification:**
- `make` (str): The manufacturer of the tractor.
- `model` (str): The model of the tractor.
- `year` (int): The year of manufacture.
- `manual_url` (str | None): URL to the operational manual.

**Engine and Basic Controls:**
- `engine_on` (bool): Whether the engine is currently running.
- `speed` (int): Current speed in mph.
- `gear` (int): Current gear (0-10).
- `power_takeoff` (bool): Whether the PTO is engaged.
- `hydraulics` (bool): Whether hydraulics are activated.

**GPS and Navigation:**
- `gps_latitude` (float | None): Current GPS latitude coordinate.
- `gps_longitude` (float | None): Current GPS longitude coordinate.
- `auto_steer_enabled` (bool): Whether auto-steer is active.
- `waypoints` (List[Tuple[float, float]]): Navigation waypoints.
- `current_heading` (float): Current heading in degrees.

**Implement Controls:**
- `implement_position` (ImplementPosition): Current implement position (raised/lowered/transport).
- `implement_depth` (float): Working depth in inches.
- `implement_width` (float): Working width in feet.

**Field Operations:**
- `field_mode` (FieldMode): Current field operation mode.
- `work_rate` (float): Work rate in acres/hour.
- `area_covered` (float): Total area covered in acres.

**Engine and Fuel:**
- `fuel_level` (float): Fuel level percentage.
- `engine_rpm` (int): Engine RPM.
- `engine_temp` (float): Engine temperature in Fahrenheit.

**Hydraulics:**
- `hydraulic_pressure` (float): Hydraulic pressure in PSI.
- `hydraulic_flow` (float): Hydraulic flow in GPM.

**Sensors:**
- `wheel_slip` (float): Wheel slip percentage.
- `ground_speed` (float): Ground speed in mph.
- `draft_load` (float): Draft load in pounds.

**Autonomous Features:**
- `autonomous_mode` (bool): Whether autonomous mode is enabled.
- `obstacle_detection` (bool): Whether obstacle detection is active.
- `emergency_stop_active` (bool): Whether emergency stop is active.

**Methods:**

**Engine Controls:**
- `start_engine()` -> str: Starts the engine.
- `stop_engine()` -> str: Stops the engine and resets all systems.

**Basic Operation:**
- `change_gear(gear: int | str)` -> str: Changes the gear (0-10).
- `accelerate(increase: int)` -> str: Increases speed by the specified amount.
- `brake(decrease: int)` -> str: Decreases speed by the specified amount.

**Power Systems:**
- `engage_power_takeoff()` -> str: Engages the power takeoff.
- `disengage_power_takeoff()` -> str: Disengages the power takeoff.
- `activate_hydraulics()` -> str: Activates hydraulic systems.
- `deactivate_hydraulics()` -> str: Deactivates hydraulic systems.

**GPS and Navigation:**
- `set_gps_position(latitude: float, longitude: float)` -> str: Sets GPS coordinates.
- `enable_auto_steer()` -> str: Enables GPS auto-steer system.
- `disable_auto_steer()` -> str: Disables GPS auto-steer system.
- `add_waypoint(latitude: float, longitude: float)` -> str: Adds navigation waypoint.
- `clear_waypoints()` -> str: Clears all waypoints.
- `set_heading(heading: float)` -> str: Sets current heading (0-359 degrees).

**Implement Controls:**
- `raise_implement()` -> str: Raises the attached implement.
- `lower_implement(depth: float = 6.0)` -> str: Lowers implement to working depth.
- `set_transport_position()` -> str: Sets implement to transport position.
- `set_implement_width(width: float)` -> str: Sets working width (0-80 feet).

**Field Operations:**
- `set_field_mode(mode: FieldMode)` -> str: Sets field operation mode.
- `start_field_work()` -> str: Begins field work operations.
- `update_work_progress(distance: float)` -> str: Updates work progress tracking.

**Autonomous Operations:**
- `enable_autonomous_mode()` -> str: Enables autonomous operation mode.
- `disable_autonomous_mode()` -> str: Disables autonomous operation mode.
- `emergency_stop()` -> str: Triggers emergency stop - halts all operations.
- `reset_emergency_stop()` -> str: Resets emergency stop condition.

**Diagnostic Methods:**
- `get_engine_diagnostics()` -> Dict[str, float]: Returns engine diagnostic data.
- `get_hydraulic_status()` -> Dict[str, float]: Returns hydraulic system status.
- `get_ground_conditions()` -> Dict[str, float]: Returns ground and traction data.

**Utility Methods:**
- `__str__()` -> str: Returns comprehensive string representation.
- `to_response(tractor_id: str | None = None)` -> FarmTractorResponse: Converts to API response model.

**FarmTractorResponse Class Attributes:**

The `FarmTractorResponse` is a Pydantic model used for API responses, containing:

- `tractor_id` (str | None): Optional tractor identifier.
- `make` (str): Manufacturer name.
- `model` (str): Model name.
- `year` (int): Year of manufacture.
- `manual_url` (str | None): URL to operator's manual.
- `engine_on` (bool): Engine running status.
- `speed` (int): Current speed in mph.
- `gear` (int): Current gear (0-10).
- `power_takeoff` (bool): PTO engagement status.
- `hydraulics` (bool): Hydraulics activation status.
- `gps_latitude` (float | None): GPS latitude coordinate.
- `gps_longitude` (float | None): GPS longitude coordinate.
- `auto_steer_enabled` (bool): Auto-steer status.
- `implement_position` (Literal["raised", "lowered", "transport"]): Implement position state.
- `field_mode` (Literal["transport", "tillage", "planting", "spraying", "harvesting", "maintenance"]): Current field operation mode.
- `fuel_level` (float): Fuel level percentage.
- `engine_rpm` (int): Engine RPM.
- `hydraulic_pressure` (float): Hydraulic pressure in PSI.
- `status` (str): Complete tractor status string.

**Example Usage:**

```python
from afs_fastapi.equipment.farm_tractors import FarmTractor, FieldMode

# Create a new tractor instance
tractor = FarmTractor(
    make="John Deere",
    model="9RX",
    year=2023,
    manual_url="https://www.deere.com/en/parts-and-service/manuals-and-training"
)

# Basic tractor information
print(f"Tractor: {tractor.make} {tractor.model} ({tractor.year})")
print(f"Manual: {tractor.manual_url}")
print(f"Current status:\n{tractor}")

# Start the engine and begin operations
tractor.start_engine()
print("\n--- Engine Started ---")

# Set up GPS and navigation
tractor.set_gps_position(40.123456, -85.654321)
tractor.enable_auto_steer()
tractor.add_waypoint(40.125000, -85.650000)
tractor.add_waypoint(40.127000, -85.648000)
print("GPS and auto-steer configured")

# Configure for field work
tractor.change_gear(3)
tractor.accelerate(12)  # 12 mph working speed
tractor.activate_hydraulics()
tractor.set_implement_width(32.0)  # 32-foot implement
tractor.lower_implement(8.0)  # 8 inches deep
tractor.set_field_mode(FieldMode.TILLAGE)
print("Configured for tillage operations")

# Start field work
tractor.start_field_work()
print(f"Work rate: {tractor.work_rate:.1f} acres/hour")

# Simulate work progress
tractor.update_work_progress(1320)  # Covered 1/4 mile
print(f"Area covered: {tractor.area_covered:.2f} acres")

# Enable autonomous mode for precision farming
tractor.enable_autonomous_mode()
print("Autonomous mode active")

# Get diagnostic information
engine_diagnostics = tractor.get_engine_diagnostics()
hydraulic_status = tractor.get_hydraulic_status()
ground_conditions = tractor.get_ground_conditions()

print(f"\n--- Diagnostics ---")
print(f"Engine RPM: {engine_diagnostics['rpm']}")
print(f"Fuel level: {engine_diagnostics['fuel_level']:.1f}%")
print(f"Hydraulic pressure: {hydraulic_status['pressure']:.0f} PSI")
print(f"Ground speed: {ground_conditions['ground_speed']:.1f} mph")
print(f"Wheel slip: {ground_conditions['wheel_slip']:.1f}%")

# Convert to API response format
response = tractor.to_response("tractor-001")
print(f"\n--- API Response ---")
print(f"Tractor ID: {response.tractor_id}")
print(f"Field mode: {response.field_mode}")
print(f"Implement position: {response.implement_position}")
print(f"Auto-steer enabled: {response.auto_steer_enabled}")

# Emergency stop if needed
# tractor.emergency_stop()
# print("Emergency stop activated!")

# End of field work - transport mode
tractor.raise_implement()
tractor.set_transport_position()
tractor.set_field_mode(FieldMode.TRANSPORT)
tractor.disable_autonomous_mode()
tractor.accelerate(8)  # Increase speed for transport
print("\n--- Configured for transport ---")

# Final status
print(f"\nFinal status:\n{tractor}")

# Stop engine when done
tractor.stop_engine()
print("Engine stopped - all systems reset")
```

**Sources:**

1. [AgManuals](https://agmanuals.com)
2. [Case IH Operator Manuals](https://www.caseih.com/en-us/unitedstates/service-support/operators-manuals)
3. [Farm Manuals Fast](https://farmmanualsfast.com)
4. [AGCO Technical Publications](https://www.agcopubs.com)
5. [John Deere Manuals and Training](https://www.deere.com/en/parts-and-service/manuals-and-training)
6. [Farming and Construction Manuals](https://farming-constructionmanuals.com)
7. [Solano Horizonte](https://solano-horizonte.com/download-catalogs-and-manuals-of-agricultural-machinery)
8. [Yesterday's Tractors Forums](https://forums.yesterdaystractors.com)
9. [Tractor Tools Direct](https://tractortoolsdirect.com/manuals)
10. [General Implement Distributors](https://www.generalimp.com/manuals)
11. [TractorData](https://www.tractordata.com)
12. [Tractor Manuals Downunder](https://www.tractor-manuals-downunder.com)

---

**Build Process:**

To build the project, follow these steps:

1. Clone the repository: `git clone https://github.com/dderyldowney/afs_fastapi.git`
2. Change to the project directory: `cd afs_fastapi`
3. Create a virtual environment: `python -m venv .venv`
4. Activate the virtual environment: `source .venv/bin/activate`
5. Install the project dependencies: `pip install -r requirements.txt`
6. Install build tools: `pip install build`
7. Build the project: `python -m build`
8. Install the generated wheel file: `pip install dist/afs_fastapi-0.1.0-py3-none-any.whl`
9. Import afs_fastapi into your project: `import afs_fastapi`

Note on extras: The project uses `fastapi[all]` and `starlette[full]` in development to enable optional features commonly exercised in tests and local runs (e.g., test client utilities, templating, multipart/form-data handling, and uvicorn’s standard extras). This keeps “pip install -r requirements.txt” sufficient for running tests and docs locally.

---

**Run the API locally:**

- Quick start (defaults to 127.0.0.1:8000):
  - `python -m afs_fastapi`
  - or `afs-api` (installed console script)
- Environment overrides:
  - `AFS_API_HOST` (default: 127.0.0.1)
  - `AFS_API_PORT` (default: 8000)
  - `AFS_API_RELOAD` (true/false, default: false)
  - `AFS_API_LOG_LEVEL` (debug/info/warning/error, default: info)

---

**Sensor backend interfaces:**

Monitoring classes accept pluggable backends so you can swap real sensors without changing API code.

Example (Soil):

```python
from afs_fastapi.monitoring.interfaces import SoilSensorBackend
from afs_fastapi.monitoring.soil_monitor import SoilMonitor

class MySoilBackend(SoilSensorBackend):
    def read(self, sensor_id: str):
        return {"ph": 6.7, "moisture": 0.33, "nitrogen": 1.2, "phosphorus": 0.5, "potassium": 0.7}

monitor = SoilMonitor("SOIL001", backend=MySoilBackend())
print(monitor.get_soil_composition())
```

Example (Water):

```python
from afs_fastapi.monitoring.interfaces import WaterSensorBackend
from afs_fastapi.monitoring.water_monitor import WaterMonitor

class MyWaterBackend(WaterSensorBackend):
    def read(self, sensor_id: str):
        return {"ph": 7.2, "turbidity": 1.1, "temperature": 18.0, "conductivity": 0.23, "dissolved_oxygen": 8.0}

monitor = WaterMonitor("WTR001", backend=MyWaterBackend())
print(monitor.get_water_quality())
```

---

### 3. Monitoring and Maintaining Soil Conditions

**Objective:** Research and utilize tools, sensors, and platforms to monitor soil composition, mineral content, and pH
balance, ensuring optimal crop health.

**Resources:**

1. [Soil Scout](https://soilscout.com)
2. [Renke 4-in-1 Soil Nutrient Sensor](https://www.renkeer.com/product/soil-nutrient-sensor/)
3. [Murata Soil Sensors](https://www.murata.com/en-us/products/sensor/soil)
4. [HORIBA LAQUAtwin pH Meters](https://www.horiba.com/usa/water-quality/applications/agriculture-crop-science/soil-ph-and-nutrient-availability/)
5. [Sensoterra Soil Moisture Sensors](https://www.sensoterra.com/soil-sensor-for-agriculture/)
6. [DFRobot 4-in-1 Soil Sensor](https://www.dfrobot.com/product-2830.html)
7. [EarthScout Agricultural Field Sensors](https://www.earthscout.com/)
8. [University of Minnesota Extension: Soil Moisture Sensors](https://extension.umn.edu/irrigation/soil-moisture-sensors-irrigation-scheduling)
9. [ATTRA: Soil Moisture Monitoring Tools](https://attra.ncat.org/publication/soil-moisture-monitoring-low-cost-tools-and-methods/)
10. [ESCATEC Electrochemical Sensors](https://www.escatec.com/blog/electrochemical-sensors-soil-analysis-through-precision-agriculture)

---

### 4. Monitoring and Maintaining Water Conditions

**Objective:** Identify and deploy tools to assess and maintain water composition, mineral levels, and pH balance,
ensuring water quality is optimized for agricultural use.

**Resources:**

1. [Renke Water Quality Sensors](https://www.renkeer.com/top-7-water-quality-sensors/)
2. [In-Situ Agriculture Water Monitoring](https://in-situ.com/us/agriculture)
3. [Xylem Analytics Water Quality Monitoring](https://www.xylemanalytics.com/en/products/water-quality-monitoring)
4. [KETOS Automated Water Monitoring](https://ketos.co/)
5. [YSI Water Quality Systems](https://www.ysi.com/products)
6. [SGS Agricultural Water Testing](https://www.sgs.com/en-us/services/agricultural-water-testing)
7. [Boqu Instrument Water Quality Sensors](https://www.boquinstrument.com/how-water-quality-sensors-are-used-in-agriculture-and-farming.html)
8. [Digital Matter Remote Sensor Solutions](https://sense.digitalmatter.com/blog/water-quality-monitoring)
9. [Intuz IoT Water Monitoring](https://www.intuz.com/blog/iot-for-water-monitoring-in-crops)
10. [Rika Sensor Water Quality Sensors](https://www.rikasensor.com/blog-top-10-water-quality-sensors-for-water-treatments.html)

---

### 5. Utilizing Publicly Available Water Sampling Datasets

**Objective:** Access and analyze publicly available water quality datasets to inform ML models for monitoring water
conditions suitable for farming.

**Sources:**

1. [Water Quality Portal (WQP)](https://www.waterqualitydata.us/)
2. [USGS National Water Information System (NWIS)](https://catalog.data.gov/dataset)
3. [EPA Water Quality Data](https://www.epa.gov/waterdata/water-quality-data)
4. [Kaggle: Water Quality Dataset for Crop](https://www.kaggle.com/datasets/abhishekkhanna004/water-quality-dataset-for-crop)
5. [Ag Data Commons: Soil and Water Hub Modeling](https://agdatacommons.nal.usda.gov/articles/dataset/Soil_and_Water_Hub_Modeling_Datasets/24852681)
6. [NASA Earthdata: Water Quality](https://www.earthdata.nasa.gov/topics/ocean/water-quality)

---

### 6. Project Integration and Machine Learning Goals

**Objective:** Synthesize the research and datasets into ML models and robotics systems capable of automating farm
operations, improving efficiency, and ensuring sustainability. Models will address:

- Autonomous machine operation (leveraging operational manuals).
- Soil condition predictions and adjustments.
- Water quality monitoring and real-time management.

**Tools and Techniques:**

- ML libraries like TensorFlow and PyTorch.
- IoT-enabled sensors for real-time data collection.
- Integration with cloud platforms for data storage and analysis.

---

### Conclusion

This project will employ cutting-edge ML and robotics solutions to automate farming processes, ensuring optimized
resource utilization and sustainable agricultural practices.

---

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for the Quick Verification Checklist and contribution guidelines.

---

## Security Notes

This project enables automated checks (Dependabot + pip-audit) for dependency vulnerabilities. Two current advisories are known and monitored:

- **Starlette 0.41.3: GHSA-2c2j-9gv5-cj73 (CVE-2025-54121)** - **UNRESOLVED**
  - Summary: Large multipart form uploads may block the event loop while rolling files to disk.
  - Current version: **0.41.3** (vulnerable)
  - Fixed in: Starlette >= 0.47.2
  - Project impact: This API does not use multipart uploads; risk is low in our deployment.
  - Status: Awaiting compatible FastAPI release that supports Starlette >= 0.47.2.

- **h11 0.14.0: GHSA-vqfr-h8mv-ghfj (CVE-2025-43859)** - **UNRESOLVED**
  - Summary: Lenient chunked-encoding parsing could enable request smuggling in specific proxy scenarios.
  - Current version: **0.14.0** (vulnerable)
  - Fixed in: h11 >= 0.16.0
  - Project impact: h11 is used via httpx/httpcore for HTTP client operations. Server stack uses Uvicorn/Starlette. Risk is low in typical deployments with proper reverse proxy configuration.
  - Status: Upgrade blocked by httpcore compatibility. Requires httpcore >= 1.0.9 which conflicts with current httpx pinning.

**Recent Security Improvements (January 2025):**
- ✅ **requests**: Upgraded to 2.32.5 (latest) - includes URI parsing security improvements
- ✅ **urllib3**: Upgraded to 2.5.0 (latest) - fixes redirect vulnerability (security patch)
- ✅ **setuptools**: Upgraded to 80.9.0 (latest) - stability and security updates

**Mitigations in place:**
- No multipart form endpoints are exposed in the API.
- HTTP client usage is limited to development/testing scenarios.
- CI automatically flags vulnerabilities and proposes coordinated updates.
- Reverse proxy configurations should include proper request validation.
