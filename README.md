# ToDoWrite: Hierarchical Task Management System

[![Python 3.12+](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/)
[![Version 0.1.7.1](https://img.shields.io/badge/version-0.1.7.1-green.svg)](https://github.com/dderyldowney/todowrite)
[![SQLAlchemy 2.0](https://img.shields.io/badge/SQLAlchemy-2.0-orange.svg)](https://www.sqlalchemy.org/)
[![Zero Tech Debt](https://img.shields.io/badge/tech%20debt-zero-red.svg)](https://github.com/dderyldowney/todowrite)
[![Security Hardened](https://img.shields.io/badge/security-hardened-green.svg)](https://github.com/dderyldowney/todowrite)

**ToDoWrite** is a sophisticated hierarchical task management system designed for complex project planning and execution. Built with a 12-layer declarative framework, it provides both standalone CLI capabilities and Python module integration for developers and project managers who need structured, traceable task management.

## 🚀 Installation

### From PyPI (Recommended)

```bash
pip install todowrite
```

### From GitHub (Latest Main Branch)

For the latest development version, you can install directly from the GitHub main branch:

```bash
pip install git+https://github.com/dderyldowney/todowrite.git@main
```

Or for a specific commit hash:
```bash
pip install git+https://github.com/dderyldowney/todowrite.git@<commit-hash>
```

### For Development

If you want to contribute or modify the code:

```bash
# Clone the repository
git clone https://github.com/dderyldowney/todowrite.git
cd todowrite

# Install with development dependencies
pip install -e ".[dev]"

# Or using setup.py
pip install -e .
```

### Requirements

- **Python**: 3.12 or higher
- **Operating System**: Windows, macOS, or Linux

## 🎯 Overview

ToDoWrite transforms complex project planning into a structured, hierarchical framework that ensures nothing falls through the cracks. Whether you're managing software development projects, or any complex multi-stage initiative, ToDoWrite provides the structure and tools to break down goals into actionable commands.

### Key Features

- **12-Layer Hierarchical Framework**: From high-level goals to executable commands
- **Dual Interface**: Standalone CLI application and Python module
- **Database Flexibility**: SQLite for development, PostgreSQL for production
- **Type Safety**: Comprehensive type hints with Python 3.12+ syntax
- **Status Tracking**: Full lifecycle management with status transitions
- **Relationship Management**: Parent-child relationships with link validation
- **Zero Tech Debt**: All code quality checks pass (pytest, mypy, ruff, bandit)
- **Security Hardened**: Subprocess calls secured, proper exception handling throughout
- **Modern Python**: Pipe syntax, modern type annotations, comprehensive tooling

## 📚 Documentation

For comprehensive documentation, including installation, usage, API references, and architectural details, please refer to the [main documentation index](docs/index.md).

## 🤝 Contributing

We welcome contributions to ToDoWrite! Please see our [Contributing Guidelines](CONTRIBUTING.md) for more information.

## 🔧 Code Quality & Security

### Quality Assurance Status ✅
- **9/9 pytest tests passing** - Full test coverage
- **0 mypy errors** - Perfect type safety
- **0 ruff linting errors** - Code style compliance
- **Bandit security** - Only LOW severity warnings (acceptable imports)

### Recent Security Hardening
- ✅ **HIGH severity** subprocess shell=True vulnerabilities fixed using `shlex.split()`
- ✅ **Try/except/pass** issues resolved with proper exception handling
- ✅ **Import security** - All subprocess usage now uses `shell=False`
- ✅ **Error handling** - Added comprehensive logging throughout

### Modern Python Standards
- ✅ **Type annotations** - Full pipe syntax (`str | None`) usage
- ✅ **Python 3.12+** - Modern syntax throughout
- ✅ **Formatting** - Black, isort, and ruff format compliance
- ✅ **Security** - Bandit-compliant with hardened subprocess calls

---

**Version**: 0.1.7.1
**Python**: 3.12+
**Database**: SQLite (development) / PostgreSQL (production)
**Architecture**: Hierarchical task management with 12-layer planning framework
**Quality Status**: Zero Tech Debt Achieved 🎉
