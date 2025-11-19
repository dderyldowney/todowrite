"""
PostgreSQL Docker Test Suite

Comprehensive tests for PostgreSQL setup, teardown, schema import/export,
and new API functionality using PostgreSQL as the backend.
"""

from __future__ import annotations

import json
import tempfile
from pathlib import Path
from typing import Any, Dict

import pytest
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

# Import Docker utilities
try:
    from .docker_utils import (
        DockerManager,
        TestPostgreSQLConfig,
        docker_manager,
        skip_if_no_docker,
    )
except ImportError:
    # Fallback for when running directly
    import sys
    from pathlib import Path

    # Add the parent directory to path so we can import docker_utils
    parent_dir = Path(__file__).parent.parent.parent
    if str(parent_dir) not in sys.path:
        sys.path.insert(0, str(parent_dir))

    from tests.lib.docker.docker_utils import (
        DockerManager,
        TestPostgreSQLConfig,
        docker_manager,
        skip_if_no_docker,
    )


@pytest.mark.skipif(
    not docker_manager.is_docker_available(),
    reason="Docker is not available or not running",
)
class TestPostgreSQLDocker:
    """Test PostgreSQL Docker setup and management."""

    @pytest.fixture(scope="class")
    def postgresql_container(self: "TestPostgreSQLDocker") -> str:
        """Start PostgreSQL container for testing."""
        # Start the container
        if not docker_manager.start_postgresql_container():
            pytest.skip("Failed to start PostgreSQL container")

        yield TestPostgreSQLConfig.get_connection_url()

        # Cleanup
        docker_manager.stop_postgresql_container()

    @pytest.fixture
    def postgresql_session(self: "TestPostgreSQLDocker", postgresql_container: str) -> Any:
        """Create database session for PostgreSQL testing."""
        engine = create_engine(postgresql_container)
        Base.metadata.create_all(engine)

        Session = sessionmaker(bind=engine)
        session = Session()

        yield session

        session.close()

    def test_docker_availability_detection(self: "TestPostgreSQLDocker") -> None:
        """Test Docker availability detection."""
        manager = DockerManager()

        # Should detect Docker is available
        assert manager.is_docker_available()

        # Should find compose files
        assert len(manager.compose_files) > 0
        assert any("docker-compose" in name for name in manager.compose_files.keys())

    def test_postgresql_container_lifecycle(self: "TestPostgreSQLDocker") -> None:
        """Test PostgreSQL container start/stop lifecycle."""
        compose_file = "docker-compose"

        # Start container
        assert docker_manager.start_postgresql_container(compose_file=compose_file)

        # Verify container is running
        connection_url = docker_manager.get_postgresql_connection_url()
        assert connection_url is not None

        # Test basic connection
        engine = create_engine(connection_url)
        with engine.connect() as conn:
            result = conn.execute(text("SELECT 1"))
            assert result.scalar() == 1

        # Stop container
        assert docker_manager.stop_postgresql_container(compose_file=compose_file)

    def test_database_schema_creation(self: "TestPostgreSQLDocker", postgresql_session: Any) -> None:
        """Test database schema creation in PostgreSQL."""
        # Test that all tables were created
        with postgresql_session.bind.connect() as conn:
            result = conn.execute(
                text("""
                    SELECT table_name
                    FROM information_schema.tables
                    WHERE table_schema = 'public'
                    ORDER BY table_name
                """)
            )
            tables = [row[0] for row in result]

        # Should have all our model tables
        expected_tables = {
            'goals', 'concepts', 'contexts', 'constraints',
            'requirements', 'acceptance_criteria', 'interface_contracts',
            'phases', 'steps', 'tasks', 'sub_tasks', 'commands', 'labels'
        }

        for table in expected_tables:
            assert table in tables, f"Table {table} should exist"

        # Should have association tables
        association_tables = [t for t in tables if '_' in t and 'labels' in t]
        assert len(association_tables) > 0, "Should have association tables"

    def test_postgresql_model_operations(self: "TestPostgreSQLDocker", postgresql_session: Any) -> None:
        """Test SQLAlchemy model operations with PostgreSQL."""
        # Create test data
        goal = Goal(
            title="PostgreSQL Test Goal",
            description="Testing model operations with PostgreSQL",
            owner="test-user",
            severity="high",
            work_type="feature",
            assignee="developer",
            extra_data='{"priority": 1, "environment": "postgresql"}'
        )

        task = Task(
            title="PostgreSQL Test Task",
            description="Testing task operations with PostgreSQL",
            owner="test-user",
            severity="medium",
            work_type="testing",
            assignee="qa-engineer"
        )

        label = Label(name="postgresql-test")

        postgresql_session.add_all([goal, task, label])
        postgresql_session.commit()

        # Verify data persistence
        retrieved_goal = postgresql_session.query(Goal).filter(
            Goal.title == "PostgreSQL Test Goal"
        ).first()
        assert retrieved_goal is not None
        assert retrieved_goal.severity == "high"

        retrieved_task = postgresql_session.query(Task).filter(
            Task.title == "PostgreSQL Test Task"
        ).first()
        assert retrieved_task is not None
        assert retrieved_task.work_type == "testing"

        retrieved_label = postgresql_session.query(Label).filter(
            Label.name == "postgresql-test"
        ).first()
        assert retrieved_label is not None

        # Test extra_data JSON field
        extra_data = json.loads(retrieved_goal.extra_data)
        assert extra_data["environment"] == "postgresql"
        assert extra_data["priority"] == 1

    def test_postgresql_relationships_and_constraints(
        self: "TestPostgreSQLDocker",
        postgresql_session: Any
    ) -> None:
        """Test PostgreSQL foreign key relationships and constraints."""
        # Create goal and labels
        goal = Goal(title="Relationship Test", description="Testing relationships")
        label1 = Label(name="urgent")
        label2 = Label(name="backend")

        postgresql_session.add_all([goal, label1, label2])
        postgresql_session.commit()

        # Add labels to goal (many-to-many relationship)
        goal.labels.append(label1)
        goal.labels.append(label2)
        postgresql_session.commit()

        # Verify relationship
        retrieved_goal = postgresql_session.query(Goal).filter(
            Goal.title == "Relationship Test"
        ).first()
        assert len(retrieved_goal.labels) == 2

        label_names = [label.name for label in retrieved_goal.labels]
        assert "urgent" in label_names
        assert "backend" in label_names

        # Test unique constraint on labels
        duplicate_label = Label(name="urgent")
        postgresql_session.add(duplicate_label)

        with pytest.raises(Exception):  # Should raise IntegrityError
            postgresql_session.commit()

    def test_postgresql_transaction_handling(
        self: "TestPostgreSQLDocker",
        postgresql_session: Any
    ) -> None:
        """Test PostgreSQL transaction handling and rollback."""
        initial_count = postgresql_session.query(Goal).count()

        # Test successful transaction
        try:
            goal1 = Goal(title="Transaction Test 1", description="First test")
            goal2 = Goal(title="Transaction Test 2", description="Second test")

            postgresql_session.add_all([goal1, goal2])
            postgresql_session.commit()

            assert postgresql_session.query(Goal).count() == initial_count + 2

        except Exception as e:
            postgresql_session.rollback()
            pytest.fail(f"Successful transaction failed: {e}")

        # Test transaction rollback
        try:
            goal3 = Goal(title="Rollback Test", description="Should be rolled back")
            postgresql_session.add(goal3)
            postgresql_session.flush()

            # Create duplicate label to trigger constraint violation
            existing_label = Label(name="rollback-test")
            postgresql_session.add(existing_label)
            postgresql_session.commit()

            duplicate_label = Label(name="rollback-test")
            postgresql_session.add(duplicate_label)
            postgresql_session.commit()

        except Exception:
            postgresql_session.rollback()

        # Verify rollback worked
        final_count = postgresql_session.query(Goal).count()
        assert final_count == initial_count + 2  # Only the successful ones

    def test_postgresql_performance_characteristics(
        self: "TestPostgreSQLDocker",
        postgresql_session: Any
    ) -> None:
        """Test PostgreSQL performance characteristics."""
        import time

        # Test bulk insert performance
        start_time = time.time()

        goals = [
            Goal(title=f"Performance Goal {i}", description=f"Test {i}")
            for i in range(100)
        ]

        postgresql_session.add_all(goals)
        postgresql_session.commit()

        insert_time = time.time() - start_time

        # Should complete reasonably fast (under 5 seconds for 100 records)
        assert insert_time < 5.0, f"Bulk insert took too long: {insert_time:.2f} seconds"

        # Test bulk query performance
        start_time = time.time()

        all_goals = postgresql_session.query(Goal).filter(
            Goal.title.like("Performance Goal%")
        ).all()

        query_time = time.time() - start_time

        # Should query 100 records quickly
        assert query_time < 1.0, f"Bulk query took too long: {query_time:.2f} seconds"
        assert len(all_goals) == 100

    def test_postgresql_schema_export_import(
        self: "TestPostgreSQLDocker",
        postgresql_container: str
    ) -> None:
        """Test PostgreSQL schema export and import functionality."""
        # Create a temporary database for testing import/export
        test_db_url = TestPostgreSQLConfig.get_connection_url(database="todowrite_test")

        try:
            # Create test database and schema
            engine = create_engine(test_db_url)
            Base.metadata.create_all(engine)

            # Add test data
            Session = sessionmaker(bind=engine)
            session = Session()

            goal = Goal(
                title="Export Test Goal",
                description="Testing export functionality",
                owner="export-test",
                severity="critical"
            )
            session.add(goal)
            session.commit()
            session.close()

            # Export schema
            with tempfile.NamedTemporaryFile(mode='w', suffix='.sql', delete=False) as temp_file:
                temp_path = temp_file.name

            # Use pg_dump to export schema
            import subprocess
            config = TestPostgreSQLConfig.DEFAULT_CONFIG

            dump_cmd = [
                "pg_dump",
                "--host", config["host"],
                "--port", str(config["port"]),
                "--username", config["username"],
                "--no-password",
                "--schema-only",
                "--no-owner",
                "--no-privileges",
                "--file", temp_path,
                config["database"]
            ]

            # Set PGPASSWORD environment variable for pg_dump
            import os
            env = os.environ.copy()
            env["PGPASSWORD"] = config["password"]

            subprocess.run(dump_cmd, env=env, check=True, capture_output=True)

            # Verify export file exists and has content
            assert Path(temp_path).exists()
            assert Path(temp_path).stat().st_size > 0

            # Clean up test database
            engine.dispose()

            # Drop test database
            drop_engine = create_engine(
                f"postgresql://{config['username']}:{config['password']}"
                f"@{config['host']}:{config['port']}/postgres"
            )
            with drop_engine.connect() as conn:
                conn.execute(text("DROP DATABASE IF EXISTS todowrite_test"))
                conn.commit()

        finally:
            # Clean up temp file
            Path(temp_path).unlink(missing_ok=True)
            if 'engine' in locals():
                engine.dispose()
            if 'drop_engine' in locals():
                drop_engine.dispose()

    def test_postgresql_data_types_support(
        self: "TestPostgreSQLDocker",
        postgresql_session: Any
    ) -> None:
        """Test PostgreSQL-specific data type support."""
        # Test JSON field with complex data
        complex_data = {
            "metadata": {
                "nested": {
                    "arrays": [1, 2, 3],
                    "objects": {"key": "value"},
                    "boolean": True,
                    "null": None
                }
            },
            "tags": ["postgresql", "testing", "json"],
            "config": {
                "enabled": True,
                "timeout": 30.5
            }
        }

        goal = Goal(
            title="JSON Data Type Test",
            description="Testing PostgreSQL JSON field support",
            extra_data=json.dumps(complex_data)
        )

        postgresql_session.add(goal)
        postgresql_session.commit()

        # Retrieve and verify JSON data integrity
        retrieved_goal = postgresql_session.query(Goal).filter(
            Goal.title == "JSON Data Type Test"
        ).first()

        assert retrieved_goal is not None

        retrieved_data = json.loads(retrieved_goal.extra_data)
        assert retrieved_data == complex_data
        assert retrieved_data["metadata"]["nested"]["arrays"] == [1, 2, 3]
        assert retrieved_data["tags"] == ["postgresql", "testing", "json"]
        assert retrieved_data["config"]["enabled"] is True

    def test_postgresql_concurrent_access(
        self: "TestPostgreSQLDocker",
        postgresql_container: str
    ) -> None:
        """Test PostgreSQL concurrent access handling."""
        # Create multiple sessions to test concurrency
        engines = [
            create_engine(postgresql_container)
            for _ in range(3)
        ]

        sessions = [
            sessionmaker(bind=engine)()
            for engine in engines
        ]

        try:
            # Create goals concurrently
            goals_data = [
                {"title": f"Concurrent Goal {i}", "description": f"Created by session {i}"}
                for i in range(3)
            ]

            for i, (session, goal_data) in enumerate(zip(sessions, goals_data)):
                goal = Goal(**goal_data)
                session.add(goal)
                session.commit()

            # Verify all data was created correctly
            total_goals = sum(
                session.query(Goal).filter(
                    Goal.title.like("Concurrent Goal%")
                ).count()
                for session in sessions
            )

            # Should have 3 unique goals
            assert total_goals >= 3

        finally:
            # Clean up sessions
            for session in sessions:
                session.close()
            for engine in engines:
                engine.dispose()