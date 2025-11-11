from __future__ import annotations

import os
import re
import shutil
import unittest
from pathlib import Path

from click.testing import CliRunner
from sqlalchemy import delete
from todowrite_cli.main import cli

from todowrite import ToDoWrite
from todowrite.database.models import Artifact, node_labels
from todowrite.database.models import Command as DBCommand
from todowrite.database.models import Link as DBLink
from todowrite.database.models import Node as DBNode


class TestCli(unittest.TestCase):
    app: ToDoWrite

    @classmethod
    def setUpClass(cls) -> None:
        """Initialize the application with SQLite for testing."""
        # Use SQLite for testing to avoid PostgreSQL dependency
        db_url = "sqlite:///test_cli.db"
        cls.app = ToDoWrite(
            db_url,
            auto_import=False,
        )  # Disable auto-import for cleaner tests

    @classmethod
    def tearDownClass(cls) -> None:
        """Clean up test files and directories."""
        # Remove test database files if they exist
        test_files = [
            "test_cli.db",
            "test.db",
            "test_validation.db",
            ".todowrite.db",
            "todowrite.db",
            "todos.db",
            "todowrite/todos.db",
        ]

        for file_path in test_files:
            if Path(file_path).exists():
                try:
                    Path(file_path).unlink()
                    print(f"🧹 Removed test file: {file_path}")
                except OSError as e:
                    print(f"⚠️  Could not remove {file_path}: {e}")

        # Remove cache directories
        cache_dirs = [
            ".pytest_cache",
            ".pyright_cache",
            "__pycache__",
            "tests/__pycache__",
        ]

        for cache_dir in cache_dirs:
            if Path(cache_dir).exists():
                try:
                    shutil.rmtree(cache_dir)
                    print(f"🧹 Removed cache directory: {cache_dir}")
                except OSError as e:
                    print(f"⚠️  Could not remove {cache_dir}: {e}")

        # Remove results directory if it exists
        if Path("results").exists():
            try:
                shutil.rmtree("results")
                print("🧹 Removed results directory")
            except OSError as e:
                print(f"⚠️  Could not remove results directory: {e}")

        # Remove trace directory if it exists
        if Path("trace").exists():
            try:
                shutil.rmtree("trace")
                print("🧹 Removed trace directory")
            except OSError as e:
                print(f"⚠️  Could not remove trace directory: {e}")

        # Remove any other temporary files that might be created
        temp_patterns = ["*.tmp", "*.log", "temp_*"]
        for pattern in temp_patterns:
            temp_files: list[Path] = list(Path().glob(pattern))
            for temp_file in temp_files:
                try:
                    if temp_file.is_file():
                        temp_file.unlink()
                        print(f"🧹 Removed temporary file: {temp_file}")
                except OSError as e:
                    print(f"⚠️  Could not remove {temp_file}: {e}")

    def setUp(self) -> None:
        self.runner = CliRunner()
        # The CLI will use the environment variable for the database URL
        os.environ["TODOWRITE_DATABASE_URL"] = "sqlite:///test_cli.db"
        self.app.init_database()

    def tearDown(self) -> None:
        with self.app.get_db_session() as session:
            # Delete in proper order to avoid foreign key constraint violations
            session.execute(delete(node_labels))
            session.execute(delete(Artifact))
            session.execute(delete(DBCommand))
            session.execute(delete(DBLink))
            session.execute(delete(DBNode))

    def test_init_command(self) -> None:
        """Test the init command."""
        result = self.runner.invoke(cli, ["init"])
        self.assertEqual(result.exit_code, 0)
        # The output may include auto-import messages, so just check that it ends with the expected message
        self.assertTrue(
            result.output.endswith("✓ Database initialized successfully!\n"),
        )

    def test_create_command(self) -> None:
        """Test the create command."""
        result = self.runner.invoke(cli, ["init"])
        self.assertEqual(result.exit_code, 0)

        result = self.runner.invoke(
            cli,
            [
                "create",
                "--layer",
                "Goal",
                "--title",
                "Test Goal",
                "--description",
                "This is a test goal.",
            ],
        )
        if result.exit_code != 0:
            print(f"CLI Output: {result.output}")
            print(f"CLI Exception: {result.exception}")
        self.assertEqual(result.exit_code, 0)
        self.assertIn("Created Goal:", result.output)

    def test_get_command(self) -> None:
        """Test the get command."""
        result = self.runner.invoke(cli, ["init"])
        self.assertEqual(result.exit_code, 0)

        result = self.runner.invoke(
            cli,
            [
                "create",
                "--layer",
                "Goal",
                "--title",
                "Test Goal",
                "--description",
                "This is a test goal.",
            ],
        )
        if result.exit_code != 0:
            print(f"CLI Output: {result.output}")
            print(f"CLI Exception: {result.exception}")
        self.assertEqual(result.exit_code, 0)
        # Extract node ID from output like "Created Goal: Test Goal (ID: GOAL-A58B86E71041)"
        match = re.search(r"\(ID: ([^)]+)\)", result.output)
        node_id = match.group(1) if match else result.output.split(" ")[-1].strip()

        result = self.runner.invoke(cli, ["get", node_id])
        self.assertEqual(result.exit_code, 0)
        self.assertIn(node_id, result.output)

    def test_list_command(self) -> None:
        """Test the list command."""
        result = self.runner.invoke(cli, ["init"])
        self.assertEqual(result.exit_code, 0)

        result = self.runner.invoke(
            cli,
            [
                "create",
                "--layer",
                "Goal",
                "--title",
                "Test Goal",
                "--description",
                "This is a test goal.",
            ],
        )
        if result.exit_code != 0:
            print(f"CLI Output: {result.output}")
            print(f"CLI Exception: {result.exception}")
        self.assertEqual(result.exit_code, 0)

        result = self.runner.invoke(cli, ["list"])
        self.assertEqual(result.exit_code, 0)
        self.assertIn("Goal", result.output)
        self.assertIn("Test Goal", result.output)


if __name__ == "__main__":
    unittest.main()
