"""
Message prioritization system for CAN traffic management and network optimization.

This module provides comprehensive traffic management, prioritization, and
network optimization for high-throughput agricultural ISOBUS operations.

Implementation follows Test-First Development (TDD) GREEN phase.
"""

from __future__ import annotations

import heapq
import logging
import time
from collections import defaultdict, deque
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import Any

from afs_fastapi.equipment.farm_tractors import ISOBUSMessage

# Configure logging for message prioritization
logger = logging.getLogger(__name__)


@dataclass
class TrafficClass:
    """Traffic class definition for agricultural message categorization."""

    class_id: str
    priority_level: int
    max_bandwidth_percentage: float
    guaranteed_bandwidth_kbps: float
    max_latency_ms: float
    max_jitter_ms: float = 5.0
    description: str = ""
    weight: int = 1


@dataclass
class MessageClassification:
    """Result of message traffic classification."""

    traffic_class: TrafficClass
    confidence_score: float
    classification_metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class BandwidthReservation:
    """Bandwidth reservation for traffic class."""

    traffic_class: str
    reserved_kbps: float
    priority: int
    created_at: datetime = field(default_factory=datetime.now)


@dataclass
class TransmissionRecord:
    """Record of message transmission for bandwidth tracking."""

    traffic_class: str
    message_size_bytes: int
    transmission_time_ms: float
    timestamp: datetime = field(default_factory=datetime.now)


@dataclass
class ScheduledMessage:
    """Message with scheduling information."""

    message: ISOBUSMessage
    traffic_class: str
    priority: int
    enqueue_time: datetime = field(default_factory=datetime.now)
    effective_priority: float = 0.0


class TrafficAnalyzer:
    """Analyzes and classifies ISOBUS messages for traffic management."""

    def __init__(self) -> None:
        """Initialize traffic analyzer with agricultural classifications."""
        self._classification_rules: dict[int, str] = {
            0xE001: "EMERGENCY_SAFETY",
            0xE002: "COLLISION_AVOIDANCE",
            0xE003: "FIELD_COORDINATION",
            0xE004: "TELEMETRY_STREAMING",
            0xE005: "IMPLEMENT_CONTROL",
            0xE006: "DIAGNOSTICS",
        }

        self._default_classes = self._create_default_classes()

    def _create_default_classes(self) -> list[TrafficClass]:
        """Create default agricultural traffic classes."""
        return [
            TrafficClass(
                class_id="EMERGENCY_SAFETY",
                priority_level=0,
                max_bandwidth_percentage=30.0,
                guaranteed_bandwidth_kbps=150.0,
                max_latency_ms=10.0,
                max_jitter_ms=2.0,
                description="Emergency stop and safety-critical messages",
                weight=40,
            ),
            TrafficClass(
                class_id="COLLISION_AVOIDANCE",
                priority_level=1,
                max_bandwidth_percentage=20.0,
                guaranteed_bandwidth_kbps=100.0,
                max_latency_ms=20.0,
                max_jitter_ms=5.0,
                description="Obstacle detection and collision avoidance",
                weight=30,
            ),
            TrafficClass(
                class_id="FIELD_COORDINATION",
                priority_level=2,
                max_bandwidth_percentage=20.0,
                guaranteed_bandwidth_kbps=100.0,
                max_latency_ms=50.0,
                max_jitter_ms=10.0,
                description="Multi-tractor field operations coordination",
                weight=20,
            ),
            TrafficClass(
                class_id="IMPLEMENT_CONTROL",
                priority_level=3,
                max_bandwidth_percentage=15.0,
                guaranteed_bandwidth_kbps=75.0,
                max_latency_ms=100.0,
                max_jitter_ms=20.0,
                description="Tractor-implement communication and control",
                weight=15,
            ),
            TrafficClass(
                class_id="TELEMETRY_STREAMING",
                priority_level=4,
                max_bandwidth_percentage=10.0,
                guaranteed_bandwidth_kbps=50.0,
                max_latency_ms=200.0,
                max_jitter_ms=50.0,
                description="Real-time telemetry and sensor data",
                weight=10,
            ),
            TrafficClass(
                class_id="STATUS_UPDATES",
                priority_level=5,
                max_bandwidth_percentage=3.0,
                guaranteed_bandwidth_kbps=15.0,
                max_latency_ms=500.0,
                max_jitter_ms=100.0,
                description="Routine status updates and heartbeats",
                weight=5,
            ),
            TrafficClass(
                class_id="DIAGNOSTICS",
                priority_level=6,
                max_bandwidth_percentage=2.0,
                guaranteed_bandwidth_kbps=10.0,
                max_latency_ms=1000.0,
                max_jitter_ms=200.0,
                description="Non-critical diagnostic information",
                weight=2,
            ),
            TrafficClass(
                class_id="BEST_EFFORT",
                priority_level=7,
                max_bandwidth_percentage=0.0,
                guaranteed_bandwidth_kbps=0.0,
                max_latency_ms=5000.0,
                max_jitter_ms=1000.0,
                description="Best-effort traffic with no guarantees",
                weight=1,
            ),
        ]

    def get_default_agricultural_classes(self) -> list[TrafficClass]:
        """Get default agricultural traffic classes.

        Returns
        -------
        list[TrafficClass]
            List of default traffic classes for agricultural operations
        """
        return self._default_classes.copy()

    def classify_message(self, message: ISOBUSMessage) -> MessageClassification:
        """Classify ISOBUS message into traffic class.

        Parameters
        ----------
        message : ISOBUSMessage
            Message to classify

        Returns
        -------
        MessageClassification
            Classification result with confidence score
        """
        # Classify based on PGN
        class_id = self._classification_rules.get(message.pgn, "BEST_EFFORT")

        # Find traffic class
        traffic_class = next(
            (cls for cls in self._default_classes if cls.class_id == class_id),
            self._default_classes[-1],  # Default to BEST_EFFORT
        )

        # Calculate confidence based on PGN match and other factors
        confidence = 0.95 if message.pgn in self._classification_rules else 0.50

        # Boost confidence for emergency/safety messages
        if class_id in ["EMERGENCY_SAFETY", "COLLISION_AVOIDANCE"]:
            confidence = max(confidence, 0.95)
        elif class_id == "TELEMETRY_STREAMING":
            confidence = max(confidence, 0.80)

        return MessageClassification(
            traffic_class=traffic_class,
            confidence_score=confidence,
            classification_metadata={"pgn": message.pgn, "source": message.source_address},
        )


