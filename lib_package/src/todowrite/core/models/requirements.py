"""
Requirements model.

This module contains the Requirements SQLAlchemy model.
"""

from __future__ import annotations

from sqlalchemy import Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from todowrite.core.associations import (
    constraints_requirements,
    requirements_acceptance_criteria,
    requirements_concepts,
    requirements_contexts,
    requirements_labels,
)
from todowrite.core.models.base import Base
from todowrite.core.timestamp_mixins import TimestampMixin


class Requirements(Base, TimestampMixin):
    """ToDoWrite Requirements model for hierarchical task management."""

    __tablename__ = "requirements"

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
        "Label", secondary=requirements_labels, back_populates="requirements"
    )

    # belongs_to :constraints (through constraints_requirements)
    constraints: Mapped[list[Constraints]] = relationship(
        "Constraints",
        secondary=constraints_requirements,
        back_populates="requirements",
    )

    # has_many :acceptance_criteria (through requirements_acceptance_criteria)
    acceptance_criteria: Mapped[list[AcceptanceCriteria]] = relationship(
        "AcceptanceCriteria",
        secondary=requirements_acceptance_criteria,
        back_populates="requirements",
    )

    # has_many :concepts (through requirements_concepts)
    concepts: Mapped[list[Concept]] = relationship(
        "Concept",
        secondary=requirements_concepts,
        back_populates="requirements",
    )

    # has_many :contexts (direct relationship - "context for requirement")
    contexts: Mapped[list[Context]] = relationship(
        "Context",
        secondary=requirements_contexts,
        back_populates="requirements",
    )
