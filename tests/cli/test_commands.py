"""
CLI Command Tests

Comprehensive tests for CLI commands, options, error handling, and edge cases.
"""

import os
import shutil
import tempfile
import unittest
from pathlib import Path

from click.testing import CliRunner

from cli_package.todowrite_cli.main import main as todowrite_cli


class TestCLICommands(unittest.TestCase):
    """Test individual CLI commands and their options."""

    def setUp(self) -> None:
        """Set up test environment."""
        self.runner = CliRunner()
        self.temp_dir = tempfile.mkdtemp()
        self.original_cwd = os.getcwd()

    def tearDown(self) -> None:
        """Clean up test environment."""
        os.chdir(self.original_cwd)
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_init_command_basic(self) -> None:
        """Test basic init command."""
        os.chdir(self.temp_dir)
        result = self.runner.invoke(todowrite_cli, ["init"])
        self.assertEqual(result.exit_code, 0)
        self.assertIn("Database initialized", result.output)

        # Check if database file was created
        db_files = list(Path(self.temp_dir).glob("*.db"))
        self.assertTrue(len(db_files) > 0)

    def test_init_with_storage_preference(self) -> None:
        """Test init command with storage preference."""
        os.chdir(self.temp_dir)

        # Test different storage preferences
        for storage in ["postgresql_only", "sqlite_only", "yaml_only"]:
            # Clean up previous
            for f in Path(self.temp_dir).glob("*.db"):
                f.unlink()

            result = self.runner.invoke(
                todowrite_cli, ["--storage-preference", storage, "init"]
            )
            self.assertEqual(result.exit_code, 0)
            self.assertIn("Database initialized", result.output)

    def test_init_duplicate(self) -> None:
        """Test init command on existing database."""
        os.chdir(self.temp_dir)
        self.runner.invoke(todowrite_cli, ["init"])

        # Run init again
        result = self.runner.invoke(todowrite_cli, ["init"])
        self.assertEqual(result.exit_code, 0)
        self.assertIn("Database initialized", result.output)

    def test_create_node_basic(self) -> None:
        """Test basic node creation."""
        os.chdir(self.temp_dir)
        self.runner.invoke(todowrite_cli, ["init"])

        result = self.runner.invoke(
            todowrite_cli, ["create", "Goal", "Test Goal", "Test goal description"]
        )
        self.assertEqual(result.exit_code, 0)
        self.assertIn("Node created:", result.output)

        # Extract node ID
        node_id = result.output.split("Node created: ")[1].strip()
        self.assertTrue(node_id.startswith("GOAL-"))

    def test_create_node_with_options(self) -> None:
        """Test node creation with various options."""
        os.chdir(self.temp_dir)
        self.runner.invoke(todowrite_cli, ["init"])

        result = self.runner.invoke(
            todowrite_cli,
            [
                "create",
                "Task",
                "Test Task",
                "Test task description",
                "--owner",
                "developer1",
                "--assignee",
                "developer2",
                "--severity",
                "high",
                "--work-type",
                "implementation",
                "--labels",
                "urgent,important",
                "--progress",
                "50",
            ],
        )
        self.assertEqual(result.exit_code, 0)
        self.assertIn("Node created:", result.output)

    def test_create_node_invalid_layer(self) -> None:
        """Test creating node with invalid layer."""
        os.chdir(self.temp_dir)
        self.runner.invoke(todowrite_cli, ["init"])

        result = self.runner.invoke(
            todowrite_cli, ["create", "InvalidLayer", "Test Node", "Test description"]
        )
        self.assertNotEqual(result.exit_code, 0)
        self.assertIn("Invalid layer", result.output)

    def test_create_node_missing_required_fields(self) -> None:
        """Test creating node with missing required fields."""
        os.chdir(self.temp_dir)
        self.runner.invoke(todowrite_cli, ["init"])

        # Missing title
        result = self.runner.invoke(
            todowrite_cli, ["create", "Goal", "", "Test description"]
        )
        self.assertNotEqual(result.exit_code, 0)

    def test_get_node_success(self) -> None:
        """Test successful node retrieval."""
        os.chdir(self.temp_dir)
        self.runner.invoke(todowrite_cli, ["init"])

        # Create node
        create_result = self.runner.invoke(
            todowrite_cli, ["create", "Goal", "Test Goal", "Test description"]
        )
        node_id = create_result.output.split("Node created: ")[1].strip()

        # Get node
        result = self.runner.invoke(todowrite_cli, ["get", node_id])
        self.assertEqual(result.exit_code, 0)
        self.assertIn(f"ID: {node_id}", result.output)
        self.assertIn("Test Goal", result.output)

    def test_get_node_not_found(self) -> None:
        """Test retrieving non-existent node."""
        os.chdir(self.temp_dir)
        self.runner.invoke(todowrite_cli, ["init"])

        result = self.runner.invoke(todowrite_cli, ["get", "NONEXISTENT"])
        self.assertNotEqual(result.exit_code, 0)
        self.assertIn("not found", result.output)

    def test_update_node_basic(self) -> None:
        """Test basic node update."""
        os.chdir(self.temp_dir)
        self.runner.invoke(todowrite_cli, ["init"])

        # Create node
        create_result = self.runner.invoke(
            todowrite_cli, ["create", "Task", "Original Task", "Original description"]
        )
        node_id = create_result.output.split("Node created: ")[1].strip()

        # Update node
        result = self.runner.invoke(
            todowrite_cli,
            [
                "update",
                node_id,
                "--title",
                "Updated Task",
                "--description",
                "Updated description",
                "--status",
                "in_progress",
                "--progress",
                "75",
            ],
        )
        self.assertEqual(result.exit_code, 0)
        self.assertIn(f"Updated {node_id}", result.output)
        self.assertIn("in_progress", result.output)
        self.assertIn("75%", result.output)

    def test_update_node_status_only(self) -> None:
        """Test updating only node status."""
        os.chdir(self.temp_dir)
        self.runner.invoke(todowrite_cli, ["init"])

        # Create node
        create_result = self.runner.invoke(
            todowrite_cli, ["create", "Goal", "Test Goal", "Test description"]
        )
        node_id = create_result.output.split("Node created: ")[1].strip()

        # Update only status
        result = self.runner.invoke(
            todowrite_cli, ["update", node_id, "--status", "completed"]
        )
        self.assertEqual(result.exit_code, 0)
        self.assertIn("completed", result.output)

    def test_update_node_invalid_status(self) -> None:
        """Test updating with invalid status."""
        os.chdir(self.temp_dir)
        self.runner.invoke(todowrite_cli, ["init"])

        # Create node
        create_result = self.runner.invoke(
            todowrite_cli, ["create", "Goal", "Test Goal", "Test description"]
        )
        node_id = create_result.output.split("Node created: ")[1].strip()

        # Update with invalid status
        result = self.runner.invoke(
            todowrite_cli, ["update", node_id, "--status", "invalid_status"]
        )
        self.assertNotEqual(result.exit_code, 0)

    def test_delete_node_success(self) -> None:
        """Test successful node deletion."""
        os.chdir(self.temp_dir)
        self.runner.invoke(todowrite_cli, ["init"])

        # Create node
        create_result = self.runner.invoke(
            todowrite_cli, ["create", "Task", "Task to Delete", "Description"]
        )
        node_id = create_result.output.split("Node created: ")[1].strip()

        # Delete node
        result = self.runner.invoke(todowrite_cli, ["delete", node_id])
        self.assertEqual(result.exit_code, 0)
        self.assertIn(f"Deleted {node_id}", result.output)

        # Verify node is gone
        get_result = self.runner.invoke(todowrite_cli, ["get", node_id])
        self.assertNotEqual(get_result.exit_code, 0)

    def test_delete_node_not_found(self) -> None:
        """Test deleting non-existent node."""
        os.chdir(self.temp_dir)
        self.runner.invoke(todowrite_cli, ["init"])

        result = self.runner.invoke(todowrite_cli, ["delete", "NONEXISTENT"])
        self.assertNotEqual(result.exit_code, 0)
        self.assertIn("not found", result.output)

    def test_list_all_nodes(self) -> None:
        """Test listing all nodes."""
        os.chdir(self.temp_dir)
        self.runner.invoke(todowrite_cli, ["init"])

        # Create multiple nodes
        nodes_data = [
            ("Goal", "Goal 1", "First goal"),
            ("Task", "Task 1", "First task"),
            ("Concept", "Concept 1", "First concept"),
        ]

        for layer, title, description in nodes_data:
            self.runner.invoke(todowrite_cli, ["create", layer, title, description])

        # List all nodes
        result = self.runner.invoke(todowrite_cli, ["list"])
        self.assertEqual(result.exit_code, 0)
        self.assertIn("--- Goal ---", result.output)
        self.assertIn("--- Task ---", result.output)
        self.assertIn("--- Concept ---", result.output)

    def test_list_by_layer(self) -> None:
        """Test listing nodes by layer."""
        os.chdir(self.temp_dir)
        self.runner.invoke(todowrite_cli, ["init"])

        # Create multiple nodes
        self.runner.invoke(todowrite_cli, ["create", "Goal", "Goal 1", "First goal"])
        self.runner.invoke(todowrite_cli, ["create", "Goal", "Goal 2", "Second goal"])
        self.runner.invoke(todowrite_cli, ["create", "Task", "Task 1", "First task"])

        # List only goals
        result = self.runner.invoke(todowrite_cli, ["list", "--layer", "Goal"])
        self.assertEqual(result.exit_code, 0)
        self.assertIn("--- Goal ---", result.output)
        self.assertNotIn("--- Task ---", result.output)

    def test_list_by_owner(self) -> None:
        """Test listing nodes by owner."""
        os.chdir(self.temp_dir)
        self.runner.invoke(todowrite_cli, ["init"])

        # Create nodes with different owners
        self.runner.invoke(
            todowrite_cli,
            ["create", "Task", "Task 1", "Description", "--owner", "developer1"],
        )
        self.runner.invoke(
            todowrite_cli,
            ["create", "Task", "Task 2", "Description", "--owner", "developer2"],
        )

        # List by owner
        result = self.runner.invoke(todowrite_cli, ["list", "--owner", "developer1"])
        self.assertEqual(result.exit_code, 0)
        self.assertIn("Task 1", result.output)
        self.assertNotIn("Task 2", result.output)

    def test_status_update_command(self) -> None:
        """Test status update subcommand."""
        os.chdir(self.temp_dir)
        self.runner.invoke(todowrite_cli, ["init"])

        # Create node
        create_result = self.runner.invoke(
            todowrite_cli, ["create", "Task", "Test Task", "Description"]
        )
        node_id = create_result.output.split("Node created: ")[1].strip()

        # Update status
        result = self.runner.invoke(
            todowrite_cli,
            [
                "status",
                "update",
                node_id,
                "--status",
                "in_progress",
                "--progress",
                "50",
            ],
        )
        self.assertEqual(result.exit_code, 0)
        self.assertIn("in_progress", result.output)
        self.assertIn("50%", result.output)

    def test_status_show_command(self) -> None:
        """Test status show subcommand."""
        os.chdir(self.temp_dir)
        self.runner.invoke(todowrite_cli, ["init"])

        # Create node with progress
        create_result = self.runner.invoke(
            todowrite_cli,
            ["create", "Task", "Test Task", "Description", "--progress", "75"],
        )
        node_id = create_result.output.split("Node created: ")[1].strip()

        # Show status
        result = self.runner.invoke(todowrite_cli, ["status", "show", node_id])
        self.assertEqual(result.exit_code, 0)
        self.assertIn("Node: ", result.output)
        self.assertIn("Status:", result.output)
        self.assertIn("Progress:", result.output)

    def test_status_complete_command(self) -> None:
        """Test status complete subcommand."""
        os.chdir(self.temp_dir)
        self.runner.invoke(todowrite_cli, ["init"])

        # Create node
        create_result = self.runner.invoke(
            todowrite_cli, ["create", "Task", "Test Task", "Description"]
        )
        node_id = create_result.output.split("Node created: ")[1].strip()

        # Complete node
        result = self.runner.invoke(
            todowrite_cli,
            ["status", "complete", node_id, "--message", "Task completed successfully"],
        )
        self.assertEqual(result.exit_code, 0)
        self.assertIn("completed", result.output)
        self.assertIn("Task completed successfully", result.output)

    def test_status_complete_already_completed(self) -> None:
        """Test completing already completed node."""
        os.chdir(self.temp_dir)
        self.runner.invoke(todowrite_cli, ["init"])

        # Create and complete node
        create_result = self.runner.invoke(
            todowrite_cli, ["create", "Task", "Test Task", "Description"]
        )
        node_id = create_result.output.split("Node created: ")[1].strip()

        self.runner.invoke(todowrite_cli, ["status", "complete", node_id])

        # Try to complete again
        result = self.runner.invoke(todowrite_cli, ["status", "complete", node_id])
        self.assertEqual(result.exit_code, 0)
        self.assertIn("already completed", result.output)

    def test_help_commands(self) -> None:
        """Test help commands."""
        os.chdir(self.temp_dir)

        # Main help
        result = self.runner.invoke(todowrite_cli, ["--help"])
        self.assertEqual(result.exit_code, 0)
        self.assertIn("Usage:", result.output)
        self.assertIn("Commands:", result.output)

        # Command-specific help
        result = self.runner.invoke(todowrite_cli, ["create", "--help"])
        self.assertEqual(result.exit_code, 0)
        self.assertIn("Creates a new node", result.output)

        # Subcommand help
        result = self.runner.invoke(todowrite_cli, ["status", "--help"])
        self.assertEqual(result.exit_code, 0)
        self.assertIn("Status management", result.output)

        result = self.runner.invoke(todowrite_cli, ["status", "update", "--help"])
        self.assertEqual(result.exit_code, 0)
        self.assertIn("Update node status", result.output)

    def test_db_status_command(self) -> None:
        """Test database status command."""
        os.chdir(self.temp_dir)
        self.runner.invoke(todowrite_cli, ["init"])

        result = self.runner.invoke(todowrite_cli, ["db-status"])
        self.assertEqual(result.exit_code, 0)
        self.assertIn("Storage", result.output)
        self.assertIn("Database", result.output)

    def test_export_yaml_command(self) -> None:
        """Test YAML export command."""
        os.chdir(self.temp_dir)
        self.runner.invoke(todowrite_cli, ["init"])

        # Create some nodes
        self.runner.invoke(
            todowrite_cli, ["create", "Goal", "Test Goal", "Description"]
        )

        # Export to YAML
        result = self.runner.invoke(todowrite_cli, ["export-yaml"])
        self.assertEqual(result.exit_code, 0)
        self.assertIn("Exported", result.output)

        # Check if files were created
        configs_dir = Path(self.temp_dir) / "configs"
        if configs_dir.exists():
            yaml_files = list(configs_dir.rglob("*.yaml"))
            self.assertTrue(len(yaml_files) > 0)

    def test_export_yaml_with_options(self) -> None:
        """Test YAML export with options."""
        os.chdir(self.temp_dir)
        self.runner.invoke(todowrite_cli, ["init"])

        # Create some nodes
        self.runner.invoke(
            todowrite_cli, ["create", "Goal", "Test Goal", "Description"]
        )

        # Export with custom output dir and no backup
        output_dir = self.temp_dir / "custom_output"
        result = self.runner.invoke(
            todowrite_cli,
            ["export-yaml", "--output-dir", str(output_dir), "--no-backup"],
        )
        self.assertEqual(result.exit_code, 0)
        self.assertIn("Exported", result.output)

        # Check if files were created in custom directory
        self.assertTrue(output_dir.exists())

    def test_import_yaml_command(self) -> None:
        """Test YAML import command."""
        os.chdir(self.temp_dir)
        self.runner.invoke(todowrite_cli, ["init"])

        # Create a test YAML file
        configs_dir = Path(self.temp_dir) / "configs"
        configs_dir.mkdir(parents=True)

        goals_dir = configs_dir / "plans" / "goals"
        goals_dir.mkdir(parents=True)

        yaml_file = goals_dir / "test_goal.yaml"
        yaml_content = """
id: GOAL-001
layer: Goal
title: Imported Goal
description: Goal imported from YAML
links:
  parents: []
  children: []
metadata:
  owner: importer
  labels: []
  severity: medium
  work_type: architecture
"""

        with open(yaml_file, "w") as f:
            f.write(yaml_content)

        # Import YAML
        result = self.runner.invoke(todowrite_cli, ["import-yaml"])
        self.assertEqual(result.exit_code, 0)
        self.assertIn("Importing YAML files", result.output)

    def test_import_yaml_with_options(self) -> None:
        """Test YAML import with options."""
        os.chdir(self.temp_dir)
        self.runner.invoke(todowrite_cli, ["init"])

        # Create a test YAML file
        configs_dir = Path(self.temp_dir) / "configs"
        configs_dir.mkdir(parents=True)

        goals_dir = configs_dir / "plans" / "goals"
        goals_dir.mkdir(parents=True)

        yaml_file = goals_dir / "test_goal.yaml"
        yaml_content = """
id: GOAL-001
layer: Goal
title: Imported Goal
description: Goal imported from YAML
links:
  parents: []
  children: []
metadata:
  owner: importer
  labels: []
  severity: medium
  work_type: architecture
"""

        with open(yaml_file, "w") as f:
            f.write(yaml_content)

        # Import with dry run
        result = self.runner.invoke(todowrite_cli, ["import-yaml", "--dry-run"])
        self.assertEqual(result.exit_code, 0)
        self.assertIn("DRY RUN", result.output)

    def test_sync_status_command(self) -> None:
        """Test sync status command."""
        os.chdir(self.temp_dir)
        self.runner.invoke(todowrite_cli, ["init"])

        # Create some nodes
        self.runner.invoke(
            todowrite_cli, ["create", "Goal", "Test Goal", "Description"]
        )

        # Check sync status
        result = self.runner.invoke(todowrite_cli, ["sync-status"])
        self.assertEqual(result.exit_code, 0)
        self.assertIn("Synchronization Status", result.output)

    def test_error_handling(self) -> None:
        """Test error handling for various commands."""
        os.chdir(self.temp_dir)
        self.runner.invoke(todowrite_cli, ["init"])

        # Test various error cases
        error_cases = [
            ["get", "invalid-id"],
            ["update", "invalid-id", "--status", "planned"],
            ["delete", "invalid-id"],
            ["status", "update", "invalid-id"],
            ["status", "show", "invalid-id"],
            ["list", "--layer", "invalid-layer"],
            ["create", "InvalidLayer", "Test", "Description"],
        ]

        for args in error_cases:
            result = self.runner.invoke(todowrite_cli, args)
            self.assertNotEqual(result.exit_code, 0)

    def test_cli_with_custom_config(self) -> None:
        """Test CLI with custom configuration."""
        os.chdir(self.temp_dir)

        # Test with different storage preferences
        for storage in ["postgresql_only", "sqlite_only", "yaml_only"]:
            result = self.runner.invoke(
                todowrite_cli, ["--storage-preference", storage, "init"]
            )
            self.assertEqual(result.exit_code, 0)

            # Test that the command works with the storage preference
            result = self.runner.invoke(
                todowrite_cli, ["--storage-preference", storage, "list"]
            )
            self.assertEqual(result.exit_code, 0)


