"""
Storage utilities for ToDoWrite Models.

This module provides compatibility utilities for the ToDoWrite Models implementation.
"""


# Legacy storage exceptions for backward compatibility
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

# Re-export factory functions if they exist
try:
    from .factory import (
        create_storage_backend,
        create_storage_backend_for_environment,
        detect_storage_backend_type,
        get_default_database_url,
        validate_database_url,
    )

    factory_available = True
except ImportError:
    factory_available = False
    create_storage_backend = None
    create_storage_backend_for_environment = None
    detect_storage_backend_type = None
    get_default_database_url = None
    validate_database_url = None

__all__ = [
    # ToDoWrite Models schema validation
    "ToDoWriteSchemaValidator",
    "DatabaseSchemaInitializer",
    "get_schema_validator",
    "validate_model_data",
    "initialize_database",
    "SchemaValidationError",
    # Legacy storage exceptions
    "StorageError",
    "StorageConnectionError",
    "StorageQueryError",
    # Conditional exports
    "YAMLManager",
    "create_storage_backend",
    "create_storage_backend_for_environment",
    "detect_storage_backend_type",
    "get_default_database_url",
    "validate_database_url",
]
