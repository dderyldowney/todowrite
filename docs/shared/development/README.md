# Development Guide

**Comprehensive development guide for the ToDoWrite hierarchical task management system with SQLAlchemy ORM.**

---

## 🏗️ Architecture Overview

ToDoWrite uses a **SQLAlchemy ORM architecture** with individual database tables for each hierarchical layer:

- **12 Individual Models** - One for each layer of the hierarchy
- **Database-agnostic storage** - SQLite and PostgreSQL support
- **SQLAlchemy query interfaces** - Type-safe database operations
- **Proper foreign key relationships** - Enforced referential integrity
- **Many-to-many associations** - Through join tables
- **Schema validation** - JSON schema validation for all models

### Key Components

#### Models (`lib_package/src/todowrite/core/models.py`)
- **12 Hierarchical Models** - Goal, Concept, Context, Constraints, Requirements, AcceptanceCriteria, InterfaceContract, Phase, Step, Task, SubTask, Command
- **Label Model** - Shared categorization system
- **Relationships** - SQLAlchemy associations and join tables
- **Type Safety** - Full Python type hints

#### Database Layer
- **SQLAlchemy ORM** - Professional database ORM
- **Database Engines** - SQLite and PostgreSQL support
- **Session Management** - Connection and transaction handling
- **Schema Generation** - Automated table creation

## 🚀 Development Workflow

### Environment Setup
```bash
# Clone repository
git clone https://github.com/dderyldowney/todowrite.git
cd todowrite

# Setup development environment
./dev_tools/build.sh install

# Install todowrite library in development mode
cd lib_package && uv pip install -e . && cd ..
```

### Project Structure
```
todowrite/
├── lib_package/src/todowrite/          # Core library
│   ├── core/                           # SQLAlchemy models and core functionality
│   │   ├── models.py                  # 12 hierarchical models + Label
│   │   ├── exceptions.py              # Custom exception classes
│   │   ├── schemas/                   # JSON and SQL schema files
│   │   └── types.py                   # Type definitions
│   ├── database/                      # Database layer
│   │   ├── connection.py              # Database connections
│   │   └── initialization.py          # Database setup
│   ├── storage/                       # Storage backends
│   └── tools/                         # Utilities and schema generator
├── cli_package/src/todowrite_cli/     # CLI interface
└── web_package/                        # Web application (planning)
```

## 📋 Development Tasks

### Running Tests
```bash
# Run all tests
./dev_tools/build.sh test

# Run specific test suites
uv run pytest tests/lib/core/test_models.py -v
uv run pytest tests/lib/database/test_migrations.py -v
```

### Building Documentation
```bash
# Build Sphinx documentation
./dev_tools/build.sh docs

# View locally
open docs/sphinx/build/html/index.html
```

### Code Quality
```bash
# Full development workflow
./dev_tools/build.sh dev

# Linting and formatting
./dev_tools/build.sh format
./dev_tools/build.sh lint
```

## 🔧 SQLAlchemy ORM Features

### Model Usage
```python
from todowrite import (
    Goal, Task, Label, create_engine, sessionmaker
)

# Initialize database session
engine = create_engine("sqlite:///project.db")
Session = sessionmaker(bind=engine)
session = Session()

# Create a goal
goal = Goal(
    title="Build Application",
    owner="dev-team",
    description="Main application goal",
    severity="high"
)
session.add(goal)
session.commit()

# Create and associate labels
label = Label(name="backend")
session.add(label)
session.commit()

goal.labels.append(label)
session.commit()
```

### Query Interface
```python
# SQLAlchemy queries
goals = session.query(Goal).filter(Goal.status == "planned").order_by(Goal.created_at.desc()).limit(10)

# Method chaining
completed_tasks = session.query(Task).filter(
    Task.status == "completed",
    Task.progress == 100
).all()

# Find specific items
goal = session.query(Goal).filter(Goal.title == "Build Application").first()

# Complex queries
high_priority_tasks = session.query(Task).filter(
    Task.severity.in_(["high", "critical"]),
    Task.progress < 50
).all()
```

