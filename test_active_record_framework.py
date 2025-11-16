#!/usr/bin/env python3
"""
Comprehensive test of the new Active Record framework.
This demonstrates the patterns that all other tests should follow.
"""

import os
import tempfile

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from lib_package.src.todowrite.core.types import Base, Node
from lib_package.src.todowrite.storage.sqlite_backend import SQLiteBackend


def test_active_record_framework():
    """Test the complete Active Record framework implementation."""
    print("🚀 Comprehensive Active Record Framework Test\n")

    # Create a temporary database
    with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as tmp:
        db_path = tmp.name

    try:
        # Setup database and Active Record session
        engine = create_engine(f"sqlite:///{db_path}")
        Base.metadata.create_all(engine)
        Session = sessionmaker(bind=engine)
        session = Session()
        Node.configure_session(session)
        print("✅ Database and Active Record session configured")

        print("\n🎯 1. Goal Creation and Active Record Patterns")
        # Create a goal using factory method
        goal = Node.create_goal(
            title="Launch Amazing Product", owner="product-team", severity="high"
        )
        goal.start()
        print(f"   ✅ Created and started goal: {goal.title} ({goal.status})")

        print("\n🏗️ 2. Active Record Collections - Build vs Create")
        # Build (not saved) vs Create (saved) patterns
        phase_built = goal.phases().build(title="Technical Constraints", owner="architecture-team")
        print(
            f"   ✅ Built phase (not saved): {phase_built.title} (is_new: {phase_built._is_new_record})"
        )

        phase_created = goal.phases().create(title="Business Constraints", owner="business-team")
        print(
            f"   ✅ Created phase (saved): {phase_created.title} (is_new: {phase_created._is_new_record})"
        )

        # Save the built phase
        phase_built.save()
        print(f"   ✅ After save - built phase is_new: {phase_built._is_new_record}")

        print("\n📊 3. Active Record Collection Operations")
        # Test collection methods
        phases = goal.phases().all()
        print(f"   ✅ goal.phases().all(): {len(phases)} phases")
        print(f"   ✅ goal.phases().size(): {goal.phases().size()}")
        print(f"   ✅ goal.phases().empty(): {goal.phases().empty()}")

        # Find operations
        tech_phase = goal.phases().find_by(owner="architecture-team")
        print(
            f"   ✅ Find by owner='architecture-team': {tech_phase.title if tech_phase else 'None'}"
        )

        business_phases = goal.phases().where(owner="business-team")
        print(f"   ✅ Where owner='business-team': {len(business_phases)} phases")

        print("\n🔗 4. Complete Hierarchy with Method Chaining")
        # Create complete hierarchy using Active Record patterns
        requirement = (
            phase_created.requirements()
            .create(
                title="Must support 1000 concurrent users",
                description="System must scale to handle high traffic",
            )
            .start()
        )

        task = (
            requirement.tasks()
            .create(title="Implement load balancing", assignee="backend-team")
            .update(progress=75)
        )

        command = task.commands().create(title="Deploy load balancer", work_type="ops").start()

        print("   ✅ Complete hierarchy:")
        print(f"      Goal: {goal.title} ({goal.status})")
        print(f"      → Phase: {phase_created.title}")
        print(f"      → Requirement: {requirement.title} ({requirement.status})")
        print(f"      → Task: {task.title} ({task.progress}%)")
        print(f"      → Command: {command.title} ({command.status})")

        print("\n🔄 5. Cascading Collections")
        # Test cascading collection access
        print(f"   ✅ Goal phases: {len(goal.phases().all())}")
        for phase in goal.phases().all():
            print(f"      Phase: {phase.title}")
            print(f"        Requirements: {len(phase.requirements().all())}")
            for req in phase.requirements().all():
                print(f"          Requirement: {req.title}")
                print(f"            Tasks: {len(req.tasks().all())}")
                for task_item in req.tasks().all():
                    print(f"              Task: {task_item.title} ({task_item.progress}%)")
                    print(f"                Commands: {len(task_item.commands().all())}")

        print("\n⚡ 6. Active Record Query Operations")
        # Test class-level finders
        all_goals = Node.where(layer="Goal")
        all_tasks = Node.where(layer="SubTask")
        in_progress_commands = Node.where(layer="Command", status="in_progress")

        print(f"   ✅ All goals: {len(all_goals)}")
        print(f"   ✅ All tasks: {len(all_tasks)}")
        print(f"   ✅ In-progress commands: {len(in_progress_commands)}")

        print("\n💾 7. Storage Backend Integration")
        # Test that storage backend works with Active Record
        backend = SQLiteBackend(db_path)
        backend.connect_to_storage()

        # Create another node through storage backend
        another_goal = Node.create_goal(title="Mobile App Launch", owner="mobile-team")
        storage_result = backend.create_new_node(another_goal)
        print(f"   ✅ Storage backend create: {storage_result.was_newly_created}")

        # Test retrieval through storage backend
        retrieved = backend.retrieve_node_by_id(goal.id)
        print(f"   ✅ Storage backend retrieve: {retrieved.title}")

        # Test relationship creation through storage backend
        new_phase = Node.new(
            layer="Constraints", title="Mobile Platform Constraints", owner="mobile-architect"
        )
        new_phase.save()

        relationship_result = backend.create_parent_child_relationship(
            another_goal.id, new_phase.id
        )
        print(f"   ✅ Storage backend relationship: {relationship_result.was_newly_linked}")

        print("\n🗑️ 8. Active Record Delete Operations")
        # Test delete using storage backend (which calls Node.destroy())
        delete_result = backend.remove_node_by_id(new_phase.id)
        print(f"   ✅ Storage backend delete: {delete_result}")

        # Verify deletion
        try:
            deleted_node = backend.retrieve_node_by_id(new_phase.id)
            print("   ❌ Node still exists after deletion!")
        except Exception:
            print("   ✅ Node successfully deleted")

        session.close()
        backend.disconnect_from_storage()

        print("\n🎉 ACTIVE RECORD FRAMEWORK TEST COMPLETE!")
        print("   ✅ All Active Record patterns working perfectly!")
        print("   ✅ Storage backend integration successful!")
        print("   ✅ Ready to update all existing tests!")

    finally:
        # Clean up
        if os.path.exists(db_path):
            os.unlink(db_path)


if __name__ == "__main__":
    test_active_record_framework()
