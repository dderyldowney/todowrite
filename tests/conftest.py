"""
Pytest configuration and fixtures for ToDoWrite testing.

Provides database fixtures that ensure proper test isolation by recreating
database tables between tests while using a single test database file.
"""

import os
import sys
from pathlib import Path
from typing import Any, Generator

import pytest
from sqlalchemy import create_engine, text
from sqlalchemy.orm import Session, sessionmaker

# Add project root to sys.path for imports
project_root = Path(__file__).resolve().parent
sys.path.insert(0, str(project_root))

# Set test environment variables before importing todowrite modules
os.environ["TODOWRITE_DATABASE_URL"] = "sqlite:///testing_todowrite.db"
os.environ["TODOWRITE_STORAGE_PREFERENCE"] = "sqlite_only"

from todowrite.database.models import Base


@pytest.fixture(scope="session")
def test_database_engine() -> Generator[Any, None, None]:
    """Create a test database engine for the entire test session.

    This fixture creates the database file and tables once per test session.
    Individual tests will use the table recreation fixture for isolation.
    """
    # Use a consistent test database file
    database_url = "sqlite:///testing_todowrite.db"

    # Remove existing test database if it exists
    db_file = Path("testing_todowrite.db")
    if db_file.exists():
        db_file.unlink()

    # Create engine and tables
    engine = create_engine(database_url)
    Base.metadata.create_all(engine)

    yield engine

    # Cleanup: remove database file
    engine.dispose()
    if db_file.exists():
        db_file.unlink()


@pytest.fixture(scope="function")
def test_db_session(test_database_engine: Any) -> Generator[Session, None, None]:
    """Provide a database session with complete table recreation for each test.

    This fixture ensures test isolation by:
    1. Dropping all tables
    2. Recreating all tables
    3. Providing a fresh session
    4. Cleaning up after the test
    """
    # Drop all tables to ensure clean state
    Base.metadata.drop_all(test_database_engine)

    # Recreate all tables
    Base.metadata.create_all(test_database_engine)

    # Create session
    SessionLocal = sessionmaker(bind=test_database_engine)
    session = SessionLocal()

    try:
        yield session
    finally:
        session.close()
        # No need to drop tables here - the next test will do it


@pytest.fixture(scope="function")
def test_database_url() -> str:
    """Provide the test database URL for tests that need it."""
    return "sqlite:///testing_todowrite.db"


@pytest.fixture(autouse=True)
def setup_test_environment(monkeypatch: pytest.MonkeyPatch) -> None:
    """Automatically set up test environment for all tests."""
    # Set test environment variables
    monkeypatch.setenv("TODOWRITE_DATABASE_URL", "sqlite:///testing_todowrite.db")
    monkeypatch.setenv("TODOWRITE_STORAGE_PREFERENCE", "sqlite_only")


@pytest.fixture
def sample_node_data() -> dict[str, Any]:
    """Provide unique sample node data for each test call."""
    import uuid

    # Generate unique data for each fixture call
    unique_id = uuid.uuid4().hex[:8].upper()
    return {
        "id": f"GOAL-{unique_id}",
        "title": f"Test Goal {unique_id}",
        "description": f"A test goal for unit testing {unique_id}",
        "layer": "Goal",
        "status": "planned",
        "metadata": {
            "created_at": "2024-01-01T00:00:00Z",
            "updated_at": "2024-01-01T00:00:00Z",
            "version": 1,
        },
        "links": {"parents": [], "children": []},
    }