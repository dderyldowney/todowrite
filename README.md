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

### Standalone CLI Application

Execute ToDoWrite directly from the command line:

```bash
# Initialize the database
todowrite init

# Create a new goal
todowrite create Goal "My new goal" "This is a test goal."

# Get a node by its ID
todowrite get <node_id>

# List all nodes
todowrite list
```

### Python Module Integration

Import and use ToDoWrite in your Python applications:

```python
from todowrite.app import ToDoWrite

# Initialize the application
app = ToDoWrite()

# Initialize the database
app.init_database()

# Create a new goal
node_data = {
    "id": "goal1",
    "layer": "Goal",
    "title": "Test Goal",
    "description": "A test goal",
    "status": "in_progress",
    "links": {"parents": [], "children": []},
    "metadata": {
        "owner": "test",
        "labels": ["test"],
        "severity": "high",
        "work_type": "architecture",
    },
}
node = app.create_node(node_data)
print(f"Created node: {node.id}")

# Get a node by its ID
retrieved_node = app.get_node("goal1")
print(f"Retrieved node: {retrieved_node.title}")

# Get all nodes
all_nodes = app.get_all_nodes()
print(f"All nodes: {all_nodes}")
```

## 🗄️ Database Configuration

### SQLite (Default)
Perfect for development and single-user scenarios:

```python
# Uses default SQLite database
# No configuration needed - works out of the box
from todowrite.app import ToDoWrite
app = ToDoWrite()
```

### PostgreSQL (Production)
For production environments and multi-user access:

```bash
# Set environment variable
export TODOWRITE_DATABASE_URL="postgresql://user:password@localhost:5432/todowrite_db"
```

```python
# Or configure programmatically
from todowrite.app import ToDoWrite
db_url = "postgresql://user:password@localhost:5432/todowrite_db"
app = ToDoWrite(db_url)
```

## 🏛️ Architecture

### Core Components

- **Application Layer**: High-level API for task management operations
- **Database Models**: Type-safe SQLAlchemy 2.0 models with relationships
- **Configuration System**: Environment-based database configuration
- **CLI Interface**: Simple command-line access to core functionality

## 🔧 Development

### Prerequisites
- Python 3.12+
- SQLAlchemy 2.0+
- Click 8.0+
- Psycopg2 (for PostgreSQL support)

### Development Installation
```bash
git clone https://github.com/dderyldowney/todowrite.git
cd todowrite
pip install -e .
```

### Testing

Run the tests with `pytest`:

```bash
python -m pytest
```

To run the PostgreSQL integration tests, you need to have a PostgreSQL database running.
You can use the provided `docker-compose.yml` file to start a PostgreSQL container:

```bash
docker-compose up -d
```

Then, run the tests:

```bash
python -m pytest
```

After running the tests, you can stop the container with:

```bash
docker-compose down
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

---

**Version**: 0.1.5
**Python**: 3.12+
**Database**: SQLite (development) / PostgreSQL (production)
**Architecture**: Hierarchical task management with 12-layer planning framework