class PriorityQueue:
    """Priority queue implementation with aging for message scheduling."""

    def __init__(
        self,
        max_queue_size: int = 1000,
        priority_levels: int = 8,
        aging_enabled: bool = True,
        aging_factor: float = 0.1,
    ) -> None:
        """Initialize priority queue.

        Parameters
        ----------
        max_queue_size : int, default 1000
            Maximum number of messages in queue
        priority_levels : int, default 8
            Number of priority levels
        aging_enabled : bool, default True
            Enable priority aging to prevent starvation
        aging_factor : float, default 0.1
            Factor for priority aging adjustment
        """
        self.max_queue_size = max_queue_size
        self.priority_levels = priority_levels
        self.aging_enabled = aging_enabled
        self.aging_factor = aging_factor

        # Priority queue: (effective_priority, sequence, message)
        self._queue: list[tuple[float, int, ISOBUSMessage]] = []
        self._sequence_counter = 0
        self._message_priorities: dict[int, int] = {}  # Use sequence as key
        self._enqueue_times: dict[int, datetime] = {}  # Use sequence as key
        self._message_lookup: dict[int, ISOBUSMessage] = {}  # sequence -> message

    @property
    def current_size(self) -> int:
        """Get current queue size."""
        return len(self._queue)

    def is_full(self) -> bool:
        """Check if queue is full."""
        return self.current_size >= self.max_queue_size

    def is_empty(self) -> bool:
        """Check if queue is empty."""
        return self.current_size == 0

    def enqueue(self, message: ISOBUSMessage, priority: int) -> bool:
        """Enqueue message with priority.

        Parameters
        ----------
        message : ISOBUSMessage
            Message to enqueue
        priority : int
            Message priority (lower = higher priority)

        Returns
        -------
        bool
            True if message was enqueued successfully
        """
        if self.is_full():
            return False

        self._sequence_counter += 1
        effective_priority = float(priority)

        heapq.heappush(self._queue, (effective_priority, self._sequence_counter, message))
        self._message_priorities[self._sequence_counter] = priority
        self._enqueue_times[self._sequence_counter] = datetime.now()
        self._message_lookup[self._sequence_counter] = message

        return True

    def dequeue(self) -> ISOBUSMessage | None:
        """Dequeue highest priority message.

        Returns
        -------
        ISOBUSMessage | None
            Highest priority message or None if queue empty
        """
        if self.is_empty():
            return None

        _, sequence, message = heapq.heappop(self._queue)

        # Clean up tracking data
        self._message_priorities.pop(sequence, None)
        self._enqueue_times.pop(sequence, None)
        self._message_lookup.pop(sequence, None)

        return message

    def age_messages(self) -> None:
        """Apply aging to prevent message starvation."""
        if not self.aging_enabled or self.is_empty():
            return

        current_time = datetime.now()
        updated_queue: list[tuple[float, int, ISOBUSMessage]] = []

        # Rebuild queue with aged priorities
        while self._queue:
            _, sequence, message = heapq.heappop(self._queue)

            original_priority = self._message_priorities.get(sequence, 7)
            enqueue_time = self._enqueue_times.get(sequence, current_time)

            # Calculate aging adjustment
            age_seconds = (current_time - enqueue_time).total_seconds()
            aging_adjustment = age_seconds * self.aging_factor

            # Apply aging (reduce effective priority)
            effective_priority = max(0.0, original_priority - aging_adjustment)

            updated_queue.append((effective_priority, sequence, message))

        # Rebuild heap
        self._queue = updated_queue
        heapq.heapify(self._queue)

    def get_effective_priority(self, message: ISOBUSMessage) -> float:
        """Get effective priority for message.

        Parameters
        ----------
        message : ISOBUSMessage
            Message to check

        Returns
        -------
        float
            Effective priority after aging
        """
        # Find the sequence number for this message
        sequence = None
        for seq, msg in self._message_lookup.items():
            if msg is message:
                sequence = seq
                break

        if sequence is None:
            return 7.0  # Default priority if not found

        original_priority = self._message_priorities.get(sequence, 7)

        if not self.aging_enabled:
            return float(original_priority)

        enqueue_time = self._enqueue_times.get(sequence, datetime.now())
        age_seconds = (datetime.now() - enqueue_time).total_seconds()
        aging_adjustment = age_seconds * self.aging_factor

        return max(0.0, original_priority - aging_adjustment)


