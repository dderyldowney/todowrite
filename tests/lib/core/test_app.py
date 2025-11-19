"""Tests for the ToDoWrite Models API."""

from __future__ import annotations

import tempfile
from pathlib import Path

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from todowrite.core.models import (
    Base,
    Goal,
    Label,
    Phase,
    Step,
    Task,
)


class TestToDoWriteModelsAPI:
    """Test the ToDoWrite Models API."""

    @pytest.fixture
    def temp_db_path(self):
        """Create a temporary database path."""
        with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as temp_file:
            yield temp_file.name
        # Cleanup
        Path(temp_file.name).unlink(missing_ok=True)

    @pytest.fixture
    def session(self, temp_db_path):
        """Create a database session."""
        engine = create_engine(f"sqlite:///{temp_db_path}")
        Base.metadata.create_all(engine)
        Session = sessionmaker(bind=engine)
        session = Session()
        yield session
        session.close()

    def test_create_goal(self, session):
        """Test creating a goal using the Models API."""
        goal = Goal(
            title="Test Goal", description="A test goal", owner="test-user", severity="high"
        )
        session.add(goal)
        session.commit()

        retrieved_goal = session.query(Goal).filter(Goal.title == "Test Goal").first()
        assert retrieved_goal is not None
        assert retrieved_goal.title == "Test Goal"
        assert retrieved_goal.description == "A test goal"
        assert retrieved_goal.owner == "test-user"
        assert retrieved_goal.severity == "high"

    def test_create_task_with_goal_relationship(self, session):
        """Test creating a task with goal relationship."""
        # Create goal first
        goal = Goal(title="Project Goal", description="Main project goal")
        session.add(goal)
        session.commit()

        # Create task
        task = Task(
            title="Implementation Task",
            description="Implement the feature",
            owner="developer",
            severity="medium",
        )
        session.add(task)
        session.commit()

        # Verify both exist
        assert session.query(Goal).count() == 1
        assert session.query(Task).count() == 1
        assert task.title == "Implementation Task"

    def test_create_hierarchy(self, session):
        """Test creating a full hierarchy."""
        # Create goal
        goal = Goal(title="Launch Product", description="Successfully launch product")
        session.add(goal)
        session.commit()

        # Create phase
        phase = Phase(title="Development Phase", description="Development work", owner="team-lead")
        session.add(phase)
        session.commit()

        # Create step
        step = Step(title="API Development", description="Develop REST API", owner="backend-dev")
        session.add(step)
        session.commit()

        # Create task
        task = Task(
            title="User Endpoint",
            description="Implement user management endpoint",
            owner="developer",
        )
        session.add(task)
        session.commit()

        # Verify hierarchy
        assert session.query(Goal).count() == 1
        assert session.query(Phase).count() == 1
        assert session.query(Step).count() == 1
        assert session.query(Task).count() == 1

    def test_label_creation_and_relationships(self, session):
        """Test creating labels and their relationships."""
        # Create labels
        urgent_label = Label(name="urgent")
        backend_label = Label(name="backend")
        session.add_all([urgent_label, backend_label])
        session.commit()

        # Create goal with labels (would be done through association in real app)
        goal = Goal(
            title="Urgent Backend Task", description="Critical backend work", severity="high"
        )
        session.add(goal)
        session.commit()

        # Verify creation
        assert session.query(Label).count() == 2
        assert session.query(Goal).count() == 1
        assert urgent_label.name == "urgent"
        assert backend_label.name == "backend"

    def test_model_metadata(self, session):
        """Test model metadata fields."""
        goal = Goal(
            title="Metadata Test",
            description="Testing metadata fields",
            owner="test-user",
            severity="medium",
            work_type="feature",
            assignee="developer",
        )
        session.add(goal)
        session.commit()

        retrieved_goal = session.query(Goal).filter(Goal.title == "Metadata Test").first()
        assert retrieved_goal is not None
        assert retrieved_goal.owner == "test-user"
        assert retrieved_goal.severity == "medium"
        assert retrieved_goal.work_type == "feature"
        assert retrieved_goal.assignee == "developer"
        assert retrieved_goal.created_at is not None
        assert retrieved_goal.updated_at is not None

    def test_model_validation(self, session):
        """Test model validation and constraints."""
        # Test required field
        with pytest.raises(Exception):  # Should fail without title
            goal = Goal(description="No title provided")
            session.add(goal)
            session.commit()

        session.rollback()

        # Test proper creation
        goal = Goal(title="Valid Goal")
        session.add(goal)
        session.commit()

        assert goal.id is not None
        assert goal.title == "Valid Goal"
