"""
Step association tables.

This module contains association tables for step relationships.
"""

from __future__ import annotations

from sqlalchemy import (
    Column,
    ForeignKey,
    Integer,
    Table,
)

from todowrite.core.models.base import Base

# Step < Task associations
steps_tasks = Table(
    "steps_tasks",  # Step < Task (alphabetical)
    Base.metadata,
    Column("step_id", Integer, ForeignKey("steps.id")),
    Column("task_id", Integer, ForeignKey("tasks.id")),
)
