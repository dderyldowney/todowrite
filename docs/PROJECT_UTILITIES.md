# ToDoWrite Project Utilities

This document provides comprehensive documentation for the new centralized project utility methods that replace individual scripts. These utilities provide both programmatic API access and CLI commands for managing ToDoWrite projects.

## Overview

The new project utilities system consolidates multiple standalone scripts into a single, maintainable `ProjectManager` class. This reduces file maintenance and provides a unified interface for project development tasks.

## Quick Start

### For All Users (AI and Non-AI)

```bash
# Check project setup
python -m todowrite utils validate-setup /path/to/your/project

# Set up integration in a new project
python -m todowrite utils setup-integration /path/to/new/project

# Create basic project structure
python -m todowrite utils create-structure /path/to/new/project
```

## API Reference

### Core Project Utilities (Available to All Users)

These methods are available to both AI-enabled and non-AI users:

#### `setup_integration(project_path, db_type="postgres")`
**Purpose**: Set up ToDoWrite integration in a project with database configuration.

**Parameters**:
- `project_path` (str): Path to the project directory
- `db_type` (str): Database type - "postgres" or "sqlite"

**Returns**: `True` if setup was successful

**Usage**:
```python
from todowrite import setup_integration

# PostgreSQL setup
setup_integration("/path/to/my-project", "postgres")

# SQLite setup
setup_integration("/path/to/my-project", "sqlite")
```

**CLI Equivalent**:
```bash
python -m todowrite utils setup-integration /path/to/my-project --db-type postgres
```

#### `create_project_structure(project_path)`
**Purpose**: Create a basic ToDoWrite project structure with recommended directories.

**Parameters**:
- `project_path` (str): Where to create the structure

**Returns**: `True` if structure was created successfully

**Usage**:
```python
from todowrite import create_project_structure

create_project_structure("/path/to/new-project")
```

**CLI Equivalent**:
```bash
python -m todowrite utils create-structure /path/to/new-project
```

#### `validate_project_setup(project_path)`
**Purpose**: Validate that a project is properly set up for ToDoWrite.

**Parameters**:
- `project_path` (str): Path to validate

**Returns**: Dictionary with validation results

**Usage**:
```python
from todowrite import validate_project_setup

results = validate_project_setup("/path/to/project")
print(f"Valid: {results['valid']}")
print(f"Issues: {results['issues']}")
print(f"Found files: {results['found_files']}")
```

**CLI Equivalent**:
```bash
python -m todowrite utils validate-setup /path/to/project
```

#### `check_schema_changes()`
**Purpose**: Verify that schema changes are made in the correct location.

**Returns**: `True` if validation passes

**Usage**:
```python
from todowrite import check_schema_changes

if check_schema_changes():
    print("✅ Schema location is correct")
else:
    print("❌ Schema location issues found")
```

**CLI Equivalent**:
```bash
python -m todowrite utils check-schema
```

#### `check_deprecated_schema()`
**Purpose**: Check that deprecated schema hasn't been modified.

**Returns**: `True` if deprecated schema is untouched

**Usage**:
```python
from todowrite import check_deprecated_schema

if check_deprecated_schema():
    print("✅ Deprecated schema unchanged")
else:
    print("❌ Deprecated schema was modified")
```

**CLI Equivalent**:
```bash
python -m todowrite utils check-deprecated
```

#### `init_database_sql()`
**Purpose**: Get PostgreSQL initialization SQL as a string.

**Returns**: SQL script string

**Usage**:
```python
from todowrite import init_database_sql

sql = init_database_sql()
print(sql)
```

**CLI Equivalent**:
```bash
python -m todowrite utils init-database-sql
```

## Usage Patterns by User Type

### Non-AI Users

**Primary Focus**: Core project setup and maintenance

**Common Workflows**:

#### 1. Project Setup Workflow
```python
from todowrite import setup_integration, create_project_structure, validate_project_setup

# Create new project structure
create_project_structure("/path/to/new-project")

# Set up integration
setup_integration("/path/to/new-project", "sqlite")  # For simpler projects

# Validate setup
validation = validate_project_setup("/path/to/new-project")
if validation['valid']:
    print("Project is ready!")
else:
    print(f"Issues: {validation['issues']}")
```

