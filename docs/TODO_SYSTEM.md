# AFS FastAPI TODO System

This document provides a comprehensive guide to the new hierarchical TODOs system used in the AFS FastAPI project. The system is designed to be accessible and manageable by both humans and AI agents, ensuring a clear and structured development workflow.

## Three-Level Hierarchy

The TODOs system is organized into a three-level hierarchy:

1.  **Strategic Goals:** High-level objectives that define the long-term vision for the project.
2.  **Phases:** A collection of tasks that represent a single development phase to achieve a part of a strategic goal.
3.  **Tasks:** Individual, actionable steps required to complete a phase.

This structure ensures that all development work is aligned with the strategic goals of the project.

## Data Storage

All TODOs are stored in a single JSON file located at `.claude/todos.json`. This file is the single source of truth for the entire TODOs system.

## Command-Line Interface

A set of command-line scripts are provided in the `bin` directory to manage the TODOs at all three levels.

### Strategic Goal Commands

-   `strategic-list`: Lists all strategic goals.
-   `strategic-status`: Shows a detailed status of all strategic goals.
-   `strategic-status-brief`: Shows a brief summary of the strategic goals.
-   `strategic-add "<description>" [--category <category>] [--priority <priority>]`: Adds a new strategic goal.
-   `strategic-complete <goal_id>`: Marks a strategic goal as completed.
-   `strategic-delete <goal_id>`: Deletes a strategic goal.
-   `strategic-reorder <goal_id> <new_position>`: Reorders a strategic goal.
-   `strategic-pause <goal_id>`: Pauses a pending strategic goal.
-   `strategic-resume <goal_id>`: Resumes a paused strategic goal.

### Phase Commands

-   `phase-list-all`: Lists all phases.
-   `phase-status`: Shows the status of the active phase.
-   `phase-start "<name>" --strategic-id <goal_id>`: Starts a new phase aligned with a strategic goal.
-   `phase-end [--force]`: Ends the active phase.
-   `phase-activate <phase_id>`: Activates a phase.
-   `phase-pause`: Pauses the active phase.
-   `phase-resume`: Resumes a paused phase.
-   `phase-delete <phase_id>`: Deletes a phase.
-   `phase-reorder <phase_id> <new_position>`: Reorders a phase within its strategic goal.

### Task Commands

-   `task-add "<description>"`: Adds a new task to the active phase.
-   `task-complete <task_id>`: Marks a task as completed.
-   `task-delete <task_id>`: Deletes a task.
-   `task-reorder <task_id> <new_position>`: Reorders a task within its phase.
-   `task-pause <task_id>`: Pauses a pending task.
-   `task-resume <task_id>`: Resumes a paused task.

## Session Management

-   `loadsession`: Displays a summary of the current session, including the TODOs status, from `SESSION_SUMMARY.md`.
-   `savesession`: Creates a `SESSION_SUMMARY.md` file with a summary of the current TODOs state.

This new system provides a robust and flexible way to manage the development workflow of the AFS FastAPI project.
