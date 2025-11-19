"""
ToDoWrite Core Models.

This module contains the SQLAlchemy ORM models for the 12-layer hierarchical
task management system. These models implement proper SQLAlchemy ORM patterns
with comprehensive relationships and associations.

Key Models:
- Goal: High-level project objectives
- Concept: Abstract ideas and requirements
- Context: Background information and constraints
- Constraints: Technical and business constraints
- Requirements: Specific functional requirements
- AcceptanceCriteria: Definition of done criteria
- InterfaceContract: API and interface contracts
- Phase: Project phases and milestones
- Step: Individual steps within phases
- Task: Specific tasks with owners and status
- SubTask: Breakdown of tasks into smaller units
- Command: Executable commands and scripts
- Label: Tags and categorization system

Example:
    >>> from todowrite.core.models import Goal
    >>>
    >>> goal = Goal(
    ...     title="Launch Product",
    ...     description="Successfully launch the new product",
    ...     owner="product-team",
    ...     severity="high"
    ... )
"""

from __future__ import annotations

import json
from datetime import datetime
from typing import Any, Literal

from sqlalchemy import (
    Column,
    ForeignKey,
    Integer,
    String,
    Table,
    Text,
)
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column,
    relationship,
)


class Base(DeclarativeBase):
    """SQLAlchemy declarative base for all ToDoWrite models."""


# Join tables (lexical order, no primary keys)
goals_labels = Table(
    "goals_labels",  # Goal < Label (alphabetical)
    Base.metadata,
    Column("goal_id", Integer, ForeignKey("goals.id")),
    Column("label_id", Integer, ForeignKey("labels.id")),
)

concepts_labels = Table(
    "concepts_labels",  # Concept < Label (alphabetical)
    Base.metadata,
    Column("concept_id", Integer, ForeignKey("concepts.id")),
    Column("label_id", Integer, ForeignKey("labels.id")),
)

contexts_labels = Table(
    "contexts_labels",  # Context < Label (alphabetical)
    Base.metadata,
    Column("context_id", Integer, ForeignKey("contexts.id")),
    Column("label_id", Integer, ForeignKey("labels.id")),
)

goals_concepts = Table(
    "goals_concepts",  # Goal < Concept (alphabetical)
    Base.metadata,
    Column("goal_id", Integer, ForeignKey("goals.id")),
    Column("concept_id", Integer, ForeignKey("concepts.id")),
)

goals_contexts = Table(
    "goals_contexts",  # Goal < Context (alphabetical)
    Base.metadata,
    Column("goal_id", Integer, ForeignKey("goals.id")),
    Column("context_id", Integer, ForeignKey("contexts.id")),
)

concepts_contexts = Table(
    "concepts_contexts",  # Concept < Context (alphabetical)
    Base.metadata,
    Column("concept_id", Integer, ForeignKey("concepts.id")),
    Column("context_id", Integer, ForeignKey("contexts.id")),
)

requirements_concepts = Table(
    "requirements_concepts",  # Requirement < Concept (alphabetical)
    Base.metadata,
    Column("requirement_id", Integer, ForeignKey("requirements.id")),
    Column("concept_id", Integer, ForeignKey("concepts.id")),
)

requirements_contexts = Table(
    "requirements_contexts",  # Requirement < Context (alphabetical)
    Base.metadata,
    Column("requirement_id", Integer, ForeignKey("requirements.id")),
    Column("context_id", Integer, ForeignKey("contexts.id")),
)

constraints_labels = Table(
    "constraints_labels",  # Constraints < Label (alphabetical)
    Base.metadata,
    Column("constraint_id", Integer, ForeignKey("constraints.id")),
    Column("label_id", Integer, ForeignKey("labels.id")),
)

requirements_labels = Table(
    "requirements_labels",  # Requirements < Label (alphabetical)
    Base.metadata,
    Column("requirement_id", Integer, ForeignKey("requirements.id")),
    Column("label_id", Integer, ForeignKey("labels.id")),
)

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

interface_contracts_labels = Table(
    "interface_contracts_labels",  # InterfaceContract < Label (alphabetical)
    Base.metadata,
    Column(
        "interface_contract_id", Integer, ForeignKey("interface_contracts.id")
    ),
    Column("label_id", Integer, ForeignKey("labels.id")),
)

