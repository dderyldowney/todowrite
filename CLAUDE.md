# CLAUDE.md

> **Reference guide for all project development.**

---

## 🔴 **AGENT INSTRUCTIONS**

**IMPORTANT**: As an agent, you MUST read and follow ALL guidelines in this document BEFORE executing any task. These standards supersede any conflicting instructions you may have received previously.

---

## 🚨 **MANUAL STARTUP SEQUENCE**

**Manual startup is required for each session since Claude Code CLI does not have automatic startup capabilities.**

**Before starting any work, manually run:**
```bash
./.claude/startup.sh
```

**This manual startup sequence executes:**
- ✅ Load all environment variables from .env
- ✅ Activate virtual environment and set PYTHONPATH
- ✅ Load and enforce CLAUDE.md rules
- ✅ **Initialize HAL Agent System** (token-savvy preprocessing)
- ✅ **Activate Token Optimization System** (always_token_sage)
- ✅ Initialize MCP Systems (81 tools across 7 servers)
- ✅ Verify MCP server health and connectivity
- ✅ Verify PostgreSQL backend connectivity
- ✅ Load session state from database
- ✅ **Enforce TDD compliance and all development mandates**
- ✅ **Enforce MCP-First workflow**

**DO NOT START ANY WORK until startup sequence completes successfully!**

---

## 🚨 **MONOREPO PROJECT STRUCTURE**

**ToDoWrite is a Python monorepo with 3 packages:**

```
todowrite/                          # Root monorepo
├── docs/                           # Comprehensive documentation
│   └── CHANGELOG.md
├── examples/                       # Usage examples for all packages
├── lib_package/                    # Core todowrite library
│   ├── src/todowrite/             # Library source code
│   └── pyproject.toml             # Library package config
├── cli_package/                    # Command-line interface
│   ├── src/todowrite_cli/         # CLI source code
│   └── pyproject.toml             # CLI package config
├── web_package/                    # Web interface (planned)
│   ├── src/todowrite_web/         # Web source code
│   └── pyproject.toml             # Web package config
├── tests/                          # Unified test suite
│   ├── lib_package/               # Library tests
│   ├── cli_package/               # CLI tests
│   └── web_package/               # Web tests
├── pyproject.toml                  # Root monorepo workspace config
├── uv.lock                        # UV workspace lockfile
└── README.md
```

### **Package Management**
- **Monorepo Management**: Always use `uv` workspace with root `pyproject.toml`
- **Package Development**: Each package has its own `pyproject.toml` and follows standard structure
- **Mirror Structure**: `tests/` mirrors package structure with separate directories for each package
- **Internal Dependencies**: Packages can depend on each other via workspace (e.g., CLI depends on lib)
- **Installation**: Use `uv sync` at root to install all workspace dependencies

---

## 🔴 **DEVELOPMENT STANDARDS**

### **Module Requirements**
- **Maximum 500 lines** per Python file (split larger files logically)
- **Documentation Header**: Every file MUST include:
  - Description of purpose and role in monorepo
  - Links to third-party package documentation
  - Sample input/output examples
  - Cross-package integration notes (if applicable)
- **Validation Function**: Every Python file needs a main block (`if __name__ == "__main__":`) that tests with real data

### **Architecture Principles**
- **Function-First Development**: Prefer simple functions over classes throughout the monorepo
- **Class Usage**: Only use classes when maintaining state across package boundaries, implementing data validation models, or following established design patterns
- **Async Code**: Never use `asyncio.run()` inside functions - only in main blocks
- **NO Conditional Imports**: Never use try/except blocks for imports of required packages

### **Type Hints Standards (Python 3.12+ MANDATORY)**
- **100% Coverage Required**: ALL code MUST have comprehensive type hinting (functions, classes, methods, variables, returns)
- **Python 3.12+ Syntax Only**: Use modern type hinting syntax (`|` for unions, `list[str]` instead of `List[str]`, `T | None` instead of `Optional[T]`)
- **No 'Any' Types**: Replace `Any` with specific types or `typing.Never` when truly no type applies
- **Cross-package types**: Shared type definitions should be in `lib_package/src/todowrite/types/`
- **Forward References**: Always use `from __future__ import annotations`

