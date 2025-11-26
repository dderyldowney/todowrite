"""
ToDoWrite Core Associations Package.

This package contains SQLAlchemy association tables for model relationships.
"""

from __future__ import annotations

from .concepts import (
    concepts_contexts,
    goals_concepts,
)
from .contexts import (
    goals_contexts,
)
from .goals import (
    constraints_goals,
    constraints_requirements,
    goals_phases,
    goals_tasks,
)

# Import all association tables
from .labels import (
    acceptance_criteria_labels,
    commands_labels,
    concepts_labels,
    constraints_labels,
    contexts_labels,
    goals_labels,
    interface_contracts_labels,
    phases_labels,
    requirements_labels,
    steps_labels,
    sub_tasks_labels,
    tasks_labels,
)
from .phases import (
    interface_contracts_phases,
    phases_steps,
)
from .requirements import (
    acceptance_criteria_interface_contracts,
    requirements_acceptance_criteria,
    requirements_concepts,
    requirements_contexts,
)
from .steps import (
    steps_tasks,
)
from .tasks import (
    sub_tasks_commands,
    tasks_sub_tasks,
)

__all__ = [
    # Label associations
    "goals_labels",
    "concepts_labels",
    "contexts_labels",
    # Goal associations
    "goals_tasks",
    "goals_phases",
    "constraints_goals",
    "constraints_labels",
    "constraints_requirements",
    # Additional label associations
    "requirements_labels",
    "acceptance_criteria_labels",
    "interface_contracts_labels",
    "phases_labels",
    "steps_labels",
    "tasks_labels",
    "sub_tasks_labels",
    "commands_labels",
    # Concept associations
    "goals_concepts",
    "concepts_contexts",
    # Context associations
    "goals_contexts",
    "requirements_contexts",
    # Requirement associations
    "requirements_concepts",
    "requirements_acceptance_criteria",
    # Phase associations
    "phases_steps",
    "interface_contracts_labels",
    "interface_contracts_phases",
    # Step associations
    "steps_tasks",
    # Task associations
    "tasks_sub_tasks",
    "sub_tasks_commands",
    # AcceptanceCriteria associations
    "acceptance_criteria_interface_contracts",
]
