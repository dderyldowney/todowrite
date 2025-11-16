from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from ..core.types import Node


class StorageError(Exception):
    """Base exception for all storage backend operations."""

    def __init__(
        self, message: str, backend_name: str, operation: str
    ) -> None:
        self.backend_name = backend_name
        self.operation = operation
        super().__init__(f"{backend_name} {operation} failed: {message}")


class NodeNotFoundError(StorageError):
    """Raised when a requested node cannot be found in storage."""

    def __init__(self, node_id: str, backend_name: str) -> None:
        super().__init__(
            f"Node '{node_id}' not found", backend_name, "retrieve node"
        )


class NodeCreationError(StorageError):
    """Raised when node creation fails due to validation or storage constraints."""

    def __init__(self, node_id: str, reason: str, backend_name: str) -> None:
        super().__init__(
            f"Cannot create node '{node_id}': {reason}",
            backend_name,
            "create node",
        )


class NodeUpdateError(StorageError):
    """Raised when node update fails due to conflicts or storage constraints."""

    def __init__(self, node_id: str, reason: str, backend_name: str) -> None:
        super().__init__(
            f"Cannot update node '{node_id}': {reason}",
            backend_name,
            "update node",
        )


class NodeDeletionError(StorageError):
    """Raised when node deletion fails due to constraints or storage issues."""

    def __init__(self, node_id: str, reason: str, backend_name: str) -> None:
        super().__init__(
            f"Cannot delete node '{node_id}': {reason}",
            backend_name,
            "delete node",
        )


class RelationshipError(StorageError):
    """Raised when parent-child relationship operations fail."""

    def __init__(
        self, parent_id: str, child_id: str, reason: str, backend_name: str
    ) -> None:
        super().__init__(
            f"Cannot link parent '{parent_id}' to child '{child_id}': {reason}",
            backend_name,
            "create relationship",
        )


class StorageConnectionError(StorageError):
    """Raised when backend cannot establish or maintain connection."""

    def __init__(self, backend_name: str, connection_details: str) -> None:
        super().__init__(
            f"Connection failed: {connection_details}",
            backend_name,
            "connect to storage",
        )


class StorageQueryError(StorageError):
    """Raised when search or query operations fail."""

    def __init__(
        self, query_description: str, reason: str, backend_name: str
    ) -> None:
        super().__init__(
            f"Query failed for '{query_description}': {reason}",
            backend_name,
            "query nodes",
        )


@dataclass
class NodeCreationResult:
    """Represents the result of a node creation operation."""

    created_node: Node
    was_newly_created: bool

    def __str__(self) -> str:
        status = "created" if self.was_newly_created else "retrieved existing"
        return f"Node '{self.created_node.id}' {status}"


@dataclass
class RelationshipCreationResult:
    """Represents the result of creating a parent-child relationship."""

    parent_id: str
    child_id: str
    was_newly_linked: bool

    def __str__(self) -> str:
        status = "linked" if self.was_newly_linked else "already linked"
        return f"Parent '{self.parent_id}' {status} to child '{self.child_id}'"


