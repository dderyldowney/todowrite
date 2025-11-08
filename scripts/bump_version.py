#!/usr/bin/env python3
"""
Version bump utility for ToDoWrite project.

This script provides a simple workflow to bump the version number
while maintaining the VERSION file as the single source of truth.

Usage:
    python scripts/bump_version.py 0.3.2
    python scripts/bump_version.py patch
    python scripts/bump_version.py minor
    python scripts/bump_version.py major
"""

import argparse
import re
import sys
from pathlib import Path


def get_version() -> str:
    """Read version from VERSION file (single source of truth)."""
    version_file = Path(__file__).parent.parent / "VERSION"
    try:
        return version_file.read_text(encoding="utf-8").strip()
    except (FileNotFoundError, OSError) as e:
        msg = f"VERSION file not found at {version_file}"
        raise FileNotFoundError(msg) from e


def parse_version(version_str: str) -> tuple[int, int, int]:
    """Parse version string into (major, minor, patch)."""
    match = re.match(r"^(\d+)\.(\d+)\.(\d+)$", version_str.strip())
    if not match:
        msg = f"Invalid version format: {version_str}. Expected: X.Y.Z"
        raise ValueError(msg)
    return tuple(int(x) for x in match.groups())


def format_version(major: int, minor: int, patch: int) -> str:
    """Format version components into string."""
    return f"{major}.{minor}.{patch}"


def bump_version_type(current: str, bump_type: str) -> str:
    """Bump version by type (patch, minor, major)."""
    major, minor, patch = parse_version(current)

    if bump_type == "patch":
        patch += 1
    elif bump_type == "minor":
        minor += 1
        patch = 0
    elif bump_type == "major":
        major += 1
        minor = 0
        patch = 0
    else:
        msg = f"Invalid bump type: {bump_type}. Expected: patch, minor, major"
        raise ValueError(msg)

    return format_version(major, minor, patch)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Bump version in VERSION file"
    )
    parser.add_argument(
        "new_version",
        help="New version (X.Y.Z) or bump type (patch, minor, major)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be changed without making changes",
    )

    args = parser.parse_args()

    try:
        # Get current version
        current_version = get_version()
        print(f"Current version: {current_version}")

        # Determine new version
        if args.new_version in ["patch", "minor", "major"]:
            new_version = bump_version_type(current_version, args.new_version)
            print(
                f"Bumping {args.new_version}: {current_version} → "
                f"{new_version}"
            )
        else:
            # Validate explicit version format
            parse_version(args.new_version)
            new_version = args.new_version
            print(f"Setting version: {current_version} → {new_version}")

        if args.dry_run:
            print("🔍 DRY RUN - No changes made")
            return 0

        # Update VERSION file
        version_file = Path(__file__).parent.parent / "VERSION"
        version_file.write_text(f"{new_version}\n", encoding="utf-8")
        print(f"✅ Updated VERSION file to {new_version}")

        # Show current state
        print(f"✅ Verified: get_version() returns {get_version()}")

        return 0

    except (ValueError, OSError, RuntimeError) as e:
        print(f"❌ Error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
