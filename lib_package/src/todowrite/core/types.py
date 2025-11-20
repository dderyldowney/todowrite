"""
ToDoWrite Core Type Definitions.

This module contains shared type definitions and utility classes used
throughout the ToDoWrite package.

Key Concepts:
- LayerType: The 12 hierarchical layers from Goal to Command
- StatusType: Workflow states for task tracking
- Metadata: Extensible metadata system
- Command: Executable command definitions

Example:
    >>> from todowrite.core.models import Goal
    >>> from todowrite.core.types import LayerType, Metadata
    >>>
    >>> goal = Goal(
    ...     title="Launch Product",
    ...     description="Successfully launch the new product",
    ...     owner="product-team",
    ...     severity="high"
    ... )
"""

from __future__ import annotations

from typing import Any, Literal

# Define the 12 hierarchical layers in the ToDoWrite system
LayerType = Literal[
    "Goal",
    "Concept",
    "Context",
    "Constraints",
    "Requirements",
    "AcceptanceCriteria",
    "InterfaceContract",
    "Phase",
    "Step",
    "Task",
    "SubTask",
    "Command",
]

# Define workflow status types
StatusType = Literal[
    "planned", "in_progress", "completed", "blocked", "cancelled"
]

# ToDoWrite Core Type Definitions
#
# This module contains shared type definitions and utility classes used
# throughout the ToDoWrite package.
#
# SQLAlchemy model classes are in todowrite.core.models
#
# Available exports:
__all__ = [
    "AcceptanceCriteriaCollection",
    "CommandCollection",
    "LayerType",
    "Metadata",
    "PhaseCollection",
    "StatusType",
    "StepCollection",
    "SubTaskCollection",
    "TaskCollection",
    "ToDoWriteCollection",
]


class Metadata:
    """Extensible metadata for ToDoWrite nodes."""

    def __init__(
        self,
        owner: str = "",
        labels: list[str] | None = None,
        severity: str = "",
        work_type: str = "",
        assignee: str = "",
        extra: dict[str, Any] | None = None,
    ) -> None:
        self.owner = owner
        self.labels = labels or []
        self.severity = severity
        self.work_type = work_type
        self.assignee = assignee
        self.extra = extra or {}

    def to_dict(self) -> dict[str, Any]:
        """Convert metadata to dictionary."""
        return {
            "owner": self.owner,
            "labels": self.labels,
            "severity": self.severity,
            "work_type": self.work_type,
            "assignee": self.assignee,
            **self.extra,
        }


class ToDoWriteCollection:
    """Base collection class for ToDoWrite models."""

    def __init__(self, items: list[Any] | None = None) -> None:
        self.items = items or []

    def all(self) -> list[Any]:
        """Get all items in the collection."""
        return self.items

    def size(self) -> int:
        """Get the size of the collection."""
        return len(self.items)

    def empty(self) -> bool:
        """Check if the collection is empty."""
        return len(self.items) == 0

    def exists(self) -> bool:
        """Check if any items exist in the collection."""
        return len(self.items) > 0


class PhaseCollection(ToDoWriteCollection):
    """Collection for Phase items."""

    pass


class TaskCollection(ToDoWriteCollection):
    """Collection for Task items."""

    pass


class AcceptanceCriteriaCollection(ToDoWriteCollection):
    """Collection for AcceptanceCriteria items."""

    pass


class StepCollection(ToDoWriteCollection):
    """Collection for Step items."""

    pass


class SubTaskCollection(ToDoWriteCollection):
    """Collection for SubTask items."""

    pass


class CommandCollection(ToDoWriteCollection):
    """Collection for Command items."""

    pass
