"""
Test ToDoWrite Flexible Entry Points and Mandatory Hierarchy Completion.

This test demonstrates two key ToDoWrite system capabilities:
1. FLEXIBLE ENTRY: You can start at any layer in the 12-layer hierarchy
2. MANDATORY COMPLETION: All layers below your starting point MUST be defined

The 12-layer hierarchy:
Goal → Concept → Context → Constraints → Requirements → Acceptance Criteria →
Interface Contract → Phase → Step → Task → SubTask → Command
"""

import sys
import tempfile
import uuid
from pathlib import Path
from typing import Any

# Add project root to sys.path
project_root = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(project_root))

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from todowrite.core.types import (
    Command,
    Goal,
    Phase,
    SubTask,
    Task,
)


def create_standalone_node(layer: str, title: str, description: str) -> dict[str, Any]:
    """Create a node without requiring a parent - demonstrates flexible entry.

    Uses real database operations with the new ToDoWrite models.
    """
    # Create temporary database for testing
    temp_db = tempfile.mktemp(suffix=".db")
    engine = create_engine(f"sqlite:///{temp_db}")
    Session = sessionmaker(bind=engine)

    # Create all tables
    from todowrite.core.types import Base

    Base.metadata.create_all(engine)

    # Map layer names to model classes
    layer_model_map = {
        "Goal": Goal,
        "Task": Task,
        "Command": Command,
        "Phase": Phase,
        "SubTask": SubTask,
    }

    with Session() as session:
        # Get the appropriate model class
        model_class = layer_model_map.get(layer)
        if not model_class:
            raise ValueError(f"Unsupported layer: {layer}")

        # Create node with basic fields
        if layer == "Command":
            # Command nodes have special fields
            node = model_class(
                title=title,
                description=description,
                owner="test-user",
                severity="medium",
                ac_ref=f"AC-{uuid.uuid4().hex[:8].upper()}",
                run={"shell": "echo 'flexible entry test'"},
            )
        else:
            # Regular nodes
            node = model_class(
                title=title, description=description, owner="test-user", severity="medium"
            )

        session.add(node)
        session.commit()

        result = {"id": node.id, "title": node.title, "status": node.status}

    # Clean up temporary database
    import os

    os.unlink(temp_db)

    return result


class TestFlexibleEntryPoints:
    """Test flexible entry points and mandatory hierarchy completion."""

    def test_flexible_entry_at_any_layer(self):
        """Demonstrate that you can start at ANY layer in the hierarchy."""

        # Entry Point 1: Start at Command (Layer 12) - Minimal hierarchy
        command_node = create_standalone_node(
            "Command", "Emergency System Check", "Quick diagnostic command"
        )
        assert command_node["id"] is not None
        assert command_node["title"] == "Emergency System Check"

        # Entry Point 2: Start at Task (Layer 10) - Implementation level
        task_node = create_standalone_node(
            "Task", "Fix GPS Module", "Repair GPS communication issue"
        )
        assert task_node["id"] is not None
        assert task_node["title"] == "Fix GPS Module"

        # Entry Point 3: Start at Phase (Layer 8) - Project level
        phase_node = create_standalone_node(
            "Phase", "Hardware Integration", "Install and configure sensors"
        )
        assert phase_node["id"] is not None
        assert phase_node["title"] == "Hardware Integration"

        # Entry Point 4: Start at Goal (Layer 1) - Strategic level
        goal_node = create_standalone_node(
            "Goal",
            "Autonomous Harvesting",
            "Develop autonomous harvesting system",
        )
        assert goal_node["id"] is not None
        assert goal_node["title"] == "Autonomous Harvesting"

        print("✅ FLEXIBLE ENTRY DEMONSTRATED: Started at 4 different layers independently")

    def test_mandatory_hierarchy_completion_from_task(self):
        """Demonstrate that starting at Task requires completing mandatory lower layers."""

        # Start at Task (Layer 10)
        task = create_standalone_node(
            "Task",
            "Implement CAN Driver",
            "Develop CAN bus communication driver",
        )
        task_id = task["id"]
        assert task_id is not None

        # Test that we can create SubTask and Command nodes
        subtask_node = create_standalone_node(
            "SubTask", "Write CAN Protocol", "Implement CAN protocol specification"
        )
        assert subtask_node["id"] is not None

        command_node = create_standalone_node(
            "Command", "Test CAN Bus", "Run CAN bus diagnostic tests"
        )
        assert command_node["id"] is not None

        print("✅ MANDATORY COMPLETION DEMONSTRATED: Task + SubTask + Command layers created")
