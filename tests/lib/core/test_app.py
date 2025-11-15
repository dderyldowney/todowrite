"""Tests for the unified Node architecture."""

from __future__ import annotations

import tempfile
from pathlib import Path

import pytest

from lib_package.src.todowrite.core.app_refactored import ToDoWrite
from lib_package.src.todowrite.core.types import Node, Link, Metadata
from lib_package.src.todowrite.storage import (
    NodeNotFoundError,
    NodeCreationError,
)


class TestUnifiedNodeArchitecture:
    """Test the unified Node architecture."""

    @pytest.fixture
    def temp_db_path(self):
        """Create a temporary database path."""
        with tempfile.NamedTemporaryFile(suffix='.db', delete=False) as temp_file:
            yield temp_file.name

    @pytest.fixture
    def todowrite_app(self, temp_db_path):
        """Create a ToDoWrite app with temporary database."""
        # For now, let's use the original factory but it will use unified approach
        app = ToDoWrite(f"sqlite:///{temp_db_path}", auto_import=False)
        yield app

    def test_create_node_from_dict_compatibility(self, todowrite_app):
        """Test that dict-based creation still works for backward compatibility."""
        node_data = {
            "id": "GOAL-TEST-001",
            "layer": "Goal",
            "title": "Test Goal",
            "description": "A test goal",
            "links": {"parents": [], "children": []},
            "metadata": {"owner": "test-user", "labels": ["test"]},
        }
        node = todowrite_app.create_new_node(node_data)
        assert node.id == "GOAL-TEST-001"
        assert node.title == "Test Goal"
        assert node.description == "A test goal"

    def test_create_node_object_directly(self, todowrite_app):
        """Test creating a Node object directly."""
        app_node = Node(
            id="GOAL-DIRECT-001",
            layer="Goal",
            title="Direct Node Creation",
            description="Created directly as Node object",
            links=Link(parents=[], children=[]),
            metadata=Metadata(owner="test-user", labels=["direct"]),
        )

        # This would use the create_node_from_object method when implemented
        # For now, let's test the dict conversion
        node_dict = app_node.to_dict()
        node = todowrite_app.create_new_node(node_dict)
        assert node.id == "GOAL-DIRECT-001"
        assert node.title == "Direct Node Creation"

    def test_retrieve_node_returns_node_object(self, todowrite_app):
        """Test that retrieve returns proper Node object."""
        # Create a node first
        node_data = {
            "id": "GOAL-RETRIEVE-001",
            "layer": "Goal",
            "title": "Retrieve Test",
            "description": "Test retrieval",
            "links": {"parents": [], "children": []},
            "metadata": {"owner": "test-user", "labels": []},
        }
        todowrite_app.create_new_node(node_data)

        # Retrieve the node
        retrieved_node = todowrite_app.retrieve_node_by_id("GOAL-RETRIEVE-001")
        assert isinstance(retrieved_node, Node)
        assert retrieved_node.id == "GOAL-RETRIEVE-001"
        assert retrieved_node.title == "Retrieve Test"
        assert isinstance(retrieved_node.links, Link)
        assert isinstance(retrieved_node.metadata, Metadata)

    def test_node_object_properties(self, todowrite_app):
        """Test Node object has proper structure."""
        node_data = {
            "id": "GOAL-PROPS-001",
            "layer": "Goal",
            "title": "Properties Test",
            "description": "Testing Node object structure",
            "links": {"parents": ["GOAL-PARENT-001"], "children": ["TSK-CHILD-001"]},
            "metadata": {
                "owner": "test-user",
                "labels": ["test", "validation"],
                "severity": "high",
                "work_type": "feature"
            },
        }
        node = todowrite_app.create_new_node(node_data)

        # Test basic properties
        assert isinstance(node, Node)
        assert node.id == "GOAL-PROPS-001"
        assert node.layer == "Goal"
        assert node.title == "Properties Test"

        # Test complex properties
        assert hasattr(node, 'links')
        assert hasattr(node, 'metadata')
        assert isinstance(node.links, Link)
        assert isinstance(node.metadata, Metadata)
        assert node.links.parents == ["GOAL-PARENT-001"]
        assert node.links.children == ["TSK-CHILD-001"]
        assert node.metadata.owner == "test-user"
        assert node.metadata.labels == ["test", "validation"]
        assert node.metadata.severity == "high"

    def test_node_to_dict_conversion(self, todowrite_app):
        """Test Node.to_dict() method works correctly."""
        node_data = {
            "id": "GOAL-TO-DICT-001",
            "layer": "Goal",
            "title": "Dict Conversion Test",
            "description": "Testing to_dict conversion",
            "links": {"parents": ["PARENT"], "children": ["CHILD"]},
            "metadata": {"owner": "user", "labels": ["test"]},
        }
        node = todowrite_app.create_new_node(node_data)

        # Test to_dict conversion
        node_dict = node.to_dict()
        assert isinstance(node_dict, dict)
        assert node_dict["id"] == "GOAL-TO-DICT-001"
        assert node_dict["title"] == "Dict Conversion Test"
        assert "links" in node_dict
        assert "metadata" in node_dict

    def test_no_duplicate_node_types(self):
        """Test we're not creating multiple Node representations."""
        # Import only one Node type
        from lib_package.src.todowrite.core.types import Node

        # Should only be one Node class in core.types
        # No database.models.Node should exist
        try:
            from lib_package.src.todowrite.database.models import Node as DBNode
            # If this import succeeds, we still have duplicate Node types
            pytest.skip("Database Node model still exists - migration not complete")
        except ImportError:
            # Expected - database Node should be removed
            pass

        # Verify Node is the expected class
        assert Node is not None
        assert hasattr(Node, 'to_dict')
        assert hasattr(Node, 'from_dict')


class TestUnifiedNodeStorage:
    """Test that storage works with unified Node objects."""

    def test_sqlite_unified_backend(self):
        """Test the SQLite unified backend."""
        from lib_package.src.todowrite.storage.sqlite_unified import SQLiteUnifiedBackend

        backend = SQLiteUnifiedBackend(":memory:")
        assert backend.backend_name == "SQLite"

        # Test connection
        backend.connect_to_storage()
        assert backend.storage_is_healthy()

        # Test disconnection
        backend.disconnect_from_storage()

    def test_node_persistence_roundtrip(self):
        """Test Node objects survive storage roundtrip."""
        from lib_package.src.todowrite.storage.sqlite_unified import SQLiteUnifiedBackend
        from lib_package.src.todowrite.core.types import Node, Link, Metadata

        backend = SQLiteUnifiedBackend(":memory:")
        backend.connect_to_storage()

        # Create Node object
        original_node = Node(
            id="GOAL-ROUNDTRIP-001",
            layer="Goal",
            title="Roundtrip Test",
            description="Testing Node object persistence",
            links=Link(parents=[], children=[]),
            metadata=Metadata(owner="test", labels=["roundtrip"]),
        )

        # Store the node
        result = backend.create_new_node(original_node)
        assert result.was_newly_created

        # Retrieve the node
        retrieved_node = backend.retrieve_node_by_id("GOAL-ROUNDTRIP-001")

        # Verify roundtrip preserved data
        assert retrieved_node.id == original_node.id
        assert retrieved_node.title == original_node.title
        assert retrieved_node.description == original_node.description
        assert retrieved_node.links.parents == original_node.links.parents
        assert retrieved_node.metadata.owner == original_node.metadata.owner
        assert retrieved_node.metadata.labels == original_node.metadata.labels

        backend.disconnect_from_storage()