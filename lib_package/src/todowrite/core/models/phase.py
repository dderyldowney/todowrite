"""
Phase model.

This module contains the Phase SQLAlchemy model.
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
    goals_phases,
    interface_contracts_phases,
    phases_labels,
    phases_steps,
)
from todowrite.core.models.base import Base
from todowrite.core.timestamp_mixins import (
    TimestampMixin,
)


class Phase(Base, TimestampMixin):
    """ToDoWrite Phase model for hierarchical task management."""

    __tablename__ = "phases"

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
        "Label", secondary=phases_labels, back_populates="phases"
    )

    # belongs_to :goals (through goals_phases)
    goals: Mapped[list[Goal]] = relationship(
        "Goal", secondary=goals_phases, back_populates="phases"
    )

    # has_many :steps (through phases_steps)
    steps: Mapped[list[Step]] = relationship(
        "Step", secondary=phases_steps, back_populates="phases"
    )

    # belongs_to :interface_contracts (through interface_contracts_phases)
    interface_contracts: Mapped[list[InterfaceContract]] = relationship(
        "InterfaceContract",
        secondary=interface_contracts_phases,
        back_populates="phases",
    )

    # Note: self.steps relationship is already provided by the SQLAlchemy relationship

    # TODO: Phase-level aggregation properties can be added later
    # Phase.tasks, Phase.commands - maintaining clean architecture
