# CLI Reference

The `todowrite` command-line interface provides a set of commands to interact with the ToDoWrite application.

## `todowrite`

The main entry point for the CLI.

### `todowrite init`

Initializes the database. This command creates all necessary tables in the configured database.

**Usage:**

```bash
todowrite init
```

**Output:**

```
Database initialized.
```

### `todowrite create <layer> <title> <description> [OPTIONS]`

Creates a new node in the ToDoWrite system.

**Arguments:**

*   `<layer>`: The layer of the new node (e.g., "Goal", "Phase", "Task").
*   `<title>`: The title of the new node.
*   `<description>`: A detailed description of the new node.

**Options:**

*   `--parent <parent_id>`: The ID of the parent node. (Optional)

**Usage:**

```bash
todowrite create Goal "My New Goal" "This is a detailed description of my new goal."
todowrite create Phase "Planning Phase" "Break down the goal into actionable steps." --parent goal-abc123def456
```

**Output:**

```
Node created: <node_id>
```

### `todowrite get <node_id>`

Retrieves and displays the details of a specific node by its ID.

**Arguments:**

*   `<node_id>`: The ID of the node to retrieve.

**Usage:**

```bash
todowrite get goal-abc123def456
```

**Output (example):**

```
ID: goal-abc123def456
Layer: Goal
Title: My New Goal
Description: This is a detailed description of my new goal.
Status: planned
Owner: system
Labels: []
Severity:
Work Type:
```

### `todowrite list`

Lists all nodes in the ToDoWrite system, grouped by their layer.

**Usage:**

```bash
todowrite list
```

**Output (example):**

```
--- Goal ---
- goal-abc123def456: My New Goal
--- Phase ---
- phase-xyz789uvw012: Planning Phase
```