# ToDoWrite Schema Change Workflow

## Overview

This document establishes the standard workflow for making changes to the ToDoWrite JSON schema and database models. All schema changes must follow this workflow to ensure consistency, backward compatibility, and proper testing.

## Current Schema Architecture

### JSON Schema Location
```bash
lib_package/src/todowrite/core/schemas/todowrite.schema.json
```

### Database Models Location
```bash
lib_package/src/todowrite/database/models.py
```

### Type Definitions Location
```bash
lib_package/src/todowrite/core/types.py
```

## Schema Change Workflow

### Step 1: Design the Change

Before implementing any schema change, answer these questions:

1. **What is the purpose of this change?**
   - New feature requirement
   - Bug fix in validation
   - Performance optimization
   - Data integrity improvement

2. **What is the impact?**
   - Breaking change (requires migration)
   - Additive change (backward compatible)
   - Validation change only
   - Internal model change only

3. **What testing is needed?**
   - Unit tests for new validation rules
   - Integration tests with existing data
   - Migration tests (if applicable)
   - Performance impact assessment

### Step 2: Update Type Definitions

If changing core data structures, update `lib_package/src/todowrite/core/types.py`:

```python
# Example: Adding a new metadata field
@dataclass
class Metadata:
    owner: str = ""
    labels: list[str] = field(default_factory=list)
    severity: str = "low"
    work_type: str = "chore"
    assignee: str = ""
    priority: str = "medium"  # NEW: Add priority field

    def __post_init__(self) -> None:
        # Validation logic for new field
        valid_priorities = ["low", "medium", "high", "urgent"]
        if self.priority not in valid_priorities:
            raise ValueError(f"Invalid priority: {self.priority}")
```

### Step 3: Update Database Models

If changing the database schema, update `lib_package/src/todowrite/database/models.py`:

```python
class Node(Base):
    """Represents a node in the ToDoWrite system."""

    __tablename__ = "nodes"

    # Existing fields...
    id: Mapped[str] = mapped_column(String, primary_key=True)
    layer: Mapped[str] = mapped_column(String, nullable=False)
    # ... other existing fields

    # NEW: Add priority field
    priority: Mapped[str] = mapped_column(String, default="medium")
```

### Step 4: Update JSON Schema

Update `lib_package/src/todowrite/core/schemas/todowrite.schema.json`:

```json
{
  "title": "ToDoWrite Node",
  "type": "object",
  "required": ["id", "layer", "title", "description", "links"],
  "properties": {
    "id": {
      "type": "string",
      "pattern": "^(GOAL|CON|CTX|CST|R|AC|IF|PH|STP|TSK|SUB|CMD)-[A-Za-z0-9_-]+$"
    },
    "layer": {
      "type": "string",
      "enum": ["Goal", "Concept", "Context", "Constraints", "Requirements", "AcceptanceCriteria", "InterfaceContract", "Phase", "Step", "Task", "SubTask", "Command"]
    },
    "title": {
      "type": "string",
      "minLength": 1
    },
    "description": {
      "type": "string"
    },
    "metadata": {
      "type": "object",
      "properties": {
        "owner": {"type": "string"},
        "labels": {"type": "array", "items": {"type": "string"}},
        "severity": {"type": "string", "enum": ["low", "medium", "high", "critical"]},
        "work_type": {"type": "string", "enum": ["architecture", "spec", "interface", "validation", "implementation", "development", "docs", "ops", "refactor", "chore", "test"]},
        "assignee": {"type": "string"},
        "priority": {"type": "string", "enum": ["low", "medium", "high", "urgent"], "default": "medium"}  // NEW
      }
    }
    // ... other properties
  }
}
```

### Step 5: Add Tests

Create comprehensive tests for the schema change:

