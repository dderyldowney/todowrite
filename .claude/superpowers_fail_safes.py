#!/usr/bin/env python3
"""
Superpowers Fail-Safe Mechanisms

This module implements comprehensive fail-safe mechanisms for superpowers subagent execution
to prevent session locking, memory consumption issues, and resource exhaustion.

Features:
- Resource limits (memory, CPU, time)
- Session timeout protections
- Memory monitoring and cleanup
- Emergency termination capabilities
- Resource usage tracking

Author: Claude Code Assistant
Version: 2025.1.0
"""

import json
import logging
import signal
import subprocess
import sys
import threading
import time
from collections.abc import Callable
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
from pathlib import Path
from typing import Any

import psutil

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class FailSafeStatus(Enum):
    """Fail-safe status enumeration"""

    ACTIVE = "active"
    WARNING = "warning"
    CRITICAL = "critical"
    TERMINATED = "terminated"


@dataclass
class ResourceLimits:
    """Resource limits configuration"""

    max_memory_mb: int = 2048  # 2GB combined limit for all subagents
    max_cpu_percent: float = 80.0
    max_execution_time_seconds: int = 300
    max_concurrent_subagents: int = 3
    memory_check_interval_seconds: float = 5.0
    session_timeout_minutes: int = 30  # 30 minutes safety net for entire session


@dataclass
class SubagentExecution:
    """Subagent execution tracking"""

    subagent_id: str
    start_time: datetime
    process: subprocess.Popen | None = None
    thread: threading.Thread | None = None
    status: FailSafeStatus = FailSafeStatus.ACTIVE
    memory_usage_mb: float = 0.0
    cpu_usage_percent: float = 0.0
    warnings: list[str] = field(default_factory=list)


