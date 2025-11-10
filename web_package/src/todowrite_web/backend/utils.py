"""Shared utility functions for ToDoWrite web backend.

This module provides common utility functions for node operations,
validation, hierarchy management, and data transformation.
"""

import csv
import json
import re
from datetime import UTC, datetime
from io import StringIO
from typing import Any
from uuid import uuid4

from .models import Node, NodeLayer, NodeStatus

# Node ID validation and generation
NODE_ID_PATTERN = re.compile(
    r"^(GOAL|CON|CTX|CST|R|AC|IF|PH|STP|TSK|SUB|CMD)-[A-Za-z0-9_-]+$"
)

LAYER_PREFIXES = {
    NodeLayer.GOAL: "GOAL",
    NodeLayer.CONCEPT: "CON",
    NodeLayer.CONTEXT: "CTX",
    NodeLayer.CONSTRAINTS: "CST",
    NodeLayer.REQUIREMENTS: "R",
    NodeLayer.ACCEPTANCE_CRITERIA: "AC",
    NodeLayer.INTERFACE_CONTRACT: "IF",
    NodeLayer.PHASE: "PH",
    NodeLayer.STEP: "STP",
    NodeLayer.TASK: "TSK",
    NodeLayer.SUBTASK: "SUB",
    NodeLayer.COMMAND: "CMD",
}

STATUS_COLORS = {
    NodeStatus.PLANNED: "#6B7280",  # gray
    NodeStatus.IN_PROGRESS: "#3B82F6",  # blue
    NodeStatus.COMPLETED: "#10B981",  # green
    NodeStatus.BLOCKED: "#EF4444",  # red
    NodeStatus.CANCELLED: "#9CA3AF",  # gray
}

STATUS_FLOW = {
    NodeStatus.PLANNED: NodeStatus.IN_PROGRESS,
    NodeStatus.IN_PROGRESS: NodeStatus.COMPLETED,
    NodeStatus.COMPLETED: NodeStatus.COMPLETED,
    NodeStatus.BLOCKED: NodeStatus.PLANNED,
    NodeStatus.CANCELLED: NodeStatus.PLANNED,
}


def is_valid_node_id(node_id: str) -> bool:
    """Check if a node ID follows the valid format."""
    return bool(NODE_ID_PATTERN.match(node_id))


def get_layer_prefix(layer: NodeLayer) -> str:
    """Get the prefix for a given layer."""
    return LAYER_PREFIXES[layer]


def generate_node_id(layer: NodeLayer, suffix: str | None = None) -> str:
    """Generate a new node ID for the given layer."""
    prefix = get_layer_prefix(layer)
    if suffix:
        return f"{prefix}-{suffix}"
    # Generate a UUID-based suffix for uniqueness
    uuid_suffix = str(uuid4()).replace("-", "")[:12].upper()
    return f"{prefix}-{uuid_suffix}"


# Status utilities
def get_status_color(status: NodeStatus) -> str:
    """Get the color associated with a status."""
    return STATUS_COLORS[status]


def get_next_status(current_status: NodeStatus) -> NodeStatus:
    """Get the next logical status in the workflow."""
    return STATUS_FLOW[current_status]


def can_transition_to(current_status: NodeStatus, new_status: NodeStatus) -> bool:
    """Check if a status transition is valid."""
    # Define valid transitions
    valid_transitions = {
        NodeStatus.PLANNED: [NodeStatus.IN_PROGRESS, NodeStatus.CANCELLED],
        NodeStatus.IN_PROGRESS: [
            NodeStatus.COMPLETED,
            NodeStatus.BLOCKED,
            NodeStatus.CANCELLED,
        ],
        NodeStatus.COMPLETED: [NodeStatus.IN_PROGRESS],  # Allow reopening
        NodeStatus.BLOCKED: [NodeStatus.IN_PROGRESS, NodeStatus.CANCELLED],
        NodeStatus.CANCELLED: [NodeStatus.PLANNED],
    }
    return new_status in valid_transitions.get(current_status, [])


# Progress utilities
def calculate_progress(nodes: list[Node]) -> int:
    """Calculate overall progress percentage from a list of nodes."""
    if not nodes:
        return 0

    completed_count = sum(1 for node in nodes if node.status == NodeStatus.COMPLETED)
    return round((completed_count / len(nodes)) * 100)


