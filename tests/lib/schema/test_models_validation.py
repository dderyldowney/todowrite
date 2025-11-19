"""
Models Validation Tests

Tests for validating ToDoWrite models using modern SQLAlchemy patterns.
Replaces the legacy schema validation functionality.
"""

import json
import tempfile
from pathlib import Path

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from todowrite.core.models import (
    Base,
    Command,
    Goal,
    Label,
    Task,
)


class TestModelsValidation:
    """Test class for validating ToDoWrite models."""

    @pytest.fixture
    def temp_session(self):
        """Create a temporary database session."""
        with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as temp_file:
            db_path = temp_file.name

        engine = create_engine(f"sqlite:///{db_path}")
        Base.metadata.create_all(engine)
        Session = sessionmaker(bind=engine)
        session = Session()

        yield session

        session.close()
        Path(db_path).unlink(missing_ok=True)

    def test_goal_model_validation(self, temp_session):
        """Test Goal model validation rules."""
        # Test valid goal
        valid_goal = Goal(
            title="Valid Goal",
            description="A properly formatted goal",
            owner="test-user",
            severity="medium",
        )
        temp_session.add(valid_goal)
        temp_session.commit()

        # Verify valid goal persists correctly
        retrieved_goal = temp_session.query(Goal).filter(Goal.title == "Valid Goal").first()
        assert retrieved_goal is not None
        assert retrieved_goal.severity in ["low", "medium", "high", "critical"]

    def test_task_model_validation(self, temp_session):
        """Test Task model validation rules."""
        # Test valid task with all fields
        valid_task = Task(
            title="Valid Task",
            description="A properly formatted task",
            owner="test-user",
            severity="high",
            work_type="feature",
            assignee="developer",
        )
        temp_session.add(valid_task)
        temp_session.commit()

        # Verify valid task persists correctly
        retrieved_task = temp_session.query(Task).filter(Task.title == "Valid Task").first()
        assert retrieved_task is not None
        assert retrieved_task.work_type in ["feature", "bug-fix", "documentation", "testing"]
        assert retrieved_task.severity in ["low", "medium", "high", "critical"]

    def test_label_model_validation(self, temp_session):
        """Test Label model validation rules."""
        # Test valid label
        valid_label = Label(name="urgent")
        temp_session.add(valid_label)
        temp_session.commit()

        # Verify valid label persists correctly
        retrieved_label = temp_session.query(Label).filter(Label.name == "urgent").first()
        assert retrieved_label is not None
        assert len(retrieved_label.name) > 0
        assert (
            retrieved_label.name.isalnum()
            or "-" in retrieved_label.name
            or "_" in retrieved_label.name
        )

    def test_command_model_validation(self, temp_session):
        """Test Command model validation rules."""
        # Test valid command
        valid_command = Command(
            title="Valid Command",
            description="A properly formatted command",
            cmd="echo 'Hello World'",
            cmd_params="--verbose",
            owner="test-user",
        )
        temp_session.add(valid_command)
        temp_session.commit()

        # Verify valid command persists correctly
        retrieved_command = (
            temp_session.query(Command).filter(Command.title == "Valid Command").first()
        )
        assert retrieved_command is not None
        assert retrieved_command.cmd is not None
        assert len(retrieved_command.cmd.strip()) > 0

    def test_extra_data_json_validation(self, temp_session):
        """Test extra_data JSON field validation."""
        # Test valid JSON in extra_data
        valid_extra_data = {
            "priority": 1,
            "estimated_hours": 40,
            "tags": ["backend", "api"],
            "metadata": {"complex": True, "nested": {"value": 42}},
        }
        valid_json = json.dumps(valid_extra_data)

        goal = Goal(
            title="Goal with JSON Data",
            description="Testing JSON extra_data field",
            extra_data=valid_json,
        )
        temp_session.add(goal)
        temp_session.commit()

        # Verify JSON persists and can be retrieved
        retrieved_goal = (
            temp_session.query(Goal).filter(Goal.title == "Goal with JSON Data").first()
        )
        assert retrieved_goal is not None

        # Verify JSON is valid
        parsed_data = json.loads(retrieved_goal.extra_data)
        assert parsed_data["priority"] == 1
        assert parsed_data["estimated_hours"] == 40
        assert "backend" in parsed_data["tags"]
        assert parsed_data["metadata"]["nested"]["value"] == 42

    def test_model_relationship_validation(self, temp_session):
        """Test model relationship validation."""
        # Create test data
        goal = Goal(title="Project Goal", description="Main project goal")
        label1 = Label(name="urgent")
        label2 = Label(name="backend")

        temp_session.add_all([goal, label1, label2])
        temp_session.commit()

        # Verify relationships can be established
        assert goal.id is not None
        assert label1.id is not None
        assert label2.id is not None

        # Query models and verify they exist
        goal_count = temp_session.query(Goal).count()
        label_count = temp_session.query(Label).count()

        assert goal_count == 1
        assert label_count == 2

    def test_model_timestamp_validation(self, temp_session):
        """Test model timestamp validation."""
        goal = Goal(title="Timestamp Test", description="Testing automatic timestamps")
        temp_session.add(goal)
        temp_session.commit()

        # Verify timestamps are set and valid
        assert goal.created_at is not None
        assert goal.updated_at is not None
        assert len(goal.created_at) >= 19  # ISO format: "2025-01-01T00:00:00"
        assert len(goal.updated_at) >= 19

        # Verify timestamp format (basic check for ISO datetime)
        assert "T" in goal.created_at
        assert goal.created_at.count("-") == 2  # YYYY-MM-DD

    def test_model_field_length_validation(self, temp_session):
        """Test model field length validation."""
        # Test very long title (should work if no explicit length constraint)
        long_title = "A" * 200  # 200 character title
        goal = Goal(title=long_title, description="Testing long field lengths")
        temp_session.add(goal)
        temp_session.commit()

        retrieved_goal = temp_session.query(Goal).filter(Goal.id == goal.id).first()
        assert retrieved_goal is not None
        assert len(retrieved_goal.title) == 200

    def test_model_data_integrity_validation(self, temp_session):
        """Test model data integrity validation."""
        # Create test data with various data types
        goals_data = [
            {
                "title": "Goal 1",
                "description": "First goal",
                "owner": "user1",
                "severity": "high",
                "extra_data": json.dumps({"priority": 1, "complex": True}),
            },
            {
                "title": "Goal 2",
                "description": "Second goal",
                "owner": "user2",
                "severity": "low",
                "extra_data": json.dumps({"priority": 3, "complex": False}),
            },
        ]

        # Create goals
        for goal_data in goals_data:
            goal = Goal(**goal_data)
            temp_session.add(goal)
        temp_session.commit()

        # Verify data integrity
        all_goals = temp_session.query(Goal).all()
        assert len(all_goals) == 2

        for goal in all_goals:
            # Verify extra_data can be parsed and matches original
            extra_data = json.loads(goal.extra_data)
            assert "priority" in extra_data
            assert "complex" in extra_data
            assert isinstance(extra_data["priority"], int)
            assert isinstance(extra_data["complex"], bool)

    def test_model_query_validation(self, temp_session):
        """Test model query validation."""
        # Create test data
        goals = [
            Goal(title="High Priority", description="High priority goal", severity="high"),
            Goal(title="Medium Priority", description="Medium priority goal", severity="medium"),
            Goal(title="Low Priority", description="Low priority goal", severity="low"),
        ]

        for goal in goals:
            temp_session.add(goal)
        temp_session.commit()

        # Test query validation - should return expected results
        high_priority_goals = temp_session.query(Goal).filter(Goal.severity == "high").all()
        assert len(high_priority_goals) == 1
        assert high_priority_goals[0].title == "High Priority"

        # Test ordering
        ordered_goals = temp_session.query(Goal).order_by(Goal.title).all()
        titles = [g.title for g in ordered_goals]
        assert titles == ["High Priority", "Low Priority", "Medium Priority"]

    def test_model_error_handling_validation(self, temp_session):
        """Test model error handling validation."""
        # Test constraint violation (unique constraint on Label.name)
        label1 = Label(name="unique-label")
        temp_session.add(label1)
        temp_session.commit()

        # Try to create duplicate label
        label2 = Label(name="unique-label")
        temp_session.add(label2)

        # Should raise an exception due to unique constraint
        with pytest.raises(Exception):  # Could be IntegrityError or similar
            temp_session.commit()

        temp_session.rollback()
