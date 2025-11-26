"""
Concept model.

This module contains the Concept SQLAlchemy model.
"""

from __future__ import annotations

from sqlalchemy import Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from todowrite.core.associations import (
    concepts_contexts,
    concepts_labels,
    goals_concepts,
    requirements_concepts,
)
from todowrite.core.models.base import Base
from todowrite.core.timestamp_mixins import TimestampMixin


class Concept(Base, TimestampMixin):
    """ToDoWrite Concept model for hierarchical task management."""

    __tablename__ = "concepts"

    # Primary key (Integer for SQLite autoincrement compatibility)
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

    # Metadata fields (flattened for now, could be separate table)
    owner: Mapped[str | None] = mapped_column(String)
    severity: Mapped[str | None] = mapped_column(String)
    work_type: Mapped[str | None] = mapped_column(String)
    assignee: Mapped[str | None] = mapped_column(String)

    # JSON fields for complex data
    extra_data: Mapped[str | None] = mapped_column(Text)  # JSON string

    # Relationships
    labels: Mapped[list[Label]] = relationship(
        "Label", secondary=concepts_labels, back_populates="concepts"
    )

    # belongs_to :goals (through goals_concepts)
    goals: Mapped[list[Goal]] = relationship(
        "Goal", secondary=goals_concepts, back_populates="concepts"
    )

    # has_many :contexts (direct relationship - "conceptually building")
    contexts: Mapped[list[Context]] = relationship(
        "Context", secondary=concepts_contexts, back_populates="concepts"
    )

    # belongs_to :requirements (through requirements_concepts)
    requirements: Mapped[list[Requirements]] = relationship(
        "Requirements",
        secondary=requirements_concepts,
        back_populates="concepts",
    )
