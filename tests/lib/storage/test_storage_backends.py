from __future__ import annotations

import tempfile
from pathlib import Path

import pytest

from lib_package.src.todowrite.storage import (
    NodeNotFoundError,
    PostgreSQLBackend,
    SQLiteBackend,
    StorageConnectionError,
    create_storage_backend,
    detect_storage_backend_type,
    get_default_database_url,
    validate_database_url,
)


class TestStorageBackendFactory:
    """Test the storage backend factory functions."""

    def test_detect_storage_backend_type_postgresql(self):
        """Test PostgreSQL URL detection."""
        url = "postgresql://user:pass@localhost:5432/ToDoWrite"
        assert detect_storage_backend_type(url) == "postgresql"

    def test_detect_storage_backend_type_sqlite_url(self):
        """Test SQLite URL detection."""
        url = "sqlite:///tests/todowrite_testing.db"
        assert detect_storage_backend_type(url) == "sqlite"

    def test_detect_storage_backend_type_sqlite_path(self):
        """Test SQLite file path detection."""
        path = "/path/to/database.db"
        assert detect_storage_backend_type(path) == "sqlite"

    def test_detect_storage_backend_type_yaml(self):
        """Test YAML file detection."""
        path = "/path/to/config.yaml"
        assert detect_storage_backend_type(path) == "yaml"

    def test_detect_storage_backend_type_unknown(self):
        """Test unknown URL format detection."""
        url = "justsomeinvalidformat"
        assert detect_storage_backend_type(url) == "unknown"

    def test_validate_database_url_valid_postgresql(self):
        """Test validation of valid PostgreSQL URLs."""
        valid_urls = [
            "postgresql://user:pass@localhost:5432/ToDoWrite",
            "postgresql://localhost/ToDoWrite",
            "postgresql://user@host:5432/db",
        ]
        for url in valid_urls:
            is_valid, error = validate_database_url(url)
            assert is_valid, f"URL {url} should be valid: {error}"

    def test_validate_database_url_valid_sqlite(self):
        """Test validation of valid SQLite URLs."""
        valid_urls = [
            "sqlite:///path/to/db.sqlite",
            "sqlite://path/to/db.sqlite",
            "/path/to/database.db",
            "database.db",
        ]
        for url in valid_urls:
            is_valid, error = validate_database_url(url)
            assert is_valid, f"URL {url} should be valid: {error}"

    def test_validate_database_url_invalid(self):
        """Test validation of invalid URLs."""
        invalid_urls = [
            "justsomeinvalidformat",
            "postgresql://",  # Missing host
        ]
        for url in invalid_urls:
            is_valid, error = validate_database_url(url)
            assert not is_valid, f"URL {url} should be invalid"
            assert error  # Should have error message

    def test_get_default_database_url(self):
        """Test getting default database URL."""
        default_url = get_default_database_url()
        assert default_url.startswith("sqlite://")
        assert "todowrite.db" in default_url


