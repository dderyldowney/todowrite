#!/usr/bin/env python3
"""
ToDoWrite Integration Setup Script

This script helps projects integrate ToDoWrite with database-first configuration.
It can set up PostgreSQL (via Docker), SQLite3, or provide configuration templates.
"""

import argparse
import shutil
import sys
from pathlib import Path
from textwrap import dedent


class ToDoWriteIntegration:
    """Helper class to set up ToDoWrite integration in projects."""

    def __init__(self, project_path: Path):
        self.project_path = project_path
        self.todowrite_dir = project_path / ".todowrite"

    def setup_postgres_docker(self) -> None:
        """Set up PostgreSQL using Docker Compose."""
        print("🐳 Setting up PostgreSQL with Docker...")

        # Copy docker-compose.yml template
        template_path = Path(__file__).parent.parent / "docker-compose.yml"
        target_path = self.project_path / "docker-compose.todowrite.yml"

        if template_path.exists():
            shutil.copy2(template_path, target_path)
            print(f"✅ Created {target_path}")
        else:
            self.create_docker_compose_template(target_path)

        # Create .env template
        env_path = self.project_path / ".env.todowrite"
        env_content = dedent(
            """
            # ToDoWrite PostgreSQL Configuration
            TODOWRITE_DATABASE_URL=postgresql://todowrite:todowrite_dev_password@localhost:5432/todowrite

            # Alternative configurations:
            # TODOWRITE_DATABASE_URL=sqlite:///todowrite.db  # SQLite fallback
            # TODOWRITE_DATABASE_URL=postgresql://user:pass@prod-host:5432/todowrite  # Production
        """
        ).strip()

        with open(env_path, "w") as f:
            f.write(env_content)
        print(f"✅ Created {env_path}")

        print("\n📋 Next steps:")
        print("1. Run: docker-compose -f docker-compose.todowrite.yml up -d")
        print("2. Set environment: export $(cat .env.todowrite | xargs)")
        print("3. Initialize database: python -m todowrite init")

    def setup_sqlite(self) -> None:
        """Set up SQLite3 configuration."""
        print("🗄️  Setting up SQLite3...")

        env_path = self.project_path / ".env.todowrite"
        env_content = dedent(
            """
            # ToDoWrite SQLite Configuration
            TODOWRITE_DATABASE_URL=sqlite:///todowrite.db

            # Alternative configurations:
            # TODOWRITE_DATABASE_URL=sqlite:///./data/todowrite.db  # Custom path
            # TODOWRITE_DATABASE_URL=sqlite:///:memory:  # In-memory (testing)
        """
        ).strip()

        with open(env_path, "w") as f:
            f.write(env_content)
        print(f"✅ Created {env_path}")

        print("\n📋 Next steps:")
        print("1. Set environment: export $(cat .env.todowrite | xargs)")
        print("2. Initialize database: python -m todowrite init")

    def create_docker_compose_template(self, target_path: Path) -> None:
        """Create a Docker Compose template."""
        content = dedent(
            """
            version: '3.8'

            services:
              postgres:
                image: postgres:16-alpine
                container_name: todowrite-postgres
                environment:
                  POSTGRES_DB: todowrite
                  POSTGRES_USER: todowrite
                  POSTGRES_PASSWORD: todowrite_dev_password
                ports:
                  - "5432:5432"
                volumes:
                  - postgres_data:/var/lib/postgresql/data
                healthcheck:
                  test: ["CMD-SHELL", "pg_isready -U todowrite -d todowrite"]
                  interval: 10s
                  timeout: 5s
                  retries: 5

            volumes:
              postgres_data:
        """
        ).strip()

        with open(target_path, "w") as f:
            f.write(content)

    def create_makefile_integration(self) -> None:
        """Create Makefile targets for ToDoWrite."""
        makefile_path = self.project_path / "Makefile.todowrite"
        content = dedent(
            """
            # ToDoWrite Integration Makefile
            # Include this in your main Makefile with: include Makefile.todowrite

            .PHONY: tw-setup tw-start tw-stop tw-import tw-export tw-init tw-validate

            # Setup ToDoWrite database
            tw-setup:
            \t@echo "🚀 Setting up ToDoWrite..."
            \t@python -m todowrite init
            \t@python -m todowrite import-yaml

            # Start PostgreSQL (if using Docker)
            tw-start:
            \t@echo "🐳 Starting ToDoWrite PostgreSQL..."
            \t@docker-compose -f docker-compose.todowrite.yml up -d

            # Stop PostgreSQL
            tw-stop:
            \t@echo "🛑 Stopping ToDoWrite PostgreSQL..."
            \t@docker-compose -f docker-compose.todowrite.yml down

            # Import existing YAML files
            tw-import:
            \t@echo "📥 Importing YAML files to database..."
            \t@python -m todowrite import-yaml

            # Export database to YAML
            tw-export:
            \t@echo "📤 Exporting database to YAML..."
            \t@python -m todowrite export-yaml

            # Initialize database
            tw-init:
            \t@echo "🗄️ Initializing ToDoWrite database..."
            \t@python -m todowrite init

            # Validate ToDoWrite structure
            tw-validate:
            \t@echo "✅ Validating ToDoWrite structure..."
            \t@python -m todowrite todowrite validate-plan
        """
        ).strip()

        with open(makefile_path, "w") as f:
            f.write(content)
        print(f"✅ Created {makefile_path}")

    def show_status(self) -> None:
        """Show current ToDoWrite integration status."""
        print("📊 ToDoWrite Integration Status:")
        print("-" * 40)

        # Check for configuration files
        files_to_check = [
            ".env.todowrite",
            "docker-compose.todowrite.yml",
            "Makefile.todowrite",
        ]

        for file_name in files_to_check:
            file_path = self.project_path / file_name
            status = "✅ Found" if file_path.exists() else "❌ Missing"
            print(f"{status}: {file_name}")

        # Check database connectivity
        try:
            import subprocess

            result = subprocess.run(
                [
                    sys.executable,
                    "-c",
                    "from todowrite.app import ToDoWrite; ToDoWrite().init_database()",
                ],
                capture_output=True,
                text=True,
            )
            if result.returncode == 0:
                print("✅ Database: Connected")
            else:
                print("❌ Database: Connection failed")
        except Exception:
            print("❌ Database: Cannot test connection")


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description="ToDoWrite Integration Setup")
    parser.add_argument(
        "command",
        choices=["postgres", "sqlite", "makefile", "status"],
        help="Setup command to run",
    )
    parser.add_argument(
        "--project-path",
        type=Path,
        default=Path.cwd(),
        help="Project directory path (default: current directory)",
    )

    args = parser.parse_args()

    integration = ToDoWriteIntegration(args.project_path)

    if args.command == "postgres":
        integration.setup_postgres_docker()
    elif args.command == "sqlite":
        integration.setup_sqlite()
    elif args.command == "makefile":
        integration.create_makefile_integration()
    elif args.command == "status":
        integration.show_status()


if __name__ == "__main__":
    main()
