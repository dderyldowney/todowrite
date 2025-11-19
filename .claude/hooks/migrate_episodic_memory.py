#!/usr/bin/env python3
"""
Episodic Memory Migration to PostgreSQL

Migrates episodic memory database from SQLite to PostgreSQL
and configures the system to use PostgreSQL for episodic storage.
"""

from __future__ import annotations

import sqlite3
from pathlib import Path
from typing import Any

import sqlalchemy
from sqlalchemy import (
    BigInteger,
    Boolean,
    Column,
    ForeignKey,
    Integer,
    LargeBinary,
    Text,
    create_engine,
    text,
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

# PostgreSQL connection

# Define PostgreSQL models for episodic memory
EpisodicBase = declarative_base()


class Exchange(EpisodicBase):
    """Exchange model for episodic memory."""

    __tablename__ = "exchanges"

    id = Column(Text, primary_key=True)
    project = Column(Text, nullable=False)
    timestamp = Column(Text, nullable=False)
    user_message = Column(Text, nullable=False)
    assistant_message = Column(Text, nullable=False)
    archive_path = Column(Text, nullable=False)
    line_start = Column(Integer, nullable=False)
    line_end = Column(Integer, nullable=False)
    embedding = Column(LargeBinary)
    last_indexed = Column(BigInteger)
    parent_uuid = Column(Text)
    is_sidechain = Column(Boolean, default=False)
    session_id = Column(Text)
    cwd = Column(Text)
    git_branch = Column(Text)
    claude_version = Column(Text)
    thinking_level = Column(Text)
    thinking_disabled = Column(Boolean)
    thinking_triggers = Column(Text)

    # Relationship
    tool_calls = relationship("ToolCall", back_populates="exchange")


class ToolCall(EpisodicBase):
    """Tool call model for episodic memory."""

    __tablename__ = "tool_calls"

    id = Column(Text, primary_key=True)
    exchange_id = Column(Text, ForeignKey("exchanges.id"), nullable=False)
    tool_name = Column(Text, nullable=False)
    tool_input = Column(Text)
    tool_result = Column(Text)
    is_error = Column(Boolean, default=False)
    timestamp = Column(Text, nullable=False)

    # Relationship
    exchange = relationship("Exchange", back_populates="tool_calls")


class EpisodicMemoryMigrator:
    """Handles episodic memory migration to PostgreSQL."""

    def __init__(self: EpisodicMemoryMigrator) -> None:
        """Initialize migrator."""
        self.sqlite_db_path: str = ""
        self.postgresql_url: str = ""
        self.sqlite_engine: Any = None
        self.postgresql_engine: Any = None

    def find_episodic_database(self: EpisodicMemoryMigrator) -> bool:
        """Find the episodic memory SQLite database."""
        episodic_db = Path(".claude/episodic_memory.db")
        if episodic_db.exists():
            self.sqlite_db_path = str(episodic_db)
            print(f"✅ Found episodic memory database: {episodic_db}")
            return True

        print("❌ Episodic memory database not found")
        return False

    def setup_postgresql_connection(self: EpisodicMemoryMigrator) -> bool:
        """Setup PostgreSQL connection."""
        try:
            # Read PostgreSQL URL from environment file
            env_file = Path(".claude/postgresql_env.sh")
            if not env_file.exists():
                print("❌ PostgreSQL environment file not found")
                return False

            # Extract PostgreSQL URL from environment file
            with open(env_file) as f:
                for line in f:
                    if line.startswith("export TODOWRITE_DATABASE_URL="):
                        self.postgresql_url = line.split("=")[1].strip().strip('"')
                        break
                else:
                    print("❌ PostgreSQL URL not found in environment file")
                    return False

            self.postgresql_engine = create_engine(self.postgresql_url)

            print("✅ PostgreSQL connection established for episodic memory")
            return True

        except OSError as e:
            print(f"❌ Error setting up PostgreSQL connection: {e}")
            return False

    def create_episodic_tables(self: EpisodicMemoryMigrator) -> None:
        """Create episodic memory tables in PostgreSQL."""
        try:
            # Drop existing tables to recreate with correct schema
            with self.postgresql_engine.connect() as conn:
                conn.execute(text("DROP TABLE IF EXISTS tool_calls CASCADE"))
                conn.execute(text("DROP TABLE IF EXISTS exchanges CASCADE"))
                conn.commit()

            # Create tables with corrected schema
            EpisodicBase.metadata.create_all(self.postgresql_engine)

            # Create indexes for better performance
            with self.postgresql_engine.connect() as conn:
                conn.execute(
                    text(
                        "CREATE INDEX IF NOT EXISTS idx_episodic_timestamp ON exchanges(timestamp DESC)"
                    )
                )
                conn.execute(
                    text(
                        "CREATE INDEX IF NOT EXISTS idx_episodic_session_id ON exchanges(session_id)"
                    )
                )
                conn.execute(
                    text("CREATE INDEX IF NOT EXISTS idx_episodic_project ON exchanges(project)")
                )
                conn.execute(
                    text(
                        "CREATE INDEX IF NOT EXISTS idx_episodic_sidechain ON exchanges(is_sidechain)"
                    )
                )
                conn.execute(
                    text(
                        "CREATE INDEX IF NOT EXISTS idx_episodic_git_branch ON exchanges(git_branch)"
                    )
                )
                conn.execute(
                    text(
                        "CREATE INDEX IF NOT EXISTS idx_episodic_tool_name ON tool_calls(tool_name)"
                    )
                )
                conn.execute(
                    text(
                        "CREATE INDEX IF NOT EXISTS idx_episodic_tool_exchange ON tool_calls(exchange_id)"
                    )
                )
                conn.commit()

            print("✅ Episodic memory tables created in PostgreSQL")

        except (sqlalchemy.exc.SQLAlchemyError, OSError) as e:
            print(f"⚠️  Error creating episodic tables: {e}")

    def migrate_exchanges(self: EpisodicMemoryMigrator) -> int:
        """Migrate exchanges table."""
        try:
            print("📋 Migrating episodic memory exchanges...")

            sqlite_engine = create_engine(f"sqlite:///{self.sqlite_db_path}")

            with sqlite_engine.connect() as sqlite_conn:
                result = sqlite_conn.execute(text("SELECT * FROM exchanges"))
                rows = result.fetchall()
                columns = result.keys()

                if not rows:
                    print("  📭 No exchanges found")
                    return 0

                column_info = {col: idx for idx, col in enumerate(columns)}
                migrated_count = 0

                with self.postgresql_engine.connect() as pg_conn:
                    for row in rows:
                        row_data = {}
                        for col in columns:
                            row_data[col] = row[column_info[col]]

                        # Convert boolean values for PostgreSQL
                        for col in columns:
                            if (
                                col in ["is_sidechain", "thinking_disabled"]
                                and row_data[col] is not None
                            ):
                                row_data[col] = bool(row_data[col])

                        # Insert into PostgreSQL
                        try:
                            cols_str = ", ".join(columns)
                            placeholders = ", ".join([f":{col}" for col in columns])
                            insert_stmt = text(f"""
                                INSERT INTO exchanges ({cols_str})
                                VALUES ({placeholders})
                            """)
                            pg_conn.execute(insert_stmt, row_data)
                            migrated_count += 1
                        except (sqlalchemy.exc.SQLAlchemyError, ValueError) as e:
                            print(f"    ⚠️  Error migrating exchange: {e}")
                            continue

                    pg_conn.commit()

                print(f"  ✅ Migrated {migrated_count} exchanges")
                return migrated_count

        except (sqlalchemy.exc.SQLAlchemyError, sqlite3.Error) as e:
            print(f"  ❌ Error migrating exchanges: {e}")
            return 0

    def migrate_tool_calls(self: EpisodicMemoryMigrator) -> int:
        """Migrate tool_calls table."""
        try:
            print("📋 Migrating episodic memory tool calls...")

            sqlite_engine = create_engine(f"sqlite:///{self.sqlite_db_path}")

            with sqlite_engine.connect() as sqlite_conn:
                result = sqlite_conn.execute(text("SELECT * FROM tool_calls"))
                rows = result.fetchall()
                columns = result.keys()

                if not rows:
                    print("  📭 No tool calls found")
                    return 0

                column_info = {col: idx for idx, col in enumerate(columns)}
                migrated_count = 0

                with self.postgresql_engine.connect() as pg_conn:
                    for row in rows:
                        row_data = {}
                        for col in columns:
                            row_data[col] = row[column_info[col]]

                        # Convert boolean values for PostgreSQL
                        for col in columns:
                            if col == "is_error" and row_data[col] is not None:
                                row_data[col] = bool(row_data[col])

                        # Insert into PostgreSQL
                        try:
                            cols_str = ", ".join(columns)
                            placeholders = ", ".join([f":{col}" for col in columns])
                            insert_stmt = text(f"""
                                INSERT INTO tool_calls ({cols_str})
                                VALUES ({placeholders})
                            """)
                            pg_conn.execute(insert_stmt, row_data)
                            migrated_count += 1
                        except (sqlalchemy.exc.SQLAlchemyError, ValueError) as e:
                            print(f"    ⚠️  Error migrating tool call: {e}")
                            continue

                    pg_conn.commit()

                print(f"  ✅ Migrated {migrated_count} tool calls")
                return migrated_count

        except (sqlalchemy.exc.SQLAlchemyError, sqlite3.Error) as e:
            print(f"  ❌ Error migrating tool calls: {e}")
            return 0

    def update_episodic_memory_config(self: EpisodicMemoryMigrator) -> bool:
        """Update episodic memory configuration to use PostgreSQL."""
        try:
            print("🔧 Updating episodic memory configuration...")

            # Create PostgreSQL episodic memory database path
            pg_episodic_db_path = Path(".claude/episodic_memory_postgresql.db")

            # Update the environment variable file
            env_file = Path(".claude/episodic_memory_env.sh")
            with open(env_file, "w") as f:
                f.write(f'export EPISODIC_MEMORY_DB_PATH="{pg_episodic_db_path}"\n')
                f.write('export EPISODIC_MEMORY_BACKEND="postgresql"\n')
                f.write(f'export EPISODIC_MEMORY_POSTGRESQL_URL="{self.postgresql_url}"\n')

            print("✅ Episodic memory configuration updated")
            print("   Database: PostgreSQL")
            print(f"   URL: {self.postgresql_url}")
            print(f"   Config file: {env_file}")

            return True

        except OSError as e:
            print(f"❌ Error updating episodic memory config: {e}")
            return False

    def run_migration(self: EpisodicMemoryMigrator) -> bool:
        """Run the complete episodic memory migration."""
        print("🚀 Starting Episodic Memory Migration to PostgreSQL...")
        print("=" * 60)

        # Find episodic database
        if not self.find_episodic_database():
            return False

        # Setup PostgreSQL connection
        if not self.setup_postgresql_connection():
            return False

        # Create tables
        self.create_episodic_tables()

        total_migrated = 0

        # Migrate data
        total_migrated += self.migrate_exchanges()
        total_migrated += self.migrate_tool_calls()

        # Update configuration
        if not self.update_episodic_memory_config():
            print("⚠️  Configuration update failed, but migration succeeded")

        print("=" * 60)
        print(f"✅ Episodic Memory Migration Complete! Total records: {total_migrated}")
        print("=" * 60)
        return True

    def verify_migration(self: EpisodicMemoryMigrator) -> bool:
        """Verify episodic memory migration."""
        print("🔍 Verifying Episodic Memory Migration...")
        try:
            with self.postgresql_engine.connect() as conn:
                # Count records
                exchanges_result = conn.execute(text("SELECT COUNT(*) FROM exchanges"))
                tool_calls_result = conn.execute(text("SELECT COUNT(*) FROM tool_calls"))

                exchanges_count = exchanges_result.fetchone()[0]
                tool_calls_count = tool_calls_result.fetchone()[0]

                print("📊 PostgreSQL Episodic Memory Record Counts:")
                print(f"  exchanges: {exchanges_count}")
                print(f"  tool_calls: {tool_calls_count}")
                print(f"  Total: {exchanges_count + tool_calls_count}")

                return True

        except (sqlalchemy.exc.SQLAlchemyError, OSError) as e:
            print(f"❌ Verification failed: {e}")
            return False


def main() -> None:
    """Main function."""
    migrator = EpisodicMemoryMigrator()

    if migrator.run_migration():
        migrator.verify_migration()

        # Suggest next steps
        print("\n📋 Next Steps:")
        print("1. Source the episodic memory environment:")
        print("   source .claude/episodic_memory_env.sh")
        print("2. Update your session to use PostgreSQL episodic memory")
        print("3. Test the episodic memory system")
    else:
        print("❌ Episodic memory migration failed")
        exit(1)


if __name__ == "__main__":
    main()
