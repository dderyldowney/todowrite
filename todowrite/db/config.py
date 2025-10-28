"""
This module contains the configuration for the database connection.

Supports both SQLite (default) and PostgreSQL databases through environment variables.
"""

import os

# Database configuration with environment variable support
DATABASE_URL: str = os.getenv("TODOWRITE_DATABASE_URL", "sqlite:///todowrite.db")
"""The URL for the database connection.

Environment Variables:
    TODOWRITE_DATABASE_URL: Full database URL (overrides default SQLite)

Examples:
    SQLite (default): sqlite:///todowrite.db
    PostgreSQL: postgresql://user:password@localhost:5432/todowrite_db
"""


# PostgreSQL configuration helpers
def get_postgresql_url(
    user: str,
    password: str,
    host: str = "localhost",
    port: int = 5432,
    database: str = "todowrite",
) -> str:
    """
    Generate PostgreSQL connection URL.

    Args:
        user: Database username
        password: Database password
        host: Database host (default: localhost)
        port: Database port (default: 5432)
        database: Database name (default: todowrite)

    Returns:
        PostgreSQL connection URL string
    """
    return f"postgresql://{user}:{password}@{host}:{port}/{database}"


# Database type detection
def is_sqlite() -> bool:
    """Check if current configuration uses SQLite."""
    return DATABASE_URL.startswith("sqlite:")


def is_postgresql() -> bool:
    """Check if current configuration uses PostgreSQL."""
    return DATABASE_URL.startswith("postgresql:")
