# PERMANENT AGENT INSTRUCTIONS - READ BEFORE EVERY RESPONSE

This file contains mandatory instructions that apply to ALL Claude agents in ALL sessions, including after /clear commands.

## 🏗️ CRITICAL MONOREPO STRUCTURE AWARENESS

**THIS IS A MONOREPO WITH 3 RELATED PACKAGES - ALL AGENTS MUST KNOW THIS:**

1. **lib_package** - `todowrite` library (core Python library with SQLAlchemy 2 models, database, storage, core functionality)
2. **cli_package** - `todowrite_cli` (CLI interface for the todowrite library)
3. **web_package** - `todowrite_web` (FastAPI web app frontend for the library - NOT implemented yet)

**PACKAGE DIRECTORIES - NEVER FORGET THESE EXACT PATHS:**
- `lib_package/` - Main todowrite library
- `cli_package/` - CLI interface for todowrite
- `web_package/` - FastAPI web interface for todowrite

**TODOWRITE LIBRARY - 12 CRITICAL LAYERS - NEVER FORGET THEIR NAMES:**
1. **Goal** - High-level project objectives
2. **Concept** - Abstract ideas and approaches
3. **Context** - Environmental constraints and background
4. **Constraints** - Specific limitations and requirements
5. **Requirements** - Formal specifications
6. **AcceptanceCriteria** - Definition of done conditions
7. **InterfaceContract** - API and interface definitions
8. **Phase** - Major project phases
9. **Step** - Sequential work steps
10. **Task** - Individual work items
11. **SubTask** - Granular sub-components
12. **Command** - Executable actions

**SQLALCHEMY 2 MODELS LOCATION:**
- Database models: `lib_package/src/todowrite/database/models.py`
- Uses SQLAlchemy 2 with DeclarativeBase
- Alembic migrations in project root (NOT in lib_package)
- Database storage: PostgreSQL → SQLite3 → YAML (fallback chain)

**CRITICAL REMINDER:**
- This is NOT separate projects - it's one monorepo with interconnected packages
- ALWAYS remember the 12 layer names and their hierarchy
- ALWAYS use the correct package directories: `lib_package/`, `cli_package/`, `web_package/`

## 🚨 ZERO TOLERANCE POLICIES

The following practices are FORBIDDEN and will result in immediate session termination:
- **ANY MOCKING FRAMEWORKS**: @patch, MagicMock, Mock, unittest.mock, ANY fakes/stubs/doubles
- Writing production code before tests
- Committing without running tests
- Bypassing pre-commit hooks
- Ignoring semantic scoping requirements
- Leaving test artifacts (tests_todowrite.db, commit-msgs.txt, etc.)
- Ignoring ruff S-mode security rules
- Ignoring bandit security findings
- Using anything other than REAL implementations
- **HARDCODED TMP FILES**: /tmp, "tmp", "temp", Path("tmp"), open("tmp"), mkdir("tmp"), etc.
- **ANY HARDCODED TEMPORARY PATHS**: Use tempfile module ONLY
- **INVALID MIGRATIONS**: Multiple alembic heads, duplicate revision IDs, poor messages
- **PYTHON VERSION**: All packages must target py312 and require >=3.12

## 🎯 MANDATORY WORKFLOWS

### Before ANY Work (No Exceptions):
1. Check episodic memory for past context: `/.episodic-memory:search-conversations`
2. Verify semantic scoping understanding
3. Ensure todowrite_cli is available and working
4. Read this file to understand current requirements

### For ANY Code Change:
1. **RED PHASE**: Write failing test first, watch it fail for correct reason
2. **GREEN PHASE**: Write minimal code to make test pass
3. **REFACTOR PHASE**: Clean up code while keeping tests green

### Before ANY Commit:
1. Run all quality checks: `pre-commit run --all-files`
2. Validate commit message has proper semantic scope
3. Ensure all tests pass
4. Verify NO test artifacts remain: `python .hooks/test-cleanup-enforcer.py --check`
5. Confirm ZERO mocking used: `find . -name '*.py' -exec grep -l 'mock\\|Mock\\|patch\\|MagicMock' {} \\;`
6. Check ruff security mode: `ruff check . --select=S`
7. Verify bandit security: `bandit -r .`
8. Check no hardcoded tmp: `python .hooks/tmp-file-enforcer.py --check`
9. Verify alembic migrations: `python .hooks/alembic-enforcer.py --check`
10. Check Python version: `grep -r 'target-version.*py312' *.toml && grep -r 'requires-python.*>=3\.12' *.toml`

## 🔧 ENFORCED TOOLS

The following tools are MANDATORY and automatically enforced:
- **Semantic Scoping**: Project-specific commit scopes (lib, cli, web, tests, docs, build, config, ci, deps)
- **Red-Green-Refactor**: TDD methodology enforcement
- **Ruff**: Linting, formatting, import sorting, security analysis
- **Bandit**: Security vulnerability scanning
- **Detect-Secrets**: Secret scanning for API keys, passwords, tokens
- **SQLFluff**: SQL linting and formatting
- **Token Optimization**: Code efficiency analysis
- **Hardcoded Tmp Prevention**: Zero hardcoded temporary files
- **Alembic Enforcement**: Migration best practices enforced
- **Python Version**: py312 target and >=3.12 requirement enforced
- **Pre-commit Hooks**: All quality checks before commits

## 📋 QUALITY GATES

The following quality gates have ZERO TOLERANCE:
- Semantic scope violations
- Commit message format errors
- Security vulnerabilities
- Secret detection failures
- Syntax errors
- Pre-commit hook failures

## ⚠️ CONSEQUENCES

Failure to follow these mandatory instructions will result in:
- Immediate session failure
- Rejection of all code changes
- Requirement to restart with proper workflow
- Potential blocking of future work until compliance

## ✅ VERIFICATION

Before proceeding with any work, verify compliance by running:
```bash
# Check enforcement is active
test -f .claude/permanent_code_quality_enforcement.json

# Validate tools are working
python .hooks/token-optimizer.py --help
python .hooks/semantic-scope-validator.py --help
python .hooks/red-green-refactor-enforcer.py --help

# Run quality checks
pre-commit run --all-files
```

## 🔄 PERSISTENCE

This enforcement system persists across:
- Session resets (/clear)
- Claude restarts
- Agent changes
- Context switches

These instructions CANNOT be disabled or bypassed by any agent or user command.
