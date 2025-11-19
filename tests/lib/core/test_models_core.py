"""Models Core Tests

Tests for the unified ToDoWrite Models architecture.
Tests functionality only - no fakes, no mocks, no stubs.
"""

from __future__ import annotations

import tempfile

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from todowrite.core.models import (
    Base,
    Command,
    Goal,
    Label,
    Phase,
    Step,
    SubTask,
    Task,
)


class TestModelsCore:
    """Test the unified ToDoWrite Models architecture."""

    @pytest.fixture
    def temp_db_path(self):
        """Create a temporary database path."""
        with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as temp_file:
            yield temp_file.name

    @pytest.fixture
    def models_session(self, temp_db_path):
        """Create Models session with temporary database."""
        engine = create_engine(f"sqlite:///{temp_db_path}")
        Base.metadata.create_all(engine)
        Session = sessionmaker(bind=engine)
        session = Session()
        yield session
        session.close()

    def test_create_goal_with_direct_instantiation(self, models_session):
        """Test goal creation using direct model instantiation."""
        # Create goal using direct instantiation
        goal = Goal(
            title="Test Goal",
            owner="test-user",
            severity="high",
            description="A test goal created via direct instantiation",
        )

        models_session.add(goal)
        models_session.commit()
        models_session.refresh(goal)

        # Verify goal was created
        assert goal.id is not None
        assert goal.title == "Test Goal"
        assert goal.owner == "test-user"
        assert goal.severity == "high"
        assert goal.description == "A test goal created via direct instantiation"
        assert goal.status == "planned"  # default value

    def test_create_task_with_goal_relationship(self, models_session):
        """Test task creation with goal relationship."""
        # Create a goal first
        goal = Goal(
            title="Parent Goal", owner="test-user", description="Parent goal for task testing"
        )
        models_session.add(goal)
        models_session.commit()
        models_session.refresh(goal)

        # Create task
        task = Task(
            title="Test Task", owner="test-user", description="A test task", status="in_progress"
        )
        models_session.add(task)
        models_session.commit()
        models_session.refresh(task)

        # Establish relationship
        goal.tasks.append(task)
        models_session.commit()

        # Verify relationship
        assert task.id is not None
        assert goal.id is not None
        assert task in goal.tasks

    def test_create_full_hierarchy(self, models_session):
        """Test creating a complete hierarchy from Goal to Command."""
        # Create Goal
        goal = Goal(
            title="Launch Product",
            owner="product-team",
            severity="high",
            description="Successfully launch the new product",
        )
        models_session.add(goal)
        models_session.commit()

        # Create Phase
        phase = Phase(
            title="Development Phase", owner="dev-team", description="Development and testing phase"
        )
        models_session.add(phase)
        models_session.commit()

        # Create Step
        step = Step(
            title="Implement Core Features",
            owner="dev-team",
            description="Implement the main product features",
        )
        models_session.add(step)
        models_session.commit()

        # Create Task
        task = Task(
            title="Build User Authentication",
            owner="backend-team",
            description="Implement user login and registration",
            status="in_progress",
            progress=60,
        )
        models_session.add(task)
        models_session.commit()

        # Create SubTask
        subtask = SubTask(
            title="Set up Database Schema",
            owner="backend-team",
            description="Create user tables and relationships",
            status="completed",
        )
        models_session.add(subtask)
        models_session.commit()

        # Create Command
        command = Command(
            title="Run Database Migration",
            owner="backend-team",
            description="Execute database migration script",
            cmd="alembic upgrade head",
            status="completed",
        )
        models_session.add(command)
        models_session.commit()

        # Establish relationships
        goal.phases.append(phase)
        phase.steps.append(step)
        step.tasks.append(task)
        task.sub_tasks.append(subtask)
        subtask.commands.append(command)
        models_session.commit()

        # Verify the hierarchy
        assert command.id is not None
        assert subtask in command.sub_tasks
        assert command in subtask.commands
        assert subtask in task.sub_tasks
        assert task in step.tasks
        assert step in phase.steps
        assert phase in goal.phases

    def test_query_models_by_type(self, models_session):
        """Test querying models by their type."""
        # Create various model instances
        goal1 = Goal(title="Goal 1", owner="user1")
        goal2 = Goal(title="Goal 2", owner="user2")
        task1 = Task(title="Task 1", owner="user1")
        task2 = Task(title="Task 2", owner="user1")

        models_session.add_all([goal1, goal2, task1, task2])
        models_session.commit()

        # Query goals
        goals = models_session.query(Goal).all()
        assert len(goals) == 2
        assert all(isinstance(g, Goal) for g in goals)

        # Query tasks
        tasks = models_session.query(Task).all()
        assert len(tasks) == 2
        assert all(isinstance(t, Task) for t in tasks)

        # Query by owner
        user1_tasks = models_session.query(Task).filter(Task.owner == "user1").all()
        assert len(user1_tasks) == 2

    def test_label_relationships(self, models_session):
        """Test many-to-many relationships with labels."""
        # Create labels
        urgent_label = Label(name="urgent")
        backend_label = Label(name="backend")

        # Create goal and task
        goal = Goal(title="Critical Backend Fix", owner="dev-team", severity="high")
        task = Task(title="Fix Database Connection", owner="backend-team", status="in_progress")

        models_session.add_all([urgent_label, backend_label, goal, task])
        models_session.commit()

        # Establish label relationships
        goal.labels.append(urgent_label)
        goal.labels.append(backend_label)
        task.labels.append(urgent_label)
        models_session.commit()

        # Verify label relationships
        assert len(goal.labels) == 2
        assert urgent_label in goal.labels
        assert backend_label in goal.labels
        assert len(task.labels) == 1
        assert urgent_label in task.labels
        assert len(urgent_label.goals) == 1
        assert len(urgent_label.tasks) == 1

    def test_model_validation(self, models_session):
        """Test model validation and constraints."""
        # Test required fields
        with pytest.raises(Exception):  # Should raise some kind of database error
            goal = Goal()  # Missing required title
            models_session.add(goal)
            models_session.commit()

        models_session.rollback()

        # Test valid creation
        goal = Goal(title="Valid Goal")
        models_session.add(goal)
        models_session.commit()

        assert goal.id is not None
        assert goal.title == "Valid Goal"
