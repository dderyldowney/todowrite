from __future__ import annotations

"""Core ToDoWrite functionality - Clean separation of models and types."""

# Re-export only what's needed for the core module interface
# Models should be imported from todowrite.core.models, not from todowrite.core
from .models import Base
from .types import LayerType, StatusType

__all__ = [
    # Core essentials only - models imported from todowrite.core.models
    "Base",
    # Type definitions
    "LayerType",
    "StatusType",
]
