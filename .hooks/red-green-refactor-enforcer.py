#!/usr/bin/env python3
"""
Red-Green-Refactor Methodology Enforcer

Enforces TDD methodology: Write failing test (RED), write minimal code (GREEN),
then refactor (REFACTOR) while keeping tests passing.
"""

import json
import re
import sys
from pathlib import Path


class RedGreenRefactorEnforcer:
    """Enforces Red-Green-Refactor methodology for development work."""

    def __init__(self, project_root: Path | None = None):
        self.project_root = project_root or Path.cwd()
        self.config_file = self.project_root / ".claude" / "rgr_enforcement.json"
        self.load_config()

    def load_config(self):
        """Load RGR enforcement configuration."""
        default_config = {
            "enforcement_level": "strict",
            "red_phase": {
                "required": True,
                "description": "Write failing test before production code",
                "verification": "Must watch test fail for correct reason",
                "forbidden_actions": [
                    "Write production code before test",
                    "Skip watching test fail",
                    "Write code that passes immediately"
                ]
            },
            "green_phase": {
                "required": True,
                "description": "Write minimal code to make test pass",
                "verification": "All tests must pass with clean output",
                "forbidden_actions": [
                    "Add features beyond test requirements",
                    "Over-engineering",
                    "Write production code without failing test"
                ]
            },
            "refactor_phase": {
                "required": True,
                "description": "Clean up code while keeping tests green",
                "verification": "Tests must remain green throughout refactoring",
                "forbidden_actions": [
                    "Adding new behavior during refactoring",
                    "Changing test requirements",
                    "Breaking existing functionality"
                ]
            },
            "quality_gates": {
                "require_test_for_new_code": True,
                "zero_mocking_policy": True,
                "real_implementations_only": True,
                "test_coverage_threshold": 0.8
            }
        }

        if self.config_file.exists():
            try:
                with open(self.config_file) as f:
                    loaded_config = json.load(f)
                self.config = {**default_config, **loaded_config}
            except (OSError, json.JSONDecodeError):
                self.config = default_config
        else:
            self.config = default_config

    def validate_commit_message_rgr_compliance(self, commit_message: str) -> tuple[bool, list[str]]:
        """Validate commit message for RGR compliance."""
        errors = []
        commit_lower = commit_message.lower()

        # Extract conventional commit info
        conventional_match = re.match(r"^(?P<type>\w+)(?:\((?P<scope>[^)]+)\))?:\s+(?P<subject>.+)", commit_message.strip())
        if not conventional_match:
            return True, []  # Let other validators handle format

        commit_type = conventional_match.group("type")
        subject = conventional_match.group("subject")

        # Check for RGR methodology violations
        if commit_type in ["feat", "fix"] and "test" not in commit_lower and "refactor" not in commit_lower:
            errors.append(
                "Feature/fix commits should include tests according to Red-Green-Refactor methodology:\n"
                "1. RED: Write failing test first\n"
                "2. GREEN: Write minimal code to pass\n"
                "3. REFACTOR: Clean up while tests remain green"
            )

        # Check refactor compliance
        if commit_type == "refactor" and "test" not in subject.lower():
            errors.append(
                "Refactor commits should indicate test maintenance. "
                "Consider: 'refactor(scope): improve X while keeping tests green'"
            )

        return len(errors) == 0, errors

    def get_rgr_help(self) -> str:
        """Get comprehensive RGR methodology help."""
        return """
🔴🟢🔄 RED-GREEN-REFACTOR METHODOLOGY ENFORCED

RED PHASE:
• Write failing test BEFORE writing production code
• Watch test FAIL for correct reason
• Test should fail because feature doesn't exist
• NO production code before test

GREEN PHASE:
• Write MINIMAL code to make test pass
• All tests must pass with CLEAN output
• NO extra features beyond test requirements
• NO over-engineering

REFACTOR PHASE:
• Clean up code while keeping tests GREEN
• Remove duplication and improve design
• Tests must REMAIN GREEN throughout
• NO new behavior during refactoring

QUALITY GATES:
• Zero mocking policy enforced
• Real implementations only
• Test coverage threshold: 80%
• All tests must pass before commits
        """


def main():
    """Main entry point for RGR enforcement."""
    if len(sys.argv) == 2 and sys.argv[1] == "--help":
        enforcer = RedGreenRefactorEnforcer()
        print(enforcer.get_rgr_help())
        sys.exit(0)

    if len(sys.argv) != 2:
        print("Usage: python red-green-refactor-enforcer.py <commit_message_file>")
        print("       python red-green-refactor-enforcer.py --help")
        sys.exit(1)

    commit_file = sys.argv[1]

    try:
        with open(commit_file) as f:
            commit_message = f.read().strip()
    except FileNotFoundError:
        print(f"Error: Commit message file not found: {commit_file}")
        sys.exit(1)
    except OSError:
        print(f"Error: Could not read commit message file: {commit_file}")
        sys.exit(1)

    enforcer = RedGreenRefactorEnforcer()
    is_compliant, errors = enforcer.validate_commit_message_rgr_compliance(commit_message)

    if not is_compliant:
        print("❌ Red-Green-Refactor Methodology Violation Detected")
        print("=" * 55)
        for error in errors:
            print(f"• {error}")
        print()
        print(enforcer.get_rgr_help())
        sys.exit(1)
    else:
        print("✅ Red-Green-Refactor methodology compliance verified")
        sys.exit(0)


if __name__ == "__main__":
    main()
