"""
Label model.

This module contains the Label SQLAlchemy model.
"""

from __future__ import annotations

from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from todowrite.core.associations import (
    acceptance_criteria_labels,
    commands_labels,
    concepts_labels,
    constraints_labels,
    contexts_labels,
    goals_labels,
    interface_contracts_labels,
    phases_labels,
    requirements_labels,
    steps_labels,
    sub_tasks_labels,
    tasks_labels,
)
from todowrite.core.models.base import Base
from todowrite.core.timestamp_mixins import TimestampMixin


class Label(Base, TimestampMixin):
    """ToDoWrite Label model for categorizing and tagging other models."""

    __tablename__ = "labels"

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True, nullable=False
    )
    name: Mapped[str] = mapped_column(String, nullable=False, unique=True)

    # Relationships (bidirectional with back_populates)
    goals: Mapped[list[Goal]] = relationship(
        "Goal", secondary=goals_labels, back_populates="labels"
    )
    concepts: Mapped[list[Concept]] = relationship(
        "Concept", secondary=concepts_labels, back_populates="labels"
    )
    contexts: Mapped[list[Context]] = relationship(
        "Context", secondary=contexts_labels, back_populates="labels"
    )
    constraints: Mapped[list[Constraints]] = relationship(
        "Constraints", secondary=constraints_labels, back_populates="labels"
    )
    requirements: Mapped[list[Requirements]] = relationship(
        "Requirements", secondary=requirements_labels, back_populates="labels"
    )
    acceptance_criteria: Mapped[list[AcceptanceCriteria]] = relationship(
        "AcceptanceCriteria",
        secondary=acceptance_criteria_labels,
        back_populates="labels",
    )
    interface_contracts: Mapped[list[InterfaceContract]] = relationship(
        "InterfaceContract",
        secondary=interface_contracts_labels,
        back_populates="labels",
    )
    phases: Mapped[list[Phase]] = relationship(
        "Phase", secondary=phases_labels, back_populates="labels"
    )
    steps: Mapped[list[Step]] = relationship(
        "Step", secondary=steps_labels, back_populates="labels"
    )
    tasks: Mapped[list[Task]] = relationship(
        "Task", secondary=tasks_labels, back_populates="labels"
    )
    sub_tasks: Mapped[list[SubTask]] = relationship(
        "SubTask", secondary=sub_tasks_labels, back_populates="labels"
    )
    commands: Mapped[list[Command]] = relationship(
        "Command", secondary=commands_labels, back_populates="labels"
    )
