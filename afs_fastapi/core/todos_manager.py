import json
from datetime import datetime
from typing import TypedDict


class TaskItem(TypedDict):
    id: str
    description: str
    status: str
    date_completed: str | None


class PhaseItem(TypedDict):
    id: str
    name: str
    status: str
    date_started: str
    date_completed: str | None
    tasks: list[TaskItem]
    paused_at: str | None
    resumed_at: str | None
    strategic_goal_id: str


class StrategicGoal(TypedDict):
    id: str
    description: str
    category: str
    priority: str
    status: str
    date_added: str
    date_completed: str | None
    phases: list[PhaseItem]


class TodosData(TypedDict):
    strategic_goals: list[StrategicGoal]


TODOS_FILE = ".claude/todos.json"


def load_todos() -> TodosData:
    try:
        with open(TODOS_FILE) as f:
            todos: TodosData = json.load(f)
            return todos
    except FileNotFoundError:
        return TodosData(strategic_goals=[])


def save_todos(todos: TodosData) -> None:
    with open(TODOS_FILE, "w") as f:
        json.dump(todos, f, indent=2)


def get_strategic_goals() -> list[StrategicGoal]:
    todos = load_todos()
    return todos["strategic_goals"]


def add_strategic_goal(description: str, category: str, priority: str) -> StrategicGoal:
    todos = load_todos()
    new_id = f"strategic-{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    new_goal: StrategicGoal = {
        "id": new_id,
        "description": description,
        "category": category,
        "priority": priority,
        "status": "pending",
        "date_added": datetime.now().isoformat(timespec="seconds") + "Z",
        "date_completed": None,
        "phases": [],
    }
    todos["strategic_goals"].append(new_goal)
    save_todos(todos)
    return new_goal


def complete_strategic_goal(goal_id: str) -> bool:
    todos = load_todos()
    for goal in todos["strategic_goals"]:
        if goal["id"] == goal_id:
            goal["status"] = "completed"
            goal["date_completed"] = datetime.now().isoformat(timespec="seconds") + "Z"
            save_todos(todos)
            return True
    return False


def reorder_strategic_goals(goal_id: str, new_position: int) -> bool:
    todos = load_todos()
    goals: list[StrategicGoal] = todos["strategic_goals"]

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
    todos["strategic_goals"] = goals
    save_todos(todos)
    return True


def get_all_phases() -> list[PhaseItem]:
    todos = load_todos()
    all_phases: list[PhaseItem] = []
    for goal in todos["strategic_goals"]:
        for phase in goal["phases"]:
            phase["strategic_goal_id"] = goal["id"]
            all_phases.append(phase)
    return all_phases


def get_active_phase() -> PhaseItem | None:
    todos = load_todos()
    for goal in todos["strategic_goals"]:
        for phase in goal["phases"]:
            if phase.get("status") in ["active", "partially-paused"]:
                phase["strategic_goal_id"] = goal["id"]
                return phase
    return None


def start_phase(name: str, strategic_goal_id: str) -> tuple[PhaseItem | None, str | None]:
    todos = load_todos()

    # Check for existing active phase
    for goal in todos["strategic_goals"]:
        for phase in goal["phases"]:
            if phase.get("status") == "active":
                return None, f"Phase already active: {phase.get('name', 'Unknown Phase')}"

    new_phase_id = f"phase-{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    new_phase: PhaseItem = {
        "id": new_phase_id,
        "name": name,
        "status": "active",
        "date_started": datetime.now().isoformat(timespec="seconds") + "Z",
        "date_completed": None,
        "tasks": [],
        "paused_at": None,
        "resumed_at": None,
        "strategic_goal_id": strategic_goal_id,
    }

    goal_found = False
    for goal in todos["strategic_goals"]:
        if goal["id"] == strategic_goal_id:
            goal["phases"].append(new_phase)
            goal_found = True
            break

    if not goal_found:
        return None, f"Strategic goal with ID ''{strategic_goal_id}'' not found."

    save_todos(todos)
    return new_phase, None


