# ToDoWrite Codebase Comprehensive Exploration Report

## Executive Summary

ToDoWrite is a sophisticated hierarchical task management system designed for complex project planning and execution. It implements a **12-layer declarative planning framework** with database-first architecture supporting PostgreSQL → SQLite → YAML fallback chain. The system emphasizes **Separation of Concerns**, build-time validation, and traceability.

**Project Details:**
- **Version:** See VERSION file
- **Python:** 3.12+ (strict type hints with mypy)
- **Primary Dependencies:** SQLAlchemy 2.0, Click CLI, PyYAML, jsonschema
- **Current Branch:** develop
- **Architecture:** Hierarchical task management with pluggable storage backends

---

## 1. PROJECT STRUCTURE & ENTRY POINTS

### Directory Organization

```
ToDoWrite/
├── todowrite/                    # Main Python package
│   ├── __init__.py             # Package exports: ToDoWrite class
│   ├── __main__.py             # Entry point: calls main()
│   ├── main.py                 # main() function → calls cli()
│   ├── cli.py                  # Click CLI implementation (primary interface)
│   ├── app.py                  # Core ToDoWrite application class
│   ├── yaml_manager.py         # YAML import/export manager
│   ├── yaml_storage.py         # YAML-based storage backend
│   ├── db/
│   │   ├── config.py           # Database configuration & fallback chain
│   │   └── models.py           # SQLAlchemy ORM models
│   └── tools/
│       ├── extract_schema.py   # Schema extraction from markdown
│       ├── tw_validate.py      # JSON schema validator
│       ├── tw_trace.py         # Traceability matrix builder
│       ├── tw_lint_soc.py      # Separation of Concerns linter
│       └── tw_stub_command.py  # Command stub generator
│
├── configs/                     # YAML configuration files
│   ├── plans/                  # 11-layer planning hierarchy
│   │   ├── goals/              # Layer 1: Goal nodes
│   │   ├── concepts/           # Layer 2: Concept nodes
│   │   ├── contexts/           # Layer 3: Context nodes
│   │   ├── constraints/        # Layer 4: Constraints nodes
│   │   ├── requirements/       # Layer 5: Requirements nodes
│   │   ├── acceptance_criteria/# Layer 6: Acceptance Criteria nodes
│   │   ├── interface_contracts/# Layer 7: Interface Contract nodes
│   │   ├── phases/             # Layer 8: Phase nodes
│   │   ├── steps/              # Layer 9: Step nodes
│   │   ├── tasks/              # Layer 10: Task nodes
│   │   └── subtasks/           # Layer 11: SubTask nodes
│   ├── commands/               # Layer 12: Executable Command nodes
│   └── schemas/
│       └── todowrite.schema.json # JSON schema for validation
│
├── tests/                       # Test suite
│   ├── test_app.py             # Application logic tests
│   └── test_cli.py             # CLI functionality tests
│
├── docs/                        # Documentation
├── pyproject.toml              # Python project configuration
├── Makefile                    # Workflow automation
└── docker-compose.yml          # PostgreSQL + pgAdmin setup
```

### Entry Points

1. **CLI Entry Point** (Primary)
   - Path: `$HOME/projects/ToDoWrite/todowrite/cli.py`
   - Command: `todowrite` (defined in pyproject.toml as `todowrite = "todowrite.cli:cli"`)
   - Framework: Click (8.0+)
   - Root Command: `cli()` - main Click group with storage preference option

2. **Python Module Entry Point**
   - Path: `$HOME/projects/ToDoWrite/todowrite/__init__.py`
   - Export: `ToDoWrite` class from `app.py`
   - Usage: `from todowrite import ToDoWrite`

3. **Main Execution Flow**
   - `__main__.py` → `main.py` (calls `cli()`) → `cli.py` (Click CLI)

---

## 2. DATABASE IMPLEMENTATION

### Storage Architecture: Database-First with Fallback Chain

Located: `$HOME/projects/ToDoWrite/todowrite/db/config.py`

**Three-Tier Fallback Strategy:**
```
Priority 1: PostgreSQL (preferred, enterprise-grade)
    ↓ (if unavailable)
Priority 2: SQLite3 (reliable fallback, development-friendly)
    ↓ (if unavailable)
Priority 3: YAML Files (last resort, no database needed)
```

### Database Configuration System

**Enums:**
- `StorageType`: PostgreSQL, SQLite, YAML
- `StoragePreference`: auto, postgresql_only, sqlite_only, yaml_only