```python
# CORRECT - Python 3.12+ modern type hinting for monorepo:
from __future__ import annotations
from todowrite.types import TaskConfig, ValidationResult  # Shared types

def process_task(
    config: TaskConfig,
    options: dict[str, str] | None = None
) -> ValidationResult:
    """Process a task with optional configuration."""
    result: ValidationResult
    processed_data: list[str] = []

    for item_id: str in config.item_ids:
        item_result: str = _process_single_item(item_id)
        processed_data.append(item_result)

    result = ValidationResult(success=True, data=processed_data)
    return result

class TaskManager:
    """Manager for task operations with full type coverage."""

    def __init__(
        self,
        database_url: str,
        max_retries: int = 3
    ) -> None:
        self._database_url: str = database_url
        self._max_retries: int = max_retries
        self._active_tasks: dict[str, TaskConfig] = {}

    def add_task(self, task: TaskConfig) -> bool:
        """Add a task to the manager."""
        self._active_tasks[task.id] = task
        return True

    def get_task(self, task_id: str) -> TaskConfig | None:
        """Retrieve a task by ID."""
        return self._active_tasks.get(task_id)
```

---

## 🔴 **VALIDATION & TESTING**

### **Real Data Testing**
- **Always test with actual data**, never fake inputs
- **Cross-package integration**: Test real data flow between packages
- **Expected Results**: Verify outputs against concrete expected results
- **No Mocking**: NEVER mock core functionality, especially inter-package communication
- **Real Implementations Only**: Test with actual code, real data, and real connections
- **User-Exception Only**: Mock only when explicitly instructed by USER for specific portions

### **Validation Requirements**
- **Usage Functions Before Tests**: ALL relevant usage functions MUST successfully output expected results BEFORE any creation of tests
- **Results Before Lint**: ALL usage functionality MUST produce expected results BEFORE addressing any Pylint or other linter warnings
- **External Research After 3 Failures**: If a usage function fails validation 3 consecutive times, use external research tools

### **Validation Output Requirements**
- **NEVER print "All Tests Passed"** unless ALL tests actually passed
- **ALWAYS verify actual results** against expected results BEFORE printing ANY success message
- **ALWAYS track ALL failures** and report them at the end
- **ALWAYS include test counts** (e.g., "3 of 5 tests failed")
- **ALWAYS exit with code 1** if ANY tests fail, code 0 ONLY if ALL pass

```python
# CORRECT VALIDATION FOR MONOREPO with full type coverage:
if __name__ == "__main__":
    import sys

    all_validation_failures: list[str] = []
    total_tests: int = 0

    # Test 1: Core library functionality
    total_tests += 1
    from todowrite.core.models import Task
    test_task: Task = Task(title="Test Task", description="Test Description")
    expected_title: str = "Test Task"
    if test_task.title != expected_title:
        failure_message: str = f"Library model: Expected '{expected_title}', got '{test_task.title}'"
        all_validation_failures.append(failure_message)

    # Test 2: CLI integration
    total_tests += 1
    from todowrite_cli.commands import create_task
    try:
        cli_result: ValidationResult = create_task("CLI Test Task")
        if not cli_result.success:
            all_validation_failures.append("CLI integration: Task creation failed")
    except Exception as e:
        error_message: str = f"CLI integration: Unexpected error {e}"
        all_validation_failures.append(error_message)

    # Final validation result
    failed_count: int = len(all_validation_failures)
    if failed_count > 0:
        print(f"❌ VALIDATION FAILED - {failed_count} of {total_tests} tests failed:")
        for failure_index: int, failure_message in enumerate(all_validation_failures, start=1):
            print(f"  {failure_index}. {failure_message}")
        sys.exit(1)
    else:
        success_message: str = f"✅ VALIDATION PASSED - All {total_tests} tests produced expected results"
        print(success_message)
        sys.exit(0)
```

---

## 🔴 **STANDARD COMPONENTS & TOOLS**

### **Package Management**
- **Primary Tool**: Always use `uv` with workspace configuration
- **Development Commands**:
  - `uv sync` - Install all workspace dependencies
  - `uv run lib_package/src/todowrite/__main__.py` - Run library directly
  - `uv run cli_package/src/todowrite_cli/main.py` - Run CLI
  - `uv add package_name` - Add dependency to root workspace
  - `uv add --package lib_package package_name` - Add to specific package

