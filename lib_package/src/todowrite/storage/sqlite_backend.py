from __future__ import annotations

import logging
from collections.abc import Iterator
from contextlib import contextmanager
from pathlib import Path
from typing import Any

from sqlalchemy import (
    Engine,
    and_,
    create_engine,
    delete,
    func,
    or_,
    select,
    text,
)
from sqlalchemy.orm import Session, sessionmaker

from ..core.types import Node, links
from .backends import (
    NodeCreationError,
    NodeCreationResult,
    NodeDeletionError,
    NodeNotFoundError,
    NodeUpdateError,
    RelationshipCreationResult,
    RelationshipError,
    StorageBackend,
    StorageConnectionError,
    StorageQueryError,
)

logger = logging.getLogger(__name__)


class SQLiteBackend(StorageBackend):
    """
    SQLite storage backend optimized for development and single-user
    environments.

    This backend provides lightweight, file-based storage for ToDoWrite
    nodes using SQLite with optimizations for speed and simplicity in
    development environments.
    """

    def __init__(self, database_path: str | Path) -> None:
        """
        Initialize SQLite backend with database file path.

        Args:
            database_path: Path to SQLite database file (will be created if
                it doesn't exist)
        """
        self.database_path = Path(database_path)
        self.database_url = f"sqlite:///{self.database_path}"
        self.engine: Engine | None = None
        self.Session: sessionmaker | None = None
        self._is_connected = False

        # Ensure parent directory exists
        self.database_path.parent.mkdir(parents=True, exist_ok=True)

    @property
    def backend_name(self) -> str:
        """Return the human-readable name of this storage backend."""
        return "SQLite"

    def connect_to_storage(self) -> None:
        """Establish connection to SQLite database with optimized settings."""
        try:
            # Create engine optimized for SQLite
            self.engine = create_engine(
                self.database_url,
                echo=False,  # Set to True for SQL logging in development
                connect_args={
                    "check_same_thread": False,  # Allow cross-thread access
                    "timeout": 30,  # 30 second timeout
                },
                pool_pre_ping=True,  # Validate connections
            )

            # Configure session factory
            self.Session = sessionmaker(
                bind=self.engine,
                expire_on_commit=False,  # Keep objects accessible after commit
            )

            # Create tables if they don't exist
            from ..database.models import Base

            Base.metadata.create_all(self.engine)

            # Test the connection using session directly
            test_session = self.Session()
            test_session.execute(text("SELECT 1"))
            test_session.commit()
            test_session.close()

            self._is_connected = True
            logger.info(f"Connected to SQLite database: {self.database_path}")

        except Exception as e:
            self._is_connected = False
            raise StorageConnectionError(
                self.backend_name,
                f"Failed to connect to SQLite database at "
                f"{self.database_path}: {e!s}",
            ) from e

    def disconnect_from_storage(self) -> None:
        """Close SQLite connection and cleanup resources."""
        if self.engine:
            self.engine.dispose()
            self.engine = None
            self.Session = None
            self._is_connected = False
            logger.info("Disconnected from SQLite database")

    @contextmanager
    def _get_session(self) -> Iterator[Session]:
        """Context manager for SQLite database sessions with proper error
        handling."""
        if not self._is_connected or not self.Session:
            raise StorageConnectionError(
                self.backend_name,
                "Not connected to database - call connect_to_storage() first",
            )

        session = self.Session()
        try:
            # Enable foreign key constraints for SQLite
            session.execute(text("PRAGMA foreign_keys = ON"))
            yield session
            session.commit()
        except Exception as e:
            session.rollback()
            logger.error(f"SQLite session error: {e}")
            raise
        finally:
            session.close()

    def create_new_node(self, node: Node) -> NodeCreationResult:
        """Create a new node using Active Record patterns."""
        try:
            with self._get_session() as session:
                # Configure Node with session for Active Record operations
                Node.configure_session(session)

                # Check if node already exists
                existing_node = session.get(Node, node.id)
                if existing_node:
                    return NodeCreationResult(
                        created_node=existing_node,
                        was_newly_created=False,
                    )

                # Use Active Record pattern - Node saves itself
                node.save()

                return NodeCreationResult(
                    created_node=node,
                    was_newly_created=True,
                )

        except Exception as e:
            raise NodeCreationError(
                node.id if hasattr(node, "id") else "unknown",
                f"SQLite creation failed: {e!s}",
                self.backend_name,
            ) from e

    def retrieve_node_by_id(self, node_id: str) -> Node:
        """Retrieve a node from SQLite by its unique identifier."""
        try:
            with self._get_session() as session:
                Node.configure_session(session)

                node = session.get(Node, node_id)
                if not node:
                    raise NodeNotFoundError(node_id, self.backend_name)
                return node

        except NodeNotFoundError:
            raise
        except Exception as e:
            raise StorageConnectionError(
                self.backend_name,
                f"Failed to retrieve node '{node_id}': {e!s}",
            ) from e

    def update_existing_node(
        self, node_id: str, update_data: dict[str, Any]
    ) -> Node:
        """Update an existing node using Active Record patterns."""
        try:
            with self._get_session() as session:
                Node.configure_session(session)

                node = session.get(Node, node_id)
                if not node:
                    raise NodeNotFoundError(node_id, self.backend_name)

                # Update basic fields
                for field, value in update_data.items():
                    if field not in [
                        "labels",
                        "command",
                        "parents",
                        "children",
                    ]:
                        if hasattr(node, field):
                            setattr(node, field, value)

                # Handle label updates
                if "labels" in update_data:
                    self._update_node_labels(
                        session, node, update_data["labels"]
                    )

                # Handle command updates
                if "command" in update_data:
                    self._update_node_command(
                        session, node, update_data["command"]
                    )

                # Handle relationship updates
                if "parents" in update_data or "children" in update_data:
                    parents_data = update_data.get("parents", [])
                    children_data = update_data.get("children", [])
                    self._update_node_relationships(
                        session, node, parents_data, children_data
                    )

                # Use Active Record pattern - Node saves itself
                node.save()
                return node

        except NodeNotFoundError:
            raise
        except Exception as e:
            raise NodeUpdateError(
                node_id, f"SQLite update failed: {e!s}", self.backend_name
            ) from e

    def remove_node_by_id(self, node_id: str) -> bool:
        """Remove a node using Active Record patterns."""
        try:
            with self._get_session() as session:
                Node.configure_session(session)

                node = session.get(Node, node_id)
                if not node:
                    return False  # Node didn't exist, nothing to remove

                # Use Active Record pattern - Node destroys itself and
                # cleans up relationships
                node.destroy()
                return True

        except Exception as e:
            raise NodeDeletionError(
                node_id, f"SQLite deletion failed: {e!s}", self.backend_name
            ) from e

    def list_all_nodes_in_layer(
        self, layer_name: str | None = None
    ) -> list[Node]:
        """List all nodes in SQLite, optionally filtered by layer."""
        try:
            with self._get_session() as session:
                query = select(Node)
                if layer_name:
                    query = query.where(Node.layer == layer_name)
                query = query.order_by(Node.layer, Node.title)

                return list(session.execute(query).scalars().all())

        except Exception as e:
            raise StorageConnectionError(
                self.backend_name, f"Failed to list nodes: {e!s}"
            ) from e

    def search_nodes_by_criteria(
        self, search_criteria: dict[str, Any]
    ) -> list[Node]:
        """Search for nodes in SQLite matching the provided criteria."""
        try:
            with self._get_session() as session:
                query = select(Node)

                # Build search conditions
                conditions = []
                for field, value in search_criteria.items():
                    if hasattr(Node, field):
                        if isinstance(value, str):
                            # SQLite uses LIKE for case-insensitive search
                            conditions.append(
                                getattr(Node, field).like(f"%{value}%")
                            )
                        else:
                            conditions.append(getattr(Node, field) == value)

                if conditions:
                    query = query.where(and_(*conditions))

                query = query.order_by(Node.layer, Node.title)
                return list(session.execute(query).scalars().all())

        except Exception as e:
            raise StorageQueryError(
                str(search_criteria),
                f"SQLite search failed: {e!s}",
                self.backend_name,
            ) from e

    def create_parent_child_relationship(
        self, parent_id: str, child_id: str
    ) -> RelationshipCreationResult:
        """Create a parent-child relationship using Active Record patterns."""
        try:
            with self._get_session() as session:
                Node.configure_session(session)

                # Verify both nodes exist
                parent_node = session.get(Node, parent_id)
                child_node = session.get(Node, child_id)

                if not parent_node:
                    raise NodeNotFoundError(parent_id, self.backend_name)
                if not child_node:
                    raise NodeNotFoundError(child_id, self.backend_name)

                # Check if relationship already exists using Active Record
                if child_node in parent_node.children:
                    return RelationshipCreationResult(
                        parent_id=parent_id,
                        child_id=child_id,
                        was_newly_linked=False,
                    )

                # Use Active Record pattern - parent adds child
                parent_node.add_child(child_node)

                return RelationshipCreationResult(
                    parent_id=parent_id,
                    child_id=child_id,
                    was_newly_linked=True,
                )

        except (NodeNotFoundError, RelationshipError):
            raise
        except Exception as e:
            raise RelationshipError(
                parent_id,
                child_id,
                f"SQLite relationship creation failed: {e!s}",
                self.backend_name,
            ) from e

    def remove_parent_child_relationship(
        self, parent_id: str, child_id: str
    ) -> bool:
        """Remove a parent-child relationship between two nodes in SQLite."""
        try:
            with self._get_session() as session:
                result = session.execute(
                    delete(Link).where(
                        and_(
                            links.c.parent_id == parent_id,
                            links.c.child_id == child_id,
                        )
                    )
                )
                return result.rowcount > 0

        except Exception as e:
            raise StorageConnectionError(
                self.backend_name, f"Failed to remove relationship: {e!s}"
            ) from e

    def get_all_parents_of_node(self, node_id: str) -> list[Node]:
        """Retrieve all direct parent nodes for the given node from SQLite."""
        try:
            with self._get_session() as session:
                # Verify node exists first
                if not session.get(Node, node_id):
                    raise NodeNotFoundError(node_id, self.backend_name)

                # Query for parents
                query = (
                    select(Node)
                    .join(links, Node.id == links.c.parent_id)
                    .where(links.c.child_id == node_id)
                    .order_by(Node.title)
                )

                return list(session.execute(query).scalars().all())

        except NodeNotFoundError:
            raise
        except Exception as e:
            raise StorageConnectionError(
                self.backend_name,
                f"Failed to retrieve parents for node '{node_id}': {e!s}",
            ) from e

    def get_all_children_of_node(self, node_id: str) -> list[Node]:
        """Retrieve all direct child nodes for the given node from SQLite."""
        try:
            with self._get_session() as session:
                # Verify node exists first
                if not session.get(Node, node_id):
                    raise NodeNotFoundError(node_id, self.backend_name)

                # Query for children
                query = (
                    select(Node)
                    .join(links, Node.id == links.c.child_id)
                    .where(links.c.parent_id == node_id)
                    .order_by(Node.title)
                )

                return list(session.execute(query).scalars().all())

        except NodeNotFoundError:
            raise
        except Exception as e:
            raise StorageConnectionError(
                self.backend_name,
                f"Failed to retrieve children for node '{node_id}': {e!s}",
            ) from e

    def count_nodes_in_storage(self) -> int:
        """Count the total number of nodes currently stored in SQLite."""
        try:
            with self._get_session() as session:
                result = session.execute(select(func.count(Node.id)))
                return result.scalar() or 0

        except Exception as e:
            raise StorageConnectionError(
                self.backend_name, f"Failed to count nodes: {e!s}"
            ) from e

    def storage_is_healthy(self) -> bool:
        """Check if SQLite storage is healthy and accessible."""
        try:
            if not self._is_connected:
                return False

            # Check if database file is accessible
            if not self.database_path.exists():
                return False

            with self._get_session() as session:
                session.execute(text("SELECT 1"))
                return True

        except Exception:
            return False

    # Helper methods for complex operations

    def _attach_labels_to_node(
        self, session: Session, node: Node, labels_data: list[str]
    ) -> None:
        """Attach labels to a node, creating label records if needed."""
        for label_text in labels_data:
            label = session.get(Label, label_text)
            if not label:
                label = Label(label=label_text)
                session.add(label)
                session.flush()  # Get the label without committing

            node.labels.append(label)

    def _attach_command_to_node(
        self, session: Session, node: Node, command_data: dict[str, Any]
    ) -> None:
        """Attach command details to a Command layer node."""
        command = Command(
            node_id=node.id,
            ac_ref=command_data.get("ac_ref"),
            run=command_data.get("run"),
        )
        session.add(command)

        # Handle artifacts if present
        artifacts_data = command_data.get("artifacts", [])
        for artifact_text in artifacts_data:
            artifact = Artifact(artifact=artifact_text, command_id=node.id)
            session.add(artifact)

    def _attach_relationships_to_node(
        self,
        session: Session,
        node: Node,
        parents_data: list[str],
        children_data: list[str],
    ) -> None:
        """Attach parent-child relationships to a node."""
        # Add parent relationships
        for parent_id in parents_data:
            if session.get(Node, parent_id):  # Verify parent exists
                session.execute(
                    Link.insert().values(parent_id=parent_id, child_id=node.id)
                )

        # Add child relationships
        for child_id in children_data:
            if session.get(Node, child_id):  # Verify child exists
                session.execute(
                    Link.insert().values(parent_id=node.id, child_id=child_id)
                )

    def _update_node_labels(
        self, session: Session, node: Node, labels_data: list[str]
    ) -> None:
        """Update node labels by replacing all existing labels."""
        # Clear existing labels
        node.labels.clear()

        # Add new labels
        self._attach_labels_to_node(session, node, labels_data)

    def _update_node_command(
        self, session: Session, node: Node, command_data: dict[str, Any]
    ) -> None:
        """Update or create command details for a Command layer node."""
        # Delete existing command and artifacts
        session.execute(delete(Command).where(Command.c.node_id == node.id))

        # Create new command if data provided
        if command_data:
            self._attach_command_to_node(session, node, command_data)

    def _update_node_relationships(
        self,
        session: Session,
        node: Node,
        parents_data: list[str],
        children_data: list[str],
    ) -> None:
        """Update node relationships by replacing all existing ones."""
        # Clear existing relationships
        session.execute(
            delete(Link).where(
                or_(links.c.parent_id == node.id, links.c.child_id == node.id)
            )
        )

        # Add new relationships
        self._attach_relationships_to_node(
            session, node, parents_data, children_data
        )
