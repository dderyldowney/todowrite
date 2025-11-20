"""Tests for CLI using current ToDoWrite Models API."""

from __future__ import annotations

import os
import tempfile
import unittest
from pathlib import Path

from click.testing import CliRunner

from cli_package.src.todowrite_cli.main import cli


class TestCLI(unittest.TestCase):
    """Test CLI functionality with current API."""

    def setUp(self) -> None:
        """Set up test environment."""
        self.runner = CliRunner()
        # Use a temporary database for testing
        self.temp_db = tempfile.NamedTemporaryFile(suffix=".db", delete=False)
        self.temp_db.close()
        self.db_url = f"sqlite:///{self.temp_db.name}"
        os.environ["TODOWRITE_DATABASE_URL"] = self.db_url

    def tearDown(self) -> None:
        """Clean up test environment."""
        # Clean up temporary database
        if hasattr(self, "temp_db") and Path(self.temp_db.name).exists():
            Path(self.temp_db.name).unlink()

    def test_list_command(self) -> None:
        """Test the list command."""
        result = self.runner.invoke(cli, ["list"])
        self.assertEqual(result.exit_code, 0)
        self.assertIn("ToDoWrite Items", result.output)

    def test_list_with_layer(self) -> None:
        """Test listing items with layer filter."""
        result = self.runner.invoke(cli, ["list", "--layer", "goal"])
        self.assertEqual(result.exit_code, 0)

    def test_list_with_limit(self) -> None:
        """Test listing items with limit."""
        result = self.runner.invoke(cli, ["list", "--limit", "5"])
        self.assertEqual(result.exit_code, 0)

    def test_help_command(self) -> None:
        """Test the help command."""
        result = self.runner.invoke(cli, ["--help"])
        self.assertEqual(result.exit_code, 0)
        self.assertIn("ToDoWrite CLI", result.output)


if __name__ == "__main__":
    unittest.main()
