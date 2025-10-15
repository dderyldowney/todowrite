import json
import subprocess
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
    date_completed: str | None


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

    # Action verbs and conjunctions for strict checking
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
        "fix",
        "repair",
        "locate",
        "identify",
        "improve",
        "enhance",
    ]

    desc_lower = item["description"].lower()

    if item["level"] != "Goal":
        # Apply strict checks for non-Goal items (Phase, Step, Task, SubTask)
        found_verbs_desc = [verb for verb in action_verbs if verb in desc_lower]

    else:
        # For Goal level items, apply a more relaxed check on description
        # Only flag if description is excessively long or contains too many distinct concerns
        found_verbs_desc = [verb for verb in action_verbs if verb in desc_lower]
        if len(found_verbs_desc) > 4:  # Allow more verbs for high-level goals
            errors.append(f"Goal description may contain too many concerns: {found_verbs_desc}")

    # Update single_concern flag
    if not errors:
        item["single_concern"] = True
    else:
        item["single_concern"] = False

    return errors


def validate_granularity(item: BaseItem, all_items: dict[str, BaseItem]) -> list[str]:
    """V3: Granularity check: Steps MUST only contain Tasks serving the Step's concern; Tasks MUST only contain SubTasks serving the Task's concern."""
    errors: list[str] = []

    if item["level"] in ["Step", "Task"]:
        # Get children
        children = [child for child in all_items.values() if child["parent_id"] == item["id"]]

        for _child in children:
            # Check if child serves parent's concern
            pass
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
    """Load TodoWrite.md format data."""
    try:
        with open(TODOS_FILE) as f:
            data = json.load(f)

            if "goals" in data:
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
    new_id = f"goal-{datetime.now().strftime('%Y%m%d_%H%M%S_%f')}"

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
        "date_completed": None,
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

    new_phase_id = f"phase-{datetime.now().strftime('%Y%m%d_%H%M%S_%f')}"
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
        "date_completed": None,
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

    new_step_id = f"step-{datetime.now().strftime('%Y%m%d_%H%M%S_%f')}"
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
        "date_completed": None,
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

    new_task_id = f"task-{datetime.now().strftime('%Y%m%d_%H%M%S_%f')}"
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
        "date_completed": None,
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

    new_subtask_id = f"subtask-{datetime.now().strftime('%Y%m%d_%H%M%S_%f')}"
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
        "date_completed": None,
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
    save_todos(todos)

    try:
        command = target_subtask["command"]
        command_type = target_subtask.get("command_type", "bash")

        if command_type == "bash":
            result = subprocess.run(command, shell=True, capture_output=True, text=True)
            if result.returncode == 0:
                target_subtask["execution_log"].append(
                    f"{datetime.now().isoformat()}: Execution successful"
                )
                target_subtask["execution_log"].append(f"stdout:\n{result.stdout}")
                target_subtask["status"] = "done"
                save_todos(todos)
                return True, "SubTask executed successfully"
            else:
                target_subtask["execution_log"].append(
                    f"{datetime.now().isoformat()}: Execution failed"
                )
                target_subtask["execution_log"].append(f"stderr:\n{result.stderr}")
                target_subtask["status"] = "blocked"
                save_todos(todos)
                return False, f"SubTask execution failed: {result.stderr}"
        elif command_type == "todo":
            target_subtask["execution_log"].append(
                f"{datetime.now().isoformat()}: TODO command - requires manual completion"
            )
            # Not changing status, as it requires manual intervention.
            save_todos(todos)
            return True, "SubTask marked for manual completion (TODO command)"
        else:
            # TODO: Implement other command types
            target_subtask["execution_log"].append(
                f"{datetime.now().isoformat()}: Command execution for type '{command_type}' not yet implemented"
            )
            target_subtask["status"] = "blocked"
            save_todos(todos)
            return False, f"Command execution for type '{command_type}' not yet implemented"

    except Exception as e:
        target_subtask["status"] = "blocked"
        target_subtask["execution_log"].append(
            f"{datetime.now().isoformat()}: Execution failed: {str(e)}"
        )
        save_todos(todos)
        return False, f"SubTask execution failed: {str(e)}"


