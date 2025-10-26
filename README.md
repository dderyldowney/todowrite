# ToDoWrite: Hierarchical Task Management System

[![Python 3.12+](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/)
[![Version 0.1.5](https://img.shields.io/badge/version-0.1.5-green.svg)](https://github.com/dderyldowney/todowrite)
[![SQLAlchemy 2.0](https://img.shields.io/badge/SQLAlchemy-2.0-orange.svg)](https://www.sqlalchemy.org/)

**ToDoWrite** is a sophisticated hierarchical task management system designed for complex project planning and execution. Built with a 12-layer declarative framework, it provides both standalone CLI capabilities and Python module integration for developers and project managers who need structured, traceable task management.

## 🎯 Overview

ToDoWrite transforms complex project planning into a structured, hierarchical framework that ensures nothing falls through the cracks. Whether you're managing software development projects, or any complex multi-stage initiative, ToDoWrite provides the structure and tools to break down goals into actionable commands.

### Key Features

- **12-Layer Hierarchical Framework**: From high-level goals to executable commands
- **Dual Interface**: Standalone CLI application and Python module
- **Database Flexibility**: SQLite for development, PostgreSQL for production
- **Type Safety**: Comprehensive type hints with Python 3.12+ syntax
- **Status Tracking**: Full lifecycle management with status transitions
- **Relationship Management**: Parent-child relationships with link validation

## 🏗️ Hierarchical Planning Framework

ToDoWrite organizes work into 12 distinct layers, each serving a specific purpose in the planning hierarchy:

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

### CLI Usage Guide

For detailed information on using the `todowrite` command-line interface, refer to the [CLI Reference](docs/cli_reference.md).

### Python Module Integration

ToDoWrite can be seamlessly integrated into your Python applications. Here are some examples:

```python
from todowrite.app import ToDoWrite

# Initialize the application (defaults to SQLite)
app = ToDoWrite()

# Initialize the database (creates tables)
app.init_database()

# Add a new Goal
goal = app.add_goal(
    title="Implement Feature X",
    description="Develop and integrate Feature X into the main product.",
    owner="Alice",
    labels=["feature", "backend"]
)
print(f"Created Goal: {goal.title} (ID: {goal.id})")

# Add a Phase linked to the Goal
phase = app.add_phase(
    parent_id=goal.id,
    title="Design Phase",
    description="Outline the architecture and technical specifications.",
    owner="Bob"
)
print(f"Created Phase: {phase.title} (ID: {phase.id})")

# Add a Task linked to the Phase
task = app.add_task(
    parent_id=phase.id,
    title="Database Schema Design",
    description="Design and implement the database schema for Feature X."
)
print(f"Created Task: {task.title} (ID: {task.id})")

# Get a node by its ID
retrieved_node = app.get_node(goal.id)
if retrieved_node:
    print(f"Retrieved Node: {retrieved_node.title} (Layer: {retrieved_node.layer})")

# Get all nodes and display active items
all_nodes = app.load_todos()
print("\nAll Nodes by Layer:")
for layer, nodes_list in all_nodes.items():
    print(f"  --- {layer} ({len(nodes_list)} items) ---")
    for n in nodes_list:
        print(f"    - {n.title} (Status: {n.status})")

active_items = app.get_active_items(all_nodes)
print("\nActive Items:")
for layer, active_node in active_items.items():
    print(f"  - {layer}: {active_node.title} (Status: {active_node.status})")

# Update a node's status
updated_goal = app.update_node(goal.id, {"status": "in_progress"})
if updated_goal:
    print(f"\nUpdated Goal {updated_goal.title} status to: {updated_goal.status}")

# Delete a node
app.delete_node(task.id)
print(f"\nDeleted Task: {task.title}")
```

## 🗄️ Database Configuration

ToDoWrite supports both SQLite and PostgreSQL. The database connection is configured via the `db_url` parameter in the `ToDoWrite` constructor or by setting the `TODOWRITE_DATABASE_URL` environment variable.

### SQLite (Default)

SQLite is used by default for convenience, especially during development or for single-user scenarios. No explicit configuration is needed.

```python
from todowrite.app import ToDoWrite

# Uses default SQLite database (e.g., todowrite.db in the current directory)
app = ToDoWrite()
```

### PostgreSQL

For production environments or multi-user access, PostgreSQL is recommended. You can configure it by providing a PostgreSQL connection string.

**Using Environment Variable (Recommended for Deployment):**

```bash
export TODOWRITE_DATABASE_URL="postgresql://user:password@localhost:5432/todowrite_db"
# Then, initialize ToDoWrite without arguments
# from todowrite.app import ToDoWrite
# app = ToDoWrite()
```

**Configuring Programmatically:**

```python
from todowrite.app import ToDoWrite

db_url = "postgresql://user:password@localhost:5432/my_todowrite_db"
app = ToDoWrite(db_url)
```

## 🏛️ Architecture

For a detailed overview of the project's architecture, including its core components, data flow, and database agnosticism, please refer to the [Architectural Overview](docs/architecture.md).

## 🔧 Development

### Prerequisites
- Python 3.12+
- SQLAlchemy 2.0+
- Click 8.0+
- Psycopg2 (for PostgreSQL support)
- Docker (for PostgreSQL integration tests)

### Development Installation
```bash
git clone https://github.com/dderyldowney/todowrite.git
cd todowrite
pip install -e .
```

### Testing

ToDoWrite includes a comprehensive test suite to ensure functionality and database compatibility. All tests, including PostgreSQL integration tests, can be run using `pytest`.

**Running All Tests:**

To run all tests, including those that require a PostgreSQL database, ensure Docker is running and then execute:

```bash
python -m pytest
```

This command will automatically start a PostgreSQL container, run the tests against it, and then stop the container. If you wish to run tests against SQLite, you can temporarily unset the `TODOWRITE_DATABASE_URL` environment variable or modify the test files directly.

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

---

**Version**: 0.1.5
**Python**: 3.12+
**Database**: SQLite (development) / PostgreSQL (production)
**Architecture**: Hierarchical task management with 12-layer planning framework