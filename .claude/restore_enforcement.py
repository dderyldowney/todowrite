#!/usr/bin/env python3
"""Post-clear restoration script for ToDoWrite enforcement systems.

This script restores full enforcement functionality after a /clear command.
Run this manually if you notice missing enforcement after /clear.
"""

import subprocess  # nosec B404
import sys
from pathlib import Path


def run_script(script_path: str, description: str) -> bool:
    """Run a script and report success/failure."""
    script_file = Path(script_path)
    if not script_file.exists():
        print(f"❌ {description} - Script not found: {script_path}")
        return False

    try:
        result = subprocess.run(  # nosec B603, B607
            ["python", str(script_file)], capture_output=True, text=True, cwd=Path.cwd()
        )

        if result.returncode == 0:
            print(f"✅ {description}")
            if result.stdout.strip():
                print(f"   {result.stdout.strip()}")
            return True
        else:
            print(f"❌ {description} - Failed")
            if result.stderr.strip():
                print(f"   Error: {result.stderr.strip()}")
            return False

    except Exception as e:
        print(f"❌ {description} - Exception: {e}")
        return False


def main():
    """Restore full enforcement after /clear."""
    print("🔄 Restoring ToDoWrite enforcement systems after /clear...")
    print()

    success_count = 0
    total_scripts = 3

    # 1. Session initialization
    if run_script(".claude/hooks/session_initialization.py", "Session initialization"):
        success_count += 1

    # 2. Permanent enforcement activation
    if run_script(".claude/autorun.py", "Permanent enforcement activation"):
        success_count += 1

    # 3. Episodic memory initialization
    if run_script(
        ".claude/hooks/session_startup_episodic_memory.py", "Episodic memory initialization"
    ):
        success_count += 1

    print()
    if success_count == total_scripts:
        print("🚀 All enforcement systems restored successfully!")
        print("✅ Full ToDoWrite compliance is now active")
        return 0
    else:
        print(f"⚠️  Partial restoration: {success_count}/{total_scripts} systems active")
        print("🔧 You may need to manually run the failing components")
        return 1


if __name__ == "__main__":
    sys.exit(main())
