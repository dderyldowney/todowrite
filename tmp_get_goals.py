import json
import sys
from pathlib import Path

# Add project root to sys.path
project_root = Path(__file__).resolve().parent
sys.path.insert(0, str(project_root))

from afs_fastapi.core.todos_manager import get_goals  # noqa: E402

goals = get_goals()
# Convert GoalItem objects (TypedDicts) to a JSON-serializable format
serializable_goals = []
for goal in goals:
    serializable_goals.append(goal)

print(json.dumps(serializable_goals, indent=2))
