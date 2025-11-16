"""
Standalone API Functions for ToDoWrite.

Provides standalone functions that create a temporary ToDoWrite instance
to perform operations, making it easier to use the library without
managing app instances manually.
"""

from __future__ import annotations

from typing import Any

from .core import Node, ToDoWrite


def create_node(database_url: str, node_data: dict[str, Any]) -> Node:
    """Create a new node using a temporary ToDoWrite instance.

    Args:
        database_url: Database connection URL
        node_data: Node data dictionary

    Returns:
        Created node object

    Raises:
        InvalidNodeError: If node data is invalid
        DatabaseError: If database operation fails
    """
    app = ToDoWrite(database_url)
    return app.create_node(node_data)


def get_node(database_url: str, node_id: str) -> Node | None:
    """Retrieve a node by ID using a temporary ToDoWrite instance.

    Args:
        database_url: Database connection URL
        node_id: Unique node identifier

    Returns:
        Node object if found, None otherwise
    """
    app = ToDoWrite(database_url)
    return app.get_node(node_id)


def update_node(
    database_url: str, node_id: str, update_data: dict[str, Any]
) -> Node | None:
    """Update a node using a temporary ToDoWrite instance.

    Args:
        database_url: Database connection URL
        node_id: Unique node identifier
        update_data: Updated node data

    Returns:
        Updated node object if successful, None otherwise
    """
    app = ToDoWrite(database_url)
    return app.update_node(node_id, update_data)


def delete_node(database_url: str, node_id: str) -> bool:
    """Delete a node using a temporary ToDoWrite instance.

    Args:
        database_url: Database connection URL
        node_id: Unique node identifier

    Returns:
        True if node was deleted, False if node didn't exist
    """
    app = ToDoWrite(database_url)
    return app.delete_node(node_id)


def list_nodes(database_url: str, layer: str | None = None) -> list[Node]:
    """List all nodes, optionally filtered by layer.

    Args:
        database_url: Database connection URL
        layer: Optional layer filter (e.g., "Goal", "Task")

    Returns:
        List of node objects
    """
    app = ToDoWrite(database_url)
    return app.list_nodes(layer)


def search_nodes(database_url: str, criteria: dict[str, Any]) -> list[Node]:
    """Search nodes by criteria using a temporary ToDoWrite instance.

    Args:
        database_url: Database connection URL
        criteria: Search criteria dictionary

    Returns:
        List of matching node objects
    """
    app = ToDoWrite(database_url)
    return app.search_nodes(criteria)


def link_nodes(database_url: str, parent_id: str, child_id: str) -> bool:
    """Create a parent-child relationship between nodes.

    Args:
        database_url: Database connection URL
        parent_id: Parent node ID
        child_id: Child node ID

    Returns:
        True if linking was successful, False otherwise
    """
    app = ToDoWrite(database_url)
    return app.link_nodes(parent_id, child_id)


def unlink_nodes(database_url: str, parent_id: str, child_id: str) -> bool:
    """Remove a parent-child relationship between nodes.

    Args:
        database_url: Database connection URL
        parent_id: Parent node ID
        child_id: Child node ID

    Returns:
        True if unlinking was successful, False otherwise
    """
    app = ToDoWrite(database_url)
    return app.unlink_nodes(parent_id, child_id)
