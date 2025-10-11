import json
from datetime import datetime
from typing import Literal, TypedDict

# TodoWrite.md Schema Implementation
# 5-level hierarchy: Goal → Phase → Step → Task → SubTask

LevelType = Literal["Goal", "Phase", "Step", "Task", "SubTask"]
StatusType = Literal["planned", "in_progress", "blocked", "done", "rejected"]


class BaseItem(TypedDict):
    """Base schema for all TodoWrite levels according to TodoWrite.md specification."""

    id: str
    parent_id: str | None
    level: LevelType
    title: str
    description: str
    single_concern: bool
    dependencies: list[str]
    status: StatusType
    validation_log: list[str]


class SubTaskItem(BaseItem):
    """SubTask: Maps 1:1 to an executable Command."""

    command: str  # The actual executable command
    command_type: str  # e.g., "bash", "python", "api_call"
    execution_log: list[str]  # Execution history


class TaskItem(BaseItem):
    """Task: Contains SubTasks serving the Task's concern."""

    subtasks: list[SubTaskItem]


class StepItem(BaseItem):
    """Step: Contains Tasks serving the Step's concern."""

    tasks: list[TaskItem]


class PhaseItem(BaseItem):
    """Phase: Contains Steps serving the Phase's concern."""

    steps: list[StepItem]


class GoalItem(BaseItem):
    """Goal: Contains Phases (each Phase = one concern)."""

    phases: list[PhaseItem]
    category: str  # Maintain compatibility with existing system
    priority: str  # Maintain compatibility with existing system


class TodosData(TypedDict):
    goals: list[GoalItem]


# Legacy compatibility types
class LegacyTaskItem(TypedDict):
    id: str
    description: str
    status: str
    date_completed: str | None


class LegacyStepItem(TypedDict):
    id: str
    name: str
    status: str
    date_started: str
    date_completed: str | None
    tasks: list[LegacyTaskItem]
    phase_id: str


class LegacyPhaseItem(TypedDict):
    id: str
    name: str
    status: str
    date_started: str
    date_completed: str | None
    steps: list[LegacyStepItem]
    paused_at: str | None
    resumed_at: str | None
    strategic_goal_id: str


class LegacyStrategicGoal(TypedDict):
    id: str
    description: str
    category: str
    priority: str
    status: str
    date_added: str
    date_completed: str | None
    phases: list[LegacyPhaseItem]


class LegacyTodosData(TypedDict):
    strategic_goals: list[LegacyStrategicGoal]


TODOS_FILE = ".claude/todos.json"


# TodoWrite.md Validation Pipeline Implementation


def validate_hierarchy_order(item: BaseItem, expected_level: LevelType) -> list[str]:
    """V1: Require hierarchy order: Goal>Phase>Step>Task>SubTask; reject skips/misplacements."""
    errors = []

    if item["level"] != expected_level:
        errors.append(f"Hierarchy violation: Expected {expected_level}, got {item['level']}")

    # Check parent relationship
    if expected_level == "Goal" and item["parent_id"] is not None:
        errors.append("Goal must have parent_id=null")
    elif expected_level != "Goal" and item["parent_id"] is None:
        errors.append(f"{expected_level} must have a parent_id")

    return errors


def validate_single_concern(item: BaseItem) -> list[str]:
    """V2: SoC check: title+description MUST express one concern; if multiple verbs/concerns, split."""
    errors = []

    # Check for multiple action verbs in title
    action_verbs = [
        "implement",
        "create",
        "design",
        "develop",
        "build",
        "test",
        "validate",
        "configure",
        "setup",
        "analyze",
    ]
    title_lower = item["title"].lower()
    found_verbs = [verb for verb in action_verbs if verb in title_lower]

    if len(found_verbs) > 1:
        errors.append(
            f"Multiple concerns in title: contains {found_verbs}. Split into separate items."
        )

    # Check for coordination conjunctions indicating multiple concerns
    conjunctions = [" and ", " or ", " plus ", " also ", " as well as "]
    if any(conj in title_lower for conj in conjunctions):
        errors.append(
            "Title contains conjunctions suggesting multiple concerns. Split into separate items."
        )

    # Check description for multiple concerns
    desc_lower = item["description"].lower()
    desc_verbs = [verb for verb in action_verbs if verb in desc_lower]
    if len(desc_verbs) > 2:  # Allow some flexibility in description
        errors.append(f"Description may contain multiple concerns: {desc_verbs}")

    # Update single_concern flag
    if not errors:
        item["single_concern"] = True
    else:
        item["single_concern"] = False

    return errors


def validate_granularity(item: BaseItem, all_items: dict[str, BaseItem]) -> list[str]:
    """V3: Granularity check: Steps MUST only contain Tasks serving the Step's concern; Tasks MUST only contain SubTasks serving the Task's concern."""
    errors = []

    if item["level"] in ["Step", "Task"]:
        # Get children
        children = [child for child in all_items.values() if child["parent_id"] == item["id"]]

        for child in children:
            # Check if child serves parent's concern
            parent_keywords = set(
                item["title"].lower().split() + item["description"].lower().split()
            )
            child_keywords = set(
                child["title"].lower().split() + child["description"].lower().split()
            )

            # Simple keyword overlap check (can be enhanced)
            overlap = len(parent_keywords & child_keywords)
            if overlap < 2:  # Require at least 2 keyword matches
                errors.append(f"Child {child['id']} may not serve parent concern {item['id']}")

    return errors


def validate_dependencies(item: BaseItem, all_items: dict[str, BaseItem]) -> list[str]:
    """V4: Dependency check: no cycles; deps reference existing items; no cross-concern leakage."""
    errors = []

    # Check if all dependencies exist
    for dep_id in item["dependencies"]:
        if dep_id not in all_items:
            errors.append(f"Dependency {dep_id} does not exist")

    # Check for circular dependencies (simplified check)
    visited = set()

    def check_cycle(current_id: str, path: set[str]) -> bool:
        if current_id in path:
            return True
        if current_id in visited:
            return False

        visited.add(current_id)
        path.add(current_id)

        current_item = all_items.get(current_id)
        if current_item:
            for dep in current_item["dependencies"]:
                if check_cycle(dep, path.copy()):
                    return True

        path.remove(current_id)
        return False

    if check_cycle(item["id"], set()):
        errors.append(f"Circular dependency detected for {item['id']}")

    return errors


def validate_subtask_atomicity(item: SubTaskItem) -> list[str]:
    """V5: SubTask atomicity: 1 SubTask → 1 Command; no composite/multi-action commands."""
    errors: list[str] = []

    if item["level"] != "SubTask":
        return errors

    command = item.get("command", "")

    # Check for multiple commands (simplified)
    command_separators = [" && ", " || ", " ; ", " | "]
    if any(sep in command for sep in command_separators):
        errors.append("SubTask contains multiple commands. Split into separate SubTasks.")

    # Check for empty command
    if not command.strip():
        errors.append("SubTask must have a non-empty command")

    return errors


