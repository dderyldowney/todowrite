# Usage

ToDoWrite offers two primary ways to interact with the system: through its command-line interface (CLI) for quick operations and scripting, and as a Python module for deeper integration into other applications.

## CLI Usage Guide

For detailed information on using the `todowrite` command-line interface, including all available commands and their options, please refer to the [CLI Reference](../docs/cli_reference.md).

## Python Module Integration

ToDoWrite can be seamlessly integrated into your Python applications. Below are examples demonstrating how to initialize the application, create various types of nodes, retrieve, update, and delete them.

First, import the `ToDoWrite` class:

```python
from todowrite.app import ToDoWrite
```

### Initializing the Application

You can initialize `ToDoWrite` without any arguments to use the default SQLite database, or provide a `db_url` for other databases like PostgreSQL.

```python
# Uses default SQLite database (e.g., todowrite.db in the current directory)
app = ToDoWrite()

# Initialize the database (creates tables if they don't exist)
app.init_database()
```

### Creating Nodes

ToDoWrite provides convenience methods for adding different types of hierarchical nodes. Each method returns the newly created `Node` object.

```python
# Add a new Goal
goal = app.add_goal(
    title="Implement Feature X",
    description="Develop and integrate Feature X into the main product.",
    owner="Alice",
    labels=["feature", "backend"]
)
print(f"Created Goal: {goal.title} (ID: {goal.id})")

# Add a Phase linked to the Goal
phase = app.add_phase(
    parent_id=goal.id,
    title="Design Phase",
    description="Outline the architecture and technical specifications.",
    owner="Bob"
)
print(f"Created Phase: {phase.title} (ID: {phase.id})")

# Add a Task linked to the Phase
task = app.add_task(
    parent_id=phase.id,
    title="Database Schema Design",
    description="Design and implement the database schema for Feature X."
)
print(f"Created Task: {task.title} (ID: {task.id})")

# You can add other node types similarly:
# app.add_step(...)
# app.add_subtask(...)
# app.add_command(...)
# app.add_concept(...)
# app.add_context(...)
# app.add_constraint(...)
# app.add_requirement(...)
# app.add_acceptance_criteria(...)
# app.add_interface_contract(...)
```

### Retrieving Nodes

You can retrieve individual nodes by their ID or load all nodes grouped by layer.

```python
# Get a node by its ID
retrieved_node = app.get_node(goal.id)
if retrieved_node:
    print(f"Retrieved Node: {retrieved_node.title} (Layer: {retrieved_node.layer})")

# Load all nodes and display them by layer
all_nodes = app.load_todos() # Alias for get_all_nodes()
print("\nAll Nodes by Layer:")
for layer, nodes_list in all_nodes.items():
    print(f"  --- {layer} ({len(nodes_list)} items) ---")
    for n in nodes_list:
        print(f"    - {n.title} (Status: {n.status})")

# Get active items (status != 'done' and 'rejected')
active_items = app.get_active_items(all_nodes)
print("\nActive Items:")
for layer, active_node in active_items.items():
    print(f"  - {layer}: {active_node.title} (Status: {active_node.status})")
```

### Updating Nodes

Modify existing nodes using their ID and a dictionary of fields to update.

```python
# Update a node's status
updated_goal = app.update_node(goal.id, {"status": "in_progress"})
if updated_goal:
    print(f"\nUpdated Goal {updated_goal.title} status to: {updated_goal.status}")

# Update multiple fields
updated_task = app.update_node(task.id, {
    "description": "Finalize database schema and review with team.",
    "metadata": {"owner": "Charlie", "labels": ["database", "review"]}
})
if updated_task:
    print(f"\nUpdated Task {updated_task.title} description and owner.")
```

### Deleting Nodes

Remove nodes from the database using their ID. This operation also handles cascading deletions for related entities like links, labels, commands, and artifacts.

```python
# Delete a node
app.delete_node(task.id)
print(f"\nDeleted Task: {task.title}")
```
