import json
import os
import sys

from afs_fastapi.core.todos_manager import get_goals

# Add the project root to the python path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "."))
sys.path.insert(0, project_root)

goals = get_goals()
print(json.dumps(goals, indent=2))
