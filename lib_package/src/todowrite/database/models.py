"""
Database models for ToDoWrite.

This module provides the Rails ActiveRecord-style models for the ToDoWrite system.
These models use SQLAlchemy ORM for database operations.
"""

from __future__ import annotations

from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import declarative_base

# Base class for all Rails ActiveRecord models
Base = declarative_base()

# Database engine placeholder
_engine: Engine | None = None


def get_database_engine(
    database_url: str = "sqlite:///todowrite.db",
) -> Engine:
    """Get or create database engine."""
    global _engine
    if _engine is None:
        _engine = create_engine(database_url)
    return _engine


__all__ = ["Base", "get_database_engine"]