def end_phase(force: bool = False) -> tuple[PhaseItem | None, str | None]:
    todos = load_todos()
    active_phase: PhaseItem | None = None
    active_goal: StrategicGoal | None = None

    for goal in todos["strategic_goals"]:
        for phase in goal["phases"]:
            if phase.get("status") == "active":
                active_phase = phase
                active_goal = goal
                break
        if active_phase:
            break

    if not active_phase:
        return None, "No active phase found."

    tasks: list[TaskItem] = active_phase.get("tasks", [])
    pending_tasks = [t for t in tasks if t.get("status") == "pending"]

    if pending_tasks and not force:
        return None, f"Phase has {len(pending_tasks)} pending tasks. Use --force to end anyway."

    active_phase["status"] = "completed"
    active_phase["date_completed"] = datetime.now().isoformat(timespec="seconds") + "Z"

    # Only complete the strategic goal if the phase is completed without forcing
    if not pending_tasks and active_goal:
        active_goal["status"] = "completed"
        active_goal["date_completed"] = datetime.now().isoformat(timespec="seconds") + "Z"

    save_todos(todos)
    return active_phase, None


def add_task_to_active_phase(description: str) -> tuple[TaskItem | None, str | None]:
    todos = load_todos()
    active_phase: PhaseItem | None = None

    for goal in todos["strategic_goals"]:
        for phase in goal["phases"]:
            if phase.get("status") == "active":
                active_phase = phase
                break
        if active_phase:
            break

    if not active_phase:
        return None, "No active phase found."

    new_task_id = f"task-{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    new_task: TaskItem = {
        "id": new_task_id,
        "description": description,
        "status": "pending",
        "date_completed": None,
    }

    if "tasks" not in active_phase:
        active_phase["tasks"] = []

    active_phase["tasks"].append(new_task)
    save_todos(todos)
    return new_task, None


def complete_task_in_active_phase(search_term: str) -> tuple[TaskItem | None, str | None]:
    todos = load_todos()
    active_phase: PhaseItem | None = None

    for goal in todos["strategic_goals"]:
        for phase in goal["phases"]:
            if phase.get("status") == "active":
                active_phase = phase
                break
        if active_phase:
            break

    if not active_phase:
        return None, "No active phase found."

    tasks: list[TaskItem] = active_phase.get("tasks", [])
    matched_task: TaskItem | None = None
    for task in tasks:
        if task["id"] == search_term or search_term.lower() in task["description"].lower():
            matched_task = task
            break

    if not matched_task:
        return None, f"Task not found matching ''{search_term}''"

    if matched_task["status"] == "completed":
        return None, f"Task already completed: {matched_task['description']}"

    matched_task["status"] = "completed"
    matched_task["date_completed"] = datetime.now().isoformat(timespec="seconds") + "Z"

    save_todos(todos)
    return matched_task, None


def activate_phase(phase_id: str) -> tuple[PhaseItem | None, str | None]:
    todos = load_todos()

    # Find the phase to activate and the current active phase
    phase_to_activate: PhaseItem | None = None
    current_active_phase: PhaseItem | None = None
    for goal in todos["strategic_goals"]:
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

    for goal in todos["strategic_goals"]:
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

    for goal in todos["strategic_goals"]:
        for phase in goal["phases"]:
            if phase.get("status") == "paused":
                paused_phase = phase
                break
        if paused_phase:
            break

    if not paused_phase:
        return None, "No paused phase found to resume."

    # Check for existing active phase
    for goal in todos["strategic_goals"]:
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
    goals: list[StrategicGoal] = todos["strategic_goals"]

    goal_found = False
    for i, goal in enumerate(goals):
        if goal["id"] == goal_id:
            goals.pop(i)
            goal_found = True
            break

    if not goal_found:
        return False, f"Strategic goal with ID ''{goal_id}'' not found."

    todos["strategic_goals"] = goals
    save_todos(todos)
    return True, None


