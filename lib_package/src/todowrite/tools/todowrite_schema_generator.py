#!/usr/bin/env python3
"""
ToDoWrite Model Schema Generator

Automatically generates JSON schemas and SQL DDL from SQLAlchemy models
to ensure perfect synchronization between models and schemas.
"""

import json
import sys
from datetime import datetime
from pathlib import Path
from typing import Any

# Add lib_package/src to Python path for imports
project_root = Path(__file__).resolve().parent.parent.parent.parent
lib_src = project_root / "lib_package" / "src"
sys.path.insert(0, str(lib_src))

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
    acceptance_criteria_labels,
    concepts_contexts,
    concepts_labels,
    constraints_labels,
    constraints_requirements,
    contexts_labels,
    # Association tables
    goals_concepts,
    goals_contexts,
    goals_labels,
    interface_contracts_labels,
    interface_contracts_phases,
    phases_labels,
    phases_steps,
    requirements_acceptance_criteria,
    requirements_concepts,
    requirements_contexts,
    requirements_labels,
    steps_labels,
    steps_tasks,
    sub_tasks_labels,
    tasks_labels,
    tasks_sub_tasks,
)


class ToDoWriteSchemaGenerator:
    """Generates JSON schemas and database-agnostic SQL DDL from SQLAlchemy models."""

    def __init__(
        self: "ToDoWriteSchemaGenerator", dialect: str = "postgresql"
    ) -> None:
        self.project_root = project_root
        self.timestamp = datetime.now().isoformat()
        self.dialect = dialect  # "postgresql" or "sqlite"

    def generate_json_schema(
        self: "ToDoWriteSchemaGenerator",
    ) -> dict[str, Any]:
        """Generate JSON schema for ToDoWrite Models."""

        schema = {
            "$schema": "https://json-schema.org/draft/2020-12/schema",
            "title": "ToDoWrite Models",
            "description": "JSON schema for ToDoWrite hierarchical task management system with integer primary keys",
            "type": "object",
            "generated_at": self.timestamp,
            "models": {},
        }

        # Define model order for consistency
        model_classes = [
            Goal,
            Concept,
            Context,
            Constraints,
            Requirements,
            AcceptanceCriteria,
            InterfaceContract,
            Phase,
            Step,
            Task,
            SubTask,
            Command,
            Label,
        ]

        for model_class in model_classes:
            model_name = model_class.__name__
            table_name = model_class.__tablename__

            # Get model fields from SQLAlchemy columns
            model_schema = self._extract_model_schema(model_class)

            schema["models"][model_name] = {
                "description": f"Schema for individual {model_name} model instances",
                "table_name": table_name,
                "table_description": f"Table containing a collection of {model_name.lower()} model instances",
                "primary_key": {
                    "field": "id",
                    "type": "integer",
                    "description": f"Unique identifier for this {model_name.lower()} instance",
                },
                "fields": model_schema["fields"],
                "relationships": model_schema["relationships"],
                "required_fields": model_schema["required_fields"],
                "model_instance": f"Represents one {model_name.lower()} with specific attributes and relationships",
                "table_purpose": f"Stores multiple {model_name.lower()} instances as rows in the database",
            }

        # Add association tables
        schema["association_tables"] = self._get_association_table_schemas()

        return schema

    def _extract_model_schema(
        self: "ToDoWriteSchemaGenerator", model_class: Any
    ) -> dict[str, Any]:
        """Extract schema information from a SQLAlchemy model."""

        fields = {}
        relationships = {}
        required_fields = []

        # Get SQLAlchemy columns
        for column in model_class.__table__.columns:
            field_name = column.name
            field_type = str(column.type)
            nullable = column.nullable
            primary_key = column.primary_key

            # Skip automatic fields
            if field_name in ["id", "created_at", "updated_at"]:
                continue

            # Determine JSON schema type
            json_type = self._sqlalchemy_to_json_type(field_type)

            field_info = {
                "type": json_type,
                "nullable": nullable,
                "sqlalchemy_type": field_type,
            }

            # Add enum values if applicable - get from the SQLAlchemy column directly
            for sqlalchemy_col in model_class.__table__.columns:
                if sqlalchemy_col.name == field_name:
                    column_type = sqlalchemy_col.type
                    if hasattr(column_type, "enums"):
                        field_info["enum"] = list(column_type.enums)
                        field_info["enum_description"] = (
                            f"Allowed values for {field_name}"
                        )
                    break

            fields[field_name] = field_info

            if not nullable and not primary_key:
                required_fields.append(field_name)

        # Get relationships
        for relationship_name in model_class.__mapper__.relationships:
            rel = model_class.__mapper__.relationships[relationship_name]
            relationships[relationship_name] = {
                "target_model": rel.entity.class_.__name__,
                "type": "many-to-many"
                if rel.secondary
                else "one-to-many"
                if rel.uselist
                else "many-to-one",
                "back_populates": getattr(rel, "back_populates", None),
            }

        return {
            "fields": fields,
            "relationships": relationships,
            "required_fields": required_fields,
        }

    def _get_association_table_schemas(
        self: "ToDoWriteSchemaGenerator",
    ) -> dict[str, Any]:
        """Get schemas for all association tables."""

        association_tables = [
            goals_concepts,
            goals_contexts,
            concepts_contexts,
            constraints_requirements,
            requirements_acceptance_criteria,
            requirements_concepts,
            requirements_contexts,
            interface_contracts_phases,
            interface_contracts_labels,
            phases_steps,
            steps_tasks,
            tasks_sub_tasks,
            sub_tasks_labels,
            goals_labels,
            concepts_labels,
            contexts_labels,
            constraints_labels,
            requirements_labels,
            acceptance_criteria_labels,
            phases_labels,
            steps_labels,
            tasks_labels,
        ]

        schemas = {}
        for table in association_tables:
            schemas[table.name] = {
                "columns": [
                    {
                        "name": col.name,
                        "type": str(col.type),
                        "foreign_key": col.foreign_keys[0].target_fullname
                        if col.foreign_keys
                        else None,
                    }
                    for col in table.columns
                ]
            }

        return schemas

    def _sqlalchemy_to_json_type(
        self: "ToDoWriteSchemaGenerator", sqlalchemy_type: str
    ) -> str:
        """Convert SQLAlchemy type to JSON schema type."""

        type_mapping = {
            "VARCHAR": "string",
            "TEXT": "string",
            "INTEGER": "integer",
            "BOOLEAN": "boolean",
            "DATETIME": "string",
            "DATE": "string",
            "FLOAT": "number",
            "NUMERIC": "number",
        }

        # Handle SQLAlchemy type variations
        for sql_type, json_type in type_mapping.items():
            if sql_type in sqlalchemy_type.upper():
                return json_type

        return "string"  # Default fallback

    def generate_sql_schema(self: "ToDoWriteSchemaGenerator") -> str:
        """Generate database-agnostic SQL DDL for ToDoWrite Models."""

        db_config = self._get_database_config()

        sql_statements = [
            "-- ToDoWrite Models Schema",
            f"-- Database Dialect: {db_config['name']}",
            f"-- Generated on: {self.timestamp}",
            "-- Total tables: 33 (12 model tables + 21 association tables)",
            "-- Compatible with: SQLite3, PostgreSQL, and any SQLAlchemy-compatible database",
            "",
        ]

        # Get all table metadata from SQLAlchemy
        metadata = Base.metadata

        # Sort tables for consistent output
        tables = sorted(metadata.tables.values(), key=lambda t: t.name)

        for table in tables:
            # Skip nodes table (old Node-based system)
            if table.name == "nodes":
                continue

            sql_statements.append(f"CREATE TABLE {table.name} (")

            column_definitions = []
            primary_key_columns = []

            for column in table.columns:
                col_def = f"    {column.name} {self._get_column_type(column)}"

                if column.primary_key:
                    primary_key_columns.append(column.name)
                    if (
                        db_config["autoincrement_suffix"]
                        and column.autoincrement
                    ):
                        col_def += db_config["autoincrement_suffix"]
                    elif not column.nullable:
                        col_def += " NOT NULL"
                elif not column.nullable:
                    col_def += " NOT NULL"

                # Add unique constraints
                if column.unique and not column.primary_key:
                    col_def += " UNIQUE"

                column_definitions.append(col_def)

            # Add primary key constraint if composite
            if len(primary_key_columns) > 1:
                pk_def = f"    PRIMARY KEY ({', '.join(primary_key_columns)})"
                column_definitions.append(pk_def)

            sql_statements.append(",\n".join(column_definitions))
            sql_statements.append(");")

            # Add table-level constraints separately for clarity
            foreign_key_constraints = []
            for column in table.columns:
                if column.foreign_keys:
                    for fk in column.foreign_keys:
                        if hasattr(fk, "column") and fk.column:
                            target_table = fk.column.table.name
                            target_col = fk.column.name
                            fk_def = f"ALTER TABLE {table.name} ADD CONSTRAINT fk_{table.name}_{column.name} FOREIGN KEY ({column.name}) REFERENCES {target_table}({target_col}) {db_config['referentialAction']};"
                            foreign_key_constraints.append(fk_def)

            if foreign_key_constraints:
                sql_statements.append("")
                sql_statements.append("-- Foreign Key Constraints")
                sql_statements.extend(foreign_key_constraints)

            sql_statements.append("")

        # Add indexes for performance
        sql_statements.extend(
            [
                "-- Performance indexes",
                "-- Add indexes for frequently queried columns",
            ]
        )

        indexes = [
            ("goals", "status"),
            ("tasks", "status"),
            ("requirements", "severity"),
            ("concepts", "owner"),
            ("contexts", "owner"),
            ("phases", "status"),
            ("steps", "status"),
        ]

        for table, column in indexes:
            index_name = f"idx_{table}_{column}"
            create_index = f"CREATE INDEX {index_name} ON {table}({column});"
            sql_statements.append(create_index)

        # Indexes for association tables
        sql_statements.extend(
            ["", "-- Indexes for association tables (foreign key columns)"]
        )

        association_tables = [
            "goals_concepts",
            "goals_contexts",
            "concepts_contexts",
            "requirements_concepts",
            "requirements_contexts",
            "constraints_requirements",
            "requirements_acceptance_criteria",
        ]

        for assoc_table in association_tables:
            if metadata.tables.get(assoc_table):
                table = metadata.tables[assoc_table]
                for column in table.columns:
                    if column.foreign_keys:  # This is a foreign key column
                        index_name = f"idx_{assoc_table}_{column.name}"
                        create_index = f"CREATE INDEX {index_name} ON {assoc_table}({column.name});"
                        sql_statements.append(create_index)

        sql_statements.extend(["", "-- Schema generation complete", ""])

        return "\n".join(sql_statements)

    def _get_database_config(
        self: "ToDoWriteSchemaGenerator",
    ) -> dict[str, str]:
        """Get database-specific configuration."""

        configs = {
            "sqlite": {
                "name": "SQLite3",
                "autoincrement_suffix": " PRIMARY KEY AUTOINCREMENT",
                "referentialAction": "ON DELETE CASCADE",
            },
            "postgresql": {
                "name": "PostgreSQL",
                "autoincrement_suffix": " GENERATED ALWAYS AS IDENTITY PRIMARY KEY",
                "referentialAction": "ON DELETE CASCADE",
            },
            "mysql": {
                "name": "MySQL",
                "autoincrement_suffix": " AUTO_INCREMENT PRIMARY KEY",
                "referentialAction": "ON DELETE CASCADE",
            },
        }

        return configs.get(self.dialect.lower(), configs["postgresql"])

    def _get_column_type(self: "ToDoWriteSchemaGenerator", column: Any) -> str:
        """Get database-appropriate column type."""

        base_type = str(column.type)

        # Database-specific type mappings
        if self.dialect.lower() == "sqlite":
            # SQLite type simplifications
            if "VARCHAR" in base_type:
                return "VARCHAR"
            elif "TEXT" in base_type:
                return "TEXT"
            elif "INTEGER" in base_type:
                return "INTEGER"
            elif "BOOLEAN" in base_type:
                return "BOOLEAN"
            elif "DATETIME" in base_type:
                return "DATETIME"

        elif self.dialect.lower() == "postgresql":
            # PostgreSQL-specific types
            if "VARCHAR" in base_type:
                # Extract length if specified
                if "(" in base_type:
                    return base_type
                else:
                    return "VARCHAR(255)"
            elif "TEXT" in base_type:
                return "TEXT"
            elif "INTEGER" in base_type:
                return "INTEGER"
            elif "BOOLEAN" in base_type:
                return "BOOLEAN"
            elif "DATETIME" in base_type:
                return "TIMESTAMP"

        # Default: return SQLAlchemy type as-is
        return base_type

    def write_json_schema(
        self: "ToDoWriteSchemaGenerator",
        schema: dict[str, Any],
        output_path: Path,
    ) -> None:
        """Write JSON schema to file."""

        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, "w") as f:
            json.dump(schema, f, indent=2, default=str)
        print(f"✅ JSON schema written to: {output_path}")

    def write_sql_schema(
        self: "ToDoWriteSchemaGenerator", sql: str, output_path: Path
    ) -> None:
        """Write SQL schema to file."""

        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, "w") as f:
            f.write(sql)
        print(f"✅ SQL schema written to: {output_path}")

    def generate_all_schemas(self: "ToDoWriteSchemaGenerator") -> None:
        """Generate JSON schema and SQL schemas for all supported databases."""

        print(
            "🏗️  Generating ToDoWrite Model Schemas from SQLAlchemy Models..."
        )
        print("=" * 60)

        # Generate JSON schema (database-agnostic)
        print("📝 Generating JSON schema...")
        json_schema = self.generate_json_schema()
        json_output_path = (
            self.project_root
            / "lib_package"
            / "src"
            / "todowrite"
            / "core"
            / "schemas"
            / "rails_activerecord.schema.json"
        )
        self.write_json_schema(json_schema, json_output_path)

        # Generate SQL schemas for each supported database
        supported_databases = ["sqlite", "postgresql"]

        for dialect in supported_databases:
            print(f"🗃️  Generating {dialect.upper()} schema...")
            self.dialect = dialect
            sql_schema = self.generate_sql_schema()

            # Create dialect-specific output file
            sql_filename = f"rails_activerecord_schema_{dialect}.sql"
            sql_output_path = self.project_root / "docs" / sql_filename
            self.write_sql_schema(sql_schema, sql_output_path)

        print("\n🎯 Schema Generation Complete!")
        print("=" * 60)
        print(f"📊 Generated schemas for {len(json_schema['models'])} models")
        print(
            f"🔗 Includes {len(json_schema['association_tables'])} association tables"
        )
        print(
            f"🗄️  Generated SQL for: {', '.join([db.upper() for db in supported_databases])}"
        )
        print("✅ Models and schemas are now synchronized")
        print("✅ Ready for multi-database ToDoWrite Models development")
        print(
            "✅ Compatible with SQLite3, PostgreSQL, and any SQLAlchemy-supported database"
        )


def main() -> int:
    """Main entry point."""
    try:
        generator = ToDoWriteSchemaGenerator()
        generator.generate_all_schemas()
        return 0
    except Exception as e:
        print(f"❌ Schema generation failed: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
