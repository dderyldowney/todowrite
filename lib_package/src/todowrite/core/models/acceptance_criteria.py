"""
AcceptanceCriteria model.

This module contains the AcceptanceCriteria SQLAlchemy model.
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
    acceptance_criteria_interface_contracts,
    acceptance_criteria_labels,
    requirements_acceptance_criteria,
)
from todowrite.core.models.base import Base
from todowrite.core.timestamp_mixins import (
    TimestampMixin,
)


class AcceptanceCriteria(Base, TimestampMixin):
    """ToDoWrite AcceptanceCriteria model for hierarchical task management."""

    __tablename__ = "acceptance_criteria"

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
        "Label",
        secondary=acceptance_criteria_labels,
        back_populates="acceptance_criteria",
    )

    # belongs_to :requirements (through requirements_acceptance_criteria)
    requirements: Mapped[list[Requirements]] = relationship(
        "Requirements",
        secondary=requirements_acceptance_criteria,
        back_populates="acceptance_criteria",
    )

    # has_many :interface_contracts (through association table)
    interface_contracts: Mapped[list[InterfaceContract]] = relationship(
        "InterfaceContract",
        secondary=acceptance_criteria_interface_contracts,
        back_populates="acceptance_criteria",
    )
