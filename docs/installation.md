# Installation Guide

**Version**: 0.3.1
**Status**: Production Ready
**Last Updated**: November 8, 2025

## Overview

This document provides comprehensive installation instructions for ToDoWrite, including both end-user installation and development setup.

## Quick Start

### Install from PyPI (Recommended)

```bash
# Install core library
pip install todowrite

# Install CLI interface
pip install todowrite-cli

# For PostgreSQL support
pip install 'todowrite[postgres]'
pip install 'todowrite-cli[postgres]'
```

### Verify Installation

```bash
# Test library import
python -c "from todowrite import ToDoWrite; print('Library installed successfully')"

# Test CLI
todowrite --version
```

## Detailed Installation Options

### Option 1: Library + CLI (Production)

For production use with the latest stable version:

```bash
# Install both packages
pip install todowrite todowrite-cli

# Verify installation
todowrite init
todowrite create --layer goal --title "Test Goal" --description "Testing installation"
```

### Option 2: Development Version

For the latest development features from GitHub:

```bash
# Install from main branch
pip install git+https://github.com/dderyldowney/todowrite.git@main
pip install git+https://github.com/dderyldowney/todowrite.git@main#subdirectory=cli_package
```

### Option 3: Development Setup

For contributing to the project:

```bash
# Clone repository
git clone https://github.com/dderyldowney/todowrite.git
cd todowrite

# Run development setup script
./setup_dev.sh

# Or install manually
pip install -e "./lib_package[dev]"
pip install -e "./cli_package[dev]"

# Verify setup
export PYTHONPATH="lib_package/src:cli_package/src"
python -m pytest
```

## System Requirements

### Required
- **Python**: 3.12 or higher
- **Operating System**: Windows, macOS, or Linux
- **Database**: SQLite (built-in) or PostgreSQL

### Dependencies (Automatically Installed)

**Core Library (`todowrite`)**:
- `sqlalchemy>=2.0.0` - Database ORM
- `jsonschema>=4.0.0` - Schema validation
- `pyyaml>=6.0` - YAML file support

**CLI Package (`todowrite-cli`)**:
- `todowrite>=0.3.1` - Core library
- `click>=8.0.0` - CLI framework
- `rich>=13.0.0` - Rich terminal output

**Optional PostgreSQL Support**:
- `psycopg2-binary>=2.9.0` - PostgreSQL adapter

## Database Setup

### SQLite (Default)

```bash
# Initialize with SQLite (default)
todowrite init
# Creates todowrite.db in current directory
```

### PostgreSQL (Optional)

```bash
# Install PostgreSQL support
pip install 'todowrite[postgres]'

# Initialize with PostgreSQL
todowrite init --database-url "postgresql://user:password@localhost/todowrite"
```

Or set environment variable:

```bash
export TODOWRITE_DATABASE_URL="postgresql://user:password@localhost/todowrite"
todowrite init
```

## Development Environment

### Prerequisites

```bash
# Ensure Python 3.12+
python --version

# Install development tools
pip install hatchling twine pytest pytest-cov ruff black mypy
```

### Development Workflow

```bash
# Clone repository
git clone https://github.com/dderyldowney/todowrite.git
cd todowrite

# Setup development environment
./setup_dev.sh

# Run tests
export PYTHONPATH="lib_package/src:cli_package/src"
python -m pytest

# Build packages
./scripts/build.sh

# Install locally
pip install -e "./lib_package[dev]"
pip install -e "./cli_package[dev]"
```

## Troubleshooting

### Common Issues

**Issue**: `ModuleNotFoundError: No module named 'todowrite'`
```bash
# Solution: Install packages or set PYTHONPATH
pip install todowrite todowrite-cli
# OR for development:
export PYTHONPATH="lib_package/src:cli_package/src"
```

**Issue**: Database connection errors
```bash
# Solution: Check database permissions and PostgreSQL status
todowrite db-status
```

**Issue**: CLI command not found
```bash
# Solution: Verify CLI package installation
pip install todowrite-cli
todowrite --version
```

### Verification Commands

```bash
# Test library functionality
python -c "
from todowrite import ToDoWrite
app = ToDoWrite('sqlite:///test.db')
app.init_database()
print('✓ Library working correctly')
"

# Test CLI functionality
todowrite init
todowrite list
echo "✓ CLI working correctly"
```

## Next Steps

After successful installation:

1. **Read the main [README.md](../README.md)** for project overview
2. **Follow the [Integration Guide](INTEGRATION_GUIDE.md)** for usage examples
3. **Consult the [CLI Documentation](../cli_package/README.md)** for command reference
4. **Review [Contributing Guidelines](../CONTRIBUTING.md)** for development

## Additional Documentation

- **[← Documentation Index](README.md)** - Complete documentation overview
- **[Main Project Documentation](../README.md)** - Project overview and features
- **[CLI Reference](../cli_package/README.md)** - Command-line interface reference
- **[Integration Guide](INTEGRATION_GUIDE.md)** - Usage examples and tutorials
- **[Project Architecture](../MONOREPO_STRUCTURE.md)** - Monorepo structure
- **[Build System](../BUILD_SYSTEM.md)** - Build system documentation
- **[Version Management](../VERSION_MANAGEMENT.md)** - Version management system

---

**Current Version**: 0.3.1
**Python Support**: 3.12+
**Test Status**: 157/157 tests passing ✅
**License**: MIT