**Key Functions:**
- `determine_storage_backend()`: Returns (StorageType, url)
- `get_postgresql_candidates()`: Finds PostgreSQL connection URLs
  - Checks: explicit env var, Docker container, localhost defaults
- `get_sqlite_candidates()`: Finds SQLite file locations
- `test_postgresql_connection()`: Validates PostgreSQL availability
- `test_sqlite_connection()`: Validates SQLite availability
- `get_storage_info()`: Returns current configuration details
- `get_setup_guidance()`: Provides setup instructions based on current state

**Environment Variables:**
```
TODOWRITE_DATABASE_URL     # Full database URL override
DATABASE_URL               # Standard database URL (fallback)
TODOWRITE_STORAGE_PREFERENCE # Storage preference (auto/postgresql_only/sqlite_only/yaml_only)
```

### SQLAlchemy ORM Models

Located: `$HOME/projects/ToDoWrite/todowrite/db/models.py`

**Core Tables:**

1. **Node** (Primary Entity)
   - Fields: id (PK), layer, title, description, status, owner, severity, work_type
   - Relationships: labels (many-to-many), command (one-to-one)
   - Status: planned, in_progress, blocked, done, rejected

2. **Link** (Parent-Child Relationships)
   - Composite PK: (parent_id, child_id) - both FK to Node.id
   - Enables hierarchical structure

3. **Label** (Tags/Categories)
   - PK: label (string)
   - M2M: node_labels junction table with Node

4. **node_labels** (Junction Table)
   - Composite PK: (node_id, label)
   - Many-to-many relationship between nodes and labels

5. **Command** (Executable Commands - Layer 12)
   - PK: node_id (FK to Node.id)
   - Fields: ac_ref (Acceptance Criteria reference), run (JSON string)
   - Relationship: artifacts (one-to-many)

6. **Artifact** (Command Outputs)
   - Composite PK: (artifact, command_id)
   - FK: command_id → Command.node_id
   - Stores expected output artifacts from commands

### Database Migrations

**No explicit migration files** - Uses SQLAlchemy's declarative base:
- `Base.metadata.create_all()` - creates all tables
- Automatic table creation on initialization
- Called by `ToDoWrite.init_database()`

---

## 3. CLI IMPLEMENTATION

Located: `$HOME/projects/ToDoWrite/todowrite/cli.py`

### CLI Architecture

Framework: **Click 8.0+** (Pallets Projects)

**Root Command Group:**
```python
@click.group()
@click.option("--storage-preference", type=click.Choice([...]))
def cli(ctx, storage_preference):
    """A CLI for the ToDoWrite application."""
```

### Core Commands (Layer 0 - Database Operations)

1. **init**
   - Initializes database/YAML storage
   - Creates all tables or directories

2. **create** `<layer> <title> <description> [--parent]`
   - Creates new node with auto-generated ID
   - Validates layer type against LayerType enum

3. **get** `<node_id>`
   - Retrieves and displays single node details

4. **list**
   - Displays all nodes grouped by layer

5. **db-status** `[--storage-preference]`
   - Shows current storage configuration
   - Displays connection status
   - Provides setup guidance

6. **import-yaml** `[--force] [--dry-run]`
   - Imports YAML files to database
   - Handles conflicts and dry-run mode

7. **export-yaml** `[--output-dir] [--no-backup]`
   - Exports database content to YAML
   - Creates backups automatically

8. **sync-status**
   - Checks sync between YAML and database
   - Shows orphaned nodes

### ToDoWrite Subcommand Group (Layers 1-12 Framework Tools)

**Subcommand prefix:** `todowrite`

**Commands:**

1. **todowrite validate-plan** `[--strict]`
   - Schema validation against todowrite.schema.json
   - Maps to: `tw_validate.py`

2. **todowrite trace-links** `[--summary]`
   - Builds traceability matrix
   - Analyzes dependency graph
   - Maps to: `tw_trace.py`

3. **todowrite generate-commands** `[--force]`
   - Generates Command stubs from Acceptance Criteria
   - Maps to: `tw_stub_command.py`

4. **todowrite execute-commands** `[CMD_ID|--all] [--dry-run]`
   - Executes generated command stubs
   - Captures output to `results/CMD-ID/execution.log`

5. **todowrite show-hierarchy** `[--layer] [--format tree|flat|json]`
   - Displays planning hierarchy in multiple formats
   - Loads from `configs/plans/` directory

