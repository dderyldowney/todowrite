from __future__ import annotations

import logging
from pathlib import Path

from .backends import StorageBackend, StorageConnectionError
from .postgresql_backend import PostgreSQLBackend
from .sqlite_backend import SQLiteBackend

logger = logging.getLogger(__name__)


def create_storage_backend(database_url: str) -> StorageBackend:
    """
    Create the appropriate storage backend based on the database URL.

    This factory function analyzes the database URL and creates the corresponding
    storage backend instance with proper configuration.

    Args:
        database_url: The database connection URL (e.g., 'postgresql://user:pass@host/db',
                     'sqlite:///path/to/file.db', or 'path/to/file.yaml')

    Returns:
        Configured StorageBackend instance ready for use

    Raises:
        StorageConnectionError: If the URL format is not supported
    """
    try:
        backend = _create_backend_by_url_type(database_url)
        logger.info(f"Created {backend.backend_name} storage backend")
        return backend

    except Exception as e:
        raise StorageConnectionError(
            "StorageBackendFactory",
            f"Failed to create backend for URL '{database_url}': {e!s}",
        )


def _create_backend_by_url_type(database_url: str) -> StorageBackend:
    """Create backend based on URL type detection."""
    database_url = database_url.strip()
    backend_type = detect_storage_backend_type(database_url)

    if backend_type == "postgresql":
        return _create_postgresql_backend(database_url)

    elif backend_type == "sqlite":
        if database_url.startswith("sqlite://"):
            return _create_sqlite_backend_from_url(database_url)
        else:
            return _create_sqlite_backend_from_path(database_url)

    elif backend_type == "yaml":
        return _create_yaml_backend(database_url)

    else:
        raise ValueError(f"Unsupported database URL format: {database_url}")


def _create_postgresql_backend(database_url: str) -> PostgreSQLBackend:
    """Create PostgreSQL backend with optimized connection pooling."""
    try:
        # Extract connection details for logging (mask password)
        safe_url = (
            database_url.replace("://", "://***@")
            if "@" in database_url
            else database_url
        )

        # Create backend with production-ready pool settings
        backend = PostgreSQLBackend(
            database_url=database_url,
            pool_size=10,  # Base connections in pool
            max_overflow=20,  # Additional connections under load
        )

        logger.info(f"Configured PostgreSQL backend: {safe_url}")
        return backend

    except Exception as e:
        raise StorageConnectionError(
            "PostgreSQL", f"Failed to configure PostgreSQL backend: {e!s}"
        )


def _create_sqlite_backend_from_url(database_url: str) -> SQLiteBackend:
    """Create SQLite backend from sqlite:// URL."""
    try:
        # Extract path from sqlite:///path/to/db or sqlite://path/to/db
        if database_url.startswith("sqlite:///"):
            database_path = database_url[10:]  # Remove 'sqlite:///'
        elif database_url.startswith("sqlite://"):
            database_path = database_url[9:]  # Remove 'sqlite://'
        else:
            raise ValueError(f"Invalid SQLite URL format: {database_url}")

        return SQLiteBackend(database_path)

    except Exception as e:
        raise StorageConnectionError(
            "SQLite", f"Failed to create SQLite backend from URL: {e!s}"
        )


def _create_sqlite_backend_from_path(database_path: str) -> SQLiteBackend:
    """Create SQLite backend from direct file path."""
    try:
        path = Path(database_path)

        # Ensure the path has .db extension
        if path.suffix not in [".db", ".sqlite", ".sqlite3"]:
            path = path.with_suffix(".db")

        logger.info(f"Configured SQLite backend with path: {path}")
        return SQLiteBackend(path)

    except Exception as e:
        raise StorageConnectionError(
            "SQLite", f"Failed to create SQLite backend from path: {e!s}"
        )


def _create_yaml_backend(yaml_path: str) -> StorageBackend:
    """Create YAML backend for file-based storage."""
    # This will be implemented when we create the YAML backend
    # For now, we'll raise an error to indicate it's not ready yet
    raise NotImplementedError(
        "YAML backend not yet implemented. Use PostgreSQL or SQLite backends."
    )


