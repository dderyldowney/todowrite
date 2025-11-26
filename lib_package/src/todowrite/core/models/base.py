"""
Base model.

This module contains the Base SQLAlchemy model.
"""

from __future__ import annotations

from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    """Base class for all ToDoWrite models."""

    pass
