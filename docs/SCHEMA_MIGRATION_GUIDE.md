# ToDoWrite Database Schema Migration Guide

## Overview

This guide covers database schema migrations for the ToDoWrite hierarchical task management system using SQLAlchemy ORM. The system supports automatic schema migrations and handles both SQLite and PostgreSQL backends.

## Current Database Schema

### 12-Layer Model Architecture (Current)

The current schema uses individual SQLAlchemy models for each hierarchical layer defined in `lib_package/src/todowrite/core/models.py`:

#### Core Architecture
- **12 Individual Models** - One database table per hierarchical layer
- **SQLAlchemy ORM** - Professional database persistence with full relationships
- **Foreign Key Constraints** - Enforced referential integrity
- **Association Tables** - 29 join tables for many-to-many relationships
- **Type Safety** - Full Python type hints throughout

#### The 12 Hierarchical Layers
1. **Goal** - High-level project objectives
2. **Concept** - Design concepts and architectural patterns
3. **Context** - Environmental and project context
4. **Constraints** - Project constraints and limitations
5. **Requirements** - Functional requirements
6. **AcceptanceCriteria** - Acceptance conditions and criteria
7. **InterfaceContract** - Interface specifications and contracts
8. **Phase** - Project phases and milestones
9. **Step** - Implementation steps
10. **Task** - Specific tasks with progress tracking
11. **SubTask** - Sub-tasks that break down larger tasks
12. **Command** - Executable commands with run instructions

#### Additional Models
- **Label** - Shared categorization system across all layers
- **29 Association Tables** - Many-to-many relationships (e.g., goals_labels, tasks_labels)

## Database Initialization

### Automatic Schema Creation

```python
from todowrite import (
    Goal, Concept, Context, Constraints, Requirements,
    AcceptanceCriteria, InterfaceContract, Phase, Step,
    Task, SubTask, Command, Label,
    create_engine, sessionmaker
)

# Initialize database engine
engine = create_engine("sqlite:///project.db")

# Create all tables automatically
from todowrite.core.models import Base
Base.metadata.create_all(engine)

# Initialize session
Session = sessionmaker(bind=engine)
session = Session()
```

### Manual Schema Control

```python
# Create all tables
from todowrite.core.models import Base
from todowrite.database import initialize_database

# Initialize all tables with proper constraints
initialize_database(engine)

# Drop all tables (development only)
Base.metadata.drop_all(engine)
```

## Schema Versions

### Version 0.3.1 (Current)

**Models:**
- `Node` with 12 supported layers
- `Link` for hierarchical relationships
- `Label` system for categorization
- `Command` and `Artifact` for executable nodes

**Key Features:**
- Full 12-layer hierarchy support
- Progress tracking (0-100%)
- Status management (planned, in_progress, completed, blocked, cancelled)
- Rich metadata (owner, severity, work_type, assignee)
- Command execution with artifact tracking

### Future Schema Changes

Planned enhancements for future versions:
- Enhanced indexing for performance
- Additional metadata fields
- Audit trail for node changes
- Custom field support

## Migration Procedures

### Development Migration

For development databases, it's often easiest to recreate:

```bash
# Backup existing data
todowrite export-yaml > backup.yaml

# Reinitialize database
rm project.db
todowrite init

# Restore data
todowrite import-yaml backup.yaml
```

### Production Migration

For production databases with data to preserve:

```python
from todowrite import ToDoWrite
from todowrite.database.models import Base, engine
from alembic import op
import sqlalchemy as sa

def migrate_database():
    """Example migration function"""
    # Connect to database
    tdw = ToDoWrite("postgresql://user:pass@localhost/todowrite")

    # Example: Add new column to nodes table
    with engine.connect() as conn:
        # Check if column exists
        inspector = sa.inspect(engine)
        columns = [col['name'] for col in inspector.get_columns('nodes')]

        if 'new_field' not in columns:
            conn.execute(
                sa.text("ALTER TABLE nodes ADD COLUMN new_field VARCHAR")
            )
            conn.commit()

    print("Migration completed successfully")
```

## Database Backend Migrations

### SQLite to PostgreSQL