class TrafficShaper:
    """Traffic shaping for bandwidth management using token bucket algorithm."""

    def __init__(
        self,
        total_bandwidth_kbps: float = 500.0,
        shaping_algorithm: str = "token_bucket",
        burst_size_bytes: int = 1024,
        measurement_window_ms: int = 100,
    ) -> None:
        """Initialize traffic shaper.

        Parameters
        ----------
        total_bandwidth_kbps : float, default 500.0
            Total network bandwidth in Kbps
        shaping_algorithm : str, default "token_bucket"
            Shaping algorithm to use
        burst_size_bytes : int, default 1024
            Maximum burst size in bytes
        measurement_window_ms : int, default 100
            Measurement window in milliseconds
        """
        self.total_bandwidth_kbps = total_bandwidth_kbps
        self.shaping_algorithm = shaping_algorithm
        self.burst_size_bytes = burst_size_bytes
        self.measurement_window_ms = measurement_window_ms

        # Token buckets per traffic class
        self._class_allocations: dict[str, float] = {}
        self._token_buckets: dict[str, dict[str, Any]] = {}
        self._last_refill_time = time.time()

        # Configure default allocations
        self._configure_default_allocations()

    def _configure_default_allocations(self) -> None:
        """Configure default bandwidth allocations for agricultural traffic classes."""
        default_allocations = {
            "EMERGENCY_SAFETY": 30.0,
            "COLLISION_AVOIDANCE": 20.0,
            "FIELD_COORDINATION": 20.0,
            "IMPLEMENT_CONTROL": 15.0,
            "TELEMETRY_STREAMING": 10.0,
            "STATUS_UPDATES": 3.0,
            "DIAGNOSTICS": 2.0,
        }
        self.configure_class_allocations(default_allocations)

    def configure_class_allocations(self, allocations: dict[str, float]) -> None:
        """Configure bandwidth allocations for traffic classes.

        Parameters
        ----------
        allocations : dict[str, float]
            Bandwidth allocation percentages per class
        """
        self._class_allocations = allocations.copy()

        # Initialize token buckets
        for class_id, percentage in allocations.items():
            bandwidth_kbps = (percentage / 100.0) * self.total_bandwidth_kbps

            self._token_buckets[class_id] = {
                "bandwidth_kbps": bandwidth_kbps,
                "tokens": self.burst_size_bytes,  # Start with full bucket
                "last_refill": time.time(),
                "max_tokens": self.burst_size_bytes,
            }

    def get_allocated_bandwidth(self, class_id: str) -> float:
        """Get allocated bandwidth for traffic class.

        Parameters
        ----------
        class_id : str
            Traffic class identifier

        Returns
        -------
        float
            Allocated bandwidth in Kbps
        """
        percentage = self._class_allocations.get(class_id, 0.0)
        return (percentage / 100.0) * self.total_bandwidth_kbps

    def can_send_message(self, class_id: str, message_size_bytes: int) -> bool:
        """Check if message can be sent based on token bucket.

        Parameters
        ----------
        class_id : str
            Traffic class identifier
        message_size_bytes : int
            Message size in bytes

        Returns
        -------
        bool
            True if message can be sent
        """
        if class_id not in self._token_buckets:
            return False

        bucket = self._token_buckets[class_id]
        self._refill_bucket(class_id)

        return bucket["tokens"] >= message_size_bytes

    def consume_tokens(self, class_id: str, message_size_bytes: int) -> bool:
        """Consume tokens for message transmission.

        Parameters
        ----------
        class_id : str
            Traffic class identifier
        message_size_bytes : int
            Message size in bytes

        Returns
        -------
        bool
            True if tokens were consumed successfully
        """
        if not self.can_send_message(class_id, message_size_bytes):
            return False

        bucket = self._token_buckets[class_id]
        bucket["tokens"] -= message_size_bytes

        return True

    def _refill_bucket(self, class_id: str) -> None:
        """Refill token bucket based on bandwidth allocation."""
        if class_id not in self._token_buckets:
            return

        bucket = self._token_buckets[class_id]
        current_time = time.time()
        time_elapsed = current_time - bucket["last_refill"]

        # Calculate tokens to add based on bandwidth
        bandwidth_bps = bucket["bandwidth_kbps"] * 1000 / 8  # Convert to bytes per second
        tokens_to_add = int(bandwidth_bps * time_elapsed)

        # Add tokens up to maximum
        bucket["tokens"] = min(bucket["max_tokens"], bucket["tokens"] + tokens_to_add)
        bucket["last_refill"] = current_time


