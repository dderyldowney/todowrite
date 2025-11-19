"""Main CLI entry point for ToDoWrite."""

import os
import sys

import click
from rich.console import Console
from rich.table import Table

from .version import __version__

# Import from the ToDoWrite library
try:
    from sqlalchemy import create_engine, select
    from sqlalchemy.orm import sessionmaker
    from todowrite.core.models import (
        AcceptanceCriteria,
        Command,
        Concept,
        Constraints,
        Context,
        Goal,
        InterfaceContract,
        Label,
        Phase,
        Requirements,
        Step,
        SubTask,
        Task,
    )
    from todowrite.core.schema_validator import (
        DatabaseInitializationError,
        initialize_database,
    )
except ImportError as e:
    click.echo(
        f"Error: ToDoWrite library not found: {e}. Please install it first: "
        "pip install todowrite",
    )
    sys.exit(1)


# Model mapping for CLI
MODEL_MAP = {
    "goal": Goal,
    "concept": Concept,
    "context": Context,
    "constraints": Constraints,
    "requirement": Requirements,
    "requirements": Requirements,
    "acceptancecriteria": AcceptanceCriteria,
    "acceptance_criteria": AcceptanceCriteria,
    "ac": AcceptanceCriteria,
    "interfacecontract": InterfaceContract,
    "interface_contract": InterfaceContract,
    "iface": InterfaceContract,
    "phase": Phase,
    "step": Step,
    "task": Task,
    "subtask": SubTask,
    "sub_task": SubTask,
    "command": Command,
    "label": Label,
}

# Reverse mapping for display
LAYER_NAMES = {
    Goal: "Goal",
    Concept: "Concept",
    Context: "Context",
    Constraints: "Constraints",
    Requirements: "Requirements",
    AcceptanceCriteria: "AcceptanceCriteria",
    InterfaceContract: "InterfaceContract",
    Phase: "Phase",
    Step: "Step",
    Task: "Task",
    SubTask: "SubTask",
    Command: "Command",
    Label: "Label",
}


def get_session(database_url: str = "sqlite:///todowrite.db"):
    """Get SQLAlchemy session."""
    engine = create_engine(database_url)
    Session = sessionmaker(bind=engine)
    return Session(), engine


def init_database(database_url: str = "sqlite:///todowrite.db") -> None:
    """Initialize database with all tables."""
    try:
        initialize_database(database_url)
    except DatabaseInitializationError as e:
        click.echo(f"Error initializing database: {e}")
        sys.exit(1)


console = Console()


def get_current_username() -> str:
    """Get the current username from environment or system."""
    try:
        username = (
            os.environ.get("USER")
            or os.environ.get("USERNAME")
            or os.environ.get("LOGNAME")
        )
        if username:
            return username

        import getpass

        return getpass.getuser()
    except (OSError, ImportError):
        return "unknown"


@click.group()
@click.version_option(version=__version__)
@click.option(
    "--database",
    default="todowrite.db",
    help="Database file path (default: todowrite.db)",
)
@click.pass_context
def cli(ctx: click.Context, database: str) -> None:
    """Todowrite CLI - Hierarchical Task Management System."""
    ctx.ensure_object(dict)

    # Convert to SQLite URL if needed
    if not database.startswith(("sqlite:///", "postgresql://")):
        database_path = os.path.expanduser(database)
        database_url = f"sqlite:///{database_path}"
    else:
        database_url = database

    ctx.obj["database_url"] = database_url
    ctx.obj["database_path"] = database


@cli.command()
@click.pass_context
def init(ctx: click.Context) -> None:
    """Initialize the database."""
    database_url = ctx.obj["database_url"]

    try:
        init_database(database_url)
        console.print(f"✅ Database initialized: {database_url}")
    except Exception as e:
        console.print(f"❌ Error initializing database: {e}")
        sys.exit(1)


