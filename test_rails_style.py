#!/usr/bin/env python3
"""
Quick demo of the Rails-style Active Record Node implementation.

This shows how the new unified Node works like Rails Active Record.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from lib_package.src.todowrite.core.types import Base, Node


def demo_rails_style_node():
    """Demonstrate Rails-style Node usage."""
    print("🎉 Rails-Style Active Record Node Demo\n")

    # Setup database session
    engine = create_engine("sqlite:///test_rails.db")
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()

    # Configure the Node class with session (like Rails)
    Node.configure_session(session)

    print("1. Creating nodes with Node.new() (Rails-style)")

    # Create a goal node (Rails-style)
    goal = Node.new(
        layer="Goal",
        title="Launch Amazing Product",
        description="Successfully launch v1.0 of our amazing product",
        owner="product-team",
        severity="high",
        work_type="development",
    )
    print(f"   Created: {goal.id} - {goal.title}")

    # Create a task node (Rails-style)
    task = Node.new(
        layer="Task", title="Build API endpoints", owner="backend-team", work_type="implementation"
    )
    print(f"   Created: {task.id} - {task.title}")

    print("\n2. Using Rails-style relationships")

    # Add relationships (Rails-style)
    goal.add_child(task)
    task.add_parent(goal)
    print(f"   Goal children: {len(goal.children)}")
    print(f"   Task parents: {len(task.parents)}")

    print("\n3. Using Rails-style business methods")

    # Start working on the task
    task.start()
    print(f"   Task status: {task.status}")

    # Make progress
    task.update(progress=50)
    print(f"   Task progress: {task.progress}%")

    print("\n4. Using Rails-style persistence")

    # Save both nodes
    goal.save()
    task.save()
    print("   ✅ Both nodes saved to database")

    print("\n5. Using Rails-style finders")

    # Find by ID
    found_goal = Node.find(goal.id)
    print(f"   Found goal: {found_goal.title if found_goal else 'Not found'}")

    # Find by attributes
    tasks = Node.find_by(layer="Task")
    print(f"   Found {len(tasks)} tasks")

    # Use where clause
    active_nodes = Node.where(status="in_progress")
    print(f"   Found {len(active_nodes)} active nodes")

    print("\n6. Method chaining like Rails")

    # Chain method calls
    new_task = (
        Node.new(layer="Task", title="Write documentation", owner="tech-writer")
        .start()
        .update(progress=25)
    )

    new_task.add_parent(goal)
    new_task.save()
    print(f"   Created and configured: {new_task.title}")

    print("\n7. Accessing relationships (returns Node objects!)")

    # Access children and parents - these return actual Node objects!
    print(f"   Goal '{goal.title}' has {len(goal.children)} children:")
    for child in goal.children:
        print(f"     - {child.title} ({child.status})")

    print(f"\n   Task '{task.title}' has {len(task.parents)} parents:")
    for parent in task.parents:
        print(f"     - {parent.title} ({parent.layer})")

    print("\n8. Rails-style lifecycle methods")

    # Complete the task
    task.complete()
    task.save()
    print(f"   Task completed: {task.status} at {task.completion_date}")

    print("\n✅ Rails-Style Active Record Demo Complete!")
    print("   The Node class now works like Rails Active Record!")

    # Clean up
    session.close()


if __name__ == "__main__":
    demo_rails_style_node()