### Schema Management
```python
# Initialize database with all tables
from todowrite.core.models import Base
from todowrite.database import initialize_database

# Create all tables
initialize_database(engine)

# Or manually
Base.metadata.create_all(engine)
```

## 🧪 Testing

### Model Testing
```python
import pytest
from todowrite import Goal, Task, create_engine, sessionmaker

class TestGoalModel:
    def test_goal_creation(self):
        engine = create_engine("sqlite:///:memory:")
        Session = sessionmaker(bind=engine)
        session = Session()

        goal = Goal(
            title="Test Goal",
            owner="test-user",
            status="planned"
        )
        session.add(goal)
        session.commit()

        assert goal.id is not None
        assert goal.status == "planned"

    def test_associations(self):
        engine = create_engine("sqlite:///:memory:")
        Session = sessionmaker(bind=engine)
        session = Session()

        goal = Goal(title="Test Goal", owner="test")
        task = Task(
            title="Test Task",
            owner="test"
        )

        session.add_all([goal, task])
        session.commit()

        # Associate task with goal through phases
        phase = Phase(title="Development", owner="test")
        session.add(phase)
        session.commit()

        goal.phases.append(phase)
        phase.tasks.append(task)
        session.commit()

        # Test associations
        assert len(goal.phases) == 1
        assert len(phase.tasks) == 1
```

### Database Testing
```python
class TestDatabaseOperations:
    def test_table_creation(self):
        from todowrite.core.models import Base
        from sqlalchemy import inspect as Inspector

        engine = create_engine("sqlite:///:memory:")
        Base.metadata.create_all(engine)

        # Test that tables exist
        inspector = Inspector.from_engine(engine)
        tables = inspector.get_table_names()

        expected_tables = [
            'goals', 'concepts', 'contexts', 'constraints',
            'requirements', 'acceptance_criteria', 'interface_contracts',
            'phases', 'steps', 'tasks', 'sub_tasks', 'commands', 'labels'
        ]

        for table in expected_tables:
            assert table in tables

    def test_session_management(self):
        from todowrite.database import create_session

        # Test database session creation
        session = create_session("sqlite:///:memory:")

        # Test queries
        goal_count = session.query(Goal).count()
        assert goal_count >= 0
```

## 🔄 Migration from Old System

The project has migrated from a Node-based system to individual SQLAlchemy models:

### Key Changes
1. **Individual Models** - 12 separate models instead of generic Node
2. **SQLAlchemy ORM** - Professional database ORM instead of custom implementation
3. **Proper Relationships** - Foreign key relationships and join tables
4. **Type Safety** - Full Python type hints throughout
5. **Schema Validation** - JSON schema validation for all models

### Updated Patterns
```python
# Old approach (REMOVED)
from todowrite import create_node, Node
node = create_node(database, node_data)
Node.where(status="pending")

# New SQLAlchemy approach
from todowrite import Goal, Task, create_engine, sessionmaker
engine = create_engine("sqlite:///project.db")
Session = sessionmaker(bind=engine)
session = Session()

goal = Goal(title="My Goal", owner="team")
session.add(goal)
session.commit()

tasks = session.query(Task).filter(Task.status == "pending").all()
```

## 📚 Additional Resources

- **[Build System](../../BUILD_SYSTEM.md)** - Build tools and automation
- **[ToDoWrite Models Data Schema](../../ToDoWrite_Models_Data_Schema.md)** - Database design
- **[ToDoWrite Documentation](../../ToDoWrite.md)** - Project overview
- **[SQLAlchemy API](../../docs/sphinx/source/userdocs/SQLALCHEMY_API.rst)** - API documentation

---

**Last Updated**: 2025-11-18
**Architecture**: SQLAlchemy ORM with 12 Hierarchical Models
**Status**: ✅ Production Ready
