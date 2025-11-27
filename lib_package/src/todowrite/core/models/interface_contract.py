"""
InterfaceContract model.

This module contains the InterfaceContract SQLAlchemy model.
"""

from __future__ import annotations

from datetime import datetime

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
    acceptance_criteria_interface_contracts,
    interface_contracts_labels,
    interface_contracts_phases,
)
from todowrite.core.models.base import Base
from todowrite.core.timestamp_mixins import (
    TimestampMixin,
)


class InterfaceContract(Base, TimestampMixin):
    """ToDoWrite InterfaceContract model for hierarchical task management."""

    __tablename__ = "interface_contracts"

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
        "Label",
        secondary=interface_contracts_labels,
        back_populates="interface_contracts",
    )

    # belongs_to :acceptance_criteria (through association table)
    acceptance_criteria: Mapped[list[AcceptanceCriteria]] = relationship(
        "AcceptanceCriteria",
        secondary=acceptance_criteria_interface_contracts,
        back_populates="interface_contracts",
    )

    # has_many :phases (through interface_contracts_phases)
    phases: Mapped[list[Phase]] = relationship(
        "Phase",
        secondary=interface_contracts_phases,
        back_populates="interface_contracts",
    )
