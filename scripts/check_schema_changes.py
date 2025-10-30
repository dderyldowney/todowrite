#!/usr/bin/env python3
"""
Pre-commit hook to ensure schema changes are made against the package location.

This script checks that any modified schema files are in the correct location
and enforces the new schema change workflow.
"""

import json
import sys
from pathlib import Path
from typing import Any


def get_primary_schema_path() -> Path:
    """Get the primary schema file path."""
    return Path("todowrite/schemas/todowrite.schema.json")


def get_deprecated_schema_path() -> Path:
    """Get the deprecated schema file path."""
    return Path("configs/schemas/todowrite.schema.json")


def load_schema(schema_path: Path) -> dict[str, Any]:
    """Load schema from file."""
    try:
        with open(schema_path) as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


def check_schema_location() -> bool:
    """Check if schema changes are in the correct location."""
    primary_schema = get_primary_schema_path()
    deprecated_schema = get_deprecated_schema_path()

    # Check if primary schema exists
    if not primary_schema.exists():
        print("ERROR: Primary schema file not found!")
        print(f"Expected location: {primary_schema}")
        print("All schema changes must be made in the package location.")
        return False

    # Load both schemas
    primary_data = load_schema(primary_schema)
    deprecated_data = load_schema(deprecated_schema)

    # Check if deprecated schema has newer content (shouldn't happen)
    if deprecated_data:
        primary_title = primary_data.get("title", "").replace(" (DEPRECATED)", "")
        deprecated_title = deprecated_data.get("title", "").replace(" (DEPRECATED)", "")

        if primary_title and deprecated_title and primary_title != deprecated_title:
            print(
                "WARNING: Deprecated schema has different content than primary schema!"
            )
            print("This may indicate changes were made in the wrong location.")
            print(f"Primary: {primary_title}")
            print(f"Deprecated: {deprecated_title}")
            return False

    print("✅ Schema location check passed")
    print(f"Primary schema: {primary_schema}")
    if deprecated_schema.exists():
        print(f"Deprecated schema: {deprecated_schema} (should not be modified)")

    return True


def check_package_import() -> bool:
    """Test that the package schema import works."""
    try:
        import todowrite

        schema = todowrite.TODOWRITE_SCHEMA
        if isinstance(schema, dict) and len(schema) > 0:
            print("✅ Package schema import works")
            return True
        else:
            print("ERROR: Package schema import returned invalid data")
            return False
    except ImportError as e:
        print(f"ERROR: Cannot import todowrite package: {e}")
        return False
    except Exception as e:
        print(f"ERROR: Package schema import failed: {e}")
        return False


def main() -> int:
    """Main function."""
    print("ToDoWrite Schema Location Check")
    print("=" * 40)

    # Check schema location
    location_ok = check_schema_location()

    print()

    # Check package import
    import_ok = check_package_import()

    print()

    if location_ok and import_ok:
        print("✅ All checks passed!")
        print("Schema changes are being made in the correct location.")
        return 0
    else:
        print("❌ Some checks failed!")
        print("Please ensure:")
        print(
            "1. All schema changes are made in todowrite/schemas/todowrite.schema.json"
        )
        print("2. The todowrite package can be imported correctly")
        print("3. See SCHEMA_CHANGE_WORKFLOW.md for details")
        return 1


if __name__ == "__main__":
    sys.exit(main())
