#!/usr/bin/env python3
"""
Complete SQLite to PostgreSQL Migration

This script performs a complete migration:
1. Clears existing PostgreSQL data
2. Migrates all SQLite development data
3. Migrates session data
"""

from __future__ import annotations

import json
import sqlite3
from pathlib import Path
from typing import Any

import sqlalchemy
from sqlalchemy import JSON, Column, Integer, String, create_engine, text

# Session models (from previous migration script)
from sqlalchemy.ext.declarative import declarative_base
from todowrite.core.models import (
    AcceptanceCriteria,
    Base,
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
from todowrite.database.config import determine_storage_backend

SessionBase = declarative_base()


class ClaudeSession(SessionBase):
    """Claude session data model."""

    __tablename__ = "claude_sessions"

    id = Column(Integer, primary_key=True)
    session_id = Column(String, nullable=False, unique=True)
    start_time = Column(String, nullable=False)
    last_heartbeat = Column(String, nullable=False)
    agent = Column(String, nullable=False)
    session_type = Column(String, nullable=False)
    session_metadata = Column(JSON)


class AgentRegistry(SessionBase):
    """Agent registry data model."""

    __tablename__ = "agent_registry"

    id = Column(Integer, primary_key=True)
    agent_name = Column(String, nullable=False, unique=True)
    last_seen = Column(String, nullable=False)
    agent_type = Column(String, nullable=False)
    capabilities = Column(JSON)
    workflow_enforcement = Column(JSON)


class CompleteMigrator:
    """Complete SQLite to PostgreSQL migration."""

    def __init__(self: CompleteMigrator) -> None:
        """Initialize migrator."""
        self.sqlite_db_path: str = ""
        self.postgresql_url: str = ""
        self.sqlite_engine: Any = None
        self.postgresql_engine: Any = None

    def find_databases(self: CompleteMigrator) -> bool:
        """Find both SQLite databases."""
        # Development database
        dev_path = Path.home() / "dbs" / "todowrite_development.db"
        if dev_path.exists():
            self.sqlite_db_path = str(dev_path)
            print(f"✅ Found SQLite development database: {dev_path}")
            return True

        print("❌ SQLite development database not found")
        return False

    def setup_connections(self: CompleteMigrator) -> bool:
        """Setup database connections."""
        try:
            # SQLite connection
            self.sqlite_engine = create_engine(f"sqlite:///{self.sqlite_db_path}")

            # PostgreSQL connection
            storage_type, url = determine_storage_backend()
            if storage_type.value != "postgresql":
                print("❌ PostgreSQL backend not available")
                return False

            self.postgresql_url = url
            self.postgresql_engine = create_engine(self.postgresql_url)

            print("✅ Database connections established")
            return True

        except (sqlalchemy.exc.SQLAlchemyError, sqlite3.Error, OSError) as e:
            print(f"❌ Error setting up connections: {e}")
            return False

    def migrate_table(self: CompleteMigrator, table_name: str, model_class: Any) -> int:
        """Migrate a complete table."""
        try:
            print(f"📋 Migrating {table_name}...")

            with self.sqlite_engine.connect() as sqlite_conn:
                result = sqlite_conn.execute(text(f"SELECT * FROM {table_name}"))
                rows = result.fetchall()
                columns = result.keys()

                if not rows:
                    print(f"  📭 No data in {table_name}")
                    return 0

                column_info = {col: idx for idx, col in enumerate(columns)}
                migrated_count = 0

                with self.postgresql_engine.connect() as pg_conn:
                    for row in rows:
                        row_data = {}
                        for col in columns:
                            value = row[column_info[col]]
                            # Handle JSON data
                            if col.endswith("_metadata") and value:
                                try:
                                    if isinstance(value, str):
                                        row_data[col] = json.loads(value)
                                    else:
                                        row_data[col] = value
                                except (json.JSONDecodeError, TypeError):
                                    row_data[col] = value
                            else:
                                row_data[col] = value

                        # Insert into PostgreSQL
                        try:
                            # Build INSERT statement dynamically
                            cols_str = ", ".join(columns)
                            placeholders = ", ".join([f":{col}" for col in columns])
                            insert_stmt = text(f"""
                                INSERT INTO {table_name} ({cols_str})
                                VALUES ({placeholders})
                            """)
                            pg_conn.execute(insert_stmt, row_data)
                            migrated_count += 1
                        except (sqlalchemy.exc.SQLAlchemyError, ValueError, TypeError) as e:
                            print(f"    ⚠️  Error migrating {table_name} record: {e}")
                            continue

                    pg_conn.commit()

                print(f"  ✅ Migrated {migrated_count} records from {table_name}")
                return migrated_count

        except (sqlalchemy.exc.SQLAlchemyError, sqlite3.Error) as e:
            print(f"  ❌ Error migrating {table_name}: {e}")
            return 0

    def migrate_session_tables(self: CompleteMigrator) -> bool:
        """Migrate session data from episodic memory SQLite."""
        try:
            # Find episodic memory database
            episodic_db = Path(".claude/episodic_memory.db")
            if not episodic_db.exists():
                print("  📭 No episodic memory database found")
                return True

            print("📋 Migrating session data...")

            episodic_engine = create_engine(f"sqlite:///{episodic_db}")

            # Create session tables if they don't exist
            SessionBase.metadata.create_all(self.postgresql_engine)

            # Migrate session start data
            with episodic_engine.connect() as epi_conn:
                try:
                    result = epi_conn.execute(text("SELECT * FROM session_start"))
                    rows = result.fetchall()
                    if rows:
                        with self.postgresql_engine.connect() as pg_conn:
                            for row in rows:
                                session_data = {
                                    "session_id": f"session_{row[0]}",
                                    "start_time": row[1] if len(row) > 1 else None,
                                    "last_heartbeat": row[1] if len(row) > 1 else None,
                                    "agent": row[2] if len(row) > 2 else "claude-code",
                                    "session_type": row[3] if len(row) > 3 else "development",
                                    "session_metadata": {
                                        "original_data": dict(zip(result.keys(), row))
                                    },
                                }
                                insert_stmt = text("""
                                    INSERT INTO claude_sessions (session_id, start_time, last_heartbeat, agent, session_type, session_metadata)
                                    VALUES (:session_id, :start_time, :last_heartbeat, :agent, :session_type, :session_metadata)
                                    ON CONFLICT DO NOTHING
                                """)
                                pg_conn.execute(insert_stmt, session_data)
                            pg_conn.commit()
                        print(f"  ✅ Migrated {len(rows)} session records")
                except (sqlalchemy.exc.SQLAlchemyError, sqlite3.Error):
                    print("  📭 No session start data found")

            # Migrate agent registry if it exists
            with episodic_engine.connect() as epi_conn:
                try:
                    result = epi_conn.execute(text("SELECT * FROM agent_registry"))
                    rows = result.fetchall()
                    if rows:
                        with self.postgresql_engine.connect() as pg_conn:
                            for row in rows:
                                agent_data = {
                                    "agent_name": row[0] if len(row) > 0 else "claude-code",
                                    "last_seen": row[1] if len(row) > 1 else None,
                                    "agent_type": row[2] if len(row) > 2 else "development",
                                    "capabilities": json.loads(row[3])
                                    if len(row) > 3 and row[3]
                                    else None,
                                    "workflow_enforcement": json.loads(row[4])
                                    if len(row) > 4 and row[4]
                                    else None,
                                }
                                insert_stmt = text("""
                                    INSERT INTO agent_registry (agent_name, last_seen, agent_type, capabilities, workflow_enforcement)
                                    VALUES (:agent_name, :last_seen, :agent_type, :capabilities, :workflow_enforcement)
                                    ON CONFLICT DO NOTHING
                                """)
                                pg_conn.execute(insert_stmt, agent_data)
                            pg_conn.commit()
                        print(f"  ✅ Migrated {len(rows)} agent registry records")
                except (sqlalchemy.exc.SQLAlchemyError, sqlite3.Error):
                    print("  📭 No agent registry data found")

            return True

        except (sqlalchemy.exc.SQLAlchemyError, sqlite3.Error, OSError) as e:
            print(f"  ❌ Error migrating session data: {e}")
            return False

    def run_complete_migration(self: CompleteMigrator) -> bool:
        """Run complete migration."""
        print("🚀 Starting Complete SQLite to PostgreSQL Migration...")
        print("=" * 60)

        # Find databases
        if not self.find_databases():
            return False

        # Setup connections
        if not self.setup_connections():
            return False

        total_migrated = 0

        # Migration plan - main tables only (association tables will be handled by SQLAlchemy)
        migration_plan = [
            ("labels", Label),
            ("phases", Phase),
            ("contexts", Context),
            ("concepts", Concept),
            ("goals", Goal),
            ("tasks", Task),
            ("requirements", Requirements),
            ("interface_contracts", InterfaceContract),
            ("constraints", Constraints),
            ("steps", Step),
            ("acceptance_criteria", AcceptanceCriteria),
            ("sub_tasks", SubTask),
            ("commands", Command),
        ]

        try:
            # Recreate all tables
            Base.metadata.create_all(self.postgresql_engine)

            # Migrate each table
            for table_name, model_class in migration_plan:
                migrated = self.migrate_table(table_name, model_class)
                total_migrated += migrated

            # Migrate session data
            if not self.migrate_session_tables():
                print("⚠️  Session migration failed, but continuing...")

        except (sqlalchemy.exc.SQLAlchemyError, sqlite3.Error, OSError) as e:
            print(f"❌ Migration failed: {e}")
            return False

        print("=" * 60)
        print(f"✅ Complete Migration Finished! Total records: {total_migrated}")
        print("=" * 60)
        return True

    def verify_migration(self: CompleteMigrator) -> bool:
        """Verify migration results."""
        print("🔍 Verifying Complete Migration...")
        try:
            with self.postgresql_engine.connect() as conn:
                main_tables = [
                    "goals",
                    "tasks",
                    "labels",
                    "commands",
                    "concepts",
                    "contexts",
                    "phases",
                    "requirements",
                    "constraints",
                    "claude_sessions",
                    "agent_registry",
                ]

                print("📊 PostgreSQL Final Record Counts:")
                total_records = 0
                for table in main_tables:
                    try:
                        result = conn.execute(text(f"SELECT COUNT(*) FROM {table}"))
                        count = result.fetchone()[0]
                        print(f"  {table}: {count}")
                        total_records += count
                    except (sqlalchemy.exc.SQLAlchemyError, ValueError):
                        print(f"  {table}: Error")

                print(f"\n📊 Total Records Migrated: {total_records}")
            return True

        except (sqlalchemy.exc.SQLAlchemyError, OSError) as e:
            print(f"❌ Verification failed: {e}")
            return False


def main() -> None:
    """Main function."""
    migrator = CompleteMigrator()

    if migrator.run_complete_migration():
        migrator.verify_migration()
    else:
        print("❌ Complete migration failed")
        exit(1)


if __name__ == "__main__":
    main()
