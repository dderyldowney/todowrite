"""ToDoWrite schema module for external projects.

This module provides access to the JSON schema for validating ToDoWrite nodes.
Projects can import this schema to validate data before creating nodes.
"""

import json
from pathlib import Path

# Get the path to the schema file within the package
_SCHEMA_PATH = Path(__file__).parent / "schemas" / "ToDoWrite.schema.json"

# Load the schema
try:
    with open(_SCHEMA_PATH) as f:
        ToDoWrite_SCHEMA = json.load(f)
except FileNotFoundError as err:
    raise FileNotFoundError(
        f"ToDoWrite schema not found at {_SCHEMA_PATH}. "
        "The schema should be included in the ToDoWrite package."
    ) from err

__all__ = ["ToDoWrite_SCHEMA"]
