#!/usr/bin/env python3
"""Update CHANGELOG.md with recent git commits following Keep a Changelog format.

This script automates CHANGELOG.md maintenance for the AFS FastAPI agricultural
robotics platform, ensuring comprehensive change tracking essential for safety-
critical systems compliance (ISO 18497, ISO 11783).

Agricultural Context:
Multi-tractor coordination systems require complete audit trails for regulatory
compliance, debugging coordination issues, and maintaining equipment certification.
Automated changelog generation ensures no changes are missed in documentation.
"""

from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path
from typing import Any


def parse_git_commits(commits: list[str]) -> list[dict[str, Any]]:
    """Parse git commit log entries into structured data.

    Args:
        commits: List of commit strings in format "hash|subject|author|date"

    Returns:
        List of parsed commit dictionaries with type, scope, description
    """
    parsed_commits: list[dict[str, Any]] = []

    for commit in commits:
        if not commit.strip():
            continue

        parts = commit.split("|")
        if len(parts) < 4:
            continue

        commit_hash, subject, author, date = parts[0], parts[1], parts[2], parts[3]

        # Parse conventional commit format: type(scope): description
        # Supports both "type(scope): desc" and "type: desc" (no scope)
        pattern = r"^(\w+)(?:\(([^)]+)\))?: (.+)$"
        match = re.match(pattern, subject)

        if match:
            commit_type = match.group(1)
            scope = match.group(2) if match.group(2) else None
            description = match.group(3)

            parsed_commits.append(
                {
                    "hash": commit_hash,
                    "type": commit_type,
                    "scope": scope,
                    "description": description,
                    "author": author,
                    "date": date,
                }
            )

    return parsed_commits


def categorize_commits(commits: list[dict[str, Any]]) -> dict[str, list[dict[str, Any]]]:
    """Categorize commits by type into CHANGELOG sections.

    Args:
        commits: List of parsed commit dictionaries

    Returns:
        Dictionary mapping CHANGELOG sections to commit lists
    """
    categories: dict[str, list[dict[str, Any]]] = {
        "Added": [],
        "Changed": [],
        "Fixed": [],
        "Security": [],
        "Documentation": [],
        "Configuration": [],
    }

    for commit in commits:
        commit_type = commit.get("type", "")

        # Map conventional commit types to CHANGELOG sections
        if commit_type == "feat":
            categories["Added"].append(commit)
        elif commit_type == "fix":
            categories["Fixed"].append(commit)
        elif commit_type in ["refactor", "perf", "style"]:
            categories["Changed"].append(commit)
        elif commit_type == "security":
            categories["Security"].append(commit)
        elif commit_type == "docs":
            categories["Documentation"].append(commit)
        elif commit_type in ["config", "build", "ci", "chore"]:
            categories["Configuration"].append(commit)

    # Remove empty categories
    return {k: v for k, v in categories.items() if v}


def format_changelog_section(categorized: dict[str, list[dict[str, Any]]]) -> str:
    """Format categorized commits into Keep a Changelog sections.

    Args:
        categorized: Dictionary mapping sections to commit lists

    Returns:
        Formatted CHANGELOG sections as string
    """
    output: list[str] = []

    for section, commits in categorized.items():
        if not commits:
            continue

        output.append(f"### {section}")
        for commit in commits:
            scope_prefix = f"**{commit['scope']}**: " if commit["scope"] else ""
            output.append(f"- {scope_prefix}{commit['description']}")

        output.append("")  # Blank line between sections

    return "\n".join(output)


def update_changelog(existing_content: str, new_entries: dict[str, list[dict[str, Any]]]) -> str:
    """Update existing CHANGELOG.md content with new entries.

    Args:
        existing_content: Current CHANGELOG.md content
        new_entries: New categorized commit entries

    Returns:
        Updated CHANGELOG.md content
    """
    lines = existing_content.split("\n")

    # Find [Unreleased] section
    unreleased_index = -1
    for i, line in enumerate(lines):
        if line.strip() == "## [Unreleased]":
            unreleased_index = i
            break

    # If no [Unreleased] section, create one after header
    if unreleased_index == -1:
        # Find first ## [version] section
        version_index = -1
        for i, line in enumerate(lines):
            if line.startswith("## [") and "[Unreleased]" not in line:
                version_index = i
                break

        if version_index > 0:
            # Insert [Unreleased] before first version
            lines.insert(version_index, "")
            lines.insert(version_index, "## [Unreleased]")
            unreleased_index = version_index + 1
        else:
            # Append to end if no versions found
            lines.append("")
            lines.append("## [Unreleased]")
            unreleased_index = len(lines) - 1

    # Format new entries
    new_content = format_changelog_section(new_entries)

    # Find where to insert new content (after ## [Unreleased])
    insert_index = unreleased_index + 1

    # Skip existing empty lines
    while insert_index < len(lines) and lines[insert_index].strip() == "":
        insert_index += 1

    # Insert new content
    new_lines = new_content.split("\n")
    for j, new_line in enumerate(new_lines):
        lines.insert(insert_index + j, new_line)

    return "\n".join(lines)


