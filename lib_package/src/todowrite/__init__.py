"""ToDoWrite: Hierarchical Task Management System.

A sophisticated hierarchical task management system designed for complex
project planning and execution. Built with ToDoWrite Models patterns,
it provides both a standalone CLI and a Python module for programmatic use.
"""

from __future__ import annotations

# Core version information
from .version import get_version

__version__ = get_version()
__title__ = "ToDoWrite"
__description__ = (
    "Hierarchical task management system with ToDoWrite Models patterns"
)

# ToDoWrite Models - THE ONLY SUPPORTED API
# Database session management
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from .core.models import (
    AcceptanceCriteria,
    # SQLAlchemy base and utilities
    Base,
    Command,
    Concept,
    Constraints,
    Context,
    # ToDoWrite Models (12 layers)
    Goal,
    InterfaceContract,
    Label,  # Shared model for many-to-many relationships
    Phase,
    Requirements,
    Step,
    SubTask,
    Task,
)

# Schema validation and database management
from .core.schema_validator import (
    DatabaseInitializationError,
    DatabaseSchemaInitializer,
    SchemaValidationError,
    ToDoWriteSchemaValidator,
    get_schema_validator,
    initialize_database,
    validate_model_data,
)

__all__ = [
    # ToDoWrite Models (12 layers) - PRIMARY API
    "Goal",
    "Concept",
    "Context",
    "Constraints",
    "Requirements",
    "AcceptanceCriteria",
    "InterfaceContract",
    "Phase",
    "Step",
    "Task",
    "SubTask",
    "Command",
    "Label",
    # Database utilities
    "Base",
    "create_engine",
    "sessionmaker",
    # Schema validation and management
    "ToDoWriteSchemaValidator",
    "DatabaseSchemaInitializer",
    "get_schema_validator",
    "validate_model_data",
    "initialize_database",
    "SchemaValidationError",
    "DatabaseInitializationError",
    # Metadata
    "__description__",
    "__title__",
    "__version__",
]


def init_project(_project_path: str = ".", _db_type: str = "postgres") -> bool:
    """Quick project initialization helper.

    Args:
        _project_path: Path to the project directory
        (default: current directory)
        _db_type: Database type to configure (``'postgres'`` or ``'sqlite'``)

    Returns:
        True if initialization was successful (placeholder implementation).

    """
    # Placeholder implementation. Project initialization helpers live in
    # ToDoWrite Models and will be wired into this convenience helper when
    # those APIs are stabilized.
    return True
