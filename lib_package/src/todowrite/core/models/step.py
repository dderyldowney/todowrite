"""
Step model.

This module contains the Step SQLAlchemy model.
"""

from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from todowrite.core.models.label import Label
    from todowrite.core.models.phase import Phase
    from todowrite.core.models.task import Task

from sqlalchemy import (
    TIMESTAMP,
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
    phases_steps,
    steps_labels,
    steps_tasks,
)
from todowrite.core.models.base import Base
from todowrite.core.timestamp_mixins import (
    TimestampMixin,
)


class Step(Base, TimestampMixin):
    """ToDoWrite Step model for hierarchical task management."""

    __tablename__ = "steps"

    # Primary key convention
    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True, nullable=False
    )

    # Model fields
    title: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str | None] = mapped_column(Text)
    status: Mapped[str] = mapped_column(String, default="planned")
    progress: Mapped[int | None] = mapped_column(Integer)
    started_on: Mapped[datetime | None] = mapped_column(
        TIMESTAMP, nullable=True
    )
    ended_on: Mapped[datetime | None] = mapped_column(TIMESTAMP, nullable=True)

    # Metadata fields
    owner: Mapped[str | None] = mapped_column(String)
    severity: Mapped[str | None] = mapped_column(String)
    work_type: Mapped[str | None] = mapped_column(String)
    assignee: Mapped[str | None] = mapped_column(String)

    # JSON fields for complex data
    extra_data: Mapped[str | None] = mapped_column(Text)

    # Relationships
    labels: Mapped[list[Label]] = relationship(
        "Label", secondary=steps_labels, back_populates="steps"
    )

    # belongs_to :phases (through phases_steps)
    phases: Mapped[list[Phase]] = relationship(
        "Phase", secondary=phases_steps, back_populates="steps"
    )

    # has_many :tasks (through steps_tasks)
    tasks: Mapped[list[Task]] = relationship(
        "Task", secondary=steps_tasks, back_populates="steps"
    )
