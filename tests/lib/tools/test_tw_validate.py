"""Tests for tw_validate module"""

import json
import os
import tempfile
from pathlib import Path

import pytest
from todowrite.tools.tw_validate import todowriteValidator


class TesttodowriteValidator:
    """Test cases for todowriteValidator class"""

    def test_init_with_schema_path(self):
        """Test initialization with custom schema path"""
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            schema_file = temp_path / "schema.json"

            # Create valid schema
            schema = {
                "$schema": "https://json-schema.org/draft/2020-12/schema",
                "type": "object",
                "properties": {"name": {"type": "string"}},
            }
            schema_file.write_text(json.dumps(schema))

            validator = todowriteValidator(str(schema_file))
            assert validator.schema_path == str(schema_file)
            assert validator.schema == schema

    def test_init_missing_schema_file(self):
        """Test initialization with missing schema file"""
        with pytest.raises(SystemExit) as excinfo:
            todowriteValidator("nonexistent_schema.json")
        assert excinfo.value.code == 1

    def test_load_schema_invalid_json(self):
        """Test loading invalid JSON schema"""
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            schema_file = temp_path / "invalid.json"
            schema_file.write_text("{ invalid json")

            with pytest.raises(SystemExit) as excinfo:
                todowriteValidator(str(schema_file))
            assert excinfo.value.code == 1

    def test_find_yaml_files_no_plans_directory(self):
        """Test finding YAML files when plans directory doesn't exist"""
        with tempfile.TemporaryDirectory() as temp_dir:
            # Change to temp directory where no configs/plans exists
            original_cwd = Path.cwd()
            try:
                os.chdir(temp_dir)
                validator = todowriteValidator()
                yaml_files = validator._find_yaml_files()
                assert yaml_files == []
            finally:
                os.chdir(original_cwd)

    def test_find_yaml_files_with_files(self):
        """Test finding YAML files in existing directory structure"""
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            plans_dir = temp_path / "configs" / "plans"
            plans_dir.mkdir(parents=True)

            # Create subdirectories with YAML files
            subdir1 = plans_dir / "project1"
            subdir2 = plans_dir / "project2"
            subdir1.mkdir()
            subdir2.mkdir()

            yaml1 = subdir1 / "plan.yaml"
            yaml2 = subdir1 / "backup.yaml"
            yaml3 = subdir2 / "another.yaml"

            yaml1.write_text("name: test")
            yaml2.write_text("name: backup")
            yaml3.write_text("name: another")

            # Change to temp directory for the validator to find our test structure
            original_cwd = Path.cwd()
            try:
                os.chdir(temp_dir)
                validator = todowriteValidator()
                yaml_files = validator._find_yaml_files()
                assert len(yaml_files) == 3
                # Files should be returned in sorted order
                assert any("project1" in str(f) for f in yaml_files)
                assert any("project2" in str(f) for f in yaml_files)
            finally:
                os.chdir(original_cwd)

    def test_load_yaml_file_success(self):
        """Test successful YAML file loading"""
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            yaml_file = temp_path / "test.yaml"
            yaml_file.write_text("name: test\nvalue: 42")

            validator = todowriteValidator()
            data, success = validator._load_yaml_file(yaml_file)

            assert success
            assert data == {"name": "test", "value": 42}

    def test_load_yaml_file_invalid_yaml(self):
        """Test loading invalid YAML file"""
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            yaml_file = temp_path / "invalid.yaml"
            yaml_file.write_text("invalid: yaml: content: [")  # Invalid YAML

            validator = todowriteValidator()
            data, success = validator._load_yaml_file(yaml_file)

            assert not success
            assert data == {}

    def test_validate_file_success(self):
        """Test successful file validation"""
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            schema_file = temp_path / "schema.json"
            yaml_file = temp_path / "test.yaml"

            # Create schema
            schema = {
                "$schema": "https://json-schema.org/draft/2020-12/schema",
                "type": "object",
                "properties": {"name": {"type": "string"}},
                "required": ["name"],
            }
            schema_file.write_text(json.dumps(schema))

            # Create valid YAML
            yaml_file.write_text("name: test")

            validator = todowriteValidator(str(schema_file))
            result = validator.validate_file(yaml_file, strict=True)
            assert result

    def test_validate_file_failure(self):
        """Test file validation failure"""
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            schema_file = temp_path / "schema.json"
            yaml_file = temp_path / "test.yaml"

            # Create schema
            schema = {
                "$schema": "https://json-schema.org/draft/2020-12/schema",
                "type": "object",
                "properties": {"name": {"type": "string"}},
                "required": ["name"],
            }
            schema_file.write_text(json.dumps(schema))

            # Create invalid YAML (missing required field)
            yaml_file.write_text("other: value")

            validator = todowriteValidator(str(schema_file))
            result = validator.validate_file(yaml_file, strict=True)
            assert not result

    def test_validate_all_no_files(self):
        """Test validate_all when no YAML files found"""
        with tempfile.TemporaryDirectory() as temp_dir:
            # Change to empty temp directory
            original_cwd = Path.cwd()
            try:
                os.chdir(temp_dir)
                validator = todowriteValidator()
                valid_count, total_count = validator.validate_all()
                assert valid_count == 0
                assert total_count == 0
            finally:
                os.chdir(original_cwd)

    def test_validate_all_with_files(self):
        """Test validate_all with files to validate"""
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            plans_dir = temp_path / "configs" / "plans"
            plans_dir.mkdir(parents=True)

            # Create test directory and files
            subdir = plans_dir / "test_project"
            subdir.mkdir()

            # Create schema file
            schema_file = temp_path / "schema.json"
            schema = {
                "$schema": "https://json-schema.org/draft/2020-12/schema",
                "type": "object",
                "properties": {"name": {"type": "string"}},
                "required": ["name"],
            }
            schema_file.write_text(json.dumps(schema))

            # Create one valid and one invalid file
            valid_file = subdir / "valid.yaml"
            invalid_file = subdir / "invalid.yaml"
            valid_file.write_text("name: test")
            invalid_file.write_text("other: value")  # Missing required 'name'

            # Change to temp directory for validator to find files
            original_cwd = Path.cwd()
            try:
                os.chdir(temp_dir)
                validator = todowriteValidator(str(schema_file))
                valid_count, total_count = validator.validate_all(strict=True)
                assert total_count == 2
                assert valid_count == 1  # Only one file is valid
            finally:
                os.chdir(original_cwd)

    def test_generate_summary_success(self):
        """Test summary generation for successful validation"""
        validator = todowriteValidator()
        # This just verifies the method runs without error
        validator.generate_summary(5, 5)

    def test_generate_summary_failure(self):
        """Test summary generation for failed validation"""
        validator = todowriteValidator()
        # This just verifies the method runs without error
        validator.generate_summary(3, 5)

    def test_complex_schema_validation(self):
        """Test validation with complex nested schema"""
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            schema_file = temp_path / "complex_schema.json"
            yaml_file = temp_path / "complex.yaml"

            # Create complex schema
            complex_schema = {
                "$schema": "https://json-schema.org/draft/2020-12/schema",
                "type": "object",
                "properties": {
                    "project": {
                        "type": "object",
                        "properties": {
                            "name": {"type": "string"},
                            "version": {"type": "string"},
                            "tasks": {
                                "type": "array",
                                "items": {
                                    "type": "object",
                                    "properties": {
                                        "id": {"type": "integer"},
                                        "title": {"type": "string"},
                                        "completed": {"type": "boolean"},
                                    },
                                    "required": ["id", "title"],
                                },
                            },
                        },
                        "required": ["name", "tasks"],
                    }
                },
                "required": ["project"],
            }
            schema_file.write_text(json.dumps(complex_schema))

            # Create valid complex YAML
            complex_yaml = """
project:
  name: "Test Project"
  version: "1.0.0"
  tasks:
    - id: 1
      title: "First task"
      completed: false
    - id: 2
      title: "Second task"
      completed: true
"""
            yaml_file.write_text(complex_yaml)

            validator = todowriteValidator(str(schema_file))
            result = validator.validate_file(yaml_file, strict=True)
            assert result

    def test_validation_with_additional_properties(self):
        """Test validation allowing additional properties"""
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            schema_file = temp_path / "schema.json"
            yaml_file = temp_path / "test.yaml"

            # Create schema that allows additional properties
            schema = {
                "$schema": "https://json-schema.org/draft/2020-12/schema",
                "type": "object",
                "properties": {"name": {"type": "string"}},
                "required": ["name"],
                "additionalProperties": True,
            }
            schema_file.write_text(json.dumps(schema))

            # Create YAML with additional properties
            yaml_file.write_text("name: test\nextra: property\nanother_extra: value")

            validator = todowriteValidator(str(schema_file))
            result = validator.validate_file(yaml_file, strict=True)
            assert result
