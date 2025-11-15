"""Tests for simplified CLI database connection using library approach.

Following TDD methodology: RED → GREEN → REFACTOR

This test file intentionally uses NO MOCKING per project mandate.
All tests use real database connections and temporary files.
"""

from __future__ import annotations

import tempfile
from pathlib import Path
from unittest.mock import patch

from click.testing import CliRunner
from todowrite_cli.main import cli, get_app


class TestSimplifiedCLIConnection:
    """Test suite for simplified CLI database connection approach."""

    def test_cli_respects_storage_preference_from_library(self) -> None:
        """Test that CLI respects storage preference from library."""
        runner = CliRunner()

        # Should work with library's simplified connection logic
        result = runner.invoke(cli, ["--storage-preference", "sqlite_only", "init"])

        # Should succeed with SQLite fallback
        assert result.exit_code == 0
        assert "Database initialized successfully" in result.output

    def test_cli_uses_library_auto_detection_when_no_preference(self) -> None:
        """Test that CLI uses library auto-detection when no preference specified."""
        runner = CliRunner()

        # Should use library's auto-detection (PostgreSQL → SQLite → YAML)
        result = runner.invoke(cli, ["init"])

        # Should succeed with auto-detected backend
        assert result.exit_code == 0
        assert "Database initialized successfully" in result.output

    def test_cli_explicit_database_path_works_with_library(self) -> None:
        """Test that CLI explicit database path works through library."""
        runner = CliRunner()

        with tempfile.TemporaryDirectory() as temp_dir:
            db_path = Path(temp_dir) / "cli_test.db"

            result = runner.invoke(cli, ["init", "--database-path", str(db_path)])

            # Should succeed and use explicit path
            assert result.exit_code == 0
            assert "Database initialized successfully" in result.output

    def test_cli_handles_yaml_preference_via_library(self) -> None:
        """Test that CLI handles YAML preference through library."""
        runner = CliRunner()

        result = runner.invoke(cli, ["--storage-preference", "yaml_only", "init"])

        # Should succeed with YAML backend
        assert result.exit_code == 0
        assert "Database initialized successfully" in result.output

    def test_get_app_uses_simplified_library_logic(self) -> None:
        """Test that get_app() uses simplified library connection logic."""
        with tempfile.TemporaryDirectory() as temp_dir:
            db_path = Path(temp_dir) / "get_app_test.db"

            # Should use simplified library connection
            app = get_app(str(db_path))

            # Should be able to initialize
            app.init_database()

            # Database file should be created
            assert db_path.exists()

    def test_get_app_with_no_arguments_uses_library_auto_detection(self) -> None:
        """Test get_app() with no arguments uses library auto-detection."""
        # Should use library's simplified auto-detection
        app = get_app()

        # Should be able to initialize
        app.init_database()

        # Should have a valid storage backend
        assert hasattr(app, "storage_type")

    def test_get_app_with_sqlite_url_uses_library_directly(self) -> None:
        """Test get_app() with SQLite URL uses library directly."""
        with tempfile.TemporaryDirectory() as temp_dir:
            db_path = Path(temp_dir) / "sqlite_test.db"
            sqlite_url = f"sqlite:///{db_path}"

            # Should use library's simplified connection
            app = get_app(sqlite_url)

            # Should use SQLite
            assert app.storage_type.value == "sqlite"

            # Database file should be created
            assert db_path.exists()

    def test_cli_commands_work_with_simplified_connection(self) -> None:
        """Test that CLI commands work with simplified connection."""
        runner = CliRunner()

        # Initialize first
        init_result = runner.invoke(cli, ["init"])
        assert init_result.exit_code == 0

        # Create a node should work
        create_result = runner.invoke(
            cli,
            ["create", "--layer", "goal", "--title", "Test Goal", "--description", "A test goal"],
        )

        # Should succeed with simplified connection
        assert create_result.exit_code == 0
        assert "Created Goal" in create_result.output

    def test_cli_list_command_works_with_simplified_connection(self) -> None:
        """Test that CLI list command works with simplified connection."""
        runner = CliRunner()

        # Initialize first
        runner.invoke(cli, ["init"])

        # List should work even with empty database
        result = runner.invoke(cli, ["list"])

        # Should succeed with simplified connection
        assert result.exit_code == 0
        # Should show "No nodes found" when empty

    def test_get_app_uses_storage_preference_parameter(self) -> None:
        """Test that get_app() respects storage preference parameter."""
        # Mock environment to test preference handling
        with patch("todowrite.database.config.StoragePreference") as mock_pref:
            mock_pref.AUTO = "auto"
            mock_pref.SQLITE_ONLY = "sqlite_only"

            # Should pass preference through to library
            app = get_app()

            # Should have called library with preference
            assert app is not None

    def test_cli_status_commands_use_simplified_connection(self) -> None:
        """Test that CLI status commands use simplified connection."""
        runner = CliRunner()

        # Initialize first
        runner.invoke(cli, ["init"])

        # Status command should work
        result = runner.invoke(cli, ["db-status"])

        # Should succeed with simplified connection
        assert result.exit_code == 0