6. **todowrite check-soc**
   - Validates Separation of Concerns compliance
   - Ensures layers 1-11 are non-executable
   - Maps to: `tw_lint_soc.py`

### Layer-to-ID-Prefix Mapping

```python
LAYER_TO_PREFIX = {
    "Goal": "GOAL",
    "Concept": "CON",
    "Context": "CTX",
    "Constraints": "CST",
    "Requirements": "R",
    "AcceptanceCriteria": "AC",
    "InterfaceContract": "IF",
    "Phase": "PH",
    "Step": "STP",
    "Task": "TSK",
    "SubTask": "SUB",
    "Command": "CMD",
}
```

---

## 4. CORE APPLICATION LOGIC

Located: `$HOME/projects/ToDoWrite/todowrite/app.py`

### ToDoWrite Application Class

**Main Interface:** `class ToDoWrite`

**Initialization:**
```python
def __init__(
    self,
    db_url: str | None = None,
    auto_import: bool = True,
    storage_preference: StoragePreference | None = None,
)
```

**Key Attributes:**
- `storage_type`: StorageType enum (PostgreSQL/SQLite/YAML)
- `db_url`: Connection string
- `engine`: SQLAlchemy engine (None if YAML)
- `Session`: SQLAlchemy session factory
- `yaml_storage`: YAMLStorage instance (if YAML mode)

**Core Data Models:**

1. **Node** (Dataclass)
   - `id`: str, `layer`: LayerType, `title`: str
   - `description`: str, `status`: StatusType
   - `links`: Link, `metadata`: Metadata, `command`: Command | None

2. **Link** (Dataclass)
   - `parents`: list[str], `children`: list[str]

3. **Metadata** (Dataclass)
   - `owner`: str, `labels`: list[str]
   - `severity`: str, `work_type`: str

4. **Command** (Dataclass)
   - `ac_ref`: str, `run`: dict[str, Any]
   - `artifacts`: list[str]

5. **Type Aliases**
   - `LayerType`: Union of 12 layer names
   - `StatusType`: "planned", "in_progress", "blocked", "done", "rejected"

### CRUD Operations

**Create:**
```python
def [REMOVED_LEGACY_PATTERN](self, node_data: dict[str, Any]) -> Node
```
- Validates against JSON schema
- Routes to DB or YAML based on storage type
- Returns Node object

**Read:**
```python
def get_node(self, node_id: str) -> Node | None
def get_all_nodes(self) -> dict[str, list[Node]]
```
- Returns nodes grouped by layer

**Update:**
```python
def update_node(self, node_id: str, node_data: dict[str, Any]) -> Node | None
```
- Updates all fields including links and labels

**Delete:**
```python
def delete_node(self, node_id: str) -> None
```

### Helper Methods for Node Creation

**Layer-specific factory methods:**
- `add_goal()`, `add_phase()`, `add_step()`, `add_task()`, `add_subtask()`
- `add_command()`, `add_concept()`, `add_context()`
- `add_constraint()`, `add_requirement()`, `add_acceptance_criteria()`
- `add_interface_contract()`

Each generates appropriate ID prefix and calls `[REMOVED_LEGACY_PATTERN]()`

### Session Management

```python
@contextmanager
def get_session(self) -> Generator[Session, None, None]:
    # For YAML storage: yields None
    # For DB storage: handles commit/rollback
```

### Validation

```python
def _validate_node_data(self, node_data: dict[str, Any]) -> None
    # Uses jsonschema against todowrite.schema.json
```

### Internal Conversion Methods

- `_convert_db_node_to_node()`: DBNode → Node dataclass
- `_dict_to_node()`: dict → Node dataclass
- `_create_db_node()`: Creates and persists DB node

### Auto-Import Feature

```python
def _auto_import_yaml_files(self) -> None
```
- Automatically imports YAML files on startup
- Only when using database storage (not YAML)
- Uses YAMLManager for synchronization

---

## 5. YAML STORAGE SYSTEM

### YAML Storage Backend

Located: `$HOME/projects/ToDoWrite/todowrite/yaml_storage.py`

**Purpose:** Standalone YAML-based storage when databases unavailable

**Class:** `YAMLStorage`

**Key Methods:**