def detect_storage_backend_type(database_url: str) -> str:
    """
    Detect the type of storage backend that would be used for a given URL.

    This is useful for validation and configuration purposes without actually
    creating the backend instance.

    Args:
        database_url: The database connection URL to analyze

    Returns:
        String indicating the backend type: 'postgresql', 'sqlite', 'yaml', or 'unknown'
    """
    database_url = database_url.strip()

    if not database_url:
        return "unknown"

    if database_url.startswith("postgresql://"):
        return "postgresql"
    elif database_url.startswith("sqlite://"):
        return "sqlite"
    elif database_url.endswith(".yaml") or database_url.endswith(".yml"):
        return "yaml"
    elif (
        "/" in database_url or "\\" in database_url or "." in database_url
    ) and not database_url.startswith(("http://", "https://", "ftp://")):
        # Assume SQLite file path if it looks like a file path and isn't a URL protocol
        return "sqlite"
    else:
        return "unknown"


def validate_database_url(database_url: str) -> tuple[bool, str]:
    """
    Validate that a database URL is properly formatted and supported.

    Args:
        database_url: The database connection URL to validate

    Returns:
        Tuple of (is_valid: bool, error_message: str)
    """
    try:
        if not database_url or not database_url.strip():
            return False, "Database URL cannot be empty"

        database_url = database_url.strip()
        backend_type = detect_storage_backend_type(database_url)

        if backend_type == "unknown":
            return False, "Unable to determine storage backend type from URL"

        # Additional validation based on backend type
        if backend_type == "postgresql":
            if not database_url.startswith("postgresql://"):
                return False, "PostgreSQL URL must start with 'postgresql://'"
            # Basic validation - should have at least postgresql://host
            url_without_protocol = database_url.replace("postgresql://", "", 1)
            host_part = url_without_protocol.split("/")[0]
            if not host_part:
                return False, "PostgreSQL URL must specify a host"

        elif backend_type == "sqlite":
            # SQLite URLs are generally valid if they start with sqlite:// or look like paths
            if database_url.startswith("sqlite://"):
                path_part = database_url[10:]  # Remove sqlite://
                if not path_part.strip():
                    return False, "SQLite URL must specify a database path"
            elif not database_url.endswith((".db", ".sqlite", ".sqlite3")):
                # Warn but allow for flexibility
                pass

        elif backend_type == "yaml":
            if not (
                database_url.endswith(".yaml") or database_url.endswith(".yml")
            ):
                return (
                    False,
                    "YAML backend requires file ending with .yaml or .yml",
                )

        return True, "Valid database URL"

    except Exception as e:
        return False, f"Validation error: {e!s}"


def get_default_database_url() -> str:
    """
    Get a default SQLite database URL for development and testing.

    Returns:
        Default SQLite database URL in the current directory
    """
    return "sqlite:///todowrite.db"


# Configuration constants for different deployment environments
DEVELOPMENT_CONFIG = {
    "default_url": "sqlite:///todowrite_dev.db",
    "pool_size": 5,
    "max_overflow": 10,
}

PRODUCTION_CONFIG = {
    "default_url": "postgresql://user:password@localhost:5432/todowrite",
    "pool_size": 20,
    "max_overflow": 40,
}

TESTING_CONFIG = {
    "default_url": "sqlite:///tmp/todowrite_test.db",
    "pool_size": 1,
    "max_overflow": 1,
}


def create_storage_backend_for_environment(
    environment: str = "development", custom_url: str | None = None
) -> StorageBackend:
    """
    Create a storage backend optimized for a specific environment.

    Args:
        environment: One of 'development', 'production', or 'testing'
        custom_url: Optional custom database URL to override environment default

    Returns:
        StorageBackend instance configured for the specified environment
    """
    configs = {
        "development": DEVELOPMENT_CONFIG,
        "production": PRODUCTION_CONFIG,
        "testing": TESTING_CONFIG,
    }

    if environment not in configs:
        raise ValueError(
            f"Unknown environment: {environment}. Use: development, production, testing"
        )

    config = configs[environment]
    database_url = custom_url or config["default_url"]

    if environment == "production" and not custom_url:
        logger.warning(
            "Using default production database URL. Consider providing a custom URL."
        )

    if database_url.startswith("postgresql://"):
        return PostgreSQLBackend(
            database_url=database_url,
            pool_size=config["pool_size"],
            max_overflow=config["max_overflow"],
        )
    else:
        return create_storage_backend(database_url)
