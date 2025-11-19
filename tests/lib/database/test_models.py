"""
Database Models Tests

Tests for database models, relationships, and operations.
"""

import json
import tempfile
import unittest
from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from todowrite.core.models import (
    Base,
    Command,
    Goal,
    Label,
    Phase,
    Step,
    Task,
)


class TestDatabaseModels(unittest.TestCase):
    """Test database models and operations."""

    def setUp(self) -> None:
        """Set up test database."""
        self.temp_db = tempfile.NamedTemporaryFile(suffix=".db", delete=False)
        self.temp_db.close()
        self.engine = create_engine(f"sqlite:///{self.temp_db.name}")
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)
        self.session = self.Session()

    def tearDown(self) -> None:
        """Clean up test database."""
        self.session.close()
        Path(self.temp_db.name).unlink(missing_ok=True)

    def test_create_goal(self) -> None:
        """Test creating a goal."""
        goal = Goal(
            title="Test Goal", description="A test goal", owner="test-user", severity="medium"
        )
        self.session.add(goal)
        self.session.commit()

        retrieved_goal = self.session.query(Goal).filter(Goal.title == "Test Goal").first()
        self.assertIsNotNone(retrieved_goal)
        self.assertEqual(retrieved_goal.title, "Test Goal")
        self.assertEqual(retrieved_goal.description, "A test goal")
        self.assertEqual(retrieved_goal.owner, "test-user")
        self.assertEqual(retrieved_goal.severity, "medium")

    def test_create_task(self) -> None:
        """Test creating a task."""
        task = Task(
            title="Test Task",
            description="A test task",
            owner="test-user",
            severity="high",
            work_type="feature",
            assignee="developer",
        )
        self.session.add(task)
        self.session.commit()

        retrieved_task = self.session.query(Task).filter(Task.title == "Test Task").first()
        self.assertIsNotNone(retrieved_task)
        self.assertEqual(retrieved_task.title, "Test Task")
        self.assertEqual(retrieved_task.description, "A test task")
        self.assertEqual(retrieved_task.severity, "high")
        self.assertEqual(retrieved_task.work_type, "feature")
        self.assertEqual(retrieved_task.assignee, "developer")

    def test_create_phase(self) -> None:
        """Test creating a phase."""
        phase = Phase(
            title="Development Phase",
            description="Development work phase",
            owner="team-lead",
            severity="medium",
        )
        self.session.add(phase)
        self.session.commit()

        retrieved_phase = (
            self.session.query(Phase).filter(Phase.title == "Development Phase").first()
        )
        self.assertIsNotNone(retrieved_phase)
        self.assertEqual(retrieved_phase.title, "Development Phase")
        self.assertEqual(retrieved_phase.description, "Development work phase")
        self.assertEqual(retrieved_phase.owner, "team-lead")

    def test_create_step(self) -> None:
        """Test creating a step."""
        step = Step(
            title="API Development",
            description="Develop REST API",
            owner="backend-dev",
            severity="high",
        )
        self.session.add(step)
        self.session.commit()

        retrieved_step = self.session.query(Step).filter(Step.title == "API Development").first()
        self.assertIsNotNone(retrieved_step)
        self.assertEqual(retrieved_step.title, "API Development")
        self.assertEqual(retrieved_step.description, "Develop REST API")
        self.assertEqual(retrieved_step.owner, "backend-dev")

    def test_create_label(self) -> None:
        """Test creating a label."""
        label = Label(name="urgent")
        self.session.add(label)
        self.session.commit()

        retrieved_label = self.session.query(Label).filter(Label.name == "urgent").first()
        self.assertIsNotNone(retrieved_label)
        self.assertEqual(retrieved_label.name, "urgent")

    def test_create_command(self) -> None:
        """Test creating a command."""
        command = Command(
            title="Test Command",
            description="A test command",
            cmd="echo 'Hello, World!'",
            cmd_params="--verbose",
            owner="test-user",
        )
        self.session.add(command)
        self.session.commit()

        retrieved_command = (
            self.session.query(Command).filter(Command.title == "Test Command").first()
        )
        self.assertIsNotNone(retrieved_command)
        self.assertEqual(retrieved_command.title, "Test Command")
        self.assertEqual(retrieved_command.cmd, "echo 'Hello, World!'")
        self.assertEqual(retrieved_command.cmd_params, "--verbose")

    def test_label_uniqueness(self) -> None:
        """Test label name uniqueness constraint."""
        label1 = Label(name="urgent")
        self.session.add(label1)
        self.session.commit()

        # Try to create duplicate label
        label2 = Label(name="urgent")
        self.session.add(label2)

        # Should raise an exception due to unique constraint
        with self.assertRaises(Exception):
            self.session.commit()

    def test_model_extra_data(self) -> None:
        """Test extra_data JSON field."""
        extra_data = {"priority": 1, "estimated_hours": 40, "tags": ["backend", "api"]}
        goal = Goal(
            title="Goal with Extra Data",
            description="Testing extra data field",
            extra_data=json.dumps(extra_data),
        )
        self.session.add(goal)
        self.session.commit()

        retrieved_goal = (
            self.session.query(Goal).filter(Goal.title == "Goal with Extra Data").first()
        )
        self.assertIsNotNone(retrieved_goal)

        # Parse and verify extra data
        parsed_extra_data = json.loads(retrieved_goal.extra_data)
        self.assertEqual(parsed_extra_data["priority"], 1)
        self.assertEqual(parsed_extra_data["estimated_hours"], 40)
        self.assertEqual(parsed_extra_data["tags"], ["backend", "api"])

    def test_model_timestamps(self) -> None:
        """Test automatic timestamp fields."""
        goal = Goal(title="Timestamp Test", description="Testing timestamps")
        self.session.add(goal)
        self.session.commit()

        # Verify timestamps are set
        self.assertIsNotNone(goal.created_at)
        self.assertIsNotNone(goal.updated_at)

    def test_query_by_fields(self) -> None:
        """Test querying models by various fields."""
        # Create test data
        goals = [
            Goal(title="High Priority Goal", description="Test", severity="high", owner="alice"),
            Goal(title="Medium Priority Goal", description="Test", severity="medium", owner="bob"),
            Goal(title="Low Priority Goal", description="Test", severity="low", owner="alice"),
        ]

        for goal in goals:
            self.session.add(goal)
        self.session.commit()

        # Query by severity
        high_priority_goals = self.session.query(Goal).filter(Goal.severity == "high").all()
        self.assertEqual(len(high_priority_goals), 1)
        self.assertEqual(high_priority_goals[0].title, "High Priority Goal")

        # Query by owner
        alice_goals = self.session.query(Goal).filter(Goal.owner == "alice").all()
        self.assertEqual(len(alice_goals), 2)

        # Query by multiple fields
        alice_high_priority = (
            self.session.query(Goal).filter(Goal.owner == "alice", Goal.severity == "high").all()
        )
        self.assertEqual(len(alice_high_priority), 1)

    def test_order_and_limit_queries(self) -> None:
        """Test ordered and limited queries."""
        # Create test data
        titles = ["C Goal", "A Goal", "B Goal", "D Goal"]
        for title in titles:
            goal = Goal(title=title, description="Test")
            self.session.add(goal)
        self.session.commit()

        # Test ordering
        ordered_goals = self.session.query(Goal).order_by(Goal.title).all()
        ordered_titles = [g.title for g in ordered_goals]
        self.assertEqual(ordered_titles, ["A Goal", "B Goal", "C Goal", "D Goal"])

        # Test limit
        limited_goals = self.session.query(Goal).order_by(Goal.title).limit(2).all()
        self.assertEqual(len(limited_goals), 2)
        self.assertEqual([g.title for g in limited_goals], ["A Goal", "B Goal"])

    def test_update_operations(self) -> None:
        """Test updating model instances."""
        goal = Goal(
            title="Original Title", description="Original description", owner="original-owner"
        )
        self.session.add(goal)
        self.session.commit()

        # Update goal
        goal.title = "Updated Title"
        goal.description = "Updated description"
        goal.owner = "updated-owner"
        self.session.commit()

        # Verify updates
        retrieved_goal = self.session.query(Goal).filter(Goal.id == goal.id).first()
        self.assertIsNotNone(retrieved_goal)
        self.assertEqual(retrieved_goal.title, "Updated Title")
        self.assertEqual(retrieved_goal.description, "Updated description")
        self.assertEqual(retrieved_goal.owner, "updated-owner")

    def test_delete_operations(self) -> None:
        """Test deleting model instances."""
        goal = Goal(title="To Be Deleted", description="Will be deleted")
        self.session.add(goal)
        self.session.commit()

        goal_id = goal.id

        # Delete goal
        self.session.delete(goal)
        self.session.commit()

        # Verify deletion
        deleted_goal = self.session.query(Goal).filter(Goal.id == goal_id).first()
        self.assertIsNone(deleted_goal)


if __name__ == "__main__":
    unittest.main()
