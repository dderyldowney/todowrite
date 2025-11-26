"""
Label association tables.

This module contains association tables for label relationships.
"""

from __future__ import annotations

from sqlalchemy import (
    Column,
    ForeignKey,
    Integer,
    Table,
)

from todowrite.core.models.base import Base

# Goal < Label associations
goals_labels = Table(
    "goals_labels",  # Goal < Label (alphabetical)
    Base.metadata,
    Column("goal_id", Integer, ForeignKey("goals.id")),
    Column("label_id", Integer, ForeignKey("labels.id")),
)

# Concept < Label associations
concepts_labels = Table(
    "concepts_labels",  # Concept < Label (alphabetical)
    Base.metadata,
    Column("concept_id", Integer, ForeignKey("concepts.id")),
    Column("label_id", Integer, ForeignKey("labels.id")),
)

# Context < Label associations
contexts_labels = Table(
    "contexts_labels",  # Context < Label (alphabetical)
    Base.metadata,
    Column("context_id", Integer, ForeignKey("contexts.id")),
    Column("label_id", Integer, ForeignKey("labels.id")),
)

# Constraints < Label associations
constraints_labels = Table(
    "constraints_labels",  # Constraints < Label (alphabetical)
    Base.metadata,
    Column("constraint_id", Integer, ForeignKey("constraints.id")),
    Column("label_id", Integer, ForeignKey("labels.id")),
)

# Requirements < Label associations
requirements_labels = Table(
    "requirements_labels",  # Requirements < Label (alphabetical)
    Base.metadata,
    Column("requirement_id", Integer, ForeignKey("requirements.id")),
    Column("label_id", Integer, ForeignKey("labels.id")),
)

# AcceptanceCriteria < Label associations
acceptance_criteria_labels = Table(
    "acceptance_criteria_labels",  # AcceptanceCriteria < Label (alphabetical)
    Base.metadata,
    Column(
        "acceptance_criterion_id",
        Integer,
        ForeignKey("acceptance_criteria.id"),
    ),
    Column("label_id", Integer, ForeignKey("labels.id")),
)


# InterfaceContract < Label associations
interface_contracts_labels = Table(
    "interface_contracts_labels",  # InterfaceContract < Label (alphabetical)
    Base.metadata,
    Column(
        "interface_contract_id", Integer, ForeignKey("interface_contracts.id")
    ),
    Column("label_id", Integer, ForeignKey("labels.id")),
)

# Phase < Label associations
phases_labels = Table(
    "phases_labels",  # Phase < Label (alphabetical)
    Base.metadata,
    Column("phase_id", Integer, ForeignKey("phases.id")),
    Column("label_id", Integer, ForeignKey("labels.id")),
)

# Step < Label associations
steps_labels = Table(
    "steps_labels",  # Step < Label (alphabetical)
    Base.metadata,
    Column("step_id", Integer, ForeignKey("steps.id")),
    Column("label_id", Integer, ForeignKey("labels.id")),
)

# Task < Label associations
tasks_labels = Table(
    "tasks_labels",  # Task < Label (alphabetical)
    Base.metadata,
    Column("task_id", Integer, ForeignKey("tasks.id")),
    Column("label_id", Integer, ForeignKey("labels.id")),
)

# SubTask < Label associations
sub_tasks_labels = Table(
    "sub_tasks_labels",  # SubTask < Label (alphabetical)
    Base.metadata,
    Column("sub_task_id", Integer, ForeignKey("sub_tasks.id")),
    Column("label_id", Integer, ForeignKey("labels.id")),
)

# Command < Label associations
commands_labels = Table(
    "commands_labels",  # Command < Label (alphabetical)
    Base.metadata,
    Column("command_id", Integer, ForeignKey("commands.id")),
    Column("label_id", Integer, ForeignKey("labels.id")),
)
