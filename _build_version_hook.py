"""Build hook for dynamic version management."""

from __future__ import annotations

import sys
from pathlib import Path

# Add root to path to import _version
sys.path.insert(0, str(Path(__file__).parent))

from _version import get_version


def get_project_version() -> str:
    """Get the project version from the central VERSION file.

    This function can be used by build tools to dynamically determine
    the version during the build process.

    Returns:
        The current version string.
    """
    return get_version()


if __name__ == "__main__":
    # Support command line usage for build tools
    print(get_project_version())