def delete_phase(phase_id: str) -> tuple[bool, str | None]:
    todos = load_todos()

    phase_found = False
    for goal in todos["strategic_goals"]:
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
    todos = load_todos()

    task_found = False
    for goal in todos["strategic_goals"]:
        for phase in goal["phases"]:
            tasks: list[TaskItem] = phase["tasks"]
            for i, task in enumerate(tasks):
                if task["id"] == task_id:
                    tasks.pop(i)
                    task_found = True
                    break
            if task_found:
                break
        if task_found:
            break

    if not task_found:
        return False, f"Task with ID ''{task_id}'' not found."

    save_todos(todos)
    return True, None


def reorder_phases(phase_id: str, new_position: int) -> tuple[bool, str | None]:
    todos = load_todos()

    phase_to_move: PhaseItem | None = None
    goal_of_phase: StrategicGoal | None = None
    for goal in todos["strategic_goals"]:
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
    todos = load_todos()

    task_to_move: TaskItem | None = None
    phase_of_task: PhaseItem | None = None
    for goal in todos["strategic_goals"]:
        for phase in goal["phases"]:
            tasks: list[TaskItem] = phase["tasks"]
            for i, task in enumerate(tasks):
                if task["id"] == task_id:
                    task_to_move = phase["tasks"].pop(i)
                    phase_of_task = phase
                    break
            if task_to_move:
                break
        if task_to_move:
            break

    if not task_to_move:
        return False, f"Task with ID ''{task_id}'' not found."

    if not phase_of_task:
        return False, "Internal error: Phase of task not found."

    if new_position < 1:
        new_position = 1
    if new_position > len(phase_of_task["tasks"]) + 1:
        new_position = len(phase_of_task["tasks"]) + 1

    phase_of_task["tasks"].insert(new_position - 1, task_to_move)

    save_todos(todos)
    return True, None


def pause_strategic_goal(goal_id: str) -> tuple[bool | None, str | None]:
    todos = load_todos()

    goal_found = False
    for goal in todos["strategic_goals"]:
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
    for goal in todos["strategic_goals"]:
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
    todos = load_todos()

    strategic_goals: list[StrategicGoal] = todos["strategic_goals"]
    for goal in strategic_goals:
        has_paused_phase = False
        phases: list[PhaseItem] = goal["phases"]
        for phase in phases:
            tasks: list[TaskItem] = phase["tasks"]
            has_paused_task = any(t.get("status") == "paused" for t in tasks)
            if has_paused_task:
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
    todos = load_todos()

    task_found = False
    strategic_goals: list[StrategicGoal] = todos["strategic_goals"]
    for goal in strategic_goals:
        phases: list[PhaseItem] = goal["phases"]
        for phase in phases:
            tasks: list[TaskItem] = phase["tasks"]
            for task in tasks:
                if task["id"] == task_id:
                    if task.get("status") == "pending":
                        task["status"] = "paused"
                        task_found = True
                        break
                    else:
                        return None, f"Task is not pending. Current status: {task.get('status')}"
            if task_found:
                break
        if task_found:
            break

    if not task_found:
        return None, f"Task with ID ''{task_id}'' not found."

    save_todos(todos)
    update_parent_statuses()
    return True, None


def resume_task(task_id: str) -> tuple[bool | None, str | None]:
    todos = load_todos()

    task_found = False
    strategic_goals: list[StrategicGoal] = todos["strategic_goals"]
    for goal in strategic_goals:
        phases: list[PhaseItem] = goal["phases"]
        for phase in phases:
            tasks: list[TaskItem] = phase["tasks"]
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

    if not task_found:
        return None, f"Task with ID ''{task_id}'' not found."

    save_todos(todos)
    update_parent_statuses()
    return True, None
