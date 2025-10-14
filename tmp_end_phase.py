import sys
from pathlib import Path

# Add project root to sys.path
project_root = Path(__file__).resolve().parent
sys.path.insert(0, str(project_root))

from afs_fastapi.core.todos_manager import end_phase, get_active_phase  # noqa: E402

active_phase = get_active_phase()

if active_phase:
    print(f"Attempting to end active phase: {active_phase['title']} (ID: {active_phase['id']})")
    ended_phase, error = end_phase(active_phase["id"])
    if ended_phase:
        print(f"Successfully ended phase: {ended_phase['title']}")
    else:
        print(f"Failed to end phase: {error}")
else:
    print("No active phase found.")
