"""
Production-grade CAN bus connection manager for agricultural fleet operations.

This module provides enterprise-level CAN bus connection management with features
like connection pooling, automatic failover, health monitoring, message routing,
and comprehensive diagnostics for real-world agricultural deployments.

Implementation follows Test-First Development (TDD) GREEN phase.
"""

from __future__ import annotations

import asyncio
import logging
from collections import defaultdict
from collections.abc import Callable
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
from typing import Any

import can

from afs_fastapi.core.can_frame_codec import CANFrameCodec, DecodedPGN
from afs_fastapi.equipment.can_error_handling import CANErrorHandler, ISOBUSErrorLogger
from afs_fastapi.equipment.physical_can_interface import (
    InterfaceConfiguration,
    InterfaceState,
    PhysicalCANManager,
)

# Configure logging for CAN bus manager
logger = logging.getLogger(__name__)


class ManagerState(Enum):
    """CAN bus manager operational states."""

    INITIALIZING = "initializing"
    RUNNING = "running"
    DEGRADED = "degraded"  # Some interfaces failed
    FAILOVER = "failover"  # Primary interfaces failed, using backup
    MAINTENANCE = "maintenance"
    STOPPED = "stopped"
    ERROR = "error"


class MessagePriority(Enum):
    """Message priority levels for routing."""

    CRITICAL = 0  # Emergency, safety
    HIGH = 1  # Engine, transmission critical
    NORMAL = 2  # Standard telemetry
    LOW = 3  # Diagnostics, configuration


@dataclass
class RoutingRule:
    """Message routing rule configuration."""

    name: str
    pgn_filters: list[int]
    source_filters: list[int]
    destination_filters: list[int]
    priority: MessagePriority
    target_interfaces: list[str]
    enabled: bool = True
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class ConnectionPoolConfig:
    """Configuration for CAN interface connection pool."""

    primary_interfaces: list[str]
    backup_interfaces: list[str]
    max_connections_per_interface: int = 1
    health_check_interval: float = 5.0
    failover_timeout: float = 30.0
    auto_recovery: bool = True
    load_balancing: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class ManagerStatistics:
    """CAN bus manager operational statistics."""

    manager_state: ManagerState
    uptime: timedelta
    total_messages_processed: int = 0
    messages_routed: int = 0
    messages_dropped: int = 0
    failover_events: int = 0
    active_interfaces: int = 0
    failed_interfaces: int = 0
    last_health_check: datetime = field(default_factory=datetime.now)
    performance_metrics: dict[str, float] = field(default_factory=dict)