class CongestionController:
    """Congestion control for network optimization."""

    def __init__(
        self,
        congestion_threshold: float = 0.8,
        measurement_window_seconds: float = 1.0,
        backoff_strategy: str = "exponential",
    ) -> None:
        """Initialize congestion controller.

        Parameters
        ----------
        congestion_threshold : float, default 0.8
            Network utilization threshold for congestion detection
        measurement_window_seconds : float, default 1.0
            Measurement window for congestion detection
        backoff_strategy : str, default "exponential"
            Backoff strategy for congestion response
        """
        self.congestion_threshold = congestion_threshold
        self.measurement_window_seconds = measurement_window_seconds
        self.backoff_strategy = backoff_strategy

        self._transmission_records: deque[dict[str, Any]] = deque()
        self._is_congested = False
        self._congestion_level = 0.0

    def record_message_transmission(
        self,
        message_size: int,
        transmission_time_ms: float,
        queue_depth: int,
    ) -> None:
        """Record message transmission for congestion analysis.

        Parameters
        ----------
        message_size : int
            Message size in bytes
        transmission_time_ms : float
            Transmission time in milliseconds
        queue_depth : int
            Current queue depth
        """
        record = {
            "timestamp": time.time(),
            "message_size": message_size,
            "transmission_time_ms": transmission_time_ms,
            "queue_depth": queue_depth,
        }

        self._transmission_records.append(record)

        # Clean old records
        cutoff_time = time.time() - self.measurement_window_seconds
        while (
            self._transmission_records and self._transmission_records[0]["timestamp"] < cutoff_time
        ):
            self._transmission_records.popleft()

        # Update congestion level
        self._update_congestion_level()

    def _update_congestion_level(self) -> None:
        """Update current congestion level based on recent transmissions."""
        if not self._transmission_records:
            self._congestion_level = 0.0
            self._is_congested = False
            return

        # Calculate average queue depth and transmission times
        total_queue_depth = sum(r["queue_depth"] for r in self._transmission_records)
        avg_queue_depth = total_queue_depth / len(self._transmission_records)

        total_tx_time = sum(r["transmission_time_ms"] for r in self._transmission_records)
        avg_tx_time = total_tx_time / len(self._transmission_records)

        # Estimate congestion level (0.0 to 1.0)
        queue_factor = min(1.0, avg_queue_depth / 20.0)  # Normalize to 20 messages (more sensitive)
        latency_factor = min(1.0, avg_tx_time / 10.0)  # Normalize to 10ms (more sensitive)

        # Weight queue depth more heavily for congestion detection
        self._congestion_level = (queue_factor * 0.7) + (latency_factor * 0.3)
        self._is_congested = self._congestion_level > self.congestion_threshold

    def get_congestion_level(self) -> float:
        """Get current congestion level.

        Returns
        -------
        float
            Congestion level (0.0 to 1.0)
        """
        return self._congestion_level

    def is_network_congested(self) -> bool:
        """Check if network is currently congested.

        Returns
        -------
        bool
            True if network is congested
        """
        return self._is_congested

    def set_congestion_state(self, congested: bool) -> None:
        """Manually set congestion state for testing.

        Parameters
        ----------
        congested : bool
            Whether network is congested
        """
        self._is_congested = congested
        self._congestion_level = 0.9 if congested else 0.3

    def get_backoff_factor(self, traffic_class: str) -> float:
        """Get backoff factor for traffic class during congestion.

        Parameters
        ----------
        traffic_class : str
            Traffic class identifier

        Returns
        -------
        float
            Backoff factor (1.0 = no delay, >1.0 = delay)
        """
        if not self._is_congested:
            return 1.0

        # No backoff for critical traffic
        if traffic_class in ["EMERGENCY_SAFETY", "COLLISION_AVOIDANCE"]:
            return 1.0

        # Progressive backoff for other traffic
        backoff_factors = {
            "FIELD_COORDINATION": 1.5,
            "IMPLEMENT_CONTROL": 2.0,
            "TELEMETRY_STREAMING": 3.0,
            "STATUS_UPDATES": 4.0,
            "DIAGNOSTICS": 5.0,
            "BEST_EFFORT": 10.0,
        }

        return backoff_factors.get(traffic_class, 2.0)

    def get_transmission_rate(self, traffic_class: str) -> float:
        """Get transmission rate factor for traffic class.

        Parameters
        ----------
        traffic_class : str
            Traffic class identifier

        Returns
        -------
        float
            Rate factor (1.0 = full rate, <1.0 = reduced rate)
        """
        if not self._is_congested:
            return 1.0

        # Maintain full rate for critical traffic
        if traffic_class in ["EMERGENCY_SAFETY", "COLLISION_AVOIDANCE"]:
            return 1.0

        # Reduce rate for other traffic during congestion
        return max(0.1, 1.0 - (self._congestion_level * 0.8))


