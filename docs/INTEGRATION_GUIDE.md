# ToDoWrite Integration Guide

**Version**: 0.3.1
**Status**: Production Ready
**Testing**: 119/119 tests passing with real implementations

## Overview

This guide demonstrates real integration scenarios for the ToDoWrite hierarchical task management system, showing how to structure projects from goals to executable commands.

## Core Concepts

### The Hierarchical Framework

ToDoWrite organizes project planning into hierarchical layers:

**High-Level Planning:**
1. **Goal** - Project objectives and desired outcomes
2. **Concept** - Design concepts and architectural approaches
3. **Context** - Environment and project constraints
4. **Constraints** - Project limitations and requirements

**Specification:**
5. **Requirements** - Functional requirements
6. **AcceptanceCriteria** - Success conditions
7. **InterfaceContract** - API specifications

**Implementation:**
8. **Phase** - Project phases and milestones
9. **Step** - Implementation steps
10. **Task** - Specific work assignments
11. **SubTask** - Detailed sub-tasks
12. **Command** - Executable commands

### Key Principles

- **Database Storage**: All data stored in SQLite/PostgreSQL
- **Schema Validation**: JSON Schema validation ensures data integrity
- **Type Safety**: Comprehensive type hints
- **Real Testing**: All functionality verified with actual implementations

## Scenario 1: Software Development Project

### Project Overview

Build a web application with user authentication and data management.

### Step 1: Initialize Project

```bash
# Initialize the project
todowrite init

# Create project directory structure
mkdir project_configs
cd project_configs
```

### Step 2: Create High-Level Goals

```python
from todowrite import ToDoWrite

# Initialize
app = ToDoWrite("sqlite:///webapp.db")
app.init_database()

# Create main project goal
goal = app.create_node({
    "id": "GOAL-WEBAPP-001",
    "layer": "Goal",
    "title": "Build Web Application Platform",
    "description": "Create a web application with user authentication and data management",
    "status": "planned",
    "progress": 0,
    "links": {"parents": [], "children": []},
    "metadata": {
        "owner": "project-manager",
        "labels": ["webapp", "platform"],
        "severity": "high",
        "work_type": "development"
    }
})
```

### Step 3: Define Architecture Concepts

```python
# Create architectural concepts
auth_concept = app.create_node({
    "id": "CON-AUTH-001",
    "layer": "Concept",
    "title": "User Authentication System",
    "description": "Secure user authentication with JWT tokens",
    "links": {"parents": [], "children": []},
    "metadata": {
        "owner": "architect",
        "labels": ["authentication", "security"],
        "severity": "high",
        "work_type": "architecture"
    }
})

data_concept = app.create_node({
    "id": "CON-DATA-001",
    "layer": "Concept",
    "title": "Data Management System",
    "description": "Database design and data access patterns",
    "links": {"parents": [], "children": []},
    "metadata": {
        "owner": "architect",
        "labels": ["database", "data"],
        "severity": "medium",
        "work_type": "architecture"
    }
})
```

### Step 4: Link Hierarchy

```python
from todowrite import link_nodes

# Link concepts to goal
link_nodes("sqlite:///webapp.db", goal.id, auth_concept.id)
link_nodes("sqlite:///webapp.db", goal.id, data_concept.id)
```

### Step 5: Create Tasks

```python
# Create implementation tasks
tasks = [
    {
        "id": "TSK-AUTH-001",
        "layer": "Task",
        "title": "Implement User Registration",
        "description": "Create user registration endpoint and validation",
        "links": {"parents": [auth_concept.id], "children": []},
        "metadata": {
            "owner": "backend-dev",
            "labels": ["authentication", "endpoint"],
            "severity": "high",
            "work_type": "implementation"
        }
    },
    {
        "id": "TSK-AUTH-002",
        "layer": "Task",
        "title": "Implement User Login",
        "description": "Create login endpoint with JWT token generation",
        "links": {"parents": [auth_concept.id], "children": []},
        "metadata": {
            "owner": "backend-dev",
            "labels": ["authentication", "jwt"],
            "severity": "high",
            "work_type": "implementation"
        }
    },
    {
        "id": "TSK-DATA-001",
        "layer": "Task",
        "title": "Design Database Schema",
        "description": "Create PostgreSQL schema for users and data",
        "links": {"parents": [data_concept.id], "children": []},
        "metadata": {
            "owner": "backend-dev",
            "labels": ["database", "schema"],
            "severity": "high",
            "work_type": "design"
        }
    }
]

for task_data in tasks:
    app.create_node(task_data)
```

