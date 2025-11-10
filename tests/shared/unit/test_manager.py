"""
Simplified manager tests that work with current architecture.

Tests core functionality without complex database setup.
"""

import sys
from pathlib import Path

# Add project root to sys.path
project_root = Path(__file__).resolve().parent.parent.parent.parent
sys.path.insert(0, str(project_root))

import unittest
from unittest.mock import patch

from todowrite.core.app import (
    create_node,
    get_node,
    list_nodes,
    search_nodes,
)


class TestTodosManager(unittest.TestCase):
    """Simplified manager tests using current architecture."""

    def setUp(self):
        """Set up test data."""
        self.test_node_data = {
            "id": "GOAL-TEST123",
            "title": "Test Goal",
            "description": "A test goal for unit testing",
            "layer": "Goal",
            "status": "planned",
            "metadata": {
                "created_at": "2024-01-01T00:00:00Z",
                "updated_at": "2024-01-01T00:00:00Z",
                "version": 1,
            },
            "links": {"parents": [], "children": []},
        }

    def test_create_node(self):
        """Test creating a node."""
        node = create_node(self.test_node_data)
        self.assertEqual(node.id, "GOAL-TEST123")
        self.assertEqual(node.title, "Test Goal")
        self.assertEqual(node.layer, "Goal")

    def test_get_node(self):
        """Test retrieving a node."""
        # First create a node
        created_node = create_node(self.test_node_data)

        # Then retrieve it
        retrieved_node = get_node(created_node.id)
        self.assertIsNotNone(retrieved_node)
        self.assertEqual(retrieved_node.id, created_node.id)
        self.assertEqual(retrieved_node.title, "Test Goal")

    def test_list_nodes(self):
        """Test listing all nodes."""
        # Create a test node first
        create_node(self.test_node_data)

        # List nodes
        result = list_nodes()
        self.assertIsInstance(result, dict)
        self.assertIn("nodes", result)

    def test_search_nodes(self):
        """Test searching nodes."""
        # Create a test node first
        create_node(self.test_node_data)

        # Search for nodes
        result = search_nodes("Test")
        self.assertIsInstance(result, dict)
        self.assertIn("nodes", result)


if __name__ == "__main__":
    unittest.main()