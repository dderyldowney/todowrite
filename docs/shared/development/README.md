# Development Guide

**Comprehensive development guide for the ToDoWrite project with Rails ActiveRecord-inspired architecture.**

---

## 🏗️ Architecture Overview

ToDoWrite now uses a **Rails ActiveRecord-inspired architecture** that provides:

- **Model-based entities** with relationships (has_many, belongs_to)
- **Automatic migrations and schema management** (like Rails migrations)
- **Database-agnostic storage backends** (SQLite, PostgreSQL)
- **ActiveRecord-style query interfaces** and method chaining
- **Model validations and callbacks**
- **Association management** between hierarchical nodes

### Key Components

#### Models (`lib_package/src/todowrite/core/models.py`)
- **`Node`** - Base ActiveRecord-like model for all nodes
- **Relationships** - `has_many`, `belongs_to`, `has_one` associations
- **Validations** - Model-level validation framework
- **Callbacks** - Before/after save, create, update, delete hooks

#### Database Layer
- **`ActiveRecord`** - Base ORM functionality
- **`Connection`** - Database connection management
- **`Migration`** - Schema migration system
- **`QueryBuilder`** - ActiveRecord-style query builder

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
│   ├── core/                           # ActiveRecord-like core
│   │   ├── models.py                   # Model definitions (Node, etc.)
│   │   ├── active_record.py           # Base ActiveRecord functionality
│   │   ├── associations.py            # Model relationships
│   │   ├── validations.py             # Model validations
│   │   ├── migrations.py              # Migration system
│   │   └── query_builder.py           # Query builder
│   ├── database/                      # Database layer
│   │   ├── connection.py              # Database connections
│   │   ├── models.py                  # SQLAlchemy models
│   │   └── migrations/                # Migration files
│   ├── storage/                       # Storage backends
│   └── tools/                         # Utilities
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

## 🔧 ActiveRecord Features

### Model Definitions
```python
from todowrite.core.models import Node, has_many, belongs_to

class Goal(Node):
    """Goal model with ActiveRecord-like features."""

    class Meta:
        table_name = "nodes"
        layer = "Goal"

    # Rails-style associations
    has_many("tasks", foreign_key="parent_id")
    has_many("children", class_name="Node", foreign_key="parent_id")
    belongs_to("project", class_name="Node", foreign_key="parent_id", optional=True)

    # Validations
    validates_presence_of(["title", "owner"])
    validates_length_of("title", maximum=200)

    # Callbacks
    before_save :set_default_status
    after_create :log_creation

    def set_default_status(self):
        if not self.status:
            self.status = "planned"

    def log_creation(self):
        print(f"Goal created: {self.title}")

# Usage
goal = Goal.create(
    title="Build Application",
    owner="dev-team",
    description="Main application goal"
)
```

### Query Interface
```python
# ActiveRecord-style queries
goals = Goal.where(status="planned").order("created_at desc").limit(10)

# Method chaining
completed_tasks = Task.where(status="completed").where("progress = 100")

# Finders
goal = Goal.find_by_title("Build Application")

# Scopes
class Task(Node):
    @classmethod
    def high_priority(cls):
        return cls.where(metadata__contains="high")

# Usage
urgent_tasks = Task.high_priority().where("progress < 50")
```

### Migrations
```python
# Create migration
from todowrite.core.migrations import Migration

class AddProgressTracking(Migration):
    def change(self):
        self.add_column("nodes", "progress", self.integer, default=0)
        self.add_index("nodes", "progress")

        # Add new association
        self.add_reference("nodes", "parent", foreign_key="parent_id")

# Run migration
from todowrite.core.active_record import ActiveRecord
ActiveRecord.migrate()
```

## 🧪 Testing

### Model Testing
```python
import pytest
from todowrite.core.models import Goal, Task

class TestGoalModel:
    def test_goal_creation(self):
        goal = Goal.create(
            title="Test Goal",
            owner="test-user"
        )
        assert goal.id is not None
        assert goal.status == "planned"  # Set by callback

    def test_associations(self):
        goal = Goal.create(title="Test Goal", owner="test")
        task = Task.create(
            title="Test Task",
            owner="test",
            parent_id=goal.id
        )

        # Test associations
        assert len(goal.tasks) == 1
        assert task.parent == goal
```

### Database Testing
```python
class TestDatabaseOperations:
    def test_migration_execution(self):
        # Test that migrations run successfully
        from todowrite.core.active_record import ActiveRecord

        result = ActiveRecord.migrate()
        assert result.success

    def test_connection_management(self):
        # Test database connections
        conn = ActiveRecord.connection()
        assert conn.is_connected()

        # Test queries
        result = conn.execute("SELECT COUNT(*) FROM nodes")
        assert result[0][0] >= 0
```

## 🔄 Migration from Old System

The project has migrated from a traditional ORM to an ActiveRecord-inspired system:

### Key Changes
1. **Model-centric design** - Models now contain business logic
2. **Associations** - `has_many`, `belongs_to` relationships
3. **Migrations** - Schema changes via migration files
4. **Query builder** - Chainable query methods
5. **Validations** - Model-level validation framework

### Updated Patterns
```python
# Old approach
app = ToDoWrite("sqlite:///project.db")
node = app.create_node({...})

# New ActiveRecord approach
goal = Goal.create({...})
tasks = goal.tasks.where(status="pending")
```

## 📚 Additional Resources

- **[Build System](BUILD_SYSTEM.md)** - Build tools and automation
- **[Database Architecture](UNIVERSAL_DATABASE_ARCHITECTURE.md)** - Database design
- **[Development Workflow](DEVELOPMENT_WORKFLOW.md)** - Claude Code powered workflow
- **[Enforcement System](ENFORCEMENT_SYSTEM.md)** - Code quality enforcement

---

**Last Updated**: 2025-11-17
**Architecture**: ActiveRecord-inspired
**Status**: ✅ Production Ready
