"""Version information for ToDoWrite CLI."""

from __future__ import annotations

from pathlib import Path

# Navigate from: cli_package/src/todowrite_cli/version.py -> project root
current_file = Path(__file__)
project_root = current_file.parent.parent.parent.parent

# Read version from central VERSION file
version_file = project_root / "VERSION"
if version_file.exists():
    __version__ = version_file.read_text().strip()
else:
    # Fallback - should never happen in a proper installation
    __version__ = "0.0.0"

__author__ = "D Deryl Downey"
__email__ = "dderyldowney@gmail.com"

__all__ = ["__author__", "__email__", "__version__"]
