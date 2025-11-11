"""
Real database isolation tests using pytest fixtures.

These tests demonstrate complete table recreation between tests
using real database operations - no mocking allowed.
"""

import uuid

from todowrite.core.app import (
    create_node,
    get_node,
    list_nodes,
    search_nodes,
    update_node_status,
)


class TestDatabaseIsolation:
    """Test database isolation with real table recreation."""

    def test_create_and_retrieve_node(self, sample_node_data: dict) -> None:
        """Test creating and retrieving a node with real database operations."""
        # Create node using real database operation
        created_node = create_node(sample_node_data)

        # Verify node was actually created in real database
        assert created_node.id == sample_node_data["id"]
        assert created_node.title == sample_node_data["title"]
        assert created_node.layer == sample_node_data["layer"]
        assert created_node.status == sample_node_data["status"]

        # Retrieve node from real database
        retrieved_node = get_node(created_node.id)

        # Verify retrieval from real database
        assert retrieved_node is not None
        assert retrieved_node.id == created_node.id
        assert retrieved_node.title == sample_node_data["title"]

    def test_multiple_nodes_in_same_test(self, test_db_session) -> None:
        """Test creating multiple nodes within the same test."""
        # Create multiple unique nodes
        node_data_1 = {
            "id": f"GOAL-{uuid.uuid4().hex[:8].upper()}",
            "title": "First Test Goal",
            "description": "First test goal description",
            "layer": "Goal",
            "status": "planned",
            "metadata": {
                "created_at": "2024-01-01T00:00:00Z",
                "updated_at": "2024-01-01T00:00:00Z",
                "version": 1,
            },
            "links": {"parents": [], "children": []},
        }

        node_data_2 = {
            "id": f"TSK-{uuid.uuid4().hex[:8].upper()}",
            "title": "First Test Task",
            "description": "First test task description",
            "layer": "Task",
            "status": "planned",
            "metadata": {
                "created_at": "2024-01-01T00:00:00Z",
                "updated_at": "2024-01-01T00:00:00Z",
                "version": 1,
            },
            "links": {"parents": [], "children": []},
        }

        # Create both nodes in real database
        created_node_1 = create_node(node_data_1)
        created_node_2 = create_node(node_data_2)

        # Verify both nodes exist
        retrieved_1 = get_node(created_node_1.id)
        retrieved_2 = get_node(created_node_2.id)

        assert retrieved_1 is not None
        assert retrieved_2 is not None
        assert retrieved_1.id != retrieved_2.id

        # Test list_nodes shows both
        nodes_list = list_nodes()
        assert len(nodes_list.get("nodes", [])) >= 2

    def test_node_status_update_real_database(self, sample_node_data: dict) -> None:
        """Test updating node status using real database operations."""
        # Create node in real database
        created_node = create_node(sample_node_data)
        assert created_node.status == "planned"

        # Update status using real database operation
        updated_node = update_node_status(created_node.id, "in_progress")

        # Verify update persisted to real database
        assert updated_node is not None
        assert updated_node.status == "in_progress"

        # Retrieve again to confirm persistence
        retrieved_node = get_node(created_node.id)
        assert retrieved_node is not None
        assert retrieved_node.status == "in_progress"

    def test_search_functionality_real_database(self, test_db_session) -> None:
        """Test search functionality using real database operations."""
        # Create searchable nodes
        searchable_titles = ["Autonomous System", "User Management", "Data Processing"]
        created_nodes = []

        for title in searchable_titles:
            node_data = {
                "id": f"GOAL-{uuid.uuid4().hex[:8].upper()}",
                "title": title,
                "description": f"Description for {title}",
                "layer": "Goal",
                "status": "planned",
                "metadata": {
                    "created_at": "2024-01-01T00:00:00Z",
                    "updated_at": "2024-01-01T00:00:00Z",
                    "version": 1,
                },
                "links": {"parents": [], "children": []},
            }
            created_node = create_node(node_data)
            created_nodes.append(created_node)

        # Test search functionality on real database
        search_results = search_nodes("User")
        assert isinstance(search_results, dict)
        assert "nodes" in search_results

        # Should find the "User Management" node
        found_user_node = False
        for node in search_results["nodes"]:
            if "User" in node.title:
                found_user_node = True
                break

        assert found_user_node, "Search should find node with 'User' in title"

    def test_table_isolation_between_tests(self, sample_node_data: dict) -> None:
        """Test that tables are properly isolated between tests.

        This test should always start with a clean database regardless of
        what previous tests have done.
        """
        # At the start of this test, database should be clean
        # (tables were dropped and recreated)

        # Create a node
        created_node = create_node(sample_node_data)

        # Should only find our newly created node
        nodes_list = list_nodes()
        all_nodes = []
        for layer_nodes in nodes_list.values():
            all_nodes.extend(layer_nodes)
        node_ids = [node.id for node in all_nodes]

        # Should only contain our node
        assert len(node_ids) == 1
        assert created_node.id in node_ids
