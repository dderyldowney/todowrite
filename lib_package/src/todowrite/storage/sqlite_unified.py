"""Simplified SQLite backend working directly with core.types.Node.

This implementation eliminates conversion complexity by working with Node objects
throughout and using simple SQL for persistence.
"""

from __future__ import annotations

import logging
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

from ..core.types import Node
from ..database.node_mapping import (
    Base,
    NodeTable,
    artifacts,
    commands,
    labels,
    links,
    node_labels,
)
from .backends import (
    NodeCreationError,
    NodeCreationResult,
    NodeDeletionError,
    NodeNotFoundError,
    NodeUpdateError,
    RelationshipCreationResult,
    RelationshipError,
    StorageConnectionError,
    StorageQueryError,
)

logger = logging.getLogger(__name__)


class SQLiteUnifiedBackend:
    """
    Simplified SQLite backend that works directly with core.types.Node.

    This implementation eliminates the complex ORM conversions and works with
    Node objects throughout, using simple SQL for persistence.
    """

    def __init__(self, database_path: str | Path):
        """
        Initialize SQLite backend with database file path.
        """
        self.database_path = Path(database_path)
        self.database_url = f"sqlite:///{self.database_path}"
        self.engine: Engine | None = None
        self.Session: sessionmaker[Session] | None = None
        self._is_connected = False

        # Ensure parent directory exists
        self.database_path.parent.mkdir(parents=True, exist_ok=True)

    @property
    def backend_name(self) -> str:
        """Return the human-readable name of this storage backend."""
        return "SQLite"

    def connect_to_storage(self) -> None:
        """Establish connection to SQLite database."""
        try:
            # Create engine
            self.engine = create_engine(
                self.database_url,
                echo=False,
                connect_args={
                    "check_same_thread": False,
                    "timeout": 30,
                },
                pool_pre_ping=True,
            )

            # Configure session factory
            self.Session = sessionmaker(
                bind=self.engine,
                expire_on_commit=False,
            )

            # Create tables
            Base.metadata.create_all(self.engine)

            # Test connection
            test_session = self.Session()
            test_session.execute(text("SELECT 1"))
            test_session.commit()
            test_session.close()

            self._is_connected = True
            logger.info(f"Connected to SQLite database: {self.database_path}")

        except (OSError, ValueError, RuntimeError) as e:
            self._is_connected = False
            raise StorageConnectionError(
                self.backend_name,
                f"Failed to connect to SQLite database at {self.database_path}: {e!s}",
            )

    def disconnect_from_storage(self) -> None:
        """Close SQLite connection."""
        if self.engine:
            self.engine.dispose()
            self.engine = None
            self.Session = None
            self._is_connected = False
            logger.info("Disconnected from SQLite database")

    @contextmanager
    def _get_session(self):
        """Get database session with proper error handling."""
        if not self._is_connected or not self.Session:
            raise StorageConnectionError(
                self.backend_name,
                "Not connected to database - call connect_to_storage() first",
            )

        session = self.Session()
        try:
            session.execute(text("PRAGMA foreign_keys = ON"))
            yield session
            session.commit()
        except Exception as e:
            session.rollback()
            logger.error(f"SQLite session error: {e}")
            raise
        finally:
            session.close()

    def create_new_node(self, app_node: Node) -> NodeCreationResult:
        """Create a new node in storage."""
        try:
            with self._get_session() as session:
                # Check if node already exists
                existing = session.get(NodeTable, app_node.id)
                if existing:
                    # Load relationships and return existing node
                    loaded_node = self._load_node_with_relationships(
                        session, app_node.id
                    )
                    return NodeCreationResult(
                        created_node=loaded_node, was_newly_created=False
                    )

                # Insert main node data
                db_node = NodeTable(
                    id=app_node.id,
                    layer=app_node.layer,
                    title=app_node.title,
                    description=app_node.description,
                    status=app_node.status,
                    progress=app_node.progress,
                    started_date=app_node.started_date,
                    completion_date=app_node.completion_date,
                    owner=app_node.metadata.owner,
                    severity=app_node.metadata.severity,
                    work_type=app_node.metadata.work_type,
                    assignee=app_node.metadata.assignee,
                )
                session.add(db_node)

                # Insert labels
                for label in app_node.metadata.labels:
                    session.execute(labels.insert().values(label=label))
                    session.execute(
                        node_labels.insert().values(
                            node_id=app_node.id, label=label
                        )
                    )

                # Insert command if present
                if app_node.command:
                    session.execute(
                        commands.insert().values(
                            node_id=app_node.id,
                            ac_ref=app_node.command.get("ac_ref", ""),
                            run=app_node.command.get("run", ""),
                        )
                    )
                    # Insert artifacts
                    for artifact in app_node.command.get("artifacts", []):
                        session.execute(
                            artifacts.insert().values(
                                artifact=artifact, command_id=app_node.id
                            )
                        )

                # Insert relationships
                for parent_id in app_node.links.parents:
                    session.execute(
                        links.insert().values(
                            parent_id=parent_id, child_id=app_node.id
                        )
                    )
                for child_id in app_node.links.children:
                    session.execute(
                        links.insert().values(
                            parent_id=app_node.id, child_id=child_id
                        )
                    )

                return NodeCreationResult(
                    created_node=app_node, was_newly_created=True
                )

        except (ValueError, KeyError, AttributeError) as e:
            raise NodeCreationError(
                app_node.id,
                f"SQLite creation failed: {e!s}",
                self.backend_name,
            )

    def retrieve_node_by_id(self, node_id: str) -> Node:
        """Retrieve a node by ID."""
        try:
            with self._get_session() as session:
                return self._load_node_with_relationships(session, node_id)

        except (ValueError, KeyError, AttributeError) as e:
            if "not found" in str(e).lower():
                raise NodeNotFoundError(node_id, self.backend_name)
            raise StorageConnectionError(
                self.backend_name,
                f"Failed to retrieve node '{node_id}': {e!s}",
            )

    def _load_node_with_relationships(
        self, session: Session, node_id: str
    ) -> Node:
        """Load a complete Node with all relationships."""
        # Get main node data
        db_node = session.get(NodeTable, node_id)
        if not db_node:
            raise NodeNotFoundError(node_id, self.backend_name)

        # Get labels
        label_rows = (
            session.execute(
                select(node_labels.c.label).where(
                    node_labels.c.node_id == node_id
                )
            )
            .scalars()
            .all()
        )

        # Get parents
        parent_rows = (
            session.execute(
                select(links.c.parent_id).where(links.c.child_id == node_id)
            )
            .scalars()
            .all()
        )

        # Get children
        child_rows = (
            session.execute(
                select(links.c.child_id).where(links.c.parent_id == node_id)
            )
            .scalars()
            .all()
        )

        # Get command
        command_row = session.execute(
            select(commands).where(commands.c.node_id == node_id)
        ).first()

        # Get artifacts for command
        artifact_rows = []
        if command_row:
            artifact_rows = (
                session.execute(
                    select(artifacts.c.artifact).where(
                        artifacts.c.command_id == node_id
                    )
                )
                .scalars()
                .all()
            )

        # Build Node object
        from ..core.types import Link, Metadata

        command = None
        if command_row:
            command = {
                "ac_ref": command_row.ac_ref or "",
                "run": command_row.run or "",
                "artifacts": list(artifact_rows),
            }

        return Node(
            id=db_node.id,
            layer=db_node.layer,
            title=db_node.title,
            description=db_node.description or "",
            status=db_node.status or "planned",
            progress=db_node.progress or 0,
            started_date=db_node.started_date,
            completion_date=db_node.completion_date,
            links=Link(parents=list(parent_rows), children=list(child_rows)),
            metadata=Metadata(
                owner=db_node.owner or "system",
                labels=list(label_rows),
                severity=db_node.severity or "low",
                work_type=db_node.work_type or "chore",
                assignee=db_node.assignee or "",
            ),
            command=command,
        )

    def update_existing_node(self, app_node: Node) -> Node:
        """Update an existing node."""
        try:
            with self._get_session() as session:
                # Check if node exists
                existing = session.get(NodeTable, app_node.id)
                if not existing:
                    raise NodeNotFoundError(app_node.id, self.backend_name)

                # Update main node data
                existing.layer = app_node.layer
                existing.title = app_node.title
                existing.description = app_node.description
                existing.status = app_node.status
                existing.progress = app_node.progress
                existing.started_date = app_node.started_date
                existing.completion_date = app_node.completion_date
                existing.owner = app_node.metadata.owner
                existing.severity = app_node.metadata.severity
                existing.work_type = app_node.metadata.work_type
                existing.assignee = app_node.metadata.assignee

                # Clear existing relationships
                session.execute(
                    delete(node_labels).where(
                        node_labels.c.node_id == app_node.id
                    )
                )
                session.execute(
                    delete(commands).where(commands.c.node_id == app_node.id)
                )
                session.execute(
                    delete(links).where(
                        or_(
                            links.c.parent_id == app_node.id,
                            links.c.child_id == app_node.id,
                        )
                    )
                )

                # Re-insert updated relationships
                for label in app_node.metadata.labels:
                    session.execute(labels.insert().values(label=label))
                    session.execute(
                        node_labels.insert().values(
                            node_id=app_node.id, label=label
                        )
                    )

                # Re-insert command
                if app_node.command:
                    session.execute(
                        commands.insert().values(
                            node_id=app_node.id,
                            ac_ref=app_node.command.get("ac_ref", ""),
                            run=app_node.command.get("run", ""),
                        )
                    )
                    for artifact in app_node.command.get("artifacts", []):
                        session.execute(
                            artifacts.insert().values(
                                artifact=artifact, command_id=app_node.id
                            )
                        )

                # Re-insert relationships
                for parent_id in app_node.links.parents:
                    session.execute(
                        links.insert().values(
                            parent_id=parent_id, child_id=app_node.id
                        )
                    )
                for child_id in app_node.links.children:
                    session.execute(
                        links.insert().values(
                            parent_id=app_node.id, child_id=child_id
                        )
                    )

                return app_node

        except NodeNotFoundError:
            raise
        except (ValueError, KeyError, AttributeError) as e:
            raise NodeUpdateError(
                app_node.id, f"SQLite update failed: {e!s}", self.backend_name
            )

    def remove_node_by_id(self, node_id: str) -> bool:
        """Remove a node."""
        try:
            with self._get_session() as session:
                # Check if node exists
                existing = session.get(NodeTable, node_id)
                if not existing:
                    return False

                # Delete relationships first
                session.execute(
                    delete(node_labels).where(node_labels.c.node_id == node_id)
                )
                session.execute(
                    delete(commands).where(commands.c.node_id == node_id)
                )
                session.execute(
                    delete(links).where(
                        or_(
                            links.c.parent_id == node_id,
                            links.c.child_id == node_id,
                        )
                    )
                )

                # Delete main node
                session.delete(existing)
                return True

        except (ValueError, KeyError, AttributeError) as e:
            raise NodeDeletionError(
                node_id, f"SQLite deletion failed: {e!s}", self.backend_name
            )

    def create_parent_child_relationship(
        self, parent_id: str, child_id: str
    ) -> RelationshipCreationResult:
        """Create parent-child relationship."""
        try:
            with self._get_session() as session:
                # Verify both nodes exist
                parent_exists = session.get(NodeTable, parent_id)
                child_exists = session.get(NodeTable, child_id)

                if not parent_exists:
                    raise NodeNotFoundError(parent_id, self.backend_name)
                if not child_exists:
                    raise NodeNotFoundError(child_id, self.backend_name)

                # Check if relationship already exists
                existing = session.execute(
                    select(links).where(
                        and_(
                            links.c.parent_id == parent_id,
                            links.c.child_id == child_id,
                        )
                    )
                ).first()

                if existing:
                    return RelationshipCreationResult(
                        parent_id=parent_id,
                        child_id=child_id,
                        was_newly_linked=False,
                    )

                # Create relationship
                session.execute(
                    links.insert().values(
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
                f"SQLite relationship creation failed: {e!s}",
                self.backend_name,
            )

    def remove_parent_child_relationship(
        self, parent_id: str, child_id: str
    ) -> bool:
        """Remove parent-child relationship."""
        try:
            with self._get_session() as session:
                result = session.execute(
                    delete(links).where(
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
            )

    def list_all_nodes_in_layer(
        self, layer_name: str | None = None
    ) -> list[Node]:
        """List nodes, optionally filtered by layer."""
        try:
            with self._get_session() as session:
                query = select(NodeTable)
                if layer_name:
                    query = query.where(NodeTable.layer == layer_name)
                query = query.order_by(NodeTable.layer, NodeTable.title)

                db_nodes = session.execute(query).scalars().all()
                return [
                    self._load_node_with_relationships(session, node.id)
                    for node in db_nodes
                ]

        except Exception as e:
            raise StorageConnectionError(
                self.backend_name, f"Failed to list nodes: {e!s}"
            )

    def get_all_children_of_node(self, node_id: str) -> list[Node]:
        """Get children of a node."""
        try:
            with self._get_session() as session:
                # Verify node exists
                if not session.get(NodeTable, node_id):
                    raise NodeNotFoundError(node_id, self.backend_name)

                child_rows = (
                    session.execute(
                        select(links.c.child_id).where(
                            links.c.parent_id == node_id
                        )
                    )
                    .scalars()
                    .all()
                )

                return [
                    self._load_node_with_relationships(session, child_id)
                    for child_id in child_rows
                ]

        except NodeNotFoundError:
            raise
        except Exception as e:
            raise StorageConnectionError(
                self.backend_name,
                f"Failed to get children for node '{node_id}': {e!s}",
            )

    def get_all_parents_of_node(self, node_id: str) -> list[Node]:
        """Get parents of a node."""
        try:
            with self._get_session() as session:
                # Verify node exists
                if not session.get(NodeTable, node_id):
                    raise NodeNotFoundError(node_id, self.backend_name)

                parent_rows = (
                    session.execute(
                        select(links.c.parent_id).where(
                            links.c.child_id == node_id
                        )
                    )
                    .scalars()
                    .all()
                )

                return [
                    self._load_node_with_relationships(session, parent_id)
                    for parent_id in parent_rows
                ]

        except NodeNotFoundError:
            raise
        except Exception as e:
            raise StorageConnectionError(
                self.backend_name,
                f"Failed to get parents for node '{node_id}': {e!s}",
            )

    def count_nodes_in_storage(self) -> int:
        """Count total nodes."""
        try:
            with self._get_session() as session:
                result = session.execute(select(func.count(NodeTable.id)))
                return result.scalar() or 0

        except Exception as e:
            raise StorageConnectionError(
                self.backend_name, f"Failed to count nodes: {e!s}"
            )

    def search_nodes_by_criteria(
        self, search_criteria: dict[str, Any]
    ) -> list[Node]:
        """Search nodes by criteria."""
        try:
            with self._get_session() as session:
                query = select(NodeTable)

                conditions = []
                for field, value in search_criteria.items():
                    if hasattr(NodeTable, field):
                        if isinstance(value, str):
                            conditions.append(
                                getattr(NodeTable, field).like(f"%{value}%")
                            )
                        else:
                            conditions.append(
                                getattr(NodeTable, field) == value
                            )

                if conditions:
                    query = query.where(and_(*conditions))

                query = query.order_by(NodeTable.layer, NodeTable.title)
                db_nodes = session.execute(query).scalars().all()
                return [
                    self._load_node_with_relationships(session, node.id)
                    for node in db_nodes
                ]

        except Exception as e:
            raise StorageQueryError(
                str(search_criteria),
                f"SQLite search failed: {e!s}",
                self.backend_name,
            )

    def storage_is_healthy(self) -> bool:
        """Check storage health."""
        try:
            if not self._is_connected:
                return False

            if not self.database_path.exists():
                return False

            with self._get_session() as session:
                session.execute(text("SELECT 1"))
                return True

        except Exception:
            return False