def validate_status_rules(item: BaseItem, all_items: dict[str, BaseItem]) -> list[str]:
    """V6: Status rules: parents cannot be done unless all children are done; blocked bubbles upward."""
    errors = []

    # Get children
    children = [child for child in all_items.values() if child["parent_id"] == item["id"]]

    if item["status"] == "done" and children:
        # Check if all children are done
        incomplete_children = [child for child in children if child["status"] != "done"]
        if incomplete_children:
            child_ids = [child["id"] for child in incomplete_children]
            errors.append(
                f"Parent {item['id']} cannot be done while children {child_ids} are incomplete"
            )

    # Check blocked propagation
    blocked_children = [child for child in children if child["status"] == "blocked"]
    if blocked_children and item["status"] not in ["blocked", "rejected"]:
        errors.append(f"Parent {item['id']} should be blocked due to blocked children")

    return errors


def run_validation_pipeline(
    item: BaseItem, all_items: dict[str, BaseItem], expected_level: LevelType | None = None
) -> list[str]:
    """Run the complete validation pipeline on an item."""
    all_errors = []

    # V1: Hierarchy order
    if expected_level:
        all_errors.extend(validate_hierarchy_order(item, expected_level))

    # V2: Single concern
    all_errors.extend(validate_single_concern(item))

    # V3: Granularity
    all_errors.extend(validate_granularity(item, all_items))

    # V4: Dependencies
    all_errors.extend(validate_dependencies(item, all_items))

    # V5: SubTask atomicity
    if item["level"] == "SubTask":
        all_errors.extend(validate_subtask_atomicity(item))  # type: ignore

    # V6: Status rules
    all_errors.extend(validate_status_rules(item, all_items))

    # Update validation log
    timestamp = datetime.now().isoformat()
    if all_errors:
        item["validation_log"].extend([f"{timestamp}: {error}" for error in all_errors])
    else:
        item["validation_log"].append(f"{timestamp}: Validation passed")

    return all_errors


# Data Migration Functions for TodoWrite.md Schema


def migrate_legacy_to_todowrite(legacy_data: LegacyTodosData) -> TodosData:
    """Migrate legacy 4-level data to TodoWrite.md 5-level schema."""
    migrated_goals: list[GoalItem] = []

    for legacy_goal in legacy_data["strategic_goals"]:
        # Convert legacy status to TodoWrite status
        status_map = {
            "pending": "planned",
            "active": "in_progress",
            "completed": "done",
            "paused": "blocked",
        }

        goal: GoalItem = {
            "id": legacy_goal["id"],
            "parent_id": None,
            "level": "Goal",
            "title": legacy_goal["description"][:100],  # Truncate for title
            "description": legacy_goal["description"],
            "single_concern": True,  # Will be validated
            "dependencies": [],
            "status": status_map.get(legacy_goal["status"], "planned"),
            "validation_log": [f"{datetime.now().isoformat()}: Migrated from legacy format"],
            "phases": [],
            "category": legacy_goal["category"],
            "priority": legacy_goal["priority"],
        }

        # Migrate phases
        for legacy_phase in legacy_goal["phases"]:
            phase: PhaseItem = {
                "id": legacy_phase["id"],
                "parent_id": goal["id"],
                "level": "Phase",
                "title": legacy_phase["name"][:100],
                "description": legacy_phase["name"],
                "single_concern": True,
                "dependencies": [],
                "status": status_map.get(legacy_phase["status"], "planned"),
                "validation_log": [f"{datetime.now().isoformat()}: Migrated from legacy format"],
                "steps": [],
            }

            # Migrate steps (if they exist) or create from legacy tasks
            if "steps" in legacy_phase:
                for legacy_step in legacy_phase["steps"]:
                    step: StepItem = {
                        "id": legacy_step["id"],
                        "parent_id": phase["id"],
                        "level": "Step",
                        "title": legacy_step["name"][:100],
                        "description": legacy_step["name"],
                        "single_concern": True,
                        "dependencies": [],
                        "status": status_map.get(legacy_step["status"], "planned"),
                        "validation_log": [
                            f"{datetime.now().isoformat()}: Migrated from legacy format"
                        ],
                        "tasks": [],
                    }

                    # Migrate tasks to Task/SubTask structure
                    for legacy_task in legacy_step.get("tasks", []):
                        task: TaskItem = {
                            "id": legacy_task["id"],
                            "parent_id": step["id"],
                            "level": "Task",
                            "title": legacy_task["description"][:100],
                            "description": legacy_task["description"],
                            "single_concern": True,
                            "dependencies": [],
                            "status": status_map.get(legacy_task["status"], "planned"),
                            "validation_log": [
                                f"{datetime.now().isoformat()}: Migrated from legacy format"
                            ],
                            "subtasks": [],
                        }

                        # Create a default SubTask for each Task (required for execution)
                        subtask: SubTaskItem = {
                            "id": f"subtask-{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                            "parent_id": task["id"],
                            "level": "SubTask",
                            "title": f"Execute: {legacy_task['description'][:50]}",
                            "description": f"Atomic execution of: {legacy_task['description']}",
                            "single_concern": True,
                            "dependencies": [],
                            "status": status_map.get(legacy_task["status"], "planned"),
                            "validation_log": [
                                f"{datetime.now().isoformat()}: Auto-created from legacy task"
                            ],
                            "command": f"# TODO: Define command for {legacy_task['description']}",
                            "command_type": "todo",
                            "execution_log": [],
                        }

                        task["subtasks"].append(subtask)
                        step["tasks"].append(task)

                    phase["steps"].append(step)

            # Handle legacy phases with direct tasks (no steps)
            elif "tasks" in legacy_phase:
                # Create a default step for legacy tasks
                step_id = f"step-{datetime.now().strftime('%Y%m%d_%H%M%S')}"
                step: StepItem = {
                    "id": step_id,
                    "parent_id": phase["id"],
                    "level": "Step",
                    "title": f"Implementation - {legacy_phase['name']}",
                    "description": f"Implementation tasks for {legacy_phase['name']}",
                    "single_concern": True,
                    "dependencies": [],
                    "status": status_map.get(legacy_phase["status"], "planned"),
                    "validation_log": [f"{datetime.now().isoformat()}: Created from legacy tasks"],
                    "tasks": [],
                }

                # Convert legacy tasks
                for legacy_task in legacy_phase["tasks"]:
                    task: TaskItem = {
                        "id": legacy_task["id"],
                        "parent_id": step["id"],
                        "level": "Task",
                        "title": legacy_task["description"][:100],
                        "description": legacy_task["description"],
                        "single_concern": True,
                        "dependencies": [],
                        "status": status_map.get(legacy_task["status"], "planned"),
                        "validation_log": [
                            f"{datetime.now().isoformat()}: Migrated from legacy format"
                        ],
                        "subtasks": [],
                    }

                    # Create default SubTask
                    subtask: SubTaskItem = {
                        "id": f"subtask-{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                        "parent_id": task["id"],
                        "level": "SubTask",
                        "title": f"Execute: {legacy_task['description'][:50]}",
                        "description": f"Atomic execution of: {legacy_task['description']}",
                        "single_concern": True,
                        "dependencies": [],
                        "status": status_map.get(legacy_task["status"], "planned"),
                        "validation_log": [
                            f"{datetime.now().isoformat()}: Auto-created from legacy task"
                        ],
                        "command": f"# TODO: Define command for {legacy_task['description']}",
                        "command_type": "todo",
                        "execution_log": [],
                    }

                    task["subtasks"].append(subtask)
                    step["tasks"].append(task)

                phase["steps"].append(step)

            goal["phases"].append(phase)

        migrated_goals.append(goal)

    return TodosData(goals=migrated_goals)


