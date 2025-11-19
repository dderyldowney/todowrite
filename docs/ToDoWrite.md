# ToDoWrite — Hierarchical Task Management System

**Status:** PRODUCTION READY — Monorepo with Python library, CLI, and web interface for hierarchical task management
**Testing:** Comprehensive test suite with real implementations (no mocks) - component and subsystem organized
**Verification:** Complete library and CLI verification with enhanced configuration management
**Configuration:** Mandatory documentation loading and authoritative sources consultation enforced

---

## Overview

### System Version
- **Version:** See VERSION file for current version
- **Architecture:** Monorepo with hierarchical task management and database persistence
- **Packages:**
  - `todowrite` - Core Python library (lib_package)
  - `todowrite_cli` - Command-line interface (cli_package)
  - `todowrite_web` - Web application interface (web_package, planning stage)
- **Testing:** Component and subsystem organized test suite with real implementations, no mocking
- **Configuration:** Enhanced CLAUDE.md with mandatory rules for documentation, authoritative sources, and development practices

### What ToDoWrite Is
ToDoWrite is a hierarchical task management system that allows you to:
- Create and manage hierarchical relationships between goals, concepts, tasks, and commands
- Store data in SQLite, PostgreSQL databases with auto-import from YAML
- Use Python API, CLI interface, and upcoming web interface
- Import/export data in JSON and YAML formats
- Follow TDD methodology with Red-Green-Refactor workflow
- Use authoritative sources for all development decisions

### Key Principles
- **Database-First**: All data stored in SQL databases with proper relationships and auto-import
- **Schema Validated**: JSON Schema validation ensures data integrity
- **Type Safe**: Comprehensive type hints with Python 3.12+

### Development Standards
**See**: `.claude/CLAUDE.md` for complete development rules and policies
- **TDD Methodology**: Strict Red-Green-Refactor development workflow
- **Real Testing**: Component-organized tests with actual implementations
- **No Mocking/Fake Code**: Real implementations only, no placeholders
- **Documentation-Driven**: Consult authoritative sources for all decisions
- **Local Tools Preferred**: Use command-line tools over internal tools
- **Simplicity First**: Code and tests that read like natural language
- **Progressive Disclosure**: From high-level goals to detailed commands

## ToDoWrite Models Tables (2025 Design Update)

**NEW DESIGN (2025): Individual Tables Per Layer**

The ToDoWrite system uses the ToDoWrite Models API with **individual database tables** for each layer:

### ToDoWrite Models Tables (12 Layers)

| Layer | Table Name | Model Class | Description |
|------|------------|-------------|-------------|
| Goal | `goals` | `Goal` | High-level project objectives |
| Concept | `concepts` | `Concept` | Design concepts and architectural patterns |
| Context | `contexts` | `Context` | Environmental and project context |
| Constraints | `constraints` | `Constraints` | Project constraints and limitations |
| Requirements | `requirements` | `Requirements` | Functional requirements |
| AcceptanceCriteria | `acceptance_criteria` | `AcceptanceCriteria` | Acceptance conditions and criteria |
| InterfaceContract | `interface_contracts` | `InterfaceContract` | Interface specifications and contracts |
| Phase | `phases` | `Phase` | Project phases and milestones |
| Step | `steps` | `Step` | Implementation steps |
| Task | `tasks` | `Task` | Specific tasks with progress tracking |
| SubTask | `sub_tasks` | `SubTask` | Sub-tasks that break down larger tasks |
| Command | `commands` | `Command` | Executable commands with run instructions |

### ToDoWrite Models Design Benefits

**✅ Clean Database Design:**
- Each layer has its own table with clear separation of concerns
- Plural table names following database conventions (`goals`, not `goal`)
- Individual entries trackable by unique integer IDs

**✅ Database Primary Key Design:**
- `id INTEGER PRIMARY KEY AUTOINCREMENT` for every table
- IDs are **UNIQUE, NOT NULL, and NEVER REUSED** (referential integrity)
- Auto-incrementing sequence: 1, 2, 3, 4, 5...

**✅ Database Timestamp Fields:**
- `created_at` - Set once on creation, readonly afterward
- `updated_at` - Automatically updated on every save
- ISO format timestamps with timezone awareness

**✅ Database Relationship Design:**
- Many-to-many relationships through join tables
- Lexical naming: `goals_labels`, `concepts_labels`, etc.
- Bidirectional navigation: `goal.labels` and `label.goals` both work
- Foreign keys follow `model_name_id` pattern

**✅ Database Query Patterns:**
- Type-safe SQLAlchemy queries with full Python support
- Modern query methods
- Efficient relationship loading and caching

### Database Schema Example

