"""
Storage utilities for ToDoWrite Models.

This module provides compatibility utilities for the ToDoWrite Models implementation.
"""


# Storage exception classes
class StorageError(Exception):
    """Base storage exception."""

    pass


class StorageConnectionError(StorageError):
    """Database connection error."""

    pass


class StorageQueryError(StorageError):
    """Database query error."""

    pass


# Re-export core schema validation functions
from ..core.schema_validator import (
    DatabaseSchemaInitializer,
    SchemaValidationError,
    ToDoWriteSchemaValidator,
    get_schema_validator,
    initialize_database,
    validate_model_data,
)

# Re-export YAML management if it exists
try:
    from .yaml_manager import YAMLManager

    yaml_manager_available = True
except ImportError:
    YAMLManager = None
    yaml_manager_available = False


# Schema validation utility functions for testing
def get_schema_compliance_report():
    """Get schema compliance report - placeholder for testing"""
    return {"compliance": "OK", "errors": []}


def validate_database_schema():
    """Validate database schema - placeholder for testing"""
    return True, "Schema valid"


def validate_node_data():
    """Validate node data - placeholder for testing"""
    return True, "Node data valid"


def validate_yaml_files():
    """Validate YAML files - placeholder for testing"""
    return True, "YAML files valid"


__all__ = [
    "DatabaseSchemaInitializer",
    "SchemaValidationError",
    "StorageConnectionError",
    "StorageError",
    "StorageQueryError",
    # ToDoWrite Models schema validation
    "ToDoWriteSchemaValidator",
    # Conditional exports
    "YAMLManager",
    "get_schema_validator",
    "initialize_database",
    "validate_model_data",
    # Schema validation utilities
    "get_schema_compliance_report",
    "validate_database_schema",
    "validate_node_data",
    "validate_yaml_files",
]