@cli.command()
@click.option(
    "--layer",
    required=True,
    type=click.Choice(list(MODEL_MAP.keys())),
    help="Layer type to create",
)
@click.option("--title", required=True, help="Title of the item")
@click.option("--description", help="Description of the item")
@click.option("--owner", help="Owner of the item")
@click.option("--severity", help="Severity level")
@click.option("--status", default="planned", help="Status of the item")
@click.option("--run-command", help="Command to execute (for Command items)")
@click.option(
    "--progress", type=int, default=0, help="Progress percentage (0-100)"
)
@click.pass_context
def create(
    ctx: click.Context,
    layer: str,
    title: str,
    description: str | None,
    owner: str | None,
    severity: str | None,
    status: str,
    run_command: str | None,
    progress: int,
) -> None:
    """Create a new item."""
    database_url = ctx.obj["database_url"]
    session, _engine = get_session(database_url)

    try:
        model_class = MODEL_MAP[layer.lower()]

        # Create model instance
        kwargs = {
            "title": title,
            "status": status,
            "progress": progress,
        }

        if description:
            kwargs["description"] = description
        if owner:
            kwargs["owner"] = owner
        if severity:
            kwargs["severity"] = severity
        if run_command and model_class == Command:
            # Store the command in cmd field (can be parsed later)
            kwargs["cmd"] = run_command

        item = model_class(**kwargs)
        session.add(item)
        session.commit()
        session.refresh(item)

        console.print(
            f"✅ Created {layer.title()} '{title}' with ID {item.id}"
        )

    except Exception as e:
        console.print(f"❌ Error creating item: {e}")
        session.rollback()
    finally:
        session.close()


@cli.command()
@click.option("--layer", help="Filter by layer type")
@click.option("--owner", help="Filter by owner")
@click.option("--status", help="Filter by status")
@click.option(
    "--limit", type=int, default=20, help="Maximum number of items to show"
)
@click.pass_context
def list(
    ctx: click.Context,
    layer: str | None,
    owner: str | None,
    status: str | None,
    limit: int,
) -> None:
    """List items."""
    database_url = ctx.obj["database_url"]
    session, _engine = get_session(database_url)

    try:
        # Start with all models or filter by specific layer
        if layer:
            model_classes = [MODEL_MAP.get(layer.lower())]
            if not model_classes or not model_classes[0]:
                console.print(f"❌ Unknown layer: {layer}")
                return
        else:
            model_classes = [
                Goal,
                Concept,
                Context,
                Constraints,
                Requirements,
                AcceptanceCriteria,
                InterfaceContract,
                Phase,
                Step,
                Task,
                SubTask,
                Command,
                Label,
            ]

        all_items = []
        for model_class in model_classes:
            if not model_class:
                continue

            query = select(model_class)

            # Apply filters
            if owner:
                query = query.where(model_class.owner == owner)
            if status:
                query = query.where(model_class.status == status)

            items = session.execute(query.limit(limit)).scalars().all()
            all_items.extend(items)

        if not all_items:
            console.print("No items found.")
            return

        # Create table
        table = Table(title="ToDoWrite Items")
        table.add_column("ID", style="cyan", no_wrap=True)
        table.add_column("Type", style="magenta")
        table.add_column("Title", style="white")
        table.add_column("Owner", style="green")
        table.add_column("Status", style="yellow")
        table.add_column("Progress", justify="right", style="blue")

        for item in all_items:
            table.add_row(
                str(item.id),
                LAYER_NAMES.get(type(item), "Unknown"),
                item.title,
                item.owner or "No owner",
                item.status or "No status",
                f"{item.progress}%" if hasattr(item, "progress") else "N/A",
            )

        console.print(table)
        console.print(f"\nTotal: {len(all_items)} items")

    except Exception as e:
        console.print(f"❌ Error listing items: {e}")
    finally:
        session.close()


