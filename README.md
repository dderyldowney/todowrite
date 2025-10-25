# ToDoWrite: A Standalone Task Management System

ToDoWrite is a comprehensive 12-layer declarative planning framework designed for managing complex projects, particularly in domains requiring rigorous hierarchical task management like agricultural robotics and safety-critical systems.

Originally integrated within the AFS FastAPI project, ToDoWrite has been refactored into a standalone Python package to allow for broader applicability and easier integration into various development workflows. It is primarily intended as a **development and testing mode only** package, providing robust task tracking and validation capabilities without imposing runtime dependencies on production systems.

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

ToDoWrite can be installed as a standalone Python package. It is recommended to install it in an editable mode for development purposes.

1.  **Clone the repository** (if you haven't already, or if you're integrating into an existing project):
    ```bash
    git clone https://github.com/dderyldowney/afs_fastapi.git
    cd afs_fastapi
    ```
2.  **Navigate to the `todowrite` directory**:
    ```bash
    cd todowrite
    ```
3.  **Create and activate a virtual environment** (recommended):
    ```bash
    python -m venv .venv
    source .venv/bin/activate
    ```
4.  **Install ToDoWrite in editable mode**:
    ```bash
    pip install -e .
    ```
    This command installs the package such that changes to the source code are immediately reflected without reinstallation.

## Usage

### Command Line Interface (CLI)

ToDoWrite provides a set of CLI tools for managing tasks. These tools are typically found in the `bin/` directory of the parent project (e.g., `afs_fastapi/bin/`).

Example commands:

-   **Initialize the database**:
    ```bash
    ./bin/loadsession # This command also initializes the todowrite database
    ```

-   **Add a new strategic goal**:
    ```bash
    ./bin/goal-add "Develop Autonomous Navigation System" "Implement a robust autonomous navigation system for agricultural vehicles."
    ```

-   **View strategic goals**:
    ```bash
    ./bin/strategic-status
    ```

-   **Add a phase to a goal**:
    ```bash
    ./bin/phase-add "Sensor Integration Phase" "Integrate various sensors for navigation." --goal-id GOAL-ID-HERE
    ```

-   **View all phases**:
    ```bash
    ./bin/phase-status
    ```

### Python API

ToDoWrite can be imported and used programmatically in your Python applications.

```python
from todowrite.manager import add_goal, load_todos, init_database

# Initialize the database (important for programmatic use)
init_database()

# Add a new goal
new_goal, error = add_goal(
    "Optimize Crop Yield", "Implement AI-driven strategies for maximizing crop yield."
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

To run the tests for the ToDoWrite package, navigate to the project root and execute:

```bash
PYTHONPATH=$PWD pytest todowrite/tests
```

### Linting and Formatting

Ensure code quality by running linters and formatters:

```bash
ruff check todowrite
black todowrite
isort todowrite
```

## Contributing

Contributions are welcome! Please ensure that all contributions adhere to the project's TDD guidelines, code quality standards, and include comprehensive tests.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
