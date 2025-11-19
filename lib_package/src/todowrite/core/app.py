"""ToDoWrite Core Application Module - Refactored with StorageBackend Pattern.

This module contains the main ToDoWrite application class that provides
hierarchical task management functionality using the new StorageBackend
abstraction pattern.

The refactored ToDoWrite system:
- Uses Strategy pattern for storage backends
- Eliminates storage type conditionals throughout codebase
- Provides clean, natural language method names
- Maintains backward compatibility with existing API

Example:
    >>> tw = ToDoWrite("sqlite:///todowrite.db")
    >>> goal = tw.create_new_node({
    ...     "layer": "Goal",
    ...     "title": "My Goal",
    ...     "description": "Description"
    ... })
    >>> print(f"Created goal: {goal.id}")

"""

from __future__ import annotations

import logging

# Legacy storage system - DEPRECATED in ToDoWrite Models API
# from ..storage import (
#     NodeCreationError,
#     NodeNotFoundError,
#     NodeUpdateError,
#     StorageBackend,
#     StorageConnectionError,
#     create_storage_backend,
# )
# from ..storage.schema_validator import validate_database_schema
# from .types import Node  # Node class removed - MAJOR BREAKING CHANGE

logger = logging.getLogger(__name__)


# DEPRECATED: Legacy ToDoWrite app class removed as part of
# the MAJOR BREAKING CHANGE to ToDoWrite Models API
# Use the new ToDoWrite Models directly instead:
#
# from todowrite import Goal, Task, create_engine, sessionmaker
#
# engine = create_engine("sqlite:///development.db")
# Session = sessionmaker(bind=engine)
# session = Session()
#
# goal = Goal(title="My Goal", owner="team")
# session.add(goal)
# session.commit()
#
# class ToDoWrite:

# ENTIRE CLASS REMOVED - MAJOR BREAKING CHANGE TO ToDoWrite MODELS
# See above for migration example
