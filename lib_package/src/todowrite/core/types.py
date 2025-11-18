"""
ToDoWrite Core Type Definitions.

This module contains shared type definitions and data structures used
throughout the ToDoWrite package. It defines the fundamental types for the
12-layer hierarchical task management system.

Key Concepts:
- LayerType: The 12 hierarchical layers from Goal to Command
- StatusType: Workflow states for task tracking
- Node: Core data structure for all task items (NOW WITH RAILS-STYLE
         ACTIVE RECORD)
- Metadata: Extensible metadata system
- Links: Hierarchical relationships between nodes
- Command: Executable command definitions

Example:
    >>> from todowrite.core.types import Node, LayerType, Metadata
    >>>
    >>> node = Node(
    ...     id="GOAL-001",
    ...     layer="Goal",
    ...     title="Launch Product",
    ...     description="Successfully launch the new product",
    ...     metadata=Metadata(owner="product-team", severity="high")
    ... )
"""

from __future__ import annotations

import json
from datetime import datetime
from typing import TYPE_CHECKING, Any, Literal, TypedDict

from sqlalchemy import (
    BigInteger,
    Column,
    ForeignKey,
    Integer,
    String,
    Table,
    Text,
    and_,
    event,
    exists,
    func,
    select,
)
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    Session,
    joinedload,
    mapped_column,
    relationship,
)

if TYPE_CHECKING:
    from sqlalchemy.orm.interfaces import SessionState


class Base(DeclarativeBase):
    """SQLAlchemy declarative base for all ToDoWrite models."""


# Association tables for many-to-many relationships (Rails-style naming)
# Rails naming convention: lexical order of class names
node_labels = Table(
    "labels_nodes",  # Node + Label (alphabetical)
    Base.metadata,
    Column("node_id", BigInteger, ForeignKey("nodes.id"), primary_key=True),
    Column("label_id", BigInteger, ForeignKey("labels.id"), primary_key=True),
)

# Rails-style join tables (lexical order, no primary keys)
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

# Goal + Constraints = constraints_goals (alphabetical)
constraints_goals = Table(
    "constraints_goals",
    Base.metadata,
    Column("goal_id", String, ForeignKey("nodes.id"), primary_key=True),
    Column("constraint_id", String, ForeignKey("nodes.id"), primary_key=True),
)

# Constraints + Requirements = constraints_requirements
constraints_requirements = Table(
    "constraints_requirements",
    Base.metadata,
    Column("constraint_id", String, ForeignKey("nodes.id"), primary_key=True),
    Column("requirement_id", String, ForeignKey("nodes.id"), primary_key=True),
)

# Requirements + AcceptanceCriteria = requirements_acceptance_criteria
requirements_acceptance_criteria = Table(
    "requirements_acceptance_criteria",
    Base.metadata,
    Column("requirement_id", String, ForeignKey("nodes.id"), primary_key=True),
    Column(
        "acceptance_criterion_id",
        String,
        ForeignKey("nodes.id"),
        primary_key=True,
    ),
)

# AcceptanceCriteria + InterfaceContract =
# acceptance_criteria_interface_contracts
acceptance_criteria_interface_contracts = Table(
    "acceptance_criteria_interface_contracts",
    Base.metadata,
    Column(
        "acceptance_criterion_id",
        String,
        ForeignKey("nodes.id"),
        primary_key=True,
    ),
    Column(
        "interface_contract_id",
        String,
        ForeignKey("nodes.id"),
        primary_key=True,
    ),
)

# InterfaceContract + Phase = interface_contracts_phases
interface_contracts_phases = Table(
    "interface_contracts_phases",
    Base.metadata,
    Column(
        "interface_contract_id",
        String,
        ForeignKey("nodes.id"),
        primary_key=True,
    ),
    Column("phase_id", String, ForeignKey("nodes.id"), primary_key=True),
)

# Phase + Step = phases_steps
phases_steps = Table(
    "phases_steps",
    Base.metadata,
    Column("phase_id", String, ForeignKey("nodes.id"), primary_key=True),
    Column("step_id", String, ForeignKey("nodes.id"), primary_key=True),
)

# Step + Task = steps_tasks
steps_tasks = Table(
    "steps_tasks",
    Base.metadata,
    Column("step_id", String, ForeignKey("nodes.id"), primary_key=True),
    Column("task_id", String, ForeignKey("nodes.id"), primary_key=True),
)

# Task + SubTask = tasks_sub_tasks
tasks_sub_tasks = Table(
    "tasks_sub_tasks",
    Base.metadata,
    Column("task_id", String, ForeignKey("nodes.id"), primary_key=True),
    Column("sub_task_id", String, ForeignKey("nodes.id"), primary_key=True),
)

# SubTask + Command = sub_tasks_commands
sub_tasks_commands = Table(
    "sub_tasks_commands",
    Base.metadata,
    Column("sub_task_id", String, ForeignKey("nodes.id"), primary_key=True),
    Column("command_id", String, ForeignKey("nodes.id"), primary_key=True),
)

