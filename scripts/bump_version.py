#!/usr/bin/env python3
"""Version bumping script for ToDoWrite project."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path


def bump_version(new_version: str) -> None:
    """Bump the version in the VERSION file.

    Args:
        new_version: The new version string to set.
    """
    version_file = Path(__file__).parent.parent / "VERSION"

    # Validate version format (basic semantic versioning)
    import re

    version_pattern = r"^\d+\.\d+\.\d+(?:-[a-zA-Z0-9]+)?$"
    if not re.match(version_pattern, new_version):
        print(f"Error: Invalid version format: {new_version}")
        print("Expected format: X.Y.Z or X.Y.Z-PRERELEASE")
        sys.exit(1)

    # Write new version
    version_file.write_text(new_version.strip() + "\n", encoding="utf-8")
    print(f"Version bumped to: {new_version}")


def get_current_version() -> str:
    """Get the current version from the VERSION file.

    Returns:
        The current version string.
    """
    version_file = Path(__file__).parent.parent / "VERSION"
    return version_file.read_text(encoding="utf-8").strip()


def main() -> None:
    """Main entry point for the version bump script."""
    parser = argparse.ArgumentParser(description="Manage ToDoWrite project version")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Bump command
    bump_parser = subparsers.add_parser("bump", help="Bump to a new version")
    bump_parser.add_argument("version", help="New version (e.g., 0.2.3, 1.0.0)")

    # Get command
    subparsers.add_parser("get", help="Get current version")

    args = parser.parse_args()

    if args.command == "bump":
        bump_version(args.version)
    elif args.command == "get":
        print(get_current_version())
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
