"""
API Integration Tests with PostgreSQL

Tests the new ToDoWrite Models API using PostgreSQL as the backend database.
This ensures our modern API works correctly with a production-grade database.
"""

from __future__ import annotations

import json
import tempfile
from pathlib import Path

import pytest
import yaml
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

from todowrite.core.models import (
    Goal,
    Task,
    Phase,
    Step,
    Label,
    Command,
    Base,
)

try:
    from .docker_utils import docker_manager, TestPostgreSQLConfig
except ImportError:
    # Fallback for when running directly
    import sys
    from pathlib import Path

    # Add the parent directory to path so we can import docker_utils
    parent_dir = Path(__file__).parent.parent.parent
    if str(parent_dir) not in sys.path:
        sys.path.insert(0, str(parent_dir))

    from tests.lib.docker.docker_utils import docker_manager, TestPostgreSQLConfig


@pytest.mark.requires_docker
class TestAPIPostgreSQLIntegration:
    """Integration tests for ToDoWrite API with PostgreSQL backend."""

    @pytest.fixture(scope="class")
    def postgresql_url(self: "TestAPIPostgreSQLIntegration") -> str:
        """Start PostgreSQL and return connection URL."""
        if not docker_manager.start_postgresql_container():
            pytest.skip("Failed to start PostgreSQL container")

        yield TestPostgreSQLConfig.get_connection_url()

        docker_manager.stop_postgresql_container()

    @pytest.fixture
    def session(self: "TestAPIPostgreSQLIntegration", postgresql_url: str):
        """Create database session for testing."""
        engine = create_engine(postgresql_url)
        Base.metadata.create_all(engine)

        Session = sessionmaker(bind=engine)
        session = Session()

        yield session

        session.close()

    def test_complete_crud_operations(self: "TestAPIPostgreSQLIntegration", session: Any) -> None:
        """Test complete CRUD operations with PostgreSQL."""
        # CREATE: Create a goal with full metadata
        goal_data = {
            "title": "PostgreSQL CRUD Test",
            "description": "Testing complete CRUD operations",
            "owner": "test-user",
            "severity": "high",
            "work_type": "feature",
            "assignee": "developer",
            "extra_data": json.dumps({
                "priority": 1,
                "estimated_hours": 40,
                "dependencies": ["database-setup", "api-design"]
            })
        }

        goal = Goal(**goal_data)
        session.add(goal)
        session.commit()

        assert goal.id is not None

        # READ: Retrieve and verify data
        retrieved_goal = session.query(Goal).filter(Goal.title == "PostgreSQL CRUD Test").first()
        assert retrieved_goal is not None
        assert retrieved_goal.owner == "test-user"
        assert retrieved_goal.severity == "high"

        extra_data = json.loads(retrieved_goal.extra_data)
        assert extra_data["priority"] == 1
        assert len(extra_data["dependencies"]) == 2

        # UPDATE: Modify the goal
        retrieved_goal.severity = "critical"
        retrieved_goal.extra_data = json.dumps({
            "priority": 1,
            "estimated_hours": 50,  # Updated
            "dependencies": ["database-setup", "api-design", "testing"]
        })
        session.commit()

        updated_goal = session.query(Goal).filter(Goal.id == retrieved_goal.id).first()
        assert updated_goal.severity == "critical"

        updated_extra = json.loads(updated_goal.extra_data)
        assert updated_extra["estimated_hours"] == 50
        assert len(updated_extra["dependencies"]) == 3

        # DELETE: Remove the goal
        session.delete(updated_goal)
        session.commit()

        deleted_goal = session.query(Goal).filter(Goal.id == updated_goal.id).first()
        assert deleted_goal is None

    def test_complex_relationships_and_queries(self: "TestAPIPostgreSQLIntegration", session: Any) -> None:
        """Test complex relationships and advanced queries with PostgreSQL."""
        # Create comprehensive test data
        goals = [
            Goal(title="E-commerce Platform", description="Main project", severity="high", owner="alice"),
            Goal(title="Mobile App", description="Mobile application", severity="medium", owner="bob"),
            Goal(title="Admin Dashboard", description="Administrative interface", severity="low", owner="alice"),
        ]

        tasks = [
            Task(
                title="User Authentication",
                description="Implement login and registration",
                work_type="feature",
                owner="charlie",
                assignee="backend-dev",
                extra_data=json.dumps({"complexity": "high", "api_endpoints": 8})
            ),
            Task(
                title="Database Migration",
                description="Migrate database schema",
                work_type="infrastructure",
                owner="alice",
                assignee="dba"
            ),
            Task(
                title="Payment Integration",
                description="Integrate payment gateway",
                work_type="feature",
                owner="bob",
                assignee="backend-dev",
                extra_data=json.dumps({"gateway": "stripe", "test_mode": True})
            ),
        ]

        labels = [
            Label(name="urgent"),
            Label(name="backend"),
            Label(name="frontend"),
            Label(name="security"),
        ]

        session.add_all(goals + tasks + labels)
        session.commit()

        # Test complex queries
        # Query by severity and owner using AND
        high_priority_alice_goals = session.query(Goal).filter(
            Goal.severity == "high",
            Goal.owner == "alice"
        ).all()
        assert len(high_priority_alice_goals) == 1
        assert high_priority_alice_goals[0].title == "E-commerce Platform"

        # Query tasks with complex extra_data
        backend_tasks_with_complexity = session.query(Task).filter(
            Task.extra_data.like('%complexity%')
        ).all()
        assert len(backend_tasks_with_complexity) == 1

        # Test JSON field queries (PostgreSQL-specific)
        payment_tasks = session.query(Task).filter(
            Task.extra_data.contains('gateway')
        ).all()
        assert len(payment_tasks) == 1

    def test_yaml_integration_with_postgresql(self: "TestAPIPostgreSQLIntegration", session: Any) -> None:
        """Test YAML data import/export functionality with PostgreSQL."""
        # Create YAML test data
        yaml_content = """
project:
  name: "YAML Integration Test"
  description: "Testing YAML import with PostgreSQL"

goals:
  - title: "Setup Development Environment"
    description: "Configure development tools and environment"
    owner: "dev-lead"
    severity: "high"
    work_type: "infrastructure"
    extra_data:
      tools: ["docker", "postgresql", "python"]
      setup_time: "2h"

  - title: "Implement Core Features"
    description: "Develop main application features"
    owner: "tech-lead"
    severity: "high"
    work_type: "feature"
    extra_data:
      features: ["authentication", "crud", "api"]
      estimated_days: 10

tasks:
  - title: "Database Schema Design"
    description: "Design PostgreSQL database schema"
    owner: "database-architect"
    severity: "high"
    work_type: "design"
    extra_data:
      tables: 15
      relationships: "complex"
      optimization_required: true

labels:
  - name: "development"
  - name: "database"
  - name: "api"
"""

        # Parse YAML and create models
        yaml_data = yaml.safe_load(yaml_content)

        created_goals = []
        created_tasks = []
        created_labels = []

        # Process goals
        for goal_data in yaml_data["goals"]:
            goal = Goal(
                title=goal_data["title"],
                description=goal_data["description"],
                owner=goal_data["owner"],
                severity=goal_data["severity"],
                work_type=goal_data["work_type"],
                extra_data=json.dumps(goal_data.get("extra_data", {}))
            )
            created_goals.append(goal)

        # Process tasks
        for task_data in yaml_data["tasks"]:
            task = Task(
                title=task_data["title"],
                description=task_data["description"],
                owner=task_data["owner"],
                severity=task_data["severity"],
                work_type=task_data["work_type"],
                extra_data=json.dumps(task_data.get("extra_data", {}))
            )
            created_tasks.append(task)

        # Process labels
        for label_data in yaml_data["labels"]:
            label = Label(name=label_data["name"])
            created_labels.append(label)

        # Save to PostgreSQL
        session.add_all(created_goals + created_tasks + created_labels)
        session.commit()

        # Verify data integrity in PostgreSQL
        assert session.query(Goal).count() == 2
        assert session.query(Task).count() == 1
        assert session.query(Label).count() == 3

        # Verify complex JSON data preservation
        dev_goal = session.query(Goal).filter(
            Goal.title == "Setup Development Environment"
        ).first()
        assert dev_goal is not None

        dev_extra = json.loads(dev_goal.extra_data)
        assert "docker" in dev_extra["tools"]
        assert dev_extra["setup_time"] == "2h"

        # Test YAML export functionality
        exported_goals = session.query(Goal).all()
        yaml_export_data = {
            "goals": [
                {
                    "title": goal.title,
                    "description": goal.description,
                    "owner": goal.owner,
                    "severity": goal.severity,
                    "work_type": goal.work_type,
                    "extra_data": json.loads(goal.extra_data) if goal.extra_data else {}
                }
                for goal in exported_goals
            ]
        }

        # Verify YAML can be serialized back
        yaml_output = yaml.dump(yaml_export_data, default_flow_style=False)
        parsed_back = yaml.safe_load(yaml_output)
        assert len(parsed_back["goals"]) == 2

    def test_database_performance_and_scaling(self: "TestAPIPostgreSQLIntegration", postgresql_url: str) -> None:
        """Test database performance characteristics with PostgreSQL."""
        # Create a separate engine for performance testing
        perf_engine = create_engine(postgresql_url)
        perf_session = sessionmaker(bind=perf_engine)()

        try:
            # Test bulk insert performance
            import time

            start_time = time.time()

            # Create large dataset
            bulk_goals = [
                Goal(
                    title=f"Performance Test Goal {i}",
                    description=f"Testing PostgreSQL performance with record {i}",
                    owner=f"user-{i % 10}",  # 10 different users
                    severity=["low", "medium", "high", "critical"][i % 4],
                    work_type=["feature", "bug-fix", "documentation", "testing"][i % 4],
                    extra_data=json.dumps({
                        "batch_id": i // 100,
                        "timestamp": time.time(),
                        "metadata": {"test": True, "record": i}
                    })
                )
                for i in range(1000)  # 1000 records
            ]

            perf_session.add_all(bulk_goals)
            perf_session.commit()

            bulk_insert_time = time.time() - start_time

            # Should complete bulk insert reasonably fast (under 10 seconds)
            assert bulk_insert_time < 10.0, f"Bulk insert too slow: {bulk_insert_time:.2f}s"

            # Test complex query performance
            start_time = time.time()

            # Complex query with filtering and JSON operations
            complex_results = perf_session.query(Goal).filter(
                Goal.severity.in_(["high", "critical"]),
                Goal.extra_data.contains('batch_id'),
                Goal.title.like("%Performance Test%")
            ).all()

            query_time = time.time() - start_time

            # Should complete complex query quickly (under 2 seconds)
            assert query_time < 2.0, f"Complex query too slow: {query_time:.2f}s"
            assert len(complex_results) > 0

            # Test index usage (should use title index if available)
            start_time = time.time()

            indexed_query = perf_session.query(Goal).filter(
                Goal.title == "Performance Test Goal 500"
            ).first()

            index_query_time = time.time() - start_time

            # Should be very fast with proper indexing
            assert index_query_time < 0.1, f"Indexed query too slow: {index_query_time:.4f}s"
            assert indexed_query is not None

        finally:
            perf_session.close()
            perf_engine.dispose()

    def test_transaction_isolation_and_concurrency(self: "TestAPIPostgreSQLIntegration", postgresql_url: str) -> None:
        """Test transaction isolation and concurrent access."""
        # Create multiple engines for concurrent testing
        engines = [create_engine(postgresql_url) for _ in range(3)]
        sessions = [sessionmaker(bind=engine)() for engine in engines]

        try:
            # Test concurrent writes
            def create_concurrent_goal(session_num: int, session: Any) -> int:
                """Create a goal in a specific session."""
                goal = Goal(
                    title=f"Concurrent Goal {session_num}",
                    description=f"Created by session {session_num}",
                    owner=f"user-{session_num}"
                )
                session.add(goal)
                session.commit()
                return goal.id

            # Create goals concurrently
            goal_ids = []
            for i, session in enumerate(sessions):
                goal_id = create_concurrent_goal(i + 1, session)
                goal_ids.append(goal_id)

            # Verify all goals were created with unique IDs
            assert len(set(goal_ids)) == 3, "Concurrent goals should have unique IDs"

            # Test transaction isolation
            # Start a transaction in session 0
            test_goal = Goal(
                title="Isolation Test",
                description="Testing transaction isolation",
                owner="test-user"
            )
            sessions[0].add(test_goal)
            sessions[0].flush()  # Get ID but don't commit yet

            # Other sessions should not see this uncommitted data
            for i in range(1, 3):
                invisible_goal = sessions[i].query(Goal).filter(
                    Goal.title == "Isolation Test"
                ).first()
                assert invisible_goal is None, "Uncommitted data should not be visible"

            # Commit and verify visibility
            sessions[0].commit()

            for session in sessions:
                visible_goal = session.query(Goal).filter(
                    Goal.title == "Isolation Test"
                ).first()
                assert visible_goal is not None, "Committed data should be visible"

        finally:
            # Clean up
            for session in sessions:
                session.close()
            for engine in engines:
                engine.dispose()