#!/usr/bin/env python3
"""Simple database test to debug tuple issues"""

import psycopg2


def test_database():
    db_config = {
        "host": "localhost",
        "port": 5433,
        "database": "mcp_tools",
        "user": "mcp_user",
        "password": "mcp_secure_password_2024",
    }

    try:
        conn = psycopg2.connect(**db_config)
        with conn.cursor() as cursor:
            # Test simple insert with return
            cursor.execute(
                """
                INSERT INTO todowrite_goals (title, description, session_id)
                VALUES (%s, %s, %s)
                RETURNING id
            """,
                ("Python Test Goal", "Test from Python", "python_test"),
            )

            result = cursor.fetchone()
            print(f"Result type: {type(result)}")
            print(f"Result value: {result}")
            print(f"Result[0] if available: {result[0] if result and len(result) > 0 else 'None'}")

            conn.commit()

        conn.close()
        print("✅ Database test successful")

    except Exception as e:
        print(f"❌ Database test failed: {e}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    test_database()
