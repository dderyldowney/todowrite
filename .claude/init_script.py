#!/usr/bin/env python3
"""
Claude Code Auto-Initialization Script

This script ensures that the session startup process is automatically
loaded by Claude Code CLI at the beginning of every session.

This file should be referenced in Claude Code's configuration to
automatically load the session startup environment.
"""

import sys
import os
from pathlib import Path

# Get the directory containing this script
claude_dir = Path(__file__).parent

# Import and run the session startup
try:
    session_startup_path = claude_dir / "session_startup.py"
    if session_startup_path.exists():
        # Add the current directory to Python path
        sys.path.insert(0, str(claude_dir))

        # Import and execute session startup
        import session_startup

        # Call the main function if it exists
        if hasattr(session_startup, 'main'):
            session_startup.main()

    else:
        print(f"⚠️ Session startup script not found: {session_startup_path}")

except Exception as e:
    print(f"❌ Error loading session startup: {e}")
    print("⚠️ Continuing with limited session initialization")