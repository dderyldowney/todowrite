"""Utility functions for database naming and path management."""

import os
from pathlib import Path


def get_project_name() -> str:
    """Get the current project name based on current working directory."""
    # Get current working directory name
    cwd = Path.cwd()
    project_name = cwd.name

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
        environment: The environment type (development, testing, production, etc.)
        project_name: Optional project name override. If None, detected from CWD.

    Returns:
        Database filename with project-specific naming.
    """
    if project_name is None:
        project_name = get_project_name()

    return f"todowrite_{project_name}_{environment}.db"


def get_database_path(
    environment: str = "development",
    base_dir: str | None = None,
    project_name: str | None = None,
) -> str:
    """Get a full database path with project-specific naming.

    Args:
        environment: The environment type (development, testing, production, etc.)
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
        from pathlib import Path
        project_root = Path.cwd()
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
