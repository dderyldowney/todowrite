"""
ToDoWrite: Hierarchical Task Management System

A sophisticated hierarchical task management system designed for complex project planning and execution.
Built with a 12-layer declarative framework, it provides both standalone CLI capabilities and Python module integration.
"""

# Core version information
from .version import get_version

__version__ = get_version()
__title__ = "ToDoWrite"
__description__ = (
    "Hierarchical task management system with 12-layer declarative planning framework"
)

# CLI interface
# Main application components
from .app import (
    create_node,
    delete_node,
    export_nodes,
    get_node,
    import_nodes,
    list_nodes,
    search_nodes,
    update_node,
    update_node_status,
)
from .cli import cli

# Shared constants
from .constants import (
    DEFAULT_BASE_PATH,
    DEFAULT_COMMANDS_PATH,
    DEFAULT_PLANS_PATH,
    LAYER_DIRS,
)

# Database components
from .db import (
    StoragePreference,
    StorageType,
    determine_storage_backend,
    get_storage_info,
    set_storage_preference,
)

# Custom exceptions
from .exceptions import (
    CLIError,
    ConfigurationError,
    DatabaseError,
    InvalidNodeError,
    NodeError,
    NodeNotFoundError,
    SchemaError,
    StorageError,
    ToDoWriteError,
    TokenOptimizationError,
    YAMLError,
)

# Project utilities - centralized methods that replace individual scripts
# AI optimization utilities - available when AI dependencies are installed
from .project_manager import (
    check_deprecated_schema,
    check_schema_changes,
    create_project_structure,
    ensure_token_sage,
    init_database_sql,
    optimize_token_usage,
    setup_integration,
    validate_project_setup,
)

# Schema management
from .schema import TODOWRITE_SCHEMA
from .schema_validator import validate_database_schema as validate_schema
from .schema_validator import validate_node_data as validate_node

# Core types and schemas
from .types import Command, LayerType, Link, Metadata, Node, StatusType

# YAML management
from .yaml_manager import YAMLManager

# Public utility functions
__all__ = [
    "DEFAULT_BASE_PATH",
    "DEFAULT_COMMANDS_PATH",
    "DEFAULT_PLANS_PATH",
    "LAYER_DIRS",
    "TODOWRITE_SCHEMA",
    "CLIError",
    "Command",
    "ConfigurationError",
    "DatabaseError",
    "InvalidNodeError",
    "LayerType",
    "Link",
    "Metadata",
    "Node",
    "NodeError",
    "NodeNotFoundError",
    "SchemaError",
    "StatusType",
    "StorageError",
    "StoragePreference",
    "StorageType",
    "ToDoWriteError",
    "TokenOptimizationError",
    "YAMLError",
    "YAMLManager",
    "__description__",
    "__title__",
    "__version__",
    "check_deprecated_schema",
    "check_schema_changes",
    "cli",
    "create_node",
    "create_project_structure",
    "delete_node",
    "determine_storage_backend",
    "ensure_token_sage",
    "export_nodes",
    "get_node",
    "get_storage_info",
    "import_nodes",
    "init_database_sql",
    "list_nodes",
    "optimize_token_usage",
    "search_nodes",
    "set_storage_preference",
    "setup_integration",
    "update_node",
    "update_node_status",
    "validate_node",
    "validate_project_setup",
    "validate_schema",
]


# Convenience function for quick initialization
def init_project(project_path: str = ".", db_type: str = "postgres") -> bool:
    """
    Quick project initialization.

    Args:
        project_path: Path to the project directory (default: current directory)
        db_type: Database type ('postgres' or 'sqlite')

    Returns:
        True if initialization was successful
    """
    return create_project_structure(project_path) and setup_integration(
        project_path, db_type
    )


# Add to __all__ for public API
__all__.append("init_project")