class BandwidthManager:
    """Bandwidth management and monitoring for agricultural networks."""

    def __init__(
        self,
        total_bandwidth_kbps: float = 500.0,
        monitoring_interval_ms: int = 100,
    ) -> None:
        """Initialize bandwidth manager.

        Parameters
        ----------
        total_bandwidth_kbps : float, default 500.0
            Total network bandwidth in Kbps
        monitoring_interval_ms : int, default 100
            Monitoring interval in milliseconds
        """
        self.total_bandwidth_kbps = total_bandwidth_kbps
        self.monitoring_interval_ms = monitoring_interval_ms

        self._transmission_history: deque[TransmissionRecord] = deque()
        self._reservations: dict[str, BandwidthReservation] = {}
        self._class_utilization: dict[str, float] = defaultdict(float)

    def record_transmission(
        self,
        traffic_class: str,
        message_size_bytes: int,
        transmission_time_ms: float,
    ) -> None:
        """Record message transmission for bandwidth tracking.

        Parameters
        ----------
        traffic_class : str
            Traffic class identifier
        message_size_bytes : int
            Message size in bytes
        transmission_time_ms : float
            Transmission time in milliseconds
        """
        record = TransmissionRecord(
            traffic_class=traffic_class,
            message_size_bytes=message_size_bytes,
            transmission_time_ms=transmission_time_ms,
        )

        self._transmission_history.append(record)

        # Clean old records (keep last 10 seconds)
        cutoff_time = datetime.now() - timedelta(seconds=10)
        while self._transmission_history and self._transmission_history[0].timestamp < cutoff_time:
            self._transmission_history.popleft()

        # Update utilization
        self._update_utilization()

    def _update_utilization(self) -> None:
        """Update bandwidth utilization statistics."""
        if not self._transmission_history:
            self._class_utilization.clear()
            return

        # Calculate utilization over last second
        cutoff_time = datetime.now() - timedelta(seconds=1)
        recent_records = [r for r in self._transmission_history if r.timestamp > cutoff_time]

        class_bytes: dict[str, int] = defaultdict(int)
        total_bytes = 0

        for record in recent_records:
            class_bytes[record.traffic_class] += record.message_size_bytes
            total_bytes += record.message_size_bytes

        # Convert to utilization percentages
        if total_bytes > 0:
            total_bandwidth_bps = (
                self.total_bandwidth_kbps * 1000 / 8
            )  # Convert to bytes per second

            for class_id, bytes_used in class_bytes.items():
                self._class_utilization[class_id] = bytes_used / total_bandwidth_bps
        else:
            self._class_utilization.clear()

    def get_current_utilization(self) -> float:
        """Get current total bandwidth utilization.

        Returns
        -------
        float
            Total utilization (0.0 to 1.0)
        """
        return sum(self._class_utilization.values())

    def get_class_utilization(self, traffic_class: str) -> float:
        """Get bandwidth utilization for specific traffic class.

        Parameters
        ----------
        traffic_class : str
            Traffic class identifier

        Returns
        -------
        float
            Class utilization (0.0 to 1.0)
        """
        return self._class_utilization.get(traffic_class, 0.0)

    def reserve_bandwidth(
        self,
        traffic_class: str,
        reserved_kbps: float,
        priority: int,
    ) -> bool:
        """Reserve bandwidth for traffic class.

        Parameters
        ----------
        traffic_class : str
            Traffic class identifier
        reserved_kbps : float
            Bandwidth to reserve in Kbps
        priority : int
            Reservation priority

        Returns
        -------
        bool
            True if reservation was successful
        """
        # Check available bandwidth
        if self.get_available_bandwidth() < reserved_kbps:
            return False

        reservation = BandwidthReservation(
            traffic_class=traffic_class,
            reserved_kbps=reserved_kbps,
            priority=priority,
        )

        self._reservations[traffic_class] = reservation
        return True

    def get_available_bandwidth(self) -> float:
        """Get available bandwidth after reservations.

        Returns
        -------
        float
            Available bandwidth in Kbps
        """
        reserved_total = sum(r.reserved_kbps for r in self._reservations.values())
        return self.total_bandwidth_kbps - reserved_total

    def get_active_reservations(self) -> dict[str, dict[str, Any]]:
        """Get active bandwidth reservations.

        Returns
        -------
        dict[str, dict[str, Any]]
            Active reservations by traffic class
        """
        return {
            class_id: {
                "reserved_kbps": reservation.reserved_kbps,
                "priority": reservation.priority,
                "created_at": reservation.created_at,
            }
            for class_id, reservation in self._reservations.items()
        }


