"""
Requirements and AcceptanceCriteria association tables.

This module contains all associations for requirements and acceptance criteria relationships.
"""

from __future__ import annotations

from sqlalchemy import (
    Column,
    ForeignKey,
    Integer,
    Table,
)

from todowrite.core.models.base import Base

# Requirement < Concept associations
requirements_concepts = Table(
    "requirements_concepts",  # Requirement < Concept (alphabetical)
    Base.metadata,
    Column("requirement_id", Integer, ForeignKey("requirements.id")),
    Column("concept_id", Integer, ForeignKey("concepts.id")),
)


# Requirement < Context associations
requirements_contexts = Table(
    "requirements_contexts",  # Requirement < Context (alphabetical)
    Base.metadata,
    Column("requirement_id", Integer, ForeignKey("requirements.id")),
    Column("context_id", Integer, ForeignKey("contexts.id")),
)

# Requirement < AcceptanceCriteria associations
requirements_acceptance_criteria = Table(
    "requirements_acceptance_criteria",
    Base.metadata,
    Column("requirement_id", Integer, ForeignKey("requirements.id")),
    Column(
        "acceptance_criterion_id",
        Integer,
        ForeignKey("acceptance_criteria.id"),
    ),
)


# AcceptanceCriteria + InterfaceContract association table
acceptance_criteria_interface_contracts = Table(
    "acceptance_criteria_interface_contracts",
    Base.metadata,
    Column(
        "acceptance_criterion_id",
        Integer,
        ForeignKey("acceptance_criteria.id"),
    ),
    Column(
        "interface_contract_id", Integer, ForeignKey("interface_contracts.id")
    ),
)
