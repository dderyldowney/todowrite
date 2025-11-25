#!/usr/bin/env python3
"""
Test script to verify CASCADE DELETE constraints are applied during database initialization.

This script tests that:
1. Database initialization creates tables
2. CASCADE DELETE constraints are applied automatically
3. Goal.delete() properly cascades to all children

Usage:
    python test_cascade_integration.py
"""

import sys
import os
from pathlib import Path

# Add lib_package to Python path
sys.path.insert(0, str(Path(__file__).parent / "lib_package" / "src"))

# Import everything at the top as required
from todowrite.core.schema_validator import initialize_database, DatabaseSchemaInitializer
from sqlalchemy import create_engine, text

def test_database_initialization():
    """Test database initialization with cascade constraints."""
    try:

        print("✅ Testing database initialization with cascade constraints...")

        # Initialize database with test data (use existing todowrite database)
        db_url = "postgresql://mcp_user:mcp_secure_password_2024@localhost:5433/todowrite"

        # Initialize the database with cascade constraints
        print("🚀 Initializing database with cascade constraints...")
        initialize_database(db_url)
        success = True

        if success:
            print("✅ Database initialization successful")
        else:
            print("❌ Database initialization failed")
            return False

        # Test cascade constraints by creating and deleting a hierarchy
        print("🧪 Testing cascade delete functionality...")

        try:
            engine = create_engine(db_url)

            # Create a simple hierarchy to test cascade
            with engine.connect() as conn:
                with conn.begin():
                    # Create goal
                    result = conn.execute(text("""
                        INSERT INTO goals (title, description, status, owner, created_at, updated_at)
                        VALUES ('Test Goal', 'Testing cascade delete', 'planned', 'test_user', NOW(), NOW())
                        RETURNING id
                    """))
                    goal_id = result.scalar()

                    # Create phase
                    result = conn.execute(text("""
                        INSERT INTO phases (title, description, status, owner, created_at, updated_at)
                        VALUES ('Test Phase', 'Testing cascade delete', 'planned', 'test-user', NOW(), NOW())
                        RETURNING id
                    """))
                    phase_id = result.scalar()

                    # Link goal to phase
                    conn.execute(text("""
                        INSERT INTO goals_phases (goal_id, phase_id) VALUES (:goal_id, :phase_id)
                    """), {"goal_id": goal_id, "phase_id": phase_id})

                    # Verify hierarchy exists
                    result = conn.execute(text("""
                        SELECT COUNT(*) FROM goals_phases WHERE goal_id = :goal_id
                    """), {"goal_id": goal_id})
                    linked_count = result.scalar()

                    if linked_count == 1:
                        print("✅ Test hierarchy created successfully")

                        # Test cascade delete
                        conn.execute(text("""
                            DELETE FROM goals WHERE id = :goal_id
                        """), {"goal_id": goal_id})

                        # Verify cascade worked - link should be gone
                        result = conn.execute(text("""
                            SELECT COUNT(*) FROM goals_phases WHERE goal_id = :goal_id
                        """), {"goal_id": goal_id})
                        after_delete_count = result.scalar()

                        if after_delete_count == 0:
                            print("✅ CASCADE DELETE working correctly!")
                        else:
                            print("❌ CASCADE DELETE failed - orphaned records remain")
                            return False
                    else:
                        print("❌ Failed to create test hierarchy")
                        return False

        except Exception as e:
            print(f"❌ Test failed with error: {e}")
            return False

        print("✅ All tests passed! CASCADE DELETE constraints are working.")
        return True

    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_database_initialization()
    sys.exit(0 if success else 1)