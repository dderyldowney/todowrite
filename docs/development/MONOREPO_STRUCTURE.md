# ToDoWrite Monorepo Structure

## Overview

ToDoWrite is a **3-package monorepo** providing a complete hierarchical task management system. Each package serves a specific purpose while sharing common functionality and version management.

## Package Structure

```
todowrite/
├── lib_package/              # Core Python library (todowrite)
├── cli_package/              # Command-line interface (todowrite-cli)
├── web_package/              # Web frontend (todowrite-web)
├── docs/                     # Documentation
├── scripts/                  # Build and deployment scripts
├── tests/                    # Cross-package integration tests
├── VERSION                   # Centralized version file
└── pyproject.toml           # Root project configuration
```

## Package Details

### 1. lib_package/ - Core Library

**Package Name**: `todowrite`
**Purpose**: Core functionality and Python API
**Primary Users**: Python developers embedding ToDoWrite

#### Structure
```
lib_package/
├── pyproject.toml           # Package configuration
├── src/
│   └── todowrite/
│       ├── __init__.py     # Public API exports
│       ├── core/           # Core business logic
│       │   ├── __init__.py
│       │   ├── app.py      # Main application class
│       │   ├── models.py   # Data models and types
│       │   └── validators.py
│       ├── database/       # Database layer
│       │   ├── __init__.py
│       │   ├── config.py   # Database configuration
│       │   ├── models.py   # SQLAlchemy models
│       │   └── migrations/
│       ├── storage/        # Storage backends
│       │   ├── __init__.py
│       │   ├── yaml_manager.py
│       │   └── file_storage.py
│       └── version.py      # Version information
├── tests/                  # Unit tests
└── README.md              # Package-specific docs
```

#### Key Components
- **12-Layer Hierarchy**: Goal → Concept → Context → Constraint → Requirement → AcceptanceCriteria → InterfaceContract → Phase → Step → Task → SubTask → Command
- **Database Abstraction**: SQLite (default), PostgreSQL support
- **YAML Import/Export**: Human-readable data persistence
- **Type Safety**: 100% type annotations, Pyright strict mode

### 2. cli_package/ - Command-Line Interface

**Package Name**: `todowrite-cli`
**Purpose**: Command-line interface for end users
**Primary Users**: DevOps, developers, power users

#### Structure
```
cli_package/
├── pyproject.toml           # Package configuration
├── src/
│   └── todowrite_cli/
│       ├── __init__.py     # Package initialization
│       ├── main.py         # CLI entry point and command groups
│       ├── commands/       # Command implementations
│       │   ├── __init__.py
│       │   ├── create.py   # Node creation commands
│       │   ├── get.py      # Node retrieval commands
│       │   ├── update.py   # Node modification commands
│       │   ├── delete.py   # Node deletion commands
│       │   ├── list.py     # Node listing commands
│       │   ├── search.py   # Search functionality
│       │   ├── import.py   # Import commands
│       │   └── export.py   # Export commands
│       ├── formatters/     # Output formatting
│       │   ├── __init__.py
│       │   ├── table.py    # Table output
│       │   ├── json.py     # JSON output
│       │   └── yaml.py     # YAML output
│       └── utils/          # CLI utilities
│           ├── __init__.py
│           ├── config.py   # Configuration management
│           └── validation.py
├── tests/                  # CLI-specific tests
└── README.md              # CLI documentation
```

#### Key Features
- **Click Framework**: Modern CLI tooling
- **Multiple Output Formats**: Table, JSON, YAML
- **Interactive Mode**: Guided operations
- **Configuration Management**: User settings and profiles
- **Currently Supports**: 4/12 layers (Goal, Task, Concept, Command)

### 3. web_package/ - Web Frontend

**Package Name**: `todowrite-web`
**Purpose**: Web-based user interface
**Primary Users**: Project managers, team collaborators
**Status**: 🚧 **Currently in Development** (Active development in progress)

#### Current Implementation Status
```
web_package/
├── pyproject.toml           # Package configuration ✅
├── uv.lock                 # Dependency lock file ✅
├── docker-compose.yml      # Development environment ✅
├── nginx.conf              # Reverse proxy configuration ✅
├── src/
│   └── todowrite_web/
│       ├── __init__.py     # Web application initialization ✅
│       ├── api/            # API layer ✅
│       │   ├── backend/    # FastAPI backend ✅
│       │   │   ├── main.py      # FastAPI application ✅
│       │   │   ├── models.py    # API data models ✅
│       │   │   ├── utils.py     # Utility functions ✅
│       │   │   ├── middleware/  # Middleware components ✅
│       │   │   └── v1/          # API version 1 ✅
│       │   │       └── endpoints/  # API endpoints 🚧
│       │   └── frontend/   # Frontend components 🚧
├── tests/                  # Web-specific tests 🚧
└── README.md              # Web documentation ✅
```

#### Current Development Focus
- **FastAPI Backend**: REST API implementation in progress
- **API Models**: Data models for web interface
- **Version 1 API**: Structured endpoint organization
- **Docker Support**: Development environment setup
- **Frontend Planning**: Frontend component architecture

#### Planned Features (Next Phases)
- **REST API**: Full CRUD operations for all 12 layers
- **Real-time Updates**: WebSocket integration
- **Visual Hierarchy**: Interactive tree views
- **Team Collaboration**: Multi-user support
- **Dashboard**: Project overview and analytics

## Inter-Package Dependencies

### Dependency Flow
```
web_package
    ↓ (depends on)
cli_package
    ↓ (depends on)
lib_package
```

### Integration Points
1. **Shared Models**: All packages use the same data models from `lib_package`
2. **Database Schema**: Centralized in `lib_package/database/`
3. **Configuration**: Shared via environment variables and config files
4. **Version Management**: Centralized in root `VERSION` file

