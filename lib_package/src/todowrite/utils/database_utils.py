"""Utility functions for database naming and path management."""

import os
from pathlib import Path


def find_project_root() -> str:
    """Find the project root (monorepo root) by looking for package structure.

    Searches up the directory tree for a directory containing lib_package,
    cli_package, and web_package subdirectories.

    Returns:
        Path to project root directory, or current directory if not found
    """
    search_dir = Path.cwd()

    # Search up the directory tree for project root
    # (contains lib_package, cli_package, web_package)
    while str(search_dir) != "/":
        if (
            (search_dir / "lib_package").exists()
            and (search_dir / "cli_package").exists()
            and (search_dir / "web_package").exists()
        ):
            return str(search_dir)
        search_dir = search_dir.parent

    # If not found, return current directory
    # (fallback for non-monorepo projects)
    return str(Path.cwd())


def get_project_name() -> str:
    """Get the current project name based on project root detection."""
    # Try to find project root first
    project_root = find_project_root()
    project_name = Path(project_root).name

    # If we found a project root that's different from current directory,
    # use its name
    if project_root != str(Path.cwd()):
        # We're in a package directory, use the project root name
        pass  # project_name already set correctly
    else:
        # Fallback to current directory name for non-monorepo projects
        project_name = Path.cwd().name

    # If directory name is generic or empty, use a timestamp-based fallback
    generic_names = {"", ".", "src", "lib", "app", "project", "home"}
    if project_name in generic_names or not project_name:
        from datetime import datetime

        project_name = f"project_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

    # Sanitize project name for filesystem
    project_name = project_name.replace(" ", "_").replace("-", "_")
    project_name = "".join(c for c in project_name if c.isalnum() or c == "_")

    return project_name


def get_project_database_name(
    environment: str = "development", project_name: str | None = None
) -> str:
    """Generate a project-specific database name for the given environment.

    Args:
        environment: The environment type (development, testing, production)
        project_name: Optional project name override. If None,
                    detected from CWD.

    Returns:
        Database filename with project-specific naming.
    """
    if project_name is None:
        project_name = get_project_name()

    return f"ToDoWrite_{project_name}_{environment}.db"


def get_database_path(
    environment: str = "development",
    base_dir: str | None = None,
    project_name: str | None = None,
) -> str:
    """Get a full database path with project-specific naming.

    Args:
        environment: The environment type (development, testing, production)
        base_dir: Base directory for databases. Defaults to ~/dbs
        project_name: Optional project name override.

    Returns:
        Full path to the database file.
    """
    if project_name is None:
        project_name = get_project_name()

    db_name = get_project_database_name(environment, project_name)

    # Handle different environments with different base directories
    if environment == "testing":
        # Testing databases go in project_root/tmp
        project_root = Path(find_project_root())
        tmp_dir = project_root / "tmp"
        tmp_dir.mkdir(exist_ok=True)
        db_path = tmp_dir / db_name
    elif environment == "production":
        # Production databases go in ~/dbs
        if base_dir is None:
            base_dir = "~/dbs"
        db_path = os.path.join(os.path.expanduser(base_dir), db_name)
    else:
        # Development databases go in ~/dbs
        if base_dir is None:
            base_dir = "~/dbs"
        db_path = os.path.join(os.path.expanduser(base_dir), db_name)

    return str(db_path)