```python
# tests/test_schema_changes.py
import pytest
from jsonschema import validate
from todowrite.schema import TODOWRITE_SCHEMA

class TestSchemaChanges:
    """Test schema validation with new priority field"""

    def test_valid_priority_values(self):
        """Test that all valid priority values are accepted"""
        for priority in ["low", "medium", "high", "urgent"]:
            node_data = {
                "id": "TEST-PRIORITY-001",
                "layer": "Task",
                "title": "Test Priority",
                "description": "Test priority validation",
                "links": {"parents": [], "children": []},
                "metadata": {"priority": priority}
            }

            # Should not raise an exception
            validate(instance=node_data, schema=TODOWRITE_SCHEMA)

    def test_invalid_priority_value(self):
        """Test that invalid priority values are rejected"""
        node_data = {
            "id": "TEST-PRIORITY-002",
            "layer": "Task",
            "title": "Test Priority",
            "description": "Test priority validation",
            "links": {"parents": [], "children": []},
            "metadata": {"priority": "invalid"}  # Invalid priority
        }

        with pytest.raises(Exception) as exc_info:
            validate(instance=node_data, schema=TODOWRITE_SCHEMA)

        assert "priority" in str(exc_info.value)

    def test_default_priority(self):
        """Test that priority defaults to medium when not specified"""
        node_data = {
            "id": "TEST-PRIORITY-003",
            "layer": "Task",
            "title": "Test Priority",
            "description": "Test priority default",
            "links": {"parents": [], "children": []},
            "metadata": {}  # No priority specified
        }

        # Should be valid (defaults to medium)
        validate(instance=node_data, schema=TODOWRITE_SCHEMA)
```

### Step 6: Update Migration Scripts

If database schema changed, update migration procedures:

```python
# scripts/migrations/add_priority_field.py
from todowrite import ToDoWrite
import sqlalchemy as sa

def add_priority_field(database_url):
    """Add priority field to existing nodes table"""

    tdw = ToDoWrite(database_url)

    with tdw.get_engine().connect() as conn:
        # Check if column exists
        inspector = sa.inspect(tdw.get_engine())
        columns = [col['name'] for col in inspector.get_columns('nodes')]

        if 'priority' not in columns:
            # Add the column
            conn.execute(
                sa.text("ALTER TABLE nodes ADD COLUMN priority VARCHAR DEFAULT 'medium'")
            )

            # Set default value for existing records
            conn.execute(
                sa.text("UPDATE nodes SET priority = 'medium' WHERE priority IS NULL")
            )

            conn.commit()
            print("Priority field added successfully")
        else:
            print("Priority field already exists")
```

### Step 7: Update Documentation

Update relevant documentation:

1. **SCHEMA_USAGE.md** - Add new field documentation
2. **API_DOCUMENTATION.md** - Update API examples
3. **CLI documentation** - Update command examples if needed

### Step 8: Validation Testing

Run comprehensive validation tests:

```bash
# Test JSON schema validation
python -c "
from todowrite.schema import TODOWRITE_SCHEMA
from jsonschema import validate
import json

# Test with existing YAML files
import glob
for yaml_file in glob.glob('configs/**/*.yaml'):
    # Load and validate each file
    print(f'Validating {yaml_file}...')
"

# Test database operations
PYTHONPATH="lib_package/src:cli_package/src" python -m pytest tests/ -v

# Test CLI functionality
todowrite --help
todowrite create --layer task --title "Schema Test" --metadata '{"priority": "high"}'
```

## Change Categories

### Additive Changes (Preferred)

These changes add new functionality without breaking existing code:

