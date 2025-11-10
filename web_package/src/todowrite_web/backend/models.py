"""Shared Python models for ToDoWrite web backend-frontend communication.

This module contains Pydantic models that mirror the ToDoWrite schema
for use in the web API and data validation.
"""

from datetime import datetime
from enum import Enum
from typing import Any

from pydantic import BaseModel, ConfigDict, Field, model_validator


class NodeLayer(str, Enum):
    """Valid node layers in ToDoWrite."""

    GOAL = "Goal"
    CONCEPT = "Concept"
    CONTEXT = "Context"
    CONSTRAINTS = "Constraints"
    REQUIREMENTS = "Requirements"
    ACCEPTANCE_CRITERIA = "AcceptanceCriteria"
    INTERFACE_CONTRACT = "InterfaceContract"
    PHASE = "Phase"
    STEP = "Step"
    TASK = "Task"
    SUBTASK = "SubTask"
    COMMAND = "Command"


class NodeStatus(str, Enum):
    """Valid node statuses."""

    PLANNED = "planned"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    BLOCKED = "blocked"
    CANCELLED = "cancelled"


class Severity(str, Enum):
    """Valid severity levels."""

    LOW = "low"
    MED = "med"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class WorkType(str, Enum):
    """Valid work types."""

    ARCHITECTURE = "architecture"
    SPEC = "spec"
    INTERFACE = "interface"
    VALIDATION = "validation"
    IMPLEMENTATION = "implementation"
    DEVELOPMENT = "development"
    DOCS = "docs"
    OPS = "ops"
    REFACTOR = "refactor"
    CHORE = "chore"
    TEST = "test"


class NodeMetadata(BaseModel):
    """Optional metadata for nodes."""

    owner: str | None = None
    labels: list[str] | None = None
    severity: Severity | None = None
    work_type: WorkType | None = None
    assignee: str | None = None
    extra: dict[str, Any] | None = Field(default_factory=dict)

    model_config = ConfigDict(extra="allow")


class CommandRun(BaseModel):
    """Command execution configuration."""

    shell: str
    workdir: str | None = None
    env: dict[str, str] | None = None


class Command(BaseModel):
    """Command definition for Command layer nodes."""

    ac_ref: str = Field(..., pattern=r"^AC-[A-Z0-9_-]+$")
    run: CommandRun
    artifacts: list[str] | None = None


class NodeLinks(BaseModel):
    """Parent-child relationships for nodes."""

    parents: list[str] = Field(default_factory=list)
    children: list[str] = Field(default_factory=list)


class Node(BaseModel):
    """Core ToDoWrite node model."""

    id: str = Field(
        ..., pattern=r"^(GOAL|CON|CTX|CST|R|AC|IF|PH|STP|TSK|SUB|CMD)-[A-Za-z0-9_-]+$"
    )
    layer: NodeLayer
    title: str = Field(..., min_length=1)
    description: str
    status: NodeStatus | None = NodeStatus.PLANNED
    metadata: NodeMetadata | None = None
    progress: int | None = Field(None, ge=0, le=100)
    started_date: datetime | None = None
    completion_date: datetime | None = None
    assignee: str | None = None
    links: NodeLinks = Field(default_factory=NodeLinks)
    command: Command | None = None

    model_config = ConfigDict(
        extra="allow", json_encoders={datetime: lambda v: v.isoformat() if v else None}
    )

    @model_validator(mode="after")
    def validate_command_for_layer(self) -> "Node":
        if self.layer == NodeLayer.COMMAND and self.command is None:
            raise ValueError("Command layer nodes must have a command")
        if self.layer != NodeLayer.COMMAND and self.command is not None:
            raise ValueError("Only Command layer nodes can have a command")
        return self


# API Request/Response Models
class CreateNodeRequest(BaseModel):
    """Request model for creating nodes."""

    layer: NodeLayer
    title: str = Field(..., min_length=1)
    description: str
    status: NodeStatus | None = NodeStatus.PLANNED
    metadata: NodeMetadata | None = None
    assignee: str | None = None
    parent_ids: list[str] | None = None
    command: Command | None = None


class UpdateNodeRequest(BaseModel):
    """Request model for updating nodes."""

    title: str | None = Field(None, min_length=1)
    description: str | None = None
    status: NodeStatus | None = None
    metadata: NodeMetadata | None = None
    progress: int | None = Field(None, ge=0, le=100)
    started_date: datetime | None = None
    completion_date: datetime | None = None
    assignee: str | None = None
    command: Command | None = None


class NodeResponse(BaseModel):
    """Response model for single node operations."""

    node: Node
    children: list[Node] | None = None
    parents: list[Node] | None = None


class NodeListResponse(BaseModel):
    """Response model for node list operations."""

    nodes: list[Node]
    total: int
    page: int
    page_size: int


class SearchRequest(BaseModel):
    """Request model for search operations."""

    query: str = Field(..., min_length=1)
    layer: NodeLayer | None = None
    status: NodeStatus | None = None
    assignee: str | None = None
    labels: list[str] | None = None
    limit: int | None = Field(50, ge=1, le=1000)
    offset: int | None = Field(0, ge=0)


class SearchResponse(BaseModel):
    """Response model for search operations."""

    nodes: list[Node]
    total: int
    query: str


class ErrorResponse(BaseModel):
    """Standard error response model."""

    error: str
    message: str
    details: dict[str, Any] | None = None


# Project-level simplified models
class Project(BaseModel):
    """Simplified project representation."""

    id: str
    title: str
    description: str
    status: NodeStatus
    progress: int = Field(..., ge=0, le=100)
    node_count: int
    completed_count: int
    last_updated: datetime

    model_config = ConfigDict(json_encoders={datetime: lambda v: v.isoformat()})


class ProjectListResponse(BaseModel):
    """Response model for project list operations."""

    projects: list[Project]
    total: int


# WebSocket message models
class WebSocketMessageType(str, Enum):
    """WebSocket message types."""

    NODE_CREATED = "node_created"
    NODE_UPDATED = "node_updated"
    NODE_DELETED = "node_deleted"
    ERROR = "error"


class WebSocketMessage(BaseModel):
    """Standard WebSocket message format."""

    type: WebSocketMessageType
    data: dict[str, Any]
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class NodeSubscription(BaseModel):
    """Node subscription filter criteria."""

    node_ids: list[str] | None = None
    layer: NodeLayer | None = None
    project_id: str | None = None


# Health check models
class HealthResponse(BaseModel):
    """Health check response."""

    status: str = "healthy"
    version: str
    database: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)


# Configuration models
class DatabaseConfig(BaseModel):
    """Database configuration."""

    url: str
    pool_size: int = 5
    max_overflow: int = 10


class APIConfig(BaseModel):
    """API configuration."""

    title: str = "ToDoWrite API"
    description: str = "Hierarchical task management system API"
    version: str = "1.0.0"
    debug: bool = False
    cors_origins: list[str] = Field(default_factory=lambda: ["http://localhost:3000"])


class Config(BaseModel):
    """Application configuration."""

    database: DatabaseConfig
    api: APIConfig = Field(default_factory=APIConfig)
    secret_key: str
    environment: str = "development"
