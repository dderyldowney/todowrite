"""
Goal and Constraints association tables.

This module contains association tables for goal and constraint relationships.
"""

from __future__ import annotations

from sqlalchemy import (
    Column,
    ForeignKey,
    Integer,
    Table,
)

from todowrite.core.models.base import Base

# Goal < Task associations
goals_tasks = Table(
    "goals_tasks",  # Goal < Task (alphabetical)
    Base.metadata,
    Column("goal_id", Integer, ForeignKey("goals.id")),
    Column("task_id", Integer, ForeignKey("tasks.id")),
)

# Goal < Phase associations
goals_phases = Table(
    "goals_phases",  # Goal < Phase (alphabetical)
    Base.metadata,
    Column("goal_id", Integer, ForeignKey("goals.id")),
    Column("phase_id", Integer, ForeignKey("phases.id")),
)

# Goal < Constraints associations
constraints_goals = Table(
    "constraints_goals",  # Constraint < Goal (alphabetical)
    Base.metadata,
    Column("constraint_id", Integer, ForeignKey("constraints.id")),
    Column("goal_id", Integer, ForeignKey("goals.id")),
)

# Constraints < Requirements associations
constraints_requirements = Table(
    "constraints_requirements",
    Base.metadata,
    Column("constraint_id", Integer, ForeignKey("constraints.id")),
    Column("requirement_id", Integer, ForeignKey("requirements.id")),
)
