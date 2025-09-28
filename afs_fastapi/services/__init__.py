"""AFS FastAPI Services Module.

Business logic and coordination services for agricultural robotics platform.
This module contains distributed systems components for multi-tractor
fleet coordination and synchronization.
"""

from .synchronization import VectorClock

__all__ = ["VectorClock"]