class StorageBackend(ABC):
    """
    Abstract interface for all storage backends in the ToDoWrite system.

    This defines a contract that all storage implementations must follow,
    providing consistent operations regardless of the underlying storage technology.
    All method names are designed to read like natural language sentences.
    """

    @property
    @abstractmethod
    def backend_name(self) -> str:
        """Return the human-readable name of this storage backend."""
        pass

    @abstractmethod
    def connect_to_storage(self) -> None:
        """
        Establish connection to the storage backend.

        Raises:
            StorageConnectionError: If connection cannot be established
        """
        pass

    @abstractmethod
    def disconnect_from_storage(self) -> None:
        """Close connection to the storage backend and cleanup resources."""
        pass

    @abstractmethod
    def create_new_node(self, app_node: Node) -> NodeCreationResult:
        """
        Create a new node in storage with the provided Node object.

        Args:
            app_node: Application Node object containing all node fields and relationships

        Returns:
            NodeCreationResult with the created node and whether it was newly created

        Raises:
            NodeCreationError: If node validation fails or constraints are violated
            StorageConnectionError: If storage is unavailable
        """
        pass

    @abstractmethod
    def retrieve_node_by_id(self, node_id: str) -> Node:
        """
        Retrieve a specific node from storage by its unique identifier.

        Args:
            node_id: The unique identifier of the node to retrieve

        Returns:
            The requested Node object

        Raises:
            NodeNotFoundError: If no node exists with the given ID
            StorageConnectionError: If storage is unavailable
        """
        pass

    @abstractmethod
    def update_existing_node(self, app_node: Node) -> Node:
        """
        Update an existing node with new data and return the updated version.

        Args:
            app_node: The updated Node object containing all fields

        Returns:
            The updated Node object

        Raises:
            NodeNotFoundError: If no node exists with the given ID
            NodeUpdateError: If update violates constraints or validation
            StorageConnectionError: If storage is unavailable
        """
        pass

    @abstractmethod
    def remove_node_by_id(self, node_id: str) -> bool:
        """
        Remove a node from storage by its unique identifier.

        Args:
            node_id: The unique identifier of the node to remove

        Returns:
            True if node was removed, False if node didn't exist

        Raises:
            NodeDeletionError: If node cannot be deleted due to constraints
            StorageConnectionError: If storage is unavailable
        """
        pass

    @abstractmethod
    def list_all_nodes_in_layer(
        self, layer_name: str | None = None
    ) -> list[Node]:
        """
        List all nodes in storage, optionally filtered by layer type.

        Args:
            layer_name: Optional layer name to filter results (e.g., 'Goal', 'Task')

        Returns:
            List of Node objects matching the filter criteria

        Raises:
            StorageConnectionError: If storage is unavailable
        """
        pass

    @abstractmethod
    def search_nodes_by_criteria(
        self, search_criteria: dict[str, Any]
    ) -> list[Node]:
        """
        Search for nodes matching the provided criteria.

        Args:
            search_criteria: Dictionary of field-value pairs to match

        Returns:
            List of Node objects that match all search criteria

        Raises:
            StorageQueryError: If search cannot be executed
            StorageConnectionError: If storage is unavailable
        """
        pass

    @abstractmethod
    def create_parent_child_relationship(
        self, parent_id: str, child_id: str
    ) -> RelationshipCreationResult:
        """
        Create a parent-child relationship between two nodes.

        Args:
            parent_id: The unique identifier of the parent node
            child_id: The unique identifier of the child node

        Returns:
            RelationshipCreationResult indicating if relationship was newly created

        Raises:
            NodeNotFoundError: If either parent or child node doesn't exist
            RelationshipError: If relationship cannot be created due to constraints
            StorageConnectionError: If storage is unavailable
        """
        pass

    @abstractmethod
    def remove_parent_child_relationship(
        self, parent_id: str, child_id: str
    ) -> bool:
        """
        Remove a parent-child relationship between two nodes.

        Args:
            parent_id: The unique identifier of the parent node
            child_id: The unique identifier of the child node

        Returns:
            True if relationship was removed, False if relationship didn't exist

        Raises:
            StorageConnectionError: If storage is unavailable
        """
        pass

    @abstractmethod
    def get_all_parents_of_node(self, node_id: str) -> list[Node]:
        """
        Retrieve all direct parent nodes for the given node.

        Args:
            node_id: The unique identifier of the child node

        Returns:
            List of Node objects that are direct parents of the given node

        Raises:
            NodeNotFoundError: If the child node doesn't exist
            StorageConnectionError: If storage is unavailable
        """
        pass

    @abstractmethod
    def get_all_children_of_node(self, node_id: str) -> list[Node]:
        """
        Retrieve all direct child nodes for the given node.

        Args:
            node_id: The unique identifier of the parent node

        Returns:
            List of Node objects that are direct children of the given node

        Raises:
            NodeNotFoundError: If the parent node doesn't exist
            StorageConnectionError: If storage is unavailable
        """
        pass

    @abstractmethod
    def count_nodes_in_storage(self) -> int:
        """
        Count the total number of nodes currently stored.

        Returns:
            The total count of nodes in storage

        Raises:
            StorageConnectionError: If storage is unavailable
        """
        pass

    @abstractmethod
    def storage_is_healthy(self) -> bool:
        """
        Check if the storage backend is healthy and accessible.

        Returns:
            True if storage is accessible and functioning normally
        """
        pass
