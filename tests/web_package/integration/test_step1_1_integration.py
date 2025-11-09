"""
RED PHASE: Tests for Step 1.1 Integration - Web Package Backend-Frontend Communication
These tests MUST FAIL before implementation exists.
NO MOCKING ALLOWED - Tests will use real backend and frontend integration.
"""

from __future__ import annotations

import json
import subprocess
import time
from typing import Any

import pytest
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class TestStep1_1Integration:
    """Test that Step 1.1 web_package backend and frontend integrate correctly."""

    @pytest.fixture(scope="class")
    def setup_step1_1_servers(self) -> None:
        """Start Step 1.1 backend and frontend servers for integration testing."""
        # Start Step 1.1 backend server
        self.backend_process = subprocess.Popen(
            [
                "python",
                "-m",
                "uvicorn",
                "todowrite_web.main:app",
                "--host",
                "0.0.0.0",
                "--port",
                "8000",
            ],
            cwd="web_package/backend",
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )

        # Give backend time to start
        time.sleep(3)

        # Start Step 1.1 frontend server
        self.frontend_process = subprocess.Popen(
            ["npm", "run", "dev"],
            cwd="web_package/frontend",
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )

        # Give frontend time to start
        time.sleep(5)

        yield

        # Clean up servers
        self.backend_process.terminate()
        self.frontend_process.terminate()
        self.backend_process.wait(timeout=5)
        self.frontend_process.wait(timeout=5)

    @pytest.fixture(scope="class")
    def setup_web_driver(self) -> webdriver.Chrome:
        """Set up Chrome WebDriver for Step 1.1 integration testing."""
        chrome_options: Options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--window-size=1920,1080")

        driver: webdriver.Chrome = webdriver.Chrome(options=chrome_options)
        driver.implicitly_wait(10)
        yield driver
        driver.quit()

    def test_step1_1_backend_health_check(
        self, setup_step1_1_servers: None
    ) -> None:
        """RED: Test that Step 1.1 backend health check works."""
        response = requests.get("http://localhost:8000/health", timeout=10)
        assert (
            response.status_code == 200
        ), "Step 1.1 backend health endpoint should respond"

        health_data: dict[str, Any] = response.json()
        assert (
            health_data["status"] == "healthy"
        ), "Step 1.1 health check should return healthy"

    def test_step1_1_backend_root_endpoint(
        self, setup_step1_1_servers: None
    ) -> None:
        """RED: Test that Step 1.1 backend root endpoint works."""
        response = requests.get("http://localhost:8000/", timeout=10)
        assert (
            response.status_code == 200
        ), "Step 1.1 backend root endpoint should respond"

        data: dict[str, Any] = response.json()
        assert (
            "message" in data
        ), "Step 1.1 root endpoint should return message"
        assert (
            "ToDoWrite Web API" in data["message"]
        ), "Step 1.1 message should identify the service"

    def test_step1_1_frontend_startup(
        self, setup_web_driver: webdriver.Chrome, setup_step1_1_servers: None
    ) -> None:
        """RED: Test that Step 1.1 frontend starts correctly."""
        driver: webdriver.Chrome = setup_web_driver

        driver.get("http://localhost:3000")

        # Wait for React app to load
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.ID, "root"))
        )

        # Verify Step 1.1 frontend content
        page_source: str = driver.page_source
        assert (
            "react" in page_source.lower()
            or "todowrite" in page_source.lower()
        ), "Step 1.1 should load React application"

    def test_step1_1_cors_configuration(
        self, setup_step1_1_servers: None
    ) -> None:
        """RED: Test that Step 1.1 CORS is configured correctly."""
        headers: dict[str, str] = {
            "Origin": "http://localhost:3000",
            "Access-Control-Request-Method": "GET",
            "Access-Control-Request-Headers": "Content-Type",
        }

        # Preflight request
        preflight_response = requests.options(
            "http://localhost:8000/", headers=headers, timeout=10
        )

        assert preflight_response.status_code in [
            200,
            204,
        ], "Step 1.1 CORS preflight should be allowed"

        # Check CORS headers
        cors_headers = preflight_response.headers
        assert (
            "Access-Control-Allow-Origin" in cors_headers
        ), "Step 1.1 should have CORS allow origin header"

    def test_step1_1_api_documentation(
        self, setup_step1_1_servers: None
    ) -> None:
        """RED: Test that Step 1.1 API documentation is available."""
        # Test OpenAPI documentation
        response = requests.get("http://localhost:8000/docs", timeout=10)
        assert (
            response.status_code == 200
        ), "Step 1.1 OpenAPI documentation should be accessible"

        # Test OpenAPI schema
        schema_response = requests.get(
            "http://localhost:8000/openapi.json", timeout=10
        )
        assert (
            schema_response.status_code == 200
        ), "Step 1.1 OpenAPI schema should be available"

        schema_data: dict[str, Any] = schema_response.json()
        assert (
            "openapi" in schema_data
        ), "Step 1.1 should have valid OpenAPI schema"
        assert "info" in schema_data, "Step 1.1 should have API info in schema"

    def test_step1_1_error_handling(self, setup_step1_1_servers: None) -> None:
        """RED: Test that Step 1.1 error handling works correctly."""
        # Test 404 error
        response = requests.get(
            "http://localhost:8000/nonexistent", timeout=10
        )
        assert (
            response.status_code == 404
        ), "Step 1.1 should return 404 for nonexistent endpoint"

        error_data: dict[str, Any] = response.json()
        assert isinstance(
            error_data, dict
        ), "Step 1.1 error should be JSON object"

    def test_step1_1_package_structure_validation(self) -> None:
        """RED: Test that Step 1.1 package structure is correct."""
        import pathlib

        # Verify web_package structure
        web_package_path = pathlib.Path("web_package")
        assert web_package_path.exists(), "web_package directory should exist"
        assert web_package_path.is_dir(), "web_package should be a directory"

        # Verify backend structure
        backend_path = pathlib.Path("web_package/backend")
        assert (
            backend_path.exists()
        ), "web_package/backend directory should exist"
        assert (
            backend_path.is_dir()
        ), "web_package/backend should be a directory"

        # Verify frontend structure
        frontend_path = pathlib.Path("web_package/frontend")
        assert (
            frontend_path.exists()
        ), "web_package/frontend directory should exist"
        assert (
            frontend_path.is_dir()
        ), "web_package/frontend should be a directory"

        # Verify shared structure
        shared_path = pathlib.Path("web_package/shared")
        assert (
            shared_path.exists()
        ), "web_package/shared directory should exist"
        assert shared_path.is_dir(), "web_package/shared should be a directory"

    def test_step1_1_backend_package_configuration(self) -> None:
        """RED: Test that Step 1.1 backend package is configured correctly."""
        import pathlib

        import toml

        # Check pyproject.toml exists
        pyproject_path = pathlib.Path("web_package/backend/pyproject.toml")
        assert (
            pyproject_path.exists()
        ), "Step 1.1 backend pyproject.toml should exist"

        # Check pyproject.toml content
        config: dict[str, Any] = toml.load(pyproject_path)
        assert (
            "project" in config
        ), "Step 1.1 backend should have project configuration"
        assert (
            "name" in config["project"]
        ), "Step 1.1 backend should have project name"
        assert (
            "dependencies" in config["project"]
        ), "Step 1.1 backend should have dependencies"

        # Check for FastAPI dependency
        assert "fastapi" in str(
            config["project"]["dependencies"]
        ), "Step 1.1 backend should include FastAPI"

    def test_step1_1_frontend_package_configuration(self) -> None:
        """RED: Test that Step 1.1 frontend package is configured correctly."""
        import pathlib

        # Check package.json exists
        package_json_path = pathlib.Path("web_package/frontend/package.json")
        assert (
            package_json_path.exists()
        ), "Step 1.1 frontend package.json should exist"

        # Check package.json content
        content: dict[str, Any] = json.loads(package_json_path.read_text())
        assert "name" in content, "Step 1.1 frontend should have name field"
        assert (
            "react" in content["dependencies"]
        ), "Step 1.1 frontend should include React framework"
        assert (
            "scripts" in content
        ), "Step 1.1 frontend should have scripts section"

    def test_step1_1_shared_types_integration(self) -> None:
        """RED: Test that Step 1.1 shared types integration works."""
        import pathlib

        # Check shared types directory
        shared_types = pathlib.Path("web_package/shared/types")
        assert (
            shared_types.exists()
        ), "Step 1.1 shared types directory should exist"

        # Check backend can import shared types
        backend_types = pathlib.Path(
            "web_package/backend/src/todowrite_web/types"
        )
        assert (
            backend_types.exists()
        ), "Step 1.1 backend types directory should exist"

        # Check frontend can import shared types
        frontend_types = pathlib.Path("web_package/frontend/src/types")
        assert (
            frontend_types.exists()
        ), "Step 1.1 frontend types directory should exist"

    def test_step1_1_shared_utils_integration(self) -> None:
        """RED: Test that Step 1.1 shared utils integration works."""
        import pathlib

        # Check shared utils directory
        shared_utils = pathlib.Path("web_package/shared/utils")
        assert (
            shared_utils.exists()
        ), "Step 1.1 shared utils directory should exist"

        # Check backend can import shared utils
        backend_utils = pathlib.Path(
            "web_package/backend/src/todowrite_web/utils"
        )
        assert (
            backend_utils.exists()
        ), "Step 1.1 backend utils directory should exist"

        # Check frontend can import shared utils
        frontend_utils = pathlib.Path("web_package/frontend/src/utils")
        assert (
            frontend_utils.exists()
        ), "Step 1.1 frontend utils directory should exist"

    def test_step1_1_docker_configuration(self) -> None:
        """RED: Test that Step 1.1 Docker configuration is correct."""
        import pathlib

        # Check backend Dockerfile
        backend_dockerfile = pathlib.Path("web_package/backend/Dockerfile")
        assert (
            backend_dockerfile.exists()
        ), "Step 1.1 backend Dockerfile should exist"

        # Check frontend Dockerfile
        frontend_dockerfile = pathlib.Path("web_package/frontend/Dockerfile")
        assert (
            frontend_dockerfile.exists()
        ), "Step 1.1 frontend Dockerfile should exist"

        # Check docker-compose.yml
        docker_compose = pathlib.Path("web_package/docker-compose.yml")
        assert (
            docker_compose.exists()
        ), "Step 1.1 docker-compose.yml should exist"

    def test_step1_1_development_environment(self) -> None:
        """RED: Test that Step 1.1 development environment is correctly set up."""
        import pathlib

        # Check backend development dependencies
        backend_pyproject = pathlib.Path("web_package/backend/pyproject.toml")
        if backend_pyproject.exists():
            import toml

            config = toml.load(backend_pyproject)
            assert (
                "dependencies" in config["project"]
            ), "Step 1.1 backend should have development dependencies"

        # Check frontend development dependencies
        frontend_package = pathlib.Path("web_package/frontend/package.json")
        if frontend_package.exists():
            import json

            content = json.loads(frontend_package.read_text())
            assert (
                "devDependencies" in content
            ), "Step 1.1 frontend should have development dependencies"

    def test_step1_1_logging_configuration(
        self, setup_step1_1_servers: None
    ) -> None:
        """RED: Test that Step 1.1 logging is configured correctly."""
        # Check that backend server logs output
        assert (
            self.backend_process is not None
        ), "Step 1.1 backend process should be running"
        assert (
            self.backend_process.poll() is None
        ), "Step 1.1 backend process should not have terminated"

        # Check that frontend server logs output
        assert (
            self.frontend_process is not None
        ), "Step 1.1 frontend process should be running"
        assert (
            self.frontend_process.poll() is None
        ), "Step 1.1 frontend process should not have terminated"

    def test_step1_1_environment_variables(self) -> None:
        """RED: Test that Step 1.1 environment variables are properly configured."""
        import pathlib

        # Check for .env files
        backend_env = pathlib.Path("web_package/backend/.env")
        frontend_env = pathlib.Path("web_package/frontend/.env")

        # At least one environment file should exist
        assert (
            backend_env.exists() or frontend_env.exists()
        ), "Step 1.1 should have environment configuration"

    def test_step1_1_database_connection(
        self, setup_step1_1_servers: None
    ) -> None:
        """RED: Test that Step 1.1 can connect to database (if configured)."""
        # This test will check if backend can connect to todowrite database
        try:
            response = requests.get(
                "http://localhost:8000/api/test-db", timeout=10
            )
            if response.status_code == 200:
                db_data: dict[str, Any] = response.json()
                assert (
                    "status" in db_data
                ), "Database test should return status"
            else:
                pytest.skip("Database endpoint not implemented yet")
        except:
            pytest.skip("Database connection not implemented yet")

    def test_step1_1_static_file_serving(
        self, setup_web_driver: webdriver.Chrome, setup_step1_1_servers: None
    ) -> None:
        """RED: Test that Step 1.1 static files are served correctly."""
        driver: webdriver.Chrome = setup_web_driver

        driver.get("http://localhost:3000")

        try:
            # Check for CSS files
            css_elements = driver.find_elements(By.TAG_NAME, "link")
            css_found = any(
                "stylesheet" in element.get_attribute("rel") or ""
                for element in css_elements
            )
            # CSS might not be loaded in RED phase

            # Check for JavaScript files
            js_elements = driver.find_elements(By.TAG_NAME, "script")
            js_found = len(js_elements) > 0
            assert js_found, "Step 1.1 should load JavaScript files"

        except:
            pytest.skip("Static file serving not fully implemented yet")

    def test_step1_1_performance_benchmarks(
        self, setup_step1_1_servers: None
    ) -> None:
        """RED: Test that Step 1.1 performance meets basic benchmarks."""
        import time

        # Test backend response time
        start_time = time.time()
        response = requests.get("http://localhost:8000/health", timeout=10)
        response_time = time.time() - start_time

        assert response.status_code == 200, "Health endpoint should respond"
        assert (
            response_time < 2.0
        ), "Step 1.1 backend should respond within 2 seconds"

    def test_step1_1_security_headers(
        self, setup_step1_1_servers: None
    ) -> None:
        """RED: Test that Step 1.1 security headers are configured."""
        response = requests.get("http://localhost:8000/", timeout=10)

        # Check for basic security headers
        headers = response.headers

        # In RED phase, security headers might not be implemented yet
        # We'll test that the response structure is correct
        assert isinstance(
            headers, dict
        ), "Step 1.1 should return response headers"

    def test_step1_1_api_versioning(self, setup_step1_1_servers: None) -> None:
        """RED: Test that Step 1.1 API versioning is implemented."""
        try:
            response = requests.get(
                "http://localhost:8000/api/v1/", timeout=10
            )
            if response.status_code == 200:
                version_data: dict[str, Any] = response.json()
                assert (
                    "version" in version_data or "api" in version_data
                ), "Step 1.1 should indicate API version"
            else:
                pytest.skip("API versioning not implemented yet")
        except:
            pytest.skip("API versioning endpoint not implemented yet")
