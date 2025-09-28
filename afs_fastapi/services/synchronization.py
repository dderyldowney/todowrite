"""Distributed Systems Synchronization Components for Agricultural Robotics.

This module implements vector clocks and related distributed systems primitives
for coordinating multi-tractor operations in agricultural environments.

Vector clocks provide causal ordering of events across distributed tractors
without requiring centralized coordination, essential for field operations
with intermittent network connectivity.

Agricultural Context:
- Multiple tractors operating simultaneously in the same field
- Network connectivity may be intermittent in rural areas
- Operations must be correctly sequenced for safety and efficiency
- ISOBUS protocol constraints require efficient timestamp encoding
"""

import copy


class VectorClock:
    """Vector Clock implementation for distributed tractor coordination.

    A vector clock is a logical clock that provides causal ordering of events
    in a distributed system. Each process (tractor) maintains a vector of
    logical timestamps, one for each process in the system.

    Agricultural Use Case:
    When multiple tractors work the same field, vector clocks ensure that
    operations like "tractor A finished section 1" → "tractor B started section 2"
    are properly ordered even if messages arrive out of order due to network delays.

    Attributes:
        _clocks: Dictionary mapping process IDs to logical timestamps
        _process_ids: Set of all known process IDs in the system

    """

    def __init__(self, process_ids: list[str]) -> None:
        """Initialize vector clock for given set of processes.

        Args:
            process_ids: List of process identifiers (e.g., tractor IDs)

        Raises:
            ValueError: If process_ids is empty or contains duplicates

        Agricultural Context:
        Process IDs typically represent tractors: ["tractor_001", "tractor_002", ...]

        """
        if not process_ids:
            msg = "Process IDs list cannot be empty"
            raise ValueError(msg)

        # Remove duplicates and validate
        unique_ids = list(set(process_ids))
        if len(unique_ids) != len(process_ids):
            msg = "Process IDs list contains duplicates"
            raise ValueError(msg)

        self._process_ids: set[str] = set(unique_ids)
        self._clocks: dict[str, int] = dict.fromkeys(unique_ids, 0)

    def get_time(self, process_id: str) -> int:
        """Get logical timestamp for specified process.

        Args:
            process_id: Process identifier to query

        Returns:
            Current logical timestamp for the process

        Raises:
            ValueError: If process_id is not known to this clock

        """
        if process_id not in self._process_ids:
            msg = f"Process ID '{process_id}' not found in clock"
            raise ValueError(msg)
        return self._clocks[process_id]

    def get_process_ids(self) -> list[str]:
        """Get list of all process IDs tracked by this clock.

        Returns:
            List of process identifiers (tractor IDs)

        """
        return list(self._process_ids)

    def increment(self, process_id: str) -> None:
        """Increment logical clock for local event.

        Args:
            process_id: Process that experienced the local event

        Raises:
            ValueError: If process_id is not known to this clock

        Agricultural Context:
        Called when a tractor performs a local operation like:
        - Starting/stopping engine
        - Beginning work on a field section
        - Completing a planting/harvesting task

        """
        if process_id not in self._process_ids:
            msg = f"Process ID '{process_id}' not found in clock"
            raise ValueError(msg)
        self._clocks[process_id] += 1

    def update_with_received_message(
        self, receiving_process: str, sender_clock: "VectorClock"
    ) -> None:
        """Update clock when receiving message from another process.

        This implements the vector clock update rule:
        1. For each process, take max of current time and received time
        2. Increment the receiving process's clock

        Args:
            receiving_process: Process ID that received the message
            sender_clock: Vector clock timestamp from message sender

        Agricultural Context:
        Called when a tractor receives an ISOBUS message containing
        another tractor's vector clock timestamp. This maintains
        causal ordering across the fleet.

        """
        if receiving_process not in self._process_ids:
            msg = f"Process ID '{receiving_process}' not found in clock"
            raise ValueError(msg)

        # Update rule: take max of current and received time for each process
        for process_id in self._process_ids:
            if process_id in sender_clock._clocks:
                self._clocks[process_id] = max(
                    self._clocks[process_id],
                    sender_clock._clocks[process_id],
                )

        # Increment receiving process's clock (local event)
        self._clocks[receiving_process] += 1

    def happens_before(self, other: "VectorClock") -> bool:
        """Determine if this clock's events happen before other clock's events.

        Vector clock A happens before B if:
        - For all processes: A[i] <= B[i]
        - For at least one process: A[i] < B[i]

        Args:
            other: Vector clock to compare against

        Returns:
            True if this clock happens before other clock

        Agricultural Context:
        Used to determine if one tractor's operations causally precede
        another's. Critical for maintaining proper work sequencing.

        """
        # Check if all timestamps are <= corresponding timestamps in other
        all_less_equal = all(
            self._clocks.get(pid, 0) <= other._clocks.get(pid, 0)
            for pid in self._process_ids.union(other._process_ids)
        )

        # Check if at least one timestamp is strictly less
        at_least_one_less = any(
            self._clocks.get(pid, 0) < other._clocks.get(pid, 0)
            for pid in self._process_ids.union(other._process_ids)
        )

        return all_less_equal and at_least_one_less

    def is_concurrent_with(self, other: "VectorClock") -> bool:
        """Determine if events are concurrent (no causal relationship).

        Events are concurrent if neither happens before the other.

        Args:
            other: Vector clock to compare against

        Returns:
            True if events are concurrent

        Agricultural Context:
        Concurrent events indicate independent operations that can
        be performed simultaneously without coordination, such as
        tractors working different field sections.

        """
        return not self.happens_before(other) and not other.happens_before(self)

    def to_dict(self) -> dict[str, int]:
        """Serialize vector clock to dictionary for transmission.

        Returns:
            Dictionary mapping process IDs to timestamps

        Agricultural Context:
        Used to include vector clock in ISOBUS messages for
        distributed coordination. Must be efficient due to
        ISO 11783 message size constraints.

        """
        return copy.deepcopy(self._clocks)

    @classmethod
    def from_dict(cls, clock_dict: dict[str, int], process_ids: list[str]) -> "VectorClock":
        """Deserialize vector clock from dictionary.

        Args:
            clock_dict: Dictionary mapping process IDs to timestamps
            process_ids: List of expected process IDs

        Returns:
            Reconstructed VectorClock instance

        Agricultural Context:
        Used to reconstruct vector clock from received ISOBUS messages.

        """
        clock = cls(process_ids)
        for process_id, timestamp in clock_dict.items():
            if process_id in clock._process_ids:
                clock._clocks[process_id] = timestamp
        return clock

    def __str__(self) -> str:
        """Return string representation of vector clock."""
        return f"VectorClock({dict(sorted(self._clocks.items()))})"

    def __repr__(self) -> str:
        """Detailed string representation for debugging."""
        return f"VectorClock(process_ids={sorted(self._process_ids)}, clocks={self._clocks})"