class SuperpowersFailSafes:
    """Main fail-safe manager for superpowers subagent execution"""

    def __init__(self, limits: ResourceLimits | None = None) -> None:
        """
        Initialize fail-safe manager.

        Args:
            limits: Resource limits configuration
        """
        self.limits = limits or ResourceLimits()
        self.active_subagents: dict[str, SubagentExecution] = {}
        self.monitoring_active = True
        self.session_start_time = datetime.now()
        self.total_memory_used_mb = 0.0

        # Initialize monitoring thread
        self.monitor_thread = threading.Thread(
            target=self._monitor_resources, daemon=True, name="FailSafeMonitor"
        )
        self.monitor_thread.start()

        # Setup signal handlers for emergency termination
        signal.signal(signal.SIGTERM, self._emergency_termination)
        signal.signal(signal.SIGINT, self._emergency_termination)

        logger.info("Superpowers Fail-Safes initialized")
        logger.info(f"Resource limits: {self.limits}")

    def register_subagent(self, subagent_id: str) -> bool:
        """
        Register a new subagent execution.

        Args:
            subagent_id: Unique identifier for the subagent

        Returns:
            True if registration successful, False if limits exceeded
        """
        # Check concurrent subagent limit
        if len(self.active_subagents) >= self.limits.max_concurrent_subagents:
            logger.warning(
                f"Subagent limit exceeded: {len(self.active_subagents)}/{self.limits.max_concurrent_subagents}"
            )
            return False

        # Check session timeout
        session_duration = datetime.now() - self.session_start_time
        if session_duration > timedelta(minutes=self.limits.session_timeout_minutes):
            logger.warning(f"Session timeout exceeded: {session_duration}")
            self._emergency_cleanup()
            return False

        # Create subagent execution record
        execution = SubagentExecution(subagent_id=subagent_id, start_time=datetime.now())

        self.active_subagents[subagent_id] = execution
        logger.info(f"Subagent registered: {subagent_id}")
        return True

    def update_subagent_resources(
        self, subagent_id: str, process: subprocess.Popen | None = None
    ) -> None:
        """
        Update resource usage for a specific subagent.

        Args:
            subagent_id: Subagent identifier
            process: Optional subprocess process to monitor
        """
        if subagent_id not in self.active_subagents:
            logger.warning(f"Unknown subagent: {subagent_id}")
            return

        execution = self.active_subagents[subagent_id]
        if process:
            execution.process = process

        # Get current resource usage
        try:
            current_process = psutil.Process()
            execution.memory_usage_mb = current_process.memory_info().rss / 1024 / 1024
            execution.cpu_usage_percent = current_process.cpu_percent()

            # Update total memory usage
            self.total_memory_used_mb = sum(
                exec.memory_usage_mb for exec in self.active_subagents.values()
            )

        except (psutil.NoSuchProcess, psutil.AccessDenied):
            logger.warning(f"Could not access process info for {subagent_id}")

    def check_subagent_health(self, subagent_id: str) -> FailSafeStatus:
        """
        Check health status of a specific subagent.

        Args:
            subagent_id: Subagent identifier

        Returns:
            Current health status
        """
        if subagent_id not in self.active_subagents:
            return FailSafeStatus.TERMINATED

        execution = self.active_subagents[subagent_id]

        # Check execution time
        execution_time = datetime.now() - execution.start_time
        if execution_time > timedelta(seconds=self.limits.max_execution_time_seconds):
            logger.warning(f"Subagent {subagent_id} exceeded time limit")
            execution.warnings.append("Execution time limit exceeded")
            self.terminate_subagent(subagent_id, "Time limit exceeded")
            return FailSafeStatus.TERMINATED

        # Check memory usage
        if execution.memory_usage_mb > self.limits.max_memory_mb:
            logger.warning(f"Subagent {subagent_id} exceeded memory limit")
            execution.warnings.append(f"Memory usage exceeded: {execution.memory_usage_mb:.1f}MB")

            if execution.memory_usage_mb > self.limits.max_memory_mb * 1.5:
                self.terminate_subagent(subagent_id, "Memory limit exceeded")
                return FailSafeStatus.TERMINATED
            else:
                return FailSafeStatus.WARNING

        # Check CPU usage
        if execution.cpu_usage_percent > self.limits.max_cpu_percent:
            logger.warning(f"Subagent {subagent_id} high CPU usage")
            execution.warnings.append(f"High CPU usage: {execution.cpu_usage_percent:.1f}%")
            return FailSafeStatus.WARNING

        # Check total system memory
        if self.total_memory_used_mb > self.limits.max_memory_mb:
            logger.warning(f"Total memory usage exceeded: {self.total_memory_used_mb:.1f}MB")
            return FailSafeStatus.WARNING

        return FailSafeStatus.ACTIVE

    def terminate_subagent(self, subagent_id: str, reason: str) -> bool:
        """
        Terminate a specific subagent.

        Args:
            subagent_id: Subagent identifier
            reason: Reason for termination

        Returns:
            True if termination successful
        """
        if subagent_id not in self.active_subagents:
            logger.warning(f"Cannot terminate unknown subagent: {subagent_id}")
            return False

        execution = self.active_subagents[subagent_id]
        logger.info(f"Terminating subagent {subagent_id}: {reason}")

        # Terminate process if exists
        if execution.process and execution.process.poll() is None:
            try:
                execution.process.terminate()
                # Wait a bit for graceful termination
                time.sleep(2)
                if execution.process.poll() is None:
                    execution.process.kill()
                logger.info(f"Process terminated for {subagent_id}")
            except (psutil.NoSuchProcess, OSError) as e:
                logger.warning(f"Error terminating process for {subagent_id}: {e}")

        # Mark as terminated
        execution.status = FailSafeStatus.TERMINATED
        return True

    def cleanup_subagent(self, subagent_id: str) -> None:
        """
        Clean up resources for a completed subagent.

        Args:
            subagent_id: Subagent identifier
        """
        if subagent_id not in self.active_subagents:
            return

        execution = self.active_subagents[subagent_id]

        # Log execution summary
        execution_time = datetime.now() - execution.start_time
        logger.info(f"Subagent {subagent_id} cleanup:")
        logger.info(f"  Duration: {execution_time}")
        logger.info(f"  Max memory: {execution.memory_usage_mb:.1f}MB")
        logger.info(f"  Warnings: {len(execution.warnings)}")

        # Remove from active subagents
        del self.active_subagents[subagent_id]

    def get_system_status(self) -> dict[str, Any]:
        """
        Get current system status and resource usage.

        Returns:
            System status dictionary
        """
        try:
            system_memory = psutil.virtual_memory()
            system_cpu = psutil.cpu_percent(interval=1)

            return {
                "timestamp": datetime.now().isoformat(),
                "active_subagents": len(self.active_subagents),
                "total_memory_used_mb": self.total_memory_used_mb,
                "system_memory_percent": system_memory.percent,
                "system_cpu_percent": system_cpu,
                "session_duration_minutes": (
                    datetime.now() - self.session_start_time
                ).total_seconds()
                / 60,
                "limits": {
                    "max_memory_mb": self.limits.max_memory_mb,
                    "max_cpu_percent": self.limits.max_cpu_percent,
                    "max_concurrent_subagents": self.limits.max_concurrent_subagents,
                    "session_timeout_minutes": self.limits.session_timeout_minutes,
                },
                "subagent_details": {
                    subagent_id: {
                        "status": execution.status.value,
                        "memory_mb": execution.memory_usage_mb,
                        "cpu_percent": execution.cpu_usage_percent,
                        "warnings": execution.warnings,
                        "duration_seconds": (datetime.now() - execution.start_time).total_seconds(),
                    }
                    for subagent_id, execution in self.active_subagents.items()
                },
            }
        except Exception as e:
            logger.error(f"Error getting system status: {e}")
            return {"error": str(e), "timestamp": datetime.now().isoformat()}

    def _monitor_resources(self) -> None:
        """Background thread for resource monitoring."""
        while self.monitoring_active:
            try:
                # Check each active subagent
                for subagent_id in list(self.active_subagents.keys()):
                    status = self.check_subagent_health(subagent_id)

                    if status == FailSafeStatus.TERMINATED:
                        self.cleanup_subagent(subagent_id)

                # Check overall system limits
                if self.total_memory_used_mb > self.limits.max_memory_mb:
                    logger.warning("System memory limit exceeded, terminating oldest subagent")
                    oldest_subagent = min(
                        self.active_subagents.items(), key=lambda x: x[1].start_time
                    )[0]
                    self.terminate_subagent(oldest_subagent, "System memory limit exceeded")

                time.sleep(self.limits.memory_check_interval_seconds)

            except Exception as e:
                logger.error(f"Error in resource monitoring: {e}")
                time.sleep(self.limits.memory_check_interval_seconds)

    def _emergency_termination(self, signum: int, frame) -> None:
        """Emergency termination signal handler."""
        logger.warning("Emergency termination triggered")
        self.monitoring_active = False

        # Terminate all active subagents
        for subagent_id in list(self.active_subagents.keys()):
            self.terminate_subagent(subagent_id, "Emergency termination")
            self.cleanup_subagent(subagent_id)

        sys.exit(1)

    def _emergency_cleanup(self) -> None:
        """Emergency cleanup for resource exhaustion."""
        logger.warning("Emergency cleanup triggered")

        # Terminate all subagents
        for subagent_id in list(self.active_subagents.keys()):
            self.terminate_subagent(subagent_id, "Emergency cleanup")

    def shutdown(self) -> None:
        """Graceful shutdown of fail-safe manager."""
        logger.info("Shutting down Superpowers Fail-Safes")
        self.monitoring_active = False

        # Wait for all subagents to complete or terminate them
        for subagent_id in list(self.active_subagents.keys()):
            self.terminate_subagent(subagent_id, "Shutdown")
            self.cleanup_subagent(subagent_id)

        # Wait for monitoring thread to finish
        if self.monitor_thread.is_alive():
            self.monitor_thread.join(timeout=5)

        logger.info("Superpowers Fail-Safes shutdown complete")