phases_labels = Table(
    "phases_labels",  # Phase < Label (alphabetical)
    Base.metadata,
    Column("phase_id", Integer, ForeignKey("phases.id")),
    Column("label_id", Integer, ForeignKey("labels.id")),
)

steps_labels = Table(
    "steps_labels",  # Step < Label (alphabetical)
    Base.metadata,
    Column("step_id", Integer, ForeignKey("steps.id")),
    Column("label_id", Integer, ForeignKey("labels.id")),
)

tasks_labels = Table(
    "tasks_labels",  # Task < Label (alphabetical)
    Base.metadata,
    Column("task_id", Integer, ForeignKey("tasks.id")),
    Column("label_id", Integer, ForeignKey("labels.id")),
)

sub_tasks_labels = Table(
    "sub_tasks_labels",  # SubTask < Label (alphabetical)
    Base.metadata,
    Column("sub_task_id", Integer, ForeignKey("sub_tasks.id")),
    Column("label_id", Integer, ForeignKey("labels.id")),
)

commands_labels = Table(
    "commands_labels",  # Command < Label (alphabetical)
    Base.metadata,
    Column("command_id", Integer, ForeignKey("commands.id")),
    Column("label_id", Integer, ForeignKey("labels.id")),
)

# Layer association tables (proper ToDoWrite Models style)
# Goal + Constraints = constraints_goals (alphabetical)
constraints_goals = Table(
    "constraints_goals",
    Base.metadata,
    Column("goal_id", Integer, ForeignKey("goals.id")),
    Column("constraint_id", Integer, ForeignKey("constraints.id")),
)

# Constraints + Requirements = constraints_requirements
constraints_requirements = Table(
    "constraints_requirements",
    Base.metadata,
    Column("constraint_id", Integer, ForeignKey("constraints.id")),
    Column("requirement_id", Integer, ForeignKey("requirements.id")),
)

# Requirements + AcceptanceCriteria = requirements_acceptance_criteria
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

# InterfaceContract + Phase = interface_contracts_phases
interface_contracts_phases = Table(
    "interface_contracts_phases",
    Base.metadata,
    Column(
        "interface_contract_id", Integer, ForeignKey("interface_contracts.id")
    ),
    Column("phase_id", Integer, ForeignKey("phases.id")),
)

# Hierarchical associations (following association patterns)
# Goal has many Tasks, Tasks belong to Goal
goals_tasks = Table(
    "goals_tasks",  # Goal < Task (alphabetical)
    Base.metadata,
    Column("goal_id", Integer, ForeignKey("goals.id")),
    Column("task_id", Integer, ForeignKey("tasks.id")),
)

# Goal has many Phases, Phases belong to Goal
goals_phases = Table(
    "goals_phases",  # Goal < Phase (alphabetical)
    Base.metadata,
    Column("goal_id", Integer, ForeignKey("goals.id")),
    Column("phase_id", Integer, ForeignKey("phases.id")),
)

# Phase has many Steps, Steps belong to Phase
phases_steps = Table(
    "phases_steps",  # Phase < Step (alphabetical)
    Base.metadata,
    Column("phase_id", Integer, ForeignKey("phases.id")),
    Column("step_id", Integer, ForeignKey("steps.id")),
)

# Step has many Tasks, Tasks belong to Step (additional to Goal->Task)
steps_tasks = Table(
    "steps_tasks",  # Step < Task (alphabetical)
    Base.metadata,
    Column("step_id", Integer, ForeignKey("steps.id")),
    Column("task_id", Integer, ForeignKey("tasks.id")),
)

# Task has many SubTasks, SubTasks belong to Task
tasks_sub_tasks = Table(
    "tasks_sub_tasks",  # Task < SubTask (alphabetical)
    Base.metadata,
    Column("task_id", Integer, ForeignKey("tasks.id")),
    Column("sub_task_id", Integer, ForeignKey("sub_tasks.id")),
)

