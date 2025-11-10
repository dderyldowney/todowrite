# ToDoWrite Monorepo Structure

This document describes the updated monorepo structure that follows Python packaging best practices.

## Project Structure

The project follows the standard `src/` layout as recommended by the [Python Packaging User Guide](https://packaging.python.org/en/latest/tutorials/packaging-projects/):

```
todowrite/
├── lib_package/                  # todowrite library package
│   ├── src/
│   │   └── todowrite/           # Library source code
│   │       ├── __init__.py
│   │       ├── core/            # Core application logic
│   │       │   ├── __init__.py
│   │       │   ├── app.py
│   │       │   ├── app_node_updater.py
│   │       │   ├── constants.py
│   │       │   ├── exceptions.py
│   │       │   ├── project_manager.py
│   │       │   ├── schema.py
│   │       │   ├── types.py
│   │       │   ├── utils.py
│   │       │   └── schemas/
│   │       ├── database/        # Database models and configuration
│   │       │   ├── __init__.py
│   │       │   ├── config.py
│   │       │   └── models.py
│   │       ├── storage/         # Storage backends (YAML, etc.)
│   │       │   ├── __init__.py
│   │       │   ├── yaml_manager.py
│   │       │   ├── yaml_storage.py
│   │       │   └── schema_validator.py
│   │       ├── tools/           # Utility tools and scripts
│   │       │   ├── __init__.py
│   │       │   ├── extract_schema.py
│   │       │   ├── tw_lint_soc.py
│   │       │   ├── tw_stub_command.py
│   │       │   ├── tw_trace.py
│   │       │   └── tw_validate.py
│   │       ├── version.py
│   │       └── py.typed
│   ├── pyproject.toml           # Library build configuration
│   ├── README.md
│   ├── LICENSE
│   └── setup.py
├── cli_package/                  # todowrite_cli package
│   ├── src/
│   │   └── todowrite_cli/       # CLI source code
│   │       ├── __init__.py
│   │       ├── __main__.py
│   │       ├── main.py
│   │       └── version.py
│   ├── pyproject.toml           # CLI build configuration
│   ├── README.md
│   ├── LICENSE
│   └── setup.py
├── web_package/                  # todowrite_web package (FastAPI + TypeScript)
│   ├── src/
│   │   └── todowrite_web/       # Web package source code
│   │       ├── __init__.py      # Main package interface (imports from backend)
│   │       ├── backend/          # Python backend module
│   │       │   ├── __init__.py  # Backend module interface
│   │       │   ├── models.py    # Pydantic models for all entities
│   │       │   ├── utils.py     # Utility functions for node management
│   │       │   └── api/         # FastAPI API structure
│   │       │       ├── __init__.py
│   │       │       ├── middleware/
│   │       │       │   └── __init__.py
│   │       │       └── v1/
│   │       │           ├── __init__.py
│   │       │           └── endpoints/
│   │       │               └── __init__.py
│   │       └── frontend/        # TypeScript frontend
│   │           ├── jest.config.js
│   │           ├── package.json
│   │           ├── public/
│   │           │   └── index.html
│   │           └── src/
│   │               ├── components/
│   │               └── types/
│   │                   └── index.ts
│   ├── pyproject.toml           # Web package build configuration
│   ├── README.md
│   ├── LICENSE
│   └── setup.py
├── tests/                       # Test files organized by package and subsystem
│   ├── lib/                     # Library package tests
│   │   ├── api/                 # General library API tests
│   │   ├── core/                # Core application logic tests
│   │   ├── database/            # Database models and configuration tests
│   │   ├── storage/             # Storage backend tests (YAML, etc.)
│   │   ├── schema/              # Schema validation tests
│   │   └── tools/               # Utility tools and scripts tests
│   ├── cli/                     # CLI package tests
│   ├── web/                     # Web package tests
│   │   ├── api/                 # API endpoint tests
│   │   ├── backend/             # FastAPI application tests
│   │   ├── frontend/            # Frontend TypeScript tests
│   │   ├── models/              # Shared model tests
│   │   └── utils/               # Shared utility tests
│   └── shared/                  # Cross-package shared tests
│       ├── development/         # Development workflow tests
│       ├── unit/                # Multi-package unit tests
│       ├── workflows/           # End-to-end workflow tests
│       ├── features/            # Feature-specific tests
│       ├── test_flexible_entry_points.py
│       └── test_todowrite_flexible_hierarchy.py
├── pyproject.toml               # Root development configuration
├── pyrightconfig.json
├── .pre-commit-config.yaml
├── Makefile
└── README.md
```

## Package Dependencies

- **todowrite** (library): Core functionality for managing Goals, Tasks, Concepts, and Commands
- **todowrite_cli** (CLI): Thin wrapper around the library that provides command-line interface
- **todowrite_web** (web package): FastAPI backend + TypeScript frontend for web interface

The CLI and web packages depend on the library (`todowrite>=0.2.0`), but the library is completely independent and can be used on its own. The web package provides both REST API endpoints and a modern TypeScript frontend.

## Building and Installation

### Development Installation

For development, install all packages in editable mode:

```bash
# Install the library
pip install -e ./lib_package

# Install the CLI
pip install -e ./cli_package

# Install the web package
pip install -e ./web_package
```

### Running Tests

Tests are located in the `tests/` directory and can be run from the project root:

```bash
# Set PYTHONPATH to include all src directories
export PYTHONPATH="lib_package/src:cli_package/src:web_package/src"

# Run all tests
python -m pytest tests/

# Run tests for specific package
python -m pytest tests/lib/
python -m pytest tests/cli/
python -m pytest tests/web/

# Run tests for specific subsystem
python -m pytest tests/lib/core/
python -m pytest tests/web/api/
python -m pytest tests/shared/
```

### Building Packages

Each package can be built independently:

```bash
# Build the library
cd lib_package
python -m build

# Build the CLI
cd ../cli_package
python -m build

# Build the web package
cd ../web_package
python -m build
```

### Installing from PyPI

```bash
# Install the library
pip install todowrite

# Install the CLI (will also install the library)
pip install todowrite-cli

# Install the web package (will also install the library)
pip install todowrite-web
```

## Development Workflow

### Code Quality Tools

The project uses several code quality tools configured in the root `pyproject.toml`:

- **Black**: Code formatting
- **Ruff**: Linting and import sorting
- **Pyright**: Type checking
- **pytest**: Testing
- **Coverage**: Test coverage

### Development Commands

```bash
# Format code
black src/ tests/

# Lint code
ruff check src/ tests/

# Type check
pyright src/

# Run tests with coverage
python -m pytest tests/ --cov=src --cov-report=html
```

## Key Benefits of This Structure

1. **Clear Separation**: Library, CLI, and Web are separate packages with their own build configurations
2. **Standard Layout**: Follows Python packaging guidelines with `src/` layout for all packages
3. **Independent Development**: Each package can be developed, tested, and released independently
4. **Organized Tests**: Tests organized by package and subsystem for better maintainability
5. **Clean Dependencies**: Clear dependency relationship between packages
6. **Full-Stack Support**: Complete stack from library core to CLI and web interface

## Migration Notes

This structure was migrated from a non-standard layout to follow Python packaging best practices. The key changes were:

1. Moved source code from `lib_package/todowrite/`, `cli_package/todowrite_cli/`, and `web_package/todowrite_web/` to `src/todowrite/`, `src/todowrite_cli/`, and `src/todowrite_web/`
2. Updated all `pyproject.toml` files to reference the new `src/` structure
3. Added comprehensive web package with FastAPI backend and TypeScript frontend
4. Reorganized tests by package and subsystem for better maintainability
5. Adjusted build configurations, test paths, and coverage settings
6. Maintained backward compatibility for all imports and functionality

The API and functionality remain exactly the same - only the project structure has been improved and extended with full-stack capabilities.