class MessageRouter:
    """Intelligent message routing for agricultural CAN networks."""

    def __init__(self, codec: CANFrameCodec) -> None:
        """Initialize message router.

        Parameters
        ----------
        codec : CANFrameCodec
            CAN frame codec for message parsing
        """
        self.codec = codec
        self.routing_rules: list[RoutingRule] = []
        self.message_stats: dict[int, int] = defaultdict(int)  # PGN -> count
        self.route_cache: dict[int, list[str]] = {}  # PGN -> interface list

    def add_routing_rule(self, rule: RoutingRule) -> None:
        """Add a message routing rule.

        Parameters
        ----------
        rule : RoutingRule
            Routing rule to add
        """
        self.routing_rules.append(rule)
        logger.info(f"Added routing rule: {rule.name}")

    def remove_routing_rule(self, rule_name: str) -> bool:
        """Remove a routing rule by name.

        Parameters
        ----------
        rule_name : str
            Name of rule to remove

        Returns
        -------
        bool
            True if rule was removed
        """
        for i, rule in enumerate(self.routing_rules):
            if rule.name == rule_name:
                del self.routing_rules[i]
                logger.info(f"Removed routing rule: {rule_name}")
                return True
        return False

    def route_message(
        self, message: can.Message, available_interfaces: list[str]
    ) -> tuple[list[str], MessagePriority]:
        """Route a CAN message to appropriate interfaces.

        Parameters
        ----------
        message : can.Message
            CAN message to route
        available_interfaces : List[str]
            Available interface names

        Returns
        -------
        Tuple[List[str], MessagePriority]
            (target_interfaces, message_priority)
        """
        # Decode message to get PGN
        decoded = self.codec.decode_message(message)
        if not decoded:
            return available_interfaces, MessagePriority.LOW

        pgn = decoded.pgn
        source_address = decoded.source_address

        # Update statistics
        self.message_stats[pgn] += 1

        # Check cache first
        if pgn in self.route_cache:
            cached_interfaces = [
                iface for iface in self.route_cache[pgn] if iface in available_interfaces
            ]
            if cached_interfaces:
                return cached_interfaces, self._get_pgn_priority(pgn)

        # Apply routing rules
        target_interfaces = []
        message_priority = MessagePriority.NORMAL

        for rule in self.routing_rules:
            if not rule.enabled:
                continue

            # Check PGN filter
            if rule.pgn_filters and pgn not in rule.pgn_filters:
                continue

            # Check source filter
            if rule.source_filters and source_address not in rule.source_filters:
                continue

            # Check destination filter (if applicable)
            if (
                rule.destination_filters
                and decoded.destination_address not in rule.destination_filters
            ):
                continue

            # Rule matches - add target interfaces
            for interface in rule.target_interfaces:
                if interface in available_interfaces and interface not in target_interfaces:
                    target_interfaces.append(interface)

            # Use highest priority found
            if rule.priority.value < message_priority.value:
                message_priority = rule.priority

        # If no rules matched, use all available interfaces
        if not target_interfaces:
            target_interfaces = available_interfaces

        # Cache the result
        self.route_cache[pgn] = target_interfaces

        return target_interfaces, message_priority

    def _get_pgn_priority(self, pgn: int) -> MessagePriority:
        """Get priority level for a PGN.

        Parameters
        ----------
        pgn : int
            Parameter Group Number

        Returns
        -------
        MessagePriority
            Message priority level
        """
        # Critical PGNs (safety, emergency)
        critical_pgns = {0xE001, 0xE002, 0xE003}  # Emergency, safety, collision
        if pgn in critical_pgns:
            return MessagePriority.CRITICAL

        # High priority PGNs (engine, transmission)
        high_priority_pgns = {0xF004, 0xF005, 0xFEF1}  # EEC1, ETC1, WVS
        if pgn in high_priority_pgns:
            return MessagePriority.HIGH

        # Diagnostic PGNs
        diagnostic_pgns = {0xFECA, 0xFECB, 0xFECC}  # DM1, DM2, DM3
        if pgn in diagnostic_pgns:
            return MessagePriority.LOW

        return MessagePriority.NORMAL

    def get_routing_statistics(self) -> dict[str, Any]:
        """Get routing statistics.

        Returns
        -------
        Dict[str, Any]
            Routing statistics
        """
        return {
            "total_rules": len(self.routing_rules),
            "active_rules": len([r for r in self.routing_rules if r.enabled]),
            "message_stats": dict(self.message_stats),
            "cache_size": len(self.route_cache),
        }


