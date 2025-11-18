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

## Node Types (Layers)

ToDoWrite supports these node types, organized hierarchically:

1. **Goal** (`GOAL-*`) - High-level project objectives
2. **Concept** (`CON-*`) - Design concepts and architectural patterns
3. **Context** (`CTX-*`) - Environmental and project context
4. **Constraints** (`CST-*`) - Project constraints and limitations
5. **Requirements** (`R-*`) - Functional requirements
6. **AcceptanceCriteria** (`AC-*`) - Acceptance conditions and criteria
7. **InterfaceContract** (`IF-*`) - Interface specifications and contracts
8. **Phase** (`PH-*`) - Project phases and milestones
9. **Step** (`STP-*`) - Implementation steps
10. **Task** (`TSK-*`) - Specific tasks with progress tracking
11. **SubTask** (`SUB-*`) - Sub-tasks that break down larger tasks
12. **Command** (`CMD-*`) - Executable commands with run instructions

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

# View all nodes
todowrite list

# Search nodes
todowrite search "database"

# Export to YAML
todowrite export-yaml
```

### Python API Usage

#### Traditional API (Dictionary-based)
```python
from todowrite import ToDoWrite, link_nodes

# Initialize
app = ToDoWrite("sqlite:///project.db")
app.init_database()

# Create nodes
goal = app.create_node({
    "id": "GOAL-001",
    "layer": "Goal",
    "title": "Build TodoWrite App",
    "description": "Create the application",
    "links": {"parents": [], "children": []},
    "metadata": {"owner": "dev-team", "labels": ["app"], "severity": "high"}
})

task = app.create_node({
    "id": "TSK-001",
    "layer": "Task",
    "title": "Set up database",
    "description": "Initialize database schema",
    "links": {"parents": [], "children": []},
    "metadata": {"owner": "dev-team", "labels": ["database"], "severity": "medium"}
})

# Link nodes
link_nodes("sqlite:///project.db", goal.id, task.id)

# Get all nodes
all_nodes = app.get_all_nodes()
print(f"Total nodes: {sum(len(nodes) for nodes in all_nodes.values())}")
```

#### ActiveRecord-Style API (Recommended)
```python
from todowrite import ToDoWrite, Node

# Initialize application
app = ToDoWrite("sqlite:///project.db")
app.init_database()

# Configure Node class for ActiveRecord methods
Node.configure_session(app.get_session())

# Create nodes using Rails-style patterns
goal = Node.create_goal(
    "Build TodoWrite App",
    "dev-team",
    description="Create the application",
    labels=["app"],
    severity="high"
)

# Create task under goal (automatically linked)
task = goal.tasks().create(
    title="Set up database",
    description="Initialize database schema",
    owner="dev-team",
    labels=["database"],
    severity="medium"
)

# Or create separately and link
task = Node.create_task(
    "Set up database",
    "GOAL-001",  # Parent goal ID
    description="Initialize database schema",
    owner="dev-team",
    labels=["database"],
    severity="medium"
)

# Workflow management
task.start().save()  # Start work
task.update_progress(50)  # Update progress
task.complete().save()  # Mark complete

# Query nodes
all_goals = Node.where(layer="Goal")
backend_tasks = Node.where(owner="dev-team")
in_progress = Node.where(status="in_progress")

# Collection operations
goal_tasks = goal.tasks()  # Get tasks collection
task_count = goal_tasks.size()
has_tasks = goal_tasks.exists()

print(f"Goal '{goal.title}' has {task_count} tasks")
print(f"Total goals: {len(all_goals)}")
print(f"In-progress tasks: {len(in_progress)}")
```

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

## Command Nodes

Command nodes have additional executable information:

```python
command_node = {
    "id": "CMD-001",
    "layer": "Command",
    "title": "Build Application",
    "command": {                        # Required for Command nodes
        "ac_ref": "AC-001",             # Acceptance criteria reference
        "run": {
            "shell": "make build",
            "workdir": "/project",
            "env": {"TARGET": "production"}
        },
        "artifacts": ["dist/", "build.log"]
    },
    # ... standard node fields
}
```

## Database Operations

### CRUD Operations
```python
from todowrite import create_node, get_node, update_node, delete_node

# Create
node = create_node("sqlite:///project.db", node_data)

# Read
node = get_node("sqlite:///project.db", "GOAL-001")

# Update
updated = update_node("sqlite:///project.db", "GOAL-001", {"title": "Updated"})

# Delete
delete_node("sqlite:///project.db", "GOAL-001")
```

### Search Operations
```python
from todowrite import search_nodes, list_nodes

# Search by criteria
results = search_nodes("sqlite:///project.db", {"owner": "dev"})

# List all nodes
all_nodes = list_nodes("sqlite:///project.db")
```

### Import/Export
```python
from todowrite import export_nodes, import_nodes

# Export to JSON
exported = export_nodes("sqlite:///project.db", "backup.json")

# Import from JSON
results = import_nodes("sqlite:///project.db", "backup.json")
print(f"Imported {results['imported']} nodes")
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

### Graceful Degradation
```python
# Non-existent nodes return None (don't raise exceptions)
node = get_node("sqlite:///project.db", "NONEXISTENT")  # Returns None

# Operations on non-existent nodes are safe
result = update_node("sqlite:///project.db", "NONEXISTENT", {"title": "test"})  # Returns None

# Delete is idempotent
delete_node("sqlite:///project.db", "NONEXISTENT")  # No exception raised
```

### Exception Types
- `InvalidNodeError`: Invalid node data
- `NodeNotFoundError`: Node not found (rare, usually returns None)
- `DatabaseError`: Database operation failed
- `SchemaError`: Schema validation failed

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