- `load_node(node_id)`: Load single node from YAML file
- `save_node(node)`: Save node to YAML file
- `delete_node(node_id)`: Delete node YAML file
- `load_all_nodes()`: Load all nodes, grouped by layer
- `node_exists(node_id)`: Check if node file exists
- `update_node_links()`: Update parent/child links
- `get_nodes_by_layer(layer)`: Get all nodes in layer
- `count_nodes()`: Total node count

**Directory Structure:**
```
configs/
├── plans/
│   ├── goals/
│   ├── concepts/
│   ├── contexts/
│   ├── constraints/
│   ├── requirements/
│   ├── acceptance_criteria/
│   ├── interface_contracts/
│   ├── phases/
│   ├── steps/
│   ├── tasks/
│   └── subtasks/
└── commands/
```

**Layer Mapping:**
```python
self.layer_dirs = {
    "Goal": "goals",
    "Concept": "concepts",
    # ... etc
    "Command": "commands",  # Special: separate from plans/
}
```

### YAML File Format

Example: `configs/plans/goals/GOAL-TODOWRITE-SYSTEM-IMPLEMENTATION.yaml`

```yaml
id: GOAL-TODOWRITE-SYSTEM-IMPLEMENTATION
layer: Goal
title: Complete ToDoWrite System Implementation
description: >
  Implement the complete ToDoWrite 12-layer declarative planning framework...
metadata:
  owner: system-architect
  labels: ["work:architecture", "todowrite", "planning-framework"]
  severity: high
  work_type: architecture
links:
  parents: []
  children: [CON-DECLARATIVE-SEPARATION-ARCHITECTURE]
```

**Optional fields:** status, command

### YAML Manager (Import/Export)

Located: `$HOME/projects/ToDoWrite/todowrite/yaml_manager.py`

**Class:** `YAMLManager`

**Key Methods:**

**Discovery:**
- `get_yaml_files()`: Find all YAML files in configs/
- `get_existing_node_ids()`: Get all DB node IDs

**Import:**
- `import_yaml_files(force, dry_run)`: Import YAML to database
  - Handles duplicates and conflicts
  - Dry-run preview mode
  - Returns summary: imported, skipped, errors, total_files, total_imported

**Export:**
- `export_to_yaml(output_dir, backup_existing)`: Export database to YAML
  - Creates backup of existing YAML files
  - Returns summary: exported, errors, total_nodes, total_exported

**Synchronization:**
- `check_yaml_sync()`: Compare YAML files with database
  - Returns: yaml_only, database_only, both node IDs

**Auto-Import:**
- `auto_import_on_startup()`: Automatically import missing YAML files

**Conversion:**
- `node_to_yaml()`: Node → YAML-compatible dict
- `load_yaml_file()`: Load and validate YAML file

---

## 6. VALIDATION SYSTEM

### JSON Schema Validation

**Schema File:** `configs/schemas/todowrite.schema.json`

**Schema Features:**
- Enforces required fields: id, layer, title, description, links
- ID pattern validation: `^(GOAL|CON|CTX|CST|R|AC|IF|PH|STP|TSK|SUB|CMD)-[A-Z0-9_-]+$`
- Layer enum validation: All 12 layer types
- Metadata validation:
  - severity: low, med, high
  - work_type: architecture, spec, interface, validation, implementation, docs, ops, refactor, chore, test
- Links validation: parents and children arrays
- Conditional validation:
  - Command layer MUST have command field
  - Layers 1-11 MUST NOT have command field
- Command validation:
  - ac_ref pattern: `^AC-[A-Z0-9_-]+$`
  - run object with required shell field
  - Optional: workdir, env variables, artifacts array

### Schema Validator Tool

Located: `$HOME/projects/ToDoWrite/todowrite/tools/tw_validate.py`

**Class:** `ToDoWriteValidator`

**Functionality:**
- Loads JSON schema from `configs/schemas/todowrite.schema.json`
- Discovers all YAML files in `configs/plans/*`
- Validates each file against schema
- Reports validation errors with location details
- Summary output: valid count, total count

**CLI Integration:**
```bash
todowrite todowrite validate-plan [--strict]
python todowrite/tools/tw_validate.py [--strict]
make tw-validate
```

---

## 7. SEPARATION OF CONCERNS LINTING

Located: `$HOME/projects/ToDoWrite/todowrite/tools/tw_lint_soc.py`

**Class:** `SoCLinter`

**Purpose:** Enforce architectural constraint that only Layer 12 (Command) can contain executable content

**Non-Executable Layers (1-11):**
- Goal, Concept, Context, Constraints, Requirements
- AcceptanceCriteria, InterfaceContract, Phase, Step, Task, SubTask

