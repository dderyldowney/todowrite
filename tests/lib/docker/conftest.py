"""
Pytest configuration for Docker-based testing.

Provides fixtures and configuration for running tests with Docker containers,
particularly PostgreSQL for database testing.
"""

from __future__ import annotations

import pytest

try:
    from .docker_utils import docker_manager, skip_if_no_docker
except ImportError:
    # Fallback for when running directly
    import sys
    from pathlib import Path

    # Add the parent directory to path so we can import docker_utils
    parent_dir = Path(__file__).parent.parent.parent
    if str(parent_dir) not in sys.path:
        sys.path.insert(0, str(parent_dir))

    from tests.lib.docker.docker_utils import docker_manager, skip_if_no_docker


def pytest_configure(config: pytest.Config) -> None:
    """Configure pytest with custom markers."""
    config.addinivalue_line(
        "markers",
        "requires_docker: mark test as requiring Docker to be available"
    )


def pytest_collection_modifyitems(config: pytest.Config, items: list[pytest.Item]) -> None:
    """Modify test collection to handle Docker requirements."""
    # Auto-skip tests that require Docker if it's not available
    if not docker_manager.is_docker_available():
        skip_docker = pytest.mark.skip(reason="Docker is not available or not running")
        for item in items:
            if "requires_docker" in item.keywords or "docker" in item.nodeid.lower():
                item.add_marker(skip_docker)


@pytest.fixture(scope="session")
def docker_available() -> bool:
    """Fixture to check if Docker is available."""
    return docker_manager.is_docker_available()


@pytest.fixture(scope="session")
def docker_manager_instance():
    """Fixture providing access to the Docker manager instance."""
    return docker_manager