### **Logging Standards**
- **Required Library**: Always use `loguru` for logging across all packages
```python
from loguru import logger

# Configure logger (typically in CLI entrypoint)
logger.add("app.log", rotation="10 MB", level="INFO")

# Package-specific logging
logger.info("Library operation completed")
logger.debug("CLI command executed")
```

### **CLI Structure**
- **Required File**: Every package with CLI must have a `cli.py` or `main.py`
- **CLI Framework**: Every command-line tool must use `typer` with full type annotations
```python
from __future__ import annotations
import typer
from loguru import logger

app: typer.Typer = typer.Typer(help="ToDoWrite CLI Tools")

@app.command()
def create_task(
    title: str = typer.Argument(..., help="Task title"),
    description: str = typer.Option("", "--description", "-d", help="Task description")
) -> None:
    """Create a new task in the system."""
    logger.info(f"Creating task: {title}")
    # Implementation using lib_package
    from todowrite.core.models import Task
    new_task: Task = Task(title=title, description=description)
    print(f"✅ Task created: {new_task.title}")

if __name__ == "__main__":
    app()
```

---

## 🔴 **DEVELOPMENT PRIORITY & EXECUTION**

### **Priority Order**
1. **Working Code** - Functionality first
2. **Validation** - Real data testing
3. **Readability** - Code clarity
4. **Static Analysis** - Linting and formatting (after code works)

### **Execution Standards**
- **Package Development**: `uv run lib_package/src/todowrite/module/script.py`
- **CLI Development**: `uv run cli_package/src/todowrite_cli/commands.py`
- **Testing**: `uv run pytest tests/lib_package/` or `uv run pytest tests/cli_package/`
- **Environment Variables**: `env VAR_NAME="value" uv run command`

---

## 🔴 **COMPLIANCE CHECK**

Before completing any task, verify that your work adheres to ALL monorepo standards:

1. ✅ All files have appropriate documentation headers with package context
2. ✅ Each module has a working validation function that tests real data and cross-package integration
3. ✅ **100% Type Coverage**: All code has comprehensive Python 3.12+ type hints
4. ✅ **Modern Syntax**: Uses `|` for unions, `list[str]` instead of `List[str]`, `T | None` instead of `Optional[T]`
5. ✅ **No Any Types**: Replaced `Any` with specific types or proper type annotations
6. ✅ All functionality is validated with real data before addressing linting issues
7. ✅ No asyncio.run() is used inside functions - only in main blocks
8. ✅ Code is under the 500-line limit for each file
9. ✅ If function failed validation 3+ times, external research was conducted and documented
10. ✅ Validation functions NEVER include unconditional "All Tests Passed" messages
11. ✅ Validation functions ONLY report success if explicitly verified
12. ✅ Validation functions track and report ALL failures, not just the first one encountered
13. ✅ Validation output includes count of failed tests out of total tests run
14. ✅ Cross-package communication is properly typed and tested
15. ✅ Package dependencies are correctly declared in pyproject.toml files
16. ✅ Workspace imports are used correctly throughout the monorepo
17. ✅ **Forward References**: `from __future__ import annotations` is used for all modules
18. ✅ **Variable Typing**: Every variable assignment is explicitly typed
19. ✅ **Class Attributes**: All class attributes are properly typed
20. ✅ **Method Signatures**: All method parameters and returns are fully typed

If any standard is not met, fix the issue before submitting the work.

---

## 🚨 **POSTGRESQL BACKEND SYSTEM**

### **🚨 MCP TOOLS USAGE REQUIREMENT**

**ALL AGENTS MUST USE MCP TOOLS - NEVER BUILT-IN TOOLS**

**ACTIVE MCP SERVERS (81 tools total):**
- **filesystem (11 tools)** - File operations
- **github-official (40 tools)** - GitHub integration
- **git (12 tools)** - Version control
- **SQLite (6 tools)** - Database operations
- **context7 (2 tools)** - AI assistance
- **docker** - Container management
- **hugging-face (9 tools)** - AI/ML integration

