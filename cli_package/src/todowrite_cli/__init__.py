"""ToDoWrite CLI Package - CLI interface for the ToDoWrite library."""

from .main import cli as main
from .version import __author__, __email__, __version__

__all__ = ["__author__", "__email__", "__version__", "main"]