# SubTask has many Commands, Commands belong to SubTask
sub_tasks_commands = Table(
    "sub_tasks_commands",  # SubTask < Command (alphabetical)
    Base.metadata,
    Column("sub_task_id", Integer, ForeignKey("sub_tasks.id")),
    Column("command_id", Integer, ForeignKey("commands.id")),
)


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

StatusType = Literal[
    "planned", "in_progress", "completed", "blocked", "cancelled"
]


class Goal(Base):
    """ToDoWrite Goal model for hierarchical task management."""

    __tablename__ = "goals"

    # Primary key (Integer for SQLite autoincrement compatibility)
    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True, nullable=False
    )

    # Model fields
    title: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str | None] = mapped_column(Text)
    status: Mapped[str] = mapped_column(String, default="planned")
    progress: Mapped[int | None] = mapped_column(Integer)
    started_date: Mapped[str | None] = mapped_column(String)
    completion_date: Mapped[str | None] = mapped_column(String)

    # Metadata fields (flattened for now, could be separate table)
    owner: Mapped[str | None] = mapped_column(String)
    severity: Mapped[str | None] = mapped_column(String)
    work_type: Mapped[str | None] = mapped_column(String)
    assignee: Mapped[str | None] = mapped_column(String)

    # JSON fields for complex data
    extra_data: Mapped[str | None] = mapped_column(Text)  # JSON string

    # Timestamps: created_at readonly, updated_at updates on save
    # created_at: Set once on creation, never changes (readonly)
    created_at: Mapped[str] = mapped_column(
        String, default=lambda: datetime.now().isoformat(), nullable=False
    )

    # updated_at: Updates on every save (writable)
    updated_at: Mapped[str] = mapped_column(
        String,
        default=lambda: datetime.now().isoformat(),
        nullable=False,
        onupdate=lambda: datetime.now().isoformat(),
    )

    # Relationships (bidirectional with back_populates)
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
    constraints: Mapped[list[Constraints]] = relationship(
        "Constraints", secondary=constraints_goals, back_populates="goals"
    )

    # has_many :concepts (through goals_concepts)
    concepts: Mapped[list[Concept]] = relationship(
        "Concept", secondary=goals_concepts, back_populates="goals"
    )

    # has_many :contexts (direct relationship - "why defining this goal")
    contexts: Mapped[list[Context]] = relationship(
        "Context", secondary=goals_contexts, back_populates="goals"
    )


class Concept(Base):
    """ToDoWrite Concept model for hierarchical task management."""

    __tablename__ = "concepts"

    # Primary key (Integer for SQLite autoincrement compatibility)
    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True, nullable=False
    )

    # Model fields
    title: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str | None] = mapped_column(Text)
    status: Mapped[str] = mapped_column(String, default="planned")
    progress: Mapped[int | None] = mapped_column(Integer)
    started_date: Mapped[str | None] = mapped_column(String)
    completion_date: Mapped[str | None] = mapped_column(String)

    # Metadata fields (flattened for now, could be separate table)
    owner: Mapped[str | None] = mapped_column(String)
    severity: Mapped[str | None] = mapped_column(String)
    work_type: Mapped[str | None] = mapped_column(String)
    assignee: Mapped[str | None] = mapped_column(String)

    # JSON fields for complex data
    extra_data: Mapped[str | None] = mapped_column(Text)  # JSON string

    # Timestamp conventions - created_at readonly, updated_at writable
    created_at: Mapped[str] = mapped_column(
        String, default=lambda: datetime.now().isoformat(), nullable=False
    )
    updated_at: Mapped[str] = mapped_column(
        String,
        default=lambda: datetime.now().isoformat(),
        nullable=False,
        onupdate=lambda: datetime.now().isoformat(),
    )

    # Relationships
    labels: Mapped[list[Label]] = relationship(
        "Label", secondary=concepts_labels, back_populates="concepts"
    )

    # belongs_to :goals (through goals_concepts)
    goals: Mapped[list[Goal]] = relationship(
        "Goal", secondary=goals_concepts, back_populates="concepts"
    )

    # has_many :contexts (direct relationship - "conceptually building")
    contexts: Mapped[list[Context]] = relationship(
        "Context", secondary=concepts_contexts, back_populates="concepts"
    )

    # belongs_to :requirements (through requirements_concepts)
    requirements: Mapped[list[Requirements]] = relationship(
        "Requirements",
        secondary=requirements_concepts,
        back_populates="concepts",
    )


