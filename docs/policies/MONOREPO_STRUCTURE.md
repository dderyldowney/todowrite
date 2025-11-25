# Monorepo Structure Policy

## Project Structure

**ToDoWrite is a Python monorepo with 3 packages:**

```
todowrite/                          # Root monorepo
├── docs/                           # Comprehensive documentation
│   └── policies/                   # Development policies and mandates
├── examples/                       # Usage examples for all packages
├── lib_package/                    # Core todowrite library
│   ├── src/todowrite/             # Library source code
│   └── pyproject.toml             # Library package config
├── cli_package/                    # Command-line interface
│   ├── src/todowrite_cli/         # CLI source code
│   └── pyproject.toml             # CLI package config
├── web_package/                    # Web interface (planned)
│   ├── src/todowrite_web/         # Web source code
│   └── pyproject.toml             # Web package config
├── tests/                          # Unified test suite
│   ├── lib_package/               # Library tests
│   ├── cli_package/               # CLI tests
│   └── web_package/               # Web tests
├── pyproject.toml                  # Root monorepo workspace config
├── uv.lock                        # UV workspace lockfile
└── README.md
```

## Package Management

### Monorepo Management
- **Primary Tool**: Always use `uv` workspace with root `pyproject.toml`
- **Package Development**: Each package has its own `pyproject.toml` and follows standard structure
- **Mirror Structure**: `tests/` mirrors package structure with separate directories for each package
- **Internal Dependencies**: Packages can depend on each other via workspace (e.g., CLI depends on lib)
- **Installation**: Use `uv sync` at root to install all workspace dependencies

### Development Commands

```bash
# Workspace operations
uv sync                           # Install all dependencies
uv add package_name               # Add to root workspace
uv add --package lib_package package_name  # Add to specific package

# Package development
uv run lib_package/src/todowrite/__main__.py     # Run library
uv run cli_package/src/todowrite_cli/main.py     # Run CLI

# Testing
uv run pytest tests/lib_package/                 # Library tests
uv run pytest tests/cli_package/                 # CLI tests
uv run pytest tests/                             # All tests
```

### Cross-Package Integration

- **Shared Types**: Place shared type definitions in `lib_package/src/todowrite/types/`
- **Internal Imports**: Use workspace imports (e.g., `from todowrite.core.models import Task`)
- **Dependency Declaration**: Declare inter-package dependencies in respective `pyproject.toml` files
- **Testing**: Test real data flow between packages, no mocking of core functionality

## File Organization Standards

- **Maximum 500 lines** per Python file
- **Documentation headers** required in every file
- **Validation functions** in main blocks for real data testing
- **Type hints** mandatory for all code (Python 3.12+ syntax)
