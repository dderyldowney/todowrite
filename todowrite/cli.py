"""
This module contains the CLI for the ToDoWrite application.
"""

from __future__ import annotations

import shlex
import subprocess
import sys
from pathlib import Path
from typing import Any, get_args

import click
import yaml

from .app import ToDoWrite
from .db.config import (
    StoragePreference,
    get_setup_guidance,
    get_storage_info,
    set_storage_preference,
)
from .types import LayerType, Node
from .utils import generate_node_id
from .yaml_manager import YAMLManager

LAYER_TO_PREFIX = {
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


@click.group()
@click.option(
    "--storage-preference",
    type=click.Choice(["auto", "postgresql_only", "sqlite_only", "yaml_only"]),
    help="Override default storage preference",
)
@click.pass_context
def cli(ctx: click.Context, storage_preference: str) -> None:
    """A CLI for the ToDoWrite application."""
    # Ensure context object exists
    ctx.ensure_object(dict)

    # Set storage preference if provided
    if storage_preference:
        set_storage_preference(StoragePreference(storage_preference))
        ctx.obj["storage_preference"] = storage_preference


@cli.command()
def init() -> None:
    """Initializes the database."""
    app: ToDoWrite = ToDoWrite()
    app.init_database()
    click.echo("Database initialized.")


@cli.command()
@click.argument("layer")
@click.argument("title")
@click.argument("description")
@click.option("--parent", default=None, help="The parent of the node.")
def create(layer: str, title: str, description: str, parent: str | None) -> None:
    """Creates a new node."""
    if layer not in get_args(LayerType):
        click.echo(
            f"Error: Invalid layer type '{layer}'. Must be one of {get_args(LayerType)}"
        )
        return

    app: ToDoWrite = ToDoWrite()
    prefix: str | None = LAYER_TO_PREFIX.get(layer)
    if not prefix:
        click.echo(f"Error: Could not find prefix for layer '{layer}'.")
        return

    node_id: str = generate_node_id(prefix)
    node_data: dict[str, Any] = {
        "id": node_id,
        "layer": layer,
        "title": title,
        "description": description,
        "links": {"parents": [parent] if parent else [], "children": []},
        "metadata": {
            "owner": "system",
            "labels": [],
        },
    }
    try:
        node: Node = app.create_node(node_data)
        click.echo(f"Node created: {node.id}")
    except Exception as e:
        click.echo(f"Error creating node: {e}", err=True)
        import traceback

        click.echo(traceback.format_exc(), err=True)
        exit(1)


@cli.command()
@click.argument("node_id")
def get(node_id: str) -> None:
    """Gets a node by its ID."""
    app: ToDoWrite = ToDoWrite()
    node: Node | None = app.get_node(node_id)
    if node:
        click.echo(f"ID: {node.id}")
        click.echo(f"Layer: {node.layer}")
        click.echo(f"Title: {node.title}")
        click.echo(f"Description: {node.description}")
        click.echo(f"Status: {node.status}")
        click.echo(f"Owner: {node.metadata.owner}")
        click.echo(f"Labels: {node.metadata.labels}")
        click.echo(f"Severity: {node.metadata.severity}")
        click.echo(f"Work Type: {node.metadata.work_type}")
    else:
        click.echo("Node not found.")


@cli.command("list")
def list_nodes() -> None:
    """Lists all the nodes."""
    app: ToDoWrite = ToDoWrite()
    nodes: dict[str, list[Node]] = app.get_all_nodes()
    for layer, layer_nodes in nodes.items():
        click.echo(f"--- {layer} ---")
        for node in layer_nodes:
            click.echo(f"- {node.id}: {node.title}")


@cli.command("db-status")
@click.option(
    "--storage-preference",
    type=click.Choice(["auto", "postgresql_only", "sqlite_only", "yaml_only"]),
    help="Override storage preference for this check",
)
def db_status(storage_preference: str) -> None:
    """Show storage configuration and status."""
    click.echo("🗄️  ToDoWrite Storage Status")
    click.echo("=" * 30)

    # Set temporary preference if provided
    if storage_preference:
        set_storage_preference(StoragePreference(storage_preference))

    info = get_storage_info()

    click.echo(f"Storage Type: {info['type']}")
    click.echo(f"Priority Level: {info['priority']}")
    click.echo(f"Is Fallback: {info['fallback']}")
    click.echo(f"Storage Location: {info['url']}")
    click.echo(f"Preference: {info['preference']}")

    # Test storage connectivity
    try:
        app = ToDoWrite(auto_import=False)  # Disable auto-import for status check
        app.init_database()
        click.echo("Connection Status: ✅ Connected")

        # Count existing nodes
        if app.storage_type.value == "yaml":
            yaml_storage = app._get_yaml_storage()
            node_count = yaml_storage.count_nodes()
            click.echo(f"Nodes in YAML Files: {node_count}")
        else:
            with app.get_db_session() as session:
                from .db.models import Node as DBNode

                node_count = session.query(DBNode).count()
                click.echo(f"Nodes in Database: {node_count}")

    except Exception as e:
        click.echo(f"Connection Status: ❌ Failed ({e})")

    # Show setup guidance
    click.echo(f"\n{get_setup_guidance()}")


@cli.command("import-yaml")
@click.option("--force", is_flag=True, help="Force import, overwriting existing nodes")
@click.option(
    "--dry-run", is_flag=True, help="Show what would be imported without doing it"
)
def import_yaml(force: bool, dry_run: bool) -> None:
    """Import YAML files from configs/ directory to database."""
    yaml_manager = YAMLManager()

    if dry_run:
        click.echo("🔍 DRY RUN: Checking what would be imported...")
    else:
        click.echo("📥 Importing YAML files to database...")

    results = yaml_manager.import_yaml_files(force=force, dry_run=dry_run)

    # Print summary
    click.echo("\n📊 Import Summary:")
    click.echo(f"Total files processed: {results['total_files']}")
    click.echo(f"Successfully imported: {results['total_imported']}")
    click.echo(f"Skipped (already exist): {len(results['skipped'])}")
    click.echo(f"Errors: {len(results['errors'])}")

    if results["errors"]:
        click.echo("\n❌ Errors encountered:")
        for error in results["errors"]:
            click.echo(f"  - {error}")

    if not dry_run and results["total_imported"] > 0:
        click.echo(
            f"\n✅ Successfully imported {results['total_imported']} files to database"
        )


@cli.command("export-yaml")
@click.option(
    "--output-dir", type=click.Path(), help="Output directory (default: configs/)"
)
@click.option("--no-backup", is_flag=True, help="Don't create backup of existing files")
def export_yaml(output_dir: str, no_backup: bool) -> None:
    """Export database content to YAML files."""
    yaml_manager = YAMLManager()

    click.echo("📤 Exporting database to YAML files...")

    output_path = Path(output_dir) if output_dir else None
    results = yaml_manager.export_to_yaml(
        output_dir=output_path, backup_existing=not no_backup
    )

    # Print summary
    click.echo("\n📊 Export Summary:")
    click.echo(f"Total nodes processed: {results['total_nodes']}")
    click.echo(f"Successfully exported: {results['total_exported']}")
    click.echo(f"Errors: {len(results['errors'])}")

    if results["errors"]:
        click.echo("\n❌ Errors encountered:")
        for error in results["errors"]:
            click.echo(f"  - {error}")

    if results["total_exported"] > 0:
        click.echo(
            f"\n✅ Successfully exported {results['total_exported']} nodes to YAML"
        )


@cli.command("sync-status")
def sync_status() -> None:
    """Check synchronization status between YAML files and database."""
    yaml_manager = YAMLManager()

    click.echo("🔍 Checking synchronization between YAML and database...")

    results = yaml_manager.check_yaml_sync()

    click.echo("\n📊 Synchronization Status:")
    click.echo(f"In both YAML and database: {len(results['both'])}")
    click.echo(f"Only in YAML files: {len(results['yaml_only'])}")
    click.echo(f"Only in database: {len(results['database_only'])}")

    if results["yaml_only"]:
        click.echo("\n📄 YAML-only nodes (can be imported):")
        for node_id in results["yaml_only"]:
            click.echo(f"  - {node_id}")

    if results["database_only"]:
        click.echo("\n🗄️  Database-only nodes (can be exported):")
        for node_id in results["database_only"]:
            click.echo(f"  - {node_id}")

    if not results["yaml_only"] and not results["database_only"]:
        click.echo("\n✅ YAML files and database are in sync!")


# ToDoWrite-specific commands for 12-layer framework management


@cli.group()
def todowrite() -> None:
    """ToDoWrite framework commands for 12-layer planning system."""
    pass


@todowrite.command()
@click.option("--strict", is_flag=True, help="Enable strict validation mode")
def validate_plan() -> None:
    """Validate all YAML files against ToDoWrite schema."""
    click.echo("🔍 Validating ToDoWrite planning files...")

    try:
        # Run schema validation
        result = subprocess.run(
            [sys.executable, "todowrite/tools/tw_validate.py"]
            + (
                ["--strict"] if click.get_current_context().params.get("strict") else []
            ),
            capture_output=True,
            text=True,
        )

        click.echo(result.stdout)
        if result.stderr:
            click.echo(result.stderr, err=True)

        if result.returncode == 0:
            click.echo("✅ Plan validation completed successfully")
        else:
            click.echo("❌ Plan validation failed", err=True)
            sys.exit(1)

    except Exception as e:
        click.echo(f"Error running validation: {e}", err=True)
        sys.exit(1)


@todowrite.command()
@click.option("--summary", is_flag=True, help="Show summary report only")
def trace_links() -> None:
    """Build and analyze traceability matrix for all planning layers."""
    click.echo("🔗 Building traceability matrix...")

    try:
        result = subprocess.run(
            [sys.executable, "todowrite/tools/tw_trace.py"]
            + (
                ["--summary"]
                if click.get_current_context().params.get("summary")
                else []
            ),
            capture_output=True,
            text=True,
        )

        click.echo(result.stdout)
        if result.stderr:
            click.echo(result.stderr, err=True)

        if result.returncode == 0:
            click.echo("✅ Traceability analysis completed")
        else:
            click.echo("⚠️  Traceability analysis found issues", err=True)

    except Exception as e:
        click.echo(f"Error running traceability analysis: {e}", err=True)
        sys.exit(1)


@todowrite.command()
@click.option("--force", is_flag=True, help="Regenerate existing command stubs")
def generate_commands() -> None:
    """Generate executable command stubs from Acceptance Criteria."""
    click.echo("⚡ Generating command stubs from Acceptance Criteria...")

    try:
        result = subprocess.run(
            [sys.executable, "todowrite/tools/tw_stub_command.py"]
            + (["--force"] if click.get_current_context().params.get("force") else []),
            capture_output=True,
            text=True,
        )

        click.echo(result.stdout)
        if result.stderr:
            click.echo(result.stderr, err=True)

        if result.returncode == 0:
            click.echo("✅ Command generation completed")
        else:
            click.echo("❌ Command generation failed", err=True)
            sys.exit(1)

    except Exception as e:
        click.echo(f"Error generating commands: {e}", err=True)
        sys.exit(1)


@todowrite.command()
@click.argument("command_id", required=False)
@click.option("--all", is_flag=True, help="Execute all available commands")
@click.option(
    "--dry-run", is_flag=True, help="Show what would be executed without running"
)
def execute_commands(command_id: str, all: bool, dry_run: bool) -> None:
    """Execute ToDoWrite command stubs."""
    if not command_id and not all:
        click.echo("Error: Must specify either a command ID or --all flag")
        sys.exit(1)

    commands_dir = Path("configs/commands")
    if not commands_dir.exists():
        click.echo(
            "Error: Commands directory not found. Run 'todowrite generate-commands' first."
        )
        sys.exit(1)

    if all:
        command_files = list(commands_dir.glob("CMD-*.yaml"))
        if not command_files:
            click.echo("No command files found in configs/commands/")
            return
    else:
        command_file = commands_dir / f"{command_id}.yaml"
        if not command_file.exists():
            click.echo(f"Command file not found: {command_file}")
            sys.exit(1)
        command_files = [command_file]

    for cmd_file in command_files:
        try:
            with open(cmd_file) as f:
                cmd_data = yaml.safe_load(f)

            cmd_id = cmd_data.get("id", "Unknown")
            shell_cmd = cmd_data.get("command", {}).get("run", {}).get("shell", "")

            click.echo(f"\n🚀 Executing: {cmd_id}")
            click.echo(f"Command: {shell_cmd}")

            if dry_run:
                click.echo("(DRY RUN - not executed)")
                continue

            # Create results directory
            results_dir = Path("results") / cmd_id
            results_dir.mkdir(parents=True, exist_ok=True)

            # Execute command
            # Use shlex to split command safely instead of shell=True
            cmd_args = shlex.split(shell_cmd)
            result = subprocess.run(
                cmd_args, shell=False, capture_output=True, text=True
            )

            # Save execution log
            log_file = results_dir / "execution.log"
            with open(log_file, "w") as f:
                f.write(f"Command: {shell_cmd}\n")
                f.write(f"Exit Code: {result.returncode}\n")
                f.write(f"STDOUT:\n{result.stdout}\n")
                f.write(f"STDERR:\n{result.stderr}\n")

            if result.returncode == 0:
                click.echo(f"✅ {cmd_id} completed successfully")
            else:
                click.echo(f"❌ {cmd_id} failed (exit code: {result.returncode})")
                if result.stderr:
                    click.echo(f"Error: {result.stderr}")

        except Exception as e:
            click.echo(f"Error executing {cmd_file}: {e}", err=True)


@todowrite.command()
@click.option("--layer", help="Show only specific layer")
@click.option(
    "--format",
    type=click.Choice(["tree", "flat", "json"]),
    default="tree",
    help="Output format",
)
def show_hierarchy(layer: str, format: str) -> None:
    """Display the ToDoWrite planning hierarchy."""
    plans_dir = Path("configs/plans")

    if not plans_dir.exists():
        click.echo("Error: Plans directory not found")
        sys.exit(1)

    hierarchy = {}
    layer_order = [
        "goals",
        "concepts",
        "contexts",
        "constraints",
        "requirements",
        "acceptance_criteria",
        "interface_contracts",
        "phases",
        "steps",
        "tasks",
        "subtasks",
    ]

    # Load all nodes
    for layer_dir in layer_order:
        layer_path = plans_dir / layer_dir
        if layer_path.exists():
            layer_nodes = []
            for yaml_file in layer_path.glob("*.yaml"):
                try:
                    with open(yaml_file) as f:
                        node_data = yaml.safe_load(f)
                    layer_nodes.append(
                        {
                            "id": node_data.get("id", ""),
                            "title": node_data.get("title", ""),
                            "layer": node_data.get("layer", ""),
                            "parents": node_data.get("links", {}).get("parents", []),
                            "children": node_data.get("links", {}).get("children", []),
                        }
                    )
                except Exception as e:
                    click.echo(f"Warning: Could not load {yaml_file}: {e}")

            if layer_nodes:
                hierarchy[layer_dir] = layer_nodes

    # Add commands layer
    commands_dir = Path("configs/commands")
    if commands_dir.exists():
        command_nodes = []
        for yaml_file in commands_dir.glob("CMD-*.yaml"):
            try:
                with open(yaml_file) as f:
                    node_data = yaml.safe_load(f)
                command_nodes.append(
                    {
                        "id": node_data.get("id", ""),
                        "title": node_data.get("title", ""),
                        "layer": "Command",
                        "parents": node_data.get("links", {}).get("parents", []),
                        "children": node_data.get("links", {}).get("children", []),
                    }
                )
            except (yaml.YAMLError, FileNotFoundError, PermissionError):
                # Skip invalid YAML files or files that can't be read
                continue
        if command_nodes:
            hierarchy["commands"] = command_nodes

    if format == "json":
        import json

        click.echo(json.dumps(hierarchy, indent=2))
    elif format == "flat":
        for layer_name, nodes in hierarchy.items():
            if layer and layer.lower() not in layer_name.lower():
                continue
            click.echo(f"\n--- {layer_name.upper()} ---")
            for node in nodes:
                click.echo(f"  {node['id']}: {node['title']}")
    else:  # tree format
        click.echo("📋 ToDoWrite Planning Hierarchy")
        click.echo("=" * 40)
        for layer_name, nodes in hierarchy.items():
            if layer and layer.lower() not in layer_name.lower():
                continue
            click.echo(f"\n📁 {layer_name.replace('_', ' ').title()}")
            for node in nodes:
                click.echo(f"  └── {node['id']}: {node['title']}")
                if node["children"]:
                    for child in node["children"][:3]:  # Show first 3 children
                        click.echo(f"      └─> {child}")
                    if len(node["children"]) > 3:
                        click.echo(
                            f"      └─> ... and {len(node['children']) - 3} more"
                        )


@todowrite.command()
def check_soc() -> None:
    """Check Separation of Concerns compliance for layers 1-11."""
    click.echo("🔒 Checking Separation of Concerns compliance...")

    try:
        result = subprocess.run(
            [sys.executable, "todowrite/tools/tw_lint_soc.py"],
            capture_output=True,
            text=True,
            shell=False,
        )

        click.echo(result.stdout)
        if result.stderr:
            click.echo(result.stderr, err=True)

        if result.returncode == 0:
            click.echo("✅ All files comply with SoC requirements")
        else:
            click.echo("❌ SoC violations found", err=True)
            sys.exit(1)

    except Exception as e:
        click.echo(f"Error running SoC check: {e}", err=True)
        sys.exit(1)


# Status Management Commands
@cli.group()
def status() -> None:
    """Status management commands for tracking task progress."""
    pass


@status.command("update")
@click.argument("node_id")
@click.option(
    "--status",
    type=click.Choice(["planned", "in_progress", "completed", "blocked", "cancelled"]),
    required=True,
    help="Set the status of the node",
)
@click.option(
    "--progress", type=click.IntRange(0, 100), help="Set progress percentage (0-100)"
)
@click.option("--owner", help="Set the owner of the node")
@click.option("--assignee", help="Set the assignee of the node")
@click.option("--started-date", help="Set the started date (ISO 8601 format)")
@click.option("--completion-date", help="Set the completion date (ISO 8601 format)")
def update_status(
    node_id: str,
    status: str,
    progress: int,
    owner: str,
    assignee: str,
    started_date: str,
    completion_date: str,
) -> None:
    """Update the status of a node."""
    app: ToDoWrite = ToDoWrite()

    # Validate node exists
    node = app.get_node(node_id)
    if not node:
        click.echo(f"Error: Node {node_id} not found", err=True)
        sys.exit(1)

    # Validate status transition
    if node.status == "completed" and status != "completed":
        click.echo(
            "Warning: Cannot change status from 'completed' to other states", err=True
        )

    # Prepare update data
    update_data = node.to_dict()
    update_data["status"] = status

    # Update metadata fields
    if progress is not None:
        update_data["progress"] = progress
    if owner:
        update_data["metadata"]["owner"] = owner
    if assignee:
        update_data["metadata"]["assignee"] = assignee
    if started_date:
        update_data["started_date"] = started_date
    if completion_date:
        update_data["completion_date"] = completion_date

    # Save the node
    try:
        updated_node = app.update_node(node_id, update_data)
        if updated_node:
            click.echo(f"✅ Updated {node_id}: status={status}")
            if progress is not None:
                click.echo(f"   Progress: {progress}%")
            if owner:
                click.echo(f"   Owner: {owner}")
            if assignee:
                click.echo(f"   Assignee: {assignee}")
            if started_date:
                click.echo(f"   Started: {started_date}")
            if completion_date:
                click.echo(f"   Completed: {completion_date}")
        else:
            click.echo(f"Error: Failed to update {node_id}", err=True)
            sys.exit(1)
    except Exception as e:
        click.echo(f"Error updating node: {e}", err=True)
        sys.exit(1)


@status.command("show")
@click.argument("node_id")
def show_progress(node_id: str) -> None:
    """Show progress and status details for a node."""
    app: ToDoWrite = ToDoWrite()
    node = app.get_node(node_id)

    if not node:
        click.echo(f"Error: Node {node_id} not found", err=True)
        sys.exit(1)

    click.echo(f"📊 Node: {node_id}")
    click.echo(f"   Status: {node.status}")
    click.echo(f"   Layer: {node.layer}")
    click.echo(f"   Title: {node.title}")
    click.echo(f"   Description: {node.description}")

    # Status tracking fields
    click.echo(f"   Owner: {node.metadata.owner}")
    if hasattr(node.metadata, "assignee") and node.metadata.assignee:
        click.echo(f"   Assignee: {node.metadata.assignee}")

    # Progress and dates
    if hasattr(node, "progress"):
        click.echo(f"   Progress: {node.progress}%")

    if hasattr(node, "started_date"):
        click.echo(f"   Started: {node.started_date}")

    if hasattr(node, "completion_date"):
        click.echo(f"   Completed: {node.completion_date}")

    # Show hierarchy
    if node.links.parents:
        click.echo(f"   Parents: {', '.join(node.links.parents)}")
    if node.links.children:
        click.echo(f"   Children: {', '.join(node.links.children)}")

    # Show other metadata
    if node.metadata.severity:
        click.echo(f"   Severity: {node.metadata.severity}")
    if node.metadata.work_type:
        click.echo(f"   Work Type: {node.metadata.work_type}")
    if node.metadata.labels:
        click.echo(f"   Labels: {', '.join(node.metadata.labels)}")


@status.command("complete")
@click.argument("node_id")
@click.option("--message", help="Optional completion message")
def mark_complete(node_id: str, message: str) -> None:
    """Mark a node as completed."""
    app: ToDoWrite = ToDoWrite()
    node = app.get_node(node_id)

    if not node:
        click.echo(f"Error: Node {node_id} not found", err=True)
        sys.exit(1)

    if node.status == "completed":
        click.echo(f"Node {node_id} is already completed")
        return

    # Prepare update data
    update_data = node.to_dict()
    update_data["status"] = "completed"

    try:
        updated_node = app.update_node(node_id, update_data)
        if updated_node:
            click.echo(f"✅ Marked {node_id} as completed")
            if message:
                click.echo(f"   Message: {message}")
        else:
            click.echo(f"Error: Failed to mark {node_id} as complete", err=True)
            sys.exit(1)
    except Exception as e:
        click.echo(f"Error marking node as complete: {e}", err=True)
        sys.exit(1)


@status.command("report")
@click.option("--layer", help="Show report for specific layer only")
@click.option(
    "--format",
    type=click.Choice(["summary", "detailed", "json"]),
    default="summary",
    help="Report format",
)
def status_report(layer: str, format: str) -> None:
    """Generate a status report for all nodes."""
    app: ToDoWrite = ToDoWrite()
    nodes = app.get_all_nodes()

    if not layer:
        # Show all layers
        click.echo("📋 ToDoWrite Status Report")
        click.echo("=" * 50)

        for layer_name, layer_nodes in nodes.items():
            if layer_nodes:
                status_counts = {}
                for node in layer_nodes:
                    status = node.status
                    status_counts[status] = status_counts.get(status, 0) + 1

                click.echo(f"\n📁 {layer_name} ({len(layer_nodes)} nodes)")
                for status, count in status_counts.items():
                    emoji = {
                        "planned": "⏸️",
                        "in_progress": "🔄",
                        "completed": "✅",
                        "blocked": "🚫",
                        "cancelled": "❌",
                    }.get(status, "❓")
                    click.echo(f"   {emoji} {status}: {count}")
    else:
        # Show specific layer
        layer_nodes = nodes.get(layer, [])
        if not layer_nodes:
            click.echo(f"No nodes found for layer: {layer}")
            return

        if format == "json":
            import json

            report = {
                layer: [
                    {
                        "id": node.id,
                        "title": node.title,
                        "status": node.status,
                        "owner": node.metadata.owner,
                        "severity": node.metadata.severity,
                    }
                    for node in layer_nodes
                ]
            }
            click.echo(json.dumps(report, indent=2))
        elif format == "detailed":
            click.echo(f"📋 Detailed Status Report - {layer}")
            click.echo("=" * 40)
            for node in layer_nodes:
                emoji = {
                    "planned": "⏸️",
                    "in_progress": "🔄",
                    "completed": "✅",
                    "blocked": "🚫",
                    "cancelled": "❌",
                }.get(node.status, "❓")
                click.echo(f"  {emoji} {node.id}: {node.title}")
                click.echo(f"     Status: {node.status}")
                click.echo(f"     Owner: {node.metadata.owner}")
                if node.metadata.severity:
                    click.echo(f"     Severity: {node.metadata.severity}")
                click.echo()
        else:  # summary
            status_counts = {}
            for node in layer_nodes:
                status = node.status
                status_counts[status] = status_counts.get(status, 0) + 1

            click.echo(f"📋 Status Report - {layer}")
            click.echo("=" * 30)
            click.echo(f"Total nodes: {len(layer_nodes)}")
            for status, count in status_counts.items():
                emoji = {
                    "planned": "⏸️",
                    "in_progress": "🔄",
                    "completed": "✅",
                    "blocked": "🚫",
                    "cancelled": "❌",
                }.get(status, "❓")
                percentage = (count / len(layer_nodes)) * 100
                click.echo(f"  {emoji} {status}: {count} ({percentage:.1f}%)")


# ===== Project Utility Commands =====


@cli.group()
def utils() -> None:
    """Project utility commands for development and setup."""
    pass


@utils.command("check-schema")
def check_schema_cmd() -> None:
    """Check that schema changes are in the correct location."""
    try:
        from .project_manager import check_schema_changes

        if check_schema_changes():
            click.echo("✅ Schema location check passed!")
        else:
            click.echo("❌ Schema location check failed!")
            sys.exit(1)
    except ImportError:
        click.echo(
            "❌ Cannot import project utilities. Make sure todowrite is properly installed."
        )
        sys.exit(1)


@utils.command("check-deprecated")
def check_deprecated_cmd() -> None:
    """Check that deprecated schema hasn't been modified."""
    try:
        from .project_manager import check_deprecated_schema

        if check_deprecated_schema():
            click.echo("✅ Deprecated schema check passed!")
        else:
            click.echo("❌ Deprecated schema check failed!")
            sys.exit(1)
    except ImportError:
        click.echo(
            "❌ Cannot import project utilities. Make sure todowrite is properly installed."
        )
        sys.exit(1)


@utils.command("validate-schema")
@click.option(
    "--storage-type",
    type=click.Choice(["postgresql", "sqlite", "yaml", "all"]),
    default="all",
    help="Which storage backend(s) to validate",
)
@click.option(
    "--db-url",
    help="Database URL for validation (overrides auto-detection)",
)
def validate_schema_cmd(storage_type: str, db_url: str) -> None:
    """Validate schema compliance across storage backends."""
    try:
        from .schema_validator import get_schema_compliance_report

        click.echo("🔍 Validating schema compliance...")
        click.echo()

        if storage_type in ["all", "postgresql"] or storage_type in ["all", "sqlite"]:
            # Check databases if available
            try:
                # Create an app instance to get the engine
                app = ToDoWrite(db_url=db_url, auto_import=False)
                if app.engine:
                    if storage_type in ["all"]:
                        # Validate both PostgreSQL and SQLite if available
                        for db_type in ["postgresql", "sqlite"]:
                            try:
                                report = get_schema_compliance_report(
                                    db_type, engine=app.engine
                                )
                                _print_schema_report(report)
                            except Exception:
                                click.echo(
                                    f"⏭️  {db_type.upper()} validation failed (database may not be configured for this type)"
                                )
                    else:
                        # Validate specific type
                        report = get_schema_compliance_report(
                            storage_type, engine=app.engine
                        )
                        _print_schema_report(report)
                else:
                    click.echo("⏭️  No database available for validation...")
            except Exception as e:
                click.echo(f"⏭️  Database validation unavailable: {e}")

        if storage_type in ["all", "yaml"]:
            # Check YAML files
            try:
                report = get_schema_compliance_report("yaml")
                _print_schema_report(report)
            except Exception as e:
                click.echo(f"❌ YAML validation error: {e}")

        click.echo("\n✅ Schema validation complete!")

    except ImportError:
        click.echo(
            "❌ Cannot import schema validator. Make sure todowrite is properly installed."
        )
        sys.exit(1)


def _print_schema_report(report: dict[str, Any]) -> None:
    """Print a formatted schema compliance report."""
    storage_type = report["storage_type"].upper()

    if report["is_compliant"]:
        click.echo(f"✅ {storage_type}: Schema compliant")
    else:
        click.echo(f"❌ {storage_type}: Schema non-compliant")

    if report["errors"]:
        click.echo("   Errors:")
        for error in report["errors"]:
            click.echo(f"     - {error}")

    if report["warnings"]:
        click.echo("   Warnings:")
        for warning in report["warnings"]:
            click.echo(f"     - {warning}")

    if report["details"]:
        if "total_files" in report["details"]:
            total_files = report["details"]["total_files"]
            click.echo(f"   Files checked: {total_files}")

        if "file_counts" in report["details"]:
            file_counts = report["details"]["file_counts"]
            click.echo("   Files by layer:")
            for layer, count in file_counts.items():
                if count > 0:
                    click.echo(f"     {layer}: {count}")

    click.echo()


@utils.command("setup-integration")
@click.argument("project_path", type=click.Path(exists=True))
@click.option(
    "--db-type",
    type=click.Choice(["postgres", "sqlite"]),
    default="postgres",
    help="Database type to set up",
)
def setup_integration_cmd(project_path: str, db_type: str) -> None:
    """Set up ToDoWrite integration in a project."""
    try:
        from .project_manager import setup_integration

        if setup_integration(project_path, db_type):
            click.echo(f"✅ Integration set up successfully in {project_path}")
        else:
            click.echo("❌ Failed to set up integration!")
            sys.exit(1)
    except ImportError:
        click.echo(
            "❌ Cannot import project utilities. Make sure todowrite is properly installed."
        )
        sys.exit(1)


@utils.command("create-structure")
@click.argument("project_path", type=click.Path())
def create_structure_cmd(project_path: str) -> None:
    """Create a basic ToDoWrite project structure."""
    try:
        from .project_manager import create_project_structure

        if create_project_structure(project_path):
            click.echo(f"✅ Project structure created at {project_path}")
        else:
            click.echo("❌ Failed to create project structure!")
            sys.exit(1)
    except ImportError:
        click.echo(
            "❌ Cannot import project utilities. Make sure todowrite is properly installed."
        )
        sys.exit(1)


@utils.command("validate-setup")
@click.argument("project_path", type=click.Path(exists=True))
def validate_setup_cmd(project_path: str) -> None:
    """Validate that a project is properly set up for ToDoWrite."""
    try:
        from .project_manager import validate_project_setup

        results = validate_project_setup(project_path)

        click.echo(f"\n🔍 Validation results for {project_path}:")

        if results["valid"]:
            click.echo("✅ Project is properly set up!")
        else:
            click.echo("❌ Project setup issues found:")
            for issue in results["issues"]:
                click.echo(f"  - {issue}")

        if results["recommendations"]:
            click.echo("\n💡 Recommendations:")
            for rec in results["recommendations"]:
                click.echo(f"  - {rec}")

        if results["found_files"]:
            click.echo(
                f"\n📁 Found {len(results['found_files'])} key files/components:"
            )
            for item in results["found_files"]:
                click.echo(f"  - {item}")

        if not results["valid"]:
            sys.exit(1)

    except ImportError:
        click.echo(
            "❌ Cannot import project utilities. Make sure todowrite is properly installed."
        )
        sys.exit(1)


@utils.command("init-database-sql")
def init_database_sql_cmd() -> None:
    """Print PostgreSQL initialization SQL."""
    try:
        from .project_manager import init_database_sql

        sql = init_database_sql()
        click.echo(sql)
    except ImportError:
        click.echo(
            "❌ Cannot import project utilities. Make sure todowrite is properly installed."
        )
        sys.exit(1)


# Add utility commands to main CLI
cli.add_command(utils)

# Add status commands to main CLI
cli.add_command(status)

# Add todowrite subcommands to main CLI
cli.add_command(todowrite)


if __name__ == "__main__":
    cli()
