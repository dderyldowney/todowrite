#!/usr/bin/env python3
"""Session Startup Hook - Ensure Episodic Memory is Ready."""

import subprocess  # nosec B404
from pathlib import Path


def main():
    """Ensure episodic memory is ready for the session."""
    project_root = Path(__file__).parent.parent

    # Check if episodic memory plugin is installed
    plugins_file = Path.home() / ".claude" / "plugins" / "installed_plugins.json"
    if not plugins_file.exists():
        print("⚠️  No episodic memory plugin found")
        return

    # Run a quick index to ensure embedding model is loaded
    episodic_cli = (
        Path.home()
        / ".claude"
        / "plugins"
        / "cache"
        / "episodic-memory"
        / "cli"
        / "episodic-memory.js"
    )

    if episodic_cli.exists():
        try:
            # Run a quick index to load embedding model
            result = subprocess.run(  # nosec B603, B607
                ["node", str(episodic_cli), "stats"], capture_output=True, text=True, timeout=30
            )

            if result.returncode == 0:
                print("✅ Episodic memory ready - embedding model loaded")
            else:
                print("🔄 Initializing episodic memory indexing...")
                # Run background indexing if stats fail
                subprocess.Popen(  # nosec B603, B607
                    ["node", str(episodic_cli), "index", "--cleanup"],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                )

        except subprocess.TimeoutExpired:
            print("⏳ Episodic memory indexing in progress...")
        except Exception as e:
            print(f"⚠️  Episodic memory error: {e}")

    # Create a marker file to indicate episodic memory was initialized
    marker = project_root / ".claude" / "episodic_memory_ready.json"
    marker.write_text('{"status": "initialized", "timestamp": "' + str(Path().cwd()) + '"}')


if __name__ == "__main__":
    main()