class MessageScheduler:
    """Message scheduling with weighted fair queuing."""

    def __init__(
        self,
        scheduling_algorithm: str = "weighted_fair_queuing",
        max_pending_messages: int = 1000,
        enable_preemption: bool = True,
    ) -> None:
        """Initialize message scheduler.

        Parameters
        ----------
        scheduling_algorithm : str, default "weighted_fair_queuing"
            Scheduling algorithm to use
        max_pending_messages : int, default 1000
            Maximum pending messages
        enable_preemption : bool, default True
            Enable message preemption
        """
        self.scheduling_algorithm = scheduling_algorithm
        self.max_pending_messages = max_pending_messages
        self.enable_preemption = enable_preemption

        self._scheduled_messages: list[ScheduledMessage] = []
        self._class_weights: dict[str, int] = {}
        self._class_counters: dict[str, int] = defaultdict(int)
        self._sequence_counter = 0

    def configure_class_weights(self, weights: dict[str, int]) -> None:
        """Configure weights for traffic classes.

        Parameters
        ----------
        weights : dict[str, int]
            Weights for each traffic class
        """
        self._class_weights = weights.copy()

    def schedule_message(
        self,
        message: ISOBUSMessage,
        traffic_class: str,
        preempt_lower_priority: bool = False,
    ) -> bool:
        """Schedule message for transmission.

        Parameters
        ----------
        message : ISOBUSMessage
            Message to schedule
        traffic_class : str
            Traffic class identifier
        preempt_lower_priority : bool, default False
            Whether to preempt lower priority messages

        Returns
        -------
        bool
            True if message was scheduled successfully
        """
        if len(self._scheduled_messages) >= self.max_pending_messages:
            return False

        # Get priority from traffic class
        priority_map = {
            "EMERGENCY_SAFETY": 0,
            "COLLISION_AVOIDANCE": 1,
            "FIELD_COORDINATION": 2,
            "IMPLEMENT_CONTROL": 3,
            "TELEMETRY_STREAMING": 4,
            "STATUS_UPDATES": 5,
            "DIAGNOSTICS": 6,
            "BEST_EFFORT": 7,
        }

        priority = priority_map.get(traffic_class, 7)

        scheduled_msg = ScheduledMessage(
            message=message,
            traffic_class=traffic_class,
            priority=priority,
        )

        # Handle preemption if enabled
        if preempt_lower_priority and self.enable_preemption:
            # Remove lower priority messages if high priority message arrives
            self._scheduled_messages = [
                msg for msg in self._scheduled_messages if msg.priority <= priority
            ]

        self._scheduled_messages.append(scheduled_msg)

        # Sort by priority (lower number = higher priority)
        self._scheduled_messages.sort(key=lambda x: (x.priority, x.enqueue_time))

        return preempt_lower_priority if self.enable_preemption else True

    def get_next_scheduled_message(self) -> tuple[ISOBUSMessage | None, str | None]:
        """Get next message to transmit using scheduling algorithm.

        Returns
        -------
        tuple[ISOBUSMessage | None, str | None]
            Next message and its traffic class, or (None, None) if empty
        """
        if not self._scheduled_messages:
            return None, None

        if self.scheduling_algorithm == "weighted_fair_queuing":
            return self._get_next_wfq_message()
        else:
            # Simple priority scheduling
            scheduled_msg = self._scheduled_messages.pop(0)
            return scheduled_msg.message, scheduled_msg.traffic_class

    def _get_next_wfq_message(self) -> tuple[ISOBUSMessage | None, str | None]:
        """Get next message using weighted fair queuing."""
        if not self._scheduled_messages:
            return None, None

        # Group messages by traffic class
        class_messages: dict[str, list[ScheduledMessage]] = defaultdict(list)
        for msg in self._scheduled_messages:
            class_messages[msg.traffic_class].append(msg)

        # Find class with lowest counter relative to weight
        best_class = None
        best_ratio = float("inf")

        for class_id, messages in class_messages.items():
            if not messages:
                continue

            weight = self._class_weights.get(class_id, 1)
            counter = self._class_counters[class_id]
            ratio = counter / weight if weight > 0 else float("inf")

            if ratio < best_ratio:
                best_ratio = ratio
                best_class = class_id

        if best_class is None:
            return None, None

        # Get highest priority message from selected class
        class_msgs = class_messages[best_class]
        class_msgs.sort(key=lambda x: (x.priority, x.enqueue_time))
        selected_msg = class_msgs[0]

        # Remove from scheduled messages
        self._scheduled_messages.remove(selected_msg)

        # Update counter
        self._class_counters[best_class] += 1

        return selected_msg.message, selected_msg.traffic_class


