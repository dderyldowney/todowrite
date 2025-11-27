"""
Context model.

This module contains the Context SQLAlchemy model.
"""

from __future__ import annotations

from datetime import datetime

from sqlalchemy import TIMESTAMP, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from todowrite.core.associations import (
    concepts_contexts,
    contexts_labels,
    goals_contexts,
    requirements_contexts,
)
from todowrite.core.models.base import Base
from todowrite.core.timestamp_mixins import TimestampMixin


class Context(Base, TimestampMixin):
    """ToDoWrite Context model for hierarchical task management."""

    __tablename__ = "contexts"

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
        "Label", secondary=contexts_labels, back_populates="contexts"
    )

    # belongs_to :concepts (through concepts_contexts)
    concepts: Mapped[list[Concept]] = relationship(
        "Concept", secondary=concepts_contexts, back_populates="contexts"
    )

    # belongs_to :goals (through goals_contexts)
    goals: Mapped[list[Goal]] = relationship(
        "Goal", secondary=goals_contexts, back_populates="contexts"
    )

    # belongs_to :requirements (through requirements_contexts)
    requirements: Mapped[list[Requirements]] = relationship(
        "Requirements",
        secondary=requirements_contexts,
        back_populates="contexts",
    )