class Context(Base):
    """ToDoWrite Context model for hierarchical task management."""

    __tablename__ = "contexts"

    # Primary key convention
    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True, nullable=False
    )

    # Model fields
    title: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str | None] = mapped_column(Text)
    status: Mapped[str] = mapped_column(String, default="planned")
    progress: Mapped[int | None] = mapped_column(Integer)
    started_date: Mapped[str | None] = mapped_column(String)
    completion_date: Mapped[str | None] = mapped_column(String)

    # Metadata fields
    owner: Mapped[str | None] = mapped_column(String)
    severity: Mapped[str | None] = mapped_column(String)
    work_type: Mapped[str | None] = mapped_column(String)
    assignee: Mapped[str | None] = mapped_column(String)

    # JSON fields for complex data
    extra_data: Mapped[str | None] = mapped_column(Text)

    # Timestamp conventions
    created_at: Mapped[str] = mapped_column(
        String, default=lambda: datetime.now().isoformat(), nullable=False
    )
    updated_at: Mapped[str] = mapped_column(
        String,
        default=lambda: datetime.now().isoformat(),
        nullable=False,
        onupdate=lambda: datetime.now().isoformat(),
    )

    # Relationships
    labels: Mapped[list[Label]] = relationship(
        "Label", secondary=contexts_labels, back_populates="contexts"
    )

    # belongs_to :concepts (through concepts_contexts)
    concepts: Mapped[list[Concept]] = relationship(
        "Concept", secondary=concepts_contexts, back_populates="contexts"
    )

    # belongs_to :goals (through goals_contexts)
    goals: Mapped[list[Goal]] = relationship(
        "Goal", secondary=goals_contexts, back_populates="contexts"
    )

    # belongs_to :requirements (through requirements_contexts)
    requirements: Mapped[list[Requirements]] = relationship(
        "Requirements",
        secondary=requirements_contexts,
        back_populates="contexts",
    )


class Constraints(Base):
    """ToDoWrite Constraints model for hierarchical task management."""

    __tablename__ = "constraints"

    # Primary key convention
    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True, nullable=False
    )

    # Model fields
    title: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str | None] = mapped_column(Text)
    status: Mapped[str] = mapped_column(String, default="planned")
    progress: Mapped[int | None] = mapped_column(Integer)
    started_date: Mapped[str | None] = mapped_column(String)
    completion_date: Mapped[str | None] = mapped_column(String)

    # Metadata fields
    owner: Mapped[str | None] = mapped_column(String)
    severity: Mapped[str | None] = mapped_column(String)
    work_type: Mapped[str | None] = mapped_column(String)
    assignee: Mapped[str | None] = mapped_column(String)

    # JSON fields for complex data
    extra_data: Mapped[str | None] = mapped_column(Text)

    # Timestamp conventions
    created_at: Mapped[str] = mapped_column(
        String, default=lambda: datetime.now().isoformat(), nullable=False
    )
    updated_at: Mapped[str] = mapped_column(
        String,
        default=lambda: datetime.now().isoformat(),
        nullable=False,
        onupdate=lambda: datetime.now().isoformat(),
    )

    # Relationships
    labels: Mapped[list[Label]] = relationship(
        "Label", secondary=constraints_labels, back_populates="constraints"
    )

    # belongs_to :goals (through constraints_goals)
    goals: Mapped[list[Goal]] = relationship(
        "Goal", secondary=constraints_goals, back_populates="constraints"
    )

    # has_many :requirements (through constraints_requirements)
    requirements: Mapped[list[Requirements]] = relationship(
        "Requirements",
        secondary=constraints_requirements,
        back_populates="constraints",
    )


