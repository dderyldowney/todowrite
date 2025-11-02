# Test Organization

This directory contains organized tests for the ToDoWrite project, separated by functionality and component.

## Directory Structure

```
tests/
├── cli/                    # CLI-specific tests
│   ├── __init__.py
│   └── test_cli.py         # Basic CLI functionality tests
├── core/                   # Core application tests
│   ├── __init__.py
│   └── test_app.py         # Core ToDoWrite app functionality
├── database/               # Database-specific tests (currently empty)
│   ├── __init__.py
├── storage/                # Storage-specific tests (currently empty)
│   ├── __init__.py
└── workflows/              # End-to-end user workflow tests
    ├── __init__.py
    ├── test_user_cli_workflows.py      # CLI user scenario tests
    └── test_user_library_workflows.py  # Library user scenario tests
```

## Running Tests

### Run all tests:
```bash
python -m pytest tests/
```

### Run tests by directory:
```bash
# CLI tests only
python -m pytest tests/cli/

# Core tests only
python -m pytest tests/core/

# Workflow tests only
python -m pytest tests/workflows/
```

### Run specific test file:
```bash
python -m pytest tests/cli/test_cli.py
python -m pytest tests/workflows/test_user_cli_workflows.py
```

## Test Categories

### CLI Tests (`tests/cli/`)
- Basic CLI command testing
- Command interface validation
- CLI error handling

### Core Tests (`tests/core/`)
- Core application logic
- Database operations
- Main functionality testing

### Workflow Tests (`tests/workflows/`)
- **CLI Workflows**: Complete user scenarios using the command-line interface
- **Library Workflows**: Complete user scenarios using the Python library API
- End-to-end testing of real-world usage patterns

### Database Tests (`tests/database/`)
- Database schema validation
- Database operation testing
- Database error handling
*(Currently empty - add database-specific tests here)*

### Storage Tests (`tests/storage/`)
- YAML storage operations
- Storage backend testing
- Storage error handling
*(Currently empty - add storage-specific tests here)*

## Test Naming Convention

All tests follow the pattern:
- **Component tests**: `test_{component}_{functionality}.py`
- **Workflow tests**: `test_{user_type}_{workflow_type}.py`

Example workflow test names:
- `test_cli_initialization_workflow`
- `test_library_node_creation_workflow`
- `test_cli_progress_tracking_workflow`

## Adding New Tests

1. **Component tests**: Add to the appropriate subdirectory
2. **Workflow tests**: Add to `workflows/` with descriptive names
3. **Database tests**: Add to `database/` when needed
4. **Storage tests**: Add to `storage/` when needed

## Coverage

- **Total tests**: 27
- **CLI tests**: 4
- **Core tests**: 5
- **Workflow tests**: 18 (8 CLI workflows + 10 library workflows)
- **Database tests**: 0
- **Storage tests**: 0
