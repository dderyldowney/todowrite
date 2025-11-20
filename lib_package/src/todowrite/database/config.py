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
storage_preference: StoragePreference = StoragePreference.POSTGRESQL_ONLY


def get_database_url() -> str:
    """Get database URL from environment variables.

    Environment Variables:
        TODOWRITE_DATABASE_URL: Full database URL (overrides automatic detection)
        DATABASE_URL: Standard database URL environment variable
        TODOWRITE_STORAGE_PREFERENCE: Storage preference (auto, postgresql_only, sqlite_only, yaml_only)

    Examples:
        PostgreSQL: postgresql://user:password@localhost:5432/ToDoWrite_db
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

        engine = create_engine(url, pool_pre_ping=True, pool_timeout=5)
        with engine.connect() as conn:
            result = conn.execute(text("SELECT 1"))
            return result.scalar() == 1
    except Exception:
        return False


def is_docker_available() -> bool:
    """Check if Docker is available and running."""
    try:
        import subprocess

        # Check if Docker daemon is running
        result = subprocess.run(
            ["docker", "info"],
            capture_output=True,
            check=True,
            timeout=5,
        )
        return result.returncode == 0
    except (
        subprocess.CalledProcessError,
        subprocess.TimeoutExpired,
        FileNotFoundError,
    ):
        return False


def is_docker_postgresql_running() -> bool:
    """Check if PostgreSQL Docker container is running."""
    if not is_docker_available():
        return False

    try:
        import json
        import subprocess

        # Check for running PostgreSQL containers (try multiple methods)
        # Method 1: Filter by image name
        result = subprocess.run(
            [
                "docker",
                "ps",
                "--filter",
                "ancestor=postgres",
                "--format",
                "json",
            ],
            capture_output=True,
            timeout=10,
        )

        if result.returncode == 0 and result.stdout:
            # Docker --format json outputs JSONL (one JSON per line)
            lines = result.stdout.decode().strip().split("\n")
            for line in lines:
                if line.strip():
                    container = json.loads(line)
                    if container.get("State") == "running":
                        return True

        # Method 2: Filter by image name (more permissive)
        result = subprocess.run(
            ["docker", "ps", "--filter", "name=postgres", "--format", "json"],
            capture_output=True,
            timeout=10,
        )

        if result.returncode == 0 and result.stdout:
            # Docker --format json outputs JSONL (one JSON per line)
            lines = result.stdout.decode().strip().split("\n")
            for line in lines:
                if line.strip():
                    container = json.loads(line)
                    if container.get("State") == "running":
                        return True

        # Method 3: Check all containers for postgres in image name
        result = subprocess.run(
            ["docker", "ps", "--format", "json"],
            capture_output=True,
            timeout=10,
        )

        if result.returncode == 0 and result.stdout:
            # Docker --format json outputs JSONL (one JSON per line)
            lines = result.stdout.decode().strip().split("\n")
            for line in lines:
                if line.strip():
                    container = json.loads(line)
                    image = container.get("Image", "")
                    names = container.get("Names", "")
                    if container.get("State") == "running" and (
                        "postgres" in image.lower() or "postgres" in str(names)
                    ):
                        return True

    except Exception:
        pass

    return False


def get_docker_postgresql_candidates() -> list[str]:
    """Get PostgreSQL connection candidates from running Docker containers."""
    candidates = []

    if not is_docker_available():
        return candidates

    try:
        import json
        import subprocess

        # Use the same detection logic as is_docker_postgresql_running
        # Method 1: Filter by image name
        result = subprocess.run(
            [
                "docker",
                "ps",
                "--filter",
                "ancestor=postgres",
                "--format",
                "json",
            ],
            capture_output=True,
            timeout=10,
        )

        if result.returncode == 0 and result.stdout:
            # Docker --format json outputs JSONL (one JSON per line)
            lines = result.stdout.decode().strip().split("\n")
            for line in lines:
                if line.strip():
                    container = json.loads(line)
                    if container.get("State") == "running":
                        # Extract port information
                        ports = container.get("Ports", "")
                        port = _extract_port_from_container(container)
                        candidates.append(
                            f"postgresql://todowrite:todowrite_dev_password@localhost:{port}/todowrite"
                        )

        # Method 2: Filter by container name (more permissive)
        result = subprocess.run(
            ["docker", "ps", "--filter", "name=postgres", "--format", "json"],
            capture_output=True,
            timeout=10,
        )

        if result.returncode == 0 and result.stdout:
            # Docker --format json outputs JSONL (one JSON per line)
            lines = result.stdout.decode().strip().split("\n")
            for line in lines:
                if line.strip():
                    container = json.loads(line)
                    if container.get("State") == "running":
                        # Extract port information
                        ports = container.get("Ports", "")
                        port = _extract_port_from_container(container)
                        candidates.append(
                            f"postgresql://todowrite:todowrite_dev_password@localhost:{port}/todowrite"
                        )

        # Method 3: Check all containers for postgres in image or name
        result = subprocess.run(
            ["docker", "ps", "--format", "json"],
            capture_output=True,
            timeout=10,
        )

        if result.returncode == 0 and result.stdout:
            # Docker --format json outputs JSONL (one JSON per line)
            lines = result.stdout.decode().strip().split("\n")
            for line in lines:
                if line.strip():
                    container = json.loads(line)
                    if container.get("State") == "running":
                        image = container.get("Image", "")
                        names = container.get("Names", [])
                        if "postgres" in image.lower() or "postgres" in str(
                            names
                        ):
                            port = _extract_port_from_container(container)
                            candidates.append(
                                f"postgresql://todowrite:todowrite_dev_password@localhost:{port}/todowrite"
                            )

    except Exception:
        pass

    return candidates


def _extract_port_from_container(container: dict[str, Any]) -> int:
    """Extract PostgreSQL port from Docker container info."""
    ports = container.get("Ports", "")

    # Default PostgreSQL ports
    if "5434" in ports:
        return 5434  # Performance testing container
    elif "5433" in ports:
        return 5433  # Test container
    elif "5432" in ports:
        return 5432  # Default container

    # Extract port from port mapping if available
    # Format is typically "0.0.0.0:5432->5432/tcp"
    port_mappings = ports.split(", ") if ports else []
    for mapping in port_mappings:
        if "->" in mapping:
            try:
                host_port = mapping.split("->")[0].split(":")[-1]
                if host_port.isdigit():
                    return int(host_port)
            except (ValueError, IndexError):
                continue

    return 5432  # Default fallback


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

    # Check Docker PostgreSQL containers first (highest priority)
    docker_candidates = get_docker_postgresql_candidates()
    candidates.extend(docker_candidates)

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
    """Try to find a working PostgreSQL connection (legacy compatibility)."""
    # This function is kept for backward compatibility but the actual logic
    # is now in _try_native_postgresql_candidates and _try_docker_postgresql_candidates
    native_result = _try_native_postgresql_candidates()
    if native_result:
        return native_result

    docker_result = _try_docker_postgresql_candidates()
    if docker_result:
        return docker_result

    return None


def _try_sqlite_candidates() -> tuple[StorageType, str] | None:
    """Try to find a working SQLite connection."""
    for url in get_sqlite_candidates():
        if check_sqlite_connection(url):
            return StorageType.SQLITE, url
    return None


def _auto_detect_storage() -> tuple[StorageType, str | None]:
    """Auto-detect the best available storage backend following priority: Native PostgreSQL → Docker PostgreSQL → SQLite3 → YAML."""
    # Priority 1: Try native PostgreSQL first
    native_postgresql_result = _try_native_postgresql_candidates()
    if native_postgresql_result:
        return native_postgresql_result

    # Priority 2: Try Docker PostgreSQL
    docker_postgresql_result = _try_docker_postgresql_candidates()
    if docker_postgresql_result:
        return docker_postgresql_result

    # Priority 3: Try SQLite3
    sqlite_result = _try_sqlite_candidates()
    if sqlite_result:
        return sqlite_result

    # Priority 4: Fall back to YAML
    return StorageType.YAML, None


def _try_native_postgresql_candidates() -> tuple[StorageType, str] | None:
    """Try to find a working native PostgreSQL connection."""
    # Check native PostgreSQL candidates first
    native_candidates = [
        # Standard localhost PostgreSQL
        "postgresql://todowrite:todowrite_dev_password@localhost:5432/todowrite",
        # Environment variable for native PostgreSQL
        os.getenv("POSTGRESQL_URL", ""),
        os.getenv("DATABASE_URL", ""),
    ]

    # Filter out empty strings and check PostgreSQL-specific URLs
    postgresql_candidates = [
        url for url in native_candidates if url.startswith("postgresql://")
    ]

    for url in postgresql_candidates:
        if check_postgresql_connection(url):
            return StorageType.POSTGRESQL, url

    return None


def _try_docker_postgresql_candidates() -> tuple[StorageType, str] | None:
    """Try to find a working PostgreSQL connection via Docker."""
    docker_candidates = get_docker_postgresql_candidates()

    for url in docker_candidates:
        if check_postgresql_connection(url):
            return StorageType.POSTGRESQL, url

    return None


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
        docker_running = is_docker_postgresql_running()
        if docker_running:
            return """
