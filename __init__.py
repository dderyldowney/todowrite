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

# CLI interface
from .cli import cli

# Database components
from .db import Database, DatabaseConfig, get_default_config

# Project utilities - centralized methods that replace individual scripts
from .project_manager import (
    check_deprecated_schema,
    check_schema_changes,
    create_project_structure,
    init_database_sql,
    setup_integration,
    validate_project_setup,
)
from .schema import TODOWRITE_SCHEMA, validate_node, validate_schema

# Core types and schemas
from .types import Command, LayerType, Link, Metadata, Node, StatusType

# YAML management
from .yaml_manager import YAMLManager

# Public utility functions
__all__ = [
    # Version
    "__version__",
    "__title__",
    "__description__",
    # Core application functions
    "create_node",
    "get_node",
    "update_node",
    "delete_node",
    "list_nodes",
    "search_nodes",
    "export_nodes",
    "import_nodes",
    "update_node_status",
    # Database
    "Database",
    "DatabaseConfig",
    "get_default_config",
    # Types
    "Node",
    "LayerType",
    "StatusType",
    "Metadata",
    "Link",
    "Command",
    # Schema
    "TODOWRITE_SCHEMA",
    "validate_node",
    "validate_schema",
    # Utilities
    "check_deprecated_schema",
    "check_schema_changes",
    "setup_integration",
    "create_project_structure",
    "validate_project_setup",
    "init_database_sql",
    # Management
    "YAMLManager",
    "cli",
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
    # Create project structure
    if not create_project_structure(project_path):
        return False

    # Set up integration
    if not setup_integration(project_path, db_type):
        return False

    return True


# Add to __all__ for public API
__all__.append("init_project")
