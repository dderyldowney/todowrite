# ToDoWrite — Hierarchical Task Management System
> **Status:** ACTIVE SYSTEM (Version 0.1.7.1) — Standalone Python package with 12-layer declarative planning framework.
> **Intent:** Complete 12-layer declarative planning framework with enforced Separation of Concerns. Only **Command** layer executes; all others are declarative YAML files.
> **User Types:** Supports both AI-enhanced and non-AI users with appropriate feature sets.

---

## 1) Overview

### System Version
- **Version:** 0.1.7.1 (Current Production)
- **Architecture:** 12-layer declarative hierarchy with build-time validation
- **Package:** Standalone Python package with CLI and Python module API

### User Types
1. **Non-AI Users** - Focus on core functionality, simple setup, essential features
2. **AI-Enhanced Users** - All core features plus token optimization and AI workflow enhancements

### Non‑negotiables
- Layers 1–11 are **non-executable** (no side effects, no CLI/API code)
- Layer 12 (**Command**) is the **only executable** layer
- **One concern per node.** Split mixed responsibilities horizontally
- **Traceability** is required (forward & backward links present)
- **Backward compatibility** maintained for existing YAML files

### Applies To
This repository and all projects using the ToDoWrite Python package.

## 2) Hierarchy (12 layers; only the last executes)

### I. Strategic & High-Level Planning (Layers 1-4)
| Layer | Name | Purpose | Storage Directory |
|-------|------|---------|------------------|
| 1 | **Goal** | Business/mission intent | `goals/` |
| 2 | **Concept** | Architectural approaches | `concepts/` |
| 3 | **Context** | Environment & assumptions | `contexts/` |
| 4 | **Constraints** | Standards & legal limits | `constraints/` |

### II. Specification & Definition (Layers 5-7)
| Layer | Name | Purpose | Storage Directory |
|-------|------|---------|------------------|
| 5 | **Requirements** | Atomic specifications | `requirements/` |
| 6 | **Acceptance Criteria** | Pass/fail conditions | `acceptance_criteria/` |
| 7 | **Interface Contract** | APIs & protocols | `interface_contracts/` |

### III. Work Breakdown & Granular Units (Layers 8-11)
| Layer | Name | Purpose | Storage Directory |
|-------|------|---------|------------------|
| 8 | **Phase** | Major delivery slices | `phases/` |
| 9 | **Step** | Single-concern work units | `steps/` |
| 10 | **Task** | Contributor work assignments | `tasks/` |
| 11 | **SubTask** | Smallest planning units | `subtasks/` |

### IV. Execution (Layer 12)
| Layer | Name | Purpose | Storage Directory |
|-------|------|---------|------------------|
| 12 | **Command** | **ONLY** executable layer | `commands/` |

## 3) Current Project Layout (Version 0.1.7.1)

### Core Package Structure
```
todowrite/
├── __init__.py                 # Main package exports
├── app.py                      # Core ToDoWrite application class
├── cli.py                      # Click-based CLI interface
├── types.py                    # Type definitions (Node, LayerType, StatusType)
├── schema.py                   # JSON schema validation
├── project_manager.py          # Centralized project utilities
├── yaml_manager.py             # YAML file management
├── db/
│   ├── __init__.py
│   ├── config.py               # Database configuration
│   └── models.py               # SQLAlchemy models
├── schemas/
│   └── todowrite.schema.json    # JSON Schema with status tracking
└── tools/
    ├── extract_schema.py       # Schema extraction utility
    ├── tw_lint_soc.py           # Separation of Concerns linter
    ├── tw_trace.py              # Traceability matrix generator
    ├── tw_stub_command.py       # Command stub generator
    ├── tw_validate.py           # Schema validator
    ├── git-commit-msg-hook.sh   # Git hook
    └── tw_deprecate.py          # Deprecated schema checker
```

### User Configuration Structure
```
project-root/
├── .todowrite/                 # Project configuration
│   ├── config.yaml             # Project settings
│   └── session.db              # Session database (optional)
├── configs/
│   ├── plans/                  # Declarative nodes (layers 1-11)
│   │   ├── goals/
│   │   ├── concepts/
│   │   ├── contexts/
│   │   ├── constraints/
│   │   ├── requirements/
│   │   ├── acceptance_criteria/
│   │   ├── interface_contracts/
│   │   ├── phases/
│   │   ├── steps/
│   │   ├── tasks/
│   │   └── subtasks/
│   ├── commands/               # Layer 12 executable commands
│   └── schemas/
│       └── todowrite.schema.json # Local schema copy
├── .env.todowrite              # Environment configuration
├── docker-compose.todowrite.yml # Docker setup (optional)
└── results/                    # Command execution artifacts
```

