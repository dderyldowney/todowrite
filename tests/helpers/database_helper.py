"""
Database helper utilities for testing.

Provides utilities to create isolated database contexts for tests
that don't use pytest fixtures directly.
"""

import os
import sys
from collections.abc import Generator
from contextlib import contextmanager
from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

# Ensure we can import todowrite modules
project_root = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(project_root))

from todowrite.database.models import Base
from todowrite.utils.database_utils import get_project_database_name


@contextmanager
def isolated_test_database() -> Generator[Session, None, None]:
    """Context manager for isolated test database sessions.

    This context manager provides a completely fresh database state:
    1. Sets up test environment variables
    2. Drops and recreates all tables
    3. Yields a fresh session
    4. Cleans up afterwards

    Usage:
        with isolated_test_database() as session:
            # Use session for database operations
            # Tables are fresh for this test
            pass
    """
    # Set test environment with project-specific naming
    test_db_name = get_project_database_name("testing")
    os.environ["TODOWRITE_DATABASE_URL"] = f"sqlite:///{test_db_name}"
    os.environ["TODOWRITE_STORAGE_PREFERENCE"] = "sqlite_only"

    # Database setup
    database_url = f"sqlite:///{test_db_name}"
    engine = create_engine(database_url)

    try:
        # Drop and recreate all tables for complete isolation
        Base.metadata.drop_all(engine)
        Base.metadata.create_all(engine)

        # Create session
        SessionLocal = sessionmaker(bind=engine)
        session = SessionLocal()

        yield session

    finally:
        # Always close session and dispose engine
        if "session" in locals():
            session.close()
        engine.dispose()


def get_test_database_url() -> str:
    """Get the test database URL with project-specific naming."""
    test_db_name = get_project_database_name("testing")
    return f"sqlite:///{test_db_name}"


def ensure_test_database() -> None:
    """Ensure the test database exists and has proper schema."""
    test_db_name = get_project_database_name("testing")
    database_url = f"sqlite:///{test_db_name}"
    engine = create_engine(database_url)

    # Create tables if they don't exist
    Base.metadata.create_all(engine)
    engine.dispose()
