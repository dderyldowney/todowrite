#!/usr/bin/env python3
"""
ToDoWrite Schema Validator (tw_validate.py)
Validates all YAML files in configs/plans/* against ToDoWrite.schema.json
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import TypedDict

import yaml
from jsonschema import Draft202012Validator, ValidationError, validate


# Type definitions for ToDoWrite YAML data structure
class RequirementSpec(TypedDict):
    """Type for a requirement specification."""

    title: str
    description: str
    priority: str
    status: str


class AcceptanceCriteriaSpec(TypedDict):
    """Type for acceptance criteria specification."""

    criteria: str
    given: str
    when: str
    then: str


class TaskSpec(TypedDict):
    """Type for a task specification."""

    title: str
    description: str
    status: str
    priority: str


class SubTaskSpec(TypedDict):
    """Type for a subtask specification."""

    title: str
    description: str
    status: str
    parent_task: str


class CommandSpec(TypedDict):
    """Type for a command specification."""

    command: str
    description: str
    parameters: dict[str, str]


class PhaseSpec(TypedDict):
    """Type for a phase specification."""

    name: str
    description: str
    status: str
    steps: list[str]


class StepSpec(TypedDict):
    """Type for a step specification."""

    title: str
    description: str
    status: str
    tasks: list[str]


class ConceptSpec(TypedDict):
    """Type for a concept specification."""

    name: str
    description: str
    context: str


class ContextSpec(TypedDict):
    """Type for a context specification."""

    name: str
    description: str
    constraints: list[str]


class ConstraintSpec(TypedDict):
    """Type for a constraint specification."""

    name: str
    description: str
    type: str


class InterfaceContractSpec(TypedDict):
    """Type for an interface contract specification."""

    name: str
    interface_type: str
    methods: dict[str, dict[str, str]]


class LabelSpec(TypedDict):
    """Type for a label specification."""

    name: str
    color: str
    description: str


class ToDoWriteYAMLData(TypedDict):
    """Complete type for ToDoWrite YAML file data structure."""

    # Core planning elements
    title: str
    description: str
    status: str
    priority: str

    # Optional structured components
    requirements: dict[str, RequirementSpec] | None
    acceptance_criteria: dict[str, AcceptanceCriteriaSpec] | None
    tasks: dict[str, TaskSpec] | None
    subtasks: dict[str, SubTaskSpec] | None
    commands: dict[str, CommandSpec] | None
    phases: dict[str, PhaseSpec] | None
    steps: dict[str, StepSpec] | None
    concepts: dict[str, ConceptSpec] | None
    contexts: dict[str, ContextSpec] | None
    constraints: dict[str, ConstraintSpec] | None
    interface_contracts: dict[str, InterfaceContractSpec] | None
    labels: dict[str, LabelSpec] | None

    # Metadata
    created_at: str | None
    updated_at: str | None
    version: str | None
    tags: list[str] | None


# Type definitions for JSON schema structure
class JSONSchema(TypedDict, total=False):
    """Base type for JSON Schema definitions."""

    type: str
    properties: dict[str, JSONSchema]
    required: list[str]
    items: JSONSchema
    additionalProperties: bool | JSONSchema
    ref: str  # JSON Schema $ref field
    description: str
    enum: list[str | int | bool | None]
    minimum: int | None
    maximum: int | None
    pattern: str | None


class ToDoWriteJSONSchema(TypedDict):
    """Type for the complete ToDoWrite JSON schema."""

    schema: str  # JSON Schema $schema field
    id: str  # JSON Schema $id field
    title: str
    description: str
    type: str
    properties: dict[str, JSONSchema]
    required: list[str]
    additionalProperties: bool


class todowriteValidator:
    """Schema validator for ToDoWrite YAML files"""

    def __init__(
        self: todowriteValidator, schema_path: str | None = None
    ) -> None:
        if schema_path is None:
            # Try to load from package first, fall back to old location
            try:
                from todowrite.core.schemas import todowrite_SCHEMA

                self.schema: ToDoWriteJSONSchema = todowrite_SCHEMA
                self.schema_path = (
                    "ToDoWrite.schema"  # Virtual path for display
                )
                self.validator = Draft202012Validator(self.schema)
                return
            except ImportError:
                schema_path = "configs/schemas/ToDoWrite.schema.json"

        self.schema_path = schema_path
        self.schema = self._load_schema()
        self.validator = Draft202012Validator(self.schema)

    def _load_schema(self) -> ToDoWriteJSONSchema:
        """Load JSON schema from file"""
        try:
            with open(self.schema_path) as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"ERROR: Schema file not found: {self.schema_path}")
            print("Run 'make tw-schema' to generate schema file")
            sys.exit(1)
        except json.JSONDecodeError as e:
            print(f"ERROR: Invalid JSON in schema file: {e}")
            sys.exit(1)

    def _find_yaml_files(self) -> list[Path]:
        """Find all YAML files in configs/plans/* directories"""
        yaml_files: list[Path] = []
        plans_dir = Path("configs/plans")

        if not plans_dir.exists():
            print(f"ERROR: Plans directory not found: {plans_dir}")
            print("Run 'make tw-init' to initialize directory structure")
            return []

        # Scan all subdirectories for .yaml files
        for subdir in plans_dir.iterdir():
            if subdir.is_dir():
                yaml_files.extend(subdir.glob("*.yaml"))

        return sorted(yaml_files)

    def _load_yaml_file(
        self: todowriteValidator, file_path: Path
    ) -> tuple[ToDoWriteYAMLData, bool]:
        """Load and parse YAML file, return (data, success)"""
        try:
            with open(file_path) as f:
                data = yaml.safe_load(f)
            return data, True
        except yaml.YAMLError as e:
            print(f"ERROR: Invalid YAML in {file_path}: {e}")
            return {}, False
        except (OSError, PermissionError) as e:
            print(f"ERROR: Failed to read {file_path}: {e}")
            return {}, False

    def validate_file(
        self: todowriteValidator, file_path: Path, strict: bool = False
    ) -> bool:
        """Validate single YAML file against schema"""
        data, load_success = self._load_yaml_file(file_path)
        if not load_success:
            return False

        try:
            validate(instance=data, schema=self.schema)
            if not strict:
                print(f"✓ {file_path}")
            return True

        except ValidationError as e:
            print(f"✗ {file_path}")
            print(f"  Validation Error: {e.message}")
            if e.absolute_path:
                path_str = " -> ".join(str(p) for p in e.absolute_path)
                print(f"  Location: {path_str}")
            if e.instance is not None:
                print(f"  Invalid value: {e.instance}")
            print()
            return False

    def validate_all(
        self: todowriteValidator, strict: bool = False
    ) -> tuple[int, int]:
        """Validate all YAML files, return (valid_count, total_count)"""
        yaml_files = self._find_yaml_files()

        if not yaml_files:
            print("No YAML files found in configs/plans/")
            return 0, 0

        valid_count = 0
        total_count = len(yaml_files)

        print(f"Validating {total_count} YAML files against schema...")
        print()

        for file_path in yaml_files:
            if self.validate_file(file_path, strict):
                valid_count += 1

        return valid_count, total_count

    def generate_summary(
        self, valid_count: int, total_count: int, strict: bool = False
    ) -> None:
        """Generate validation summary report"""
        print("=" * 50)
        print("VALIDATION SUMMARY")
        print("=" * 50)
        print(f"Total files processed: {total_count}")
        print(f"Valid files: {valid_count}")
        print(f"Invalid files: {total_count - valid_count}")

        if valid_count == total_count:
            print("✓ All files are valid!")
            status = "SUCCESS"
        else:
            print(
                f"✗ {total_count - valid_count} files have validation errors"
            )
            status = "FAILED"

        print(f"Validation {status} {'(strict mode)' if strict else ''}")
        print("=" * 50)


def main() -> None:
    """Main entry point for tw_validate.py"""
    parser = argparse.ArgumentParser(
        description="Validate ToDoWrite YAML files against JSON schema"
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Enable strict mode with detailed error reporting",
    )
    parser.add_argument(
        "--summary", action="store_true", help="Show summary report only"
    )
    parser.add_argument(
        "--schema",
        default="configs/schemas/ToDoWrite.schema.json",
        help="Path to JSON schema file",
    )

    args = parser.parse_args()

    # Initialize validator
    validator = todowriteValidator(args.schema)

    # Run validation
    valid_count, total_count = validator.validate_all(args.strict)

    # Generate summary if requested or if there are errors
    if args.summary or valid_count != total_count or args.strict:
        print()
        validator.generate_summary(valid_count, total_count, args.strict)

    # Exit with appropriate code
    sys.exit(0 if valid_count == total_count else 1)


if __name__ == "__main__":
    main()
