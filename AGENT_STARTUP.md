# Agent Startup Configuration for ToDoWrite Development

This document provides **essential startup information** for all AI agents working on the ToDoWrite codebase. It defines the exact tooling, workflows, and configurations that must be used.

## 🎯 MANDATORY STARTUP CHECKLIST

All agents **must complete this checklist** before beginning any work:

- [ ] **Environment**: UV workspace is active and recognized
- [ ] **Code Quality**: Ruff configured for formatting, linting, and security (S mode)
- [ ] **Security**: Bandit available for deep security scans
- [ ] **Build System**: Using `./dev_tools/build.sh` commands (not direct tools)
- [ ] **Testing**: pytest configured with `--ignore=tests/web/`
- [ ] **No Mocking**: STRICT no-mocking policy understood and followed

## 🛠️ TOOLING CONFIGURATION

### Environment Manager: UV
**REQUIRED**: All operations must use UV, NOT virtualenv+pip

```bash
# Check UV is active
uv --version
uv sync --group dev  # Install dependencies
```

**UV Features Enabled**:
- Workspace dependency management
- Isolated build environments
- Package building via `uv run python -m build`
- Development tool execution via `uv run`

### Code Quality: Ruff (Primary)
**REQUIRED**: Ruff for ALL formatting, linting, and S-mode security

```bash
# Format code (NOT black, not autopep8)
uv run ruff format lib_package/ cli_package/

# Lint code (NOT flake8, not pylint directly)
uv run ruff check lib_package/ cli_package/

# Security checks (S mode enabled in Ruff)
uv run ruff check lib_package/ cli_package/ --select=S
```

**Ruff Configuration** (pyproject.toml):
- Line length: 100 characters
- Security rules (S) enabled for basic security
- Comprehensive rule set for code quality

### Security: Bandit (Deep Security)
**REQUIRED**: Bandit for additional security analysis

```bash
# Deep security scanning
uv run bandit -r lib_package/ cli_package/ -f json -q
```

### Testing: pytest
**REQUIRED**: pytest with specific exclusions

```bash
# Run tests (web_package excluded)
uv run pytest tests/ --ignore=tests/web/

# With coverage
uv run pytest tests/ --cov=lib_package/src --cov=cli_package/src --ignore=tests/web/
```

## 🚀 BUILD SYSTEM COMMANDS

**PRIMARY RULE**: ALWAYS use build script commands, NEVER direct tool calls

### Daily Development Workflow
```bash
# Complete development workflow
./dev_tools/build.sh dev        # install + format + lint + test

# Individual operations
./dev_tools/build.sh install    # Install/update dependencies
./dev_tools/build.sh format     # Format code (uses ruff)
./dev_tools/build.sh lint       # Lint code (uses ruff)
./dev_tools/build.sh test       # Run tests (uses pytest)
./dev_tools/build.sh audit      # Security scan (uses bandit + safety)
./dev_tools/build.sh validate   # Validate build system
```

### Quality Gates
```bash
# Quality gate with coverage threshold
./dev_tools/build.sh quality-gate --coverage-threshold 80

# Strict mode (fails on any warnings)
./dev_tools/build.sh quality-gate --strict
```

## 📋 ESSENTENTIAL FILE LOCATIONS

### Configuration Files
- **`pyproject.toml`**: UV workspace, Ruff, Bandit configuration
- **`VERSION`**: Central version management
- **`.claude/CLAUDE.md`**: Project rules and mandates

### Build System Files
- **`dev_tools/build.sh`**: PRIMARY build interface (use this!)
- **`lib_package/src/todowrite/build_system.py`**: Library API for applications
- **`dev_tools/build_system.py`**: Development tool API

### Package Structure
```
todowrite/
├── lib_package/     # Core library (todowrite) - PRODUCTION READY
├── cli_package/     # CLI interface (todowrite_cli) - PRODUCTION READY
├── web_package/     # Web application - PLANNING STAGE (excluded from tools)
└── tests/           # Test suites (NO MOCKING ALLOWED)
```

## 🔧 AGENT WORKFLOWS

### Before Starting Work
1. **Verify UV environment**:
   ```bash
   uv sync --group dev
   uv tree  # Verify dependencies
   ```

2. **Run validation**:
   ```bash
   ./dev_tools/build.sh validate
   ```

3. **Check code quality**:
   ```bash
   ./dev_tools/build.sh lint
   ./dev_tools/build.sh format
   ```

### During Development
1. **Use build scripts ONLY**:
   ```bash
   # ❌ WRONG: Direct tool calls
   ruff format .
   pytest tests/

   # ✅ CORRECT: Build script commands
   ./dev_tools/build.sh format
   ./dev_tools/build.sh test
   ```

2. **Security scanning**:
   ```bash
   ./dev_tools/build.sh audit  # Includes both ruff S-mode and bandit
   ```

### Before Committing
1. **Run complete workflow**:
   ```bash
   ./dev_tools/build.sh dev  # Complete development workflow
   ```

2. **Quality gate validation**:
   ```bash
   ./dev_tools/build.sh quality-gate --strict
   ```

## 🚨 CRITICAL RULES

### NO MOCKING POLICY
**ABSOLUTELY FORBIDDEN**: No mocking, stubs, fakes, or test doubles
- ❌ `@patch`, `MagicMock`, `Mock`, `mock_open`
- ❌ Test doubles or dependency injection of fakes
- ✅ Real implementations with actual system resources
- ✅ Temporary directories and files for testing
- ✅ Real subprocess calls and API interactions

### TDD REQUIREMENT
**MANDATORY**: All code must follow RED → GREEN → REFACTOR
1. **RED**: Write failing test first
2. **GREEN**: Implement minimal code to pass
3. **REFACTOR**: Clean up with tests still passing

### EXCLUSIONS
**web_package is in PLANNING STAGE**:
- Excluded from testing: `--ignore=tests/web/`
- Excluded from linting and formatting
- Build scripts handle this automatically

## 🎛️ TOOLING SPECIFICATIONS

### UV Configuration
```toml
[tool.uv.workspace]
members = ["lib_package", "cli_package", "web_package"]

[tool.uv.sources]
todowrite = { workspace = true }
```

### Ruff Configuration
```toml
[tool.ruff]
line-length = 100
select = ["E", "W", "F", "I", "B", "C4", "UP", "RUF", "S", ...]  # Comprehensive rules

[tool.ruff.format]
quote-style = "double"
indent-style = "space"
```

### Bandit Configuration
```toml
[tool.bandit]
exclude_dirs = [".git", "htmlcov", ".ruff_cache"]
skips = ["B101", "B601"]  # Example skip rules
```

## 📞 GETTING HELP

### Build Script Help
```bash
./dev_tools/build.sh help      # Shows all available commands
./dev_tools/deploy.sh help     # Deployment commands
```

### Environment Status
```bash
uv tree                        # Show dependency tree
./dev_tools/build.sh validate  # Validate build system
```

### Troubleshooting
```bash
# Clean and reinstall
./dev_tools/build.sh clean
./dev_tools/build.sh install

# Check specific package issues
./dev_tools/build.sh build lib
./dev_tools/build.sh validate
```

## ⚡ QUICK START COMMANDS

For agents who need to get started immediately:

```bash
# 1. Setup environment
./dev_tools/build.sh install

# 2. Validate everything works
./dev_tools/build.sh validate

# 3. Run complete development workflow
./dev_tools/build.sh dev

# 4. Check quality gates
./dev_tools/build.sh quality-gate
```

**Remember**: Always use build script commands, never direct tool calls. The build system is optimized and configured for this specific project structure.
