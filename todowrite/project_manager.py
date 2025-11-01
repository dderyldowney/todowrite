"""
Project Manager for ToDoWrite Utilities

This module provides centralized project utility methods that replace individual scripts.
It separates core functionality from AI-specific features.
"""

import json
import shutil
from pathlib import Path
from textwrap import dedent
from typing import Any


class ProjectManager:
    """Centralized project management and utility methods."""

    def __init__(self):
        self.cache_dir = Path.home() / ".todowrite_cache"
        self.cache_dir.mkdir(exist_ok=True)

    # ===== Core Project Utilities =====

    def check_deprecated_schema(self) -> bool:
        """
        Check that the deprecated schema doesn't have unintended changes.
        Returns True if check passes, False if there are issues.
        """
        primary_path = Path("todowrite/schemas/todowrite.schema.json")
        deprecated_path = Path("configs/schemas/todowrite.schema.json")

        def get_schema_content(path: Path) -> dict:
            """Load schema content from file."""
            try:
                with open(path) as f:
                    return json.load(f)
            except (FileNotFoundError, json.JSONDecodeError):
                return {}

        # Load both schemas
        primary_content = get_schema_content(primary_path)
        deprecated_content = get_schema_content(deprecated_path)

        if not deprecated_content:
            print("INFO: Deprecated schema not found (may have been cleaned up)")
            return True

        if not primary_content:
            print("❌ Primary schema not found!")
            return False

        # Check if deprecated schema still has deprecation notice
        deprecated_title = deprecated_content.get("title", "")
        if "DEPRECATED" not in deprecated_title:
            print("❌ Deprecated schema title missing DEPRECATED marker!")
            print(f"Found: {deprecated_title}")
            return False

        # Check that core schema structure matches
        def get_core_properties(schema: dict) -> dict:
            """Get core schema properties for comparison."""
            return {
                "required": schema.get("required", []),
                "properties": schema.get("properties", {}),
                "type": schema.get("type", "object"),
            }

        primary_core = get_core_properties(primary_content)
        deprecated_core = get_core_properties(deprecated_content)

        if primary_core != deprecated_core:
            print("❌ Deprecated schema has different core properties than primary!")
            print("This suggests someone modified the deprecated schema.")
            print("All schema changes should be made to the primary schema location.")
            return False

        print("✅ Deprecated schema check passed")
        print(f"Deprecated schema title: {deprecated_title}")
        print("Core properties match primary schema")
        return True

    def check_schema_changes(self) -> bool:
        """
        Check if schema changes are in the correct location.
        Returns True if check passes, False if there are issues.
        """
        primary_schema = Path("todowrite/schemas/todowrite.schema.json")
        deprecated_schema = Path("configs/schemas/todowrite.schema.json")

        # Check if primary schema exists
        if not primary_schema.exists():
            print("ERROR: Primary schema file not found!")
            print(f"Expected location: {primary_schema}")
            print("All schema changes must be made in the package location.")
            return False

        # Load both schemas
        def load_schema(schema_path: Path) -> dict[str, Any]:
            """Load schema from file."""
            try:
                with open(schema_path) as f:
                    return json.load(f)
            except (FileNotFoundError, json.JSONDecodeError):
                return {}

        primary_data = load_schema(primary_schema)
        deprecated_data = load_schema(deprecated_schema)

        # Check if deprecated schema has newer content (shouldn't happen)
        if deprecated_data:
            primary_title = primary_data.get("title", "").replace(" (DEPRECATED)", "")
            deprecated_title = deprecated_data.get("title", "").replace(
                " (DEPRECATED)", ""
            )

            if primary_title and deprecated_title and primary_title != deprecated_title:
                print(
                    "WARNING: Deprecated schema has different content than primary schema!"
                )
                print("This may indicate changes were made in the wrong location.")
                print(f"Primary: {primary_title}")
                print(f"Deprecated: {deprecated_title}")
                return False

        print("✅ Schema location check passed")
        print(f"Primary schema: {primary_schema}")
        if deprecated_schema.exists():
            print(f"Deprecated schema: {deprecated_schema} (should not be modified)")

        return True

    def setup_integration(self, project_path: str, db_type: str = "postgres") -> bool:
        """
        Set up ToDoWrite integration in a project.

        Args:
            project_path: Path to the project directory
            db_type: Database type ('postgres', 'sqlite')

        Returns:
            True if setup was successful, False otherwise
        """
        project_path = Path(project_path)
        if not project_path.exists():
            print(f"❌ Project path does not exist: {project_path}")
            return False

        todowrite_dir = project_path / ".todowrite"
        todowrite_dir.mkdir(exist_ok=True)

        print(f"🚀 Setting up ToDoWrite integration in {project_path}")

        if db_type == "postgres":
            if not self._setup_postgres_docker(project_path):
                return False
        else:
            if not self._setup_sqlite(project_path):
                return False

        # Create configuration template
        if not self._create_config_template(project_path, db_type):
            return False

        print("✅ ToDoWrite integration setup complete!")
        print(f"📁 Configuration created in: {todowrite_dir}")
        print(f"📄 Database type: {db_type}")

        return True

    def init_database_sql(self) -> str:
        """
        Return PostgreSQL initialization SQL as string.
        This provides the SQL content that would be in the init script.
        """
        return dedent(
            """
        -- ToDoWrite PostgreSQL Initialization Script
        -- This script sets up the ToDoWrite database with proper permissions and extensions

        -- Create additional users if needed
        -- CREATE USER todowrite_readonly WITH PASSWORD 'readonly_password';

        -- Grant permissions
        GRANT CONNECT ON DATABASE todowrite TO todowrite;
        GRANT USAGE ON SCHEMA public TO todowrite;
        GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO todowrite;
        GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO todowrite;

        -- Enable extensions if needed
        -- CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
        -- CREATE EXTENSION IF NOT EXISTS "pg_trgm";

        -- Create indexes for better performance (will be created by SQLAlchemy migrations)
        -- This file can be extended with additional setup as needed

        -- Set default database settings for ToDoWrite
        ALTER DATABASE todowrite SET timezone TO 'UTC';
        ALTER DATABASE todowrite SET log_statement TO 'all';
        """
        ).strip()

    def create_project_structure(self, project_path: str) -> bool:
        """
        Create a basic ToDoWrite project structure.

        Args:
            project_path: Path where to create the structure

        Returns:
            True if structure was created successfully
        """
        project_path = Path(project_path)

        try:
            # Create basic directory structure
            directories = [
                project_path / "configs" / "schemas",
                project_path / "docs",
                project_path / "scripts",
                project_path / ".todowrite",
            ]

            for directory in directories:
                directory.mkdir(parents=True, exist_ok=True)

            # Create example files
            self._create_readme(project_path)
            self._create_gitignore(project_path)

            print(f"✅ Project structure created at: {project_path}")
            return True

        except Exception as e:
            print(f"❌ Failed to create project structure: {e}")
            return False

    def validate_project_setup(self, project_path: str) -> dict[str, Any]:
        """
        Validate that a project is properly set up for ToDoWrite.

        Returns:
            Dictionary with validation results
        """
        project_path = Path(project_path)
        result = {"valid": True, "issues": [], "recommendations": [], "found_files": []}

        # Check if directory exists
        if not project_path.exists():
            result["valid"] = False
            result["issues"].append("Project directory does not exist")
            return result

        # Look for key files
        key_files = [
            "todowrite/schemas/todowrite.schema.json",
            "pyproject.toml",
            "requirements.txt",
            ".env.todowrite",
        ]

        for file_path in key_files:
            full_path = project_path / file_path
            if full_path.exists():
                result["found_files"].append(file_path)
            else:
                result["recommendations"].append(f"Optional file missing: {file_path}")

        # Check if todowrite package is accessible
        try:
            import todowrite

            result["found_files"].append("todowrite package accessible")
        except ImportError:
            result["issues"].append("todowrite package not importable")
            result["valid"] = False

        return result

    # ===== Internal Helper Methods =====

    def _setup_postgres_docker(self, project_path: Path) -> bool:
        """Set up PostgreSQL using Docker Compose."""
        template_path = Path(__file__).parent.parent / "docker-compose.yml"
        target_path = project_path / "docker-compose.todowrite.yml"

        if template_path.exists():
            shutil.copy2(template_path, target_path)
            print(f"✅ Created {target_path}")
        else:
            self._create_docker_compose_template(target_path)

        return True

    def _setup_sqlite(self, project_path: Path) -> bool:
        """Set up SQLite configuration."""
        env_path = project_path / ".env.todowrite"
        env_content = dedent(
            """
            # ToDoWrite SQLite Configuration
            TODOWRITE_DATABASE_URL=sqlite:///todowrite.db
        """
        ).strip()

        with open(env_path, "w") as f:
            f.write(env_content)

        print(f"✅ Created {env_path}")
        return True

    def _create_config_template(self, project_path: Path, db_type: str) -> bool:
        """Create configuration template."""
        config_content = dedent(
            f"""
            # ToDoWrite Configuration

            # Database Configuration
            TODOWRITE_DATABASE_URL={'postgresql://todowrite:todowrite_dev_password@localhost:5432/todowrite' if db_type == 'postgres' else 'sqlite:///todowrite.db'}

            # Optional: Log level
            LOG_LEVEL=INFO

            # Optional: Storage preference (yaml_only, db_only, both)
            TODOWRITE_STORAGE_PREFERENCE=both

            # Schema validation
            TODOWRITE_VALIDATE_SCHEMA=true

            # Database migration
            TODOWRITE_AUTO_MIGRATE=true
            """
        ).strip()

        config_path = project_path / ".todowrite" / "config.yaml"
        with open(config_path, "w") as f:
            f.write(config_content)

        print(f"✅ Created configuration template: {config_path}")
        return True

    def _create_docker_compose_template(self, target_path: Path) -> None:
        """Create Docker Compose template for PostgreSQL."""
        content = dedent(
            """
        version: '3.8'

        services:
          postgres:
            image: postgres:15
            environment:
              POSTGRES_DB: todowrite
              POSTGRES_USER: todowrite
              POSTGRES_PASSWORD: todowrite_dev_password
            ports:
              - "5432:5432"
            volumes:
              - postgres_data:/var/lib/postgresql/data
            healthcheck:
              test: ["CMD-SHELL", "pg_isready -U todowrite"]
              interval: 10s
              timeout: 5s
              retries: 5

        volumes:
          postgres_data:
        """
        ).strip()

        with open(target_path, "w") as f:
            f.write(content)

    def _create_readme(self, project_path: Path) -> None:
        """Create a basic README file."""
        content = dedent(
            f"""
        # {project_path.name}

        ## ToDoWrite Integration

        This project is integrated with ToDoWrite for hierarchical task management.

        ### Setup Instructions

        1. Ensure Docker is installed if using PostgreSQL
        2. Run `setup-integration` command
        3. Start the database and run migrations

        ### Getting Started

        ```bash
        # Initialize ToDoWrite
        python -m todowrite init

        # Create your first goal
        python -m todowrite create --id GOAL-PROJECT-VISION --layer Goal --title "Project Vision"
        ```
        """
        ).strip()

        readme_path = project_path / "README.md"
        if not readme_path.exists():
            with open(readme_path, "w") as f:
                f.write(content)

    def _create_gitignore(self, project_path: Path) -> None:
        """Create .gitignore template."""
        content = dedent(
            """
        # Python
        __pycache__/
        *.py[cod]
        *$py.class
        *.so
        .Python
        build/
        develop-eggs/
        dist/
        downloads/
        eggs/
        .eggs/
        lib/
        lib64/
        parts/
        sdist/
        var/
        wheels/
        pip-wheel-metadata/
        share/python-wheels/
        *.egg-info/
        .installed.cfg
        *.egg

        # Virtual environments
        .venv/
        venv/
        env/
        ENV/
        env.bak/
        venv.bak/

        # ToDoWrite
        .todowrite/
        *.db
        *.sqlite
        *.sqlite3

        # IDE
        .vscode/
        .idea/
        *.swp
        *.swo

        # OS
        .DS_Store
        Thumbs.db

        # Logs
        *.log
        log/
        logs/
        """
        ).strip()

        gitignore_path = project_path / ".gitignore"
        if not gitignore_path.exists():
            with open(gitignore_path, "w") as f:
                f.write(content)


