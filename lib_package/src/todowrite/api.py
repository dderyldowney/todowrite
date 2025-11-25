"""ToDoWrite API - Industry Standard Interface.

This module provides the main ToDoWrite class following industry standards
for Python APIs and software development practices.

Created for professional hierarchical task management system integration.
"""

from __future__ import annotations

import logging

# Import at module level as required by industry standards
try:
    from .storage.factory import StorageFactory, initialize_database
except ImportError:
    initialize_database = None
    StorageFactory = None


# Handle database initialization error gracefully
class DatabaseInitializationError(Exception):
    """Database initialization error."""

    pass


logger = logging.getLogger(__name__)


class ToDoWrite:
    """
    Industry-standard ToDoWrite API for hierarchical task management.

    This class provides a clean, professional interface for interacting with
    ToDoWrite's hierarchical task management system, following Python
    community best practices and design patterns.

    Attributes:
        database_url (Optional[str]): Database connection URL. If None,
            uses environment variables or defaults.

    Example:
        >>> # Initialize with default database
        app = ToDoWrite()
        >>> app.init_database()

        >>> # Initialize with custom database
        app = ToDoWrite("sqlite:///my_tasks.db")
        >>> app.init_database()
    """

    def __init__(self, database_url: str | None = None) -> None:
        """
        Initialize ToDoWrite API instance.

        Args:
            database_url: Database connection URL. Supports SQLite and PostgreSQL.
                          If None, reads from TODOWRITE_DATABASE_URL environment
                          variable or uses appropriate default.

        Raises:
            ValueError: If database_url format is invalid.
        """
        self.database_url = database_url
        self._validate_database_url()

    def _validate_database_url(self) -> None:
        """Validate the database URL format."""
        if self.database_url and not isinstance(self.database_url, str):
            raise ValueError("Database URL must be a string")

        if self.database_url and not self.database_url.strip():
            raise ValueError("Database URL cannot be empty")

    def init_database(self) -> bool:
        """
        Initialize the database with proper schema.

        Creates all necessary tables and applies migrations if needed.
        Uses industry-standard database initialization practices.

        Returns:
            bool: True if initialization was successful.

        Raises:
            DatabaseInitializationError: If database initialization fails.
        """
        try:
            if self.database_url:
                logger.info(f"Initializing database: {self.database_url}")
                initialize_database(self.database_url)
            else:
                logger.info("Initializing default database")
                initialize_database()

            logger.info("Database initialization completed successfully")
            return True

        except Exception as e:
            logger.error(f"Database initialization failed: {e}")
            raise DatabaseInitializationError(
                f"Failed to initialize database: {e}"
            )

    def get_database_url(self) -> str:
        """
        Get the current database URL.

        Returns:
            str: The database connection URL.
        """
        return self.database_url or "Default database"

    def __repr__(self) -> str:
        """Return string representation of ToDoWrite instance."""
        return f"ToDoWrite(database_url='{self.get_database_url()}')"

    def __str__(self) -> str:
        """Return human-readable string representation."""
        return f"ToDoWrite API - Database: {self.get_database_url()}"
