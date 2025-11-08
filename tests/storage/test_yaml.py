"""
YAML Storage Tests

Tests for YAML storage operations, file management, and import/export functionality.
"""

import shutil
import tempfile
import unittest
from pathlib import Path

import yaml

from todowrite.core import ToDoWrite
from todowrite.storage.yaml_manager import YAMLManager
from todowrite.storage.yaml_storage import YAMLStorage


class TestYAMLStorage(unittest.TestCase):
    """Test YAML storage functionality."""

    def setUp(self) -> None:
        """Set up test environment."""
        self.temp_dir = tempfile.mkdtemp()
        self.yaml_base_path = Path(self.temp_dir) / "configs"
        self.yaml_base_path.mkdir(parents=True)
        self.yaml_storage = YAMLStorage(str(self.yaml_base_path))

    def tearDown(self) -> None:
        """Clean up test environment."""
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_yaml_directory_creation(self) -> None:
        """Test YAML directory structure creation."""
        self.assertTrue(self.yaml_base_path.exists())

        plans_dir = self.yaml_base_path / "plans"
        commands_dir = self.yaml_base_path / "commands"

        # Should create directories on first access
        self.assertTrue(plans_dir.exists())
        self.assertTrue(commands_dir.exists())

    def test_save_and_load_node(self) -> None:
        """Test saving and loading a single node."""
        node_data = {
            "id": "GOAL-001",
            "layer": "Goal",
            "title": "Test Goal",
            "description": "A test goal",
            "status": "planned",
            "progress": 0,
            "links": {"parents": [], "children": []},
            "metadata": {
                "owner": "test-user",
                "labels": ["important"],
                "severity": "med",
                "work_type": "architecture",
            },
        }

        # Save node
        self.yaml_storage.save_node(node_data)

        # Load node
        loaded_node = self.yaml_storage.load_node("GOAL-001")

        self.assertIsNotNone(loaded_node)
        self.assertEqual(loaded_node.id, "GOAL-001")
        self.assertEqual(loaded_node.title, "Test Goal")
        self.assertEqual(loaded_node.layer, "Goal")
        self.assertEqual(loaded_node.metadata.owner, "test-user")

    def test_save_and_load_all_nodes(self) -> None:
        """Test loading all nodes from YAML storage."""
        # Create test nodes
        nodes_data = [
            {
                "id": "GOAL-001",
                "layer": "Goal",
                "title": "Goal 1",
                "description": "First goal",
                "links": {"parents": [], "children": []},
                "metadata": {"owner": "test", "labels": []},
            },
            {
                "id": "TSK-001",
                "layer": "Task",
                "title": "Task 1",
                "description": "First task",
                "links": {"parents": [], "children": []},
                "metadata": {"owner": "test", "labels": []},
            },
            {
                "id": "CON-001",
                "layer": "Concept",
                "title": "Concept 1",
                "description": "First concept",
                "links": {"parents": [], "children": []},
                "metadata": {"owner": "test", "labels": []},
            },
        ]

        # Save all nodes
        saved_nodes = []
        for node_data in nodes_data:
            node = self.yaml_storage.save_node(node_data)
            saved_nodes.append(node)

        # Load all nodes
        all_nodes = self.yaml_storage.load_all_nodes()

        self.assertEqual(len(all_nodes), 3)
        self.assertIn("Goal", all_nodes)
        self.assertIn("Task", all_nodes)
        self.assertIn("Concept", all_nodes)

        # Verify count
        self.assertEqual(len(all_nodes["Goal"]), 1)
        self.assertEqual(len(all_nodes["Task"]), 1)
        self.assertEqual(len(all_nodes["Concept"]), 1)

    def test_update_node(self) -> None:
        """Test updating an existing node."""
        # Create initial node
        node_data = {
            "id": "GOAL-001",
            "layer": "Goal",
            "title": "Original Goal",
            "description": "Original description",
            "links": {"parents": [], "children": []},
            "metadata": {"owner": "test", "labels": []},
        }

        self.yaml_storage.save_node(node_data)

        # Update node
        updated_data = node_data.copy()
        updated_data["title"] = "Updated Goal"
        updated_data["progress"] = 50
        updated_data["metadata"]["owner"] = "updated-user"

        updated_node = self.yaml_storage.update_node("GOAL-001", updated_data)

        self.assertIsNotNone(updated_node)
        self.assertEqual(updated_node.title, "Updated Goal")
        self.assertEqual(updated_node.progress, 50)
        self.assertEqual(updated_node.metadata.owner, "updated-user")

    def test_delete_node(self) -> None:
        """Test deleting a node."""
        # Create node
        node_data = {
            "id": "GOAL-001",
            "layer": "Goal",
            "title": "Test Goal",
            "description": "Test description",
            "links": {"parents": [], "children": []},
            "metadata": {"owner": "test", "labels": []},
        }

        self.yaml_storage.save_node(node_data)

        # Verify node exists
        loaded_node = self.yaml_storage.load_node("GOAL-001")
        self.assertIsNotNone(loaded_node)

        # Delete node
        self.yaml_storage.delete_node("GOAL-001")

        # Verify node is deleted
        deleted_node = self.yaml_storage.load_node("GOAL-001")
        self.assertIsNone(deleted_node)

    def test_nonexistent_node_operations(self) -> None:
        """Test operations on non-existent nodes."""
        # Load non-existent node
        node = self.yaml_storage.load_node("NONEXISTENT")
        self.assertIsNone(node)

        # Update non-existent node
        node_data = {
            "id": "NONEXISTENT",
            "layer": "Goal",
            "title": "Test",
            "description": "Test",
            "links": {"parents": [], "children": []},
            "metadata": {"owner": "test", "labels": []},
        }

        updated_node = self.yaml_storage.update_node("NONEXISTENT", node_data)
        self.assertIsNone(updated_node)

    def test_layer_directory_organization(self) -> None:
        """Test that nodes are stored in appropriate layer directories."""
        # Create nodes of different layers
        nodes_data = [
            {
                "id": "GOAL-001",
                "layer": "Goal",
                "title": "Goal 1",
                "description": "Goal description",
                "links": {"parents": [], "children": []},
                "metadata": {"owner": "test", "labels": []},
            },
            {
                "id": "TSK-001",
                "layer": "Task",
                "title": "Task 1",
                "description": "Task description",
                "links": {"parents": [], "children": []},
                "metadata": {"owner": "test", "labels": []},
            },
            {
                "id": "CMD-001",
                "layer": "Command",
                "title": "Command 1",
                "description": "Command description",
                "links": {"parents": [], "children": []},
                "metadata": {"owner": "test", "labels": []},
                "command": {
                    "ac_ref": "AC-001",
                    "run": {"shell": "echo hello"},
                },
            },
        ]

        # Save nodes
        for node_data in nodes_data:
            self.yaml_storage.save_node(node_data)

        # Check file locations
        plans_dir = self.yaml_base_path / "plans"
        commands_dir = self.yaml_base_path / "commands"

        # Goal should be in plans/goals
        goal_file = plans_dir / "goals" / "GOAL-001.yaml"
        self.assertTrue(goal_file.exists())

        # Task should be in plans/tasks
        task_file = plans_dir / "tasks" / "TSK-001.yaml"
        self.assertTrue(task_file.exists())

        # Command should be in commands
        cmd_file = commands_dir / "CMD-001.yaml"
        self.assertTrue(cmd_file.exists())

    def test_yaml_file_format(self) -> None:
        """Test YAML file format and content."""
        node_data = {
            "id": "GOAL-001",
            "layer": "Goal",
            "title": "Test Goal",
            "description": "Test description",
            "status": "in_progress",
            "progress": 50,
            "started_date": "2023-01-01",
            "completion_date": "",
            "links": {"parents": [], "children": []},
            "metadata": {
                "owner": "test-user",
                "labels": ["urgent", "important"],
                "severity": "high",
                "work_type": "implementation",
                "assignee": "developer1",
            },
        }

        # Save node
        self.yaml_storage.save_node(node_data)

        # Read YAML file directly
        goal_file = self.yaml_base_path / "plans" / "goals" / "GOAL-001.yaml"
        self.assertTrue(goal_file.exists())

        with open(goal_file) as f:
            file_content = yaml.safe_load(f)

        # Verify content
        self.assertEqual(file_content["id"], "GOAL-001")
        self.assertEqual(file_content["layer"], "Goal")
        self.assertEqual(file_content["title"], "Test Goal")
        self.assertEqual(
            file_content["metadata"]["labels"],
            ["urgent", "important"],
        )


