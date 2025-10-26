"""
This module contains the CLI for the ToDoWrite application.
"""

import uuid
from typing import Any, get_args

import click

from .app import LayerType, Node, ToDoWrite

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
def cli():
    """A CLI for the ToDoWrite application."""
    pass


@cli.command()
def init():
    """Initializes the database."""
    app: ToDoWrite = ToDoWrite()
    app.init_database()
    click.echo("Database initialized.")


@cli.command()
@click.argument("layer")
@click.argument("title")
@click.argument("description")
@click.option("--parent", default=None, help="The parent of the node.")
def create(layer: str, title: str, description: str, parent: str | None):
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
        "status": "planned",
        "links": {"parents": [parent] if parent else [], "children": []},
        "metadata": {
            "owner": "system",
            "labels": [],
        },
    }
    try:
        node: Node = app.create_node(node_data)
        click.echo(f"Node created: {node.id}")
    except Exception as e:  # type: ignore
        click.echo(f"Error creating node: {e}", err=True)
        import traceback

        click.echo(traceback.format_exc(), err=True)
        exit(1)


@cli.command()
@click.argument("node_id")
def get(node_id: str):
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
def list_nodes():
    """Lists all the nodes."""
    app: ToDoWrite = ToDoWrite()
    nodes: dict[str, list[Node]] = app.get_all_nodes()
    for layer, layer_nodes in nodes.items():
        click.echo(f"--- {layer} ---")
        for node in layer_nodes:
            click.echo(f"- {node.id}: {node.title}")


if __name__ == "__main__":
    cli()
