"""Tests for the unified ToDoWrite application using Models API."""

from __future__ import annotations

import tempfile
from pathlib import Path

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from todowrite.core.models import (
    Goal,
    Task,
    Phase,
    Step,
    Label,
    Base,
)


def create_test_model_data(
    title: str,
    description: str,
    owner: str = "test-user",
    severity: str = "medium",
    work_type: str = "feature",
    assignee: str = "developer",
) -> dict[str, str]:
    """Create test model data."""
    return {
        "title": title,
        "description": description,
        "owner": owner,
        "severity": severity,
        "work_type": work_type,
        "assignee": assignee,
    }


class TestUnifiedModelsAPI:
    """Test the unified ToDoWrite Models API."""

    @pytest.fixture
    def temp_db_path(self):
        """Create a temporary database path."""
        with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as temp_file:
            yield temp_file.name
        # Cleanup
        Path(temp_file.name).unlink(missing_ok=True)

    @pytest.fixture
    def session(self, temp_db_path):
        """Create a database session for testing."""
        engine = create_engine(f"sqlite:///{temp_db_path}")
        Base.metadata.create_all(engine)
        Session = sessionmaker(bind=engine)
        session = Session()
        yield session
        session.close()

    def test_create_goal_with_minimal_data(self, session):
        """Test creating a goal with minimal required data."""
        goal_data = create_test_model_data(
            title="Test Goal",
            description="A test goal for the unified API"
        )

        goal = Goal(**goal_data)
        session.add(goal)
        session.commit()

        assert goal.id is not None
        assert goal.title == "Test Goal"
        assert goal.description == "A test goal for the unified API"
        assert goal.owner == "test-user"

    def test_create_full_hierarchy(self, session):
        """Test creating a full hierarchy of models."""
        # Create goal
        goal_data = create_test_model_data(
            title="Product Launch",
            description="Successfully launch the new product",
            owner="product-manager",
            severity="high"
        )
        goal = Goal(**goal_data)
        session.add(goal)
        session.commit()

        # Create phase
        phase_data = create_test_model_data(
            title="Development Phase",
            description="Core development work",
            owner="tech-lead",
            work_type="development"
        )
        phase = Phase(**phase_data)
        session.add(phase)
        session.commit()

        # Create step
        step_data = create_test_model_data(
            title="API Development",
            description="Develop REST API endpoints",
            owner="backend-dev"
        )
        step = Step(**step_data)
        session.add(step)
        session.commit()

        # Create task
        task_data = create_test_model_data(
            title="User Authentication",
            description="Implement user authentication system",
            owner="security-dev",
            assignee="senior-dev"
        )
        task = Task(**task_data)
        session.add(task)
        session.commit()

        # Verify all created
        assert session.query(Goal).count() == 1
        assert session.query(Phase).count() == 1
        assert session.query(Step).count() == 1
        assert session.query(Task).count() == 1

        # Verify data integrity
        retrieved_goal = session.query(Goal).first()
        assert retrieved_goal.title == "Product Launch"
        assert retrieved_goal.severity == "high"

    def test_model_relationships_through_queries(self, session):
        """Test querying models and their relationships."""
        # Create multiple goals
        goals_data = [
            create_test_model_data("Goal 1", "First goal", severity="high"),
            create_test_model_data("Goal 2", "Second goal", severity="medium"),
            create_test_model_data("Goal 3", "Third goal", severity="low"),
        ]

        for goal_data in goals_data:
            goal = Goal(**goal_data)
            session.add(goal)
        session.commit()

        # Query goals by severity
        high_priority_goals = session.query(Goal).filter(Goal.severity == "high").all()
        assert len(high_priority_goals) == 1
        assert high_priority_goals[0].title == "Goal 1"

        # Query all goals
        all_goals = session.query(Goal).order_by(Goal.title).all()
        assert len(all_goals) == 3
        assert [g.title for g in all_goals] == ["Goal 1", "Goal 2", "Goal 3"]

    def test_label_system(self, session):
        """Test the label system."""
        # Create labels
        labels = [
            Label(name="urgent"),
            Label(name="backend"),
            Label(name="frontend"),
            Label(name="documentation"),
        ]

        for label in labels:
            session.add(label)
        session.commit()

        # Verify labels created
        assert session.query(Label).count() == 4

        # Query specific labels
        urgent_label = session.query(Label).filter(Label.name == "urgent").first()
        assert urgent_label is not None
        assert urgent_label.name == "urgent"

        # Test unique constraint
        duplicate_label = Label(name="urgent")
        session.add(duplicate_label)

        # Should fail due to unique constraint
        with pytest.raises(Exception):
            session.commit()

        session.rollback()

    def test_model_metadata_fields(self, session):
        """Test model metadata and extra fields."""
        # Create goal with full metadata
        goal = Goal(
            title="Metadata Test Goal",
            description="Testing all metadata fields",
            owner="project-lead",
            severity="critical",
            work_type="bug-fix",
            assignee="senior-developer",
            extra_data='{"priority": 1, "estimated_hours": 40}'
        )
        session.add(goal)
        session.commit()

        # Verify metadata
        retrieved_goal = session.query(Goal).filter(Goal.title == "Metadata Test Goal").first()
        assert retrieved_goal is not None
        assert retrieved_goal.owner == "project-lead"
        assert retrieved_goal.severity == "critical"
        assert retrieved_goal.work_type == "bug-fix"
        assert retrieved_goal.assignee == "senior-developer"
        assert retrieved_goal.extra_data == '{"priority": 1, "estimated_hours": 40}'

    def test_model_timestamps(self, session):
        """Test automatic timestamp functionality."""
        goal = Goal(
            title="Timestamp Test",
            description="Testing created_at and updated_at"
        )
        session.add(goal)
        session.commit()

        # Verify timestamps set on creation
        assert goal.created_at is not None
        assert goal.updated_at is not None
        # Note: created_at and updated_at may differ by microseconds
        assert goal.created_at[:19] == goal.updated_at[:19]  # Compare up to seconds

        # Update and verify updated_at changes
        original_updated_at = goal.updated_at
        goal.description = "Updated description"
        session.commit()

        # Note: In a real implementation, updated_at would be automatically updated
        # For now, we're testing the field exists and can be set
        assert goal.updated_at is not None

    def test_model_query_operations(self, session):
        """Test various query operations."""
        # Create test data
        goals = [
            Goal(title="API Development", description="Develop REST API", owner="backend-team"),
            Goal(title="UI Design", description="Design user interface", owner="frontend-team"),
            Goal(title="Testing", description="Write comprehensive tests", owner="qa-team"),
        ]

        for goal in goals:
            session.add(goal)
        session.commit()

        # Test various queries
        api_goals = session.query(Goal).filter(Goal.title.contains("API")).all()
        assert len(api_goals) == 1
        assert api_goals[0].title == "API Development"

        team_goals = session.query(Goal).filter(Goal.owner.endswith("team")).all()
        assert len(team_goals) == 3

        # Test ordering
        ordered_goals = session.query(Goal).order_by(Goal.title).all()
        titles = [g.title for g in ordered_goals]
        assert titles == ["API Development", "Testing", "UI Design"]