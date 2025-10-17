"""
Common JSON operations for checkpoint and session management.

Provides consistent JSON file handling across all session management tools.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def load_json(file_path: Path | str, default: Any = None) -> Any:
    """Load JSON data from file.

    Parameters
    ----------
    file_path : Path | str
        Path to JSON file
    default : Any, optional
        Default value if file doesn't exist

    Returns
    -------
    Any
        Loaded JSON data or default value
    """
    file_path = Path(file_path)

    if not file_path.exists():
        return default

    try:
        with open(file_path) as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError):
        return default


def save_json(file_path: Path | str, data: Any) -> bool:
    """Save JSON data to file.

    Parameters
    ----------
    file_path : Path | str
        Path to JSON file
    data : Any
        Data to save

    Returns
    -------
    bool
        True if successful, False otherwise
    """
    file_path = Path(file_path)

    try:
        # Create parent directories if they don't exist
        file_path.parent.mkdir(parents=True, exist_ok=True)

        with open(file_path, "w") as f:
            json.dump(data, f, indent=2, default=str)
        return True
    except (OSError, TypeError):
        return False