**Examples:**
- Adding new optional fields
- Adding new enum values
- Adding new validation rules (that don't invalidate existing data)
- Adding new indexes

**Process:**
1. Update models with default values
2. Update JSON schema with optional fields
3. Add tests for new functionality
4. Update documentation
5. No migration needed for existing data

### Breaking Changes

These changes require migration of existing data:

**Examples:**
- Removing fields
- Changing field types
- Making optional fields required
- Changing enum values
- Renaming fields

**Process:**
1. Create migration script
2. Update models and schema
3. Write comprehensive tests
4. Test migration on copy of production data
5. Schedule migration window
6. Execute migration
7. Validate results

### Validation Changes

These changes only affect validation rules:

**Examples:**
- Tightening pattern matching
- Adding new constraints
- Improving error messages

**Process:**
1. Update JSON schema
2. Add validation tests
3. Test against existing data
4. Update documentation
5. No database changes needed

## Quality Gates

### Before Commit

Every schema change must pass these checks:

- [ ] **Code Review**: Peer review of all changes
- [ ] **Unit Tests**: All new tests pass
- [ ] **Integration Tests**: Full test suite passes
- [ ] **Schema Validation**: Existing YAML files still validate
- [ ] **Documentation**: All documentation updated
- [ ] **Performance**: No performance regression

### Pre-merge Checks

- [ ] **Backward Compatibility**: Existing installations unaffected
- [ ] **Migration Path**: Clear upgrade path for breaking changes
- [ ] **Rollback Plan**: Procedure to revert changes if needed
- [ ] **Test Coverage**: At least 90% code coverage for changes

## Release Process

### Version Bumping

For schema changes, follow semantic versioning:

- **Patch (X.Y.Z+1)**: Additive changes, bug fixes
- **Minor (X.Y+1.0)**: New features, breaking changes with migration
- **Major (X+1.0.0)**: Major architectural changes

### Release Checklist

- [ ] Schema version updated in code
- [ ] Migration scripts tested and documented
- [ ] Release notes prepared
- [ ] Documentation updated and published
- [ ] Breaking changes communicated to users

## Emergency Schema Changes

For critical issues requiring immediate schema changes:

1. **Create Hotfix Branch**
   ```bash
   git checkout -b hotfix/schema-critical-fix
   ```

2. **Implement Minimal Fix**
   - Fix only the critical issue
   - Avoid additional changes
   - Add targeted tests

3. **Fast Review and Merge**
   - expedite code review
   - merge to develop branch
   - create emergency release

4. **Post-mortem**
   - Document root cause
   - Improve prevention measures
   - Update testing procedures

## Common Schema Changes

### Adding New Metadata Fields

```python
# Step 1: Update types.py
@dataclass
class Metadata:
    # existing fields...
    new_field: str = "default_value"

# Step 2: Update models.py (if database field needed)
class Node(Base):
    # existing fields...
    new_field: Mapped[str] = mapped_column(String, default="default_value")

# Step 3: Update JSON schema
"metadata": {
    "type": "object",
    "properties": {
        # existing properties...
        "new_field": {
            "type": "string",
            "default": "default_value"
        }
    }
}
```

### Adding New Enum Values

```python
# Step 1: Update types.py
WorkType = Literal[
    "architecture",
    "spec",
    "interface",
    "validation",
    "implementation",
    "development",
    "docs",
    "ops",
    "refactor",
    "chore",
    "test",
    "security"  # NEW: Add new work type
]

# Step 2: Update JSON schema
"work_type": {
    "type": "string",
    "enum": [
        "architecture",
        "spec",
        "interface",
        "validation",
        "implementation",
        "development",
        "docs",
        "ops",
        "refactor",
        "chore",
        "test",
        "security"  // NEW
    ]
}
```

### Changing Field Constraints

```json
// Example: Tightening ID pattern validation
{
  "properties": {
    "id": {
      "type": "string",
      "pattern": "^(GOAL|CON|CTX|CST|R|AC|IF|PH|STP|TSK|SUB|CMD)-[A-Z0-9_-]{1,20}$"  // Added length constraint
    }
  }
}
```

## Tools and Utilities

### Schema Validation Tool

```bash
# Validate all YAML files against current schema
python -m todowrite.tools.validate_schema

# Validate specific file
python -m todowrite.tools.validate_schema --file configs/goals/project.yaml

# Validate with custom schema
python -m todowrite.tools.validate_schema --schema custom_schema.json
```

### Migration Testing Tool

```bash
# Test migration on copy of database
python scripts/test_migration.py --source production.db --target test_migration.db

# Dry run migration (show what would change)
python scripts/migrate_schema.py --database production.db --dry-run

# Execute migration
python scripts/migrate_schema.py --database production.db
```

### Schema Diff Tool

```bash
# Compare two schema versions
python scripts/schema_diff.py --old schema_v1.json --new schema_v2.json

# Generate migration plan
python scripts/schema_diff.py --old schema_v1.json --new schema_v2.json --migration-plan
```

---

## Conclusion

Following this workflow ensures that schema changes are:

- **Well-planned** with clear requirements and impact analysis
- **Thoroughly tested** with comprehensive test coverage
- **Properly documented** for future reference
- **Safely deployed** with migration paths and rollback plans
- **Maintained for quality** with ongoing validation and monitoring

All schema changes should be treated carefully, as they affect both the application logic and the data integrity of existing ToDoWrite installations.
