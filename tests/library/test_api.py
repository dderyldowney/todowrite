"""
Library API Tests

Comprehensive tests for the ToDoWrite library API, covering all public interfaces
and usage patterns for developers using the library as a Python package.
"""

import unittest
from pathlib import Path

from todowrite import (
    ToDoWrite,
    create_node,
    delete_node,
    get_all_nodes,
    get_node,
    link_nodes,
    list_nodes,
    unlink_nodes,
    update_node,
)
from todowrite.core.types import Node


class TestCoreAPI(unittest.TestCase):
    """Test core library API functions."""

    def setUp(self) -> None:
        """Set up test environment."""
        self.test_db = Path("test_api.db")
        self.db_url = f"sqlite:///{self.test_db}"
        self.app = ToDoWrite(self.db_url)
        self.app.init_database()

    def tearDown(self) -> None:
        """Clean up test environment."""
        self.test_db.unlink(missing_ok=True)

    def test_create_node_function(self) -> None:
        """Test the create_node convenience function."""
        node_data = {
            "id": "GOAL-001",
            "layer": "Goal",
            "title": "Test Goal",
            "description": "A test goal for API testing",
            "metadata": {
                "owner": "developer",
                "labels": ["api-test", "important"],
                "severity": "medium",
                "work_type": "architecture",
            },
        }

        node = create_node(self.db_url, node_data)

        self.assertIsNotNone(node)
        self.assertEqual(node.id, "GOAL-001")
        self.assertEqual(node.title, "Test Goal")
        self.assertEqual(node.layer, "Goal")
        self.assertEqual(node.metadata.owner, "developer")

    def test_get_node_function(self) -> None:
        """Test the get_node convenience function."""
        # First create a node
        create_node(
            self.db_url,
            {
                "id": "TSK-001",
                "layer": "Task",
                "title": "Test Task",
                "description": "A test task",
                "metadata": {"owner": "developer", "labels": []},
            },
        )

        # Then retrieve it
        node = get_node(self.db_url, "TSK-001")

        self.assertIsNotNone(node)
        self.assertEqual(node.title, "Test Task")
        self.assertEqual(node.layer, "Task")

    def test_get_nonexistent_node(self) -> None:
        """Test getting a non-existent node."""
        node = get_node(self.db_url, "NONEXISTENT")
        self.assertIsNone(node)

    def test_update_node_function(self) -> None:
        """Test the update_node convenience function."""
        # Create initial node
        create_node(
            self.db_url,
            {
                "id": "GOAL-001",
                "layer": "Goal",
                "title": "Original Goal",
                "description": "Original description",
                "metadata": {"owner": "developer", "labels": []},
            },
        )

        # Update node
        update_data = {
            "id": "GOAL-001",
            "title": "Updated Goal",
            "description": "Updated description",
            "status": "in_progress",
            "progress": 50,
            "metadata": {
                "owner": "updated-developer",
                "labels": ["updated"],
                "severity": "high",
                "work_type": "implementation",
            },
        }

        updated_node = update_node(self.db_url, "GOAL-001", update_data)

        self.assertIsNotNone(updated_node)
        self.assertEqual(updated_node.title, "Updated Goal")
        self.assertEqual(updated_node.status, "in_progress")
        self.assertEqual(updated_node.progress, 50)
        self.assertEqual(updated_node.metadata.owner, "updated-developer")

    def test_delete_node_function(self) -> None:
        """Test the delete_node convenience function."""
        # Create a node
        create_node(
            self.db_url,
            {
                "id": "TSK-001",
                "layer": "Task",
                "title": "Task to Delete",
                "description": "This will be deleted",
                "metadata": {"owner": "developer", "labels": []},
            },
        )

        # Verify it exists
        node = get_node(self.db_url, "TSK-001")
        self.assertIsNotNone(node)

        # Delete it
        result = delete_node(self.db_url, "TSK-001")
        self.assertTrue(result)

        # Verify it's gone
        deleted_node = get_node(self.db_url, "TSK-001")
        self.assertIsNone(deleted_node)

    def test_delete_nonexistent_node(self) -> None:
        """Test deleting a non-existent node."""
        result = delete_node(self.db_url, "NONEXISTENT")
        self.assertFalse(result)

    def test_get_all_nodes_function(self) -> None:
        """Test the get_all_nodes convenience function."""
        # Create multiple nodes
        nodes_to_create = [
            ("GOAL-001", "Goal", "Main Goal"),
            ("CON-001", "Concept", "Main Concept"),
            ("TSK-001", "Task", "Main Task"),
            ("AC-001", "AcceptanceCriteria", "Main AC"),
        ]

        for node_id, layer, title in nodes_to_create:
            create_node(
                self.db_url,
                {
                    "id": node_id,
                    "layer": layer,
                    "title": title,
                    "description": f"Description for {title}",
                    "metadata": {"owner": "developer", "labels": []},
                },
            )

        # Get all nodes
        all_nodes = get_all_nodes(self.db_url)

        self.assertEqual(len(all_nodes), 4)
        self.assertIn("Goal", all_nodes)
        self.assertIn("Concept", all_nodes)
        self.assertIn("Task", all_nodes)
        self.assertIn("AcceptanceCriteria", all_nodes)

        # Verify counts
        self.assertEqual(len(all_nodes["Goal"]), 1)
        self.assertEqual(len(all_nodes["Concept"]), 1)
        self.assertEqual(len(all_nodes["Task"]), 1)
        self.assertEqual(len(all_nodes["AcceptanceCriteria"]), 1)

    def test_list_nodes_function(self) -> None:
        """Test the list_nodes convenience function."""
        # Create nodes
        create_node(
            self.db_url,
            {
                "id": "GOAL-001",
                "layer": "Goal",
                "title": "Main Goal",
                "description": "Main project goal",
                "metadata": {"owner": "developer", "labels": []},
            },
        )

        create_node(
            self.db_url,
            {
                "id": "TSK-001",
                "layer": "Task",
                "title": "Main Task",
                "description": "Main project task",
                "metadata": {"owner": "developer", "labels": []},
            },
        )

        # List all nodes
        nodes = list_nodes(self.db_url)

        self.assertEqual(len(nodes), 2)
        node_ids = [node.id for node in nodes]
        self.assertIn("GOAL-001", node_ids)
        self.assertIn("TSK-001", node_ids)

    def test_list_nodes_by_layer(self) -> None:
        """Test listing nodes filtered by layer."""
        # Create multiple nodes of different layers
        nodes_data = [
            {"id": "GOAL-001", "layer": "Goal", "title": "Goal 1"},
            {"id": "GOAL-002", "layer": "Goal", "title": "Goal 2"},
            {"id": "TSK-001", "layer": "Task", "title": "Task 1"},
            {"id": "TSK-002", "layer": "Task", "title": "Task 2"},
        ]

        for node_data in nodes_data:
            create_node(self.db_url, node_data)

        # List goals only
        goals = list_nodes(self.db_url, layer="Goal")
        self.assertEqual(len(goals), 2)

        # List tasks only
        tasks = list_nodes(self.db_url, layer="Task")
        self.assertEqual(len(tasks), 2)

    def test_list_nodes_by_owner(self) -> None:
        """Test listing nodes filtered by owner."""
        # Create nodes with different owners
        create_node(
            self.db_url,
            {
                "id": "GOAL-001",
                "layer": "Goal",
                "title": "Developer Goal",
                "metadata": {"owner": "developer", "labels": []},
            },
        )

        create_node(
            self.db_url,
            {
                "id": "TSK-001",
                "layer": "Task",
                "title": "Developer Task",
                "metadata": {"owner": "developer", "labels": []},
            },
        )

        create_node(
            self.db_url,
            {
                "id": "GOAL-002",
                "layer": "Goal",
                "title": "Designer Goal",
                "metadata": {"owner": "designer", "labels": []},
            },
        )

        # List nodes by owner
        developer_nodes = list_nodes(self.db_url, owner="developer")
        self.assertEqual(len(developer_nodes), 2)

        designer_nodes = list_nodes(self.db_url, owner="designer")
        self.assertEqual(len(designer_nodes), 1)