```python
def migrate_sqlite_to_postgres():
    """Migrate from SQLite to PostgreSQL"""

    # Initialize both connections
    sqlite_tdw = ToDoWrite("sqlite:///project.db")
    postgres_tdw = ToDoWrite("postgresql://user:pass@localhost/todowrite")

    # Initialize PostgreSQL schema
    postgres_tdw.init_database()

    # Migrate data
    all_nodes = sqlite_tdw.get_all_nodes()

    for layer, nodes in all_nodes.items():
        for node in nodes:
            # Convert node to dict and create in PostgreSQL
            node_dict = node.to_dict()
            postgres_tdw.create_node(node_dict)

    print("Migration completed successfully")
```

## Schema Validation

### JSON Schema

The system uses JSON Schema for validation:

```python
from todowrite.schema import TODOWRITE_SCHEMA
from jsonschema import validate

# Validate node data against current schema
def validate_node_data(node_data):
    try:
        validate(instance=node_data, schema=TODOWRITE_SCHEMA)
        return True, "Valid"
    except Exception as e:
        return False, str(e)
```

### Database Constraints

The database enforces these constraints:

```sql
-- Primary key constraints
ALTER TABLE nodes ADD CONSTRAINT pk_nodes PRIMARY KEY (id);
ALTER TABLE labels ADD CONSTRAINT pk_labels PRIMARY KEY (label);

-- Foreign key constraints
ALTER TABLE links ADD CONSTRAINT fk_links_parent
    FOREIGN KEY (parent_id) REFERENCES nodes(id) ON DELETE CASCADE;
ALTER TABLE links ADD CONSTRAINT fk_links_child
    FOREIGN KEY (child_id) REFERENCES nodes(id) ON DELETE CASCADE;
```

## Backup and Recovery

### SQLite Backup

```bash
# File-based backup
cp project.db project_backup.db

# SQL dump
sqlite3 project.db .dump > project_backup.sql

# Using ToDoWrite export
todowrite export-yaml > project_backup.yaml
```

### PostgreSQL Backup

```bash
# pg_dump
pg_dump todowrite > todowrite_backup.sql

# Custom format
pg_dump -Fc todowrite > todowrite_backup.dump

# Using ToDoWrite export
todowrite export-yaml > todowrite_backup.yaml
```

### Recovery Procedures

```python
def restore_from_yaml(backup_file, database_url):
    """Restore database from YAML backup"""
    tdw = ToDoWrite(database_url)
    tdw.init_database()

    # Import from backup
    from todowrite.storage.yaml_manager import YAMLManager
    yaml_manager = YAMLManager(tdw)

    # Move backup file to temporary location for import
    import shutil
    temp_path = f"configs/temp_backup.yaml"
    shutil.copy(backup_file, temp_path)

    # Import data
    results = yaml_manager.import_yaml_files(force=True)
    print(f"Imported {results['total_imported']} nodes")
```

## Performance Optimization

### Indexing Strategy

```python
# Add indexes for common queries
def add_performance_indexes():
    with engine.connect() as conn:
        # Layer-based queries
        conn.execute(sa.text(
            "CREATE INDEX IF NOT EXISTS idx_nodes_layer ON nodes(layer)"
        ))

        # Status-based queries
        conn.execute(sa.text(
            "CREATE INDEX IF NOT EXISTS idx_nodes_status ON nodes(status)"
        ))

        # Owner-based queries
        conn.execute(sa.text(
            "CREATE INDEX IF NOT EXISTS idx_nodes_owner ON nodes(owner)"
        ))

        # Date-based queries
        conn.execute(sa.text(
            "CREATE INDEX IF NOT EXISTS idx_nodes_dates ON nodes(started_date, completion_date)"
        ))

        conn.commit()
```

### Query Optimization

```python
# Efficient queries for common operations
def get_active_tasks_by_owner(tdw, owner):
    """Get active tasks for a specific owner"""
    with tdw.get_db_session() as session:
        from todowrite.database.models import Node

        return session.query(Node).filter(
            Node.layer == "Task",
            Node.owner == owner,
            Node.status.in_(["planned", "in_progress"])
        ).all()

def get_hierarchy_summary(tdw):
    """Get summary of all nodes by layer and status"""
    with tdw.get_db_session() as session:
        from todowrite.database.models import Node
        from sqlalchemy import func

        return session.query(
            Node.layer,
            Node.status,
            func.count(Node.id).label('count')
        ).group_by(Node.layer, Node.status).all()
```

