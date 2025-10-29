"""
This module contains the CLI for the ToDoWrite application.
"""

import subprocess
import sys
import uuid
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

    node_id: str = f"{prefix}-{uuid.uuid4().hex[:12].upper()}"
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
            result = subprocess.run(
                shell_cmd, shell=True, capture_output=True, text=True
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
            except Exception:
                pass
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


# Add todowrite subcommands to main CLI
cli.add_command(todowrite)


if __name__ == "__main__":
    cli()
