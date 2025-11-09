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


def update_readme_badges(
    current_version: str, new_version: str, dry_run: bool = False
) -> None:
    """Update version badges in README.md file."""
    readme_path = Path(__file__).parent.parent / "README.md"

    if not readme_path.exists():
        print(f"⚠️ README.md not found at {readme_path}")
        return

    try:
        readme_content = readme_path.read_text(encoding="utf-8")
        original_content = readme_content

        # Update version badge
        readme_content = re.sub(
            r"\[!\[Version [^\]]*\]\([^\)]*\)\]\([^\)]*\)",
            f"[![Version {new_version}](https://img.shields.io/badge/version-{new_version}-green.svg)](https://github.com/dderyldowney/todowrite)",
            readme_content,
        )

        # Update PyPI todowrite badge
        readme_content = re.sub(
            r"\[!\[PyPI\]\([^\)]*todowrite-[^\)]*\)\]\([^\)]*\)",
            f"[![PyPI](https://img.shields.io/badge/todowrite-{new_version}-blue.svg)](https://pypi.org/project/todowrite/)",
            readme_content,
        )

        # Update PyPI todowrite-cli badge
        readme_content = re.sub(
            r"\[!\[PyPI CLI\]\([^\)]*todowrite--cli-[^\)]*\)\]\([^\)]*\)",
            f"[![PyPI CLI](https://img.shields.io/badge/todowrite--cli-{new_version}-blue.svg)](https://pypi.org/project/todowrite-cli/)",
            readme_content,
        )

        # Check if any changes were made
        if readme_content != original_content:
            if dry_run:
                print("🔍 DRY RUN - README.md changes:")
                # Show what would change
                changes = []
                lines_original = original_content.split("\n")
                lines_new = readme_content.split("\n")
                for i, (old, new) in enumerate(
                    zip(lines_original, lines_new, strict=False)
                ):
                    if old != new:
                        changes.append(f"Line {i+1}: {old.strip()}")
                        changes.append(f"Line {i+1}: {new.strip()}")
                for change in changes:
                    print(f"  {change}")
            else:
                readme_path.write_text(readme_content, encoding="utf-8")
                print(f"✅ Updated README.md badges to version {new_version}")
        else:
            print(
                f"No README.md updates needed "
                f"(version {current_version} not found)"
            )

    except (OSError, UnicodeDecodeError) as e:
        print(f"⚠️ Error updating README.md: {e}")


def update_fallback_versions(new_version: str, dry_run: bool = False) -> None:
    """Update fallback versions in package version.py files."""
    package_files = [
        Path(__file__).parent.parent
        / "lib_package"
        / "src"
        / "todowrite"
        / "version.py",
        Path(__file__).parent.parent
        / "cli_package"
        / "src"
        / "todowrite_cli"
        / "version.py",
    ]

    for package_file in package_files:
        if not package_file.exists():
            print(f"⚠️ Package version file not found: {package_file}")
            continue

        try:
            content = package_file.read_text(encoding="utf-8")
            original_content = content

            # Update fallback version in else block only
            # Look for pattern in else block: __version__ = "unknown" or
            # __version__ = "0.4.1"
            # We need to be careful to only update the fallback,
            # not the import from shared_version.py
            lines = content.split("\n")
            in_else_block = False

            for i, line in enumerate(lines):
                stripped = line.strip()

                # Detect else block
                if stripped.startswith("else:"):
                    in_else_block = True
                    continue

                # If we're in an else block and find a __version__ assignment,
                # update it
                if in_else_block and "__version__ = " in line:
                    # Replace the version string
                    lines[i] = re.sub(
                        r'(__version__ = )"([^"]*)"',
                        f'\\1"{new_version}"',
                        line,
                    )
                    break  # Only update the first __version__ in else block

                # If we encounter another block structure,
                # we're no longer in the else block
                keywords = ("def ", "class ", "if ")
                if in_else_block and stripped.startswith(keywords):
                    break

            content = "\n".join(lines)

            # Check if any changes were made
            if content != original_content:
                if dry_run:
                    print(f"🔍 DRY RUN - {package_file.name} changes:")
                    # Show what would change
                    lines_original = original_content.split("\n")
                    lines_new = content.split("\n")
                    for i, (old, new) in enumerate(
                        zip(lines_original, lines_new, strict=False)
                    ):
                        if old != new and "__version__" in old:
                            print(f"  Line {i+1}: {old.strip()}")
                            print(f"  Line {i+1}: {new.strip()}")
                else:
                    package_file.write_text(content, encoding="utf-8")
                    print(
                        f"✅ Updated fallback version in {package_file.name}"
                    )
            else:
                print(f"No fallback version updates needed in {package_file}")

        except (OSError, UnicodeDecodeError) as e:
            print(f"⚠️ Error updating {package_file}: {e}")


