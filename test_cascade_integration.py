#!/usr/bin/env python3
"""Test script to verify CASCADE DELETE constraints are applied during database initialization.

This script tests that:
1. Database initialization creates tables
2. CASCADE DELETE constraints are applied automatically
3. Goal.delete() properly cascades to all children

Usage:
    python test_cascade_integration.py
"""

import os
import sys
import traceback
from pathlib import Path

# Add lib_package to Python path
sys.path.insert(0, str(Path(__file__).parent / "lib_package" / "src"))

# Import everything at the top as required
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from todowrite.core.models import Goal, Phase, Task
from todowrite.core.schema_validator import initialize_database


def test_database_initialization():
    """Test database initialization with cascade constraints."""
    try:
        print("✅ Testing database initialization with cascade constraints...")

        # Initialize database with test data (use existing todowrite database)
        # pragma: allowlist secret
        db_url = os.environ.get(
            "TODOWRITE_DB_URL",
            "postgresql://mcp_user:mcp_secure_password_2024@localhost:5433/todowrite",
        )

        # Initialize the database with cascade constraints
        print("🚀 Initializing database with cascade constraints...")
        initialize_database(db_url)
        success = True

        if success:
            print("✅ Database initialization successful")
        else:
            print("❌ Database initialization failed")
            return False

        # Test cascade constraints by creating and deleting a hierarchy
        print("🧪 Testing cascade delete functionality...")

        try:
            # Test using the Goal model with the new delete() method
            engine = create_engine(db_url)
            session_factory = sessionmaker(bind=engine)

            with session_factory() as session:
                with session.begin():
                    # Create goal using model
                    goal = Goal(
                        title="Test Goal", description="Testing cascade delete", owner="test_user"
                    )
                    session.add(goal)
                    session.flush()  # Get the ID
                    goal_id = goal.id

                    # Create phase using model
                    phase = Phase(
                        title="Test Phase", description="Testing cascade delete", owner="test_user"
                    )
                    session.add(phase)
                    session.flush()
                    phase_id = phase.id

                    # Link goal to phase
                    goal.phases.append(phase)
                    session.flush()

                    # Create a task directly linked to goal
                    task = Task(
                        title="Test Task", description="Testing cascade delete", owner="test_user"
                    )
                    session.add(task)
                    session.flush()
                    goal.tasks.append(task)

                print("✅ Test hierarchy created successfully")

                # Verify all entities exist before deletion
                result = session.execute(
                    text("SELECT COUNT(*) FROM goals WHERE id = :goal_id"), {"goal_id": goal_id}
                )
                goal_count_before = result.scalar()

                result = session.execute(
                    text("SELECT COUNT(*) FROM phases WHERE id = :phase_id"), {"phase_id": phase_id}
                )
                phase_count_before = result.scalar()

                result = session.execute(
                    text("SELECT COUNT(*) FROM goals_phases WHERE goal_id = :goal_id"),
                    {"goal_id": goal_id},
                )
                link_count_before = result.scalar()

                print(
                    f"   Before delete: Goals={goal_count_before}, "
                    f"Phases={phase_count_before}, Links={link_count_before}"
                )

                # Test cascade delete using Goal.delete() method
                goal.delete(session)

                # Verify all entities are deleted
                result = session.execute(
                    text("SELECT COUNT(*) FROM goals WHERE id = :goal_id"), {"goal_id": goal_id}
                )
                goal_count_after = result.scalar()

                result = session.execute(
                    text("SELECT COUNT(*) FROM phases WHERE id = :phase_id"), {"phase_id": phase_id}
                )
                phase_count_after = result.scalar()

                result = session.execute(
                    text("SELECT COUNT(*) FROM tasks WHERE title = 'Test Task'")
                )
                task_count_after = result.scalar()

                result = session.execute(
                    text("SELECT COUNT(*) FROM goals_phases WHERE goal_id = :goal_id"),
                    {"goal_id": goal_id},
                )
                link_count_after = result.scalar()

                print(
                    f"   After delete: Goals={goal_count_after}, "
                    f"Phases={phase_count_after}, Tasks={task_count_after}, "
                    f"Links={link_count_after}"
                )

                if (
                    goal_count_after == 0
                    and phase_count_after == 0
                    and task_count_after == 0
                    and link_count_after == 0
                ):
                    print("✅ CASCADE DELETE working correctly! All entities deleted!")
                    return True
                print("❌ CASCADE DELETE failed - some entities remain")
                print(f"   Goals remaining: {goal_count_after}")
                print(f"   Phases remaining: {phase_count_after}")
                print(f"   Tasks remaining: {task_count_after}")
                print(f"   Links remaining: {link_count_after}")
                return False

        except Exception as e:
            print(f"❌ Test failed with error: {e}")
            return False

        print("✅ All tests passed! CASCADE DELETE constraints are working.")
        return True

    except Exception as e:
        print(f"❌ Test failed: {e}")
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = test_database_initialization()
    sys.exit(0 if success else 1)
