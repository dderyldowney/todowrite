# ToDoWrite Schema Usage for External Projects

## Overview

TheToDoWrite package now includes its JSON schema as part of the package distribution, making it easy for external projects to validate their data without manually managing schema files.

## Importing the Schema

External projects can import the schema directly from the todowrite package:

```python
import todowrite

# Access the JSON schema
schema = todowrite.TODOWRITE_SCHEMA

# Example usage for validation
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

# Validate the data against the schema
try:
    validate(instance=node_data, schema=schema)
    print("Node data is valid!")
except jsonschema.ValidationError as e:
    print(f"Validation error: {e}")
```

## Alternative Usage

You can also import the schema module directly:

```python
from todowrite.schema import TODOWRITE_SCHEMA
from jsonschema import validate

# Use the schema for validation
validate(instance=your_data, schema=TODOWRITE_SCHEMA)
```

## Schema Location

The schema is now distributed with the package at:
```
todowrite/schemas/todowrite.schema.json
```

This ensures that:
1. The schema is always available when the package is installed
2. External projects don't need to manage separate schema files
3. The schema version stays in sync with the package version

## Legacy Support

For backward compatibility, tools that reference the old schema location (`configs/schemas/todowrite.schema.json`) will still work if the old file structure is present. However, it's recommended to use the new package-relative schema import.

## CLI Usage

The schema is also used internally by the CLI for validation:
```bash
# Validate YAML files using the package schema
todowrite validate --schema todowrite.schema
```

## Integration Tips

1. **Version Control**: Always validate your data before committing to ensure schema compliance
2. **CI/CD**: Add schema validation to your CI pipeline to catch schema violations early
3. **Custom Validation**: Extend the schema validation with project-specific rules while using the base schema for structure validation
