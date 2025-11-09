"""
Pytest configuration for todowrite_web package.
"""

from __future__ import annotations

import os
from pathlib import Path
from typing import TYPE_CHECKING

import pytest
from fastapi.testclient import TestClient
from httpx import AsyncClient

if TYPE_CHECKING:
    from fastapi import FastAPI

# Add the src directory to Python path for testing
SRC_DIR = Path(__file__).parent.parent / "src"
os.environ["PYTHONPATH"] = str(SRC_DIR) + ":" + os.environ.get("PYTHONPATH", "")


@pytest.fixture(scope="session")
def test_database_url() -> str:
    """Provide test database URL."""
    return "sqlite:///./test_todowrite.db"


@pytest.fixture
def test_app() -> FastAPI:
    """Create FastAPI test application."""
    from todowrite_web.main import app

    return app


@pytest.fixture
def client(test_app: FastAPI) -> TestClient:
    """Create test client."""
    return TestClient(test_app)


@pytest.fixture
async def async_client(test_app: FastAPI) -> AsyncClient:
    """Create async test client."""
    async with AsyncClient(app=test_app, base_url="http://test") as ac:
        yield ac


@pytest.fixture
def sample_goal_data() -> dict[str, str]:
    """Sample goal data for testing."""
    return {
        "title": "Test Goal",
        "description": "A test goal for unit testing",
        "layer": "Goal",
    }


@pytest.fixture
def sample_task_data() -> dict[str, str]:
    """Sample task data for testing."""
    return {
        "title": "Test Task",
        "description": "A test task for unit testing",
        "layer": "Task",
        "status": "planned",
    }
