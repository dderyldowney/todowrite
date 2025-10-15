import os
import sys

from afs_fastapi.core.todos_manager import activate_phase, end_phase

# Add the project root to the python path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "."))
sys.path.insert(0, project_root)

phase_id = "phase-20251014_182131_986542"
activate_phase(phase_id)
print(f"Phase {phase_id} activated")
end_phase(force=True)
print(f"Phase {phase_id} status updated to done")
