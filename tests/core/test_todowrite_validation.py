import sys
import unittest
from pathlib import Path

from afs_fastapi.core.todos_manager import (
    BaseItem,
    GoalItem,
    PhaseItem,
    StepItem,
    SubTaskItem,
    TaskItem,
    validate_dependencies,
    validate_granularity,
    validate_hierarchy_order,
    validate_single_concern,
    validate_status_rules,
    validate_subtask_atomicity,
)


class TestTodoWriteValidation(unittest.TestCase):
    """Test the validation pipeline for the TodoWrite.md schema."""

    def setUp(self) -> None:
        """Set up test environment."""
        project_root = Path(__file__).resolve().parent.parent.parent
        sys.path.insert(0, str(project_root))

    def test_validate_hierarchy_order_goal_with_parent(self) -> None:
        """Test that a Goal with a parent_id is flagged as a hierarchy violation."""
        goal: GoalItem = {
            "id": "goal-1",
            "parent_id": "some-parent",  # This should be an error
            "level": "Goal",
            "title": "Test Goal",
            "description": "...",
            "single_concern": True,
            "dependencies": [],
            "status": "planned",
            "validation_log": [],
            "phases": [],
            "category": "test",
            "priority": "high",
        }
        errors = validate_hierarchy_order(goal, "Goal")
        self.assertEqual(len(errors), 1)
        self.assertIn("Goal must have parent_id=null", errors[0])

    def test_validate_hierarchy_order_child_without_parent(self) -> None:
        """Test that a Phase without a parent_id is flagged as a hierarchy violation."""
        phase: PhaseItem = {
            "id": "phase-1",
            "parent_id": None,  # This should be an error
            "level": "Phase",
            "title": "Test Phase",
            "description": "...",
            "single_concern": True,
            "dependencies": [],
            "status": "planned",
            "validation_log": [],
            "steps": [],
        }
        errors = validate_hierarchy_order(phase, "Phase")
        self.assertEqual(len(errors), 1)
        self.assertIn("Phase must have a parent_id", errors[0])

    def test_validate_hierarchy_order_incorrect_level(self) -> None:
        """Test that an item with an incorrect level is flagged as a hierarchy violation."""
        phase_with_wrong_level: PhaseItem = {
            "id": "phase-1",
            "parent_id": "goal-1",
            "level": "Goal",  # Incorrect level
            "title": "Test Phase",
            "description": "...",
            "single_concern": True,
            "dependencies": [],
            "status": "planned",
            "validation_log": [],
            "steps": [],
        }
        errors = validate_hierarchy_order(phase_with_wrong_level, "Phase")  # Expecting a Phase
        self.assertEqual(len(errors), 1)
        self.assertIn("Hierarchy violation: Expected Phase, got Goal", errors[0])

    def test_validate_single_concern_multiple_verbs(self) -> None:
        """Test that a title with multiple action verbs fails single concern validation."""
        item: BaseItem = {
            "id": "item-1",
            "parent_id": None,
            "level": "Task",
            "title": "Implement and test the new feature",
            "description": "...",
            "single_concern": True,
            "dependencies": [],
            "status": "planned",
            "validation_log": [],
        }
        errors = validate_single_concern(item)
        self.assertEqual(len(errors), 2)  # Two verbs and a conjunction
        self.assertIn("Multiple concerns in title", errors[0])

    def test_validate_single_concern_conjunction(self) -> None:
        """Test that a title with a conjunction fails single concern validation."""
        item: BaseItem = {
            "id": "item-1",
            "parent_id": None,
            "level": "Task",
            "title": "Design and analyze the database schema",
            "description": "...",
            "single_concern": True,
            "dependencies": [],
            "status": "planned",
            "validation_log": [],
        }
        errors = validate_single_concern(item)
        self.assertEqual(len(errors), 2)
        self.assertIn("Multiple concerns in title", errors[0])

    def test_validate_granularity(self) -> None:
        """Test that a child item that does not serve the parent's concern fails granularity validation."""
        step: StepItem = {
            "id": "step-1",
            "parent_id": "phase-1",
            "level": "Step",
            "title": "Implement User Authentication",
            "description": "...",
            "single_concern": True,
            "dependencies": [],
            "status": "planned",
            "validation_log": [],
            "tasks": [],
        }
        task: TaskItem = {
            "id": "task-1",
            "parent_id": "step-1",
            "level": "Task",
            "title": "Design the Database Schema",  # Unrelated to authentication
            "description": "...",
            "single_concern": True,
            "dependencies": [],
            "status": "planned",
            "validation_log": [],
            "subtasks": [],
        }
        all_items = {"step-1": step, "task-1": task}
        errors = validate_granularity(step, all_items)
        self.assertEqual(len(errors), 1)
        self.assertIn("Child task-1 may not serve parent concern step-1", errors[0])

    def test_validate_dependencies_non_existent(self) -> None:
        """Test that a non-existent dependency is flagged as a validation error."""
        item: BaseItem = {
            "id": "item-1",
            "parent_id": None,
            "level": "Task",
            "title": "Test Task",
            "description": "...",
            "single_concern": True,
            "dependencies": ["item-2"],  # item-2 does not exist
            "status": "planned",
            "validation_log": [],
        }
        all_items = {"item-1": item}
        errors = validate_dependencies(item, all_items)
        self.assertEqual(len(errors), 1)
        self.assertIn("Dependency item-2 does not exist", errors[0])

    def test_validate_dependencies_circular(self) -> None:
        """Test that a circular dependency is flagged as a validation error."""
        item1: BaseItem = {
            "id": "item-1",
            "parent_id": None,
            "level": "Task",
            "title": "Test Task 1",
            "description": "...",
            "single_concern": True,
            "dependencies": ["item-2"],
            "status": "planned",
            "validation_log": [],
        }
        item2: BaseItem = {
            "id": "item-2",
            "parent_id": None,
            "level": "Task",
            "title": "Test Task 2",
            "description": "...",
            "single_concern": True,
            "dependencies": ["item-1"],  # Circular dependency
            "status": "planned",
            "validation_log": [],
        }
        all_items = {"item-1": item1, "item-2": item2}
        errors = validate_dependencies(item1, all_items)
        self.assertEqual(len(errors), 1)
        self.assertIn("Circular dependency detected for item-1", errors[0])

    def test_validate_subtask_atomicity_multiple_commands(self) -> None:
        """Test that a subtask with multiple commands fails atomicity validation."""
        subtask: SubTaskItem = {
            "id": "subtask-1",
            "parent_id": "task-1",
            "level": "SubTask",
            "title": "Test SubTask",
            "description": "...",
            "single_concern": True,
            "dependencies": [],
            "status": "planned",
            "validation_log": [],
            "command": "echo 'hello' && echo 'world'",
            "command_type": "bash",
            "execution_log": [],
        }
        errors = validate_subtask_atomicity(subtask)
        self.assertEqual(len(errors), 1)
        self.assertIn("SubTask contains multiple commands", errors[0])

    def test_validate_subtask_atomicity_empty_command(self) -> None:
        """Test that a subtask with an empty command fails atomicity validation."""
        subtask: SubTaskItem = {
            "id": "subtask-1",
            "parent_id": "task-1",
            "level": "SubTask",
            "title": "Test SubTask",
            "description": "...",
            "single_concern": True,
            "dependencies": [],
            "status": "planned",
            "validation_log": [],
            "command": "",
            "command_type": "bash",
            "execution_log": [],
        }
        errors = validate_subtask_atomicity(subtask)
        self.assertEqual(len(errors), 1)
        self.assertIn("SubTask must have a non-empty command", errors[0])

    def test_validate_status_rules_parent_done_with_incomplete_child(self) -> None:
        """Test that a parent marked as done with an incomplete child fails validation."""
        parent: BaseItem = {
            "id": "parent-1",
            "parent_id": None,
            "level": "Task",
            "title": "Test Task",
            "description": "...",
            "single_concern": True,
            "dependencies": [],
            "status": "done",  # This should be an error
            "validation_log": [],
        }
        child: BaseItem = {
            "id": "child-1",
            "parent_id": "parent-1",
            "level": "SubTask",
            "title": "Test SubTask",
            "description": "...",
            "single_concern": True,
            "dependencies": [],
            "status": "planned",
            "validation_log": [],
        }
        all_items = {"parent-1": parent, "child-1": child}
        errors = validate_status_rules(parent, all_items)
        self.assertEqual(len(errors), 1)
        self.assertIn(
            "Parent parent-1 cannot be done while children ['child-1'] are incomplete", errors[0]
        )

    def test_validate_status_rules_blocked_child(self) -> None:
        """Test that a parent with a blocked child is flagged if not also blocked."""
        parent: BaseItem = {
            "id": "parent-1",
            "parent_id": None,
            "level": "Task",
            "title": "Test Task",
            "description": "...",
            "single_concern": True,
            "dependencies": [],
            "status": "in_progress",  # This should be an error
            "validation_log": [],
        }
        child: BaseItem = {
            "id": "child-1",
            "parent_id": "parent-1",
            "level": "SubTask",
            "title": "Test SubTask",
            "description": "...",
            "single_concern": True,
            "dependencies": [],
            "status": "blocked",
            "validation_log": [],
        }
        all_items = {"parent-1": parent, "child-1": child}
        errors = validate_status_rules(parent, all_items)
        self.assertEqual(len(errors), 1)
        self.assertIn("Parent parent-1 should be blocked due to blocked children", errors[0])


if __name__ == "__main__":
    unittest.main()