class Requirements(Base):
    """ToDoWrite Requirements model for hierarchical task management."""

    __tablename__ = "requirements"

    # Primary key convention
    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True, nullable=False
    )

    # Model fields
    title: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str | None] = mapped_column(Text)
    status: Mapped[str] = mapped_column(String, default="planned")
    progress: Mapped[int | None] = mapped_column(Integer)
    started_date: Mapped[str | None] = mapped_column(String)
    completion_date: Mapped[str | None] = mapped_column(String)

    # Metadata fields
    owner: Mapped[str | None] = mapped_column(String)
    severity: Mapped[str | None] = mapped_column(String)
    work_type: Mapped[str | None] = mapped_column(String)
    assignee: Mapped[str | None] = mapped_column(String)

    # JSON fields for complex data
    extra_data: Mapped[str | None] = mapped_column(Text)

    # Timestamp conventions
    created_at: Mapped[str] = mapped_column(
        String, default=lambda: datetime.now().isoformat(), nullable=False
    )
    updated_at: Mapped[str] = mapped_column(
        String,
        default=lambda: datetime.now().isoformat(),
        nullable=False,
        onupdate=lambda: datetime.now().isoformat(),
    )

    # Relationships
    labels: Mapped[list[Label]] = relationship(
        "Label", secondary=requirements_labels, back_populates="requirements"
    )

    # belongs_to :constraints (through constraints_requirements)
    constraints: Mapped[list[Constraints]] = relationship(
        "Constraints",
        secondary=constraints_requirements,
        back_populates="requirements",
    )

    # has_many :acceptance_criteria (through requirements_acceptance_criteria)
    acceptance_criteria: Mapped[list[AcceptanceCriteria]] = relationship(
        "AcceptanceCriteria",
        secondary=requirements_acceptance_criteria,
        back_populates="requirements",
    )

    # has_many :concepts (through requirements_concepts)
    concepts: Mapped[list[Concept]] = relationship(
        "Concept",
        secondary=requirements_concepts,
        back_populates="requirements",
    )

    # has_many :contexts (direct relationship - "context for requirement")
    contexts: Mapped[list[Context]] = relationship(
        "Context",
        secondary=requirements_contexts,
        back_populates="requirements",
    )


class AcceptanceCriteria(Base):
    """ToDoWrite AcceptanceCriteria model for hierarchical task management."""

    __tablename__ = "acceptance_criteria"

    # Primary key convention
    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True, nullable=False
    )

    # Model fields
    title: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str | None] = mapped_column(Text)
    status: Mapped[str] = mapped_column(String, default="planned")
    progress: Mapped[int | None] = mapped_column(Integer)
    started_date: Mapped[str | None] = mapped_column(String)
    completion_date: Mapped[str | None] = mapped_column(String)

    # Metadata fields
    owner: Mapped[str | None] = mapped_column(String)
    severity: Mapped[str | None] = mapped_column(String)
    work_type: Mapped[str | None] = mapped_column(String)
    assignee: Mapped[str | None] = mapped_column(String)

    # JSON fields for complex data
    extra_data: Mapped[str | None] = mapped_column(Text)

    # Timestamp conventions
    created_at: Mapped[str] = mapped_column(
        String, default=lambda: datetime.now().isoformat(), nullable=False
    )
    updated_at: Mapped[str] = mapped_column(
        String,
        default=lambda: datetime.now().isoformat(),
        nullable=False,
        onupdate=lambda: datetime.now().isoformat(),
    )

    # Relationships
    labels: Mapped[list[Label]] = relationship(
        "Label",
        secondary=acceptance_criteria_labels,
        back_populates="acceptance_criteria",
    )

    # belongs_to :requirements (through requirements_acceptance_criteria)
    requirements: Mapped[list[Requirements]] = relationship(
        "Requirements",
        secondary=requirements_acceptance_criteria,
        back_populates="acceptance_criteria",
    )

    # has_many :interface_contracts (through association table)
    interface_contracts: Mapped[list[InterfaceContract]] = relationship(
        "InterfaceContract",
        secondary=acceptance_criteria_interface_contracts,
        back_populates="acceptance_criteria",
    )


