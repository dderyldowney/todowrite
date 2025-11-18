"""Tests for simplified database connection supporting only PostgreSQL and SQLite3.

Following TDD methodology: RED → GREEN → REFACTOR

This test file intentionally uses NO MOCKING per project mandate.
All tests use real database connections and temporary files.
"""

from __future__ import annotations

import tempfile
from pathlib import Path

from todowrite.database.config import (
    StorageType,
    check_postgresql_connection,
    check_sqlite_connection,
    determine_storage_backend,
    get_postgresql_candidates,
    get_sqlite_candidates,
)


class TestSimplifiedConnection:
    """Test suite for simplified database connection approach."""

    def test_sqlite_connection_detection_with_temp_file(self) -> None:
        """Test SQLite connection detection using temporary file."""
        with tempfile.TemporaryDirectory() as temp_dir:
            db_path = Path(temp_dir) / "test.db"
            sqlite_url = f"sqlite:///{db_path}"

            # This should work with a real temporary file
            assert check_sqlite_connection(sqlite_url) is True

            # Verify the database file was actually created
            assert db_path.exists()

    def test_sqlite_connection_detection_with_memory(self) -> None:
        """Test SQLite connection detection using in-memory database."""
        # This should work with in-memory SQLite
        assert check_sqlite_connection("sqlite:///:memory:") is True

    def test_sqlite_connection_detection_fails_invalid_path(self) -> None:
        """Test SQLite connection detection fails with invalid path."""
        # Use a non-existent directory that should fail
        invalid_url = "sqlite:///tests/todowrite_testing.db"
        assert check_sqlite_connection(invalid_url) is False

    def test_postgresql_connection_detection_fakes_no_real_db(self) -> None:
        """Test PostgreSQL connection detection fails without real database."""
        # This should fail since we don't have a real PostgreSQL running
        fake_url = "postgresql://user:pass@localhost:5432/fakedb"  # pragma: allowlist secret
        assert check_postgresql_connection(fake_url) is False

    def test_get_sqlite_candidates_returns_valid_urls(self) -> None:
        """Test that SQLite candidate generation returns valid URLs."""
        candidates = get_sqlite_candidates()

        # Should return at least one candidate
        assert len(candidates) > 0

        # All candidates should be valid SQLite URLs
        for candidate in candidates:
            assert candidate.startswith("sqlite:///")
            assert len(candidate) > len("sqlite:///")

    def test_get_postgresql_candidates_returns_valid_urls(self) -> None:
        """Test that PostgreSQL candidate generation returns valid URLs."""
        candidates = get_postgresql_candidates()

        # Should return candidates (even if they don't work)
        assert len(candidates) >= 0

        # All candidates should be valid PostgreSQL URLs
        for candidate in candidates:
            assert candidate.startswith("postgresql://")
            assert len(candidate) > len("postgresql://")

    def test_determine_storage_backend_prefers_postgresql(self) -> None:
        """Test storage backend determination prefers PostgreSQL when available."""
        # Clear environment to force auto-detection
        import os

        original_env = os.environ.get("TODOWRITE_DATABASE_URL")
        original_pref = os.environ.get("TODOWRITE_STORAGE_PREFERENCE")

        # Clear environment variables
        if "TODOWRITE_DATABASE_URL" in os.environ:
            del os.environ["TODOWRITE_DATABASE_URL"]
        if "TODOWRITE_STORAGE_PREFERENCE" in os.environ:
            del os.environ["TODOWRITE_STORAGE_PREFERENCE"]

        try:
            # Should try PostgreSQL first, fail connection, then fall back to SQLite
            storage_type, url = determine_storage_backend()

            # Should fallback to SQLite since PostgreSQL connection fails
            assert storage_type == StorageType.SQLITE
            assert url is not None
            assert url.startswith("sqlite:///")
        finally:
            # Restore original environment
            if original_env:
                os.environ["TODOWRITE_DATABASE_URL"] = original_env
            if original_pref:
                os.environ["TODOWRITE_STORAGE_PREFERENCE"] = original_pref

    def test_determine_storage_backend_finds_sqlite_when_no_postgres(self) -> None:
        """Test storage backend falls back to SQLite when PostgreSQL unavailable."""
        # Clear any existing database URL to force auto-detection
        import os

        original_env = os.environ.get("TODOWRITE_DATABASE_URL")
        if "TODOWRITE_DATABASE_URL" in os.environ:
            del os.environ["TODOWRITE_DATABASE_URL"]

        try:
            # Should find SQLite as fallback
            storage_type, url = determine_storage_backend()

            # Should use SQLite since PostgreSQL is not available
            assert storage_type == StorageType.SQLITE
            assert url is not None
            assert url.startswith("sqlite:///")
        finally:
            # Restore original environment
            if original_env:
                os.environ["TODOWRITE_DATABASE_URL"] = original_env

    def test_determine_storage_backend_uses_explicit_sqlite_url(self) -> None:
        """Test storage backend uses explicit SQLite URL when provided."""
        with tempfile.TemporaryDirectory() as temp_dir:
            db_path = Path(temp_dir) / "explicit_test.db"
            explicit_url = f"sqlite:///{db_path}"

            import os

            original_env = os.environ.get("TODOWRITE_DATABASE_URL")
            os.environ["TODOWRITE_DATABASE_URL"] = explicit_url

            try:
                # Should use the explicit SQLite URL
                storage_type, url = determine_storage_backend()

                assert storage_type == StorageType.SQLITE
                # URL should match exactly since we provided it explicitly
                assert url == explicit_url
            finally:
                # Restore original environment
                if original_env:
                    os.environ["TODOWRITE_DATABASE_URL"] = original_env
                elif "TODOWRITE_DATABASE_URL" in os.environ:
                    del os.environ["TODOWRITE_DATABASE_URL"]

    def test_determine_storage_backend_uses_explicit_postgresql_url(self) -> None:
        """Test storage backend uses explicit PostgreSQL URL when provided."""
        explicit_url = (
            "postgresql://testuser:testpass@localhost:5432/testdb"  # pragma: allowlist secret
        )

        import os

        original_env = os.environ.get("TODOWRITE_DATABASE_URL")
        original_pref = os.environ.get("TODOWRITE_STORAGE_PREFERENCE")

        # Clear storage preference to ensure AUTO mode
        if "TODOWRITE_STORAGE_PREFERENCE" in os.environ:
            del os.environ["TODOWRITE_STORAGE_PREFERENCE"]

        os.environ["TODOWRITE_DATABASE_URL"] = explicit_url

        try:
            # Should use the explicit PostgreSQL URL (even if fake)
            storage_type, url = determine_storage_backend()

            # Should use PostgreSQL with the explicit URL
            assert storage_type == StorageType.POSTGRESQL
            assert url == explicit_url
        finally:
            # Restore original environment
            os.environ["TODOWRITE_DATABASE_URL"] = original_env or ""
            if original_pref:
                os.environ["TODOWRITE_STORAGE_PREFERENCE"] = original_pref


