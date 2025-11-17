"""Main CLI entry point for ToDoWrite."""

import getpass
import os
import sys
from pathlib import Path
from typing import Any, cast

import click
import jsonschema
from rich.console import Console
from rich.table import Table

from .version import __version__

# Import from the todowrite library
try:
    from todowrite import (
        YAMLManager,
        delete_node,
        get_node,
        list_nodes,
        update_node,
    )
    from todowrite.core import Node, ToDoWrite, generate_node_id
except ImportError:
    click.echo(
        "Error: todowrite library not found. Please install it first: "
        "pip install todowrite",
    )
    sys.exit(1)


console = Console()


def get_current_username() -> str:
    """Get the current username from environment or system."""
    try:
        # Try environment variables first
        username = (
            os.environ.get("USER")
            or os.environ.get("USERNAME")
            or os.environ.get("LOGNAME")
        )
        if username:
            return username

        # Fallback to system calls
        try:
            return getpass.getuser()
        except OSError:
            # Final fallback - try a system call
            import pwd

            return pwd.getpwuid(os.getuid()).pw_name
    except Exception:
        # Ultimate fallback
        return "system"


def capitalize_status(status: str) -> str:
    """Capitalize status for display (e.g., 'in_progress' -> 'In Progress')."""
    status_mapping = {
        "planned": "Planned",
        "in_progress": "In Progress",
        "completed": "Completed",
        "blocked": "Blocked",
        "cancelled": "Cancelled",
    }
    return status_mapping.get(status, status.title())


# Helper functions for CLI validation and data processing
def normalize_layer(layer: str) -> str | None:
    """Normalize layer input to proper case (case-insensitive)."""
    layer_mapping = {
        "goal": "Goal",
        "concept": "Concept",
        "context": "Context",
        "constraints": "Constraints",
        "requirements": "Requirements",
        "acceptancecriteria": "AcceptanceCriteria",
        "acceptance_criteria": "AcceptanceCriteria",
        "acceptance-criteria": "AcceptanceCriteria",
        "interfacecontract": "InterfaceContract",
        "interface_contract": "InterfaceContract",
        "interface-contract": "InterfaceContract",
        "phase": "Phase",
        "step": "Step",
        "task": "Task",
        "subtask": "SubTask",
        "sub_task": "SubTask",
        "sub-task": "SubTask",
        "command": "Command",
    }
    return layer_mapping.get(layer.lower())


def validate_and_normalize_severity(severity: str) -> str | None:
    """Validate and normalize severity input."""
    severity_mapping = {
        "low": "low",
        "medium": "medium",
        "med": "medium",
        "high": "high",
        "critical": "critical",
    }
    return severity_mapping.get(severity.lower())


def validate_and_normalize_work_type(work_type: str) -> str | None:
    """Validate and normalize work_type input."""
    work_type_mapping = {
        "architecture": "architecture",
        "spec": "spec",
        "interface": "interface",
        "validation": "validation",
        "implementation": "implementation",
        "development": "implementation",
        "docs": "docs",
        "operations": "ops",
        "ops": "ops",
        "refactor": "refactor",
        "chore": "chore",
        "test": "test",
    }
    return work_type_mapping.get(work_type.lower())


def get_layer_prefix(layer: str) -> str:
    """Get the ID prefix for a layer type."""
    layer_prefixes = {
        "Goal": "GOAL",
        "Concept": "CON",
        "Context": "CTX",
        "Constraints": "CST",
        "Requirements": "R",
        "AcceptanceCriteria": "AC",
        "InterfaceContract": "IF",
        "Phase": "PH",
        "Step": "STP",
        "Task": "TSK",
        "SubTask": "SUB",
        "Command": "CMD",
    }
    return layer_prefixes.get(layer, layer[:3].upper())


def validate_parent_node(parent_id: str) -> bool:
    """Validate that a parent node exists."""
    try:
        parent_node = get_node(parent_id)
        return parent_node is not None
    except (ValueError, KeyError, RuntimeError):
        return False


def build_command_data(
    layer: str,
    ac_ref: str | None,
    run_shell: str | None,
    artifacts: str | None,
) -> dict[str, Any] | None:
    """Build command-specific data for Command layer nodes."""
    if layer != "Command":
        return None

    command_data = {}
    if ac_ref:
        command_data["ac_ref"] = ac_ref

    command_data["run"] = {}
    if run_shell:
        command_data["run"]["shell"] = run_shell

    if artifacts:
        command_data["artifacts"] = [
            artifact.strip() for artifact in artifacts.split(",")
        ]

    return command_data