class InterfaceContract(Base):
    """ToDoWrite InterfaceContract model for hierarchical task management."""

    __tablename__ = "interface_contracts"

    # Primary key convention
    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True, nullable=False
    )

    # Model fields
    title: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str | None] = mapped_column(Text)
    status: Mapped[str] = mapped_column(String, default="planned")
    progress: Mapped[int | None] = mapped_column(Integer)
    started_date: Mapped[str | None] = mapped_column(String)
    completion_date: Mapped[str | None] = mapped_column(String)

    # Metadata fields
    owner: Mapped[str | None] = mapped_column(String)
    severity: Mapped[str | None] = mapped_column(String)
    work_type: Mapped[str | None] = mapped_column(String)
    assignee: Mapped[str | None] = mapped_column(String)

    # JSON fields for complex data
    extra_data: Mapped[str | None] = mapped_column(Text)

    # Timestamp conventions
    created_at: Mapped[str] = mapped_column(
        String, default=lambda: datetime.now().isoformat(), nullable=False
    )
    updated_at: Mapped[str] = mapped_column(
        String,
        default=lambda: datetime.now().isoformat(),
        nullable=False,
        onupdate=lambda: datetime.now().isoformat(),
    )

    # Relationships
    labels: Mapped[list[Label]] = relationship(
        "Label",
        secondary=interface_contracts_labels,
        back_populates="interface_contracts",
    )

    # belongs_to :acceptance_criteria (through association table)
    acceptance_criteria: Mapped[list[AcceptanceCriteria]] = relationship(
        "AcceptanceCriteria",
        secondary=acceptance_criteria_interface_contracts,
        back_populates="interface_contracts",
    )

    # has_many :phases (through interface_contracts_phases)
    phases: Mapped[list[Phase]] = relationship(
        "Phase",
        secondary=interface_contracts_phases,
        back_populates="interface_contracts",
    )


class Phase(Base):
    """ToDoWrite Phase model for hierarchical task management."""

    __tablename__ = "phases"

    # Primary key convention
    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True, nullable=False
    )

    # Model fields
    title: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str | None] = mapped_column(Text)
    status: Mapped[str] = mapped_column(String, default="planned")
    progress: Mapped[int | None] = mapped_column(Integer)
    started_date: Mapped[str | None] = mapped_column(String)
    completion_date: Mapped[str | None] = mapped_column(String)

    # Metadata fields
    owner: Mapped[str | None] = mapped_column(String)
    severity: Mapped[str | None] = mapped_column(String)
    work_type: Mapped[str | None] = mapped_column(String)
    assignee: Mapped[str | None] = mapped_column(String)

    # JSON fields for complex data
    extra_data: Mapped[str | None] = mapped_column(Text)

    # Timestamp conventions
    created_at: Mapped[str] = mapped_column(
        String, default=lambda: datetime.now().isoformat(), nullable=False
    )
    updated_at: Mapped[str] = mapped_column(
        String,
        default=lambda: datetime.now().isoformat(),
        nullable=False,
        onupdate=lambda: datetime.now().isoformat(),
    )

    # Relationships
    labels: Mapped[list[Label]] = relationship(
        "Label", secondary=phases_labels, back_populates="phases"
    )

    # belongs_to :goals (through goals_phases)
    goals: Mapped[list[Goal]] = relationship(
        "Goal", secondary=goals_phases, back_populates="phases"
    )

    # has_many :steps (through phases_steps)
    steps: Mapped[list[Step]] = relationship(
        "Step", secondary=phases_steps, back_populates="phases"
    )

    # belongs_to :interface_contracts (through interface_contracts_phases)
    interface_contracts: Mapped[list[InterfaceContract]] = relationship(
        "InterfaceContract",
        secondary=interface_contracts_phases,
        back_populates="phases",
    )