### Step 6: Create Commands

```python
# Create executable commands
build_command = app.create_node({
    "id": "CMD-BUILD-001",
    "layer": "Command",
    "title": "Build Authentication Module",
    "description": "Build and test authentication components",
    "command": {
        "ac_ref": "AC-AUTH-001",
        "run": {
            "shell": "python -m pytest tests/auth/ && python setup.py build",
            "workdir": "/project",
            "env": {"TEST_ENV": "production"}
        },
        "artifacts": ["dist/auth_module.tar.gz", "test_reports.html"]
    },
    "links": {"parents": ["TSK-AUTH-001"], "children": []},
    "metadata": {
        "owner": "devops",
        "labels": ["build", "test"],
        "severity": "medium",
        "work_type": "automation"
    }
})
```

### Step 7: Query and Update

```python
from todowrite import search_nodes

# Get all tasks
all_nodes = app.get_all_nodes()
tasks = all_nodes.get("Task", [])
print(f"Total tasks: {len(tasks)}")

# Search for authentication-related items
auth_items = search_nodes("sqlite:///webapp.db", {"labels": ["authentication"]})
print(f"Authentication items: {len(auth_items)}")

# Update task progress
app.update_node("TSK-AUTH-001", {
    "status": "in_progress",
    "progress": 50,
    "metadata": {"assignee": "developer1"}
})
```

## Scenario 2: CLI Workflow Integration

### Using the Command Line Interface

```bash
# Initialize a new project
todowrite init

# Create goals
todowrite create --layer goal --title "Deploy Application" --description "Deploy to production" --owner "devops"

# Create tasks
todowrite create --layer task --title "Set up production database" --description "Configure PostgreSQL" --owner "devops" --severity "high"

todowrite create --layer task --title "Configure deployment pipeline" --description "Set up CI/CD" --owner "devops" --labels "infrastructure"

# View project structure
todowrite list

# Search for specific items
todowrite search "database"

# Export to YAML for backup
todowrite export-yaml

# Import from YAML
todowrite import-yaml

# Check status
todowrite status list
```

### Advanced CLI Operations

```bash
# Update task status
todowrite update TSK-001 --status completed --progress 100

# Delete a node
todowrite delete GOAL-001

# Get specific node details
todowrite get TSK-001

# Check database status
todowrite db-status
```

## Scenario 3: Integration with Development Workflow

### Pre-commit Integration

```yaml
# .pre-commit-config.yaml
repos:
  - repo: local
    hooks:
      - id: todowrite-status
        name: Update ToDoWrite Status
        entry: todowrite status list
        language: system
        pass_filenames: false
        always_run: true
```

### CI/CD Pipeline Integration

```bash
#!/bin/bash
# ci_pipeline.sh

echo "Updating ToDoWrite status..."

# Update task status
todowrite update TSK-BUILD-001 --status in_progress --progress 50

# Run tests
pytest tests/

if [ $? -eq 0 ]; then
    # Tests passed - mark as completed
    todowrite update TSK-BUILD-001 --status completed --progress 100
    echo "Build completed successfully"
else
    # Tests failed - mark as blocked
    todowrite update TSK-BUILD-001 --status blocked --progress 25
    echo "Build failed - check logs"
    exit 1
fi

# Export status for reporting
todowrite export-yaml
```

### Development Environment Setup

```python
# scripts/project_setup.py
import os
from todowrite import ToDoWrite

def setup_project():
    """Initialize ToDoWrite project with standard structure"""

    app = ToDoWrite("sqlite:///project.db")
    app.init_database()

    # Create standard project structure
    phases = [
        {
            "id": "PH-001",
            "layer": "Phase",
            "title": "Development Phase",
            "description": "Core development work",
            "metadata": {"owner": "tech-lead", "labels": ["development"]}
        },
        {
            "id": "PH-002",
            "layer": "Phase",
            "title": "Testing Phase",
            "description": "Quality assurance and testing",
            "metadata": {"owner": "qa-lead", "labels": ["testing"]}
        },
        {
            "id": "PH-003",
            "layer": "Phase",
            "title": "Deployment Phase",
            "description": "Production deployment",
            "metadata": {"owner": "devops", "labels": ["deployment"]}
        }
    ]

    for phase in phases:
        app.create_node(phase)

    print("Project structure initialized")

if __name__ == "__main__":
    setup_project()
```

