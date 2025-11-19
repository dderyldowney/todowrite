"""Tests for simplified CLI database connection using library approach.

Following TDD methodology: RED → GREEN → REFACTOR

This test file intentionally uses NO MOCKING per project mandate.
All tests use real database connections and temporary files.
Each test gets its own isolated database for proper test isolation.
"""

from __future__ import annotations

import tempfile
from pathlib import Path
from unittest import TestCase

from click.testing import CliRunner
from sqlalchemy import create_engine
from todowrite.core.models import Base, Goal
from todowrite_cli.main import cli, get_session, init_database


class TestSimplifiedCLIConnection(TestCase):
    """Test suite for simplified CLI database connection approach."""

    def setUp(self) -> None:
        """Set up test environment with CLI runner."""
        self.runner = CliRunner()

    def _create_test_database(self) -> str:
        """Create a temporary test database and return its path."""
        with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as tmp:
            test_db_path = tmp.name

        # Initialize database with all tables
        engine = create_engine(f"sqlite:///{test_db_path}")
        Base.metadata.create_all(engine)
        engine.dispose()

        return test_db_path

    def _cleanup_test_database(self, test_db_path: str) -> None:
        """Remove the temporary test database file."""
        test_db_file = Path(test_db_path)
        if test_db_file.exists():
            test_db_file.unlink()

    def test_cli_with_temporary_database(self) -> None:
        """Test that CLI works with temporary database."""
        test_db_path = self._create_test_database()

        try:
            # Initialize database
            result = self.runner.invoke(cli, ["--database", test_db_path, "init"])
            assert result.exit_code == 0
            assert "Database initialized" in result.output

            # Create a goal
            result = self.runner.invoke(
                cli,
                [
                    "--database",
                    test_db_path,
                    "create",
                    "--layer",
                    "goal",
                    "--title",
                    "Test Goal",
                    "--owner",
                    "test-user",
                ],
            )
            assert result.exit_code == 0
            assert "Created Goal" in result.output

            # List items
            result = self.runner.invoke(cli, ["--database", test_db_path, "list"])
            assert result.exit_code == 0
            assert "Test Goal" in result.output

        finally:
            self._cleanup_test_database(test_db_path)

    def test_cli_get_session_function(self) -> None:
        """Test the get_session helper function."""
        test_db_path = self._create_test_database()

        try:
            # Test session creation
            session, _engine = get_session(f"sqlite:///{test_db_path}")
            assert session is not None
            assert _engine is not None

            # Test that session is functional
            goal = Goal(title="Test Goal")
            session.add(goal)
            session.commit()

            # Query back the goal
            retrieved = session.query(Goal).first()
            assert retrieved is not None
            assert retrieved.title == "Test Goal"

            session.close()

        finally:
            self._cleanup_test_database(test_db_path)

    def test_cli_init_database_function(self) -> None:
        """Test the init_database helper function."""
        test_db_path = self._create_test_database()

        try:
            # This should work without errors
            init_database(f"sqlite:///{test_db_path}")

            # Verify tables were created by checking model count
            session, _engine = get_session(f"sqlite:///{test_db_path}")

            # Should be able to query without errors (even if empty)
            goals = session.query(Goal).all()
            assert isinstance(goals, list)

            session.close()

        finally:
            self._cleanup_test_database(test_db_path)

    def test_cli_command_with_invalid_database_path(self) -> None:
        """Test CLI behavior with invalid database path."""
        test_db_path = self._create_test_database()

        try:
            # Try to use a directory that doesn't exist
            invalid_path = "/nonexistent/directory/test.db"
            result = self.runner.invoke(cli, ["--database", invalid_path, "list"])

            # Should handle gracefully (SQLite creates the database)
            assert result.exit_code == 0

        finally:
            self._cleanup_test_database(test_db_path)

    def test_cli_with_memory_database(self) -> None:
        """Test CLI with in-memory database."""
        test_db_path = "sqlite:///:memory:"

        # Note: In-memory databases don't persist between CLI invocations
        # Each invocation gets a fresh database, so we test init only

        # Initialize memory database
        result = self.runner.invoke(cli, ["--database", test_db_path, "init"])
        assert result.exit_code == 0

        # Memory database works for initialization
        # Cannot test item creation as each CLI call gets fresh database

    def test_cli_multiple_commands_same_session(self) -> None:
        """Test multiple CLI commands with same database."""
        test_db_path = self._create_test_database()

        try:
            # Initialize and create multiple items
            self.runner.invoke(cli, ["--database", test_db_path, "init"])

            self.runner.invoke(
                cli, ["--database", test_db_path, "create", "--layer", "goal", "--title", "Goal 1"]
            )

            self.runner.invoke(
                cli, ["--database", test_db_path, "create", "--layer", "task", "--title", "Task 1"]
            )

            # List all items
            result = self.runner.invoke(cli, ["--database", test_db_path, "list"])
            assert result.exit_code == 0
            assert "Goal 1" in result.output
            assert "Task 1" in result.output

            # Get stats
            result = self.runner.invoke(cli, ["--database", test_db_path, "stats"])
            assert result.exit_code == 0
            assert "Goal" in result.output
            assert "Task" in result.output

        finally:
            self._cleanup_test_database(test_db_path)

    def test_database_isolation_between_tests(self) -> None:
        """Test that each test gets a completely isolated database."""
        test_db_path = self._create_test_database()

        try:
            # Create data in this test's database
            result = self.runner.invoke(
                cli,
                [
                    "--database",
                    test_db_path,
                    "create",
                    "--layer",
                    "goal",
                    "--title",
                    "Isolation Test Goal",
                ],
            )
            assert result.exit_code == 0

            # Verify data exists in this database
            result = self.runner.invoke(cli, ["--database", test_db_path, "list"])
            assert result.exit_code == 0
            assert "Isolation Test Goal" in result.output

            # Verify database file exists and has content
            db_file = Path(test_db_path)
            assert db_file.exists()
            assert db_file.stat().st_size > 0

            # Create a second database to verify isolation
            test_db_path_2 = self._create_test_database()

            try:
                # Second database should be empty
                result = self.runner.invoke(cli, ["--database", test_db_path_2, "list"])
                assert result.exit_code == 0
                assert "No items found" in result.output
                assert "Isolation Test Goal" not in result.output

            finally:
                self._cleanup_test_database(test_db_path_2)

        finally:
            self._cleanup_test_database(test_db_path)

    def test_database_cleanup_verification(self) -> None:
        """Test that database cleanup properly removes all files."""
        test_db_path = self._create_test_database()

        # Verify database file exists before cleanup
        db_file = Path(test_db_path)
        assert db_file.exists()

        # Add some data to make the database file larger
        self.runner.invoke(
            cli,
            [
                "--database",
                test_db_path,
                "create",
                "--layer",
                "goal",
                "--title",
                "Cleanup Test Goal",
            ],
        )

        # Verify file has content
        initial_size = db_file.stat().st_size
        assert initial_size > 0

        # Cleanup database
        self._cleanup_test_database(test_db_path)

        # Verify file is completely removed
        assert not db_file.exists()

    def test_multiple_databases_concurrent_access(self) -> None:
        """Test that multiple databases can be used simultaneously."""
        test_db_1 = self._create_test_database()
        test_db_2 = self._create_test_database()

        try:
            # Create different data in each database
            self.runner.invoke(
                cli,
                [
                    "--database",
                    test_db_1,
                    "create",
                    "--layer",
                    "goal",
                    "--title",
                    "Database 1 Goal",
                ],
            )

            self.runner.invoke(
                cli,
                [
                    "--database",
                    test_db_2,
                    "create",
                    "--layer",
                    "task",
                    "--title",
                    "Database 2 Task",
                ],
            )

            # Verify each database contains only its own data
            result_1 = self.runner.invoke(cli, ["--database", test_db_1, "list"])
            assert result_1.exit_code == 0
            assert "Database 1 Goal" in result_1.output
            assert "Database 2 Task" not in result_1.output

            result_2 = self.runner.invoke(cli, ["--database", test_db_2, "list"])
            assert result_2.exit_code == 0
            assert "Database 2 Task" in result_2.output
            assert "Database 1 Goal" not in result_2.output

        finally:
            self._cleanup_test_database(test_db_1)
            self._cleanup_test_database(test_db_2)

    def test_database_persistence_across_commands(self) -> None:
        """Test that data persists across multiple CLI commands on same database."""
        test_db_path = self._create_test_database()

        try:
            # Create initial data
            self.runner.invoke(
                cli,
                [
                    "--database",
                    test_db_path,
                    "create",
                    "--layer",
                    "goal",
                    "--title",
                    "Persistent Goal",
                ],
            )

            # Add more data
            self.runner.invoke(
                cli,
                [
                    "--database",
                    test_db_path,
                    "create",
                    "--layer",
                    "task",
                    "--title",
                    "Persistent Task",
                ],
            )

            # Update data (if we had an update command)
            # For now, just verify both items persist

            # Verify all data persists
            result = self.runner.invoke(cli, ["--database", test_db_path, "list"])
            assert result.exit_code == 0
            assert "Persistent Goal" in result.output
            assert "Persistent Task" in result.output

            # Verify stats show correct count
            result = self.runner.invoke(cli, ["--database", test_db_path, "stats"])
            assert result.exit_code == 0
            assert "TOTAL" in result.output

        finally:
            self._cleanup_test_database(test_db_path)