```sql
-- Goals table (individual goals table)
CREATE TABLE goals (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title VARCHAR NOT NULL,
    description TEXT,
    status VARCHAR DEFAULT 'planned',
    progress INTEGER,
    owner VARCHAR,
    severity VARCHAR,
    work_type VARCHAR,
    assignee VARCHAR,
    extra_data TEXT,  -- JSON for complex data
    created_at VARCHAR NOT NULL,
    updated_at VARCHAR NOT NULL
);

-- Labels table (shared across all layers)
CREATE TABLE labels (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR NOT NULL UNIQUE,
    created_at VARCHAR NOT NULL,
    updated_at VARCHAR NOT NULL
);

-- Join table (lexical order, no primary key)
CREATE TABLE goals_labels (
    goal_id INTEGER NOT NULL REFERENCES goals(id),
    label_id INTEGER NOT NULL REFERENCES labels(id)
);
```

### Migration Notes

- **Legacy Support**: Old `Node` table remains for backward compatibility during migration
- **Data Integrity**: All foreign keys maintain referential integrity
- **Performance**: Individual tables enable better indexing and query optimization
- **Scalability**: Clean separation allows independent evolution of each layer

## Installation

### Core Library
```bash
pip install todowrite
```

### CLI Interface
```bash
pip install todowrite-cli
```

### With PostgreSQL Support
```bash
pip install 'todowrite[postgres]'
pip install 'todowrite-cli[postgres]'
```

### Development Installation
```bash
git clone https://github.com/dderyldowney/todowrite.git
cd todowrite
./setup_dev.sh
```

## Quick Start

### CLI Usage
```bash
# Initialize project (creates todowrite.db)
todowrite init

# Create a goal
todowrite create --layer goal --title "Build TodoWrite App" --description "Create the application" --owner "dev-team"

# Create a task
todowrite create --layer task --title "Set up database" --description "Initialize database schema" --owner "dev-team"

# View all items
todowrite list

# Search items
todowrite search "database"

# Export to YAML
todowrite export-yaml
```

### Python API Usage


#### ToDoWrite Models API (Recommended) - Updated Design

**NEW DESIGN (2025): Individual Tables per Layer**

The ToDoWrite system uses the ToDoWrite Models API with separate tables for each layer:

- **Pluralized tables**: `goals`, `concepts`, `contexts`, `constraints`, `requirements`, `acceptance_criteria`, `interface_contracts`, `phases`, `steps`, `tasks`, `sub_tasks`
- **Integer primary keys**: Auto-incrementing IDs that are never reused
- **Database timestamps**: `created_at` (readonly) and `updated_at` (writable)
- **Individual models**: Each layer has its own ToDoWrite Model class

```python
from todowrite.core.types import Goal, Task, Label

# Initialize database session
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine("sqlite:///project.db")
Session = sessionmaker(bind=engine)
session = Session()

# Create records using ToDoWrite Models patterns
goal = Goal(
    title="Build TodoWrite App",
    description="Create the application",
    owner="dev-team",
    severity="high"
)
session.add(goal)
session.commit()

print(f"Goal created with ID: {goal.id}")  # Outputs: Goal created with ID: 1

# Create task with relationship
task = Task(
    title="Set up database",
    description="Initialize database schema",
    owner="dev-team",
    severity="medium"
)
session.add(task)
session.commit()

print(f"Task created with ID: {task.id}")  # Outputs: Task created with ID: 1

# Add labels (many-to-many through join tables)
strategic_label = Label(name="strategic")
database_label = Label(name="database")
session.add_all([strategic_label, database_label])
session.commit()

goal.labels.append(strategic_label)
task.labels.extend([strategic_label, database_label])
session.commit()

# ToDoWrite Models queries
all_goals = session.query(Goal).all()
backend_tasks = session.query(Task).filter(Task.owner == "dev-team").all()
in_progress = session.query(Task).filter(Task.status == "in_progress").all()

# Bidirectional relationships work
print(f"Goal {goal.id} labels: {[l.name for l in goal.labels]}")
print(f"Label '{strategic_label.name}' goals: {[g.title for g in strategic_label.goals]}")

# Collection operations
task_count = len(goal.labels) if goal.labels else 0
print(f"Goal '{goal.title}' has {task_count} labels")

print(f"Total goals: {len(all_goals)}")
print(f"Backend tasks: {len(backend_tasks)}")
print(f"In-progress tasks: {len(in_progress)}")
```

**Key ToDoWrite Models Benefits:**

1. **Clean Database Design**: Each layer has its own table with auto-incrementing integer IDs
2. **Referential Integrity**: IDs are never reused, even after deletion
3. **Database Conventions**: Plural table names, timestamp fields, proper foreign keys
4. **Bidirectional Relationships**: `goal.labels` and `label.goals` both work
5. **Type Safety**: Full Python type hints for all models
6. **SQLAlchemy Integration**: Leverages powerful ORM features while maintaining ToDoWrite Models patterns

