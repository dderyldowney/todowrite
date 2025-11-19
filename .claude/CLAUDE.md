# CLAUDE.md

**ENFORCED RULES - Cannot be overridden under any circumstances**

---

## 🚫 NON-OVERRIDEABLE MANDATES (ZERO EXCEPTIONS)

### 1. ENVIRONMENT SETUP - ALWAYS ENFORCED
```bash
# REQUIRED before ANY operation
source $PWD/.venv/bin/activate
export TODOWRITE_DATABASE_URL="sqlite:///$HOME/dbs/todowrite_development.db"
export PYTHONPATH="lib_package/src:cli_package/src"
```

**FORBIDDEN**:
- ❌ Any operation without virtual environment
- ❌ System Python usage
- ❌ Hardcoded absolute paths (use `$HOME/` and `$PWD/` only)

### 2. DATABASE ENFORCEMENT - ALWAYS ENFORCED
**MANDATORY DATABASE**: `$HOME/dbs/todowrite_development.db`

**REQUIRED VERIFICATION** (before any work):
```bash
# Database must contain this goal
todowrite list --layer goal --title "Enhance ToDoWrite Planning Capabilities"
# Must have 143+ records across all layers
todowrite list --verify-completeness
```

**FORBIDDEN**:
- ❌ Database files in project root
- ❌ Any database except `$HOME/dbs/todowrite_development.db`
- ❌ Hardcoded absolute database paths

### 3. BRANCH WORKFLOW - ALWAYS ENFORCED
- ❌ Direct commits to `main` (production releases only)
- ❌ Direct commits to `develop` (integration only)
- ✅ All work on feature branches off `develop`
- ✅ Naming: `<type>/<description>` (feature/enhance-planning, fix/database-naming)

### 4. NO MOCKING - ALWAYS ENFORCED
- ❌ Mocks, stubs, fakes, test doubles
- ✅ Real implementations only
- ✅ Real in-memory components shared with production

### 5. PATH SECURITY - ALWAYS ENFORCED
**ALLOWED**: `$HOME/`, `$PWD/`, `./`, `../`, environment variables
**FORBIDDEN**: `/Users/username/`, `/home/user/`, hardcoded absolute paths

### 6. TODOWRITE MODELS API - EXCLUSIVE USE ONLY
**FORBIDDEN**:
- ❌ Old Node-based API functions (`create_node`, `get_node`, etc.)
- ❌ String-based IDs with random suffixes
- ❌ Old database schema or table structures

**REQUIRED**:
- ✅ Only Rails ActiveRecord models: `Goal`, `Concept`, `Task`, etc.
- ✅ Integer primary keys (1, 2, 3...)
- ✅ SQLAlchemy sessions and queries

### 7. AGENT STARTUP SEQUENCE - ALWAYS ENFORCED
```bash
# 1. Activate venv
source $PWD/.venv/bin/activate
# 2. Set database
export TODOWRITE_DATABASE_URL="sqlite:///$HOME/dbs/todowrite_development.db"
# 3. Load and apply CLAUDE.md rules
todowrite --enforce-claude-rules
# 4. Verify database content
todowrite verify --contains-goal "Enhance ToDoWrite Planning Capabilities"
# 5. Initialize ToDoWrite Models API
python .claude/auto_init_todowrite_models.py
```

**ENFORCEMENT**: CLI startup MUST read and apply these rules before any operations

---

## 📋 CODE QUALITY REQUIREMENTS

### 8. IMPLEMENTATION STANDARDS
- ✅ Full type hints (Python 3.12+ syntax, NO `Any` types)
- ✅ Natural language code style (reads like conversation)
- ✅ Comprehensive error handling (specific exceptions only, **NO `except Exception:` allowed**)
- ✅ Complete import organization (standard library → third-party → local, alphabetical)

**FORBIDDEN Exception Patterns**:
- ❌ `except Exception:` (too generic)
- ❌ `except:` (bare except)
- ❌ `except BaseException:` (too broad)

