import os
import sys

from afs_fastapi.core.todos_manager import update_goal_status

# Add the project root to the python path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "."))
sys.path.insert(0, project_root)

goal_id = "goal-20251014_181935_030970"
new_status = "done"

update_goal_status(goal_id, new_status)
print(f"Goal {goal_id} status updated to {new_status}")