class Step(Base):
    """ToDoWrite Step model for hierarchical task management."""

    __tablename__ = "steps"

    # Primary key convention
    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True, nullable=False
    )

    # Model fields
    title: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str | None] = mapped_column(Text)
    status: Mapped[str] = mapped_column(String, default="planned")
    progress: Mapped[int | None] = mapped_column(Integer)
    started_date: Mapped[str | None] = mapped_column(String)
    completion_date: Mapped[str | None] = mapped_column(String)

    # Metadata fields
    owner: Mapped[str | None] = mapped_column(String)
    severity: Mapped[str | None] = mapped_column(String)
    work_type: Mapped[str | None] = mapped_column(String)
    assignee: Mapped[str | None] = mapped_column(String)

    # JSON fields for complex data
    extra_data: Mapped[str | None] = mapped_column(Text)

    # Timestamp conventions
    created_at: Mapped[str] = mapped_column(
        String, default=lambda: datetime.now().isoformat(), nullable=False
    )
    updated_at: Mapped[str] = mapped_column(
        String,
        default=lambda: datetime.now().isoformat(),
        nullable=False,
        onupdate=lambda: datetime.now().isoformat(),
    )

    # Relationships
    labels: Mapped[list[Label]] = relationship(
        "Label", secondary=steps_labels, back_populates="steps"
    )

    # belongs_to :phases (through phases_steps)
    phases: Mapped[list[Phase]] = relationship(
        "Phase", secondary=phases_steps, back_populates="steps"
    )

    # has_many :tasks (through steps_tasks)
    tasks: Mapped[list[Task]] = relationship(
        "Task", secondary=steps_tasks, back_populates="steps"
    )


class Task(Base):
    """ToDoWrite Task model for hierarchical task management."""

    __tablename__ = "tasks"

    # Primary key convention
    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True, nullable=False
    )

    # Model fields
    title: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str | None] = mapped_column(Text)
    status: Mapped[str] = mapped_column(String, default="planned")
    progress: Mapped[int | None] = mapped_column(Integer)
    started_date: Mapped[str | None] = mapped_column(String)
    completion_date: Mapped[str | None] = mapped_column(String)

    # Metadata fields
    owner: Mapped[str | None] = mapped_column(String)
    severity: Mapped[str | None] = mapped_column(String)
    work_type: Mapped[str | None] = mapped_column(String)
    assignee: Mapped[str | None] = mapped_column(String)

    # JSON fields for complex data
    extra_data: Mapped[str | None] = mapped_column(Text)

    # Timestamp conventions
    created_at: Mapped[str] = mapped_column(
        String, default=lambda: datetime.now().isoformat(), nullable=False
    )
    updated_at: Mapped[str] = mapped_column(
        String,
        default=lambda: datetime.now().isoformat(),
        nullable=False,
        onupdate=lambda: datetime.now().isoformat(),
    )

    # Relationships
    labels: Mapped[list[Label]] = relationship(
        "Label", secondary=tasks_labels, back_populates="tasks"
    )

    # belongs_to :goals (through goals_tasks)
    goals: Mapped[list[Goal]] = relationship(
        "Goal", secondary=goals_tasks, back_populates="tasks"
    )

    # belongs_to :steps (through steps_tasks) - Task can belong to a Step
    steps: Mapped[list[Step]] = relationship(
        "Step", secondary=steps_tasks, back_populates="tasks"
    )

    # has_many :sub_tasks (through tasks_sub_tasks)
    sub_tasks: Mapped[list[SubTask]] = relationship(
        "SubTask", secondary=tasks_sub_tasks, back_populates="tasks"
    )


class SubTask(Base):
    """ToDoWrite SubTask model for hierarchical task management."""

    __tablename__ = "sub_tasks"

    # Primary key convention
    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True, nullable=False
    )

    # Model fields
    title: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str | None] = mapped_column(Text)
    status: Mapped[str] = mapped_column(String, default="planned")
    progress: Mapped[int | None] = mapped_column(Integer)
    started_date: Mapped[str | None] = mapped_column(String)
    completion_date: Mapped[str | None] = mapped_column(String)

    # Metadata fields
    owner: Mapped[str | None] = mapped_column(String)
    severity: Mapped[str | None] = mapped_column(String)
    work_type: Mapped[str | None] = mapped_column(String)
    assignee: Mapped[str | None] = mapped_column(String)

    # JSON fields for complex data
    extra_data: Mapped[str | None] = mapped_column(Text)

    # Timestamp conventions
    created_at: Mapped[str] = mapped_column(
        String, default=lambda: datetime.now().isoformat(), nullable=False
    )
    updated_at: Mapped[str] = mapped_column(
        String,
        default=lambda: datetime.now().isoformat(),
        nullable=False,
        onupdate=lambda: datetime.now().isoformat(),
    )

    # Relationships
    labels: Mapped[list[Label]] = relationship(
        "Label", secondary=sub_tasks_labels, back_populates="sub_tasks"
    )

    # belongs_to :tasks (through tasks_sub_tasks)
    tasks: Mapped[list[Task]] = relationship(
        "Task", secondary=tasks_sub_tasks, back_populates="sub_tasks"
    )

    # has_many :commands (through sub_tasks_commands)
    commands: Mapped[list[Command]] = relationship(
        "Command", secondary=sub_tasks_commands, back_populates="sub_tasks"
    )


