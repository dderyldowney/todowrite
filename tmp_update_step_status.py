import sys
import os

# Add the project root to the python path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '.'))
sys.path.insert(0, project_root)

from afs_fastapi.core.todos_manager import update_step_status

step_id = "step-20251014_182131_996988"
new_status = "done"

update_step_status(step_id, new_status)
print(f"Step {step_id} status updated to {new_status}")