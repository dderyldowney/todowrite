"""Version information for the todowrite package."""

__version__ = "0.2.2"
__author__ = "D Deryl Downey"
__email__ = "dderyldowney@gmail.com"


def get_version() -> str:
    """Return the current version string."""
    return __version__


__all__ = ["__version__", "__author__", "__email__", "get_version"]
