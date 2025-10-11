"""TodoWrite Integration Module for Claude Code.

Provides seamless integration between Claude Code TodoWrite tool and the
4-level AFS FastAPI hierarchy: Strategic Goal → Phase → Step → Task.

This module enables saving TodoWrite tasks at any level with minimal steps,
fulfilling the user requirement for "as few steps as possible" saving.
"""

from __future__ import annotations

from typing import Any

from .todos_manager import (
    auto_save_todowrite,
    get_active_phase,
    get_active_step,
    save_todowrite_to_phase,
    save_todowrite_to_step,
)


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
            target_level: 'auto', 'step', 'phase', or 'strategic' (default: 'auto')

        Returns:
            Tuple of (success_message, error_message)
        """
        if not todowrite_tasks:
            return "No TodoWrite tasks to save", None

        # Automatic level detection (default)
        if target_level == "auto":
            return auto_save_todowrite(todowrite_tasks, agricultural_context)

        # Explicit level targeting
        if target_level == "step":
            active_step = get_active_step()
            if active_step:
                created_tasks, error = save_todowrite_to_step(active_step["id"], todowrite_tasks)
                if not error:
                    return f"Saved {len(created_tasks)} tasks to step: {active_step['name']}", None
                return "", error
            return "", "No active step found. Use 'auto' or 'phase' level."

        if target_level == "phase":
            active_phase = get_active_phase()
            if active_phase:
                step_name = "TodoWrite Tasks"
                if agricultural_context:
                    step_name = f"{agricultural_context} - TodoWrite Tasks"

                new_step, error = save_todowrite_to_phase(
                    active_phase["id"], todowrite_tasks, step_name
                )
                if not error and new_step:
                    return (
                        f"Created step '{new_step['name']}' with {len(todowrite_tasks)} tasks",
                        None,
                    )
                return "", error or "Failed to create step in active phase"
            return "", "No active phase found. Use 'auto' level."

        return "", f"Unknown target level: {target_level}. Use 'auto', 'step', or 'phase'."

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
                "content": task_content.strip(),
                "status": "pending",
                "activeForm": f"Working on {task_content.strip()}",
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
                "content": task.get("content", "").strip(),
                "status": task.get("status", "pending"),
                "activeForm": f"Working on {task.get('content', '').strip()}",
            }
            for task in tasks_with_status
            if task.get("content", "").strip()
        ]

        return TodoWriteIntegration.save_current_todowrite(todowrite_tasks, agricultural_context)

    @staticmethod
    def get_current_context() -> dict[str, Any]:
        """Get current agricultural context for TodoWrite saving.

        Returns:
            Dictionary with current phase, step, and suggested contexts
        """
        active_phase = get_active_phase()
        active_step = get_active_step()

        context = {
            "active_phase": active_phase["name"] if active_phase else None,
            "active_step": active_step["name"] if active_step else None,
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


def get_save_context() -> dict[str, Any]:
    """Get current context for TodoWrite saving decisions."""
    return TodoWriteIntegration.get_current_context()
