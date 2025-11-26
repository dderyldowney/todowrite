"""
Task model.

This module contains the Task SQLAlchemy model.
"""

from __future__ import annotations

from sqlalchemy import (
    Integer,
    String,
    Text,
)
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)

from todowrite.core.associations import (
    goals_tasks,
    steps_tasks,
    tasks_labels,
    tasks_sub_tasks,
)
from todowrite.core.models.base import Base
from todowrite.core.timestamp_mixins import (
    TimestampMixin,
)


class Task(Base, TimestampMixin):
    """ToDoWrite Task model for hierarchical task management."""

    __tablename__ = "tasks"

    # Primary key convention
    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True, nullable=False
    )

    # Model fields
    title: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str | None] = mapped_column(Text)
    status: Mapped[str] = mapped_column(String, default="planned")
    progress: Mapped[int | None] = mapped_column(Integer)
    started_date: Mapped[str | None] = mapped_column(String)
    completion_date: Mapped[str | None] = mapped_column(String)

    # Metadata fields
    owner: Mapped[str | None] = mapped_column(String)
    severity: Mapped[str | None] = mapped_column(String)
    work_type: Mapped[str | None] = mapped_column(String)
    assignee: Mapped[str | None] = mapped_column(String)

    # JSON fields for complex data
    extra_data: Mapped[str | None] = mapped_column(Text)

    # Relationships
    labels: Mapped[list[Label]] = relationship(
        "Label", secondary=tasks_labels, back_populates="tasks"
    )

    # belongs_to :goals (through goals_tasks)
    goals: Mapped[list[Goal]] = relationship(
        "Goal", secondary=goals_tasks, back_populates="tasks"
    )

    # belongs_to :steps (through steps_tasks) - Task can belong to a Step
    steps: Mapped[list[Step]] = relationship(
        "Step", secondary=steps_tasks, back_populates="tasks"
    )

    # has_many :sub_tasks (through tasks_sub_tasks)
    sub_tasks: Mapped[list[SubTask]] = relationship(
        "SubTask", secondary=tasks_sub_tasks, back_populates="tasks"
    )

    @property
    def commands(self) -> list[Command]:
        """Get all commands from all subtasks for this task.

        Provides complete execution plan visibility by aggregating all commands
        across all subtasks belonging to this task.

        Returns:
            List of all Command objects from all subtasks in execution order.
        """
        all_commands: list[Command] = []
        for subtask in self.sub_tasks:
            all_commands.extend(subtask.commands)
        return all_commands

    @property
    def total_commands_count(self) -> int:
        """Get total number of commands across all subtasks."""
        return len(self.commands)

    @property
    def completed_commands_count(self) -> int:
        """Get count of completed commands across all subtasks."""
        return len([cmd for cmd in self.commands if cmd.status == "completed"])

    @property
    def execution_progress_percentage(self) -> float:
        """Calculate execution progress as percentage based on completed commands."""
        total = self.total_commands_count
        if total == 0:
            return 0.0
        completed = self.completed_commands_count
        return round((completed / total) * 100, 2)