def filter_nodes_by_criteria(
    nodes: dict[str, list],
    layer: str | None,
    owner: str | None,
    status: str | None,
) -> list[tuple[str, Any]]:
    """Filter nodes by layer, owner, and status criteria."""
    # Apply layer filter if specified
    if layer:
        normalized_layer = normalize_layer(layer) or layer.title()
        nodes = {k: v for k, v in nodes.items() if k == normalized_layer}

    # Apply additional filters
    filtered_nodes = []
    for layer_name, layer_nodes in nodes.items():
        for node in layer_nodes:
            # Owner filter
            if owner and not _node_matches_owner(node, owner):
                continue
            # Status filter
            if status and node.status.lower() != status.lower():
                continue
            filtered_nodes.append((layer_name, node))

    return filtered_nodes


def _node_matches_owner(node: Any, owner: str) -> bool:
    """Check if node matches owner criteria."""
    if not hasattr(node, "metadata") or not node.metadata:
        return False
    if not hasattr(node.metadata, "owner"):
        return False
    return node.metadata.owner.lower() == owner.lower()


def extract_node_metadata(node: Any) -> dict[str, str]:
    """Extract metadata values from a node with proper fallbacks."""
    metadata = {
        "owner": get_current_username(),
        "severity": "low",
        "work_type": "chore",
    }

    if hasattr(node, "metadata") and node.metadata:
        if hasattr(node.metadata, "owner"):
            metadata["owner"] = (
                getattr(node.metadata, "owner", "") or get_current_username()
            )
        if hasattr(node.metadata, "severity"):
            metadata["severity"] = (
                getattr(node.metadata, "severity", "") or "low"
            )
        if hasattr(node.metadata, "work_type"):
            metadata["work_type"] = (
                getattr(node.metadata, "work_type", "") or "chore"
            )

    return metadata


def format_node_for_display(
    layer_name: str,
    node: Any,
    metadata: dict[str, str],
) -> list[str]:
    """Format node data for table display."""
    title_display = (
        node.title[:30] + "..." if len(node.title) > 30 else node.title
    )
    id_display = node.id[:12] + "…" if len(node.id) > 12 else node.id
    owner_display = (
        metadata["owner"][:20] + "…"
        if len(metadata["owner"]) > 20
        else metadata["owner"]
    )

    return [
        layer_name,
        id_display,
        title_display,
        capitalize_status(node.status),
        f"{node.progress}%" if node.progress is not None else "0%",
        owner_display,
        metadata["severity"].title(),
        metadata["work_type"].title(),
    ]


def validate_and_normalize_status(status: str) -> str | None:
    """Validate and normalize status input."""
    status_mapping = {
        "planned": "planned",
        "inprogress": "in_progress",
        "in_progress": "in_progress",
        "completed": "completed",
        "blocked": "blocked",
        "cancelled": "cancelled",
    }
    return status_mapping.get(status.lower())


def build_update_data(
    title: str | None,
    description: str | None,
    owner: str | None,
    severity: str | None,
    work_type: str | None,
    status: str | None,
    progress: int | None,
    labels: str | None,
) -> dict[str, Any]:
    """Build update data dictionary from command line arguments."""
    update_data: dict[str, Any] = {}

    # Basic fields
    if title is not None:
        update_data["title"] = title
    if description is not None:
        update_data["description"] = description
    if progress is not None:
        update_data["progress"] = progress

    # Metadata fields
    metadata_updates = {}
    if owner is not None:
        metadata_updates["owner"] = owner
    if labels is not None:
        metadata_updates["labels"] = [
            label.strip() for label in labels.split(",")
        ]

    # Validated metadata fields
    if severity is not None:
        severity_normalized = validate_and_normalize_severity(severity)
        if not severity_normalized:
            valid_severities = ", ".join(
                sorted(["low", "medium", "med", "high", "critical"])
            )
            raise ValueError(
                f"Invalid severity: '{severity}'. "
                f"Valid options: {valid_severities}"
            )
        metadata_updates["severity"] = severity_normalized

    if work_type is not None:
        work_type_normalized = validate_and_normalize_work_type(work_type)
        if not work_type_normalized:
            valid_work_types = ", ".join(
                sorted(
                    [
                        "architecture",
                        "spec",
                        "interface",
                        "validation",
                        "implementation",
                        "development",
                        "docs",
                        "ops",
                        "refactor",
                        "chore",
                        "test",
                    ]
                )
            )
            raise ValueError(
                f"Invalid work_type: '{work_type}'. "
                f"Valid options: {valid_work_types}"
            )
        metadata_updates["work_type"] = work_type_normalized

    if metadata_updates:
        update_data["metadata"] = metadata_updates

    # Status field
    if status is not None:
        status_normalized = validate_and_normalize_status(status)
        if not status_normalized:
            valid_statuses = ", ".join(
                sorted(
                    [
                        "planned",
                        "inprogress",
                        "in_progress",
                        "completed",
                        "blocked",
                        "cancelled",
                    ]
                )
            )
            raise ValueError(
                f"Invalid status: '{status}'. Valid options: {valid_statuses}"
            )
        update_data["status"] = status_normalized

    return update_data


