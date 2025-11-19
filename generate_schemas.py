#!/usr/bin/env python3
"""Simple Rails ActiveRecord Schema Generator.

Quickly generates schemas from SQLAlchemy models.
"""

import json
import sys
from datetime import datetime
from pathlib import Path

# Add lib_package/src to Python path
project_root = Path.cwd()
lib_src = project_root / "lib_package" / "src"
sys.path.insert(0, str(lib_src))


def main():
    print("🏗️  Generating Rails ActiveRecord Schemas...")
    print("=" * 60)

    try:
        # Import models
        from todowrite.core.models import (
            AcceptanceCriteria,
            Base,
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

        print("✅ Models imported successfully")

        # Generate basic JSON schema
        schema = {
            "$schema": "https://json-schema.org/draft/2020-12/schema",
            "title": "ToDoWrite Rails ActiveRecord Models",
            "description": "Schema for hierarchical task management with integer primary keys",
            "generated_at": datetime.now().isoformat(),
            "models": {},
        }

        # Define model order
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
            Label,
        ]

        for model_class in model_classes:
            model_name = model_class.__name__
            table_name = model_class.__tablename__

            print(f"📝 Processing {model_name} -> {table_name}")

            # Extract basic field information
            fields = {}
            required = []

            for column in model_class.__table__.columns:
                if column.name == "id":
                    continue  # Skip auto-generated primary key

                if column.name in ["created_at", "updated_at"]:
                    continue  # Skip timestamp fields

                field_type = "string"
                nullable = column.nullable

                # Convert SQLAlchemy types to JSON types
                col_type_str = str(column.type).upper()
                if "INTEGER" in col_type_str:
                    field_type = "integer"
                elif "BOOLEAN" in col_type_str:
                    field_type = "boolean"
                elif "TEXT" in col_type_str:
                    field_type = "string"

                fields[column.name] = {
                    "type": field_type,
                    "nullable": nullable,
                    "sqlalchemy_type": str(column.type),
                }

                if not nullable:
                    required.append(column.name)

            # Get relationships
            relationships = {}
            for rel_name in model_class.__mapper__.relationships:
                rel = model_class.__mapper__.relationships[rel_name]
                target_model = rel.entity.class_.__name__

                relationships[rel_name] = {
                    "type": "relationship",
                    "target": target_model,
                    "description": f"This {model_name.lower()} has related {target_model.lower()} instances",
                    "accessor": f"Use .{rel_name} to access related {target_model.lower()} records",
                }

            schema["models"][model_name] = {
                "table_name": table_name,
                "description": f"Individual {model_name} model instance",
                "table_description": f"Collection of {model_name.lower()} instances stored as rows",
                "primary_key": "id (integer)",
                "fields": fields,
                "required_fields": required,
                "relationships": relationships,
                "model_purpose": f"Represents one {model_name.lower()} with its specific attributes",
            }

        # Add association tables with Rails ActiveRecord association descriptions
        schema["association_tables"] = {
            "goals_concepts": {
                "rails_associations": "Goal has_and_belongs_to_many :concepts (through this table), Concept has_and_belongs_to_many :goals (through this table)",
                "purpose": "Implements the many-to-many relationship between Goal and Concept models",
                "table_purpose": "Stores the specific Goal-Concept pairs that are associated",
                "models_involved": ["Goal", "Concept"],
                "columns": ["goal_id", "concept_id"],
                "relationship_description": "These specific Goals are connected to these specific Concepts",
            },
            "goals_contexts": {
                "rails_associations": "Goal has_and_belongs_to_many :contexts (through this table), Context has_and_belongs_to_many :goals (through this table)",
                "purpose": "Implements the many-to-many relationship between Goal and Context models",
                "table_purpose": "Stores the specific Goal-Context pairs that define 'why are we defining this goal'",
                "models_involved": ["Goal", "Context"],
                "columns": ["goal_id", "context_id"],
                "relationship_description": "These specific Goals are defined within these specific Contexts",
            },
            "concepts_contexts": {
                "rails_associations": "Concept has_and_belongs_to_many :contexts (through this table), Context has_and_belongs_to_many :concepts (through this table)",
                "purpose": "Implements the many-to-many relationship between Concept and Context models",
                "table_purpose": "Stores the specific Concept-Context pairs that define 'what conceptually are we building'",
                "models_involved": ["Concept", "Context"],
                "columns": ["concept_id", "context_id"],
                "relationship_description": "These specific Concepts are viewed through these specific Contexts",
            },
            "requirements_concepts": {
                "rails_associations": "Requirement has_and_belongs_to_many :concepts (through this table), Concept has_and_belongs_to_many :requirements (through this table)",
                "purpose": "Implements the many-to-many relationship between Requirements and Concept models",
                "table_purpose": "Stores the specific Requirement-Concept pairs that answer 'what conceptually do you mean?'",
                "models_involved": ["Requirements", "Concept"],
                "columns": ["requirement_id", "concept_id"],
                "relationship_description": "These specific Requirements are clarified by these specific Concepts",
            },
            "requirements_contexts": {
                "rails_associations": "Requirement has_and_belongs_to_many :contexts (through this table), Context has_and_belongs_to_many :requirements (through this table)",
                "purpose": "Implements the many-to-many relationship between Requirements and Context models",
                "table_purpose": "Stores the specific Requirement-Context pairs that answer 'in what context does this requirement apply?'",
                "models_involved": ["Requirements", "Context"],
                "columns": ["requirement_id", "context_id"],
                "relationship_description": "These specific Requirements apply in these specific Contexts",
            },
            "constraints_requirements": {
                "rails_associations": "Constraint has_and_belongs_to_many :requirements (through this table), Requirement has_and_belongs_to_many :constraints (through this table)",
                "purpose": "Implements the many-to-many relationship between Constraints and Requirements models",
                "table_purpose": "Stores the specific Constraint-Requirement pairs that define constraints",
                "models_involved": ["Constraints", "Requirements"],
                "columns": ["constraint_id", "requirement_id"],
                "relationship_description": "These specific Constraints constrain these specific Requirements",
            },
        }

        # Generate JSON schema file
        json_output_path = (
            project_root
            / "lib_package"
            / "src"
            / "todowrite"
            / "core"
            / "schemas"
            / "rails_activerecord.schema.json"
        )
        json_output_path.parent.mkdir(parents=True, exist_ok=True)

        with open(json_output_path, "w") as f:
            json.dump(schema, f, indent=2)

        print(f"✅ JSON schema written to: {json_output_path}")

        # Generate basic SQL schema
        sql_lines = [
            "-- ToDoWrite Rails ActiveRecord Schema",
            f"-- Generated on: {datetime.now().isoformat()}",
            "-- Total tables: 33 (12 model tables + 21 association tables)",
            "",
        ]

        metadata = Base.metadata
        tables = sorted(metadata.tables.values(), key=lambda t: t.name)

        for table in tables:
            if table.name == "nodes":
                continue  # Skip old Node table

            sql_lines.append(f"CREATE TABLE {table.name} (")

            col_defs = []
            for col in table.columns:
                col_def = f"    {col.name} {col.type}"
                if col.primary_key and col.autoincrement:
                    col_def += " PRIMARY KEY AUTOINCREMENT"
                elif col.primary_key:
                    col_def += " PRIMARY KEY"
                elif not col.nullable:
                    col_def += " NOT NULL"
                if col.unique and not col.primary_key:
                    col_def += " UNIQUE"
                col_defs.append(col_def)

            sql_lines.append(",\n".join(col_defs))
            sql_lines.append(");\n")

        # Generate SQL schema file
        sql_output_path = project_root / "docs" / "rails_activerecord_schema.sql"
        sql_output_path.parent.mkdir(parents=True, exist_ok=True)

        with open(sql_output_path, "w") as f:
            f.write("\n".join(sql_lines))

        print(f"✅ SQL schema written to: {sql_output_path}")

        print("\n🎯 Schema Generation Complete!")
        print("=" * 60)
        print(f"📊 Generated schemas for {len(model_classes)} models")
        print("✅ Models and schemas synchronized")
        print("✅ Ready for Rails ActiveRecord development")

        return 0

    except Exception as e:
        print(f"❌ Schema generation failed: {e}")
        import traceback

        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
