"""
Constraints model.

This module contains the Constraints SQLAlchemy model.
"""

from __future__ import annotations

from sqlalchemy import Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from todowrite.core.associations import (
    constraints_goals,
    constraints_labels,
    constraints_requirements,
)
from todowrite.core.models.base import Base
from todowrite.core.timestamp_mixins import TimestampMixin


class Constraints(Base, TimestampMixin):
    """ToDoWrite Constraints model for hierarchical task management."""

    __tablename__ = "constraints"

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
        "Label", secondary=constraints_labels, back_populates="constraints"
    )

    # belongs_to :goals (through constraints_goals)
    goals: Mapped[list[Goal]] = relationship(
        "Goal", secondary=constraints_goals, back_populates="constraints"
    )

    # has_many :requirements (through constraints_requirements)
    requirements: Mapped[list[Requirements]] = relationship(
        "Requirements",
        secondary=constraints_requirements,
        back_populates="constraints",
    )