**REQUIRED Exception Patterns**:
```python
# ✅ CORRECT: Specific exceptions only
try:
    database.connect()
except DatabaseConnectionError as e:
    logger.error(f"Database connection failed: {e}")
except ConfigurationError as e:
    logger.error(f"Configuration error: {e}")

# ✅ CORRECT: Multiple specific exceptions
try:
    node = session.query(Node).filter(Node.id == node_id).one()
except (NodeNotFoundError, DatabaseError) as e:
    handle_node_error(e)
```

### 9. TESTING REQUIREMENTS (REAL TESTING ONLY)
- ✅ TDD methodology only (Red → Green → Refactor)
- ✅ Real implementations only (NO mocking, stubs, fakes, or test doubles)
- ✅ Component-based test organization (SoC required - no monolithic test files)
- ✅ Integration testing with real database and actual file systems
- ✅ End-to-end validation of real behavior, not simulated behavior

### 10. DATABASE OPTIMIZATION (MANDATORY)
- ✅ Minimize database calls (batch operations where possible)
- ✅ One query vs multiple queries analysis
- ✅ Cache results appropriately to avoid redundant calls
- ✅ Profile database operations to identify bottlenecks
- ✅ Prefer local tools (`grep`, `rg`, `sed`, `awk`) over AI reasoning for simple tasks

### 11. HAL AGENT & TOKEN OPTIMIZATION (ZERO EXCEPTIONS)
**MANDATORY**: All agents MUST use both systems for every task

**HAL Agent System** (0 API tokens):
```bash
python dev_tools/agent_controls/hal_token_savvy_agent.py \
  --provider anthropic --model $ANTHROPIC_MODEL \
  --goal "analyze database models" \
  --roots lib_package/ --include "*.py" \
  --chars 1000 --max-files 50
```

**Token Optimization System** (90% token savings):
```bash
python dev_tools/token_optimization/always_token_sage.py "analyze patterns"
```

**Enforcement**: Zero bypassing allowed. All AI interactions must go through HAL preprocessing first.

### 12. IMPORT ORGANIZATION STANDARDS (MANDATORY)
**Required Structure**:
1. Standard library imports (alphabetical)
2. Third-party imports (alphabetical)
3. Local/application imports (alphabetical)

**Example**:
```python
import json
import logging
from pathlib import Path
from typing import Any

import click
import sqlalchemy
from rich.console import Console

from todowrite.core.models import Goal, Task
from todowrite.utils.database_utils import get_database_path
```

**Forbidden**: `from module import *`, mixed imports, non-alphabetical order

### 13. FULL TYPE HINTING (MANDATORY)
- ✅ All function parameters typed (`self: Self`)
- ✅ All return types explicitly declared
- ✅ No `Any` types unless absolutely unavoidable
- ✅ Use Python 3.12+ syntax (`str | int` instead of `Union[str, int]`)
- ✅ All class attributes must have type hints

### 14. COMMIT STANDARDS (MANDATORY)
```
<type>(<scope>): <description>

[optional body]

🤖 Generated with [Claude Code](https://claude.com/claude-code)
Co-Authored-By: Claude <noreply@anthropic.com>
```

**Types**: feat, fix, docs, style, refactor, perf, test, build, ci, chore, revert
**Subject**: MAX 100 characters, start with capital, imperative mood
**Scope**: project-specific (lib, cli, docs, tests, build, config, ci)

---

## ⚡ ENFORCEMENT MECHANISMS

### CLI Startup Enforcement
The CLI MUST:
1. Read and parse this file on every startup
2. Verify virtual environment is active
3. Validate database URL and connectivity
4. Check database contains required goal and completeness
5. Fail immediately if any rule is violated

### /clear Command Enforcement
When `/clear` is issued, the CLI MUST:
1. Re-read this file
2. Re-verify all environment conditions
3. Re-validate database state
4. Verify HAL Agent System is ready
5. Verify Token Optimization System is active
6. Verify MCP Systems are initialized
7. Verify Anthropic API configuration
8. Only then clear context

