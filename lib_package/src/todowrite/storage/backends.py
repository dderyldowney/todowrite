"""
Storage backends for ToDoWrite.

This module provides abstract base classes and exceptions for storage implementations.
Compatible with Rails ActiveRecord patterns.
"""

from abc import ABC, abstractmethod
from typing import Any


class StorageError(Exception):
    """Base exception for storage operations."""

    pass


class StorageConnectionError(StorageError):
    """Exception raised when storage connection fails."""

    pass


class StorageQueryError(StorageError):
    """Exception raised when storage query fails."""

    pass


class NodeNotFoundError(StorageError):
    """Exception raised when a node is not found in storage."""

    pass


class NodeCreationError(StorageError):
    """Exception raised when node creation fails."""

    pass


class NodeUpdateError(StorageError):
    """Exception raised when node update fails."""

    pass


class NodeDeletionError(StorageError):
    """Exception raised when node deletion fails."""

    pass


class RelationshipError(StorageError):
    """Exception raised when relationship operations fail."""

    pass


class StorageBackend(ABC):
    """Abstract base class for storage backends."""

    @abstractmethod
    def connect(self) -> None:
        """Establish connection to storage."""
        pass

    @abstractmethod
    def disconnect(self) -> None:
        """Close connection to storage."""
        pass

    @abstractmethod
    def save_record(self, record: Any) -> Any:
        """Save a record to storage."""
        pass

    @abstractmethod
    def get_record(self, model_class: type, record_id: int) -> Any | None:
        """Get a record by ID."""
        pass

    @abstractmethod
    def delete_record(self, record: Any) -> bool:
        """Delete a record from storage."""
        pass


# Result classes for operation feedback
class NodeCreationResult:
    """Result of node creation operation."""

    def __init__(
        self, success: bool, node_id: int | None = None, message: str = ""
    ) -> None:
        self.success = success
        self.node_id = node_id
        self.message = message


class RelationshipCreationResult:
    """Result of relationship creation operation."""

    def __init__(self, success: bool, message: str = "") -> None:
        self.success = success
        self.message = message


# Compatibility exports for Rails ActiveRecord
__all__ = [
    "NodeCreationError",
    "NodeCreationResult",
    "NodeDeletionError",
    "NodeNotFoundError",
    "NodeUpdateError",
    "RelationshipCreationResult",
    "RelationshipError",
    "StorageBackend",
    "StorageConnectionError",
    "StorageError",
    "StorageQueryError",
]
