#!/usr/bin/env python3
"""
Universal Automatic Session Initialization Hook for AFS FastAPI

This hook ensures that 'loadsession' is automatically executed for ALL agents
and objects created by the '/new' command, providing immediate project context
restoration with persistent cross-session behavior.

UNIVERSAL AGENT INITIALIZATION:
- Executes loadsession on first tool use in any new session or agent
- Maintains project context continuity across ALL development cycles
- Preserves enterprise-grade standards and strategic direction
- Enables sophisticated agricultural robotics development from session start
- Ensures ALL agents (main, subagents, specialized agents) have context access

PERSISTENT SESSION MANAGEMENT:
- Cross-session state persistence using multiple marker strategies
- Agent-aware initialization tracking
- Robust session detection across different Claude Code invocation patterns
- Universal access guarantee for all agent types

Agricultural Context:
- Critical for safety-critical multi-tractor coordination systems
- Maintains ISO 18497 and ISO 11783 compliance context
- Preserves Test-First Development methodology enforcement
- Ensures synchronization infrastructure development continuity
- Supports distributed agent coordination for agricultural robotics
"""

import json
import os
import subprocess
import sys
import time
import uuid
from pathlib import Path


class UniversalSessionInitializationHook:
    """
    Universal Automatic Session Initialization for AFS FastAPI Platform

    Ensures immediate loadsession execution for ALL Claude Code sessions and agents,
    maintaining enterprise-grade development context and strategic priorities across
    ALL agent types with persistent cross-session behavior.

    UNIVERSAL AGENT SUPPORT:
    - Main Claude Code sessions
    - Subagents (Task tool spawned agents)
    - Specialized agents (general-purpose, statusline-setup, output-style-setup)
    - Cross-session persistence with multiple detection strategies
    """

    def __init__(self):
        self.project_root = Path.cwd()

        # Multi-layered session detection for robust persistence
        self.session_marker = self.project_root / ".claude" / ".session_initialized"
        self.agent_registry = self.project_root / ".claude" / ".agent_registry.json"
        self.global_session_marker = self.project_root / ".claude" / ".global_session_state"

        # Universal loadsession access
        self.loadsession_script = self.project_root / "loadsession"

        # Agent identification for tracking
        self.current_agent_id = self._generate_agent_id()
        self.session_timestamp = time.time()

    def _generate_agent_id(self) -> str:
        """Generate unique agent identifier for tracking."""
        return f"agent_{uuid.uuid4().hex[:8]}_{int(time.time())}"

    def _load_agent_registry(self) -> dict:
        """Load agent registry for cross-agent tracking."""
        if self.agent_registry.exists():
            try:
                with open(self.agent_registry) as f:
                    return json.load(f)
            except (OSError, json.JSONDecodeError):
                return {}
        return {}

    def _save_agent_registry(self, registry: dict) -> None:
        """Save agent registry for persistent tracking."""
        self.agent_registry.parent.mkdir(parents=True, exist_ok=True)
        try:
            with open(self.agent_registry, "w") as f:
                json.dump(registry, f, indent=2)
        except OSError:
            pass  # Graceful failure for registry operations

    def _register_agent_initialization(self) -> None:
        """Register current agent as initialized."""
        registry = self._load_agent_registry()
        registry[self.current_agent_id] = {
            "initialized_at": self.session_timestamp,
            "project_root": str(self.project_root),
            "loadsession_executed": True,
        }
        self._save_agent_registry(registry)

    def is_new_session(self) -> bool:
        """Check if this is a new session requiring initialization.

        Uses multiple detection strategies for robust session identification:
        1. Primary session marker (per-session)
        2. Global session state (cross-session persistence)
        3. Agent registry (multi-agent tracking)
        """
        # Strategy 1: Check primary session marker
        if not self.session_marker.exists():
            return True

        # Strategy 2: Check global session state for persistence
        if not self.global_session_marker.exists():
            return True

        # Strategy 3: Check agent registry for cross-agent initialization
        registry = self._load_agent_registry()
        if not registry:  # Empty registry indicates fresh start
            return True

        # Verify recent agent activity (within last 24 hours)
        current_time = time.time()
        recent_agents = [
            agent_id
            for agent_id, data in registry.items()
            if current_time - data.get("initialized_at", 0) < 86400  # 24 hours
        ]

        # If no recent agents, treat as new session
        return len(recent_agents) == 0

    def mark_session_initialized(self) -> None:
        """Mark current session as initialized with multi-layered persistence."""
        # Ensure .claude directory exists
        self.session_marker.parent.mkdir(parents=True, exist_ok=True)

        # Strategy 1: Create primary session marker
        self.session_marker.touch()

        # Strategy 2: Create global session state for cross-session persistence
        self.global_session_marker.touch()

        # Strategy 3: Register agent in persistent registry
        self._register_agent_initialization()

        # Create universal access marker for all agent types
        universal_marker = self.project_root / ".claude" / ".universal_access_enabled"
        universal_marker.touch()

    def execute_loadsession(self) -> bool:
        """Execute loadsession command for context restoration."""
        try:
            if not self.loadsession_script.exists():
                print(
                    f"⚠️  loadsession script not found at {self.loadsession_script}", file=sys.stderr
                )
                return False

            # Execute loadsession with proper agricultural context and agent awareness
            result = subprocess.run(
                [str(self.loadsession_script)],
                cwd=self.project_root,
                capture_output=True,
                text=True,
                timeout=45,  # Extended timeout for agent operations
                env={**os.environ, "CLAUDE_AGENT_ID": self.current_agent_id},
            )

            if result.returncode == 0:
                print(
                    f"🚀 AFS FastAPI Session Context Automatically Loaded (Agent: {self.current_agent_id[:12]})",
                    file=sys.stderr,
                )
                print("✅ Enterprise platform ready for sophisticated development", file=sys.stderr)
                print(
                    "🤖 Universal agent access enabled for all Claude Code operations",
                    file=sys.stderr,
                )
                return True
            else:
                print(f"❌ loadsession execution failed: {result.stderr}", file=sys.stderr)
                return False

        except subprocess.TimeoutExpired:
            print("❌ loadsession execution timed out", file=sys.stderr)
            return False
        except Exception as e:
            print(f"❌ loadsession execution error: {e}", file=sys.stderr)
            return False

    def run_session_initialization(self) -> None:
        """Run automatic session initialization if needed."""
        if self.is_new_session():
            print("🔄 New session detected - Auto-executing loadsession...", file=sys.stderr)

            if self.execute_loadsession():
                self.mark_session_initialized()
                print("✨ Session initialization complete - Ready for development", file=sys.stderr)
            else:
                print(
                    "⚠️  Session initialization failed - Manual loadsession recommended",
                    file=sys.stderr,
                )


def main():
    """
    Main hook execution for automatic session initialization.

    This hook runs before any tool execution and ensures loadsession
    is automatically called for new Claude Code sessions.
    """
    try:
        # Read hook input data (not used but required for hook interface)
        _ = json.loads(sys.stdin.read())

        # Initialize universal session hook
        session_hook = UniversalSessionInitializationHook()

        # Run automatic session initialization
        session_hook.run_session_initialization()

        # Continue with normal tool execution
        sys.exit(0)

    except Exception as e:
        print(f"Session initialization hook error: {e}", file=sys.stderr)
        # Don't block tool execution on hook errors
        sys.exit(0)


if __name__ == "__main__":
    main()