def update_command_data(
    update_data: dict[str, Any],
    ac_ref: str | None,
    run_shell: str | None,
    artifacts: str | None,
) -> None:
    """Update command-specific data if provided."""
    command_updates = {}
    if ac_ref is not None:
        command_updates["ac_ref"] = ac_ref
    if run_shell is not None:
        command_updates["run"] = {"shell": run_shell}
    if artifacts is not None:
        command_updates["artifacts"] = [
            artifact.strip() for artifact in artifacts.split(",")
        ]

    if command_updates:
        update_data["command"] = command_updates


def display_update_results(
    updated_node: Any, original_fields: dict[str, Any]
) -> None:
    """Display the results of a node update."""
    console.print(
        f"[green]✓[/green] Updated "
        f"{getattr(updated_node, 'id', 'Unknown')}: "
        f"{getattr(updated_node, 'title', 'Unknown')}"
    )

    if "status" in original_fields:
        console.print(
            f"  Status: {getattr(updated_node, 'status', 'Unknown')}"
        )
    if "progress" in original_fields:
        console.print(f"  Progress: {getattr(updated_node, 'progress', 0)}%")
    if (
        "metadata" in original_fields
        and "owner" in original_fields["metadata"]
    ):
        owner_val = getattr(updated_node, "owner", None)
        if (
            not owner_val
            and hasattr(updated_node, "metadata")
            and updated_node.metadata
        ):
            owner_val = getattr(updated_node.metadata, "owner", None)
        owner_val = owner_val or "N/A"
        console.print(f"  Owner: {owner_val}")


def get_app(
    database_path: str | None = None,
    _yaml_base_path: str | None = None,
) -> ToDoWrite:
    """Get or create ToDoWrite application instance using simplified library

    Args:
        database_path: Path to database file or full database URL
        _yaml_base_path: Base path for YAML files (currently unused)

    Returns:
        Configured ToDoWrite application instance
    """
    if database_path:
        # Expand ~ to user home directory
        database_path = os.path.expanduser(database_path)
        # Convert file path to SQLite URL
        if not database_path.startswith(("sqlite:///", "postgresql://")):
            db_url = f"sqlite:///{database_path}"
        else:
            db_url = database_path

        # Use library's simplified connection
        app = ToDoWrite(database_url=db_url)
    else:
        # Let library handle auto-detection (PostgreSQL → SQLite → YAML)
        app = ToDoWrite("sqlite:///todowrite.db")

    # Initialize database through library
    app.init_database()
    return app


@click.group()
@click.version_option(version=__version__)
@click.option(
    "--storage-preference",
    type=click.Choice(["auto", "postgresql_only", "sqlite_only", "yaml_only"]),
    default="auto",
    help="Override default storage preference "
    "(auto=auto-detect, postgresql_only, sqlite_only, yaml_only)",
)
@click.pass_context
def cli(ctx: click.Context, storage_preference: str) -> None:
    """A CLI for the ToDoWrite application."""
    ctx.ensure_object(dict)
    ctx.obj["storage_preference"] = storage_preference

    # Set storage preference for library globally
    if storage_preference != "auto":
        os.environ["TODOWRITE_STORAGE_PREFERENCE"] = storage_preference


@cli.command()
@click.option(
    "--database-path",
    "-d",
    default=None,
    help="Database file path (default: auto-detect via library)",
)
@click.option(
    "--yaml-path",
    "-y",
    default=None,
    help="YAML configuration path (default: auto-detect via library)",
)
@click.pass_context
def init(
    ctx: click.Context, database_path: str | None, yaml_path: str | None
) -> None:
    """Initialize the database."""
    # Pass storage preference from context to library via environment
    if ctx.obj.get("storage_preference"):
        os.environ["TODOWRITE_STORAGE_PREFERENCE"] = ctx.obj[
            "storage_preference"
        ]

    app = get_app(database_path, yaml_path)

    try:
        console.print(f"Storage type: {app.storage.backend_name}")
        console.print("[green]✓[/green] Database initialized successfully!")
        if hasattr(app, "db_url") and app.db_url:
            console.print(f"Database URL: {app.db_url}")
    except (OSError, ValueError, RuntimeError) as e:
        console.print(f"[red]✗[/red] Error initializing database: {e}")
        sys.exit(1)