## Troubleshooting

### Common Migration Issues

#### Foreign Key Constraint Errors
```sql
-- Check for orphaned records
SELECT child_id FROM links
WHERE parent_id NOT IN (SELECT id FROM nodes);

-- Clean up orphaned records
DELETE FROM links
WHERE parent_id NOT IN (SELECT id FROM nodes);
```

#### Schema Mismatch Errors
```python
def debug_schema_mismatch():
    """Debug schema validation issues"""
    from todowrite.database.models import Base
    from sqlalchemy import inspect

    inspector = inspect(engine)

    # Check existing tables
    tables = inspector.get_table_names()
    print(f"Existing tables: {tables}")

    # Check columns in nodes table
    if 'nodes' in tables:
        columns = inspector.get_columns('nodes')
        print(f"Nodes table columns: {[col['name'] for col in columns]}")
```

#### Data Type Issues
```python
def fix_data_types():
    """Fix common data type issues"""
    with engine.connect() as conn:
        # Fix progress values outside 0-100 range
        conn.execute(sa.text(
            "UPDATE nodes SET progress = 0 WHERE progress < 0 OR progress IS NULL"
        ))
        conn.execute(sa.text(
            "UPDATE nodes SET progress = 100 WHERE progress > 100"
        ))

        # Fix invalid status values
        valid_statuses = ['planned', 'in_progress', 'completed', 'blocked', 'cancelled']
        conn.execute(sa.text(
            "UPDATE nodes SET status = 'planned' WHERE status NOT IN :valid_statuses"
        ), {'valid_statuses': valid_statuses})

        conn.commit()
```

## Testing Migrations

### Migration Test Suite

```python
import pytest
import tempfile
import os

def test_migration_backward_compatibility():
    """Test that migration maintains backward compatibility"""

    # Create temporary database
    with tempfile.NamedTemporaryFile(suffix='.db', delete=False) as f:
        temp_db = f"sqlite:///{f.name}"

    try:
        # Initialize with current schema
        tdw = ToDoWrite(temp_db)
        tdw.init_database()

        # Create test data
        test_node = {
            "id": "TEST-MIGRATION-001",
            "layer": "Task",
            "title": "Migration Test",
            "description": "Test backward compatibility"
        }
        tdw.create_node(test_node)

        # Verify data integrity
        retrieved = tdw.get_node("TEST-MIGRATION-001")
        assert retrieved.title == "Migration Test"

    finally:
        # Cleanup
        if os.path.exists(f.name):
            os.unlink(f.name)

def test_schema_validation():
    """Test schema validation works correctly"""
    from todowrite.schema import TODOWRITE_SCHEMA
    from jsonschema import validate

    # Valid node should pass
    valid_node = {
        "id": "TEST-001",
        "layer": "Goal",
        "title": "Test Goal",
        "description": "A test goal",
        "links": {"parents": [], "children": []}
    }

    validate(instance=valid_node, schema=TODOWRITE_SCHEMA)

    # Invalid node should fail
    invalid_node = {
        "id": "TEST-002",
        "layer": "InvalidLayer",  # Invalid layer
        "title": "Test",
        "description": "Test",
        "links": {"parents": [], "children": []}
    }

    with pytest.raises(Exception):
        validate(instance=invalid_node, schema=TODOWRITE_SCHEMA)
```

## Best Practices

### Development Workflow
1. **Always backup** before schema changes
2. **Test migrations** on development databases first
3. **Use transactions** for multi-step migrations
4. **Validate data** after migration completion
5. **Document changes** in migration scripts

### Production Considerations
1. **Schedule downtime** for major schema changes
2. **Monitor performance** after migration
3. **Have rollback plan** ready
4. **Test with production data copy** first
5. **Communicate changes** to all stakeholders

### Schema Evolution
1. **Additive changes** preferred over destructive changes
2. **Backward compatibility** when possible
3. **Version your migrations** with clear documentation
4. **Test edge cases** thoroughly
5. **Monitor for data integrity** post-migration

---

For detailed information about the current schema structure, see [SCHEMA_USAGE.md](SCHEMA_USAGE.md).
