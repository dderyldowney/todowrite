"""
Context association tables.

This module contains association tables for context relationships.
"""

from __future__ import annotations

from sqlalchemy import (
    Column,
    ForeignKey,
    Integer,
    Table,
)

from todowrite.core.models.base import Base

# Goal < Context associations
goals_contexts = Table(
    "goals_contexts",  # Goal < Context (alphabetical)
    Base.metadata,
    Column("goal_id", Integer, ForeignKey("goals.id")),
    Column("context_id", Integer, ForeignKey("contexts.id")),
)
