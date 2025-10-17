"""Advanced message prioritization framework with QoS levels for agricultural operations.

This module provides sophisticated CAN bus message prioritization using Quality of Service
(QoS) levels specifically designed for multi-tractor fleet coordination and agricultural
robotics operations with safety-critical message handling.
"""

from __future__ import annotations

import time
from dataclasses import dataclass, field
from datetime import UTC, datetime
from enum import Enum
from typing import Any


class QoSLevel(Enum):
    """Quality of Service levels for agricultural CAN bus message prioritization.

    Defines priority levels optimized for agricultural equipment coordination
    with safety-critical and operational message classification.
    """

    EMERGENCY = ("emergency", 1000, 50)  # Highest priority, 50ms max delay
    CRITICAL = ("critical", 750, 200)  # Safety-critical, 200ms max delay
    OPERATIONAL = ("operational", 500, 1000)  # Field operations, 1s max delay
    INFORMATIONAL = ("informational", 250, 5000)  # Status updates, 5s max delay

    def __init__(self, name: str, priority: int, max_delay_ms: int) -> None:
        self.level_name = name
        self.priority = priority
        self.max_delay_ms = max_delay_ms


class AgriculturalOperationContext(Enum):
    """Agricultural operation contexts that affect message prioritization.

    Different agricultural operations require different message prioritization
    strategies for optimal fleet coordination and safety.
    """

    FIELD_CULTIVATION = ("field_cultivation", 1.5)
    TRANSPORT_MODE = ("transport", 1.0)
    MAINTENANCE_MODE = ("maintenance", 0.8)
    IDLE_MODE = ("idle", 0.5)

    def __init__(self, operation: str, priority_modifier: float) -> None:
        self.operation = operation
        self.priority_modifier = priority_modifier


@dataclass
class PrioritizedMessage:
    """Represents a CAN bus message with prioritization metadata.

    Contains the original message plus computed prioritization information
    for advanced traffic management and QoS enforcement.
    """

    message_id: str
    original_message: dict[str, Any]
    qos_level: QoSLevel
    base_priority: int
    effective_priority: int
    fleet_coordination_boost: bool = False
    safety_related: bool = False
    can_be_throttled: bool = True
    max_allowable_delay: int = 0
    operation_context: AgriculturalOperationContext | None = None
    timestamp: datetime = field(default_factory=lambda: datetime.now(UTC))