### Violation Consequences
- 🚫 **Immediate termination** for virtual environment violations
- 🚫 **Database migration** for wrong database location
- 🚫 **Session restart** for any mandate violation
- 🚫 **Required re-initialization** of all work

---

## 🔧 ESSENTIAL WORKFLOW

### Development Sequence
```bash
# 1. Environment (MANDATORY)
source $PWD/.venv/bin/activate
export TODOWRITE_DATABASE_URL="sqlite:///$HOME/dbs/todowrite_development.db"

# 2. Verification (MANDATORY)
todowrite list --layer goal --title "Enhance ToDoWrite Planning Capabilities"

# 3. Development Work
todowrite create --layer task --title "Your task title"
# ... your work here ...

# 4. Pre-commit Quality Checks (MANDATORY)
./dev_tools/build.sh format
./dev_tools/build.sh lint

# 5. Quality Gates
./dev_tools/build.sh dev
./dev_tools/build.sh quality-gate

# 6. Commit (with verification)
git add .
git commit -m "feat(scope): description"
git push origin develop
```

**IMPORTANT**: Step 4 (Pre-commit Quality Checks) is MANDATORY before all commits. This follows a strict 4-phase process:

### Phase 1: INFORMATION GATHERING
```bash
./dev_tools/build.sh format
./dev_tools/build.sh lint
```
- Tools **INFORM** you of exactly what errors/warnings exist and where
- Tools report specific file locations and line numbers for each issue
- Tools provide clear descriptions of what needs to be fixed

### Phase 2: SYSTEMATIC FIXING
- **FIX ALL** issues identified by the tools
- Address every single error and warning reported
- Use the specific location information provided by the tools
- Do NOT proceed until all issues are resolved

### Phase 3: VERIFICATION
```bash
./dev_tools/build.sh format
./dev_tools/build.sh lint
```
- Re-run tools to **confirm ZERO issues remain**
- Only proceed when tools report clean output with no errors/warnings
- If any issues remain, return to Phase 2

### Phase 4: COMMIT
```bash
git add .
git commit -m "feat(scope): description"
git push origin develop
```
- **ONLY** commit after tools confirm clean code
- Pre-commit hooks should pass without any fixes needed
- Clean commit history maintained

**CRITICAL**: The tools must give you the "all clear" (ZERO issues) before any commit is attempted. Pre-commit hooks are safety nets, not primary workflow tools.

### Quick Commands
```bash
# Build and validate
./dev_tools/build.sh dev

# Quality gates
./dev_tools/build.sh quality-gate --strict

# Database verification
todowrite list --verify-completeness
```

---

## 📚 AUTHORITATIVE SOURCES

For all technical decisions, consult:
- Python: https://python.org, https://docs.python.org/3/library/typing.html
- SQLAlchemy: https://docs.sqlalchemy.org/
- UV: https://docs.astral.sh/uv/
- Conventional Commits: https://www.conventionalcommits.org/
- TodoWrite Models API: docs/ToDoWrite.md

---

**🚨 CRITICAL: These rules are enforced by the CLI and cannot be bypassed. Any attempt to override them will result in immediate session termination.**

## 21. Episodic Memory Initialization - MANDATORY

**ABSOLUTE REQUIREMENT**: ALL agents MUST ensure episodic memory is initialized and available

- **MANDATORY**: Run episodic memory indexing before starting development work
- **MANDATORY**: Ensure `/search-conversations` slash command is available
- **MANDATORY**: Verify embedding model is loaded and ready
- **MANDATORY**: Use episodic memory for context before starting new tasks
- **AUTOMATED**: Session startup hooks ensure episodic memory is ready
- **ZERO EXCEPTIONS**: This applies to ALL agents at ALL times

### Implementation:
```bash
# Manual episodic memory initialization
./dev_tools/ensure_episodic_memory.sh

# Or automatic via startup hook
.claude/hooks/session_startup_episodic_memory.py
```
