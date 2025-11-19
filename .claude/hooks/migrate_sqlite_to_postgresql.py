#!/usr/bin/env python3
"""
SQLite to PostgreSQL Migration Script

This script migrates data from the existing SQLite development database
to the new PostgreSQL development database, preserving all existing
data and relationships.
"""

from __future__ import annotations

import json
import sqlite3
from pathlib import Path
from typing import Any

import sqlalchemy
from sqlalchemy import JSON, Column, Integer, String, create_engine, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Create session models for migration
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
from todowrite.database.config import determine_storage_backend


class SQLiteToPostgreSQLMigrator:
    """Handles migration from SQLite to PostgreSQL."""

    def __init__(self: SQLiteToPostgreSQLMigrator) -> None:
        """Initialize migrator."""
        self.sqlite_db_path: str = ""
        self.postgresql_url: str = ""
        self.sqlite_engine: Any = None
        self.postgresql_engine: Any = None
        self.sqlite_session: Any = None
        self.postgresql_session: Any = None

    def find_sqlite_database(self: SQLiteToPostgreSQLMigrator) -> bool:
        """Find the SQLite development database."""
        # Common SQLite development database locations
        possible_paths = [
            str(Path.home() / "dbs" / "todowrite_development.db"),
            "todowrite_development.db",
            "data/todowrite.db",
            "todowrite.db",
        ]

        for path in possible_paths:
            if Path(path).exists():
                self.sqlite_db_path = path
                print(f"✅ Found SQLite database: {path}")
                return True

        print("❌ SQLite development database not found")
        return False

    def setup_connections(self: SQLiteToPostgreSQLMigrator) -> bool:
        """Setup database connections."""
        try:
            # SQLite connection
            self.sqlite_engine = create_engine(f"sqlite:///{self.sqlite_db_path}")
            SQLiteSession = sessionmaker(bind=self.sqlite_engine)
            self.sqlite_session = SQLiteSession()

            # PostgreSQL connection
            storage_type, url = determine_storage_backend()
            if storage_type.value != "postgresql":
                print("❌ PostgreSQL backend not available")
                return False

            self.postgresql_url = url
            self.postgresql_engine = create_engine(self.postgresql_url)
            PostgreSQLSession = sessionmaker(bind=self.postgresql_engine)
            self.postgresql_session = PostgreSQLSession()

            print("✅ Database connections established")
            return True

        except (
            sqlalchemy.exc.SQLAlchemyError,
            sqlalchemy.exc.DBAPIError,
            sqlite3.Error,
            OSError,
        ) as e:
            print(f"❌ Error setting up connections: {e}")
            return False

    def create_session_tables(self: SQLiteToPostgreSQLMigrator) -> None:
        """Create session tables in PostgreSQL."""
        try:
            SessionBase.metadata.create_all(self.postgresql_engine)
            print("✅ Session tables created in PostgreSQL")
        except (sqlalchemy.exc.SQLAlchemyError, sqlalchemy.exc.DBAPIError) as e:
            print(f"⚠️  Error creating session tables: {e}")
            # Don't fail migration if session tables can't be created

    def migrate_table_data(
        self: SQLiteToPostgreSQLMigrator, table_name: str, model_class: Any
    ) -> int:
        """Migrate data from a specific table."""
        try:
            # Get data from SQLite
            result = self.sqlite_session.execute(text(f"SELECT * FROM {table_name}"))
            rows = result.fetchall()
            columns = result.keys()

            if not rows:
                print(f"  📭 No data in {table_name}")
                return 0

            # Get column info from result
            column_info = {col: idx for idx, col in enumerate(columns)}

            migrated_count = 0
            for row in rows:
                # Convert row to dict
                row_data = {}
                for col in columns:
                    value = row[column_info[col]]
                    # Handle JSON data conversion
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

                # Create new record in PostgreSQL
                try:
                    new_record = model_class(**row_data)
                    self.postgresql_session.add(new_record)
                    migrated_count += 1
                except (sqlalchemy.exc.SQLAlchemyError, ValueError, TypeError) as e:
                    print(f"    ⚠️  Error migrating {table_name} record: {e}")
                    continue

            self.postgresql_session.commit()
            print(f"  ✅ Migrated {migrated_count} records from {table_name}")
            return migrated_count

        except (sqlalchemy.exc.SQLAlchemyError, sqlite3.Error) as e:
            print(f"  ❌ Error migrating {table_name}: {e}")
            self.postgresql_session.rollback()
            return 0

    def migrate_association_table(self: SQLiteToPostgreSQLMigrator, table_name: str) -> int:
        """Migrate association table data."""
        try:
            result = self.sqlite_session.execute(text(f"SELECT * FROM {table_name}"))
            rows = result.fetchall()
            columns = result.keys()

            if not rows:
                print(f"  📭 No data in {table_name}")
                return 0

            column_info = {col: idx for idx, col in enumerate(columns)}
            migrated_count = 0

            for row in rows:
                row_data = {col: row[column_info[col]] for col in columns}

                # Insert directly into PostgreSQL association table
                insert_stmt = text(f"""
                    INSERT INTO {table_name} ({", ".join(columns)})
                    VALUES ({", ".join([f":{col}" for col in columns])})
                    ON CONFLICT DO NOTHING
                """)

                try:
                    self.postgresql_session.execute(insert_stmt, row_data)
                    migrated_count += 1
                except (sqlalchemy.exc.SQLAlchemyError, ValueError) as e:
                    print(f"    ⚠️  Error migrating {table_name} association: {e}")
                    continue

            self.postgresql_session.commit()
            print(f"  ✅ Migrated {migrated_count} associations from {table_name}")
            return migrated_count

        except (sqlalchemy.exc.SQLAlchemyError, sqlite3.Error) as e:
            print(f"  ❌ Error migrating association table {table_name}: {e}")
            self.postgresql_session.rollback()
            return 0

    def run_migration(self: SQLiteToPostgreSQLMigrator) -> bool:
        """Run the complete migration."""
        print("🚀 Starting SQLite to PostgreSQL migration...")
        print("=" * 60)

        # Find SQLite database
        if not self.find_sqlite_database():
            return False

        # Setup connections
        if not self.setup_connections():
            return False

        # Create session tables in PostgreSQL
        self.create_session_tables()

        total_migrated = 0

        # Define table migration order (respecting foreign key dependencies)
        migration_plan = [
            # Basic entities first
            ("labels", Label),
            ("phases", Phase),
            ("contexts", Context),
            ("concepts", Concept),
            # Main entities
            ("goals", Goal),
            ("tasks", Task),
            ("requirements", Requirements),
            ("interface_contracts", InterfaceContract),
            ("constraints", Constraints),
            ("steps", Step),
            ("acceptance_criteria", AcceptanceCriteria),
            ("sub_tasks", SubTask),
            # Association tables (in dependency order)
            ("goals_labels", "association"),
            ("goals_contexts", "association"),
            ("goals_concepts", "association"),
            ("goals_phases", "association"),
            ("goals_tasks", "association"),
            ("tasks_labels", "association"),
            ("tasks_sub_tasks", "association"),
            ("requirements_labels", "association"),
            ("requirements_contexts", "association"),
            ("requirements_concepts", "association"),
            ("requirements_acceptance_criteria", "association"),
            ("concepts_contexts", "association"),
            ("concepts_labels", "association"),
            ("constraints_goals", "association"),
            ("constraints_labels", "association"),
            ("constraints_requirements", "association"),
            ("contexts_labels", "association"),
            ("phases_labels", "association"),
            ("phases_steps", "association"),
            ("steps_labels", "association"),
            ("steps_tasks", "association"),
            ("sub_tasks_labels", "association"),
            ("sub_tasks_commands", "association"),
            ("interface_contracts_labels", "association"),
            ("interface_contracts_phases", "association"),
            ("acceptance_criteria_labels", "association"),
            ("acceptance_criteria_interface_contracts", "association"),
            ("commands", Command),  # Last due to potential dependencies
            # Session and system data
            ("claude_sessions", ClaudeSession),
            ("agent_registry", AgentRegistry),
        ]

        try:
            for table_name, model_or_type in migration_plan:
                print(f"📋 Migrating {table_name}...")

                if model_or_type == "association":
                    migrated = self.migrate_association_table(table_name)
                else:
                    migrated = self.migrate_table_data(table_name, model_or_type)

                total_migrated += migrated

        except (sqlalchemy.exc.SQLAlchemyError, sqlite3.Error, OSError) as e:
            print(f"❌ Migration failed: {e}")
            return False

        finally:
            # Close sessions
            self.sqlite_session.close()
            self.postgresql_session.close()

        print("=" * 60)
        print(f"✅ Migration complete! Total records migrated: {total_migrated}")
        print("=" * 60)
        return True

    def verify_migration(self: SQLiteToPostgreSQLMigrator) -> bool:
        """Verify migration results."""
        print("🔍 Verifying migration results...")

        try:
            with self.postgresql_engine.connect() as conn:
                # Count records in main tables
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
                ]

                print("📊 PostgreSQL Record Counts:")
                for table in main_tables:
                    try:
                        result = conn.execute(text(f"SELECT COUNT(*) FROM {table}"))
                        count = result.fetchone()[0]
                        print(f"  {table}: {count}")
                    except (sqlalchemy.exc.SQLAlchemyError, ValueError):
                        print(f"  {table}: Error")

            return True

        except (sqlalchemy.exc.SQLAlchemyError, OSError) as e:
            print(f"❌ Verification failed: {e}")
            return False


def main() -> None:
    """Main migration function."""
    migrator = SQLiteToPostgreSQLMigrator()

    success = migrator.run_migration()
    if success:
        migrator.verify_migration()
    else:
        print("❌ Migration failed")
        exit(1)


if __name__ == "__main__":
    main()
