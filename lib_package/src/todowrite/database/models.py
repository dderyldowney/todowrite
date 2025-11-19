"""
Database models for ToDoWrite.

This module provides the Rails ActiveRecord-style models for the ToDoWrite system.
These models use SQLAlchemy ORM for database operations.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base

# Base class for all Rails ActiveRecord models
Base = declarative_base()

# Database engine placeholder
_engine = None


def get_database_engine(database_url: str = "sqlite:///todowrite.db"):
    """Get or create database engine."""
    global _engine
    if _engine is None:
        _engine = create_engine(database_url)
    return _engine


__all__ = ["Base", "get_database_engine"]