# Global fail-safe instance
_fail_safe_instance: SuperpowersFailSafes | None = None


def get_fail_safes() -> SuperpowersFailSafes:
    """Get or create global fail-safe instance."""
    global _fail_safe_instance
    if _fail_safe_instance is None:
        _fail_safe_instance = SuperpowersFailSafes()
    return _fail_safe_instance


def with_fail_safes(subagent_name: str) -> Callable:
    """
    Decorator for running functions with fail-safe protection.

    Args:
        subagent_name: Name of the subagent for tracking

    Returns:
        Decorated function with fail-safe protection
    """

    def decorator(func: Callable) -> Callable:
        def wrapper(*args, **kwargs) -> Any:
            fail_safes = get_fail_safes()

            # Generate unique subagent ID
            subagent_id = f"{subagent_name}_{int(time.time())}"

            if not fail_safes.register_subagent(subagent_id):
                raise RuntimeError(f"Failed to register subagent: {subagent_id}")

            try:
                # Update resource tracking
                fail_safes.update_subagent_resources(subagent_id)

                # Check health before execution
                status = fail_safes.check_subagent_health(subagent_id)
                if status == FailSafeStatus.TERMINATED:
                    raise RuntimeError(f"Subagent {subagent_id} terminated before execution")

                # Execute function
                result = func(*args, **kwargs)

                return result

            except Exception as e:
                logger.error(f"Subagent {subagent_id} execution failed: {e}")
                raise

            finally:
                # Always cleanup
                fail_safes.cleanup_subagent(subagent_id)

        return wrapper

    return decorator


def save_fail_safe_report(file_path: Path) -> None:
    """
    Save fail-safe status report to file.

    Args:
        file_path: Path to save report
    """
    fail_safes = get_fail_safes()
    status = fail_safes.get_system_status()

    try:
        with open(file_path, "w") as f:
            json.dump(status, f, indent=2, default=str)
        logger.info(f"Fail-safe report saved to {file_path}")
    except Exception as e:
        logger.error(f"Error saving fail-safe report: {e}")


if __name__ == "__main__":
    # Test fail-safe mechanisms
    print("Testing Superpowers Fail-Safes...")

    fail_safes = SuperpowersFailSafes()

    # Test subagent registration
    subagent_id = "test_subagent"
    if fail_safes.register_subagent(subagent_id):
        print(f"✅ Subagent {subagent_id} registered")

        # Update resources
        fail_safes.update_subagent_resources(subagent_id)

        # Check health
        status = fail_safes.check_subagent_health(subagent_id)
        print(f"✅ Health status: {status.value}")

        # Get system status
        system_status = fail_safes.get_system_status()
        print(f"✅ System status: {system_status['active_subagents']} active subagents")

        # Cleanup
        fail_safes.cleanup_subagent(subagent_id)
        print(f"✅ Subagent {subagent_id} cleaned up")

    # Save report
    save_fail_safe_report(Path("fail_safe_report.json"))

    print("✅ Fail-safe testing complete")
