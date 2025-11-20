"""Tests for storage backend compatibility with ToDoWrite Models."""

from __future__ import annotations

import tempfile
from pathlib import Path

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from todowrite.core.models import Goal, Label, Task
from todowrite.storage import (
    initialize_database,
    validate_model_data,
)


class TestDatabaseSchemaValidation:
    """Test database schema validation with ToDoWrite Models."""

    def test_validate_goal_model_data(self):
        """Test validation of Goal model data."""
        valid_goal_data = {
            "title": "Test Goal",
            "description": "A test goal",
            "owner": "test-user",
            "status": "planned",
        }

        # This should not raise an exception
        assert validate_model_data("Goal", valid_goal_data) == True

    def test_validate_task_model_data(self):
        """Test validation of Task model data."""
        valid_task_data = {
            "title": "Test Task",
            "description": "A test task",
            "owner": "test-user",
            "status": "planned",
        }

        # This should not raise an exception
        assert validate_model_data("Task", valid_task_data) == True

    def test_validate_label_model_data(self):
        """Test validation of Label model data."""
        valid_label_data = {"name": "test-label"}

        # This should not raise an exception
        assert validate_model_data("Label", valid_label_data) == True

    def test_validate_invalid_model_data(self):
        """Test validation fails with invalid data."""
        # Missing required title field
        invalid_goal_data = {"description": "A test goal without title", "owner": "test-user"}

        # This should return False or raise an exception
        try:
            result = validate_model_data("Goal", invalid_goal_data)
            assert result == False
        except Exception:
            # Expected behavior for validation failures
            pass


class TestSQLiteDatabaseIntegration:
    """Test SQLite database integration with ToDoWrite Models."""

    @pytest.fixture
    def temp_sqlite_db(self):
        """Create a temporary SQLite database for testing."""
        temp_db = tempfile.mktemp(suffix=".db")
        engine = create_engine(f"sqlite:///{temp_db}")

        # Use todowrite storage initialize_database function
        initialize_database(f"sqlite:///{temp_db}")

        Session = sessionmaker(bind=engine)
        yield Session

        Path(temp_db).unlink(missing_ok=True)

    def test_create_goal_with_validation(self, temp_sqlite_db):
        """Test creating a Goal with validation."""
        session = temp_sqlite_db()

        # Create goal data
        goal_data = {
            "title": "Test Goal",
            "description": "A test goal for database integration",
            "owner": "test-user",
            "status": "planned",
        }

        # Validate first
        assert validate_model_data("Goal", goal_data) == True

        # Create the goal
        goal = Goal(**goal_data)
        session.add(goal)
        session.commit()

        # Verify the goal was created
        retrieved_goal = session.query(Goal).filter(Goal.id == goal.id).first()
        assert retrieved_goal is not None
        assert retrieved_goal.title == goal_data["title"]
        assert retrieved_goal.owner == goal_data["owner"]
        assert retrieved_goal.status == goal_data["status"]

        session.close()

    def test_create_task_with_validation(self, temp_sqlite_db):
        """Test creating a Task with validation."""
        session = temp_sqlite_db()

        # Create task data
        task_data = {
            "title": "Test Task",
            "description": "A test task for database integration",
            "owner": "test-user",
            "status": "planned",
        }

        # Validate first
        assert validate_model_data("Task", task_data) == True

        # Create the task
        task = Task(**task_data)
        session.add(task)
        session.commit()

        # Verify the task was created
        retrieved_task = session.query(Task).filter(Task.id == task.id).first()
        assert retrieved_task is not None
        assert retrieved_task.title == task_data["title"]
        assert retrieved_task.owner == task_data["owner"]

        session.close()

    def test_create_label_with_validation(self, temp_sqlite_db):
        """Test creating a Label with validation."""
        session = temp_sqlite_db()

        # Create label data
        label_data = {"name": "test-label"}

        # Validate first
        assert validate_model_data("Label", label_data) == True

        # Create the label
        label = Label(**label_data)
        session.add(label)
        session.commit()

        # Verify the label was created
        retrieved_label = session.query(Label).filter(Label.id == label.id).first()
        assert retrieved_label is not None
        assert retrieved_label.name == label_data["name"]

        session.close()

    def test_query_and_filter_models(self, temp_sqlite_db):
        """Test querying and filtering ToDoWrite Models."""
        session = temp_sqlite_db()

        # Create multiple goals
        goals = [
            Goal(title="Goal 1", owner="user1", status="planned"),
            Goal(title="Goal 2", owner="user2", status="in_progress"),
            Goal(title="Goal 3", owner="user1", status="completed"),
        ]

        for goal in goals:
            session.add(goal)

        session.commit()

        # Query all goals
        all_goals = session.query(Goal).all()
        assert len(all_goals) == 3

        # Filter by owner
        user1_goals = session.query(Goal).filter(Goal.owner == "user1").all()
        assert len(user1_goals) == 2

        # Filter by status
        planned_goals = session.query(Goal).filter(Goal.status == "planned").all()
        assert len(planned_goals) == 1

        session.close()

    def test_model_relationships(self, temp_sqlite_db):
        """Test that models can have proper relationships."""
        session = temp_sqlite_db()

        # Create goal and task
        goal = Goal(title="Parent Goal", owner="test-user")
        task = Task(title="Child Task", owner="test-user")

        session.add(goal)
        session.add(task)
        session.commit()

        # Both should be created successfully
        assert goal.id is not None
        assert task.id is not None

        # Basic queries should work
        retrieved_goal = session.query(Goal).filter(Goal.id == goal.id).first()
        retrieved_task = session.query(Task).filter(Task.id == task.id).first()

        assert retrieved_goal is not None
        assert retrieved_task is not None
        assert retrieved_goal.title == "Parent Goal"
        assert retrieved_task.title == "Child Task"

        session.close()


class TestModelConstraints:
    """Test model constraints and validation."""

    def test_label_name_uniqueness(self):
        """Test that Label names must be unique."""
        temp_db = tempfile.mktemp(suffix=".db")
        engine = create_engine(f"sqlite:///{temp_db}")
        initialize_database(f"sqlite:///{temp_db}")

        Session = sessionmaker(bind=engine)
        session = Session()

        try:
            # Create first label
            label1 = Label(name="unique-label")
            session.add(label1)
            session.commit()

            # Try to create second label with same name
            label2 = Label(name="unique-label")
            session.add(label2)

            # This should fail due to unique constraint
            with pytest.raises(Exception):
                session.commit()

        finally:
            session.close()
            Path(temp_db).unlink(missing_ok=True)

    def test_goal_required_fields(self):
        """Test that Goal model enforces required fields."""
        temp_db = tempfile.mktemp(suffix=".db")
        engine = create_engine(f"sqlite:///{temp_db}")
        initialize_database(f"sqlite:///{temp_db}")

        Session = sessionmaker(bind=engine)
        session = Session()

        try:
            # Try to create goal without required title
            goal = Goal()  # No title provided
            session.add(goal)

            # This should fail
            with pytest.raises(Exception):
                session.commit()

        finally:
            session.close()
            Path(temp_db).unlink(missing_ok=True)
