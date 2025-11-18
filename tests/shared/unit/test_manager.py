"""
Real database manager tests using pytest fixtures for complete isolation.

Tests core functionality using real database operations with pytest fixtures
that ensure proper table recreation for each test.
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

    def update_node(self, node_id: int, update_data: dict) -> Goal:
        session = self.Session()
        try:
            node = session.query(Goal).filter_by(id=node_id).first()
            if node:
                for key, value in update_data.items():
                    if hasattr(node, key):
                        setattr(node, key, value)
                session.commit()
                session.refresh(node)
            return node
        finally:
            session.close()

    def get_all_nodes(self) -> list[Goal]:
        session = self.Session()
        try:
            return session.query(Goal).all()
        finally:
            session.close()


class TestTodosManagerWithDatabaseIsolation:
    """Real database manager tests with complete table isolation using pytest."""

    def test_create_and_retrieve_node_isolated(self, test_db_session) -> None:
        """Test creating and retrieving a node with database isolation."""
        # Create unique test data
        unique_id = uuid.uuid4().hex[:8].upper()
        test_node_data = {
            "id": f"GOAL-{unique_id}",
            "title": f"Test Goal {unique_id}",
            "description": f"A test goal for unit testing {unique_id}",
            "layer": "Goal",
            "status": "planned",
            "metadata": {
                "created_at": "2024-01-01T00:00:00Z",
                "updated_at": "2024-01-01T00:00:00Z",
                "version": 1,
            },
            "links": {"parents": [], "children": []},
        }

        # Create node using real database operation
        created_node = app.create_node

        # Verify node creation
        assert created_node.id == test_node_data["id"]
        assert created_node.title == test_node_data["title"]
        assert created_node.layer == test_node_data["layer"]

        # Retrieve node from real database
        retrieved_node = app.get_node(created_node.id)

        # Verify retrieval
        assert retrieved_node is not None
        assert retrieved_node.id == created_node.id
        assert retrieved_node.title == test_node_data["title"]

    def test_node_lifecycle_operations(self, test_db_session) -> None:
        """Test complete node lifecycle with real database operations."""
        # Create unique test data
        unique_id = uuid.uuid4().hex[:8].upper()
        test_node_data = {
            "id": f"TSK-{unique_id}",
            "title": f"Test Task {unique_id}",
            "description": f"A test task for unit testing {unique_id}",
            "layer": "Task",
            "status": "planned",
            "metadata": {
                "created_at": "2024-01-01T00:00:00Z",
                "updated_at": "2024-01-01T00:00:00Z",
                "version": 1,
            },
            "links": {"parents": [], "children": []},
        }

        # Create node
        created_node = app.create_node
        assert created_node.status == "planned"

        # Update status
        updated_node = app.update_node(created_node.id, {"status": "in_progress"})
        assert updated_node is not None
        assert updated_node.status == "in_progress"

        # Verify update persisted
        retrieved_node = app.get_node(created_node.id)
        assert retrieved_node is not None
        assert retrieved_node.status == "in_progress"

        # Update to completed
        completed_node = app.update_node(created_node.id, {"status": "completed"})
        assert completed_node is not None
        assert completed_node.status == "completed"

    def test_multiple_nodes_with_real_database(self, test_db_session) -> None:
        """Test creating and managing multiple nodes with real database."""
        # Create multiple nodes of different types
        nodes_to_create = [
            {
                "id": f"GOAL-{uuid.uuid4().hex[:8].upper()}",
                "title": "Project Goal",
                "description": "Main project goal",
                "layer": "Goal",
                "status": "planned",
                "metadata": {
                    "created_at": "2024-01-01T00:00:00Z",
                    "updated_at": "2024-01-01T00:00:00Z",
                    "version": 1,
                },
                "links": {"parents": [], "children": []},
            },
            {
                "id": f"TSK-{uuid.uuid4().hex[:8].upper()}",
                "title": "Implementation Task",
                "description": "Task to implement the project",
                "layer": "Task",
                "status": "planned",
                "metadata": {
                    "created_at": "2024-01-01T00:00:00Z",
                    "updated_at": "2024-01-01T00:00:00Z",
                    "version": 1,
                },
                "links": {"parents": [], "children": []},
            },
            {
                "id": f"CMD-{uuid.uuid4().hex[:8].upper()}",
                "title": "Build Command",
                "description": "Command to build the project",
                "layer": "Command",
                "status": "planned",
                "command": {
                    "ac_ref": f"AC-{uuid.uuid4().hex[:8].upper()}",
                    "run": {"shell": "echo 'build complete'"},
                    "artifacts": [],
                },
                "metadata": {
                    "created_at": "2024-01-01T00:00:00Z",
                    "updated_at": "2024-01-01T00:00:00Z",
                    "version": 1,
                },
                "links": {"parents": [], "children": []},
            },
        ]

        created_nodes = []
        for node_data in nodes_to_create:
            created_node = app.create_node
            created_nodes.append(created_node)

        # Verify all nodes were created
        assert len(created_nodes) == 3

        # Test listing nodes
        nodes_list = app.get_all_nodes()
        assert isinstance(nodes_list, dict)

        # Count total nodes across all layers
        total_nodes = 0
        for layer_nodes in nodes_list.values():
            total_nodes += len(layer_nodes)

        assert total_nodes == 3

        # Test search functionality
        search_results = search_nodes("Goal")
        assert isinstance(search_results, dict)
        assert "Goal" in search_results  # Should find the goal layer

        goal_nodes = search_results.get("Goal", [])
        assert len(goal_nodes) >= 1
        assert any("Project Goal" in node.title for node in goal_nodes)

    def test_database_isolation_between_tests(self, test_db_session) -> None:
        """Test that database is properly isolated between tests.

        This test should always start with a completely clean database
        regardless of what other tests have done.
        """
        # At the start of this test, database should be completely clean
        # (tables were dropped and recreated by the fixture)

        # Create a node
        unique_id = uuid.uuid4().hex[:8].upper()
        test_node_data = {
            "id": f"GOAL-{unique_id}",
            "title": f"Isolation Test {unique_id}",
            "description": f"Testing database isolation {unique_id}",
            "layer": "Goal",
            "status": "planned",
            "metadata": {
                "created_at": "2024-01-01T00:00:00Z",
                "updated_at": "2024-01-01T00:00:00Z",
                "version": 1,
            },
            "links": {"parents": [], "children": []},
        }

        created_node = app.create_node

        # Should only find our newly created node
        nodes_list = app.get_all_nodes()
        total_nodes = 0
        found_node_ids = []
        for layer_nodes in nodes_list.values():
            total_nodes += len(layer_nodes)
            found_node_ids.extend([node.id for node in layer_nodes])

        # Should only contain our node
        assert total_nodes == 1
        assert created_node.id in found_node_ids

    def test_search_and_filter_operations(self, test_db_session) -> None:
        """Test search and filter operations with real database."""
        # Create multiple searchable nodes
        search_terms = ["Autonomous", "Database", "User Interface"]
        created_nodes = []

        for term in search_terms:
            node_data = {
                "id": f"GOAL-{uuid.uuid4().hex[:8].upper()}",
                "title": f"{term} System",
                "description": f"Complete {term.lower()} system implementation",
                "layer": "Goal",
                "status": "planned",
                "metadata": {
                    "created_at": "2024-01-01T00:00:00Z",
                    "updated_at": "2024-01-01T00:00:00Z",
                    "version": 1,
                },
                "links": {"parents": [], "children": []},
            }
            created_node = app.create_node
            created_nodes.append(created_node)

        # Test searching for each term
        for term in search_terms:
            search_results = search_nodes(term)
            assert isinstance(search_results, dict)

            # Should find nodes matching the search term
            found_matching_nodes = []
            for layer_nodes in search_results.values():
                for node in layer_nodes:
                    if term in node.title or term in node.description:
                        found_matching_nodes.append(node)

            assert len(found_matching_nodes) >= 1
            assert any(term in node.title for node in found_matching_nodes)
