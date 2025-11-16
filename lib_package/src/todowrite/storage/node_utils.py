"""Node conversion utilities between application and database representations.

This module provides clean conversion functions to work with the unified Node architecture.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from ..core.types import Link as AppLink
    from ..core.types import Metadata
    from ..core.types import Node as AppNode
    from ..database.models import Node as DBNode


def app_node_to_db_node(app_node: AppNode) -> dict[str, Any]:
    """Convert application Node to database Node fields."""
    return {
        "id": app_node.id,
        "layer": app_node.layer,
        "title": app_node.title,
        "description": app_node.description,
        "status": app_node.status,
        "progress": app_node.progress,
        "started_date": app_node.started_date,
        "completion_date": app_node.completion_date,
        "owner": app_node.metadata.owner,
        "severity": app_node.metadata.severity,
        "work_type": app_node.metadata.work_type,
        "assignee": app_node.metadata.assignee,
    }


def db_node_to_app_node(db_node: DBNode) -> AppNode:
    """Convert database Node to application Node."""
    # Handle relationships safely
    labels = []
    try:
        if hasattr(db_node, "labels") and db_node.labels:
            labels = [label.label for label in db_node.labels]
    except Exception:
        pass

    command = None
    try:
        if hasattr(db_node, "command") and db_node.command:
            command = {
                "ac_ref": db_node.command.ac_ref,
                "run": db_node.command.run,
                "artifacts": [
                    a.artifact
                    for a in getattr(db_node.command, "artifacts", [])
                ]
                if hasattr(db_node.command, "artifacts")
                and db_node.command.artifacts
                else [],
            }
    except Exception:
        pass

    # Build parents and children from relationships
    parents = []
    children = []
    try:
        if hasattr(db_node, "parents"):
            parents = [parent.id for parent in db_node.parents]
        if hasattr(db_node, "children"):
            children = [child.id for child in db_node.children]
    except Exception:
        pass

    return AppNode(
        id=db_node.id,
        layer=db_node.layer,
        title=db_node.title,
        description=db_node.description or "",
        status=db_node.status or "planned",
        progress=db_node.progress or 0,
        started_date=db_node.started_date,
        completion_date=db_node.completion_date,
        links=AppLink(parents=parents, children=children),
        metadata=Metadata(
            owner=db_node.owner or "system",
            labels=labels,
            severity=db_node.severity or "low",
            work_type=db_node.work_type or "chore",
            assignee=db_node.assignee or "",
        ),
        command=command,
    )


def extract_relationships_from_app_node(
    app_node: AppNode,
) -> tuple[list[str], list[str], list[str]]:
    """Extract parents, children, and labels from an application Node."""
    return (
        app_node.links.parents,
        app_node.links.children,
        app_node.metadata.labels,
    )


def extract_command_from_app_node(app_node: AppNode) -> dict[str, Any] | None:
    """Extract command data from an application Node."""
    return app_node.command
