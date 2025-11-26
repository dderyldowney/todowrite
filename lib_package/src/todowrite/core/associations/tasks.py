"""
Task association tables.

This module contains association tables for task relationships.
"""

from __future__ import annotations

from sqlalchemy import (
    Column,
    ForeignKey,
    Integer,
    Table,
)

from todowrite.core.models.base import Base

# Task < SubTask associations (original naming with underscore)
tasks_sub_tasks = Table(
    "tasks_sub_tasks",  # Task < SubTask (alphabetical)
    Base.metadata,
    Column("task_id", Integer, ForeignKey("tasks.id")),
    Column("sub_task_id", Integer, ForeignKey("sub_tasks.id")),
)

# SubTask < Command associations (conceptual to executable layer)
sub_tasks_commands = Table(
    "sub_tasks_commands",  # SubTask < Command (alphabetical)
    Base.metadata,
    Column("sub_task_id", Integer, ForeignKey("sub_tasks.id")),
    Column("command_id", Integer, ForeignKey("commands.id")),
)