**🚫 FORBIDDEN BUILT-IN TOOLS (NEVER USE):**
- `Read` → Use MCP `read_file`
- `Write` → Use MCP `edit_file`
- `Edit` → Use MCP `edit_file`
- `Glob` → Use MCP `list_directory`
- `Bash` (for file operations) → Use MCP filesystem tools
- Direct bash git commands → Use MCP git tools

**🔴 MCP-FIRST WORKFLOW MANDATE:**
- **ALWAYS** use MCP tools for file operations BEFORE using Read/Edit/Write
- **ALWAYS** use MCP git tools BEFORE using bash git commands
- **ALWAYS** use MCP python_refactoring for code changes BEFORE manual editing
- **ALWAYS** use MCP database tools before direct SQL commands
- **NEVER** use built-in Claude Code tools when MCP equivalents exist
- **MANDATORY**: Research capabilities BEFORE assuming limitations
- **VERIFICATION REQUIRED**: Confirm MCP servers are healthy before starting work
- **VIOLATION**: Any bypass of MCP tools requires explicit justification in reasoning

**MCP Server Health Check:**
```bash
# Verify all MCP servers are running and healthy
python .claude/mcp_server_health_check.py

# Discover available MCP services
python .claude/mcp_service_discovery.py

# Verify MCP capabilities
python .claude/mcp_capability_discovery.py
```

### **🚨 MCP INFRASTRUCTURE LIFECYCLE POLICY**

**FUNDAMENTAL RULE: ALL MCP infrastructure (servers, Docker MCP Gateway, and toolsets) are SYSTEM-WIDE resources that MUST STAY RUNNING**

**🔴 EXPECTATION & REALITY:**
- **EXPECTATION**: MCP servers AND Docker MCP Gateway toolsets ARE already running
- **REALITY**: They will STAY RUNNING before, during, and after ALL sessions
- **NEVER stop/kill MCP servers or Docker MCP Gateway** - they serve ALL projects on the machine
- **NOT project-specific** - All MCP infrastructure are shared system resources
- **NO lifecycle management** - Scripts should NOT control any MCP infrastructure uptime

**🔴 ALLOWED OPERATIONS:**
- **✅ Verify server health** - Check if servers are running
- **✅ Restart individual servers** - Only if specific server is malfunctioning
- **✅ Restart AS NEEDED** - For troubleshooting or maintenance
- **✅ Discover available services** - Query capabilities and status

**🔴 FORBIDDEN OPERATIONS:**
- **❌ Stop ALL MCP servers** - Never at session end or project cleanup
- **❌ Stop Docker MCP Gateway** - Gateway toolsets serve all projects
- **❌ Kill MCP processes** - All MCP infrastructure are system-wide resources
- **❌ Automatic shutdown** - No session-based lifecycle management
- **❌ Project-specific culling** - MCP infrastructure serves multiple projects

**🔴 RECOVERY PROCEDURES (ONLY WHEN MCP INFRASTRUCTURE DIES):**
```bash
# ONLY use if MCP servers or Gateway are NOT running (unexpected failure):
docker mcp server ls  # Check Docker MCP Gateway status
bash .claude/start-mcp-servers.sh  # Recovery for MCP servers

# ONLY use if specific MCP server or Gateway is malfunctioning:
docker restart <specific-mcp-container>  # Individual server recovery
docker mcp gateway restart  # Docker MCP Gateway recovery
bash .claude/restart-mcp-servers.sh  # Bulk MCP server recovery

# Verify all MCP infrastructure is running (expected state):
python .claude/mcp_server_health_check.py
docker mcp server ls
```

**🔴 NORMAL OPERATION:**
- **EXPECT all MCP infrastructure running** - MCP servers AND Docker MCP Gateway
- **NO startup/shutdown scripts needed** - Should already be running
- **Health verification only** - Confirm infrastructure is running as expected
- **Leave everything running** - At session end, MCP infrastructure continues serving other projects

