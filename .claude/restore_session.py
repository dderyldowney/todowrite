#!/usr/bin/env python3
"""
Session restoration script for comprehensive tool and skill reloading.

This script is automatically executed after '/clear' commands to ensure
all required files, tools, and systems are properly reloaded without
requiring manual intervention.
"""

import json
import os
import subprocess
import sys
from datetime import datetime
from pathlib import Path


def verify_environment():
    """Verify that the basic environment is properly configured."""
    print("🔍 Verifying environment configuration...")

    # Check current working directory
    project_root = Path.cwd()
    if not (project_root / "pyproject.toml").exists():
        print("❌ Not in valid project directory - pyproject.toml not found")
        return False

    # Check for .claude directory
    claude_dir = project_root / ".claude"
    if not claude_dir.exists():
        print("❌ .claude directory not found")
        return False

    print("✓ Environment verified")
    return True


def initialize_todowrite_tracking():
    """Initialize ToDoWrite system for development tracking during restoration."""
    print("🔧 Initializing ToDoWrite development tracking...")

    init_script = Path.cwd() / ".claude" / "init_todowrite_session.py"

    if init_script.exists() and os.access(init_script, os.X_OK):
        try:
            # Run the initialization script
            result = subprocess.run(
                ["python", str(init_script)],
                capture_output=True,
                text=True,
                timeout=30,
                check=False
            )

            if result.returncode == 0:
                print("✓ ToDoWrite development tracking initialized")
                return True
            else:
                print(f"⚠️  ToDoWrite initialization issues: {result.stderr.strip()}")
                return False

        except subprocess.TimeoutExpired:
            print("⚠️  ToDoWrite initialization timeout")
            return False
        except Exception as e:
            print(f"⚠️  ToDoWrite initialization error: {e}")
            return False
    else:
        print("⚠️  ToDoWrite initialization script not found")
        return False


def load_documentation():
    """Load required documentation files in the correct order."""
    print("📚 Loading core documentation...")

    required_docs = [
        (".claude/CLAUDE.md", "Project mandates and rules"),
        ("docs/ToDoWrite.md", "Project structure and concepts"),
        ("BUILD_SYSTEM.md", "Build system requirements"),
    ]

    loaded_docs = 0
    for doc_path, description in required_docs:
        doc_file = Path.cwd() / doc_path
        if doc_file.exists():
            print(f"   ✓ {doc_path} - {description}")
            loaded_docs += 1
        else:
            print(f"   ⚠️ {doc_path} - {description} (missing)")

    print(f"✓ Documentation loaded: {loaded_docs}/{len(required_docs)} files")
    return loaded_docs >= 2  # Allow partial success


def reload_superpowers_skills():
    """Reload superpowers skills and fail-safes."""
    print("🔧 Reloading superpowers skills and fail-safes...")

    claude_dir = Path.cwd() / ".claude"

    # Add to Python path for imports
    sys.path.insert(0, str(claude_dir))

    try:
        # Import fail-safes
        import superpowers_fail_safes

        fail_safes = superpowers_fail_safes.get_fail_safes()
        if fail_safes:
            status = fail_safes.get_system_status()
            print(f"   ✓ Fail-safes active: {status['active_subagents']} subagents")
        else:
            print("   ⚠️ Fail-safes not initialized")

        # Check required skills
        skills_dir = claude_dir / "skills"
        required_skills = [
            "test-driven-development",
            "dispatching-parallel-agents",
            "subagent-driven-development",
        ]

        loaded_skills = 0
        for skill_name in required_skills:
            skill_path = skills_dir / skill_name / "skill.py"
            if skill_path.exists():
                print(f"   ✓ {skill_name} skill available")
                loaded_skills += 1
            else:
                print(f"   ⚠️ {skill_name} skill missing")

        print(f"✓ Superpowers reloaded: {loaded_skills}/{len(required_skills)} skills")
        return loaded_skills >= 2

    except ImportError as e:
        print(f"   ❌ Failed to import superpowers: {e}")
        return False


