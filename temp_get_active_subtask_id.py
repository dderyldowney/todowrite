import os
import sys

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "afs_fastapi")))

from afs_fastapi.core.todos_manager import get_active_items


def main():
    active_items = get_active_items()
    active_subtask = active_items.get("subtask")

    if active_subtask:
        print(f"Active SubTask ID: {active_subtask['id']}")
        print(f"Active SubTask Title: {active_subtask['title']}")
    else:
        print("No active subtask found.")


if __name__ == "__main__":
    main()
