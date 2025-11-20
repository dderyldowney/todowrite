"""Core ToDoWrite functionality - Clean separation of models and types."""

# SQLAlchemy Models - ONLY from todowrite.core.models
from .models import (
    AcceptanceCriteria,
    Base,
    Command,
    Concept,
    Constraints,
    Context,
    Goal,
    InterfaceContract,
    Label,
    Phase,
    Requirements,
    Step,
    SubTask,
    Task,
)

# Type definitions - ONLY from todowrite.core.types
from .types import (
    LayerType,
    StatusType,
)

__all__ = [
    # SQLAlchemy Models (12 layers + Base)
    "AcceptanceCriteria",
    "Base",
    "Command",
    "Concept",
    "Constraints",
    "Context",
    "Goal",
    "InterfaceContract",
    "Label",
    "Phase",
    "Requirements",
    "Step",
    "SubTask",
    "Task",
    # Type definitions
    "LayerType",
    "StatusType",
]
