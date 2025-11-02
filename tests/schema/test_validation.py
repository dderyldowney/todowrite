"""
Schema Validation Tests

Tests for JSON schema validation, node validation, and data integrity.
"""

import unittest
from pathlib import Path

from todowrite.core import ToDoWrite
from todowrite.storage.validators import (
    get_schema_compliance_report,
    validate_database_schema,
    validate_node_data,
    validate_yaml_files,
)


class TestSchemaValidation(unittest.TestCase):
    """Test schema validation functionality."""

    def setUp(self) -> None:
        """Set up test environment."""
        self.app = ToDoWrite()

    def test_node_data_validation(self) -> None:
        """Test node data validation against schema."""
        # Valid node data
        valid_node = {
            "id": "GOAL-001",
            "layer": "Goal",
            "title": "Test Goal",
            "description": "A test goal",
            "status": "planned",
            "links": {"parents": [], "children": []},
            "metadata": {
                "owner": "test-user",
                "labels": [],
                "severity": "medium",
                "work_type": "architecture",
            },
        }

        # Should pass validation
        try:
            validate_node_data(valid_node)
        except Exception as e:
            self.fail(f"Valid node data should not raise exception: {e}")

        # Invalid node data - missing required field
        invalid_node = valid_node.copy()
        invalid_node.pop("title", None)

        with self.assertRaises(Exception):
            validate_node_data(invalid_node)

        # Invalid node data - wrong layer type
        invalid_node_layer = valid_node.copy()
        invalid_node_layer["layer"] = "InvalidLayer"

        with self.assertRaises(Exception):
            validate_node_data(invalid_node_layer)

        # Invalid node data - empty work_type
        invalid_node_work_type = valid_node.copy()
        invalid_node_work_type["metadata"]["work_type"] = ""

        with self.assertRaises(Exception):
            validate_node_data(invalid_node_work_type)

    def test_node_id_validation(self) -> None:
        """Test node ID format validation."""
        # Valid IDs
        valid_ids = [
            "GOAL-001",
            "CON-ABC123",
            "TSK-test_node",
            "CMD-A1B2C3D4",
            "AC-valid-123",
        ]

        for valid_id in valid_ids:
            node_data = {
                "id": valid_id,
                "layer": "Goal",  # Use valid layer for basic validation
                "title": "Test",
                "description": "Test node",
                "links": {"parents": [], "children": []},
                "metadata": {"owner": "test", "labels": []},
            }
            try:
                validate_node_data(node_data)
            except Exception as e:
                self.fail(f"Valid ID {valid_id} should not raise exception: {e}")

        # Invalid IDs
        invalid_ids = [
            "invalid-id",
            "GOAL001",  # Missing hyphen
            "CON-",  # Missing suffix
            "123INVALID",
            "GOAL@123",  # Invalid character
        ]

        for invalid_id in invalid_ids:
            node_data = {
                "id": invalid_id,
                "layer": "Goal",
                "title": "Test",
                "description": "Test node",
                "links": {"parents": [], "children": []},
                "metadata": {"owner": "test", "labels": []},
            }
            with self.assertRaises(Exception):
                validate_node_data(node_data)

    def test_metadata_validation(self) -> None:
        """Test metadata field validation."""
        base_node = {
            "id": "GOAL-001",
            "layer": "Goal",
            "title": "Test Goal",
            "description": "Test goal",
            "links": {"parents": [], "children": []},
            "metadata": {"owner": "test", "labels": []},
        }

        # Valid metadata
        valid_metadata = {
            "owner": "user123",
            "labels": ["urgent", "important"],
            "severity": "high",
            "work_type": "implementation",
            "assignee": "developer1",
        }

        node_data = base_node.copy()
        node_data["metadata"].update(valid_metadata)
        try:
            validate_node_data(node_data)
        except Exception as e:
            self.fail(f"Valid metadata should not raise exception: {e}")

        # Invalid severity
        invalid_severity = valid_metadata.copy()
        invalid_severity["severity"] = "invalid_severity"

        node_data = base_node.copy()
        node_data["metadata"].update(invalid_severity)
        with self.assertRaises(Exception):
            validate_node_data(node_data)

        # Invalid work_type
        invalid_work_type = valid_metadata.copy()
        invalid_work_type["work_type"] = "invalid_work_type"

        node_data = base_node.copy()
        node_data["metadata"].update(invalid_work_type)
        with self.assertRaises(Exception):
            validate_node_data(node_data)

    def test_links_validation(self) -> None:
        """Test links structure validation."""
        base_node = {
            "id": "GOAL-001",
            "layer": "Goal",
            "title": "Test Goal",
            "description": "Test goal",
            "metadata": {"owner": "test", "labels": []},
        }

        # Valid links
        valid_links = {
            "parents": ["GOAL-002", "CON-001"],
            "children": ["TSK-001", "TSK-002"],
        }

        node_data = base_node.copy()
        node_data["links"] = valid_links
        try:
            validate_node_data(node_data)
        except Exception as e:
            self.fail(f"Valid links should not raise exception: {e}")

        # Invalid links structure
        invalid_links = {"invalid_structure": ["GOAL-002"]}

        node_data = base_node.copy()
        node_data["links"] = invalid_links
        with self.assertRaises(Exception):
            validate_node_data(node_data)

        # Invalid parent ID format
        invalid_parent_id = {"parents": ["invalid-id"], "children": []}

        node_data = base_node.copy()
        node_data["links"] = invalid_parent_id
        with self.assertRaises(Exception):
            validate_node_data(node_data)

    def test_command_validation(self) -> None:
        """Test command structure validation."""
        base_node = {
            "id": "CMD-001",
            "layer": "Command",
            "title": "Test Command",
            "description": "Test command",
            "links": {"parents": [], "children": []},
            "metadata": {"owner": "test", "labels": []},
        }

        # Valid command
        valid_command = {
            "ac_ref": "AC-001",
            "run": {"shell": "echo hello", "workdir": "/tmp", "env": {"DEBUG": "true"}},
            "artifacts": ["output.txt", "log.txt"],
        }

        node_data = base_node.copy()
        node_data["command"] = valid_command
        try:
            validate_node_data(node_data)
        except Exception as e:
            self.fail(f"Valid command should not raise exception: {e}")

        # Invalid command - missing ac_ref
        invalid_command = valid_command.copy()
        invalid_command.pop("ac_ref", None)

        node_data = base_node.copy()
        node_data["command"] = invalid_command
        with self.assertRaises(Exception):
            validate_node_data(node_data)

        # Invalid command - missing run shell
        invalid_command_shell = valid_command.copy()
        invalid_command_shell["run"] = {"workdir": "/tmp"}

        node_data = base_node.copy()
        node_data["command"] = invalid_command_shell
        with self.assertRaises(Exception):
            validate_node_data(node_data)


