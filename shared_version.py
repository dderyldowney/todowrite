"""Shared version module that can be easily imported from both packages."""

from __future__ import annotations

import re
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
# The VERSION file is the authoritative source - always edit it to bump
# This literal is kept in sync with VERSION file for Hatch build system
# compatibility. Run sync_version() after editing VERSION file to update
__version__ = "0.3.1"  # KEEP IN SYNC - run sync_version() after editing VERSION

# Package metadata
__author__ = "D Deryl Downey"
__email__ = "dderyldowney@gmail.com"


def get_version() -> str:
    """Return the current version string from VERSION file "
    "(single source of truth).

    This function reads the version from the VERSION file, ensuring
    that all packages use the same version as their single source of truth.

    Returns:
        The current version string from VERSION file.
    """
    return _get_version()


def sync_version() -> None:
    """Sync __version__ literal with VERSION file content.

    This function should be run after editing the VERSION file to keep
    the literal __version__ in sync for Hatch build system compatibility.

    Example:
        python -c "from shared_version import sync_version; sync_version()"
    """
    new_version = _get_version()
    current_file = Path(__file__)

    # Read current file content
    content = current_file.read_text(encoding="utf-8")

    # Find and replace the __version__ line
    version_pattern = r'^__version__ = "[^"]*"'
    new_line = f'__version__ = "{new_version}"'

    new_content = re.sub(version_pattern, new_line, content, flags=re.MULTILINE)

    # Only write if changed
    if new_content != content:
        current_file.write_text(new_content, encoding="utf-8")
        print(f"✅ Synced __version__ to {new_version}")
    else:
        msg = f"✅ __version__ already in sync with VERSION file ({new_version})"
        print(msg)


__all__ = ["__author__", "__email__", "__version__", "get_version"]
