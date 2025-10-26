import os
import unittest
from click.testing import CliRunner

from todowrite.cli import cli


class TestCli(unittest.TestCase):

    def setUp(self):
        self.runner = CliRunner()
        self.db_path = "todowrite.db"

    def tearDown(self):
        if os.path.exists(self.db_path):
            os.remove(self.db_path)

    def test_init_command(self):
        """Test the init command."""
        result = self.runner.invoke(cli, ["init"])
        self.assertEqual(result.exit_code, 0)
        self.assertEqual(result.output, "Database initialized.\n")
        self.assertTrue(os.path.exists(self.db_path))

    def test_create_command(self):
        """Test the create command."""
        result = self.runner.invoke(cli, ["init"])
        self.assertEqual(result.exit_code, 0)

        result = self.runner.invoke(cli, ["create", "Goal", "Test Goal", "This is a test goal."])
        self.assertEqual(result.exit_code, 0)
        self.assertIn("Node created:", result.output)

    def test_get_command(self):
        """Test the get command."""
        result = self.runner.invoke(cli, ["init"])
        self.assertEqual(result.exit_code, 0)

        result = self.runner.invoke(cli, ["create", "Goal", "Test Goal", "This is a test goal."])
        self.assertEqual(result.exit_code, 0)
        node_id = result.output.split(" ")[-1].strip()

        result = self.runner.invoke(cli, ["get", node_id])
        self.assertEqual(result.exit_code, 0)
        self.assertIn(f"ID: {node_id}", result.output)

    def test_list_command(self):
        """Test the list command."""
        result = self.runner.invoke(cli, ["init"])
        self.assertEqual(result.exit_code, 0)

        result = self.runner.invoke(cli, ["create", "Goal", "Test Goal", "This is a test goal."])
        self.assertEqual(result.exit_code, 0)

        result = self.runner.invoke(cli, ["list"])
        self.assertEqual(result.exit_code, 0)
        self.assertIn("--- Goal ---", result.output)
        self.assertIn("Test Goal", result.output)


if __name__ == "__main__":
    unittest.main()