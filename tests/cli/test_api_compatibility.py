"""Tests for CLI API compatibility with new ToDoWrite Models.

These tests ensure that the CLI commands work correctly with the new
ToDoWrite Models API instead of the old Node-based functions.
Each test gets its own isolated database for proper test isolation.
"""

from __future__ import annotations

import tempfile
from pathlib import Path
from unittest import TestCase

from click.testing import CliRunner
from sqlalchemy import create_engine
from todowrite.core.models import Base
from todowrite_cli.main import cli


class TestCLIAPICompatibility(TestCase):
    """Test CLI API compatibility with ToDoWrite Models."""

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

    def test_cli_init_command(self) -> None:
        """Test that init command works with new Models API."""
        test_db_path = self._create_test_database()

        try:
            with self.runner.isolated_filesystem():
                result = self.runner.invoke(cli, ["--database", test_db_path, "init"])

                # Should succeed
                self.assertEqual(result.exit_code, 0)
                self.assertIn("Database initialized", result.output)
        finally:
            self._cleanup_test_database(test_db_path)

    def test_cli_list_command_empty_database(self) -> None:
        """Test that list command works with empty database."""
        test_db_path = self._create_test_database()

        try:
            result = self.runner.invoke(cli, ["--database", test_db_path, "list"])

            # Should succeed even with empty database
            self.assertEqual(result.exit_code, 0)
            self.assertIn("No items found", result.output)
        finally:
            self._cleanup_test_database(test_db_path)

    def test_cli_create_goal_command(self) -> None:
        """Test that create command works for goals."""
        test_db_path = self._create_test_database()

        try:
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
                    "--description",
                    "A test goal for CLI testing",
                    "--owner",
                    "test-user",
                    "--severity",
                    "high",
                ],
            )

            # Should succeed
            self.assertEqual(result.exit_code, 0)
            self.assertIn("Created Goal 'Test Goal'", result.output)
        finally:
            self._cleanup_test_database(test_db_path)

    def test_cli_create_task_command(self) -> None:
        """Test that create command works for tasks."""
        test_db_path = self._create_test_database()

        try:
            result = self.runner.invoke(
                cli,
                [
                    "--database",
                    test_db_path,
                    "create",
                    "--layer",
                    "task",
                    "--title",
                    "Test Task",
                    "--description",
                    "A test task for CLI testing",
                    "--owner",
                    "test-user",
                    "--status",
                    "in_progress",
                    "--progress",
                    "50",
                ],
            )

            # Should succeed
            self.assertEqual(result.exit_code, 0)
            self.assertIn("Created Task 'Test Task'", result.output)
        finally:
            self._cleanup_test_database(test_db_path)

    def test_cli_create_command_with_cmd(self) -> None:
        """Test that create command works for commands with cmd field."""
        test_db_path = self._create_test_database()

        try:
            result = self.runner.invoke(
                cli,
                [
                    "--database",
                    test_db_path,
                    "create",
                    "--layer",
                    "command",
                    "--title",
                    "Test Command",
                    "--description",
                    "A test command for CLI testing",
                    "--owner",
                    "test-user",
                    "--run-command",
                    "echo 'Hello World'",
                    "--status",
                    "planned",
                ],
            )

            # Should succeed and store command in cmd field
            self.assertEqual(result.exit_code, 0)
            self.assertIn("Created Command 'Test Command'", result.output)
        finally:
            self._cleanup_test_database(test_db_path)

    def test_cli_list_command_with_data(self) -> None:
        """Test list command with actual data."""
        test_db_path = self._create_test_database()

        try:
            # First create some data
            self.runner.invoke(
                cli,
                [
                    "--database",
                    test_db_path,
                    "create",
                    "--layer",
                    "goal",
                    "--title",
                    "Test Goal 1",
                    "--owner",
                    "user1",
                ],
            )

            self.runner.invoke(
                cli,
                [
                    "--database",
                    test_db_path,
                    "create",
                    "--layer",
                    "task",
                    "--title",
                    "Test Task 1",
                    "--owner",
                    "user1",
                    "--status",
                    "planned",
                ],
            )

            # Now list items
            result = self.runner.invoke(cli, ["--database", test_db_path, "list"])

            # Should show items
            self.assertEqual(result.exit_code, 0)
            self.assertIn("Test Goal 1", result.output)
            self.assertIn("Test Task 1", result.output)
            self.assertIn("Total:", result.output)
        finally:
            self._cleanup_test_database(test_db_path)

    def test_cli_list_with_layer_filter(self) -> None:
        """Test list command with layer filtering."""
        test_db_path = self._create_test_database()

        try:
            # Create different types of items
            self.runner.invoke(
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
                    "user1",
                ],
            )

            self.runner.invoke(
                cli,
                [
                    "--database",
                    test_db_path,
                    "create",
                    "--layer",
                    "task",
                    "--title",
                    "Test Task",
                    "--owner",
                    "user1",
                ],
            )

            # List only goals
            result = self.runner.invoke(
                cli, ["--database", test_db_path, "list", "--layer", "goal"]
            )

            # Should show only goals
            self.assertEqual(result.exit_code, 0)
            self.assertIn("Test Goal", result.output)
            self.assertNotIn("Test Task", result.output)
        finally:
            self._cleanup_test_database(test_db_path)

    def test_cli_get_command(self) -> None:
        """Test get command for specific item."""
        test_db_path = self._create_test_database()

        try:
            # Create a goal
            create_result = self.runner.invoke(
                cli,
                [
                    "--database",
                    test_db_path,
                    "create",
                    "--layer",
                    "goal",
                    "--title",
                    "Test Goal for Get",
                    "--owner",
                    "test-user",
                    "--description",
                    "Goal for testing get command",
                ],
            )

            # Extract ID from output (format: "Created Goal 'title' with ID X")
            output_lines = create_result.output.strip().split("\n")
            created_line = next(line for line in output_lines if "with ID" in line)
            item_id = int(created_line.split("with ID")[1].strip())

            # Get the item
            result = self.runner.invoke(cli, ["--database", test_db_path, "get", str(item_id)])

            # Should show item details
            self.assertEqual(result.exit_code, 0)
            self.assertIn("Goal Details", result.output)
            self.assertIn("Test Goal for Get", result.output)
            self.assertIn("test-user", result.output)
        finally:
            self._cleanup_test_database(test_db_path)

    def test_cli_search_command(self) -> None:
        """Test search command."""
        test_db_path = self._create_test_database()

        try:
            # Create some data
            self.runner.invoke(
                cli,
                [
                    "--database",
                    test_db_path,
                    "create",
                    "--layer",
                    "goal",
                    "--title",
                    "Important Goal",
                    "--description",
                    "This is about authentication",
                    "--owner",
                    "security-team",
                ],
            )

            self.runner.invoke(
                cli,
                [
                    "--database",
                    test_db_path,
                    "create",
                    "--layer",
                    "task",
                    "--title",
                    "Regular Task",
                    "--description",
                    "This is about UI design",
                    "--owner",
                    "design-team",
                ],
            )

            # Search for "authentication"
            result = self.runner.invoke(
                cli, ["--database", test_db_path, "search", "authentication"]
            )

            # Should find the goal
            self.assertEqual(result.exit_code, 0)
            self.assertIn("Important Goal", result.output)
            self.assertNotIn("Regular Task", result.output)
        finally:
            self._cleanup_test_database(test_db_path)

    def test_cli_search_with_layer_filter(self) -> None:
        """Test search command with layer filtering."""
        test_db_path = self._create_test_database()

        try:
            # Create different types with similar content
            self.runner.invoke(
                cli,
                [
                    "--database",
                    test_db_path,
                    "create",
                    "--layer",
                    "goal",
                    "--title",
                    "Authentication Goal",
                    "--description",
                    "User authentication project",
                ],
            )

            self.runner.invoke(
                cli,
                [
                    "--database",
                    test_db_path,
                    "create",
                    "--layer",
                    "task",
                    "--title",
                    "Authentication Task",
                    "--description",
                    "Implement user authentication",
                ],
            )

            # Search only in tasks
            result = self.runner.invoke(
                cli, ["--database", test_db_path, "search", "authentication", "--layer", "task"]
            )

            # Should find only the task
            self.assertEqual(result.exit_code, 0)
            self.assertIn("Authentication Task", result.output)
            self.assertNotIn("Authentication Goal", result.output)
        finally:
            self._cleanup_test_database(test_db_path)

    def test_cli_stats_command(self) -> None:
        """Test stats command."""
        test_db_path = self._create_test_database()

        try:
            # Create some data
            self.runner.invoke(
                cli, ["--database", test_db_path, "create", "--layer", "goal", "--title", "Goal 1"]
            )

            self.runner.invoke(
                cli, ["--database", test_db_path, "create", "--layer", "task", "--title", "Task 1"]
            )

            self.runner.invoke(
                cli, ["--database", test_db_path, "create", "--layer", "task", "--title", "Task 2"]
            )

            # Get stats
            result = self.runner.invoke(cli, ["--database", test_db_path, "stats"])

            # Should show statistics
            self.assertEqual(result.exit_code, 0)
            self.assertIn("Statistics", result.output)
            self.assertIn("Goal", result.output)
            self.assertIn("Task", result.output)
            self.assertIn("TOTAL", result.output)
        finally:
            self._cleanup_test_database(test_db_path)

    def test_cli_multiple_item_creation(self) -> None:
        """Test creating multiple items of different types in sequence."""
        test_db_path = self._create_test_database()

        try:
            # Create multiple items
            items_created = []

            # Create goals
            for i in range(3):
                result = self.runner.invoke(
                    cli,
                    [
                        "--database",
                        test_db_path,
                        "create",
                        "--layer",
                        "goal",
                        "--title",
                        f"Goal {i + 1}",
                        "--owner",
                        f"user{i + 1}",
                    ],
                )
                self.assertEqual(result.exit_code, 0)
                items_created.append(f"Goal {i + 1}")

            # Create tasks
            for i in range(2):
                result = self.runner.invoke(
                    cli,
                    [
                        "--database",
                        test_db_path,
                        "create",
                        "--layer",
                        "task",
                        "--title",
                        f"Task {i + 1}",
                        "--owner",
                        "task-user{i+1}",
                        "--status",
                        "planned",
                    ],
                )
                self.assertEqual(result.exit_code, 0)
                items_created.append(f"Task {i + 1}")

            # Create a command
            result = self.runner.invoke(
                cli,
                [
                    "--database",
                    test_db_path,
                    "create",
                    "--layer",
                    "command",
                    "--title",
                    "Deploy Command",
                    "--owner",
                    "deploy-user",
                    "--run-command",
                    "kubectl apply -f .",
                ],
            )
            self.assertEqual(result.exit_code, 0)
            items_created.append("Deploy Command")

            # Verify all items exist in list
            list_result = self.runner.invoke(cli, ["--database", test_db_path, "list"])
            self.assertEqual(list_result.exit_code, 0)

            for item_name in items_created:
                self.assertIn(item_name, list_result.output)

            # Verify stats show correct counts
            stats_result = self.runner.invoke(cli, ["--database", test_db_path, "stats"])
            self.assertEqual(stats_result.exit_code, 0)
            self.assertIn("TOTAL", stats_result.output)

        finally:
            self._cleanup_test_database(test_db_path)

    def test_cli_invalid_layer(self) -> None:
        """Test CLI with invalid layer type."""
        test_db_path = self._create_test_database()

        try:
            result = self.runner.invoke(
                cli,
                [
                    "--database",
                    test_db_path,
                    "create",
                    "--layer",
                    "invalid_layer",
                    "--title",
                    "Test",
                ],
            )

            # Should fail
            self.assertNotEqual(result.exit_code, 0)
            self.assertIn("Invalid value for '--layer'", result.output)
        finally:
            self._cleanup_test_database(test_db_path)

    def test_cli_get_nonexistent_item(self) -> None:
        """Test get command with non-existent item ID."""
        test_db_path = self._create_test_database()

        try:
            result = self.runner.invoke(cli, ["--database", test_db_path, "get", "99999"])

            # Should handle gracefully
            self.assertEqual(result.exit_code, 0)
            self.assertIn("not found", result.output)
        finally:
            self._cleanup_test_database(test_db_path)

    def test_cli_search_no_results(self) -> None:
        """Test search command with no matching results."""
        test_db_path = self._create_test_database()

        try:
            result = self.runner.invoke(
                cli, ["--database", test_db_path, "search", "nonexistent_term"]
            )

            # Should handle gracefully
            self.assertEqual(result.exit_code, 0)
            self.assertIn("No items found", result.output)
        finally:
            self._cleanup_test_database(test_db_path)

    def test_database_file_isolation(self) -> None:
        """Test that different tests use completely isolated databases."""
        test_db_path = self._create_test_database()

        try:
            # Create data in this database
            self.runner.invoke(
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

            # Verify data exists
            result = self.runner.invoke(cli, ["--database", test_db_path, "list"])
            self.assertEqual(result.exit_code, 0)
            self.assertIn("Isolation Test Goal", result.output)

            # Verify database file actually exists
            db_file = Path(test_db_path)
            self.assertTrue(db_file.exists())

            # Verify database has content (file size > 0)
            self.assertGreater(db_file.stat().st_size, 0)

        finally:
            # Cleanup and verify file is removed
            self._cleanup_test_database(test_db_path)
            db_file = Path(test_db_path)
            self.assertFalse(db_file.exists(), "Database file should be cleaned up")