**Executable Pattern Detection:**
Detects dangerous patterns:
- Shebangs: `#!/.*`
- Python exec/eval: `exec(`, `eval(`
- Python subprocess: `subprocess.`, `import subprocess`, `from subprocess`
- Python system calls: `os.system`, `os.popen`
- Shell command substitution: `$()`, backticks
- Dangerous subprocess: `shell=True`

**Validation Rules:**
1. Check for 'command' key in non-executable layers (forbidden)
2. Scan all string values for executable patterns
3. Verify Command layer has proper command field structure
4. Report violations with file path and details

**CLI Integration:**
```bash
todowrite todowrite check-soc
python todowrite/tools/tw_lint_soc.py
make tw-lint
```

---

## 8. TRACEABILITY SYSTEM

Located: `$HOME/projects/ToDoWrite/todowrite/tools/tw_trace.py`

**Class:** `TraceabilityBuilder`

**Purpose:** Build and analyze dependency graph and traceability matrix

**Key Data Structures:**
- `nodes`: Dictionary of all nodes (id → node_data)
- `forward_links`: Dictionary mapping nodes to their children
- `backward_links`: Dictionary mapping nodes to their parents
- `orphaned_nodes`: Set of nodes without proper relationships
- `circular_deps`: List of circular dependency chains

**Analysis Methods:**
- `load_all_nodes()`: Load nodes from YAML files
- `build_links()`: Construct forward/backward link mappings
- `check_traceability()`: Verify all nodes are traceable
- `find_circular_dependencies()`: Detect circular references
- `find_orphaned_nodes()`: Identify unreachable nodes
- `generate_traceability_matrix()`: Output CSV traceability matrix
- `generate_dependency_graph()`: Output JSON dependency graph

**Output Files:**
- `trace/trace.csv`: Traceability matrix (CSV format)
- `trace/graph.json`: Dependency graph (JSON format)

**CLI Integration:**
```bash
todowrite todowrite trace-links [--summary]
python todowrite/tools/tw_trace.py [--summary]
make tw-trace
```

---

## 9. COMMAND STUB GENERATOR

Located: `$HOME/projects/ToDoWrite/todowrite/tools/tw_stub_command.py`

**Class:** `CommandStubGenerator`

**Purpose:** Auto-generate executable Command layer stubs from Acceptance Criteria

**Workflow:**
1. Find all AC-*.yaml files in `configs/plans/acceptance_criteria/`
2. For each AC without corresponding command:
   - Generate CMD ID (AC-X → CMD-X)
   - Generate appropriate shell command based on AC title/content
   - Generate expected artifacts list
   - Create YAML command file in `configs/commands/`
   - Update AC file's children links to include new command

**Shell Command Generation Logic:**

| AC Content | Generated Command |
|-----------|------------------|
| "makefile"/"targets" | `make tw-all && echo 'Makefile targets verified'` |
| "validation"/"schema" | `python todowrite/tools/tw_validate.py --strict` |
| "lint"/"soc" | `python todowrite/tools/tw_lint_soc.py` |
| "trace"/"links" | `python todowrite/tools/tw_trace.py` |
| "cli"/"command" | `python -m todowrite --help && echo 'CLI commands verified'` |
| "documentation"/"docs" | Find and verify documentation files |
| "test" | `python -m pytest tests/ -v` |
| Other | `echo 'Manual verification required for: {title}'` |

**Artifact Generation:**
- Based on AC type, generates expected output artifacts
- Example: validation AC → "validation_report.txt"

**CLI Integration:**
```bash
todowrite todowrite generate-commands [--force]
python todowrite/tools/tw_stub_command.py [--force]
make tw-prove
```

---

## 10. COMMAND EXECUTION

**Location in CLI:** `todowrite todowrite execute-commands`

**Functionality:**
- Execute generated command stubs from `configs/commands/`
- Supports single command or batch execution
- Captures output to `results/{CMD_ID}/execution.log`

**Command File Format:**
```yaml
id: CMD-EXAMPLE-TASK
layer: Command
title: Execute Example Task
description: Executes example command
metadata:
  owner: system
  labels: []
command:
  ac_ref: AC-EXAMPLE-TASK
  run:
    shell: "your command here"
  artifacts: ["output.txt"]
links:
  parents: [AC-EXAMPLE-TASK]
  children: []
```