def create_flat_item_dict(todos: TodosData) -> dict[str, BaseItem]:
    """Create a flat dictionary of all items for validation."""
    items: dict[str, BaseItem] = {}

    for goal in todos["goals"]:
        items[goal["id"]] = goal
        for phase in goal["phases"]:
            items[phase["id"]] = phase
            for step in phase["steps"]:
                items[step["id"]] = step
                for task in step["tasks"]:
                    items[task["id"]] = task
                    for subtask in task["subtasks"]:
                        items[subtask["id"]] = subtask

    return items


def load_todos() -> TodosData:
    """Load TodoWrite.md format data, migrating from legacy format if needed."""
    try:
        with open(TODOS_FILE) as f:
            data = json.load(f)

            # Check if data is in legacy format (strategic_goals) or new format (goals)
            if "strategic_goals" in data:
                # Legacy format - migrate to TodoWrite.md format
                legacy_data = LegacyTodosData(strategic_goals=data["strategic_goals"])
                todos = migrate_legacy_to_todowrite(legacy_data)

                # Run validation pipeline on migrated data
                all_items = create_flat_item_dict(todos)
                for item in all_items.values():
                    run_validation_pipeline(item, all_items)

                # Save migrated data back to file
                save_todos(todos)
                return todos

            elif "goals" in data:
                # New TodoWrite.md format
                todos = TodosData(goals=data["goals"])

                # Run validation pipeline
                all_items = create_flat_item_dict(todos)
                for item in all_items.values():
                    run_validation_pipeline(item, all_items)

                return todos

            else:
                # Empty or invalid file
                return TodosData(goals=[])

    except FileNotFoundError:
        return TodosData(goals=[])


def save_todos(todos: TodosData) -> None:
    """Save TodoWrite.md format data with validation."""
    # Run validation pipeline before saving
    all_items = create_flat_item_dict(todos)
    validation_errors = []

    for item in all_items.values():
        errors = run_validation_pipeline(item, all_items)
        validation_errors.extend(errors)

    # Log validation results but don't block saving
    if validation_errors:
        print(f"Warning: {len(validation_errors)} validation errors found during save")

    with open(TODOS_FILE, "w") as f:
        json.dump(todos, f, indent=2)


# New TodoWrite.md API Functions


def get_goals() -> list[GoalItem]:
    """Get all goals in TodoWrite.md format."""
    todos = load_todos()
    return todos["goals"]


def add_goal(
    title: str, description: str, category: str = "general", priority: str = "medium"
) -> GoalItem:
    """Add a new goal according to TodoWrite.md schema."""
    todos = load_todos()
    new_id = f"goal-{datetime.now().strftime('%Y%m%d_%H%M%S')}"

    new_goal: GoalItem = {
        "id": new_id,
        "parent_id": None,
        "level": "Goal",
        "title": title,
        "description": description,
        "single_concern": True,
        "dependencies": [],
        "status": "planned",
        "validation_log": [f"{datetime.now().isoformat()}: Created"],
        "phases": [],
        "category": category,
        "priority": priority,
    }

    # Validate new goal
    all_items = create_flat_item_dict(todos)
    all_items[new_goal["id"]] = new_goal
    errors = run_validation_pipeline(new_goal, all_items, "Goal")

    if errors:
        print(f"Warning: Goal validation errors: {errors}")

    todos["goals"].append(new_goal)
    save_todos(todos)
    return new_goal


def add_phase(goal_id: str, title: str, description: str) -> tuple[PhaseItem | None, str | None]:
    """Add a new phase to a goal."""
    todos = load_todos()

    # Find the goal
    target_goal = None
    for goal in todos["goals"]:
        if goal["id"] == goal_id:
            target_goal = goal
            break

    if not target_goal:
        return None, f"Goal with ID '{goal_id}' not found."

    new_phase_id = f"phase-{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    new_phase: PhaseItem = {
        "id": new_phase_id,
        "parent_id": goal_id,
        "level": "Phase",
        "title": title,
        "description": description,
        "single_concern": True,
        "dependencies": [],
        "status": "planned",
        "validation_log": [f"{datetime.now().isoformat()}: Created"],
        "steps": [],
    }

    # Validate new phase
    all_items = create_flat_item_dict(todos)
    all_items[new_phase["id"]] = new_phase
    errors = run_validation_pipeline(new_phase, all_items, "Phase")

    if errors:
        print(f"Warning: Phase validation errors: {errors}")

    target_goal["phases"].append(new_phase)
    save_todos(todos)
    return new_phase, None


def add_step(phase_id: str, title: str, description: str) -> tuple[StepItem | None, str | None]:
    """Add a new step to a phase."""
    todos = load_todos()

    # Find the phase
    target_phase = None
    for goal in todos["goals"]:
        for phase in goal["phases"]:
            if phase["id"] == phase_id:
                target_phase = phase
                break

    if not target_phase:
        return None, f"Phase with ID '{phase_id}' not found."

    new_step_id = f"step-{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    new_step: StepItem = {
        "id": new_step_id,
        "parent_id": phase_id,
        "level": "Step",
        "title": title,
        "description": description,
        "single_concern": True,
        "dependencies": [],
        "status": "planned",
        "validation_log": [f"{datetime.now().isoformat()}: Created"],
        "tasks": [],
    }

    # Validate new step
    all_items = create_flat_item_dict(todos)
    all_items[new_step["id"]] = new_step
    errors = run_validation_pipeline(new_step, all_items, "Step")

    if errors:
        print(f"Warning: Step validation errors: {errors}")

    target_phase["steps"].append(new_step)
    save_todos(todos)
    return new_step, None