class TestNodeAPI(unittest.TestCase):
    """Test Node object API and methods."""

    def setUp(self) -> None:
        """Set up test environment."""
        self.test_db = Path("test_node_api.db")
        self.db_url = f"sqlite:///{self.test_db}"
        self.app = ToDoWrite(self.db_url)
        self.app.init_database()

    def tearDown(self) -> None:
        """Clean up test environment."""
        self.test_db.unlink(missing_ok=True)

    def test_node_to_dict(self) -> None:
        """Test Node.to_dict() method."""
        # Create a node
        node_data = {
            "id": "GOAL-001",
            "layer": "Goal",
            "title": "Test Goal",
            "description": "Test description",
            "status": "in_progress",
            "progress": 75,
            "metadata": {
                "owner": "developer",
                "labels": ["urgent", "important"],
                "severity": "high",
                "work_type": "implementation",
            },
        }
        node = create_node(self.db_url, node_data)

        # Convert to dict
        node_dict = node.to_dict()

        self.assertEqual(node_dict["id"], "GOAL-001")
        self.assertEqual(node_dict["title"], "Test Goal")
        self.assertEqual(node_dict["status"], "in_progress")
        self.assertEqual(node_dict["progress"], 75)
        self.assertEqual(node_dict["metadata"]["labels"], ["urgent", "important"])

    def test_node_from_dict(self) -> None:
        """Test creating Node from dictionary."""
        node_dict = {
            "id": "TSK-001",
            "layer": "Task",
            "title": "Test Task",
            "description": "Test task description",
            "status": "planned",
            "links": {"parents": [], "children": []},
            "metadata": {
                "owner": "developer",
                "labels": ["test"],
                "severity": "medium",
            },
        }

        node = Node.from_dict(node_dict)

        self.assertEqual(node.id, "TSK-001")
        self.assertEqual(node.title, "Test Task")
        self.assertEqual(node.layer, "Task")
        self.assertEqual(node.metadata.owner, "developer")

    def test_node_metadata_access(self) -> None:
        """Test Node metadata access patterns."""
        node_data = {
            "id": "GOAL-001",
            "layer": "Goal",
            "title": "Test Goal",
            "description": "Test description",
            "metadata": {
                "owner": "developer",
                "labels": ["label1", "label2"],
                "severity": "high",
                "work_type": "implementation",
                "assignee": "team-lead",
            },
        }
        node = create_node(self.db_url, node_data)

        # Test direct access
        self.assertEqual(node.metadata.owner, "developer")
        self.assertEqual(node.metadata.severity, "high")
        self.assertEqual(node.metadata.work_type, "implementation")

        # Test labels access
        self.assertIn("label1", node.metadata.labels)
        self.assertIn("label2", node.metadata.labels)

    def test_node_links_access(self) -> None:
        """Test Node links access and manipulation."""
        # Create parent and child nodes
        parent_data = {
            "id": "GOAL-001",
            "layer": "Goal",
            "title": "Parent Goal",
            "description": "Parent description",
            "metadata": {"owner": "developer", "labels": []},
        }
        parent = create_node(self.db_url, parent_data)

        child_data = {
            "id": "TSK-001",
            "layer": "Task",
            "title": "Child Task",
            "description": "Child description",
            "metadata": {"owner": "developer", "labels": []},
        }
        child = create_node(self.db_url, child_data)

        # Link nodes using convenience function
        link_nodes(self.db_url, parent.id, child.id)

        # Refresh nodes to get updated links
        parent = get_node(self.db_url, parent.id)
        child = get_node(self.db_url, child.id)

        # Test links access
        self.assertIn(child.id, parent.links.children)
        self.assertIn(parent.id, child.links.parents)

    def test_node_status_progress_properties(self) -> None:
        """Test Node status and progress properties."""
        node_data = {
            "id": "TSK-001",
            "layer": "Task",
            "title": "Test Task",
            "description": "Test description",
            "status": "in_progress",
            "progress": 50,
            "metadata": {"owner": "developer", "labels": []},
        }
        node = create_node(self.db_url, node_data)

        # Test status property
        self.assertEqual(node.status, "in_progress")

        # Test progress property
        self.assertEqual(node.progress, 50)

    def test_node_equality(self) -> None:
        """Test Node object equality."""
        node_data = {
            "id": "GOAL-001",
            "layer": "Goal",
            "title": "Test Goal",
            "description": "Test description",
            "metadata": {"owner": "developer", "labels": []},
        }

        node1 = create_node(self.db_url, node_data.copy())
        node2 = get_node(self.db_url, "GOAL-001")

        # Should be equal (same ID)
        self.assertEqual(node1, node2)
        self.assertEqual(node1.id, node2.id)

    def test_node_string_representation(self) -> None:
        """Test Node string representation."""
        node_data = {
            "id": "GOAL-001",
            "layer": "Goal",
            "title": "Test Goal",
            "description": "Test description",
            "metadata": {"owner": "developer", "labels": []},
        }
        node = create_node(self.db_url, node_data)

        # Test string representation
        str_repr = str(node)
        self.assertIn("GOAL-001", str_repr)
        self.assertIn("Test Goal", str_repr)
        self.assertIn("Goal", str_repr)