✅ PostgreSQL detected via Docker (preferred storage)
   Connected to running PostgreSQL container.
   No additional setup needed.
            """.strip()
        else:
            return """
✅ PostgreSQL detected (preferred storage)
   Direct PostgreSQL connection established.
   No additional setup needed.
            """.strip()

    elif info["type"] == "SQLite":
        docker_available = is_docker_available()
        if docker_available:
            return """
📋 SQLite detected (PostgreSQL available via Docker)

   To use PostgreSQL (recommended):
   1. Start PostgreSQL: cd tests && docker-compose up -d postgres
   2. Restart application (will auto-detect Docker PostgreSQL)
   3. Or manually: export TODOWRITE_DATABASE_URL=postgresql://todowrite:todowrite_dev_password@localhost:5432/todowrite

   Current SQLite file: {sqlite_path}
            """.format(sqlite_path=info.get("url", "Unknown"))
        else:
            return """
📋 SQLite detected (database fallback)

   PostgreSQL is not available on this system.
   Current SQLite file: {sqlite_path}

   To enable PostgreSQL:
   1. Install Docker Desktop
   2. Run: cd tests && docker-compose up -d postgres
   3. Restart application
            """.format(sqlite_path=info.get("url", "Unknown"))

    elif info["type"] == "YAML Files":
        docker_available = is_docker_available()
        if docker_available:
            return """
