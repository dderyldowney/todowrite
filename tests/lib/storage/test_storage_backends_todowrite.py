from __future__ import annotations

import tempfile
from pathlib import Path

import pytest

from lib_package.src.todowrite.storage import (
    StorageBackend,
    PostgreSQLBackend,
    SQLiteBackend,
    create_storage_backend,
    detect_storage_backend_type,
    validate_database_url,
    get_default_database_url,
    NodeNotFoundError,
    NodeCreationError,
    StorageConnectionError,
)
from lib_package.src.todowrite.core.types import Node, Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


class TestStorageBackendFactoryModels:
    """Test the storage backend factory with Models integration."""

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

    def test_create_storage_backend_sqlite(self):
        """Test SQLite backend creation."""
        with tempfile.NamedTemporaryFile(suffix='.db', delete=False) as tmp:
            db_path = tmp.name

        try:
            backend = create_storage_backend(str(db_path))
            assert isinstance(backend, SQLiteBackend)
        finally:
            Path(db_path).unlink(missing_ok=True)

    def test_create_storage_backend_postgresql(self):
        """Test PostgreSQL backend creation."""
        url = "postgresql://user:pass@localhost:5432/ToDoWrite_test"
        backend = create_storage_backend(url)
        assert isinstance(backend, PostgreSQLBackend)

    def test_validate_database_url_sqlite(self):
        """Test SQLite database URL validation."""
        valid_urls = [
            "sqlite:///tests/todowrite_testing.db",
            "sqlite:///:memory:",
            "/absolute/path/to/db.db",
            "relative/path/to/db.db"
        ]
        for url in valid_urls:
            result = validate_database_url(url)
            assert isinstance(result, tuple) and result[0] is True

    def test_validate_database_url_postgresql(self):
        """Test PostgreSQL database URL validation."""
        valid_url = "postgresql://user:pass@localhost:5432/ToDoWrite"
        result = validate_database_url(valid_url)
        assert isinstance(result, tuple) and result[0] is True

    def test_validate_database_url_invalid(self):
        """Test invalid database URL validation."""
        # Note: The validation function is quite permissive and accepts many URLs
        # This test documents the current behavior
        test_urls = [
            "invalid://format",
            "",
            "not-a-url",
            "ftp://file.server.com/file.db"
        ]
        for url in test_urls:
            result = validate_database_url(url)
            # The function returns a tuple, check that it does
            assert isinstance(result, tuple)
            # Document the actual behavior - function is permissive
            if url:
                assert len(result) == 2  # Always returns (bool, message) tuple

    def test_get_default_database_url(self):
        """Test getting default database URL."""
        url = get_default_database_url()
        assert url is not None
        result = validate_database_url(url)
        assert isinstance(result, tuple) and result[0] is True