@cli.command()
@click.option(
    "--layer",
    "-l",
    help=(
        "Layer type (case-insensitive: goal, concept, context, constraints, "
        "requirements, acceptancecriteria, interfacecontract, phase, step, "
        "task, subtask, command)"
    ),
    required=True,
)
@click.option(
    "--title",
    "-t",
    required=True,
    help="Title of the node",
)
@click.option(
    "--description",
    "-d",
    help="Description of the node",
)
@click.option(
    "--owner",
    help="Owner of the node",
)
@click.option(
    "--labels",
    help="Comma-separated labels",
)
@click.option(
    "--severity",
    help="Severity level (case-insensitive: low, med, medium, high, critical)",
)
@click.option(
    "--work-type",
    help="Type of work",
)
@click.option(
    "--ac-ref",
    help="Acceptance criteria reference (for Commands)",
)
@click.option(
    "--run-shell",
    help="Shell command to run (for Commands)",
)
@click.option(
    "--artifacts",
    help="Comma-separated artifact paths (for Commands)",
)
@click.option(
    "--parent-id",
    help="Parent node ID to link this node as a child",
)
@click.pass_context
def create(
    _: click.Context,
    layer: str,
    title: str,
    description: str,
    owner: str | None,
    labels: str | None,
    severity: str | None,
    work_type: str | None,
    ac_ref: str | None,
    run_shell: str | None,
    artifacts: str | None,
    parent_id: str | None,
) -> None:
    """Creates a new node."""
    # Validate and normalize layer
    layer_normalized = normalize_layer(layer)
    if not layer_normalized:
        valid_options = ", ".join(
            sorted(
                [
                    "goal",
                    "concept",
                    "context",
                    "constraints",
                    "requirements",
                    "acceptancecriteria",
                    "interfacecontract",
                    "phase",
                    "step",
                    "task",
                    "subtask",
                    "command",
                ]
            )
        )
        console.print(
            f"[red]✗[/red] Invalid layer: '{layer}'. "
            f"Valid options: {valid_options}"
        )
        sys.exit(1)

    layer = layer_normalized

    # Build node data
    prefix = get_layer_prefix(layer)
    node_data: dict[str, Any] = {
        "id": generate_node_id(prefix),
        "layer": layer,
        "title": title,
        "description": description or "",
        "links": {"parents": [], "children": []},
        "metadata": {},
    }

    # Handle parent linking if parent_id is provided
    if parent_id:
        if not validate_parent_node(parent_id):
            console.print(
                f"[red]✗[/red] Parent node with ID '{parent_id}' not found"
            )
            sys.exit(1)

        node_data["links"]["parents"] = [parent_id]
        console.print(f"[green]✓[/green] Will link to parent: {parent_id}")

    # Add metadata
    metadata = cast("dict[str, Any]", node_data["metadata"])
    metadata["owner"] = owner or get_current_username()

    if labels:
        metadata["labels"] = [label.strip() for label in labels.split(",")]

    if severity:
        severity_normalized = validate_and_normalize_severity(severity)
        if not severity_normalized:
            valid_severities = ", ".join(
                sorted(["low", "medium", "med", "high", "critical"])
            )
            console.print(
                f"[red]✗[/red] Invalid severity: '{severity}'. "
                f"Valid options: {valid_severities}"
            )
            sys.exit(1)
        metadata["severity"] = severity_normalized

    if work_type:
        work_type_normalized = validate_and_normalize_work_type(work_type)
        if not work_type_normalized:
            valid_work_types = ", ".join(
                sorted(
                    [
                        "architecture",
                        "spec",
                        "interface",
                        "validation",
                        "implementation",
                        "development",
                        "docs",
                        "ops",
                        "refactor",
                        "chore",
                        "test",
                    ]
                )
            )
            console.print(
                f"[red]✗[/red] Invalid work_type: '{work_type}'. "
                f"Valid options: {valid_work_types}"
            )
            sys.exit(1)
        metadata["work_type"] = work_type_normalized

    # Add command-specific data ONLY for Command layer
    if layer == "Command":
        command_data = build_command_data(layer, ac_ref, run_shell, artifacts)
        if command_data:
            node_data["command"] = command_data

    try:
        # Get app instance and create node
        app = get_app()
        node = app.create_node(node_data)

        # If parent linking was specified, update the parent node's children
        if parent_id:
            try:
                # Use the app instance to link nodes
                success = app.link_nodes(parent_id, node.id)
                if success:
                    success_msg = (
                        f"[green]✓[/green] Linked parent {parent_id} "
                        f"→ child {node.id}"
                    )
                    console.print(success_msg)
            except (
                ValueError,
                KeyError,
                RuntimeError,
            ) as e:
                warning_msg = (
                    f"[yellow]⚠[/yellow] Warning: Could not link "
                    f"parent → child: {e}"
                )
                console.print(warning_msg)

        console.print(
            f"[green]✓[/green] Created {layer}: {node.title} (ID: {node.id})"
        )
    except (
        ValueError,
        KeyError,
        AttributeError,
        jsonschema.ValidationError,
        RuntimeError,
    ) as e:
        console.print(f"[red]✗[/red] Error creating node: {e}")
        sys.exit(1)


