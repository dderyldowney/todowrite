"""ToDoWrite Model Schema Validator and Database Initializer.

This module provides programmatic access to the ToDoWrite model schemas,
allowing the library to validate data, initialize databases from schemas,
and ensure consistency between models and database structure.
"""

import json
from pathlib import Path
from typing import Any

from sqlalchemy import (
    Engine,
    create_engine,
    text,
)
from sqlalchemy.orm import sessionmaker

from .exceptions import ToDoWriteError
from .models import Base


class SchemaValidationError(ToDoWriteError):
    """Raised when schema validation fails."""

    pass


class DatabaseInitializationError(ToDoWriteError):
    """Raised when database initialization from schema fails."""

    pass


class ToDoWriteSchemaValidator:
    """
    ToDoWrite Model Schema Validator and Database Manager.

    Provides programmatic access to:
    1. Validate data against schemas
    2. Initialize databases from schema definitions
    3. Ensure model-schema consistency
    4. Import schemas into properly typed database tables
    """

    def __init__(self, schema_path: Path | None = None) -> None:
        """Initialize schema validator with schema file path."""
        if schema_path is None:
            # Default to the generated ToDoWrite Models schema
            schema_path = (
                Path(__file__).parent
                / "schemas"
                / "todowrite_models.schema.json"
            )

        self.schema_path = schema_path
        self.schema: dict[str, Any] = self._load_schema()

    def _load_schema(self) -> dict[str, Any]:
        """Load the ToDoWrite model schema from JSON file."""
        try:
            with open(self.schema_path) as f:
                return json.load(f)
        except FileNotFoundError:
            raise SchemaValidationError(
                f"Schema file not found: {self.schema_path}"
            )
        except json.JSONDecodeError as e:
            raise SchemaValidationError(f"Invalid JSON in schema file: {e}")

    def get_model_schema(self, model_name: str) -> dict[str, Any]:
        """Get the schema definition for a specific model."""
        if model_name not in self.schema.get("models", {}):
            available = list(self.schema.get("models", {}).keys())
            raise SchemaValidationError(
                f"Model '{model_name}' not found. Available models: {available}"
            )

        return self.schema["models"][model_name]

    def get_association_table_schema(self, table_name: str) -> dict[str, Any]:
        """Get the schema definition for an association table."""
        if table_name not in self.schema.get("association_tables", {}):
            available = list(self.schema.get("association_tables", {}).keys())
            raise SchemaValidationError(
                f"Association table '{table_name}' not found. Available: {available}"
            )

        return self.schema["association_tables"][table_name]

    def validate_model_data(
        self, model_name: str, data: dict[str, Any]
    ) -> bool:
        """Validate data against a specific model schema."""
        model_schema = self.get_model_schema(model_name)
        errors: list[str] = []

        # Check required fields
        required_fields = model_schema.get("required_fields", [])
        for field in required_fields:
            if field not in data:
                errors.append(f"Missing required field: {field}")

        # Check field types and constraints
        fields = model_schema.get("fields", {})
        for field_name, field_value in data.items():
            if field_name in fields:
                field_schema = fields[field_name]

                # Type validation
                expected_type = field_schema.get("type")
                if expected_type == "string" and not isinstance(
                    field_value, str
                ):
                    errors.append(
                        f"Field '{field_name}' should be string, got {type(field_value).__name__}"
                    )
                elif expected_type == "integer" and not isinstance(
                    field_value, int
                ):
                    errors.append(
                        f"Field '{field_name}' should be integer, got {type(field_value).__name__}"
                    )
                elif expected_type == "boolean" and not isinstance(
                    field_value, bool
                ):
                    errors.append(
                        f"Field '{field_name}' should be boolean, got {type(field_value).__name__}"
                    )

                # Nullable validation
                nullable = field_schema.get("nullable", True)
                if not nullable and field_value is None:
                    errors.append(f"Field '{field_name}' cannot be null")

        if errors:
            raise SchemaValidationError(
                f"Data validation failed for {model_name}: {errors}"
            )

        return True

    def initialize_database_from_schema(
        self, engine: Engine, drop_existing: bool = False
    ) -> None:
        """
        Initialize database with all tables defined in the schema.

        Args:
            engine: SQLAlchemy engine to use for database operations
            drop_existing: Whether to drop existing tables first
        """
        try:
            # Drop existing tables if requested
            if drop_existing:
                Base.metadata.drop_all(engine)

            # Create all tables from SQLAlchemy models
            Base.metadata.create_all(engine)

            # Verify all expected tables exist
            self._verify_database_structure(engine)

        except Exception as e:
            raise DatabaseInitializationError(
                f"Database initialization failed: {e}"
            )

    def _verify_database_structure(self, engine: Engine) -> None:
        """Verify that all expected tables and columns exist in the database."""
        with engine.connect() as conn:
            # Check model tables
            for _model_name, model_schema in self.schema.get(
                "models", {}
            ).items():
                table_name = model_schema["table_name"]

                # Check table exists
                result = conn.execute(
                    text(
                        "SELECT name FROM sqlite_master WHERE type='table' AND name=:table_name"
                    ),
                    {"table_name": table_name},
                )

                if not result.fetchone():
                    raise DatabaseInitializationError(
                        f"Table '{table_name}' not created"
                    )

                # Check columns
                columns = model_schema.get("fields", {}).keys()
                for column in columns:
                    # Skip auto-generated columns
                    if column in ["id", "created_at", "updated_at"]:
                        continue

                    result = conn.execute(
                        text(f"PRAGMA table_info({table_name})")
                    )
                    table_columns = [row[1] for row in result.fetchall()]

                    if column not in table_columns:
                        raise DatabaseInitializationError(
                            f"Column '{column}' not found in table '{table_name}'"
                        )

            # Check association tables
            for table_name in self.schema.get("association_tables", {}):
                result = conn.execute(
                    text(
                        "SELECT name FROM sqlite_master WHERE type='table' AND name=:table_name"
                    ),
                    {"table_name": table_name},
                )

                if not result.fetchone():
                    raise DatabaseInitializationError(
                        f"Association table '{table_name}' not created"
                    )

    def get_all_model_schemas(self) -> dict[str, dict[str, Any]]:
        """Get all model schemas."""
        return self.schema.get("models", {})

    def get_all_association_table_schemas(self) -> dict[str, dict[str, Any]]:
        """Get all association table schemas."""
        return self.schema.get("association_tables", {})

    def get_model_relationships(self, model_name: str) -> dict[str, Any]:
        """Get relationship information for a model."""
        model_schema = self.get_model_schema(model_name)
        return model_schema.get("relationships", {})

    def get_associated_models(self, model_name: str) -> list[str]:
        """Get list of models that this model has relationships with."""
        relationships = self.get_model_relationships(model_name)
        return [
            rel.get("target")
            for rel in relationships.values()
            if rel.get("target")
        ]

    def get_schema_summary(self) -> dict[str, Any]:
        """Get a summary of the schema structure."""
        models = list(self.schema.get("models", {}).keys())
        association_tables = list(
            self.schema.get("association_tables", {}).keys()
        )

        return {
            "total_models": len(models),
            "total_association_tables": len(association_tables),
            "models": models,
            "association_tables": association_tables,
            "generated_at": self.schema.get("generated_at"),
            "description": self.schema.get("description"),
        }


