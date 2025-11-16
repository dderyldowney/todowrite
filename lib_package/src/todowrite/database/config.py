"""
Simplified database connection configuration for ToDoWrite.

Supports PostgreSQL, SQLite3, and YAML fallback for simplicity over complexity.
Priority: PostgreSQL (if available) → SQLite3 (fallback) → YAML (last resort)

No complex auto-detection, no Docker discovery.
Simple, direct database connections.
"""

from __future__ import annotations

import os
from enum import Enum


class StorageType(Enum):
    """Available storage types for ToDoWrite."""

    POSTGRESQL = "postgresql"
    SQLITE = "sqlite"
    YAML = "yaml"


class StoragePreference(Enum):
    """Storage preference options."""

    AUTO = "auto"  # Try PostgreSQL → SQLite → YAML
    POSTGRESQL_ONLY = "postgresql_only"  # Only try PostgreSQL
    SQLITE_ONLY = "sqlite_only"  # Only try SQLite
    YAML_ONLY = "yaml_only"  # Only use YAML files


# Global storage preference - can be overridden
storage_preference: StoragePreference = StoragePreference.AUTO


def get_database_url() -> str:
    """Get database URL from environment variables.

    Environment Variables:
        TODOWRITE_DATABASE_URL: Full database URL (overrides automatic detection)
        DATABASE_URL: Standard database URL environment variable
        TODOWRITE_STORAGE_PREFERENCE: Storage preference (auto, postgresql_only, sqlite_only, yaml_only)

    Examples:
        PostgreSQL: postgresql://user:password@localhost:5432/todowrite_db
        SQLite: sqlite:///todowrite.db
        YAML: leave empty for YAML fallback
    """
    return os.getenv(
        "TODOWRITE_DATABASE_URL",
        os.getenv("DATABASE_URL", ""),  # Check standard DATABASE_URL too
    )


# Legacy compatibility - use get_database_url() instead
DATABASE_URL = get_database_url()


def set_storage_preference(preference: StoragePreference) -> None:
    """Set the global storage preference."""
    global storage_preference
    storage_preference = preference


def get_storage_preference() -> StoragePreference:
    """Get the current storage preference."""
    # Check environment variable first
    env_pref = os.getenv("TODOWRITE_STORAGE_PREFERENCE", "").lower()
    if env_pref:
        try:
            return StoragePreference(env_pref)
        except ValueError:
            pass

    return storage_preference


def check_postgresql_connection(url: str) -> bool:
    """Test if PostgreSQL connection is available."""
    try:
        from sqlalchemy import create_engine, text

        engine = create_engine(url)
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        return True
    except Exception:
        return False


def check_sqlite_connection(url: str) -> bool:
    """Test if SQLite connection is available."""
    try:
        from sqlalchemy import create_engine, text

        engine = create_engine(url)
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        return True
    except Exception:
        return False


def get_postgresql_candidates() -> list[str]:
    """Get list of potential PostgreSQL connection URLs to try."""
    candidates: list[str] = []

    # Explicit URL from environment (read dynamically)
    db_url = get_database_url()
    if db_url and db_url.startswith("postgresql:"):
        candidates.append(db_url)

    # Standard localhost (simple, no Docker detection)
    candidates.append(
        "postgresql://todowrite:todowrite_dev_password@localhost:5432/todowrite"
    )

    return candidates


def get_sqlite_candidates() -> list[str]:
    """Get list of potential SQLite connection URLs to try."""
    candidates: list[str] = []

    # Explicit URL from environment (read dynamically)
    db_url = get_database_url()
    if db_url and db_url.startswith("sqlite:"):
        candidates.append(db_url)

    # Simple default locations
    candidates.extend(
        [
            "sqlite:///todowrite.db",
            "sqlite:///./todowrite.db",
        ]
    )

    return candidates


def _handle_explicit_database_url(
    db_url: str, preference: StoragePreference
) -> tuple[StorageType, str] | None:
    """Handle explicitly provided database URL."""
    if db_url.startswith("postgresql:"):
        if preference == StoragePreference.SQLITE_ONLY:
            raise RuntimeError("SQLite requested but PostgreSQL URL provided")
        return StorageType.POSTGRESQL, db_url
    elif db_url.startswith("sqlite:"):
        if preference == StoragePreference.POSTGRESQL_ONLY:
            raise RuntimeError("PostgreSQL requested but SQLite URL provided")
        return StorageType.SQLITE, db_url
    return None


def _try_postgresql_candidates() -> tuple[StorageType, str] | None:
    """Try to find a working PostgreSQL connection."""
    for url in get_postgresql_candidates():
        if check_postgresql_connection(url):
            return StorageType.POSTGRESQL, url
    return None


