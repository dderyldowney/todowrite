# ToDoWrite: Hierarchical Task Management System

[![Python 3.12+](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/)
[![Version 0.3.0](https://img.shields.io/badge/version-0.3.0-green.svg)](https://github.com/dderyldowney/todowrite)
[![PyPI](https://img.shields.io/badge/todowrite-0.3.0-blue.svg)](https://pypi.org/project/todowrite/)
[![PyPI CLI](https://img.shields.io/badge/todowrite--cli-0.3.0-blue.svg)](https://pypi.org/project/todowrite-cli/)
[![SQLAlchemy 2.0](https://img.shields.io/badge/SQLAlchemy-2.0-orange.svg)](https://www.sqlalchemy.org/)
[![Zero Tech Debt](https://img.shields.io/badge/tech%20debt-zero-red.svg)](https://github.com/dderyldowney/todowrite)
[![Security Hardened](https://img.shields.io/badge/security-hardened-green.svg)](https://github.com/dderyldowney/todowrite)

**ToDoWrite** is a sophisticated hierarchical task management system designed for complex project planning and execution. Built with a 12-layer declarative framework, it provides both standalone CLI capabilities and Python module integration for developers and project managers who need structured, traceable task management.

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

- **12-Layer Hierarchical Framework**: From high-level goals to executable commands
- **Dual Interface**: Standalone CLI application and Python module
- **Database Flexibility**: SQLite for development, PostgreSQL for production
- **Type Safety**: Comprehensive type hints with Python 3.12+ syntax
- **Status Tracking**: Full lifecycle management with status transitions
- **Relationship Management**: Parent-child relationships with link validation
- **YAML Configuration**: Human-readable project configuration and import/export
- **Zero Tech Debt**: All code quality checks pass (pytest, pyright, ruff, bandit)
- **Security Hardened**: Subprocess calls secured, proper exception handling throughout
- **Modern Python**: Pipe syntax, modern type annotations, comprehensive tooling
- **Centralized Version Management**: Single source of truth for version synchronization

## 🚀 Quick Start

### CLI Usage

```bash
# Initialize a project
todowrite init --database-path myproject.db

# Create a goal
todowrite create --goal "Implement User Authentication" --description "Create secure user authentication system"

# Create a task linked to the goal
todowrite create --task "Design Database Schema" --description "Design user database schema"

# Link task to goal
todowrite link --parent "GOAL-001" --child "TSK-001"

# View project status
todowrite status list
```

### Python API Usage

```python
from todowrite import ToDoWrite

# Initialize project
tdw = ToDoWrite(database_path="myproject.db")

# Create nodes
goal = tdw.create_node("goal", "Implement User Authentication", "Create secure auth system")
task = tdw.create_node("task", "Design Database Schema", "Design user database schema")

# Link nodes
tdw.link_nodes(goal["id"], task["id"])

# Get project overview
status = tdw.list_nodes()
print(f"Project has {len(status)} total nodes")
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
- **Test Coverage**: Comprehensive pytest test suite
- **Pre-commit**: Automated quality gates for all commits

### Recent v0.3.0 Improvements
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

**Current Version**: 0.3.0
**Python**: 3.12+
**Database**: SQLite (development) / PostgreSQL (production)
**Architecture**: Hierarchical task management with 12-layer planning framework
**Build System**: Hatchling + Twine
**Quality Status**: Zero Tech Debt Achieved 🎉
**License**: MIT

### Package Information

- **[todowrite](https://pypi.org/project/todowrite/)**: Core Python library
- **[todowrite-cli](https://pypi.org/project/todowrite-cli/)**: Command-line interface
- **[GitHub Repository](https://github.com/dderyldowney/todowrite)**: Source code and development