## Build System

### Root pyproject.toml
```toml
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[project]
name = "todowrite-monorepo"
version = "0.4.0"  # From VERSION file
description = "Hierarchical task management system monorepo"

[tool.hatch.build.targets.wheel]
packages = ["src/todowrite"]

[tool.hatch.envs.default]
dependencies = [
    "lib_package[dev]",
    "cli_package[dev]",
]

[tool.hatch.envs.test]
dependencies = [
    "pytest>=7.0.0",
    "pytest-cov>=4.0.0",
]
```

### Version Management
- **Central Version**: `VERSION` file in root
- **Sync Script**: `scripts/sync_version.py`
- **Automatic Updates**: Pre-commit hooks ensure version consistency

### Build Commands
```bash
# Build all packages
./scripts/build.sh

# Build specific package
./scripts/build.sh lib_package

# Build and publish
./scripts/build.sh --publish

# Run tests across all packages
./scripts/test.sh
```

## Development Workflow

### 1. Package Development
```bash
# Work on core library
cd lib_package
pip install -e ".[dev]"
python -m pytest

# Work on CLI
cd cli_package
pip install -e ".[dev]"
python -m todowrite_cli --help

# Work on web
cd web_package
pip install -e ".[dev]"
uvicorn todowrite_web.app:app --reload
```

### 2. Integration Testing
```bash
# Cross-package integration tests
python -m pytest tests/integration/

# CLI integration with library
cd cli_package
python -m todowrite_cli create --goal "Test Goal"
```

### 3. Release Process
```bash
# Update version
echo "0.4.1" > VERSION
python scripts/sync_version.py

# Build and test
./scripts/build.sh
./scripts/test.sh

# Publish packages
./scripts/publish.sh
```

## Testing Strategy

### 1. Unit Tests
- **lib_package/**: Core business logic tests
- **cli_package/**: Command interface tests
- **web_package/**: API endpoint tests

### 2. Integration Tests
- **tests/integration/**: Cross-package functionality
- **tests/e2e/**: End-to-end user workflows
- **tests/performance/**: Performance benchmarks

### 3. Test Coverage
- **Minimum**: 80% code coverage per package
- **Target**: 95% for core functionality
- **Tools**: pytest, pytest-cov, pytest-asyncio

## Configuration Management

### 1. Environment Variables
```bash
# Database configuration
TODOWRITE_DATABASE_URL="sqlite:///todowrite.db"
TODOWRITE_POSTGRES_URL="postgresql://user:pass@localhost/todowrite"

# Web configuration
TODOWRITE_WEB_HOST="localhost"
TODOWRITE_WEB_PORT="8000"
TODOWRITE_SECRET_KEY="your-secret-key"

# Development settings
TODOWRITE_DEBUG=true
TODOWRITE_LOG_LEVEL="INFO"
```

### 2. Configuration Files
```yaml
# todowrite.yaml (user config)
database:
  url: "sqlite:///projects.db"
  auto_migrate: true

cli:
  output_format: "table"
  default_limit: 50

web:
  host: "localhost"
  port: 8000
  debug: false
```

## Deployment Architecture

### 1. Standalone Deployment
```
┌─────────────────┐
│   CLI Package   │ ← Direct command line usage
└─────────────────┘

┌─────────────────┐
│  lib_package    │ ← Python library imports
└─────────────────┘
```

### 2. Web Application Deployment
```
┌─────────────────┐
│   web_package   │ ← Web interface
└─────────┬───────┘
          │ API calls
          ▼
┌─────────────────┐
│  lib_package    │ ← Core business logic
└─────────┬───────┘
          │ Database
          ▼
┌─────────────────┐
│   PostgreSQL    │ ← Production database
└─────────────────┘
```

### 3. Enterprise Deployment
```
┌─────────────────┐    ┌─────────────────┐
│   Load Balancer │ ←→ │   web_package   │ (multiple instances)
└─────────┬───────┘    └─────────────────┘
          │
          ▼
┌─────────────────┐    ┌─────────────────┐
│  Redis Cache    │ ←→ │  lib_package    │ (shared services)
└─────────────────┘    └─────────┬───────┘
                                │
                                ▼
                       ┌─────────────────┐
                       │   PostgreSQL    │ ← High availability cluster
                       └─────────────────┘
```

## Development Guidelines

### 1. Code Standards
- **Python 3.12+**: Modern syntax and type hints
- **Static Typing**: Pyright strict mode, no `Any` types
- **Code Quality**: Ruff formatting, pre-commit hooks
- **Testing**: 100% real implementations, no mocking

### 2. API Design
- **Consistency**: Same patterns across all packages
- **Type Safety**: All public APIs fully typed
- **Documentation**: Complete docstrings with examples
- **Error Handling**: Structured exceptions with context

### 3. Performance
- **Memory Efficiency**: Optimized data structures
- **Database Performance**: Indexed queries, connection pooling
- **CLI Performance**: Fast startup, minimal dependencies
- **Web Performance**: Caching, lazy loading

## Future Roadmap

### Phase 1: CLI Enhancement
- **Goal**: Support all 12 layers in CLI
- **Timeline**: Q1 2025
- **Features**: Advanced filtering, bulk operations, interactive mode

### Phase 2: Web Interface
- **Goal**: Complete web package implementation
- **Timeline**: Q2 2025
- **Features**: REST API, React frontend, real-time updates

### Phase 3: Enterprise Features
- **Goal**: Multi-tenant, team collaboration
- **Timeline**: Q3 2025
- **Features**: User management, permissions, audit logs

This monorepo structure enables efficient development, consistent APIs across packages, and flexible deployment options for different use cases.
