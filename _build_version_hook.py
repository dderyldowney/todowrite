"""Build hook for dynamic version management."""

from __future__ import annotations


def get_project_version() -> str:
    """Get the project version from the central VERSION file.

    This function can be used by build tools to dynamically determine
    the version during the build process.

    Returns:
        The current version string.
    """
    # Import here to avoid flake8 E402 error while keeping path setup
    from shared_version import get_version

    return get_version()


if __name__ == "__main__":
    # Support command line usage for build tools
    print(get_project_version())