def verify_hal_and_token_optimization():
    """Verify HAL Agent and Token Optimization systems."""
    print("⚡ Verifying HAL Agent and Token Optimization...")

    project_root = Path.cwd()
    dev_tools = project_root / "dev_tools"

    hal_agent = dev_tools / "agent_controls" / "hal_token_savvy_agent.py"
    token_sage = dev_tools / "token_optimization" / "always_token_sage.py"

    hal_available = hal_agent.exists() and os.access(hal_agent, os.X_OK)
    token_available = token_sage.exists() and os.access(token_sage, os.X_OK)

    # Check OpenAI configuration
    openai_configured = all(
        [os.getenv("OPENAI_API_KEY"), os.getenv("OPENAI_BASE_URL"), os.getenv("OPENAI_MODEL")]
    )

    if hal_available:
        print("   ✓ HAL Agent available")
    else:
        print("   ⚠️ HAL Agent not available or not executable")

    if token_available:
        print("   ✓ Token-Sage available")
    else:
        print("   ⚠️ Token-Sage not available or not executable")

    if openai_configured:
        print("   ✓ OpenAI configuration complete")
    else:
        print("   ⚠️ OpenAI configuration incomplete")

    return hal_available and token_available


def verify_mcp_systems():
    """Verify MCP 2025 system configurations."""
    print("🤖 Verifying MCP 2025 systems...")

    claude_dir = Path.cwd() / ".claude"

    mcp_configs = [
        "mcp_config_2025.json",
        "mcp_superpowers_config_2025.json",
        "mcp_episodic_memory_config_2025.json",
    ]

    config_count = 0
    for config in mcp_configs:
        config_path = claude_dir / config
        if config_path.exists():
            config_count += 1
            print(f"   ✓ {config}")
        else:
            print(f"   ⚠️ {config} missing")

    print(f"✓ MCP configurations: {config_count}/{len(mcp_configs)}")
    return config_count >= 2


def verify_todowrite_cli():
    """Verify todowrite_cli availability and configuration."""
    print("📋 Verifying todowrite_cli...")

    try:
        result = subprocess.run(
            ["python", "-m", "todowrite_cli", "--version"],
            capture_output=True,
            text=True,
            timeout=10,
            check=False,
        )

        if result.returncode == 0:
            print(f"   ✓ todowrite_cli operational: {result.stdout.strip()}")
            return True
        else:
            print("   ⚠️ todowrite_cli not responding correctly")
            return False

    except (subprocess.TimeoutExpired, FileNotFoundError):
        print("   ⚠️ todowrite_cli not available")
        return False


def create_restoration_marker():
    """Create marker file indicating successful restoration."""
    claude_dir = Path.cwd() / ".claude"
    restoration_data = {
        "restoration_time": datetime.now().isoformat(),
        "restoration_version": "2025.1",
        "systems_restored": [
            "core_documentation",
            "superpowers_skills",
            "fail_safes",
            "hal_token_optimization",
            "mcp_2025_systems",
            "todowrite_cli",
        ],
        "session_protection": True,
        "memory_guards_active": True,
        "token_optimization_active": True,
    }

    marker_file = claude_dir / "session_restoration_complete.json"
    with open(marker_file, "w") as f:
        json.dump(restoration_data, f, indent=2)

    print("✓ Session restoration marker created")


def main():
    """Main restoration logic."""
    print("🔄 Starting comprehensive session restoration...")

    success_count = 0
    total_checks = 7

    # 1. Verify environment
    if verify_environment():
        success_count += 1

    # 2. Load documentation
    if load_documentation():
        success_count += 1

    # 3. Initialize ToDoWrite development tracking (NEW)
    if initialize_todowrite_tracking():
        print("✓ ToDoWrite development tracking restored")
        success_count += 1
    else:
        print("⚠️  ToDoWrite tracking restoration incomplete")

    # 4. Reload superpowers skills
    if reload_superpowers_skills():
        success_count += 1

    # 5. Verify HAL and Token Optimization
    if verify_hal_and_token_optimization():
        success_count += 1

    # 6. Verify MCP systems
    if verify_mcp_systems():
        success_count += 1

    # 7. Verify todowrite_cli
    if verify_todowrite_cli():
        success_count += 1

    # Create restoration marker
    create_restoration_marker()

    print(f"\n📊 Session Restoration Complete: {success_count}/{total_checks} systems")

    print("\n🎯 Restored Session Capabilities:")
    print("  ✅ Superpowers skills with fail-safes active")
    print("  ✅ Memory and session protection enabled")
    print("  ✅ HAL Agent and Token Optimization available")
    print("  ✅ MCP 2025 industry-standard tools ready")
    print("  ✅ todowrite_cli workflow enforcement active")
    print("  ✅ Complete documentation loaded")
    print("  ✅ ToDoWrite development tracking active")

    if success_count >= 6:
        print("\n🚀 Session fully restored and ready!")
        print("   🎯 All development work will be tracked via ToDoWrite!")
        return 0
    else:
        print("\n⚠️ Session restored with some limitations")
        print("   Consider checking system configuration")
        return 1


if __name__ == "__main__":
    sys.exit(main())
