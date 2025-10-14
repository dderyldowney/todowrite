import sys
from pathlib import Path

# Add project root to sys.path
project_root = Path(__file__).resolve().parent
sys.path.insert(0, str(project_root))

from afs_fastapi.core.todos_manager import add_goal  # noqa: E402

# Add new goal for system errors
new_goal_errors = add_goal(
    title="Locate and repair system errors",
    description="Identify and fix system-wide errors, including mypy and other type-checking issues.",
    category="maintenance",
    priority="high",
)
print(f"Added new goal: {new_goal_errors['title']} (ID: {new_goal_errors['id']})")

# Add new goal for code quality
new_goal_quality = add_goal(
    title="Improve code quality",
    description="Enhance overall code quality, readability, and adherence to best practices.",
    category="refactoring",
    priority="medium",
)
print(f"Added new goal: {new_goal_quality['title']} (ID: {new_goal_quality['id']})")
