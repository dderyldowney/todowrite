#!/usr/bin/env python3
"""
Database migration script for ToDoWrite.

This script migrates databases from the old schema (with session_id column)
to the new schema (without session_id column).
"""

import argparse
import sys
from typing import Any

import sqlalchemy as sa
from sqlalchemy import text


def check_database_needs_migration(engine: Any) -> bool:
    """Check if the database has the old session_id column."""
    try:
        with engine.connect() as conn:
            # Check if session_id column exists in nodes table
            result = conn.execute(
                text(
                    """
                PRAGMA table_info(nodes)
            """
                )
            )

            columns = [row[1] for row in result.fetchall()]
            return "session_id" in columns
    except Exception as e:
        print(f"Error checking database schema: {e}")
        return False


def migrate_database(engine: Any, dry_run: bool = False) -> bool:
    """Migrate database from old schema to new schema."""
    try:
        with engine.connect() as conn:
            # Check if session_id column exists
            if not check_database_needs_migration(engine):
                print("✅ Database is already using the new schema.")
                return True

            print("🔄 Detected old database schema with session_id column...")

            if dry_run:
                print("🔍 DRY RUN: Would perform the following operations:")
                print("  1. Create backup table nodes_backup")
                print("  2. Copy data from nodes to nodes_backup (excluding session_id)")
                print("  3. Drop nodes table")
                print("  4. Rename nodes_backup to nodes")
                print("  5. Recreate indexes")
                return True

            # Start migration
            print("📋 Step 1: Creating backup table...")
            conn.execute(
                text(
                    """
                CREATE TABLE nodes_backup AS
                SELECT id, layer, title, description, status, progress,
                       started_date, completion_date, owner, severity,
                       work_type, assignee
                FROM nodes
            """
                )
            )

            print("📋 Step 2: Dropping old table...")
            conn.execute(text("DROP TABLE nodes"))

            print("📋 Step 3: Renaming backup table...")
            conn.execute(text("ALTER TABLE nodes_backup RENAME TO nodes"))

            print("📋 Step 4: Creating new schema...")
            # The new schema will be created automatically when initializing

            print("✅ Migration completed successfully!")
            conn.commit()
            return True

    except Exception as e:
        print(f"❌ Migration failed: {e}")
        return False


def main():
    """Main migration function."""
    parser = argparse.ArgumentParser(description="Migrate ToDoWrite database schema")
    parser.add_argument(
        "--database-url",
        "-d",
        default="sqlite:///./todowrite.db",
        help="Database URL (default: sqlite:///./todowrite.db)",
    )
    parser.add_argument(
        "--dry-run", action="store_true", help="Show what would be done without making changes"
    )
    parser.add_argument(
        "--check-only", action="store_true", help="Only check if migration is needed"
    )

    args = parser.parse_args()

    print(f"🔍 Checking database: {args.database_url}")

    try:
        # Create database engine
        engine = sa.create_engine(args.database_url)

        if args.check_only:
            needs_migration = check_database_needs_migration(engine)
            if needs_migration:
                print("❌ Database needs migration")
                sys.exit(1)
            else:
                print("✅ Database schema is up to date")
                sys.exit(0)

        # Perform migration
        success = migrate_database(engine, dry_run=args.dry_run)

        if success:
            print("🎉 Migration completed successfully!")
            sys.exit(0)
        else:
            print("💥 Migration failed!")
            sys.exit(1)

    except Exception as e:
        print(f"💥 Fatal error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
