#!/usr/bin/env python3
"""
Git Commit Separation of Concerns Enforcement Hook

This pre-commit hook enforces mandatory separation of concerns in git commits
for the AFS FastAPI agricultural robotics platform. Ensures each commit
addresses exactly one logical concern for safety-critical development.

Agricultural Development Context:
Separation of concerns is essential for safety-critical agricultural robotics
where precise change tracking enables rapid debugging, regulatory compliance
(ISO 18497, ISO 11783), and surgical fixes without affecting unrelated systems.
"""

from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path


class CommitSeparationError(Exception):
    """Exception raised when commit separation validation fails."""

    pass


class CommitSeparationValidator:
    """Validates git commits follow separation of concerns methodology.

    Ensures each commit addresses exactly one concern category with proper
    formatting, scope definition, and agricultural robotics context.
    """

    # Valid commit types with their descriptions and requirements
    VALID_TYPES = {
        "feat": {
            "description": "New functionality or capability additions",
            "requires_tests": True,
            "requires_agricultural_context": True,
            "examples": [
                "feat(equipment): add multi-tractor synchronization capability",
                "feat(api): implement field allocation endpoint with ISOBUS integration",
                "feat(monitoring): add soil composition sensor interface",
            ],
        },
        "fix": {
            "description": "Correcting defects or unexpected behavior",
            "requires_tests": True,
            "requires_agricultural_context": True,
            "examples": [
                "fix(coordination): resolve vector clock synchronization race condition",
                "fix(api): correct equipment status validation logic",
                "fix(safety): ensure emergency stop triggers across all tractors",
            ],
        },
        "refactor": {
            "description": "Code structure improvements without behavior changes",
            "requires_tests": False,
            "requires_agricultural_context": True,
            "examples": [
                "refactor(equipment): extract tractor interface into abstract base class",
                "refactor(services): consolidate ISOBUS message handling logic",
                "refactor(monitoring): simplify sensor data aggregation pipeline",
            ],
        },
        "docs": {
            "description": "Documentation-only changes",
            "requires_tests": False,
            "requires_agricultural_context": True,
            "examples": [
                "docs(api): update equipment endpoint examples for agricultural context",
                "docs(safety): add ISO 18497 compliance documentation",
                "docs(workflow): enhance TDD methodology examples",
            ],
        },
        "test": {
            "description": "Test-only additions or improvements",
            "requires_tests": False,
            "requires_agricultural_context": True,
            "examples": [
                "test(equipment): add comprehensive tractor coordination scenarios",
                "test(integration): enhance multi-field operation validation",
                "test(performance): add sub-millisecond coordination timing tests",
            ],
        },
        "config": {
            "description": "Configuration, build, or tooling changes",
            "requires_tests": False,
            "requires_agricultural_context": False,
            "examples": [
                "config(hooks): enhance TDD enforcement with commit validation",
                "config(ci): add agricultural safety standards validation pipeline",
                "config(deps): update FastAPI to support enhanced ISOBUS features",
            ],
        },
        "perf": {
            "description": "Performance improvements without functional changes",
            "requires_tests": True,
            "requires_agricultural_context": True,
            "examples": [
                "perf(coordination): optimize vector clock operations for embedded systems",
                "perf(api): reduce ISOBUS message serialization overhead",
                "perf(monitoring): improve sensor data processing throughput",
            ],
        },
        "security": {
            "description": "Security-related improvements or fixes",
            "requires_tests": True,
            "requires_agricultural_context": True,
            "examples": [
                "security(api): add equipment authentication validation",
                "security(communication): enhance ISOBUS message encryption",
                "security(access): implement role-based tractor operation permissions",
            ],
        },
    }

    # Valid scope areas for agricultural robotics platform
    VALID_SCOPES = {
        "equipment",
        "coordination",
        "api",
        "monitoring",
        "safety",
        "services",
        "communication",
        "isobus",
        "sensors",
        "vision",
        "control",
        "power",
        "data",
        "fleet",
        "field",
        "workflow",
        "integration",
        "performance",
        "auth",
        "config",
        "docs",
        "test",
        "hooks",
        "ci",
        "deps",
    }

    # Agricultural robotics keywords that should appear in relevant commits
    AGRICULTURAL_KEYWORDS = {
        "tractor",
        "field",
        "equipment",
        "isobus",
        "iso 11783",
        "iso 18497",
        "agricultural",
        "farming",
        "coordination",
        "fleet",
        "sensor",
        "monitoring",
        "safety",
        "emergency",
        "collision",
        "boundary",
        "planting",
        "harvesting",
        "cultivation",
        "precision",
        "autonomous",
    }

    def __init__(self) -> None:
        """Initialize commit separation validator."""
        self.commit_msg_file = Path(".git/COMMIT_EDITMSG")

    def get_commit_message(self) -> str:
        """Get the commit message from git.

        Returns:
            The commit message content.

        Raises:
            CommitSeparationError: If commit message cannot be retrieved.
        """
        if self.commit_msg_file.exists():
            try:
                return self.commit_msg_file.read_text(encoding="utf-8").strip()
            except OSError as e:
                raise CommitSeparationError(f"Failed to read commit message: {e}") from e

        # Fallback to git command
        try:
            result = subprocess.run(
                ["git", "log", "-1", "--pretty=format:%B"],
                capture_output=True,
                text=True,
                check=True,
            )
            return result.stdout.strip()
        except subprocess.SubprocessError as e:
            raise CommitSeparationError(f"Failed to get commit message from git: {e}") from e

    def parse_commit_message(self, message: str) -> tuple[str, str, str, str]:
        """Parse commit message into components.

        Args:
            message: The commit message to parse.

        Returns:
            Tuple of (type, scope, description, body).

        Raises:
            CommitSeparationError: If message format is invalid.
        """
        lines = message.split("\n", 1)
        subject = lines[0].strip()
        body = lines[1].strip() if len(lines) > 1 else ""

        # Match conventional commit format: type(scope): description
        pattern = r"^(\w+)(?:\(([^)]+)\))?: (.+)$"
        match = re.match(pattern, subject)

        if not match:
            raise CommitSeparationError(
                f"Invalid commit message format. Expected: type(scope): description\n"
                f"Got: {subject}\n\n"
                f"Examples:\n"
                f"- feat(equipment): add multi-tractor synchronization capability\n"
                f"- fix(safety): ensure emergency stop triggers across all tractors\n"
                f"- docs(api): update equipment endpoint examples"
            )

        commit_type = match.group(1).lower()
        scope = match.group(2) if match.group(2) else ""
        description = match.group(3)

        return commit_type, scope, description, body

    def validate_commit_type(self, commit_type: str) -> None:
        """Validate commit type is recognized.

        Args:
            commit_type: The commit type to validate.

        Raises:
            CommitSeparationError: If commit type is invalid.
        """
        if commit_type not in self.VALID_TYPES:
            valid_types = ", ".join(sorted(self.VALID_TYPES.keys()))
            examples = []
            for _type_name, config in list(self.VALID_TYPES.items())[:3]:
                examples.extend(config["examples"][:2])  # type: ignore[index]

            raise CommitSeparationError(
                f"Invalid commit type '{commit_type}'. Must be one of: {valid_types}\n\n"
                f"Examples:\n" + "\n".join(f"- {ex}" for ex in examples)
            )

    def validate_scope(self, scope: str) -> None:
        """Validate commit scope is appropriate.

        Args:
            scope: The commit scope to validate.

        Raises:
            CommitSeparationError: If scope is invalid or missing.
        """
        if not scope:
            raise CommitSeparationError(
                "Commit scope is required for separation of concerns.\n"
                "Scope should indicate the area of the codebase affected.\n\n"
                f"Valid scopes: {', '.join(sorted(self.VALID_SCOPES))}"
            )

        if scope not in self.VALID_SCOPES:
            valid_scopes = ", ".join(sorted(self.VALID_SCOPES))
            raise CommitSeparationError(
                f"Invalid scope '{scope}'. Must be one of: {valid_scopes}\n\n"
                f"Scope should clearly indicate the area of the codebase affected."
            )

    def validate_description(self, description: str, commit_type: str) -> None:
        """Validate commit description quality and content.

        Args:
            description: The commit description to validate.
            commit_type: The commit type for context.

        Raises:
            CommitSeparationError: If description is inadequate.
        """
        if len(description) < 10:
            raise CommitSeparationError(
                f"Commit description too short: '{description}'\n"
                f"Description should clearly explain what was changed and why."
            )

        if len(description) > 72:
            raise CommitSeparationError(
                f"Commit description too long ({len(description)} chars, max 72):\n"
                f"'{description}'\n"
                f"Keep subject line concise, use body for details."
            )

        # Check for proper verb tense (imperative mood)
        if description[0].islower():
            raise CommitSeparationError(
                f"Commit description should start with capital letter: '{description}'"
            )

        # Check for agricultural context in relevant commits
        type_config = self.VALID_TYPES[commit_type]
        if type_config.get("requires_agricultural_context", False):
            description_lower = description.lower()
            has_agricultural_context = any(
                keyword in description_lower for keyword in self.AGRICULTURAL_KEYWORDS
            )

            if not has_agricultural_context:
                agricultural_keywords = ", ".join(sorted(self.AGRICULTURAL_KEYWORDS))
                raise CommitSeparationError(
                    f"Commit type '{commit_type}' requires agricultural context in description.\n"
                    f"Consider including terms like: {agricultural_keywords[:100]}..."
                )

    def validate_separation_of_concerns(self, message: str, commit_type: str) -> None:
        """Validate that commit addresses single concern.

        Args:
            message: Full commit message.
            commit_type: The commit type.

        Raises:
            CommitSeparationError: If multiple concerns detected.
        """
        # Look for multiple concern indicators
        concern_indicators = {
            "and also",
            "additionally",
            "furthermore",
            "moreover",
            "as well as",
            "plus",
            "along with",
            "in addition",
        }

        message_lower = message.lower()
        multiple_concerns = [
            indicator for indicator in concern_indicators if indicator in message_lower
        ]

        if multiple_concerns:
            raise CommitSeparationError(
                f"Commit appears to address multiple concerns.\n"
                f"Found indicators: {', '.join(multiple_concerns)}\n\n"
                f"Each commit should address exactly one concern.\n"
                f"Consider splitting into separate commits."
            )

        # Check for mixed types in description
        other_types = [t for t in self.VALID_TYPES.keys() if t != commit_type]
        description_lower = message.lower()

        mixed_type_words = []
        for other_type in other_types:
            if other_type in description_lower:
                # Avoid false positives for common words
                if other_type not in ["test", "fix"] or f"{other_type} " in description_lower:
                    mixed_type_words.append(other_type)

        if mixed_type_words:
            raise CommitSeparationError(
                f"Commit description mentions other concern types: {', '.join(mixed_type_words)}\n"
                f"Each commit should focus on a single concern type: {commit_type}\n"
                f"Consider splitting into separate commits for each concern."
            )

    def validate_commit_message(self, message: str) -> None:
        """Validate complete commit message for separation of concerns.

        Args:
            message: The commit message to validate.

        Raises:
            CommitSeparationError: If validation fails.
        """
        # Parse message components
        commit_type, scope, description, body = self.parse_commit_message(message)

        # Validate each component
        self.validate_commit_type(commit_type)
        self.validate_scope(scope)
        self.validate_description(description, commit_type)
        self.validate_separation_of_concerns(message, commit_type)

        print(f"✅ Commit separation validation passed: {commit_type}({scope})")

    def validate_current_commit(self) -> None:
        """Validate the current commit being made.

        Raises:
            CommitSeparationError: If validation fails.
        """
        message = self.get_commit_message()
        self.validate_commit_message(message)


def main() -> int:
    """Main entry point for commit separation enforcement hook.

    Returns:
        Exit code (0 for success, 1 for failure).
    """
    try:
        print("🔍 Validating commit separation of concerns...")

        validator = CommitSeparationValidator()
        validator.validate_current_commit()

        print("✅ Commit separation of concerns validation completed successfully")
        return 0

    except CommitSeparationError as e:
        print("❌ Commit Separation Violation:")
        print(f"{e}")
        print()
        print("📋 Commit Separation Requirements:")
        print("- Each commit must address exactly one concern")
        print("- Use conventional commit format: type(scope): description")
        print("- Include agricultural context for relevant changes")
        print("- Keep descriptions concise and clear")
        print()
        print("📖 See GIT_COMMIT_SEPARATION_MANDATORY.md for complete guidelines")
        return 1

    except Exception as e:
        print(f"❌ Unexpected error during commit separation validation: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