### Database Storage (Optional)
- **PostgreSQL** (Production): `postgresql://user:pass@host:port/dbname`
- **SQLite** (Development): `sqlite:///todowrite.db`
- **YAML Fallback**: Pure YAML storage without database

## 4) Project Utilities (New in v0.1.7.1)

The new `ProjectManager` class provides centralized utilities that replace individual scripts:

### For All Users (CLI Commands)
```bash
# Check project setup
todowrite utils validate-setup /path/to/project

# Set up project integration
todowrite utils setup-integration /path/to/project --db-type postgres

# Create project structure
todowrite utils create-structure /path/to/new-project

# Check schema integrity
todowrite utils check-schema
todowrite utils check-deprecated

# Get database initialization SQL
todowrite utils init-database-sql
```

### For All Users (Python API)
```python
from todowrite import setup_integration, validate_project_setup

# Set up project
setup_integration("/path/to/project", "sqlite")

# Validate project setup
results = validate_project_setup("/path/to/project")
print(f"Project valid: {results['valid']}")

# Check schema changes
from todowrite import check_schema_changes
check_schema_changes()

# Create project structure
from todowrite import create_project_structure
create_project_structure("/path/to/new-project")
```

### For AI-Enhanced Users (Internal Methods)
```python
from todowrite._optimize_token_usage import optimize_token_usage
from todowrite._ensure_token_sage import ensure_token_sage

# Check AI features availability
if ensure_token_sage():
    token_info = optimize_token_usage("Enhance task analysis")
    print(f"Tokens saved: {token_info['tokens_saved']}")
```

## 5) Node Schema (Updated with Status Tracking)

### Core Node Structure
```yaml
id: TSK-EXAMPLE-001
layer: Task
title: Example Task
description: Task description
status: in_progress              # planned, in_progress, completed, blocked, cancelled
progress: 75                    # 0-100 percentage
started_date: "2025-01-15T10:00:00Z"
completion_date: "2025-01-20T18:00:00Z"
assignee: developer             # Root level or in metadata
links:
  parents: []
  children: []
metadata:
  owner: system
  labels: [test, status]
  severity: med
  work_type: implementation
  assignee: developer           # Duplicate for backward compatibility
command: null                   # Only for Command layer
```

### Status Tracking Fields (New in v0.1.7.1)
- **status**: Node lifecycle state (planned, in_progress, completed, blocked, cancelled)
- **progress**: Completion percentage (0-100)
- **started_date**: ISO 8601 timestamp when work started
- **completion_date**: ISO 8601 timestamp when work completed
- **assignee**: Person responsible (available at root and metadata levels)

## 6) Installation & Setup

### For All Users
```bash
# Install from PyPI
pip install todowrite

# Install from source (for development)
git clone https://github.com/dderyldowney/todowrite.git
cd todowrite
pip install -e ".[dev]"
```

### Project Setup
```bash
# Initialize a new project
mkdir my-project
cd my-project

# Set up ToDoWrite integration
todowrite utils setup-integration . --db-type sqlite

# Validate setup
todowrite utils validate-setup .
```

### Optional: AI-Enhanced Setup
```bash
# Install AI dependencies (optional)
pip install openai anthropic

# AI features work automatically when available
todowrite utils setup-integration . --db-type postgres
```

## 7) Core API Reference

### ToDoWrite Application Class
```python
from todowrite import ToDoWrite

# Initialize application
app = ToDoWrite()

# Core CRUD operations
node = app.create_node(
    id="TSK-EXAMPLE-001",
    layer="Task",
    title="Example Task",
    description="Task description"
)

# Retrieve node
retrieved_node = app.get_node("TSK-EXAMPLE-001")

# Update node with status tracking
app.update_node("TSK-EXAMPLE-001", {
    "status": "in_progress",
    "progress": 50,
    "assignee": "developer"
})

# Delete node
app.delete_node("TSK-EXAMPLE-001")

# List nodes
nodes = app.list_nodes(layer="Task", status="in_progress")
```

