"""Shared version module that can be easily imported from both packages."""

from __future__ import annotations

from pathlib import Path

# Get the project root directory (where VERSION file is located)
# This works when called from any subdirectory
PROJECT_ROOT = Path(__file__).parent

# Read version from VERSION file
VERSION_FILE = PROJECT_ROOT / "VERSION"


def _get_version() -> str:
    """Read version from VERSION file with fallback."""
    try:
        return VERSION_FILE.read_text(encoding="utf-8").strip()
    except (FileNotFoundError, OSError):
        return "0.2.2"  # Fallback version


# Single source of truth for version
# NOTE: Hatch build system requires this to be a literal string for
# regex parsing
__version__ = "0.3.1"  # This should match VERSION file content

# Package metadata
__author__ = "D Deryl Downey"
__email__ = "dderyldowney@gmail.com"


def get_version() -> str:
    """Return the current version string.

    This function reads the version from the VERSION file, ensuring
    that all packages use the same version as their single source of truth.

    Returns:
        The current version string.
    """
    return __version__


__all__ = ["__author__", "__email__", "__version__", "get_version"]