#### Method Chaining Examples
```python
# Create and complete in one chain
quick_task = Node.new(
    layer="Task",
    title="Quick fix",
    owner="dev"
).save().complete().save()

# Complex query chains
critical_backend_tasks = Node.where(
    layer="Task"
).where(
    owner="backend-team"
).where(
    severity="high"
)

# Business workflow chains
completed_critical_task = Node.new(
    layer="Task",
    title="Critical bug fix",
    owner="backend-team",
    severity="critical"
).save().start().save().update_progress(100).save().complete().save()
```

## Node Structure

All nodes follow this structure:

```python
node_data = {
    "id": "GOAL-001",                    # Required: Unique ID
    "layer": "Goal",                     # Required: Node type
    "title": "Node Title",               # Required: Title
    "description": "Description",        # Optional: Description
    "status": "planned",                 # Optional: Status
    "progress": 0,                       # Optional: Progress (0-100)
    "links": {
        "parents": [],                   # Parent node IDs
        "children": []                   # Child node IDs
    },
    "metadata": {
        "owner": "user",                 # Required: Owner
        "labels": ["label1"],            # Optional: Labels
        "severity": "medium",            # Optional: Severity
        "work_type": "implementation",   # Optional: Work type
        "assignee": "assignee"           # Optional: Assignee
    }
}
```

## Command Model - The Executable Layer

The Command model is the **only executable layer** in ToDoWrite, bridging planning with automation:

### Core Fields
- **`acceptance_criteria_id`**: Foreign key to parent AcceptanceCriteria (INTEGER)
- **`cmd`**: The executable script or command name (TEXT)
- **`cmd_params`**: Command parameters and arguments (TEXT)
- **`runtime_env`**: Environment variables and runtime configuration (TEXT)
- **`output`**: Command execution output (stdout/stderr) (TEXT)
- **`artifacts`**: Expected output files and generated artifacts (TEXT)

### Example Usage
```python
from todowrite import Command, AcceptanceCriteria, sessionmaker

# Find acceptance criteria
ac = session.query(AcceptanceCriteria).filter(
    AcceptanceCriteria.title == "User Authentication Complete"
).first()

# Create command for that acceptance criteria
cmd = Command(
    title="Run Authentication Tests",
    cmd="pytest",
    cmd_params="tests/auth/ -v",
    runtime_env='{"PYTHONPATH": "./src"}',
    acceptance_criteria_id=ac.id
)
session.add(cmd)
session.commit()
```
```

## Database Operations

### CRUD Operations (ToDoWrite Models Pattern)
```python
from todowrite import Goal, Task, create_engine, sessionmaker

# Initialize database session
engine = create_engine("sqlite:///project.db")
Session = sessionmaker(bind=engine)
session = Session()

# Create (ToDoWrite Models pattern)
goal = Goal(title="Build TodoWrite App", owner="dev-team", severity="high")
session.add(goal)
session.commit()

# Read
goal = session.query(Goal).filter(Goal.id == 1).first()

# Update
goal.title = "Updated Title"
session.commit()

# Delete
session.delete(goal)
session.commit()
```

### Search Operations (ToDoWrite Models Pattern)
```python
from todowrite import Goal, Task, create_engine, sessionmaker

# Initialize database session
engine = create_engine("sqlite:///project.db")
Session = sessionmaker(bind=engine)
session = Session()

# Search by criteria (ToDoWrite Models pattern)
results = session.query(Goal).filter(Goal.owner == "dev").all()
tasks = session.query(Task).filter(Task.status == "in_progress").all()

# List all items
all_goals = session.query(Goal).all()
all_tasks = session.query(Task).all()
```


## Validation

### Node Validation
```python
from todowrite.storage import validate_node_data

try:
    validate_node_data(node_data)
    print("Node data is valid")
except Exception as e:
    print(f"Invalid: {e}")
```

### ID Validation
Node IDs must follow the pattern: `{LAYER}-{IDENTIFIER}`
- Valid: `GOAL-PROJECT-COMPLETION`, `TSK-DATABASE-SETUP`
- Invalid: `random-node`, `123`, `INVALID-LAYER-001`

### Status Values
Valid statuses: `planned`, `in_progress`, `completed`, `blocked`, `cancelled`

### Severity Levels
Valid severities: `low`, `med`, `medium`, `high`, `critical`

## Storage

### SQLite (Default)
```python
app = ToDoWrite("sqlite:///project.db")
```

### PostgreSQL
```python
app = ToDoWrite("postgresql://user:password@localhost/projectdb")
```

### YAML Storage
```python
from todowrite.storage import YAMLManager