@cli.command()
@click.argument("node_id")
@click.pass_context
def get(_: click.Context, node_id: str) -> None:
    """Gets a node by its ID."""
    try:
        node = cast("Any", get_node(node_id))
        if node:
            table = Table(title=f"Node: {node.id}")
            table.add_column("Property", style="cyan")
            table.add_column("Value", style="magenta")

            table.add_row("ID", node.id)
            table.add_row("Layer", node.layer)
            table.add_row("Title", node.title)
            table.add_row("Description", node.description)
            table.add_row("Status", capitalize_status(node.status))
            table.add_row(
                "Progress",
                f"{node.progress}%" if node.progress is not None else "0%",
            )

            if hasattr(node, "owner") and node.owner:
                table.add_row("Owner", node.owner)
            if hasattr(node, "severity") and node.severity:
                table.add_row("Severity", node.severity)
            if hasattr(node, "work_type") and node.work_type:
                table.add_row("Work Type", node.work_type)

            console.print(table)
        else:
            console.print(f"[red]✗[/red] Node with ID '{node_id}' not found")
            sys.exit(1)
    except (ValueError, KeyError, RuntimeError) as e:
        console.print(f"[red]✗[/red] Error getting node: {e}")
        sys.exit(1)


@cli.command()
@click.option(
    "--layer",
    "-l",
    help="Filter by layer (Goal, Task, Concept, Command)",
)
@click.option(
    "--owner",
    "-o",
    help="Filter by owner",
)
@click.option(
    "--status",
    "-s",
    help="Filter by status",
)
@click.pass_context
def list_command(
    _: click.Context,
    layer: str | None,
    owner: str | None,
    status: str | None,
) -> None:
    """Lists all the nodes."""

    try:
        app = get_app()
        all_nodes = app.list_nodes()

        # Group nodes by layer
        nodes = {}
        for node in all_nodes:
            layer_name = node.layer
            if layer_name not in nodes:
                nodes[layer_name] = []
            nodes[layer_name].append(node)

        if layer:
            nodes = {k: v for k, v in nodes.items() if k == layer}

        all_nodes: list[tuple[str, Node]] = []
        for layer_name, layer_nodes in nodes.items():
            for node in layer_nodes:
                all_nodes.append((layer_name, node))

        if not all_nodes:
            console.print("[yellow]No nodes found[/yellow]")
            return

        table = Table(title="All Nodes")
        table.add_column("Layer", style="cyan")
        table.add_column("ID", style="magenta")
        table.add_column("Title", style="green")
        table.add_column("Status", style="yellow")
        table.add_column("Progress", style="blue")
        table.add_column("Owner", style="red")

        for layer_name, node in all_nodes:
            # Apply filters
            if owner and (
                hasattr(node, "metadata") and node.metadata.owner != owner
            ):
                continue
            if status and node.status != status:
                continue

            # Get owner from metadata with proper fallback
            owner_val = get_current_username()  # Default to current user
            if hasattr(node, "metadata") and node.metadata:
                owner_val = (
                    getattr(node.metadata, "owner", "")
                    or get_current_username()
                )

            table.add_row(
                layer_name,
                node.id,
                node.title,
                capitalize_status(node.status),
                f"{node.progress or 0}%",
                owner_val,
            )

        console.print(table)
    except Exception as e:
        console.print(f"[red]✗[/red] Error listing nodes: {e}")
        sys.exit(1)


@cli.group()
def status() -> None:
    """Status management commands for tracking task progress."""


