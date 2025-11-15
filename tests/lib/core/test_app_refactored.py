"""Tests for the refactored ToDoWrite application using StorageBackend pattern."""

from __future__ import annotations

import tempfile
from pathlib import Path

import pytest

from lib_package.src.todowrite.core.app_refactored import ToDoWrite
from lib_package.src.todowrite.storage import (
    NodeNotFoundError,
    NodeCreationError,
    NodeUpdateError,
)


def create_test_node_data(
    node_id: str,
    layer: str,
    title: str,
    description: str = "",
    owner: str = "test-user",
    **extra_fields
) -> dict[str, Any]:
    """Create valid test node data with required fields."""
    base_data = {
        "id": node_id,
        "layer": layer,
        "title": title,
        "description": description,
        "owner": owner,
        "links": {"parents": [], "children": []},
        "metadata": {"owner": owner, "labels": []},
    }
    base_data.update(extra_fields)
    return base_data


class TestRefactoredToDoWrite:
    """Test the refactored ToDoWrite application."""

    @pytest.fixture
    def temp_db_path(self):
        """Create a temporary database path."""
        with tempfile.NamedTemporaryFile(suffix='.db', delete=False) as temp_file:
            yield temp_file.name
        # Cleanup is handled by tempfile

    @pytest.fixture
    def todowrite_app(self, temp_db_path):
        """Create a ToDoWrite app instance with temporary database."""
        app = ToDoWrite(f"sqlite:///{temp_db_path}", auto_import=False)
        yield app
        # No explicit cleanup needed - storage backend handles it

    def test_app_initialization(self, todowrite_app):
        """Test that the app initializes correctly."""
        assert todowrite_app.storage is not None
        assert todowrite_app.storage_is_healthy()
        assert todowrite_app.count_nodes_in_storage() == 0

    def test_create_new_node(self, todowrite_app):
        """Test creating a new node."""
        node_data = create_test_node_data(
            "GOAL-TEST-001",
            "Goal",
            "Test Goal",
            "A test goal",
            metadata={"labels": ["test"]}
        )

        node = todowrite_app.create_new_node(node_data)
        assert node.id == "GOAL-TEST-001"
        assert node.title == "Test Goal"
        assert node.description == "A test goal"
        assert todowrite_app.count_nodes_in_storage() == 1

    def test_retrieve_existing_node(self, todowrite_app):
        """Test retrieving an existing node."""
        # Create a node first
        node_data = create_test_node_data(
            "GOAL-RETRIEVE-001",
            "Goal",
            "Retrieve Test",
            "A test node for retrieval"
        )
        todowrite_app.create_new_node(node_data)

        # Retrieve the node
        retrieved_node = todowrite_app.retrieve_node_by_id("GOAL-RETRIEVE-001")
        assert retrieved_node.id == "GOAL-RETRIEVE-001"
        assert retrieved_node.title == "Retrieve Test"

    def test_retrieve_nonexistent_node(self, todowrite_app):
        """Test retrieving a node that doesn't exist."""
        with pytest.raises(NodeNotFoundError):
            todowrite_app.retrieve_node_by_id("NONEXISTENT-NODE")

    def test_update_existing_node(self, todowrite_app):
        """Test updating an existing node."""
        # Create a node first
        node_data = {
            "id": "GOAL-UPDATE-001",
            "layer": "Goal",
            "title": "Original Title",
            "description": "Original description",
            "owner": "test-user",
        }
        todowrite_app.create_new_node(node_data)

        # Update the node
        update_data = {
            "title": "Updated Title",
            "description": "Updated description",
        }
        updated_node = todowrite_app.update_existing_node("GOAL-UPDATE-001", update_data)
        assert updated_node.title == "Updated Title"
        assert updated_node.description == "Updated description"

    def test_update_nonexistent_node(self, todowrite_app):
        """Test updating a node that doesn't exist."""
        with pytest.raises(NodeNotFoundError):
            todowrite_app.update_existing_node("NONEXISTENT", {"title": "New Title"})

    def test_remove_existing_node(self, todowrite_app):
        """Test removing an existing node."""
        # Create a node first
        node_data = {
            "id": "GOAL-DELETE-001",
            "layer": "Goal",
            "title": "To Delete",
            "owner": "test-user",
        }
        todowrite_app.create_new_node(node_data)
        assert todowrite_app.count_nodes_in_storage() == 1

        # Delete the node
        result = todowrite_app.remove_node_by_id("GOAL-DELETE-001")
        assert result is True
        assert todowrite_app.count_nodes_in_storage() == 0

    def test_remove_nonexistent_node(self, todowrite_app):
        """Test removing a node that doesn't exist."""
        result = todowrite_app.remove_node_by_id("NONEXISTENT")
        assert result is False

    def test_list_nodes_by_layer(self, todowrite_app):
        """Test listing nodes filtered by layer."""
        # Create nodes in different layers
        goal_data = {
            "id": "GOAL-LIST-001",
            "layer": "Goal",
            "title": "Test Goal",
            "owner": "test-user",
        }
        task_data = {
            "id": "TSK-LIST-001",
            "layer": "Task",
            "title": "Test Task",
            "owner": "test-user",
        }

        todowrite_app.create_new_node(goal_data)
        todowrite_app.create_new_node(task_data)

        # List all nodes
        all_nodes = todowrite_app.list_all_nodes_in_layer()
        assert len(all_nodes) == 2

        # List nodes by layer
        goal_nodes = todowrite_app.list_all_nodes_in_layer("Goal")
        assert len(goal_nodes) == 1
        assert goal_nodes[0].layer == "Goal"

    def test_search_nodes(self, todowrite_app):
        """Test searching nodes by criteria."""
        # Create a test node
        node_data = {
            "id": "GOAL-SEARCH-001",
            "layer": "Goal",
            "title": "Search Test Goal",
            "description": "A goal for testing search",
            "owner": "search-user",
        }
        todowrite_app.create_new_node(node_data)

        # Search by title
        results = todowrite_app.search_nodes_by_criteria({"title": "Search"})
        assert len(results) == 1
        assert "Search" in results[0].title

        # Search by owner
        results = todowrite_app.search_nodes_by_criteria({"owner": "search-user"})
        assert len(results) == 1
        assert results[0].owner == "search-user"

    def test_create_parent_child_relationship(self, todowrite_app):
        """Test creating parent-child relationships."""
        # Create parent and child nodes
        parent_data = {
            "id": "GOAL-PARENT-001",
            "layer": "Goal",
            "title": "Parent Goal",
            "owner": "test-user",
        }
        child_data = {
            "id": "TSK-CHILD-001",
            "layer": "Task",
            "title": "Child Task",
            "owner": "test-user",
        }

        todowrite_app.create_new_node(parent_data)
        todowrite_app.create_new_node(child_data)

        # Create relationship
        result = todowrite_app.create_parent_child_relationship("GOAL-PARENT-001", "TSK-CHILD-001")
        assert result is True

        # Get parents and children
        parents = todowrite_app.get_all_parents_of_node("TSK-CHILD-001")
        assert len(parents) == 1
        assert parents[0].id == "GOAL-PARENT-001"

        children = todowrite_app.get_all_children_of_node("GOAL-PARENT-001")
        assert len(children) == 1
        assert children[0].id == "TSK-CHILD-001"

    def test_backward_compatibility_methods(self, todowrite_app):
        """Test backward compatibility method aliases."""
        # Test create_node alias
        node_data = {
            "id": "GOAL-COMPAT-001",
            "layer": "Goal",
            "title": "Compatibility Test",
            "owner": "test-user",
        }
        node = todowrite_app.create_node(node_data)
        assert node.id == "GOAL-COMPAT-001"

        # Test get_node alias
        retrieved = todowrite_app.get_node("GOAL-COMPAT-001")
        assert retrieved.id == "GOAL-COMPAT-001"

        # Test list_nodes alias
        all_nodes = todowrite_app.list_nodes()
        assert len(all_nodes) == 1

        # Test count_nodes alias
        count = todowrite_app.count_nodes()
        assert count == 1

    def test_error_handling(self, todowrite_app):
        """Test proper error handling."""
        # Test creating invalid node data
        invalid_data = {
            "id": "INVALID-001",
            # Missing required fields
        }

        with pytest.raises((ValueError, NodeCreationError)):
            todowrite_app.create_new_node(invalid_data)


class TestRefactoredToDoWriteWithPostgreSQL:
    """Test the refactored ToDoWrite application with PostgreSQL backend."""

    def test_postgresql_backend_creation(self):
        """Test that PostgreSQL backend can be created (without actual connection)."""
        # This test verifies the factory can create PostgreSQL backend
        from lib_package.src.todowrite.storage import PostgreSQLBackend

        backend = PostgreSQLBackend("postgresql://user:password@localhost:5432/test")  # pragma: allowlist secret
        assert backend.backend_name == "PostgreSQL"
        assert backend.database_url == "postgresql://user:password@localhost:5432/test"  # pragma: allowlist secret