def _try_sqlite_candidates() -> tuple[StorageType, str] | None:
    """Try to find a working SQLite connection."""
    for url in get_sqlite_candidates():
        if check_sqlite_connection(url):
            return StorageType.SQLITE, url
    return None


def _auto_detect_storage() -> tuple[StorageType, str | None]:
    """Auto-detect the best available storage backend."""
    # Try PostgreSQL first
    postgresql_result = _try_postgresql_candidates()
    if postgresql_result:
        return postgresql_result

    # Try SQLite second
    sqlite_result = _try_sqlite_candidates()
    if sqlite_result:
        return sqlite_result

    # Fall back to YAML
    return StorageType.YAML, None


def determine_storage_backend() -> tuple[StorageType, str | None]:
    """
    Determine storage backend based on preference and availability.

    Returns:
        Tuple of (StorageType, connection_url_or_none_for_yaml)
    """
    preference = get_storage_preference()

    # YAML preference - skip database detection
    if preference == StoragePreference.YAML_ONLY:
        return StorageType.YAML, None

    # Handle explicit database URL
    db_url = get_database_url()
    if db_url:
        explicit_result = _handle_explicit_database_url(db_url, preference)
        if explicit_result:
            return explicit_result

    # Handle specific preferences
    if preference == StoragePreference.POSTGRESQL_ONLY:
        result = _try_postgresql_candidates()
        if result:
            return result
        raise RuntimeError("PostgreSQL requested but not available")

    if preference == StoragePreference.SQLITE_ONLY:
        result = _try_sqlite_candidates()
        if result:
            return result
        raise RuntimeError("SQLite requested but not available")

    # Auto-detection (StoragePreference.AUTO)
    return _auto_detect_storage()


def get_storage_info() -> dict[str, str]:
    """Get information about the current storage configuration."""
    try:
        storage_type, url = determine_storage_backend()
        preference = get_storage_preference()

        if storage_type == StorageType.POSTGRESQL:
            return {
                "type": "PostgreSQL",
                "url": url or "",
                "priority": "1 (Preferred)",
                "fallback": "No",
                "preference": preference.value,
            }
        elif storage_type == StorageType.SQLITE:
            return {
                "type": "SQLite",
                "url": url or "",
                "priority": "2 (Database Fallback)",
                "fallback": "Yes",
                "preference": preference.value,
            }
        else:  # YAML
            return {
                "type": "YAML Files",
                "url": "configs/ directory",
                "priority": "3 (Last Resort)",
                "fallback": "Yes",
                "preference": preference.value,
            }
    except Exception as e:
        return {
            "type": "Error",
            "url": f"Error: {e}",
            "priority": "Unknown",
            "fallback": "Unknown",
            "preference": get_storage_preference().value,
        }


def get_setup_guidance() -> str:
    """Provide setup guidance for storage configuration."""
    info = get_storage_info()

    if info["type"] == "PostgreSQL":
        return """
✅ PostgreSQL detected (preferred storage)
   No additional setup needed.
        """.strip()

    elif info["type"] == "SQLite":
        return """
📋 SQLite detected (database fallback)

   To use PostgreSQL (recommended):
   1. Run: cd tests && docker-compose up -d postgres
   2. Optional: export TODOWRITE_DATABASE_URL=postgresql://todowrite:todowrite_dev_password@localhost:5432/todowrite
   3. Restart application (will auto-detect PostgreSQL)
        """.strip()

    elif info["type"] == "YAML Files":
        return """
📄 YAML files mode (last resort fallback)
   Database connections failed, using YAML files for storage.

   To use database storage:
   1. For PostgreSQL: cd tests && docker-compose up -d postgres
   2. For SQLite: Ensure write permissions in current directory
   3. Check: python -m todowrite db-status
        """.strip()

    else:
        return """
❌ Storage configuration error

   To resolve:
   1. Try: cd tests && docker-compose up -d postgres (PostgreSQL)
   2. Or: ensure current directory is writable (SQLite)
   3. Or: set TODOWRITE_STORAGE_PREFERENCE=yaml_only (YAML fallback)
        """.strip()


# Legacy compatibility functions
def get_postgresql_url(
    user: str,
    password: str,
    host: str = "localhost",
    port: int = 5432,
    database: str = "todowrite",
) -> str:
    """Generate PostgreSQL connection URL."""
    return f"postgresql://{user}:{password}@{host}:{port}/{database}"


def is_sqlite() -> bool:
    """Check if current configuration uses SQLite."""
    storage_type, _ = determine_storage_backend()
    return storage_type == StorageType.SQLITE


def is_postgresql() -> bool:
    """Check if current configuration uses PostgreSQL."""
    storage_type, _ = determine_storage_backend()
    return storage_type == StorageType.POSTGRESQL


def is_yaml() -> bool:
    """Check if current configuration uses YAML files."""
    storage_type, _ = determine_storage_backend()
    return storage_type == StorageType.YAML
