import sys
from pathlib import Path

project_root = Path(__file__).resolve().parent
sys.path.insert(0, str(project_root))

from afs_fastapi.core.todos_manager import add_goal  # noqa: E402

if __name__ == "__main__":
    add_goal(
        title="System Maintenance",
        description="Improve overall system stability and maintainability.",
        category="maintenance",
        priority="high",
    )
    print("Added strategic goal: System Maintenance")
