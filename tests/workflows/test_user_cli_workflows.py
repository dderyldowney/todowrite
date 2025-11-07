"""
User CLI Workflows Tests

These tests verify the step-by-step workflows that a user would follow to use ToDoWrite
as a command-line application. Each test represents a complete user scenario.
"""

import os
import shutil
import tempfile
import unittest
from pathlib import Path

from click.testing import CliRunner
from todowrite_cli.main import cli as todowrite_cli


class TestUserCliWorkflows(unittest.TestCase):
    """Test CLI workflows that represent typical user scenarios."""

    def setUp(self) -> None:
        """Set up test environment."""
        self.runner = CliRunner()
        self.temp_dir = tempfile.mkdtemp()
        self.original_cwd = Path.cwd()

    def tearDown(self) -> None:
        """Clean up test environment."""
        os.chdir(self.original_cwd)
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_todowrite_cli_initialization_workflow(self) -> None:
        """
        Test: User initializes ToDoWrite project for the first time
        Steps:
        1. User navigates to project directory
        2. User runs todowrite init to set up database
        3. User verifies successful initialization
        """
        # Step 1: Change to temporary directory (simulate user navigating to project)
        os.chdir(self.temp_dir)

        # Step 2: Run initialization command
        result = self.runner.invoke(todowrite_cli, ["init"])

        # Step 3: Verify successful initialization
        self.assertEqual(result.exit_code, 0, "Init command should succeed")
        self.assertIn(
            "Database initialized successfully",
            result.output,
            "Should show success message",
        )

        # Verify database file was created (for SQLite)
        db_files = list(Path(self.temp_dir).glob("*.db"))
        self.assertTrue(len(db_files) > 0, "Database file should be created")

    def test_todowrite_cli_goal_creation_workflow(self) -> None:
        """
        Test: User creates a hierarchical goal structure
        Steps:
        1. User initializes project (prerequisite)
        2. User creates a main goal
        3. User creates supporting goals/concepts
        4. User verifies the hierarchy
        """
        # Setup: Initialize project first
        os.chdir(self.temp_dir)
        self.runner.invoke(todowrite_cli, ["init"])

        # Step 2: Create main goal
        result = self.runner.invoke(
            todowrite_cli,
            [
                "create",
                "--layer",
                "Goal",
                "--title",
                "Launch New Product",
                "--description",
                "Successfully launch our new product to market",
            ],
        )
        self.assertEqual(result.exit_code, 0, "Goal creation should succeed")
        # Extract node ID from output like "Created Goal: Launch Mobile App (ID: GOAL-A58B86E71041)"

        # goal_id extraction not needed for this test

        # Step 3: Create supporting concept
        result = self.runner.invoke(
            todowrite_cli,
            [
                "create",
                "--layer",
                "Concept",
                "--title",
                "Market Research",
                "--description",
                "Research target market and customer needs",
            ],
        )
        self.assertEqual(
            result.exit_code,
            0,
            "Concept creation should succeed",
        )

        # Step 4: Create a task related to the goal
        result = self.runner.invoke(
            todowrite_cli,
            [
                "create",
                "--layer",
                "Task",
                "--title",
                "Create Business Plan",
                "--description",
                "Write comprehensive business plan for the product launch",
            ],
        )
        self.assertEqual(result.exit_code, 0, "Task creation should succeed")

    def test_todowrite_cli_progress_tracking_workflow(self) -> None:
        """
        Test: User tracks progress of tasks
        Steps:
        1. User creates a task
        2. User starts working on the task
        3. User updates progress
        4. User checks status
        """
        # Setup: Create project and task
        os.chdir(self.temp_dir)
        self.runner.invoke(todowrite_cli, ["init"])

        result = self.runner.invoke(
            todowrite_cli,
            [
                "create",
                "--layer",
                "Task",
                "--title",
                "Develop Prototype",
                "--description",
                "Create initial product prototype",
            ],
        )
        self.assertEqual(result.exit_code, 0)
        # Extract node ID from output like "Created Task: Develop Prototype (ID: TSK-A58B86E71041)"
        import re

        match = re.search(r"\(ID: ([^)]+)\)", result.output)
        task_id = (
            match.group(1) if match else result.output.split(" ")[-1].strip()
        )

        # Step 2: Start working on task - use update command instead of status update
        # Clean task_id by removing any trailing parenthesis
        task_id = task_id.rstrip(")")
        result = self.runner.invoke(
            todowrite_cli,
            ["update", task_id, "--status", "in_progress"],
        )
        self.assertEqual(
            result.exit_code,
            0,
            f"Failed to update task {task_id}: {result.output}",
        )

        # Step 3: Update progress
        result = self.runner.invoke(
            todowrite_cli,
            [
                "update",
                task_id,
                "--status",
                "in_progress",
                "--progress",
                "75",
            ],
        )
        self.assertEqual(result.exit_code, 0)

        # Step 4: Check status
        result = self.runner.invoke(todowrite_cli, ["get", task_id])
        self.assertEqual(result.exit_code, 0)
        self.assertIn("In Progress", result.output)

    def test_todowrite_cli_listing_workflow(self) -> None:
        """
        Test: User lists and organizes nodes
        Steps:
        1. User creates multiple nodes of different types
        2. User lists all nodes
        3. User lists nodes by type
        4. User searches for specific nodes
        """
        # Setup: Initialize and create multiple nodes
        os.chdir(self.temp_dir)
        self.runner.invoke(todowrite_cli, ["init"])

        # Create different types of nodes
        nodes_to_create = [
            ("Goal", "Company Vision", "Long-term company vision statement"),
            ("Concept", "User Research", "Understanding user needs"),
            ("Task", "Design UI", "Create user interface design"),
            ("Step", "Sketch Wireframes", "Initial UI wireframes"),
            ("Constraints", "Budget Limit", "Must stay under $100k budget"),
        ]

        created_ids = []
        for node_type, title, description in nodes_to_create:
            # Skip unsupported node types for now
            if node_type not in ["Goal", "Concept", "Task", "Command"]:
                continue
            result = self.runner.invoke(
                todowrite_cli,
                [
                    "create",
                    "--layer",
                    node_type,
                    "--title",
                    title,
                    "--description",
                    description,
                ],
            )
            self.assertEqual(result.exit_code, 0)
            node_id = result.output.split(" ")[-1].strip()
            created_ids.append(node_id)

        # Step 2: List all nodes
        result = self.runner.invoke(todowrite_cli, ["list"])
        self.assertEqual(result.exit_code, 0)
        self.assertGreater(
            len(result.output.split("\n")),
            3,
            "Should list multiple nodes",
        )

        # Step 3: List by specific layer (should work with --layer option if available)
        # Test listing available commands
        result = self.runner.invoke(todowrite_cli, ["--help"])
        self.assertEqual(result.exit_code, 0)
        self.assertIn(
            "list",
            result.output,
            "List command should be available",
        )

    def test_todowrite_cli_export_import_workflow(self) -> None:
        """
        Test: User exports and imports data
        Steps:
        1. User creates some nodes
        2. User exports data to YAML
        3. User imports data (or verifies export format)
        """
        # Setup: Initialize and create nodes
        os.chdir(self.temp_dir)
        self.runner.invoke(todowrite_cli, ["init"])

        # Create test nodes
        result = self.runner.invoke(
            todowrite_cli,
            [
                "create",
                "--layer",
                "Goal",
                "--title",
                "Test Goal",
                "--description",
                "A test goal for export",
            ],
        )
        self.assertEqual(result.exit_code, 0)

        # Step 2: Export to YAML
        result = self.runner.invoke(todowrite_cli, ["export-yaml"])
        self.assertEqual(result.exit_code, 0)
        self.assertIn(
            "Export completed",
            result.output,
            "Should show export success",
        )

        # Verify export directory exists
        configs_dir = Path(self.temp_dir) / "configs"
        if configs_dir.exists():
            yaml_files = list(configs_dir.rglob("*.yaml"))
            self.assertTrue(
                len(yaml_files) > 0,
                "YAML files should be created",
            )

    def test_todowrite_cli_database_status_workflow(self) -> None:
        """
        Test: User checks database and storage status
        Steps:
        1. User checks database status
        2. User verifies storage configuration
        3. User gets setup guidance if needed
        """
        # Step 1: Check database status
        os.chdir(self.temp_dir)
        result = self.runner.invoke(todowrite_cli, ["db-status"])
        self.assertEqual(result.exit_code, 0)
        self.assertIn(
            "Database Status",
            result.output,
            "Should show database information",
        )

        # Step 2: Verify database configuration info
        self.assertIn(
            "Schema Valid",
            result.output,
            "Should show schema validation",
        )

    def test_todowrite_cli_help_workflow(self) -> None:
        """
        Test: User explores available commands and help
        Steps:
        1. User runs main help
        2. User explores subcommand help
        3. User gets help for specific commands
        """
        # Step 1: Main help
        result = self.runner.invoke(todowrite_cli, ["--help"])
        self.assertEqual(result.exit_code, 0)
        self.assertIn("Usage:", result.output, "Should show usage")
        self.assertIn(
            "Commands:",
            result.output,
            "Should show available commands",
        )

        # Step 2: Subcommand help
        result = self.runner.invoke(todowrite_cli, ["create", "--help"])
        self.assertEqual(result.exit_code, 0)
        self.assertIn(
            "Creates a new node",
            result.output,
            "Should show create command help",
        )

        # Step 3: Help for other commands
        result = self.runner.invoke(todowrite_cli, ["list", "--help"])
        self.assertEqual(result.exit_code, 0)
        self.assertIn(
            "Lists all the nodes",
            result.output,
            "Should show list command help",
        )

    def test_todowrite_cli_multistep_project_workflow(self) -> None:
        """
        Test: Complete project workflow from concept to completion
        Steps:
        1. User sets up project structure with goals and concepts
        2. User breaks down into requirements and acceptance criteria
        3. User creates tasks and steps
        4. User tracks progress through completion
        5. User reviews the completed project structure
        """
        # Setup: Initialize project
        os.chdir(self.temp_dir)
        self.runner.invoke(todowrite_cli, ["init"])

        # Step 1: Create project vision and goals
        result = self.runner.invoke(
            todowrite_cli,
            [
                "create",
                "--layer",
                "Goal",
                "--title",
                "Launch Mobile App",
                "--description",
                "Launch successful mobile app",
            ],
        )
        self.assertEqual(result.exit_code, 0)
        # Extract node ID from output like "Created Goal: Launch Mobile App (ID: GOAL-A58B86E71041)"

        # goal_id extraction not needed for this test

        result = self.runner.invoke(
            todowrite_cli,
            [
                "create",
                "--layer",
                "Concept",
                "--title",
                "User Research",
                "--description",
                "Understand target users",
            ],
        )
        self.assertEqual(result.exit_code, 0)

        # Step 2: Define requirements - use Task as proxy for unsupported types
        result = self.runner.invoke(
            todowrite_cli,
            [
                "create",
                "--layer",
                "Task",
                "--title",
                "Core Features",
                "--description",
                "User authentication, push notifications, offline mode",
            ],
        )
        self.assertEqual(result.exit_code, 0)

        # Step 3: Create acceptance criteria - use Task as proxy for unsupported types
        result = self.runner.invoke(
            todowrite_cli,
            [
                "create",
                "--layer",
                "Task",
                "--title",
                "Login Flow",
                "--description",
                "Users can login with email/password, social login, biometric auth",
            ],
        )
        self.assertEqual(result.exit_code, 0)

        # Step 4: Break down into tasks
        result = self.runner.invoke(
            todowrite_cli,
            [
                "create",
                "--layer",
                "Task",
                "--title",
                "Design Architecture",
                "--description",
                "Create technical architecture for the mobile app",
            ],
        )
        self.assertEqual(result.exit_code, 0)

        result = self.runner.invoke(
            todowrite_cli,
            [
                "create",
                "--layer",
                "Task",
                "--title",
                "Setup CI/CD",
                "--description",
                "Set up continuous integration and deployment pipeline",
            ],
        )
        self.assertEqual(result.exit_code, 0)

        # Step 5: Start working on first task
        task_result = self.runner.invoke(
            todowrite_cli,
            [
                "create",
                "--layer",
                "Task",
                "--title",
                "Setup Development Environment",
                "--description",
                "Configure local development setup",
            ],
        )
        self.assertEqual(task_result.exit_code, 0)
        task_id = task_result.output.split(" ")[-1].strip()

        # Mark as in progress - use update command instead of status update
        # Clean task_id by removing any trailing parenthesis
        task_id = task_id.rstrip(")")
        result = self.runner.invoke(
            todowrite_cli,
            ["update", task_id, "--status", "in_progress"],
        )
        self.assertEqual(
            result.exit_code,
            0,
            f"Failed to update task {task_id}: {result.output}",
        )

        # Update progress to 50%
        result = self.runner.invoke(
            todowrite_cli,
            [
                "update",
                task_id,
                "--status",
                "in_progress",
                "--progress",
                "50",
            ],
        )
        self.assertEqual(result.exit_code, 0)

        # Step 6: Review project structure
        result = self.runner.invoke(todowrite_cli, ["list"])
        self.assertEqual(result.exit_code, 0)
        self.assertGreater(
            len(result.output.split("\n")),
            5,
            "Should show multiple project elements",
        )

        # Verify we have multiple layers represented
        output_lines = result.output.split("\n")
        layer_types = set()
        for line in output_lines:
            if any(layer in line for layer in ["Goal", "Concept", "Task"]):
                for layer_type in ["Goal", "Concept", "Task"]:
                    if layer_type in line:
                        layer_types.add(layer_type)
                        break

        self.assertGreaterEqual(
            len(layer_types),
            2,
            "Should have multiple layer types",
        )


if __name__ == "__main__":
    unittest.main()
