"""
Concept association tables.

This module contains association tables for concept relationships.
"""

from __future__ import annotations

from sqlalchemy import (
    Column,
    ForeignKey,
    Integer,
    Table,
)

from todowrite.core.models.base import Base

# Goal < Concept associations
goals_concepts = Table(
    "goals_concepts",  # Goal < Concept (alphabetical)
    Base.metadata,
    Column("goal_id", Integer, ForeignKey("goals.id")),
    Column("concept_id", Integer, ForeignKey("concepts.id")),
)

# Concept < Context associations
concepts_contexts = Table(
    "concepts_contexts",  # Concept < Context (alphabetical)
    Base.metadata,
    Column("concept_id", Integer, ForeignKey("concepts.id")),
    Column("context_id", Integer, ForeignKey("contexts.id")),
)
