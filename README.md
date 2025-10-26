# ToDoWrite: Hierarchical Task Management System

[![Python 3.12+](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/)
[![Version 0.1.5](https://img.shields.io/badge/version-0.1.5-green.svg)](https://github.com/dderyldowney/todowrite)
[![SQLAlchemy 2.0](https://img.shields.io/badge/SQLAlchemy-2.0-orange.svg)](https://www.sqlalchemy.org/)

**ToDoWrite** is a sophisticated hierarchical task management system designed for complex project planning and execution. Built with a 10-layer declarative framework, it provides both standalone CLI capabilities and Python module integration for developers and project managers who need structured, traceable task management.

## 🎯 Overview

ToDoWrite transforms complex project planning into a structured, hierarchical framework that ensures nothing falls through the cracks. Whether you're managing agricultural robotics operations, software development projects, or any complex multi-stage initiative, ToDoWrite provides the structure and tools to break down goals into actionable commands.

### Key Features

- **10-Layer Hierarchical Framework**: From high-level goals to executable commands
- **Dual Interface**: Standalone CLI application and Python module
- **Database Flexibility**: SQLite for development, PostgreSQL for production
- **Type Safety**: Comprehensive type hints with Python 3.12+ syntax
- **Agricultural Optimization**: Purpose-built for agricultural robotics but universally applicable
- **Status Tracking**: Full lifecycle management with status transitions
- **Relationship Management**: Parent-child relationships with link validation

## 🏗️ Hierarchical Planning Framework

ToDoWrite organizes work into 10 distinct layers, each serving a specific purpose in the planning hierarchy:

### Planning Layers (Strategic)
1. **Goal** — High-level objectives and strategic outcomes
2. **Concept** — Core ideas and approaches
3. **Context** — Environmental factors and constraints
4. **Constraints** — Limitations and boundaries
5. **Requirements** — Specific needs and specifications
6. **Acceptance Criteria** — Success definitions and validation criteria
7. **Interface Contract** — APIs, schemas, and system interfaces

### Execution Layers (Tactical)
8. **Phase** — Major project phases and milestones
9. **Step** — Concrete implementation steps
10. **Task** — Specific work items
11. **SubTask** — Granular task breakdown
12. **Command** — Executable operations and scripts

### Status Types
Each layer supports comprehensive status tracking:
- `planned` — Initial state, ready for work
- `in_progress` — Currently being worked on
- `blocked` — Waiting for dependencies
- `done` — Successfully completed
- `rejected` — Decided not to proceed

## 📦 Installation

### As a Standalone Application
```bash
pip install todowrite
```

### For Development
```bash
git clone https://github.com/dderyldowney/todowrite.git
cd todowrite
pip install -e .
```

## 🚀 Usage

### Standalone CLI Application

Execute ToDoWrite directly from the command line:

```bash
# Run the main CLI
todowrite

# Run as a Python module
python -m todowrite
```

### Python Module Integration

Import and use ToDoWrite in your Python applications:

```python
import todowrite
from todowrite import manager

# Initialize the database
result = manager.init_database()
print(f"Database initialized: {result['status']}")

# Create a new goal
goal, error = manager.add_goal(
    title="Automate Field Operations",
    description="Implement autonomous tractor coordination for precision agriculture"
)
if goal:
    print(f"Created goal: {goal['title']} (ID: {goal['id']})")

# Add a phase to the goal
phase, error = manager.add_phase(
    goal_id=goal['id'],
    title="System Integration Phase",
    description="Integrate all subsystems and test coordination protocols"
)

# Add a step to the phase
step, error = manager.add_step(
    phase_id=phase['id'],
    name="Database Setup",
    description="Configure production database with proper schemas"
)

# Create a task
task, error = manager.add_task(
    step_id=step['id'],
    title="Deploy PostgreSQL",
    description="Set up PostgreSQL database with agricultural schemas"
)

# Add executable subtask with command
subtask, error = manager.add_subtask(
    task_id=task['id'],
    title="Install PostgreSQL",
    description="Install and configure PostgreSQL server",
    command="sudo apt-get install postgresql postgresql-contrib",
    command_type="bash"
)
```

### Working with the Hierarchy

```python
# Load all todos and inspect the hierarchy
todos = manager.load_todos()
for layer, nodes in todos.items():
    print(f"\n{layer} ({len(nodes)} items):")
    for node in nodes:
        print(f"  - {node.title} [{node.status}]")

# Get active items across all layers
active_items = manager.get_active_items(todos)
for layer, node in active_items.items():
    print(f"Active {layer}: {node.title}")

# Update node status
updated_node, error = manager.update_node(
    goal['id'],
    {"status": "in_progress"}
)

# Complete a phase
completed_phase, error = manager.complete_phase(phase['id'])
if completed_phase:
    print(f"Phase completed: {completed_phase.title}")
```

### Database Management

```python
# Get database information
db_info = manager.get_database_info()
print(f"Database type: {db_info['database_type']}")
print(f"Connection status: {db_info['connection_status']}")
print(f"Production ready: {db_info['supports_concurrent_access']}")

# Reset database for testing
manager.reset_database_engine()

# Reinitialize with clean state
init_result = manager.init_database()
```

### Advanced Usage Examples

#### Creating a Complete Project Structure

```python
# Create comprehensive project hierarchy
def create_project_structure() -> str:
    """Create a complete project structure and return the root goal ID."""

    # 1. Strategic Planning
    goal, _ = manager.add_goal(
        "Smart Irrigation System",
        "Develop autonomous irrigation control for precision agriculture"
    )

    concept, _ = manager.add_concept(
        "Sensor-Driven Automation",
        "Use soil moisture sensors to trigger irrigation events",
        goal_id=goal['id']
    )

    context, _ = manager.add_context(
        "Field Environment",
        "Variable soil conditions across 100-acre farm with center pivot system",
        concept_id=concept['id']
    )

    constraint, _ = manager.add_constraint(
        "Water Usage Limits",
        "Municipal water restrictions: max 50,000 gallons per week",
        context_id=context['id']
    )

    requirement, _ = manager.add_requirement(
        "Real-time Monitoring",
        "System must respond to sensor data within 5 minutes",
        constraint_id=constraint['id']
    )

    # 2. Implementation Planning
    phase, _ = manager.add_phase(
        goal_id=goal['id'],
        title="Sensor Network Deployment",
        description="Install and configure soil moisture sensors"
    )

    step, _ = manager.add_step(
        phase_id=phase['id'],
        name="Hardware Installation",
        description="Physical deployment of sensors in field"
    )

    task, _ = manager.add_task(
        step_id=step['id'],
        title="Sensor Calibration",
        description="Configure sensors for local soil conditions"
    )

    # 3. Executable Commands
    subtask, _ = manager.add_subtask(
        task_id=task['id'],
        title="Run Calibration Script",
        description="Execute automated sensor calibration",
        command="python scripts/calibrate_sensors.py --field=north --sensors=all",
        command_type="python"
    )

    return goal['id']

# Execute project creation
project_id = create_project_structure()
print(f"Created complete project structure with root goal: {project_id}")
```

#### Status Management and Reporting

```python
# Track project progress with type safety
def generate_status_report() -> None:
    """Generate a comprehensive status report for all goals."""
    goals = manager.get_goals()

    for goal in goals:
        print(f"\n📊 Goal: {goal['title']}")
        print(f"   Status: {goal['status']}")
        print(f"   Owner: {goal['owner']}")
        print(f"   Priority: {goal['priority']}")

        # Get all phases for this goal
        phases = manager.get_phases()
        goal_phases = [p for p in phases if goal['id'] in p.links.parents]

        for phase in goal_phases:
            print(f"   📋 Phase: {phase.title} [{phase.status}]")

# Mark items as complete with proper error handling
def complete_workflow() -> None:
    """Complete workflow items in proper hierarchical order."""
    todos = manager.load_todos()

    # Complete all commands first
    for command in todos.get('Command', []):
        if command.status == 'in_progress':
            result, error = manager.complete_command(command.id)
            if result:
                print(f"✅ Completed command: {command.title}")
            elif error:
                print(f"❌ Failed to complete command {command.title}: {error}")

    # Then complete higher-level items
    completion_layers = ['SubTask', 'Task', 'Step', 'Phase', 'Goal']

    for layer in completion_layers:
        for item in todos.get(layer, []):
            if item.status == 'in_progress':
                match layer:
                    case 'Goal':
                        result, error = manager.complete_goal(item.id)
                    case 'Phase':
                        result, error = manager.complete_phase(item.id)
                    case _:
                        # Add other completion functions as needed
                        continue

                if result:
                    print(f"✅ Completed {layer}: {item.title}")
                elif error:
                    print(f"❌ Failed to complete {layer} {item.title}: {error}")
```

#### Type-Safe Data Processing

```python
from typing import TypedDict

class ProjectMetrics(TypedDict):
    total_items: int
    completed_items: int
    in_progress_items: int
    completion_percentage: float

def calculate_project_metrics() -> ProjectMetrics:
    """Calculate project completion metrics with type safety."""
    todos = manager.load_todos()

    total_items = sum(len(nodes) for nodes in todos.values())
    completed_items = sum(
        len([node for node in nodes if node.status == 'done'])
        for nodes in todos.values()
    )
    in_progress_items = sum(
        len([node for node in nodes if node.status == 'in_progress'])
        for nodes in todos.values()
    )

    completion_percentage = (completed_items / total_items * 100) if total_items > 0 else 0.0

    return ProjectMetrics(
        total_items=total_items,
        completed_items=completed_items,
        in_progress_items=in_progress_items,
        completion_percentage=completion_percentage
    )

# Usage with pattern matching
metrics = calculate_project_metrics()
match metrics:
    case {"completion_percentage": percentage} if percentage >= 90:
        print(f"🎉 Project nearly complete: {percentage:.1f}%")
    case {"completion_percentage": percentage} if percentage >= 50:
        print(f"🚀 Project progressing well: {percentage:.1f}%")
    case {"completion_percentage": percentage}:
        print(f"📝 Project in early stages: {percentage:.1f}%")
```

## 🗄️ Database Configuration

### SQLite (Default)
Perfect for development and single-user scenarios:

```python
# Uses default SQLite database
# No configuration needed - works out of the box
import todowrite.manager as manager
```

### PostgreSQL (Production)
For production environments and multi-user access:

```bash
# Set environment variable
export TODOWRITE_DATABASE_URL="postgresql://user:password@localhost:5432/todowrite_db"
```

```python
# Or configure programmatically
import os
from todowrite.db.config import get_postgresql_url

# Generate PostgreSQL URL with type safety
db_url = get_postgresql_url(
    user="agricultural_user",
    password="secure_password",
    host="db.farm.example.com",
    database="farm_operations"
)

# Set environment variable
os.environ["TODOWRITE_DATABASE_URL"] = db_url

# Now imports will use PostgreSQL
import todowrite.manager as manager
```

### Database Settings
ToDoWrite includes optimized settings for both database types:

```python
from todowrite.db.config import AGRICULTURAL_DB_SETTINGS

# SQLite settings
sqlite_config = AGRICULTURAL_DB_SETTINGS["sqlite"]
# {"pool_pre_ping": True, "echo": False}

# PostgreSQL settings
postgres_config = AGRICULTURAL_DB_SETTINGS["postgresql"]
# {"pool_size": 10, "max_overflow": 20, "pool_pre_ping": True,
#  "pool_recycle": 3600, "echo": False}
```

## 🏛️ Architecture

### Core Components

- **Manager Layer**: High-level API for task management operations
- **Repository Pattern**: Data access abstraction with SQLAlchemy
- **Database Models**: Type-safe SQLAlchemy 2.0 models with relationships
- **Configuration System**: Environment-based database configuration
- **CLI Interface**: Simple command-line access to core functionality

### Data Model

```python
from dataclasses import dataclass, field
from typing import Literal

LayerType = Literal[
    "Goal", "Concept", "Context", "Constraints", "Requirements",
    "Acceptance Criteria", "Interface Contract", "Phase",
    "Step", "Task", "SubTask", "Command"
]

StatusType = Literal["planned", "in_progress", "blocked", "done", "rejected"]

@dataclass
class Node:
    id: str                         # Unique identifier
    layer: LayerType               # One of 10 hierarchical layers
    title: str                     # Human-readable name
    description: str               # Detailed description
    links: Link                    # Parent-child relationships
    metadata: Metadata             # Owner, labels, severity, work_type
    status: StatusType = "planned" # Current state
    command: Command | None = None # Optional executable command

@dataclass
class Link:
    parents: list[str] = field(default_factory=list)   # Parent node IDs
    children: list[str] = field(default_factory=list)  # Child node IDs

@dataclass
class Metadata:
    owner: str                                          # Responsible party
    labels: list[str] = field(default_factory=list)    # Categorization tags
    severity: str = ""                                  # Priority/importance level
    work_type: str = ""                                 # Type of work required

@dataclass
class Command:
    ac_ref: str                                         # Acceptance criteria reference
    run: dict[str, Any]                                # Execution parameters
    artifacts: list[str] = field(default_factory=list) # Output artifacts
```

### Type Safety

ToDoWrite uses comprehensive type hints and runtime validation with Python 3.12+ syntax:

```python
from typing import Any, Literal

# Literal types ensure only valid values
LayerType = Literal[
    "Goal", "Concept", "Context", "Constraints", "Requirements",
    "Acceptance Criteria", "Interface Contract", "Phase",
    "Step", "Task", "SubTask", "Command"
]

StatusType = Literal["planned", "in_progress", "blocked", "done", "rejected"]

# Runtime validation prevents invalid states
def _validate_literal(value: str, literal_type: type[Any]) -> str:
    """Validate that a value is one of the allowed literal values."""
    if value not in literal_type.__args__:
        raise ValueError(f"Invalid literal value: {value}")
    return value

# Modern union syntax for return types
def create_node(node_data: dict[str, Any]) -> tuple[Node | None, str | None]:
    """Create a new node, returning the node or an error message."""
    try:
        # Node creation logic
        pass
    except Exception as e:
        return None, str(e)
```

### Error Handling Patterns

```python
from typing import TypeAlias

# Type aliases for common patterns
NodeResult: TypeAlias = tuple[Node | None, str | None]
DatabaseResult: TypeAlias = dict[str, str | bool]

def handle_node_operation(operation_result: NodeResult) -> bool:
    """Handle the result of a node operation with pattern matching."""
    node, error = operation_result

    match (node, error):
        case (None, str(error_msg)):
            print(f"❌ Operation failed: {error_msg}")
            return False
        case (Node() as successful_node, None):
            print(f"✅ Operation succeeded: {successful_node.title}")
            return True
        case _:
            print("⚠️ Unexpected result pattern")
            return False
```

## 🔧 Development

### Prerequisites
- Python 3.12+
- SQLAlchemy 2.0+
- Alembic 1.8+
- Pydantic 2.0+

### Development Installation
```bash
git clone https://github.com/dderyldowney/todowrite.git
cd todowrite
pip install -e .
```

### Project Structure
```
todowrite/
├── __init__.py              # Package initialization
├── __main__.py              # Module execution entry point
├── main.py                  # CLI application main function
├── manager.py               # Core management API (1,559 lines)
├── db/
│   ├── __init__.py         # Database package
│   ├── config.py           # Database configuration
│   ├── models.py           # SQLAlchemy models
│   └── repository.py       # Repository pattern implementation
└── tools/
    └── extract_schema.py   # Schema extraction utilities
```

### Testing Installation

```bash
# Verify installation
pip show todowrite

# Test standalone command
todowrite

# Test module execution
python -m todowrite

# Test Python import
python -c "import todowrite; print('✅ Import successful')"
```

### Database Migrations

ToDoWrite includes Alembic support for database schema management:

```python
# Initialize database with latest schema
result = manager.init_database()
print(f"Database status: {result['status']}")
print(f"Database type: {result['database_type']}")
```

## 🤝 Contributing

ToDoWrite follows strict quality standards:

1. **Type Safety**: All code must include comprehensive Python 3.12+ type hints
2. **Documentation**: Functions and classes require docstrings
3. **Testing**: New features need corresponding tests
4. **Database Compatibility**: Changes must work with both SQLite and PostgreSQL

### Code Style
- Python 3.12+ features and syntax
- Modern union syntax (`|` instead of `Union`)
- SQLAlchemy 2.0 patterns
- Dataclasses for data modeling
- Comprehensive error handling with pattern matching

### Development Workflow

```python
# Example of modern Python 3.12+ patterns in ToDoWrite
from typing import TypedDict, TypeAlias

class TaskSummary(TypedDict):
    id: str
    title: str
    status: StatusType
    completion_date: str | None

TaskList: TypeAlias = list[TaskSummary]

def get_task_summaries(layer: LayerType) -> TaskList:
    """Get task summaries for a specific layer using modern syntax."""
    todos = manager.load_todos()

    return [
        TaskSummary(
            id=node.id,
            title=node.title,
            status=node.status,
            completion_date=getattr(node.metadata, 'date_completed', None)
        )
        for node in todos.get(layer, [])
    ]
```

## 📝 License

ToDoWrite is designed for agricultural robotics applications but is suitable for any hierarchical project management needs.

## 🔗 Related Projects

- **Agricultural Robotics Platform**: Production implementation using ToDoWrite
- **Multi-Tractor Coordination**: Distributed systems built on ToDoWrite framework
- **ISOBUS Compliance**: Agricultural equipment integration using ToDoWrite planning

---

**Version**: 0.1.5
**Python**: 3.12+
**Database**: SQLite (development) / PostgreSQL (production)
**Architecture**: Hierarchical task management with 10-layer planning framework