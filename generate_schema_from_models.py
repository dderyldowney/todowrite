#!/usr/bin/env python3
"""Generate PostgreSQL schema from updated SQLAlchemy models.

This script creates a schema file based on the actual models,
ensuring the models are the single source of truth.
"""

from __future__ import annotations

import os
import sys

# Add lib_package to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "lib_package", "src"))

from sqlalchemy import create_engine
from sqlalchemy.schema import CreateIndex, CreateTable
from todowrite.core.models import Base


def generate_schema():
    """Generate PostgreSQL schema from updated models."""
    # Create a PostgreSQL engine
    engine = create_engine("postgresql://")

    print("-- ToDoWrite Database Schema - Generated from Models")
    print("-- This is the single source of truth for database schema")
    print(
        "-- Field names follow standard ORM conventions: created_at, updated_at, started_on, ended_on"
    )
    print("-- All IDs are INTEGER with proper constraints")
    print("-- All timestamps use TIMESTAMP WITH TIME ZONE for UTC storage")
    print("-- Association tables use standard practice without timestamps")
    print()

    # Generate table creation statements
    tables = sorted(
        Base.metadata.tables.keys(),
        key=lambda x: (
            # Sort core tables first, then association tables
            (0 if "_" not in x else 1, x)
        ),
    )

    for table_name in tables:
        table = Base.metadata.tables[table_name]

        # Skip association tables (those with underscores in name) for now
        if "_" in table_name:
            continue

        print(f"-- {table_name.title().replace('_', ' ')}")
        sql = str(CreateTable(table).compile(engine)).replace(
            "CREATE TABLE", "CREATE TABLE IF NOT EXISTS"
        )
        print(sql)
        print()

    # Generate association tables
    print("-- Association Tables")
    for table_name in tables:
        if "_" in table_name:
            table = Base.metadata.tables[table_name]
            sql = str(CreateTable(table).compile(engine)).replace(
                "CREATE TABLE", "CREATE TABLE IF NOT EXISTS"
            )
            print(sql)
            print()

    # Generate indexes
    print("-- Indexes for Performance")
    for table_name in tables:
        table = Base.metadata.tables[table_name]
        for index in table.indexes:
            print(CreateIndex(index).compile(engine))
    print()

    # Generate triggers for updated_at timestamps
    print("-- Triggers for Automatic updated_at")
    print("""
-- Create trigger function to automatically update updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Apply triggers to all tables with updated_at
""")

    for table_name in tables:
        if "_" not in table_name:  # Only for main tables, not association tables
            table = Base.metadata.tables[table_name]
            if "updated_at" in [col.name for col in table.columns]:
                print(
                    f"CREATE TRIGGER update_{table_name}_updated_at BEFORE UPDATE ON {table_name} FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();"
                )


if __name__ == "__main__":
    generate_schema()
