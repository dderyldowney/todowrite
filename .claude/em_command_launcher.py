#!/usr/bin/env python3
"""
Episodic Memory Command Launcher
Project-specific command execution without polluting regular environment
"""

import argparse
import os
import subprocess
import sys
from pathlib import Path

# Add project root to Python path for this session only
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))


def setup_environment():
    """Setup project-specific environment without polluting system"""
    # Set PYTHONPATH for this session
    python_path = f"{PROJECT_ROOT}/lib_package/src:{PROJECT_ROOT}/cli_package/src"

    # Environment variables for this session
    env = os.environ.copy()
    env["PYTHONPATH"] = python_path
    env["EPISODIC_MEMORY_DB_PATH"] = (
        "postgresql://mcp_user:mcp_secure_password_2024@localhost:5433/mcp_tools"
    )

    return env


def execute_episodic_command(command_type, query=None, limit=10):
    """Execute episodic memory commands without polluting environment"""
    env = setup_environment()

    # Path to episodic memory script
    episodic_script = PROJECT_ROOT / ".claude" / "episodic_memory.py"

    if not episodic_script.exists():
        return f"❌ Episodic memory script not found: {episodic_script}"

    try:
        # Activate virtual environment and run command
        venv_python = PROJECT_ROOT / ".venv" / "bin" / "python"
        if not venv_python.exists():
            return f"❌ Virtual environment not found: {venv_python}"

        cmd = [str(venv_python), str(episodic_script)]

        if command_type == "stats":
            cmd.append("--stats")
        elif command_type == "index":
            cmd.append("--index")
        elif command_type == "search":
            cmd.extend(["--search", query])
            cmd.extend(["--limit", str(limit)])
        else:
            return f"❌ Unknown command type: {command_type}"

        # Execute the command
        result = subprocess.run(cmd, capture_output=True, text=True, env=env, cwd=PROJECT_ROOT)

        if result.returncode == 0:
            return result.stdout
        else:
            return f"❌ Command failed: {result.stderr}"

    except Exception as e:
        return f"❌ Error executing command: {e}"


def main():
    """Command line interface for the launcher"""
    parser = argparse.ArgumentParser(description="Episodic Memory Command Launcher")
    parser.add_argument("command", choices=["stats", "index", "search"], help="Command to execute")
    parser.add_argument("query", nargs="?", help="Search query (for search command)")
    parser.add_argument("--limit", type=int, default=10, help="Result limit (for search command)")

    args = parser.parse_args()

    if args.command == "search" and not args.query:
        print("❌ Search command requires a query")
        sys.exit(1)

    result = execute_episodic_command(args.command, args.query, args.limit)
    print(result)


if __name__ == "__main__":
    main()