yaml_manager = YAMLManager("project.yaml")
yaml_manager.write_yaml({"nodes": {}})
data = yaml_manager.read_yaml()
```

## Performance

### Verified Characteristics
- **Node Creation**: 100 nodes in ~2.4 seconds
- **Node Retrieval**: 100 nodes in ~0.01 seconds
- **Individual Lookups**: 10 nodes in ~0.02 seconds
- **Test Suite**: 119 tests all passing

### Performance Considerations
- SQLite for development and smaller projects
- PostgreSQL for production and larger datasets
- Efficient indexing on node IDs and common fields

## Error Handling

### Graceful Degradation (ToDoWrite Models Pattern)
```python
# Non-existent records return None (don't raise exceptions)
goal = session.query(Goal).filter(Goal.id == 99999).first()  # Returns None

# Query operations are safe
results = session.query(Goal).filter(Goal.title == "Nonexistent").all()  # Returns []

# Operations check for existence before execution
goal = session.query(Goal).filter(Goal.id == 1).first()
if goal:
    session.delete(goal)  # Only executes if goal exists
    session.commit()
```

### Exception Types
- `SQLAlchemyError`: Database operation failed (SQLAlchemy exceptions)
- `IntegrityError`: Database constraint violation
- `OperationalError`: Database connection or operation error
- `ValueError`: Invalid data values

## Testing

### Test Organization
Tests are organized by monorepo packages and components:
```
tests/
├── lib/                    # todowrite package tests
│   ├── api/               # API interface tests
│   ├── core/              # Core functionality tests
│   ├── database/          # Database layer tests
│   ├── schema/            # Schema validation tests
│   ├── storage/           # Storage backend tests
│   └── tools/             # Tools and utilities tests
├── cli/                    # todowrite_cli package tests
├── web/                    # todowrite_web package tests
│   ├── api/               # Web API tests
│   ├── backend/           # Backend tests
│   ├── frontend/          # Frontend tests
│   ├── models/            # Web model tests
│   └── utils/             # Web utility tests
└── shared/                 # Shared test utilities and fixtures
```

### Run Tests
```bash
# Run all tests (component and subsystem organized)
./dev_tools/build.sh test

# Or directly with UV
uv run pytest tests/ --ignore=tests/web/

# Run specific package tests
uv run pytest tests/lib/ tests/cli/
```

### Test Results (Current)
- **Total Tests**: Comprehensive component-organized test suite
- **Pass Rate**: 100%
- **Implementation**: Real (no mocks, no fake code)
- **Organization**: Component and subsystem based with Separation of Concerns
- **Quality Gates**: TDD methodology enforced with Red-Green-Refactor workflow

### Test Categories
- `tests/lib/` - Core todowrite library tests (models, database, schema, storage, api)
- `tests/cli/` - todowrite_cli command-line interface tests
- `tests/web/` - todowrite_web web application tests (planning stage)
- `tests/shared/` - Shared test utilities, fixtures, and helpers

### Testing Strategy
**Implementation**: See `BUILD_SYSTEM.md` for detailed testing architecture

- **Component Organization**: Tests organized by packages (lib/, cli/, web/)
- **Real Implementations**: No mocking or fake code allowed
- **TDD Workflow**: Red → Green → Refactor methodology
- **Natural Language**: Tests that read like specifications
- **Test Commands**: Use `./dev_tools/build.sh test` or `uv run pytest`

## Configuration

### Environment Variables
```bash
# Override default database location
TODOWRITE_DATABASE_URL="sqlite:///custom.db"

# Override storage preference
TODOWRITE_STORAGE_PREFERENCE="sqlite_only"
```

### Default Behavior
- Creates `todowrite.db` in current directory for SQLite
- Uses SQLite as default storage backend
- Validates all node data against JSON schema
- Auto-generates node IDs if not provided

## Known Limitations

### Current Scope
- Local database storage only (no distributed features)
- No built-in web interface
- No multi-user authentication
- No real-time collaboration features

### Minor Issues
- Labels field gets cleared during node updates
- Some CLI commands have limited error messages

### Future Enhancements (Not Implemented)
- Web interface
- REST API
- Multi-user support
- Real-time updates

## Contributing

### Development Standards
- All tests must use real implementations (no mocking)
- 100% test pass rate required
- Static analysis compliance (Ruff for linting and formatting)
- Comprehensive schema validation
- Clear documentation for new features

### Quality Assurance
- Real database operations in all tests
- File system operations use actual files
- CLI tests use real command execution
- No simulated or mocked functionality

---

**Status**: ✅ Production Ready
**Version**: See VERSION file
**Tests**: All tests passing
**Implementation**: Real (no mocks)
**Verification**: Complete
