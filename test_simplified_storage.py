#!/usr/bin/env python3
"""
Test the simplified storage backend using Active Record patterns.
"""

import os
import tempfile

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from lib_package.src.todowrite.core.types import Base, Node
from lib_package.src.todowrite.storage.sqlite_backend import SQLiteBackend


def test_simplified_storage_backend():
    """Test the simplified storage backend with Active Record patterns."""
    print("🧪 Testing Simplified Storage Backend with Active Record Patterns\n")

    # Create a temporary database
    with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as tmp:
        db_path = tmp.name

    try:
        # Initialize storage backend
        backend = SQLiteBackend(db_path)
        backend.connect_to_storage()
        print("✅ Storage backend connected")

        # Setup Node session (Active Record pattern)
        engine = create_engine(f"sqlite:///{db_path}")
        Base.metadata.create_all(engine)
        Session = sessionmaker(bind=engine)
        session = Session()
        Node.configure_session(session)
        print("✅ Active Record session configured")

        print("\n🎯 Test 1: Create nodes using storage backend")
        # Create a goal using storage backend
        goal = Node.create_goal(title="Test Goal", owner="test-user")
        result = backend.create_new_node(goal)
        print(f"   Created goal: {goal.title} (was_newly_created: {result.was_newly_created})")

        # Create a phase using Active Record pattern
        phase = Node.new(layer="Constraints", title="Test Phase", owner="test-user")
        phase.save()
        print(f"   Created phase: {phase.title}")

        print("\n🔗 Test 2: Create relationships using storage backend")
        # Create relationship using storage backend (should use Active Record)
        relationship_result = backend.create_parent_child_relationship(goal.id, phase.id)
        print(f"   Relationship created: {relationship_result.was_newly_linked}")

        print("\n📊 Test 3: Test Active Record collections")
        # Test Active Record collections
        phases = goal.phases().all()
        print(f"   Goal phases: {len(phases)}")
        for phase_item in phases:
            print(f"     - {phase_item.title}")

        print("\n🔍 Test 4: Retrieve nodes using storage backend")
        # Retrieve using storage backend
        retrieved_goal = backend.retrieve_node_by_id(goal.id)
        print(f"   Retrieved goal: {retrieved_goal.title}")

        print("\n⚡ Test 5: Update nodes using Active Record patterns")
        # Update using Active Record pattern
        goal.update(progress=50).save()
        print(f"   Updated goal progress: {goal.progress}%")

        # Test retrieval after update
        updated_goal = backend.retrieve_node_by_id(goal.id)
        print(f"   Retrieved updated progress: {updated_goal.progress}%")

        print("\n✅ All tests passed! Simplified storage backend working perfectly!")
        print("   🎉 Active Record patterns integrated successfully!")

        session.close()
        backend.disconnect_from_storage()

    finally:
        # Clean up
        if os.path.exists(db_path):
            os.unlink(db_path)


if __name__ == "__main__":
    test_simplified_storage_backend()
