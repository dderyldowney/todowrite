# Universal Database Architecture for TodoWrite

This document describes the universal database architecture that works across **ALL projects** using TodoWrite, not just this specific project.

## Architecture Overview

TodoWrite uses a **three-tier database strategy** with project-specific naming that works universally:

### 1. Development Database
- **Purpose**: Tracking development work (we eat our own dog food!)
- **Location**: `~/dbs/todowrite_{project}_development.db`
- **Usage**: Daily development work, project planning, task tracking
- **Persistence**: Long-term, permanent storage

### 2. Testing Database
- **Purpose**: Automated test isolation
- **Location**: `{project_root}/tmp/todowrite_{project}_testing.db`
- **Usage**: Automated tests, CI/CD pipelines
- **Persistence**: Ephemeral, recreated for each test session

### 3. Production Database
- **Purpose**: Production deployment
- **Location**: `~/dbs/todowrite_{project}_production.db`
- **Usage**: Production work, user data
- **Persistence**: Long-term, permanent storage

## Universal Project Detection

The system automatically detects the project name from the current working directory:

```python
# Current directory: /Users/me/projects/my-awesome-app/
# Project name: my-awesome-app
# Database names:
#   Development: ~/dbs/todowrite_my-awesome_app_development.db
#   Testing: /Users/me/projects/my-awesome-app/tmp/todowrite_my-awesome_app_testing.db
#   Production: ~/dbs/todowrite_my-awesome_app_production.db
```

## Fallback for Generic Directories

When in generic directories (`src`, `lib`, `app`, etc.):

```python
# Generic directory: /Users/me/src/
# Fallback project name: project_20251112_143847
# Database names:
#   Development: ~/dbs/todowrite_project_20251112_143847_development.db
#   Testing: /Users/me/src/tmp/todowrite_project_20251112_143847_testing.db
#   Production: ~/dbs/todowrite_project_20251112_143847_production.db
```

## Usage Examples

### CLI Usage (Universal)

```bash
# Development work - auto-detects project
todowrite create --layer Goal --title "Build my project"

# Explicit database path
todowrite --database-path ~/dbs/todowrite_myproject_development.db list

# Testing (automatic via environment variables)
TODOWRITE_DATABASE_URL="sqlite:///tmp/todowrite_myproject_testing.db" pytest
```

### Programmatic Usage (Universal)

```python
from todowrite.utils.database_utils import get_database_path, get_project_database_name
from todowrite import ToDoWrite

# Auto-detect project and get appropriate database
dev_db = get_database_path('development')  # ~/dbs/todowrite_myproject_development.db
test_db = get_database_path('testing')     # /path/to/project/tmp/todowrite_myproject_testing.db
prod_db = get_database_path('production') # ~/dbs/todowrite_myproject_production.db

# Use with ToDoWrite
app = ToDoWrite(f"sqlite:///{dev_db}")
```

## Environment Variables

The system respects standard environment variables:

```bash
# Override default database location
export TODOWRITE_DATABASE_URL="sqlite:///custom/path.db"

# Set storage preference
export TODOWRITE_STORAGE_PREFERENCE="sqlite_only"
```

## Benefits

1. **No Conflicts**: Different projects get completely separate databases
2. **Clear Ownership**: Database names explicitly show project and environment
3. **Universal**: Works the same way across ALL projects
4. **Organized**: Consistent directory structure (`~/dbs/` for persistent, `project_root/tmp/` for tests)
5. **Backward Compatible**: Existing explicit database paths still work
6. **Development Tracking**: We use our own tools for development work

## Implementation Details

### Core Utility Functions

```python
from todowrite.utils.database_utils import (
    get_project_name,           # Detects project from CWD
    get_project_database_name,  # Generates todowrite_{project}_{env}.db
    get_database_path,          # Returns full path with correct directory
)
```

### Directory Structure

```
~/
├── dbs/                           # Persistent databases
│   ├── todowrite_project1_development.db
│   ├── todowrite_project1_production.db
│   ├── todowrite_project2_development.db
│   └── todowrite_project2_production.db

~/projects/my-project/
├── tmp/                          # Test databases (project-specific)
│   └── todowrite_my_project_testing.db
├── src/
└── configs/
```

This architecture ensures that **every project** using TodoWrite gets proper database isolation and clear naming conventions, whether it's this specific project or any other project in the future.
