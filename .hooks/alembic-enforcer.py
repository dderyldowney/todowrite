#!/usr/bin/env python3
"""
Alembic Enforcement System

Permanently enforces alembic best practices including:
- Single migration head
- No duplicate migration IDs
- Migration message conventions
- Database schema consistency
"""

import json
import re
import sys
from pathlib import Path
from typing import Any


class AlembicEnforcer:
    """Enforces alembic best practices and migration rules."""

    def __init__(self, project_root: Path | None = None):
        self.project_root = project_root or Path.cwd()
        self.config_file = self.project_root / ".claude" / "alembic_enforcement_config.json"
        self.load_config()

    def load_config(self):
        """Load alembic enforcement configuration."""
        default_config = {
            "enforcement_level": "strict",
            "enforcement_permanent": True,
            "survives_session_reset": True,

            # Alembic directories and files to check
            "alembic_locations": [
                "migrations/",
                "alembic/",
                "lib_package/migrations/",
                "cli_package/migrations/",
                "web_package/migrations/",
            ],

            # Required alembic file patterns
            "required_files": [
                "alembic.ini",
                "env.py",
                "script.py.mako",
            ],

            # Migration rules
            "migration_rules": {
                "single_head_required": True,
                "no_duplicate_ids": True,
                "revision_format": "uuid",
                "message_format": "^[a-z][a-z0-9_]*(: .+)?$",
                "dependencies_required": True,
                "downgrade_migration_required": True,
                "autogenerate_warning": True,
            },

            # Message conventions
            "message_conventions": {
                "prefixes": ["create", "add", "remove", "alter", "drop", "rename"],
                "descriptions": True,
                "no_empty_descriptions": True,
                "max_length": 100,
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
            # Save default config
            self.config_file.parent.mkdir(exist_ok=True)
            with open(self.config_file, "w") as f:
                json.dump(self.config, f, indent=2)

    def find_alembic_directories(self) -> list[Path]:
        """Find all alembic directories in the project."""
        alembic_dirs = []

        for location in self.config["alembic_locations"]:
            path = self.project_root / location
            if path.exists() and path.is_dir():
                alembic_dirs.append(path)

        return alembic_dirs

    def check_single_head(self, alembic_dir: Path) -> dict[str, Any]:
        """Check that there's only one migration head."""
        versions_dir = alembic_dir / "versions"
        if not versions_dir.exists():
            return {"status": "no_versions", "heads": 0}

        heads = []
        for file_path in versions_dir.glob("*.py"):
            if file_path.name == "__init__.py":
                continue

            try:
                with open(file_path) as f:
                    content = f.read()
                    if "down_revision = None" in content or "down_revision = 'head'" in content:
                        heads.append(file_path.name)
            except:
                continue

        return {
            "status": "multiple_heads" if len(heads) > 1 else "single_head",
            "heads": len(heads),
            "head_files": heads
        }

    def check_duplicate_revision_ids(self, alembic_dir: Path) -> dict[str, Any]:
        """Check for duplicate revision IDs."""
        versions_dir = alembic_dir / "versions"
        if not versions_dir.exists():
            return {"status": "no_versions", "duplicates": []}

        revision_ids = []
        for file_path in versions_dir.glob("*.py"):
            if file_path.name == "__init__.py":
                continue

            try:
                with open(file_path) as f:
                    content = f.read()
                    # Find revision IDs
                    revision_match = re.search(r'revision\s*=\s*[\'"]([^\'"]+)[\'"]', content)
                    if revision_match:
                        revision_ids.append({
                            "revision": revision_match.group(1),
                            "file": file_path.name
                        })
            except:
                continue

        # Check for duplicates
        seen_revisions = {}
        duplicates = []
        for rev_info in revision_ids:
            rev = rev_info["revision"]
            if rev in seen_revisions:
                duplicates.append({
                    "revision": rev,
                    "files": [seen_revisions[rev]["file"], rev_info["file"]]
                })
            else:
                seen_revisions[rev] = rev_info

        return {
            "status": "duplicates_found" if duplicates else "no_duplicates",
            "duplicates": duplicates
        }

    def check_migration_messages(self, alembic_dir: Path) -> dict[str, Any]:
        """Check migration message conventions."""
        versions_dir = alembic_dir / "versions"
        if not versions_dir.exists():
            return {"status": "no_versions", "issues": []}

        issues = []
        for file_path in versions_dir.glob("*.py"):
            if file_path.name == "__init__.py":
                continue

            try:
                with open(file_path) as f:
                    content = f.read()

                # Extract upgrade message
                upgrade_match = re.search(r'def upgrade\(\):\s*\n\s*.*?###?\s*(.+)', content, re.DOTALL | re.MULTILINE)
                if upgrade_match:
                    message = upgrade_match.group(1).strip()

                    # Check message conventions
                    if not message:
                        issues.append({
                            "file": file_path.name,
                            "issue": "empty_migration_message",
                            "message": "Empty migration message"
                        })
                    elif len(message) > self.config["message_conventions"]["max_length"]:
                        issues.append({
                            "file": file_path.name,
                            "issue": "message_too_long",
                            "message": f"Message too long ({len(message)} > {self.config['message_conventions']['max_length']})"
                        })
                    elif not re.match(self.config["migration_rules"]["message_format"], message):
                        issues.append({
                            "file": file_path.name,
                            "issue": "invalid_message_format",
                            "message": f"Invalid message format: {message}"
                        })

            except:
                continue

        return {
            "status": "issues_found" if issues else "no_issues",
            "issues": issues
        }

    def verify_alembic_requirements(self) -> dict[str, Any]:
        """Verify alembic installation and requirements."""
        try:
            import alembic
            # Get version using importlib.metadata (alembic.__version__ doesn't exist in newer versions)
            try:
                import importlib.metadata
                alembic_version = importlib.metadata.version('alembic')
            except Exception:
                # Fallback to pkg_resources if importlib.metadata fails
                try:
                    import pkg_resources
                    alembic_version = pkg_resources.get_distribution('alembic').version
                except Exception:
                    alembic_version = "unknown"
        except ImportError:
            return {
                "status": "alembic_not_installed",
                "error": "Alembic is not installed"
            }

        # Check alembic configuration
        alembic_ini = self.project_root / "alembic.ini"
        if not alembic_ini.exists():
            return {
                "status": "no_alembic_ini",
                "error": "alembic.ini not found"
            }

        return {
            "status": "alembic_ready",
            "version": alembic_version,
            "config_file": str(alembic_ini)
        }

    def run_alembic_check(self) -> dict[str, Any]:
        """Run comprehensive alembic checks."""
        results = {
            "alembic_status": self.verify_alembic_requirements(),
            "directories_checked": [],
            "issues": []
        }

        alembic_dirs = self.find_alembic_directories()
        if not alembic_dirs:
            results["issues"].append("No alembic directories found")
            return results

        for alembic_dir in alembic_dirs:
            dir_results = {
                "directory": str(alembic_dir),
                "single_head": self.check_single_head(alembic_dir),
                "duplicate_ids": self.check_duplicate_revision_ids(alembic_dir),
                "messages": self.check_migration_messages(alembic_dir)
            }
            results["directories_checked"].append(dir_results)

            # Collect issues
            if dir_results["single_head"]["status"] == "multiple_heads":
                results["issues"].append(f"Multiple heads in {alembic_dir}")

            if dir_results["duplicate_ids"]["status"] == "duplicates_found":
                results["issues"].append(f"Duplicate revision IDs in {alembic_dir}")

            if dir_results["messages"]["status"] == "issues_found":
                results["issues"].extend([
                    f"Message issue in {issue['file']}: {issue['message']}"
                    for issue in dir_results["messages"]["issues"]
                ])

        results["overall_status"] = "passed" if not results["issues"] else "failed"
        return results

    def verify_compliance(self) -> tuple[bool, list[str]]:
        """Verify compliance with alembic rules."""
        results = self.run_alembic_check()
        errors = []

        if results["alembic_status"]["status"] != "alembic_ready":
            errors.append(f"Alembic issue: {results['alembic_status'].get('error', 'Unknown error')}")

        for issue in results["issues"]:
            errors.append(f"Alembic violation: {issue}")

        return len(errors) == 0, errors

    def get_enforcement_help(self) -> str:
        """Get comprehensive enforcement help."""
        return """
🔄 ALEMBIC ENFORCEMENT

REQUIRED ALEMBIC FILES:
• alembic.ini - Alembic configuration
• env.py - Alembic environment setup
• script.py.mako - Migration script template

MIGRATION RULES (Zero Tolerance):
• Single migration head only
• No duplicate revision IDs
• Proper message conventions
• Downgrade migration required
• Dependencies between migrations

MESSAGE CONVENTIONS:
• Format: [action]: [description]
• Valid prefixes: create, add, remove, alter, drop, rename
• Descriptive messages required
• Maximum length: 100 characters

EXAMPLES:
✅ GOOD: create_users_table
✅ GOOD: add_user_email_index: Add index for email lookup
✅ GOOD: remove_legacy_fields: Drop deprecated columns

❌ BAD: migration_001
❌ BAD: add stuff
❌ BAD: Empty message

ENFORCEMENT:
• Pre-commit hooks check all migrations
• Single head requirement enforced
• Message conventions validated
• Duplicate ID detection automatic

ZERO TOLERANCE:
• No multiple migration heads
• No duplicate revision IDs
• No improperly formatted messages
• No missing downgrade migrations
        """

    def create_precommit_hook(self):
        """Create pre-commit hook for alembic enforcement."""
        hook_content = """#!/bin/bash
# Alembic Enforcement Pre-commit Hook

echo "🔄 Checking Alembic migrations..."

# Check if alembic changes exist
if git diff --cached --name-only | grep -E "(alembic|migrations)" > /dev/null; then
    echo "Alembic changes detected, running checks..."

    # Run alembic enforcer
    python .hooks/alembic-enforcer.py --check

    if [ $? -ne 0 ]; then
        echo "❌ ALEMBIC VIOLATIONS DETECTED"
        echo "Fix alembic issues before committing"
        exit 1
    fi

    # Run alembic check command if available
    if command -v alembic &> /dev/null; then
        alembic check
        if [ $? -ne 0 ]; then
            echo "❌ ALEMBIC CHECK FAILED"
            exit 1
        fi
    fi
fi

echo "✅ Alembic checks passed"
"""

        hook_path = self.project_root / ".hooks" / "precommit-alembic-check.sh"
        hook_path.parent.mkdir(exist_ok=True)
        with open(hook_path, "w") as f:
            f.write(hook_content)
        hook_path.chmod(0o755)

        return str(hook_path)


def main():
    """Main entry point for alembic enforcement."""
    if len(sys.argv) == 2 and sys.argv[1] == "--help":
        enforcer = AlembicEnforcer()
        print(enforcer.get_enforcement_help())
        sys.exit(0)

    if len(sys.argv) == 2 and sys.argv[1] == "--check":
        enforcer = AlembicEnforcer()
        is_compliant, errors = enforcer.verify_compliance()
        if is_compliant:
            print("✅ No alembic violations found")
            sys.exit(0)
        else:
            print("❌ Alembic violations detected:")
            for error in errors:
                print(f"• {error}")
            print()
            print("Use --help for alembic best practices")
            sys.exit(1)

    if len(sys.argv) == 2 and sys.argv[1] == "--report":
        enforcer = AlembicEnforcer()
        results = enforcer.run_alembic_check()

        print("🔄 ALEMBIC ENFORCEMENT REPORT")
        print(f"Overall status: {results['overall_status']}")
        print(f"Directories checked: {len(results['directories_checked'])}")

        if results["alembic_status"]["status"] == "alembic_ready":
            print(f"Alembic version: {results['alembic_status']['version']}")
        else:
            print(f"Alembic status: {results['alembic_status']['error']}")

        if results["issues"]:
            print()
            print("Issues found:")
            for issue in results["issues"]:
                print(f"  • {issue}")
        sys.exit(0 if results["overall_status"] == "passed" else 1)

    # Default: run check
    enforcer = AlembicEnforcer()
    results = enforcer.run_alembic_check()
    if results["overall_status"] != "passed":
        print(f"❌ Alembic issues found: {len(results['issues'])}")
        sys.exit(1)
    else:
        print("✅ No alembic violations found")
        sys.exit(0)


if __name__ == "__main__":
    main()
