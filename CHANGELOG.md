Changelog
=========

All notable changes to this project will be documented in this file.

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

[0.1.0]: https://github.com/dderyldowney/afs_fastapi/releases/tag/0.1.0
