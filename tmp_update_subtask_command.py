import sys
import os
from afs_fastapi.core.todos_manager import update_subtask_command

# Add the project root to the python path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '.'))
sys.path.insert(0, project_root)

subtask_id = "subtask-20251014_182131_984322"
new_command = "echo \"This is a placeholder for implement_error_fix_2.py\""

update_subtask_command(subtask_id, new_command)
print(f"Subtask {subtask_id} command updated to: {new_command}")