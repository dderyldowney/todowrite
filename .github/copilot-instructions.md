## AFS-FastAPI — Copilot instructions (short)

This file helps AI coding agents be immediately productive in this repository.

High level
- The project is a small FastAPI application that exposes equipment and monitoring APIs.
- Entrypoint: `python -m afs_fastapi` (see `afs_fastapi/__main__.py`). Uvicorn is used to run the app: `uvicorn.run("afs_fastapi.api.main:app", ...)`.
- Config via environment variables: `AFS_API_HOST`, `AFS_API_PORT`, `AFS_API_RELOAD`, `AFS_API_LOG_LEVEL`. CORS origins may be set with `AFS_CORS_ORIGINS` (comma-separated) in `afs_fastapi/api/main.py`.

Architecture & boundaries
- API layer: `afs_fastapi/api/main.py` — defines FastAPI app, routes (`/`, `/health`, `/version`, `/equipment/tractor/{id}`, `/monitoring/{soil|water}/{id}`) and response models.
- Domain/equipment: `afs_fastapi/equipment/farm_tractors.py` — domain class `FarmTractor` with logic and `to_response()` that returns `FarmTractorResponse` (a Pydantic model). Prefer converting domain objects to response models for API output.
- Monitoring: `afs_fastapi/monitoring/*` —
  - `interfaces.py` defines abstract backends (`SoilSensorBackend`, `WaterSensorBackend`) and `Dummy*` implementations used by default.
  - `soil_monitor.py` / `water_monitor.py` wrap a backend and expose `get_*` and `log_reading()` methods.
- Schemas: `afs_fastapi/monitoring/schemas.py` — Pydantic models for transport layer (keep these separate from domain/backends).

Conventions & patterns to follow
- Separation of concerns: domain classes (e.g., `FarmTractor`) are plain Python classes; API-facing types are Pydantic models (`*Response`). Use `.to_response()` where available.
- Pluggable backends: monitoring uses abstract base classes. When adding integrations, implement `read(sensor_id: str) -> Dict[str, float]` and pass it into monitors (e.g., `SoilMonitor(sensor_id, backend=MyBackend())`).
- Defaults: tests and local runs expect `Dummy*` backends; avoid changing defaults unless adding real hardware integration and corresponding tests.
- Environment-driven runtime: respect `AFS_API_*` env vars in `__main__.py`.

Developer workflows (commands discovered in README)
- Install deps and run tests locally:
  - Create venv, pip install -r requirements.txt
  - Run tests: `pytest` (project has unit and integration tests under `tests/` and `tests/unit/`).
- Run API locally (no docker):
  - `python -m afs_fastapi` (defaults to 127.0.0.1:8000)
  - Or install and run the console script `afs-api` if packaged.

Testing & CI notes
- Tests live in `tests/` with subfolders `unit/` and `features/`. Look at `tests/unit/equipment/test_farm_tractor.py` to see usage patterns (happy-path + error conditions) for `FarmTractor`.
- CI workflow referenced in README: `.github/workflows/afs-testing.yml` (badge present in README). Respect CI linting and pinned package versions.

Integration points & external dependencies
- FastAPI / Starlette / Uvicorn: app and middleware in `afs_fastapi/api/main.py` and `__main__.py`.
- No external sensor drivers included — integrations should implement the sensor backend ABCs in `monitoring/interfaces.py`.
- Packaging: project uses standard Python packaging (pyproject/setup.cfg/setup.py). README documents `python -m build` and wheel installation.

Code examples agents can use
- Return a tractor response in an API handler:
  - create `FarmTractor(...)` and call `.to_response(tractor_id)` (see `api/main.py` and `equipment/farm_tractors.py`).
- Add a real soil backend:
  - implement `class MySoilBackend(SoilSensorBackend): def read(self, sensor_id): ...` then `SoilMonitor(sensor_id, backend=MySoilBackend())`.

When editing code
- Keep domain logic in `afs_fastapi/equipment` or `afs_fastapi/monitoring`; keep API shape / validation in `monitoring/schemas.py` and `equipment/*.py` response models.
- Follow existing error handling: domain methods raise `ValueError` for invalid operations (see `FarmTractor.change_gear`, `start_engine`, etc.). Tests expect exceptions for invalid states.

Files to inspect for examples
- `afs_fastapi/api/main.py`, `afs_fastapi/__main__.py`, `afs_fastapi/equipment/farm_tractors.py`, `afs_fastapi/monitoring/interfaces.py`, `afs_fastapi/monitoring/soil_monitor.py`, `afs_fastapi/monitoring/schemas.py`, `tests/unit/equipment/test_farm_tractor.py`.

Conservative editing rules for AI agents
- Don't modify environment variable names or the CLI entrypoint without updating `__main__.py` and README.
- When adding sensor backends, include tests using the Dummy backends or simple mock classes under `tests/`.
- Preserve public API routes and response model shapes unless explicitly changing version (update `__version__` in `afs_fastapi/version.py` and add a changelog entry).

If uncertain, ask the maintainer to clarify:
- Which sensor integrations are targeted (MQTT, HTTP gateway, serial)?
- Is there a desired async backend for sensors (current backends are sync)?

End of instructions.

Code style, typing and linting
- This repo includes static-check configs: `mypy.ini` and `pyrightconfig.json`. Respect the project's typing and strictness when changing public APIs.
- Tests and pytest settings are configured via `pytest.ini`.
- Recommended quick commands (run inside a Python virtualenv):

```bash
# create and activate venv (macOS / zsh)
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# run tests
pytest -q

# run mypy (uses mypy.ini)
mypy .

# run pyright (if installed globally or via npm)
npx pyright --project pyrightconfig.json
```

Notes
- If you add or change public Pydantic response models, update tests under `tests/unit/` that assert shapes (see `tests/unit/equipment/test_to_response.py`).
- Keep default Dummy backends intact for tests — add integration tests for any real-backend code in a separate `tests/features/` example or mark with an env var.

Quick example: add a soil backend and unit test

When adding a real sensor integration, implement the backend ABC and write a small unit test that uses the monitor with the new backend (or the provided Dummy backend). Keep the API-layer shapes unchanged.

Example backend (place under `afs_fastapi/monitoring/backends/my_soil_backend.py`):

```python
from typing import Dict
from afs_fastapi.monitoring.interfaces import SoilSensorBackend


class MySoilBackend(SoilSensorBackend):
  def read(self, sensor_id: str) -> Dict[str, float]:
    # call hardware driver or gateway here and return numeric metrics
    return {"ph": 6.8, "moisture": 0.42, "nitrogen": 1.1}

```

Minimal pytest (example file: `tests/unit/monitoring/test_my_soil_backend.py`):

```python
from afs_fastapi.monitoring.soil_monitor import SoilMonitor
from afs_fastapi.monitoring.backends.my_soil_backend import MySoilBackend


def test_my_soil_backend_read():
  backend = MySoilBackend()
  monitor = SoilMonitor("SENSOR1", backend=backend)
  readings = monitor.get_soil_composition()
  assert isinstance(readings, dict)
  assert "ph" in readings
  assert readings["ph"] > 0

```

Notes on tests:
- Prefer testing the monitor wrapper (e.g., `SoilMonitor`) with either Dummy or real backend mocks; avoid trying to run hardware in CI.
- Keep tests fast and deterministic; use small, local fixtures or mocking for network/gateway calls.

