#!/usr/bin/env python3
"""Project-Scoped Episodic Memory Session Startup Hook"""

import os
import subprocess
import sys
from pathlib import Path

def main():
    """Initialize project-scoped episodic memory for this session"""

    project_root = Path(__file__).parent.parent
    episodic_db = project_root / ".claude" / "episodic_memory.db"

    # Set environment variable for project-specific database
    os.environ["EPISODIC_MEMORY_DB_PATH"] = str(episodic_db)

    print(f"🔍 Project-scoped episodic memory initialized")
    print(f"📁 Database: {episodic_db}")

    # Create project-specific episodic memory directory if needed
    episodic_db.parent.mkdir(parents=True, exist_ok=True)

if __name__ == "__main__":
    main()
