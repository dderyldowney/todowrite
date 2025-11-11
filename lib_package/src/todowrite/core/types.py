"""
ToDoWrite Core Type Definitions.

This module contains shared type definitions and data structures used throughout
the ToDoWrite package. It defines the fundamental types for the 12-layer
hierarchical task management system.

The types defined here are used across:
- Database models and ORM mappings
- YAML storage structures
- API request/response models
- Validation schemas
- Internal data processing

Key Concepts:
- LayerType: The 12 hierarchical layers from Goal to Command
- StatusType: Workflow states for task tracking
- Node: Core data structure for all task items
- Metadata: Extensible metadata system
- Links: Hierarchical relationships between nodes
- Command: Executable command definitions

Example:
    >>> from todowrite.core.types import Node, LayerType, Metadata
    >>>
    >>> node = Node(
    ...     id="GOAL-001",
    ...     layer="Goal",
    ...     title="Launch Product",
    ...     description="Successfully launch the new product",
    ...     metadata=Metadata(owner="product-team", severity="high")
    ... )
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Literal

# pyright: reportUnknownVariableType=none


LayerType = Literal[
    "Goal",
    "Concept",
    "Context",
    "Constraints",
    "Requirements",
    "AcceptanceCriteria",
    "InterfaceContract",
    "Phase",
    "Step",
    "Task",
    "SubTask",
    "Command",
]

StatusType = Literal[
    "planned", "in_progress", "completed", "blocked", "cancelled"
]


@dataclass
class Metadata:
    """
    Extensible metadata for ToDoWrite nodes.

    This class provides standardized metadata fields that can be extended
    with additional custom data as needed through the extra field.

    Attributes:
        owner: Team or individual responsible for the node
        labels: List of categorical tags for organization and filtering
        severity: Priority level (low, medium, high, critical)
        work_type: Type of work (architecture, spec, implementation, etc.)
        assignee: Individual assigned to work on this node
        extra: Dictionary for additional custom metadata

    Example:
        >>> metadata = Metadata(
        ...     owner="backend-team",
        ...     labels=["api", "security", "v2.0"],
        ...     severity="high",
        ...     work_type="implementation",
        ...     assignee="alice@example.com",
        ...     extra={"sprint": "12", "story_points": 8}
        ... )
    """

    owner: str = ""
    labels: list[str] = field(default_factory=list)
    severity: str = "low"
    work_type: str = "chore"
    assignee: str = ""
    extra: dict[str, Any] = field(default_factory=dict)


@dataclass
class Link:
    """
    Hierarchical relationships between ToDoWrite nodes.

    This class defines the parent-child relationships that create the
    hierarchical structure connecting the 12 layers. Each node can have
    multiple parents and children to support complex dependency graphs.

    Attributes:
        parents: List of parent node IDs (higher in hierarchy)
        children: List of child node IDs (lower in hierarchy)

    Example:
        >>> # A requirement linked to a goal and with child acceptance criteria
        >>> link = Link(
        ...     parents=["GOAL-001"],
        ...     children=["AC-001", "AC-002"]
        ... )
    """

    parents: list[str] = field(default_factory=list)
    children: list[str] = field(default_factory=list)


@dataclass
class Command:
    """
    Executable command definition for Command layer nodes.

    This class defines the executable components of the ToDoWrite system,
    linking acceptance criteria to actual automation scripts and commands.

    Attributes:
        ac_ref: Reference to the acceptance criteria this command validates
        run: Dictionary defining how to execute the command
        artifacts: List of expected output files/artifacts

    Example:
        >>> command = Command(
        ...     ac_ref="AC-API-001",
        ...     run={
        ...         "shell": "pytest tests/api/test_health.py",
        ...         "workdir": ".",
        ...         "timeout": 300
        ...     },
        ...     artifacts=["test_results.xml", "coverage_report.html"]
        ... )
    """

    ac_ref: str = ""
    run: dict[str, Any] = field(default_factory=dict)
    artifacts: list[str] = field(default_factory=list)


@dataclass
class Label:
    """
    Categorization label for organizing and filtering nodes.

    Labels provide a flexible tagging system that can be used for
    organizing work, filtering views, and creating custom workflows.

    Attributes:
        name: Short identifier for the label
        description: Detailed explanation of the label's purpose

    Example:
        >>> label = Label(
        ...     name="security",
        ...     description="Security-related tasks and requirements"
        ... )
    """

    name: str = ""
    description: str = ""


@dataclass
class Node:
    """
    Core data structure representing a node in the ToDoWrite hierarchical system.

    A Node is the fundamental unit of work in ToDoWrite, representing any item
    across the 12-layer hierarchy from strategic Goals down to executable Commands.
    Each node contains progress tracking, relationships, metadata, and optionally
    executable command definitions.

    Attributes:
        id: Unique identifier following pattern LAYER-DESCRIPTION-NNN
        layer: One of the 12 hierarchical layers (Goal, Concept, ..., Command)
        title: Human-readable title/name for the node
        description: Detailed description of the node's purpose and scope
        status: Workflow state (planned, in_progress, completed, blocked, cancelled)
        progress: Completion percentage (0-100)
        started_date: ISO timestamp when work began on this node
        completion_date: ISO timestamp when node was completed
        links: Parent-child relationships connecting to other nodes
        metadata: Extensible metadata including owner, labels, severity, etc.
        command: Executable command definition (only for Command layer nodes)

    Example:
        >>> node = Node(
        ...     id="GOAL-001",
        ...     layer="Goal",
        ...     title="Automate Testing Pipeline",
        ...     description="Implement fully automated CI/CD testing pipeline",
        ...     metadata=Metadata(
        ...         owner="devops-team",
        ...         labels=["automation", "testing", "ci-cd"],
        ...         severity="high"
        ...     )
        ... )
    """

    id: str
    layer: LayerType
    title: str
    description: str = ""
    status: StatusType = "planned"
    progress: int = 0
    started_date: str | None = None
    completion_date: str | None = None
    links: Link = field(default_factory=Link)
    metadata: Metadata = field(default_factory=Metadata)
    command: Command | None = None

    def to_dict(self) -> dict[str, Any]:
        """
        Convert node to dictionary representation for serialization.

        Returns:
            Dictionary containing all node data suitable for JSON/YAML export
            or database storage.

        Example:
            >>> node = Node(id="TEST-001", layer="Task", title="Test")
            >>> data = node.to_dict()
            >>> print(data["id"])  # Output: TEST-001
        """
        result: dict[str, Any] = {
            "id": self.id,
            "layer": self.layer,
            "title": self.title,
            "description": self.description,
            "status": self.status,
            "links": {
                "parents": self.links.parents,
                "children": self.links.children,
            },
            "metadata": {
                "owner": self.metadata.owner,
                "labels": self.metadata.labels,
                "severity": self.metadata.severity,
                "work_type": self.metadata.work_type,
                "assignee": self.metadata.assignee,
            },
        }

        # Add optional status tracking fields
        if self.progress is not None:
            result["progress"] = self.progress
        if self.started_date is not None:
            result["started_date"] = str(self.started_date)
        if self.completion_date is not None:
            result["completion_date"] = str(self.completion_date)
        if self.metadata.assignee:
            result["assignee"] = self.metadata.assignee

        if self.command:
            result["command"] = {
                "ac_ref": self.command.ac_ref,
                "run": self.command.run,
                "artifacts": self.command.artifacts,
            }

        return result

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Node:
        """Create node from dictionary representation."""
        links_data = data.get("links", {})
        metadata_data = data.get("metadata", {})
        command_data = data.get("command")

        links = Link(
            parents=links_data.get("parents", []),
            children=links_data.get("children", []),
        )

        metadata = Metadata(
            owner=metadata_data.get("owner", "system"),
            labels=metadata_data.get("labels", []),
            severity=metadata_data.get("severity", ""),
            work_type=metadata_data.get("work_type", ""),
            assignee=metadata_data.get("assignee", ""),
        )

        command = None
        if command_data:
            command = Command(
                ac_ref=command_data.get("ac_ref", ""),
                run=command_data.get("run", {}),
                artifacts=command_data.get("artifacts", []),
            )

        return cls(
            id=data["id"],
            layer=data["layer"],
            title=data["title"],
            description=data.get("description", ""),
            status=data.get("status", "planned"),
            progress=data.get("progress", 0),
            started_date=data.get("started_date"),
            completion_date=data.get("completion_date"),
            links=links,
            metadata=metadata,
            command=command,
        )
