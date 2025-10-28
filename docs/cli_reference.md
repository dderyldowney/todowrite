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

## ToDoWrite Framework Commands

The `todowrite todowrite` command group provides specialized commands for managing the 12-layer declarative planning framework.

### `todowrite todowrite validate-plan [OPTIONS]`

Validates all YAML files in the planning hierarchy against the ToDoWrite schema.

**Options:**

*   `--strict`: Enable strict validation mode with detailed error reporting.

**Usage:**

```bash
todowrite todowrite validate-plan
todowrite todowrite validate-plan --strict
```

**Output:**

```
🔍 Validating ToDoWrite planning files...
✓ configs/plans/goals/GOAL-TODOWRITE-SYSTEM-IMPLEMENTATION.yaml
✓ configs/plans/concepts/CON-DECLARATIVE-SEPARATION-ARCHITECTURE.yaml
...
✅ Plan validation completed successfully
```

### `todowrite todowrite trace-links [OPTIONS]`

Builds and analyzes the traceability matrix for all planning layers, detecting orphaned nodes and circular dependencies.

**Options:**

*   `--summary`: Show summary report only.

**Usage:**

```bash
todowrite todowrite trace-links
todowrite todowrite trace-links --summary
```

**Output:**

```
🔗 Building traceability matrix...
Loading 25 YAML files...
Building link mappings...
Identifying orphaned nodes...
Checking for circular dependencies...
Exporting traceability matrix to trace/trace.csv...
Exporting dependency graph to trace/graph.json...
✅ Traceability analysis completed
```

### `todowrite todowrite generate-commands [OPTIONS]`

Generates executable command stubs from Acceptance Criteria files.

**Options:**

*   `--force`: Regenerate existing command stubs.

**Usage:**

```bash
todowrite todowrite generate-commands
todowrite todowrite generate-commands --force
```

**Output:**

```
⚡ Generating command stubs from Acceptance Criteria...
Found 4 Acceptance Criteria files
Found 0 existing commands
✓ Generated configs/commands/CMD-MAKEFILE-TARGETS-COMPLETE.yaml
✓ Generated configs/commands/CMD-VALIDATION-TOOLS-FUNCTIONAL.yaml
✓ Generated configs/commands/CMD-CLI-COMMANDS-INTEGRATED.yaml
✓ Generated configs/commands/CMD-DOCUMENTATION-COMPLETE.yaml
✅ Command generation completed
```

### `todowrite todowrite execute-commands [COMMAND_ID] [OPTIONS]`

Executes generated command stubs to verify Acceptance Criteria.

**Arguments:**

*   `[COMMAND_ID]`: Specific command ID to execute (optional if using --all).

**Options:**

*   `--all`: Execute all available commands.
*   `--dry-run`: Show what would be executed without running commands.

**Usage:**

```bash
todowrite todowrite execute-commands CMD-MAKEFILE-TARGETS-COMPLETE
todowrite todowrite execute-commands --all
todowrite todowrite execute-commands --all --dry-run
```

**Output:**

```
🚀 Executing: CMD-MAKEFILE-TARGETS-COMPLETE
Command: make tw-all && echo 'Makefile targets verified'
✅ CMD-MAKEFILE-TARGETS-COMPLETE completed successfully
```

### `todowrite todowrite show-hierarchy [OPTIONS]`

Displays the ToDoWrite planning hierarchy in various formats.

**Options:**

*   `--layer <layer_name>`: Show only specific layer.
*   `--format <format>`: Output format (tree, flat, json). Default: tree.

**Usage:**

```bash
todowrite todowrite show-hierarchy
todowrite todowrite show-hierarchy --layer goals
todowrite todowrite show-hierarchy --format json
todowrite todowrite show-hierarchy --format flat
```

**Output (tree format):**

```
📋 ToDoWrite Planning Hierarchy
========================================

📁 Goals
  └── GOAL-TODOWRITE-SYSTEM-IMPLEMENTATION: Complete ToDoWrite System Implementation
      └─> CON-DECLARATIVE-SEPARATION-ARCHITECTURE

📁 Concepts
  └── CON-DECLARATIVE-SEPARATION-ARCHITECTURE: 11+1 Declarative Separation Architecture
      └─> CTX-PYTHON-CLI-ENVIRONMENT

📁 Contexts
  └── CTX-PYTHON-CLI-ENVIRONMENT: Python CLI Development Environment
      └─> CST-SYSTEM-CONSTRAINTS
```

### `todowrite todowrite check-soc`

Checks Separation of Concerns compliance for layers 1-11, ensuring no executable content exists in declarative layers.

**Usage:**

```bash
todowrite todowrite check-soc
```

**Output:**

```
🔒 Checking Separation of Concerns compliance...
✓ configs/plans/goals/GOAL-TODOWRITE-SYSTEM-IMPLEMENTATION.yaml
✓ configs/plans/concepts/CON-DECLARATIVE-SEPARATION-ARCHITECTURE.yaml
...
✅ All files comply with SoC requirements
```

## Makefile Integration

ToDoWrite also provides Makefile targets for automation:

### `make tw-all`

Runs the complete validation workflow: schema validation, SoC linting, traceability analysis, and command generation.

```bash
make tw-all
```

### `make tw-deps`

Installs required Python dependencies.

```bash
make tw-deps
```

### `make tw-init`

Initializes the ToDoWrite directory structure.

```bash
make tw-init
```

### `make tw-schema`

Generates the JSON schema file from the specification.

```bash
make tw-schema
```

### `make tw-lint`

Runs Separation of Concerns linting.

```bash
make tw-lint
```

### `make tw-validate`

Validates all YAML files against the schema.

```bash
make tw-validate
```

### `make tw-trace`

Builds the traceability matrix and dependency graph.

```bash
make tw-trace
```

### `make tw-prove`

Generates command stubs from Acceptance Criteria.

```bash
make tw-prove
```

### `make tw-hooks`

Installs git commit message hooks for Conventional Commits enforcement.

```bash
make tw-hooks
```

### `make tw-clean`

Removes generated files.

```bash
make tw-clean
```

### `make tw-check`

Runs strict validation with error checking.

```bash
make tw-check
```

### `make tw-test`

Runs the complete system test suite.

```bash
make tw-test
```

## Examples

### Complete Workflow Example

1. **Initialize the system:**
   ```bash
   make tw-deps
   make tw-init
   ```

2. **Create a planning hierarchy:**
   ```bash
   todowrite create Goal "Agricultural Automation" "Implement autonomous farming coordination"
   todowrite create Concept "Robot Fleet Management" "Coordinate multiple autonomous tractors" --parent GOAL-AGRICULTURAL-AUTOMATION
   ```

3. **Validate the planning structure:**
   ```bash
   todowrite todowrite validate-plan --strict
   todowrite todowrite trace-links
   ```

4. **Generate and execute verification commands:**
   ```bash
   todowrite todowrite generate-commands
   todowrite todowrite execute-commands --all
   ```

5. **Check system compliance:**
   ```bash
   todowrite todowrite check-soc
   make tw-check
   ```

### Error Handling

All commands provide clear error messages and exit codes:

- **Exit code 0**: Success
- **Exit code 1**: Validation errors or command failures

Example error output:
```
❌ Plan validation failed
ERROR: Invalid YAML in configs/plans/goals/GOAL-EXAMPLE.yaml: mapping values are not allowed here
  in "<unicode string>", line 3, column 8
```
