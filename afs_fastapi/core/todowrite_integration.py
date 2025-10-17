"""TodoWrite Integration Module for Claude Code.

Provides seamless integration between Claude Code TodoWrite tool and the
4-level AFS FastAPI hierarchy: Strategic Goal → Phase → Step → Task.

This module enables saving TodoWrite tasks at any level with minimal steps,
fulfilling the user requirement for "as few steps as possible" saving.
"""

from __future__ import annotations

from typing import Any, TypedDict


class Context(TypedDict):
    active_goal: str | None
    active_phase: str | None
    active_step: str | None
    active_task: str | None
    suggested_agricultural_contexts: list[str]
    available_levels: list[str]


from .todos_manager import add_step, add_subtask, add_task, get_active_items  # noqa: E402


class TodoWriteIntegration:
    """Seamless integration interface for TodoWrite tool."""

    @staticmethod
    def save_current_todowrite(
        todowrite_tasks: list[dict[str, Any]],
        agricultural_context: str | None = None,
        target_level: str = "auto",
    ) -> tuple[str, str | None]:
        """Save current TodoWrite tasks with automatic level detection.

        Args:
            todowrite_tasks: List of TodoWrite task dictionaries with 'content', 'status', etc.
            agricultural_context: Optional context for agricultural robotics domain
            target_level: 'auto', 'task', 'step', or 'phase' (default: 'auto')

        Returns:
            Tuple of (success_message, error_message)
        """
        if not todowrite_tasks:
            return "No tasks to save", None

        active_items = get_active_items()
        active_phase = active_items.get("phase")
        active_step = active_items.get("step")
        active_task = active_items.get("task")

        created_count = 0
        error_message = None

        if target_level == "auto":
            if active_task:
                for task_data in todowrite_tasks:
                    subtask, err = add_subtask(
                        task_id=active_task["id"],
                        title=task_data.get("content", "New SubTask"),
                        description=task_data.get("content", "No description provided."),
                        command=task_data.get("command", "todo"),
                        command_type=task_data.get("command_type", "bash"),
                    )
                    if subtask:
                        created_count += 1
                    if err:
                        error_message = err
                        break
                if created_count > 0:
                    return (
                        f"Saved {created_count} subtasks to active task: {active_task['title']}",
                        error_message,
                    )
            elif active_step:
                for task_data in todowrite_tasks:
                    task, err = add_task(
                        step_id=active_step["id"],
                        title=task_data.get("content", "New Task"),
                        description=task_data.get("content", "No description provided."),
                    )
                    if task:
                        created_count += 1
                    if err:
                        error_message = err
                        break
                if created_count > 0:
                    return (
                        f"Saved {created_count} tasks to active step: {active_step['title']}",
                        error_message,
                    )
            elif active_phase:
                for task_data in todowrite_tasks:
                    step, err = add_step(
                        phase_id=active_phase["id"],
                        title=task_data.get("content", "New Step"),
                        description=task_data.get("content", "No description provided."),
                    )
                    if step:
                        created_count += 1
                    if err:
                        error_message = err
                        break
                if created_count > 0:
                    return (
                        f"Saved {created_count} steps to active phase: {active_phase['title']}",
                        error_message,
                    )
            else:
                return "", "No active goal, phase, step, or task found for auto-saving."

        elif target_level == "task":
            if active_task:
                for task_data in todowrite_tasks:
                    subtask, err = add_subtask(
                        task_id=active_task["id"],
                        title=task_data.get("content", "New SubTask"),
                        description=task_data.get("content", "No description provided."),
                        command=task_data.get("command", "todo"),
                        command_type=task_data.get("command_type", "bash"),
                    )
                    if subtask:
                        created_count += 1
                    if err:
                        error_message = err
                        break
                if created_count > 0:
                    return (
                        f"Saved {created_count} subtasks to active task: {active_task['title']}",
                        error_message,
                    )
                return "", error_message or "Failed to save subtasks to active task."
            return "", "No active task found for saving."

        elif target_level == "step":
            if active_step:
                for task_data in todowrite_tasks:
                    task, err = add_task(
                        step_id=active_step["id"],
                        title=task_data.get("content", "New Task"),
                        description=task_data.get("content", "No description provided."),
                    )
                    if task:
                        created_count += 1
                    if err:
                        error_message = err
                        break
                if created_count > 0:
                    return (
                        f"Saved {created_count} tasks to active step: {active_step['title']}",
                        error_message,
                    )
                return "", error_message or "Failed to save tasks to active step."
            return "", "No active step found for saving."

        elif target_level == "phase":
            if active_phase:
                for task_data in todowrite_tasks:
                    step, err = add_step(
                        phase_id=active_phase["id"],
                        title=task_data.get("content", "New Step"),
                        description=task_data.get("content", "No description provided."),
                    )
                    if step:
                        created_count += 1
                    if err:
                        error_message = err
                        break
                if created_count > 0:
                    return (
                        f"Saved {created_count} steps to active phase: {active_phase['title']}",
                        error_message,
                    )
                return "", error_message or "Failed to save steps to active phase."
            return "", "No active phase found for saving."

        return "", f"Unknown target level: {target_level}. Use 'auto', 'task', 'step', or 'phase'."

    @staticmethod
    def quick_save(
        content_list: list[str], agricultural_context: str | None = None
    ) -> tuple[str, str | None]:
        """Quick save for simple task lists with minimal interface.

        Args:
            content_list: List of task descriptions as strings
            agricultural_context: Optional agricultural robotics context

        Returns:
            Tuple of (success_message, error_message)
        """
        if not content_list:
            return "No tasks to save", None

        # Convert simple strings to TodoWrite format
        todowrite_tasks = [
            {
                "content": task_content.strip() if task_content else "",
                "status": "pending",
                "activeForm": f"Working on {task_content.strip() if task_content else ''}",
            }
            for task_content in content_list
            if task_content.strip()
        ]

        return TodoWriteIntegration.save_current_todowrite(todowrite_tasks, agricultural_context)

    @staticmethod
    def save_with_status(
        tasks_with_status: list[dict[str, str]], agricultural_context: str | None = None
    ) -> tuple[str, str | None]:
        """Save tasks that already have completion status.

        Args:
            tasks_with_status: List of dicts with 'content' and 'status' ('pending'/'completed')
            agricultural_context: Optional agricultural robotics context

        Returns:
            Tuple of (success_message, error_message)
        """
        if not tasks_with_status:
            return "No tasks to save", None

        # Convert to TodoWrite format
        todowrite_tasks = [
            {
                "content": task.get("content", "").strip() if task.get("content") else "",
                "status": task.get("status", "planned"),
                "activeForm": f"Working on {task.get('content', '').strip() if task.get('content') else ''}",
            }
            for task in tasks_with_status
            if task.get("content", "").strip()
        ]

        return TodoWriteIntegration.save_current_todowrite(todowrite_tasks, agricultural_context)

    def get_current_context(self) -> Context:
        """Get current agricultural context for TodoWrite saving.

        Returns:
            Dictionary with current phase, step, and suggested contexts
        """
        active_items = get_active_items()
        active_goal = active_items.get("goal")
        active_phase = active_items.get("phase")
        active_step = active_items.get("step")
        active_task = active_items.get("task")

        context: Context = {
            "active_goal": active_goal["title"] if active_goal else None,
            "active_phase": active_phase["title"] if active_phase else None,
            "active_step": active_step["title"] if active_step else None,
            "active_task": active_task["title"] if active_task else None,
            "suggested_agricultural_contexts": [
                "CAN Bus Integration",
                "Agricultural Robotics Testing",
                "Tractor Fleet Coordination",
                "Safety Critical Systems",
                "Network Traffic Management",
                "Equipment Telemetry Processing",
            ],
            "available_levels": [],
        }

        # Determine available save levels
        if active_task:
            context["available_levels"].append("task")
        if active_step:
            context["available_levels"].append("step")
        if active_phase:
            context["available_levels"].append("phase")
        context["available_levels"].append("auto")

        return context


# Convenience functions for Claude Code integration
def save_todowrite_tasks(
    tasks: list[dict[str, Any]], context: str | None = None
) -> tuple[str, str | None]:
    """Main integration function for Claude Code TodoWrite tool.

    Saves TodoWrite tasks to the most appropriate level in the hierarchy
    with minimal steps required from the user.
    """
    return TodoWriteIntegration.save_current_todowrite(tasks, context)


def quick_save_tasks(task_list: list[str], context: str | None = None) -> tuple[str, str | None]:
    """Quick save function for simple task lists."""
    return TodoWriteIntegration.quick_save(task_list, context)


def get_save_context() -> Context:
    """Get current context for TodoWrite saving decisions."""
    return TodoWriteIntegration().get_current_context()
