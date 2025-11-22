#!/usr/bin/env python3
"""
Test Models API Functionality
Run this to verify the existing ToDoWrite Models API works properly
"""

import sys
from pathlib import Path

# Set up paths
sys.path.insert(0, str(Path(__file__).parent.parent / "lib_package" / "src"))


def test_models_api():
    print("📚 Testing Existing ToDoWrite Models API")
    print("=" * 50)

    try:
        # Test importing all models
        from todowrite.core.models import (
            Concept,
            Goal,
            Task,
        )

        print("✅ All Models Imported Successfully")

        # Test creating instances
        print("\n🧪 Testing Model Creation:")

        # Goal
        goal = Goal(
            title="Test Goal from IDE",
            description="Testing Models API functionality in IDE session",
        )
        print(f"✅ Goal: {goal.title}")

        # Concept
        concept = Concept(title="Test Concept from IDE", description="Testing concept creation")
        print(f"✅ Concept: {concept.title}")

        # Task
        task = Task(title="Test Task from IDE", description="Testing task creation")
        print(f"✅ Task: {task.title}")

        # Test database integration
        print("\n🗄️ Testing Database Integration:")
        import psycopg2

        conn = psycopg2.connect(
            host="localhost",
            port=5433,
            database="mcp_tools",
            user="mcp_user",
            password="mcp_secure_password_2024",
        )

        with conn.cursor() as cursor:
            # Store goal in database
            cursor.execute(
                """
                INSERT INTO todowrite_goals (title, description, session_id)
                VALUES (%s, %s, %s)
                RETURNING id
            """,
                (goal.title, goal.description, "models_api_test"),
            )

            result = cursor.fetchone()
            goal_id = result[0] if result else None
            print(f"✅ Goal stored in database - ID: {goal_id}")

            # Store concept in database
            cursor.execute(
                """
                INSERT INTO todowrite_concepts (title, description, session_id)
                VALUES (%s, %s, %s)
                RETURNING id
            """,
                (concept.title, concept.description, "models_api_test"),
            )

            result = cursor.fetchone()
            concept_id = result[0] if result else None
            print(f"✅ Concept stored in database - ID: {concept_id}")

            # Store task in database
            cursor.execute(
                """
                INSERT INTO todowrite_tasks (title, description, session_id)
                VALUES (%s, %s, %s)
                RETURNING id
            """,
                (task.title, task.description, "models_api_test"),
            )

            result = cursor.fetchone()
            task_id = result[0] if result else None
            print(f"✅ Task stored in database - ID: {task_id}")

            # Create association
            cursor.execute(
                """
                INSERT INTO todowrite_goal_tasks (goal_id, task_id, priority, session_id)
                VALUES (%s, %s, %s, %s)
            """,
                (goal_id, task_id, 1, "models_api_test"),
            )

            conn.commit()
            print("✅ Association created successfully")

        conn.close()

        print("\n🎉 Models API Test - COMPLETE SUCCESS!")
        print("✅ Import: Working")
        print("✅ Creation: Working")
        print("✅ Database: Working")
        print("✅ Associations: Working")

    except Exception as e:
        print(f"\n❌ Models API Test Failed: {e}")
        import traceback

        traceback.print_exc()
        return False

    return True


if __name__ == "__main__":
    test_models_api()
