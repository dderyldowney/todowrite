# Python 3.12 Mastery Guide - Project-Specific Implementation

## Core Python 3.12 Features

### PEP 695: Type Parameter Syntax (NEW)
```python
# Generic functions
def max[T](args: Iterable[T]) -> T: ...

# Generic classes
class Container[T]:
    def __init__(self, items: list[T]) -> None: ...

# Type aliases
type Point = tuple[float, float]
type NodeId = str
```

### PEP 701: Enhanced F-Strings
```python
# Multi-line expressions
f"""This is a multi-line
expression: {some_long_variable_name}"""

# Quote reuse
f"This is the playlist: {", ".join(songs)}"

# Backslashes and Unicode escapes
f"Path: {path.replace('\\', '/')} "
```

### PEP 698: Override Decorator
```python
from typing import override

class GoodChild(Base):
    @override  # Type checker verifies this overrides Base.get_color
    def get_color(self) -> str:
        return "yellow"
```

## Advanced Static Typing System

### Union Types with `|` Syntax
```python
# Preferred over Union[str, int]
def process_data(data: str | int) -> str:
    return str(data)

# Optional types
def get_config(key: str) -> str | None:
    return config.get(key)
```

### TypedDict for **kwargs (PEP 692)
```python
class Movie(TypedDict):
    name: str
    year: int

def create_movie(**kwargs: Unpack[Movie]) -> Movie:
    return Movie(**kwargs)
```

### Protocols for Structural Subtyping
```python
class SupportsExport(Protocol):
    def export(self, format: str) -> str: ...
    def validate(self) -> bool: ...

class Closable(Protocol):
    def close(self) -> None: ...

def safe_close(obj: Closable) -> None:
    obj.close()
```

### NewType for Type Safety
```python
UserId = NewType('UserId', int)
NodeIdentifier = NewType('NodeIdentifier', str)

def get_user(user_id: UserId) -> str:
    # Type safety prevents accidental mixing
    pass
```

## Package Structure - PROJECT COMPLIANCE

### src-layout Package Structure
```
todowrite/                      # Project root
├── lib_package/               # Core library package
│   ├── pyproject.toml         # Hatchling configuration
│   ├── src/
│   │   └── todowrite/        # Main package
│   │       ├── __init__.py
│   │       ├── core/
│   │       ├── database/
│   │       └── storage/
│   └── tests/
├── cli_package/               # CLI package
│   ├── pyproject.toml
│   ├── src/
│   │   └── todowrite_cli/
│   └── tests/
├── web_package/               # Web package
│   ├── pyproject.toml
│   ├── src/
│   │   └── todowrite_web/
│   └── tests/
├── docs/                      # Project documentation
├── scripts/                   # Build scripts
├── VERSION                    # Centralized version
└── pyproject.toml            # Root configuration
```

### pyproject.toml Configuration (Hatchling ONLY)
```toml
[build-system]
requires = ["hatchling"]  # NEVER setuptools
build-backend = "hatchling.build"

[project]
name = "todowrite"
version = "0.4.1"  # From VERSION file
description = "Hierarchical task management system"
requires-python = ">=3.12"

[project.optional-dependencies]
dev = [
    "uv>=0.1.0",           # Fast dependency management
    "pytest>=7.0.0",       # Testing framework
    "pytest-cov>=4.0.0",   # Coverage
    "ruff>=0.6.0",          # Formatting & linting (NO black, mypy)
    "pyright>=1.1.0",       # Type checking (NEVER mypy)
    "bandit>=1.7.0",        # Security scanning
    "twine>=4.0.0",         # Publishing
]

[tool.ruff]
line-length = 100
target-version = "py312"

[tool.pyright]
typeCheckingMode = "strict"
pythonVersion = "3.12"
```

## Essential Standard Library Modules

### File System Operations
```python
from pathlib import Path
import tempfile
import shutil

# Path operations (preferred over os.path)
project_root = Path(__file__).parent.parent
config_file = project_root / "config" / "settings.yaml"

# Safe temporary files
with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml') as tmp:
    tmp.write(yaml_content)
    # Process file...

# High-level file operations
shutil.copy2(src, dst)  # Copy with metadata
shutil.rmtree(dir_path)  # Remove directory tree
```

### Database Operations
```python
import sqlite3
from contextlib import contextmanager

@contextmanager
def get_db_connection(db_path: str):
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()
```

### JSON and YAML Processing
```python
import json
from typing import Any, TypedDict
from datetime import datetime

class NodeData(TypedDict):
    id: str
    type: str
    title: str
    created_at: str

def serialize_node(node: NodeData) -> str:
    return json.dumps(node, indent=2, default=str)

# Custom JSON encoder for datetime
class DateTimeEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        return super().default(obj)
```

## TDD Red-Green-Refactor Methodology (MANDATORY)

### RED Phase: Write Failing Test
```python
# tests/test_node_creation.py
def test_create_goal_node():
    """RED: Test doesn't exist yet, will fail"""
    with get_db_connection(":memory:") as conn:
        app = ToDoWrite(conn)
        node = app.create_node("goal", "Test Goal", "Description")
        assert node["type"] == "goal"
        assert node["id"].startswith("GOAL-")
```

### GREEN Phase: Minimal Implementation
```python
# core/app.py
def create_node(self, node_type: str, title: str, description: str) -> dict[str, str]:
    """GREEN: Minimal implementation to pass test"""
    node_id = f"{node_type.upper()}-{uuid.uuid4().hex[:8]}"
    return {
        "id": node_id,
        "type": node_type,
        "title": title,
        "description": description
    }
```

