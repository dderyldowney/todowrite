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
├── tests/                       # Test files (shared for both packages)
│   ├── cli/
│   ├── core/
│   ├── database/
│   ├── library/
│   ├── schema/
│   ├── storage/
│   └── workflows/
├── pyproject.toml               # Root development configuration
├── pyrightconfig.json
├── .pre-commit-config.yaml
├── Makefile
└── README.md
```

## Package Dependencies

- **todowrite** (library): Core functionality for managing Goals, Tasks, Concepts, and Commands
- **todowrite_cli** (CLI): Thin wrapper around the library that provides command-line interface

The CLI package depends on the library (`todowrite>=0.2.0`), but the library is completely independent and can be used on its own.

## Building and Installation

### Development Installation

For development, install both packages in editable mode:

```bash
# Install the library
pip install -e ./lib_package

# Install the CLI
pip install -e ./cli_package
```

### Running Tests

Tests are located in the `tests/` directory and can be run from the project root:

```bash
# Set PYTHONPATH to include both src directories
export PYTHONPATH="lib_package/src:cli_package/src"

# Run all tests
python -m pytest tests/

# Run tests for specific module
python -m pytest tests/core/
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
```

### Installing from PyPI

```bash
# Install the library
pip install todowrite

# Install the CLI (will also install the library)
pip install todowrite-cli
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

1. **Clear Separation**: Library and CLI are separate packages with their own build configurations
2. **Standard Layout**: Follows Python packaging guidelines with `src/` layout
3. **Independent Development**: Each package can be developed, tested, and released independently
4. **Shared Tests**: Common test infrastructure for both packages
5. **Clean Dependencies**: Clear dependency relationship between packages

## Migration Notes

This structure was migrated from a non-standard layout to follow Python packaging best practices. The key changes were:

1. Moved source code from `lib_package/todowrite/` and `cli_package/todowrite_cli/` to `src/todowrite/` and `src/todowrite_cli/`
2. Updated all `pyproject.toml` files to reference the new `src/` structure
3. Adjusted build configurations, test paths, and coverage settings
4. Maintained backward compatibility for all imports and functionality

The API and functionality remain exactly the same - only the project structure has been improved.