def add_task(step_id: str, title: str, description: str) -> tuple[TaskItem | None, str | None]:
    """Add a new task to a step."""
    todos = load_todos()

    # Find the step
    target_step = None
    for goal in todos["goals"]:
        for phase in goal["phases"]:
            for step in phase["steps"]:
                if step["id"] == step_id:
                    target_step = step
                    break

    if not target_step:
        return None, f"Step with ID '{step_id}' not found."

    new_task_id = f"task-{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    new_task: TaskItem = {
        "id": new_task_id,
        "parent_id": step_id,
        "level": "Task",
        "title": title,
        "description": description,
        "single_concern": True,
        "dependencies": [],
        "status": "planned",
        "validation_log": [f"{datetime.now().isoformat()}: Created"],
        "subtasks": [],
    }

    # Validate new task
    all_items = create_flat_item_dict(todos)
    all_items[new_task["id"]] = new_task
    errors = run_validation_pipeline(new_task, all_items, "Task")

    if errors:
        print(f"Warning: Task validation errors: {errors}")

    target_step["tasks"].append(new_task)
    save_todos(todos)
    return new_task, None


def add_subtask(
    task_id: str, title: str, description: str, command: str, command_type: str = "bash"
) -> tuple[SubTaskItem | None, str | None]:
    """Add a new subtask to a task. SubTasks are the only executable level."""
    todos = load_todos()

    # Find the task
    target_task = None
    for goal in todos["goals"]:
        for phase in goal["phases"]:
            for step in phase["steps"]:
                for task in step["tasks"]:
                    if task["id"] == task_id:
                        target_task = task
                        break

    if not target_task:
        return None, f"Task with ID '{task_id}' not found."

    new_subtask_id = f"subtask-{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    new_subtask: SubTaskItem = {
        "id": new_subtask_id,
        "parent_id": task_id,
        "level": "SubTask",
        "title": title,
        "description": description,
        "single_concern": True,
        "dependencies": [],
        "status": "planned",
        "validation_log": [f"{datetime.now().isoformat()}: Created"],
        "command": command,
        "command_type": command_type,
        "execution_log": [],
    }

    # Validate new subtask
    all_items = create_flat_item_dict(todos)
    all_items[new_subtask["id"]] = new_subtask
    errors = run_validation_pipeline(new_subtask, all_items, "SubTask")

    if errors:
        print(f"Warning: SubTask validation errors: {errors}")

    target_task["subtasks"].append(new_subtask)
    save_todos(todos)
    return new_subtask, None


def execute_subtask(subtask_id: str) -> tuple[bool, str | None]:
    """Execute a SubTask command. Only SubTasks can be executed per TodoWrite.md."""
    todos = load_todos()

    # Find the subtask
    target_subtask = None
    for goal in todos["goals"]:
        for phase in goal["phases"]:
            for step in phase["steps"]:
                for task in step["tasks"]:
                    for subtask in task["subtasks"]:
                        if subtask["id"] == subtask_id:
                            target_subtask = subtask
                            break

    if not target_subtask:
        return False, f"SubTask with ID '{subtask_id}' not found."

    if target_subtask["status"] not in ["planned", "in_progress"]:
        return False, f"SubTask status '{target_subtask['status']}' is not executable."

    # Mark as in progress
    target_subtask["status"] = "in_progress"
    target_subtask["execution_log"].append(f"{datetime.now().isoformat()}: Execution started")

    try:
        # This is where actual command execution would happen
        # For now, we'll just simulate execution
        if target_subtask["command_type"] == "todo":
            target_subtask["execution_log"].append(
                f"{datetime.now().isoformat()}: TODO command - requires manual completion"
            )
            return True, "SubTask marked for manual completion (TODO command)"
        else:
            # TODO: Implement actual command execution based on command_type
            target_subtask["execution_log"].append(
                f"{datetime.now().isoformat()}: Command execution not yet implemented"
            )
            target_subtask["status"] = "done"
            save_todos(todos)
            return True, "SubTask execution simulated successfully"

    except Exception as e:
        target_subtask["status"] = "blocked"
        target_subtask["execution_log"].append(
            f"{datetime.now().isoformat()}: Execution failed: {str(e)}"
        )
        save_todos(todos)
        return False, f"SubTask execution failed: {str(e)}"


def get_active_items() -> dict[str, BaseItem | None]:
    """Get currently active items at each level."""
    todos = load_todos()
    active_items: dict[str, BaseItem | None] = {
        "goal": None,
        "phase": None,
        "step": None,
        "task": None,
        "subtask": None,
    }

    for goal in todos["goals"]:
        if goal["status"] == "in_progress":
            active_items["goal"] = goal
            for phase in goal["phases"]:
                if phase["status"] == "in_progress":
                    active_items["phase"] = phase
                    for step in phase["steps"]:
                        if step["status"] == "in_progress":
                            active_items["step"] = step
                            for task in step["tasks"]:
                                if task["status"] == "in_progress":
                                    active_items["task"] = task
                                    for subtask in task["subtasks"]:
                                        if subtask["status"] == "in_progress":
                                            active_items["subtask"] = subtask
                                            break
                                    break
                            break
                    break
            break

    return active_items


# Legacy compatibility functions (will be deprecated)


def get_strategic_goals() -> list[GoalItem]:
    """Legacy compatibility: return goals as strategic goals."""
    return get_goals()


# TodoWrite Integration Functions