class DatabaseSchemaInitializer:
    """
    Helper class for database initialization using schema definitions.

    Provides methods to create, drop, and verify database structure
    based on the ToDoWrite model schema.
    """

    def __init__(
        self, validator: ToDoWriteSchemaValidator | None = None
    ) -> None:
        """Initialize with schema validator."""
        self.validator = validator or ToDoWriteSchemaValidator()

    def create_database(
        self, database_url: str, drop_existing: bool = False
    ) -> Engine:
        """
        Create a new database initialized with the ToDoWrite model schema.

        Args:
            database_url: SQLAlchemy database URL
            drop_existing: Whether to drop existing database first

        Returns:
            SQLAlchemy engine for the created database
        """
        engine = create_engine(database_url)

        try:
            self.validator.initialize_database_from_schema(
                engine, drop_existing
            )

            # Create session factory
            Session = sessionmaker(bind=engine)

            # Test the database
            with Session() as session:
                session.execute(text("SELECT 1"))

            return engine

        except Exception as e:
            raise DatabaseInitializationError(
                f"Failed to create database: {e}"
            )

    def verify_database_structure(self, database_url: str) -> bool:
        """Verify that database matches the schema structure."""
        engine = create_engine(database_url)

        try:
            self.validator._verify_database_structure(engine)
            return True
        except DatabaseInitializationError:
            return False

    def get_database_status(self, database_url: str) -> dict[str, Any]:
        """Get status information about the database."""
        engine = create_engine(database_url)

        try:
            schema_summary = self.validator.get_schema_summary()

            with engine.connect() as conn:
                # Count records in each table
                table_counts = {}

                for (
                    _model_name,
                    model_schema,
                ) in self.validator.get_all_model_schemas().items():
                    table_name = model_schema["table_name"]

                    try:
                        result = conn.execute(
                            text(f"SELECT COUNT(*) FROM {table_name}")
                        )
                        count = result.scalar()
                        table_counts[table_name] = count
                    except:
                        table_counts[table_name] = 0

                return {
                    "database_url": database_url,
                    "schema_matches": self.verify_database_structure(
                        database_url
                    ),
                    "table_counts": table_counts,
                    "schema_summary": schema_summary,
                }

        except Exception as e:
            return {
                "database_url": database_url,
                "schema_matches": False,
                "error": str(e),
                "schema_summary": self.validator.get_schema_summary(),
            }


# Global validator instance for easy access
_default_validator: ToDoWriteSchemaValidator | None = None


def get_schema_validator() -> ToDoWriteSchemaValidator:
    """Get the default schema validator instance."""
    global _default_validator
    if _default_validator is None:
        _default_validator = ToDoWriteSchemaValidator()
    return _default_validator


def validate_model_data(model_name: str, data: dict[str, Any]) -> bool:
    """Validate data against model schema using default validator."""
    validator = get_schema_validator()
    return validator.validate_model_data(model_name, data)


def initialize_database(
    database_url: str, drop_existing: bool = False
) -> Engine:
    """Initialize database with schema using default validator."""
    initializer = DatabaseSchemaInitializer()
    return initializer.create_database(database_url, drop_existing)
