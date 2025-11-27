"""
Command model.

This module contains the Command SQLAlchemy model.
"""

from __future__ import annotations

import json
from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import (
    TIMESTAMP,
    Integer,
    String,
    Text,
)

if TYPE_CHECKING:
    from todowrite.core.models.label import Label
    from todowrite.core.models.sub_task import SubTask
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)

from todowrite.core.associations import (
    commands_labels,
    sub_tasks_commands,
)
from todowrite.core.models.base import Base
from todowrite.core.timestamp_mixins import (
    TimestampMixin,
    get_optimized_timestamp,
)


class Command(Base, TimestampMixin):
    """ToDoWrite Command model for hierarchical task management."""

    __tablename__ = "commands"

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

    # Command-specific fields
    acceptance_criteria_id: Mapped[int | None] = mapped_column(
        Integer
    )  # Foreign key to AcceptanceCriteria
    cmd: Mapped[str | None] = mapped_column(Text)  # The script/executable name
    cmd_params: Mapped[str | None] = mapped_column(
        Text
    )  # Command parameters/arguments
    runtime_env: Mapped[str | None] = mapped_column(
        Text
    )  # JSON string with environment variables and runtime config
    output: Mapped[str | None] = mapped_column(
        Text
    )  # Command execution output (stdout/stderr)
    artifacts: Mapped[str | None] = mapped_column(
        Text
    )  # JSON string with expected outputs (log files, generated files, etc.)

    # Relationships
    labels: Mapped[list[Label]] = relationship(
        "Label", secondary=commands_labels, back_populates="commands"
    )

    # belongs_to :sub_tasks (through sub_tasks_commands)
    sub_tasks: Mapped[list[SubTask]] = relationship(
        "SubTask", secondary=sub_tasks_commands, back_populates="commands"
    )

    @property
    def runtime_env_dict(self) -> dict[str, str | int | bool | None]:
        """Get runtime environment as dictionary."""
        return json.loads(self.runtime_env) if self.runtime_env else {}

    @runtime_env_dict.setter
    def runtime_env_dict(
        self, value: dict[str, str | int | bool | None]
    ) -> None:
        """Set runtime environment from dictionary."""
        self.runtime_env = json.dumps(value)

    @property
    def artifacts_list(self) -> list[str]:
        """Get artifacts as list."""
        return json.loads(self.artifacts) if self.artifacts else []

    @artifacts_list.setter
    def artifacts_list(self, value: list[str]) -> None:
        """Set artifacts from list."""
        self.artifacts = json.dumps(value)

    def mark_completed(self) -> None:
        """Mark command as completed with current timestamp."""
        self.status = "completed"
        self.ended_on = get_optimized_timestamp()

    def mark_started(self) -> None:
        """Mark command as started with current timestamp."""
        self.status = "in_progress"
        self.started_on = get_optimized_timestamp()
