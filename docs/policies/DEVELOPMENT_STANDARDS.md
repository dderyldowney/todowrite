# Development Standards Policy

## Module Requirements

### File Structure
- **Maximum 500 lines** per Python file (split larger files logically)
- **Documentation Header**: Every file MUST include:
  - Description of purpose and role in monorepo
  - Links to third-party package documentation
  - Sample input/output examples
  - Cross-package integration notes (if applicable)
- **Validation Function**: Every Python file needs a main block (`if __name__ == "__main__":`) that tests with real data

### Architecture Principles

#### Function-First Development
- **Prefer simple functions** over classes throughout the monorepo
- **Class Usage**: Only use classes when:
  - Maintaining state across package boundaries
  - Implementing data validation models
  - Following established design patterns

#### Async Code Standards
- **Never use `asyncio.run()` inside functions** - only in main blocks
- **NO Conditional Imports**: Never use try/except blocks for imports of required packages

## 🔴 100% Type Hinting Requirement

### Mandatory Type Coverage
**All Python code MUST include:**
- Full type hints
- Modern Python 3.12+ syntax
- `from __future__ import annotations`
- No use of `Any`
- Typed variables, fields, returns, parameters

If a type hint is missing → **STOP**.

## Type Hints Standards (Python 3.12+ MANDATORY)

### 100% Coverage Requirements
- **ALL code MUST have comprehensive type hinting** (functions, classes, methods, variables, returns)
- **Python 3.12+ Syntax Only**: Use modern type hinting syntax:
  - `|` for unions (not `Union`)
  - `list[str]` instead of `List[str]`
  - `T | None` instead of `Optional[T]`
- **No 'Any' Types**: Replace `Any` with specific types or `typing.Never` when truly no type applies
- **Forward References**: Always use `from __future__ import annotations`

### Cross-Package Types
- **Shared type definitions** should be in `lib_package/src/todowrite/types/`
- **Import paths**: Use proper workspace imports for shared types

### Example Implementation

```python
# CORRECT - Python 3.12+ modern type hinting for monorepo:
from __future__ import annotations
from todowrite.types import TaskConfig, ValidationResult  # Shared types

def process_task(
    config: TaskConfig,
    options: dict[str, str] | None = None
) -> ValidationResult:
    """Process a task with optional configuration."""
    result: ValidationResult
    processed_data: list[str] = []

    for item_id: str in config.item_ids:
        item_result: str = _process_single_item(item_id)
        processed_data.append(item_result)

    result = ValidationResult(success=True, data=processed_data)
    return result

class TaskManager:
    """Manager for task operations with full type coverage."""

    def __init__(
        self,
        database_url: str,
        max_retries: int = 3
    ) -> None:
        self._database_url: str = database_url
        self._max_retries: int = max_retries
        self._active_tasks: dict[str, TaskConfig] = {}

    def add_task(self, task: TaskConfig) -> bool:
        """Add a task to the manager."""
        self._active_tasks[task.id] = task
        return True

    def get_task(self, task_id: str) -> TaskConfig | None:
        """Retrieve a task by ID."""
        return self._active_tasks.get(task_id)
```

## Logging Standards

### Required Library
- **Always use `loguru` for logging** across all packages

```python
from loguru import logger

# Configure logger (typically in CLI entrypoint)
logger.add("app.log", rotation="10 MB", level="INFO")

# Package-specific logging
logger.info("Library operation completed")
logger.debug("CLI command executed")
```

## CLI Structure Standards

### Required Files
- **CLI File**: Every package with CLI must have a `cli.py` or `main.py`
- **CLI Framework**: Every command-line tool must use `typer` with full type annotations

```python
from __future__ import annotations
import typer
from loguru import logger

app: typer.Typer = typer.Typer(help="ToDoWrite CLI Tools")

@app.command()
def create_task(
    title: str = typer.Argument(..., help="Task title"),
    description: str = typer.Option("", "--description", "-d", help="Task description")
) -> None:
    """Create a new task in the system."""
    logger.info(f"Creating task: {title}")
    # Implementation using lib_package
    from todowrite.core.models import Task
    new_task: Task = Task(title=title, description=description)
    print(f"✅ Task created: {new_task.title}")

if __name__ == "__main__":
    app()
```

## Development Priority & Execution

### Priority Order
1. **Working Code** - Functionality first
2. **Validation** - Real data testing
3. **Readability** - Code clarity
4. **Static Analysis** - Linting and formatting (after code works)

### Environment Variables
```bash
# Development with environment variables
env VAR_NAME="value" uv run command
```

## Compliance Checklist

Before completing any task, verify that your work adheres to ALL development standards:

1. ✅ All files have appropriate documentation headers with package context
2. ✅ Each module has a working validation function that tests real data and cross-package integration
3. ✅ **100% Type Coverage**: All code has comprehensive Python 3.12+ type hints
4. ✅ **Modern Syntax**: Uses `|` for unions, `list[str]` instead of `List[str]`, `T | None` instead of `Optional[T]`
5. ✅ **No Any Types**: Replaced `Any` with specific types or proper type annotations
6. ✅ All functionality is validated with real data before addressing linting issues
7. ✅ No asyncio.run() is used inside functions - only in main blocks
8. ✅ Code is under the 500-line limit for each file
9. ✅ Cross-package communication is properly typed and tested
10. ✅ Package dependencies are correctly declared in pyproject.toml files
11. ✅ Workspace imports are used correctly throughout the monorepo
12. ✅ **Forward References**: `from __future__ import annotations` is used for all modules
13. ✅ **Variable Typing**: Every variable assignment is explicitly typed
14. ✅ **Class Attributes**: All class attributes are properly typed
15. ✅ **Method Signatures**: All method parameters and returns are fully typed
