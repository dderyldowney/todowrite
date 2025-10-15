import sys
import os
from afs_fastapi.core.todos_manager import update_task_status

# Add the project root to the python path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '.'))
sys.path.insert(0, project_root)

task_ids = ["task-20251014_182131_991043", "task-20251014_182131_999410"]
new_status = "done"

for task_id in task_ids:
    update_task_status(task_id, new_status)
    print(f"Task {task_id} status updated to {new_status}")