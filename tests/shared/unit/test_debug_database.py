"""
Debug database operations to understand isolation issues.
"""

import uuid

from todowrite import Goal, create_engine, sessionmaker
from todowrite.core.types import Base


class ToDoWriteApp:
    """Simple ToDoWrite manager for tests."""

    def __init__(self, database_url: str) -> None:
        self.database_url = database_url
        self.engine = create_engine(database_url)
        self.Session = sessionmaker(bind=self.engine)

    def init_database(self) -> None:
        Base.metadata.create_all(self.engine)

    def create_node(self, node_data: dict) -> Goal:
        session = self.Session()
        try:
            node = Goal(**node_data)
            session.add(node)
            session.commit()
            session.refresh(node)
            return node
        finally:
            session.close()

    def get_node(self, node_id: int) -> Goal:
        session = self.Session()
        try:
            return session.query(Goal).filter_by(id=node_id).first()
        finally:
            session.close()

    def get_all_nodes(self) -> list[Goal]:
        session = self.Session()
        try:
            return session.query(Goal).all()
        finally:
            session.close()


def test_debug_database_operations():
    """Debug database operations step by step."""
    # Initialize app
    app = ToDoWriteApp("sqlite:///:memory:")
    app.init_database()

    # Create unique test data
    unique_id = uuid.uuid4().hex[:8].upper()
    test_node_data = {
        "title": f"Debug Goal {unique_id}",
        "description": f"Debug goal {unique_id}",
        "status": "planned",
    }

    print(f"Creating node: {test_node_data['title']}")

    # Create node
    created_node = app.create_node
    print(f"Created node: {created_node}")

    # Try to retrieve it immediately
    retrieved_node = app.get_node(created_node.id)
    print(f"Retrieved node: {retrieved_node}")

    # List all nodes
    nodes_list = app.get_all_nodes()
    print(f"All nodes: {nodes_list}")

    # Debug info
    print(f"Created node ID: {created_node.id}")
    print(f"Retrieved node exists: {retrieved_node is not None}")
    print(f"Number of nodes in list: {len(nodes_list.get('nodes', []))}")

    # Basic assertions
    assert created_node is not None
    assert retrieved_node is not None
    assert created_node.id == retrieved_node.id