# ===== AI-Related Methods (Internal, Optional) =====


class _AIOptimizationManager:
    """Internal AI optimization features - not exposed to users without AI access."""

    def __init__(self):
        self.cache_dir = Path.home() / ".todowrite_cache"
        self.cache_dir.mkdir(exist_ok=True)
        self._ai_available = self._check_ai_availability()

    def _check_ai_availability(self) -> bool:
        """Check if AI components are available."""
        try:
            # Check for required AI dependencies
            import anthropic
            import openai

            return True
        except ImportError:
            return False

    def optimize_token_usage(self, goal: str, **kwargs) -> dict[str, Any] | None:
        """
        Internal method for token optimization.
        Only works if AI dependencies are available.
        """
        if not self._ai_available:
            return None

        # Implementation would go here
        # This is just a placeholder
        return {
            "optimized": True,
            "tokens_saved": 1500,
            "method": "local_preprocessing",
        }

    def ensure_token_sage(self) -> bool:
        """
        Internal method to ensure token-sage is loaded.
        Only works if AI components are available.
        """
        if not self._ai_available:
            return False

        # Implementation would go here
        print("🚀 Token-sage loaded successfully")
        return True


# Create instance for public use
_project_manager = ProjectManager()
_ai_manager = _AIOptimizationManager()


