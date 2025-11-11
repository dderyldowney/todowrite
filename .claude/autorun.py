#!/usr/bin/env python3
"""
Auto-run script for permanent code quality enforcement.

This script is automatically executed by Claude at session startup
to ensure permanent enforcement is active even after /clear commands.
"""

import json
import os
import sys
from pathlib import Path


def activate_permanent_enforcement():
    """Activate permanent enforcement for current session."""
    project_root = Path.cwd()
    claude_dir = project_root / ".claude"

    # Check if permanent enforcement is configured
    enforcement_config = claude_dir / "permanent_code_quality_enforcement.json"
    if not enforcement_config.exists():
        return False

    try:
        with open(enforcement_config) as f:
            config = json.load(f)
    except:
        return False

    if not config.get("enforcement_permanent", False):
        return False

    # Set environment variables for current session
    env_overrides = config.get("environment_overrides", {})
    for key, value in env_overrides.items():
        os.environ[key] = str(value)

    # Load additional environment overrides from .env file
    env_file = claude_dir / "environment_overrides.env"
    if env_file.exists():
        with open(env_file) as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    # Handle both "export KEY=VALUE" and "KEY=VALUE" formats
                    if line.startswith('export '):
                        line = line[7:]  # Remove 'export '
                    key, value = line.split('=', 1)
                    os.environ[key] = value.strip()

    # Print activation message (only if not already active)
    if not os.environ.get("CLAUDE_PERMANENT_ENFORCEMENT_ACTIVE"):
        print("🔒 Permanent code quality enforcement activated")
        print("🚨 This enforcement persists across all sessions including /clear commands")
        print("📋 Required workflows: Semantic Scoping, Red-Green-Refactor, Token Optimization, Zero Mocking, Test Cleanup")
        print("🎯 Mandatory tools: Ruff (S-mode), Bandit, Detect-secrets, SQLFluff, Test Cleanup, Pre-commit hooks")
        print("⚠️  ABSOLUTE ZERO MOCKING POLICY ENFORCED")
        print("🧪 Test artifact cleanup automatically enforced")
        print("🔒 Security mode (ruff S rules + bandit) strictly enforced")

        # Mark as active for this session
        os.environ["CLAUDE_PERMANENT_ENFORCEMENT_ACTIVE"] = "1"

    return True


def check_enforcement_status():
    """Check current enforcement status and report compliance."""
    project_root = Path.cwd()
    claude_dir = project_root / ".claude"

    # Check for permanent enforcement marker
    marker_file = claude_dir / "permanent_enforcement_active"
    if not marker_file.exists():
        print("⚠️  Permanent enforcement not configured")
        return False

    # Check critical environment variables
    critical_vars = [
        "CLAUDE_ENFORCE_SEMANTIC_SCOPING",
        "CLAUDE_ENFORCE_RED_GREEN_REFACTOR",
        "CLAUDE_ENFORCE_TOKEN_OPTIMIZATION",
        "CLAUDE_ENFORCE_ZERO_MOCKING",
        "CLAUDE_ENFORCE_RUFF_STRICT",
        "CLAUDE_ENFORCE_BANDIT_SECURITY",
        "CLAUDE_ENFORCE_SECURITY_MODE",
        "CLAUDE_MANDATORY_REAL_IMPLEMENTATIONS",
        "CLAUDE_ENFORCE_TEST_CLEANUP",
        "CLAUDE_FORBID_TEST_ARTIFACTS",
        "CLAUDE_FORBID_HARDCODED_TMP",
        "CLAUDE_ENFORCE_SECURE_TEMPFILES",
        "CLAUDE_ENFORCE_ALEMBIC",
        "CLAUDE_ENFORCE_PYTHON_VERSION",
        "CLAUDE_REQUIRE_PY312"
    ]

    active_vars = [var for var in critical_vars if os.environ.get(var)]

    if len(active_vars) == len(critical_vars):
        print("✅ All permanent enforcement systems active")
        return True
    else:
        print(f"⚠️  {len(active_vars)}/{len(critical_vars)} enforcement systems active")
        return False


def main():
    """Auto-run activation at session start."""
    # Try to activate permanent enforcement
    if activate_permanent_enforcement():
        # Check and report status
        check_enforcement_status()
        return 0
    else:
        print("ℹ️  No permanent enforcement configuration found")
        return 1


if __name__ == "__main__":
    sys.exit(main())