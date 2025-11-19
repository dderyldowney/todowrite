"""Shared utilities and models for ToDoWrite web package.

This package provides common types, models, and utilities for
backend-frontend communication in the ToDoWrite web application.
"""

from .api.backend import (
    APIConfig,
    Command,
    CommandRun,
    # Configuration Models
    Config,
    # API Models
    CreateNodeRequest,
    DatabaseConfig,
    ErrorResponse,
    HealthResponse,
    # Core Models
    Node,
    # Enums
    NodeLayer,
    NodeLinks,
    NodeListResponse,
    NodeMetadata,
    NodeResponse,
    NodeStatus,
    NodeSubscription,
    # Project Models
    Project,
    ProjectListResponse,
    SearchRequest,
    SearchResponse,
    Severity,
    UpdateNodeRequest,
    # WebSocket Models
    WebSocketMessage,
    WebSocketMessageType,
    WorkType,
    build_hierarchy,
    build_node_hierarchy,
    calculate_node_depth,
    calculate_node_progress,
    # Progress utilities
    calculate_progress,
    can_transition_to,
    export_to_csv,
    # Export utilities
    export_to_json,
    filter_nodes_by_assignee,
    filter_nodes_by_labels,
    # Search and filter utilities
    filter_nodes_by_layer,
    filter_nodes_by_status,
    # Date utilities
    format_date,
    format_datetime,
    generate_node_id,
    get_all_ancestors,
    get_all_descendants,
    get_layer_prefix,
    get_leaf_nodes,
    get_next_status,
    # Hierarchy utilities
    get_root_nodes,
    # Status utilities
    get_status_color,
    # Import utilities
    import_nodes_from_json,
    is_overdue,
    # Node utilities
    is_valid_node_id,
    # Metadata utilities
    merge_node_metadata,
    sanitize_node_id,
    search_nodes,
    # Validation utilities
    validate_node_structure,
)

__version__ = "0.1.0"
__all__ = [
    # Configuration Models
    "APIConfig",
    # Core Models
    "Command",
    "CommandRun",
    "Config",
    # API Models
    "CreateNodeRequest",
    "DatabaseConfig",
    "ErrorResponse",
    "HealthResponse",
    "Metadata utilities",
    "Node",
    # Enums
    "NodeLayer",
    "NodeLinks",
    "NodeListResponse",
    "NodeMetadata",
    "NodeResponse",
    "NodeStatus",
    # WebSocket Models
    "NodeSubscription",
    # Project Models
    "Project",
    "ProjectListResponse",
    "SearchRequest",
    "SearchResponse",
    "Severity",
    "UpdateNodeRequest",
    "WebSocketMessage",
    "WebSocketMessageType",
    "WorkType",
    # Hierarchy utilities
    "build_hierarchy",
    "build_node_hierarchy",
    "calculate_node_depth",
    # Node utilities
    "calculate_node_progress",
    # Progress utilities
    "calculate_progress",
    # Status utilities
    "can_transition_to",
    # Export utilities
    "export_to_csv",
    "export_to_json",
    # Search and filter utilities
    "filter_nodes_by_assignee",
    "filter_nodes_by_labels",
    "filter_nodes_by_layer",
    "filter_nodes_by_status",
    # Date utilities
    "format_date",
    "format_datetime",
    "generate_node_id",
    "get_all_ancestors",
    "get_all_descendants",
    "get_layer_prefix",
    "get_leaf_nodes",
    "get_next_status",
    "get_root_nodes",
    "get_status_color",
    # Import utilities
    "import_nodes_from_json",
    "is_overdue",
    "is_valid_node_id",
    "merge_node_metadata",
    "sanitize_node_id",
    "search_nodes",
    # Validation utilities
    "validate_node_structure",
]
