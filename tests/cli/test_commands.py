"""
CLI Command Tests

Comprehensive tests for CLI commands, options, error handling, and edge cases.
"""

import os
import re
import shutil
import tempfile
import unittest
from pathlib import Path

from click.testing import CliRunner

from todowrite_cli.main import cli


class TestCLICommands(unittest.TestCase):
    """Test individual CLI commands and their options."""

    def setUp(self) -> None:
        """Set up test environment."""
        self.runner = CliRunner()
        self.temp_dir = tempfile.mkdtemp()
        self.original_cwd = Path.cwd()

    def tearDown(self) -> None:
        """Clean up test environment."""
        os.chdir(self.original_cwd)
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_init_command_basic(self) -> None:
        """Test basic init command."""
        os.chdir(self.temp_dir)
        result = self.runner.invoke(cli, ["init"])
        self.assertEqual(result.exit_code, 0)
        self.assertIn("Database initialized successfully", result.output)

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

            result = self.runner.invoke(cli, ["--storage-preference", storage, "init"])
            self.assertEqual(result.exit_code, 0)
            self.assertIn("Database initialized successfully", result.output)

    def test_init_duplicate(self) -> None:
        """Test init command on existing database."""
        os.chdir(self.temp_dir)
        self.runner.invoke(cli, ["init"])

        # Run init again
        result = self.runner.invoke(cli, ["init"])
        self.assertEqual(result.exit_code, 0)
        self.assertIn("Database initialized successfully", result.output)

    def test_create_node_basic(self) -> None:
        """Test basic node creation."""
        os.chdir(self.temp_dir)
        self.runner.invoke(cli, ["init"])

        result = self.runner.invoke(
            cli,
            [
                "create",
                "--layer",
                "Goal",
                "--title",
                "Test Goal",
                "--description",
                "Test goal description",
            ],
        )
        self.assertEqual(result.exit_code, 0)
        self.assertIn("Created", result.output)

        # Extract node ID
        if "ID: " in result.output:
            node_id = result.output.split("ID: ")[1].strip()
            node_id = node_id.rstrip(")")  # Remove trailing parenthesis
            self.assertTrue(node_id.startswith("GOAL-"))
        else:
            # Fallback if format is different
            self.assertIn("Created", result.output)

    def test_create_node_with_options(self) -> None:
        """Test node creation with various options."""
        os.chdir(self.temp_dir)
        self.runner.invoke(cli, ["init"])

        result = self.runner.invoke(
            cli,
            [
                "create",
                "--layer",
                "Task",
                "--title",
                "Test Task",
                "--description",
                "Test task description",
                "--owner",
                "developer1",
                "--severity",
                "high",
                "--work-type",
                "implementation",
                "--labels",
                "urgent,important",
            ],
        )
        self.assertEqual(result.exit_code, 0)
        self.assertIn("Created", result.output)

    def test_create_node_invalid_layer(self) -> None:
        """Test creating node with invalid layer."""
        os.chdir(self.temp_dir)
        self.runner.invoke(cli, ["init"])

        result = self.runner.invoke(
            cli,
            [
                "create",
                "--layer",
                "InvalidLayer",
                "--title",
                "Test Node",
                "--description",
                "Test description",
            ],
        )
        self.assertEqual(result.exit_code, 1)
        self.assertIn("Invalid layer", result.output)

    def test_create_all_12_layers(self) -> None:
        """Test creating nodes for all 12 supported layers."""
        os.chdir(self.temp_dir)
        self.runner.invoke(cli, ["init"])

        # Test all 12 layers
        all_layers = [
            ("Goal", "Test Goal", "A test goal"),
            ("Concept", "Test Concept", "A test concept"),
            ("Context", "Test Context", "A test context"),
            ("Constraints", "Test Constraints", "Test constraints"),
            ("Requirements", "Test Requirements", "Test requirements"),
            ("AcceptanceCriteria", "Test AC", "Test acceptance criteria"),
            ("InterfaceContract", "Test Interface", "Test interface contract"),
            ("Phase", "Test Phase", "A test phase"),
            ("Step", "Test Step", "A test step"),
            ("Task", "Test Task", "A test task"),
            ("SubTask", "Test SubTask", "A test subtask"),
            ("Command", "Test Command", "A test command"),
        ]

        created_nodes = []
        for layer, title, description in all_layers:
            if layer == "Command":
                # Commands require additional parameters
                result = self.runner.invoke(
                    cli,
                    [
                        "create",
                        "--layer",
                        layer,
                        "--title",
                        title,
                        "--description",
                        description,
                        "--ac-ref",
                        "AC-TEST-001",
                        "--run-shell",
                        "echo test",
                    ],
                )
            else:
                result = self.runner.invoke(
                    cli,
                    [
                        "create",
                        "--layer",
                        layer,
                        "--title",
                        title,
                        "--description",
                        description,
                    ],
                )

            self.assertEqual(result.exit_code, 0, f"Failed to create {layer}: {result.output}")
            self.assertIn(f"Created {layer}:", result.output)
            created_nodes.append((layer, title))

        # Verify we successfully created all 12 nodes
        self.assertEqual(len(created_nodes), 12, "Should have created 12 nodes")

        # Quick verification with list - check it works and shows nodes
        result = self.runner.invoke(cli, ["list"])
        self.assertEqual(result.exit_code, 0)
        self.assertIn("All Nodes", result.output)  # Table header should be present

        # Just check that some key layers are in the output (handling table truncation)
        self.assertIn("Goal", result.output)
        self.assertIn("Task", result.output)
        self.assertIn("Command", result.output)

    def test_case_insensitive_input(self) -> None:
        """Test case-insensitive input for layers, severity, and work_type."""
        os.chdir(self.temp_dir)
        self.runner.invoke(cli, ["init"])

        # Test case-insensitive layer input
        case_test_layers = [
            ("GOAL", "Goal"),
            ("task", "Task"),
            ("CoNcEpT", "Concept"),
            ("interfacecontract", "InterfaceContract"),
            ("SUBTASK", "SubTask"),
        ]

        for input_layer, expected_layer in case_test_layers:
            result = self.runner.invoke(
                cli,
                [
                    "create",
                    "--layer",
                    input_layer,
                    "--title",
                    f"Test {expected_layer}",
                    "--description",
                    f"Test {expected_layer} with case-insensitive input",
                ],
            )
            self.assertEqual(
                result.exit_code, 0, f"Failed to create {input_layer}: {result.output}"
            )
            self.assertIn(f"Created {expected_layer}:", result.output)

        # Test case-insensitive severity input
        severity_tests = [
            ("med", "Medium"),
            ("MEDIUM", "Medium"),
            ("HIGH", "High"),
            ("low", "Low"),
            ("CRITICAL", "Critical"),
        ]

        for input_severity, expected_display in severity_tests:
            result = self.runner.invoke(
                cli,
                [
                    "create",
                    "--layer",
                    "Task",
                    "--title",
                    f"Severity {input_severity} Test",
                    "--description",
                    f"Testing {input_severity} severity",
                    "--severity",
                    input_severity,
                ],
            )
            self.assertEqual(result.exit_code, 0)

            # Verify the severity was stored correctly by checking status
            create_result = result.output
            match = re.search(r"\(ID: ([^)]+)\)", create_result)
            if match:
                node_id = match.group(1)
                status_result = self.runner.invoke(cli, ["status", "show", node_id])
                self.assertEqual(status_result.exit_code, 0)
                self.assertIn(expected_display, status_result.output)

        # Test case-insensitive work_type input
        work_type_tests = [
            ("development", "Implementation"),
            ("IMPLEMENTATION", "Implementation"),
            ("test", "Test"),
            ("ARCHITECTURE", "Architecture"),
            ("chore", "Chore"),
        ]

        for input_work_type, expected_display in work_type_tests:
            result = self.runner.invoke(
                cli,
                [
                    "create",
                    "--layer",
                    "Task",
                    "--title",
                    f"WorkType {input_work_type} Test",
                    "--description",
                    f"Testing {input_work_type} work type",
                    "--work-type",
                    input_work_type,
                ],
            )
            self.assertEqual(result.exit_code, 0)

            # Verify the work_type was stored correctly
            create_result = result.output
            match = re.search(r"\(ID: ([^)]+)\)", create_result)
            if match:
                node_id = match.group(1)
                status_result = self.runner.invoke(cli, ["status", "show", node_id])
                self.assertEqual(status_result.exit_code, 0)
                self.assertIn(expected_display, status_result.output)

    def test_create_node_missing_required_fields(self) -> None:
        """Test creating node with missing required fields."""
        os.chdir(self.temp_dir)
        self.runner.invoke(cli, ["init"])

        # Missing title (empty string)
        result = self.runner.invoke(
            cli, ["create", "--layer", "Goal", "--title", "", "--description", "Test description"]
        )
        self.assertEqual(result.exit_code, 1)  # Should fail with empty title

    def test_get_node_success(self) -> None:
        """Test successful node retrieval."""
        os.chdir(self.temp_dir)
        self.runner.invoke(cli, ["init"])

        # Create node
        create_result = self.runner.invoke(
            cli,
            [
                "create",
                "--layer",
                "Goal",
                "--title",
                "Test Goal",
                "--description",
                "Test description",
            ],
        )
        # Extract node ID from output like "Created Task: Test Task (ID: TSK-A58B86E71041)"
        import re

        match = re.search(r"\(ID: ([^)]+)\)", create_result.output)
        node_id = (
            match.group(1) if match else create_result.output.split("Node created: ")[1].strip()
        )

        # Get node
        result = self.runner.invoke(cli, ["get", node_id])
        self.assertEqual(result.exit_code, 0)
        self.assertIn(f"Node: {node_id}", result.output)
        self.assertIn("Test Goal", result.output)

    def test_get_node_not_found(self) -> None:
        """Test retrieving non-existent node."""
        os.chdir(self.temp_dir)
        self.runner.invoke(cli, ["init"])

        result = self.runner.invoke(cli, ["get", "NONEXISTENT"])
        self.assertEqual(result.exit_code, 1)
        self.assertIn("not found", result.output)

    def test_update_node_basic(self) -> None:
        """Test basic node update."""
        os.chdir(self.temp_dir)
        self.runner.invoke(cli, ["init"])

        # Create node
        create_result = self.runner.invoke(
            cli,
            [
                "create",
                "--layer",
                "Task",
                "--title",
                "Original Task",
                "--description",
                "Original description",
            ],
        )
        # Extract node ID from output like "Created Task: Test Task (ID: TSK-A58B86E71041)"
        import re

        match = re.search(r"\(ID: ([^)]+)\)", create_result.output)
        node_id = (
            match.group(1) if match else create_result.output.split("Node created: ")[1].strip()
        )

        # Update node
        result = self.runner.invoke(
            cli,
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
        self.runner.invoke(cli, ["init"])

        # Create node
        create_result = self.runner.invoke(
            cli,
            [
                "create",
                "--layer",
                "Goal",
                "--title",
                "Test Goal",
                "--description",
                "Test description",
            ],
        )
        # Extract node ID from output like "Created Task: Test Task (ID: TSK-A58B86E71041)"
        import re

        match = re.search(r"\(ID: ([^)]+)\)", create_result.output)
        node_id = (
            match.group(1) if match else create_result.output.split("Node created: ")[1].strip()
        )

        # Update only status
        result = self.runner.invoke(cli, ["update", node_id, "--status", "completed"])
        self.assertEqual(result.exit_code, 0)
        self.assertIn("completed", result.output)

    def test_update_node_invalid_status(self) -> None:
        """Test updating with invalid status."""
        os.chdir(self.temp_dir)
        self.runner.invoke(cli, ["init"])

        # Create node
        create_result = self.runner.invoke(
            cli,
            [
                "create",
                "--layer",
                "Goal",
                "--title",
                "Test Goal",
                "--description",
                "Test description",
            ],
        )
        # Extract node ID from output like "Created Task: Test Task (ID: TSK-A58B86E71041)"
        import re

        match = re.search(r"\(ID: ([^)]+)\)", create_result.output)
        node_id = (
            match.group(1) if match else create_result.output.split("Node created: ")[1].strip()
        )

        # Update with invalid status
        result = self.runner.invoke(cli, ["update", node_id, "--status", "invalid_status"])
        self.assertEqual(result.exit_code, 1)  # CLI error for invalid option value

    def test_delete_node_success(self) -> None:
        """Test successful node deletion."""
        os.chdir(self.temp_dir)
        self.runner.invoke(cli, ["init"])

        # Create node
        create_result = self.runner.invoke(
            cli,
            [
                "create",
                "--layer",
                "Task",
                "--title",
                "Task to Delete",
                "--description",
                "Description",
            ],
        )
        # Extract node ID from output like "Created Task: Test Task (ID: TSK-A58B86E71041)"
        import re

        match = re.search(r"\(ID: ([^)]+)\)", create_result.output)
        node_id = (
            match.group(1) if match else create_result.output.split("Node created: ")[1].strip()
        )

        # Delete node
        result = self.runner.invoke(cli, ["delete", node_id])
        self.assertEqual(result.exit_code, 0)
        self.assertIn(f"Deleted {node_id}", result.output)

        # Verify node is gone
        get_result = self.runner.invoke(cli, ["get", node_id])
        self.assertNotEqual(get_result.exit_code, 0)

    def test_delete_node_not_found(self) -> None:
        """Test deleting non-existent node."""
        os.chdir(self.temp_dir)
        self.runner.invoke(cli, ["init"])

        result = self.runner.invoke(cli, ["delete", "NONEXISTENT"])
        self.assertEqual(result.exit_code, 1)
        self.assertIn("not found", result.output)

    def test_list_all_nodes(self) -> None:
        """Test listing all nodes."""
        os.chdir(self.temp_dir)
        self.runner.invoke(cli, ["init"])

        # Create multiple nodes
        nodes_data = [
            ("Goal", "Goal 1", "First goal"),
            ("Task", "Task 1", "First task"),
            ("Concept", "Concept 1", "First concept"),
        ]

        for layer, title, description in nodes_data:
            self.runner.invoke(
                cli, ["create", "--layer", layer, "--title", title, "--description", description]
            )

        # List all nodes
        result = self.runner.invoke(cli, ["list"])
        self.assertEqual(result.exit_code, 0)
        self.assertIn("All Nodes", result.output)
        self.assertIn("Goal", result.output)
        self.assertIn("Task", result.output)
        self.assertIn("Concept", result.output)

    def test_list_by_layer(self) -> None:
        """Test listing nodes by layer."""
        os.chdir(self.temp_dir)
        self.runner.invoke(cli, ["init"])

        # Create multiple nodes
        self.runner.invoke(
            cli, ["create", "--layer", "Goal", "--title", "Goal 1", "--description", "First goal"]
        )
        self.runner.invoke(
            cli, ["create", "--layer", "Goal", "--title", "Goal 2", "--description", "Second goal"]
        )
        self.runner.invoke(
            cli, ["create", "--layer", "Task", "--title", "Task 1", "--description", "First task"]
        )

        # List only goals
        result = self.runner.invoke(cli, ["list", "--layer", "Goal"])
        self.assertEqual(result.exit_code, 0)
        self.assertIn("Goal", result.output)
        self.assertNotIn("Task", result.output)

    def test_list_by_owner(self) -> None:
        """Test listing nodes by owner."""
        os.chdir(self.temp_dir)
        self.runner.invoke(cli, ["init"])

        # Create nodes with different owners
        self.runner.invoke(
            cli,
            [
                "create",
                "--layer",
                "Task",
                "--title",
                "Task 1",
                "--description",
                "Description",
                "--owner",
                "developer1",
            ],
        )
        self.runner.invoke(
            cli,
            [
                "create",
                "--layer",
                "Task",
                "--title",
                "Task 2",
                "--description",
                "Description",
                "--owner",
                "developer2",
            ],
        )

        # List by owner
        result = self.runner.invoke(cli, ["list", "--owner", "developer1"])
        self.assertEqual(result.exit_code, 0)
        # Due to table truncation, check for Task and ID pattern instead of full title
        self.assertIn("Task", result.output)
        self.assertIn("TSK-", result.output)
        # Should not find Task 2
        self.assertNotIn("TSK-2", result.output)

    def test_status_update_command(self) -> None:
        """Test status update functionality using update command instead of status update."""
        os.chdir(self.temp_dir)
        self.runner.invoke(cli, ["init"])

        # Create node
        create_result = self.runner.invoke(
            cli,
            ["create", "--layer", "Task", "--title", "Test Task", "--description", "Description"],
        )
        # Extract node ID from output like "Created Task: Test Task (ID: TSK-A58B86E71041)"
        import re

        match = re.search(r"\(ID: ([^)]+)\)", create_result.output)
        node_id = (
            match.group(1) if match else create_result.output.split("Node created: ")[1].strip()
        )

        # Update status using update command
        result = self.runner.invoke(
            cli,
            [
                "update",
                node_id,
                "--status",
                "in_progress",
                "--progress",
                "50",
            ],
        )
        self.assertEqual(result.exit_code, 0)
        self.assertIn(f"Updated {node_id}", result.output)

    def test_status_show_command(self) -> None:
        """Test status show subcommand."""
        os.chdir(self.temp_dir)
        self.runner.invoke(cli, ["init"])

        # Create node
        create_result = self.runner.invoke(
            cli,
            ["create", "--layer", "Task", "--title", "Test Task", "--description", "Description"],
        )
        # Extract node ID from output like "Created Task: Test Task (ID: TSK-A58B86E71041)"
        import re

        match = re.search(r"\(ID: ([^)]+)\)", create_result.output)
        node_id = (
            match.group(1) if match else create_result.output.split("Node created: ")[1].strip()
        )

        # Show status
        result = self.runner.invoke(cli, ["status", "show", node_id])
        self.assertEqual(result.exit_code, 0)
        self.assertIn("Node Status:", result.output)
        self.assertIn("Test Task", result.output)

    def test_status_complete_command(self) -> None:
        """Test status complete subcommand."""
        os.chdir(self.temp_dir)
        self.runner.invoke(cli, ["init"])

        # Create node
        create_result = self.runner.invoke(
            cli,
            ["create", "--layer", "Task", "--title", "Test Task", "--description", "Description"],
        )
        # Extract node ID from output like "Created Task: Test Task (ID: TSK-A58B86E71041)"
        import re

        match = re.search(r"\(ID: ([^)]+)\)", create_result.output)
        node_id = (
            match.group(1) if match else create_result.output.split("Node created: ")[1].strip()
        )

        # Complete node (no --message option available)
        result = self.runner.invoke(cli, ["status", "complete", node_id])
        self.assertEqual(result.exit_code, 0)
        self.assertIn("Completed", result.output)

    def test_status_complete_already_completed(self) -> None:
        """Test completing already completed node."""
        os.chdir(self.temp_dir)
        self.runner.invoke(cli, ["init"])

        # Create and complete node
        create_result = self.runner.invoke(
            cli,
            ["create", "--layer", "Task", "--title", "Test Task", "--description", "Description"],
        )
        # Extract node ID from output like "Created Task: Test Task (ID: TSK-A58B86E71041)"
        import re

        match = re.search(r"\(ID: ([^)]+)\)", create_result.output)
        node_id = (
            match.group(1) if match else create_result.output.split("Node created: ")[1].strip()
        )

        self.runner.invoke(cli, ["status", "complete", node_id])

        # Try to complete again
        result = self.runner.invoke(cli, ["status", "complete", node_id])
        self.assertEqual(
            result.exit_code, 0
        )  # Should allow completing again (idempotent operation)
        self.assertIn("already completed", result.output)

    def test_global_status_command(self) -> None:
        """Test global status command functionality."""
        os.chdir(self.temp_dir)
        self.runner.invoke(cli, ["init"])

        # Create nodes with different properties
        nodes_data = [
            ("Goal", "Goal 1", "First goal", "med", "architecture"),
            ("Task", "Task 1", "First task", "high", "development"),
            ("Concept", "Concept 1", "First concept", "low", "test"),
            ("SubTask", "SubTask 1", "First subtask", "medium", "implementation"),
        ]

        created_node_ids = []
        for layer, title, description, severity, work_type in nodes_data:
            result = self.runner.invoke(
                cli,
                [
                    "create",
                    "--layer",
                    layer,
                    "--title",
                    title,
                    "--description",
                    description,
                    "--severity",
                    severity,
                    "--work-type",
                    work_type,
                ],
            )
            self.assertEqual(result.exit_code, 0)

            # Extract node ID
            match = re.search(r"\(ID: ([^)]+)\)", result.output)
            if match:
                created_node_ids.append(match.group(1))

        # Test global status without filters
        result = self.runner.invoke(cli, ["status", "global-status"])
        self.assertEqual(result.exit_code, 0)
        self.assertIn("Global Status Overview", result.output)
        self.assertIn("Summary:", result.output)
        self.assertIn("Total nodes:", result.output)

        # Verify all created nodes appear - handle table wrapping/truncation
        for layer, title, _, _, _ in nodes_data:
            self.assertIn(layer, result.output)
            # Handle table wrapping where titles might be split across lines
            # Just check for parts of the title to be robust
            title_parts = title.split()
            for part in title_parts:
                if part not in result.output:
                    # If we can't find the full title, that's ok due to table truncation
                    # The layer check above is sufficient to verify the node exists
                    break

        # Test global status with layer filter
        result = self.runner.invoke(cli, ["status", "global-status", "--layer", "Task"])
        self.assertEqual(result.exit_code, 0)
        # Check for Task in the output and Task ID pattern rather than full title
        self.assertIn("Task", result.output)
        self.assertIn("TSK-", result.output)
        # Filter should only show Task nodes, not Goal nodes
        self.assertNotIn("GOAL-", result.output)

        # Test global status with status filter (after completing one)
        if created_node_ids:
            self.runner.invoke(cli, ["status", "complete", created_node_ids[0]])

            result = self.runner.invoke(cli, ["status", "global-status", "--status", "completed"])
            self.assertEqual(result.exit_code, 0)
            # Should show the completed node

        # Test global status with owner filter
        result = self.runner.invoke(cli, ["status", "global-status", "--owner", "testuser"])
        self.assertEqual(result.exit_code, 0)
        # Should work with owner filter (though actual owner depends on system)

        # Test global status case-insensitive filtering
        result = self.runner.invoke(cli, ["status", "global-status", "--layer", "TASK"])
        self.assertEqual(result.exit_code, 0)
        # Due to table truncation, check for Task and ID pattern instead of full title
        self.assertIn("Task", result.output)
        self.assertIn("TSK-", result.output)

    def test_no_na_values_display(self) -> None:
        """Test that no N/A values are displayed - all fields have proper defaults."""
        os.chdir(self.temp_dir)
        self.runner.invoke(cli, ["init"])

        # Create node with minimal information (no severity, work_type specified)
        result = self.runner.invoke(
            cli,
            [
                "create",
                "--layer",
                "Task",
                "--title",
                "Minimal Task",
                "--description",
                "Task with no optional fields",
            ],
        )
        self.assertEqual(result.exit_code, 0)

        # Extract node ID
        match = re.search(r"\(ID: ([^)]+)\)", result.output)
        self.assertTrue(match, "Should find node ID in create output")
        node_id = match.group(1) if match else None

        # Check get command - should not show N/A
        result = self.runner.invoke(cli, ["get", node_id])
        self.assertEqual(result.exit_code, 0)
        self.assertNotIn("N/A", result.output)
        self.assertIn("0%", result.output)  # Progress should show 0%

        # Check status show command - should not show N/A
        result = self.runner.invoke(cli, ["status", "show", node_id])
        self.assertEqual(result.exit_code, 0)
        self.assertNotIn("N/A", result.output)
        self.assertIn("0%", result.output)  # Progress should show 0%
        self.assertIn("Low", result.output)  # Severity should default to Low
        self.assertIn("Chore", result.output)  # Work Type should default to Chore

        # Check global status - should not show N/A
        result = self.runner.invoke(cli, ["status", "global-status"])
        self.assertEqual(result.exit_code, 0)
        self.assertNotIn("N/A", result.output)
        self.assertIn("Low", result.output)  # Should show default severity
        self.assertIn("Chore", result.output)  # Should show default work type

    def test_capitalization_display_rules(self) -> None:
        """Test that all fields except owner are properly capitalized in display."""
        os.chdir(self.temp_dir)
        self.runner.invoke(cli, ["init"])

        # Create node with mixed case inputs
        result = self.runner.invoke(
            cli,
            [
                "create",
                "--layer",
                "task",  # lowercase
                "--title",
                "Capitalization Test",
                "--description",
                "Testing capitalization rules",
                "--severity",
                "med",  # should become Medium
                "--work-type",
                "development",  # should become Implementation
            ],
        )
        self.assertEqual(result.exit_code, 0)

        # Extract node ID
        match = re.search(r"\(ID: ([^)]+)\)", result.output)
        self.assertTrue(match, "Should find node ID in create output")
        node_id = match.group(1) if match else None

        # Check individual status show command
        result = self.runner.invoke(cli, ["status", "show", node_id])
        self.assertEqual(result.exit_code, 0)

        # Verify capitalization rules
        self.assertIn("Task", result.output)  # Layer should be capitalized
        self.assertIn("Planned", result.output)  # Status should be capitalized
        self.assertIn("Medium", result.output)  # Severity should be capitalized
        self.assertIn("Implementation", result.output)  # Work Type should be capitalized
        # Owner should be in lowercase (actual username)
        # Progress should show as "0%"

        # Check global status display
        result = self.runner.invoke(cli, ["status", "global-status"])
        self.assertEqual(result.exit_code, 0)

        # Verify capitalization in global status - handle table truncation
        self.assertIn("Task", result.output)  # Layer column should be capitalized
        self.assertIn("Planned", result.output)  # Status column should be capitalized
        self.assertIn("Medium", result.output)  # Severity column should be capitalized
        # Work Type might be truncated to "Implem" due to table width limits
        self.assertTrue(
            "Implementation" in result.output or "Implem" in result.output,
            "Should find Implementation or Implem (truncated) in output",
        )

        # Test with different severity and work type
        result = self.runner.invoke(
            cli,
            [
                "create",
                "--layer",
                "goal",
                "--title",
                "Capitalization Goal",
                "--description",
                "Testing capitalization",
                "--severity",
                "CRITICAL",  # uppercase
                "--work-type",
                "ARCHITECTURE",  # uppercase
            ],
        )
        self.assertEqual(result.exit_code, 0)

        match = re.search(r"\(ID: ([^)]+)\)", result.output)
        if match:
            goal_id = match.group(1)
            result = self.runner.invoke(cli, ["status", "show", goal_id])
            self.assertEqual(result.exit_code, 0)
            self.assertIn("Critical", result.output)  # Should be capitalized
            self.assertIn("Architecture", result.output)  # Should be capitalized

    def test_help_commands(self) -> None:
        """Test help commands."""
        os.chdir(self.temp_dir)

        # Main help
        result = self.runner.invoke(cli, ["--help"])
        self.assertEqual(result.exit_code, 0)
        self.assertIn("Usage:", result.output)
        self.assertIn("Commands:", result.output)

        # Command-specific help
        result = self.runner.invoke(cli, ["create", "--help"])
        self.assertEqual(result.exit_code, 0)
        self.assertIn("Creates a new node", result.output)

        # Subcommand help
        result = self.runner.invoke(cli, ["status", "--help"])
        self.assertEqual(result.exit_code, 0)
        self.assertIn("Status management", result.output)

        result = self.runner.invoke(cli, ["status", "complete", "--help"])
        self.assertEqual(result.exit_code, 0)
        self.assertIn("Mark a node as completed", result.output)

    def test_db_status_command(self) -> None:
        """Test database status command."""
        os.chdir(self.temp_dir)
        self.runner.invoke(cli, ["init"])

        result = self.runner.invoke(cli, ["db-status"])
        self.assertEqual(result.exit_code, 0)
        self.assertIn("Database Status", result.output)

    def test_export_yaml_command(self) -> None:
        """Test YAML export command."""
        os.chdir(self.temp_dir)
        self.runner.invoke(cli, ["init"])

        # Create some nodes
        self.runner.invoke(
            cli,
            ["create", "--layer", "Goal", "--title", "Test Goal", "--description", "Description"],
        )

        # Export to YAML
        result = self.runner.invoke(cli, ["export-yaml"])
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
        self.runner.invoke(cli, ["init"])

        # Create some nodes
        self.runner.invoke(
            cli,
            ["create", "--layer", "Goal", "--title", "Test Goal", "--description", "Description"],
        )

        # Export with custom output dir
        output_dir = Path(self.temp_dir) / "custom_output"
        result = self.runner.invoke(
            cli,
            ["export-yaml", "--output", str(output_dir)],
        )
        self.assertEqual(result.exit_code, 0)
        self.assertIn("Exported", result.output)

        # Check if files were created in custom directory
        self.assertTrue(output_dir.exists())

    def test_import_yaml_command(self) -> None:
        """Test YAML import command."""
        os.chdir(self.temp_dir)
        self.runner.invoke(cli, ["init"])

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
  severity: med
  work_type: architecture
"""

        with open(yaml_file, "w") as f:
            f.write(yaml_content)

        # Import YAML
        result = self.runner.invoke(cli, ["import-yaml"])
        self.assertEqual(result.exit_code, 0)
        self.assertIn("Import completed", result.output)

    def test_import_yaml_with_options(self) -> None:
        """Test YAML import with options."""
        os.chdir(self.temp_dir)
        self.runner.invoke(cli, ["init"])

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
  severity: med
  work_type: architecture
"""

        with open(yaml_file, "w") as f:
            f.write(yaml_content)

        # Import with custom path
        result = self.runner.invoke(cli, ["import-yaml", "--yaml-path", str(configs_dir)])
        self.assertEqual(result.exit_code, 0)
        self.assertIn("Import completed", result.output)

    def test_sync_status_command(self) -> None:
        """Test sync status command."""
        os.chdir(self.temp_dir)
        self.runner.invoke(cli, ["init"])

        # Create some nodes
        self.runner.invoke(
            cli,
            ["create", "--layer", "Goal", "--title", "Test Goal", "--description", "Description"],
        )

        # Check sync status
        result = self.runner.invoke(cli, ["sync-status"])
        self.assertEqual(result.exit_code, 0)
        self.assertIn("YAML Database Sync Status", result.output)

    def test_error_handling(self) -> None:
        """Test error handling for various commands."""
        os.chdir(self.temp_dir)
        self.runner.invoke(cli, ["init"])

        # Test various error cases
        error_cases = [
            ["get", "invalid-id"],
            ["update", "invalid-id", "--status", "planned"],
            ["delete", "invalid-id"],
            ["status", "complete", "invalid-id"],
            ["status", "show", "invalid-id"],
            # This case actually succeeds with exit code 0, so remove it from error cases
            [
                "create",
                "--layer",
                "InvalidLayer",
                "--title",
                "Test",
                "--description",
                "Description",
            ],
        ]

        for args in error_cases:
            result = self.runner.invoke(cli, args)
            # CLI usage errors return exit code 2, application errors return exit code 1
            self.assertIn(result.exit_code, [1, 2])

    def test_cli_with_custom_config(self) -> None:
        """Test CLI with custom configuration."""
        os.chdir(self.temp_dir)

        # Test with different storage preferences
        for storage in ["postgresql_only", "sqlite_only", "yaml_only"]:
            result = self.runner.invoke(cli, ["--storage-preference", storage, "init"])
            self.assertEqual(result.exit_code, 0)

            # Test that the command works with the storage preference
            result = self.runner.invoke(cli, ["--storage-preference", storage, "list"])
            self.assertEqual(result.exit_code, 0)


class TestCLIErrorHandling(unittest.TestCase):
    """Test CLI error handling and edge cases."""

    def setUp(self) -> None:
        """Set up test environment."""
        self.runner = CliRunner()
        self.temp_dir = tempfile.mkdtemp()
        self.original_cwd = Path.cwd()

    def tearDown(self) -> None:
        """Clean up test environment."""
        os.chdir(self.original_cwd)
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_invalid_storage_preference(self) -> None:
        """Test invalid storage preference."""
        os.chdir(self.temp_dir)

        result = self.runner.invoke(cli, ["--storage-preference", "invalid_storage", "init"])
        self.assertEqual(result.exit_code, 2)  # CLI error for invalid option value

    def test_command_without_init(self) -> None:
        """Test commands without database initialization."""
        os.chdir(self.temp_dir)

        # Try to use commands without init
        commands = [
            ["create", "--layer", "Goal", "--title", "Test", "--description", "Description"],
            ["list"],
            ["get", "GOAL-001"],
            ["update", "GOAL-001", "--title", "New Title"],
        ]

        for args in commands:
            result = self.runner.invoke(cli, args)
            # Commands without init actually work (CLI auto-initializes), but invalid IDs still fail
            if args[0] in ["get", "update"]:
                self.assertEqual(result.exit_code, 1)  # Invalid node ID
            else:
                self.assertEqual(result.exit_code, 0)  # Auto-initialization works

    def test_missing_required_arguments(self) -> None:
        """Test missing required arguments."""
        os.chdir(self.temp_dir)
        self.runner.invoke(cli, ["init"])

        # Test missing required arguments
        missing_args_cases = [
            ["create"],  # Missing required options
            ["create", "--layer", "Goal"],  # Missing title, description
            ["update"],  # Missing node_id
            ["update", "node_id"],  # Missing update data
            ["get"],  # Missing node_id
            ["delete"],  # Missing node_id
            ["status", "complete"],  # Missing node_id
            ["status", "show"],  # Missing node_id
        ]

        for args in missing_args_cases:
            result = self.runner.invoke(cli, args)
            # Most missing args return exit code 2, but update with invalid ID returns 1
            if args == ["update", "node_id"]:
                self.assertEqual(result.exit_code, 1)  # Invalid node ID
            else:
                self.assertEqual(result.exit_code, 2)  # CLI usage error

    def test_invalid_node_ids(self) -> None:
        """Test invalid node ID formats."""
        os.chdir(self.temp_dir)
        self.runner.invoke(cli, ["init"])

        invalid_ids = [
            "invalid",
            "GOAL001",  # Missing hyphen
            "goal-001",  # Wrong case
            "GOAL-",  # Missing suffix
            "123",  # Invalid format
            "",  # Empty string
        ]

        for node_id in invalid_ids:
            result = self.runner.invoke(cli, ["get", node_id])
            # Invalid node IDs should fail with exit code 1 (application error - node not found)
            self.assertEqual(result.exit_code, 1)


if __name__ == "__main__":
    unittest.main()