**Execution Log Format:**
```
Command: <shell command>
Exit Code: <return code>
STDOUT:
<output>
STDERR:
<error output>
```

---

## 11. CONFIGURATION SYSTEM

### Project Configuration

**File:** `pyproject.toml`

**Python Requirements:**
```toml
requires-python = ">=3.12"
dependencies = [
    "sqlalchemy>=2.0.0",
    "typing-extensions>=4.0.0",
    "click>=8.0.0",
    "psycopg2-binary>=2.9.0",
]
```

**Development Tools:**
- mypy: Type checking (strict mode enabled)
- ruff: Linting and formatting
- black: Code formatting
- isort: Import sorting
- pytest: Testing
- bandit: Security analysis
- pre-commit: Git hooks

**Quality Settings:**
- Target Python: 3.12+
- Line length: 88 characters (Black standard)
- Ruff rules: E, W, F, I, B, C4, UP, RUF, S, T20, SIM, ARG, PTH
- MyPy: Strict mode (disallow_untyped_defs, etc.)

### Storage Configuration

**Environment Variables:**
```
TODOWRITE_DATABASE_URL           # PostgreSQL/SQLite URL
DATABASE_URL                      # Fallback standard variable
TODOWRITE_STORAGE_PREFERENCE     # auto/postgresql_only/sqlite_only/yaml_only
```

**Docker Configuration:**

File: `docker-compose.yml`

Services:
- **postgres**: PostgreSQL 16-Alpine
  - Container: todowrite-postgres
  - Port: 5432
  - User: todowrite / Password: todowrite_dev_password
  - Health check: pg_isready

- **pgadmin** (optional): pgAdmin 4
  - Port: 8080
  - Email: admin@todowrite.dev / Password: admin

---

## 12. TEST STRUCTURE

Located: `$HOME/projects/ToDoWrite/tests/`

### test_app.py - Application Tests

**Setup:** Requires docker-compose with PostgreSQL

**Test Coverage:**
- `test_init_database()`: Database initialization
- `test_[REMOVED_LEGACY_PATTERN]()`: Node creation with metadata
- `test_get_node()`: Single node retrieval
- `test_get_all_nodes()`: Bulk node retrieval
- `test_update_node()`: Node updates with link changes
- `test_delete_node()`: Node deletion
- Command-specific tests: Commands with artifacts

**Database:** PostgreSQL (localhost:5432)

### test_cli.py - CLI Tests

**Framework:** Click's CliRunner

**CLI Commands Tested:**
- `init`: Database initialization
- `create`: Node creation via CLI
- `get`: Node retrieval via CLI
- `list`: Node listing via CLI
- `db-status`: Storage status reporting
- `import-yaml`: YAML file importing
- `export-yaml`: Database to YAML export
- `sync-status`: YAML/DB synchronization

**Test Setup:**
- Starts PostgreSQL container
- Sets TODOWRITE_DATABASE_URL environment variable
- Cleans up database after each test

### Test Execution

```bash
# Run all tests
python -m pytest tests/ -v

# Run specific test file
python -m pytest tests/test_app.py -v

# Run with markers
python -m pytest -m "not slow" tests/
```

---

## 13. WORKFLOW AUTOMATION (Makefile)

Located: `$HOME/projects/ToDoWrite/Makefile`

### Key Targets

**Setup:**
- `tw-deps`: Install all dependencies
- `tw-init`: Initialize directory structure

**Validation Pipeline:**
- `tw-schema`: Generate JSON schema
- `tw-lint`: Run SoC linter
- `tw-validate`: Validate all YAML against schema
- `tw-trace`: Build traceability matrix
- `tw-prove`: Generate command stubs
- `tw-check`: Full strict validation
- `tw-all`: Run schema, lint, validate, trace, prove

**Development Workflow:**
- `tw-dev`: lint + validate + prove (fast iteration)
- `tw-prod`: all + check (production-ready)

**Testing & Cleanup:**
- `tw-test`: Run pytest suite
- `tw-clean`: Remove generated files

---

## 14. INTEGRATION ARCHITECTURE

### Data Flow Diagram

```
CLI Input
    ↓
Click Commands (cli.py)
    ↓
ToDoWrite App (app.py)
    ├─→ Validation (jsonschema)
    ├─→ Storage Router
    │   ├─→ PostgreSQL (preferred)
    │   ├─→ SQLite (fallback)
    │   └─→ YAML (last resort)
    ├─→ CRUD Operations
    └─→ YAML Manager (import/export)

Tools (Parallel):
    ├─→ Schema Validator (tw_validate.py)
    ├─→ SoC Linter (tw_lint_soc.py)
    ├─→ Traceability Builder (tw_trace.py)
    └─→ Command Generator (tw_stub_command.py)
```

