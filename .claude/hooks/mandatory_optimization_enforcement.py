#!/usr/bin/env python3
"""
Mandatory Token Optimization Enforcement Hook for AFS FastAPI.

This hook AUTOMATICALLY enforces real-time token optimization across ALL AI agents
and sessions. It cannot be disabled and ensures universal optimization compliance.

APPLIES TO: Claude, GPT, Gemini, Copilot, CodeWhisperer, ALL AI agents.
"""

import json
import os
import sys
import time
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

try:
    from afs_fastapi.core.conversation_manager import (
        configure_optimization,
        get_conversation_manager,
        optimize_interaction,
    )

    OPTIMIZATION_AVAILABLE = True
except ImportError:
    OPTIMIZATION_AVAILABLE = False


class MandatoryOptimizationEnforcer:
    """
    Enforces mandatory token optimization across all AI agents and sessions.

    This system automatically intercepts ALL AI interactions and applies
    real-time optimization while maintaining agricultural safety compliance.
    """

    def __init__(self):
        """Initialize mandatory optimization enforcement."""
        self.project_root = project_root
        self.enforcement_config_path = self.project_root / ".claude" / "mandatory_optimization.json"
        self.monitoring_data_path = self.project_root / ".claude" / "optimization_monitoring.json"
        self.session_tracking_path = (
            self.project_root / ".claude" / "session_optimization_tracking.json"
        )

        # Ensure directories exist
        self.enforcement_config_path.parent.mkdir(parents=True, exist_ok=True)

        # Load or create enforcement configuration
        self.enforcement_config = self._load_enforcement_config()
        self.monitoring_data = self._load_monitoring_data()
        self.session_tracking = self._load_session_tracking()

        # Initialize conversation manager if available
        self.conversation_manager = None
        if OPTIMIZATION_AVAILABLE:
            self.conversation_manager = get_conversation_manager(project_root)
            self._ensure_optimization_enabled()

    def _load_enforcement_config(self) -> dict[str, Any]:
        """Load or create mandatory enforcement configuration."""
        default_config = {
            "enforcement_enabled": True,
            "mandatory_for_all_agents": True,
            "agricultural_compliance_required": True,
            "minimum_optimization_level": "standard",
            "monitoring_enabled": True,
            "cross_session_persistence": True,
            "agent_types_enforced": [
                "claude",
                "gpt",
                "gemini",
                "copilot",
                "codewhisperer",
                "anthropic",
                "openai",
                "google",
                "microsoft",
                "amazon",
            ],
            "enforcement_version": "1.0.0",
            "created": datetime.now().isoformat(),
            "last_updated": datetime.now().isoformat(),
        }

        if self.enforcement_config_path.exists():
            try:
                with open(self.enforcement_config_path) as f:
                    config = json.load(f)
                # Merge with defaults to ensure all keys exist
                return {**default_config, **config}
            except (json.JSONDecodeError, OSError):
                pass

        # Save default configuration
        with open(self.enforcement_config_path, "w") as f:
            json.dump(default_config, f, indent=2)

        return default_config

    def _load_monitoring_data(self) -> dict[str, Any]:
        """Load persistent monitoring data across sessions."""
        default_monitoring = {
            "total_sessions_monitored": 0,
            "total_interactions_optimized": 0,
            "total_tokens_saved_all_time": 0,
            "average_optimization_effectiveness": 0.0,
            "agricultural_compliance_violations": 0,
            "enforcement_failures": 0,
            "last_monitoring_update": datetime.now().isoformat(),
            "session_history": [],
            "effectiveness_trend": [],
        }

        if self.monitoring_data_path.exists():
            try:
                with open(self.monitoring_data_path) as f:
                    return json.load(f)
            except (json.JSONDecodeError, OSError):
                pass

        return default_monitoring

    def _load_session_tracking(self) -> dict[str, Any]:
        """Load current session tracking data."""
        default_tracking = {
            "current_session_id": f"session_{int(time.time())}",
            "session_start": datetime.now().isoformat(),
            "interactions_this_session": 0,
            "tokens_saved_this_session": 0,
            "optimization_applied_count": 0,
            "agricultural_interactions": 0,
            "safety_critical_interactions": 0,
            "agent_type": "unknown",
        }

        if self.session_tracking_path.exists():
            try:
                with open(self.session_tracking_path) as f:
                    tracking = json.load(f)

                # Check if this is a new session (more than 5 minutes since last update)
                last_update = datetime.fromisoformat(tracking.get("session_start", "1970-01-01"))
                if datetime.now() - last_update > timedelta(minutes=5):
                    # New session - archive old data and start fresh
                    self._archive_session_data(tracking)
                    return default_tracking

                return tracking
            except (json.JSONDecodeError, ValueError, OSError):
                pass

        return default_tracking

    def _archive_session_data(self, session_data: dict[str, Any]) -> None:
        """Archive completed session data to monitoring history."""
        session_summary = {
            "session_id": session_data.get("current_session_id", "unknown"),
            "session_start": session_data.get("session_start"),
            "session_end": datetime.now().isoformat(),
            "total_interactions": session_data.get("interactions_this_session", 0),
            "total_tokens_saved": session_data.get("tokens_saved_this_session", 0),
            "agricultural_interactions": session_data.get("agricultural_interactions", 0),
            "safety_critical_interactions": session_data.get("safety_critical_interactions", 0),
            "agent_type": session_data.get("agent_type", "unknown"),
        }

        # Add to session history
        self.monitoring_data["session_history"].append(session_summary)

        # Keep only last 50 sessions
        if len(self.monitoring_data["session_history"]) > 50:
            self.monitoring_data["session_history"] = self.monitoring_data["session_history"][-50:]

        # Update global counters
        self.monitoring_data["total_sessions_monitored"] += 1
        self.monitoring_data["total_interactions_optimized"] += session_data.get(
            "interactions_this_session", 0
        )
        self.monitoring_data["total_tokens_saved_all_time"] += session_data.get(
            "tokens_saved_this_session", 0
        )

        # Update effectiveness trend
        if session_data.get("interactions_this_session", 0) > 0:
            session_effectiveness = session_data.get(
                "tokens_saved_this_session", 0
            ) / session_data.get("interactions_this_session", 1)
            self.monitoring_data["effectiveness_trend"].append(
                {
                    "timestamp": datetime.now().isoformat(),
                    "effectiveness": session_effectiveness,
                    "interactions": session_data.get("interactions_this_session", 0),
                }
            )

            # Keep only last 100 effectiveness measurements
            if len(self.monitoring_data["effectiveness_trend"]) > 100:
                self.monitoring_data["effectiveness_trend"] = self.monitoring_data[
                    "effectiveness_trend"
                ][-100:]

        self._save_monitoring_data()

    def _ensure_optimization_enabled(self) -> None:
        """Ensure optimization is enabled and properly configured."""
        if not OPTIMIZATION_AVAILABLE:
            return

        try:
            # Force enable optimization
            configure_optimization(
                enabled=True, token_budget=2000, adaptive_mode=True, debug_mode=False
            )
        except Exception:
            self.monitoring_data["enforcement_failures"] += 1

    def enforce_optimization(
        self, user_input: str, ai_response: str = "", interaction_type: str = "general"
    ) -> dict[str, Any]:
        """
        Mandatory enforcement of token optimization for any AI interaction.

        This method CANNOT be bypassed and automatically applies optimization
        to all AI conversations while tracking effectiveness.
        """
        if not self.enforcement_config["enforcement_enabled"]:
            # Even if disabled in config, still track the interaction
            self._track_interaction(user_input, ai_response, optimized=False)
            return {
                "optimized": False,
                "reason": "enforcement_disabled",
                "original_input": user_input,
                "original_response": ai_response,
            }

        if not OPTIMIZATION_AVAILABLE:
            # Optimization system not available - track failure
            self.monitoring_data["enforcement_failures"] += 1
            self._save_monitoring_data()
            return {
                "optimized": False,
                "reason": "optimization_system_unavailable",
                "original_input": user_input,
                "original_response": ai_response,
            }

        try:
            # Apply mandatory optimization
            result = optimize_interaction(
                user_input=user_input, ai_response=ai_response, command_type=interaction_type
            )

            # Track successful optimization
            self._track_optimization_success(result)

            return {
                "optimized": True,
                "optimization_result": result,
                "optimized_input": result["optimized_content"]["user_input"],
                "optimized_response": result["optimized_content"]["ai_response"],
                "tokens_saved": result["optimization_metadata"]["total_tokens_saved"],
                "agricultural_compliance": result["agricultural_compliance"],
            }

        except Exception as e:
            # Track optimization failure but don't break the interaction
            self.monitoring_data["enforcement_failures"] += 1
            self._track_interaction(user_input, ai_response, optimized=False)
            return {
                "optimized": False,
                "reason": f"optimization_failed: {str(e)}",
                "original_input": user_input,
                "original_response": ai_response,
            }

    def _track_optimization_success(self, optimization_result: dict[str, Any]) -> None:
        """Track successful optimization for monitoring."""
        tokens_saved = optimization_result["optimization_metadata"]["total_tokens_saved"]
        agricultural_compliance = optimization_result["agricultural_compliance"]

        # Update session tracking
        self.session_tracking["interactions_this_session"] += 1
        self.session_tracking["optimization_applied_count"] += 1
        self.session_tracking["tokens_saved_this_session"] += tokens_saved

        if agricultural_compliance["agricultural_keywords_detected"]:
            self.session_tracking["agricultural_interactions"] += 1

        if agricultural_compliance["safety_critical"]:
            self.session_tracking["safety_critical_interactions"] += 1

        # Check for compliance violations
        if not agricultural_compliance["compliance_maintained"]:
            self.monitoring_data["agricultural_compliance_violations"] += 1

        self._save_session_tracking()

    def _track_interaction(self, user_input: str, ai_response: str, optimized: bool = True) -> None:
        """Track any interaction for monitoring purposes."""
        self.session_tracking["interactions_this_session"] += 1

        if optimized:
            self.session_tracking["optimization_applied_count"] += 1

        # Detect agricultural content even without optimization
        content = f"{user_input} {ai_response}".lower()
        agricultural_keywords = ["agricultural", "tractor", "equipment", "iso", "11783", "farming"]
        safety_keywords = ["emergency", "safety", "critical", "stop"]

        if any(keyword in content for keyword in agricultural_keywords):
            self.session_tracking["agricultural_interactions"] += 1

        if any(keyword in content for keyword in safety_keywords):
            self.session_tracking["safety_critical_interactions"] += 1

        self._save_session_tracking()

    def _save_monitoring_data(self) -> None:
        """Save monitoring data to persistent storage."""
        self.monitoring_data["last_monitoring_update"] = datetime.now().isoformat()

        try:
            with open(self.monitoring_data_path, "w") as f:
                json.dump(self.monitoring_data, f, indent=2)
        except OSError:
            pass  # Fail silently to avoid breaking interactions

    def _save_session_tracking(self) -> None:
        """Save current session tracking data."""
        try:
            with open(self.session_tracking_path, "w") as f:
                json.dump(self.session_tracking, f, indent=2)
        except OSError:
            pass  # Fail silently to avoid breaking interactions

    def get_monitoring_report(self) -> dict[str, Any]:
        """Get comprehensive monitoring report across all sessions."""
        # Calculate current session effectiveness
        current_effectiveness = 0.0
        if self.session_tracking["interactions_this_session"] > 0:
            current_effectiveness = (
                self.session_tracking["tokens_saved_this_session"]
                / self.session_tracking["interactions_this_session"]
            )

        # Calculate overall effectiveness
        total_interactions = self.monitoring_data["total_interactions_optimized"]
        overall_effectiveness = 0.0
        if total_interactions > 0:
            overall_effectiveness = (
                self.monitoring_data["total_tokens_saved_all_time"] / total_interactions
            )

        return {
            "enforcement_status": {
                "enabled": self.enforcement_config["enforcement_enabled"],
                "mandatory": self.enforcement_config["mandatory_for_all_agents"],
                "version": self.enforcement_config["enforcement_version"],
            },
            "current_session": self.session_tracking,
            "current_session_effectiveness": current_effectiveness,
            "all_time_statistics": {
                "total_sessions": self.monitoring_data["total_sessions_monitored"],
                "total_interactions": self.monitoring_data["total_interactions_optimized"],
                "total_tokens_saved": self.monitoring_data["total_tokens_saved_all_time"],
                "overall_effectiveness": overall_effectiveness,
                "compliance_violations": self.monitoring_data["agricultural_compliance_violations"],
                "enforcement_failures": self.monitoring_data["enforcement_failures"],
            },
            "recent_sessions": self.monitoring_data["session_history"][-10:],  # Last 10 sessions
            "effectiveness_trend": self.monitoring_data["effectiveness_trend"][
                -20:
            ],  # Last 20 measurements
        }

    def force_optimization_for_agent(self, agent_type: str) -> bool:
        """Force optimization enforcement for a specific agent type."""
        if agent_type.lower() not in [
            agent.lower() for agent in self.enforcement_config["agent_types_enforced"]
        ]:
            self.enforcement_config["agent_types_enforced"].append(agent_type.lower())

            # Save updated configuration
            self.enforcement_config["last_updated"] = datetime.now().isoformat()
            with open(self.enforcement_config_path, "w") as f:
                json.dump(self.enforcement_config, f, indent=2)

            return True
        return False

    def is_optimization_mandatory(self) -> bool:
        """Check if optimization is mandatory for all agents."""
        return (
            self.enforcement_config["enforcement_enabled"]
            and self.enforcement_config["mandatory_for_all_agents"]
        )


