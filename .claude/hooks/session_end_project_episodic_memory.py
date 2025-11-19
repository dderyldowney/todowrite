#!/usr/bin/env python3
"""Project-Scoped Episodic Memory Session End Hook"""

import os
import subprocess
import sys
from pathlib import Path

def main():
    """Index current project conversations at session end"""

    project_root = Path(__file__).parent.parent
    script_path = project_root / "dev_tools" / "project_episodic_memory.sh"

    if script_path.exists():
        # Set environment variable for project-specific database
        episodic_db = project_root / ".claude" / "episodic_memory.db"
        os.environ["EPISODIC_MEMORY_DB_PATH"] = str(episodic_db)

        # Run project-specific indexing
        try:
            result = subprocess.run(
                [str(script_path), "index"],
                capture_output=True,
                text=True,
                timeout=300
            )
            if result.returncode == 0:
                print("✅ Project episodic memory indexed successfully")
            else:
                print(f"⚠️  Episodic memory indexing issue: {result.stderr}")
        except subprocess.TimeoutExpired:
            print("⏳ Episodic memory indexing timed down...")
        except Exception as e:
            print(f"⚠️  Episodic memory error: {e}")

if __name__ == "__main__":
    main()