# Generic links for hierarchical relationships (fallback)
links = Table(
    "links",
    Base.metadata,
    Column("parent_id", String, ForeignKey("nodes.id"), primary_key=True),
    Column("child_id", String, ForeignKey("nodes.id"), primary_key=True),
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


class NodeCreateFields(TypedDict, total=False):
    """TypedDict for Node.new() and Node.create() method parameters.

    Matches the Node.__init__ signature but with all fields optional
    to allow flexible creation like Rails Active Record.
    """

    id: str
    layer: LayerType
    title: str
    description: str
    status: StatusType
    progress: int
    started_date: str | None
    completion_date: str | None
    links: Link | None
    metadata: Metadata | None
    command: Command | None
    owner: str | None
    severity: str | None
    work_type: str | None
    assignee: str | None


class NodeQueryFields(TypedDict, total=False):
    """TypedDict for Node.find_by() and query method parameters.

    Used for searching/filtering nodes by specific attributes.
    """

    layer: LayerType
    title: str
    description: str
    status: StatusType
    progress: int
    owner: str
    severity: str
    work_type: str
    assignee: str


class Goal(Base):
    """Rails ActiveRecord Goal model following Rails conventions."""

    __tablename__ = "goals"

    # Rails primary key (Integer for SQLite autoincrement compatibility)
    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True
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

    # Rails timestamps: created_at readonly, updated_at updates on save
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

    # Rails-style relationships (bidirectional with back_populates)
    labels: Mapped[list[Label]] = relationship(
        "Label", secondary=goals_labels, back_populates="goals"
    )


class Concept(Base):
    """Rails ActiveRecord Concept model following Rails conventions."""

    __tablename__ = "concepts"

    # Rails primary key (Integer for SQLite autoincrement compatibility)
    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True
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

    # Rails timestamp conventions - created_at readonly, updated_at writable
    created_at: Mapped[str] = mapped_column(
        String, default=lambda: datetime.now().isoformat(), nullable=False
    )
    updated_at: Mapped[str] = mapped_column(
        String,
        default=lambda: datetime.now().isoformat(),
        nullable=False,
        onupdate=lambda: datetime.now().isoformat(),
    )

    # Rails-style relationships
    labels: Mapped[list[Label]] = relationship(
        "Label", secondary=concepts_labels, back_populates="concepts"
    )


class Context(Base):
    """Rails ActiveRecord Context model following Rails conventions."""

    __tablename__ = "contexts"

    # Rails primary key convention
    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True
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

    # Rails timestamp conventions
    created_at: Mapped[str] = mapped_column(
        String, default=lambda: datetime.now().isoformat(), nullable=False
    )
    updated_at: Mapped[str] = mapped_column(
        String,
        default=lambda: datetime.now().isoformat(),
        nullable=False,
        onupdate=lambda: datetime.now().isoformat(),
    )

    # Rails-style relationships
    labels: Mapped[list[Label]] = relationship(
        "Label", secondary=contexts_labels, back_populates="contexts"
    )


class Constraints(Base):
    """Rails ActiveRecord Constraints model following Rails conventions."""

    __tablename__ = "constraints"

    # Rails primary key convention
    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True
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

    # Rails timestamp conventions
    created_at: Mapped[str] = mapped_column(
        String, default=lambda: datetime.now().isoformat(), nullable=False
    )
    updated_at: Mapped[str] = mapped_column(
        String,
        default=lambda: datetime.now().isoformat(),
        nullable=False,
        onupdate=lambda: datetime.now().isoformat(),
    )

    # Rails-style relationships
    labels: Mapped[list[Label]] = relationship(
        "Label", secondary=constraints_labels, back_populates="constraints"
    )


class Requirements(Base):
    """Rails ActiveRecord Requirements model following Rails conventions."""

    __tablename__ = "requirements"

    # Rails primary key convention
    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True
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

    # Rails timestamp conventions
    created_at: Mapped[str] = mapped_column(
        String, default=lambda: datetime.now().isoformat(), nullable=False
    )
    updated_at: Mapped[str] = mapped_column(
        String,
        default=lambda: datetime.now().isoformat(),
        nullable=False,
        onupdate=lambda: datetime.now().isoformat(),
    )

    # Rails-style relationships
    labels: Mapped[list[Label]] = relationship(
        "Label", secondary=requirements_labels, back_populates="requirements"
    )


class AcceptanceCriteria(Base):
    """Rails ActiveRecord AcceptanceCriteria model per Rails conventions."""

    __tablename__ = "acceptance_criteria"

    # Rails primary key convention
    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True
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

    # Rails timestamp conventions
    created_at: Mapped[str] = mapped_column(
        String, default=lambda: datetime.now().isoformat(), nullable=False
    )
    updated_at: Mapped[str] = mapped_column(
        String,
        default=lambda: datetime.now().isoformat(),
        nullable=False,
        onupdate=lambda: datetime.now().isoformat(),
    )

    # Rails-style relationships
    labels: Mapped[list[Label]] = relationship(
        "Label",
        secondary=acceptance_criteria_labels,
        back_populates="acceptance_criteria",
    )


class InterfaceContract(Base):
    """Rails ActiveRecord InterfaceContract model per Rails conventions."""

    __tablename__ = "interface_contracts"

    # Rails primary key convention
    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True
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

    # Rails timestamp conventions
    created_at: Mapped[str] = mapped_column(
        String, default=lambda: datetime.now().isoformat(), nullable=False
    )
    updated_at: Mapped[str] = mapped_column(
        String,
        default=lambda: datetime.now().isoformat(),
        nullable=False,
        onupdate=lambda: datetime.now().isoformat(),
    )

    # Rails-style relationships
    labels: Mapped[list[Label]] = relationship(
        "Label",
        secondary=interface_contracts_labels,
        back_populates="interface_contracts",
    )


class Phase(Base):
    """Rails ActiveRecord Phase model following Rails conventions."""

    __tablename__ = "phases"

    # Rails primary key convention
    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True
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

    # Rails timestamp conventions
    created_at: Mapped[str] = mapped_column(
        String, default=lambda: datetime.now().isoformat(), nullable=False
    )
    updated_at: Mapped[str] = mapped_column(
        String,
        default=lambda: datetime.now().isoformat(),
        nullable=False,
        onupdate=lambda: datetime.now().isoformat(),
    )

    # Rails-style relationships
    labels: Mapped[list[Label]] = relationship(
        "Label", secondary=phases_labels, back_populates="phases"
    )


class Step(Base):
    """Rails ActiveRecord Step model following Rails conventions."""

    __tablename__ = "steps"

    # Rails primary key convention
    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True
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

    # Rails timestamp conventions
    created_at: Mapped[str] = mapped_column(
        String, default=lambda: datetime.now().isoformat(), nullable=False
    )
    updated_at: Mapped[str] = mapped_column(
        String,
        default=lambda: datetime.now().isoformat(),
        nullable=False,
        onupdate=lambda: datetime.now().isoformat(),
    )

    # Rails-style relationships
    labels: Mapped[list[Label]] = relationship(
        "Label", secondary=steps_labels, back_populates="steps"
    )


class Task(Base):
    """Rails ActiveRecord Task model following Rails conventions."""

    __tablename__ = "tasks"

    # Rails primary key convention
    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True
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

    # Rails timestamp conventions
    created_at: Mapped[str] = mapped_column(
        String, default=lambda: datetime.now().isoformat(), nullable=False
    )
    updated_at: Mapped[str] = mapped_column(
        String,
        default=lambda: datetime.now().isoformat(),
        nullable=False,
        onupdate=lambda: datetime.now().isoformat(),
    )

    # Rails-style relationships
    labels: Mapped[list[Label]] = relationship(
        "Label", secondary=tasks_labels, back_populates="tasks"
    )


class SubTask(Base):
    """Rails ActiveRecord SubTask model following Rails conventions."""

    __tablename__ = "sub_tasks"

    # Rails primary key convention
    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True
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

    # Rails timestamp conventions
    created_at: Mapped[str] = mapped_column(
        String, default=lambda: datetime.now().isoformat(), nullable=False
    )
    updated_at: Mapped[str] = mapped_column(
        String,
        default=lambda: datetime.now().isoformat(),
        nullable=False,
        onupdate=lambda: datetime.now().isoformat(),
    )

    # Rails-style relationships
    labels: Mapped[list[Label]] = relationship(
        "Label", secondary=sub_tasks_labels, back_populates="sub_tasks"
    )


class Label(Base):
    """Represents a label that can be attached to goals and other models."""

    __tablename__ = "labels"

    # Rails primary key (Integer for SQLite autoincrement compatibility)
    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True
    )

    # Model field (unique label name)
    name: Mapped[str] = mapped_column(
        String, nullable=False, unique=True
    )  # Rails uses 'name', not 'label'

    # Rails timestamp conventions - created_at readonly, updated_at writable
    created_at: Mapped[str] = mapped_column(
        String, default=lambda: datetime.now().isoformat(), nullable=False
    )
    updated_at: Mapped[str] = mapped_column(
        String,
        default=lambda: datetime.now().isoformat(),
        nullable=False,
        onupdate=lambda: datetime.now().isoformat(),
    )

    # Rails-style relationships (bidirectional with back_populates)
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

    # Legacy relationship (for backward compatibility during migration)
    nodes: Mapped[list[Node]] = relationship(
        "Node", secondary=node_labels, back_populates="labels"
    )