def calculate_node_progress(node: Node, all_nodes: dict[str, Node]) -> int:
    """Calculate progress for a node based on its children."""
    if not node.links.children:
        return node.progress or 0

    child_nodes = [
        all_nodes[child_id] for child_id in node.links.children if child_id in all_nodes
    ]
    if not child_nodes:
        return node.progress or 0

    return calculate_progress(child_nodes)


# Hierarchy utilities
def get_root_nodes(nodes: list[Node]) -> list[Node]:
    """Get nodes that have no parents (root nodes)."""
    return [node for node in nodes if not node.links.parents]


def get_leaf_nodes(nodes: list[Node]) -> list[Node]:
    """Get nodes that have no children (leaf nodes)."""
    return [node for node in nodes if not node.links.children]


def build_hierarchy(nodes: list[Node]) -> dict[str, list[Node]]:
    """Build a hierarchy mapping parent IDs to child nodes."""
    hierarchy = {}
    for node in nodes:
        for parent_id in node.links.parents:
            if parent_id not in hierarchy:
                hierarchy[parent_id] = []
            hierarchy[parent_id].append(node)
    return hierarchy


def get_node_depth(node: Node, all_nodes: dict[str, Node]) -> int:
    """Calculate the depth of a node in the hierarchy."""
    if not node.links.parents:
        return 0

    max_depth = 0
    for parent_id in node.links.parents:
        if parent_id in all_nodes:
            depth = get_node_depth(all_nodes[parent_id], all_nodes)
            max_depth = max(max_depth, depth)

    return max_depth + 1


def get_node_hierarchy(
    node: Node, all_nodes: dict[str, Node], max_depth: int | None = None
) -> dict[str, Any]:
    """Get the complete hierarchy for a node up to optional max depth."""
    result = {"node": node.model_dump(), "children": []}

    if max_depth is None or max_depth > 0:
        current_depth = max_depth - 1 if max_depth is not None else None

        for child_id in node.links.children:
            if child_id in all_nodes:
                child_hierarchy = get_node_hierarchy(
                    all_nodes[child_id], all_nodes, current_depth
                )
                result["children"].append(child_hierarchy)

    return result


def get_all_descendants(node: Node, all_nodes: dict[str, Node]) -> set[str]:
    """Get all descendant node IDs for a given node."""
    descendants = set()

    for child_id in node.links.children:
        if child_id in all_nodes:
            descendants.add(child_id)
            child_descendants = get_all_descendants(all_nodes[child_id], all_nodes)
            descendants.update(child_descendants)

    return descendants


def get_all_ancestors(node: Node, all_nodes: dict[str, Node]) -> set[str]:
    """Get all ancestor node IDs for a given node."""
    ancestors = set()

    for parent_id in node.links.parents:
        if parent_id in all_nodes:
            ancestors.add(parent_id)
            parent_ancestors = get_all_ancestors(all_nodes[parent_id], all_nodes)
            ancestors.update(parent_ancestors)

    return ancestors


# Search and filter utilities
def filter_nodes_by_layer(nodes: list[Node], layers: list[NodeLayer]) -> list[Node]:
    """Filter nodes by one or more layers."""
    return [node for node in nodes if node.layer in layers]


def filter_nodes_by_status(nodes: list[Node], statuses: list[NodeStatus]) -> list[Node]:
    """Filter nodes by one or more statuses."""
    return [node for node in nodes if node.status and node.status in statuses]


def filter_nodes_by_assignee(nodes: list[Node], assignee: str) -> list[Node]:
    """Filter nodes by assignee."""
    return [
        node
        for node in nodes
        if node.assignee == assignee
        or (node.metadata and node.metadata.assignee == assignee)
    ]


def filter_nodes_by_labels(nodes: list[Node], labels: list[str]) -> list[Node]:
    """Filter nodes that have any of the specified labels."""
    return [
        node
        for node in nodes
        if node.metadata
        and node.metadata.labels
        and any(label in node.metadata.labels for label in labels)
    ]


def search_nodes(nodes: list[Node], query: str) -> list[Node]:
    """Search nodes by title, description, or ID."""
    query_lower = query.lower()
    return [
        node
        for node in nodes
        if (
            query_lower in node.title.lower()
            or query_lower in node.description.lower()
            or query_lower in node.id.lower()
        )
    ]


# Date utilities
def format_date(date: datetime | None) -> str:
    """Format a datetime as a date string."""
    return date.strftime("%Y-%m-%d") if date else ""


