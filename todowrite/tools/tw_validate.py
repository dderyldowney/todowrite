#!/usr/bin/env python3
"""
ToDoWrite Schema Validator (tw_validate.py)
Validates all YAML files in configs/plans/* against todowrite.schema.json
"""

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, List, Tuple

import yaml
from jsonschema import Draft202012Validator, ValidationError, validate


class ToDoWriteValidator:
    """Schema validator for ToDoWrite YAML files"""

    def __init__(self, schema_path: str = "configs/schemas/todowrite.schema.json"):
        self.schema_path = schema_path
        self.schema = self._load_schema()
        self.validator = Draft202012Validator(self.schema)

    def _load_schema(self) -> Dict[str, Any]:
        """Load JSON schema from file"""
        try:
            with open(self.schema_path, "r") as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"ERROR: Schema file not found: {self.schema_path}")
            print("Run 'make tw-schema' to generate schema file")
            sys.exit(1)
        except json.JSONDecodeError as e:
            print(f"ERROR: Invalid JSON in schema file: {e}")
            sys.exit(1)

    def _find_yaml_files(self) -> List[Path]:
        """Find all YAML files in configs/plans/* directories"""
        yaml_files = []
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

    def _load_yaml_file(self, file_path: Path) -> Tuple[Dict[str, Any], bool]:
        """Load and parse YAML file, return (data, success)"""
        try:
            with open(file_path, "r") as f:
                data = yaml.safe_load(f)
            return data, True
        except yaml.YAMLError as e:
            print(f"ERROR: Invalid YAML in {file_path}: {e}")
            return {}, False
        except Exception as e:
            print(f"ERROR: Failed to read {file_path}: {e}")
            return {}, False

    def validate_file(self, file_path: Path, strict: bool = False) -> bool:
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
                print(f"  Location: {' -> '.join(str(p) for p in e.absolute_path)}")
            if e.instance is not None:
                print(f"  Invalid value: {e.instance}")
            print()
            return False

    def validate_all(self, strict: bool = False) -> Tuple[int, int]:
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
            print(f"✗ {total_count - valid_count} files have validation errors")
            status = "FAILED"

        print(f"Validation {status} {'(strict mode)' if strict else ''}")
        print("=" * 50)


def main():
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
        default="configs/schemas/todowrite.schema.json",
        help="Path to JSON schema file",
    )

    args = parser.parse_args()

    # Initialize validator
    validator = ToDoWriteValidator(args.schema)

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
