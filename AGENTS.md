
# AFS FastAPI Agent Configuration

## Agent Information

### Agent Name

Hal — AFS FastAPI Assistant

### Version

1.1.0

### Description

Repository-scoped coding assistant for the AFS FastAPI agricultural robotics platform. Hal enforces mandatory Test-Driven Development (Red→Green→Refactor) methodology with automated compliance validation, maintains professional educational documentation standards, and ensures alignment with agricultural safety standards (ISO 18497) and ISOBUS communication protocols (ISO 11783). Optimized for intermediate Python developers working in safety-critical agricultural robotics systems.

### Author

D Deryl Downey <dderyl@cyberspacetechgroup.com>

### License

MIT (project license)

## Instructions

## How to Use

- **CRITICAL**: Initialize session context: `./loadsession` (loads `SESSION_SUMMARY.md` and mandatory TDD enforcement policies)
- **MANDATORY**: Follow TDD methodology strictly (enforced by pre-commit hooks):
  1. **RED**: Write failing test first describing agricultural robotics behavior
  2. **GREEN**: Implement minimal code to satisfy test requirements
  3. **REFACTOR**: Enhance code quality while maintaining test coverage
- Read comprehensive testing guidance: `WORKFLOW.md`, `TDD_WORKFLOW.md`, `TDD_FRAMEWORK_MANDATORY.md`
- Validate changes locally with `pytest` and ensure all 129 tests pass (see `WORKFLOW.md`)
- Consult synchronization specifications: `SYNCHRONIZATION_INFRASTRUCTURE.md`, `STATE_OF_AFFAIRS.md`
- Maintain professional tone and documentation standards per `CLAUDE.md` requirements

## Configuration

- Python: `>=3.12,<3.13` (see `pyproject.toml`)
- **Quality gates**: Ruff, Black, MyPy, isort; zero warnings expected (129 tests maintained)
- **TDD enforcement hooks** (MANDATORY):
  - `.claude/hooks/tdd_enforcement.py` - Validates Test-First Development compliance
  - `.claude/hooks/safety_validation.py` - Ensures ISO 18497 agricultural safety standards
- **Documentation style**: NumPy-style docstrings; dual audience (educational + professional)
- **Safety & standards**: Mandatory ISO 11783 (ISOBUS) and ISO 18497 compliance for agricultural equipment
- **Performance requirements**: Sub-millisecond coordination operations for embedded agricultural systems

## Dependencies

- Runtime: `fastapi`, `uvicorn[standard]`, `starlette`, `pydantic`
- Dev/Test: `pytest`, `pytest-asyncio`, `httpx`, `mypy`, `ruff`, `black`, `isort`
- See `pyproject.toml` for pinned versions and scripts

## Examples

- **Mandatory TDD workflow** (enforced by pre-commit hooks):
  1) **RED**: Create/extend test in `tests/` that fails, including agricultural context
  2) Run `pytest` to confirm RED phase - test must fail initially
  3) **GREEN**: Implement minimal code in `afs_fastapi/` to satisfy test requirements
  4) Run `pytest` to confirm GREEN phase - test now passes
  5) **REFACTOR**: Enhance code quality while maintaining test coverage
  6) Ensure all quality gates pass: `ruff`, `black`, `mypy`, `isort` (zero warnings)
  7) Pre-commit hooks validate TDD compliance and agricultural safety standards
- **Session initialization**: `./loadsession` → review `WHERE_WE_ARE.md` → check `STATE_OF_AFFAIRS.md`

## VS Code & CLI Workflows

- VS Code tasks (suggested):
  - Run API: command `python -m afs_fastapi` (uses env vars below)
  - Run tests: command `pytest -q`
  - Linters/formatters: `ruff check . && black --check . && mypy .`
- Environment variables for running the API:
  - `AFS_API_HOST` (default `127.0.0.1`)
  - `AFS_API_PORT` (default `8000`)
  - `AFS_API_RELOAD` (`true/false`, default `false`)
  - `AFS_API_LOG_LEVEL` (`debug|info|warning|error`, default `info`)
- Handy CLI snippets:
  - Start API quickly: `AFS_API_RELOAD=1 python -m afs_fastapi`
  - Exercise OpenAPI docs: open `http://127.0.0.1:8000/docs`
  - Run focused tests: `pytest -q tests/services/test_*.py -k fleet`
  - Type-check changed files: `git diff --name-only HEAD~1 | rg ".py$" | xargs -r mypy`
  - Lint and format: `ruff check . && black . && isort .`
  - Pre-commit: `make precommit-install` then `make precommit-run`
  - Pytest config now in `pytest.ini` (kept minimal; mirrors previous pyproject settings)

## Recommended VS Code Settings (optional)

- Python interpreter: use `.venv` if present; otherwise configure 3.12
- Enable "Format on Save" with Black; run Ruff as a linter
- Pylance/Pyright strict mode to mirror `pyproject.toml`
- Set test discovery to `pytest` with `tests` as root

## Pre-commit Hooks (MANDATORY TDD ENFORCEMENT)

- **Config**: `.pre-commit-config.yaml` (local hooks; no network dependency)
- **Enforced on every commit** (blocks non-compliant code):
  - **Code quality**: Ruff (lint), Black (format check), isort (imports), MyPy (types)
  - **TDD enforcement**: `.claude/hooks/tdd_enforcement.py` - Validates Test-First Development
  - **Safety validation**: `.claude/hooks/safety_validation.py` - Ensures ISO 18497 compliance
- **Installation**: `make precommit-install` (installs pre-commit and registers hooks)
- **Manual execution**: `make precommit-run` (run all hooks without committing)
- **Status**: ACTIVE and ENFORCED - prevents non-TDD code from entering codebase

## Recent TDD Enforcement Implementation

- **TDD_FRAMEWORK_MANDATORY.md**: Comprehensive mandatory TDD policy (319 lines) with enforcement mechanisms
- **TDD_IMPLEMENTATION_RATIONALE.md**: Detailed justification (335 lines) for agricultural robotics TDD requirements
- **STATE_OF_AFFAIRS.md**: Current platform status documentation (393 lines) with strategic analysis
- **.claude/hooks/**: TDD enforcement (239 lines) and safety validation (296 lines) pre-commit hooks
- **SESSION_SUMMARY.md**: Enhanced with prominent TDD enforcement policies and visual warnings
- **CLAUDE.md**: Updated with mandatory TDD requirements for AI code generation
- **loadsession**: Enhanced with critical TDD compliance reminders for all future sessions
- **.pre-commit-config.yaml**: Local hooks for quality gates plus mandatory TDD and Safety validators
- **CI/CD Pipeline**: Automated validation ensuring 129 tests pass with TDD compliance enforcement

## Coding Conventions (Agricultural Robotics Standards)

- **Naming**: Clear, conversational naming following PEP 8 with agricultural domain context
- **Type safety**: Precise type hints; maintain mypy strict mode compliance (zero warnings)
- **Function design**: Compact, purposeful functions avoiding over-engineering
- **Testing requirements**: Comprehensive tests with realistic agricultural scenarios and performance validation
- **Documentation standards**: Professional tone with concrete agricultural examples and educational context
- **Safety compliance**: All equipment and coordination code must include ISO 18497 safety considerations
- **Performance constraints**: Code must meet embedded agricultural equipment limitations (<1ms coordination operations)