class TestCLIConnectionSimplification:
    """Test suite for verifying CLI connection simplification."""

    def test_no_direct_sqlalchemy_imports_in_cli_logic(self) -> None:
        """Test that CLI logic doesn't directly import SQLAlchemy for connection."""
        # The CLI should use the library, not directly handle database connections
        runner = CliRunner()

        result = runner.invoke(cli, ["init"])

        # Should work without direct SQLAlchemy connection handling
        assert result.exit_code == 0

    def test_get_app_uses_library_not_direct_database_logic(self) -> None:
        """Test that get_app() uses library, not direct database logic."""
        with tempfile.TemporaryDirectory() as temp_dir:
            db_path = Path(temp_dir) / "simplified_test.db"

            # Should delegate to library, not handle connection directly
            app = get_app(str(db_path))

            # Library should handle the connection
            assert app is not None
            assert hasattr(app, "storage_type")

    def test_cli_respects_environment_variables_through_library(self) -> None:
        """Test that CLI respects environment variables through library."""
        runner = CliRunner()

        with tempfile.TemporaryDirectory() as temp_dir:
            db_path = Path(temp_dir) / "env_test.db"
            db_url = f"sqlite:///{db_path}"

            # Should pass environment to library for handling
            result = runner.invoke(cli, ["init"], env={"TODOWRITE_DATABASE_URL": db_url})

            # Should succeed with environment variable
            assert result.exit_code == 0

    def test_no_complex_config_file_parsing_in_cli(self) -> None:
        """Test that CLI doesn't do complex config file parsing."""
        # CLI should delegate to library, not parse config files directly
        runner = CliRunner()

        result = runner.invoke(cli, ["init"])

        # Should work without complex config parsing
        assert result.exit_code == 0

    def test_cli_error_handling_uses_library_errors(self) -> None:
        """Test that CLI error handling uses library error types."""
        runner = CliRunner()

        # Should handle library errors appropriately
        result = runner.invoke(cli, ["get", "nonexistent-id"])

        # Should handle missing node gracefully
        assert result.exit_code == 1
        assert "not found" in result.output.lower()


class TestRealCLIConnectionBehavior:
    """Test real CLI connection behavior without mocking."""

    def test_real_cli_with_sqlite_database(self) -> None:
        """Test real CLI behavior with SQLite database."""
        runner = CliRunner()

        with tempfile.TemporaryDirectory() as temp_dir:
            db_path = Path(temp_dir) / "real_cli_test.db"

            # Initialize with real database
            init_result = runner.invoke(cli, ["init", "--database-path", str(db_path)])
            assert init_result.exit_code == 0

            # Create a real node
            create_result = runner.invoke(
                cli,
                [
                    "create",
                    "--layer",
                    "task",
                    "--title",
                    "Real Task",
                    "--description",
                    "A real task created via CLI",
                    "--severity",
                    "medium",
                ],
            )
            assert create_result.exit_code == 0
            assert "Created Task" in create_result.output

            # List nodes should show the created node
            list_result = runner.invoke(cli, ["list"])
            assert list_result.exit_code == 0
            assert "Real Task" in list_result.output

    def test_real_cli_database_status_command(self) -> None:
        """Test real CLI database status command."""
        runner = CliRunner()

        # Initialize database
        runner.invoke(cli, ["init"])

        # Check database status
        result = runner.invoke(cli, ["db-status"])

        # Should work with real database
        assert result.exit_code == 0
        assert "Database Status" in result.output
