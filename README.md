# ToDoWrite: Hierarchical Task Management System

[![Python 3.12+](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/)
[![Version 0.3.1](https://img.shields.io/badge/version-0.3.1-green.svg)](https://github.com/dderyldowney/todowrite)
[![PyPI](https://img.shields.io/badge/todowrite-0.3.1-blue.svg)](https://pypi.org/project/todowrite/)
[![PyPI CLI](https://img.shields.io/badge/todowrite--cli-0.3.1-blue.svg)](https://pypi.org/project/todowrite-cli/)
[![Tests Passing](https://img.shields.io/badge/tests-157%20passing-brightgreen.svg)](https://github.com/dderyldowney/todowrite)
[![Real Implementations](https://img.shields.io/badge/tests-real%20implementations-blue.svg)](https://github.com/dderyldowney/todowrite)

**ToDoWrite** is a hierarchical task management system designed for project planning and execution. It provides both CLI capabilities and Python module integration for developers and project managers who need structured task management with database persistence and schema validation.

## 🚀 Installation

### Library + CLI (Recommended)

Install both the core library and CLI interface:

```bash
# Install core library
pip install todowrite

# Install CLI interface (requires todowrite library)
pip install todowrite-cli

# For PostgreSQL support
pip install 'todowrite[postgres]'
pip install 'todowrite-cli[postgres]'
```

### Quick Install (All-in-One)

```bash
pip install todowrite todowrite-cli
```

### From GitHub (Development Version)

For the latest development version:

```bash
pip install git+https://github.com/dderyldowney/todowrite.git@main
pip install git+https://github.com/dderyldowney/todowrite.git@main#subdirectory=cli_package
```

### For Development

If you want to contribute or modify the code:

```bash
# Clone the repository
git clone https://github.com/dderyldowney/todowrite.git
cd todowrite

# Install development environment
./setup_dev.sh

# Or install manually
pip install -e "./lib_package[dev]"
pip install -e "./cli_package[dev]"
```

### Requirements

- **Python**: 3.12 or higher
- **Operating System**: Windows, macOS, or Linux
- **Dependencies**: SQLAlchemy 2.0+, JSONSchema 4.0+, PyYAML 6.0+

## 🎯 Overview

ToDoWrite transforms complex project planning into a structured, hierarchical framework that ensures nothing falls through the cracks. Whether you're managing software development projects, or any complex multi-stage initiative, ToDoWrite provides the structure and tools to break down goals into actionable commands.

### Key Features

- **Hierarchical Task Management**: Create goals, concepts, tasks, and commands
- **CLI and Python API**: Command-line interface and programmatic access
- **Database Storage**: SQLite and PostgreSQL support with SQLAlchemy
- **Schema Validation**: JSON Schema validation ensures data integrity
- **Progress Tracking**: Track task completion with progress percentages
- **Node Relationships**: Link related items with parent-child relationships
- **Import/Export**: JSON and YAML import/export functionality
- **Type Safety**: Comprehensive type hints with Python 3.12+ syntax
- **Status Management**: Track nodes through planned, in_progress, completed states
- **Real Testing**: 157 tests using actual implementations (no mocks)

## 🚀 Quick Start

### CLI Usage

```bash
# Initialize a project (creates todowrite.db in current directory)
todowrite init

# Create a goal
todowrite create --layer goal --title "Implement User Authentication" --description "Create secure user authentication system" --owner "dev-team"

# Create a task
todowrite create --layer task --title "Design Database Schema" --description "Design user database schema" --owner "dev-team"

# View all nodes
todowrite list

# Search for nodes
todowrite search "authentication"

# Export to YAML
todowrite export-yaml

# Get node details
todowrite get GOAL-001
```

### Python API Usage

```python
from todowrite import ToDoWrite

# Initialize project
tdw = ToDoWrite("sqlite:///myproject.db")
tdw.init_database()

# Create nodes
goal_data = {
    "id": "GOAL-001",
    "layer": "Goal",
    "title": "Implement User Authentication",
    "description": "Create secure auth system",
    "links": {"parents": [], "children": []},
    "metadata": {"owner": "dev-team", "labels": ["security"], "severity": "high"}
}
goal = tdw.create_node(goal_data)

task_data = {
    "id": "TSK-001",
    "layer": "Task",
    "title": "Design Database Schema",
    "description": "Design user database schema",
    "links": {"parents": [], "children": []},
    "metadata": {"owner": "dev-team", "labels": ["database"], "severity": "medium"}
}
task = tdw.create_node(task_data)

# Link nodes
from todowrite import link_nodes
link_nodes("sqlite:///myproject.db", goal.id, task.id)

# Get project overview
all_nodes = tdw.get_all_nodes()
total_nodes = sum(len(nodes) for nodes in all_nodes.values())
print(f"Project has {total_nodes} total nodes")
```

## 📚 Documentation

- **[BUILD_SYSTEM.md](BUILD_SYSTEM.md)**: Build system architecture and development workflows
- **[VERSION_MANAGEMENT.md](VERSION_MANAGEMENT.md)**: Centralized version management system
- **[PyPI_HOWTO.md](PyPI_HOWTO.md)**: Package publishing guide
- **[MONOREPO_STRUCTURE.md](MONOREPO_STRUCTURE.md)**: Project architecture overview
- **[CLI Documentation](cli_package/README.md)**: Complete CLI reference and examples

## 🤝 Contributing

We welcome contributions to ToDoWrite! Please see our [Contributing Guidelines](CONTRIBUTING.md) for more information.

## 🔧 Code Quality & Security

### Quality Assurance Status ✅
- **Zero Tech Debt**: All code quality checks pass
- **Type Safety**: Perfect pyright compliance with strict mode
- **Code Style**: Black, isort, and ruff format compliant
- **Security**: Bandit-compliant with hardened subprocess calls
- **Test Coverage**: 157/157 tests passing with comprehensive pytest suite (54.25% coverage)
- **Real Implementation Testing**: All tests use actual implementations, no mocks
- **Pre-commit**: Automated quality gates for all commits

### Recent v0.3.1 Improvements
- ✅ **Progress Field Fix**: Resolved storage/retrieval issue for node progress tracking
- ✅ **Library Verification Complete**: Comprehensive verification of all library components
- ✅ **Real Implementation Testing**: Verified all 157 tests use actual implementations, no mocks
- ✅ **Database Integrity Confirmed**: SQLite/PostgreSQL backends thoroughly tested
- ✅ **Schema Validation Robust**: All 12 layer types and 5 status types validated
- ✅ **Performance Verified**: Handles 100+ nodes efficiently (2.43s creation, 0.01s retrieval)
- ✅ **Static Analysis Compliant**: MyPy and Ruff validation passing
- ✅ **Installation Verified**: Package installs and imports correctly
- ✅ **Centralized Version Management**: Single source of truth for both packages
- ✅ **Modern Build System**: Hatchling + Twine with comprehensive tooling
- ✅ **Monorepo Structure**: Proper Python packaging standards
- ✅ **Asyncio Support**: Updated pytest configuration for modern async patterns
- ✅ **Security Hardening**: All subprocess calls use shell=False with proper validation

### Development Standards
- ✅ **Python 3.12+**: Modern syntax with type union operators (`str | None`)
- ✅ **PEP 517/518**: Compliant build system with hatchling backend
- ✅ **Static Analysis**: Comprehensive type checking and linting
- ✅ **Security**: Subprocess calls secured, proper exception handling throughout

## 🛠️ Development

### Build System

We use **Hatchling** as our build backend with **Twine** for publishing:

```bash
# Build packages
./scripts/build.sh

# Publish to TestPyPI
./scripts/publish.sh

# Publish to PyPI
./scripts/publish.sh prod

# Clean and build
./scripts/build.sh clean
```

See [BUILD_SYSTEM.md](BUILD_SYSTEM.md) for detailed documentation.

### Development Setup

```bash
# Clone and setup development environment
git clone https://github.com/dderyldowney/todowrite.git
cd todowrite

# Run development setup script
./setup_dev.sh

# Install development dependencies manually
pip install -e "./lib_package[dev]"
pip install -e "./cli_package[dev]"
```

### Version Management

Version is centrally managed using the `VERSION` file:

```bash
# Get current version
python scripts/bump_version.py get

# Bump version
python scripts/bump_version.py bump 0.3.1
```

See [VERSION_MANAGEMENT.md](VERSION_MANAGEMENT.md) for complete details.

---

**Current Version**: 0.3.1
**Python**: 3.12+
**Database**: SQLite (development) / PostgreSQL (production)
**Architecture**: Hierarchical task management with 12-layer planning framework
**Build System**: Hatchling + Twine
**Quality Status**: Zero Tech Debt Achieved 🎉
**Test Status**: 157/157 tests passing, real implementations verified ✅
**License**: MIT

### Package Information

- **[todowrite](https://pypi.org/project/todowrite/)**: Core Python library
- **[todowrite-cli](https://pypi.org/project/todowrite-cli/)**: Command-line interface
- **[GitHub Repository](https://github.com/dderyldowney/todowrite)**: Source code and development
