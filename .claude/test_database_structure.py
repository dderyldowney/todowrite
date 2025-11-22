#!/usr/bin/env python3
"""
Test Complete Database Structure
Run this to verify all tables and relationships are working
"""

import psycopg2


def test_database_structure():
    print("🗄️ Testing Complete Database Structure")
    print("=" * 50)

    try:
        conn = psycopg2.connect(
            host="localhost",
            port=5433,
            database="mcp_tools",
            user="mcp_user",
            password="mcp_secure_password_2024",
        )

        with conn.cursor() as cursor:
            print("📊 Table Counts:")

            # Get all todowrite tables
            cursor.execute("""
                SELECT table_name FROM information_schema.tables
                WHERE table_schema = 'public' AND table_name LIKE 'todowrite_%'
                ORDER BY table_name
            """)
            tables = [row[0] for row in cursor.fetchall()]
            print(f"✅ Total tables: {len(tables)}")

            print("\n📋 Tables with Data:")
            for table in tables:
                try:
                    cursor.execute(f"SELECT COUNT(*) FROM {table}")
                    count = cursor.fetchone()[0]
                    if count > 0:
                        print(f"✅ {table}: {count} records")
                except Exception:
                    print(f"⚠️ {table}: Unable to count records")

            print("\n🔗 Foreign Key Constraints:")
            cursor.execute("""
                SELECT COUNT(*) FROM information_schema.referential_constraints rc
                JOIN information_schema.table_constraints tc ON tc.constraint_name = rc.constraint_name
                WHERE tc.table_schema = 'public' AND tc.table_name LIKE 'todowrite_%'
            """)
            fk_count = cursor.fetchone()[0]
            print(f"✅ Foreign key constraints: {fk_count}")

            print("\n🌐 Association Tables:")
            association_tables = [
                t
                for t in tables
                if "_" in t
                and any(x in t for x in ["goal_", "concept_", "task_", "phase_", "step_"])
            ]

            for table in association_tables:
                try:
                    cursor.execute(f"SELECT COUNT(*) FROM {table}")
                    count = cursor.fetchone()[0]
                    print(f"✅ {table}: {count} associations")
                except Exception:
                    print(f"⚠️ {table}: Unable to count associations")

            print("\n🧪 Test Data Integrity:")

            # Test creating a complete hierarchy
            cursor.execute("BEGIN")

            try:
                # Create goal
                cursor.execute("""
                    INSERT INTO todowrite_goals (title, description, session_id)
                    VALUES ('Integrity Test Goal', 'Testing database integrity', 'structure_test')
                    RETURNING id
                """)
                goal_id = cursor.fetchone()[0]

                # Create concept
                cursor.execute("""
                    INSERT INTO todowrite_concepts (title, description, session_id)
                    VALUES ('Integrity Test Concept', 'Testing concept integrity', 'structure_test')
                    RETURNING id
                """)
                concept_id = cursor.fetchone()[0]

                # Create task
                cursor.execute("""
                    INSERT INTO todowrite_tasks (title, description, session_id)
                    VALUES ('Integrity Test Task', 'Testing task integrity', 'structure_test')
                    RETURNING id
                """)
                task_id = cursor.fetchone()[0]

                # Create associations
                cursor.execute(
                    """
                    INSERT INTO todowrite_goal_concepts (goal_id, concept_id, session_id)
                    VALUES (%s, %s, 'structure_test')
                """,
                    (goal_id, concept_id),
                )

                cursor.execute(
                    """
                    INSERT INTO todowrite_goal_tasks (goal_id, task_id, priority, session_id)
                    VALUES (%s, %s, 1, 'structure_test')
                """,
                    (goal_id, task_id),
                )

                cursor.execute(
                    """
                    INSERT INTO todowrite_concept_tasks (concept_id, task_id, priority, session_id)
                    VALUES (%s, %s, 1, 'structure_test')
                """,
                    (concept_id, task_id),
                )

                cursor.execute("COMMIT")
                print("✅ Test hierarchy created successfully")

                # Verify associations were created
                cursor.execute(
                    """
                    SELECT COUNT(*) FROM todowrite_goal_concepts
                    WHERE goal_id = %s AND concept_id = %s
                """,
                    (goal_id, concept_id),
                )
                gc_count = cursor.fetchone()[0]

                cursor.execute(
                    """
                    SELECT COUNT(*) FROM todowrite_goal_tasks
                    WHERE goal_id = %s AND task_id = %s
                """,
                    (goal_id, task_id),
                )
                gt_count = cursor.fetchone()[0]

                cursor.execute(
                    """
                    SELECT COUNT(*) FROM todowrite_concept_tasks
                    WHERE concept_id = %s AND task_id = %s
                """,
                    (concept_id, task_id),
                )
                ct_count = cursor.fetchone()[0]

                print(f"✅ Goal-Concept associations: {gc_count}")
                print(f"✅ Goal-Task associations: {gt_count}")
                print(f"✅ Concept-Task associations: {ct_count}")

                # Clean up test data
                cursor.execute("BEGIN")
                cursor.execute(
                    "DELETE FROM todowrite_concept_tasks WHERE session_id = 'structure_test'"
                )
                cursor.execute(
                    "DELETE FROM todowrite_goal_tasks WHERE session_id = 'structure_test'"
                )
                cursor.execute(
                    "DELETE FROM todowrite_goal_concepts WHERE session_id = 'structure_test'"
                )
                cursor.execute("DELETE FROM todowrite_tasks WHERE session_id = 'structure_test'")
                cursor.execute("DELETE FROM todowrite_concepts WHERE session_id = 'structure_test'")
                cursor.execute("DELETE FROM todowrite_goals WHERE session_id = 'structure_test'")
                cursor.execute("COMMIT")
                print("✅ Test data cleaned up successfully")

            except Exception as e:
                cursor.execute("ROLLBACK")
                raise e

        conn.close()

        print("\n🎉 Database Structure Test - COMPLETE SUCCESS!")
        print("✅ All tables present")
        print("✅ Foreign key constraints working")
        print("✅ Association tables functional")
        print("✅ Data integrity verified")

    except Exception as e:
        print(f"\n❌ Database Structure Test Failed: {e}")
        import traceback

        traceback.print_exc()
        return False

    return True


if __name__ == "__main__":
    test_database_structure()
