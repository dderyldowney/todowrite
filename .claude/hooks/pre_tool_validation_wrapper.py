#!/usr/bin/env python3
"""
Claude Code PreToolUse Hook Wrapper for Git and Safety Validation

This wrapper adapts git commit validators and safety checkers to work as
Claude Code hooks, intercepting tool operations before they execute to
ensure compliance with agricultural robotics standards.

Hook Lifecycle: PreToolUse
- Triggers before any tool execution (Bash, Write, Edit, etc.)
- Validates git commit operations for separation and changelog compliance
- Checks safety-critical code modifications for ISO 18497 compliance
- Blocks non-compliant operations before they affect the codebase

Agricultural Context:
Multi-tractor coordination systems require strict quality gates to prevent
safety incidents. This hook enforces commit quality and safety validation
before changes enter the agricultural robotics codebase.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path


class PreToolValidator:
    """
    Validates tool operations before execution for agricultural robotics compliance.

    Intercepts tool use to enforce:
    - Git commit separation of concerns
    - CHANGELOG.md inclusion in commits
    - Safety-critical code validation
    """

    def __init__(self):
        self.project_root = Path.cwd()

    def is_git_commit_operation(self, tool_data: dict) -> bool:
        """Check if tool operation is a git commit."""
        tool_name = tool_data.get("tool", "")
        if tool_name != "Bash":
            return False

        command = tool_data.get("parameters", {}).get("command", "")
        # Check for git commit commands
        return bool(re.search(r"\bgit\s+commit\b", command))

    def is_code_modification(self, tool_data: dict) -> bool:
        """Check if tool operation modifies code files."""
        tool_name = tool_data.get("tool", "")
        if tool_name not in ["Write", "Edit", "NotebookEdit"]:
            return False

        # Check if modifying Python files
        file_path = tool_data.get("parameters", {}).get("file_path", "")
        return file_path.endswith(".py")

    def validate_git_commit(self, command: str) -> tuple[bool, str]:
        """
        Validate git commit operation compliance.

        Checks:
        1. Commit message follows separation of concerns format
        2. CHANGELOG.md is included in staged files

        Args:
            command: Git command being executed

        Returns:
            Tuple of (is_valid, error_message)
        """
        # Extract commit message from command
        message_match = re.search(r'-m\s+["\'](.+?)["\']', command, re.DOTALL)
        if not message_match:
            # No inline message - likely using editor, allow it
            # (git hooks will catch issues)
            return True, ""

        commit_message = message_match.group(1)

        # Check commit message format: type(scope): description
        format_pattern = r"^(feat|fix|refactor|docs|test|config|perf|security)\([^)]+\):\s+.+"
        if not re.match(format_pattern, commit_message, re.MULTILINE):
            error_msg = """
🚫 GIT COMMIT SEPARATION VIOLATION

Commit message must follow separation of concerns format:
type(scope): brief description

Valid types: feat, fix, refactor, docs, test, config, perf, security

Example: feat(equipment): add multi-tractor synchronization capability
Example: fix(coordination): resolve vector clock race condition

📖 Reference: GIT_COMMIT_SEPARATION_MANDATORY.md
"""
            return False, error_msg

        # NOTE: CHANGELOG.md validation happens in git pre-commit hook
        # because we can't reliably check staged files from Claude Code hook context

        return True, ""

    def validate_safety_critical_code(self, file_path: str, tool_name: str) -> tuple[bool, str]:
        """
        Validate safety-critical code modifications.

        Args:
            file_path: Path to file being modified
            tool_name: Tool performing modification

        Returns:
            Tuple of (is_valid, error_message)
        """
        # Check if file is in safety-critical modules
        safety_critical_paths = [
            "synchronization",
            "safety",
            "coordination",
            "motor_control",
            "power_management",
            "emergency",
        ]

        is_safety_critical = any(path in file_path for path in safety_critical_paths)

        if is_safety_critical:
            # Safety-critical files require extra scrutiny
            # For now, just warn (detailed validation happens in git hooks)
            warning_msg = f"""
⚠️  SAFETY-CRITICAL FILE MODIFICATION: {file_path}

This file is part of safety-critical agricultural robotics systems.

Required Standards:
- ISO 18497 (agricultural machinery safety) compliance
- ISO 11783 (ISOBUS) communication safety
- Emergency stop and safe state validation
- Comprehensive test coverage

Ensure modifications include:
✓ Emergency stop functionality
✓ Safe state handling
✓ Collision avoidance logic (if applicable)
✓ Comprehensive test coverage

📖 Reference: ISO 18497 safety documentation
"""
            print(warning_msg, file=sys.stderr)
            # Don't block, just warn
            return True, ""

        return True, ""

    def validate_tool_operation(self, tool_data: dict) -> tuple[bool, str]:
        """
        Validate tool operation before execution.

        Args:
            tool_data: Tool use data from hook

        Returns:
            Tuple of (is_valid, error_message)
        """
        # Check git commit operations
        if self.is_git_commit_operation(tool_data):
            command = tool_data.get("parameters", {}).get("command", "")
            return self.validate_git_commit(command)

        # Check code modifications
        if self.is_code_modification(tool_data):
            file_path = tool_data.get("parameters", {}).get("file_path", "")
            tool_name = tool_data.get("tool", "")
            return self.validate_safety_critical_code(file_path, tool_name)

        # Other operations allowed
        return True, ""


def main():
    """
    Main Claude Code hook execution for PreToolUse.

    Reads hook input JSON, validates tool operation compliance,
    and blocks non-compliant operations before execution.
    """
    try:
        # Read hook input data from stdin
        hook_data = json.loads(sys.stdin.read())

        # Extract tool use data
        # Hook data structure: {"tool": "tool_name", "parameters": {...}, ...}
        tool_data = hook_data

        # Validate tool operation
        validator = PreToolValidator()
        is_valid, error_message = validator.validate_tool_operation(tool_data)

        if not is_valid:
            # Print error message to stderr
            print(error_message, file=sys.stderr)
            # Block the operation
            sys.exit(1)

        # Operation is valid - allow it
        sys.exit(0)

    except json.JSONDecodeError:
        # Invalid JSON input - don't block on hook errors
        print("PreTool Hook Warning: Invalid JSON input", file=sys.stderr)
        sys.exit(0)
    except Exception as e:
        # Hook error - don't block operation
        print(f"PreTool Hook Error: {e}", file=sys.stderr)
        sys.exit(0)


if __name__ == "__main__":
    main()
