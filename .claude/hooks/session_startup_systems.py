#!/usr/bin/env python3
"""
Session Startup Hook - Initializes all required systems for AI CLI.

This hook runs automatically when the AI CLI starts and ensures:
- CLAUDE.md rules are loaded and enforced
- HAL Agent System is ready
- Token Optimization System is active
- MCP Systems are initialized
- All environment variables are set
"""

import os
import sys
from pathlib import Path


def initialize_all_systems():
    """Initialize all required systems for AI CLI session."""
    print("🚀 Initializing AI CLI Systems...")

    # 1. Verify virtual environment
    if ".venv" not in sys.executable:
        print("❌ Virtual environment not active")
        return False

    # 2. Verify environment variables
    required_vars = ["TODOWRITE_DATABASE_URL", "PYTHONPATH"]
    for var in required_vars:
        if not os.environ.get(var):
            print(f"❌ Environment variable {var} not set")
            return False

    # 3. Verify CLAUDE.md rules
    startup_script = Path(".claude/startup_enforcement.py")
    if startup_script.exists():
        print("📋 Verifying CLAUDE.md rules...")
        result = os.system("python .claude/startup_enforcement.py")
        if result != 0:
            print("❌ CLAUDE.md rule enforcement failed")
            return False
    else:
        print("⚠️  CLAUDE.md enforcement script not found")

    # 4. Verify HAL Agent System
    hal_script = Path("dev_tools/agent_controls/hal_token_savvy_agent.py")
    if hal_script.exists():
        print("🤖 Verifying HAL Agent System...")
        try:
            import importlib.util

            openai_spec = importlib.util.find_spec("openai")
            if openai_spec is not None:
                result = os.system(
                    "python dev_tools/agent_controls/hal_token_savvy_agent.py --help > /dev/null 2>&1"
                )
                if result == 0:
                    print("✅ HAL Agent System ready")
                else:
                    print("⚠️  HAL Agent System test failed")
            else:
                print("⚠️  HAL Agent dependencies missing")
        except ImportError:
            print("⚠️  HAL Agent dependencies missing")
    else:
        print("⚠️  HAL Agent System not found")

    # 5. Verify Token Optimization System
    token_script = Path("dev_tools/token_optimization/always_token_sage.py")
    if token_script.exists():
        print("⚡ Verifying Token Optimization System...")
        result = os.system(
            'python dev_tools/token_optimization/always_token_sage.py "test" > /dev/null 2>&1'
        )
        if result == 0:
            print("✅ Token Optimization System ready")
        else:
            print("⚠️  Token Optimization System test failed")
    else:
        print("⚠️  Token Optimization System not found")

    # 6. Verify MCP Systems
    episodic_memory = Path(".claude/episodic_memory")
    episodic_db = Path(".claude/episodic_memory.db")
    plugins_dir = Path(".claude/plugins")

    if episodic_memory.exists() or episodic_db.exists():
        print("🧠 Episodic Memory MCP available")

    if plugins_dir.exists():
        plugin_count = len(list(plugins_dir.glob("*.py")))
        print(f"🔌 Found {plugin_count} MCP plugins")

    # 7. Check Anthropic configuration
    if os.environ.get("ANTHROPIC_API_KEY"):
        print("🔑 Anthropic API configuration ready")
    else:
        print("⚠️  Anthropic API key not set")

    print("✅ AI CLI Systems initialization complete")
    return True


if __name__ == "__main__":
    success = initialize_all_systems()
    sys.exit(0 if success else 1)