class TestSQLiteBackend:
    """Test SQLite storage backend functionality."""

    @pytest.fixture
    def sqlite_backend(self):
        """Create a temporary SQLite backend for testing."""
        with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as temp_file:
            temp_path = temp_file.name

        backend = SQLiteBackend(temp_path)
        backend.connect_to_storage()

        yield backend

        backend.disconnect_from_storage()
        # Clean up temp file
        Path(temp_path).unlink(missing_ok=True)

    def test_backend_properties(self, sqlite_backend):
        """Test backend properties."""
        assert sqlite_backend.backend_name == "SQLite"
        assert sqlite_backend.storage_is_healthy()

    def test_create_and_retrieve_node(self, sqlite_backend):
        """Test creating and retrieving a node."""
        node_data = {
            "id": "GOAL-TEST-001",
            "layer": "Goal",
            "title": "Test Goal",
            "description": "A test goal",
            "owner": "test-user",
            "labels": ["test", "goal"],
        }

        # Create node
        result = sqlite_backend.create_new_node(node_data)
        assert result.was_newly_created
        assert result.created_node.id == "GOAL-TEST-001"
        assert result.created_node.title == "Test Goal"

        # Retrieve node
        retrieved_node = sqlite_backend.retrieve_node_by_id("GOAL-TEST-001")
        assert retrieved_node.id == "GOAL-TEST-001"
        assert retrieved_node.title == "Test Goal"
        assert retrieved_node.description == "A test goal"

    def test_create_duplicate_node(self, sqlite_backend):
        """Test creating a node that already exists."""
        node_data = {
            "id": "GOAL-DUP-001",
            "layer": "Goal",
            "title": "Duplicate Test",
            "owner": "test-user",
        }

        # Create first time
        result1 = sqlite_backend.create_new_node(node_data)
        assert result1.was_newly_created

        # Create second time (should return existing)
        result2 = sqlite_backend.create_new_node(node_data)
        assert not result2.was_newly_created
        assert result2.created_node.id == "GOAL-DUP-001"

    def test_retrieve_nonexistent_node(self, sqlite_backend):
        """Test retrieving a node that doesn't exist."""
        with pytest.raises(NodeNotFoundError) as exc_info:
            sqlite_backend.retrieve_node_by_id("NONEXISTENT")

        assert "NONEXISTENT" in str(exc_info.value)
        assert "SQLite" in str(exc_info.value)

    def test_update_node(self, sqlite_backend):
        """Test updating an existing node."""
        # Create node first
        node_data = {
            "id": "GOAL-UPDATE-001",
            "layer": "Goal",
            "title": "Original Title",
            "description": "Original description",
            "owner": "test-user",
        }
        sqlite_backend.create_new_node(node_data)

        # Update node
        update_data = {
            "title": "Updated Title",
            "description": "Updated description",
            "labels": ["updated"],
        }
        updated_node = sqlite_backend.update_existing_node("GOAL-UPDATE-001", update_data)

        assert updated_node.title == "Updated Title"
        assert updated_node.description == "Updated description"
        # Note: Label handling would need implementation in _update_node_labels

    def test_delete_node(self, sqlite_backend):
        """Test deleting a node."""
        # Create node first
        node_data = {
            "id": "GOAL-DELETE-001",
            "layer": "Goal",
            "title": "To Delete",
            "owner": "test-user",
        }
        sqlite_backend.create_new_node(node_data)

        # Delete node
        result = sqlite_backend.remove_node_by_id("GOAL-DELETE-001")
        assert result

        # Verify node is gone
        with pytest.raises(NodeNotFoundError):
            sqlite_backend.retrieve_node_by_id("GOAL-DELETE-001")

    def test_delete_nonexistent_node(self, sqlite_backend):
        """Test deleting a node that doesn't exist."""
        result = sqlite_backend.remove_node_by_id("NONEXISTENT")
        assert not result  # Should return False, not raise exception

    def test_list_nodes(self, sqlite_backend):
        """Test listing nodes with and without layer filtering."""
        # Create test nodes in different layers
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

        sqlite_backend.create_new_node(goal_data)
        sqlite_backend.create_new_node(task_data)

        # List all nodes
        all_nodes = sqlite_backend.list_all_nodes_in_layer()
        assert len(all_nodes) == 2
        layer_names = {node.layer for node in all_nodes}
        assert layer_names == {"Goal", "Task"}

        # List nodes by layer
        goal_nodes = sqlite_backend.list_all_nodes_in_layer("Goal")
        assert len(goal_nodes) == 1
        assert goal_nodes[0].layer == "Goal"

    def test_search_nodes(self, sqlite_backend):
        """Test searching nodes by criteria."""
        # Create test nodes
        node_data = {
            "id": "GOAL-SEARCH-001",
            "layer": "Goal",
            "title": "Search Test Goal",
            "description": "A goal for testing search",
            "owner": "search-user",
        }
        sqlite_backend.create_new_node(node_data)

        # Search by title
        results = sqlite_backend.search_nodes_by_criteria({"title": "Search"})
        assert len(results) == 1
        assert "Search" in results[0].title

        # Search by owner
        results = sqlite_backend.search_nodes_by_criteria({"owner": "search-user"})
        assert len(results) == 1
        assert results[0].owner == "search-user"

    def test_create_relationship(self, sqlite_backend):
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

        sqlite_backend.create_new_node(parent_data)
        sqlite_backend.create_new_node(child_data)

        # Create relationship
        result = sqlite_backend.create_parent_child_relationship("GOAL-PARENT-001", "TSK-CHILD-001")
        assert result.was_newly_linked
        assert result.parent_id == "GOAL-PARENT-001"
        assert result.child_id == "TSK-CHILD-001"

        # Create duplicate relationship
        result2 = sqlite_backend.create_parent_child_relationship(
            "GOAL-PARENT-001", "TSK-CHILD-001"
        )
        assert not result2.was_newly_linked

    def test_get_parents_and_children(self, sqlite_backend):
        """Test retrieving parent and child relationships."""
        # Create nodes and relationships
        parent_data = {
            "id": "GOAL-PARENT-002",
            "layer": "Goal",
            "title": "Parent Goal",
            "owner": "test-user",
        }
        child_data = {
            "id": "TSK-CHILD-002",
            "layer": "Task",
            "title": "Child Task",
            "owner": "test-user",
        }

        sqlite_backend.create_new_node(parent_data)
        sqlite_backend.create_new_node(child_data)
        sqlite_backend.create_parent_child_relationship("GOAL-PARENT-002", "TSK-CHILD-002")

        # Get parents of child
        parents = sqlite_backend.get_all_parents_of_node("TSK-CHILD-002")
        assert len(parents) == 1
        assert parents[0].id == "GOAL-PARENT-002"

        # Get children of parent
        children = sqlite_backend.get_all_children_of_node("GOAL-PARENT-002")
        assert len(children) == 1
        assert children[0].id == "TSK-CHILD-002"

    def test_count_nodes(self, sqlite_backend):
        """Test counting nodes in storage."""
        # Initially empty
        count = sqlite_backend.count_nodes_in_storage()
        assert count == 0

        # Create nodes
        for i in range(3):
            node_data = {
                "id": f"GOAL-COUNT-{i:03d}",
                "layer": "Goal",
                "title": f"Count Test {i}",
                "owner": "test-user",
            }
            sqlite_backend.create_new_node(node_data)

        # Count again
        count = sqlite_backend.count_nodes_in_storage()
        assert count == 3