def save_todowrite_tasks_to_new_schema(
    todowrite_tasks: list[dict], target_level: str = "auto", context: str | None = None
) -> tuple[str, str | None]:
    """Save TodoWrite tasks using the new TodoWrite.md schema."""
    if not todowrite_tasks:
        return "No tasks to save", None

    active_items = get_active_items()

    # Convert TodoWrite tasks to proper TodoWrite.md schema items
    if target_level == "auto":
        # Use active hierarchy to determine target level
        if active_items["task"]:
            # Add as SubTasks to active task
            for todo_item in todowrite_tasks:
                title = todo_item.get("content", "")[:100]
                description = todo_item.get("content", "")
                status_map = {
                    "completed": "done",
                    "pending": "planned",
                    "in_progress": "in_progress",
                }
                status = status_map.get(todo_item.get("status", "pending"), "planned")

                subtask, error = add_subtask(
                    active_items["task"]["id"], title, description, f"# TODO: {description}", "todo"
                )
                if subtask:
                    subtask["status"] = status

            return f"Added {len(todowrite_tasks)} SubTasks to active task", None

        elif active_items["step"]:
            # Add as Tasks to active step
            for todo_item in todowrite_tasks:
                title = todo_item.get("content", "")[:100]
                description = todo_item.get("content", "")
                status_map = {
                    "completed": "done",
                    "pending": "planned",
                    "in_progress": "in_progress",
                }
                status = status_map.get(todo_item.get("status", "pending"), "planned")

                task, error = add_task(active_items["step"]["id"], title, description)
                if task:
                    task["status"] = status
                    # Each Task needs at least one SubTask for execution
                    add_subtask(
                        task["id"],
                        f"Execute: {title}",
                        f"Atomic execution of: {description}",
                        f"# TODO: {description}",
                        "todo",
                    )

            return f"Added {len(todowrite_tasks)} Tasks to active step", None

        elif active_items["phase"]:
            # Create new step for tasks
            step_title = context or "TodoWrite Tasks"
            step, error = add_step(
                active_items["phase"]["id"], step_title, f"Implementation step: {step_title}"
            )
            if error:
                return "", error

            # Add tasks to new step
            for todo_item in todowrite_tasks:
                title = todo_item.get("content", "")[:100]
                description = todo_item.get("content", "")
                status_map = {
                    "completed": "done",
                    "pending": "planned",
                    "in_progress": "in_progress",
                }
                status = status_map.get(todo_item.get("status", "pending"), "planned")

                task, error = add_task(step["id"], title, description)
                if task:
                    task["status"] = status
                    add_subtask(
                        task["id"],
                        f"Execute: {title}",
                        f"Atomic execution of: {description}",
                        f"# TODO: {description}",
                        "todo",
                    )

            return f"Created step '{step_title}' with {len(todowrite_tasks)} tasks", None

        else:
            return "", "No active items found. Please create a goal/phase/step first."

    return "", f"Target level '{target_level}' not implemented yet"


def validate_all_items() -> dict[str, list[str]]:
    """Run validation pipeline on all items and return results."""
    todos = load_todos()
    all_items = create_flat_item_dict(todos)
    validation_results = {}

    for item_id, item in all_items.items():
        errors = run_validation_pipeline(item, all_items)
        if errors:
            validation_results[item_id] = errors

    return validation_results


def get_execution_ready_subtasks() -> list[SubTaskItem]:
    """Get all SubTasks that are ready for execution."""
    todos = load_todos()
    ready_subtasks = []

    for goal in todos["goals"]:
        for phase in goal["phases"]:
            for step in phase["steps"]:
                for task in step["tasks"]:
                    for subtask in task["subtasks"]:
                        if (
                            subtask["status"] in ["planned", "in_progress"]
                            and subtask["command_type"] != "todo"
                        ):
                            ready_subtasks.append(subtask)

    return ready_subtasks


# Legacy functions for backward compatibility (redirected to new schema)


def add_strategic_goal(description: str, category: str, priority: str) -> GoalItem:
    """Legacy compatibility: add goal using new schema."""
    return add_goal(description, description, category, priority)


def complete_strategic_goal(goal_id: str) -> bool:
    """Legacy compatibility: complete goal using new schema."""
    todos = load_todos()
    for goal in todos["goals"]:
        if goal["id"] == goal_id:
            goal["status"] = "done"
            save_todos(todos)
            return True
    return False


def reorder_strategic_goals(goal_id: str, new_position: int) -> bool:
    """Legacy compatibility: reorder goals using new schema."""
    todos = load_todos()
    goals: list[GoalItem] = todos["goals"]

    goal_to_move = None
    for i, goal in enumerate(goals):
        if goal["id"] == goal_id:
            goal_to_move = goals.pop(i)
            break

    if not goal_to_move:
        return False

    if new_position < 1:
        new_position = 1
    if new_position > len(goals) + 1:
        new_position = len(goals) + 1

    goals.insert(new_position - 1, goal_to_move)
    todos["goals"] = goals
    save_todos(todos)
    return True


def get_all_phases() -> list[PhaseItem]:
    """Legacy compatibility: get all phases using new schema."""
    todos = load_todos()
    all_phases: list[PhaseItem] = []
    for goal in todos["goals"]:
        for phase in goal["phases"]:
            # Note: new schema uses parent_id instead of strategic_goal_id
            all_phases.append(phase)
    return all_phases


def get_active_phase() -> PhaseItem | None:
    """Legacy compatibility: get active phase using new schema."""
    todos = load_todos()
    for goal in todos["goals"]:
        for phase in goal["phases"]:
            if phase.get("status") == "in_progress":
                return phase
    return None


def start_phase(name: str, strategic_goal_id: str) -> tuple[PhaseItem | None, str | None]:
    """Legacy compatibility: start phase using new schema."""
    # Redirect to new schema function
    return add_phase(strategic_goal_id, name, f"Implementation phase: {name}")


def add_step_to_active_phase(name: str) -> tuple[StepItem | None, str | None]:
    """Add a new step to the active phase."""
    todos = load_todos()
    active_phase: PhaseItem | None = None

    for goal in todos["goals"]:
        for phase in goal["phases"]:
            if phase.get("status") == "active":
                active_phase = phase
                break
        if active_phase:
            break

    if not active_phase:
        return None, "No active phase found."

    new_step_id = f"step-{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    new_step: StepItem = {
        "id": new_step_id,
        "name": name,
        "status": "pending",
        "date_started": datetime.now().isoformat(timespec="seconds") + "Z",
        "date_completed": None,
        "tasks": [],
        "phase_id": active_phase["id"],
    }

    if "steps" not in active_phase:
        active_phase["steps"] = []

    active_phase["steps"].append(new_step)
    save_todos(todos)
    return new_step, None


def get_active_step() -> StepItem | None:
    """Get the currently active step."""
    todos = load_todos()
    for goal in todos["goals"]:
        for phase in goal["phases"]:
            if phase.get("status") == "active":
                for step in phase.get("steps", []):
                    if step.get("status") == "active":
                        step["phase_id"] = phase["id"]
                        return step
    return None


def activate_step(step_id: str) -> tuple[StepItem | None, str | None]:
    """Activate a specific step (deactivates others)."""
    todos = load_todos()

    step_to_activate: StepItem | None = None
    current_active_step: StepItem | None = None

    for goal in todos["goals"]:
        for phase in goal["phases"]:
            for step in phase.get("steps", []):
                if step.get("id") == step_id:
                    step_to_activate = step
                if step.get("status") == "active":
                    current_active_step = step

    if not step_to_activate:
        return None, f"Step with ID '{step_id}' not found."

    if current_active_step and current_active_step["id"] == step_id:
        return step_to_activate, "Step is already active."

    # Deactivate current active step
    if current_active_step:
        current_active_step["status"] = "pending"

    # Activate the new step
    step_to_activate["status"] = "active"

    save_todos(todos)
    return step_to_activate, None