### Status Management (New in v0.1.7.1)
```python
# Update status with tracking
from todowrite import update_node_status

update_node_status(
    node_id="TSK-EXAMPLE-001",
    status="completed",
    progress=100,
    completion_date="2025-01-20T18:00:00Z",
    assignee="developer"
)

# Generate status report
from todowrite.app import generate_status_report
report = generate_status_report(layer="Task", format="table")
```

## 8) CLI Commands

### Core Commands
```bash
# Initialize database
todowrite init

# Create node
todowrite create --id TSK-EXAMPLE-001 --layer Task --title "Example Task"

# List nodes
todowrite list --layer Task --status in_progress

# Get specific node
todowrite get TSK-EXAMPLE-001

# Update node
todowrite update TSK-EXAMPLE-001 --status completed

# Delete node
todowrite delete TSK-EXAMPLE-001

# Check database status
todowrite db-status

# Export/Import YAML
todowrite export-yaml
todowrite import-yaml

# Sync status
todowrite sync-status
```

### Status Tracking Commands (New in v0.1.7.1)
```bash
# Update status with tracking
todowrite status update TSK-EXAMPLE-001 \
  --status in_progress \
  --progress 50 \
  --assignee developer \
  --started-date "2025-01-15T10:00:00Z"

# Show status details
todowrite status show TSK-EXAMPLE-001

# Quick complete
todowrite status complete TSK-EXAMPLE-001

# Generate status report
todowrite status report --layer Task --format table
```

### Project Utility Commands (New in v0.1.7.1)
```bash
# Validate project setup
todowrite utils validate-setup /path/to/project

# Set up integration
todowrite utils setup-integration /path/to/project --db-type postgres

# Create project structure
todowrite utils create-structure /path/to/new-project

# Check schema integrity
todowrite utils check-schema
todowrite utils check-deprecated

# Get database SQL
todowrite utils init-database-sql
```

## 9) Database Configuration

### Environment Variables
```bash
# Database URL
TODOWRITE_DATABASE_URL=postgresql://todowrite:todowrite_dev_password@localhost:5432/todowrite

# Storage preference
TODOWRITE_STORAGE_PREFERENCE=both

# Logging level
LOG_LEVEL=INFO

# Schema validation
TODOWRITE_VALIDATE_SCHEMA=true

# Database migration
TODOWRITE_AUTO_MIGRATE=true
```

### Database Setup
```python
from todowrite.db import Database, DatabaseConfig

# Default configuration
db = Database()

# Custom configuration
config = DatabaseConfig(
    database_url="postgresql://user:pass@localhost:5432/dbname"
)
db = Database(config)
```

## 10) Development Workflows

### For Non-AI Users
```bash
# Setup and development
make tw-deps
make tw-init
make tw-all

# Regular maintenance
todowrite utils check-schema
todowrite utils validate-setup .
```

### For AI-Enhanced Users
```bash
# Setup with AI optimization
make tw-deps
make tw-init
make tw-all

# AI-enhanced workflow
if _ensure_token_sage():
    optimize_token_usage("Development tasks")
    make tw-dev  # AI-optimized validation
```

### Quality Assurance
```bash
# For all users
make tw-check    # Full validation with error exit codes
make tw-test     # Complete system test
make tw-hooks    # Install git hooks
```

## 11) Migration Guide

### From Old Scripts to New Utilities
```bash
# Old → New CLI commands
python scripts/check_deprecated_schema.py     →    todowrite utils check-deprecated
python scripts/check_schema_changes.py       →    todowrite utils check-schema
python scripts/setup-integration.py          →    todowrite utils setup-integration
cat init-scripts/01-init-todowrite.sql        →    todowrite utils init-database-sql
```

### YAML Schema Compatibility
- **Existing YAML files** continue to work unchanged
- **New status tracking** is optional - adds progressive enhancement
- **Backward compatibility** maintained for all fields

### Database Migration
- **Existing databases** automatically updated on first use
- **New columns** added: progress, started_date, completion_date, assignee
- **No data loss** during migration

## 12) User Type Guidelines

### Non-AI Users
- **Focus**: Core task management, simple setup, essential features
- **Database**: SQLite for development, PostgreSQL for production
- **Workflow**: CLI-driven, simple validation
- **Features**: Status tracking, project utilities, basic API

### AI-Enhanced Users
- **Focus**: Enhanced productivity, token optimization, advanced workflows
- **Database**: PostgreSQL for production environments
- **Workflow**: AI-enhanced validation, token optimization, advanced API
- **Features**: All core features plus token optimization, AI-aware validation

