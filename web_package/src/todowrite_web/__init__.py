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
    "Config",
    "DatabaseConfig",
    "HealthResponse",
    # Core Models
    "Command",
    "CommandRun",
    "Node",
    "NodeLinks",
    "NodeMetadata",
    # Enums
    "NodeLayer",
    "NodeStatus",
    "Severity",
    "WebSocketMessageType",
    "WorkType",
    # Export utilities
    "export_to_csv",
    "export_to_json",
    # Hierarchy utilities
    "build_hierarchy",
    "get_all_ancestors",
    "get_all_descendants",
    "get_leaf_nodes",
    "calculate_node_depth",
    "build_node_hierarchy",
    "get_root_nodes",
    # Import utilities
    "import_nodes_from_json",
    "Metadata utilities",
    "merge_node_metadata",
    # Node utilities
    "calculate_node_progress",
    "generate_node_id",
    "get_layer_prefix",
    "is_valid_node_id",
    "sanitize_node_id",
    # Project Models
    "Project",
    "ProjectListResponse",
    # Progress utilities
    "calculate_progress",
    # Search and filter utilities
    "filter_nodes_by_assignee",
    "filter_nodes_by_labels",
    "filter_nodes_by_layer",
    "filter_nodes_by_status",
    "search_nodes",
    # Status utilities
    "can_transition_to",
    "get_next_status",
    "get_status_color",
    # Validation utilities
    "validate_node_structure",
    # WebSocket Models
    "NodeSubscription",
    "WebSocketMessage",
    # Date utilities
    "format_date",
    "format_datetime",
    "is_overdue",
    # API Models
    "CreateNodeRequest",
    "ErrorResponse",
    "NodeListResponse",
    "NodeResponse",
    "SearchRequest",
    "SearchResponse",
    "UpdateNodeRequest",
]
