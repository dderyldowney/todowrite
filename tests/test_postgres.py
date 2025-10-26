import os
import unittest
import subprocess
import time
from todowrite.app import ToDoWrite


class TestPostgres(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """Start the PostgreSQL container."""
        subprocess.run(["docker-compose", "up", "-d"], check=True)
        # Wait for the database to be ready
        time.sleep(10)

    @classmethod
    def tearDownClass(cls):
        """Stop the PostgreSQL container."""
        subprocess.run(["docker-compose", "down"], check=True)

    def setUp(self):
        db_url = "postgresql://todowrite:todowrite@localhost:5432/todowrite"
        self.app = ToDoWrite(db_url)
        self.app.init_database()

    def tearDown(self):
        # The database is cleaned up by the tearDownClass method
        pass

    def test_postgres_integration(self):
        """Test the PostgreSQL integration."""
        node_data = {
            "id": "goal1",
            "layer": "Goal",
            "title": "Test Goal",
            "description": "A test goal",
            "status": "in_progress",
            "links": {"parents": [], "children": []},
            "metadata": {
                "owner": "test",
                "labels": ["test"],
                "severity": "high",
                "work_type": "architecture",
            },
        }
        node = self.app.create_node(node_data)
        self.assertEqual(node.id, "goal1")

        retrieved_node = self.app.get_node("goal1")
        self.assertIsNotNone(retrieved_node)
        self.assertEqual(retrieved_node.id, "goal1")

        nodes = self.app.get_all_nodes()
        self.assertIn("Goal", nodes)
        self.assertEqual(len(nodes["Goal"]), 1)


if __name__ == "__main__":
    unittest.main()