@cli.command()
@click.argument("item_id", type=int)
@click.pass_context
def get(ctx: click.Context, item_id: int) -> None:
    """Get details of a specific item."""
    database_url = ctx.obj["database_url"]
    session, _engine = get_session(database_url)

    try:
        # Search in all model classes
        for model_class in [
            Goal,
            Concept,
            Context,
            Constraints,
            Requirements,
            AcceptanceCriteria,
            InterfaceContract,
            Phase,
            Step,
            Task,
            SubTask,
            Command,
            Label,
        ]:
            item = session.query(model_class).filter_by(id=item_id).first()
            if item:
                # Display item details
                table = Table(
                    title=f"{LAYER_NAMES.get(type(item), 'Unknown')} Details"
                )
                table.add_column("Field", style="cyan")
                table.add_column("Value", style="white")

                table.add_row("ID", str(item.id))
                table.add_row("Type", LAYER_NAMES.get(type(item), "Unknown"))
                table.add_row("Title", item.title)

                if hasattr(item, "description") and item.description:
                    table.add_row("Description", item.description)
                if hasattr(item, "owner") and item.owner:
                    table.add_row("Owner", item.owner)
                if hasattr(item, "status") and item.status:
                    table.add_row("Status", item.status)
                if hasattr(item, "severity") and item.severity:
                    table.add_row("Severity", item.severity)
                if hasattr(item, "progress"):
                    table.add_row("Progress", f"{item.progress}%")
                if hasattr(item, "cmd") and item.cmd:
                    table.add_row("Command", item.cmd)
                if hasattr(item, "cmd_params") and item.cmd_params:
                    table.add_row("Parameters", item.cmd_params)
                if hasattr(item, "created_at") and item.created_at:
                    table.add_row("Created", str(item.created_at))
                if hasattr(item, "updated_at") and item.updated_at:
                    table.add_row("Updated", str(item.updated_at))

                console.print(table)
                return

        console.print(f"❌ Item with ID {item_id} not found.")

    except Exception as e:
        console.print(f"❌ Error getting item: {e}")
    finally:
        session.close()


@cli.command()
@click.argument("query")
@click.option("--layer", help="Search in specific layer only")
@click.pass_context
def search(ctx: click.Context, query: str, layer: str | None) -> None:
    """Search for items."""
    database_url = ctx.obj["database_url"]
    session, _engine = get_session(database_url)

    try:
        # Determine which models to search
        if layer:
            model_classes = [MODEL_MAP.get(layer.lower())]
            if not model_classes or not model_classes[0]:
                console.print(f"❌ Unknown layer: {layer}")
                return
        else:
            model_classes = [
                Goal,
                Concept,
                Context,
                Constraints,
                Requirements,
                AcceptanceCriteria,
                InterfaceContract,
                Phase,
                Step,
                Task,
                SubTask,
                Command,
                Label,
            ]

        matching_items = []
        search_lower = query.lower()

        for model_class in model_classes:
            if not model_class:
                continue

            # Search in title and description fields
            items = session.query(model_class).all()
            for item in items:
                match = False

                if (
                    (
                        hasattr(item, "title")
                        and item.title
                        and search_lower in item.title.lower()
                    )
                    or (
                        hasattr(item, "description")
                        and item.description
                        and search_lower in item.description.lower()
                    )
                    or (
                        hasattr(item, "owner")
                        and item.owner
                        and search_lower in item.owner.lower()
                    )
                ):
                    match = True

                if match:
                    matching_items.append(item)

        if not matching_items:
            console.print(f"No items found matching '{query}'.")
            return

        # Create results table
        table = Table(title=f"Search Results for '{query}'")
        table.add_column("ID", style="cyan", no_wrap=True)
        table.add_column("Type", style="magenta")
        table.add_column("Title", style="white")
        table.add_column("Owner", style="green")
        table.add_column("Status", style="yellow")

        for item in matching_items:
            table.add_row(
                str(item.id),
                LAYER_NAMES.get(type(item), "Unknown"),
                item.title or "No title",
                item.owner or "No owner",
                item.status or "No status",
            )

        console.print(table)
        console.print(f"\nFound {len(matching_items)} matching items.")

    except Exception as e:
        console.print(f"❌ Error searching items: {e}")
    finally:
        session.close()


@cli.command()
@click.pass_context
def stats(ctx: click.Context) -> None:
    """Show database statistics."""
    database_url = ctx.obj["database_url"]
    session, _engine = get_session(database_url)

    try:
        table = Table(title="Database Statistics")
        table.add_column("Layer", style="cyan")
        table.add_column("Count", justify="right", style="green")

        total_count = 0

        for model_class in [
            Goal,
            Concept,
            Context,
            Constraints,
            Requirements,
            AcceptanceCriteria,
            InterfaceContract,
            Phase,
            Step,
            Task,
            SubTask,
            Command,
            Label,
        ]:
            count = session.query(model_class).count()
            if count > 0:
                table.add_row(
                    LAYER_NAMES.get(model_class, "Unknown"), str(count)
                )
                total_count += count

        table.add_row("TOTAL", str(total_count), style="bold red")
        console.print(table)

    except Exception as e:
        console.print(f"❌ Error getting statistics: {e}")
    finally:
        session.close()


def main() -> None:
    """Main entry point for the CLI."""
    cli()


if __name__ == "__main__":
    main()
