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

import json
import logging
from pathlib import Path
from typing import Any

import jsonschema

from ..storage import (
    NodeCreationError,
    NodeNotFoundError,
    NodeUpdateError,
    StorageBackend,
    StorageConnectionError,
    create_storage_backend,
)
from ..storage.schema_validator import validate_database_schema
from .types import Node

logger = logging.getLogger(__name__)


class ToDoWrite:
    """
    The main ToDoWrite application class for hierarchical task management.

    This refactored version uses the StorageBackend pattern to eliminate
    storage-specific conditionals and provide a clean, extensible architecture.

    The class orchestrates storage operations through the StorageBackend
    interface while maintaining the same public API as the original version.

    Key improvements:
    - No more storage type conditionals
    - Clean separation of concerns
    - Natural language method names
    - Extensible storage backend support
    """

    def __init__(
        self,
        database_url: str,
        auto_import: bool = True,
    ) -> None:
        """
        Initialize the ToDoWrite application with a storage backend.

        Args:
            database_url: Storage backend URL (e.g., 'postgresql://...', 'sqlite://...',
                         or file path)
            auto_import: Whether to auto-import YAML files on initialization
        """
        self.database_url = database_url
        self.auto_import = auto_import

        # Create and connect to storage backend
        self.storage = self._create_and_connect_storage_backend(database_url)

        # Load schema for validation
        self._load_node_schema()

        # Initialize database schema if needed
        self._initialize_database_schema()

        # Auto-import YAML files if enabled
        if auto_import:
            self._auto_import_yaml_files()

    def _create_and_connect_storage_backend(
        self, database_url: str
    ) -> StorageBackend:
        """Create and connect to the appropriate storage backend."""
        try:
            backend = create_storage_backend(database_url)
            backend.connect_to_storage()
            return backend
        except Exception as e:
            raise StorageConnectionError(
                "ToDoWrite", f"Failed to connect to storage backend: {e!s}"
            )

    def _load_node_schema(self) -> None:
        """Load the node schema for validation."""
        schema_path = (
            Path(__file__).parent / "schemas" / "todowrite.schema.json"
        )
        try:
            with open(schema_path) as f:
                self._node_schema = json.load(f)
        except FileNotFoundError:
            logger.warning(f"Schema file not found at {schema_path}")
            self._node_schema = None

    def _initialize_database_schema(self) -> None:
        """Initialize database schema if using database backend."""
        if self.storage.backend_name in ["PostgreSQL", "SQLite"]:
            try:
                validate_database_schema()
                logger.info(
                    f"{self.storage.backend_name} schema validation passed"
                )
            except Exception as e:
                logger.error(
                    f"{self.storage.backend_name} schema validation failed: {e}"
                )

    def _auto_import_yaml_files(self) -> None:
        """Auto-import YAML files if configured and using database backend."""
        # This would be implemented to use the storage backend for imports
        # For now, we'll leave the placeholder
        logger.info(
            "Auto-import of YAML files not yet implemented in refactored version"
        )

    def create_new_node(self, node_data: dict[str, Any]) -> Node:
        """
        Create a new node in storage with proper validation.

        Args:
            node_data: Dictionary containing node information

        Returns:
            Created Node object

        Raises:
            NodeCreationError: If node creation fails
        """
        try:
            # Validate and convert dict to Node
            app_node = self._validate_and_convert_to_node(node_data)

            # Use storage backend to create node - no conversion needed!
            result = self.storage.create_new_node(app_node)
            return result.created_node

        except (
            ValueError,
            KeyError,
            AttributeError,
            jsonschema.ValidationError,
        ) as e:
            if isinstance(e, NodeCreationError):
                raise
            raise NodeCreationError(
                node_data.get("id", "unknown"),
                f"Node creation failed: {e!s}",
                self.storage.backend_name,
            )

    def create_node_from_object(self, app_node: Node) -> Node:
        """
        Create a new node directly from a Node object.

        Args:
            app_node: Node object containing all node information

        Returns:
            Created Node object

        Raises:
            NodeCreationError: If node creation fails
        """
        try:
            # Validate node
            self._validate_node_object(app_node)

            # Use storage backend to create node - no conversion needed!
            result = self.storage.create_new_node(app_node)
            return result.created_node

        except (
            ValueError,
            KeyError,
            AttributeError,
            jsonschema.ValidationError,
        ) as e:
            if isinstance(e, NodeCreationError):
                raise
            raise NodeCreationError(
                app_node.id,
                f"Node creation failed: {e!s}",
                self.storage.backend_name,
            )

    def retrieve_node_by_id(self, node_id: str) -> Node:
        """
        Retrieve a node from storage by its unique identifier.

        Args:
            node_id: The unique identifier of the node to retrieve

        Returns:
            Retrieved Node object

        Raises:
            NodeNotFoundError: If node doesn't exist
        """
        try:
            # Direct return - no conversion needed!
            return self.storage.retrieve_node_by_id(node_id)
        except (ValueError, KeyError, AttributeError) as e:
            if "not found" in str(e).lower():
                raise NodeNotFoundError(node_id, self.storage.backend_name)
            raise NodeNotFoundError(node_id, self.storage.backend_name)

    def update_existing_node(
        self, node_id: str, update_data: dict[str, Any]
    ) -> Node:
        """
        Update an existing node with new data.

        Args:
            node_id: The unique identifier of the node to update
            update_data: Dictionary containing fields to update

        Returns:
            Updated Node object

        Raises:
            NodeNotFoundError: If node doesn't exist
            NodeUpdateError: If update fails
        """
        try:
            # Validate update data
            self._validate_node_data(update_data, is_update=True)

            # Use storage backend to update node
            updated_node = self.storage.update_existing_node(
                node_id, update_data
            )
            return self._convert_storage_node_to_app_node(updated_node)
        except Exception as e:
            if isinstance(e, (NodeNotFoundError, NodeUpdateError)):
                raise
            if "not found" in str(e).lower():
                raise NodeNotFoundError(node_id, self.storage.backend_name)
            raise NodeUpdateError(
                node_id,
                f"Node update failed: {e!s}",
                self.storage.backend_name,
            )

    def remove_node_by_id(self, node_id: str) -> bool:
        """
        Remove a node from storage.

        Args:
            node_id: The unique identifier of the node to remove

        Returns:
            True if node was removed, False if node didn't exist
        """
        try:
            return self.storage.remove_node_by_id(node_id)
        except Exception as e:
            logger.error(f"Failed to remove node '{node_id}': {e!s}")
            return False

    def list_all_nodes_in_layer(
        self, layer_name: str | None = None
    ) -> list[Node]:
        """
        List all nodes in storage, optionally filtered by layer.

        Args:
            layer_name: Optional layer name to filter results

        Returns:
            List of Node objects matching the filter criteria
        """
        try:
            storage_nodes = self.storage.list_all_nodes_in_layer(layer_name)
            return [
                self._convert_storage_node_to_app_node(node)
                for node in storage_nodes
            ]
        except Exception as e:
            logger.error(f"Failed to list nodes: {e!s}")
            return []

    def search_nodes_by_criteria(
        self, search_criteria: dict[str, Any]
    ) -> list[Node]:
        """
        Search for nodes matching the provided criteria.

        Args:
            search_criteria: Dictionary of field-value pairs to match

        Returns:
            List of Node objects that match all search criteria
        """
        try:
            storage_nodes = self.storage.search_nodes_by_criteria(
                search_criteria
            )
            return [
                self._convert_storage_node_to_app_node(node)
                for node in storage_nodes
            ]
        except Exception as e:
            logger.error(f"Failed to search nodes: {e!s}")
            return []

    def create_parent_child_relationship(
        self, parent_id: str, child_id: str
    ) -> bool:
        """
        Create a parent-child relationship between two nodes.

        Args:
            parent_id: The unique identifier of the parent node
            child_id: The unique identifier of the child node

        Returns:
            True if relationship was created, False if it already existed
        """
        try:
            result = self.storage.create_parent_child_relationship(
                parent_id, child_id
            )
            return result.was_newly_linked
        except Exception as e:
            logger.error(
                f"Failed to create relationship between '{parent_id}' and '{child_id}': {e!s}"
            )
            return False

    def remove_parent_child_relationship(
        self, parent_id: str, child_id: str
    ) -> bool:
        """
        Remove a parent-child relationship between two nodes.

        Args:
            parent_id: The unique identifier of the parent node
            child_id: The unique identifier of the child node

        Returns:
            True if relationship was removed, False if it didn't exist
        """
        try:
            return self.storage.remove_parent_child_relationship(
                parent_id, child_id
            )
        except Exception as e:
            logger.error(
                f"Failed to remove relationship between '{parent_id}' and '{child_id}': {e!s}"
            )
            return False

    def get_all_parents_of_node(self, node_id: str) -> list[Node]:
        """
        Retrieve all direct parent nodes for the given node.

        Args:
            node_id: The unique identifier of the child node

        Returns:
            List of Node objects that are direct parents of the given node
        """
        try:
            storage_nodes = self.storage.get_all_parents_of_node(node_id)
            return [
                self._convert_storage_node_to_app_node(node)
                for node in storage_nodes
            ]
        except Exception as e:
            logger.error(
                f"Failed to retrieve parents for node '{node_id}': {e!s}"
            )
            return []

    def get_all_children_of_node(self, node_id: str) -> list[Node]:
        """
        Retrieve all direct child nodes for the given node.

        Args:
            node_id: The unique identifier of the parent node

        Returns:
            List of Node objects that are direct children of the given node
        """
        try:
            storage_nodes = self.storage.get_all_children_of_node(node_id)
            return [
                self._convert_storage_node_to_app_node(node)
                for node in storage_nodes
            ]
        except Exception as e:
            logger.error(
                f"Failed to retrieve children for node '{node_id}': {e!s}"
            )
            return []

    def count_nodes_in_storage(self) -> int:
        """
        Count the total number of nodes currently stored.

        Returns:
            The total count of nodes in storage
        """
        try:
            return self.storage.count_nodes_in_storage()
        except Exception as e:
            logger.error(f"Failed to count nodes: {e!s}")
            return 0

    def storage_is_healthy(self) -> bool:
        """
        Check if the storage backend is healthy and accessible.

        Returns:
            True if storage is accessible and functioning normally
        """
        try:
            return self.storage.storage_is_healthy()
        except Exception as e:
            logger.error(f"Storage health check failed: {e!s}")
            return False

    # Helper methods

    def _validate_and_convert_to_node(self, node_data: dict[str, Any]) -> Node:
        """Validate node data and convert dict to Node object."""
        # Validate against schema if available
        if self._node_schema:
            try:
                import jsonschema

                jsonschema.validate(node_data, self._node_schema)
            except Exception as e:
                raise ValueError(f"Node data validation failed: {e}")

        # Convert dict to Node object using Node.from_dict method
        return Node.from_dict(node_data)

    def _validate_node_object(self, app_node: Node) -> None:
        """Validate a Node object."""
        # Convert to dict and validate against schema if available
        if self._node_schema:
            try:
                import jsonschema

                node_dict = app_node.to_dict()
                jsonschema.validate(node_dict, self._node_schema)
            except Exception as e:
                raise ValueError(f"Node validation failed: {e}")

    def _validate_node_data(
        self, node_data: dict[str, Any], is_update: bool = False
    ) -> None:
        """Validate node data against the schema."""
        if not self._node_schema:
            return  # Skip validation if no schema loaded

        try:
            import jsonschema

            # For updates, we might want more lenient validation
            jsonschema.validate(node_data, self._node_schema)
        except Exception as e:
            if not is_update:
                raise ValueError(f"Node data validation failed: {e}")
            # For updates, log warning but continue
            logger.warning(f"Update data validation warning: {e}")

    # Backward compatibility methods

    def create_node(self, node_data: dict[str, Any]) -> Node:
        """Backward compatibility alias for create_new_node."""
        return self.create_new_node(node_data)

    def get_node(self, node_id: str) -> Node | None:
        """Backward compatibility alias for retrieve_node_by_id."""
        try:
            return self.retrieve_node_by_id(node_id)
        except NodeNotFoundError:
            return None

    def update_node(
        self, node_id: str, update_data: dict[str, Any]
    ) -> Node | None:
        """Backward compatibility alias for update_existing_node."""
        try:
            return self.update_existing_node(node_id, update_data)
        except (NodeNotFoundError, NodeUpdateError):
            return None

    def delete_node(self, node_id: str) -> bool:
        """Backward compatibility alias for remove_node_by_id."""
        return self.remove_node_by_id(node_id)

    def list_nodes(self, layer: str | None = None) -> list[Node]:
        """Backward compatibility alias for list_all_nodes_in_layer."""
        return self.list_all_nodes_in_layer(layer)

    def search_nodes(self, criteria: dict[str, Any]) -> list[Node]:
        """Backward compatibility alias for search_nodes_by_criteria."""
        return self.search_nodes_by_criteria(criteria)

    def link_nodes(self, parent_id: str, child_id: str) -> bool:
        """Backward compatibility alias for create_parent_child_relationship."""
        return self.create_parent_child_relationship(parent_id, child_id)

    def unlink_nodes(self, parent_id: str, child_id: str) -> bool:
        """Backward compatibility alias for remove_parent_child_relationship."""
        return self.remove_parent_child_relationship(parent_id, child_id)

    def get_parents(self, node_id: str) -> list[Node]:
        """Backward compatibility alias for get_all_parents_of_node."""
        return self.get_all_parents_of_node(node_id)

    def get_children(self, node_id: str) -> list[Node]:
        """Backward compatibility alias for get_all_children_of_node."""
        return self.get_all_children_of_node(node_id)

    def count_nodes(self) -> int:
        """Backward compatibility alias for count_nodes_in_storage."""
        return self.count_nodes_in_storage()