def complete_step(step_id: str) -> tuple[StepItem | None, str | None]:
    """Complete a step and mark all its tasks as completed."""
    todos = load_todos()

    for goal in todos["goals"]:
        for phase in goal["phases"]:
            for step in phase.get("steps", []):
                if step["id"] == step_id:
                    step["status"] = "completed"
                    step["date_completed"] = datetime.now().isoformat(timespec="seconds") + "Z"

                    # Mark all tasks in the step as completed
                    for task in step.get("tasks", []):
                        if task.get("status") != "completed":
                            task["status"] = "completed"
                            task["date_completed"] = (
                                datetime.now().isoformat(timespec="seconds") + "Z"
                            )

                    save_todos(todos)
                    return step, None

    return None, f"Step with ID '{step_id}' not found."


def end_phase(force: bool = False) -> tuple[PhaseItem | None, str | None]:
    todos = load_todos()
    active_phase: PhaseItem | None = None
    active_goal: GoalItem | None = None

    for goal in todos["goals"]:
        for phase in goal["phases"]:
            if phase.get("status") == "active":
                active_phase = phase
                active_goal = goal
                break
        if active_phase:
            break

    if not active_phase:
        return None, "No active phase found."

    # Count pending tasks across all steps
    pending_tasks = []
    for step in active_phase.get("steps", []):
        for task in step.get("tasks", []):
            if task.get("status") == "pending":
                pending_tasks.append(task)

    if pending_tasks and not force:
        return (
            None,
            f"Phase has {len(pending_tasks)} pending tasks across {len(active_phase.get('steps', []))} steps. Use --force to end anyway.",
        )

    # Complete all steps and tasks
    for step in active_phase.get("steps", []):
        if step.get("status") != "completed":
            step["status"] = "completed"
            step["date_completed"] = datetime.now().isoformat(timespec="seconds") + "Z"

        for task in step.get("tasks", []):
            if task.get("status") != "completed":
                task["status"] = "completed"
                task["date_completed"] = datetime.now().isoformat(timespec="seconds") + "Z"

    active_phase["status"] = "completed"
    active_phase["date_completed"] = datetime.now().isoformat(timespec="seconds") + "Z"

    # Only complete the strategic goal if the phase is completed without forcing
    if not pending_tasks and active_goal:
        active_goal["status"] = "completed"
        active_goal["date_completed"] = datetime.now().isoformat(timespec="seconds") + "Z"

    save_todos(todos)
    return active_phase, None


def add_task_to_active_step(description: str) -> tuple[TaskItem | None, str | None]:
    """Add a new task to the currently active step."""
    todos = load_todos()
    active_step = get_active_step()

    if not active_step:
        return None, "No active step found. Use add_task_to_active_phase to create a default step."

    new_task_id = f"task-{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    new_task: TaskItem = {
        "id": new_task_id,
        "description": description,
        "status": "pending",
        "date_completed": None,
    }

    # Find the step in the data structure and add the task
    for goal in todos["goals"]:
        for phase in goal["phases"]:
            for step in phase.get("steps", []):
                if step["id"] == active_step["id"]:
                    step["tasks"].append(new_task)
                    save_todos(todos)
                    return new_task, None

    return None, "Failed to find active step in data structure."


def add_task_to_active_phase(description: str) -> tuple[TaskItem | None, str | None]:
    """Add a new task to the active phase. Creates a default step if none exists or no step is active."""
    todos = load_todos()
    active_phase: PhaseItem | None = None

    for goal in todos["goals"]:
        for phase in goal["phases"]:
            if phase.get("status") == "active":
                active_phase = phase
                break
        if active_phase:
            break

    if not active_phase:
        return None, "No active phase found."

    # Try to add to active step first
    active_step = get_active_step()
    if active_step:
        return add_task_to_active_step(description)

    # No active step, find first pending step or create default step
    pending_step = None
    for step in active_phase.get("steps", []):
        if step.get("status") == "pending":
            pending_step = step
            break

    if not pending_step:
        # Create a default step for the task
        default_step_name = f"Tasks - {active_phase['name']}"
        new_step, error = add_step_to_active_phase(default_step_name)
        if error or not new_step:
            return None, f"Failed to create default step: {error}"
        pending_step = new_step

    # Activate the step and add the task
    activate_step(pending_step["id"])

    new_task_id = f"task-{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    new_task: TaskItem = {
        "id": new_task_id,
        "description": description,
        "status": "pending",
        "date_completed": None,
    }

    pending_step["tasks"].append(new_task)
    save_todos(todos)
    return new_task, None


def complete_task_in_active_phase(search_term: str) -> tuple[TaskItem | None, str | None]:
    """Complete a task in the active phase by searching across all steps."""
    todos = load_todos()
    active_phase: PhaseItem | None = None

    for goal in todos["goals"]:
        for phase in goal["phases"]:
            if phase.get("status") == "active":
                active_phase = phase
                break
        if active_phase:
            break

    if not active_phase:
        return None, "No active phase found."

    # Search for task across all steps in the active phase
    matched_task: TaskItem | None = None
    matched_step: StepItem | None = None

    for step in active_phase.get("steps", []):
        for task in step.get("tasks", []):
            if task["id"] == search_term or search_term.lower() in task["description"].lower():
                matched_task = task
                matched_step = step
                break
        if matched_task:
            break

    if not matched_task:
        return None, f"Task not found matching '{search_term}' in any step of active phase"

    if matched_task["status"] == "completed":
        return None, f"Task already completed: {matched_task['description']}"

    matched_task["status"] = "completed"
    matched_task["date_completed"] = datetime.now().isoformat(timespec="seconds") + "Z"

    # Check if this was the last pending task in the step
    if matched_step:
        remaining_pending = [
            t for t in matched_step.get("tasks", []) if t.get("status") == "pending"
        ]
        if not remaining_pending:
            matched_step["status"] = "completed"
            matched_step["date_completed"] = datetime.now().isoformat(timespec="seconds") + "Z"

    save_todos(todos)
    return matched_task, None


def save_todowrite_to_step(
    step_id: str, todowrite_tasks: list[dict]
) -> tuple[list[TaskItem], str | None]:
    """Save TodoWrite tasks directly to a specific step."""
    todos = load_todos()

    target_step: StepItem | None = None
    for goal in todos["goals"]:
        for phase in goal["phases"]:
            for step in phase.get("steps", []):
                if step["id"] == step_id:
                    target_step = step
                    break

    if not target_step:
        return [], f"Step with ID '{step_id}' not found."

    created_tasks: list[TaskItem] = []
    for todo_item in todowrite_tasks:
        new_task_id = f"task-{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        new_task: TaskItem = {
            "id": new_task_id,
            "description": todo_item.get("content", "Imported from TodoWrite"),
            "status": "completed" if todo_item.get("status") == "completed" else "pending",
            "date_completed": (
                datetime.now().isoformat(timespec="seconds") + "Z"
                if todo_item.get("status") == "completed"
                else None
            ),
        }
        target_step["tasks"].append(new_task)
        created_tasks.append(new_task)

    save_todos(todos)
    return created_tasks, None