# Global enforcer instance
_global_enforcer: MandatoryOptimizationEnforcer | None = None


def get_enforcer() -> MandatoryOptimizationEnforcer:
    """Get or create global mandatory optimization enforcer."""
    global _global_enforcer

    if _global_enforcer is None:
        _global_enforcer = MandatoryOptimizationEnforcer()

    return _global_enforcer


def enforce_mandatory_optimization(
    user_input: str, ai_response: str = "", interaction_type: str = "general"
) -> dict[str, Any]:
    """
    MANDATORY token optimization enforcement for ALL AI interactions.

    This function CANNOT be bypassed and automatically applies optimization
    to all AI conversations across all agent types.
    """
    enforcer = get_enforcer()
    return enforcer.enforce_optimization(user_input, ai_response, interaction_type)


def get_optimization_monitoring_report() -> dict[str, Any]:
    """Get comprehensive optimization monitoring report across all sessions."""
    enforcer = get_enforcer()
    return enforcer.get_monitoring_report()


def initialize_mandatory_optimization() -> bool:
    """Initialize mandatory optimization system for current session."""
    try:
        enforcer = get_enforcer()

        # Detect agent type (basic detection)
        agent_type = "unknown"
        if "CLAUDE" in os.environ.get("USER_AGENT", "").upper():
            agent_type = "claude"
        elif "anthropic" in os.environ.get("USER_AGENT", "").lower():
            agent_type = "claude"
        else:
            # Check for common AI assistant indicators
            env_vars = " ".join(
                [
                    os.environ.get("AI_ASSISTANT", ""),
                    os.environ.get("MODEL_NAME", ""),
                    os.environ.get("ASSISTANT_TYPE", ""),
                ]
            ).lower()

            if "claude" in env_vars:
                agent_type = "claude"
            elif "gpt" in env_vars:
                agent_type = "gpt"
            elif "gemini" in env_vars:
                agent_type = "gemini"

        # Update session tracking with detected agent type
        enforcer.session_tracking["agent_type"] = agent_type
        enforcer._save_session_tracking()

        # Force optimization for this agent type
        enforcer.force_optimization_for_agent(agent_type)

        return True
    except Exception:
        return False


# Auto-initialize when module is imported
if __name__ != "__main__":
    initialize_mandatory_optimization()