@status.command()
@click.argument("node_id")
@click.pass_context
def show(_: click.Context, node_id: str) -> None:
    """Show detailed status information about a node."""
    app = get_app()

    try:
        node = app.get_node(node_id)
        if not node:
            console.print(f"[red]✗[/red] Node with ID '{node_id}' not found")
            sys.exit(1)

        table = Table(title=f"Node Status: {node.title}")
        table.add_column("Property", style="cyan")
        table.add_column("Value", style="magenta")

        table.add_row("ID", node.id)
        table.add_row("Layer", node.layer)
        table.add_row("Title", node.title)
        table.add_row("Description", node.description)
        table.add_row("Status", capitalize_status(node.status))
        table.add_row(
            "Progress",
            f"{node.progress}%" if node.progress is not None else "0%",
        )
        table.add_row("Owner", node.metadata.owner or get_current_username())
        table.add_row("Severity", (node.metadata.severity or "low").title())
        table.add_row(
            "Work Type", (node.metadata.work_type or "chore").title()
        )

        console.print(table)
    except Exception as e:
        console.print(f"[red]✗[/red] Error showing node status: {e}")
        sys.exit(1)


@status.command()
@click.argument("node_id")
@click.pass_context
def complete(_: click.Context, node_id: str) -> None:
    """Mark a node as completed."""
    app = get_app()

    try:
        node = app.get_node(node_id)
        if not node:
            console.print(f"[red]✗[/red] Node with ID '{node_id}' not found")
            sys.exit(1)

        if node.status == "completed":
            console.print(
                f"[yellow]Node {node_id} is already completed[/yellow]"
            )
            return

        update_data = {
            "status": "completed",
            "progress": 100,
            "completion_date": "2024-01-01",  # Default date
        }

        updated_node = app.update_node(node_id, update_data)
        if updated_node:
            console.print(
                f"[green]✓[/green] Completed {node_id}: {updated_node.title}"
            )
        else:
            console.print(
                f"[green]✓[/green] Completed {node_id}: Unknown title"
            )
    except Exception as e:
        console.print(f"[red]✗[/red] Error completing node: {e}")
        sys.exit(1)


@status.command()
@click.option(
    "--layer",
    "-l",
    help="Filter by layer type",
)
@click.option(
    "--owner",
    "-o",
    help="Filter by owner",
)
@click.option(
    "--status",
    "-s",
    help="Filter by status",
)
@click.pass_context
def global_status(
    _: click.Context,
    layer: str | None,
    owner: str | None,
    status: str | None,
) -> None:
    """Show status information for all nodes."""
    try:
        nodes = list_nodes()
        filtered_nodes = filter_nodes_by_criteria(nodes, layer, owner, status)

        if not filtered_nodes:
            console.print("[yellow]No nodes found matching criteria[/yellow]")
            return

        table = Table(title="Global Status Overview")
        table.add_column("Layer", style="cyan")
        table.add_column("ID", style="magenta")
        table.add_column("Title", style="green")
        table.add_column("Status", style="yellow")
        table.add_column("Progress", style="blue")
        table.add_column("Owner", style="red")
        table.add_column("Severity", style="white")
        table.add_column("Work Type", style="cyan")

        for layer_name, node in filtered_nodes:
            metadata = extract_node_metadata(node)
            display_row = format_node_for_display(layer_name, node, metadata)
            table.add_row(*display_row)

        console.print(table)
        _display_summary_statistics(filtered_nodes)

    except Exception as e:
        console.print(f"[red]✗[/red] Error showing global status: {e}")
        sys.exit(1)


def _display_summary_statistics(filtered_nodes: list[tuple[str, Any]]) -> None:
    """Display summary statistics for filtered nodes."""
    total_nodes = len(filtered_nodes)
    completed_nodes = len(
        [n for _, n in filtered_nodes if n.status == "completed"]
    )
    in_progress_nodes = len(
        [n for _, n in filtered_nodes if n.status == "in_progress"]
    )

    console.print("\n[bold]Summary:[/bold]")
    console.print(f"Total nodes: {total_nodes}")

    if total_nodes > 0:
        percentage = completed_nodes / total_nodes * 100
        console.print(f"Completed: {completed_nodes} ({percentage:.1f}%)")
    else:
        console.print("Completed: 0")

    if total_nodes > 0:
        percentage = in_progress_nodes / total_nodes * 100
        console.print(f"In Progress: {in_progress_nodes} ({percentage:.1f}%)")
    else:
        console.print("In Progress: 0")


