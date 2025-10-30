#!/usr/bin/env python3
"""
Script to check that the deprecated schema doesn't have unintended changes.

This should be run in CI/CD to ensure no one is modifying the deprecated schema.
"""

import json
import sys
from pathlib import Path


def get_schema_content(path: Path) -> dict:
    """Load schema content from file."""
    try:
        with open(path) as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


def check_deprecated_schema() -> bool:
    """Check that deprecated schema hasn't been modified."""
    primary_path = Path("todowrite/schemas/todowrite.schema.json")
    deprecated_path = Path("configs/schemas/todowrite.schema.json")

    # Load both schemas
    primary_content = get_schema_content(primary_path)
    deprecated_content = get_schema_content(deprecated_path)

    if not deprecated_content:
        print("INFO: Deprecated schema not found (may have been cleaned up)")
        return True

    if not primary_content:
        print("❌ Primary schema not found!")
        return False

    # Check if deprecated schema still has deprecation notice
    deprecated_title = deprecated_content.get("title", "")
    if "DEPRECATED" not in deprecated_title:
        print("❌ Deprecated schema title missing DEPRECATED marker!")
        print(f"Found: {deprecated_title}")
        return False

    # Check that core schema structure matches
    def get_core_properties(schema: dict) -> dict:
        """Get core schema properties for comparison."""
        return {
            "required": schema.get("required", []),
            "properties": schema.get("properties", {}),
            "type": schema.get("type", "object"),
        }

    primary_core = get_core_properties(primary_content)
    deprecated_core = get_core_properties(deprecated_content)

    if primary_core != deprecated_core:
        print("❌ Deprecated schema has different core properties than primary!")
        print("This suggests someone modified the deprecated schema.")
        print("All schema changes should be made to the primary schema location.")
        return False

    print("✅ Deprecated schema check passed")
    print(f"Deprecated schema title: {deprecated_title}")
    print("Core properties match primary schema")

    return True


def main() -> int:
    """Main function."""
    print("ToDoWrite Deprecated Schema Check")
    print("=" * 40)

    if check_deprecated_schema():
        print("\n✅ Deprecated schema hasn't been modified.")
        return 0
    else:
        print("\n❌ Deprecated schema has been modified!")
        print("All schema changes must be made to:")
        print("  todowrite/schemas/todowrite.schema.json")
        print("Never modify:")
        print("  configs/schemas/todowrite.schema.json")
        return 1


if __name__ == "__main__":
    sys.exit(main())
