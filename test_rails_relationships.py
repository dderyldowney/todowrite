#!/usr/bin/env python3
"""
Demo of Rails-style layer relationships in the Node Active Record implementation.

Shows how goal.phases, goal.phases.new(), etc. work like Rails has_many/belongs_to.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from lib_package.src.todowrite.core.types import Base, Node


def demo_rails_style_relationships():
    """Demonstrate Rails-style layer relationships."""
    print("🎯 Rails-Style Layer Relationships Demo\n")

    # Setup database session
    engine = create_engine("sqlite:///test_rails_relationships.db")
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()

    # Configure the Node class with session (like Rails)
    Node.configure_session(session)

    print("1. Rails-style Goal Creation and Phases")

    # Create a goal using Rails-style factory method
    goal = Node.create_goal(title="Build Amazing Product", owner="product-team", severity="high")
    print(f"   ✅ Created goal: {goal.title}")

    # Show that goal.phases is empty initially
    print(f"   Initial phases: {len(goal.phases())}")

    print("\n2. Creating Phases (Rails-style)")

    # Create phases using Rails-style factory method
    phase1 = Node.create_phase(title="Technical Constraints", goal=goal, owner="architecture-team")
    print(f"   ✅ Created phase: {phase1.title}")

    phase2 = Node.create_phase(title="Business Constraints", goal=goal, owner="business-team")
    print(f"   ✅ Created phase: {phase2.title}")

    # Now goal.phases should return the phases
    phases = goal.phases()
    print(f"   🎯 goal.phases() returns {len(phases)} phases:")
    for phase in phases:
        print(f"      - {phase.title} (owner: {phase.owner})")

    print("\n3. Adding Requirements to Phases")

    # Add requirements to phase1
    req1 = Node.create_requirement(
        title="Must support 1000 concurrent users",
        parent=phase1,
        description="System must scale to handle high traffic",
    )
    print(f"   ✅ Added requirement to {phase1.title}: {req1.title}")

    req2 = Node.create_requirement(
        title="Must have 99.9% uptime", parent=phase1, description="High availability requirement"
    )
    print(f"   ✅ Added requirement to {phase1.title}: {req2.title}")

    # Show phase1.requirements
    requirements = phase1.requirements()
    print(f"   🎯 phase1.requirements() returns {len(requirements)} requirements:")
    for req in requirements:
        print(f"      - {req.title}")

    print("\n4. Creating Tasks and Commands")

    # Add tasks to requirement
    task1 = Node.create_task(title="Implement load balancing", parent=req1, assignee="backend-team")
    task1.start().update(progress=25).save()
    print(f"   ✅ Created and started task: {task1.title}")

    # Add commands to task
    cmd1 = Node.create_command(title="Deploy load balancer", parent=task1, work_type="ops")
    print(f"   ✅ Created command: {cmd1.title}")

    print("\n5. Rails-style Cascade Navigation")

    # Navigate the hierarchy Rails-style
    print(f"   🎯 Goal: {goal.title}")
    print(f"      └── Phases ({len(goal.phases())})")
    for phase in goal.phases():
        print(f"          ├── {phase.title}")
        print(f"          │   └── Requirements ({len(phase.requirements())})")
        for req in phase.requirements():
            print(f"          │       ├── {req.title}")
            print(f"          │       │   └── Tasks ({len(req.tasks())})")
            for task in req.tasks():
                print(f"          │       │       ├── {task.title} ({task.status})")
                print(f"          │       │       │   └── Commands ({len(task.commands())})")
                for cmd in task.commands():
                    print(f"          │       │       │       └── {cmd.title}")

    print("\n6. Rails-style Finder Methods with Layer Filtering")

    # Find all goals
    all_goals = Node.where(layer="Goal")
    print(f"   🎯 Found {len(all_goals)} goals")

    # Find all tasks in progress
    active_tasks = Node.where(layer="SubTask", status="in_progress")
    print(f"   🎯 Found {len(active_tasks)} active tasks")

    # Find all commands
    all_commands = Node.where(layer="Command")
    print(f"   🎯 Found {len(all_commands)} commands")

    print("\n7. Method Chaining Like Rails")

    # Create a complete hierarchy with method chaining
    new_goal = Node.create_goal(title="Launch Mobile App", owner="mobile-team")

    new_phase = Node.create_phase(
        title="Mobile Constraints", goal=new_goal, owner="mobile-architect"
    )

    new_req = Node.create_requirement(title="iOS compatibility", parent=new_phase).start()

    new_task = Node.create_task(
        title="Build iOS wrapper", parent=new_req, assignee="ios-developer"
    ).update(progress=60)

    new_cmd = Node.create_command(title="Test on iOS simulator", parent=new_task).start()

    print(f"   ✅ Created complete hierarchy: {new_goal.title}")
    print(f"      → {new_phase.title}")
    print(f"      → {new_req.title} ({new_req.status})")
    print(f"      → {new_task.title} ({new_task.progress}%)")
    print(f"      → {new_cmd.title} ({new_cmd.status})")

    print("\n8. Rails-style State Management")

    # Complete the task
    new_task.complete().save()
    print(f"   ✅ Task completed: {new_task.status}")

    # Check command status
    print(f"   🎯 Command status: {new_cmd.status}")

    print("\n✅ Rails-Style Layer Relationships Demo Complete!")
    print("   Now you can use:")
    print("     goal.phases() - Get all Constraint layer children")
    print("     goal.phases.new() - Create new Phase auto-associated")
    print("     requirement.tasks() - Get all SubTask descendants")
    print("     Node.create_goal() - Factory methods")
    print("     Node.create_phase(goal, ...) - Auto-associate")

    # Clean up
    session.close()


if __name__ == "__main__":
    demo_rails_style_relationships()