**🔴 DATABASE TABLE PROTECTION POLICY:**
```bash
# FORBIDDEN - NEVER delete production tables:
# DROP TABLE commands on production data
# TRUNCATE TABLE on production tables
# DELETE FROM production_tables without specific business reason
# Database schema modifications outside of migration scripts

# ALLOWED - Testing and development tables (naming convention: test_, temp_, dev_):
DROP TABLE test_user_data;           # OK - clearly marked as test
TRUNCATE temp_processing_queue;      # OK - clearly marked as temporary
DROP TABLE dev_feature_experiment;   # OK - clearly marked as development
DROP DATABASE dev_test_database;      # OK - clearly marked as development

# FORBIDDEN - Mocking and MagicMock:
# NEVER use mocks or MagicMock in tests
# ALWAYS test with actual implementations
# EXCEPTION: Only when explicitly instructed by USER for specific portions

# ALLOWED - Temporary development databases:
CREATE DATABASE dev_feature_x_testing;  # OK - clearly marked as development
DROP DATABASE dev_feature_x_testing;    # OK - cleanup after development
```

**🔴 PHILOSOPHY:**
All MCP infrastructure (servers, Docker MCP Gateway, and toolsets) are like system databases - they are EXPECTED to be running continuously and remain running across all sessions and projects. Production database tables contain persistent business and system data that must be preserved. Development and testing databases/tables may be created and removed as needed during development work. Recovery scripts are ONLY for unexpected outages of any MCP component.

### **Database Architecture**
**🚨 CRITICAL: PostgreSQL is the SINGLE SOURCE OF TRUTH**

**Container**: `mcp-postgres` (port 5433, auto-restart)
**IMPORTANT CLARIFICATION**: `mcp-postgres` is the Docker **container name** for the PostgreSQL database engine, NOT an MCP server. This container hosts multiple databases that serve MCP servers and the application.

**FUNDAMENTAL ARCHITECTURAL MANDATE:**
- **PostgreSQL databases are the ONLY authoritative data source**
- **File-based storage is FORBIDDEN for all persistent data**
- **JSON files in filesystem are cache ONLY, never primary data**
- **ALL operations MUST use PostgreSQL databases exclusively**

**Databases on mcp-postgres container:**
1. **`todowrite`** - Project management (43 tables, 12-layer hierarchy) - **AUTHORITATIVE**
2. **`mcp_episodic_memory`** - Conversation storage (6,686+ conversations) - **AUTHORITATIVE**
3. **`mcp_sessions`** - Session management and persistence - **AUTHORITATIVE**
4. **`mcp_filesystem`** - MCP filesystem tool data - **AUTHORITATIVE**
5. **`mcp_main`** - General MCP server data - **AUTHORITATIVE**

**🚨 TABLE PROTECTION MANDATE:**
- **NEVER DELETE production tables** - All tables contain persistent business/system data
- **EXCEPTION**: Testing and development tables may be deleted:
  - `test_*` - Testing tables
  - `temp_*` - Temporary tables
  - `dev_*` - Development tables
- **EXCEPTION**: Development databases may be created/dropped (`dev_*` databases)
- **FORBIDDEN**: `DROP TABLE`, `TRUNCATE TABLE` on production data
- **FORBIDDEN**: Schema modifications outside of migration scripts

**🚨 TESTING MANDATE - REAL IMPLEMENTATIONS ONLY:**
- **NEVER use mocks or MagicMock** - Always test with actual implementations
- **FORBIDDEN**: Mocking frameworks unless explicitly instructed by USER
- **EXCEPTION**: Only when USER explicitly instructs for specific portions
- **ALWAYS**: Test with real data, real connections, actual implementations

**USAGE REQUIREMENTS:**
- **ToDoWrite System**: MUST use `todowrite` database on PostgreSQL for ALL project data
- **Session Management**: MUST use `mcp_sessions` database for cross-session persistence
- **Conversation History**: MUST use `mcp_episodic_memory` database - NEVER file cache
- **MCP Server Data**: Each MCP server MUST store data in designated PostgreSQL database

### **Usage Commands**
```bash
# HAL Agent System (Token-Savvy Preprocessing)
python dev_tools/agent_controls/hal_token_savvy_agent.py --help
python dev_tools/agent_controls/hal_token_savvy_agent.py preprocess "your prompt"

# Token Optimization System
python dev_tools/token_optimization/always_token_sage.py "your content"
python dev_tools/token_optimization/always_token_sage.py --help

# MCP System Management
python .claude/mcp_server_health_check.py          # Verify MCP servers
python .claude/mcp_service_discovery.py           # Discover MCP services
python .claude/mcp_capability_discovery.py        # List MCP capabilities
# MCP servers STAY RUNNING - See MCP Server Lifecycle Policy below

# Database management (via MCP SQLite tools)
python .claude/todowrite_database_manager.py

# Session state
python .claude/session_manager.py --summary

# Quick verification
bash .claude/quick_check.sh
```

