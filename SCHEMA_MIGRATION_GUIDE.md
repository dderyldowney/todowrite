# ToDoWrite Schema Migration Guide

## Overview

This document describes the migration of the ToDoWrite JSON schema from the external `configs/schemas/` directory to the internal `todowrite/schemas/` package directory. This change ensures that the schema is properly distributed with the ToDoWrite package and easily accessible to external projects.

## Changes Made

### 1. Schema Relocation
- **Before**: `configs/schemas/todowrite.schema.json`
- **After**: `todowrite/schemas/todowrite.schema.json`

### 2. Package Configuration
Updated `pyproject.toml` to include schema files as package data:
```toml
[tool.setuptools.package-data]
todowrite = ["schemas/*.json"]
```

### 3. Schema Access Module
Created `todowrite/schema.py` for easy external access:
```python
from todowrite.schema import TODOWRITE_SCHEMA
```

### 4. Main Package Export
Updated `todowrite/__init__.py` to export the schema:
```python
from .schema import TODOWRITE_SCHEMA
```

### 5. Internal Loading Updates
- Updated `todowrite/app.py` to load schema from package-relative location
- Updated `todowrite/tools/tw_validate.py` with fallback to old location
- Updated `todowrite/tools/extract_schema.py` to reference new location

## External Project Usage

### Import and Use the Schema

```python
import todowrite

# Access the JSON schema
schema = todowrite.TODOWRITE_SCHEMA

# Use for validation
import json
from jsonschema import validate

# Example node data
node_data = {
    "id": "GOAL-PROJECT-001",
    "layer": "Goal",
    "title": "Project Goal",
    "description": "A high-level project goal",
    "links": {
        "parents": [],
        "children": []
    }
}

# Validate the data
validate(instance=node_data, schema=schema)
```

### Alternative Import Method

```python
from todowrite.schema import TODOWRITE_SCHEMA
```

## Backward Compatibility

### Legacy Support
Tools that reference the old schema location (`configs/schemas/todowrite.schema.json`) will continue to work if the old file structure is maintained. However, it's recommended to use the new package-relative schema import.

### Migration Path for Projects Using ToDoWrite
1. **No Action Required**: The package maintains backward compatibility
2. **Recommended Migration**: Update imports to use `todowrite.TODOWRITE_SCHEMA`
3. **Tools Update**: Update custom tools to use the new package schema

## Benefits

### 1. Package Distribution
- Schema is now distributed with the package installation
- No need for external projects to manage separate schema files
- Schema version stays in sync with package version

### 2. External Project Integration
- Easy schema import: `import todowrite; schema = todowrite.TODOWRITE_SCHEMA`
- No file path management required
- Consistent API for all ToDoWrite users

### 3. Maintainability
- Single source of truth for schema definition
- Schema updates are automatically available with package upgrades
- Reduced risk of schema version mismatches

## Implementation Details

### Schema Loading Logic
The new loading logic in `tw_validate.py`:
1. First tries to load from package: `todowrite.schema.TODOWRITE_SCHEMA`
2. Falls back to old location: `configs/schemas/todowrite.schema.json`
3. Provides clear error messages if neither is available

### Package Structure
```
todowrite/
├── __init__.py              # Exports TODOWRITE_SCHEMA
├── schema.py                # Schema loading module
├── schemas/
│   └── todowrite.schema.json # JSON schema definition
└── app.py                   # Updated to use package schema
```

### Path Resolution
- **Package Path**: `Path(__file__).parent / "schemas" / "todowrite.schema.json"`
- **Old Path**: `Path(__file__).parent.parent / "configs" / "schemas" / "todowrite.schema.json"`

## Testing

### External Project Test
```python
# Test that schema can be imported
import todowrite
assert hasattr(todowrite, 'TODOWRITE_SCHEMA')
assert isinstance(todowrite.TODOWRITE_SCHEMA, dict)

# Test basic validation
test_node = {
    "id": "GOAL-TEST-001",
    "layer": "Goal",
    "title": "Test Goal",
    "description": "A test goal",
    "links": {"parents": [], "children": []}
}

from jsonschema import validate
validate(instance=test_node, schema=todowrite.TODOWRITE_SCHEMA)
print("Schema validation successful!")
```

### CLI Validation Test
```bash
# Test CLI with new schema location
todowrite validate

# Should validate using package schema with fallback to old location
```

## Future Considerations

### Deprecation Timeline
- **Short Term**: Maintain backward compatibility with old schema location
- **Medium Term**: Update internal tools to exclusively use package schema
- **Long Term**: Consider removing old schema location dependency

### Enhancement Opportunities
1. **Versioned Schema**: Support multiple schema versions
2. **Schema Validation**: Add schema self-validation
3. **Documentation**: Auto-generate documentation from schema
4. **Registry Support**: Allow custom schema extensions

## Troubleshooting

### Common Issues

#### Import Error
```python
# If you get import errors, ensure the package is properly installed
pip install todowrite

# Then try importing
import todowrite
schema = todowrite.TODOWRITE_SCHEMA
```

#### Schema Not Found
```python
# Check if the schema file exists in the package
import todowrite.schema
print(todowrite.schema._SCHEMA_PATH)
```

#### Validation Errors
- Ensure your data matches the schema requirements
- Check that all required fields are present
- Validate layer types match the schema enum

### Debug Mode
Set environment variable for detailed schema loading information:
```bash
export TODOWRITE_DEBUG_SCHEMA=1
todowrite validate
```
