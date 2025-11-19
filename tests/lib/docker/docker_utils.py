"""
Docker Detection and Management Utilities

Provides functionality to detect Docker installation and manage Docker containers
for testing purposes, including PostgreSQL setup for database testing.
"""

from __future__ import annotations

import json
import subprocess
import tempfile
from pathlib import Path
from typing import Any, Dict, Optional
import time

import pytest
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

from todowrite.core.models import Base, Goal, Task, Label, Command


class DockerManager:
    """Manages Docker containers for testing purposes."""

    def __init__(self: "DockerManager") -> None:
        """Initialize Docker manager."""
        self.is_available: bool = self._check_docker_availability()
        self.compose_files: Dict[str, Path] = self._find_compose_files()

    def _check_docker_availability(self: "DockerManager") -> bool:
        """Check if Docker and Docker Compose are available."""
        try:
            # Check Docker daemon
            subprocess.run(
                ["docker", "--version"],
                capture_output=True,
                check=True,
                timeout=10,
            )

            # Check Docker daemon is running
            result = subprocess.run(
                ["docker", "info"],
                capture_output=True,
                check=True,
                timeout=10,
            )

            # Check Docker Compose
            subprocess.run(
                ["docker", "compose", "version"],
                capture_output=True,
                check=True,
                timeout=10,
            )

            return True

        except (subprocess.CalledProcessError, subprocess.TimeoutExpired, FileNotFoundError):
            return False

    def _find_compose_files(self: "DockerManager") -> Dict[str, Path]:
        """Find Docker Compose files in the project."""
        # Navigate from tests/lib/docker/ to tests/ directory
        current_dir = Path(__file__).parent
        tests_dir = current_dir.parent.parent  # Go up two levels: docker/ -> lib/ -> tests/
        compose_files = {}

        # Look for docker-compose files in tests directory
        for compose_file in tests_dir.glob("docker-compose*.yml"):
            compose_files[compose_file.stem] = compose_file

        return compose_files

    def is_docker_available(self: "DockerManager") -> bool:
        """Check if Docker is available and running."""
        return self.is_available

    def start_postgresql_container(
        self: "DockerManager",
        compose_file: str = "docker-compose",
        timeout: int = 60,
    ) -> bool:
        """Start PostgreSQL container using Docker Compose."""
        if not self.is_available or compose_file not in self.compose_files:
            return False

        compose_path = self.compose_files[compose_file]
        compose_dir = compose_path.parent

        try:
            # Start the services
            subprocess.run(
                ["docker", "compose", "-f", str(compose_path), "up", "-d"],
                cwd=compose_dir,
                capture_output=True,
                check=True,
                timeout=30,
            )

            # Wait for PostgreSQL to be ready
            return self._wait_for_postgresql_ready(compose_path, timeout)

        except (subprocess.CalledProcessError, subprocess.TimeoutExpired):
            return False

    def stop_postgresql_container(
        self: "DockerManager",
        compose_file: str = "docker-compose",
    ) -> bool:
        """Stop PostgreSQL container using Docker Compose."""
        if not self.is_available or compose_file not in self.compose_files:
            return False

        compose_path = self.compose_files[compose_file]
        compose_dir = compose_path.parent

        try:
            subprocess.run(
                ["docker", "compose", "-f", str(compose_path), "down"],
                cwd=compose_dir,
                capture_output=True,
                check=True,
                timeout=30,
            )
            return True

        except (subprocess.CalledProcessError, subprocess.TimeoutExpired):
            return False

    def _wait_for_postgresql_ready(
        self: "DockerManager",
        compose_path: Path,
        timeout: int,
    ) -> bool:
        """Wait for PostgreSQL to be ready."""
        start_time = time.time()
        compose_dir = compose_path.parent

        while time.time() - start_time < timeout:
            try:
                # Check container health
                result = subprocess.run(
                    ["docker", "compose", "-f", str(compose_path), "ps", "--format", "json"],
                    cwd=compose_dir,
                    capture_output=True,
                    check=True,
                    timeout=10,
                )

                services_data = json.loads(result.stdout.decode())

                # Handle both single service object and array of services
                services = services_data if isinstance(services_data, list) else [services_data]

                for service in services:
                    if (
                        service.get("Service", "") == "postgres"
                        and service.get("State", "") == "running"
                        and service.get("Health", "") == "healthy"
                    ):
                        return True

            except (subprocess.CalledProcessError, subprocess.TimeoutExpired, json.JSONDecodeError):
                pass

            time.sleep(2)

        return False

    def get_postgresql_connection_url(
        self: "DockerManager",
        database: str = "todowrite",
        username: str = "todowrite",
        password: str = "todowrite_dev_password",
        host: str = "localhost",
        port: int = 5432,
    ) -> Optional[str]:
        """Get PostgreSQL connection URL for running container."""
        if not self.is_available:
            return None

        return f"postgresql://{username}:{password}@{host}:{port}/{database}"

    def cleanup_test_containers(self: "DockerManager") -> None:
        """Clean up any test containers and volumes."""
        if not self.is_available:
            return

        try:
            # Stop and remove containers with todowrite-test label
            subprocess.run(
                [
                    "docker",
                    "ps",
                    "-q",
                    "--filter",
                    "label=todowrite-test",
                ],
                capture_output=True,
                check=True,
                timeout=10,
            )

        except (subprocess.CalledProcessError, subprocess.TimeoutExpired):
            pass


# Global Docker manager instance
docker_manager = DockerManager()


def skip_if_no_docker() -> None:
    """Pytest marker to skip tests if Docker is not available."""
    if not docker_manager.is_docker_available():
        pytest.skip("Docker is not available or not running", allow_module_level=True)


def get_docker_manager() -> DockerManager:
    """Get the global Docker manager instance."""
    return docker_manager


class TestPostgreSQLConfig:
    """Configuration for PostgreSQL testing."""

    DEFAULT_CONFIG = {
        "database": "todowrite",
        "username": "todowrite",
        "password": "todowrite_dev_password",
        "host": "localhost",
        "port": 5432,
    }

    @classmethod
    def get_connection_url(
        cls: type[TestPostgreSQLConfig],
        **overrides: Any,
    ) -> str:
        """Get PostgreSQL connection URL with optional overrides."""
        config = cls.DEFAULT_CONFIG.copy()
        config.update(overrides)

        return (
            f"postgresql://{config['username']}:{config['password']}"
            f"@{config['host']}:{config['port']}/{config['database']}"
        )