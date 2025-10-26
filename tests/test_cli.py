import os
import subprocess
import time
import unittest

from click.testing import CliRunner

from todowrite.app import ToDoWrite
from todowrite.cli import cli
from todowrite.db.models import (Artifact, Command, Label, Link, Node,
                                 node_labels)


class TestCli(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """Start the PostgreSQL container."""
        subprocess.run(["docker-compose", "up", "-d"], check=True)
        # Wait for the database to be ready
        time.sleep(10)
        db_url = "postgresql://todowrite:todowrite@localhost:5432/todowrite"
        cls.app = ToDoWrite(db_url)

    @classmethod
    def tearDownClass(cls):
        """Stop the PostgreSQL container."""
        subprocess.run(["docker-compose", "down"], check=True)

    def setUp(self):
        self.runner = CliRunner()
        # The CLI will use the environment variable for the database URL
        os.environ["TODOWRITE_DATABASE_URL"] = (
            "postgresql://todowrite:todowrite@localhost:5432/todowrite"
        )
        self.app.init_database()

    def tearDown(self):
        session = self.app.Session()
        session.execute(node_labels.delete())
        session.query(Artifact).delete()
        session.query(Command).delete()
        session.query(Link).delete()
        session.query(Label).delete()
        session.query(Node).delete()
        session.commit()
        session.close()

    def test_init_command(self):
        """Test the init command."""
        result = self.runner.invoke(cli, ["init"])
        self.assertEqual(result.exit_code, 0)
        self.assertEqual(result.output, "Database initialized.\n")

    def test_create_command(self):
        """Test the create command."""
        result = self.runner.invoke(cli, ["init"])
        self.assertEqual(result.exit_code, 0)

        result = self.runner.invoke(
            cli, ["create", "Goal", "Test Goal", "This is a test goal."]
        )
        if result.exit_code != 0:
            print(f"CLI Output: {result.output}")
            print(f"CLI Exception: {result.exception}")
        self.assertEqual(result.exit_code, 0)
        self.assertIn("Node created:", result.output)

    def test_get_command(self):
        """Test the get command."""
        result = self.runner.invoke(cli, ["init"])
        self.assertEqual(result.exit_code, 0)

        result = self.runner.invoke(
            cli, ["create", "Goal", "Test Goal", "This is a test goal."]
        )
        if result.exit_code != 0:
            print(f"CLI Output: {result.output}")
            print(f"CLI Exception: {result.exception}")
        self.assertEqual(result.exit_code, 0)
        node_id = result.output.split(" ")[-1].strip()

        result = self.runner.invoke(cli, ["get", node_id])
        self.assertEqual(result.exit_code, 0)
        self.assertIn(f"ID: {node_id}", result.output)

    def test_list_command(self):
        """Test the list command."""
        result = self.runner.invoke(cli, ["init"])
        self.assertEqual(result.exit_code, 0)

        result = self.runner.invoke(
            cli, ["create", "Goal", "Test Goal", "This is a test goal."]
        )
        if result.exit_code != 0:
            print(f"CLI Output: {result.output}")
            print(f"CLI Exception: {result.exception}")
        self.assertEqual(result.exit_code, 0)

        result = self.runner.invoke(cli, ["list"])
        self.assertEqual(result.exit_code, 0)
        self.assertIn("--- Goal ---", result.output)
        self.assertIn("Test Goal", result.output)


if __name__ == "__main__":
    unittest.main()
