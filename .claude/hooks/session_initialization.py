#!/usr/bin/env python3
"""
Session initialization hook for agricultural robotics development.

Manages session markers and agent registry for coordinated
multi-agent development sessions with ISO compliance tracking.
"""

import json
from datetime import datetime, timedelta
from pathlib import Path


def get_session_root():
    """Get the session root directory."""
    return Path.cwd()


def create_session_markers():
    """Create session markers for new session detection."""
    session_root = get_session_root()
    session_dir = session_root / ".claude"
    session_dir.mkdir(exist_ok=True)

    # Create session start marker
    start_marker = session_dir / "session_start.json"
    session_data = {
        "start_time": datetime.now().isoformat(),
        "agent": "claude-code",
        "session_type": "development",
    }

    with open(start_marker, "w") as f:
        json.dump(session_data, f, indent=2)

    # Create session heartbeat marker
    heartbeat_marker = session_dir / "session_heartbeat.json"
    heartbeat_data = {
        "last_heartbeat": datetime.now().isoformat(),
        "agent": "claude-code",
        "status": "active",
    }

    with open(heartbeat_marker, "w") as f:
        json.dump(heartbeat_data, f, indent=2)


def check_session_freshness():
    """Check if session markers are fresh (within 5 minutes)."""
    session_root = get_session_root()
    session_dir = session_root / ".claude"

    heartbeat_marker = session_dir / "session_heartbeat.json"

    if not heartbeat_marker.exists():
        return False

    try:
        with open(heartbeat_marker) as f:
            heartbeat_data = json.load(f)

        last_heartbeat = datetime.fromisoformat(heartbeat_data["last_heartbeat"])
        time_diff = datetime.now() - last_heartbeat

        return time_diff < timedelta(minutes=5)

    except (json.JSONDecodeError, KeyError, ValueError):
        return False


def update_heartbeat():
    """Update the session heartbeat."""
    session_root = get_session_root()
    session_dir = session_root / ".claude"
    heartbeat_marker = session_dir / "session_heartbeat.json"

    heartbeat_data = {
        "last_heartbeat": datetime.now().isoformat(),
        "agent": "claude-code",
        "status": "active",
    }

    with open(heartbeat_marker, "w") as f:
        json.dump(heartbeat_data, f, indent=2)


def register_agent():
    """Register agent in the agent registry."""
    session_root = get_session_root()
    session_dir = session_root / ".claude"
    registry_file = session_dir / "agent_registry.json"

    registry = {}
    if registry_file.exists():
        try:
            with open(registry_file) as f:
                registry = json.load(f)
        except json.JSONDecodeError:
            registry = {}

    registry["claude-code"] = {
        "last_seen": datetime.now().isoformat(),
        "agent_type": "development",
        "capabilities": ["code-generation", "test-fixing", "documentation"],
        "workflow_enforcement": {
            "requires_todowrite_cli": True,
            "planning_required": True,
            "token_optimization": True,
        },
    }

    with open(registry_file, "w") as f:
        json.dump(registry, f, indent=2)


def enforce_todowrite_cli_workflow():
    """Enforce todowrite_cli usage for all planning and implementation."""
    session_root = get_session_root()
    session_dir = session_root / ".claude"
    workflow_file = session_dir / "workflow_enforcement.json"

    workflow_config = {
        "todowrite_cli_required": True,
        "planning_steps": [
            "Use todowrite_cli to create tasks for all work",
            "Check episodic memory for past context",
            "Plan implementation using todowrite_cli",
            "Execute work with todowrite_cli tracking",
        ],
        "enforcement_time": datetime.now().isoformat(),
        "token_optimization_active": True,
    }

    with open(workflow_file, "w") as f:
        json.dump(workflow_config, f, indent=2)

    print("✓ todowrite_cli workflow enforcement activated")
    return True


def main():
    """Main session initialization logic."""
    if check_session_freshness():
        update_heartbeat()
        print("Session active - heartbeat updated")
        enforce_todowrite_cli_workflow()
        return 0
    create_session_markers()
    register_agent()
    enforce_todowrite_cli_workflow()
    print("New session initialized with todowrite_cli workflow enforcement")
    return 0


if __name__ == "__main__":
    import sys

    sys.exit(main())