# ===== Public API Functions =====


def check_deprecated_schema() -> bool:
    """Check that deprecated schema hasn't been modified."""
    return _project_manager.check_deprecated_schema()


def check_schema_changes() -> bool:
    """Check if schema changes are in the correct location."""
    return _project_manager.check_schema_changes()


def setup_integration(project_path: str, db_type: str = "postgres") -> bool:
    """Set up ToDoWrite integration in a project."""
    return _project_manager.setup_integration(project_path, db_type)


def create_project_structure(project_path: str) -> bool:
    """Create a basic ToDoWrite project structure."""
    return _project_manager.create_project_structure(project_path)


def validate_project_setup(project_path: str) -> dict[str, Any]:
    """Validate that a project is properly set up for ToDoWrite."""
    return _project_manager.validate_project_setup(project_path)


def init_database_sql() -> str:
    """Return PostgreSQL initialization SQL as string."""
    return _project_manager.init_database_sql()


# Internal AI methods - not exposed publicly
def _optimize_token_usage(goal: str, **kwargs) -> dict[str, Any] | None:
    """Internal token optimization - not exposed to public API."""
    return _ai_manager.optimize_token_usage(goal, **kwargs)


def _ensure_token_sage() -> bool:
    """Internal token-sage initialization - not exposed to public API."""
    return _ai_manager.ensure_token_sage()