def get_commits_since_last_changelog() -> list[str]:
    """Extract git commits since last CHANGELOG.md modification.

    Returns:
        List of commit strings in format "hash|subject|author|date"
    """
    try:
        # Get date of last CHANGELOG.md modification
        result = subprocess.run(
            ["git", "log", "-1", "--format=%ai", "--", "CHANGELOG.md"],
            capture_output=True,
            text=True,
            check=True,
        )

        last_change_date = result.stdout.strip()

        # If CHANGELOG.md never committed, get all commits
        if not last_change_date:
            cmd = ["git", "log", "--pretty=format:%h|%s|%an|%ad", "--date=short"]
        else:
            cmd = [
                "git",
                "log",
                "--pretty=format:%h|%s|%an|%ad",
                "--date=short",
                f"--since={last_change_date}",
            ]

        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        commits = result.stdout.strip().split("\n")

        # Filter out merge commits
        return [c for c in commits if c and "|Merge " not in c]

    except subprocess.CalledProcessError:
        return []


def identify_safety_critical_commits(commits: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Identify commits that are safety-critical for agricultural equipment.

    Args:
        commits: List of parsed commit dictionaries

    Returns:
        List of safety-critical commits (equipment, safety, coordination scopes)
    """
    safety_scopes = ["equipment", "safety", "coordination", "monitoring"]

    return [commit for commit in commits if commit.get("scope") in safety_scopes]


def format_with_agricultural_context(commit: dict[str, Any]) -> str:
    """Format commit with agricultural context for safety-critical entries.

    Args:
        commit: Parsed commit dictionary

    Returns:
        Formatted commit entry with context
    """
    base_format = commit["description"]

    # Add context note for safety-critical scopes
    safety_scopes = {
        "equipment": "multi-tractor equipment operations",
        "safety": "ISO 18497 agricultural safety compliance",
        "coordination": "fleet coordination systems",
        "monitoring": "field operation monitoring",
    }

    scope = commit.get("scope")
    if scope in safety_scopes:
        context = safety_scopes[scope]
        return f"{base_format} (affects {context})"

    return base_format


def create_backup(changelog_path: Path) -> None:
    """Create backup of CHANGELOG.md before modification.

    Args:
        changelog_path: Path to CHANGELOG.md file
    """
    backup_path = changelog_path.parent / f"{changelog_path.name}.bak"
    backup_path.write_text(changelog_path.read_text())


def main(changelog_path: str | None = None) -> int:
    """Main entry point for updatechangelog command.

    Args:
        changelog_path: Optional path to CHANGELOG.md (defaults to ./CHANGELOG.md)

    Returns:
        Exit code (0 for success, 1 for error)
    """
    # Determine CHANGELOG.md path
    if changelog_path:
        path = Path(changelog_path)
    else:
        path = Path.cwd() / "CHANGELOG.md"

    if not path.exists():
        print(f"Error: CHANGELOG.md not found at {path}")
        return 1

    # Create backup
    create_backup(path)

    # Get commits since last changelog update
    commit_strings = get_commits_since_last_changelog()

    if not commit_strings or (len(commit_strings) == 1 and not commit_strings[0]):
        print("No new commits to add to CHANGELOG.md")
        return 0

    # Parse and categorize commits
    parsed = parse_git_commits(commit_strings)
    categorized = categorize_commits(parsed)

    if not categorized:
        print("No categorized commits to add to CHANGELOG.md")
        return 0

    # Update CHANGELOG.md
    existing_content = path.read_text()
    updated_content = update_changelog(existing_content, categorized)

    # Write updated content
    path.write_text(updated_content)

    print("✅ CHANGELOG.md updated successfully")
    print(f"   Added {len(parsed)} commits across {len(categorized)} categories")

    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else None))
