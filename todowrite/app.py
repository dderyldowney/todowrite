"""
This module contains the core ToDoWrite application class.
"""

from __future__ import annotations

import json
import os
import uuid
from collections import defaultdict
from collections.abc import Generator
from contextlib import contextmanager
from pathlib import Path

# Forward declaration for type hints
from typing import TYPE_CHECKING, Any, cast

import jsonschema
from sqlalchemy import create_engine, delete, select
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session, joinedload, sessionmaker

from .db.config import (
    StoragePreference,
    StorageType,
    determine_storage_backend,
    set_storage_preference,
)
from .db.models import Artifact as DBArtifact
from .db.models import Base
from .db.models import Command as DBCommand
from .db.models import Label as DBLabel
from .db.models import Link as DBLink
from .db.models import Node as DBNode
from .schema_validator import validate_database_schema
from .types import Command, LayerType, Link, Metadata, Node, StatusType

if TYPE_CHECKING:
    from .yaml_storage import YAMLStorage


def _validate_literal(value: str, literal_type: Any) -> str:
    if value not in literal_type.__args__:
        raise ValueError(
            f"Invalid literal value: {value}. Expected one of {literal_type.__args__}"
        )
    return value


class ToDoWrite:
    """The main ToDoWrite application class."""

    _SCHEMA: dict[str, Any] | None = None

    def __init__(
        self,
        db_url: str | None = None,
        auto_import: bool = True,
        storage_preference: StoragePreference | None = None,
    ):
        """Initializes the ToDoWrite application."""

        # Set storage preference if provided
        if storage_preference:
            set_storage_preference(storage_preference)

        # Determine storage backend
        self.storage_type, self.db_url = determine_storage_backend()

        # Initialize attributes with proper types
        self.engine: Engine | None = None
        self.Session: sessionmaker[Session] | None = None
        self.yaml_storage: YAMLStorage | None = None

        # Override URL if explicitly provided
        if db_url:
            self.db_url = db_url
            self.storage_type = (
                StorageType.POSTGRESQL
                if db_url.startswith("postgresql:")
                else StorageType.SQLITE
            )

        # Initialize database components only if not using YAML
        if self.storage_type != StorageType.YAML and self.db_url:
            self.engine = create_engine(self.db_url)
            self.Session = sessionmaker(bind=self.engine)
        else:
            self.engine = None
            self.Session = None

        # Load schema
        if ToDoWrite._SCHEMA is None:
            schema_path = Path(__file__).parent / "schemas" / "todowrite.schema.json"
            with open(schema_path) as f:
                ToDoWrite._SCHEMA = json.load(f)

        # Initialize YAML storage if using YAML mode
        if self.storage_type == StorageType.YAML:
            from .schema_validator import validate_yaml_files
            from .yaml_storage import YAMLStorage

            self.yaml_storage = YAMLStorage()

            # Validate YAML files schema
            try:
                is_valid, errors, file_counts = validate_yaml_files()
                if not is_valid:
                    error_msg = "YAML schema validation failed:\n" + "\n".join(
                        f"  - {error}" for error in errors
                    )
                    print(f"⚠️  {error_msg}")
                else:
                    print(
                        f"✅ YAML schema validation passed (checked {sum(file_counts.values())} files)"
                    )

                    # Report file counts by layer
                    if file_counts:
                        print("  Files by layer:")
                        for layer, count in file_counts.items():
                            if count > 0:
                                print(f"    {layer}: {count} files")
            except Exception as e:
                print(f"⚠️  YAML validation error: {e}")
        else:
            self.yaml_storage = None

        # Auto-import YAML files if enabled and using database
        if auto_import and self.storage_type != StorageType.YAML:
            self._auto_import_yaml_files()

    @contextmanager
    def get_session(self) -> Generator[Session | None, None, None]:
        if self.storage_type == StorageType.YAML:
            # YAML storage doesn't use sessions
            yield None
            return

        if self.Session is None:
            raise RuntimeError("Database session not initialized")

        session = self.Session()
        try:
            yield session
            session.commit()
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()

    @contextmanager
    def get_db_session(self) -> Generator[Session, None, None]:
        """Get a database session that is guaranteed to not be None."""
        if self.storage_type == StorageType.YAML:
            raise RuntimeError("Database session requested but using YAML storage")

        if self.Session is None:
            raise RuntimeError("Database session not initialized")

        session = self.Session()
        try:
            yield session
            session.commit()
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()

    def _validate_node_data(self, node_data: dict[str, Any]) -> None:
        """Validates node data against the ToDoWrite schema."""
        if ToDoWrite._SCHEMA is None:
            raise ValueError("Schema not loaded. Cannot validate node data.")
        try:
            jsonschema.validate(instance=node_data, schema=ToDoWrite._SCHEMA)
        except jsonschema.exceptions.ValidationError as e:
            raise ValueError(f"Node data validation failed: {e.message}") from e

    def _get_yaml_storage(self) -> YAMLStorage:
        """Get YAML storage with proper error handling."""
        if not self.yaml_storage:
            raise RuntimeError("YAML storage not initialized")
        return self.yaml_storage

    def _execute_with_session(self, func: Any, *args: Any, **kwargs: Any) -> Any:
        """Execute a function with a database session, handling None checks."""
        with self.get_session() as session:
            if session is None:
                raise RuntimeError("Database session not available")
            return func(session, *args, **kwargs)

    def init_database(self) -> None:
        """Creates the database and the tables."""
        if self.storage_type == StorageType.YAML:
            # For YAML storage, just ensure directories exist
            if self.yaml_storage:
                self.yaml_storage._ensure_directories()
            return

        if self.db_url and self.db_url.startswith("sqlite"):
            db_path: str = self.db_url.split("///")[1]
            if db_path and db_path != ":memory:":
                dirname: str = os.path.dirname(db_path)
                if dirname:
                    os.makedirs(dirname, exist_ok=True)
        if self.engine:
            Base.metadata.create_all(bind=self.engine)

            # Validate database schema AFTER tables are created
            is_valid, errors = validate_database_schema(self.engine)
            if not is_valid:
                error_msg = "Database schema validation failed:\n" + "\n".join(
                    f"  - {error}" for error in errors
                )
                print(f"⚠️  {error_msg}")
            else:
                print(
                    f"✅ {self.storage_type.value.capitalize()} schema validation passed"
                )

    def create_node(self, node_data: dict[str, Any]) -> Node:
        """Creates a new node in the storage backend."""
        self._validate_node_data(node_data)

        if self.storage_type == StorageType.YAML:
            # Convert node_data to Node and save to YAML
            yaml_storage = self._get_yaml_storage()
            node = self._dict_to_node(node_data)
            yaml_storage.save_node(node)
            return node

        with self.get_db_session() as session:
            db_node = self._create_db_node(session, node_data)
            return self._convert_db_node_to_node(db_node)

    def get_node(self, node_id: str) -> Node | None:
        """Retrieves a node from the storage backend."""
        if self.storage_type == StorageType.YAML:
            yaml_storage = self._get_yaml_storage()
            return yaml_storage.load_node(node_id)

        with self.get_db_session() as session:
            stmt = (
                select(DBNode)
                .options(
                    joinedload(DBNode.labels),
                    joinedload(DBNode.command).joinedload(DBCommand.artifacts),
                )
                .where(DBNode.id == node_id)
            )
            db_node = session.execute(stmt).unique().scalar_one_or_none()
            if db_node:
                return self._convert_db_node_to_node(db_node)
            return None

    def get_all_nodes(self) -> dict[str, list[Node]]:
        """Retrieves all the nodes from the storage backend."""
        if self.storage_type == StorageType.YAML:
            yaml_storage = self._get_yaml_storage()
            return yaml_storage.load_all_nodes()

        with self.get_db_session() as session:
            stmt = select(DBNode).options(
                joinedload(DBNode.labels),
                joinedload(DBNode.command).joinedload(DBCommand.artifacts),
            )
            db_nodes = session.execute(stmt).unique().scalars().all()
            nodes: dict[str, list[Node]] = {}
            for db_node in db_nodes:
                node = self._convert_db_node_to_node(db_node)
                if node.layer not in nodes:
                    nodes[node.layer] = []
                nodes[node.layer].append(node)
            return nodes

    def update_node(self, node_id: str, node_data: dict[str, Any]) -> Node | None:
        """Updates an existing node in the storage backend."""
        self._validate_node_data(node_data)

        if self.storage_type == StorageType.YAML:
            # For YAML, just save the updated node
            yaml_storage = self._get_yaml_storage()
            node = self._dict_to_node(node_data)
            yaml_storage.save_node(node)
            return node

        with self.get_db_session() as session:
            stmt = select(DBNode).where(DBNode.id == node_id)
            db_node = session.execute(stmt).scalar_one_or_none()
            if db_node:
                db_node.layer = node_data.get("layer", db_node.layer)
                db_node.title = node_data.get("title", db_node.title)
                db_node.description = node_data.get("description", db_node.description)
                db_node.status = node_data.get("status", db_node.status)
                db_node.progress = node_data.get("progress", db_node.progress)
                db_node.started_date = node_data.get(
                    "started_date", db_node.started_date
                )
                db_node.completion_date = node_data.get(
                    "completion_date", db_node.completion_date
                )
                db_node.owner = node_data.get("metadata", {}).get(
                    "owner", db_node.owner
                )
                db_node.severity = node_data.get("metadata", {}).get(
                    "severity", db_node.severity
                )
                db_node.work_type = node_data.get("metadata", {}).get(
                    "work_type", db_node.work_type
                )
                db_node.assignee = node_data.get("metadata", {}).get(
                    "assignee", db_node.assignee
                )

                # Update links
                parent_stmt = select(DBLink).where(DBLink.child_id == node_id)
                existing_parent_links = {
                    link.parent_id
                    for link in session.execute(parent_stmt).scalars().all()
                }
                child_stmt = select(DBLink).where(DBLink.parent_id == node_id)
                existing_child_links = {
                    link.child_id
                    for link in session.execute(child_stmt).scalars().all()
                }

                new_parent_ids = set(node_data["links"].get("parents", []))
                new_child_ids = set(node_data["links"].get("children", []))

                # Handle parent links
                parents_to_add = new_parent_ids - existing_parent_links
                parents_to_remove = existing_parent_links - new_parent_ids

                for parent_id in parents_to_add:
                    link = DBLink(parent_id=parent_id, child_id=db_node.id)
                    session.add(link)
                for parent_id in parents_to_remove:
                    delete_stmt = delete(DBLink).where(
                        DBLink.parent_id == parent_id, DBLink.child_id == node_id
                    )
                    session.execute(delete_stmt)

                # Handle child links
                children_to_add = new_child_ids - existing_child_links
                children_to_remove = existing_child_links - new_child_ids

                for child_id in children_to_add:
                    link = DBLink(parent_id=db_node.id, child_id=child_id)
                    session.add(link)
                for child_id in children_to_remove:
                    delete_stmt = delete(DBLink).where(
                        DBLink.parent_id == node_id, DBLink.child_id == child_id
                    )
                    session.execute(delete_stmt)

                # Update labels
                db_node.labels.clear()
                for label_text in node_data["metadata"].get("labels", []):
                    label_stmt = select(DBLabel).where(DBLabel.label == label_text)
                    label = session.execute(label_stmt).scalar_one_or_none()
                    if not label:
                        label = DBLabel(label=label_text)
                        session.add(label)
                    db_node.labels.append(label)

                # Update command
                if node_data.get("command"):
                    cmd_stmt = select(DBCommand).where(DBCommand.node_id == node_id)
                    db_command = session.execute(cmd_stmt).scalar_one_or_none()
                    if not db_command:
                        db_command = DBCommand(node_id=node_id)
                        session.add(db_command)
                    db_command.ac_ref = node_data["command"].get(
                        "ac_ref", db_command.ac_ref
                    )
                    db_command.run = json.dumps(
                        node_data["command"].get("run", db_command.run)
                    )

                    delete_artifacts_stmt = delete(DBArtifact).where(
                        DBArtifact.command_id == node_id
                    )
                    session.execute(delete_artifacts_stmt)
                    for artifact_text in node_data["command"].get("artifacts", []):
                        artifact = DBArtifact(
                            command_id=node_id, artifact=artifact_text
                        )
                        session.add(artifact)
                else:
                    delete_cmd_stmt = delete(DBCommand).where(
                        DBCommand.node_id == node_id
                    )
                    session.execute(delete_cmd_stmt)
                    delete_artifacts_stmt = delete(DBArtifact).where(
                        DBArtifact.command_id == node_id
                    )
                    session.execute(delete_artifacts_stmt)

                session.refresh(db_node)
                return self._convert_db_node_to_node(db_node)
            return None

    def delete_node(self, node_id: str) -> None:
        """Deletes a node from the storage backend."""
        if self.storage_type == StorageType.YAML:
            yaml_storage = self._get_yaml_storage()
            yaml_storage.delete_node(node_id)
            return

        with self.get_db_session() as session:
            stmt = select(DBNode).where(DBNode.id == node_id)
            db_node = session.execute(stmt).scalar_one_or_none()
            if db_node:
                session.delete(db_node)

    def update_node_status(self, node_id: str, status: str) -> Node | None:
        """Update a node's status using the default ToDoWrite instance."""
        status = cast(StatusType, status)
        node_data = {"status": status}
        return self.update_node(node_id, node_data)

    def search_nodes(self, query: str) -> dict[str, list[Node]]:
        """Search for nodes by query string."""
        all_nodes = self.get_all_nodes()
        results = {}

        for layer, nodes in all_nodes.items():
            matching_nodes = []
            for node in nodes:
                if (
                    query.lower() in node.title.lower()
                    or query.lower() in node.description.lower()
                    or query.lower() in node.id.lower()
                ):
                    matching_nodes.append(node)

            if matching_nodes:
                results[layer] = matching_nodes

        return results

    def export_nodes(self, format: str = "yaml") -> str:
        """Export all nodes to a string in the specified format."""
        all_nodes = self.get_all_nodes()

        if format.lower() == "yaml":
            import yaml

            nodes_list = []
            for _layer, nodes in all_nodes.items():
                for node in nodes:
                    nodes_list.append(node.to_dict())
            return yaml.dump(nodes_list, default_flow_style=False)

        elif format.lower() == "json":
            import json

            nodes_dict = {}
            for layer, nodes in all_nodes.items():
                nodes_dict[layer] = [node.to_dict() for node in nodes]
            return json.dumps(nodes_dict, indent=2)

        else:
            raise ValueError(f"Unsupported export format: {format}")

    def import_nodes(self, file_path: str) -> dict[str, Any]:
        """Import nodes from a file."""
        import json
        from pathlib import Path

        import yaml

        path = Path(file_path)
        if not path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")

        # Determine file format
        if path.suffix.lower() in [".yaml", ".yml"]:
            with open(path) as f:
                data = yaml.safe_load(f)
        elif path.suffix.lower() == ".json":
            with open(path) as f:
                data = json.load(f)
        else:
            raise ValueError(f"Unsupported file format: {path.suffix}")

        # Handle both single node and list of nodes
        if isinstance(data, dict) and "layer" in data:
            # Single node
            nodes_to_import = [data]
        elif isinstance(data, list):
            # List of nodes
            nodes_to_import = data
        else:
            raise ValueError(
                "Invalid file format: expected node object or list of nodes"
            )

        results: dict[str, Any] = {"imported": 0, "errors": [], "skipped": []}

        for node_data in nodes_to_import:
            try:
                # Generate ID if not provided
                if "id" not in node_data or not node_data["id"]:
                    layer = node_data.get("layer", "Node")
                    node_data["id"] = f"{layer}-{uuid.uuid4().hex[:12].upper()}"

                # Create the node
                self.create_node(node_data)
                results["imported"] += 1
            except Exception as e:
                results["errors"].append(str(e))

        return results

    def add_goal(
        self,
        title: str,
        description: str,
        owner: str = "system",
        labels: list[str] | None = None,
    ) -> Node:
        """Adds a new Goal node."""
        node_data = {
            "id": f"GOAL-{uuid.uuid4().hex[:12].upper()}",
            "layer": "Goal",
            "title": title,
            "description": description,
            "links": {"parents": [], "children": []},
            "metadata": {
                "owner": owner,
                "labels": labels or [],
                "severity": "",
                "work_type": "",
            },
        }
        return self.create_node(node_data)

    def add_phase(
        self,
        parent_id: str,
        title: str,
        description: str,
        owner: str = "system",
        labels: list[str] | None = None,
    ) -> Node:
        """Adds a new Phase node."""
        node_data = {
            "id": f"PH-{uuid.uuid4().hex[:12].upper()}",
            "layer": "Phase",
            "title": title,
            "description": description,
            "links": {"parents": [parent_id], "children": []},
            "metadata": {
                "owner": owner,
                "labels": labels or [],
                "severity": "",
                "work_type": "",
            },
        }
        return self.create_node(node_data)

    def add_step(
        self,
        parent_id: str,
        title: str,
        description: str,
        owner: str = "system",
        labels: list[str] | None = None,
    ) -> Node:
        """Adds a new Step node."""
        node_data = {
            "id": f"STP-{uuid.uuid4().hex[:12].upper()}",
            "layer": "Step",
            "title": title,
            "description": description,
            "links": {"parents": [parent_id], "children": []},
            "metadata": {
                "owner": owner,
                "labels": labels or [],
                "severity": "",
                "work_type": "",
            },
        }
        return self.create_node(node_data)

    def add_task(
        self,
        parent_id: str,
        title: str,
        description: str,
        owner: str = "system",
        labels: list[str] | None = None,
    ) -> Node:
        """Adds a new Task node."""
        node_data = {
            "id": f"TSK-{uuid.uuid4().hex[:12].upper()}",
            "layer": "Task",
            "title": title,
            "description": description,
            "links": {"parents": [parent_id], "children": []},
            "metadata": {
                "owner": owner,
                "labels": labels or [],
                "severity": "",
                "work_type": "",
            },
        }
        return self.create_node(node_data)

    def add_subtask(
        self,
        parent_id: str,
        title: str,
        description: str,
        owner: str = "system",
        labels: list[str] | None = None,
    ) -> Node:
        """Adds a new SubTask node."""
        node_data = {
            "id": f"SUB-{uuid.uuid4().hex[:12].upper()}",
            "layer": "SubTask",
            "title": title,
            "description": description,
            "links": {"parents": [parent_id], "children": []},
            "metadata": {
                "owner": owner,
                "labels": labels or [],
                "severity": "",
                "work_type": "",
            },
        }
        return self.create_node(node_data)

    def add_command(
        self,
        parent_id: str,
        title: str,
        description: str,
        ac_ref: str,
        run: dict[str, Any],
        artifacts: list[str] | None = None,
        owner: str = "system",
        labels: list[str] | None = None,
    ) -> Node:
        """Adds a new Command node."""
        node_data = {
            "id": f"CMD-{uuid.uuid4().hex[:12].upper()}",
            "layer": "Command",
            "title": title,
            "description": description,
            "links": {"parents": [parent_id], "children": []},
            "metadata": {
                "owner": owner,
                "labels": labels or [],
                "severity": "",
                "work_type": "",
            },
            "command": {"ac_ref": ac_ref, "run": run, "artifacts": artifacts or []},
        }
        return self.create_node(node_data)

    def add_concept(
        self,
        parent_id: str,
        title: str,
        description: str,
        owner: str = "system",
        labels: list[str] | None = None,
    ) -> Node:
        """Adds a new Concept node."""
        node_data = {
            "id": f"CON-{uuid.uuid4().hex[:12].upper()}",
            "layer": "Concept",
            "title": title,
            "description": description,
            "links": {"parents": [parent_id], "children": []},
            "metadata": {
                "owner": owner,
                "labels": labels or [],
                "severity": "",
                "work_type": "",
            },
        }
        return self.create_node(node_data)

    def add_context(
        self,
        parent_id: str,
        title: str,
        description: str,
        owner: str = "system",
        labels: list[str] | None = None,
    ) -> Node:
        """Adds a new Context node."""
        node_data = {
            "id": f"CTX-{uuid.uuid4().hex[:12].upper()}",
            "layer": "Context",
            "title": title,
            "description": description,
            "links": {"parents": [parent_id], "children": []},
            "metadata": {
                "owner": owner,
                "labels": labels or [],
                "severity": "",
                "work_type": "",
            },
        }
        return self.create_node(node_data)

    def add_constraint(
        self,
        parent_id: str,
        title: str,
        description: str,
        owner: str = "system",
        labels: list[str] | None = None,
    ) -> Node:
        """Adds a new Constraint node."""
        node_data = {
            "id": f"CST-{uuid.uuid4().hex[:12].upper()}",
            "layer": "Constraints",
            "title": title,
            "description": description,
            "links": {"parents": [parent_id], "children": []},
            "metadata": {
                "owner": owner,
                "labels": labels or [],
                "severity": "",
                "work_type": "",
            },
        }
        return self.create_node(node_data)

    def add_requirement(
        self,
        parent_id: str,
        title: str,
        description: str,
        owner: str = "system",
        labels: list[str] | None = None,
    ) -> Node:
        """Adds a new Requirement node."""
        node_data = {
            "id": f"R-{uuid.uuid4().hex[:12].upper()}",
            "layer": "Requirements",
            "title": title,
            "description": description,
            "links": {"parents": [parent_id], "children": []},
            "metadata": {
                "owner": owner,
                "labels": labels or [],
                "severity": "",
                "work_type": "",
            },
        }
        return self.create_node(node_data)

    def add_acceptance_criteria(
        self,
        parent_id: str,
        title: str,
        description: str,
        owner: str = "system",
        labels: list[str] | None = None,
    ) -> Node:
        """Adds a new Acceptance Criteria node."""
        node_data = {
            "id": f"AC-{uuid.uuid4().hex[:12].upper()}",
            "layer": "AcceptanceCriteria",
            "title": title,
            "description": description,
            "links": {"parents": [parent_id], "children": []},
            "metadata": {
                "owner": owner,
                "labels": labels or [],
                "severity": "",
                "work_type": "",
            },
        }
        return self.create_node(node_data)

    def add_interface_contract(
        self,
        parent_id: str,
        title: str,
        description: str,
        owner: str = "system",
        labels: list[str] | None = None,
    ) -> Node:
        """Adds a new Interface Contract node."""
        node_data = {
            "id": f"IF-{uuid.uuid4().hex[:12].upper()}",
            "layer": "InterfaceContract",
            "title": title,
            "description": description,
            "links": {"parents": [parent_id], "children": []},
            "metadata": {
                "owner": owner,
                "labels": labels or [],
                "severity": "",
                "work_type": "",
            },
        }
        return self.create_node(node_data)

    def get_node_by_id(self, node_id: str) -> Node | None:
        """Retrieves a node by its ID."""
        return self.get_node(node_id)

    def load_todos(self) -> dict[str, list[Node]]:
        """Loads all todos from the database."""
        return self.get_all_nodes()

    def get_active_items(self, todos: dict[str, list[Node]]) -> dict[str, list[Node]]:
        """Returns a dictionary of active items (status != 'done' and 'rejected') grouped by layer."""
        active_items: dict[str, list[Node]] = defaultdict(list)
        for layer, nodes in todos.items():
            for node in nodes:
                if node.status not in ["done", "rejected"]:
                    active_items[layer].append(node)
        return dict(active_items)

    def _create_db_node(self, session: Session, node_data: dict[str, Any]) -> DBNode:
        # Data validation
        required_fields: list[str] = ["id", "layer", "title", "description"]
        for field_name in required_fields:
            if field_name not in node_data:
                raise ValueError(f"Missing required field: {field_name}")

        db_node = DBNode(
            id=node_data["id"],
            layer=node_data["layer"],
            title=node_data["title"],
            description=node_data["description"],
            status=node_data.get("status", "planned"),
            owner=node_data["metadata"].get("owner"),
            severity=node_data["metadata"].get("severity"),
            work_type=node_data["metadata"].get("work_type"),
        )
        session.add(db_node)
        session.flush()  # Flush to get the node ID for relationships

        for parent_id in node_data["links"].get("parents", []):
            if parent_id is not None:  # Skip None parents for flexible entry points
                link = DBLink(parent_id=parent_id, child_id=db_node.id)
                session.add(link)

        for label_text in node_data["metadata"].get("labels", []):
            label_stmt = select(DBLabel).where(DBLabel.label == label_text)
            label = session.execute(label_stmt).scalar_one_or_none()
            if not label:
                label = DBLabel(label=label_text)
                session.add(label)
            db_node.labels.append(label)

        if node_data.get("command"):
            command_data: dict[str, Any] = node_data["command"]
            db_command = DBCommand(
                node_id=db_node.id,
                ac_ref=command_data["ac_ref"],
                run=json.dumps(command_data["run"]),
            )
            session.add(db_command)
            session.flush()

            for artifact_text in command_data.get("artifacts", []):
                artifact = DBArtifact(
                    command_id=db_command.node_id, artifact=artifact_text
                )
                session.add(artifact)

        return db_node

    def _convert_db_node_to_node(self, db_node: DBNode) -> Node:
        links = Link(parents=[], children=[])
        metadata = Metadata(
            owner=str(db_node.owner or ""),
            labels=[label.label for label in db_node.labels],
            severity=str(db_node.severity or ""),
            work_type=str(db_node.work_type or ""),
            assignee=str(db_node.assignee or ""),
        )
        command = None
        if db_node.command:
            command = Command(
                ac_ref=str(db_node.command.ac_ref or ""),
                run=json.loads(db_node.command.run) if db_node.command.run else {},
                artifacts=[artifact.artifact for artifact in db_node.command.artifacts],
            )
        return Node(
            id=str(db_node.id),
            layer=cast(LayerType, _validate_literal(str(db_node.layer), LayerType)),
            title=str(db_node.title),
            description=str(db_node.description),
            status=cast(StatusType, _validate_literal(str(db_node.status), StatusType)),
            progress=db_node.progress,
            started_date=str(db_node.started_date) if db_node.started_date else None,
            completion_date=(
                str(db_node.completion_date) if db_node.completion_date else None
            ),
            links=links,
            metadata=metadata,
            command=command,
        )

    def _dict_to_node(self, node_data: dict[str, Any]) -> Node:
        """Convert dictionary data to Node object."""
        links = Link(
            parents=node_data.get("links", {}).get("parents", []),
            children=node_data.get("links", {}).get("children", []),
        )

        metadata = Metadata(
            owner=node_data.get("metadata", {}).get("owner", ""),
            labels=node_data.get("metadata", {}).get("labels", []),
            severity=node_data.get("metadata", {}).get("severity", ""),
            work_type=node_data.get("metadata", {}).get("work_type", ""),
        )

        command = None
        if node_data.get("command"):
            command = Command(
                ac_ref=node_data["command"].get("ac_ref", ""),
                run=node_data["command"].get("run", {}),
                artifacts=node_data["command"].get("artifacts", []),
            )

        return Node(
            id=node_data["id"],
            layer=cast(LayerType, node_data["layer"]),
            title=node_data["title"],
            description=node_data["description"],
            links=links,
            metadata=metadata,
            status=cast(StatusType, node_data.get("status", "planned")),
            command=command,
        )

    def _auto_import_yaml_files(self) -> None:
        """Automatically import YAML files that are not in the database."""
        try:
            # Only attempt auto-import if database is accessible
            if self.engine:
                Base.metadata.create_all(bind=self.engine)

            # Import YAMLManager here to avoid circular imports
            from .yaml_manager import YAMLManager

            yaml_manager = YAMLManager(self)
            sync_status = yaml_manager.check_yaml_sync()

            if sync_status["yaml_only"]:
                print(
                    f"🔄 Auto-importing {len(sync_status['yaml_only'])} YAML files..."
                )
                results = yaml_manager.import_yaml_files(force=False, dry_run=False)

                if results["total_imported"] > 0:
                    print(
                        f"✅ Auto-imported {results['total_imported']} files from YAML"
                    )

                if results["errors"]:
                    print(f"⚠️  {len(results['errors'])} errors during auto-import")

        except Exception:
            # Silently fail auto-import to not break normal operation
            # Could log this to a file or debug mode in the future
            pass


