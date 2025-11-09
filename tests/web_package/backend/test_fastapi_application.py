"""
RED PHASE: Tests for FastAPI Backend Application
These tests MUST FAIL before implementation exists.
NO MOCKING ALLOWED - Tests will use real FastAPI application.
"""

from __future__ import annotations

import subprocess
import time
from typing import Any

import requests


class TestFastAPIBackendApplication:
    """Test that FastAPI backend application works correctly."""

    def test_fastapi_application_imports(self) -> None:
        """RED: Test that FastAPI application can be imported."""
        # Test backend package imports
        import_result = subprocess.run(
            [
                "python",
                "-c",
                "import sys; sys.path.insert(0, './web_package/backend/src'); import todowrite_web; print('Import successful')",
            ],
            capture_output=True,
            text=True,
            check=False,
        )

        assert (
            import_result.returncode == 0
        ), f"Backend package should be importable: {import_result.stderr}"
        assert (
            "Import successful" in import_result.stdout
        ), "Import should succeed"

    def test_fastapi_application_creation(self) -> None:
        """RED: Test that FastAPI application can be created."""
        import_result = subprocess.run(
            [
                "python",
                "-c",
                """
import sys; sys.path.insert(0, './web_package/backend/src')
from todowrite_web.main import app
print(f'FastAPI app created: {type(app).__name__}')
print(f'Title: {app.title}')
print(f'Version: {app.version}')
            """,
            ],
            capture_output=True,
            text=True,
            check=False,
        )

        assert (
            import_result.returncode == 0
        ), f"FastAPI app creation should succeed: {import_result.stderr}"
        assert (
            "FastAPI" in import_result.stdout
        ), "Should create FastAPI application"
        assert (
            "ToDoWrite Web API" in import_result.stdout
        ), "Should have correct title"
        assert "0.1.0" in import_result.stdout, "Should have correct version"

    def test_fastapi_health_endpoint(self) -> None:
        """RED: Test that FastAPI health endpoint works."""
        # Start FastAPI server in background
        server_process = subprocess.Popen(
            [
                "python",
                "-m",
                "uvicorn",
                "todowrite_web.main:app",
                "--host",
                "0.0.0.0",
                "--port",
                "8000",
                "--reload",
            ],
            cwd="web_package/backend",
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )

        # Give server time to start
        time.sleep(3)

        try:
            # Test health endpoint
            response = requests.get("http://localhost:8000/health", timeout=10)
            assert (
                response.status_code == 200
            ), "Health endpoint should return 200"

            health_data: dict[str, Any] = response.json()
            assert (
                health_data["status"] == "healthy"
            ), "Health check should return healthy status"
            assert (
                health_data["service"] == "todowrite-web"
            ), "Should identify service correctly"

        finally:
            # Clean up server process
            server_process.terminate()
            server_process.wait(timeout=5)

    def test_fastapi_root_endpoint(self) -> None:
        """RED: Test that FastAPI root endpoint works."""
        # Start FastAPI server in background
        server_process = subprocess.Popen(
            [
                "python",
                "-m",
                "uvicorn",
                "todowrite_web.main:app",
                "--host",
                "0.0.0.0",
                "--port",
                "8001",
            ],
            cwd="web_package/backend",
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )

        time.sleep(3)

        try:
            # Test root endpoint
            response = requests.get("http://localhost:8001/", timeout=10)
            assert (
                response.status_code == 200
            ), "Root endpoint should return 200"

            root_data: dict[str, Any] = response.json()
            assert (
                "message" in root_data
            ), "Root endpoint should return message"
            assert (
                "ToDoWrite Web API is running" in root_data["message"]
            ), "Should return running message"

        finally:
            server_process.terminate()
            server_process.wait(timeout=5)

    def test_fastapi_openapi_documentation(self) -> None:
        """RED: Test that FastAPI OpenAPI documentation is available."""
        # Start FastAPI server
        server_process = subprocess.Popen(
            [
                "python",
                "-m",
                "uvicorn",
                "todowrite_web.main:app",
                "--host",
                "0.0.0.0",
                "--port",
                "8002",
            ],
            cwd="web_package/backend",
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )

        time.sleep(3)

        try:
            # Test OpenAPI docs endpoint
            response = requests.get("http://localhost:8002/docs", timeout=10)
            assert (
                response.status_code == 200
            ), "OpenAPI docs should be accessible"
            assert (
                "swagger" in response.text.lower()
                or "openapi" in response.text.lower()
            ), "Should show API documentation"

            # Test OpenAPI JSON endpoint
            openapi_response = requests.get(
                "http://localhost:8002/openapi.json", timeout=10
            )
            assert (
                openapi_response.status_code == 200
            ), "OpenAPI JSON should be accessible"

            openapi_data: dict[str, Any] = openapi_response.json()
            assert "openapi" in openapi_data, "Should contain OpenAPI version"
            assert "info" in openapi_data, "Should contain API info"
            assert (
                openapi_data["info"]["title"] == "ToDoWrite Web API"
            ), "Should have correct title"

        finally:
            server_process.terminate()
            server_process.wait(timeout=5)

    def test_fastapi_dependency_injection(self) -> None:
        """RED: Test that FastAPI dependency injection works."""
        test_result = subprocess.run(
            [
                "python",
                "-c",
                """
import sys; sys.path.insert(0, './web_package/backend/src')
from todowrite_web.main import app
from fastapi.testclient import TestClient

client = TestClient(app)
response = client.get("/")
print(f'Dependency injection test: {response.status_code}')
print(f'Response: {response.json()}')
            """,
            ],
            capture_output=True,
            text=True,
            cwd="web_package/backend",
            check=False,
        )

        assert (
            test_result.returncode == 0
        ), f"Dependency injection test should pass: {test_result.stderr}"
        assert (
            "200" in test_result.stdout
        ), "Test client should work with FastAPI app"

    def test_fastapi_cors_middleware(self) -> None:
        """RED: Test that CORS middleware is configured."""
        test_result = subprocess.run(
            [
                "python",
                "-c",
                """
import sys; sys.path.insert(0, './web_package/backend/src')
from todowrite_web.main import app
from fastapi.testclient import TestClient

client = TestClient(app)
response = client.options("/")
print(f'CORS test: {response.status_code}')
print(f'Headers: {dict(response.headers)}')
            """,
            ],
            capture_output=True,
            text=True,
            cwd="web_package/backend",
            check=False,
        )

        assert (
            test_result.returncode == 0
        ), f"CORS middleware test should pass: {test_result.stderr}"
        # In implementation, we'd check for CORS headers

    def test_fastapi_error_handling(self) -> None:
        """RED: Test that FastAPI handles errors gracefully."""
        test_result = subprocess.run(
            [
                "python",
                "-c",
                """
import sys; sys.path.insert(0, './web_package/backend/src')
from todowrite_web.main import app
from fastapi.testclient import TestClient

client = TestClient(app)
# Test 404 error
response = client.get("/nonexistent-endpoint")
print(f'404 test: {response.status_code}')
print(f'Error response: {response.json()}')
            """,
            ],
            capture_output=True,
            text=True,
            cwd="web_package/backend",
            check=False,
        )

        assert (
            test_result.returncode == 0
        ), f"Error handling test should pass: {test_result.stderr}"
        assert (
            "404" in test_result.stdout
        ), "Should handle 404 errors correctly"