## Scenario 4: Database Migration and Backup

### Data Export for Backup

```python
from todowrite import export_nodes, import_nodes
import datetime

def backup_project():
    """Create timestamped backup of project data"""

    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_file = f"backup_project_{timestamp}.json"

    # Export all data
    result = export_nodes("sqlite:///project.db", backup_file)
    print(f"Backed up {len(result)} nodes to {backup_file}")

    return backup_file

def restore_project(backup_file):
    """Restore project from backup"""

    result = import_nodes("sqlite:///project.db", backup_file)
    print(f"Imported {result['imported']} nodes")
    print(f"Errors: {len(result['errors'])}")

    return result
```

### PostgreSQL Migration

```python
from todowrite import ToDoWrite

def migrate_to_postgres():
    """Migrate from SQLite to PostgreSQL"""

    # Export from SQLite
    sqlite_app = ToDoWrite("sqlite:///project.db")
    all_nodes = sqlite_app.get_all_nodes()

    # Import to PostgreSQL
    postgres_app = ToDoWrite("postgresql://user:password@localhost/projectdb")
    postgres_app.init_database()

    # Re-create all nodes
    for layer, nodes in all_nodes.items():
        for node in nodes:
            node_data = node.to_dict()
            postgres_app.create_node(node_data)

    print("Migration completed successfully")
```

## Scenario 5: API Integration

### Web API Wrapper

```python
# api_wrapper.py
from todowrite import ToDoWrite, search_nodes, update_node
from flask import Flask, jsonify, request

app = Flask(__name__)
tdw = ToDoWrite("sqlite:///project.db")
tdw.init_database()

@app.route("/api/tasks", methods=["GET"])
def get_tasks():
    """Get all tasks"""
    all_nodes = tdw.get_all_nodes()
    tasks = all_nodes.get("Task", [])

    return jsonify([task.to_dict() for task in tasks])

@app.route("/api/tasks/<task_id>", methods=["PUT"])
def update_task(task_id):
    """Update task status"""
    data = request.get_json()

    result = update_node("sqlite:///project.db", task_id, data)

    if result:
        return jsonify(result.to_dict())
    else:
        return jsonify({"error": "Task not found"}), 404

@app.route("/api/search", methods=["POST"])
def search_nodes():
    """Search nodes by criteria"""
    criteria = request.get_json()

    results = search_nodes("sqlite:///project.db", criteria)

    return jsonify([result.to_dict() for result in results])

if __name__ == "__main__":
    app.run(debug=True)
```

## Best Practices

### Data Structure Guidelines

1. **Consistent IDs**: Use clear, consistent ID patterns
2. **Complete Metadata**: Always include owner, severity, and labels
3. **Proper Linking**: Link nodes to establish clear relationships
4. **Status Updates**: Keep status and progress up to date

### Performance Considerations

1. **SQLite for Development**: Use SQLite for smaller projects
2. **PostgreSQL for Production**: Use PostgreSQL for larger datasets
3. **Regular Backups**: Export data regularly
4. **Indexing**: Ensure proper database indexing

### Security Guidelines

1. **Database Security**: Secure database connections
2. **Input Validation**: Use schema validation
3. **Access Control**: Implement proper user permissions
4. **Data Privacy**: Protect sensitive project data

## Troubleshooting

### Common Issues

1. **Database Connection**: Check database URL and permissions
2. **Schema Validation**: Ensure node data follows schema requirements
3. **ID Conflicts**: Use unique IDs for all nodes
4. **Link Integrity**: Ensure linked nodes exist

### Debug Commands

```bash
# Check database status
todowrite db-status

# Validate YAML files
todowrite sync-status

# Export data for inspection
todowrite export-yaml

# Run tests to verify functionality
pytest tests/
```

---

**Status**: ✅ Production Ready
**Version**: 0.3.1
**Tests**: 119/119 passing
**Implementation**: Real (no mocks)
