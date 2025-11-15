"""
Storage module for ToDoWrite

This module contains storage-related functionality including:
- Abstract storage backend interface
- Database storage backends (PostgreSQL, SQLite)
- YAML storage backend
- Schema validation
- Import/export management
"""

from .backends import (
    NodeCreationError,
    NodeCreationResult,
    NodeDeletionError,
    NodeNotFoundError,
    NodeUpdateError,
    RelationshipCreationResult,
    RelationshipError,
    StorageBackend,
    StorageConnectionError,
    StorageError,
    StorageQueryError,
)
from .factory import (
    create_storage_backend,
    create_storage_backend_for_environment,
    detect_storage_backend_type,
    get_default_database_url,
    validate_database_url,
)
from .postgresql_backend import PostgreSQLBackend
from .schema_validator import (
    get_schema_compliance_report,
    validate_database_schema,
    validate_node_data,
    validate_yaml_files,
)
from .sqlite_backend import SQLiteBackend
from .yaml_manager import YAMLManager

__all__ = [
    "NodeCreationError",
    "NodeCreationResult",
    "NodeDeletionError",
    "NodeNotFoundError",
    "NodeUpdateError",
    "PostgreSQLBackend",
    "RelationshipCreationResult",
    "RelationshipError",
    "SQLiteBackend",
    "StorageBackend",
    "StorageConnectionError",
    "StorageError",
    "StorageQueryError",
    "YAMLManager",
    "create_storage_backend",
    "create_storage_backend_for_environment",
    "detect_storage_backend_type",
    "get_default_database_url",
    "get_schema_compliance_report",
    "validate_database_schema",
    "validate_database_url",
    "validate_node_data",
    "validate_yaml_files",
]
