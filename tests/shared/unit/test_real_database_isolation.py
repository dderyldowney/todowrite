"""
Real database isolation tests that work directly with database operations.

These tests demonstrate true table recreation by directly using the database
session and SQLAlchemy operations instead of the app layer functions.
"""

import uuid
from typing import Any

from todowrite.database.models import Base, Node as DBNode


class TestRealDatabaseIsolation:
    """Test real database isolation with direct database operations."""

    def test_direct_database_operations(self, test_db_session) -> None:
        """Test direct database operations with proper table isolation."""
        # Use the test database session directly
        session = test_db_session

        # Create unique test data
        unique_id = uuid.uuid4().hex[:8].upper()
        test_node = DBNode(
            id=f"GOAL-{unique_id}",
            layer="Goal",
            title=f"Test Goal {unique_id}",
            description=f"Test goal {unique_id}",
            status="planned",
            owner=None,
            severity=None,
            work_type=None,
            assignee=None,
        )

        # Add to database
        session.add(test_node)
        session.commit()

        # Query directly from database
        retrieved_node = session.query(DBNode).filter_by(id=test_node.id).first()

        # Verify node was actually created and retrieved
        assert retrieved_node is not None
        assert retrieved_node.id == test_node.id
        assert retrieved_node.title == test_node.title

        # Check total nodes in database
        all_nodes = session.query(DBNode).all()
        assert len(all_nodes) == 1
        assert all_nodes[0].id == test_node.id

    def test_table_isolation_verification(self, test_db_session) -> None:
        """Test that tables are properly isolated between tests.

        This test should always start with a completely clean database.
        """
        session = test_db_session

        # At the start, database should be completely empty
        all_nodes = session.query(DBNode).all()
        assert len(all_nodes) == 0, f"Database should be empty, but found {len(all_nodes)} nodes"

        # Create a test node
        unique_id = uuid.uuid4().hex[:8].upper()
        test_node = DBNode(
            id=f"GOAL-{unique_id}",
            layer="Goal",
            title=f"Isolation Test {unique_id}",
            description=f"Testing isolation {unique_id}",
            status="planned",
            owner=None,
            severity=None,
            work_type=None,
            assignee=None,
        )

        session.add(test_node)
        session.commit()

        # Should only find our one node
        all_nodes = session.query(DBNode).all()
        assert len(all_nodes) == 1
        assert all_nodes[0].id == test_node.id

    def test_multiple_nodes_single_test(self, test_db_session) -> None:
        """Test creating multiple nodes within the same test."""
        session = test_db_session

        # Create multiple nodes
        nodes_to_create = []
        for i in range(3):
            unique_id = uuid.uuid4().hex[:8].upper()
            node = DBNode(
                id=f"GOAL-{unique_id}",
                layer="Goal",
                title=f"Test Goal {i+1} - {unique_id}",
                description=f"Test goal {i+1}",
                status="planned",
                owner=None,
                severity=None,
                work_type=None,
                assignee=None,
            )
            nodes_to_create.append(node)
            session.add(node)

        session.commit()

        # Verify all nodes were created
        all_nodes = session.query(DBNode).all()
        assert len(all_nodes) == 3

        # Verify each created node exists
        created_ids = {node.id for node in nodes_to_create}
        retrieved_ids = {node.id for node in all_nodes}
        assert created_ids == retrieved_ids

    def test_different_layers_same_test(self, test_db_session) -> None:
        """Test creating nodes from different layers in the same test."""
        session = test_db_session

        # Create nodes from different layers
        layers_and_prefixes = [
            ("Goal", "GOAL"),
            ("Task", "TSK"),
            ("Command", "CMD"),
        ]

        created_nodes = []
        for layer, prefix in layers_and_prefixes:
            unique_id = uuid.uuid4().hex[:8].upper()
            node = DBNode(
                id=f"{prefix}-{unique_id}",
                layer=layer,
                title=f"{layer} Node {unique_id}",
                description=f"Test {layer.lower()} node",
                status="planned",
                owner=None,
                severity=None,
                work_type=None,
                assignee=None,
            )
            created_nodes.append(node)
            session.add(node)

        session.commit()

        # Verify all nodes were created
        all_nodes = session.query(DBNode).all()
        assert len(all_nodes) == 3

        # Verify each layer is represented
        created_layers = {node.layer for node in created_nodes}
        retrieved_layers = {node.layer for node in all_nodes}
        assert created_layers == retrieved_layers

    def test_database_transaction_rollback(self, test_db_session) -> None:
        """Test database transaction rollback behavior."""
        session = test_db_session

        # Start with empty database
        all_nodes = session.query(DBNode).all()
        assert len(all_nodes) == 0

        # Create a node
        unique_id = uuid.uuid4().hex[:8].upper()
        test_node = DBNode(
            id=f"GOAL-{unique_id}",
            layer="Goal",
            title=f"Transaction Test {unique_id}",
            description="Testing transaction behavior",
            status="planned",
            owner=None,
            severity=None,
            work_type=None,
            assignee=None,
        )

        session.add(test_node)
        session.commit()

        # Verify node was committed
        all_nodes = session.query(DBNode).all()
        assert len(all_nodes) == 1

        # Start a new transaction and roll it back
        try:
            rollback_node = DBNode(
                id=f"GOAL-{uuid.uuid4().hex[:8].upper()}",
                layer="Goal",
                title="This will be rolled back",
                description="Rollback test",
                status="planned",
                owner=None,
                severity=None,
                work_type=None,
                assignee=None,
            )
            session.add(rollback_node)
            session.flush()  # Flush but don't commit
            raise Exception("Force rollback")
        except Exception:
            session.rollback()

        # Verify rollback worked - only the first node should exist
        all_nodes = session.query(DBNode).all()
        assert len(all_nodes) == 1
        assert all_nodes[0].id == test_node.id