import os
import sys

from afs_fastapi.core.todos_manager import update_subtask_status

# Add the project root to the python path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "."))
sys.path.insert(0, project_root)

subtask_id = "subtask-20251014_182131_975074"
new_status = "done"

update_subtask_status(subtask_id, new_status)
print(f"Subtask {subtask_id} status updated to {new_status}")
