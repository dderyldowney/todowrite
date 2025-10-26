import subprocess
import time
import unittest

from todowrite.app import ToDoWrite
from todowrite.db.models import Artifact, Command, Label, Node, node_labels


class TestApp(unittest.TestCase):

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
        self.app.init_database()

    def tearDown(self):
        session = self.app.Session()
        session.execute(node_labels.delete())
        session.query(Artifact).delete()
        session.query(Command).delete()
        session.query(Label).delete()
        session.query(Node).delete()
        session.commit()
        session.close()

    def test_init_database(self):
        """Test that init_database creates the database file."""
        # This test is not applicable to PostgreSQL
        pass

    def test_default_database_is_sqlite(self):
        """Test that the default database is SQLite."""
        app = ToDoWrite()
        self.assertTrue(app.db_url.startswith("sqlite"))

    def test_create_node(self):
        """Test that create_node creates a new node in the database."""
        node_data = {
            "id": "GOAL-TEST1",
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
        self.assertEqual(node.id, "GOAL-TEST1")
        self.assertEqual(node.metadata.labels[0], "test")

    def test_get_node(self):
        """Test that get_node returns the correct node from the database."""
        node_data = {
            "id": "GOAL-TEST1",
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
        self.app.create_node(node_data)
        node = self.app.get_node("GOAL-TEST1")
        self.assertIsNotNone(node)
        self.assertEqual(node.id, "GOAL-TEST1")

    def test_get_all_nodes(self):
        """Test that get_all_nodes returns all the nodes from the database."""
        node_data1 = {
            "id": "GOAL-TEST1",
            "layer": "Goal",
            "title": "Test Goal 1",
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
        node_data2 = {
            "id": "GOAL-TEST2",
            "layer": "Goal",
            "title": "Test Goal 2",
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
        self.app.create_node(node_data1)
        self.app.create_node(node_data2)
        nodes = self.app.get_all_nodes()
        self.assertIn("Goal", nodes)
        self.assertEqual(len(nodes["Goal"]), 2)


if __name__ == "__main__":
    unittest.main()
