Changelog
=========

All notable changes to this project will be documented in this file.

[0.1.2] - 2025-09-27
--------------------

### Code Quality and Type Safety Improvements

This release focuses on comprehensive modernization of the codebase to meet enterprise-grade quality standards while maintaining full functionality of the robotic agriculture platform.

#### Changed

**Modern Python Standards:**
- Modernized type hints: `Dict` → `dict`, `List` → `list`, `Tuple` → `tuple`
- Updated union syntax: `Optional[T]` → `T | None`
- Organized and sorted import statements according to Python standards
- Applied consistent code formatting with Black across entire codebase

**Code Quality Enhancements:**
- Fixed 56 Ruff linting errors including import organization and type modernization
- Achieved zero linting warnings across all quality tools (Ruff, Flake8, MyPy)
- Removed duplicate method definitions and unused variables
- Ensured PEP 8 compliance throughout the project

**Type Safety Improvements:**
- Fixed type annotation compatibility in emergency stop logging system
- Updated logging to use numeric event codes (999.0 = emergency_stop) for type safety
- Ensured complete type safety across all 17 source files
- Maintained compatibility with `dict[str, float]` interface requirements

#### Fixed

- Resolved duplicate `emergency_stop` method definition (kept ISO 18497 compliant version)
- Fixed unused variables and loop variables in test files
- Corrected type annotation issues in data logging systems
- Updated emergency response integration test for new event logging format

#### Technical Highlights

- **Complete Test Coverage**: All 118 tests passing with comprehensive validation
- **Enterprise Quality**: Ruff, Black, Flake8, and MyPy all passing with zero issues
- **Robotic Agriculture Integrity**: All ISOBUS, Safety, Motor Control interfaces validated
- **Professional Standards**: Maintained ISO 11783 and ISO 18497 compliance
- **API Functionality**: Confirmed serialization and endpoint consumption work correctly

[0.1.0] - 2025-09-11
--------------------

- Added Pydantic response models for API endpoints:
  - `FarmTractorResponse` for tractor state
  - `SoilReadingResponse` and `WaterQualityResponse` for monitoring endpoints
- Introduced pluggable sensor backend interfaces with dummy defaults:
  - `SoilSensorBackend`, `WaterSensorBackend` and their dummy implementations
- Added module entrypoint and console script to run the API:
  - `python -m afs_fastapi` and `afs-api`
- Centralized version in `afs_fastapi/version.py` and aligned `/version` endpoint
- Enhanced OpenAPI metadata with tags, summaries, and `response_model_exclude_none`
- Updated README and generated docs with run instructions and backend usage
- Added GitHub Actions workflow to sync `docs/index.html` from `README.md`
- Bumped supported Python to `>=3.10,<3.13` and updated CI to `actions/setup-python@v5`

[0.1.2]: https://github.com/dderyldowney/afs_fastapi/releases/tag/0.1.2
[0.1.0]: https://github.com/dderyldowney/afs_fastapi/releases/tag/0.1.0
