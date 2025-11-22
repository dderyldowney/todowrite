#!/usr/bin/env python3
"""
Database Enforcement Hook - MANDATORY for all ToDoWrite sessions
This hook enforces that ALL work is stored in the PostgreSQL database
NO development work is permitted without database storage
"""

import json
import os
import subprocess
import sys
from datetime import datetime

import psycopg2
from psycopg2.extras import RealDictCursor


class DatabaseEnforcer:
    def __init__(self):
        self.db_config = {
            "host": "localhost",
            "port": 5433,
            "database": "todowrite",
            "user": "todowrite_user",
            "password": "todowrite_secure_2024",
        }
        self.session_id = self._get_or_create_session()

    def enforce_database_usage(self):
        """Mandatory database check before any session activity"""
        print("🔒 DATABASE ENFORCEMENT: Checking ToDoWrite PostgreSQL backend...")
        print("   REQUIREMENT: All development work MUST be stored in database")

        # 1. Verify database connectivity
        if not self._check_database_connection():
            self._start_database_container()
            if not self._check_database_connection():
                print("❌ CRITICAL: Cannot connect to todowrite-postgres database")
                print("   🚨 ALL SESSION ACTIVITY BLOCKED UNTIL DATABASE IS AVAILABLE")
                print(
                    "   🔧 Run: cd .claude && docker-compose -f docker/todowrite-postgres.yml up -d"
                )
                sys.exit(1)

        # 2. Verify database schema
        if not self._verify_database_schema():
            print("❌ CRITICAL: Database schema not properly initialized")
            print("   🚨 SESSION BLOCKED - Database initialization required")
            sys.exit(1)

        # 3. Verify current session tracking
        if not self._verify_session_tracking():
            print("❌ CRITICAL: Session tracking not functional")
            print("   🚨 SESSION BLOCKED - Session tracking required")
            sys.exit(1)

        # 4. Verify required tables exist
        if not self._verify_required_tables():
            print("❌ CRITICAL: Required tables missing")
            print("   🚨 SESSION BLOCKED - Complete table structure required")
            sys.exit(1)

        print("✅ DATABASE ENFORCEMENT PASSED")
        print("   📊 todowrite-postgres: Connected and ready")
        print("   🗄️  Schema: 12-layer hierarchy verified")
        print("   📝 Session: Tracked with ID:", self.session_id)
        print("   🔒 ENFORCEMENT: All work will be stored in database")
        print()

    def _get_or_create_session(self):
        """Get or create current session ID"""
        # Try to get existing session from environment
        session_id = os.environ.get("TODOWRITE_SESSION_ID")

        if not session_id:
            # Create new session ID
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            session_id = f"session_{timestamp}_{os.getpid()}"
            os.environ["TODOWRITE_SESSION_ID"] = session_id

        return session_id

    def _check_database_connection(self):
        """Check if PostgreSQL database is accessible"""
        try:
            conn = psycopg2.connect(**self.db_config)
            with conn.cursor() as cursor:
                cursor.execute("SELECT 1")
                result = cursor.fetchone()
            conn.close()
            return result[0] == 1
        except Exception as e:
            print(f"   Database connection failed: {e}")
            return False

    def _start_database_container(self):
        """Start the todowrite-postgres container"""
        print("   🚀 Starting todowrite-postgres container...")
        try:
            result = subprocess.run(
                ["docker-compose", "-f", "docker/todowrite-postgres.yml", "up", "-d"],
                capture_output=True,
                text=True,
                cwd=".",
                timeout=60,
            )

            if result.returncode == 0:
                print("   ✅ Container started, waiting for database...")
                import time

                time.sleep(10)  # Wait for database to initialize
            else:
                print(f"   ❌ Failed to start container: {result.stderr}")
        except Exception as e:
            print(f"   ❌ Error starting container: {e}")

    def _verify_database_schema(self):
        """Verify that the complete database schema exists"""
        try:
            conn = psycopg2.connect(**self.db_config)
            with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                # Check for core tables
                cursor.execute("""
                    SELECT table_name FROM information_schema.tables
                    WHERE table_schema = 'public'
                    AND table_name IN ('todowrite_items', 'todowrite_sessions', 'schema_migrations')
                """)
                tables = [row["table_name"] for row in cursor.fetchall()]

                required_tables = ["todowrite_items", "todowrite_sessions", "schema_migrations"]
                missing_tables = set(required_tables) - set(tables)

                if missing_tables:
                    print(f"   ❌ Missing tables: {missing_tables}")
                    return False

                # Check for all 12 layers in todowrite_items
                cursor.execute("SELECT DISTINCT layer FROM todowrite_items")
                layers = [row["layer"] for row in cursor.fetchall()]

                required_layers = [
                    "goal",
                    "concept",
                    "context",
                    "constraint",
                    "requirement",
                    "acceptance_criteria",
                    "interface_contract",
                    "phase",
                    "step",
                    "task",
                    "subtask",
                    "command",
                ]
                missing_layers = set(required_layers) - set(layers)

                if missing_layers:
                    print(f"   ❌ Missing layers in todowrite_items: {missing_layers}")
                    return False

            conn.close()
            return True

        except Exception as e:
            print(f"   ❌ Schema verification failed: {e}")
            return False

    def _verify_session_tracking(self):
        """Verify that session tracking is working"""
        try:
            conn = psycopg2.connect(**self.db_config)
            with conn.cursor() as cursor:
                # Try to insert/update session
                cursor.execute(
                    """
                    INSERT INTO todowrite_sessions (session_id, title, status, environment)
                    VALUES (%s, 'Database Enforcement Check', 'active', %s)
                    ON CONFLICT (session_id)
                    DO UPDATE SET
                        last_activity = NOW(),
                        updated_at = NOW()
                """,
                    (self.session_id, json.dumps({"checked_at": datetime.now().isoformat()})),
                )

                conn.commit()

                # Verify insertion
                cursor.execute(
                    "SELECT COUNT(*) FROM todowrite_sessions WHERE session_id = %s",
                    (self.session_id,),
                )
                count = cursor.fetchone()[0]

            conn.close()
            return count > 0

        except Exception as e:
            print(f"   ❌ Session tracking verification failed: {e}")
            return False

    def _verify_required_tables(self):
        """Verify that all required tables and constraints exist"""
        try:
            conn = psycopg2.connect(**self.db_config)
            with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                # Check todowrite_items table structure
                cursor.execute("""
                    SELECT column_name, data_type, is_nullable
                    FROM information_schema.columns
                    WHERE table_name = 'todowrite_items'
                    ORDER BY ordinal_position
                """)

                required_columns = [
                    "id",
                    "uuid",
                    "layer",
                    "parent_id",
                    "title",
                    "description",
                    "status",
                    "priority",
                    "level",
                    "path",
                    "content",
                    "metadata",
                    "created_at",
                    "updated_at",
                ]

                columns = [row["column_name"] for row in cursor.fetchall()]
                missing_columns = set(required_columns) - set(columns)

                if missing_columns:
                    print(f"   ❌ Missing columns in todowrite_items: {missing_columns}")
                    return False

                # Check constraints
                cursor.execute("""
                    SELECT constraint_name FROM information_schema.table_constraints
                    WHERE table_name = 'todowrite_items' AND constraint_type = 'CHECK'
                """)

                constraints = [row["constraint_name"] for row in cursor.fetchall()]
                if len(constraints) < 3:  # Should have several check constraints
                    print("   ❌ Insufficient constraints in todowrite_items")
                    return False

            conn.close()
            return True

        except Exception as e:
            print(f"   ❌ Required tables verification failed: {e}")
            return False

    def log_session_activity(self, activity_type, details=None):
        """Log session activity to database"""
        try:
            conn = psycopg2.connect(**self.db_config)
            with conn.cursor() as cursor:
                # Update session activity
                cursor.execute(
                    """
                    UPDATE todowrite_sessions
                    SET last_activity = NOW(),
                        actions = actions || %s
                    WHERE session_id = %s
                """,
                    (
                        json.dumps(
                            {
                                "type": activity_type,
                                "details": details or {},
                                "timestamp": datetime.now().isoformat(),
                            }
                        ),
                        self.session_id,
                    ),
                )
                conn.commit()
            conn.close()
        except Exception as e:
            print(f"   ⚠️  Could not log session activity: {e}")


def main():
    """Main enforcement function"""
    enforcer = DatabaseEnforcer()

    # Perform mandatory checks
    enforcer.enforce_database_usage()

    # Log enforcement check
    enforcer.log_session_activity(
        "database_enforcement_check",
        {"status": "passed", "message": "Database backend verified and ready for development work"},
    )


if __name__ == "__main__":
    main()
