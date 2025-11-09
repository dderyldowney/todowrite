"""Tests for extract_schema module"""

import json
import tempfile
from pathlib import Path

import pytest
from todowrite.tools.extract_schema import extract_and_write_schema


class TestExtractSchema:
    """Test cases for extract_and_write_schema function"""

    def test_extract_schema_success(self):
        """Test successful schema extraction from markdown"""
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            markdown_file = temp_path / "test.md"
            schema_file = temp_path / "schema.json"

            # Create markdown file with JSON schema
            markdown_content = """
# Some Markdown

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "type": "object",
  "properties": {
    "name": {"type": "string"}
  }
}
```

More content
"""
            markdown_file.write_text(markdown_content)

            # Extract schema
            extract_and_write_schema(markdown_file, schema_file)

            # Verify schema file was created
            assert schema_file.exists()

            # Verify schema content
            schema_data = json.loads(schema_file.read_text())
            assert schema_data["type"] == "object"
            assert "name" in schema_data["properties"]

    def test_extract_schema_no_json_block(self):
        """Test handling when no JSON block is found"""
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            markdown_file = temp_path / "test.md"
            schema_file = temp_path / "schema.json"

            # Create markdown file without JSON schema
            markdown_content = "# Just some markdown without JSON blocks"
            markdown_file.write_text(markdown_content)

            # Should exit with error
            with pytest.raises(SystemExit) as excinfo:
                extract_and_write_schema(markdown_file, schema_file)
            assert excinfo.value.code == 1

    def test_extract_schema_file_not_found(self):
        """Test handling when markdown file doesn't exist"""
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            markdown_file = temp_path / "nonexistent.md"
            schema_file = temp_path / "schema.json"

            # Should exit with error
            with pytest.raises(SystemExit) as excinfo:
                extract_and_write_schema(markdown_file, schema_file)
            assert excinfo.value.code == 1

    def test_extract_schema_invalid_json(self):
        """Test handling when JSON is invalid"""
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            markdown_file = temp_path / "test.md"
            schema_file = temp_path / "schema.json"

            # Create markdown file with invalid JSON
            markdown_content = """
# Some Markdown

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "type": "object",
  "properties": {
    "name": {"type": "string"  // Missing comma
  }
}
```
"""
            markdown_file.write_text(markdown_content)

            # Should exit with error
            with pytest.raises(SystemExit) as excinfo:
                extract_and_write_schema(markdown_file, schema_file)
            assert excinfo.value.code == 1

    def test_extract_schema_creates_directory(self):
        """Test that output directory is created if it doesn't exist"""
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            markdown_file = temp_path / "test.md"
            schema_file = temp_path / "nested" / "dir" / "schema.json"

            # Create markdown file with JSON schema
            markdown_content = """
```json
{"type": "object"}
```
"""
            markdown_file.write_text(markdown_content)

            # Extract schema
            extract_and_write_schema(markdown_file, schema_file)

            # Verify nested directory was created
            assert schema_file.parent.exists()
            assert schema_file.exists()

    def test_extract_schema_complex_json(self):
        """Test extraction of complex JSON schema with nested objects"""
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            markdown_file = temp_path / "test.md"
            schema_file = temp_path / "schema.json"

            # Create markdown file with complex JSON schema
            markdown_content = """
# API Documentation

## Schema Definition

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "type": "object",
  "properties": {
    "user": {
      "type": "object",
      "properties": {
        "id": {"type": "integer"},
        "name": {"type": "string"},
        "email": {"type": "string", "format": "email"}
      },
      "required": ["id", "name"]
    },
    "permissions": {
      "type": "array",
      "items": {"type": "string"}
    }
  },
  "required": ["user"]
}
```

## Usage
"""
            markdown_file.write_text(markdown_content)

            # Extract schema
            extract_and_write_schema(markdown_file, schema_file)

            # Verify schema file was created with correct content
            assert schema_file.exists()
            schema_data = json.loads(schema_file.read_text())

            assert schema_data["type"] == "object"
            assert "user" in schema_data["properties"]
            assert "permissions" in schema_data["properties"]
            assert schema_data["properties"]["user"]["type"] == "object"
            assert schema_data["properties"]["permissions"]["type"] == "array"
            assert "id" in schema_data["properties"]["user"]["properties"]
