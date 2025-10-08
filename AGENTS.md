
# AFS FastAPI Agent Configuration

## Agent Information

### Agent Name

Hal — AFS FastAPI Assistant

### Version

1.1.0

### Description

Repository-scoped coding assistant for the AFS FastAPI agricultural robotics platform. Hal enforces strict Test-First Development (no code without tests) and mandatory structured investigation patterns for all contributors—human and all AI agents—with zero exceptions policy and automated compliance validation. Maintains professional educational documentation standards and ensures alignment with agricultural safety standards (see [SESSION_SUMMARY.md - Agricultural Robotics Context](SESSION_SUMMARY.md#agricultural-robotics-context)). Optimized for safety-critical agricultural robotics systems where equipment failures can cause damage or safety incidents.

### Author

D Deryl Downey <dderyl@cyberspacetechgroup.com>

### License

MIT (project license)

## Instructions

## How to Use

**Universal Session Management Commands**: All AI agents have access to 7 session management commands (loadsession, savesession, runtests, whereweare, updatedocs, updatechangelog, updatewebdocs).

**Complete command specifications**: See [SESSION_SUMMARY.md - Universal Session Management Commands](SESSION_SUMMARY.md#universal-session-management-commands) for usage, functionality, and references.

**Critical commands**:
- Initialize sessions: `./bin/loadsession` (execute after starting new sessions)
- End sessions: `./bin/savesession` (capture state before ending)
- Strategic assessment: `./bin/whereweare` (display) or `./bin/whereweare --generate` (regenerate)

**Six Mandatory Requirements** (see [SESSION_SUMMARY.md](SESSION_SUMMARY.md#mandatory-requirements-for-all-ai-agents) for complete details):
- Test-First Development, Structured Investigation Pattern, Standardized Test Reporting, CHANGELOG Loop Protection, Git Commit Separation, Cross-Agent Infrastructure Sharing
- Strict Red-Green-Refactor (RGR) adherence: Green status must only be achieved through actual working implementation code; 'pass' is prohibited as a means to gain green status. No code is to be generated until a well-defined and detailed set of tests defining the expected behavior(s) have been generated and their logic verified.

**Essential documentation**:
- Session architecture: `docs/EXECUTION_ORDER.md` (6-phase initialization, 28+ files)
- Testing guidance: `WORKFLOW.md`, `TDD_WORKFLOW.md`, `TDD_FRAMEWORK_MANDATORY.md`
- Synchronization specs: `SYNCHRONIZATION_INFRASTRUCTURE.md`, `STATE_OF_AFFAIRS.md`
- Platform standards: `CLAUDE.md` (professional tone and documentation requirements)
- Test validation: Ensure all 214 tests pass (see `WORKFLOW.md`)

## Configuration

- Python: `>=3.12,<3.13` (see `pyproject.toml`)
- **Quality gates**: Ruff, Black, MyPy, isort; zero warnings expected (195 tests maintained)
- **TDD enforcement hooks** (required):
  - `.claude/hooks/tdd_enforcement.py` - Validates Test-First Development compliance
  - `.claude/hooks/safety_validation.py` - Ensures agricultural safety standards compliance
- **Documentation style**: NumPy-style docstrings; dual audience (educational + professional)
- **Safety & standards**: See [SESSION_SUMMARY.md - Agricultural Robotics Context](SESSION_SUMMARY.md#agricultural-robotics-context) for ISO compliance requirements
- **Performance requirements**: Sub-millisecond coordination operations for embedded agricultural systems

### Environment Sanity (pyenv)

- Verify pyenv before development:
  - `pyenv --version` prints a version with no errors
  - `pyenv rehash` runs clean (no “shims isn’t writable”)
- If shims warning appears: `chmod u+rwx ~/.pyenv/shims && pyenv rehash`.
- Keep zsh init in `~/.zshrc`; ensure `~/.bash_profile` is bash-safe, for example:
  - `export PYENV_ROOT="$HOME/.pyenv"`
  - `[[ -d $PYENV_ROOT/bin ]] && export PATH="$PYENV_ROOT/bin:$PATH"`
  - `eval "$(pyenv init -)"`
  - Optionally: `eval "$(pyenv virtualenv-init -)"` if plugin installed
- See the Quick Verification Checklist in `CONTRIBUTING.md` for the full procedure.

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
- **Git Commit Separation of Concerns** (enforced by pre-commit hooks):
  1) Each commit addresses exactly one concern: `feat`, `fix`, `docs`, `refactor`, `test`, `config`, `perf`, `security`
  2) Use conventional format: `type(scope): description` with agricultural context
  3) Examples: `feat(equipment): add tractor synchronization`, `fix(safety): resolve emergency stop timing`
  4) Pre-commit validation prevents commits addressing multiple concerns
  5) See `GIT_COMMIT_SEPARATION_MANDATORY.md` for complete guidelines
- **Session workflow**: `./bin/loadsession` → `./bin/whereweare` → review project state → develop → `./bin/savesession` (before ending)
- **Command details**: See [SESSION_SUMMARY.md - Universal Session Management Commands](SESSION_SUMMARY.md#universal-session-management-commands) for complete usage examples and functionality

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

## Pre-commit Hooks (Required Enforcement)

- **Config**: `.pre-commit-config.yaml` (local hooks; no network dependency)
- **Enforced on every commit** (blocks non-compliant code):
  - **Code quality**: Ruff (lint), Black (format check), isort (imports), MyPy (types)
  - **TDD enforcement**: `.claude/hooks/tdd_enforcement.py` - Validates Test-First Development
  - **Safety validation**: `.claude/hooks/safety_validation.py` - Ensures agricultural safety compliance
  - **Commit separation**: `.claude/hooks/commit_separation_enforcement.py` - Enforces single concern per commit
- **Installation**: `make precommit-install` (installs pre-commit and registers hooks)
- **Manual execution**: `make precommit-run` (run all hooks without committing)
- **Status**: ACTIVE and ENFORCED - prevents non-compliant code and commits from entering codebase

## Recent TDD Enforcement Implementation

- **INVESTIGATION_PATTERN_MANDATORY.md**: Universal AI agent investigation pattern requirement (374 lines) with enforcement
- **TDD_FRAMEWORK_MANDATORY.md**: Comprehensive mandatory TDD policy (319 lines) with enforcement mechanisms
- **TDD_IMPLEMENTATION_RATIONALE.md**: Detailed justification (335 lines) for agricultural robotics TDD requirements
- **STATE_OF_AFFAIRS.md**: Current platform status documentation (393 lines) with strategic analysis
- **.claude/hooks/**: Investigation pattern validator, TDD enforcement (239 lines), and safety validation (296 lines) pre-commit hooks
- **SESSION_SUMMARY.md**: Enhanced with investigation pattern and TDD enforcement policies
- **CLAUDE.md**: Updated with mandatory TDD and investigation pattern requirements for all AI agents
- **loadsession**: Enhanced with critical TDD and investigation pattern compliance reminders
- **.pre-commit-config.yaml**: Local hooks for quality gates plus mandatory TDD and Safety validators
- **CI/CD Pipeline**: Automated validation ensuring 195 tests pass with TDD compliance enforcement
- **whereweare command**: Strategic assessment display (`bin/whereweare`) and generation (`bin/whereweare --generate`) for universal AI agent access
- **updatedocs command**: Meta-command for unified documentation regeneration (`bin/updatedocs`) updating all 6 core documents with dry-run and selective update modes for universal AI agent access

## Coding Conventions (Agricultural Robotics Standards)

- **Naming**: Clear, conversational naming following PEP 8 with agricultural domain context
- **Type safety**: Precise type hints; maintain mypy strict mode compliance (zero warnings)
- **Function design**: Compact, purposeful functions avoiding over-engineering
- **Testing requirements**: Comprehensive tests with realistic agricultural scenarios and performance validation
- **Documentation standards**: Professional tone with concrete agricultural examples and educational context
- **Safety compliance**: All equipment and coordination code must include safety considerations (see [SESSION_SUMMARY.md - Agricultural Robotics Context](SESSION_SUMMARY.md#agricultural-robotics-context))
- **Performance constraints**: Code must meet embedded agricultural equipment limitations (<1ms coordination operations)
