# Project Utilities

**Version**: See VERSION file
**Status**: Production Ready
**Last Updated**: November 8, 2025

## Overview

This document describes the available utilities and helper functions in the ToDoWrite library for managing projects and common operations.

## Available Utilities

### 1. Database Utilities

#### Database Initialization

```python
from todowrite import ToDoWrite

# Initialize with SQLite (default)
app = ToDoWrite("sqlite:///project.db")
app.init_database()

# Initialize with PostgreSQL
app = ToDoWrite("postgresql://user:pass@localhost/project")
app.init_database()
```

#### Database Status Check

```python
# Check database configuration and status
from todowrite import ToDoWrite

app = ToDoWrite()
status = app.get_database_status()
print(f"Database Type: {status['type']}")
print(f"Connection: {status['connected']}")
```

CLI equivalent:
```bash
todowrite db-status
```

### 2. Node Management Utilities

#### Batch Node Creation

```python
from todowrite import ToDoWrite

app = ToDoWrite("sqlite:///project.db")

# Create multiple nodes efficiently
nodes_data = [
    {
        "id": "GOAL-001",
        "layer": "Goal",
        "title": "Complete Project",
        "description": "Finish the main project",
        "links": {"parents": [], "children": []},
        "metadata": {"owner": "team-lead", "labels": ["main"]}
    },
    {
        "id": "TSK-001",
        "layer": "Task",
        "title": "Implement Feature",
        "description": "Build the core feature",
        "links": {"parents": [], "children": []},
        "metadata": {"owner": "developer", "labels": ["implementation"]}
    }
]

created_nodes = []
for node_data in nodes_data:
    node = app.[REMOVED_LEGACY_PATTERN](node_data)
    created_nodes.append(node)

# Link nodes together
app.link_nodes("GOAL-001", "TSK-001")
```

#### Node Search and Filtering

```python
# Search nodes by text
results = app.search_nodes("authentication")
for node in results:
    print(f"Found: {node.title} ({node.layer})")

# Get all nodes by layer
goals = app.get_nodes_by_layer("Goal")
tasks = app.get_nodes_by_layer("Task")

# Get nodes by status
in_progress = app.get_nodes_by_status("in_progress")
```

CLI equivalents:
```bash
todowrite search "authentication"
todowrite list --layer goal
todowrite list --status in_progress
```

### 3. YAML Import/Export Utilities

#### Export Project to YAML

```python
from todowrite import ToDoWrite

app = ToDoWrite("sqlite:///project.db")

# Export all nodes to YAML files
app.export_to_yaml("./backup/")

# Export specific layers only
app.export_layer_to_yaml("Goal", "./goals/")
app.export_layer_to_yaml("Task", "./tasks/")
```

CLI equivalent:
```bash
todowrite export-yaml
```

#### Import Project from YAML

```python
from todowrite import ToDoWrite

app = ToDoWrite("sqlite:///project.db")
app.init_database()

# Import all YAML files
app.import_from_yaml("./configs/")

# Import specific layer files
app.import_layer_from_yaml("Goal", "./goals/")
app.import_layer_from_yaml("Task", "./tasks/")
```

CLI equivalent:
```bash
todowrite import-yaml
```

### 4. Progress and Status Utilities

#### Calculate Project Progress

```python
from todowrite import ToDoWrite

app = ToDoWrite("sqlite:///project.db")

# Get overall project progress
all_goals = app.get_nodes_by_layer("Goal")
for goal in all_goals:
    progress = app.calculate_goal_progress(goal.id)
    print(f"Goal {goal.title}: {progress}% complete")

# Get progress by status
stats = app.get_project_statistics()
print(f"Total nodes: {stats['total_nodes']}")
print(f"Completed: {stats['completed_count']}")
print(f"In Progress: {stats['in_progress_count']}")
```

#### Update Node Status

```python
# Update node with progress tracking
app.update_node("TSK-001", {
    "status": "in_progress",
    "progress": 75,
    "assignee": "developer-name"
})
```

CLI equivalent:
```bash
todowrite update --id "TSK-001" --status in_progress --progress 75
```

### 5. Project Validation Utilities

#### Validate Node Data

```python
from todowrite import ToDoWrite, validate_node_data

# Validate node data before creation
node_data = {
    "id": "TEST-001",
    "layer": "Task",
    "title": "Test Task",
    "description": "A test task",
    "links": {"parents": [], "children": []},
    "metadata": {"owner": "tester"}
}

try:
    validate_node_data(node_data)
    print("Node data is valid")
except Exception as e:
    print(f"Validation error: {e}")
```

#### Check Project Integrity

```python
from todowrite import ToDoWrite

app = ToDoWrite("sqlite:///project.db")

# Check for orphaned nodes
orphans = app.find_orphaned_nodes()
if orphans:
    print(f"Found {len(orphans)} orphaned nodes")

# Check for broken links
broken_links = app.check_link_integrity()
if broken_links:
    print(f"Found {len(broken_links)} broken links")
```

## Development Scripts

### Setup Script

The project includes a setup script for development:

```bash
# Run the development setup script
./setup_dev.sh
```

This script:
- Installs development dependencies
- Sets up pre-commit hooks
- Configures the development environment

### Build Script

```bash
# Build packages for distribution
./scripts/build.sh

# Clean and build
./scripts/build.sh clean
```

