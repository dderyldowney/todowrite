#!/usr/bin/env python3
"""
Semantic Scope Validator for ToDoWrite Project

Enforces semantic scoping rules for all git commits to ensure
consistent, project-specific commit message organization.
"""

import json
import re
import sys
from pathlib import Path


class SemanticScopeValidator:
    """Validates and enforces semantic scoping for git commits."""

    def __init__(self, project_root: Path | None = None):
        self.project_root = project_root or Path.cwd()
        self.config_file = self.project_root / ".claude" / "semantic_scoping_config.json"
        self.load_config()

    def load_config(self):
        """Load semantic scoping configuration."""
        default_config = {
            "enforcement_level": "moderate",  # Changed from strict
            "scope_required": False,  # Changed from True - make scope optional
            "case_sensitive": False,
            "semantic_scopes": {
                "lib": {
                    "description": "Core ToDoWrite library",
                    "patterns": ["lib_package/", "src/ToDoWrite/", "ToDoWrite/"],
                    "file_types": [".py"],
                    "enforce": True,
                },
                "cli": {
                    "description": "Command-line interface",
                    "patterns": ["cli_package/", "src/ToDoWrite_cli/", "ToDoWrite_cli/"],
                    "file_types": [".py", ".md"],
                    "enforce": True,
                },
                "web": {
                    "description": "Web interface",
                    "patterns": ["web_package/", "src/ToDoWrite_web/", "ToDoWrite_web/"],
                    "file_types": [".py", ".js", ".html", ".css", ".md"],
                    "enforce": True,
                },
                "tests": {
                    "description": "Test suite and testing infrastructure",
                    "patterns": ["tests/", "test_", "_test.py"],
                    "file_types": [".py"],
                    "enforce": True,
                },
                "docs": {
                    "description": "Documentation",
                    "patterns": ["docs/", "*.md", "README*", "CHANGELOG*"],
                    "file_types": [".md", ".rst", ".txt"],
                    "enforce": True,
                },
                "build": {
                    "description": "Build system and packaging",
                    "patterns": [
                        "pyproject.toml",
                        "setup.py",
                        "Makefile",
                        "Dockerfile",
                        "docker-compose*",
                        "build/",
                        "dist/",
                    ],
                    "file_types": [".toml", ".yaml", ".yml", ".json", ".dockerfile"],
                    "enforce": True,
                },
                "config": {
                    "description": "Configuration files and settings",
                    "patterns": [
                        ".pre-commit-config.yaml",
                        "commitlint.config.js",
                        ".env*",
                        "*.ini",
                        "*.cfg",
                        "config/",
                    ],
                    "file_types": [".yaml", ".yml", ".js", ".json", ".ini"],
                    "enforce": True,
                },
                "ci": {
                    "description": "Continuous integration and deployment",
                    "patterns": [".github/", ".gitlab-ci.yml", ".circleci/"],
                    "file_types": [".yml", ".yaml"],
                    "enforce": True,
                },
                "deps": {
                    "description": "Dependencies and requirements",
                    "patterns": ["requirements*", "poetry.lock", "Pipfile*"],
                    "file_types": [".txt", ".lock", ".toml"],
                    "enforce": True,
                },
            },
            "conventional_types": [
                "feat",
                "fix",
                "docs",
                "style",
                "refactor",
                "perf",
                "test",
                "build",
                "ci",
                "chore",
                "revert",
            ],
            "scope_mapping": {
                # Automatic scope detection based on file patterns
                "lib_package/": "lib",
                "src/ToDoWrite/": "lib",
                "cli_package/": "cli",
                "src/ToDoWrite_cli/": "cli",
                "web_package/": "web",
                "src/ToDoWrite_web/": "web",
                "tests/": "tests",
                "docs/": "docs",
                ".github/": "ci",
            },
            "scope_validators": {
                "type_pattern": r"^(feat|fix|docs|style|refactor|perf|test|build|ci|chore|revert)",
                "scope_pattern": r"^[a-z][a-z0-9_-]*$",  # scope naming convention
                "max_scope_length": 20,
                "min_subject_length": 5,  # Reduced from 10
                "max_subject_length": 100,  # Increased from 72 to follow Google/Angular practices
            },
        }

        if self.config_file.exists():
            try:
                with open(self.config_file) as f:
                    loaded_config = json.load(f)
                # Merge with defaults
                self.config = {**default_config, **loaded_config}
            except (OSError, json.JSONDecodeError):
                self.config = default_config
        else:
            self.config = default_config
            # Save default config for future use
            self.config_file.parent.mkdir(exist_ok=True)
            with open(self.config_file, "w") as f:
                json.dump(self.config, f, indent=2)

    def validate_commit_message(self, commit_message: str) -> tuple[bool, list[str]]:
        """
        Validate a commit message according to semantic scoping rules.

        Returns:
            Tuple of (is_valid, error_messages)
        """
        errors = []

        # Check basic conventional commit format
        conventional_pattern = r"^(?P<type>\w+)(?:\((?P<scope>[^)]+)\))?:\s+(?P<subject>.+)"
        match = re.match(conventional_pattern, commit_message.strip(), re.MULTILINE | re.DOTALL)

        if not match:
            errors.append(
                "Invalid commit format. Expected: <type>[scope]: <description>\n"
                "Examples: feat(lib): add new feature, fix(cli): resolve bug,\n"
                "docs(readme): update guide"
            )
            return False, errors

        commit_type = match.group("type")
        scope = match.group("scope")
        subject = match.group("subject")

        # Validate commit type
        if commit_type not in self.config["conventional_types"]:
            errors.append(
                f"Invalid commit type '{commit_type}'. "
                f"Allowed types: {', '.join(self.config['conventional_types'])}"
            )

        # Check if scope is required
        if self.config["scope_required"] and not scope:
            errors.append(
                "Scope is required for this project. "
                f"Allowed scopes: {', '.join(self.config['semantic_scopes'].keys())}"
            )

        # Validate scope if provided
        if scope:
            scope_lower = scope.lower() if not self.config["case_sensitive"] else scope

            if scope_lower not in self.config["semantic_scopes"]:
                errors.append(
                    f"Invalid scope '{scope}'. "
                    f"Allowed scopes: {', '.join(self.config['semantic_scopes'].keys())}"
                )
            else:
                # Check scope naming convention
                if not re.match(self.config["scope_validators"]["scope_pattern"], scope):
                    errors.append(
                        f"Invalid scope format '{scope}'. "
                        "Scopes should be lowercase, start with a letter,\n"
                        "and use only hyphens/underscores"
                    )

                # Check scope length
                if len(scope) > self.config["scope_validators"]["max_scope_length"]:
                    errors.append(
                        f"Scope '{scope}' too long ({len(scope)} chars). "
                        f"Maximum: {self.config['scope_validators']['max_scope_length']} chars"
                    )

        # Validate subject
        if len(subject) < self.config["scope_validators"]["min_subject_length"]:
            errors.append(
                f"Subject too short ({len(subject)} chars). "
                f"Minimum: {self.config['scope_validators']['min_subject_length']} chars"
            )

        if len(subject) > self.config["scope_validators"]["max_subject_length"]:
            errors.append(
                f"Subject too long ({len(subject)} chars). "
                f"Maximum: {self.config['scope_validators']['max_subject_length']} chars"
            )

        # Check subject doesn't end with period
        if subject.endswith("."):
            errors.append("Subject should not end with a period")

        # Check subject capitalization (first letter should be uppercase)
        if subject and not subject[0].isupper():
            errors.append("Subject should start with a capital letter")

        return len(errors) == 0, errors

    def suggest_scope_for_changes(self, changed_files: list[str]) -> str | None:
        """
        Suggest appropriate scope based on changed files.

        Returns:
            Suggested scope or None if no clear match
        """
        file_paths = [Path(f) for f in changed_files]

        scope_counts = {}
        for file_path in file_paths:
            for pattern, suggested_scope in self.config["scope_mapping"].items():
                if pattern.endswith("/"):
                    # Directory pattern
                    if any(str(file_path).startswith(pattern) for pattern in [pattern]):
                        scope_counts[suggested_scope] = scope_counts.get(suggested_scope, 0) + 1
                else:
                    # File pattern
                    if file_path.name == pattern or file_path.match(pattern):
                        scope_counts[suggested_scope] = scope_counts.get(suggested_scope, 0) + 1

        # Return scope with highest count
        if scope_counts:
            return max(scope_counts, key=scope_counts.get)
        return None

    def get_scope_help(self) -> str:
        """Generate help text for allowed scopes."""
        help_lines = ["\nAllowed scopes for this project:"]
        for scope, config in self.config["semantic_scopes"].items():
            status = "✓" if config.get("enforce", True) else "○"
            help_lines.append(f"  {status} {scope:<8} - {config['description']}")

        help_lines.append("\nExamples:")
        help_lines.extend(
            [
                "  feat(lib): add hierarchical task relationships",
                "  fix(cli): resolve authentication timeout",
                "  test(web): add comprehensive user interface coverage",
                "  docs(readme): update installation instructions",
                "  refactor(api): simplify database connection logic",
            ]
        )

        return "\n".join(help_lines)

    def enforce_for_agent(self, _agent_name: str = "unknown") -> bool:
        """
        Check if semantic scoping should be enforced for this agent.

        All agents are required to follow semantic scoping rules.
        """
        return True  # All agents must follow semantic scoping


def main():
    """Main entry point for the validator."""
    if len(sys.argv) != 2:
        print("Usage: python semantic-scope-validator.py <commit_message_file>")
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

    validator = SemanticScopeValidator()

    is_valid, errors = validator.validate_commit_message(commit_message)

    if not is_valid:
        print("❌ Semantic Scope Validation Failed")
        print("=" * 50)
        for error in errors:
            print(f"• {error}")

        print(validator.get_scope_help())
        sys.exit(1)
    else:
        print("✅ Semantic scope validation passed")
        sys.exit(0)


if __name__ == "__main__":
    main()