### Key Differences
| Feature | Non-AI Users | AI-Enhanced Users |
|---------|--------------|-------------------|
| Status Tracking | ✅ Available | ✅ Available + AI optimization |
| Token Optimization | ❌ Not available | ✅ Automatic when AI dependencies installed |
| Database Choice | SQLite/PostgreSQL | PostgreSQL preferred |
| Validation | Standard | AI-enhanced validation |
| Setup Complexity | Simple | Enhanced with AI features |

## 13) Quality Assurance

### Validation Tools
```bash
# Schema validation
make tw-validate

# Separation of Concerns checking
make tw-lint

# Full validation
make tw-all

# Traceability matrix
make tw-trace

# Command generation
make tw-prove
```

### Pre-commit Hooks
```bash
# Install hooks
make tw-hooks

# Hooks enforce:
# - Conventional commits
# - Schema validation
# - Separation of Concerns
# - Traceability checks
```

## 14) System Status: PRODUCTION READY (v0.1.7.1)

### ✅ Core Functionality
- **12-Layer Architecture**: Complete declarative planning framework
- **Status Tracking**: Enhanced progress tracking with dates and assignees
- **Project Utilities**: Centralized tools replacing individual scripts
- **Database Flexibility**: PostgreSQL, SQLite, and YAML fallback
- **CLI Interface**: Comprehensive command-line interface
- **Python Module**: Full API for integration
- **Schema Validation**: JSON Schema with backward compatibility
- **Traceability**: Complete forward/backward dependency tracking

### ✅ User Support
- **Non-AI Users**: All essential features work without AI dependencies
- **AI-Enhanced Users**: Additional optimization features when available
- **Migration Path**: Smooth upgrade from previous versions
- **Documentation**: Comprehensive guides for both user types

### ✅ Implementation State
- **Package Distribution**: Available on PyPI and GitHub
- **Development Tools**: All Makefile targets functional
- **Database Models**: Complete SQLAlchemy models with status tracking
- **CLI Commands**: Full command coverage including utilities
- **API Methods**: Complete Python module interface

## 15) Agent Requirements (NON-NEGOTIABLE)
1. **Load this system on every session startup**
2. **Use appropriate CLI commands for operations**
3. **Create YAML files in appropriate `configs/plans/` directories**
4. **Generate Commands only from Acceptance Criteria**
5. **Enforce Conventional Commit format on all commits**
6. **Validate before any git operations**
7. **Maintain traceability links in all nodes**
8. **Use project utilities for setup and maintenance**

## 16) Getting Started

### Quick Start (Non-AI)
```bash
# Install
pip install todowrite

# Create project
mkdir my-project
cd my-project

# Set up integration
todowrite utils setup-integration . --db-type sqlite

# Create first goal
todowrite create --id GOAL-PROJECT-VISION --layer Goal --title "Project Vision"

# List all nodes
todowrite list
```

### Quick Start (AI-Enhanced)
```bash
# Install with AI dependencies
pip install todowrite openai anthropic

# Set up with PostgreSQL
todowrite utils setup-integration . --db-type postgres

# AI-enhanced workflow
make tw-dev  # Includes AI-optimized validation

# Create and track tasks
todowrite create --id TSK-FIRST-TASK --layer Task --title "First Task"
todowrite status update TSK-FIRST-TASK --status in_progress --progress 50
```

### Comprehensive Documentation
- **Project Utilities**: [docs/PROJECT_UTILITIES.md](docs/PROJECT_UTILITIES.md)
- **Status Tracking**: [docs/STATUS_TRACKING.md](docs/STATUS_TRACKING.md)
- **Installation Guide**: [INSTALLATION_GUIDE.md](INSTALLATION_GUIDE.md)
- **Complete API Reference**: Available in package and docs

## 17) Troubleshooting

### Common Issues
```bash
# Import errors
from todowrite import setup_integration  # Ensure package is installed

# Database connection issues
export TODOWRITE_DATABASE_URL=sqlite:///todowrite.db  # Use SQLite

# Schema validation failures
todowrite utils check-schema  # Validate schema integrity
```

### Debug Mode
```bash
export LOG_LEVEL=debug
todowrite utils validate-setup .
```

### Support
- **Documentation**: Comprehensive guides for both user types
- **Examples**: Working examples in configs/plans/
- **Validation**: Built-in validation and troubleshooting tools
- **Community**: GitHub issues and discussions

---

**ToDoWrite** - Hierarchical task management for complex projects, supporting both AI and non-AI users with appropriate feature sets.
