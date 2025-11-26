"""
Metadata utility class.

This module contains the Metadata utility class for extensible metadata.
"""

from __future__ import annotations


class Metadata:
    """Extensible metadata for ToDoWrite nodes."""

    def __init__(
        self,
        owner: str = "",
        labels: list[str] | None = None,
        severity: str = "",
        work_type: str = "",
        assignee: str = "",
        extra: dict[str, str | int | bool] | None = None,
    ) -> None:
        self.owner = owner
        self.labels = labels or []
        self.severity = severity
        self.work_type = work_type
        self.assignee = assignee
        self.extra = extra or {}

    def to_dict(self) -> dict[str, str | list[str] | int | bool]:
        """Convert metadata to dictionary."""
        return {
            "owner": self.owner,
            "labels": self.labels,
            "severity": self.severity,
            "work_type": self.work_type,
            "assignee": self.assignee,
            **self.extra,
        }
