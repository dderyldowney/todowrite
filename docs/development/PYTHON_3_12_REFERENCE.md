# Python 3.12 Development Reference

## Core Features for ToDoWrite Development

### Python 3.12 New Features

#### 1. Type System Improvements

**Union Types with `|` Syntax** (PEP 604)
```python
# Old way
from typing import Union
def process_data(data: Union[str, int]) -> str:
    return str(data)

# New way (Python 3.10+)
def process_data(data: str | int) -> str:
    return str(data)

# Optional types
def get_config(key: str) -> str | None:
    return config.get(key)
```

**Generic Classes with `type`** (PEP 695)
```python
# Generic class definition
class Container[T]:
    def __init__(self, items: list[T]) -> None:
        self.items = items

    def add(self, item: T) -> None:
        self.items.append(item)

# Generic functions
def first_item[T](items: list[T]) -> T | None:
    return items[0] if items else None
```

#### 2. Performance Improvements

**Faster `dict` and `list` operations**
- Dictionary lookups are ~15% faster
- List comprehensions are optimized
- String concatenation improved

#### 3. New Standard Library Features

**`pathlib.Path.walk()`** for recursive directory traversal
```python
from pathlib import Path

def find_python_files(root: Path) -> list[Path]:
    python_files = []
    for file_path in root.walk():
        if file_path.suffix == ".py":
            python_files.append(file_path)
    return python_files
```

**`frozenset` improvements**
```python
# frozenset is now more memory efficient
PERMISSIONS: frozenset[str] = frozenset([
    "read", "write", "execute"
])
```

## Static Typing Best Practices

### 1. Type Annotations

**Basic Types**
```python
from typing import Optional, Literal, Final
from collections.abc import Callable, Iterable

# Function signatures
def process_nodes(
    nodes: list[dict[str, str | int]],
    filters: Optional[dict[str, str]] = None,
    limit: int = 50,
    *,
    verbose: bool = False
) -> list[dict[str, str | int]]:
    """Process nodes with optional filtering."""
    pass

# Constants
MAX_RESULTS: Final[int] = 1000
DEFAULT_TIMEOUT: Final[float] = 30.0

# Literal types for enums
NodeType: TypeAlias = Literal[
    "goal", "concept", "context", "constraint",
    "requirement", "acceptance_criteria", "interface_contract",
    "phase", "step", "task", "subtask", "command"
]
```

**Advanced Type Patterns**
```python
from typing import TypeVar, Generic, Protocol, TypeGuard
from collections.abc import Sequence, Mapping

# Type variables with bounds
T = TypeVar('T', bound='Node')
NodeType_contra = TypeVar('NodeType_contra', contravariant=True)

# Protocol for duck typing
class SupportsExport(Protocol):
    def export(self, format: str) -> str: ...
    def validate(self) -> bool: ...

# Generic base class
class DatabaseModel(Generic[T]):
    id: str
    created_at: datetime

    def to_dict(self) -> dict[str, str | int]: ...

    def from_dict(cls, data: dict[str, str | int]) -> T: ...

# Type guards
def is_valid_node(obj: object) -> TypeGuard['Node']:
    return isinstance(obj, dict) and 'id' in obj and 'type' in obj
```

### 2. Data Structures

**`dataclasses` for models**
```python
from dataclasses import dataclass, field
from datetime import datetime
from typing import ClassVar

@dataclass(frozen=True, slots=True)
[REMOVED_LEGACY_PATTERN]:
    type: str
    title: str
    description: str
    id: str = field(default_factory=lambda: f"NODE-{uuid.uuid4().hex[:8].upper()}")
    created_at: datetime = field(default_factory=datetime.utcnow)
    metadata: dict[str, str | int] = field(default_factory=dict)

    # Class constants
    MAX_TITLE_LENGTH: ClassVar[int] = 200

    def __post_init__(self) -> None:
        if len(self.title) > self.MAX_TITLE_LENGTH:
            raise ValueError(f"Title too long: {len(self.title)} > {self.MAX_TITLE_LENGTH}")
```

