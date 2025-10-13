import sys
from pathlib import Path

project_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(project_root))

from afs_fastapi.core.todos_manager import load_todos, save_todos, validate_all_items  # noqa: E402


def main():
    print("Attempting to load and save todos.json to trigger validation and potential cleanup...")
    todos = load_todos()
    print(f"Loaded {len(todos['goals'])} goals.")

    # This will trigger the validation pipeline within save_todos
    save_todos(todos)
    print("todos.json loaded and saved. Check for validation warnings above.")

    # Optionally, run explicit validation and print errors
    print("\nRunning explicit validation:")
    validation_results = validate_all_items()
    if validation_results:
        print(f"Found {len(validation_results)} items with validation errors:")
        for item_id, errors in validation_results.items():
            print(f"  Item ID: {item_id}, Errors: {errors}")
    else:
        print("No validation errors found.")


if __name__ == "__main__":
    main()