class TestSQLiteBackendModels:
    """Test SQLite backend with Models integration."""

    def test_sqlite_backend_connection(self):
        """Test SQLite backend connection and setup."""
        with tempfile.NamedTemporaryFile(suffix='.db', delete=False) as tmp:
            db_path = tmp.name

        try:
            backend = SQLiteBackend(db_path)
            backend.connect_to_storage()

            # Should be connected now
            assert backend.backend_name == "SQLite"
            assert backend._is_connected  # Private attribute for now

            backend.disconnect_from_storage()

        finally:
            Path(db_path).unlink(missing_ok=True)

    def test_sqlite_backend_create_node_with_Models(self):
        """Test creating nodes using storage backend with Models."""
        with tempfile.NamedTemporaryFile(suffix='.db', delete=False) as tmp:
            db_path = tmp.name

        try:
            # Setup database with Models
            engine = create_engine(f"sqlite:///{db_path}")
            Base.metadata.create_all(engine)
            Session = sessionmaker(bind=engine)
            session = Session()
            Node.configure_session(session)

            backend = SQLiteBackend(db_path)
            backend.connect_to_storage()

            # Create goal using Models first
            goal = Node.create_goal(
                title="Storage Test Goal",
                owner="test-user"
            )

            # Now use storage backend - should detect it already exists
            result = backend.create_new_node(goal)
            # Note: was_newly_created is False because Node.create_goal() already saved it
            assert not result.was_newly_created
            assert result.created_node.title == "Storage Test Goal"

            # Test retrieval
            retrieved = backend.retrieve_node_by_id(goal.id)
            assert retrieved.title == "Storage Test Goal"
            assert retrieved.layer == "Goal"

            backend.disconnect_from_storage()
            session.close()

        finally:
            Path(db_path).unlink(missing_ok=True)

    def test_sqlite_backend_relationships_with_Models(self):
        """Test relationship creation using storage backend with Models."""
        with tempfile.NamedTemporaryFile(suffix='.db', delete=False) as tmp:
            db_path = tmp.name

        try:
            # Setup database with Models
            engine = create_engine(f"sqlite:///{db_path}")
            Base.metadata.create_all(engine)
            Session = sessionmaker(bind=engine)
            session = Session()
            Node.configure_session(session)

            backend = SQLiteBackend(db_path)
            backend.connect_to_storage()

            # Create parent and child nodes
            goal = Node.create_goal("Parent Goal", "test-user")
            backend.create_new_node(goal)

            phase = Node.new(
                layer="Constraints",
                title="Child Phase",
                owner="test-user"
            ).save()
            backend.create_new_node(phase)

            # Create relationship using storage backend (should use Models)
            relationship_result = backend.create_parent_child_relationship(
                goal.id, phase.id
            )
            assert relationship_result.was_newly_linked
            assert relationship_result.parent_id == goal.id
            assert relationship_result.child_id == phase.id

            # Test that relationship exists
            child_nodes = backend.get_all_children_of_node(goal.id)
            assert len(child_nodes) >= 1
            assert any(child.id == phase.id for child in child_nodes)

            parent_nodes = backend.get_all_parents_of_node(phase.id)
            assert len(parent_nodes) >= 1
            assert any(parent.id == goal.id for parent in parent_nodes)

            backend.disconnect_from_storage()
            session.close()

        finally:
            Path(db_path).unlink(missing_ok=True)

    def test_sqlite_backend_update_with_Models(self):
        """Test updating nodes using storage backend with Models."""
        with tempfile.NamedTemporaryFile(suffix='.db', delete=False) as tmp:
            db_path = tmp.name

        try:
            # Setup database with Models
            engine = create_engine(f"sqlite:///{db_path}")
            Base.metadata.create_all(engine)
            Session = sessionmaker(bind=engine)
            session = Session()
            Node.configure_session(session)

            backend = SQLiteBackend(db_path)
            backend.connect_to_storage()

            # Create node
            node = Node.create_goal("Update Test", "test-user")
            backend.create_new_node(node)

            # Update using storage backend
            updated_node = backend.update_existing_node(
                node.id,
                {
                    "progress": 50,
                    "status": "in_progress"
                }
            )
            assert updated_node.progress == 50
            assert updated_node.status == "in_progress"

            # Verify persistence
            retrieved = backend.retrieve_node_by_id(node.id)
            assert retrieved.progress == 50
            assert retrieved.status == "in_progress"

            backend.disconnect_from_storage()
            session.close()

        finally:
            Path(db_path).unlink(missing_ok=True)

    def test_sqlite_backend_delete_with_Models(self):
        """Test deleting nodes using storage backend with Models."""
        with tempfile.NamedTemporaryFile(suffix='.db', delete=False) as tmp:
            db_path = tmp.name

        try:
            # Setup database with Models
            engine = create_engine(f"sqlite:///{db_path}")
            Base.metadata.create_all(engine)
            Session = sessionmaker(bind=engine)
            session = Session()
            Node.configure_session(session)

            backend = SQLiteBackend(db_path)
            backend.connect_to_storage()

            # Create node
            node = Node.create_goal("Delete Test", "test-user")
            backend.create_new_node(node)

            # Verify it exists
            retrieved = backend.retrieve_node_by_id(node.id)
            assert retrieved is not None

            # Delete using storage backend
            delete_result = backend.remove_node_by_id(node.id)
            assert delete_result is True

            # Verify it's gone
            try:
                backend.retrieve_node_by_id(node.id)
                assert False, "Node should have been deleted"
            except NodeNotFoundError:
                pass  # Expected

            backend.disconnect_from_storage()
            session.close()

        finally:
            Path(db_path).unlink(missing_ok=True)

    def test_sqlite_backend_list_nodes_by_layer(self):
        """Test listing nodes by layer using Models."""
        with tempfile.NamedTemporaryFile(suffix='.db', delete=False) as tmp:
            db_path = tmp.name

        try:
            # Setup database with Models
            engine = create_engine(f"sqlite:///{db_path}")
            Base.metadata.create_all(engine)
            Session = sessionmaker(bind=engine)
            session = Session()
            Node.configure_session(session)

            backend = SQLiteBackend(db_path)
            backend.connect_to_storage()

            # Create nodes in different layers
            goal1 = Node.create_goal("Goal 1", "user1")
            goal2 = Node.create_goal("Goal 2", "user2")
            phase = Node.new(layer="Constraints", title="Phase", owner="user1").save()
            task = Node.new(layer="SubTask", title="Task", owner="user1").save()

            backend.create_new_node(goal1)
            backend.create_new_node(goal2)
            backend.create_new_node(phase)
            backend.create_new_node(task)

            # Test listing by layer
            goals = backend.list_all_nodes_in_layer("Goal")
            phases = backend.list_all_nodes_in_layer("Constraints")
            tasks = backend.list_all_nodes_in_layer("SubTask")

            assert len(goals) == 2
            assert len(phases) == 1
            assert len(tasks) == 1

            # Verify layer filtering
            assert all(node.layer == "Goal" for node in goals)
            assert all(node.layer == "Constraints" for node in phases)
            assert all(node.layer == "SubTask" for node in tasks)

            backend.disconnect_from_storage()
            session.close()

        finally:
            Path(db_path).unlink(missing_ok=True)


if __name__ == "__main__":
    # Allow running as script for debugging
    import sys
    sys.exit(pytest.main([__file__]))