### Test Script

```bash
# Run all tests
export PYTHONPATH="lib_package/src:cli_package/src"
python -m pytest

# Run tests with coverage
python -m pytest --cov=lib_package/src --cov-report=html
```

## Configuration Utilities

### Environment Variables

ToDoWrite supports several environment variables for configuration:

```bash
# Database URL
export TODOWRITE_DATABASE_URL="postgresql://user:pass@localhost/project"  # pragma: allowlist secret

# Storage preference (auto, postgresql_only, sqlite_only, yaml_only)
export TODOWRITE_STORAGE_PREFERENCE="auto"

# Log level
export TODOWRITE_LOG_LEVEL="INFO"
```

### Configuration Files

You can create configuration files for default settings:

`~/.config/todowrite/config.yaml`:
```yaml
database:
  url: "sqlite:///default.db"

storage:
  preference: "auto"

logging:
  level: "INFO"
  file: "~/.local/share/todowrite/todowrite.log"
```

## Common Usage Patterns

### 1. Project Setup

```python
from todowrite import ToDoWrite

def setup_project(project_name: str, db_type: str = "sqlite"):
    """Setup a new ToDoWrite project"""

    # Initialize database
    if db_type == "sqlite":
        app = ToDoWrite(f"sqlite:///{project_name}.db")
    else:
        app = ToDoWrite(f"postgresql://localhost/{project_name}")

    app.init_database()

    # Create project goal
    goal = app.[REMOVED_LEGACY_PATTERN]({
        "id": f"GOAL-{project_name.upper()}-001",
        "layer": "Goal",
        "title": f"Complete {project_name}",
        "description": f"Main goal for {project_name} project",
        "links": {"parents": [], "children": []},
        "metadata": {"owner": "project-lead", "labels": ["main"]}
    })

    print(f"Project {project_name} initialized with goal: {goal.id}")
    return app
```

### 2. Progress Tracking

```python
def update_task_progress(task_id: str, progress: int, status: str = None):
    """Update task progress and status"""

    app = ToDoWrite()

    update_data = {"progress": progress}
    if status:
        update_data["status"] = status

    # Auto-set status based on progress
    if progress == 0:
        update_data["status"] = "planned"
    elif 0 < progress < 100:
        update_data["status"] = "in_progress"
    elif progress == 100:
        update_data["status"] = "completed"

    app.update_node(task_id, update_data)
    print(f"Task {task_id} updated: {progress}% ({update_data['status']})")
```

### 3. Project Backup

```python
def backup_project(project_db: str, backup_dir: str):
    """Backup entire project to YAML files"""

    app = ToDoWrite(f"sqlite:///{project_db}")

    # Export all data
    app.export_to_yaml(backup_dir)

    # Create backup info
    import datetime
    with open(f"{backup_dir}/backup_info.txt", "w") as f:
        f.write(f"Backup created: {datetime.datetime.now()}\n")
        f.write(f"Source database: {project_db}\n")
        f.write(f"Total nodes exported: {len(app.get_all_nodes())}\n")

    print(f"Project backed up to: {backup_dir}")
```

## Integration Examples

### With Other Python Projects

```python
# Integrate ToDoWrite into your existing project
from todowrite import ToDoWrite

class ProjectManager:
    def __init__(self, project_name: str):
        self.app = ToDoWrite(f"sqlite:///{project_name}.db")
        self.app.init_database()

    def add_feature_task(self, feature_name: str, description: str):
        """Add a new feature task"""
        task = self.app.[REMOVED_LEGACY_PATTERN]({
            "id": f"TSK-{feature_name.upper().replace(' ', '-')}",
            "layer": "Task",
            "title": f"Implement {feature_name}",
            "description": description,
            "links": {"parents": [], "children": []},
            "metadata": {"owner": "dev-team", "labels": ["feature"]}
        })
        return task

    def complete_feature(self, task_id: str):
        """Mark a feature as completed"""
        self.app.update_node(task_id, {
            "status": "completed",
            "progress": 100
        })

# Usage
pm = ProjectManager("myapp")
task = pm.add_feature_task("User Login", "Implement user authentication")
pm.complete_feature(task.id)
```

## Error Handling

```python
[REMOVED_LEGACY_PATTERN]NotFoundError, ValidationError

app = ToDoWrite("sqlite:///project.db")

try:
    node = app.get_node("NONEXISTENT-001")
except NodeNotFoundError:
    print("Node not found")

try:
    app.[REMOVED_LEGACY_PATTERN](invalid_data)
except ValidationError as e:
    print(f"Validation error: {e}")
except Exception as e:
    print(f"Other error: {e}")
```

## Additional Documentation

- **[← Documentation Index](README.md)** - Complete documentation overview
- **[Installation Guide](installation.md)** - Get ToDoWrite installed
- **[Integration Guide](INTEGRATION_GUIDE.md)** - Real-world usage examples
- **[Status Tracking](STATUS_TRACKING.md)** - Progress and status management
- **[Main Project Documentation](../README.md)** - Project overview and features
- **[CLI Reference](../cli_package/README.md)** - Command-line interface reference

---

**Current Version**: See VERSION file
**Python Support**: 3.12+
**Test Status**: 157/157 tests passing ✅
**License**: MIT
