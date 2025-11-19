#!/usr/bin/env python3
"""
PostgreSQL Development Database Setup

This script initializes the PostgreSQL development database for ToDoWrite.
It handles:
1. Docker PostgreSQL container startup
2. Database creation if it doesn't exist
3. Schema import for all models and association tables
4. Verification that the development database is ready
"""

from __future__ import annotations

import subprocess
import time
from pathlib import Path
from typing import Any

from sqlalchemy import create_engine, text
from todowrite.core.models import Base
from todowrite.database.config import (
    get_docker_postgresql_candidates,
    is_docker_postgresql_running,
)


class PostgreSQLDevelopmentSetup:
    """Handles PostgreSQL development database setup and initialization."""

    def __init__(self: PostgreSQLDevelopmentSetup) -> None:
        """Initialize PostgreSQL setup."""
        self.database_url: str | None = None
        self.engine: Any = None

    def ensure_docker_postgresql_running(self: PostgreSQLDevelopmentSetup) -> bool:
        """Ensure Docker PostgreSQL container is running."""
        print("🐳 Checking Docker PostgreSQL availability...")

        # Check if Docker PostgreSQL is already running
        if is_docker_postgresql_running():
            print("✅ Docker PostgreSQL is already running")
            candidates = get_docker_postgresql_candidates()
            if candidates:
                self.database_url = candidates[0]
                return True

        # Try to start Docker PostgreSQL using docker-compose
        print("🚀 Starting Docker PostgreSQL container...")
        try:
            # Navigate to tests directory and start PostgreSQL with persistent volume
            result = subprocess.run(
                ["docker", "compose", "up", "-d", "postgres"],
                cwd=Path("tests"),
                capture_output=True,
                text=True,
                timeout=60,
            )

            if result.returncode != 0:
                print(f"❌ Failed to start Docker PostgreSQL: {result.stderr}")
                return False

            print("✅ Docker PostgreSQL container started with persistent volume")

            # Wait for PostgreSQL to be ready
            for attempt in range(30):  # Wait up to 30 seconds
                if is_docker_postgresql_running():
                    candidates = get_docker_postgresql_candidates()
                    if candidates:
                        self.database_url = candidates[0]
                        break
                time.sleep(1)
            else:
                print("❌ Docker PostgreSQL failed to become ready")
                return False

            return True

        except subprocess.TimeoutExpired:
            print("❌ Timeout starting Docker PostgreSQL")
            return False
        except Exception as e:
            print(f"❌ Error starting Docker PostgreSQL: {e}")
            return False

    def create_development_database(self: PostgreSQLDevelopmentSetup) -> bool:
        """Create the development database if it doesn't exist."""
        if not self.database_url:
            print("❌ No database URL available")
            return False

        print("🗄️  Setting up development database...")

        try:
            # Connect to PostgreSQL server (without specifying database)
            server_url = self.database_url.rsplit("/", 1)[0]  # Remove database name

            # Create engine for server connection
            server_engine = create_engine(server_url)

            # Check if todowrite database exists
            with server_engine.connect() as conn:
                # Don't use transaction for database creation
                conn.execute(text("COMMIT"))  # End any existing transaction

                try:
                    # Check if database exists
                    result = conn.execute(
                        text("SELECT 1 FROM pg_database WHERE datname = 'todowrite'")
                    )
                    db_exists = result.fetchone() is not None

                    if not db_exists:
                        print("📝 Creating todowrite development database...")
                        conn.execute(text("CREATE DATABASE todowrite"))
                        conn.commit()
                        print("✅ Development database created")
                    else:
                        print("✅ Development database already exists")

                except Exception as e:
                    print(f"❌ Error checking/creating database: {e}")
                    return False
                finally:
                    server_engine.dispose()

            # Now connect to the specific database
            print(f"🔗 Connecting to development database: {self.database_url}")
            self.engine = create_engine(self.database_url)

            return True

        except Exception as e:
            print(f"❌ Error setting up development database: {e}")
            return False

    def import_schemas(self: PostgreSQLDevelopmentSetup) -> bool:
        """Import schemas for all models and association tables."""
        if not self.engine:
            print("❌ No database engine available")
            return False

        print("📋 Importing database schemas...")

        try:
            # Create all tables defined in the models
            Base.metadata.create_all(self.engine)
            print("✅ Database schemas imported successfully")

            # Verify tables were created
            with self.engine.connect() as conn:
                result = conn.execute(
                    text("""
                    SELECT table_name
                    FROM information_schema.tables
                    WHERE table_schema = 'public'
                    ORDER BY table_name
                """)
                )
                tables = [row[0] for row in result.fetchall()]
                print(f"📊 Tables created: {', '.join(tables)}")

            return True

        except Exception as e:
            print(f"❌ Error importing schemas: {e}")
            return False

    def verify_setup(self: PostgreSQLDevelopmentSetup) -> bool:
        """Verify the PostgreSQL development setup is working."""
        if not self.engine:
            print("❌ No database engine available")
            return False

        print("🔍 Verifying database setup...")

        try:
            # Test basic database operations
            with self.engine.connect() as conn:
                # Test connection
                result = conn.execute(text("SELECT 1 as test"))
                test_value = result.fetchone()[0]
                if test_value != 1:
                    print("❌ Database connection test failed")
                    return False

                # Test model tables exist and are accessible
                tables_to_check = ["goals", "tasks", "labels", "commands"]
                for table in tables_to_check:
                    try:
                        result = conn.execute(text(f"SELECT COUNT(*) FROM {table}"))
                        count = result.fetchone()[0]
                        print(f"  ✅ {table}: {count} records")
                    except Exception as e:
                        print(f"  ❌ {table}: Error - {e}")

            print("✅ PostgreSQL development database verification complete")
            return True

        except Exception as e:
            print(f"❌ Error verifying setup: {e}")
            return False

    def setup_postgresql_development(self: PostgreSQLDevelopmentSetup) -> bool:
        """Complete PostgreSQL development setup process."""
        print("🚀 Setting up PostgreSQL development environment...")
        print("=" * 60)

        success = (
            self.ensure_docker_postgresql_running()
            and self.create_development_database()
            and self.import_schemas()
            and self.verify_setup()
        )

        if success:
            print("=" * 60)
            print("✅ PostgreSQL development environment ready!")
            print(f"📍 Database URL: {self.database_url}")
            print("=" * 60)
            # Set environment variable for the current session
            import os

            os.environ["TODOWRITE_DATABASE_URL"] = self.database_url

            # Also write to a file so shell can source it
            env_file = Path(".claude/postgresql_env.sh")
            with open(env_file, "w") as f:
                f.write(f'export TODOWRITE_DATABASE_URL="{self.database_url}"\n')
            print(f"🔧 PostgreSQL URL exported to: {env_file}")
        else:
            print("=" * 60)
            print("❌ PostgreSQL development setup failed")
            print("=" * 60)

        return success


def main() -> None:
    """Main function for PostgreSQL development setup."""
    setup = PostgreSQLDevelopmentSetup()
    success = setup.setup_postgresql_development()

    if not success:
        print("❌ Failed to setup PostgreSQL development environment")
        exit(1)


if __name__ == "__main__":
    main()