@cli.command()
@click.option(
    "--yaml-path",
    "-y",
    default="./configs",
    help="Path to YAML files directory",
)
@click.pass_context
def import_yaml(_: click.Context, yaml_path: str) -> None:
    """Import YAML files from configs/ directory to database."""
    app = get_app()

    try:
        # Create a custom YAMLManager that uses the specified path
        yaml_manager = YAMLManager(app)

        # Override the paths if custom path provided
        if yaml_path != "./configs":
            custom_path = Path(yaml_path)
            yaml_manager.yaml_base_path = custom_path
            yaml_manager.plans_path = custom_path / "plans"
            yaml_manager.commands_path = custom_path / "commands"

        results = yaml_manager.import_yaml_files()

        console.print("[green]✓[/green] Import completed:")
        console.print(f"  Files processed: {results['total_files']}")
        console.print(f"  Nodes imported: {results['total_imported']}")
        console.print(f"  Errors: {len(results['errors'])}")

        if results["errors"]:
            console.print("[red]Errors encountered:[/red]")
            for error in results["errors"]:
                console.print(f"  {error}")
    except Exception as e:
        console.print(f"[red]✗[/red] Error importing YAML: {e}")
        sys.exit(1)


@cli.command()
@click.option(
    "--output",
    "-o",
    default="./exported",
    help="Output directory for YAML files",
)
@click.pass_context
def export_yaml(_: click.Context, output: str) -> None:
    """Export database content to YAML files."""
    app = get_app()

    try:
        yaml_manager = YAMLManager(app)
        results = yaml_manager.export_to_yaml(Path(output))

        console.print("[green]✓[/green] Export completed:")
        console.print(f"  Nodes exported: {results['total_nodes']}")
        console.print(f"  Files created: {results['total_exported']}")
        console.print(f"  Errors: {len(results['errors'])}")

        if results["errors"]:
            console.print("[red]Errors encountered:[/red]")
            for error in results["errors"]:
                console.print(f"  {error}")
    except Exception as e:
        console.print(f"[red]✗[/red] Error exporting YAML: {e}")
        sys.exit(1)


@cli.command()
@click.pass_context
def sync_status(_: click.Context) -> None:
    """Check synchronization status between YAML files and database."""
    app = get_app()

    try:
        yaml_manager = YAMLManager(app)
        sync_status = yaml_manager.check_yaml_sync()

        table = Table(title="YAML Database Sync Status")
        table.add_column("Type", style="cyan")
        table.add_column("Count", style="magenta")

        table.add_row("Database only", str(len(sync_status["database_only"])))
        table.add_row("YAML only", str(len(sync_status["yaml_only"])))
        table.add_row("Both", str(len(sync_status["both"])))

        console.print(table)

        if sync_status["database_only"]:
            console.print("[yellow]Database only nodes:[/yellow]")
            for node_id in sync_status["database_only"][:10]:  # Show first 10
                console.print(f"  {node_id}")
            if len(sync_status["database_only"]) > 10:
                console.print(
                    f"  ... and {len(sync_status['database_only']) - 10} more"
                )

        if sync_status["yaml_only"]:
            console.print("[yellow]YAML only nodes:[/yellow]")
            for node_id in sync_status["yaml_only"][:10]:  # Show first 10
                console.print(f"  {node_id}")
            if len(sync_status["yaml_only"]) > 10:
                console.print(
                    f"  ... and {len(sync_status['yaml_only']) - 10} more"
                )
    except Exception as e:
        console.print(f"[red]✗[/red] Error checking sync status: {e}")
        sys.exit(1)


@cli.command()
@click.pass_context
def db_status(ctx: click.Context) -> None:
    """Show storage configuration and status using simplified library approach.

    Displays current database URL, storage backend info, and system status.
    """
    try:
        # Use library's simplified connection
        app = get_app()

        # Show storage info using library's approach
        table = Table(title="Database Status")
        table.add_column("Property", style="cyan")
        table.add_column("Value", style="magenta")

        # Show storage type
        storage_type = app.storage_type.value
        table.add_row("Storage Type", storage_type.title())

        # Show database URL if available
        if hasattr(app, "db_url") and app.db_url:
            table.add_row("Database URL", app.db_url)
        else:
            table.add_row("Database URL", "N/A (YAML mode)")

        # Show node counts using library
        nodes = app.get_all_nodes()
        total_nodes = sum(len(layer_nodes) for layer_nodes in nodes.values())
        table.add_row("Total Nodes", str(total_nodes))

        # Show storage preference
        preference = ctx.obj.get("storage_preference", "auto")
        table.add_row("Storage Preference", preference)

        console.print(table)

    except Exception as e:
        console.print(f"[red]✗[/red] Error getting database status: {e}")
        sys.exit(1)


