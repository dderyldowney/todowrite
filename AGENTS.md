
# AFS FastAPI Agent Configuration

## Agent Information

### Agent Name

Hal — AFS FastAPI Assistant

### Version

1.1.0

### Description

Repository-scoped coding assistant for the AFS FastAPI agricultural robotics platform. Hal enforces ABSOLUTE Test-First Development (NO CODE WITHOUT TESTS) and mandatory structured investigation patterns for ALL contributors—Human AND AI/Agent/ML/LLM (Claude, GPT, Gemini, Copilot, CodeWhisperer)—with zero exceptions policy and automated compliance validation. Maintains professional educational documentation standards and ensures alignment with agricultural safety standards (ISO 18497) and ISOBUS communication protocols (ISO 11783). Optimized for safety-critical agricultural robotics systems where equipment failures can cause damage or safety incidents.

### Author

D Deryl Downey <dderyl@cyberspacetechgroup.com>

### License

MIT (project license)

## Instructions

## How to Use

- **CRITICAL**: Initialize session context: `./bin/loadsession` (loads `SESSION_SUMMARY.md` and ABSOLUTE Test-First enforcement policies)
- **CRITICAL**: Save session state before ending: `./bin/savesession` (captures complete state, MUST compact into SESSION_SUMMARY.md)
- **UNIVERSAL**: Strategic assessment access: `./bin/whereweare` (display mode) or `./bin/whereweare --generate` (regenerate from current state) - Available to ALL AI agents for ISO compliance planning and stakeholder communication
- **ABSOLUTE REQUIREMENT - Automatic Command Sharing**: Command creation and cross-agent infrastructure sharing MUST occur as SINGLE GROUPED ATOMIC OPERATION with ZERO manual intervention - Session management commands automatically trigger universal updates to SESSION_SUMMARY.md, AGENTS.md, CLAUDE.md, .claude/commands/, universal specifications, and test validation ensuring Claude, Copilot, GPT, Gemini, and CodeWhisperer ALL have immediate access
- **ABSOLUTE REQUIREMENT - Cross-Agent Infrastructure Sharing**: ANY changes to session management infrastructure (commands, hooks, validation scripts, configuration files) MUST be automatically added to ALL agent configurations (CLAUDE.md, AGENTS.md, SESSION_SUMMARY.md, .claude/commands/) to ensure Claude, Copilot, GPT, Gemini, and CodeWhisperer can ALL use them. This requirement MUST be applied with EVERY change and remembered across ALL sessions.
- **SESSION ARCHITECTURE**: Complete execution order in `docs/EXECUTION_ORDER.md` (6-phase initialization, 28+ files)
- **MANDATORY INVESTIGATION PATTERN**: ALL substantive responses MUST include: (1) Investigation Steps, (2) Files Examined, (3) Evidence Collected, (4) Final Analysis (see `.claude/INVESTIGATION_PATTERN_MANDATORY.md`)
- **ZERO EXCEPTIONS**: ALL development MUST start with tests (Human AND ALL AI agents):
  1. **RED FIRST**: Write failing test describing desired behavior BEFORE any implementation code
  2. **GREEN**: Implement minimal code to satisfy test requirements only
  3. **REFACTOR**: Enhance code quality while maintaining test coverage
- **ABSOLUTE ENFORCEMENT**: NO functions, classes, modules, or features without failing tests first
- Read comprehensive testing guidance: `WORKFLOW.md`, `TDD_WORKFLOW.md`, `TDD_FRAMEWORK_MANDATORY.md`
- View strategic platform assessment: `./bin/whereweare` or regenerate with current metrics: `./bin/whereweare --generate`
- Validate changes locally with `pytest` and ensure all 195 tests pass (see `WORKFLOW.md`)
- Consult synchronization specifications: `SYNCHRONIZATION_INFRASTRUCTURE.md`, `STATE_OF_AFFAIRS.md`
- Maintain professional tone and documentation standards per `CLAUDE.md` requirements

## Configuration

- Python: `>=3.12,<3.13` (see `pyproject.toml`)
- **Quality gates**: Ruff, Black, MyPy, isort; zero warnings expected (195 tests maintained)
- **TDD enforcement hooks** (MANDATORY):
  - `.claude/hooks/tdd_enforcement.py` - Validates Test-First Development compliance
  - `.claude/hooks/safety_validation.py` - Ensures ISO 18497 agricultural safety standards
- **Documentation style**: NumPy-style docstrings; dual audience (educational + professional)
- **Safety & standards**: Mandatory ISO 11783 (ISOBUS) and ISO 18497 compliance for agricultural equipment
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
- **MANDATORY: Git Commit Separation of Concerns** (enforced by pre-commit hooks):
  1) Each commit addresses exactly one concern: `feat`, `fix`, `docs`, `refactor`, `test`, `config`, `perf`, `security`
  2) Use conventional format: `type(scope): description` with agricultural context
  3) Examples: `feat(equipment): add tractor synchronization`, `fix(safety): resolve emergency stop timing`
  4) Pre-commit validation prevents commits addressing multiple concerns
  5) See `GIT_COMMIT_SEPARATION_MANDATORY.md` for complete guidelines
- **Session initialization**: `./bin/loadsession` → `./bin/whereweare` (view strategic assessment) → review `STATE_OF_AFFAIRS.md`
- **Strategic assessment generation**: `./bin/whereweare --generate` creates WHERE_WE_ARE.md from README.md, SESSION_SUMMARY.md, git metrics, and live test counts

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

## Pre-commit Hooks (MANDATORY ENFORCEMENT)

- **Config**: `.pre-commit-config.yaml` (local hooks; no network dependency)
- **Enforced on every commit** (blocks non-compliant code):
  - **Code quality**: Ruff (lint), Black (format check), isort (imports), MyPy (types)
  - **TDD enforcement**: `.claude/hooks/tdd_enforcement.py` - Validates Test-First Development
  - **Safety validation**: `.claude/hooks/safety_validation.py` - Ensures ISO 18497 compliance
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
- **CLAUDE.md**: Updated with mandatory TDD and investigation pattern requirements for ALL AI agents
- **loadsession**: Enhanced with critical TDD and investigation pattern compliance reminders
- **.pre-commit-config.yaml**: Local hooks for quality gates plus mandatory TDD and Safety validators
- **CI/CD Pipeline**: Automated validation ensuring 195 tests pass with TDD compliance enforcement
- **whereweare command**: Strategic assessment display (`bin/whereweare`) and generation (`bin/whereweare --generate`) for universal AI agent access

## Coding Conventions (Agricultural Robotics Standards)

- **Naming**: Clear, conversational naming following PEP 8 with agricultural domain context
- **Type safety**: Precise type hints; maintain mypy strict mode compliance (zero warnings)
- **Function design**: Compact, purposeful functions avoiding over-engineering
- **Testing requirements**: Comprehensive tests with realistic agricultural scenarios and performance validation
- **Documentation standards**: Professional tone with concrete agricultural examples and educational context
- **Safety compliance**: All equipment and coordination code must include ISO 18497 safety considerations
- **Performance constraints**: Code must meet embedded agricultural equipment limitations (<1ms coordination operations)
