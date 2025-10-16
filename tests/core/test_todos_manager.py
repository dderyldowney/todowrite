import sys
from pathlib import Path

project_root = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(project_root))

import json
import unittest
from unittest.mock import mock_open, patch

from afs_fastapi.core.todos_manager import (  # noqa: E402
    add_goal,
    add_phase,
    add_step,
    add_subtask,
    add_task,
    execute_subtask,
    get_active_items,
    get_execution_ready_subtasks,
    get_goals,
    load_todos,
    save_todos,
    validate_all_items,
    validate_dependencies,
    validate_granularity,
    validate_hierarchy_order,
    validate_single_concern,
    validate_status_rules,
    validate_subtask_atomicity,
)


class TestTodosManager(unittest.TestCase):

    @patch("builtins.open", new_callable=mock_open, read_data='{"goals": []}')
    def test_load_todos_file_found(self, mock_file):
        """Test that load_todos loads the file correctly with the new schema."""
        todos = load_todos()
        self.assertEqual(todos, {"goals": []})
        mock_file.assert_called_with(".claude/todos.json")

    @patch("builtins.open", side_effect=FileNotFoundError)
    def test_load_todos_file_not_found(self, mock_file):
        """Test that load_todos returns an empty structure when the file is not found."""
        todos = load_todos()
        self.assertEqual(todos, {"goals": []})

    @patch("builtins.open", new_callable=mock_open)
    def test_save_todos(self, mock_file):
        """Test that save_todos writes the todos to the file with the new schema."""
        todos = {
            "goals": [
                {
                    "id": "goal-1",
                    "parent_id": None,
                    "level": "Goal",
                    "title": "Test Goal",
                    "description": "Test Description",
                    "single_concern": True,
                    "dependencies": [],
                    "status": "planned",
                    "validation_log": [],
                    "phases": [],
                    "category": "general",
                    "priority": "medium",
                }
            ]
        }
        save_todos(todos)
        mock_file.assert_called_with(".claude/todos.json", "w")

        written_content = "".join(call.args[0] for call in mock_file().write.call_args_list)

        self.assertEqual(json.loads(written_content), todos)

    @patch("afs_fastapi.core.todos_manager.load_todos")
    def test_get_goals(self, mock_load_todos):
        """Test that get_goals returns all goals."""
        mock_load_todos.return_value = {"goals": [{"id": "goal-1"}]}
        goals = get_goals()
        self.assertEqual(goals, [{"id": "goal-1"}])

    @patch("afs_fastapi.core.todos_manager.load_todos")
    @patch("afs_fastapi.core.todos_manager.save_todos")
    @patch("afs_fastapi.core.todos_manager.run_validation_pipeline", return_value=[])
    @patch("afs_fastapi.core.todos_manager.create_flat_item_dict", return_value={})
    def test_add_goal(
        self,
        mock_create_flat_item_dict,
        mock_run_validation_pipeline,
        mock_save_todos,
        mock_load_todos,
    ):
        """Test that add_goal adds a new goal."""
        mock_load_todos.return_value = {"goals": []}
        new_goal = add_goal("Test Goal", "Test Description", "test-category", "high")
        self.assertTrue(mock_save_todos.called)
        self.assertEqual(new_goal["title"], "Test Goal")
        self.assertEqual(new_goal["description"], "Test Description")
        self.assertEqual(new_goal["category"], "test-category")
        self.assertEqual(new_goal["priority"], "high")
        self.assertEqual(new_goal["status"], "planned")
        self.assertEqual(new_goal["level"], "Goal")

    @patch("afs_fastapi.core.todos_manager.load_todos")
    @patch("afs_fastapi.core.todos_manager.save_todos")
    @patch("afs_fastapi.core.todos_manager.run_validation_pipeline", return_value=[])
    @patch("afs_fastapi.core.todos_manager.create_flat_item_dict", return_value={})
    def test_add_phase(
        self,
        mock_create_flat_item_dict,
        mock_run_validation_pipeline,
        mock_save_todos,
        mock_load_todos,
    ):
        """Test that add_phase adds a new phase to a goal."""
        mock_load_todos.return_value = {"goals": [{"id": "goal-1", "phases": []}]}
        new_phase, error = add_phase("goal-1", "Test Phase", "Test Description")
        self.assertIsNone(error)
        self.assertTrue(mock_save_todos.called)
        self.assertEqual(new_phase["title"], "Test Phase")
        self.assertEqual(new_phase["parent_id"], "goal-1")
        self.assertEqual(new_phase["level"], "Phase")

    @patch("afs_fastapi.core.todos_manager.load_todos")
    @patch("afs_fastapi.core.todos_manager.save_todos")
    @patch("afs_fastapi.core.todos_manager.run_validation_pipeline", return_value=[])
    @patch("afs_fastapi.core.todos_manager.create_flat_item_dict", return_value={})
    def test_add_step(
        self,
        mock_create_flat_item_dict,
        mock_run_validation_pipeline,
        mock_save_todos,
        mock_load_todos,
    ):
        """Test that add_step adds a new step to a phase."""
        mock_load_todos.return_value = {
            "goals": [{"id": "goal-1", "phases": [{"id": "phase-1", "steps": []}]}]
        }
        new_step, error = add_step("phase-1", "Test Step", "Test Description")
        self.assertIsNone(error)
        self.assertTrue(mock_save_todos.called)
        self.assertEqual(new_step["title"], "Test Step")
        self.assertEqual(new_step["parent_id"], "phase-1")
        self.assertEqual(new_step["level"], "Step")

    @patch("afs_fastapi.core.todos_manager.load_todos")
    @patch("afs_fastapi.core.todos_manager.save_todos")
    @patch("afs_fastapi.core.todos_manager.run_validation_pipeline", return_value=[])
    @patch("afs_fastapi.core.todos_manager.create_flat_item_dict", return_value={})
    def test_add_task(
        self,
        mock_create_flat_item_dict,
        mock_run_validation_pipeline,
        mock_save_todos,
        mock_load_todos,
    ):
        """Test that add_task adds a new task to a step."""
        mock_load_todos.return_value = {
            "goals": [
                {
                    "id": "goal-1",
                    "phases": [{"id": "phase-1", "steps": [{"id": "step-1", "tasks": []}]}],
                }
            ]
        }
        new_task, error = add_task("step-1", "Test Task", "Test Description")
        self.assertIsNone(error)
        self.assertTrue(mock_save_todos.called)
        self.assertEqual(new_task["title"], "Test Task")
        self.assertEqual(new_task["parent_id"], "step-1")
        self.assertEqual(new_task["level"], "Task")

    @patch("afs_fastapi.core.todos_manager.load_todos")
    @patch("afs_fastapi.core.todos_manager.save_todos")
    @patch("afs_fastapi.core.todos_manager.run_validation_pipeline", return_value=[])
    @patch("afs_fastapi.core.todos_manager.create_flat_item_dict", return_value={})
    def test_add_subtask(
        self,
        mock_create_flat_item_dict,
        mock_run_validation_pipeline,
        mock_save_todos,
        mock_load_todos,
    ):
        """Test that add_subtask adds a new subtask to a task."""
        mock_load_todos.return_value = {
            "goals": [
                {
                    "id": "goal-1",
                    "phases": [
                        {
                            "id": "phase-1",
                            "steps": [
                                {"id": "step-1", "tasks": [{"id": "task-1", "subtasks": []}]}
                            ],
                        }
                    ],
                }
            ]
        }
        new_subtask, error = add_subtask(
            "task-1", "Test SubTask", "Test Description", "echo 'hello'"
        )
        self.assertIsNone(error)
        self.assertTrue(mock_save_todos.called)
        self.assertEqual(new_subtask["title"], "Test SubTask")
        self.assertEqual(new_subtask["parent_id"], "task-1")
        self.assertEqual(new_subtask["level"], "SubTask")
        self.assertEqual(new_subtask["command"], "echo 'hello'")

    @patch("afs_fastapi.core.todos_manager.load_todos")
    @patch("afs_fastapi.core.todos_manager.save_todos")
    def test_execute_subtask(self, mock_save_todos, mock_load_todos):
        """Test that execute_subtask executes a subtask."""
        mock_load_todos.return_value = {
            "goals": [
                {
                    "id": "goal-1",
                    "phases": [
                        {
                            "id": "phase-1",
                            "steps": [
                                {
                                    "id": "step-1",
                                    "tasks": [
                                        {
                                            "id": "task-1",
                                            "subtasks": [
                                                {
                                                    "id": "subtask-1",
                                                    "status": "planned",
                                                    "command": "echo 'test'",
                                                    "command_type": "bash",
                                                    "execution_log": [],
                                                }
                                            ],
                                        }
                                    ],
                                }
                            ],
                        }
                    ],
                }
            ]
        }
        success, message = execute_subtask("subtask-1")
        self.assertTrue(success)
        self.assertTrue(mock_save_todos.called)
        saved_data = mock_save_todos.call_args[0][0]
        self.assertEqual(
            saved_data["goals"][0]["phases"][0]["steps"][0]["tasks"][0]["subtasks"][0]["status"],
            "done",
        )

    @patch("afs_fastapi.core.todos_manager.load_todos")
    def test_get_active_items(self, mock_load_todos):
        """Test that get_active_items returns currently active items."""
        mock_load_todos.return_value = {
            "goals": [
                {
                    "id": "goal-1",
                    "status": "in_progress",
                    "phases": [
                        {
                            "id": "phase-1",
                            "status": "in_progress",
                            "steps": [
                                {
                                    "id": "step-1",
                                    "status": "in_progress",
                                    "tasks": [
                                        {
                                            "id": "task-1",
                                            "status": "in_progress",
                                            "subtasks": [
                                                {"id": "subtask-1", "status": "in_progress"}
                                            ],
                                        }
                                    ],
                                }
                            ],
                        }
                    ],
                }
            ]
        }
        active_items = get_active_items()
        self.assertIsNotNone(active_items["goal"])
        self.assertIsNotNone(active_items["phase"])
        self.assertIsNotNone(active_items["step"])
        self.assertIsNotNone(active_items["task"])
        self.assertIsNotNone(active_items["subtask"])

    @patch("afs_fastapi.core.todos_manager.load_todos")
    @patch("afs_fastapi.core.todos_manager.create_flat_item_dict")
    @patch("afs_fastapi.core.todos_manager.run_validation_pipeline", return_value=["error"])
    def test_validate_all_items(
        self, mock_run_validation_pipeline, mock_create_flat_item_dict, mock_load_todos
    ):
        """Test that validate_all_items runs validation on all items."""
        mock_load_todos.return_value = {"goals": [{"id": "goal-1"}]}
        mock_create_flat_item_dict.return_value = {"goal-1": {"id": "goal-1"}}
        validation_results = validate_all_items()
        self.assertEqual(validation_results, {"goal-1": ["error"]})

    @patch("afs_fastapi.core.todos_manager.load_todos")
    def test_get_execution_ready_subtasks(self, mock_load_todos):
        """Test that get_execution_ready_subtasks returns subtasks ready for execution."""
        mock_load_todos.return_value = {
            "goals": [
                {
                    "id": "goal-1",
                    "phases": [
                        {
                            "id": "phase-1",
                            "steps": [
                                {
                                    "id": "step-1",
                                    "tasks": [
                                        {
                                            "id": "task-1",
                                            "subtasks": [
                                                {
                                                    "id": "subtask-1",
                                                    "status": "planned",
                                                    "command_type": "bash",
                                                },
                                                {
                                                    "id": "subtask-2",
                                                    "status": "done",
                                                    "command_type": "bash",
                                                },
                                                {
                                                    "id": "subtask-3",
                                                    "status": "planned",
                                                    "command_type": "todo",
                                                },
                                            ],
                                        }
                                    ],
                                }
                            ],
                        }
                    ],
                }
            ]
        }
        ready_subtasks = get_execution_ready_subtasks()
        self.assertEqual(len(ready_subtasks), 1)
        self.assertEqual(ready_subtasks[0]["id"], "subtask-1")

    def test_validate_hierarchy_order(self):
        """Test V1: Hierarchy order validation."""
        # Valid Goal
        goal = {
            "id": "g1",
            "parent_id": None,
            "level": "Goal",
            "title": "T",
            "description": "D",
            "single_concern": True,
            "dependencies": [],
            "status": "planned",
            "validation_log": [],
        }
        self.assertEqual(validate_hierarchy_order(goal, "Goal"), [])

        # Invalid Goal (has parent_id)
        invalid_goal = {
            "id": "g1",
            "parent_id": "p1",
            "level": "Goal",
            "title": "T",
            "description": "D",
            "single_concern": True,
            "dependencies": [],
            "status": "planned",
            "validation_log": [],
        }
        self.assertIn(
            "Goal must have parent_id=null", validate_hierarchy_order(invalid_goal, "Goal")
        )

        # Valid Phase
        phase = {
            "id": "p1",
            "parent_id": "g1",
            "level": "Phase",
            "title": "T",
            "description": "D",
            "single_concern": True,
            "dependencies": [],
            "status": "planned",
            "validation_log": [],
            "steps": [],
        }
        self.assertEqual(validate_hierarchy_order(phase, "Phase"), [])

        # Invalid Phase (no parent_id)
        invalid_phase = {
            "id": "p1",
            "parent_id": None,
            "level": "Phase",
            "title": "T",
            "description": "D",
            "single_concern": True,
            "dependencies": [],
            "status": "planned",
            "validation_log": [],
            "steps": [],
        }
        self.assertIn(
            "Phase must have a parent_id", validate_hierarchy_order(invalid_phase, "Phase")
        )

        # Level mismatch
        self.assertIn(
            "Hierarchy violation: Expected Goal, got Phase", validate_hierarchy_order(phase, "Goal")
        )

    def test_validate_single_concern(self):
        """Test V2: Single concern validation."""
        # Single concern
        item = {
            "id": "t1",
            "level": "Task",
            "title": "Implement feature X",
            "description": "Implement the core logic for feature X.",
            "single_concern": False,
            "dependencies": [],
            "status": "planned",
            "validation_log": [],
        }
        errors = validate_single_concern(item)
        self.assertEqual(errors, [])
        self.assertTrue(item["single_concern"])

        # Multiple verbs in title
        item = {
            "id": "t1",
            "level": "Task",
            "title": "Implement and test feature X",
            "description": "Implement the core logic for feature X.",
            "single_concern": False,
            "dependencies": [],
            "status": "planned",
            "validation_log": [],
        }
        errors = validate_single_concern(item)
        self.assertIn(
            "Multiple concerns in title: contains ['implement', 'test']. Split into separate items.",
            errors,
        )
        self.assertFalse(item["single_concern"])

        # Conjunction in title
        item = {
            "id": "t1",
            "level": "Task",
            "title": "Implement feature X and Y",
            "description": "Implement the core logic for feature X.",
            "single_concern": False,
            "dependencies": [],
            "status": "planned",
            "validation_log": [],
        }
        errors = validate_single_concern(item)
        self.assertIn(
            "Title contains conjunctions suggesting multiple concerns. Split into separate items.",
            errors,
        )
        self.assertFalse(item["single_concern"])

        # Multiple verbs in description
        item = {
            "id": "t1",
            "level": "Task",
            "title": "Implement feature X",
            "description": "Implement the core logic, test the functionality, and validate the solution.",
            "single_concern": False,
            "dependencies": [],
            "status": "planned",
            "validation_log": [],
        }
        errors = validate_single_concern(item)
        self.assertIn(
            "Description may contain multiple concerns: ['implement', 'test', 'validate']", errors
        )
        self.assertFalse(item["single_concern"])

    def test_validate_granularity(self):
        """Test V3: Granularity validation."""
        # Valid granularity
        step = {
            "id": "s1",
            "parent_id": "phase-1",
            "level": "Step",
            "title": "Implement login",
            "description": "Implement user login functionality.",
            "single_concern": True,
            "dependencies": [],
            "status": "planned",
            "validation_log": [],
            "tasks": [],
        }
        task = {
            "id": "t1",
            "parent_id": "s1",
            "level": "Task",
            "title": "Implement login form",
            "description": "Create the login form UI.",
            "single_concern": True,
            "dependencies": [],
            "status": "planned",
            "validation_log": [],
            "subtasks": [],
        }
        all_items = {"s1": step, "t1": task}
        self.assertEqual(validate_granularity(step, all_items), [])

        # Invalid granularity (child does not serve parent concern)
        step = {
            "id": "s1",
            "parent_id": "phase-1",
            "level": "Step",
            "title": "Implement login",
            "description": "Implement user login functionality.",
            "single_concern": True,
            "dependencies": [],
            "status": "planned",
            "validation_log": [],
            "tasks": [],
        }
        task = {
            "id": "t1",
            "parent_id": "s1",
            "level": "Task",
            "title": "Implement payment gateway",
            "description": "Integrate with Stripe.",
            "single_concern": True,
            "dependencies": [],
            "status": "planned",
            "validation_log": [],
            "subtasks": [],
        }
        all_items = {"s1": step, "t1": task}
        errors = validate_granularity(step, all_items)
        self.assertIn("Child t1 may not serve parent concern s1", errors)

    def test_validate_dependencies(self):
        """Test V4: Dependency validation."""
        # Valid dependencies
        item1 = {
            "id": "t1",
            "dependencies": [],
            "level": "Task",
            "title": "T",
            "description": "D",
            "single_concern": True,
            "status": "planned",
            "validation_log": [],
        }
        item2 = {
            "id": "t2",
            "dependencies": ["t1"],
            "level": "Task",
            "title": "T",
            "description": "D",
            "single_concern": True,
            "status": "planned",
            "validation_log": [],
        }
        all_items = {"t1": item1, "t2": item2}
        self.assertEqual(validate_dependencies(item2, all_items), [])

        # Non-existent dependency
        item = {
            "id": "t1",
            "dependencies": ["non-existent"],
            "level": "Task",
            "title": "T",
            "description": "D",
            "single_concern": True,
            "status": "planned",
            "validation_log": [],
        }
        all_items = {"t1": item}
        errors = validate_dependencies(item, all_items)
        self.assertIn("Dependency non-existent does not exist", errors)

        # Circular dependency (simplified check)
        item1 = {
            "id": "t1",
            "dependencies": ["t2"],
            "level": "Task",
            "title": "T",
            "description": "D",
            "single_concern": True,
            "status": "planned",
            "validation_log": [],
        }
        item2 = {
            "id": "t2",
            "dependencies": ["t1"],
            "level": "Task",
            "title": "T",
            "description": "D",
            "single_concern": True,
            "status": "planned",
            "validation_log": [],
        }
        all_items = {"t1": item1, "t2": item2}
        errors = validate_dependencies(item1, all_items)
        self.assertIn("Circular dependency detected for t1", errors)

    def test_validate_subtask_atomicity(self):
        """Test V5: SubTask atomicity validation."""
        # Valid SubTask
        subtask = {
            "id": "st1",
            "level": "SubTask",
            "command": "echo 'hello'",
            "command_type": "bash",
            "title": "T",
            "description": "D",
            "single_concern": True,
            "dependencies": [],
            "status": "planned",
            "validation_log": [],
            "execution_log": [],
        }
        self.assertEqual(validate_subtask_atomicity(subtask), [])

        # Multiple commands
        subtask = {
            "id": "st1",
            "level": "SubTask",
            "command": "echo 'hello' && echo 'world'",
            "command_type": "bash",
            "title": "T",
            "description": "D",
            "single_concern": True,
            "dependencies": [],
            "status": "planned",
            "validation_log": [],
            "execution_log": [],
        }
        errors = validate_subtask_atomicity(subtask)
        self.assertIn("SubTask contains multiple commands. Split into separate SubTasks.", errors)

        # Empty command
        subtask = {
            "id": "st1",
            "level": "SubTask",
            "command": "",
            "command_type": "bash",
            "title": "T",
            "description": "D",
            "single_concern": True,
            "dependencies": [],
            "status": "planned",
            "validation_log": [],
            "execution_log": [],
        }
        errors = validate_subtask_atomicity(subtask)
        self.assertIn("SubTask must have a non-empty command", errors)

    def test_validate_status_rules(self):
        """Test V6: Status rules validation."""
        # Parent done, children incomplete
        goal = {
            "id": "g1",
            "parent_id": None,
            "level": "Goal",
            "status": "done",
            "title": "T",
            "description": "D",
            "single_concern": True,
            "dependencies": [],
            "validation_log": [],
        }
        phase = {
            "id": "p1",
            "parent_id": "g1",
            "level": "Phase",
            "status": "planned",
            "title": "T",
            "description": "D",
            "single_concern": True,
            "dependencies": [],
            "validation_log": [],
            "steps": [],
        }
        all_items = {"g1": goal, "p1": phase}
        errors = validate_status_rules(goal, all_items)
        self.assertIn("Parent g1 cannot be done while children ['p1'] are incomplete", errors)

        # Child blocked, parent not blocked
        goal = {
            "id": "g1",
            "parent_id": None,
            "level": "Goal",
            "status": "planned",
            "title": "T",
            "description": "D",
            "single_concern": True,
            "dependencies": [],
            "validation_log": [],
        }
        phase = {
            "id": "p1",
            "parent_id": "g1",
            "level": "Phase",
            "status": "blocked",
            "title": "T",
            "description": "D",
            "single_concern": True,
            "dependencies": [],
            "validation_log": [],
            "steps": [],
        }
        all_items = {"g1": goal, "p1": phase}
        errors = validate_status_rules(goal, all_items)
        self.assertIn("Parent g1 should be blocked due to blocked children", errors)


if __name__ == "__main__":
    unittest.main()