@cli.command()
@click.argument("node_id")
@click.pass_context
def delete(_: click.Context, node_id: str) -> None:
    """Delete a node by its ID."""
    try:
        node = cast("Any", get_node(node_id))
        if not node:
            console.print(f"[red]✗[/red] Node with ID '{node_id}' not found")
            sys.exit(1)

        delete_node(node_id)
        console.print(f"[green]✓[/green] Deleted {node_id}: {node.title}")
    except Exception as e:
        console.print(f"[red]✗[/red] Error deleting node: {e}")
        sys.exit(1)


@cli.command()
@click.argument("node_id")
@click.option("--title", help="Update title")
@click.option("--description", help="Update description")
@click.option("--owner", help="Update owner")
@click.option(
    "--severity",
    help="Update severity (case-insensitive: low, medium, med, high, "
    "critical)",
)
@click.option(
    "--work-type",
    help="Update work type (case-insensitive: architecture, spec, interface, "
    "validation, implementation, docs, ops, refactor, chore, test)",
)
@click.option(
    "--status",
    help="Update status (case-insensitive: planned, in_progress, completed, "
    "blocked, cancelled)",
)
@click.option(
    "--progress",
    type=click.IntRange(0, 100),
    help="Update progress percentage",
)
@click.option("--labels", help="Comma-separated labels")
# Command-specific options
@click.option(
    "--ac-ref", help="Update acceptance criteria reference (for Commands)"
)
@click.option("--run-shell", help="Update shell command (for Commands)")
@click.option(
    "--artifacts", help="Comma-separated artifact paths (for Commands)"
)
@click.pass_context
def update(
    _: click.Context,
    node_id: str,
    title: str | None,
    description: str | None,
    owner: str | None,
    severity: str | None,
    work_type: str | None,
    status: str | None,
    progress: int | None,
    labels: str | None,
    ac_ref: str | None,
    run_shell: str | None,
    artifacts: str | None,
) -> None:
    """Update a node's properties."""
    try:
        node = cast("Any", get_node(node_id))
        if not node:
            console.print(f"[red]✗[/red] Node with ID '{node_id}' not found")
            sys.exit(1)

        # Track what fields we're trying to update for result display
        original_fields = {}
        if title is not None:
            original_fields["title"] = title
        if status is not None:
            original_fields["status"] = status
        if progress is not None:
            original_fields["progress"] = progress
        if owner is not None:
            original_fields["metadata"] = {"owner": owner}

        # Build update data
        try:
            update_data = build_update_data(
                title,
                description,
                owner,
                severity,
                work_type,
                status,
                progress,
                labels,
            )
        except ValueError as e:
            console.print(f"[red]✗[/red] {e}")
            sys.exit(1)

        # Handle command-specific updates
        if node.layer == "Command":
            update_command_data(update_data, ac_ref, run_shell, artifacts)

        if not update_data:
            console.print("[yellow]⚠️[/yellow] No fields to update")
            return

        updated_node = update_node(node_id, update_data)
        if updated_node:
            display_update_results(updated_node, original_fields)

    except Exception as e:
        console.print(f"[red]✗[/red] Error updating node: {e}")
        sys.exit(1)


@cli.command()
@click.argument("query")
@click.pass_context
def search(_: click.Context, query: str) -> None:
    """Search for nodes by query string."""
    try:
        app = get_app()
        # Simple text search - look for query in title and description
        criteria = {"text_search": query}
        results = app.search_nodes(criteria)

        if not results:
            console.print(f"[yellow]No results found for '{query}'[/yellow]")
            return

        table = Table(title=f"Search Results for: {query}")
        table.add_column("Layer", style="cyan")
        table.add_column("ID", style="magenta")
        table.add_column("Title", style="green")
        table.add_column("Status", style="yellow")
        table.add_column("Progress", style="blue")
        table.add_column("Owner", style="red")

        for node in results:
            # Get owner from metadata with proper fallback
            owner_val = get_current_username()  # Default to current user
            if hasattr(node, "metadata") and node.metadata:
                owner_val = (
                    getattr(node.metadata, "owner", "")
                    or get_current_username()
                )

            table.add_row(
                node.layer,
                node.id,
                node.title,
                capitalize_status(node.status),
                f"{node.progress or 0}%",
                owner_val,
            )

        console.print(table)
    except Exception as e:
        console.print(f"[red]✗[/red] Error searching nodes: {e}")
        sys.exit(1)


def main() -> None:
    """Main entry point for the CLI."""
    cli()


if __name__ == "__main__":
    main()
