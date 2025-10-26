# ToDoWrite: A Standalone Task Management System

ToDoWrite is a comprehensive 12-layer declarative planning framework designed for managing complex projects requiring rigorous hierarchical task management. It provides a structured approach to project planning and execution with enforced hierarchy validation.

ToDoWrite is a truly standalone Python package that can be imported and used in any Python project. It provides robust task tracking and validation capabilities with flexible database backends (SQLite for development, PostgreSQL for production).

## Features

- **12-Layer Hierarchical Planning**: Structured framework from Vision down to Command for detailed task breakdown.
  ```
  VISION → MISSION → STRATEGY → INITIATIVE → PROGRAM → PROJECT →
  PHASE → MILESTONE → TASK → SUBTASK → ACTION → COMMAND
  ```
- **Database Persistence**: Supports PostgreSQL for production-grade task storage and SQLite for local development/testing.
- **Flexible Entry Points**: Start planning at any layer of the hierarchy.
- **Mandatory Hierarchy Completion**: Enforces that all layers below a chosen entry point must be defined.
- **CLI Tools**: Command-line interface for easy interaction and management of tasks.
- **Python API**: Comprehensive programmatic access for integration into other Python applications.
- **Alembic Migrations**: Manages database schema evolution.

## Installation

ToDoWrite can be installed as a standalone Python package.

### From Source (Development)

1.  **Clone the ToDoWrite repository**:
    ```bash
    git clone <todowrite-repository-url>
    cd todowrite
    ```
2.  **Create and activate a virtual environment** (recommended):
    ```bash
    python -m venv .venv
    source .venv/bin/activate  # On Windows: .venv\Scripts\activate
    ```
3.  **Install ToDoWrite in editable mode**:
    ```bash
    pip install -e .
    ```

### From PyPI (Future)

Once published, ToDoWrite will be available on PyPI:
```bash
pip install todowrite
```

## Usage

### Command Line Interface (CLI)

ToDoWrite provides a CLI tool for managing tasks:

```bash
todowrite --help
```

### Python API

ToDoWrite is designed to be imported and used programmatically in your Python applications:

```python
from todowrite.manager import add_goal, load_todos, init_database

# Initialize the database (important for programmatic use)
init_database()

# Add a new goal
new_goal, error = add_goal(
    "Develop Mobile Application", "Create a user-friendly mobile application with modern features."
)
if new_goal:
    print(f"New Goal Added: {new_goal['title']} (ID: {new_goal['id']})")

# Load all todos
todos_data = load_todos()
print(f"Total Goals: {len(todos_data.get('Goal', []))}")
```

## Development & Testing

ToDoWrite adheres to a strict Test-Driven Development (TDD) methodology. All code changes must be accompanied by failing tests first.

### Running Tests

To run the tests for the ToDoWrite package:

```bash
pytest tests/
```

### Linting and Formatting

Ensure code quality by running linters and formatters:

```bash
ruff check .
black .
isort .

## Contributing

Contributions are welcome! Please ensure that all contributions adhere to the project's TDD guidelines, code quality standards, and include comprehensive tests.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