class TestLinkingAPI(unittest.TestCase):
    """Test node linking API functionality."""

    def setUp(self) -> None:
        """Set up test environment."""
        self.test_db = Path("test_linking.db")
        self.db_url = f"sqlite:///{self.test_db}"
        self.app = ToDoWrite(self.db_url)
        self.app.init_database()

    def tearDown(self) -> None:
        """Clean up test environment."""
        self.test_db.unlink(missing_ok=True)

    def test_link_nodes_function(self) -> None:
        """Test the link_nodes convenience function."""
        # Create nodes
        goal_data = {
            "id": "GOAL-001",
            "layer": "Goal",
            "title": "Main Goal",
            "description": "Main project goal",
            "metadata": {"owner": "developer", "labels": []},
        }
        goal = create_node(self.db_url, goal_data)

        task_data = {
            "id": "TSK-001",
            "layer": "Task",
            "title": "Main Task",
            "description": "Main project task",
            "metadata": {"owner": "developer", "labels": []},
        }
        task = create_node(self.db_url, task_data)

        # Link nodes
        result = link_nodes(self.db_url, goal.id, task.id)
        self.assertTrue(result)

        # Verify links
        goal = get_node(self.db_url, goal.id)
        task = get_node(self.db_url, task.id)

        self.assertIn(task.id, goal.links.children)
        self.assertIn(goal.id, task.links.parents)

    def test_link_nodes_with_links_data(self) -> None:
        """Test linking with explicit links data."""
        # Create nodes
        goal1 = create_node(
            self.db_url,
            {
                "id": "GOAL-001",
                "layer": "Goal",
                "title": "Goal 1",
                "description": "First goal",
                "metadata": {"owner": "developer", "labels": []},
            },
        )

        goal2 = create_node(
            self.db_url,
            {
                "id": "GOAL-002",
                "layer": "Goal",
                "title": "Goal 2",
                "description": "Second goal",
                "metadata": {"owner": "developer", "labels": []},
            },
        )

        task = create_node(
            self.db_url,
            {
                "id": "TSK-001",
                "layer": "Task",
                "title": "Shared Task",
                "description": "Task for both goals",
                "metadata": {"owner": "developer", "labels": []},
            },
        )

        # Link task to both goals
        links_data = {"parents": ["GOAL-001", "GOAL-002"]}
        result = link_nodes(self.db_url, task.id, links_data=links_data)
        self.assertTrue(result)

        # Verify links
        task = get_node(self.db_url, task.id)
        goal1 = get_node(self.db_url, goal1.id)
        goal2 = get_node(self.db_url, goal2.id)

        self.assertIn("GOAL-001", task.links.parents)
        self.assertIn("GOAL-002", task.links.parents)
        self.assertIn("TSK-001", goal1.links.children)
        self.assertIn("TSK-001", goal2.links.children)

    def test_unlink_nodes_function(self) -> None:
        """Test the unlink_nodes convenience function."""
        # Create and link nodes
        goal = create_node(
            self.db_url,
            {
                "id": "GOAL-001",
                "layer": "Goal",
                "title": "Main Goal",
                "metadata": {"owner": "developer", "labels": []},
            },
        )

        task = create_node(
            self.db_url,
            {
                "id": "TSK-001",
                "layer": "Task",
                "title": "Main Task",
                "metadata": {"owner": "developer", "labels": []},
            },
        )

        # First link them
        link_nodes(self.db_url, goal.id, task.id)

        # Verify links exist
        goal = get_node(self.db_url, goal.id)
        task = get_node(self.db_url, task.id)
        self.assertIn(task.id, goal.links.children)
        self.assertIn(goal.id, task.links.parents)

        # Unlink them
        result = unlink_nodes(self.db_url, goal.id, task.id)
        self.assertTrue(result)

        # Verify links are removed
        goal = get_node(self.db_url, goal.id)
        task = get_node(self.db_url, task.id)
        self.assertNotIn(task.id, goal.links.children)
        self.assertNotIn(goal.id, task.links.parents)

    def test_circular_link_prevention(self) -> None:
        """Test prevention of circular linking."""
        node_data = {
            "id": "NODE-001",
            "layer": "Task",
            "title": "Test Node",
            "description": "Test node description",
            "metadata": {"owner": "developer", "labels": []},
        }
        node = create_node(self.db_url, node_data)

        # Try to link node to itself
        result = link_nodes(self.db_url, node.id, node.id)
        self.assertFalse(result)  # Should fail

    def test_link_nonexistent_nodes(self) -> None:
        """Test linking non-existent nodes."""
        # Try to link non-existent nodes
        result = link_nodes(self.db_url, "NONEXISTENT1", "NONEXISTENT2")
        self.assertFalse(result)  # Should fail

    def test_get_node_hierarchy(self) -> None:
        """Test retrieving node hierarchy."""
        # Create hierarchy
        goal = create_node(
            self.db_url,
            {
                "id": "GOAL-001",
                "layer": "Goal",
                "title": "Main Goal",
                "metadata": {"owner": "developer", "labels": []},
            },
        )

        concept = create_node(
            self.db_url,
            {
                "id": "CON-001",
                "layer": "Concept",
                "title": "Main Concept",
                "metadata": {"owner": "developer", "labels": []},
            },
        )

        task1 = create_node(
            self.db_url,
            {
                "id": "TSK-001",
                "layer": "Task",
                "title": "Task 1",
                "metadata": {"owner": "developer", "labels": []},
            },
        )

        task2 = create_node(
            self.db_url,
            {
                "id": "TSK-002",
                "layer": "Task",
                "title": "Task 2",
                "metadata": {"owner": "developer", "labels": []},
            },
        )

        # Create hierarchy
        link_nodes(self.db_url, goal.id, concept.id)
        link_nodes(self.db_url, goal.id, task1.id)
        link_nodes(self.db_url, goal.id, task2.id)

        # Get goal hierarchy
        goal = get_node(self.db_url, goal.id)
        self.assertEqual(len(goal.links.children), 3)

        # Get task hierarchy
        task1 = get_node(self.db_url, task1.id)
        self.assertEqual(len(task1.links.parents), 1)
        self.assertIn("GOAL-001", task1.links.parents)


if __name__ == "__main__":
    unittest.main()