def format_datetime(date: datetime | None) -> str:
    """Format a datetime as a datetime string."""
    return date.strftime("%Y-%m-%d %H:%M:%S") if date else ""


def is_overdue(node: Node) -> bool:
    """Check if a node is overdue (has started date and is not completed)."""
    if not node.started_date or node.status == NodeStatus.COMPLETED:
        return False
    return node.started_date < datetime.now(UTC)


# Validation utilities
def validate_node_structure(node_data: dict[str, Any]) -> tuple[bool, list[str]]:
    """Validate node structure and return errors."""
    errors = []

    # Required fields
    if "id" not in node_data or not node_data["id"]:
        errors.append("Node ID is required")
    elif not is_valid_node_id(node_data["id"]):
        errors.append("Invalid node ID format")

    if "layer" not in node_data:
        errors.append("Layer is required")
    elif node_data["layer"] not in [layer.value for layer in NodeLayer]:
        errors.append("Invalid layer")

    if "title" not in node_data or not node_data["title"].strip():
        errors.append("Title is required")

    if "description" not in node_data:
        errors.append("Description is required")

    # Optional field validation
    if "progress" in node_data and node_data["progress"] is not None:
        progress = node_data["progress"]
        if not isinstance(progress, int) or progress < 0 or progress > 100:
            errors.append("Progress must be an integer between 0 and 100")

    # Command validation
    layer = node_data.get("layer")
    has_command = "command" in node_data and node_data["command"]

    if layer == "Command" and not has_command:
        errors.append("Command layer nodes must have a command object")
    elif layer != "Command" and has_command:
        errors.append("Only Command layer nodes can have a command object")

    return len(errors) == 0, errors


# Export utilities
def export_to_json(nodes: list[Node]) -> str:
    """Export nodes to JSON format."""
    return json.dumps([node.model_dump() for node in nodes], indent=2, default=str)


def export_to_csv(nodes: list[Node]) -> str:
    """Export nodes to CSV format."""
    output = StringIO()
    writer = csv.writer(output)

    # Headers
    headers = [
        "ID",
        "Layer",
        "Title",
        "Description",
        "Status",
        "Progress",
        "Assignee",
        "Started Date",
        "Completion Date",
    ]
    writer.writerow(headers)

    # Data rows
    for node in nodes:
        row = [
            node.id,
            node.layer.value,
            node.title,
            node.description,
            node.status.value if node.status else "",
            node.progress or "",
            node.assignee or "",
            format_date(node.started_date),
            format_date(node.completion_date),
        ]
        writer.writerow(row)

    return output.getvalue()


# Import utilities
def import_nodes_from_json(json_data: str) -> tuple[list[dict[str, Any]], list[str]]:
    """Import nodes from JSON data and return nodes and errors."""
    try:
        data = json.loads(json_data)
        if not isinstance(data, list):
            return [], ["JSON data must be a list of nodes"]

        valid_nodes = []
        errors = []

        for i, node_data in enumerate(data):
            is_valid, node_errors = validate_node_structure(node_data)
            if is_valid:
                valid_nodes.append(node_data)
            else:
                errors.extend([f"Node {i}: {error}" for error in node_errors])

        return valid_nodes, errors

    except json.JSONDecodeError as e:
        return [], [f"Invalid JSON: {e!s}"]


# Utility functions for database operations
def sanitize_node_id(node_id: str) -> str:
    """Sanitize and validate a node ID."""
    node_id = node_id.strip().upper()
    if is_valid_node_id(node_id):
        return node_id
    raise ValueError(f"Invalid node ID format: {node_id}")


def create_node_links(
    parent_ids: list[str] | None = None, child_ids: list[str] | None = None
) -> dict[str, list[str]]:
    """Create a node links dictionary."""
    return {"parents": parent_ids or [], "children": child_ids or []}


def merge_node_metadata(
    base: dict[str, Any] | None, updates: dict[str, Any] | None
) -> dict[str, Any]:
    """Merge node metadata dictionaries."""
    base = base or {}
    updates = updates or {}

    result = base.copy()
    result.update(updates)

    # Handle special case for labels - merge lists
    if "labels" in base and "labels" in updates:
        base_labels = set(base["labels"] or [])
        update_labels = set(updates["labels"] or [])
        result["labels"] = list(base_labels.union(update_labels))

    return result
