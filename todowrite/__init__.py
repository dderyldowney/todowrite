"""ToDoWrite: A standalone package for managing ToDos."""

from .app import ToDoWrite

# Project utilities - centralized methods that replace individual scripts
from .project_manager import (
    check_deprecated_schema,
    check_schema_changes,
    create_project_structure,
    init_database_sql,
    setup_integration,
    validate_project_setup,
)
from .schema import TODOWRITE_SCHEMA
from .types import Command, LayerType, Link, Metadata, Node, StatusType
from .version import __version__, get_version

__all__ = [
    "ToDoWrite",
    "TODOWRITE_SCHEMA",
    "Command",
    "LayerType",
    "Link",
    "Metadata",
    "Node",
    "StatusType",
    "get_version",
    "__version__",
    # Project utilities
    "check_deprecated_schema",
    "check_schema_changes",
    "setup_integration",
    "create_project_structure",
    "validate_project_setup",
    "init_database_sql",
]
