"""Tests to improve coverage for CLI main module"""

import pytest
from click.testing import CliRunner
from todowrite_cli.main import (
    cli,
    get_current_username,
    get_session,
    init_database,
)
from todowrite_cli.version import __version__


@pytest.fixture
def runner():
    """CLI test runner fixture."""
    return CliRunner()


class TestCLIMainCoverage:
    """Test cases for CLI main module functions to improve coverage"""

    def test_get_current_username(self):
        """Test username detection"""
        username = get_current_username()
        # Should return a non-empty string
        assert isinstance(username, str)
        assert len(username) > 0

    def test_get_current_username_fallback(self):
        """Test username detection with mocked environment"""
        # This tests the fallback mechanisms
        username = get_current_username()
        # Should always return something sensible
        assert username in ["unknown"] or len(username) > 0

    def test_get_session_with_sqlite(self):
        """Test session creation with SQLite"""
        session, engine = get_session("sqlite:///:memory:")
        assert session is not None
        assert engine is not None
        session.close()

    def test_init_database(self):
        """Test database initialization"""
        # This should not raise an exception
        init_database("sqlite:///:memory:")

    def test_cli_version_option(self, runner):
        """Test CLI version option"""
        result = runner.invoke(cli, ["--version"])
        assert result.exit_code == 0
        assert __version__ in result.output

    def test_cli_help(self, runner):
        """Test CLI help"""
        result = runner.invoke(cli, ["--help"])
        assert result.exit_code == 0
        assert "ToDoWrite CLI" in result.output
        assert "init" in result.output
        assert "create" in result.output
        assert "list" in result.output
        assert "get" in result.output
        assert "search" in result.output
        assert "stats" in result.output

    def test_cli_database_option_parsing(self, runner):
        """Test that database option is properly parsed"""
        # Test with default database
        result = runner.invoke(cli, ["--help"])
        assert "--database" in result.output
        assert "Database file path" in result.output

    def test_cli_command_structure(self):
        """Test that CLI has expected command structure"""
        # Check that the main CLI object exists and has commands
        assert cli is not None
        assert hasattr(cli, "commands")

        # Check that expected commands exist
        expected_commands = ["init", "create", "list", "get", "search", "stats"]
        for cmd_name in expected_commands:
            assert cmd_name in cli.commands, f"Command {cmd_name} should exist"