def save_todowrite_to_phase(
    phase_id: str, todowrite_tasks: list[dict], step_name: str | None = None
) -> tuple[StepItem | None, str | None]:
    """Save TodoWrite tasks as a new step in a specific phase."""
    todos = load_todos()

    target_phase: PhaseItem | None = None
    for goal in todos["goals"]:
        for phase in goal["phases"]:
            if phase["id"] == phase_id:
                target_phase = phase
                break

    if not target_phase:
        return None, f"Phase with ID '{phase_id}' not found."

    # Create new step
    step_name = step_name or f"TodoWrite Import - {datetime.now().strftime('%Y-%m-%d %H:%M')}"
    new_step_id = f"step-{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    new_step: StepItem = {
        "id": new_step_id,
        "name": step_name,
        "status": "pending",
        "date_started": datetime.now().isoformat(timespec="seconds") + "Z",
        "date_completed": None,
        "tasks": [],
        "phase_id": target_phase["id"],
    }

    # Add tasks to new step
    for todo_item in todowrite_tasks:
        new_task_id = f"task-{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        new_task: TaskItem = {
            "id": new_task_id,
            "description": todo_item.get("content", "Imported from TodoWrite"),
            "status": "completed" if todo_item.get("status") == "completed" else "pending",
            "date_completed": (
                datetime.now().isoformat(timespec="seconds") + "Z"
                if todo_item.get("status") == "completed"
                else None
            ),
        }
        new_step["tasks"].append(new_task)

    target_phase["steps"].append(new_step)
    save_todos(todos)
    return new_step, None


def auto_save_todowrite(
    todowrite_tasks: list[dict], agricultural_context: str | None = None
) -> tuple[str, str | None]:
    """Automatically save TodoWrite tasks to the most appropriate level with minimal steps."""
    if not todowrite_tasks:
        return "No tasks to save", None

    todos = load_todos()

    # Strategy 1: If there's an active step, save to it
    active_step = get_active_step()
    if active_step:
        created_tasks, error = save_todowrite_to_step(active_step["id"], todowrite_tasks)
        if not error:
            return f"Saved {len(created_tasks)} tasks to active step: {active_step['name']}", None

    # Strategy 2: If there's an active phase, create new step
    active_phase = get_active_phase()
    if active_phase:
        step_name = "TodoWrite Tasks"
        if agricultural_context:
            step_name = f"{agricultural_context} - TodoWrite Tasks"

        new_step, error = save_todowrite_to_phase(active_phase["id"], todowrite_tasks, step_name)
        if not error and new_step:
            return (
                f"Created new step '{new_step['name']}' with {len(todowrite_tasks)} tasks in active phase",
                None,
            )

    # Strategy 3: Find first pending strategic goal and create phase+step
    for goal in todos["goals"]:
        if goal.get("status") == "pending":
            # Create new phase
            phase_name = "TodoWrite Import Phase"
            if agricultural_context:
                phase_name = f"{agricultural_context} Phase"

            new_phase, error = start_phase(phase_name, goal["id"])
            if error or not new_phase:
                continue

            # Create step in new phase
            step_name = "Implementation Tasks"
            if agricultural_context:
                step_name = f"{agricultural_context} Tasks"

            new_step, error = save_todowrite_to_phase(new_phase["id"], todowrite_tasks, step_name)
            if not error and new_step:
                return (
                    f"Created new phase '{new_phase['name']}' and step '{new_step['name']}' with {len(todowrite_tasks)} tasks",
                    None,
                )

    return (
        "",
        "No suitable location found to save TodoWrite tasks. Please create a strategic goal first.",
    )


def activate_phase(phase_id: str) -> tuple[PhaseItem | None, str | None]:
    todos = load_todos()

    # Find the phase to activate and the current active phase
    phase_to_activate: PhaseItem | None = None
    current_active_phase: PhaseItem | None = None
    for goal in todos["goals"]:
        for phase in goal["phases"]:
            if phase.get("id") == phase_id:
                phase_to_activate = phase
            if phase.get("status") == "active":
                current_active_phase = phase

    if not phase_to_activate:
        return None, f"Phase with ID ''{phase_id}'' not found."

    if current_active_phase and current_active_phase["id"] == phase_id:
        return phase_to_activate, "Phase is already active."

    # Deactivate current active phase
    if current_active_phase:
        current_active_phase["status"] = "paused"

    # Activate the new phase
    phase_to_activate["status"] = "active"

    save_todos(todos)
    return phase_to_activate, None


def pause_active_phase() -> tuple[PhaseItem | None, str | None]:
    todos = load_todos()
    active_phase: PhaseItem | None = None

    for goal in todos["goals"]:
        for phase in goal["phases"]:
            if phase.get("status") == "active":
                active_phase = phase
                break
        if active_phase:
            break

    if not active_phase:
        return None, "No active phase found to pause."

    active_phase["status"] = "paused"
    active_phase["paused_at"] = datetime.now().isoformat(timespec="seconds") + "Z"

    save_todos(todos)
    return active_phase, None


def resume_paused_phase() -> tuple[PhaseItem | None, str | None]:
    todos = load_todos()
    paused_phase: PhaseItem | None = None

    for goal in todos["goals"]:
        for phase in goal["phases"]:
            if phase.get("status") == "paused":
                paused_phase = phase
                break
        if paused_phase:
            break

    if not paused_phase:
        return None, "No paused phase found to resume."

    # Check for existing active phase
    for goal in todos["goals"]:
        for phase in goal["phases"]:
            if phase.get("status") == "active":
                return (
                    None,
                    f"Another phase is already active: {phase.get('name', 'Unknown Phase')}",
                )

    paused_phase["status"] = "active"
    paused_phase["resumed_at"] = datetime.now().isoformat(timespec="seconds") + "Z"

    save_todos(todos)
    return paused_phase, None


def delete_strategic_goal(goal_id: str) -> tuple[bool, str | None]:
    todos = load_todos()
    goals: list[GoalItem] = todos["goals"]

    goal_found = False
    for i, goal in enumerate(goals):
        if goal["id"] == goal_id:
            goals.pop(i)
            goal_found = True
            break

    if not goal_found:
        return False, f"Strategic goal with ID ''{goal_id}'' not found."

    todos["goals"] = goals
    save_todos(todos)
    return True, None


def delete_phase(phase_id: str) -> tuple[bool, str | None]:
    todos = load_todos()

    phase_found = False
    for goal in todos["goals"]:
        phases: list[PhaseItem] = goal["phases"]
        for i, phase in enumerate(phases):
            if phase["id"] == phase_id:
                phases.pop(i)
                phase_found = True
                break
        if phase_found:
            break

    if not phase_found:
        return False, f"Phase with ID ''{phase_id}'' not found."

    save_todos(todos)
    return True, None