@dataclass
class TrafficThrottlingDecision:
    """Represents a traffic throttling decision for network optimization.

    Contains the decision logic for whether and how much to throttle
    a message based on QoS constraints and network conditions.
    """

    should_throttle: bool = False
    delay_ms: int = 0
    agricultural_priority_boost: bool = False
    reason: str = ""

    def evaluate_throttling(
        self,
        message: Any,
        network_state: dict[str, Any],
        agricultural_context: dict[str, Any] | None = None,
    ) -> TrafficThrottlingDecision:
        """Evaluate throttling decision based on message priority and network state."""
        # Emergency and critical messages are never throttled beyond QoS limits
        if hasattr(message, "qos_level"):
            if message.qos_level == QoSLevel.EMERGENCY:
                return TrafficThrottlingDecision(
                    should_throttle=False, delay_ms=0, reason="Emergency message - no throttling"
                )

            if message.qos_level == QoSLevel.CRITICAL:
                max_delay = (
                    message.max_allowable_delay if hasattr(message, "max_allowable_delay") else 200
                )
                congestion = network_state.get("congestion_level", 0)
                delay = min(int(congestion * 100), max_delay)
                return TrafficThrottlingDecision(
                    should_throttle=delay > 0,
                    delay_ms=delay,
                    reason=f"Critical message - limited throttling: {delay}ms",
                )

        # Fleet coordination gets priority boost
        fleet_boost = False
        if hasattr(message, "fleet_coordination") and message.fleet_coordination:
            fleet_boost = True

        if agricultural_context and "coordination_mode" in agricultural_context:
            fleet_boost = True

        # Default throttling logic for operational/informational messages
        congestion = network_state.get("congestion_level", 0)
        if congestion > 0.5:  # High congestion
            base_delay = int(congestion * 1000)  # Up to 1 second delay
            if fleet_boost:
                # Significant reduction for fleet coordination messages
                base_delay = min(base_delay // 2, 400)  # Max 400ms for fleet coordination

            return TrafficThrottlingDecision(
                should_throttle=True,
                delay_ms=base_delay,
                agricultural_priority_boost=fleet_boost,
                reason=f"Network congestion throttling: {base_delay}ms",
            )

        return TrafficThrottlingDecision(
            should_throttle=False,
            delay_ms=0,
            agricultural_priority_boost=fleet_boost,
            reason="No throttling required",
        )


class MessageClassification:
    """Message classification system for CAN bus traffic analysis.

    Classifies incoming CAN messages based on PGN, content, and operational
    context to determine appropriate QoS levels and prioritization.
    """

    def __init__(self) -> None:
        """Initialize message classification system."""
        self._emergency_pgns = {0xFECA}  # Emergency stop PGN
        self._critical_pgns = {0xF003, 0xF004}  # Engine controller, speed data
        self._operational_pgns = {0xF005}  # GPS position
        self._informational_pgns = {0xF001}  # Engine RPM

    def classify_message(
        self, message: dict[str, Any], context: AgriculturalOperationContext | None = None
    ) -> MessageClassificationResult:
        """Classify a CAN message for prioritization."""
        pgn = message.get("pgn", 0)

        # Create classification result object
        result = MessageClassificationResult()

        # Classify by PGN
        if pgn in self._emergency_pgns:
            result.qos_level = QoSLevel.EMERGENCY
            result.requires_immediate_processing = True
            result.can_be_throttled = False
            result.safety_related = True
        elif pgn in self._critical_pgns:
            result.qos_level = QoSLevel.CRITICAL
            result.safety_related = True
            result.throttling_sensitivity = "high"
        elif pgn in self._operational_pgns:
            # Context affects operational message priority
            if context == AgriculturalOperationContext.FIELD_CULTIVATION:
                result.qos_level = QoSLevel.OPERATIONAL
                result.effective_priority = 600  # Higher than base operational
            else:
                result.qos_level = QoSLevel.INFORMATIONAL
                result.effective_priority = 300  # Lower priority for non-field context
        else:
            result.qos_level = QoSLevel.INFORMATIONAL
            result.effective_priority = 250

        return result


@dataclass
class MessageClassificationResult:
    """Result of message classification containing prioritization metadata."""

    qos_level: QoSLevel = QoSLevel.INFORMATIONAL
    requires_immediate_processing: bool = False
    can_be_throttled: bool = True
    safety_related: bool = False
    throttling_sensitivity: str = "normal"
    effective_priority: int = 250


class AdvancedMessagePrioritizer:
    """Advanced message prioritization framework for agricultural CAN bus traffic.

    Provides sophisticated message prioritization using QoS levels, agricultural
    operation context, and fleet coordination awareness for optimal traffic management.
    """

    def __init__(
        self, equipment_id: str, operation_profile: str, fleet_coordination_enabled: bool = False
    ) -> None:
        """Initialize the advanced message prioritization system."""
        self.equipment_id = equipment_id
        self.operation_profile = operation_profile
        self.fleet_coordination_enabled = fleet_coordination_enabled

        # Set initial context based on operation profile
        if operation_profile == "field_cultivation":
            self.current_context = AgriculturalOperationContext.FIELD_CULTIVATION
        elif operation_profile == "transport":
            self.current_context = AgriculturalOperationContext.TRANSPORT_MODE
        else:
            self.current_context = AgriculturalOperationContext.FIELD_CULTIVATION

        self._classifier = MessageClassification()
        self._message_cache: dict[str, MessageClassificationResult] = {}
        self._context_cache: dict[str, AgriculturalOperationContext] = {}

    def set_operation_context(self, context: AgriculturalOperationContext) -> None:
        """Set the current agricultural operation context."""
        self.current_context = context

    def prioritize_single_message(self, message: dict[str, Any]) -> PrioritizedMessage:
        """Prioritize a single CAN message using QoS framework."""
        classification_result = self._classifier.classify_message(message, self.current_context)

        # Calculate effective priority
        base_priority = classification_result.qos_level.priority
        effective_priority = base_priority

        # Emergency and Critical messages maintain absolute priority
        if classification_result.qos_level in [QoSLevel.EMERGENCY, QoSLevel.CRITICAL]:
            effective_priority = base_priority  # No modifiers for safety-critical
        else:
            # Apply context modifier only for operational/informational messages
            if (
                hasattr(classification_result, "effective_priority")
                and classification_result.effective_priority
            ):
                effective_priority = classification_result.effective_priority
            else:
                effective_priority = int(base_priority * self.current_context.priority_modifier)

        # Fleet coordination boost (but never exceed safety-critical levels)
        fleet_boost = False
        if message.get("fleet_coordination") and self.fleet_coordination_enabled:
            fleet_boost = True
            if classification_result.qos_level not in [QoSLevel.EMERGENCY, QoSLevel.CRITICAL]:
                effective_priority = int(effective_priority * 1.2)  # 20% boost

        return PrioritizedMessage(
            message_id=message.get("message_id", f"msg_{int(time.time() * 1000)}"),
            original_message=message,
            qos_level=classification_result.qos_level,
            base_priority=base_priority,
            effective_priority=effective_priority,
            fleet_coordination_boost=fleet_boost,
            safety_related=classification_result.safety_related,
            can_be_throttled=classification_result.can_be_throttled,
            max_allowable_delay=classification_result.qos_level.max_delay_ms,
            operation_context=self.current_context,
        )

    def prioritize_message_batch(self, messages: list[dict[str, Any]]) -> list[PrioritizedMessage]:
        """Prioritize a batch of CAN messages efficiently."""
        prioritized = []

        for message in messages:
            prioritized_msg = self.prioritize_single_message(message)
            prioritized.append(prioritized_msg)

        # Sort by effective priority (highest first)
        prioritized.sort(key=lambda msg: msg.effective_priority, reverse=True)

        return prioritized

    def make_throttling_decision(
        self, message: dict[str, Any], network_state: dict[str, Any]
    ) -> TrafficThrottlingDecision:
        """Make throttling decision for a message based on network conditions."""
        prioritized_msg = self.prioritize_single_message(message)

        decision_framework = TrafficThrottlingDecision()
        return decision_framework.evaluate_throttling(prioritized_msg, network_state)

    def get_memory_statistics(self) -> dict[str, int]:
        """Get memory usage statistics for the prioritization system."""
        return {
            "cached_classifications": len(self._message_cache),
            "active_contexts": len(self._context_cache),
        }
