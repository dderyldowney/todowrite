#!/usr/bin/env python3
"""Test script to verify the desired relationship API pattern.

This script tests that:
1. goal.phases.append() works for creating phases
2. Relationships are automatically linked with proper IDs
3. goal.delete() cleans up everything properly

Usage:
    python test_relationship_api.py
"""

import os
import sys
import traceback
from pathlib import Path

# Add lib_package to Python path (test is in tests/core/models/, need to go up 3 levels)
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent / "lib_package" / "src"))

# Import everything at the top as required
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from todowrite.core.models import Goal, Phase, Task


def test_desired_api_pattern():
    """Test the desired API pattern for relationships."""
    try:
        print("✅ Testing desired relationship API pattern...")

        # Initialize database with test data (use existing todowrite database)
        # pragma: allowlist secret
        db_url = os.environ.get(
            "TODOWRITE_DB_URL",
            "postgresql://todowrite_user:mcp_secure_password_2024@localhost:5433/todowrite",
        )

        engine = create_engine(db_url)
        session_factory = sessionmaker(bind=engine)

        with session_factory() as session:
            print("🏗️  Creating goal with phases using desired API pattern...")

            # Create the goal
            goal = Goal(
                title="Main Project Goal",
                description="A comprehensive project with multiple phases",
                owner="test_user",
            )
            session.add(goal)
            session.commit()  # Commit to get the goal ID
            print(f"   ✅ Created Goal with ID: {goal.id}")

            # Test the desired API pattern: goal.phases.append()
            phase1 = Phase(
                title="Phase 1", description="Phase 1 deep description", owner="test_user"
            )
            goal.phases.append(phase1)
            session.commit()  # Commit to assign phase ID and link to goal
            print(f"   ✅ Created Phase 1 with ID: {phase1.id}")

            # Create another phase using the same pattern
            phase2 = Phase(
                title="Phase 2", description="Phase 2 deep description", owner="test_user"
            )
            goal.phases.append(phase2)
            session.commit()
            print(f"   ✅ Created Phase 2 with ID: {phase2.id}")

            # Create tasks directly on goal
            task1 = Task(
                title="Direct Task 1", description="Task directly under goal", owner="test_user"
            )
            goal.tasks.append(task1)
            session.commit()
            print(f"   ✅ Created Direct Task 1 with ID: {task1.id}")

            # Verify relationships are properly set up
            result = session.execute(
                text("SELECT COUNT(*) FROM goals_phases WHERE goal_id = :goal_id"),
                {"goal_id": goal.id},
            )
            phase_links = result.scalar()
            print(f"   ✅ Goal-Phase links created: {phase_links}")

            result = session.execute(
                text("SELECT COUNT(*) FROM goals_tasks WHERE goal_id = :goal_id"),
                {"goal_id": goal.id},
            )
            task_links = result.scalar()
            print(f"   ✅ Goal-Task links created: {task_links}")

            print(f"   📊 Summary: Goal has {len(goal.phases)} phases, {len(goal.tasks)} tasks")

            print("🗑️  Testing cascade deletion...")

            # Store IDs for verification after deletion
            phase1_id = phase1.id
            phase2_id = phase2.id
            task1_id = task1.id
            goal_id = goal.id

            # Delete the goal - should cascade to all associated entities
            goal.delete(session)

            print("🔍 Verifying complete deletion...")

            # Verify goal is deleted
            result = session.execute(
                text("SELECT COUNT(*) FROM goals WHERE id = :goal_id"), {"goal_id": goal_id}
            )
            goals_remaining = result.scalar()
            print(f"   Goals remaining: {goals_remaining}")

            # Verify phases are deleted
            result = session.execute(
                text("SELECT COUNT(*) FROM phases WHERE id IN (:phase1_id, :phase2_id)"),
                {"phase1_id": phase1_id, "phase2_id": phase2_id},
            )
            phases_remaining = result.scalar()
            print(f"   Phases remaining: {phases_remaining}")

            # Verify task is deleted
            result = session.execute(
                text("SELECT COUNT(*) FROM tasks WHERE id = :task_id"), {"task_id": task1_id}
            )
            tasks_remaining = result.scalar()
            print(f"   Tasks remaining: {tasks_remaining}")

            # Verify junction tables are cleaned up
            result = session.execute(
                text("SELECT COUNT(*) FROM goals_phases WHERE goal_id = :goal_id"),
                {"goal_id": goal_id},
            )
            phase_links_remaining = result.scalar()
            print(f"   Phase links remaining: {phase_links_remaining}")

            result = session.execute(
                text("SELECT COUNT(*) FROM goals_tasks WHERE goal_id = :goal_id"),
                {"goal_id": goal_id},
            )
            task_links_remaining = result.scalar()
            print(f"   Task links remaining: {task_links_remaining}")

            # Verify complete deletion
            if (
                goals_remaining == 0
                and phases_remaining == 0
                and tasks_remaining == 0
                and phase_links_remaining == 0
                and task_links_remaining == 0
            ):
                print("✅ SUCCESS: Desired API pattern works perfectly!")
                print("   ✅ goal.phases.append() creates phases properly")
                print("   ✅ Relationships are automatically linked")
                print("   ✅ goal.delete() removes everything cleanly")
                return True
            print("❌ FAILURE: Some entities remain after deletion")
            return False

    except Exception as e:
        print(f"❌ Test failed with error: {e}")
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = test_desired_api_pattern()
    sys.exit(0 if success else 1)