#### 2. Project Maintenance Workflow
```python
from todowrite import check_schema_changes, check_deprecated_schema, validate_project_setup

# Regular maintenance checks
check_schema_changes()
check_deprecated_schema()

# Periodic validation
results = validate_project_setup("/path/to/project")
if results['recommendations']:
    print(f"Consider: {results['recommendations']}")
```

#### 3. CLI-Based Workflow
```bash
# Initialize a new project
mkdir my-project
cd my-project
python -m todowrite utils setup-integration . --db-type sqlite
python -m todowrite utils validate-setup .

# Regular checks
python -m todowrite utils check-schema
python -m todowrite utils check-deprecated
```

### AI-Enabled Users

**Primary Focus**: Enhanced productivity with AI integration and advanced features

**Common Workflows**:

#### 1. Enhanced Development Workflow
```python
from todowrite import (
    setup_integration,
    create_project_structure,
    validate_project_setup,
    _optimize_token_usage,  # Internal AI method
    _ensure_token_sage     # Internal AI method
)

# Set up project with AI optimization
create_project_structure("/path/to/ai-project")
setup_integration("/path/to/ai-project", "postgres")

# AI-enhanced validation
token_info = _optimize_token_usage(
    "Review project structure for optimization",
    project_path="/path/to/ai-project"
)

if token_info:
    print(f"Tokens saved: {token_info['tokens_saved']}")
    print("Using AI-optimized preprocessing")

# Ensure token-sage for subsequent operations
if _ensure_token_sage():
    print("Token optimization active")
```

#### 2. AI-Aware Maintenance
```python
from todowrite import check_schema_changes, check_deprecated_schema, validate_project_setup

# Standard checks (same as non-AI)
check_schema_changes()
check_deprecated_schema()

# Enhanced validation with AI awareness
results = validate_project_setup("/path/to/ai-project")

if results['valid']:
    # AI-optimized operations can proceed
    token_info = _optimize_token_usage(
        "Run development tasks",
        optimize=True
    )
    print("Proceeding with AI-optimized workflow")
else:
    # Non-AI fallback
    print("Proceeding with standard workflow")
```

#### 3. Mixed Environment Workflow
```python
from todowrite import (
    setup_integration,
    validate_project_setup,
    _optimize_token_usage,
    _ensure_token_sage
)

# Setup works the same for both
setup_integration("/path/to/mixed-project", "postgres")

# Runtime AI features are optional
try:
    # Try to use AI optimization
    if _ensure_token_sage():
        token_info = _optimize_token_usage("Enhanced analysis")
        print("AI features available")
    else:
        print("AI features not available, using standard mode")
except Exception as e:
    print(f"AI features unavailable: {e}")
    print("Falling back to standard operations")
```

## Migration Guide

### From Old Scripts to New Utilities

#### 1. `scripts/check_deprecated_schema.py` → `check_deprecated_schema()`

**Before**:
```bash
python scripts/check_deprecated_schema.py
```

**After**:
```bash
python -m todowrite utils check-deprecated
```

Or in Python:
```python
from todowrite import check_deprecated_schema
check_deprecated_schema()
```

#### 2. `scripts/check_schema_changes.py` → `check_schema_changes()`

**Before**:
```bash
python scripts/check_schema_changes.py
```

**After**:
```bash
python -m todowrite utils check-schema
```

Or in Python:
```python
from todowrite import check_schema_changes
check_schema_changes()
```

#### 3. `scripts/setup-integration.py` → `setup_integration()`

**Before**:
```bash
python scripts/setup-integration.py /path/to/project
```

**After**:
```bash
python -m todowrite utils setup-integration /path/to/project
```

Or in Python:
```python
from todowrite import setup_integration
setup_integration("/path/to/project")
```

#### 4. `init-scripts/01-init-todowrite.sql` → `init_database_sql()`

**Before**:
```bash
cat init-scripts/01-init-todowrite.sql
```

**After**:
```bash
python -m todowrite utils init-database-sql
```

Or in Python:
```python
from todowrite import init_database_sql
sql = init_database_sql()
print(sql)
```

## CLI Command Reference

All utility commands are accessible through the `utils` command group:

```bash
# Help for all utility commands
python -m todowrite utils --help

# Individual command help
python -m todowrite utils check-schema --help
python -m todowrite utils setup-integration --help
```

### Available Commands:

