Contributing Guide
==================

Thanks for considering a contribution! This guide keeps changes predictable and safe.

Quick Verification Checklist
----------------------------

Before opening a PR, please run through this short list:

1. Code quality
   - Run linters: `flake8 afs_fastapi` and `black --check .`
   - Type-check: `mypy --config-file mypy.ini` (or `pyright` if preferred)
2. Tests
   - Run tests locally: `pytest -q`
   - Add tests for new behavior or edge cases
3. API and docs
   - If you change API shapes, update Pydantic response models and endpoint `response_model`
   - Update `README.md`; do NOT hand-edit `docs/index.html` (it is generated)
   - CI will regenerate docs via `.github/workflows/docs-sync.yml`
4. Versioning and changelog
   - Bump `afs_fastapi/version.py` if the change merits a release
   - Add a brief entry to `CHANGELOG.md`
5. Runtime sanity
   - Start the API: `python -m afs_fastapi` (or `afs-api`)
   - Exercise endpoints (e.g., with `httpie` or `curl`)

Development Notes
-----------------

- Domain vs transport: keep core logic in plain classes; use Pydantic models at API boundaries.
- Sensor backends: implement `read(sensor_id)` in a backend and pass it to monitors; avoid coupling monitors to specific vendors.
- Python compatibility: target Python 3.10+.

Thank you for helping improve AFS FastAPI!