class ConnectionPool:
    """Connection pool manager for CAN interfaces."""

    def __init__(
        self,
        config: ConnectionPoolConfig,
        physical_manager: PhysicalCANManager,
        error_handler: CANErrorHandler,
    ) -> None:
        """Initialize connection pool.

        Parameters
        ----------
        config : ConnectionPoolConfig
            Pool configuration
        physical_manager : PhysicalCANManager
            Physical interface manager
        error_handler : CANErrorHandler
            Error handling system
        """
        self.config = config
        self.physical_manager = physical_manager
        self.error_handler = error_handler

        self.primary_connections: dict[str, bool] = {}  # interface_id -> is_connected
        self.backup_connections: dict[str, bool] = {}
        self.connection_health: dict[str, float] = {}  # interface_id -> health_score (0-1)
        self.last_health_check: dict[str, datetime] = {}

        self._health_check_task: asyncio.Task | None = None
        self._failover_in_progress = False

    async def initialize(self) -> bool:
        """Initialize the connection pool.

        Returns
        -------
        bool
            True if initialization successful
        """
        try:
            # Initialize primary connections
            for interface_id in self.config.primary_interfaces:
                success = await self.physical_manager.connect_interface(interface_id)
                self.primary_connections[interface_id] = success
                self.connection_health[interface_id] = 1.0 if success else 0.0
                self.last_health_check[interface_id] = datetime.now()

            # Initialize backup connections if auto-recovery enabled
            if self.config.auto_recovery:
                for interface_id in self.config.backup_interfaces:
                    success = await self.physical_manager.connect_interface(interface_id)
                    self.backup_connections[interface_id] = success
                    self.connection_health[interface_id] = 1.0 if success else 0.0
                    self.last_health_check[interface_id] = datetime.now()

            # Start health checking
            self._health_check_task = asyncio.create_task(self._health_check_loop())

            logger.info(
                f"Connection pool initialized with {len(self.primary_connections)} primary interfaces"
            )
            return True

        except Exception as e:
            logger.error(f"Failed to initialize connection pool: {e}")
            return False

    async def shutdown(self) -> None:
        """Shutdown the connection pool."""
        if self._health_check_task:
            self._health_check_task.cancel()
            try:
                await self._health_check_task
            except asyncio.CancelledError:
                pass

        # Disconnect all interfaces
        await self.physical_manager.disconnect_all()

    def get_active_interfaces(self) -> list[str]:
        """Get list of currently active interface IDs.

        Returns
        -------
        List[str]
            Active interface IDs
        """
        active = []

        # Check primary interfaces first
        for interface_id, is_connected in self.primary_connections.items():
            if is_connected and self.connection_health.get(interface_id, 0) > 0.5:
                active.append(interface_id)

        # If no primary interfaces, use backup
        if not active and self.config.auto_recovery:
            for interface_id, is_connected in self.backup_connections.items():
                if is_connected and self.connection_health.get(interface_id, 0) > 0.5:
                    active.append(interface_id)

        return active

    def get_best_interface(self, exclude: list[str] | None = None) -> str | None:
        """Get the best available interface based on health score.

        Parameters
        ----------
        exclude : Optional[List[str]]
            Interface IDs to exclude

        Returns
        -------
        Optional[str]
            Best interface ID or None
        """
        exclude = exclude or []
        active_interfaces = [
            iface for iface in self.get_active_interfaces() if iface not in exclude
        ]

        if not active_interfaces:
            return None

        # Return interface with highest health score
        return max(active_interfaces, key=lambda iface: self.connection_health.get(iface, 0))

    async def _health_check_loop(self) -> None:
        """Background health checking loop."""
        while True:
            try:
                await self._perform_health_checks()
                await asyncio.sleep(self.config.health_check_interval)
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"Health check error: {e}")
                await asyncio.sleep(self.config.health_check_interval)

    async def _perform_health_checks(self) -> None:
        """Perform health checks on all connections."""
        current_time = datetime.now()

        # Check all interfaces
        all_interfaces = list(self.primary_connections.keys()) + list(
            self.backup_connections.keys()
        )

        for interface_id in all_interfaces:
            try:
                # Get interface status
                status = self.physical_manager.get_interface_status(interface_id)

                if status:
                    # Calculate health score based on various factors
                    health_score = self._calculate_health_score(status)
                    self.connection_health[interface_id] = health_score

                    # Update connection status
                    is_healthy = health_score > 0.5
                    if interface_id in self.primary_connections:
                        self.primary_connections[interface_id] = is_healthy
                    if interface_id in self.backup_connections:
                        self.backup_connections[interface_id] = is_healthy

                else:
                    # Interface not found or failed
                    self.connection_health[interface_id] = 0.0
                    if interface_id in self.primary_connections:
                        self.primary_connections[interface_id] = False
                    if interface_id in self.backup_connections:
                        self.backup_connections[interface_id] = False

                self.last_health_check[interface_id] = current_time

            except Exception as e:
                logger.warning(f"Health check failed for {interface_id}: {e}")
                self.connection_health[interface_id] = 0.0

        # Check if failover is needed
        active_primary = any(self.primary_connections.values())
        if not active_primary and not self._failover_in_progress:
            await self._trigger_failover()

    def _calculate_health_score(self, status) -> float:
        """Calculate health score for an interface.

        Parameters
        ----------
        status : InterfaceStatus
            Interface status information

        Returns
        -------
        float
            Health score (0.0 to 1.0)
        """
        score = 1.0

        # Penalize for state issues
        if status.state != InterfaceState.CONNECTED:
            score *= 0.3

        # Penalize for high error rates
        if status.errors_total > 0 and (status.messages_sent + status.messages_received) > 0:
            total_messages = status.messages_sent + status.messages_received
            error_rate = status.errors_total / total_messages
            score *= max(0.1, 1.0 - error_rate * 5)  # Reduce score based on error rate

        # Penalize for high bus load
        if status.bus_load_percentage > 80:
            score *= 0.7
        elif status.bus_load_percentage > 60:
            score *= 0.9

        # Bonus for recent activity
        time_since_update = datetime.now() - status.last_heartbeat
        if time_since_update.total_seconds() > 30:
            score *= 0.5

        return max(0.0, min(1.0, score))

    async def _trigger_failover(self) -> None:
        """Trigger failover to backup interfaces."""
        if not self.config.auto_recovery:
            return

        self._failover_in_progress = True
        logger.warning("Triggering failover to backup interfaces")

        try:
            # Attempt to activate backup interfaces
            for interface_id in self.config.backup_interfaces:
                if not self.backup_connections.get(interface_id, False):
                    success = await self.physical_manager.connect_interface(interface_id)
                    if success:
                        self.backup_connections[interface_id] = True
                        self.connection_health[interface_id] = 1.0
                        logger.info(f"Activated backup interface: {interface_id}")

        finally:
            self._failover_in_progress = False


