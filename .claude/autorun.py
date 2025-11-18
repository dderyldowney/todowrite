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


def load_superpowers_skills():
    """Load and initialize superpowers skills with fail-safes."""
    project_root = Path.cwd()
    claude_dir = project_root / ".claude"

    # Check for superpowers directory
    superpowers_dir = claude_dir / "skills"
    if not superpowers_dir.exists():
        print("🔧 Creating superpowers skills directory...")
        superpowers_dir.mkdir(parents=True, exist_ok=True)

    # Check for required skills
    required_skills = [
        "test-driven-development",
        "dispatching-parallel-agents",
        "subagent-driven-development"
    ]

    missing_skills = []
    for skill_name in required_skills:
        skill_dir = superpowers_dir / skill_name
        if not skill_dir.exists():
            missing_skills.append(skill_name)

    if missing_skills:
        print(f"⚠️  Missing superpowers skills: {', '.join(missing_skills)}")
        print("   Skills will be created when needed")
    else:
        print("✅ All required superpowers skills available")

    # Initialize fail-safes
    fail_safes_file = claude_dir / "superpowers_fail_safes.py"
    if not fail_safes_file.exists():
        print("⚠️  Superpowers fail-safes not found")
        return False

    # Add fail-safes to Python path
    sys.path.insert(0, str(claude_dir))

    try:
        import superpowers_fail_safes
        print("✅ Superpowers fail-safes loaded")

        # Initialize fail-safes instance
        fail_safes = superpowers_fail_safes.get_fail_safes()
        if fail_safes:
            status = fail_safes.get_system_status()
            print(f"   Active subagents: {status['active_subagents']}")
            print(f" Memory usage: {status['total_memory_used_mb']:.1f}MB")

        return True
    except ImportError as e:
        print(f"❌ Failed to load superpowers fail-safes: {e}")
        return False


def initialize_mcp_system():
    """Initialize MCP (Model Context Protocol) system."""
    project_root = Path.cwd()
    claude_dir = project_root / ".claude"

    # Check MCP configuration
    mcp_configs = [
        "mcp_config_2025.json",
        "mcp_superpowers_config_2025.json",
        "mcp_episodic_memory_config_2025.json"
    ]

    missing_configs = []
    for config in mcp_configs:
        config_path = claude_dir / config
        if not config_path.exists():
            missing_configs.append(config)

    if missing_configs:
        print(f"⚠️  Missing MCP configurations: {', '.join(missing_configs)}")
        return False

    print("✅ MCP 2025 configurations loaded")

    # Check for MCP tools
    mcp_tools = [
        "mcp_security_optimizer.py",
        "mcp_monitoring_dashboard.py",
        "setup_mcp_2025.sh"
    ]

    for tool in mcp_tools:
        tool_path = claude_dir / tool
        if tool_path.exists() and os.access(tool_path, os.X_OK):
            print(f"✅ MCP tool available: {tool}")

    # Initialize episodic memory
    init_mcp_script = claude_dir / "init_mcp.sh"
    if init_mcp_script.exists() and os.access(init_mcp_script, os.X_OK):
        print("✅ MCP initialization script available")

    return True


def main():
    """Auto-run activation at session start."""
    print("🔧 Loading comprehensive session configuration...")

    success_count = 0
    total_checks = 3

    # 1. Activate permanent enforcement
    if activate_permanent_enforcement():
        success_count += 1
        print("✅ Permanent enforcement activated")

    # 2. Load superpowers skills and fail-safes
    if load_superpowers_skills():
        success_count += 1
        print("✅ Superpowers skills and fail-safes loaded")

    # 3. Initialize MCP system
    if initialize_mcp_system():
        success_count += 1
        print("✅ MCP 2025 system initialized")

    # Check enforcement status
    if success_count >= 2:
        print(f"\n🚀 Session configuration complete ({success_count}/{total_checks})")
        check_enforcement_status()
        return 0
    else:
        print(f"\n⚠️  Session configuration incomplete ({success_count}/{total_checks})")
        return 1


if __name__ == "__main__":
    sys.exit(main())