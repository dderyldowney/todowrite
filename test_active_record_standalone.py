#!/usr/bin/env python3
"""
Standalone Active Record Test

This test can run independently to verify the Active Record framework
is working correctly without relying on the complex test infrastructure.
"""

import sys
import tempfile
from pathlib import Path

# Add the lib_package to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root / "lib_package" / "src"))

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from todowrite.core.types import Base, Node


def test_active_record_standalone():
    """Test Active Record framework independently."""
    print("🧪 Standalone Active Record Framework Test\n")

    # Create temporary database
    with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as tmp:
        db_path = tmp.name

    try:
        # Setup database and session
        engine = create_engine(f"sqlite:///{db_path}")
        Base.metadata.create_all(engine)
        Session = sessionmaker(bind=engine)
        session = Session()
        Node.configure_session(session)
        print("✅ Database and Active Record session configured")

        print("\n🎯 Test 1: Node Creation")
        # Test node creation
        goal = Node.create_goal(title="Active Record Test Goal", owner="test-user", severity="high")
        print(f"   ✅ Created goal: {goal.title} ({goal.status})")
        assert goal.layer == "Goal"
        assert goal.title == "Active Record Test Goal"
        assert goal.owner == "test-user"
        assert goal.severity == "high"

        print("\n🏗️ Test 2: Collections and Relationships")
        # Test collections
        phases_before = goal.phases().size()
        print(f"   Phases before: {phases_before}")

        # Create phase using collection
        phase = goal.phases().create(title="Test Constraints", owner="architecture-team")
        print(f"   ✅ Created phase: {phase.title}")

        phases_after = goal.phases().size()
        print(f"   Phases after: {phases_after}")
        assert phases_after == phases_before + 1

        # Test collection queries
        all_phases = goal.phases().all()
        print(f"   ✅ All phases: {len(all_phases)}")
        assert len(all_phases) == phases_after

        # Test find operations
        found_phase = goal.phases().find_by(owner="architecture-team")
        print(f"   ✅ Found by owner: {found_phase.title if found_phase else 'None'}")
        assert found_phase is not None
        assert found_phase.owner == "architecture-team"

        print("\n🔗 Test 3: Hierarchy Creation")
        # Create complete hierarchy
        requirement = (
            phase.requirements()
            .create(title="Must scale well", description="System should handle 1000+ users")
            .start()
        )

        task = (
            requirement.tasks()
            .create(title="Implement scaling", assignee="backend-team")
            .update(progress=75)
        )

        command = task.commands().create(title="Run load test", work_type="testing").start()

        print("   ✅ Complete hierarchy created:")
        print(f"      Goal: {goal.title}")
        print(f"      → Phase: {phase.title}")
        print(f"      → Requirement: {requirement.title} ({requirement.status})")
        print(f"      → Task: {task.title} ({task.progress}%)")
        print(f"      → Command: {command.title} ({command.status})")

        # Verify hierarchy
        assert requirement.status == "in_progress"
        assert task.progress == 75
        assert command.work_type == "testing"
        assert command.status == "in_progress"

        print("\n📊 Test 4: Class-Level Queries")
        # Test class-level finders
        all_goals = Node.where(layer="Goal")
        all_tasks = Node.where(layer="SubTask")
        all_commands = Node.where(layer="Command", status="in_progress")

        print(f"   ✅ All goals: {len(all_goals)}")
        print(f"   ✅ All tasks: {len(all_tasks)}")
        print(f"   ✅ In-progress commands: {len(all_commands)}")

        assert len(all_goals) >= 1
        assert len(all_tasks) >= 1
        assert len(all_commands) >= 1

        print("\n⚡ Test 5: Method Chaining")
        # Test method chaining
        new_goal = Node.create_goal("Chained Goal", "test-user").start().update(progress=30).save()

        print(f"   ✅ Chained creation: {new_goal.title} ({new_goal.status}, {new_goal.progress}%)")
        assert new_goal.status == "in_progress"
        assert new_goal.progress == 30

        print("\n🔄 Test 6: Cascading Collections")
        # Test cascading collections
        phases = goal.phases().all()
        print(f"   ✅ Goal phases: {len(phases)}")

        for phase_item in phases:
            requirements = phase_item.requirements().all()
            print(f"      Phase: {phase_item.title} - {len(requirements)} requirements")
            for req in requirements:
                tasks = req.tasks().all()
                print(f"        Requirement: {req.title} - {len(tasks)} tasks")
                for task_item in tasks:
                    commands = task_item.commands().all()
                    print(f"          Task: {task_item.title} - {len(commands)} commands")

        session.close()

        print("\n🎉 ALL TESTS PASSED!")
        print("   ✅ Active Record framework working perfectly!")
        print("   ✅ Ready to replace old tests with new patterns!")

    finally:
        # Clean up
        if Path(db_path).exists():
            Path(db_path).unlink()


if __name__ == "__main__":
    test_active_record_standalone()