| Command | Purpose | AI/Non-AI |
|---------|---------|-----------|
| `check-schema` | Validate schema location changes | All users |
| `check-deprecated` | Check deprecated schema modifications | All users |
| `setup-integration` | Set up project with database | All users |
| `create-structure` | Create basic project structure | All users |
| `validate-setup` | Validate project setup | All users |
| `init-database-sql` | Get PostgreSQL SQL | All users |

## Best Practices

### For All Users

1. **Run Validation Regularly**:
   ```bash
   python -m todowrite utils validate-setup .
   ```

2. **Check Schema Changes Before Committing**:
   ```bash
   python -m todowrite utils check-schema
   ```

3. **Use Appropriate Database Type**:
   - SQLite for simple projects and development
   - PostgreSQL for production and team projects

### For AI-Enabled Users

1. **Enable Token Optimization When Available**:
   ```python
   if _ensure_token_sage():
       print("AI optimization active")
   ```

2. **Use AI-Aware Validation**:
   ```python
   results = validate_project_setup(path)
   if results['valid'] and _ai_features_available():
       # Proceed with AI-enhanced workflow
   ```

3. **Monitor Token Usage**:
   ```python
   token_info = _optimize_token_usage("Your task")
   if token_info:
       print(f"Optimized: {token_info['tokens_saved']} tokens saved")
   ```

### For Non-AI Users

1. **Focus on Core Setup**:
   ```python
   from todowrite import setup_integration, create_project_structure

   create_project_structure(project_path)
   setup_integration(project_path, "sqlite")
   ```

2. **Use CLI for Simple Operations**:
   ```bash
   python -m todowrite utils setup-integration /path/to/project
   ```

3. **Ignore AI-Specific Methods**:
   - The internal AI methods (`_optimize_token_usage`, `_ensure_token_sage`) are not available
   - All core functionality works without them

## Troubleshooting

### Common Issues

#### 1. Import Errors
```python
# If you see import errors:
from todowrite import setup_integration
# Error: Cannot import module

# Solution:
# Ensure todowrite is installed:
pip install -e .
```

#### 2. Project Path Issues
```python
# Wrong path:
setup_integration("/wrong/path")
# Error: Project path does not exist

# Solution:
# Use absolute paths or relative paths from current directory
import os
setup_integration(os.path.abspath("/path/to/project"))
```

#### 3. Database Connection Issues
```python
# PostgreSQL not running:
setup_integration("/path", "postgres")
# Error: Connection failed

# Solution:
# Start Docker/PostgreSQL or use SQLite:
setup_integration("/path", "sqlite")
```

### Debug Mode

Enable debug output for troubleshooting:
```bash
export LOG_LEVEL=debug
python -m todowrite utils setup-integration /path/to/project
```

## Examples

### Example 1: New Project Setup (Non-AI)

```bash
# 1. Create project directory
mkdir my-project
cd my-project

# 2. Set up basic structure
python -m todowrite utils create-structure .

# 3. Set up integration with SQLite
python -m todowrite utils setup-integration . --db-type sqlite

# 4. Validate setup
python -m todowrite utils validate-setup .
```

### Example 2: Project Setup (AI-Enhanced)

```bash
# 1. Create project
mkdir ai-project
cd ai-project

# 2. Enhanced setup with PostgreSQL
python -m todowrite utils setup-integration . --db-type postgres

# 3. Validate with AI awareness
python -m todowrite utils validate-setup .

# 4. Check schema integrity
python -m todowrite utils check-schema
python -m todowrite utils check-deprecated
```

### Example 3: Batch Processing

```python
from todowrite import setup_integration, validate_project_setup

projects = [
    "/path/project1",
    "/path/project2",
    "/path/project3"
]

for project in projects:
    setup_integration(project, "sqlite")
    results = validate_project_setup(project)
    print(f"{project}: {'✅' if results['valid'] else '❌'}")
```

## Integration with Development Workflows

### Pre-commit Hook
```bash
# .git/hooks/pre-commit
#!/bin/bash
python -m todowrite utils check-schema
python -m todowrite utils check-deprecated
```

### CI/CD Pipeline
```yaml
# .github/workflows/ci.yml
- name: Validate ToDoWrite Setup
  run: |
    python -m todowrite utils validate-setup .
    python -m todowrite utils check-schema

- name: Check Schema Changes
  run: python -m todowrite utils check-deprecated
```

---

**Note**: AI-enhanced features are optional and don't affect core functionality. All methods work for both AI and non-AI users, with AI features providing optimization when available.
