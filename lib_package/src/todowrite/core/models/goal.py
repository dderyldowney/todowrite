"""
Goal model.

This module contains the Goal SQLAlchemy model.
"""

from __future__ import annotations

from datetime import datetime

# Import model types for type hints
from typing import TYPE_CHECKING

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
    constraints_goals,
    goals_concepts,
    goals_contexts,
    goals_labels,
    goals_phases,
    goals_tasks,
)

if TYPE_CHECKING:
    from todowrite.core.models import (
        Concept,
        Constraint,
        Context,
        Label,
        Phase,
        Task,
    )
from sqlalchemy.orm import Session as SQLAlchemySession

from todowrite.core.models.base import Base
from todowrite.core.timestamp_mixins import (
    TimestampMixin,
    format_timestamp_iso,
    get_optimized_timestamp,
)


class Goal(Base, TimestampMixin):
    """ToDoWrite Goal model for hierarchical task management."""

    __tablename__ = "goals"

    # Primary key (Integer for SQLite autoincrement compatibility)
    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True, nullable=False
    )

    # Model fields with proper types
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str | None] = mapped_column(Text)
    status: Mapped[str] = mapped_column(
        String, default="planned", nullable=False
    )
    progress: Mapped[int] = mapped_column(Integer, default=0)
    started_on: Mapped[datetime | None] = mapped_column(
        TIMESTAMP, nullable=True
    )
    ended_on: Mapped[datetime | None] = mapped_column(TIMESTAMP, nullable=True)
    owner: Mapped[str | None] = mapped_column(String(255))
    severity: Mapped[str | None] = mapped_column(String)
    work_type: Mapped[str | None] = mapped_column(String)
    assignee: Mapped[str | None] = mapped_column(String(255))
    extra_data: Mapped[str | None] = mapped_column(Text)  # JSON string

    # Relationships
    labels: Mapped[list[Label]] = relationship(
        "Label", secondary=goals_labels, back_populates="goals"
    )

    # has_many :tasks (through goals_tasks)
    tasks: Mapped[list[Task]] = relationship(
        "Task", secondary=goals_tasks, back_populates="goals"
    )

    # has_many :phases (through goals_phases)
    phases: Mapped[list[Phase]] = relationship(
        "Phase", secondary=goals_phases, back_populates="goals"
    )

    # has_many :constraints (through constraints_goals)
    constraints: Mapped[list[Constraint]] = relationship(
        "Constraint", secondary=constraints_goals, back_populates="goals"
    )

    # has_many :concepts (through goals_concepts)
    concepts: Mapped[list[Concept]] = relationship(
        "Concept", secondary=goals_concepts, back_populates="goals"
    )

    # has_many :contexts (through goals_contexts)
    contexts: Mapped[list[Context]] = relationship(
        "Context", secondary=goals_contexts, back_populates="goals"
    )

    def __str__(self) -> str:
        """String representation of Goal."""
        return f"Goal(id={self.id}, title='{self.title}', progress={self.progress})"

    def __repr__(self) -> str:
        """Detailed string representation of Goal."""
        return (
            f"Goal(id={self.id}, title='{self.title}', description='{self.description}', "
            f"progress={self.progress}, owner='{self.owner}', severity='{self.severity}', "
            f"work_type='{self.work_type}', assignee='{self.assignee}')"
        )

    # Class methods for object creation
    @classmethod
    def create(
        cls,
        title: str,
        description: str = "",
        owner: str = "",
        severity: str = "",
        work_type: str = "",
        assignee: str = "",
    ) -> Goal:
        """Create a new Goal instance with default values."""
        return cls(
            title=title,
            description=description,
            owner=owner,
            severity=severity,
            work_type=work_type,
            assignee=assignee,
        )

    # Instance methods for workflow management
    def start_work(self) -> None:
        """Mark goal as started by setting started_on to current timestamp."""
        self.started_on = get_optimized_timestamp()

    def complete_work(self) -> None:
        """Mark goal as completed by setting ended_on to current timestamp."""
        self.ended_on = get_optimized_timestamp()

    def set_progress(self, progress: int) -> None:
        """Set progress percentage (0-100)."""
        if 0 <= progress <= 100:
            self.progress = progress
        else:
            raise ValueError("Progress must be between 0 and 100")

    def is_completed(self) -> bool:
        """Check if goal is marked as completed."""
        return self.ended_on is not None

    def is_started(self) -> bool:
        """Check if goal is marked as started."""
        return self.started_on is not None

    # Instance methods for relationship management
    def add_label(self, label: Label) -> None:
        """Add a label to this goal."""
        if label not in self.labels:
            self.labels.append(label)

    def remove_label(self, label: Label) -> None:
        """Remove a label from this goal."""
        if label in self.labels:
            self.labels.remove(label)

    def add_task(self, task: Task) -> None:
        """Add a task to this goal."""
        if task not in self.tasks:
            self.tasks.append(task)

    def remove_task(self, task: Task) -> None:
        """Remove a task from this goal."""
        if task in self.tasks:
            self.tasks.remove(task)

    def add_phase(self, phase: Phase) -> None:
        """Add a phase to this goal."""
        if phase not in self.phases:
            self.phases.append(phase)

    def remove_phase(self, phase: Phase) -> None:
        """Remove a phase from this goal."""
        if phase in self.phases:
            self.phases.remove(phase)

    def to_dict(self) -> dict[str, object]:
        """Convert goal to dictionary representation."""
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "progress": self.progress,
            "started_on": format_timestamp_iso(self.started_on)
            if self.started_on
            else None,
            "ended_on": format_timestamp_iso(self.ended_on)
            if self.ended_on
            else None,
            "owner": self.owner,
            "severity": self.severity,
            "work_type": self.work_type,
            "assignee": self.assignee,
            "extra_data": self.extra_data,
            "created_at": format_timestamp_iso(self.created_at)
            if self.created_at
            else None,
            "updated_at": format_timestamp_iso(self.updated_at)
            if self.updated_at
            else None,
        }

    @classmethod
    def from_dict(cls, data: dict[str, object]) -> Goal:
        """Create Goal instance from dictionary."""
        return cls(
            title=data.get("title", ""),
            description=data.get("description", ""),
            progress=data.get("progress"),
            started_on=data.get("started_on"),
            ended_on=data.get("ended_on"),
            owner=data.get("owner", ""),
            severity=data.get("severity", ""),
            work_type=data.get("work_type", ""),
            assignee=data.get("assignee", ""),
            extra_data=data.get("extra_data"),
        )

    # Instance methods for persistence
    def save(self, session: SQLAlchemySession) -> None:
        """Save this goal to the database."""
        session.add(self)
        session.commit()

    def delete(self, session: SQLAlchemySession) -> None:
        """Delete this goal from the database."""
        session.delete(self)
        session.commit()

    # Class methods for querying
    @classmethod
    def find_by_id(
        cls, session: SQLAlchemySession, goal_id: int
    ) -> Goal | None:
        """Find a goal by ID."""
        return session.query(cls).filter(cls.id == goal_id).first()

    @classmethod
    def find_by_title(
        cls, session: SQLAlchemySession, title: str
    ) -> Goal | None:
        """Find a goal by title."""
        return session.query(cls).filter(cls.title == title).first()

    @classmethod
    def all(cls, session: SQLAlchemySession) -> list[Goal]:
        """Get all goals."""
        return session.query(cls).all()

    @classmethod
    def find_completed(cls, session: SQLAlchemySession) -> list[Goal]:
        """Get all completed goals."""
        return session.query(cls).filter(cls.ended_on.isnot(None)).all()

    @classmethod
    def find_active(cls, session: SQLAlchemySession) -> list[Goal]:
        """Get all active (not completed) goals."""
        return session.query(cls).filter(cls.ended_on.is_(None)).all()

    # Utility methods
    def get_work_duration(self) -> str | None:
        """Get the duration between start and completion in ISO format."""
        if self.started_on and self.ended_on:
            start_ts = get_optimized_timestamp()
            completion_ts = get_optimized_timestamp()
            # Calculate duration (placeholder - would need actual timestamp parsing)
            return f"Duration: {completion_ts - start_ts}"
        return None

    def get_summary(self) -> str:
        """Get a brief summary of the goal."""
        status = (
            "Completed"
            if self.is_completed()
            else ("Active" if self.is_started() else "Not Started")
        )
        return f"Goal: {self.title} ({status}) - {self.progress}% complete"

    # Validation methods
    def validate(self) -> list[str]:
        """Validate goal data and return list of errors."""
        errors = []
        if not self.title or not self.title.strip():
            errors.append("Title cannot be empty")
        if self.progress is not None and (
            self.progress < 0 or self.progress > 100
        ):
            errors.append("Progress must be between 0 and 100")
        return errors

    def is_valid(self) -> bool:
        """Check if goal data is valid."""
        return len(self.validate()) == 0

    # TODO: Hierarchical aggregation properties can be added later
    # Goal.phases, Phase.steps, Step.tasks, Task.commands - maintaining clean architecture