class CANBusConnectionManager:
    """Production-grade CAN bus connection manager for agricultural operations."""

    def __init__(
        self,
        pool_config: ConnectionPoolConfig,
        error_handler: CANErrorHandler | None = None,
        error_logger: ISOBUSErrorLogger | None = None,
    ) -> None:
        """Initialize CAN bus connection manager.

        Parameters
        ----------
        pool_config : ConnectionPoolConfig
            Connection pool configuration
        error_handler : Optional[CANErrorHandler]
            Error handling system
        error_logger : Optional[ISOBUSErrorLogger]
            Error logging system
        """
        self.pool_config = pool_config
        self.error_handler = error_handler or CANErrorHandler()
        self.error_logger = error_logger or ISOBUSErrorLogger()

        # Core components
        self.codec = CANFrameCodec()
        self.physical_manager = PhysicalCANManager(self.error_handler, self.error_logger)
        self.connection_pool = ConnectionPool(
            pool_config, self.physical_manager, self.error_handler
        )
        self.message_router = MessageRouter(self.codec)

        # State management
        self._state = ManagerState.INITIALIZING
        self._start_time = datetime.now()
        self._statistics = ManagerStatistics(
            manager_state=self._state,
            uptime=timedelta(),
        )

        # Message handling
        self._message_callbacks: list[Callable[[DecodedPGN, str], None]] = []
        self._message_queue: asyncio.Queue = asyncio.Queue(maxsize=1000)
        self._processing_task: asyncio.Task | None = None

        # Monitoring
        self._monitor_task: asyncio.Task | None = None

    async def initialize(self) -> bool:
        """Initialize the CAN bus connection manager.

        Returns
        -------
        bool
            True if initialization successful
        """
        try:
            logger.info("Initializing CAN bus connection manager")
            self._state = ManagerState.INITIALIZING

            # Initialize connection pool
            pool_success = await self.connection_pool.initialize()
            if not pool_success:
                self._state = ManagerState.ERROR
                return False

            # Setup default routing rules
            self._setup_default_routing_rules()

            # Start message processing
            self._processing_task = asyncio.create_task(self._message_processing_loop())

            # Start monitoring
            self._monitor_task = asyncio.create_task(self._monitoring_loop())

            # Add global message callback to physical manager
            self.physical_manager.add_global_callback(self._handle_incoming_message)

            self._state = ManagerState.RUNNING
            logger.info("CAN bus connection manager initialized successfully")
            return True

        except Exception as e:
            logger.error(f"Failed to initialize CAN bus manager: {e}")
            self._state = ManagerState.ERROR
            return False

    async def shutdown(self) -> None:
        """Shutdown the CAN bus connection manager."""
        logger.info("Shutting down CAN bus connection manager")
        self._state = ManagerState.STOPPED

        # Stop processing tasks
        if self._processing_task:
            self._processing_task.cancel()
        if self._monitor_task:
            self._monitor_task.cancel()

        # Shutdown connection pool
        await self.connection_pool.shutdown()

        logger.info("CAN bus connection manager shutdown complete")

    def add_message_callback(self, callback: Callable[[DecodedPGN, str], None]) -> None:
        """Add callback for processed CAN messages.

        Parameters
        ----------
        callback : Callable[[DecodedPGN, str], None]
            Callback function (decoded_message, interface_id)
        """
        self._message_callbacks.append(callback)

    def remove_message_callback(self, callback: Callable[[DecodedPGN, str], None]) -> None:
        """Remove message callback.

        Parameters
        ----------
        callback : Callable[[DecodedPGN, str], None]
            Callback function to remove
        """
        if callback in self._message_callbacks:
            self._message_callbacks.remove(callback)

    async def send_message(
        self,
        message: can.Message,
        target_interfaces: list[str] | None = None,
        priority: MessagePriority = MessagePriority.NORMAL,
    ) -> dict[str, bool]:
        """Send CAN message through managed interfaces.

        Parameters
        ----------
        message : can.Message
            CAN message to send
        target_interfaces : Optional[List[str]]
            Specific interfaces to use (None for auto-routing)
        priority : MessagePriority
            Message priority level

        Returns
        -------
        Dict[str, bool]
            Send results by interface ID
        """
        try:
            # Auto-route if no specific interfaces provided
            if target_interfaces is None:
                available_interfaces = self.connection_pool.get_active_interfaces()
                target_interfaces, priority = self.message_router.route_message(
                    message, available_interfaces
                )

            # Send to target interfaces
            results = {}
            for interface_id in target_interfaces:
                interface = self.physical_manager._interfaces.get(interface_id)
                if interface:
                    success = await interface.send_message(message)
                    results[interface_id] = success
                    if success:
                        self._statistics.messages_routed += 1
                    else:
                        self._statistics.messages_dropped += 1
                else:
                    results[interface_id] = False
                    self._statistics.messages_dropped += 1

            return results

        except Exception as e:
            logger.error(f"Failed to send message: {e}")
            return {}

    def _handle_incoming_message(self, message: can.Message, interface_id: str) -> None:
        """Handle incoming CAN message.

        Parameters
        ----------
        message : can.Message
            Received CAN message
        interface_id : str
            Interface that received the message
        """
        try:
            # Queue message for processing
            self._message_queue.put_nowait((message, interface_id))
            self._statistics.total_messages_processed += 1

        except asyncio.QueueFull:
            logger.warning("Message queue full, dropping message")
            self._statistics.messages_dropped += 1

    async def _message_processing_loop(self) -> None:
        """Background message processing loop."""
        while self._state in [ManagerState.RUNNING, ManagerState.DEGRADED, ManagerState.FAILOVER]:
            try:
                # Get message from queue
                message, interface_id = await asyncio.wait_for(
                    self._message_queue.get(), timeout=1.0
                )

                # Decode message
                decoded = self.codec.decode_message(message)
                if decoded:
                    # Call registered callbacks
                    for callback in self._message_callbacks:
                        try:
                            callback(decoded, interface_id)
                        except Exception as e:
                            logger.error(f"Message callback error: {e}")

            except TimeoutError:
                continue
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"Message processing error: {e}")

    async def _monitoring_loop(self) -> None:
        """Background monitoring and state management loop."""
        while self._state != ManagerState.STOPPED:
            try:
                # Update statistics
                self._update_statistics()

                # Check overall health
                self._check_overall_health()

                await asyncio.sleep(5.0)  # Monitor every 5 seconds

            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"Monitoring error: {e}")

    def _update_statistics(self) -> None:
        """Update manager statistics."""
        self._statistics.uptime = datetime.now() - self._start_time
        self._statistics.manager_state = self._state

        # Count active/failed interfaces
        active_interfaces = self.connection_pool.get_active_interfaces()
        self._statistics.active_interfaces = len(active_interfaces)

        all_interfaces = list(self.connection_pool.primary_connections.keys()) + list(
            self.connection_pool.backup_connections.keys()
        )
        self._statistics.failed_interfaces = (
            len(all_interfaces) - self._statistics.active_interfaces
        )

    def _check_overall_health(self) -> None:
        """Check overall manager health and update state."""
        active_interfaces = self.connection_pool.get_active_interfaces()
        primary_active = any(self.connection_pool.primary_connections.values())

        if not active_interfaces:
            self._state = ManagerState.ERROR
        elif not primary_active and self.pool_config.auto_recovery:
            self._state = ManagerState.FAILOVER
        elif len(active_interfaces) < len(self.pool_config.primary_interfaces):
            self._state = ManagerState.DEGRADED
        else:
            self._state = ManagerState.RUNNING

    def _setup_default_routing_rules(self) -> None:
        """Setup default routing rules for agricultural operations."""
        # Emergency/safety messages - all interfaces
        emergency_rule = RoutingRule(
            name="Emergency Safety",
            pgn_filters=[0xE001, 0xE002, 0xE003],  # Emergency, safety, collision
            source_filters=[],
            destination_filters=[],
            priority=MessagePriority.CRITICAL,
            target_interfaces=self.pool_config.primary_interfaces
            + self.pool_config.backup_interfaces,
        )

        # Engine/transmission critical - primary interfaces
        critical_rule = RoutingRule(
            name="Engine Transmission Critical",
            pgn_filters=[0xF004, 0xF005],  # EEC1, ETC1
            source_filters=[],
            destination_filters=[],
            priority=MessagePriority.HIGH,
            target_interfaces=self.pool_config.primary_interfaces,
        )

        # Standard telemetry - load balanced
        telemetry_rule = RoutingRule(
            name="Standard Telemetry",
            pgn_filters=[0xFEF1, 0xFEF2, 0xFEF3],  # WVS, LFE, VP
            source_filters=[],
            destination_filters=[],
            priority=MessagePriority.NORMAL,
            target_interfaces=self.pool_config.primary_interfaces,
        )

        # Add rules to router
        self.message_router.add_routing_rule(emergency_rule)
        self.message_router.add_routing_rule(critical_rule)
        self.message_router.add_routing_rule(telemetry_rule)

    def get_manager_status(self) -> dict[str, Any]:
        """Get comprehensive manager status.

        Returns
        -------
        Dict[str, Any]
            Manager status information
        """
        return {
            "state": self._state.value,
            "uptime": self._statistics.uptime.total_seconds(),
            "statistics": {
                "total_messages": self._statistics.total_messages_processed,
                "messages_routed": self._statistics.messages_routed,
                "messages_dropped": self._statistics.messages_dropped,
                "active_interfaces": self._statistics.active_interfaces,
                "failed_interfaces": self._statistics.failed_interfaces,
            },
            "connection_pool": {
                "primary_interfaces": dict(self.connection_pool.primary_connections),
                "backup_interfaces": dict(self.connection_pool.backup_connections),
                "health_scores": dict(self.connection_pool.connection_health),
            },
            "routing": self.message_router.get_routing_statistics(),
        }

    def get_active_interfaces(self) -> list[str]:
        """Get list of currently active interfaces.

        Returns
        -------
        List[str]
            Active interface IDs
        """
        return self.connection_pool.get_active_interfaces()

    async def create_interface(self, interface_id: str, config: InterfaceConfiguration) -> bool:
        """Create and configure a new CAN interface.

        Parameters
        ----------
        interface_id : str
            Unique interface identifier
        config : InterfaceConfiguration
            Interface configuration

        Returns
        -------
        bool
            True if interface created successfully
        """
        try:
            interface = await self.physical_manager.create_interface(interface_id, config)
            return interface is not None

        except Exception as e:
            logger.error(f"Failed to create interface {interface_id}: {e}")
            return False