class Command(Base):
    """Executable command definition for Command layer nodes."""

    __tablename__ = "commands"

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True
    )
    node_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("nodes.id"), nullable=False
    )
    ac_ref: Mapped[str] = mapped_column(String)
    run_data: Mapped[str | None] = mapped_column(Text)  # JSON string
    artifacts: Mapped[str | None] = mapped_column(Text)  # JSON string

    # Relationship back to the node
    node: Mapped[Node] = relationship(back_populates="command")

    @property
    def run(self) -> dict[str, Any]:
        """Get run data as dictionary."""
        return json.loads(self.run_data) if self.run_data else {}

    @run.setter
    def run(self, value: dict[str, Any]) -> None:
        """Set run data from dictionary."""
        self.run_data = json.dumps(value)

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


class Link:
    """Hierarchical relationships between ToDoWrite nodes."""

    def __init__(
        self,
        parents: list[str] | None = None,
        children: list[str] | None = None,
    ) -> None:
        self.parents = parents or []
        self.children = children or []


class ActiveCollection:
    """
    Active Record-style collection manager for Node relationships.

    Implements Active Record collection methods:
    - .all() - Get all items
    - .size() - Get count
    - .empty() - Check if empty
    - .exists() - Check if any exist
    - .build() - Create new item (not saved)
    - .create() - Create new item (saved)

    Smart Query Optimization:
    - Small datasets (< 20 items): Use simple separate queries
      (faster for small data)
    - Large datasets (>= 20 items): Use optimized JOIN queries
      (faster for large data)
    """

    # Performance thresholds for adaptive query optimization
    SMALL_DATASET_THRESHOLD = 20  # Items below this use simple queries
    EAGER_LOADING_THRESHOLD = 10  # Items below this don't use eager loading

    def __init__(
        self, parent_node: Node, session: Session | None, target_layer: str
    ) -> None:
        self.parent_node = parent_node
        self.session = session
        self.target_layer = target_layer

        # Map layers to their proper association tables and column names
        self.association_mappings = {
            "Constraints": (constraints_goals, "goal_id", "constraint_id"),
            "Requirements": (
                constraints_requirements,
                "constraint_id",
                "requirement_id",
            ),
            "AcceptanceCriteria": (
                requirements_acceptance_criteria,
                "requirement_id",
                "acceptance_criteria_id",
            ),
            "InterfaceContract": (
                acceptance_criteria_interface_contracts,
                "acceptance_criteria_id",
                "interface_contract_id",
            ),
            "Phase": (
                interface_contracts_phases,
                "interface_contract_id",
                "phase_id",
            ),
            "Step": (phases_steps, "phase_id", "step_id"),
            "Task": (steps_tasks, "step_id", "task_id"),
            "SubTask": (tasks_sub_tasks, "task_id", "sub_task_id"),
            "Command": (sub_tasks_commands, "sub_task_id", "command_id"),
        }

        # Map parent layers to their child association tables and column names
        # This handles the case where parent nodes have different layer
        # names than expected
        self.parent_to_child_mappings = {
            # When a Constraints node (layer="Constraints") creates
            # Requirements
            ("Constraints", "Requirements"): (
                constraints_requirements,
                "constraint_id",
                "requirement_id",
            ),
            # When a Requirements node (layer="Requirements") creates
            # AcceptanceCriteria
            ("Requirements", "AcceptanceCriteria"): (
                requirements_acceptance_criteria,
                "requirement_id",
                "acceptance_criteria_id",
            ),
            # When an AcceptanceCriteria node creates InterfaceContracts
            ("AcceptanceCriteria", "InterfaceContract"): (
                acceptance_criteria_interface_contracts,
                "acceptance_criteria_id",
                "interface_contract_id",
            ),
            # When an InterfaceContract creates Phases
            ("InterfaceContract", "Phase"): (
                interface_contracts_phases,
                "interface_contract_id",
                "phase_id",
            ),
            # When a Phase node creates Steps
            ("Phase", "Step"): (phases_steps, "phase_id", "step_id"),
            # When a Step node creates Tasks
            ("Step", "Task"): (steps_tasks, "step_id", "task_id"),
            # When a Task node creates SubTasks
            ("Task", "SubTask"): (tasks_sub_tasks, "task_id", "sub_task_id"),
            # When a SubTask creates Commands
            ("SubTask", "Command"): (
                sub_tasks_commands,
                "sub_task_id",
                "command_id",
            ),
        }

        # Get the correct association table and column names for this layer
        parent_layer = parent_node.layer
        parent_child_key = (parent_layer, target_layer)

        if parent_child_key in self.parent_to_child_mappings:
            self.association_table, self.parent_col, self.child_col = (
                self.parent_to_child_mappings[parent_child_key]
            )
        elif target_layer in self.association_mappings:
            self.association_table, self.parent_col, self.child_col = (
                self.association_mappings[target_layer]
            )
        else:
            # Fallback to generic links table
            self.association_table = links
            self.parent_col = "parent_id"
            self.child_col = "child_id"

    def _should_use_optimized_queries(self) -> bool:
        """
        Determine if we should use optimized JOIN queries or simple queries.

        Returns:
            True for large datasets (optimized JOIN),
            False for small datasets (simple queries)
        """
        # Quick count check to determine dataset size
        count_query = (
            select(func.count())
            .select_from(self.association_table)
            .where(
                self.association_table.c[self.parent_col]
                == self.parent_node.id
            )
        )

        count_result = self.session.execute(count_query).scalar()
        return (count_result or 0) >= self.SMALL_DATASET_THRESHOLD

    def all(self) -> list[Node]:
        """Get all associated nodes using adaptive query optimization."""
        if not self.session:
            raise RuntimeError("No database session configured")

        # Smart query optimization: choose strategy based on dataset size
        if self._should_use_optimized_queries():
            # Large dataset: Use optimized JOIN query (better for 20+ items)
            nodes_query = (
                select(Node)
                .join(
                    self.association_table,
                    Node.id == self.association_table.c[self.child_col],
                )
                .where(
                    and_(
                        self.association_table.c[self.parent_col]
                        == self.parent_node.id,
                        Node.layer == self.target_layer,
                    )
                )
                .order_by(Node.title)
            )
            nodes = self.session.execute(nodes_query).scalars().all()
        else:
            # Small dataset: Use simple separate queries (faster for <20 items)
            # This avoids JOIN overhead for small datasets
            association_query = select(
                self.association_table.c[self.child_col]
            ).where(
                self.association_table.c[self.parent_col]
                == self.parent_node.id
            )
            result = self.session.execute(association_query).fetchall()
            child_ids = [row[0] for row in result]

            if not child_ids:
                return []

            nodes_query = (
                select(Node)
                .where(Node.id.in_(child_ids), Node.layer == self.target_layer)
                .order_by(Node.title)
            )
            nodes = self.session.execute(nodes_query).scalars().all()

        return list(nodes)

    def size(self) -> int:
        """Get count of associated nodes using adaptive query optimization."""
        if not self.session:
            raise RuntimeError("No database session configured")

        # Simple count query - no JOIN needed for counting relationships
        count_query = (
            select(func.count())
            .select_from(self.association_table)
            .where(
                and_(
                    self.association_table.c[self.parent_col]
                    == self.parent_node.id
                )
            )
        )

        # For datasets with mixed layer types, we need to filter by layer too
        # But only if we're not using a layer-specific association table
        if (
            self.association_table == links
        ):  # Generic table needs layer filtering
            count_query = count_query.where(
                exists(
                    select(1)
                    .select_from(Node)
                    .where(
                        and_(
                            Node.id
                            == self.association_table.c[self.child_col],
                            Node.layer == self.target_layer,
                        )
                    )
                )
            )

        result = self.session.execute(count_query).scalar()
        return result or 0

    def empty(self) -> bool:
        """Check if collection is empty (Rails-style)."""
        return self.size() == 0

    def exists(self, **kwargs: str | int | bool | None) -> bool:
        """Check if node exists using optimized EXISTS query."""
        if not self.session:
            raise RuntimeError("No database session configured")

        if not kwargs:
            # Use efficient EXISTS query when no criteria provided
            exists_query = (
                select(func.count())
                .join(
                    self.association_table,
                    Node.id == self.association_table.c[self.child_col],
                )
                .where(
                    and_(
                        self.association_table.c[self.parent_col]
                        == self.parent_node.id,
                        Node.layer == self.target_layer,
                    )
                )
                .limit(1)  # We only need to know if at least one exists
            )
            result = self.session.execute(exists_query).scalar()
            return (result or 0) > 0

        # For specific criteria, use EXISTS with additional conditions
        conditions = [
            self.association_table.c[self.parent_col] == self.parent_node.id,
            Node.layer == self.target_layer,
        ]

        # Add criteria conditions
        for key, value in kwargs.items():
            if hasattr(Node, key):
                conditions.append(getattr(Node, key) == value)

        exists_query = (
            select(func.count())
            .join(
                self.association_table,
                Node.id == self.association_table.c[self.child_col],
            )
            .where(and_(*conditions))
            .limit(1)  # We only need to know if at least one exists
        )

        result = self.session.execute(exists_query).scalar()
        return (result or 0) > 0

    def build(self, **kwargs: str | int | bool | None) -> Node:
        """
        Build new associated node (Rails-style).

        Creates new node but doesn't save it. Association is set up in memory
        and persists to database when the node is saved.
        """

        node = self.parent_node.__class__.new(
            layer=self.target_layer, **kwargs
        )

        # Set up in-memory association only (not database)
        # Database association created when node.save() is called
        if hasattr(node, "_pending_parent"):
            node._pending_parent = self.parent_node
        else:
            node._pending_parent = self.parent_node

        # For Rails-style automatic back-reference
        if hasattr(node, "_belongs_to"):
            node._belongs_to[self.parent_node.__class__.__name__.lower()] = (
                self.parent_node
            )

        return node

    def _insert_association(self, parent: Node, child: Node) -> None:
        """Insert relationship into the correct association table."""

        # Use the parent-child mappings for dynamic column assignment
        parent_layer = parent.layer
        parent_child_key = (parent_layer, self.target_layer)

        if parent_child_key in self.parent_to_child_mappings:
            # Use mapped columns for this parent-child relationship
            mapping = self.parent_to_child_mappings[parent_child_key]
            _table, parent_col, child_col = mapping
            insert_values = {parent_col: parent.id, child_col: child.id}
        else:
            # Fallback to the target layer mappings
            insert_values = {
                self.parent_col: parent.id,
                self.child_col: child.id,
            }

        self.session.execute(
            self.association_table.insert().values(**insert_values)
        )

        self.session.commit()

    def create(self, **kwargs: str | int | bool | None) -> Node:
        """
        Create new associated node (Rails-style).

        Creates new node, sets up association, and saves it.
        """
        node = self.build(**kwargs)
        return node.save()

    def where(self, **kwargs: NodeQueryFields) -> list[Node]:
        """Find nodes in collection matching criteria."""
        items = self.all()
        result = []

        for item in items:
            matches = True
            for key, value in kwargs.items():
                if getattr(item, key, None) != value:
                    matches = False
                    break
            if matches:
                result.append(item)

        return result

    def find_by(self, **kwargs: NodeQueryFields) -> Node | None:
        """Find first node in collection matching criteria."""
        items = self.where(**kwargs)
        return items[0] if items else None