class TestCreateStorageBackend:
    """Test the create_storage_backend factory function."""

    def test_create_sqlite_backend_from_url(self):
        """Test creating SQLite backend from URL."""
        with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as temp_file:
            temp_path = temp_file.name

        try:
            backend = create_storage_backend(f"sqlite:///{temp_path}")
            assert isinstance(backend, SQLiteBackend)
            assert backend.backend_name == "SQLite"
        finally:
            Path(temp_path).unlink(missing_ok=True)

    def test_create_sqlite_backend_from_path(self):
        """Test creating SQLite backend from file path."""
        with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as temp_file:
            temp_path = temp_file.name

        try:
            backend = create_storage_backend(temp_path)
            assert isinstance(backend, SQLiteBackend)
            assert backend.backend_name == "SQLite"
        finally:
            Path(temp_path).unlink(missing_ok=True)

    def test_create_postgresql_backend(self):
        """Test creating PostgreSQL backend."""
        backend = create_storage_backend("postgresql://user:pass@localhost:5432/test")
        assert isinstance(backend, PostgreSQLBackend)
        assert backend.backend_name == "PostgreSQL"

    def test_create_backend_unsupported_url(self):
        """Test creating backend with unsupported URL."""
        with pytest.raises(StorageConnectionError):
            create_storage_backend("justsomeinvalidformat")
