"""Version information for the ToDoWrite package."""

from __future__ import annotations

import sys
from pathlib import Path

# Navigate from: lib_package/src/ToDoWrite/version.py -> project root
current_file = Path(__file__)
project_root = current_file.parent.parent.parent.parent

# Try to import from shared_version.py at project root
if (project_root / "shared_version.py").exists():
    sys.path.insert(0, str(project_root))
    from shared_version import __author__, __email__, __version__, get_version
else:
    # Fallback for when shared_version.py is not available
    __version__ = "0.5.0"  # MAJOR BREAKING CHANGE: ToDoWrite Models API Only
    __author__ = "D Deryl Downey"
    __email__ = "dderyldowney@gmail.com"

    def get_version() -> str:
        return __version__


__all__ = ["__author__", "__email__", "__version__", "get_version"]