class Label(Base):
    """Represents a label that can be attached to goals and other models."""

    __tablename__ = "labels"

    # Primary key (Integer for SQLite autoincrement compatibility)
    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True, nullable=False
    )

    # Model field (unique label name)
    name: Mapped[str] = mapped_column(
        String, nullable=False, unique=True
    )  # Uses 'name', not 'label'

    # Timestamp conventions - created_at readonly, updated_at writable
    created_at: Mapped[str] = mapped_column(
        String, default=lambda: datetime.now().isoformat(), nullable=False
    )
    updated_at: Mapped[str] = mapped_column(
        String,
        default=lambda: datetime.now().isoformat(),
        nullable=False,
        onupdate=lambda: datetime.now().isoformat(),
    )

    # Relationships (bidirectional with back_populates)
    goals: Mapped[list[Goal]] = relationship(
        "Goal", secondary=goals_labels, back_populates="labels"
    )
    concepts: Mapped[list[Concept]] = relationship(
        "Concept", secondary=concepts_labels, back_populates="labels"
    )
    contexts: Mapped[list[Context]] = relationship(
        "Context", secondary=contexts_labels, back_populates="labels"
    )
    constraints: Mapped[list[Constraints]] = relationship(
        "Constraints", secondary=constraints_labels, back_populates="labels"
    )
    requirements: Mapped[list[Requirements]] = relationship(
        "Requirements", secondary=requirements_labels, back_populates="labels"
    )
    acceptance_criteria: Mapped[list[AcceptanceCriteria]] = relationship(
        "AcceptanceCriteria",
        secondary=acceptance_criteria_labels,
        back_populates="labels",
    )
    interface_contracts: Mapped[list[InterfaceContract]] = relationship(
        "InterfaceContract",
        secondary=interface_contracts_labels,
        back_populates="labels",
    )
    phases: Mapped[list[Phase]] = relationship(
        "Phase", secondary=phases_labels, back_populates="labels"
    )
    steps: Mapped[list[Step]] = relationship(
        "Step", secondary=steps_labels, back_populates="labels"
    )
    tasks: Mapped[list[Task]] = relationship(
        "Task", secondary=tasks_labels, back_populates="labels"
    )
    sub_tasks: Mapped[list[SubTask]] = relationship(
        "SubTask", secondary=sub_tasks_labels, back_populates="labels"
    )
    commands: Mapped[list[Command]] = relationship(
        "Command", secondary=commands_labels, back_populates="labels"
    )


class Command(Base):
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
    started_date: Mapped[str | None] = mapped_column(String)
    completion_date: Mapped[str | None] = mapped_column(String)

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

    # Timestamp conventions
    created_at: Mapped[str] = mapped_column(
        String, default=lambda: datetime.now().isoformat(), nullable=False
    )
    updated_at: Mapped[str] = mapped_column(
        String,
        default=lambda: datetime.now().isoformat(),
        nullable=False,
        onupdate=lambda: datetime.now().isoformat(),
    )

    # Relationships
    labels: Mapped[list[Label]] = relationship(
        "Label", secondary=commands_labels, back_populates="commands"
    )

    # belongs_to :sub_tasks (through sub_tasks_commands)
    sub_tasks: Mapped[list[SubTask]] = relationship(
        "SubTask", secondary=sub_tasks_commands, back_populates="commands"
    )

    @property
    def runtime_env_dict(self) -> dict[str, Any]:
        """Get runtime environment as dictionary."""
        return json.loads(self.runtime_env) if self.runtime_env else {}

    @runtime_env_dict.setter
    def runtime_env_dict(self, value: dict[str, Any]) -> None:
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
