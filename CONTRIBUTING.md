Contributing Guide
==================

Thanks for considering a contribution! This guide keeps changes predictable and safe.

Quick Verification Checklist
----------------------------

Before opening a PR, please run through this short list:

1. Code quality
   - Run linters: `ruff check .` and `black --check .`
   - Type-check: `mypy .` (or `pyright` if preferred)
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
- Python compatibility: target Python 3.12+ (as specified in pyproject.toml).

Version Management and Tagging Strategy
---------------------------------------

**🚨 CRITICAL: All contributors MUST follow this tagging strategy**

### Branch and Tagging Rules

This project uses **Git Flow** with strict tagging conventions:

#### Branches
- **`main`** - Stable releases only (production-ready)
- **`develop`** - Active development (all new work goes here)
- **Feature branches** - Branch from `develop`, merge back to `develop`

#### Tag Types and Rules

**1. Release Tags (Stable Production)**
- **Format**: `v{major}.{minor}.{patch}` (e.g., `v0.1.1`, `v0.1.2`)
- **Branch**: Only created on `main` branch
- **When**: After merging `develop` → `main` for stable releases
- **Who**: Only maintainers create release tags

**2. Alpha Tags (Development)**
- **Format**: `v{major}.{minor}.{patch}a{n}` (e.g., `v0.1.2a0`, `v0.1.2a1`)
- **Branch**: Only created on `develop` branch
- **When**: After significant development milestones
- **Sequence**: Must be sequential (a0 → a1 → a2, no gaps)

#### Version File Requirements

Before creating any tag, these files MUST be synchronized:
- `afs_fastapi/version.py` - Contains `__version__ = "0.1.2"`
- `pyproject.toml` - Contains `version = "0.1.2"`

**Version format**: Without 'v' prefix (tag: `v0.1.2`, files: `0.1.2`)

#### Contributor Guidelines

**✅ Contributors CAN:**
- Work on feature branches from `develop`
- Update version files in PRs that warrant a version bump
- Request alpha tags for significant milestones

**❌ Contributors MUST NOT:**
- Create any tags directly (maintainers only)
- Work directly on `main` branch
- Create release tags on `develop` branch
- Create alpha tags on `main` branch
- Skip version numbers or create gaps in alpha sequences

#### Tag Creation Examples (Maintainers Only)

```bash
# Alpha release on develop branch
git checkout develop
git tag -a v0.1.2a1 -m "Alpha release v0.1.2a1 - Added new monitoring features"
git push origin v0.1.2a1

# Stable release on main branch (after merging develop)
git checkout main
git merge develop
git tag -a v0.1.2 -m "Release v0.1.2 - Enhanced monitoring and bug fixes"
git push origin main
git push origin v0.1.2
```

#### Current Version Status

- **Latest Stable**: `v0.1.1` (on `main` branch)
- **Current Development**: `v0.1.2a0` (on `develop` branch)
- **Next Alpha**: `v0.1.2a1` (when ready)

#### For Pull Requests

When submitting PRs:

1. **Target `develop` branch** (not `main`)
2. **Update version files** if your changes warrant a version bump:
   ```python
   # afs_fastapi/version.py
   __version__ = "0.1.2"  # Remove 'a0' when ready for next release
   ```
   ```toml
   # pyproject.toml
   version = "0.1.2"
   ```
3. **Update CHANGELOG.md** with your changes
4. **Let maintainers handle tagging** - don't create tags yourself

#### Enforcement

- GitHub Actions will validate version consistency
- PRs with incorrect version formats will be rejected
- Maintainers will create appropriate tags after PR merges
- Questions? Check `.claude/project-context.md` for full strategy details

Thank you for helping improve AFS FastAPI!
