"""
SubTask model.

This module contains the SubTask SQLAlchemy model.
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
    sub_tasks_commands,
    sub_tasks_labels,
    tasks_sub_tasks,
)
from todowrite.core.models.base import Base
from todowrite.core.timestamp_mixins import (
    TimestampMixin,
)


class SubTask(Base, TimestampMixin):
    """ToDoWrite SubTask model for hierarchical task management."""

    __tablename__ = "sub_tasks"

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
        "Label", secondary=sub_tasks_labels, back_populates="sub_tasks"
    )

    # belongs_to :tasks (through tasks_sub_tasks)
    tasks: Mapped[list[Task]] = relationship(
        "Task", secondary=tasks_sub_tasks, back_populates="sub_tasks"
    )

    # has_many :commands (through sub_tasks_commands)
    commands: Mapped[list[Command]] = relationship(
        "Command", secondary=sub_tasks_commands, back_populates="sub_tasks"
    )
