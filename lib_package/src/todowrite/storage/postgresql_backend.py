from __future__ import annotations

import logging
from contextlib import contextmanager
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
from sqlalchemy.pool import QueuePool

from ..database.models import Artifact, Command, Label, Link, Node, node_labels
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


class PostgreSQLBackend(StorageBackend):
    """
    PostgreSQL storage backend with connection pooling and robust error handling.

    This backend provides persistent storage for ToDoWrite nodes using PostgreSQL
    with connection pooling for optimal performance in concurrent environments.
    """

    def __init__(
        self, database_url: str, pool_size: int = 10, max_overflow: int = 20
    ):
        """
        Initialize PostgreSQL backend with connection pooling configuration.

        Args:
            database_url: Full PostgreSQL connection URL (e.g., 'postgresql://user:pass@host:port/db')
            pool_size: Number of connections to maintain in the pool
            max_overflow: Maximum number of connections that can overflow the pool
        """
        self.database_url = database_url
        self.pool_size = pool_size
        self.max_overflow = max_overflow
        self.engine: Engine | None = None
        self.Session: sessionmaker | None = None
        self._is_connected = False

    @property
    def backend_name(self) -> str:
        """Return the human-readable name of this storage backend."""
        return "PostgreSQL"

    def connect_to_storage(self) -> None:
        """Establish connection to PostgreSQL with optimized connection pooling."""
        try:
            # Create engine with connection pooling tuned for PostgreSQL
            self.engine = create_engine(
                self.database_url,
                poolclass=QueuePool,
                pool_size=self.pool_size,
                max_overflow=self.max_overflow,
                pool_pre_ping=True,  # Validate connections before use
                pool_recycle=3600,  # Recycle connections after 1 hour
                echo=False,  # Set to True for SQL logging in development
            )

            # Configure session factory
            self.Session = sessionmaker(
                bind=self.engine,
                expire_on_commit=False,  # Keep objects accessible after commit
            )

            # Test the connection using session directly
            test_session = self.Session()
            test_session.execute(text("SELECT 1"))
            test_session.commit()
            test_session.close()

            self._is_connected = True
            logger.info(
                f"Connected to PostgreSQL database: {self.database_url}"
            )

        except Exception as e:
            self._is_connected = False
            raise StorageConnectionError(
                self.backend_name, f"Failed to connect to PostgreSQL: {e!s}"
            )

    def disconnect_from_storage(self) -> None:
        """Close PostgreSQL connection pool and cleanup resources."""
        if self.engine:
            self.engine.dispose()
            self.engine = None
            self.Session = None
            self._is_connected = False
            logger.info("Disconnected from PostgreSQL database")

    @contextmanager
    def _get_session(self):
        """Context manager for database sessions with proper error handling."""
        if not self._is_connected or not self.Session:
            raise StorageConnectionError(
                self.backend_name,
                "Not connected to database - call connect_to_storage() first",
            )

        session = self.Session()
        try:
            yield session
            session.commit()
        except Exception as e:
            session.rollback()
            logger.error(f"Database session error: {e}")
            raise
        finally:
            session.close()

    def create_new_node(self, node_data: dict[str, Any]) -> NodeCreationResult:
        """Create a new node in PostgreSQL with all its relationships."""
        try:
            with self._get_session() as session:
                # Check if node already exists
                existing_node = session.get(Node, node_data["id"])
                if existing_node:
                    return NodeCreationResult(
                        created_node=existing_node, was_newly_created=False
                    )

                # Extract related data from node_data
                labels_data = node_data.pop("labels", [])
                command_data = node_data.pop("command", None)
                parents_data = node_data.pop("parents", [])
                children_data = node_data.pop("children", [])

                # Create the main node
                new_node = Node(**node_data)
                session.add(new_node)

                # Handle labels
                if labels_data:
                    self._attach_labels_to_node(session, new_node, labels_data)

                # Handle command if this is a Command layer
                if command_data and new_node.layer == "Command":
                    self._attach_command_to_node(
                        session, new_node, command_data
                    )

                # Handle parent-child relationships
                if parents_data or children_data:
                    self._attach_relationships_to_node(
                        session, new_node, parents_data, children_data
                    )

                session.flush()  # Get the node ID without committing
                session.refresh(new_node)

                return NodeCreationResult(
                    created_node=new_node, was_newly_created=True
                )

        except Exception as e:
            raise NodeCreationError(
                node_data.get("id", "unknown"),
                f"Database creation failed: {e!s}",
                self.backend_name,
            )

    def retrieve_node_by_id(self, node_id: str) -> Node:
        """Retrieve a node from PostgreSQL by its unique identifier."""
        try:
            with self._get_session() as session:
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
            )

    def update_existing_node(
        self, node_id: str, update_data: dict[str, Any]
    ) -> Node:
        """Update an existing node in PostgreSQL with new data."""
        try:
            with self._get_session() as session:
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

                session.flush()
                session.refresh(node)
                return node

        except NodeNotFoundError:
            raise
        except Exception as e:
            raise NodeUpdateError(
                node_id, f"Database update failed: {e!s}", self.backend_name
            )

    def remove_node_by_id(self, node_id: str) -> bool:
        """Remove a node from PostgreSQL and clean up all its relationships."""
        try:
            with self._get_session() as session:
                node = session.get(Node, node_id)
                if not node:
                    return False  # Node didn't exist, nothing to remove

                # Delete relationships first (foreign key constraints)
                session.execute(
                    delete(Link).where(
                        or_(
                            Link.c.parent_id == node_id,
                            Link.c.child_id == node_id,
                        )
                    )
                )

                # Delete label associations
                session.execute(
                    delete(node_labels).where(node_labels.c.node_id == node_id)
                )

                # Delete command if it exists
                session.execute(
                    delete(Command).where(Command.c.node_id == node_id)
                )

                # Finally delete the node
                session.delete(node)
                return True

        except Exception as e:
            raise NodeDeletionError(
                node_id, f"Database deletion failed: {e!s}", self.backend_name
            )

    def list_all_nodes_in_layer(
        self, layer_name: str | None = None
    ) -> list[Node]:
        """List all nodes in PostgreSQL, optionally filtered by layer."""
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
            )

    def search_nodes_by_criteria(
        self, search_criteria: dict[str, Any]
    ) -> list[Node]:
        """Search for nodes in PostgreSQL matching the provided criteria."""
        try:
            with self._get_session() as session:
                query = select(Node)

                # Build search conditions
                conditions = []
                for field, value in search_criteria.items():
                    if hasattr(Node, field):
                        if isinstance(value, str):
                            conditions.append(
                                getattr(Node, field).ilike(f"%{value}%")
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
                f"Database search failed: {e!s}",
                self.backend_name,
            )

    def create_parent_child_relationship(
        self, parent_id: str, child_id: str
    ) -> RelationshipCreationResult:
        """Create a parent-child relationship between two nodes in PostgreSQL."""
        try:
            with self._get_session() as session:
                # Verify both nodes exist
                parent_node = session.get(Node, parent_id)
                child_node = session.get(Node, child_id)

                if not parent_node:
                    raise NodeNotFoundError(parent_id, self.backend_name)
                if not child_node:
                    raise NodeNotFoundError(child_id, self.backend_name)

                # Check if relationship already exists
                existing_link = session.execute(
                    select(Link).where(
                        and_(
                            Link.c.parent_id == parent_id,
                            Link.c.child_id == child_id,
                        )
                    )
                ).first()

                if existing_link:
                    return RelationshipCreationResult(
                        parent_id=parent_id,
                        child_id=child_id,
                        was_newly_linked=False,
                    )

                # Create the relationship
                session.execute(
                    Link.insert().values(
                        parent_id=parent_id, child_id=child_id
                    )
                )

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
                f"Database relationship creation failed: {e!s}",
                self.backend_name,
            )

    def remove_parent_child_relationship(
        self, parent_id: str, child_id: str
    ) -> bool:
        """Remove a parent-child relationship between two nodes in PostgreSQL."""
        try:
            with self._get_session() as session:
                result = session.execute(
                    delete(Link).where(
                        and_(
                            Link.c.parent_id == parent_id,
                            Link.c.child_id == child_id,
                        )
                    )
                )
                return result.rowcount > 0

        except Exception as e:
            raise StorageConnectionError(
                self.backend_name, f"Failed to remove relationship: {e!s}"
            )

    def get_all_parents_of_node(self, node_id: str) -> list[Node]:
        """Retrieve all direct parent nodes for the given node from PostgreSQL."""
        try:
            with self._get_session() as session:
                # Verify node exists first
                if not session.get(Node, node_id):
                    raise NodeNotFoundError(node_id, self.backend_name)

                # Query for parents
                query = (
                    select(Node)
                    .join(Link, Node.id == Link.c.parent_id)
                    .where(Link.c.child_id == node_id)
                    .order_by(Node.title)
                )

                return list(session.execute(query).scalars().all())

        except NodeNotFoundError:
            raise
        except Exception as e:
            raise StorageConnectionError(
                self.backend_name,
                f"Failed to retrieve parents for node '{node_id}': {e!s}",
            )

    def get_all_children_of_node(self, node_id: str) -> list[Node]:
        """Retrieve all direct child nodes for the given node from PostgreSQL."""
        try:
            with self._get_session() as session:
                # Verify node exists first
                if not session.get(Node, node_id):
                    raise NodeNotFoundError(node_id, self.backend_name)

                # Query for children
                query = (
                    select(Node)
                    .join(Link, Node.id == Link.c.child_id)
                    .where(Link.c.parent_id == node_id)
                    .order_by(Node.title)
                )

                return list(session.execute(query).scalars().all())

        except NodeNotFoundError:
            raise
        except Exception as e:
            raise StorageConnectionError(
                self.backend_name,
                f"Failed to retrieve children for node '{node_id}': {e!s}",
            )

    def count_nodes_in_storage(self) -> int:
        """Count the total number of nodes currently stored in PostgreSQL."""
        try:
            with self._get_session() as session:
                result = session.execute(select(func.count(Node.id)))
                return result.scalar() or 0

        except Exception as e:
            raise StorageConnectionError(
                self.backend_name, f"Failed to count nodes: {e!s}"
            )

    def storage_is_healthy(self) -> bool:
        """Check if PostgreSQL storage is healthy and accessible."""
        try:
            if not self._is_connected:
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
                or_(Link.c.parent_id == node.id, Link.c.child_id == node.id)
            )
        )

        # Add new relationships
        self._attach_relationships_to_node(
            session, node, parents_data, children_data
        )
