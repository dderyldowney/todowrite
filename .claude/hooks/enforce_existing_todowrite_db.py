#!/usr/bin/env python3
"""
ENFORCEMENT: Use Existing ToDoWrite Models API with PostgreSQL
This hook enforces that ALL work uses YOUR existing ToDoWrite system
NO parallel database creation - ONLY use existing models from lib_package
"""

import subprocess
import sys
import os
import json
import psycopg2
from psycopg2.extras import RealDictCursor
from datetime import datetime
from pathlib import Path

# Add lib_package to path to import existing ToDoWrite Models API
sys.path.insert(0, str(Path(__file__).parent.parent.parent / 'lib_package' / 'src'))

try:
    from todowrite.core.models import (
        Goal, Concept, Context, Constraints, Requirements,
        AcceptanceCriteria, InterfaceContract, Phase, Step,
        Task, SubTask, Command, Label, Base
    )
    from todowrite.core.schema_validator import get_schema_validator
    print("✅ Successfully imported existing ToDoWrite Models API")
except ImportError as e:
    print(f"❌ FAILED to import existing ToDoWrite Models API: {e}")
    print("   🚨 CRITICAL: Cannot proceed without existing models")
    sys.exit(1)

class ExistingToDoWriteEnforcer:
    def __init__(self):
        # Use the existing database utilities for proper naming
        from todowrite.utils.database_utils import get_project_database_name, get_database_path

        self.project_name = Path.cwd().name
        self.db_config = {
            'host': 'localhost',
            'port': 5433,
            'database': 'mcp_tools',  # Use existing MCP PostgreSQL container
            'user': 'mcp_user',
            'password': 'mcp_secure_password_2024'
        }

        # Get proper database name using existing utilities
        self.proper_db_name = get_project_database_name("development", self.project_name)
        self.session_id = self._get_or_create_session()

    def enforce_existing_models_usage(self):
        """Mandatory enforcement that ALL work uses existing ToDoWrite Models API"""
        print("🔒 ENFORCING EXISTING ToDoWrite Models API")
        print("   REQUIREMENT: ALL development MUST use existing lib_package Models")
        print(f"   Project: {self.project_name}")
        print(f"   Database: {self.proper_db_name}")
        print(f"   Session: {self.session_id}")

        # 1. Verify PostgreSQL container is running with todowrite database
        if not self._verify_postgresql_container():
            print("❌ CRITICAL: todowrite-postgres container not running")
            print("   🚨 Starting todowrite-postgres container...")
            if not self._start_todowrite_postgres():
                print("❌ FAILED to start todowrite-postgres container")
                sys.exit(1)

        # 2. Verify we can connect and that todowrite database exists
        if not self._verify_database_connection():
            print("❌ CRITICAL: Cannot connect to todowrite database")
            sys.exit(1)

        # 3. Verify existing ToDoWrite Models API can be used
        if not self._verify_existing_models():
            print("❌ CRITICAL: Existing ToDoWrite Models API not functional")
            sys.exit(1)

        # 4. Verify session tracking works
        if not self._verify_session_tracking():
            print("❌ CRITICAL: Session tracking not working")
            sys.exit(1)

        # 5. Create/update session record
        self._update_session_record()

        print("✅ EXISTING ToDoWrite Models API ENFORCEMENT PASSED")
        print("   📚 Models API: Ready (Goal → ... → Command)")
        print("   🗄️  Database: Connected (todowrite)")
        print("   📝 Session: Tracked")
        print("   🔒 ENFORCEMENT: All work MUST use existing Models API")
        print("")

    def _verify_postgresql_container(self):
        """Verify todowrite-postgres container is running"""
        try:
            result = subprocess.run([
                'docker', 'ps', '--filter', 'name=todowrite-postgres', '--format', '{{.Status}}'
            ], capture_output=True, text=True, timeout=10)
            return result.returncode == 0 and 'Up' in result.stdout
        except Exception:
            return False

    def _start_todowrite_postgres(self):
        """Start todowrite-postgres container using existing configuration"""
        try:
            # Change to project root to find the docker-compose file
            project_root = Path(__file__).parent.parent.parent
            docker_compose_file = project_root / ".claude" / "docker" / "todowrite-postgres.yml"

            if not docker_compose_file.exists():
                print(f"   ❌ Docker compose file not found: {docker_compose_file}")
                return False

            result = subprocess.run([
                'docker-compose', '-f', str(docker_compose_file), 'up', '-d'
            ], capture_output=True, text=True, cwd=project_root, timeout=60)

            if result.returncode != 0:
                print(f"   ❌ Docker compose failed: {result.stderr}")
                return False

            print("   ✅ Container started, waiting for database...")
            import time
            time.sleep(15)  # Wait for database to be ready
            return True

        except Exception as e:
            print(f"   ❌ Error starting container: {e}")
            return False

    def _verify_database_connection(self):
        """Verify connection to todowrite database"""
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

    def _verify_existing_models(self):
        """Verify that existing ToDoWrite Models API is functional"""
        try:
            # Test that we can create instances of existing models
            test_goal = Goal(
                title="Database Enforcement Test",
                description="Testing existing ToDoWrite Models API functionality"
            )

            test_session = {"test": True, "enforced": True}

            # Test that the Base class exists
            if not hasattr(Base, 'metadata'):
                print("   ❌ Base class not found in existing models")
                return False

            print("   ✅ Existing Models API: Goal, Concept, Context, etc. available")
            return True

        except Exception as e:
            print(f"   ❌ Existing models verification failed: {e}")
            return False

    def _verify_session_tracking(self):
        """Verify session tracking table works"""
        try:
            conn = psycopg2.connect(**self.db_config)
            with conn.cursor() as cursor:
                # Create session record
                cursor.execute("""
                    INSERT INTO todowrite_sessions (session_id, title, status, environment)
                    VALUES (%s, 'Existing Models Enforcement', 'active', %s)
                    ON CONFLICT (session_id)
                    DO UPDATE SET
                        last_activity = NOW(),
                        updated_at = NOW()
                """, (self.session_id, json.dumps({
                    'models_api': 'existing',
                    'project': self.project_name,
                    'enforced': True
                })))

                conn.commit()

                # Verify insertion
                cursor.execute("SELECT COUNT(*) FROM todowrite_sessions WHERE session_id = %s", (self.session_id,))
                count = cursor.fetchone()[0]

            conn.close()
            return count > 0

        except Exception as e:
            print(f"   Session tracking verification failed: {e}")
            return False

    def _update_session_record(self):
        """Update current session record"""
        try:
            conn = psycopg2.connect(**self.db_config)
            with conn.cursor() as cursor:
                cursor.execute("""
                    UPDATE todowrite_sessions
                    SET last_activity = NOW(),
                        context = context || %s
                    WHERE session_id = %s
                """, (
                    json.dumps({
                        'enforcement_check': {
                            'timestamp': datetime.now().isoformat(),
                            'models_api': 'existing',
                            'status': 'verified',
                            'enforcement': 'active'
                        }
                    }),
                    self.session_id
                ))
                conn.commit()
            conn.close()
        except Exception as e:
            print(f"   ⚠️  Could not update session record: {e}")

    def _get_or_create_session_id(self):
        """Get or create session ID using existing pattern"""
        # Use existing session ID if available
        session_id = os.environ.get('TODOWRITE_SESSION_ID')

        if not session_id:
            # Create session ID following existing pattern
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            session_id = f"todowrite_session_{timestamp}_{os.getpid()}"
            os.environ['TODOWRITE_SESSION_ID'] = session_id

        return session_id

def main():
    """Main enforcement function"""
    print("🚨 ENFORCING USE OF EXISTING ToDoWrite Models API")
    print("   NO PARALLEL IMPLEMENTATION - ONLY USE EXISTING lib_package MODELS")
    print("")

    enforcer = ExistingToDoWriteEnforcer()
    enforcer.enforce_existing_models_usage()

if __name__ == "__main__":
    main()