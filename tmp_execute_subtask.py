import sys
import os
from afs_fastapi.core.todos_manager import execute_subtask

# Add the project root to the python path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '.'))
sys.path.insert(0, project_root)

subtask_id = "subtask-20251014_182132_002469"

success, message = execute_subtask(subtask_id)
print(f"Subtask {subtask_id} execution: {success} - {message}")