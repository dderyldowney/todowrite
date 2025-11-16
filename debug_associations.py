#!/usr/bin/env python3
"""
Debug script to investigate why association table isn't being populated.
"""

from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker

from lib_package.src.todowrite.core.types import Base, Node, links


def debug_associations():
    """Debug why association table isn't working."""
    print("🔍 Debugging Association Table Issues\n")

    # Setup database session
    engine = create_engine("sqlite:///debug_associations.db")
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()

    # Configure the Node class with session
    Node.configure_session(session)

    print("1. Create parent node")
    goal = Node.create_goal(title="Test Goal", owner="test-user")
    print(f"   Created goal: {goal.id}")

    print("\n2. Create child node")
    phase = Node.new(layer="Constraints", title="Test Phase", owner="test-user")
    print(f"   Created phase: {phase.id}")

    print("\n3. Check initial state")
    print(f"   Goal children before adding: {len(goal.children)}")
    print(f"   Phase parents before adding: {len(phase.parents)}")

    print("\n4. Add child relationship")
    try:
        result = goal.add_child(phase)
        print(f"   Called goal.add_child(phase) - returned: {result}")
    except Exception as e:
        print(f"   ERROR in add_child: {e}")
        import traceback

        traceback.print_exc()

    print("\n5. Save both nodes")
    goal.save()
    phase.save()
    print("   Saved both nodes")

    print("\n6. Check association table directly")
    # Check the association table directly
    result = session.execute(
        select(links).where((links.c.parent_id == goal.id) | (links.c.child_id == goal.id))
    ).fetchall()
    print(f"   Association table entries for goal: {result}")

    result = session.execute(
        select(links).where((links.c.parent_id == phase.id) | (links.c.child_id == phase.id))
    ).fetchall()
    print(f"   Association table entries for phase: {result}")

    print("\n7. Check all entries in links table")
    all_links = session.execute(select(links)).fetchall()
    print(f"   All entries in links table: {all_links}")

    print("\n8. Check relationship after save")
    # Refresh both nodes
    session.refresh(goal)
    session.refresh(phase)
    print(f"   Goal children after save: {len(goal.children)}")
    print(f"   Phase parents after save: {len(phase.parents)}")

    print("\n9. Test direct SQL insertion")
    # Try inserting directly into association table
    session.execute(links.insert().values(parent_id=goal.id, child_id=phase.id))
    session.commit()

    print("\n10. Check after direct SQL insertion")
    session.refresh(goal)
    session.refresh(phase)
    print(f"   Goal children after direct insertion: {len(goal.children)}")
    print(f"   Phase parents after direct insertion: {len(phase.parents)}")

    # Check association table again
    result = session.execute(
        select(links).where((links.c.parent_id == goal.id) & (links.c.child_id == phase.id))
    ).fetchall()
    print(f"   Direct association entry: {result}")

    print("\n11. Test PhaseCollection")
    # Test if our PhaseCollection sees the relationship
    phases_collection = goal.phases()
    print(f"   goal.phases().all(): {len(phases_collection.all())}")
    print(f"   goal.phases().size(): {phases_collection.size()}")
    print(f"   goal.phases().empty(): {phases_collection.empty()}")

    # Clean up
    session.close()


if __name__ == "__main__":
    debug_associations()