### REFACTOR Phase: Improve Implementation
```python
# core/app.py (refactored)
@validate_node_type
def create_node(self, node_type: str, title: str, description: str) -> NodeData:
    """REFACTOR: Enhanced with validation and proper typing"""
    if len(title) > self.MAX_TITLE_LENGTH:
        raise ValueError(f"Title too long: {len(title)}")

    node = Node(
        type=node_type,
        title=title.strip(),
        description=description.strip()
    )

    return self._save_node(node)
```

## Local CLI Tools (MANDATORY)

### grep for Code Analysis
```bash
# Find all database operations
grep -r "sqlite3\|execute\|commit" src/

# Find type annotations
grep -r ": str\|: int\|: bool" src/ | head -10

# Find TODO comments
grep -rn "TODO\|FIXME\|XXX" src/
```

### sed for Bulk Transformations
```bash
# Replace old-style Union with new syntax
sed -i 's/Union\[str, int\]/str | int/g' src/**/*.py

# Add type hints to function definitions
sed -i 's/def \(.*\)(\(.*\)):/def \1(\2) -> None:/' src/**/*.py
```

### awk for Data Processing
```bash
# Extract function signatures
awk '/def / {print FILENAME ":" NR ":" $0}' src/**/*.py

# Count type annotations by file
awk '
/^[a-zA-Z_]+: / { type_count++ }
END { print FILENAME ": " type_count " type annotations" }
' src/**/*.py
```

### patch for Code Changes
```bash
# Create diff for review
git diff > feature_changes.patch

# Apply patch from another branch
git apply feature_changes.patch

# Create patch for specific function changes
git diff lib_package/src/todowrite/core/app.py > core_app_changes.patch
```

## Token Optimization System (MANDATORY)

### Use Episodic Memory for Context
```python
# Before starting work, search past conversations
from episodic_memory import search_conversations

def get_previous_decisions(topic: str) -> list[str]:
    results = search_conversations(topic, limit=5)
    return [r["summary"] for r in results]
```

### Efficient Code Patterns
```python
# Use generators for large datasets (memory efficient)
def stream_nodes(query: str) -> Generator[Node, None, None]:
    cursor.execute(query)
    while row := cursor.fetchone():
        yield Node.from_row(row)

# Use @cached_property for expensive computations
from functools import cached_property

class NodeProcessor:
    @cached_property
    def compiled_schema(self) -> dict:
        return json.loads(self.schema_string)
```

### Batch Operations
```python
# Batch database writes
def create_nodes_batch(nodes: list[NodeData]) -> list[str]:
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.executemany(
            "INSERT INTO nodes (id, type, title, description) VALUES (?, ?, ?, ?)",
            [(n["id"], n["type"], n["title"], n["description"]) for n in nodes]
        )
        conn.commit()
    return [n["id"] for n in nodes]
```

## Project Tooling Compliance

### Required Tools (NEVER alternatives)
- **uv**: Fast package management (NO pip for complex ops)
- **ruff**: Formatting and linting (NO black, flake8)
- **pyright**: Type checking (NEVER mypy)
- **pytest**: Testing framework
- **bandit**: Security scanning
- **hatchling**: Build system (NEVER setuptools)
- **twine**: Package publishing

### Frontend Architecture
- **Claude Code CLI**: Agentic frontend (NO web UI planned)
- **CLI-first**: All user interactions via command line
- **Terminal optimization**: Efficient text-based interfaces

### Distribution Status
- **todowrite**: Published on PyPI.org ✅
- **todowrite_cli**: Published on PyPI.org ✅
- **todowrite_web**: In development (CLI-first approach)

## Memory and Performance Optimization

### Dataclass with slots
```python
@dataclass(frozen=True, slots=True)
class Node:
    """Memory-efficient node representation"""
    id: str
    type: str
    title: str
    description: str
    metadata: dict[str, str | int] = field(default_factory=dict)
```

### Connection Pooling
```python
from sqlalchemy.pool import QueuePool

engine = create_engine(
    database_url,
    poolclass=QueuePool,
    pool_size=10,
    max_overflow=20
)
```

### Efficient String Operations
```python
# Use f-strings (fastest)
message = f"Node {node_id} created successfully"

# Avoid string concatenation in loops
parts = []
for item in large_list:
    parts.append(process_item(item))
result = "".join(parts)  # Single join at end
```

## Security Best Practices

### SQL Injection Prevention
```python
# ALWAYS use parameterized queries
cursor.execute(
    "SELECT * FROM nodes WHERE type = ? AND title LIKE ?",
    (node_type, f"%{search_term}%")
)

# NEVER string formatting for SQL
# DANGEROUS: cursor.execute(f"SELECT * FROM nodes WHERE type = {node_type}")
```

### File Operation Security
```python
import tempfile
import os

def safe_file_operation(file_path: Path, content: str) -> None:
    # Validate file path is within allowed directory
    resolved_path = file_path.resolve()
    if not str(resolved_path).startswith(str(ALLOWED_BASE_DIR)):
        raise SecurityError("Path traversal attempt detected")

    # Use temporary file for atomic writes
    with tempfile.NamedTemporaryFile(
        mode='w',
        dir=resolved_path.parent,
        delete=False
    ) as tmp:
        tmp.write(content)
        os.replace(tmp.name, resolved_path)
```

### Subprocess Security (NEVER shell=True)
```python
import subprocess

def safe_command(cmd: list[str], cwd: Path | None = None) -> subprocess.CompletedProcess:
    """Secure command execution without shell"""
    return subprocess.run(
        cmd,
        cwd=cwd,
        capture_output=True,
        text=True,
        check=False,
        shell=False  # CRITICAL: Never use shell=True
    )
```

This mastery guide is stored in episodic memory and provides complete project-specific Python 3.12 knowledge for efficient development without token waste.