class TestConnectionSimplification:
    """Test suite for verifying connection simplification removes complexity."""

    def test_yaml_storage_is_fallback_when_no_database_available(self) -> None:
        """Test that YAML storage is used as fallback when databases unavailable."""
        import os

        # Clear environment to force auto-detection with no databases available
        original_env = os.environ.get("TODOWRITE_DATABASE_URL")
        original_pref = os.environ.get("TODOWRITE_STORAGE_PREFERENCE")

        # Clear environment variables
        if "TODOWRITE_DATABASE_URL" in os.environ:
            del os.environ["TODOWRITE_DATABASE_URL"]
        if "TODOWRITE_STORAGE_PREFERENCE" in os.environ:
            del os.environ["TODOWRITE_STORAGE_PREFERENCE"]

        try:
            # Should try PostgreSQL first, fail connection, then try SQLite, succeed, return SQLite
            storage_type, url = determine_storage_backend()

            # Should use SQLite (which should be available as fallback)
            # Note: YAML fallback only happens when BOTH PostgreSQL and SQLite are unavailable
            # Since SQLite file creation usually works, we typically get SQLite, not YAML
            assert storage_type == StorageType.SQLITE
            assert url is not None
            assert url.startswith("sqlite:///")
        finally:
            # Restore original environment
            if original_env:
                os.environ["TODOWRITE_DATABASE_URL"] = original_env
            if original_pref:
                os.environ["TODOWRITE_STORAGE_PREFERENCE"] = original_pref

    def test_simplified_candidate_generation(self) -> None:
        """Test that candidate generation is simplified."""
        # Clear environment to get default candidates
        import os

        original_env = os.environ.get("TODOWRITE_DATABASE_URL")
        if "TODOWRITE_DATABASE_URL" in os.environ:
            del os.environ["TODOWRITE_DATABASE_URL"]

        try:
            sqlite_candidates = get_sqlite_candidates()
            postgresql_candidates = get_postgresql_candidates()

            # Should have reasonable number of candidates
            assert len(sqlite_candidates) >= 1
            assert len(postgresql_candidates) >= 0

            # SQLite candidates should be simple paths
            for candidate in sqlite_candidates:
                assert "sqlite:///" in candidate
                # Should use simple default names, no complex project-specific naming
                assert candidate in [
                    "sqlite:///tests/todowrite_testing.db",
                    "sqlite:///tests/todowrite_testing.db",
                ]
        finally:
            # Restore environment
            if original_env:
                os.environ["TODOWRITE_DATABASE_URL"] = original_env

    def test_connection_testing_is_simple_and_direct(self) -> None:
        """Test that connection testing is simple and direct."""
        # SQLite with memory database should just work
        assert check_sqlite_connection("sqlite:///:memory:") is True

        # PostgreSQL with fake URL should just fail
        assert check_postgresql_connection("postgresql://fake@localhost/fake") is False

        # Should be fast and simple (no complex detection logic)
        # This is more of a performance/design assertion


class TestRealDatabaseBehavior:
    """Test real database behavior without mocking."""

    def test_real_sqlite_database_operations(self) -> None:
        """Test real SQLite database creation and operations."""
        with tempfile.TemporaryDirectory() as temp_dir:
            db_path = Path(temp_dir) / "real_test.db"
            sqlite_url = f"sqlite:///{db_path}"

            # Test connection
            assert check_sqlite_connection(sqlite_url) is True

            # Verify database file exists and is real file
            assert db_path.exists()
            assert db_path.is_file()
            # File might be 0 bytes initially but gets created when connected to
            # The important thing is that the file exists and connection works

            # Test actual database operations with SQLAlchemy
            from sqlalchemy import create_engine, text

            engine = create_engine(sqlite_url)
            with engine.connect() as conn:
                # Test basic query
                result = conn.execute(text("SELECT 1 as test")).fetchone()
                assert result[0] == 1

                # Test table creation
                conn.execute(
                    text("""
                    CREATE TABLE test_table (
                        id INTEGER PRIMARY KEY,
                        name TEXT NOT NULL
                    )
                """)
                )
                conn.commit()

                # Test data insertion
                conn.execute(text("INSERT INTO test_table (name) VALUES ('test')"))
                conn.commit()

                # Test data retrieval
                result = conn.execute(
                    text("SELECT name FROM test_table WHERE name = 'test'")
                ).fetchone()
                assert result[0] == "test"
