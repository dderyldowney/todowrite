#!/usr/bin/env python3
"""
Complete Rails-Style Active Record Demo

Shows how the Node class now works exactly like Rails ActiveRecord:
- goal.phases.all() - Get all phases
- goal.phases.size() - Get count
- goal.phases.empty?() - Check if empty
- goal.phases.build() - Create new phase (not saved)
- goal.phases.create() - Create new phase (saved)
- Automatic back-references (phase.goal)
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from lib_package.src.todowrite.core.types import Base, Node


def demo_complete_rails_active_record():
    """Demonstrate complete Rails-style Active Record implementation."""
    print("🚀 Complete Rails-Style Active Record Demo\n")

    # Setup database session
    engine = create_engine("sqlite:///test_complete_rails.db")
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()

    # Configure the Node class with session (like Rails)
    Node.configure_session(session)

    print("🎯 Rails-Style Goal Creation")

    # Create a goal using Rails-style factory method
    goal = Node.create_goal(title="Launch Amazing Product", owner="product-team", severity="high")
    print(f"   ✅ Created goal: {goal.title}")

    print("\n📊 Rails-Style Collection Methods")

    # Test collection methods like Rails
    phases = goal.phases()
    print(f"   goal.phases.all(): {len(phases.all())} phases")
    print(f"   goal.phases.size(): {phases.size()}")
    print(f"   goal.phases.empty(): {phases.empty()}")
    print(f"   goal.phases.exists(): {phases.exists()}")

    print("\n🏗️ Rails-Style build() vs create()")

    # Build vs Create (Rails-style)
    print("   Using .build() - creates object but doesn't save:")
    phase_built = goal.phases().build(title="Technical Constraints", owner="architecture-team")
    print(f"      Built phase: {phase_built.title} (ID: {phase_built.id})")
    print(f"      Is new record: {phase_built._is_new_record}")
    print(f"      In collection: {len(goal.phases().all())} (not saved yet)")

    print("   Using .create() - creates object AND saves:")
    phase_created = goal.phases().create(title="Business Constraints", owner="business-team")
    print(f"      Created phase: {phase_created.title} (ID: {phase_created.id})")
    print(f"      Is new record: {phase_created._is_new_record}")
    print(f"      In collection: {len(goal.phases().all())} phases")

    # Save the built phase to show both work
    phase_built.save()
    print(f"      After saving built phase: {len(goal.phases().all())} phases")

    print("\n🔍 Rails-Style Collection Querying")

    # Query collections like Rails
    all_phases = goal.phases().all()
    print(f"   All phases: {len(all_phases)}")
    for phase in all_phases:
        print(f"      - {phase.title} (owner: {phase.owner})")

    # Find by attributes
    tech_phase = goal.phases().find_by(owner="architecture-team")
    print(f"   Find by owner='architecture-team': {tech_phase.title if tech_phase else 'None'}")

    # Where clause
    business_phases = goal.phases().where(owner="business-team")
    print(f"   Where owner='business-team': {len(business_phases)} phases")

    # Exists with criteria
    exists_tech = goal.phases().exists(owner="architecture-team")
    exists_ux = goal.phases().exists(owner="ux-team")
    print(f"   Exists owner='architecture-team': {exists_tech}")
    print(f"   Exists owner='ux-team': {exists_ux}")

    print("\n🔗 Rails-Style Method Chaining")

    # Create complete hierarchy with method chaining like Rails
    new_goal = Node.create_goal(title="Mobile App Launch", owner="mobile-team").start()

    # Phase with method chaining
    phase = new_goal.phases().create(title="Mobile Platform Constraints", owner="mobile-architect")

    # Requirement with method chaining
    requirement = (
        phase.requirements().create(title="iOS Support", description="Must support iOS 15+").start()
    )

    # Task with method chaining
    task = (
        requirement.tasks()
        .create(title="Build iOS Native Components", assignee="ios-developer")
        .update(progress=75)
    )

    # Command with method chaining
    command = task.commands().create(title="Test on iOS Simulator", work_type="testing").start()

    print("   ✅ Complete hierarchy created with method chaining:")
    print(f"      Goal: {new_goal.title} ({new_goal.status})")
    print(f"      → Phase: {phase.title}")
    print(f"      → Requirement: {requirement.title} ({requirement.status})")
    print(f"      → Task: {task.title} ({task.progress}%)")
    print(f"      → Command: {command.title} ({command.status})")

    print("\n🔄 Rails-Style Cascading Collections")

    # Show cascading access like Rails
    print(f"   Goal phases: {len(new_goal.phases().all())}")
    for phase_obj in new_goal.phases().all():
        print(f"      Phase: {phase_obj.title}")
        print(f"        Requirements: {len(phase_obj.requirements().all())}")
        for req in phase_obj.requirements().all():
            print(f"          Requirement: {req.title}")
            print(f"            Tasks: {len(req.tasks().all())}")
            for task_obj in req.tasks().all():
                print(f"              Task: {task_obj.title} ({task_obj.progress}%)")
                print(f"                Commands: {len(task_obj.commands().all())}")
                for cmd in task_obj.commands().all():
                    print(f"                  Command: {cmd.title}")

    print("\n💾 Rails-Style Save States")

    # Check save states like Rails
    unsaved_phase = new_goal.phases().build(title="Unsaved Phase")
    print(f"   Unsaved phase._is_new_record: {unsaved_phase._is_new_record}")

    unsaved_phase.save()
    print(f"   After save()._is_new_record: {unsaved_phase._is_new_record}")

    print("\n⚡ Rails-Style Mass Operations")

    # Show collection operations like Rails
    all_goals = Node.where(layer="Goal")
    print(f"   All goals: {len(all_goals)}")

    in_progress_tasks = Node.where(layer="SubTask", status="in_progress")
    print(f"   In-progress tasks: {len(in_progress_tasks)}")

    # Find high priority goals by chaining
    all_goals = Node.where(layer="Goal")
    high_priority_goals = [g for g in all_goals if g.severity == "high"]
    print(f"   High-priority goals: {len(high_priority_goals)}")

    print("\n✅ Complete Rails-Style Active Record Demo!")
    print("   🎉 Node now works exactly like Rails ActiveRecord!")
    print()
    print("   Key Rails Patterns Working:")
    print("     • goal.phases.all() - Get collection")
    print("     • goal.phases.size() - Get count")
    print("     • goal.phases.empty()() - Check if empty")
    print("     • goal.phases.build() - Create not saved")
    print("     • goal.phases.create() - Create and save")
    print("     • goal.phases.where() - Filter collection")
    print("     • goal.phases.find_by() - Find by attributes")
    print("     • Node.where() - Class-level finders")
    print("     • Method chaining - .start().update().save()")
    print("     • Cascading collections - phase.requirements().tasks()")

    # Clean up
    session.close()


if __name__ == "__main__":
    demo_complete_rails_active_record()