class PhaseCollection(ActiveCollection):
    """Specialized collection for Phase (Constraints layer) nodes."""

    def __init__(self, parent_node: Node, session: Session | None) -> None:
        super().__init__(parent_node, session, "Constraints")


class RequirementCollection(ActiveCollection):
    """Specialized collection for Requirement nodes."""

    def __init__(self, parent_node: Node, session: Session | None) -> None:
        super().__init__(parent_node, session, "Requirements")


class TaskCollection(ActiveCollection):
    """Specialized collection for Task (SubTask layer) nodes."""

    def __init__(self, parent_node: Node, session: Session | None) -> None:
        super().__init__(parent_node, session, "SubTask")


class AcceptanceCriteriaCollection(ActiveCollection):
    """Specialized collection for AcceptanceCriteria nodes."""

    def __init__(self, parent_node: Node, session: Session | None) -> None:
        super().__init__(parent_node, session, "AcceptanceCriteria")


class StepCollection(ActiveCollection):
    """Specialized collection for Step nodes."""

    def __init__(self, parent_node: Node, session: Session | None) -> None:
        super().__init__(parent_node, session, "Step")


class SubTaskCollection(ActiveCollection):
    """Specialized collection for SubTask nodes."""

    def __init__(self, parent_node: Node, session: Session | None) -> None:
        super().__init__(parent_node, session, "SubTask")


