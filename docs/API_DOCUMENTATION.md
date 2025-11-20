# ToDoWrite API Documentation

**Version**: 0.6.0 - **MAJOR BREAKING CHANGE**
**Status**: Production Ready
**Testing**: Comprehensive test suite with real implementations

## Overview

ToDoWrite provides SQLAlchemy ORM interfaces for hierarchical task management with database persistence and schema validation. The system uses 12 hierarchical models with proper foreign key relationships.

## ⚠️ BREAKING CHANGES in v0.6.0

This version includes a **complete architectural redesign** that is **not backward compatible** with previous versions:

- **New Database Schema**: Completely redesigned relationships
- **Updated API Interfaces**: Modified method signatures and data structures
- **New Model Hierarchy**: Enhanced 12-layer system
- **Migration Required**: Existing databases need schema updates

## Core Models API

### SQLAlchemy Models

The 12 hierarchical layers are implemented as individual SQLAlchemy models:

```python
from todowrite import (
    Goal, Concept, Context, Constraints,
    Requirements, AcceptanceCriteria, InterfaceContract,
    Phase, Step, Task, SubTask, Command, Label,
    create_engine, sessionmaker
)

# Initialize database session
engine = create_engine("sqlite:///project.db")
Session = sessionmaker(bind=engine)
session = Session()
```

### Model Creation Examples

#### Creating a Goal
```python
# Create a goal
goal = Goal(
    title="Build User Authentication System",
    description="Implement secure user authentication with JWT tokens",
    status="planned",
    owner="dev-team",
    severity="high"
)
session.add(goal)
session.commit()
```

#### Creating a Command with Acceptance Criteria
```python
# Create acceptance criteria first
ac = AcceptanceCriteria(
    title="User Can Login",
    description="Users must be able to log in with valid credentials",
    status="pending"
)
session.add(ac)
session.commit()

# Create command for that acceptance criteria
command = Command(
    title="Run Authentication Tests",
    cmd="pytest",
    cmd_params="tests/auth/test_login.py -v",
    runtime_env='{"PYTHONPATH": "./src", "TEST_DB": "sqlite:///:memory:"}',
    acceptance_criteria_id=ac.id
)
session.add(command)
session.commit()
```

### Querying Models

#### Basic Queries
```python
# Get all goals
goals = session.query(Goal).all()

# Find a specific command
command = session.query(Command).filter(
    Command.title == "Run Authentication Tests"
).first()

# Get commands for specific acceptance criteria
commands = session.query(Command).filter(
    Command.acceptance_criteria_id == ac.id
).all()
```

#### Relationship Navigation
```python
# Navigate from goal to commands
goal = session.query(Goal).first()
for phase in goal.phases:
    for step in phase.steps:
        for task in step.tasks:
            for subtask in task.sub_tasks:
                for command in subtask.commands:
                    print(f"Command: {command.title} - {command.cmd}")
```

### Many-to-Many Relationships

#### Using Labels for Categorization
```python
# Create labels
strategic_label = Label(name="strategic")
technical_label = Label(name="technical")
session.add_all([strategic_label, technical_label])
session.commit()

# Associate labels with goals
goal.labels.extend([strategic_label, technical_label])
session.commit()

# Query goals by label
strategic_goals = session.query(Goal).join(Goal.labels).filter(
    Label.name == "strategic"
).all()
```

#### Complex Relationships
```python
# Get all concepts for a goal
goal_concepts = session.query(Concept).join(Concept.goals).filter(
    Goal.id == goal.id
).all()

# Get goals that have specific constraints
constrained_goals = session.query(Goal).join(Goal.constraints).filter(
    Constraints.severity == "critical"
).all()
```

### Database Operations

#### Schema Validation
```python
from todowrite import validate_model_data, DatabaseInitializationError

# Validate data before creation
command_data = {
    "title": "Deploy Application",
    "cmd": "docker-compose up",
    "acceptance_criteria_id": 1
}

try:
    is_valid = validate_model_data(command_data, "Command")
    if is_valid:
        command = Command(**command_data)
        session.add(command)
        session.commit()
except DatabaseInitializationError as e:
    print(f"Validation failed: {e}")
```

#### Database Initialization
```python
from todowrite import initialize_database

# Create all tables with proper foreign key constraints
try:
    initialize_database(engine)
    print("Database initialized successfully")
except Exception as e:
    print(f"Database initialization failed: {e}")
```

### Foreign Key Relationships

All relationships maintain referential integrity with proper foreign key constraints:

```python
# These relationships are enforced at the database level:
# - Command.acceptance_criteria_id -> AcceptanceCriteria.id
# - All association tables use REFERENCES model_name(id)

# Example of relationship that will fail if parent doesn't exist:
invalid_command = Command(
    title="Invalid Command",
    acceptance_criteria_id=999  # This will fail if AC 999 doesn't exist
)
# session.add(invalid_command)  # DatabaseError: foreign key constraint violation
```

### Command Execution Pattern

Commands are the **only executable layer** in ToDoWrite:

```python
# Execute commands and store results
def execute_command(command: Command) -> None:
    """Execute a command and store the output."""
    import subprocess
    import json

    try:
        # Parse runtime environment
        env = json.loads(command.runtime_env or "{}")

        # Execute command
        result = subprocess.run(
            f"{command.cmd} {command.cmd_params or ''}",
            shell=True,
            capture_output=True,
            text=True,
            env={**os.environ, **env}
        )

        # Store execution results
        command.output = f"STDOUT:\n{result.stdout}\nSTDERR:\n{result.stderr}"
        command.status = "completed" if result.returncode == 0 else "failed"

        # Update artifacts if expected files were created
        if command.artifacts:
            artifacts = json.loads(command.artifacts or "[]")
            created_files = []
            for file_path in artifacts:
                if Path(file_path).exists():
                    created_files.append(file_path)
            command.artifacts = json.dumps(created_files)

        session.commit()

    except Exception as e:
        command.output = f"Error: {str(e)}"
        command.status = "failed"
        session.commit()
```

## Schema Information

- **Total Tables**: 41 (12 model tables + 29 association tables)
- **Foreign Key Constraints**: 59 total REFERENCES ensuring referential integrity
- **Association Table Pattern**: `model1_model2` with `model_name_id INTEGER REFERENCES model_name(id)`

For complete schema details, see:
- `lib_package/src/todowrite/core/schemas/todowrite_models_schema.sql`
- `lib_package/src/todowrite/core/schemas/todowrite_models.schema.json`
