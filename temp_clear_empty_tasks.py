from afs_fastapi.core.todos_manager import load_todos, save_todos

todos = load_todos()
modified_goals = []

for goal in todos["goals"]:
    modified_phases = []
    for phase in goal["phases"]:
        modified_steps = []
        for step in phase["steps"]:
            # Only keep steps that have at least one task
            if step["tasks"]:
                modified_steps.append(step)

        # Update the phase's steps with the filtered list
        phase["steps"] = modified_steps
        modified_phases.append(phase)

    # Update the goal's phases with the filtered list
    goal["phases"] = modified_phases
    modified_goals.append(goal)

todos["goals"] = modified_goals
save_todos(todos)

print("Empty task lists cleared successfully.")