class CommandCollection(ActiveCollection):
    """Specialized collection for Command nodes."""

    def __init__(self, parent_node: Node, session: Session | None) -> None:
        super().__init__(parent_node, session, "Command")


class Node(Base):
    """
    Rails-style Active Record Node combining business logic with SQLAlchemy ORM.

    This class represents the fundamental unit of work in ToDoWrite, combining
    business logic methods with database persistence through SQLAlchemy ORM.

    Example Usage:
        # Create new node
        my_node = Node.new(
            layer="Goal",
            title="Launch Product",
            owner="team-lead"
        )

        # Access relationships
        children = my_node.children  # Returns list of child Node objects
        parents = my_node.parents    # Returns list of parent Node objects

        # Save to database
        my_node.save()

        # Business logic methods
        my_node.complete()
        my_node.add_child(child_node)
    """

    # Performance thresholds for adaptive query optimization
    SMALL_DATASET_THRESHOLD = 20  # Items below this use simple queries
    EAGER_LOADING_THRESHOLD = 10  # Items below this don't use eager loading
    BATCH_SIZE = 50  # Size for batch processing

    __tablename__ = "nodes"

    # Core fields
    id: Mapped[int] = mapped_column(
        BigInteger, primary_key=True, autoincrement=True
    )
    layer: Mapped[str] = mapped_column(String, nullable=False)
    title: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str | None] = mapped_column(Text)
    status: Mapped[str] = mapped_column(String, default="planned")
    progress: Mapped[int | None] = mapped_column(Integer)
    started_date: Mapped[str | None] = mapped_column(String)
    completion_date: Mapped[str | None] = mapped_column(String)

    # Metadata fields flattened for database
    owner: Mapped[str | None] = mapped_column(String)
    severity: Mapped[str | None] = mapped_column(String)
    work_type: Mapped[str | None] = mapped_column(String)
    assignee: Mapped[str | None] = mapped_column(String)

    # Relationships - these return actual Node objects!
    labels: Mapped[list[Label]] = relationship(
        secondary=node_labels, back_populates="nodes"
    )
    command: Mapped[Command | None] = relationship(back_populates="node")
    parents: Mapped[list[Node]] = relationship(
        secondary=links,
        primaryjoin="Node.id == links.c.child_id",
        secondaryjoin="Node.id == links.c.parent_id",
        back_populates="children",
    )
    children: Mapped[list[Node]] = relationship(
        secondary=links,
        primaryjoin="Node.id == links.c.parent_id",
        secondaryjoin="Node.id == links.c.child_id",
        back_populates="parents",
    )

    # Class-level session management (like Rails)
    _session = None

    @classmethod
    def configure_session(cls, session: Session) -> None:
        """Configure the database session for all Node operations."""
        cls._session = session

    @classmethod
    def new(cls, **kwargs: NodeCreateFields) -> Node:
        """
        Create a new Node instance (Rails-style factory method).

        Example:
            node = Node.new(
                layer="Goal",
                title="Launch Product",
                description="Successfully launch v1.0",
                owner="product-team",
                severity="high"
            )
        """
        import uuid

        # Generate ID if not provided
        if "id" not in kwargs:
            layer = kwargs.get("layer", "Task")
            safe_title = "".join(
                c.lower() if c.isalnum() else "-"
                for c in kwargs.get("title", "untitled")[:50]
            )
            unique_id = str(uuid.uuid4())[:8]
            kwargs["id"] = f"{layer.upper()}-{safe_title}-{unique_id}"

        # Create instance
        node = cls(**kwargs)

        # Mark as new for Rails-style behavior
        node._is_new_record = True

        return node

    @classmethod
    def find(cls, node_id: str) -> Node | None:
        """
        Find a node by ID (Rails-style).

        Args:
            node_id: The node ID to find

        Returns:
            Node object if found, None otherwise
        """
        session = cls._session
        if not session:
            raise RuntimeError(
                "No database session configured. Call Node.configure_session() first."
            )

        return session.get(cls, node_id)

    @classmethod
    def find_by(cls, **kwargs: NodeQueryFields) -> list[Node]:
        """
        Find nodes by attributes (Rails-style).

        Args:
            **kwargs: Attribute name/value pairs to search by

        Returns:
            List of matching Node objects
        """
        from sqlalchemy import and_

        session = cls._session
        if not session:
            raise RuntimeError(
                "No database session configured. Call Node.configure_session() first."
            )

        conditions = []
        for key, value in kwargs.items():
            if hasattr(cls, key):
                conditions.append(getattr(cls, key) == value)

        if not conditions:
            return []

        return (
            session.execute(select(cls).where(and_(*conditions)))
            .scalars()
            .all()
        )

    @classmethod
    def all(cls) -> list[Node]:
        """
        Get all nodes (Rails-style).

        Returns:
            List of all Node objects
        """
        session = cls._session
        if not session:
            raise RuntimeError(
                "No database session configured. Call Node.configure_session() first."
            )

        return session.execute(select(cls)).scalars().all()

    @classmethod
    def where(
        cls,
        layer: str | None = None,
        status: str | None = None,
        owner: str | None = None,
    ) -> list[Node]:
        """
        Find nodes with common filters (Rails-style).

        Args:
            layer: Filter by layer
            status: Filter by status
            owner: Filter by owner

        Returns:
            List of matching Node objects
        """
        from sqlalchemy import and_

        session = cls._session
        if not session:
            raise RuntimeError(
                "No database session configured. Call Node.configure_session() first."
            )

        conditions = []
        if layer:
            conditions.append(cls.layer == layer)
        if status:
            conditions.append(cls.status == status)
        if owner:
            conditions.append(cls.owner == owner)

        if not conditions:
            return cls.all()

        return (
            session.execute(select(cls).where(and_(*conditions)))
            .scalars()
            .all()
        )

    @classmethod
    def with_eager_loaded_relationships(
        cls, *relationship_names: str
    ) -> list[Node]:
        """
        Get nodes with eagerly loaded relationships to prevent N+1 queries.

        Args:
            *relationship_names: Names of relationships to eager load (e.g., 'parents', 'children')

        Returns:
            List of Node objects with specified relationships pre-loaded

        Example:
            # Load goals with all their children in one query
            goals = Node.with_eager_loaded_relationships('children').where(layer='Goal')
        """
        session = cls._session
        if not session:
            raise RuntimeError(
                "No database session configured. Call Node.configure_session() first."
            )

        query = select(cls)

        # Add eager loading for each requested relationship
        for rel_name in relationship_names:
            if hasattr(cls, rel_name):
                query = query.options(joinedload(getattr(cls, rel_name)))

        return session.execute(query).scalars().all()

    @classmethod
    def find_with_children(
        cls,
        layer: str | None = None,
        status: str | None = None,
        owner: str | None = None,
    ) -> list[Node]:
        """
        Find nodes with children loaded using adaptive optimization.

        This method adapts its strategy based on expected dataset size:
        - Small datasets (< 20 items): Simple queries without eager loading
        - Large datasets (>= 20 items): Optimized with eager loading to prevent N+1 queries

        Args:
            layer: Filter by layer type
            status: Filter by status
            owner: Filter by owner

        Returns:
            List of Node objects with children loaded appropriately
        """
        session = cls._session
        if not session:
            raise RuntimeError(
                "No database session configured. Call Node.configure_session() first."
            )

        conditions = []
        if layer:
            conditions.append(cls.layer == layer)
        if status:
            conditions.append(cls.status == status)
        if owner:
            conditions.append(cls.owner == owner)

        # First, do a quick count to determine if we should use eager loading
        count_query = select(func.count(cls.id))
        if conditions:
            count_query = count_query.where(and_(*conditions))

        estimated_count = session.execute(count_query).scalar() or 0

        # Adaptive query strategy
        if estimated_count >= cls.EAGER_LOADING_THRESHOLD:
            # Large dataset: Use eager loading to prevent N+1 queries
            query = select(cls).options(joinedload(cls.children))
            if conditions:
                query = query.where(and_(*conditions))
            return session.execute(query).unique().scalars().all()
        else:
            # Small dataset: Use simple query (eager loading overhead > benefit)
            query = select(cls)
            if conditions:
                query = query.where(and_(*conditions))
            return session.execute(query).scalars().all()

    @classmethod
    def find_with_parents(
        cls,
        layer: str | None = None,
        status: str | None = None,
        owner: str | None = None,
    ) -> list[Node]:
        """
        Find nodes with parents loaded using adaptive optimization.

        This method adapts its strategy based on expected dataset size:
        - Small datasets (< 20 items): Simple queries without eager loading
        - Large datasets (>= 20 items): Optimized with eager loading to prevent N+1 queries

        Args:
            layer: Filter by layer type
            status: Filter by status
            owner: Filter by owner

        Returns:
            List of Node objects with parents loaded appropriately
        """
        session = cls._session
        if not session:
            raise RuntimeError(
                "No database session configured. Call Node.configure_session() first."
            )

        conditions = []
        if layer:
            conditions.append(cls.layer == layer)
        if status:
            conditions.append(cls.status == status)
        if owner:
            conditions.append(cls.owner == owner)

        # First, do a quick count to determine if we should use eager loading
        count_query = select(func.count(cls.id))
        if conditions:
            count_query = count_query.where(and_(*conditions))

        estimated_count = session.execute(count_query).scalar() or 0

        # Adaptive query strategy
        if estimated_count >= cls.EAGER_LOADING_THRESHOLD:
            # Large dataset: Use eager loading to prevent N+1 queries
            query = select(cls).options(joinedload(cls.parents))
            if conditions:
                query = query.where(and_(*conditions))
            return session.execute(query).unique().scalars().all()
        else:
            # Small dataset: Use simple query (eager loading overhead > benefit)
            query = select(cls)
            if conditions:
                query = query.where(and_(*conditions))
            return session.execute(query).scalars().all()

    def __init__(
        self,
        id: str,
        layer: LayerType,
        title: str,
        description: str = "",
        status: StatusType = "planned",
        progress: int = 0,
        started_date: str | None = None,
        completion_date: str | None = None,
        links: Link | None = None,
        metadata: Metadata | None = None,
        command: Command | None = None,
        owner: str | None = None,
        severity: str | None = None,
        work_type: str | None = None,
        assignee: str | None = None,
    ) -> None:
        """Initialize Node with backward compatibility."""
        self.id = id
        self.layer = layer
        self.title = title
        self.description = description
        self.status = status
        self.progress = progress
        self.started_date = started_date
        self.completion_date = completion_date
        self.owner = owner
        self.severity = severity
        self.work_type = work_type
        self.assignee = assignee
        self.links = links or Link()
        self.node_metadata = metadata or Metadata(
            owner=owner,
            severity=severity,
            work_type=work_type,
            assignee=assignee,
        )
        self.command = command

        # Rails-style state tracking
        self._is_new_record = False
        self._destroyed = False

        # Rails-style belongs_to back-references
        self._belongs_to = {}

    # Rails-style Active Record methods
    def save(self) -> Node:
        """
        Save the node to the database (Rails-style).

        Returns:
            Self for method chaining
        """
        if self._destroyed:
            raise ValueError("Cannot save a destroyed record")

        session = self._session or self.__class__._session
        if not session:
            raise RuntimeError(
                "No database session configured. Call Node.configure_session() first."
            )

        if self._is_new_record:
            session.add(self)
            self._is_new_record = False

        session.commit()

        # Handle pending parent relationship (from build() method)
        if hasattr(self, "_pending_parent") and self._pending_parent:
            parent = self._pending_parent
            # Use the parent's add_child method to create the relationship
            parent.add_child(self)
            # Clear the pending parent after creating the relationship
            delattr(self, "_pending_parent")

        # Only refresh if object is persistent (was already in database)
        if self in session:
            try:
                session.refresh(self)
            except Exception:
                pass  # Object may not be persistent yet, that's ok

        return self

    def destroy(self) -> None:
        """
        Delete the node from the database (Rails-style).
        """
        if hasattr(self, "_destroyed") and self._destroyed:
            return

        session = self._session or self.__class__._session
        if not session:
            raise RuntimeError("No database session configured")

        session.delete(self)
        session.commit()
        self._destroyed = True

    def update(self, **kwargs: NodeCreateFields) -> Node:
        """
        Update node attributes and save (Rails-style).

        Returns:
            Self for method chaining
        """
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
        return self.save()

    def reload(self) -> Node:
        """
        Reload the node from database (Rails-style).

        Returns:
            Self for method chaining
        """
        session = self._session or self.__class__._session
        if not session:
            raise RuntimeError("No database session configured")

        session.refresh(self)
        return self

    # Relationship management methods
    def _get_association_table_for_child(self, child_layer: str) -> tuple:
        """
        Get the correct association table and column names for a child layer.

        Returns:
            Tuple of (association_table, parent_column_name, child_column_name)
        """
        # Map parent-child layer combinations to their association tables
        layer_mappings = {
            ("Goal", "Constraints"): (
                constraints_goals,
                "goal_id",
                "constraint_id",
            ),
            ("Constraints", "Requirements"): (
                constraints_requirements,
                "constraint_id",
                "requirement_id",
            ),
            ("Requirements", "AcceptanceCriteria"): (
                requirements_acceptance_criteria,
                "requirement_id",
                "acceptance_criteria_id",
            ),
            ("AcceptanceCriteria", "InterfaceContract"): (
                acceptance_criteria_interface_contracts,
                "acceptance_criteria_id",
                "interface_contract_id",
            ),
            ("InterfaceContract", "Phase"): (
                interface_contracts_phases,
                "interface_contract_id",
                "phase_id",
            ),
            ("Phase", "Step"): (phases_steps, "phase_id", "step_id"),
            ("Step", "Task"): (steps_tasks, "step_id", "task_id"),
            ("Task", "SubTask"): (tasks_sub_tasks, "task_id", "sub_task_id"),
            ("SubTask", "Command"): (
                sub_tasks_commands,
                "sub_task_id",
                "command_id",
            ),
        }

        # Try to find specific mapping
        mapping_key = (self.layer, child_layer)
        if mapping_key in layer_mappings:
            return layer_mappings[mapping_key]

        # Fallback to generic links table
        return (links, "parent_id", "child_id")

    def add_child(self, child: Node) -> Node:
        """
        Add a child node relationship (Rails-style) with optimized database access.

        Uses INSERT OR IGNORE to eliminate the need for pre-check SELECT query
        and targets layer-specific association tables for optimal performance.

        Args:
            child: The child node to add

        Returns:
            Self for method chaining
        """
        session = self._session or self.__class__._session
        if not session:
            raise RuntimeError("No database session configured")

        # Get the correct association table based on layer mapping
        association_table, parent_col, child_col = (
            self._get_association_table_for_child(child.layer)
        )

        # Use INSERT OR IGNORE for atomic operation (eliminates race conditions and extra SELECT)
        insert_stmt = association_table.insert().values(
            **{parent_col: self.id, child_col: child.id}
        )

        # Different databases have different syntax for INSERT OR IGNORE
        # For SQLite: INSERT OR IGNORE
        # For PostgreSQL: INSERT ... ON CONFLICT DO NOTHING
        if callable(insert_stmt.prefix_with):
            insert_stmt = insert_stmt.prefix_with("OR IGNORE")
        else:
            # SQLAlchemy 2.0+ style
            try:
                from sqlalchemy.dialects.sqlite import insert

                sqlite_insert = insert(association_table).values(
                    **{parent_col: self.id, child_col: child.id}
                )
                insert_stmt = sqlite_insert.on_conflict_do_nothing()
            except ImportError:
                # Fallback for other databases
                session.execute(insert_stmt)

        session.execute(insert_stmt)
        session.commit()

        # For Rails-style back-reference
        if hasattr(child, "_belongs_to"):
            child._belongs_to[self.__class__.__name__.lower()] = self

        # Also add to SQLAlchemy relationship for consistency
        if child not in self.children:
            self.children.append(child)

        return self

    def remove_child(self, child: Node) -> Node:
        """
        Remove a child node relationship.

        Args:
            child: The child node to remove

        Returns:
            Self for method chaining
        """
        if child in self.children:
            self.children.remove(child)
        return self

    def add_parent(self, parent: Node) -> Node:
        """
        Add a parent node relationship.

        Args:
            parent: The parent node to add

        Returns:
            Self for method chaining
        """
        if parent not in self.parents:
            self.parents.append(parent)
        return self

    def remove_parent(self, parent: Node) -> Node:
        """
        Remove a parent node relationship.

        Args:
            parent: The parent node to remove

        Returns:
            Self for method chaining
        """
        if parent in self.parents:
            self.parents.remove(parent)
        return self

    # Business logic methods
    def start(self) -> Node:
        """
        Mark the node as started and update started_date.

        Returns:
            Self for method chaining
        """
        from datetime import datetime

        self.status = "in_progress"
        self.started_date = datetime.now().isoformat()
        return self

    def complete(self) -> Node:
        """
        Mark the node as completed and set progress to 100%.

        Returns:
            Self for method chaining
        """
        from datetime import datetime

        self.status = "completed"
        self.progress = 100
        self.completion_date = datetime.now().isoformat()
        return self

    def block(self) -> Node:
        """
        Mark the node as blocked.

        Returns:
            Self for method chaining
        """
        self.status = "blocked"
        return self

    def cancel(self) -> Node:
        """
        Cancel the node.

        Returns:
            Self for method chaining
        """
        self.status = "cancelled"
        return self

    def get_metadata(self) -> Metadata:
        """Get metadata object from database fields."""
        return Metadata(
            owner=self.owner or "",
            severity=self.severity or "",
            work_type=self.work_type or "",
            assignee=self.assignee or "",
            labels=[label.label for label in self.labels],
        )

    def set_metadata(self, value: Metadata) -> None:
        """Set database fields from metadata object."""
        self.owner = value.owner
        self.severity = value.severity
        self.work_type = value.work_type
        self.assignee = value.assignee

    # Use different property name to avoid SQLAlchemy conflict
    node_metadata = property(get_metadata, set_metadata)

    def to_dict(self) -> dict[str, Any]:
        """Convert node to dictionary for serialization."""
        return {
            "id": self.id,
            "layer": self.layer,
            "title": self.title,
            "description": self.description,
            "status": self.status,
            "progress": self.progress,
            "started_date": self.started_date,
            "completion_date": self.completion_date,
            "links": {
                "parents": self.links.parents,
                "children": self.links.children,
            },
            "metadata": self.node_metadata.to_dict(),
            "command": {
                "ac_ref": self.command.ac_ref,
                "run": self.command.run,
                "artifacts": self.command.artifacts_list,
            }
            if self.command
            else None,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Node:
        """Create a Node instance from a dictionary."""
        # Extract required fields
        node_id = data.get("id")
        layer = data.get("layer")
        title = data.get("title")

        if not node_id or not layer or not title:
            raise ValueError(
                "Node data must contain 'id', 'layer', and 'title' fields"
            )

        # Extract optional fields
        description = data.get("description", "")
        status = data.get("status", "planned")
        progress = data.get("progress", 0)
        started_date = data.get("started_date")
        completion_date = data.get("completion_date")

        # Extract metadata fields
        metadata = data.get("metadata", {})
        owner = metadata.get("owner")
        severity = metadata.get("severity")
        work_type = metadata.get("work_type")
        assignee = metadata.get("assignee")

        # Create node with constructor parameters
        return cls(
            id=node_id,
            layer=layer,
            title=title,
            description=description,
            status=status,
            progress=progress,
            started_date=started_date,
            completion_date=completion_date,
            owner=owner,
            severity=severity,
            work_type=work_type,
            assignee=assignee,
        )

    def is_completed(self) -> bool:
        """Check if node is completed."""
        return self.status == "completed"

    def is_active(self) -> bool:
        """Check if node is actively being worked on."""
        return self.status in ("planned", "in_progress")

    def add_parent_id(self, parent_id: str) -> None:
        """Add a parent relationship by ID."""
        if parent_id not in self.links.parents:
            self.links.parents.append(parent_id)

    def get_progress_percentage(self) -> int:
        """Get progress as percentage."""
        return self.progress or 0

    def update_progress(self, progress: int) -> None:
        """Update progress percentage."""
        self.progress = max(0, min(100, progress))
        if self.progress == 100 and self.status != "completed":
            self.status = "completed"
        elif 0 < self.progress < 100 and self.status == "planned":
            self.status = "in_progress"

    # Layer-specific relationship methods (Rails-style has_many/belongs_to)
    def phases(self) -> PhaseCollection:
        """
        Get Phase collection for this Goal (Rails-style has_many).

        Returns PhaseCollection with Rails-style methods like:
        - goal.phases.all() - Get all phases
        - goal.phases.size() - Get count
        - goal.phases.empty?() - Check if empty
        - goal.phases.exists?() - Check if any exist
        - goal.phases.build() - Create new Phase (not saved)
        - goal.phases.create() - Create new Phase (saved)
        """
        return PhaseCollection(self, self._session or self.__class__._session)

    def requirements(self) -> RequirementCollection:
        """Get Requirement collection for this node (Rails-style has_many)."""
        return RequirementCollection(
            self, self._session or self.__class__._session
        )

    def acceptance_criteria(self) -> AcceptanceCriteriaCollection:
        """Get AcceptanceCriteria collection for this node (Rails-style has_many)."""
        return AcceptanceCriteriaCollection(
            self, self._session or self.__class__._session
        )

    def tasks(self) -> TaskCollection:
        """Get Task collection for this node (Rails-style has_many)."""
        return TaskCollection(self, self._session or self.__class__._session)

    def steps(self) -> StepCollection:
        """Get Step collection for this node (Rails-style has_many)."""
        return StepCollection(self, self._session or self.__class__._session)

    def subtasks(self) -> SubTaskCollection:
        """Get SubTask collection for this node (Rails-style has_many)."""
        return SubTaskCollection(
            self, self._session or self.__class__._session
        )

    def commands(self) -> CommandCollection:
        """Get Command collection for this node (Rails-style has_many)."""
        return CommandCollection(
            self, self._session or self.__class__._session
        )

    # Rails-style class methods for creating specific layer types
    @classmethod
    def create_goal(
        cls, title: str, owner: str = "", **kwargs: NodeCreateFields
    ) -> Node:
        """Create a Goal node (Rails-style factory)."""
        return cls.new(layer="Goal", title=title, owner=owner, **kwargs).save()

    @classmethod
    def create_phase(
        cls, title: str, goal: Node, **kwargs: NodeCreateFields
    ) -> Node:
        """Create a Phase node and associate it with a goal (Rails-style)."""
        phase = cls.new(layer="Constraints", title=title, **kwargs)
        goal.add_phase(phase)
        return phase.save()

    @classmethod
    def create_requirement(
        cls, title: str, parent: Node, **kwargs: NodeCreateFields
    ) -> Node:
        """Create a Requirement node and associate it with parent (Rails-style)."""
        requirement = cls.new(layer="Requirements", title=title, **kwargs)
        parent.add_requirement(requirement)
        return requirement.save()

    @classmethod
    def create_task(
        cls, title: str, parent: Node, **kwargs: NodeCreateFields
    ) -> Node:
        """Create a Task node and associate it with parent (Rails-style)."""
        task = cls.new(layer="SubTask", title=title, **kwargs)
        parent.add_task(task)
        return task.save()

    @classmethod
    def create_command(
        cls, title: str, parent: Node, **kwargs: NodeCreateFields
    ) -> Node:
        """Create a Command node and associate it with parent (Rails-style)."""
        command = cls.new(layer="Command", title=title, **kwargs)
        parent.add_command(command)
        return command.save()


# Type aliases for backward compatibility
LinkType = Link
MetadataType = Metadata
CommandType = Command
NodeType = Node


# SQLAlchemy event listener to initialize _destroyed attribute when objects are loaded
@event.listens_for(Node, "load")
def initialize_node_attributes(target: Node, context: SessionState) -> None:
    """Initialize Node attributes that aren't stored in the database."""
    if not hasattr(target, "_destroyed"):
        target._destroyed = False
    if not hasattr(target, "_is_new_record"):
        target._is_new_record = False
    if not hasattr(target, "_belongs_to"):
        target._belongs_to = {}
