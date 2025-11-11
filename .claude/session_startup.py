#!/usr/bin/env python3
"""
Session startup script that enforces todowrite_cli usage and token optimization.
Runs automatically at session start to ensure proper workflow compliance.
"""

import json
import subprocess
import sys
from datetime import datetime
from pathlib import Path


def check_todowrite_cli_available():
    """Check if todowrite_cli is available in the current environment."""
    try:
        result = subprocess.run(
            ["python", "-m", "todowrite_cli", "--help"],
            capture_output=True,
            text=True,
            timeout=10,
            check=False,
        )
        return result.returncode == 0
    except (subprocess.TimeoutExpired, FileNotFoundError):
        return False


def setup_todowrite_environment():
    """Set up environment variables for todowrite_cli."""
    import os

    env_vars = {
        "PYTHONPATH": "lib_package/src:cli_package/src",
        "TODOWRITE_DATABASE_URL": "sqlite:///development_todowrite.db",
    }

    for key, value in env_vars.items():
        if key not in os.environ or not os.environ.get(key):
            print(f"Note: {key} should be set to {value}")
            # Note: In a real implementation, these would be set in the shell environment


def verify_token_optimization():
    """Verify that token optimization is properly configured."""
    config_path = Path.home() / ".claude" / "config.json"

    if not config_path.exists():
        print("❌ config.json not found")
        return False

    try:
        with open(config_path) as f:
            config = json.load(f)

        token_opt = config.get("token_optimization", {})
        if not token_opt.get("enabled", False):
            print("❌ Token optimization not enabled")
            return False

        print("✓ Token optimization is enabled")
        print(f"  - HAL preprocessing: {token_opt.get('hal_preprocessing', False)}")
        print(f"  - Cache enabled: {token_opt.get('cache_enabled', False)}")
        print(f"  - Max context chars: {token_opt.get('max_context_chars', 'N/A')}")

        return True

    except json.JSONDecodeError:
        print("❌ config.json is malformed")
        return False


def create_workflow_markers():
    """Create workflow enforcement markers for the current session."""
    session_dir = Path.cwd() / ".claude"
    session_dir.mkdir(exist_ok=True)

    workflow_file = session_dir / "workflow_active.json"
    workflow_data = {
        "session_start": datetime.now().isoformat(),
        "todowrite_cli_enforced": True,
        "token_optimization_active": True,
        "episodic_memory_available": True,
        "workflow_version": "1.0",
    }

    with open(workflow_file, "w") as f:
        json.dump(workflow_data, f, indent=2)

    print("✓ Workflow enforcement markers created")


def main():
    """Main startup logic."""
    print("🚀 Starting session with enforced todowrite_cli workflow...")

    # Check todowrite_cli availability
    if not check_todowrite_cli_available():
        print("⚠️  todowrite_cli not available - make sure PYTHONPATH is set correctly")
        print('   export PYTHONPATH="lib_package/src:cli_package/src"')
        sys.exit(1)

    print("✓ todowrite_cli is available")

    # Verify token optimization
    if not verify_token_optimization():
        print("⚠️  Token optimization issues detected - check config.json")
        sys.exit(1)

    # Create workflow markers
    create_workflow_markers()

    # Set up environment
    setup_todowrite_environment()

    print("\n📋 Session Requirements:")
    print("  1. ALL planning must use todowrite_cli")
    print("  2. Check episodic memory before starting work")
    print("  3. Token optimization is active")
    print("  4. Document decisions in todowrite tasks")

    print("\n✅ Session ready - enforced workflow active!")

    return 0


if __name__ == "__main__":
    sys.exit(main())
