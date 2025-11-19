"""
Pytest configuration and fixtures for ToDoWrite testing.

Provides database fixtures that ensure proper test isolation by recreating
database tables between tests while using a single test database file.
"""

import os
import sys
import uuid
import warnings
from collections.abc import Generator
from pathlib import Path
from typing import Any

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

# Add project root to sys.path for imports
project_root = Path(__file__).resolve().parent
sys.path.insert(0, str(project_root))

# Add lib_package to path for proper imports
lib_package_path = project_root.parent / "lib_package" / "src"
sys.path.insert(0, str(lib_package_path))

# Import todowrite modules first
from todowrite import create_engine, sessionmaker  # noqa: E402
from todowrite.core.types import Base  # noqa: E402


# Define get_database_path function since it's referenced but missing
def get_database_path(db_name: str) -> str:
    """Get database path for testing."""
    return str(Path(__file__).parent / f"{db_name}.db")


# Set test environment variables to use shared test database
os.environ["TODOWRITE_DATABASE_URL"] = "sqlite:///tests/todowrite_testing.db"
os.environ["TODOWRITE_STORAGE_PREFERENCE"] = "sqlite_only"


@pytest.fixture(scope="session")
def test_database_engine() -> Generator[Any, None, None]:
    """Create a test database engine for the entire test session.

    This fixture creates the database file and tables once per test session.
    Individual tests will use the table recreation fixture for isolation.
    """
    # Use a consistent project-specific test database file in project_root/tmp
    test_db_path = get_database_path("testing")
    database_url = f"sqlite:///{test_db_path}"

    # Remove existing test database if it exists
    db_file = Path(test_db_path)
    if db_file.exists():
        db_file.unlink()

    # Create engine and tables
    engine = create_engine(database_url)
    Base.metadata.create_all(engine)

    # Vacuum to minimize database size
    from sqlalchemy import text

    with engine.connect() as conn:
        conn.execute(text("VACUUM"))

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
    session_local = sessionmaker(bind=test_database_engine)
    session = session_local()

    try:
        yield session
    finally:
        session.close()
        # No need to drop tables here - the next test will do it


@pytest.fixture(scope="function")
def test_database_url() -> str:
    """Provide the test database URL for tests that need it."""
    test_db_path = get_database_path("testing")
    return f"sqlite:///{test_db_path}"


@pytest.fixture(autouse=True)
def setup_test_environment(monkeypatch: pytest.MonkeyPatch) -> None:
    """Automatically set up test environment for all tests."""
    # Set test environment variables to use shared test database
    monkeypatch.setenv("TODOWRITE_DATABASE_URL", "sqlite:///tests/todowrite_testing.db")
    monkeypatch.setenv("TODOWRITE_STORAGE_PREFERENCE", "sqlite_only")

    # Ensure no production todowrite.db exists in test directories
    # This enforces the convention: dev=todowrite_development.db,
    # test=tests/todowrite_testing.db (shared), prod=todowrite_production.db
    prod_db_file = Path("todowrite.db")
    if prod_db_file.exists():
        # Warn and remove production database from test environment
        warnings.warn(
            "Production todowrite.db found in test environment. "
            "Removing to enforce database naming conventions. "
            "Use: todowrite_development.db (dev), "
            "tests/todowrite_testing.db (test), "
            "todowrite_production.db (prod)",
            UserWarning,
            stacklevel=2,
        )
        prod_db_file.unlink()


@pytest.fixture
def sample_node_data() -> dict[str, Any]:
    """Provide unique sample node data for each test call."""
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