**TypedDict for API responses**
```python
from typing import TypedDict, NotRequired, Required

[REMOVED_LEGACY_PATTERN]Response(TypedDict):
    id: Required[str]
    type: Required[str]
    title: Required[str]
    description: Required[str]
    created_at: Required[str]  # ISO format
    metadata: NotRequired[dict[str, str | int]]

class CreateNodeRequest(TypedDict):
    type: Required[str]
    title: Required[str]
    description: Required[str]
    metadata: NotRequired[dict[str, str | int]]
```

## Standard Library Essentials

### 1. `sqlite3` for Database Operations

```python
import sqlite3
from contextlib import contextmanager
from typing import Generator

# Type-safe database operations
@contextmanager
def get_db_connection(db_path: str) -> Generator[sqlite3.Connection, None, None]:
    """Context manager for database connections."""
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row  # Dict-like rows
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()

# Type-safe queries
def [REMOVED_LEGACY_PATTERN]_table(conn: sqlite3.Connection) -> None:
    conn.execute('''
        CREATE TABLE IF NOT EXISTS nodes (
            id TEXT PRIMARY KEY,
            type TEXT NOT NULL,
            title TEXT NOT NULL,
            description TEXT,
            metadata TEXT,  -- JSON string
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

def insert_node(conn: sqlite3.Connection, node: Node) -> str:
    """Insert a node and return its ID."""
    cursor = conn.execute(
        'INSERT INTO nodes (id, type, title, description, metadata) VALUES (?, ?, ?, ?, ?)',
        (node.id, node.type, node.title, node.description, json.dumps(node.metadata))
    )
    return node.id
```

### 2. `json` with Type Safety

```python
import json
from typing import Any, TypeVar
from json.decoder import JSONDecodeError

T = TypeVar('T')

def safe_json_loads(data: str, expected_type: type[T]) -> T:
    """Safely load JSON with type validation."""
    try:
        result = json.loads(data)
        if not isinstance(result, expected_type):
            raise TypeError(f"Expected {expected_type}, got {type(result)}")
        return result
    except JSONDecodeError as e:
        raise ValueError(f"Invalid JSON: {e}")

# Custom JSON encoder for datetime objects
from json import JSONEncoder
from datetime import datetime

class DateTimeEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        return super().default(obj)
```

### 3. `pathlib` for File Operations

```python
from pathlib import Path
import shutil

# Type-safe file operations
def ensure_directory(path: Path) -> Path:
    """Ensure directory exists, return Path object."""
    path.mkdir(parents=True, exist_ok=True)
    return path

def safe_file_copy(src: Path, dst: Path) -> None:
    """Safely copy file with proper error handling."""
    if not src.exists():
        raise FileNotFoundError(f"Source file not found: {src}")

    ensure_directory(dst.parent)
    shutil.copy2(src, dst)

# Project structure utilities
def get_project_root() -> Path:
    """Get project root directory."""
    return Path(__file__).parent.parent.parent

def get_package_dir(package_name: str) -> Path:
    """Get package directory within project."""
    return get_project_root() / f"{package_name}_package"
```

### 4. `subprocess` Security

```python
import subprocess
from typing import Sequence, Optional

def run_command(
    cmd: Sequence[str],
    cwd: Optional[Path] = None,
    timeout: Optional[int] = None,
    capture_output: bool = True
) -> subprocess.CompletedProcess[str]:
    """Safely run external command with proper validation."""

    # Validate command to prevent injection
    if any(' ' in arg for arg in cmd):
        raise ValueError("Command arguments must not contain spaces")

    # Security: Never use shell=True with user input
    try:
        result = subprocess.run(
            cmd,
            cwd=cwd,
            timeout=timeout,
            capture_output=capture_output,
            text=True,
            check=False,  # Don't raise on non-zero exit codes
        )
        return result
    except subprocess.TimeoutExpired as e:
        raise TimeoutError(f"Command timed out: {cmd}")
    except FileNotFoundError:
        raise FileNotFoundError(f"Command not found: {cmd[0]}")
```

## Modern Python Patterns

### 1. Context Managers

```python
from contextlib import contextmanager
from typing import Generator

@contextmanager
def database_transaction(db_path: Path) -> Generator[sqlite3.Connection, None, None]:
    """Context manager for database transactions."""
    conn = sqlite3.connect(db_path)
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()

# Usage
with database_transaction(Path("data.db")) as conn:
    insert_node(conn, my_node)
    # All operations are committed or rolled back together
```