class NetworkOptimizer:
    """Network optimization and performance analysis."""

    def __init__(
        self,
        target_utilization: float = 0.75,
        optimization_interval_seconds: int = 60,
    ) -> None:
        """Initialize network optimizer.

        Parameters
        ----------
        target_utilization : float, default 0.75
            Target network utilization
        optimization_interval_seconds : int, default 60
            Optimization analysis interval
        """
        self.target_utilization = target_utilization
        self.optimization_interval_seconds = optimization_interval_seconds

        self._network_stats: dict[str, Any] = {}
        self._recommendations: list[str] = []

    def update_network_statistics(self, stats: dict[str, Any]) -> None:
        """Update network performance statistics.

        Parameters
        ----------
        stats : dict[str, Any]
            Network performance statistics
        """
        self._network_stats = stats.copy()
        self._generate_recommendations()

    def _generate_recommendations(self) -> None:
        """Generate optimization recommendations based on statistics."""
        self._recommendations.clear()

        utilization = self._network_stats.get("utilization_percentage", 0.0) / 100.0
        latency = self._network_stats.get("average_latency_ms", 0.0)
        loss_rate = self._network_stats.get("packet_loss_rate", 0.0)
        congestion_events = self._network_stats.get("congestion_events", 0)

        # Utilization recommendations
        if utilization > self.target_utilization:
            self._recommendations.append(
                f"Network utilization ({utilization:.1%}) exceeds target "
                f"({self.target_utilization:.1%}). Consider bandwidth optimization."
            )

        # Latency recommendations
        if latency > 10.0:  # More sensitive threshold for agricultural operations
            self._recommendations.append(
                f"Average latency ({latency:.1f}ms) detected. Consider priority queue adjustments."
            )

        # Loss rate recommendations
        if loss_rate > 0.01:
            self._recommendations.append(
                f"Packet loss rate ({loss_rate:.2%}) detected. Investigate congestion control."
            )

        # Congestion recommendations
        if congestion_events > 0:
            self._recommendations.append(
                f"Congestion events ({congestion_events}) detected. Enable traffic shaping."
            )

    def get_optimization_recommendations(self) -> list[str]:
        """Get optimization recommendations.

        Returns
        -------
        list[str]
            List of optimization recommendations
        """
        return self._recommendations.copy()

    def analyze_traffic_patterns(self, patterns: dict[str, Any]) -> None:
        """Analyze traffic patterns for optimization.

        Parameters
        ----------
        patterns : dict[str, Any]
            Traffic pattern analysis data
        """
        # Store patterns for analysis
        self._traffic_patterns = patterns.copy()

    def get_parameter_adjustments(self) -> dict[str, Any]:
        """Get recommended parameter adjustments.

        Returns
        -------
        dict[str, Any]
            Recommended parameter adjustments
        """
        adjustments = {
            "priority_weights": {
                "EMERGENCY_SAFETY": 40,
                "COLLISION_AVOIDANCE": 30,
                "FIELD_COORDINATION": 20,
                "IMPLEMENT_CONTROL": 15,
                "TELEMETRY_STREAMING": 10,
                "STATUS_UPDATES": 5,
                "DIAGNOSTICS": 2,
                "BEST_EFFORT": 1,
            },
            "bandwidth_allocation": {
                "EMERGENCY_SAFETY": 30.0,
                "COLLISION_AVOIDANCE": 20.0,
                "FIELD_COORDINATION": 20.0,
                "IMPLEMENT_CONTROL": 15.0,
                "TELEMETRY_STREAMING": 10.0,
                "STATUS_UPDATES": 3.0,
                "DIAGNOSTICS": 2.0,
            },
            "congestion_threshold": 0.8,
        }

        return adjustments