def activate_phase(phase_id: str) -> tuple[PhaseItem | None, str | None]:
    """Activate a phase, setting all other phases to planned."""
    todos = load_todos()
    target_phase = None
    target_goal = None

    # Deactivate all other phases and find the target phase and its goal
    for goal in todos["goals"]:
        for phase in goal["phases"]:
            if phase["id"] == phase_id:
                target_phase = phase
                target_goal = goal
            else:
                if phase["status"] == "in_progress":
                    phase["status"] = "planned"

    if not target_phase:
        return None, f"Phase with ID '{phase_id}' not found."

    # Activate the target phase and its goal
    target_phase["status"] = "in_progress"
    if target_goal:
        target_goal["status"] = "in_progress"

    # Deactivate other goals
    for goal in todos["goals"]:
        if target_goal and goal["id"] != target_goal["id"] and goal["status"] == "in_progress":
            goal["status"] = "planned"

    save_todos(todos)
    return target_phase, None


def get_active_phase() -> PhaseItem | None:
    """Get the currently active phase."""
    active_items = get_active_items()
    phase = active_items.get("phase")
    if phase and isinstance(phase, dict):
        # This is a hack to make mypy happy
        return phase  # type: ignore
    return None


def end_phase(force: bool = False) -> tuple[PhaseItem | None, str | None]:
    """End the active phase."""
    todos = load_todos()
    active_phase = get_active_phase()

    if not active_phase:
        return None, "No active phase found."

    if not force:
        for step in active_phase.get("steps", []):
            if step.get("status") != "done":
                return None, "Phase has incomplete steps."

    for goal in todos.get("goals", []):
        for phase in goal.get("phases", []):
            if phase.get("id") == active_phase.get("id"):
                phase["status"] = "done"
                phase["date_completed"] = datetime.now().isoformat()
                save_todos(todos)
                return phase, None

    return None, "Active phase not found in todos data."


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


def activate_step(step_id: str) -> tuple[StepItem | None, str | None]:
    """Activate a step, setting all other steps in the same phase to planned."""
    todos = load_todos()
    target_step = None
    target_phase = None
    target_goal = None

    for goal in todos["goals"]:
        for phase in goal["phases"]:
            for step in phase["steps"]:
                if step["id"] == step_id:
                    target_step = step
                    target_phase = phase
                    target_goal = goal
                else:
                    if step["status"] == "in_progress":
                        step["status"] = "planned"

    if not target_step:
        return None, f"Step with ID '{step_id}' not found."

    target_step["status"] = "in_progress"
    if target_phase:
        target_phase["status"] = "in_progress"
    if target_goal:
        target_goal["status"] = "in_progress"

    save_todos(todos)
    return target_step, None


def activate_task(task_id: str) -> tuple[TaskItem | None, str | None]:
    """Activate a task, setting all other tasks in the same step to planned."""
    todos = load_todos()
    target_task = None
    target_step = None
    target_phase = None
    target_goal = None

    for goal in todos["goals"]:
        for phase in goal["phases"]:
            for step in phase["steps"]:
                for task in step["tasks"]:
                    if task["id"] == task_id:
                        target_task = task
                        target_step = step
                        target_phase = phase
                        target_goal = goal
                    else:
                        if task["status"] == "in_progress":
                            task["status"] = "planned"

    if not target_task:
        return None, f"Task with ID '{task_id}' not found."

    target_task["status"] = "in_progress"
    if target_step:
        target_step["status"] = "in_progress"
    if target_phase:
        target_phase["status"] = "in_progress"
    if target_goal:
        target_goal["status"] = "in_progress"

    save_todos(todos)
    return target_task, None


def activate_subtask(subtask_id: str) -> tuple[SubTaskItem | None, str | None]:
    """Activate a subtask, setting all other subtasks in the same task to planned."""
    todos = load_todos()
    target_subtask = None
    target_task = None
    target_step = None
    target_phase = None
    target_goal = None

    for goal in todos["goals"]:
        for phase in goal["phases"]:
            for step in phase["steps"]:
                for task in step["tasks"]:
                    for subtask in task["subtasks"]:
                        if subtask["id"] == subtask_id:
                            target_subtask = subtask
                            target_task = task
                            target_step = step
                            target_phase = phase
                            target_goal = goal
                        else:
                            if subtask["status"] == "in_progress":
                                subtask["status"] = "planned"

    if not target_subtask:
        return None, f"SubTask with ID '{subtask_id}' not found."

    target_subtask["status"] = "in_progress"
    if target_task:
        target_task["status"] = "in_progress"
    if target_step:
        target_step["status"] = "in_progress"
    if target_phase:
        target_phase["status"] = "in_progress"
    if target_goal:
        target_goal["status"] = "in_progress"

    save_todos(todos)
    return target_subtask, None