**HAL & Token Optimization ENFORCEMENT:**
- **HAL preprocessing is MANDATORY** (`HAL_PREPROCESSING_MANDATORY=true`)
- **Token optimization must be active** for all agent operations
- **Verification Required**: Both systems must respond to health checks during startup
- **Integration**: HAL preprocessing → Token optimization → Agent execution

### **Models API Usage**
```python
from todowrite.core.models import (
    Goal, Concept, Context, Constraints, Requirements,
    AcceptanceCriteria, InterfaceContract, Phase, Step,
    Task, SubTask, Command, Label
)

goal = Goal(title="My Goal", description="Goal description")
concept = Concept(title="My Concept", description="Concept description")
```

**ENFORCEMENT:** ONLY use existing lib_package Models API - NO parallel implementations

---

## 🔴 **TODOWRITE DEVELOPMENT MANDATES**

### **🚨 NON-NEGOTIABLE REQUIREMENTS**

**ALL DEVELOPMENT WORK** MUST start with ToDoWrite planning:
- **NO CODE IMPLEMENTATION** without goal/concept/task breakdown
- **ZERO EXCEPTIONS** for "quick fixes" or "simple changes"
- **ALL AGENTS** (Chat, CLI, VSCode) MUST enforce this requirement

**🚨 DATABASE DATA PROTECTION MANDATE:**
- **NEVER DELETE without investigation**: Follow DATABASE_INVESTIGATION_PROTOCOL.md
- **NEVER REBUILD without verification**: Check for existing data/tables first
- **NEVER ASSUME "not found"**: Use proper investigation commands
- **ZERO TOLERANCE** for data loss through negligence
- **MANDATORY PROTOCOL**: Database → Tables → Data → THEN work

**🚨 COST OPTIMIZATION MANDATE:**
- **MCP-FIRST**: Use MCP tools before built-in tools
- **RESEARCH-FIRST**: Never assume capabilities without investigation
- **ZERO REWORK**: Investigate thoroughly, implement correctly once
- **TOKEN MINIMIZATION**: Every mistake costs money and time

**Pre-Work Verification:**
```bash
# Verify active goals exist:
docker exec mcp-postgres psql -U mcp_user -d todowrite -c "SELECT COUNT(*) FROM goals WHERE status = 'active';"

# Check session context:
python .claude/session_manager.py --summary

# Verify TDD compliance (MUST PASS before any coding):
pytest tests/ -v  # Should show existing tests, fail new ones
```

### **🚨 POSTGRESQL-FIRST TODOWRITE USAGE**

**FUNDAMENTAL MANDATE: ToDoWrite system MUST use PostgreSQL database exclusively:**

**🔴 AUTHORITY REQUIREMENTS:**
- **`todowrite` database** on `mcp-postgres` container is the ONLY authoritative data source
- **SQLite files** are FORBIDDEN - NEVER use local file storage
- **YAML configs** are cache/import-export ONLY - never primary data
- **ALL ToDoWrite operations** MUST use PostgreSQL connection

**🔴 DATABASE CONNECTION MANDATE:**
```python
# REQUIRED - Connect to PostgreSQL ONLY
DATABASE_URL = "postgresql://mcp_user:mcp_secure_password_2024@localhost:5433/todowrite"

# FORBIDDEN - NEVER use these:
# sqlite:///path/to/todowrite.db  # ❌ FORBIDDEN
# yaml file storage               # ❌ FORBIDDEN
# local JSON files               # ❌ FORBIDDEN
```

**🔴 CLI USAGE REQUIREMENTS:**
```bash
# CORRECT - PostgreSQL ONLY
PYTHONPATH="lib_package/src:cli_package/src" python -m todowrite_cli --storage-preference postgresql_only

# FORBIDDEN - NEVER use:
# python -m todowrite_cli --storage-preference sqlite_only  # ❌ FORBIDDEN
# python -m todowrite_cli --storage-preference yaml_only   # ❌ FORBIDDEN
```