class TestCLIErrorHandling(unittest.TestCase):
    """Test CLI error handling and edge cases."""

    def setUp(self) -> None:
        """Set up test environment."""
        self.runner = CliRunner()
        self.temp_dir = tempfile.mkdtemp()
        self.original_cwd = os.getcwd()

    def tearDown(self) -> None:
        """Clean up test environment."""
        os.chdir(self.original_cwd)
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_invalid_storage_preference(self) -> None:
        """Test invalid storage preference."""
        os.chdir(self.temp_dir)

        result = self.runner.invoke(
            todowrite_cli, ["--storage-preference", "invalid_storage", "init"]
        )
        self.assertNotEqual(result.exit_code, 0)

    def test_command_without_init(self) -> None:
        """Test commands without database initialization."""
        os.chdir(self.temp_dir)

        # Try to use commands without init
        commands = [
            ["create", "Goal", "Test", "Description"],
            ["list"],
            ["get", "GOAL-001"],
            ["update", "GOAL-001", "--title", "New Title"],
        ]

        for args in commands:
            result = self.runner.invoke(todowrite_cli, args)
            self.assertNotEqual(result.exit_code, 0)

    def test_missing_required_arguments(self) -> None:
        """Test missing required arguments."""
        os.chdir(self.temp_dir)
        self.runner.invoke(todowrite_cli, ["init"])

        # Test missing required arguments
        missing_args_cases = [
            ["create"],  # Missing layer, title, description
            ["create", "Goal"],  # Missing title, description
            ["create", "Goal", "title"],  # Missing description
            ["update"],  # Missing node_id
            ["update", "node_id"],  # Missing update data
            ["get"],  # Missing node_id
            ["delete"],  # Missing node_id
            ["status", "update"],  # Missing node_id
            ["status", "show"],  # Missing node_id
        ]

        for args in missing_args_cases:
            result = self.runner.invoke(todowrite_cli, args)
            self.assertNotEqual(result.exit_code, 0)

    def test_invalid_node_ids(self) -> None:
        """Test invalid node ID formats."""
        os.chdir(self.temp_dir)
        self.runner.invoke(todowrite_cli, ["init"])

        invalid_ids = [
            "invalid",
            "GOAL001",  # Missing hyphen
            "goal-001",  # Wrong case
            "GOAL-",  # Missing suffix
            "123",  # Invalid format
            "",  # Empty string
        ]

        for node_id in invalid_ids:
            result = self.runner.invoke(todowrite_cli, ["get", node_id])
            self.assertNotEqual(result.exit_code, 0)


if __name__ == "__main__":
    unittest.main()