class TestYAMLManager(unittest.TestCase):
    """Test YAML manager functionality."""

    def setUp(self) -> None:
        """Set up test environment."""
        self.temp_dir = tempfile.mkdtemp()
        self.yaml_base_path = Path(self.temp_dir) / "configs"
        self.yaml_base_path.mkdir(parents=True)

    def tearDown(self) -> None:
        """Clean up test environment."""
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_yaml_discovery(self) -> None:
        """Test YAML file discovery."""
        manager = YAMLManager()
        manager.yaml_base_path = self.yaml_base_path
        manager.plans_path = self.yaml_base_path / "plans"
        manager.commands_path = self.yaml_base_path / "commands"

        # Create test files
        (self.yaml_base_path / "plans" / "goals").mkdir(parents=True)
        (self.yaml_base_path / "plans" / "tasks").mkdir(parents=True)
        (self.yaml_base_path / "commands").mkdir(parents=True)

        # Create test YAML files
        goal_file = self.yaml_base_path / "plans" / "goals" / "GOAL-001.yaml"
        task_file = self.yaml_base_path / "plans" / "tasks" / "TSK-001.yaml"
        cmd_file = self.yaml_base_path / "commands" / "CMD-001.yaml"

        for file_path in [goal_file, task_file, cmd_file]:
            with open(file_path, "w") as f:
                yaml.dump(
                    {
                        "id": file_path.stem,
                        "layer": (
                            file_path.parent.parent.name
                            if file_path.parent.name != "commands"
                            else "Command"
                        ),
                        "title": f"Test {file_path.stem}",
                        "description": "Test description",
                        "links": {"parents": [], "children": []},
                        "metadata": {"owner": "test", "labels": []},
                    },
                    f,
                )

        # Discover files
        yaml_files = manager.get_yaml_files()

        self.assertIn("Goal", yaml_files)
        self.assertIn("Task", yaml_files)
        self.assertIn("Command", yaml_files)
        self.assertEqual(len(yaml_files["Goal"]), 1)
        self.assertEqual(len(yaml_files["Task"]), 1)
        self.assertEqual(len(yaml_files["Command"]), 1)

    def test_yaml_import(self) -> None:
        """Test YAML import functionality."""
        # Create ToDoWrite app with YAML storage
        app = ToDoWrite("sqlite:///:memory:")
        app.init_database()

        manager = YAMLManager(app)
        manager.yaml_base_path = self.yaml_base_path
        manager.plans_path = self.yaml_base_path / "plans"
        manager.commands_path = self.yaml_base_path / "commands"

        # Create test YAML file
        goal_file = (
            self.yaml_base_path / "plans" / "goals" / "GOAL-IMPORT-001.yaml"
        )
        goal_file.parent.mkdir(parents=True)

        goal_data = {
            "id": "GOAL-IMPORT-001",
            "layer": "Goal",
            "title": "Imported Goal",
            "description": "Goal imported from YAML",
            "links": {"parents": [], "children": []},
            "metadata": {
                "owner": "import-user",
                "labels": ["imported"],
                "severity": "med",
                "work_type": "architecture",
            },
        }

        with open(goal_file, "w") as f:
            yaml.dump(goal_data, f)

        # Import YAML file
        results = manager.import_yaml_files()

        self.assertEqual(results["total_files"], 1)
        self.assertEqual(results["total_imported"], 1)
        self.assertEqual(len(results["errors"]), 0)

        # Verify import
        imported_node = app.get_node("GOAL-IMPORT-001")
        self.assertIsNotNone(imported_node)
        self.assertEqual(imported_node.title, "Imported Goal")
        self.assertEqual(imported_node.metadata.owner, "import-user")

    def test_yaml_export(self) -> None:
        """Test YAML export functionality."""
        # Create ToDoWrite app
        app = ToDoWrite("sqlite:///:memory:")
        app.init_database()

        # Create test node
        node_data = {
            "id": "GOAL-EXPORT-001",
            "layer": "Goal",
            "title": "Export Goal",
            "description": "Goal to be exported",
            "links": {"parents": [], "children": []},
            "metadata": {"owner": "export-user", "labels": ["exported"]},
        }

        app.create_node(node_data)

        # Export to YAML
        manager = YAMLManager(app)
        output_dir = Path(self.temp_dir) / "exported"
        results = manager.export_to_yaml(output_dir)

        self.assertEqual(results["total_nodes"], 1)
        self.assertEqual(results["total_exported"], 1)
        self.assertEqual(len(results["errors"]), 0)

        # Verify exported file
        export_file = output_dir / "plans" / "goals" / "GOAL-EXPORT-001.yaml"
        self.assertTrue(export_file.exists())

        with open(export_file) as f:
            exported_data = yaml.safe_load(f)

        self.assertEqual(exported_data["id"], "GOAL-EXPORT-001")
        self.assertEqual(exported_data["title"], "Export Goal")

    def test_yaml_sync_check(self) -> None:
        """Test YAML synchronization check."""
        app = ToDoWrite("sqlite:///:memory:")
        app.init_database()

        manager = YAMLManager(app)
        manager.yaml_base_path = self.yaml_base_path
        manager.plans_path = self.yaml_base_path / "plans"
        manager.commands_path = self.yaml_base_path / "commands"

        # Create node in database
        node_data = {
            "id": "GOAL-SYNC-001",
            "layer": "Goal",
            "title": "Database Goal",
            "description": "Goal in database",
            "links": {"parents": [], "children": []},
            "metadata": {"owner": "db-user", "labels": []},
        }
        app.create_node(node_data)

        # Create YAML file
        goal_file = (
            self.yaml_base_path / "plans" / "goals" / "GOAL-SYNC-002.yaml"
        )
        goal_file.parent.mkdir(parents=True)

        yaml_data = {
            "id": "GOAL-SYNC-002",
            "layer": "Goal",
            "title": "YAML Goal",
            "description": "Goal in YAML",
            "links": {"parents": [], "children": []},
            "metadata": {"owner": "yaml-user", "labels": []},
        }

        with open(goal_file, "w") as f:
            yaml.dump(yaml_data, f)

        # Check sync
        sync_status = manager.check_yaml_sync()

        self.assertIn("GOAL-SYNC-001", sync_status["database_only"])
        self.assertIn("GOAL-SYNC-002", sync_status["yaml_only"])
        self.assertEqual(len(sync_status["both"]), 0)


if __name__ == "__main__":
    unittest.main()
