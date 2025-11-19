"""
Models Database Tests

Tests for the unified ToDoWrite Models implementation and relationships.
Uses a dedicated testing database with proper setup/teardown.
"""

import tempfile
import unittest
from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from todowrite.core.models import Base, Goal, Task, Concept, Context, Constraints, Requirements, AcceptanceCriteria, InterfaceContract, Phase, Step, SubTask, Command, Label


class TestToDoWriteModels(unittest.TestCase):
    """Test ToDoWrite Models and operations with isolated test database."""

    def setUp(self) -> None:
        """Set up isolated test database for each test."""
        # Create a temporary file for the test database
        with tempfile.NamedTemporaryFile(suffix='.db', delete=False) as tmp:
            self.test_db_path = tmp.name

        # Create engine and session
        self.engine = create_engine(f"sqlite:///{self.test_db_path}", echo=False)
        self.Session = sessionmaker(bind=self.engine)

        # Create all tables
        Base.metadata.create_all(self.engine)

        # Create a session for the test
        self.session = self.Session()

    def tearDown(self) -> None:
        """Clean up test database after each test."""
        # Close the session
        if self.session:
            self.session.close()

        # Drop all tables to ensure clean state
        Base.metadata.drop_all(self.engine)

        # Dispose of the engine
        self.engine.dispose()

        # Remove the temporary database file
        test_db_file = Path(self.test_db_path)
        if test_db_file.exists():
            test_db_file.unlink()

    def test_create_and_retrieve_goal(self) -> None:
        """Test creating and retrieving a goal."""
        # Create a goal
        goal = Goal(
            title="Test Goal",
            description="A test goal for unit testing",
            owner="test-user",
            severity="medium",
            status="planned"
        )

        # Save to database
        self.session.add(goal)
        self.session.commit()
        self.session.refresh(goal)

        # Verify it was saved with an ID
        self.assertIsNotNone(goal.id)
        self.assertEqual(goal.title, "Test Goal")
        self.assertEqual(goal.owner, "test-user")

        # Retrieve from database
        retrieved_goal = self.session.query(Goal).filter(Goal.id == goal.id).first()
        self.assertIsNotNone(retrieved_goal)
        self.assertEqual(retrieved_goal.title, "Test Goal")
        self.assertEqual(retrieved_goal.description, "A test goal for unit testing")

    def test_create_goal_with_task_relationship(self) -> None:
        """Test creating goal and task with proper relationship."""
        # Create goal
        goal = Goal(
            title="Parent Goal",
            owner="test-user",
            description="Goal with associated tasks"
        )
        self.session.add(goal)
        self.session.commit()
        self.session.refresh(goal)

        # Create task
        task = Task(
            title="Child Task",
            owner="test-user",
            description="Task associated with goal",
            status="in_progress",
            progress=30
        )
        self.session.add(task)
        self.session.commit()
        self.session.refresh(task)

        # Establish relationship
        goal.tasks.append(task)
        self.session.commit()

        # Verify relationship from both sides
        self.assertIn(task, goal.tasks)
        self.assertEqual(len(goal.tasks), 1)
        self.assertEqual(task.id, goal.tasks[0].id)

    def test_create_full_hierarchy(self) -> None:
        """Test creating a complete hierarchy from Goal to Command."""
        # Create Goal
        goal = Goal(
            title="Launch Product",
            owner="product-team",
            severity="high",
            description="Successfully launch the new product"
        )
        self.session.add(goal)
        self.session.commit()

        # Create Phase
        phase = Phase(
            title="Development Phase",
            owner="dev-team",
            description="Development and testing phase"
        )
        self.session.add(phase)
        self.session.commit()

        # Create Step
        step = Step(
            title="Implement Core Features",
            owner="dev-team",
            description="Implement the main product features"
        )
        self.session.add(step)
        self.session.commit()

        # Create Task
        task = Task(
            title="Build User Authentication",
            owner="backend-team",
            description="Implement user login and registration",
            status="in_progress",
            progress=60
        )
        self.session.add(task)
        self.session.commit()

        # Create SubTask
        subtask = SubTask(
            title="Set up Database Schema",
            owner="backend-team",
            description="Create user tables and relationships",
            status="completed"
        )
        self.session.add(subtask)
        self.session.commit()

        # Create Command
        command = Command(
            title="Run Database Migration",
            owner="backend-team",
            description="Execute database migration script",
            cmd="alembic upgrade head",
            status="completed"
        )
        self.session.add(command)
        self.session.commit()

        # Establish relationships
        goal.phases.append(phase)
        phase.steps.append(step)
        step.tasks.append(task)
        task.sub_tasks.append(subtask)
        subtask.commands.append(command)
        self.session.commit()

        # Verify the hierarchy exists and is properly connected
        self.assertIsNotNone(goal.id)
        self.assertIsNotNone(phase.id)
        self.assertIsNotNone(step.id)
        self.assertIsNotNone(task.id)
        self.assertIsNotNone(subtask.id)
        self.assertIsNotNone(command.id)

        # Test navigation through hierarchy
        self.assertEqual(len(goal.phases), 1)
        self.assertEqual(len(phase.steps), 1)
        self.assertEqual(len(step.tasks), 1)
        self.assertEqual(len(task.sub_tasks), 1)
        self.assertEqual(len(subtask.commands), 1)

    def test_label_many_to_many_relationships(self) -> None:
        """Test many-to-many relationships between models and labels."""
        # Create labels
        urgent_label = Label(name="urgent")
        backend_label = Label(name="backend")
        feature_label = Label(name="feature")

        self.session.add_all([urgent_label, backend_label, feature_label])
        self.session.commit()

        # Create models
        goal = Goal(
            title="Critical Backend Feature",
            owner="dev-team",
            severity="high"
        )
        task = Task(
            title="Implement API Endpoint",
            owner="backend-team",
            status="in_progress"
        )

        self.session.add_all([goal, task])
        self.session.commit()

        # Establish label relationships
        goal.labels.append(urgent_label)
        goal.labels.append(backend_label)
        goal.labels.append(feature_label)
        task.labels.append(backend_label)
        task.labels.append(urgent_label)
        self.session.commit()

        # Verify relationships
        self.assertEqual(len(goal.labels), 3)
        self.assertEqual(len(task.labels), 2)

        # Verify bidirectional relationships
        self.assertEqual(len(urgent_label.goals), 1)
        self.assertEqual(len(urgent_label.tasks), 1)
        self.assertEqual(len(backend_label.goals), 1)
        self.assertEqual(len(backend_label.tasks), 1)
        self.assertEqual(len(feature_label.goals), 1)
        self.assertEqual(len(feature_label.tasks), 0)

    def test_query_by_different_criteria(self) -> None:
        """Test querying models by various criteria."""
        # Create test data
        goal1 = Goal(title="Goal 1", owner="alice", severity="high", status="planned")
        goal2 = Goal(title="Goal 2", owner="bob", severity="medium", status="in_progress")
        goal3 = Goal(title="Goal 3", owner="alice", severity="low", status="completed")

        task1 = Task(title="Task 1", owner="alice", status="in_progress", progress=50)
        task2 = Task(title="Task 2", owner="charlie", status="planned", progress=0)

        self.session.add_all([goal1, goal2, goal3, task1, task2])
        self.session.commit()

        # Query by owner
        alice_goals = self.session.query(Goal).filter(Goal.owner == "alice").all()
        self.assertEqual(len(alice_goals), 2)

        # Query by status
        planned_goals = self.session.query(Goal).filter(Goal.status == "planned").all()
        self.assertEqual(len(planned_goals), 1)

        # Query by severity
        high_severity_goals = self.session.query(Goal).filter(Goal.severity == "high").all()
        self.assertEqual(len(high_severity_goals), 1)

        # Query tasks by progress range
        in_progress_tasks = self.session.query(Task).filter(Task.progress > 0).all()
        self.assertEqual(len(in_progress_tasks), 1)

    def test_required_field_constraints(self) -> None:
        """Test that required field constraints are enforced."""
        # Test that title is required
        with self.assertRaises(Exception):
            goal = Goal()  # Missing required title
            self.session.add(goal)
            self.session.commit()

        self.session.rollback()  # Clear the failed transaction

        # Test valid creation succeeds
        goal = Goal(title="Valid Goal")
        self.session.add(goal)
        self.session.commit()

        self.assertIsNotNone(goal.id)
        self.assertEqual(goal.title, "Valid Goal")

    def test_database_isolation_between_tests(self) -> None:
        """Test that each test gets a clean database."""
        # This should be a clean database with no existing data
        existing_goals = self.session.query(Goal).all()
        self.assertEqual(len(existing_goals), 0)

        existing_tasks = self.session.query(Task).all()
        self.assertEqual(len(existing_tasks), 0)

        # Create some data
        goal = Goal(title="Isolation Test Goal", owner="test-user")
        self.session.add(goal)
        self.session.commit()

        # Verify it exists in this test
        goals = self.session.query(Goal).all()
        self.assertEqual(len(goals), 1)


if __name__ == '__main__':
    unittest.main()