def delete_task(task_id: str) -> tuple[bool, str | None]:
    """Delete a task from any step in the hierarchy."""
    todos = load_todos()

    task_found = False
    for goal in todos["goals"]:
        for phase in goal["phases"]:
            for step in phase.get("steps", []):
                tasks: list[TaskItem] = step["tasks"]
                for i, task in enumerate(tasks):
                    if task["id"] == task_id:
                        tasks.pop(i)
                        task_found = True
                        break
                if task_found:
                    break
            if task_found:
                break
        if task_found:
            break

    if not task_found:
        return False, f"Task with ID '{task_id}' not found."

    save_todos(todos)
    return True, None


def reorder_phases(phase_id: str, new_position: int) -> tuple[bool, str | None]:
    todos = load_todos()

    phase_to_move: PhaseItem | None = None
    goal_of_phase: GoalItem | None = None
    for goal in todos["goals"]:
        for i, phase in enumerate(goal["phases"]):
            if phase["id"] == phase_id:
                phase_to_move = goal["phases"].pop(i)
                goal_of_phase = goal
                break
        if phase_to_move:
            break

    if not phase_to_move:
        return False, f"Phase with ID ''{phase_id}'' not found."

    if new_position < 1:
        new_position = 1
    if goal_of_phase and new_position > len(goal_of_phase["phases"]) + 1:
        new_position = len(goal_of_phase["phases"]) + 1

    if goal_of_phase:
        goal_of_phase["phases"].insert(new_position - 1, phase_to_move)

    save_todos(todos)
    return True, None


def reorder_tasks(task_id: str, new_position: int) -> tuple[bool, str | None]:
    """Reorder a task within its step."""
    todos = load_todos()

    task_to_move: TaskItem | None = None
    step_of_task: StepItem | None = None
    for goal in todos["goals"]:
        for phase in goal["phases"]:
            for step in phase.get("steps", []):
                tasks: list[TaskItem] = step["tasks"]
                for i, task in enumerate(tasks):
                    if task["id"] == task_id:
                        task_to_move = step["tasks"].pop(i)
                        step_of_task = step
                        break
                if task_to_move:
                    break
            if task_to_move:
                break
        if task_to_move:
            break

    if not task_to_move:
        return False, f"Task with ID '{task_id}' not found."

    if not step_of_task:
        return False, "Internal error: Step of task not found."

    if new_position < 1:
        new_position = 1
    if new_position > len(step_of_task["tasks"]) + 1:
        new_position = len(step_of_task["tasks"]) + 1

    step_of_task["tasks"].insert(new_position - 1, task_to_move)

    save_todos(todos)
    return True, None


def pause_strategic_goal(goal_id: str) -> tuple[bool | None, str | None]:
    todos = load_todos()

    goal_found = False
    for goal in todos["goals"]:
        if goal["id"] == goal_id:
            if goal["status"] == "pending":
                goal["status"] = "paused"
                goal_found = True
                break
            else:
                return None, f"Goal is not pending. Current status: {goal['status']}"

    if not goal_found:
        return None, f"Strategic goal with ID ''{goal_id}'' not found."

    save_todos(todos)
    return True, None


def resume_strategic_goal(goal_id: str) -> tuple[bool | None, str | None]:
    todos = load_todos()

    goal_found = False
    for goal in todos["goals"]:
        if goal["id"] == goal_id:
            if goal["status"] == "paused":
                goal["status"] = "pending"
                goal_found = True
                break
            else:
                return None, f"Goal is not paused. Current status: {goal['status']}"

    if not goal_found:
        return None, f"Strategic goal with ID ''{goal_id}'' not found."

    save_todos(todos)
    return True, None


def update_parent_statuses() -> None:
    """Update status of phases and strategic goals based on child status."""
    todos = load_todos()

    strategic_goals: list[GoalItem] = todos["goals"]
    for goal in strategic_goals:
        has_paused_phase = False
        phases: list[PhaseItem] = goal["phases"]
        for phase in phases:
            has_paused_step = False
            for step in phase.get("steps", []):
                tasks: list[TaskItem] = step["tasks"]
                has_paused_task = any(t.get("status") == "paused" for t in tasks)
                if has_paused_task:
                    if step.get("status") == "active":
                        step["status"] = "partially-paused"
                    has_paused_step = True
                else:
                    if step.get("status") == "partially-paused":
                        step["status"] = "active"

            if has_paused_step:
                if phase.get("status") == "active":
                    phase["status"] = "partially-paused"
                has_paused_phase = True
            else:
                if phase.get("status") == "partially-paused":
                    phase["status"] = "active"

        if has_paused_phase:
            if goal.get("status") == "pending":
                goal["status"] = "partially-paused"
        else:
            if goal.get("status") == "partially-paused":
                goal["status"] = "pending"
    save_todos(todos)


def pause_task(task_id: str) -> tuple[bool | None, str | None]:
    """Pause a specific task within its step."""
    todos = load_todos()

    task_found = False
    strategic_goals: list[GoalItem] = todos["goals"]
    for goal in strategic_goals:
        phases: list[PhaseItem] = goal["phases"]
        for phase in phases:
            for step in phase.get("steps", []):
                tasks: list[TaskItem] = step["tasks"]
                for task in tasks:
                    if task["id"] == task_id:
                        if task.get("status") == "pending":
                            task["status"] = "paused"
                            task_found = True
                            break
                        else:
                            return (
                                None,
                                f"Task is not pending. Current status: {task.get('status')}",
                            )
                if task_found:
                    break
            if task_found:
                break
        if task_found:
            break

    if not task_found:
        return None, f"Task with ID '{task_id}' not found."

    save_todos(todos)
    update_parent_statuses()
    return True, None


def resume_task(task_id: str) -> tuple[bool | None, str | None]:
    """Resume a paused task within its step."""
    todos = load_todos()

    task_found = False
    strategic_goals: list[GoalItem] = todos["goals"]
    for goal in strategic_goals:
        phases: list[PhaseItem] = goal["phases"]
        for phase in phases:
            for step in phase.get("steps", []):
                tasks: list[TaskItem] = step["tasks"]
                for task in tasks:
                    if task["id"] == task_id:
                        if task.get("status") == "paused":
                            task["status"] = "pending"
                            task_found = True
                            break
                        else:
                            return None, f"Task is not paused. Current status: {task.get('status')}"
                if task_found:
                    break
            if task_found:
                break
        if task_found:
            break

    if not task_found:
        return None, f"Task with ID '{task_id}' not found."

    save_todos(todos)
    update_parent_statuses()
    return True, None
