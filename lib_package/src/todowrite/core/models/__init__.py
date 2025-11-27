"""
ToDoWrite Core Models Package.

This package provides access to all ToDoWrite SQLAlchemy models.
You can import models in two ways:

# Import the entire package (backward compatible)
from todowrite.core.models import Goal, Task, Command

# Or import specific models
from todowrite.core.models import Goal
from todowrite.core.models import Task
from todowrite.core.models import Command

Models Available:
- Base: SQLAlchemy declarative base
- Goal: High-level project objectives
- Concept: Abstract ideas and requirements
- Context: Background information and constraints
- Constraint: Technical and business constraints
- Requirement: Specific functional requirements
- AcceptanceCriteria: Definition of done criteria
- InterfaceContract: API and interface contracts
- Phase: Project phases and milestones
- Step: Individual steps within phases
- Task: Specific tasks with owners and status
- SubTask: Breakdown of tasks into smaller units
- Command: Executable commands and scripts
- Label: Tags and categorization system
- Metadata: Extensible metadata for ToDoWrite nodes
"""

from __future__ import annotations

from .acceptance_criteria import AcceptanceCriteria

# Import all models from their individual files
from .base import Base
from .command import Command
from .concept import Concept
from .constraint import Constraint
from .context import Context
from .goal import Goal
from .interface_contract import InterfaceContract
from .label import Label
from .metadata import Metadata
from .phase import Phase
from .requirement import Requirement
from .step import Step
from .sub_task import SubTask
from .task import Task

# Export all models for backward compatibility
__all__ = [
    "AcceptanceCriteria",
    "Base",
    "Command",
    "Concept",
    "Constraint",
    "Context",
    "Goal",
    "InterfaceContract",
    "Label",
    "Metadata",
    "Phase",
    "Requirement",
    "Step",
    "SubTask",
    "Task",
]