def verify_readme_versions(expected_version: str) -> bool:
    """Verify that README.md badges contain the expected version."""
    readme_path = Path(__file__).parent.parent / "README.md"

    if not readme_path.exists():
        print(f"⚠️ README.md not found at {readme_path}")
        return False

    try:
        readme_content = readme_path.read_text(encoding="utf-8")

        # Check for version in badges
        version_patterns = [
            rf"version-{re.escape(expected_version)}",
            rf"todowrite-{re.escape(expected_version)}-blue\.svg",
            rf"todowrite--cli-{re.escape(expected_version)}-blue\.svg",
        ]

        missing_patterns = []
        for pattern in version_patterns:
            if not re.search(pattern, readme_content):
                missing_patterns.append(pattern)

        if missing_patterns:
            print(
                f"❌ README.md missing version {expected_version} in badges:"
            )
            for pattern in missing_patterns:
                print(f"  - Pattern not found: {pattern}")
            return False
        print(f"✅ README.md badges correctly show version {expected_version}")
        return True

    except (OSError, UnicodeDecodeError) as e:
        print(f"⚠️ Error verifying README.md: {e}")
        return False


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
        description="Bump version in VERSION file and README.md badges"
    )
    parser.add_argument(
        "new_version",
        nargs="?",
        help="New version (X.Y.Z) or bump type (patch, minor, major)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be changed without making changes",
    )
    parser.add_argument(
        "--verify-only",
        action="store_true",
        help="Only verify current README.md versions without updating",
    )

    args = parser.parse_args()

    # Validate arguments
    if not args.verify_only and not args.new_version:
        parser.error("new_version is required when not using --verify-only")

    try:
        # Get current version
        current_version = get_version()
        print(f"Current version: {current_version}")

        # Handle verify-only mode
        if args.verify_only:
            print("🔍 Verifying README.md versions...")
            verify_readme_versions(current_version)
            return 0

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

        print("\n📋 Checking README.md badges...")
        verify_readme_versions(current_version)

        if args.dry_run:
            print("\n🔍 DRY RUN - No changes made")
            update_readme_badges(current_version, new_version, dry_run=True)
            update_fallback_versions(new_version, dry_run=True)
            return 0

        print(f"\n📝 Updating files to version {new_version}...")

        # Update README.md badges FIRST (before VERSION file)
        print("🔄 Updating README.md badges...")
        update_readme_badges(current_version, new_version, dry_run=False)

        # Update fallback versions in package files
        print("🔄 Updating fallback versions in package files...")
        update_fallback_versions(new_version, dry_run=False)

        # Update VERSION file LAST
        print("🔄 Updating VERSION file...")
        version_file = Path(__file__).parent.parent / "VERSION"
        version_file.write_text(f"{new_version}\n", encoding="utf-8")
        print(f"✅ Updated VERSION file to {new_version}")

        # Verify the updates
        print("\n✅ Verifying updates...")
        print(f"✅ Verified: get_version() returns {get_version()}")
        verify_readme_versions(new_version)

        print(
            f"\nSuccessfully bumped version from {current_version} "
            f"→ {new_version}"
        )
        print(
            "💡 VERSION file, README.md badges, and package fallback versions "
            "have been updated"
        )
        print("📝 Files are ready for git commit")

        return 0

    except (ValueError, OSError, RuntimeError) as e:
        print(f"❌ Error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