# Standalone wrapper functions for public API
def create_node(node_data: dict[str, Any]) -> Node:
    """Create a new node using the default ToDoWrite instance."""
    app = ToDoWrite(auto_import=False)
    return app.create_node(node_data)


def get_node(node_id: str) -> Node | None:
    """Get a node by ID using the default ToDoWrite instance."""
    app = ToDoWrite(auto_import=False)
    return app.get_node(node_id)


def update_node(node_id: str, node_data: dict[str, Any]) -> Node | None:
    """Update a node using the default ToDoWrite instance."""
    app = ToDoWrite(auto_import=False)
    return app.update_node(node_id, node_data)


def delete_node(node_id: str) -> None:
    """Delete a node using the default ToDoWrite instance."""
    app = ToDoWrite(auto_import=False)
    app.delete_node(node_id)


def list_nodes() -> dict[str, list[Node]]:
    """List all nodes using the default ToDoWrite instance."""
    app = ToDoWrite(auto_import=False)
    return app.get_all_nodes()


def search_nodes(query: str) -> dict[str, list[Node]]:
    """Search for nodes using the default ToDoWrite instance."""
    app = ToDoWrite(auto_import=False)
    return app.search_nodes(query)


def export_nodes(format: str = "yaml") -> str:
    """Export nodes using the default ToDoWrite instance."""
    app = ToDoWrite(auto_import=False)
    return app.export_nodes(format)


def import_nodes(file_path: str) -> dict[str, Any]:
    """Import nodes from a file using the default ToDoWrite instance."""
    app = ToDoWrite(auto_import=False)
    return app.import_nodes(file_path)


def update_node_status(node_id: str, status: str) -> Node | None:
    """Update node status using the default ToDoWrite instance."""
    app = ToDoWrite(auto_import=False)
    return app.update_node_status(node_id, status)
