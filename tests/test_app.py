import os
import unittest
from todowrite.app import ToDoWrite

class TestApp(unittest.TestCase):

    def setUp(self):
        self.db_path = "todowrite.db"
        self.app = ToDoWrite(f"sqlite:///{self.db_path}")

    def tearDown(self):
        if os.path.exists(self.db_path):
            os.remove(self.db_path)

    def test_init_database(self):
        """Test that init_database creates the database file."""
        self.app.init_database()
        self.assertTrue(os.path.exists(self.db_path))

    def test_default_database_is_sqlite(self):
        """Test that the default database is SQLite."""
        app = ToDoWrite()
        self.assertTrue(app.db_url.startswith("sqlite"))

    def test_create_node(self):
        """Test that create_node creates a new node in the database."""
        self.app.init_database()
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
        self.assertEqual(node.metadata.labels[0], "test")

    def test_get_node(self):
        """Test that get_node returns the correct node from the database."""
        self.app.init_database()
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
        self.app.create_node(node_data)
        node = self.app.get_node("goal1")
        self.assertIsNotNone(node)
        self.assertEqual(node.id, "goal1")

    def test_get_all_nodes(self):
        """Test that get_all_nodes returns all the nodes from the database."""
        self.app.init_database()
        node_data1 = {
            "id": "goal1",
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
            "id": "goal2",
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