class TestDatabaseSchema(unittest.TestCase):
    """Test database schema validation."""

    def setUp(self) -> None:
        """Set up test database."""
        self.test_db = Path("test_schema.db")
        self.app = ToDoWrite(f"sqlite:///{self.test_db}")
        self.app.init_database()

    def tearDown(self) -> None:
        """Clean up test database."""
        self.test_db.unlink(missing_ok=True)

    def test_database_schema_validation(self) -> None:
        """Test database schema validation."""
        try:
            result = validate_database_schema()
            self.assertIsNotNone(result)
            # Should pass validation for a properly initialized database
        except Exception as e:
            self.fail(f"Database schema validation should not raise exception: {e}")

    def test_schema_compliance_report(self) -> None:
        """Test schema compliance report generation."""
        try:
            report = get_schema_compliance_report()
            self.assertIsInstance(report, dict)
            self.assertIn("summary", report)
            self.assertIn("details", report)
        except Exception as e:
            self.fail(f"Schema compliance report should not raise exception: {e}")


class TestYAMLValidation(unittest.TestCase):
    """Test YAML file validation."""

    def setUp(self) -> None:
        """Set up test YAML files."""
        self.test_dir = Path("test_yaml")
        self.test_dir.mkdir(exist_ok=True)

    def tearDown(self) -> None:
        """Clean up test YAML files."""
        import shutil

        if self.test_dir.exists():
            shutil.rmtree(self.test_dir)

    def test_valid_yaml_file(self) -> None:
        """Test validation of valid YAML files."""
        valid_yaml_content = {
            "id": "GOAL-001",
            "layer": "Goal",
            "title": "Test Goal",
            "description": "Test goal",
            "links": {"parents": [], "children": []},
            "metadata": {
                "owner": "test-user",
                "labels": [],
                "severity": "medium",
                "work_type": "architecture",
            },
        }

        yaml_file = self.test_dir / "valid_goal.yaml"
        with open(yaml_file, "w") as f:
            import yaml

            yaml.dump(valid_yaml_content, f)

        # Should pass validation
        try:
            validate_yaml_files([str(yaml_file)])
        except Exception as e:
            self.fail(f"Valid YAML file should not raise exception: {e}")

    def test_invalid_yaml_file(self) -> None:
        """Test validation of invalid YAML files."""
        invalid_yaml_content = {
            "id": "invalid-id",
            "layer": "Goal",
            "title": "Test Goal",
            # Missing description
            "links": {"parents": [], "children": []},
            "metadata": {"owner": "test", "labels": []},
        }

        yaml_file = self.test_dir / "invalid_goal.yaml"
        with open(yaml_file, "w") as f:
            import yaml

            yaml.dump(invalid_yaml_content, f)

        # Should fail validation
        with self.assertRaises(Exception):
            validate_yaml_files([str(yaml_file)])

    def test_yaml_directory_validation(self) -> None:
        """Test validation of multiple YAML files in a directory."""
        # Create multiple test files
        test_files = [
            (
                "goal1.yaml",
                {
                    "id": "GOAL-001",
                    "layer": "Goal",
                    "title": "Goal 1",
                    "description": "First goal",
                    "links": {"parents": [], "children": []},
                    "metadata": {"owner": "test", "labels": []},
                },
            ),
            (
                "task1.yaml",
                {
                    "id": "TSK-001",
                    "layer": "Task",
                    "title": "Task 1",
                    "description": "First task",
                    "links": {"parents": [], "children": []},
                    "metadata": {"owner": "test", "labels": []},
                },
            ),
            (
                "concept1.yaml",
                {
                    "id": "CON-001",
                    "layer": "Concept",
                    "title": "Concept 1",
                    "description": "First concept",
                    "links": {"parents": [], "children": []},
                    "metadata": {"owner": "test", "labels": []},
                },
            ),
        ]

        for filename, content in test_files:
            yaml_file = self.test_dir / filename
            with open(yaml_file, "w") as f:
                import yaml

                yaml.dump(content, f)

        # Should validate all files
        try:
            validate_yaml_files([str(self.test_dir)])
        except Exception as e:
            self.fail(f"Valid YAML files should not raise exception: {e}")


if __name__ == "__main__":
    unittest.main()