📄 YAML files mode (Docker PostgreSQL available)

   Database connections failed, using YAML files for storage.

   To use database storage:
   1. Start PostgreSQL: cd tests && docker-compose up -d postgres
   2. Restart application (will auto-detect)
   3. Check with: python -c "from todowrite.database.config import get_storage_info; print(get_storage_info())"
            """.strip()
        else:
            return """
📄 YAML files mode (last resort fallback)
   Database connections failed, using YAML files for storage.

   To use database storage:
   1. Install Docker Desktop for PostgreSQL support
   2. Ensure write permissions for SQLite fallback
   3. Or use YAML-only mode with: export TODOWRITE_STORAGE_PREFERENCE=yaml_only
            """.strip()

    else:
        return """
❌ Storage configuration error

   To resolve:
   1. Try: cd tests && docker-compose up -d postgres (PostgreSQL with Docker)
   2. Or: ensure write permissions for SQLite
   3. Or: set TODOWRITE_STORAGE_PREFERENCE=yaml_only (YAML fallback)
   4. Check: python -c "from todowrite.database.config import get_storage_info; print(get_storage_info())"
        """.strip()


# Legacy compatibility functions
def get_postgresql_url(
    user: str,
    password: str,
    host: str = "localhost",
    port: int = 5432,
    database: str = "ToDoWrite",
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
