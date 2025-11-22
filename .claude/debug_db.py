#!/usr/bin/env python3
"""Debug database operations to identify tuple issue"""

import json
import sys
from datetime import datetime
from pathlib import Path

import psycopg2

# Add lib_package to path for existing Models API
sys.path.insert(0, str(Path(__file__).parent / "lib_package" / "src"))

try:
    from todowrite.core.models import (
        AcceptanceCriteria,
        Command,
        Concept,
        Constraints,
        Context,
        Goal,
        InterfaceContract,
        Label,
        Phase,
        Requirements,
        Step,
        SubTask,
        Task,
    )

    print("✅ Imported existing ToDoWrite Models API")
except ImportError as e:
    print(f"❌ Failed to import existing ToDoWrite Models API: {e}")
    sys.exit(1)


def debug_create_goal():
    """Debug goal creation step by step"""
    db_config = {
        "host": "localhost",
        "port": 5433,
        "database": "mcp_tools",
        "user": "mcp_user",
        "password": "mcp_secure_password_2024",
    }

    session_id = "debug_session"
    title = "Debug Goal"
    description = "Debug goal creation"

    print("Step 1: Creating Goal model...")
    try:
        goal = Goal(
            title=title,
            description=description,
        )
        print(f"✅ Goal model created: {goal}")
    except Exception as e:
        print(f"❌ Goal model creation failed: {e}")
        return

    print("Step 2: Connecting to database...")
    try:
        conn = psycopg2.connect(**db_config)
        print("✅ Database connected")
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        return

    print("Step 3: Executing INSERT query...")
    try:
        with conn.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO todowrite_goals (title, description, session_id)
                VALUES (%s, %s, %s)
                RETURNING id
            """,
                (title, description, session_id),
            )

            print("Step 4: Fetching result...")
            result = cursor.fetchone()
            print(f"Result type: {type(result)}")
            print(f"Result value: {result}")

            if result is None:
                print("❌ No result returned from query")
                goal_id = None
            elif len(result) == 0:
                print("❌ Empty result returned from query")
                goal_id = None
            else:
                goal_id = result[0]
                print(f"✅ Goal ID extracted: {goal_id}")

            print("Step 5: Updating session tracking...")
            cursor.execute(
                """
                INSERT INTO todowrite_sessions (session_id, title, description, actions, context)
                VALUES (%s, %s, %s, %s, %s)
                ON CONFLICT (session_id)
                DO UPDATE SET
                    last_activity = NOW(),
                    actions = actions || %s,
                    updated_at = NOW()
            """,
                (
                    session_id,
                    f"Created Goal: {title}",
                    description,
                    json.dumps(
                        [
                            {
                                "type": "create_goal",
                                "layer": "goal",
                                "title": title,
                                "goal_id": goal_id,
                                "timestamp": datetime.now().isoformat(),
                            }
                        ]
                    ),
                    json.dumps(
                        {
                            "goal_data": {
                                "id": goal_id,
                                "title": title,
                                "description": description,
                                "created_at": datetime.now().isoformat(),
                                "session_id": session_id,
                            }
                        }
                    ),
                ),
            )
            print("✅ Session tracking updated")

            conn.commit()
            print("✅ Transaction committed")

    except Exception as e:
        print(f"❌ Database operation failed: {e}")
        import traceback

        traceback.print_exc()
        conn.rollback()
        return

    try:
        conn.close()
        print("✅ Database connection closed")
    except Exception as e:
        print(f"❌ Error closing connection: {e}")

    print(f"✅ Goal creation completed with ID: {goal_id}")


if __name__ == "__main__":
    debug_create_goal()
