"""
Database Sequence Management System.

This module provides comprehensive sequence management for PostgreSQL and SQLite3
databases to prevent duplicate key constraint violations and ensure proper ID sequencing.

Features:
- Automatic sequence validation and correction
- Real-time sequence synchronization
- Prevention of duplicate key constraint errors
- Support for all ToDoWrite model tables
- Multi-database support (PostgreSQL sequences + SQLite3 AUTOINCREMENT)
"""

from __future__ import annotations

import os

from sqlalchemy import create_engine, text


class SequenceManager:
    """Manages PostgreSQL sequences to prevent ID conflicts."""

    def __init__(self, database_url: str | None = None):
        """Initialize the sequence manager."""
        self.database_url = database_url or os.getenv("TODOWRITE_DATABASE_URL")
        if not self.database_url:
            raise ValueError("Database URL is required")

        self.engine = create_engine(self.database_url)

        # Detect database type
        self.db_type = self._detect_database_type()

        # Define tables with auto-incrementing IDs
        self.managed_tables = [
            "goals",
            "concepts",
            "contexts",
            "constraints",
            "requirements",
            "acceptance_criteria",
            "interface_contracts",
            "phases",
            "steps",
            "tasks",
            "sub_tasks",
            "commands",
            "labels",
            "development_sessions",
            "agent_registry",
            "claude_sessions",
        ]

    def _detect_database_type(self) -> str:
        """Detect if we're using PostgreSQL or SQLite3."""
        url = self.database_url.lower()
        if url.startswith("postgresql://") or url.startswith("postgres://"):
            return "postgresql"
        elif url.startswith("sqlite://") or url.endswith(".db") or url.endswith(".sqlite"):
            return "sqlite3"
        else:
            # Default to PostgreSQL for safety
            return "postgresql"

    def validate_all_sequences(self) -> dict[str, dict[str, int]]:
        """Validate all managed table sequences."""
        results = {}

        with self.engine.connect() as conn:
            for table in self.managed_tables:
                try:
                    result = conn.execute(
                        text(f"SELECT id FROM {table} ORDER BY id")
                    )
                    records = result.fetchall()

                    if records:
                        max_id = max(record[0] for record in records)

                        if self.db_type == "postgresql":
                            # PostgreSQL: Check sequence
                            seq_result = conn.execute(
                                text(f"SELECT last_value FROM {table}_id_seq")
                            )
                            seq_value = seq_result.fetchone()[0]
                            needs_fix = seq_value <= max_id
                        else:
                            # SQLite3: Check sqlite_sequence table
                            try:
                                seq_result = conn.execute(
                                    text(f"SELECT seq FROM sqlite_sequence WHERE name = '{table}'")
                                )
                                seq_row = seq_result.fetchone()
                                seq_value = seq_row[0] if seq_row else 0
                                needs_fix = seq_value <= max_id
                            except Exception:
                                # Table might not exist in sqlite_sequence yet
                                seq_value = 0
                                needs_fix = True

                        results[table] = {
                            "max_id": max_id,
                            "current_sequence": seq_value,
                            "needs_fix": needs_fix,
                        }
                    else:
                        results[table] = {
                            "max_id": 0,
                            "current_sequence": 1,
                            "needs_fix": False,
                        }

                except Exception as e:
                    results[table] = {"error": str(e), "needs_fix": False}

        return results

    def fix_all_sequences(self, force: bool = False) -> dict[str, bool]:
        """Fix all sequences that need correction."""
        validation = self.validate_all_sequences()
        fixed_results = {}

        with self.engine.connect() as conn:
            for table, info in validation.items():
                if "error" in info:
                    fixed_results[table] = False
                    continue

                if info["needs_fix"] or force:
                    try:
                        new_seq_value = info["max_id"] + 1
                        if self.db_type == "postgresql":
                            # PostgreSQL: Reset sequence
                            conn.execute(
                                text(
                                    f"ALTER SEQUENCE {table}_id_seq RESTART WITH {new_seq_value}"
                                )
                            )
                        else:
                            # SQLite3: Update sqlite_sequence table
                            conn.execute(
                                text(f"UPDATE sqlite_sequence SET seq = {new_seq_value} WHERE name = '{table}'")
                            )
                            # If no entry exists, insert one
                            conn.execute(
                                text(f"INSERT OR IGNORE INTO sqlite_sequence (name, seq) VALUES ('{table}', {new_seq_value})")
                            )

                        conn.commit()
                        fixed_results[table] = True
                    except Exception as e:
                        print(f"Error fixing sequence for {table}: {e}")
                        fixed_results[table] = False
                else:
                    fixed_results[table] = True  # No fix needed

        return fixed_results

    def ensure_sequence_before_insert(self, table_name: str) -> None:
        """Ensure sequence is correct before inserting into a table."""
        if table_name not in self.managed_tables:
            return

        with self.engine.connect() as conn:
            try:
                # Get current max ID
                result = conn.execute(
                    text(f"SELECT COALESCE(MAX(id), 0) FROM {table_name}")
                )
                max_id = result.fetchone()[0]

                # Get current sequence
                result = conn.execute(
                    text(f"SELECT last_value FROM {table_name}_id_seq")
                )
                seq_value = result.fetchone()[0]

                # Fix sequence if needed
                if seq_value <= max_id:
                    new_seq_value = max_id + 1
                    conn.execute(
                        text(
                            f"ALTER SEQUENCE {table_name}_id_seq RESTART WITH {new_seq_value}"
                        )
                    )
                    conn.commit()

            except Exception as e:
                print(f"Error ensuring sequence for {table_name}: {e}")

    def get_table_status(self, table_name: str) -> dict[str, int]:
        """Get status for a specific table."""
        if table_name not in self.managed_tables:
            return {"error": f"Table {table_name} is not managed"}

        with self.engine.connect() as conn:
            try:
                # Get record count and max ID
                result = conn.execute(
                    text(
                        f"SELECT COUNT(*), COALESCE(MAX(id), 0) FROM {table_name}"
                    )
                )
                count, max_id = result.fetchone()

                # Get sequence value
                if self.db_type == "postgresql":
                    result = conn.execute(
                        text(f"SELECT last_value FROM {table_name}_id_seq")
                    )
                    seq_value = result.fetchone()[0]
                else:
                    # SQLite3: Check sqlite_sequence table
                    try:
                        result = conn.execute(
                            text(f"SELECT seq FROM sqlite_sequence WHERE name = '{table_name}'")
                        )
                        seq_row = result.fetchone()
                        seq_value = seq_row[0] if seq_row else 0
                    except Exception:
                        seq_value = 0

                return {
                    "table": table_name,
                    "record_count": count,
                    "max_id": max_id,
                    "current_sequence": seq_value,
                    "needs_fix": seq_value <= max_id,
                }

            except Exception as e:
                return {"error": str(e)}

    def report_status(self) -> str:
        """Generate a comprehensive status report."""
        validation = self.validate_all_sequences()

        report_lines = [f"Database Sequence Status Report ({self.db_type.upper()})", "=" * 50]

        needs_fix_count = 0
        for table, info in validation.items():
            if "error" in info:
                report_lines.append(f"❌ {table}: ERROR - {info['error']}")
            elif info["needs_fix"]:
                report_lines.append(
                    f"⚠️  {table}: max_id={info['max_id']}, seq={info['current_sequence']} "
                    f"(NEEDS FIX)"
                )
                needs_fix_count += 1
            else:
                report_lines.append(
                    f"✅ {table}: max_id={info['max_id']}, seq={info['current_sequence']}"
                )

        report_lines.append("")
        if needs_fix_count > 0:
            report_lines.append(
                f"🚨 {needs_fix_count} tables need sequence fixes!"
            )
            report_lines.append("Run fix_all_sequences() to correct.")
        else:
            report_lines.append("✅ All sequences are correct!")

        return "\n".join(report_lines)


def ensure_sequences_before_init():
    """Ensure all sequences are correct before database initialization."""
    try:
        manager = SequenceManager()
        print("🔧 Validating database sequences before initialization...")

        validation = manager.validate_all_sequences()
        needs_fix = any(
            info.get("needs_fix", False) for info in validation.values()
        )

        if needs_fix:
            print("⚠️  Sequence issues detected, fixing automatically...")
            fixed = manager.fix_all_sequences()
            fixed_count = sum(fixed.values())
            print(f"✅ Fixed {fixed_count} table sequences")
        else:
            print("✅ All sequences are correct")

        return True

    except Exception as e:
        print(f"❌ Error ensuring sequences: {e}")
        return False


if __name__ == "__main__":
    # Run standalone sequence validation and fix
    manager = SequenceManager()

    print("🔍 Checking database sequences...")
    print(manager.report_status())

    print("\n🔧 Fixing sequences if needed...")
    results = manager.fix_all_sequences()

    fixed_count = sum(results.values())
    total_count = len(results)

    print(
        f"Results: {fixed_count}/{total_count} tables processed successfully"
    )

    if fixed_count < total_count:
        print("⚠️  Some tables had issues. Check the detailed report above.")
    else:
        print("✅ All sequences validated and fixed!")