**🔴 VERIFICATION COMMANDS:**
```bash
# Verify ToDoWrite is using PostgreSQL (MUST PASS):
docker exec mcp-postgres psql -U mcp_user -d todowrite -c "SELECT COUNT(*) FROM goals;"

# Verify no SQLite files are being used:
find . -name "*.db" -o -name "*.sqlite" 2>/dev/null | grep -v ".venv" && echo "❌ FORBIDDEN SQLITE FILES FOUND" || echo "✅ No forbidden SQLite files"
```

### **🔬 MANDATORY TDD & RED-GREEN-REFACTOR**

**🚨 UNEQUIVOCAL TDD ENFORCEMENT:**

**ALL CODE** MUST follow TDD workflow without exception:
- **RED PHASE**: Start with failing test
- **GREEN PHASE**: Minimal code to pass test only
- **REFACTOR PHASE**: Improve code while tests pass
- **ZERO EXCEPTIONS**: No anti-TDD patterns allowed

**🔴 TDD MANDATE VERIFICATION:**
```bash
# STEP 1: Write failing test FIRST (MUST FAIL)
pytest tests/ -v -k "your_new_feature"  # MUST show failure

# STEP 2: Implement minimal code to pass (ONLY after test fails)
# ... write implementation ...

# STEP 3: Verify test passes (MUST PASS)
pytest tests/ -v -k "your_new_feature"  # MUST show success

# STEP 4: All tests must pass (MANDATORY)
pytest tests/ -v  # ALL tests MUST pass
```

**🚫 FORBIDDEN WORKFLOW VIOLATIONS:**
- **NO CODE** without failing test first
- **NO IMPLEMENTATION** before test exists and fails
- **NO "QUICK FIXES"** without test coverage
- **NO SKIP-TEST excuses** for "simple changes"
- **NO PRODUCTION CODE** that isn't tested

**TDD COMPLIANCE ENFORCEMENT:**
- **startup_enforcement.py** verifies pytest exists and tests can run
- **Compliance Check #9**: External research after 3 validation failures
- **Compliance Check #10**: No unconditional "All Tests Passed" messages
- **Zero-tolerance policy**: Any TDD violation = immediate work stoppage

---

## 🔴 **CROSS-SESSION STORAGE MANDATES**

### **🚨 POSTGRESQL SESSION AUTHORITY**

**FUNDAMENTAL REQUIREMENT: All session data MUST be stored in PostgreSQL exclusively:**

**🔴 mcp_sessions DATABASE (AUTHORITATIVE):**
- **Container**: `mcp-postgres` (PostgreSQL engine, NOT MCP server)
- **Database**: `mcp_sessions`
- **Purpose**: Cross-session persistence, conversation state, work continuity
- **Authority**: SINGLE source of truth for ALL session data
- **File-based session storage**: FORBIDDEN

**🔴 SESSION STORAGE REQUIREMENTS:**
- **ALL session context** MUST be stored in `mcp_sessions` database
- **NO JSON files** for session persistence (cache only)
- **NO local storage** for session state
- **PostgreSQL queries ONLY** for session read/write operations
- **Cross-session continuity** depends on PostgreSQL database health

**🔴 VERIFICATION COMMANDS:**
```bash
# Verify sessions database accessibility:
docker exec mcp-postgres psql -U mcp_user -d mcp_sessions -c "SELECT COUNT(*) FROM sessions LIMIT 1;"

# Verify session data is being stored (not files):
find .claude -name "*session*" -type f 2>/dev/null | grep -v ".py" && echo "❌ FORBIDDEN SESSION FILES FOUND" || echo "✅ Session data in PostgreSQL only"

# Check current session state:
python .claude/session_manager.py --summary
```

**🔴 SESSION CONTINUITY DEPENDS ON:**
1. **`mcp-postgres` container running** (PostgreSQL engine)
2. **`mcp_sessions` database accessible**
3. **No file-based session storage** (cache only)
4. **PostgreSQL as single source of truth**

---

## 🔄 **SESSION STATE RESTORE**

**To restore your previous session state:**
```bash
source $PWD/.venv/bin/activate && python .claude/session_manager.py --summary
```

**If you see a session summary, your previous work context has been successfully restored!**

---

**Session Continuity:** ✅ **MAINTAINED** - All work preserved in PostgreSQL database