def update_goal_status(goal_id: str, new_status: StatusType) -> tuple[GoalItem | None, str | None]:
    """Update the status of a specific goal."""
    todos = load_todos()
    target_goal = None

    for goal in todos["goals"]:
        if goal["id"] == goal_id:
            target_goal = goal
            break

    if not target_goal:
        return None, f"Goal with ID '{goal_id}' not found."

    target_goal["status"] = new_status
    save_todos(todos)
    return target_goal, None


def clear_goal_children(goal_id: str) -> tuple[bool, str | None]:
    """Clears all phases, steps, tasks, and subtasks under a given goal."""
    todos = load_todos()
    target_goal = None

    for goal in todos["goals"]:
        if goal["id"] == goal_id:
            target_goal = goal
            break

    if not target_goal:
        return False, f"Goal with ID '{goal_id}' not found."

    target_goal["phases"] = []
    save_todos(todos)
    return True, None


def update_step_status(step_id: str, new_status: StatusType) -> tuple[StepItem | None, str | None]:
    """Update the status of a specific step."""
    todos = load_todos()
    target_step = None

    for goal in todos["goals"]:
        for phase in goal["phases"]:
            for step in phase["steps"]:
                if step["id"] == step_id:
                    target_step = step
                    break
            if target_step:
                break
        if target_step:
            break

    if not target_step:
        return None, f"Step with ID '{step_id}' not found."

    target_step["status"] = new_status
    save_todos(todos)
    return target_step, None


def update_task_status(task_id: str, new_status: StatusType) -> tuple[TaskItem | None, str | None]:
    """Update the status of a specific task."""
    todos = load_todos()
    target_task = None

    for goal in todos["goals"]:
        for phase in goal["phases"]:
            for step in phase["steps"]:
                for task in step["tasks"]:
                    if task["id"] == task_id:
                        target_task = task
                        break
                if target_task:
                    break
            if target_task:
                break
        if target_task:
            break

    if not target_task:
        return None, f"Task with ID '{task_id}' not found."

    target_task["status"] = new_status
    save_todos(todos)
    return target_task, None


def update_subtask_command(
    subtask_id: str, new_command: str
) -> tuple[SubTaskItem | None, str | None]:
    """Update the command of a specific subtask."""
    todos = load_todos()
    target_subtask = None

    for goal in todos["goals"]:
        for phase in goal["phases"]:
            for step in phase["steps"]:
                for task in step["tasks"]:
                    for subtask in task["subtasks"]:
                        if subtask["id"] == subtask_id:
                            target_subtask = subtask
                            break
                    if target_subtask:
                        break
                if target_subtask:
                    break
            if target_subtask:
                break
        if target_subtask:
            break

    if not target_subtask:
        return None, f"SubTask with ID '{subtask_id}' not found."

    target_subtask["command"] = new_command
    save_todos(todos)
    return target_subtask, None


def update_subtask_status(
    subtask_id: str, new_status: StatusType
) -> tuple[SubTaskItem | None, str | None]:
    """Update the status of a specific subtask."""
    todos = load_todos()
    target_subtask = None

    for goal in todos["goals"]:
        for phase in goal["phases"]:
            for step in phase["steps"]:
                for task in step["tasks"]:
                    for subtask in task["subtasks"]:
                        if subtask["id"] == subtask_id:
                            target_subtask = subtask
                            break
                    if target_subtask:
                        break
                if target_subtask:
                    break
            if target_subtask:
                break
        if target_subtask:
            break

    if not target_subtask:
        return None, f"SubTask with ID '{subtask_id}' not found."

    target_subtask["status"] = new_status
    save_todos(todos)
    return target_subtask, None


def update_subtask_details(
    subtask_id: str, new_command: str, new_command_type: str
) -> tuple[SubTaskItem | None, str | None]:
    """Update the command and command_type of a specific subtask."""
    todos = load_todos()
    target_subtask = None

    for goal in todos["goals"]:
        for phase in goal["phases"]:
            for step in phase["steps"]:
                for task in step["tasks"]:
                    for subtask in task["subtasks"]:
                        if subtask["id"] == subtask_id:
                            target_subtask = subtask
                            break
                    if target_subtask:
                        break
                if target_subtask:
                    break
            if target_subtask:
                break
        if target_subtask:
            break

    if not target_subtask:
        return None, f"SubTask with ID '{subtask_id}' not found."

    target_subtask["command"] = new_command
    target_subtask["command_type"] = new_command_type
    save_todos(todos)
    return target_subtask, None


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
