"""Simplified SQLAlchemy mapping for unified Node architecture.

This provides a clean mapping that works directly with core.types.Node
without any conversion complexity.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import Column, ForeignKey, Integer, String, Table, Text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

if TYPE_CHECKING:
    from sqlalchemy.engine import Engine


class Base(DeclarativeBase):
    """Base class for all SQLAlchemy models."""

    pass


class NodeTable(Base):
    """Simple database table for Node storage.

    This is just a thin persistence layer for core.types.Node.
    All business logic stays in the core.types.Node.
    """

    __tablename__ = "nodes"

    id: Mapped[str] = mapped_column(String, primary_key=True)
    layer: Mapped[str] = mapped_column(String, nullable=False)
    title: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str | None] = mapped_column(Text)
    status: Mapped[str] = mapped_column(String, default="planned")
    progress: Mapped[int | None] = mapped_column(Integer)
    started_date: Mapped[str | None] = mapped_column(String)
    completion_date: Mapped[str | None] = mapped_column(String)

    # Flattened metadata fields
    owner: Mapped[str | None] = mapped_column(String)
    severity: Mapped[str | None] = mapped_column(String)
    work_type: Mapped[str | None] = mapped_column(String)
    assignee: Mapped[str | None] = mapped_column(String)


# Simple relationship tables
node_labels = Table(
    "node_labels",
    Base.metadata,
    Column("node_id", String, ForeignKey("nodes.id"), primary_key=True),
    Column("label", String, primary_key=True),
)

labels = Table(
    "labels",
    Base.metadata,
    Column("label", String, primary_key=True),
)

links = Table(
    "links",
    Base.metadata,
    Column("parent_id", String, ForeignKey("nodes.id"), primary_key=True),
    Column("child_id", String, ForeignKey("nodes.id"), primary_key=True),
)

commands = Table(
    "commands",
    Base.metadata,
    Column("node_id", String, ForeignKey("nodes.id"), primary_key=True),
    Column("ac_ref", String),
    Column("run", Text),
)

artifacts = Table(
    "artifacts",
    Base.metadata,
    Column("artifact", String, primary_key=True),
    Column(
        "command_id", String, ForeignKey("commands.node_id"), primary_key=True
    ),
)


def create_database_tables(engine: Engine) -> None:
    """Create all database tables."""
    Base.metadata.create_all(engine)
