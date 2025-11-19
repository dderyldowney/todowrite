#!/usr/bin/env python3
"""
Test Artifact Cleanup Enforcement

Permanently enforces cleanup of test artifacts and ensures
no test-generated files remain after sessions or commits.
"""

import json
import sys
from pathlib import Path


class TestCleanupEnforcer:
    """Enforces test artifact cleanup across all sessions."""

    def __init__(self, project_root: Path | None = None):
        self.project_root = project_root or Path.cwd()
        self.config_file = self.project_root / ".claude" / "test_cleanup_config.json"
        self.load_config()

    def load_config(self):
        """Load test cleanup configuration."""
        default_config = {
            "enforcement_level": "strict",
            "cleanup_permanent": True,
            "survives_session_reset": True,
            "forbidden_artifacts": [
                "tests/todowrite_testing.db",
                "todowrite_*_testing.db",
                "todowrite_*_development.db",
                "commit-msgs.txt",
                "test_*.db",
                "*_test.db",
                "pytest_*.db",
                "coverage_*.db",
                "*.test.db",
                "commit-msgs*.txt",
                "test_results_*.txt",
                "pytest_results_*.txt",
                "test_output_*.txt",
                "test_report_*.txt",
                "test_coverage_*.txt",
            ],
            "forbidden_directories": [
                "test_artifacts",
                "pytest_cache",
                "test_results",
                "test_reports",
                "test_outputs",
            ],
            "allowed_patterns": [
                ".git/",
                "__pycache__/",
                ".pytest_cache/",
                ".venv/",
                "venv/",
                "htmlcov/",
                ".coverage",
                "coverage.xml",
            ],
            "cleanup_commands": [
                "find . -name 'tests/todowrite_testing.db' -delete 2>/dev/null || true",
                "find . -name 'todowrite_*_testing.db' -delete 2>/dev/null || true",
                "find . -name 'todowrite_*_development.db' -delete 2>/dev/null || true",
                "find . -name 'commit-msgs.txt' -delete 2>/dev/null || true",
                "find . -name '*.db' -not -path './.git/*' -not -path './.venv/*' -not -path './venv/*' -delete 2>/dev/null || true",
                "find . -name 'commit-msgs*.txt' -not -path './.git/*' -delete 2>/dev/null || true",
                "find . -name 'test_artifacts*' -delete 2>/dev/null || true",
                "find . -name 'test_results*' -delete 2>/dev/null || true",
            ],
            "verification_patterns": [
                "tests_todowrite.db",
                "commit-msgs.txt",
                "test_artifacts",
                "test_results",
            ],
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
            # Save default config
            self.config_file.parent.mkdir(exist_ok=True)
            with open(self.config_file, "w") as f:
                json.dump(self.config, f, indent=2)

    def scan_for_forbidden_artifacts(self) -> dict:
        """Scan for forbidden test artifacts."""
        findings = {"files": [], "directories": [], "total_count": 0, "critical_violations": []}

        # Scan for forbidden files
        for pattern in self.config["forbidden_artifacts"]:
            try:
                matches = list(self.project_root.rglob(pattern))
                for match in matches:
                    if self._should_check_file(match):
                        findings["files"].append(
                            {
                                "path": str(match),
                                "size": match.stat().st_size if match.exists() else 0,
                                "modified": match.stat().st_mtime if match.exists() else 0,
                                "pattern": pattern,
                            }
                        )
                        findings["total_count"] += 1

                        # Check for critical violations
                        if any(
                            critical in match.name.lower()
                            for critical in ["tests_todowrite.db", "commit-msgs.txt"]
                        ):
                            findings["critical_violations"].append(str(match))
            except Exception:
                continue

        # Scan for forbidden directories
        for pattern in self.config["forbidden_directories"]:
            try:
                matches = list(self.project_root.rglob(pattern))
                for match in matches:
                    if match.is_dir() and self._should_check_file(match):
                        findings["directories"].append({"path": str(match), "pattern": pattern})
                        findings["total_count"] += 1
            except Exception:
                continue

        return findings

    def _should_check_file(self, file_path: Path) -> bool:
        """Check if file should be included in scan."""
        file_str = str(file_path)

        # Skip allowed patterns
        for allowed_pattern in self.config["allowed_patterns"]:
            if allowed_pattern in file_str:
                return False

        # Skip git and virtual environment directories
        if any(skip in file_str for skip in [".git/", "__pycache__/", ".venv/", "venv/"]):
            return False

        # Skip if file doesn't exist
        return file_path.exists()

    def enforce_cleanup(self, force: bool = False) -> dict:
        """Enforce test artifact cleanup."""
        findings = self.scan_for_forbidden_artifacts()

        results = {
            "scanned": True,
            "artifacts_found": findings["total_count"],
            "critical_violations": len(findings["critical_violations"]),
            "cleanup_performed": False,
            "cleanup_success": False,
            "errors": [],
        }

        if findings["total_count"] == 0:
            results["cleanup_success"] = True
            return results

        # Perform cleanup if forced or if critical violations exist
        if force or findings["critical_violations"]:
            results["cleanup_performed"] = True
            cleanup_success = True

            # Run cleanup commands
            for command in self.config["cleanup_commands"]:
                try:
                    import subprocess

                    result = subprocess.run(
                        command, shell=True, cwd=self.project_root, capture_output=True, text=True
                    )
                    if result.returncode != 0:
                        results["errors"].append(f"Command failed: {command}")
                        cleanup_success = False
                except Exception as e:
                    results["errors"].append(f"Cleanup error: {e}")
                    cleanup_success = False

            results["cleanup_success"] = cleanup_success

        return results

    def verify_compliance(self) -> tuple[bool, list[str]]:
        """Verify compliance with test cleanup rules."""
        findings = self.scan_for_forbidden_artifacts()
        errors = []

        if findings["total_count"] > 0:
            errors.append(f"Found {findings['total_count']} forbidden test artifacts")

        if findings["critical_violations"]:
            errors.append(
                f"CRITICAL: Found {len(findings['critical_violations'])} critical violations:"
            )
            for violation in findings["critical_violations"]:
                errors.append(f"  - {violation}")

        if findings["files"]:
            errors.append("Forbidden files found:")
            for file_info in findings["files"][:5]:  # Show first 5
                errors.append(f"  - {file_info['path']} ({file_info['size']} bytes)")

        if findings["directories"]:
            errors.append("Forbidden directories found:")
            for dir_info in findings["directories"]:
                errors.append(f"  - {dir_info['path']}")

        return len(errors) == 0, errors

    def get_cleanup_help(self) -> str:
        """Get comprehensive cleanup help."""
        return """
🧹 TEST ARTIFACT CLEANUP ENFORCEMENT

FORBIDDEN ARTIFACTS (Must be removed):
• tests_todowrite.db - Test database files
• commit-msgs.txt - Commit message test files
• test_*.db - Any test database files
• *_test.db - Database files ending with _test
• commit-msgs*.txt - Any commit message test files
• test_artifacts/ - Test artifact directories
• test_results/ - Test result directories

MANDATORY CLEANUP:
Before any commit or session end:
1. Remove all test databases and files
2. Clean up test artifacts directories
3. Remove temporary test output files
4. Verify no test-generated files remain

VERIFICATION COMMANDS:
• Find test databases: find . -name '*.db' -not -path './.git/*'
• Find commit messages: find . -name 'commit-msgs*.txt'
• Verify cleanup: python .hooks/test-cleanup-enforcer.py --check

ZERO TOLERANCE:
• No test artifacts may remain after commits
• No temporary test files in repository
• All test-generated content must be cleaned up
• Violations block commits and fail quality gates

AUTOMATIC CLEANUP:
• Pre-commit hooks automatically clean artifacts
• Session initialization enforces cleanup
• Manual cleanup: python .hooks/test-cleanup-enforcer.py --cleanup
        """

    def create_precommit_cleanup_hook(self):
        """Create a pre-commit cleanup action."""
        cleanup_content = """#!/bin/bash
# Test Artifact Cleanup Pre-commit Hook
# Automatically cleans test artifacts before commits

echo "🧹 Cleaning test artifacts before commit..."

# Remove common test artifacts
find . -name 'tests_todowrite.db' -delete 2>/dev/null || true
find . -name 'commit-msgs.txt' -delete 2>/dev/null || true
find . -name '*.db' -not -path './.git/*' -not -path './.venv/*' -not -path './venv/*' -delete 2>/dev/null || true
find . -name 'commit-msgs*.txt' -not -path './.git/*' -delete 2>/dev/null || true
find . -name 'test_artifacts*' -delete 2>/dev/null || true

# Verify no artifacts remain
if find . -name 'tests_todowrite.db' -not -path './.git/*' | head -1 | grep -q .; then
    echo "❌ ERROR: test artifacts still present after cleanup"
    exit 1
fi

if find . -name 'commit-msgs.txt' -not -path './.git/*' | head -1 | grep -q .; then
    echo "❌ ERROR: commit message artifacts still present after cleanup"
    exit 1
fi

echo "✅ Test artifacts cleaned successfully"
"""

        hook_path = self.project_root / ".hooks" / "precommit-cleanup.sh"
        hook_path.parent.mkdir(exist_ok=True)
        with open(hook_path, "w") as f:
            f.write(cleanup_content)
        hook_path.chmod(0o755)

        return str(hook_path)


def main():
    """Main entry point for test cleanup enforcement."""
    if len(sys.argv) == 2 and sys.argv[1] == "--help":
        enforcer = TestCleanupEnforcer()
        print(enforcer.get_cleanup_help())
        sys.exit(0)

    if len(sys.argv) == 2 and sys.argv[1] == "--check":
        enforcer = TestCleanupEnforcer()
        is_compliant, errors = enforcer.verify_compliance()
        if is_compliant:
            print("✅ Test artifact cleanup compliance verified")
            sys.exit(0)
        else:
            print("❌ Test artifact cleanup violations found:")
            for error in errors:
                print(f"• {error}")
            print()
            print(enforcer.get_cleanup_help())
            sys.exit(1)

    if len(sys.argv) == 2 and sys.argv[1] == "--cleanup":
        enforcer = TestCleanupEnforcer()
        results = enforcer.enforce_cleanup(force=True)
        if results["cleanup_success"]:
            print("✅ Test artifacts cleaned successfully")
            print(f"   Removed {results['artifacts_found']} artifacts")
            sys.exit(0)
        else:
            print("❌ Test artifact cleanup failed")
            if results["errors"]:
                for error in results["errors"]:
                    print(f"   {error}")
            sys.exit(1)

    if len(sys.argv) == 2 and sys.argv[1] == "--create-hook":
        enforcer = TestCleanupEnforcer()
        hook_path = enforcer.create_precommit_cleanup_hook()
        print(f"✅ Pre-commit cleanup hook created: {hook_path}")
        sys.exit(0)

    # Default: check compliance
    enforcer = TestCleanupEnforcer()
    is_compliant, errors = enforcer.verify_compliance()
    if not is_compliant:
        print(f"❌ Test artifact cleanup violations found: {len(errors)}")
        print("Run with --cleanup to remove artifacts or --help for more information")
        sys.exit(1)
    else:
        print("✅ No test artifacts found")
        sys.exit(0)


if __name__ == "__main__":
    main()