### 2. Async/Await Patterns

```python
import asyncio
from typing import Awaitable

async def async_database_operation(
    operation: Callable[[], Awaitable[T]]
) -> T:
    """Run database operation asynchronously."""
    return await operation()

async def process_nodes_async(nodes: list[Node]) -> list[str]:
    """Process nodes asynchronously."""
    tasks = [process_single_node(node) for node in nodes]
    return await asyncio.gather(*tasks)
```

### 3. Error Handling

```python
from typing import Union

class ToDoWriteError(Exception):
    """Base exception for ToDoWrite."""
    pass

[REMOVED_LEGACY_PATTERN]NotFoundError(ToDoWriteError):
    """Raised when a node is not found."""
    def __init__(self, node_id: str):
        self.node_id = node_id
        super().__init__(f"Node not found: {node_id}")

class ValidationError(ToDoWriteError):
    """Raised when validation fails."""
    def __init__(self, message: str, field: str):
        self.field = field
        super().__init__(f"Validation error in {field}: {message}")

# Result type for operations
Result[T] = Union[T, ToDoWriteError]

def safe_operation[T](operation: Callable[[], T]) -> Result[T]:
    """Wrap operation in try-catch for safe execution."""
    try:
        return operation()
    except ToDoWriteError:
        raise  # Re-raise our custom exceptions
    except Exception as e:
        raise ToDoWriteError(f"Unexpected error: {e}")
```

## Package Structure Standards

### 1. src-layout Package Structure

```
todowrite/
├── pyproject.toml
├── src/
│   └── todowrite/
│       ├── __init__.py
│       ├── core/
│       │   ├── __init__.py
│       │   ├── app.py
│       │   └── models.py
│       ├── database/
│       │   ├── __init__.py
│       │   ├── config.py
│       │   └── models.py
│       ├── storage/
│       │   ├── __init__.py
│       │   └── yaml_manager.py
│       └── version.py
├── tests/
│   ├── __init__.py
│   ├── conftest.py
│   ├── test_core/
│   └── test_database/
└── docs/
    ├── development/
    └── api/
```

### 2. pyproject.toml Configuration

```toml
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[project]
name = "todowrite"
version = "0.4.0"  # Managed by VERSION file
description = "Hierarchical task management system"
requires-python = ">=3.12"
dependencies = [
    "sqlalchemy>=2.0.23",
    "jsonschema>=4.17.3",
    "pyyaml>=6.0.1",
]

[project.optional-dependencies]
dev = [
    "pytest>=7.0.0",
    "pytest-cov>=4.0.0",
    "pytest-asyncio>=0.21.0",
    "black>=24.0.0",
    "ruff>=0.6.0",
    "pyright>=1.1.0",
    "bandit>=1.7.0",
]

[tool.ruff]
line-length = 100
target-version = "py312"

[tool.pyright]
typeCheckingMode = "strict"
pythonVersion = "3.12"
```

## Performance Considerations

### 1. Memory Efficiency

```python
# Use __slots__ for dataclasses with many instances
@dataclass(frozen=True, slots=True)
class CompactNode:
    id: str
    type: str
    title: str
    # No __dict__ created, saves memory

# Use generators for large datasets
def stream_nodes(db_path: Path) -> Generator[Node, None, None]:
    """Stream nodes from database without loading all into memory."""
    with get_db_connection(db_path) as conn:
        cursor = conn.execute("SELECT * FROM nodes")
        for row in cursor:
            yield Node.from_row(row)
```

### 2. Type Checking Performance

```python
# Use type aliases for complex types
NodeTypeMap = dict[str, Node]
NodeFilter = Callable[[Node], bool]

# Use Protocol for duck typing instead of complex inheritance
class Serializable(Protocol):
    def to_dict(self) -> dict[str, Any]: ...

    def from_dict(self, data: dict[str, Any]) -> "Serializable": ...
```

This reference serves as a comprehensive guide for Python 3.12 development in the ToDoWrite project, ensuring consistent, type-safe, and performant code across all packages.
