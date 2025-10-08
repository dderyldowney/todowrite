import sys
from pathlib import Path

project_root = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(project_root))

import json
import unittest
from unittest.mock import mock_open, patch

from afs_fastapi.core.todos_manager import (  # noqa: E402
    add_strategic_goal,
    add_task_to_active_phase,
    complete_strategic_goal,
    complete_task_in_active_phase,
    delete_phase,
    delete_strategic_goal,
    delete_task,
    end_phase,
    get_active_phase,
    get_all_phases,
    get_strategic_goals,
    load_todos,
    pause_active_phase,
    pause_task,
    reorder_phases,
    reorder_strategic_goals,
    reorder_tasks,
    resume_paused_phase,
    resume_task,
    save_todos,
    start_phase,
    update_parent_statuses,
)


class TestTodosManager(unittest.TestCase):

    @patch("builtins.open", new_callable=mock_open, read_data='{"strategic_goals": []}')
    def test_load_todos_file_found(self, mock_file):
        """Test that load_todos loads the file correctly."""
        todos = load_todos()
        self.assertEqual(todos, {"strategic_goals": []})
        mock_file.assert_called_with(".claude/todos.json", "r")

    @patch("builtins.open", side_effect=FileNotFoundError)
    def test_load_todos_file_not_found(self, mock_file):
        """Test that load_todos returns an empty structure when the file is not found."""
        todos = load_todos()
        self.assertEqual(todos, {"strategic_goals": []})

    @patch("builtins.open", new_callable=mock_open)
    def test_save_todos(self, mock_file):
        """Test that save_todos writes the todos to the file."""
        todos = {"strategic_goals": [{"id": "goal-1"}]}
        save_todos(todos)
        mock_file.assert_called_with(".claude/todos.json", "w")

        written_content = "".join(call.args[0] for call in mock_file().write.call_args_list)

        self.assertEqual(written_content, json.dumps(todos, indent=2))

    @patch("afs_fastapi.core.todos_manager.load_todos")
    def test_get_strategic_goals(self, mock_load_todos):
        """Test that get_strategic_goals returns the strategic goals."""
        mock_load_todos.return_value = {"strategic_goals": [{"id": "goal-1"}]}
        goals = get_strategic_goals()
        self.assertEqual(goals, [{"id": "goal-1"}])

    @patch("afs_fastapi.core.todos_manager.load_todos")
    @patch("afs_fastapi.core.todos_manager.save_todos")
    def test_add_strategic_goal(self, mock_save_todos, mock_load_todos):
        """Test that add_strategic_goal adds a new goal."""
        mock_load_todos.return_value = {"strategic_goals": []}
        add_strategic_goal("Test Goal", "test-category", "high")
        self.assertTrue(mock_save_todos.called)
        saved_data = mock_save_todos.call_args[0][0]
        self.assertEqual(len(saved_data["strategic_goals"]), 1)
        self.assertEqual(saved_data["strategic_goals"][0]["description"], "Test Goal")

    @patch("afs_fastapi.core.todos_manager.load_todos")
    @patch("afs_fastapi.core.todos_manager.save_todos")
    def test_complete_strategic_goal(self, mock_save_todos, mock_load_todos):
        """Test that complete_strategic_goal marks a goal as completed."""
        mock_load_todos.return_value = {"strategic_goals": [{"id": "goal-1", "status": "pending"}]}
        complete_strategic_goal("goal-1")
        self.assertTrue(mock_save_todos.called)
        saved_data = mock_save_todos.call_args[0][0]
        self.assertEqual(saved_data["strategic_goals"][0]["status"], "completed")

    @patch("afs_fastapi.core.todos_manager.load_todos")
    @patch("afs_fastapi.core.todos_manager.save_todos")
    def test_reorder_strategic_goals(self, mock_save_todos, mock_load_todos):
        """Test that reorder_strategic_goals reorders the goals."""
        mock_load_todos.return_value = {
            "strategic_goals": [
                {"id": "goal-1"},
                {"id": "goal-2"},
                {"id": "goal-3"},
            ]
        }
        reorder_strategic_goals("goal-3", 1)
        self.assertTrue(mock_save_todos.called)
        saved_data = mock_save_todos.call_args[0][0]
        self.assertEqual(saved_data["strategic_goals"][0]["id"], "goal-3")

    @patch("afs_fastapi.core.todos_manager.load_todos")
    @patch("afs_fastapi.core.todos_manager.save_todos")
    def test_delete_strategic_goal(self, mock_save_todos, mock_load_todos):
        """Test that delete_strategic_goal deletes a goal."""
        mock_load_todos.return_value = {"strategic_goals": [{"id": "goal-1"}]}
        delete_strategic_goal("goal-1")
        self.assertTrue(mock_save_todos.called)
        saved_data = mock_save_todos.call_args[0][0]
        self.assertEqual(len(saved_data["strategic_goals"]), 0)

    @patch("afs_fastapi.core.todos_manager.load_todos")
    def test_get_all_phases(self, mock_load_todos):
        """Test that get_all_phases returns all phases."""
        mock_load_todos.return_value = {
            "strategic_goals": [
                {"id": "goal-1", "phases": [{"id": "phase-1"}]},
                {"id": "goal-2", "phases": [{"id": "phase-2"}, {"id": "phase-3"}]},
            ]
        }
        phases = get_all_phases()
        self.assertEqual(len(phases), 3)
        self.assertEqual(phases[0]["strategic_goal_id"], "goal-1")

    @patch("afs_fastapi.core.todos_manager.load_todos")
    def test_get_active_phase(self, mock_load_todos):
        """Test that get_active_phase returns the active phase."""
        mock_load_todos.return_value = {
            "strategic_goals": [
                {"id": "goal-1", "phases": [{"id": "phase-1", "status": "active"}]},
                {"id": "goal-2", "phases": [{"id": "phase-2", "status": "completed"}]},
            ]
        }
        active_phase = get_active_phase()
        self.assertEqual(active_phase["id"], "phase-1")

    @patch("afs_fastapi.core.todos_manager.load_todos")
    @patch("afs_fastapi.core.todos_manager.save_todos")
    def test_start_phase(self, mock_save_todos, mock_load_todos):
        """Test that start_phase starts a new phase."""
        mock_load_todos.return_value = {"strategic_goals": [{"id": "goal-1", "phases": []}]}
        start_phase("New Phase", "goal-1")
        self.assertTrue(mock_save_todos.called)
        saved_data = mock_save_todos.call_args[0][0]
        self.assertEqual(len(saved_data["strategic_goals"][0]["phases"]), 1)
        self.assertEqual(saved_data["strategic_goals"][0]["phases"][0]["name"], "New Phase")
        self.assertEqual(saved_data["strategic_goals"][0]["phases"][0]["status"], "active")

    @patch("afs_fastapi.core.todos_manager.load_todos")
    @patch("afs_fastapi.core.todos_manager.save_todos")
    def test_end_phase(self, mock_save_todos, mock_load_todos):
        """Test that end_phase ends the active phase."""
        mock_load_todos.return_value = {
            "strategic_goals": [
                {"id": "goal-1", "phases": [{"id": "phase-1", "status": "active", "tasks": []}]}
            ]
        }
        end_phase()
        self.assertTrue(mock_save_todos.called)
        saved_data = mock_save_todos.call_args[0][0]
        self.assertEqual(saved_data["strategic_goals"][0]["phases"][0]["status"], "completed")

    @patch("afs_fastapi.core.todos_manager.load_todos")
    @patch("afs_fastapi.core.todos_manager.save_todos")
    def test_pause_active_phase(self, mock_save_todos, mock_load_todos):
        """Test that pause_active_phase pauses the active phase."""
        mock_load_todos.return_value = {
            "strategic_goals": [{"id": "goal-1", "phases": [{"id": "phase-1", "status": "active"}]}]
        }
        pause_active_phase()
        self.assertTrue(mock_save_todos.called)
        saved_data = mock_save_todos.call_args[0][0]
        self.assertEqual(saved_data["strategic_goals"][0]["phases"][0]["status"], "paused")

    @patch("afs_fastapi.core.todos_manager.load_todos")
    @patch("afs_fastapi.core.todos_manager.save_todos")
    def test_resume_paused_phase(self, mock_save_todos, mock_load_todos):
        """Test that resume_paused_phase resumes a paused phase."""
        mock_load_todos.return_value = {
            "strategic_goals": [{"id": "goal-1", "phases": [{"id": "phase-1", "status": "paused"}]}]
        }
        resume_paused_phase()
        self.assertTrue(mock_save_todos.called)
        saved_data = mock_save_todos.call_args[0][0]
        self.assertEqual(saved_data["strategic_goals"][0]["phases"][0]["status"], "active")

    @patch("afs_fastapi.core.todos_manager.load_todos")
    @patch("afs_fastapi.core.todos_manager.save_todos")
    def test_delete_phase(self, mock_save_todos, mock_load_todos):
        """Test that delete_phase deletes a phase."""
        mock_load_todos.return_value = {
            "strategic_goals": [{"id": "goal-1", "phases": [{"id": "phase-1"}]}]
        }
        delete_phase("phase-1")
        self.assertTrue(mock_save_todos.called)
        saved_data = mock_save_todos.call_args[0][0]
        self.assertEqual(len(saved_data["strategic_goals"][0]["phases"]), 0)

    @patch("afs_fastapi.core.todos_manager.load_todos")
    @patch("afs_fastapi.core.todos_manager.save_todos")
    def test_reorder_phases(self, mock_save_todos, mock_load_todos):
        """Test that reorder_phases reorders the phases."""
        mock_load_todos.return_value = {
            "strategic_goals": [{"id": "goal-1", "phases": [{"id": "phase-1"}, {"id": "phase-2"}]}]
        }
        reorder_phases("phase-2", 1)
        self.assertTrue(mock_save_todos.called)
        saved_data = mock_save_todos.call_args[0][0]
        self.assertEqual(saved_data["strategic_goals"][0]["phases"][0]["id"], "phase-2")

    @patch("afs_fastapi.core.todos_manager.load_todos")
    @patch("afs_fastapi.core.todos_manager.save_todos")
    def test_add_task_to_active_phase(self, mock_save_todos, mock_load_todos):
        """Test that add_task_to_active_phase adds a task."""
        mock_load_todos.return_value = {
            "strategic_goals": [
                {"id": "goal-1", "phases": [{"id": "phase-1", "status": "active", "tasks": []}]}
            ]
        }
        add_task_to_active_phase("New Task")
        self.assertTrue(mock_save_todos.called)
        saved_data = mock_save_todos.call_args[0][0]
        self.assertEqual(len(saved_data["strategic_goals"][0]["phases"][0]["tasks"]), 1)
        self.assertEqual(
            saved_data["strategic_goals"][0]["phases"][0]["tasks"][0]["description"], "New Task"
        )

    @patch("afs_fastapi.core.todos_manager.load_todos")
    @patch("afs_fastapi.core.todos_manager.save_todos")
    def test_complete_task_in_active_phase(self, mock_save_todos, mock_load_todos):
        """Test that complete_task_in_active_phase completes a task."""
        mock_load_todos.return_value = {
            "strategic_goals": [
                {
                    "id": "goal-1",
                    "phases": [
                        {
                            "id": "phase-1",
                            "status": "active",
                            "tasks": [{"id": "task-1", "status": "pending"}],
                        }
                    ],
                }
            ]
        }
        complete_task_in_active_phase("task-1")
        self.assertTrue(mock_save_todos.called)
        saved_data = mock_save_todos.call_args[0][0]
        self.assertEqual(
            saved_data["strategic_goals"][0]["phases"][0]["tasks"][0]["status"], "completed"
        )

    @patch("afs_fastapi.core.todos_manager.load_todos")
    @patch("afs_fastapi.core.todos_manager.save_todos")
    def test_delete_task(self, mock_save_todos, mock_load_todos):
        """Test that delete_task deletes a task."""
        mock_load_todos.return_value = {
            "strategic_goals": [
                {"id": "goal-1", "phases": [{"id": "phase-1", "tasks": [{"id": "task-1"}]}]}
            ]
        }
        delete_task("task-1")
        self.assertTrue(mock_save_todos.called)
        saved_data = mock_save_todos.call_args[0][0]
        self.assertEqual(len(saved_data["strategic_goals"][0]["phases"][0]["tasks"]), 0)

    @patch("afs_fastapi.core.todos_manager.load_todos")
    @patch("afs_fastapi.core.todos_manager.save_todos")
    def test_reorder_tasks(self, mock_save_todos, mock_load_todos):
        """Test that reorder_tasks reorders the tasks."""
        mock_load_todos.return_value = {
            "strategic_goals": [
                {
                    "id": "goal-1",
                    "phases": [{"id": "phase-1", "tasks": [{"id": "task-1"}, {"id": "task-2"}]}],
                }
            ]
        }
        reorder_tasks("task-2", 1)
        self.assertTrue(mock_save_todos.called)
        saved_data = mock_save_todos.call_args[0][0]
        self.assertEqual(saved_data["strategic_goals"][0]["phases"][0]["tasks"][0]["id"], "task-2")

    @patch("afs_fastapi.core.todos_manager.load_todos")
    @patch("afs_fastapi.core.todos_manager.save_todos")
    def test_pause_task(self, mock_save_todos, mock_load_todos):
        """Test that pause_task pauses a task."""
        mock_load_todos.return_value = {
            "strategic_goals": [
                {
                    "id": "goal-1",
                    "phases": [
                        {
                            "id": "phase-1",
                            "status": "active",
                            "tasks": [{"id": "task-1", "status": "pending"}],
                        }
                    ],
                }
            ]
        }
        pause_task("task-1")
        self.assertTrue(mock_save_todos.called)
        saved_data = mock_save_todos.call_args[0][0]
        self.assertEqual(
            saved_data["strategic_goals"][0]["phases"][0]["tasks"][0]["status"], "paused"
        )

    @patch("afs_fastapi.core.todos_manager.load_todos")
    @patch("afs_fastapi.core.todos_manager.save_todos")
    def test_resume_task(self, mock_save_todos, mock_load_todos):
        """Test that resume_task resumes a task."""
        mock_load_todos.return_value = {
            "strategic_goals": [
                {
                    "id": "goal-1",
                    "phases": [
                        {
                            "id": "phase-1",
                            "status": "active",
                            "tasks": [{"id": "task-1", "status": "paused"}],
                        }
                    ],
                }
            ]
        }
        resume_task("task-1")
        self.assertTrue(mock_save_todos.called)
        saved_data = mock_save_todos.call_args[0][0]
        self.assertEqual(
            saved_data["strategic_goals"][0]["phases"][0]["tasks"][0]["status"], "pending"
        )

    @patch("afs_fastapi.core.todos_manager.load_todos")
    @patch("afs_fastapi.core.todos_manager.save_todos")
    def test_update_parent_statuses(self, mock_save_todos, mock_load_todos):
        """Test that update_parent_statuses updates the parent statuses."""
        mock_load_todos.return_value = {
            "strategic_goals": [
                {
                    "id": "goal-1",
                    "status": "pending",
                    "phases": [
                        {
                            "id": "phase-1",
                            "status": "active",
                            "tasks": [{"id": "task-1", "status": "paused"}],
                        }
                    ],
                }
            ]
        }
        update_parent_statuses()
        self.assertTrue(mock_save_todos.called)
        saved_data = mock_save_todos.call_args[0][0]
        self.assertEqual(
            saved_data["strategic_goals"][0]["phases"][0]["status"], "partially-paused"
        )
        self.assertEqual(saved_data["strategic_goals"][0]["status"], "partially-paused")


if __name__ == "__main__":
    unittest.main()