### Storage Fallback Chain

```python
if STORAGE_PREFERENCE == "postgresql_only":
    Use PostgreSQL or raise error
elif STORAGE_PREFERENCE == "sqlite_only":
    Use SQLite or raise error
elif STORAGE_PREFERENCE == "yaml_only":
    Use YAML files
else:  # AUTO (default)
    Try PostgreSQL → Try SQLite → Fall back to YAML
```

### Auto-Import on Startup

When using database storage and auto_import=True:
1. Check which YAML files exist in configs/plans/ and configs/commands/
2. Get all existing node IDs from database
3. Identify YAML-only files (not in database)
4. Import missing YAML files automatically
5. Silently fail if database unavailable (doesn't break startup)

---

## 15. 12-LAYER PLANNING FRAMEWORK

### Layer Hierarchy

```
1. Goal              (Top-level objective)
2. Concept           (Design concept)
3. Context           (Operating context)
4. Constraints       (Limitations and rules)
5. Requirements      (Functional/non-functional requirements)
6. AcceptanceCriteria (Definition of done)
7. InterfaceContract (API/interface specification)
8. Phase             (Work phases/milestones)
9. Step              (Individual steps)
10. Task            (Assignable work units)
11. SubTask         (Task decomposition)
12. Command         (Executable operations)
```

### Separation of Concerns Principle

**Layers 1-11 (Non-Executable Planning):**
- Pure documentation/specification
- No shell commands, Python code execution
- Declarative nature
- Build-time validation only

**Layer 12 (Command/Execution):**
- Only layer with executable content
- Contains shell commands to verify/test AC
- References parent Acceptance Criteria
- Generates artifacts

---

## 16. EXTENSION POINTS

### Adding New Layer Types

1. Update `LayerType` in `app.py`
2. Update schema in `configs/schemas/todowrite.schema.json`
3. Add layer directory in `configs/plans/`
4. Add layer to `layer_dirs` mapping in `YAMLStorage` and `YAMLManager`
5. Add layer to database models (Node.layer)
6. Create factory method in `ToDoWrite` class

### Adding New CLI Commands

1. Add Click command function in `cli.py`
2. Decorate with `@cli.command()` or `@todowrite.command()`
3. Use Click decorators for options/arguments
4. Access ToDoWrite app: `app = ToDoWrite()`

### Adding New Validation Rules

1. Update JSON schema in `configs/schemas/todowrite.schema.json`
2. Add custom validator in `ToDoWriteValidator` if needed
3. Update tests in `tests/test_app.py`

### Adding New Tools

1. Create new Python file in `todowrite/tools/`
2. Implement main() function
3. Add to CLI via subprocess call in `cli.py`
4. Add Makefile target

---

## 17. KEY INTEGRATION POINTS

### ToDoWrite ↔ YAMLStorage
- When storage_type == StorageType.YAML
- Uses same Node dataclass
- Identical interface (load/save/delete)

### ToDoWrite ↔ YAMLManager
- Import: YAMLManager → ToDoWrite.[REMOVED_LEGACY_PATTERN]()
- Export: ToDoWrite.get_all_nodes() → YAMLManager
- Sync check: Compare file lists with node IDs

### ToDoWrite ↔ Database
- SQLAlchemy ORM for persistence
- Session management via context manager
- Automatic eager loading of relationships (joinedload)

### CLI ↔ ToDoWrite
- All CLI commands instantiate ToDoWrite()
- Respect storage preference from command options
- Pass data through Node dataclasses

### Tools ↔ File System
- All tools scan configs/plans/ and configs/commands/
- Parse YAML directly (no database access)
- Output to trace/ and results/ directories

---

## 18. EXAMPLE USAGE PATTERNS

### Programmatic Usage

```python
from todowrite import ToDoWrite

# Initialize with auto-import
app = ToDoWrite(auto_import=True)

# Create database
app.init_database()

# Create a goal
goal = app.add_goal(
    title="Build Feature X",
    description="Implement feature X with tests",
    owner="alice@example.com",
    labels=["feature", "high-priority"]
)

# Create phase
phase = app.add_phase(
    parent_id=goal.id,
    title="Design Phase",
    description="Design the architecture",
    owner="alice@example.com"
)

# Create task
task = app.add_task(
    parent_id=phase.id,
    title="Design Database Schema",
    description="Design the data model",
)

# Get node
node = app.get_node(task.id)

# Update node status
node_data = {
    "id": task.id,
    "layer": "Task",
    "title": "Design Database Schema",
    "description": "Design the data model",
    "status": "in_progress",
    "links": {"parents": [phase.id], "children": []},
    "metadata": {"owner": "alice@example.com", "labels": []}
}
app.update_node(task.id, node_data)

# Load all todos
todos = app.load_todos()

# Get active items
active = app.get_active_items(todos)
```

### CLI Usage

```bash
# Initialize
todowrite init

# Create nodes
todowrite create Goal "Build Feature X" "Implement feature X"
todowrite create Task "Design DB" "Design schema" --parent GOAL-ABC123

# View nodes
todowrite get GOAL-ABC123
todowrite list

# Database status
todowrite db-status
todowrite db-status --storage-preference postgresql_only

# Validation
todowrite todowrite validate-plan --strict
todowrite todowrite check-soc
todowrite todowrite trace-links --summary

# Command generation and execution
todowrite todowrite generate-commands
todowrite todowrite execute-commands --all
todowrite todowrite execute-commands CMD-EXAMPLE

# YAML sync
todowrite import-yaml --dry-run
todowrite export-yaml --output-dir ./configs
todowrite sync-status

# Hierarchy display
todowrite todowrite show-hierarchy
todowrite todowrite show-hierarchy --layer Task --format json
```

---

## 19. SECURITY & TYPE SAFETY

### Type Safety

- **Python 3.12+** with strict type hints
- **MyPy** in strict mode:
  - `disallow_untyped_defs`: All functions must have type hints
  - `strict_equality`: Prevents common comparison errors
  - All standard strict checks enabled
- **Type annotations** on all classes, methods, parameters
- **Literal types** for constrained values (LayerType, StatusType)

### Security Considerations

- **Bandit security linter** integration
- **SoC enforcement** prevents code injection in layers 1-11
- **Pattern matching** for dangerous Python/shell commands
- **YAML safe_load** (not unsafe load)
- **SQL injection prevention** via SQLAlchemy ORM (parameterized queries)
- **Input validation** via JSON schema
- **Pre-commit hooks** for code quality

### Database Credentials

- Docker compose uses development credentials (todowrite/todowrite_dev_password)
- Environment variables override hardcoded defaults
- No credentials in source code
- pgAdmin optional, development-only

---

## 20. PERFORMANCE & SCALABILITY

### Database Optimization

- **SQLAlchemy joinedload**: Eager loading of relationships
  - Prevents N+1 queries
  - Example: `joinedload(DBNode.labels).joinedload(DBNode.command)`
- **Composite keys** for Link and Artifact tables (efficient JOINs)
- **Index on Node.layer** (query filter)
- **Transaction batching** for bulk operations

### YAML Storage

- Single file per node (no full table scans)
- File-based filtering by directory (layer grouping)
- Suitable for small-to-medium projects (< 10K nodes)

### Scalability Path

1. Small projects: YAML storage (no setup)
2. Growing projects: SQLite (single file, no server)
3. Production: PostgreSQL (enterprise-grade)

---

## Summary of Key Files

| Path | Purpose |
|------|---------|
| `todowrite/cli.py` | Click CLI with all commands |
| `todowrite/app.py` | Core ToDoWrite application logic |
| `todowrite/db/models.py` | SQLAlchemy ORM models |
| `todowrite/db/config.py` | Storage backend detection & config |
| `todowrite/yaml_storage.py` | YAML-based storage implementation |
| `todowrite/yaml_manager.py` | YAML import/export management |
| `todowrite/tools/tw_validate.py` | Schema validation tool |
| `todowrite/tools/tw_lint_soc.py` | SoC compliance checker |
| `todowrite/tools/tw_trace.py` | Traceability matrix builder |
| `todowrite/tools/tw_stub_command.py` | Command stub generator |
| `configs/schemas/todowrite.schema.json` | JSON schema for nodes |
| `pyproject.toml` | Project configuration |
| `Makefile` | Workflow automation |
| `docker-compose.yml` | PostgreSQL setup |
| `tests/test_app.py` | Application tests |
| `tests/test_cli.py` | CLI tests |

---

**End of Exploration Report**
