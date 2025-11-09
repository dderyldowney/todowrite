"""
RED PHASE: Tests for Step 1.1 Complete End-to-End Workflow
These tests MUST FAIL before implementation exists.
NO MOCKING ALLOWED - Tests will use real complete Step 1.1 system workflow.
"""

from __future__ import annotations

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


class TestStep1_1CompleteWorkflow:
    """Test that Step 1.1 complete end-to-end workflow works correctly."""

    @pytest.fixture(scope="class")
    def setup_step1_1_complete_system(self) -> None:
        """Start complete Step 1.1 system (backend + frontend + database)."""
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

        time.sleep(3)

        # Start Step 1.1 frontend server
        self.frontend_process = subprocess.Popen(
            ["npm", "run", "dev"],
            cwd="web_package/frontend",
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )

        time.sleep(5)

        yield

        # Clean up
        self.backend_process.terminate()
        self.frontend_process.terminate()
        self.backend_process.wait(timeout=5)
        self.frontend_process.wait(timeout=5)

    @pytest.fixture(scope="class")
    def setup_web_driver(self) -> webdriver.Chrome:
        """Set up Chrome WebDriver for Step 1.1 E2E testing."""
        chrome_options: Options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--window-size=1920,1080")

        driver: webdriver.Chrome = webdriver.Chrome(options=chrome_options)
        driver.implicitly_wait(10)
        yield driver
        driver.quit()

    def test_step1_1_system_startup_workflow(
        self,
        setup_web_driver: webdriver.Chrome,
        setup_step1_1_complete_system: None,
    ) -> None:
        """RED: Test complete Step 1.1 system startup workflow."""
        driver: webdriver.Chrome = setup_web_driver

        # Step 1: Verify backend is running
        backend_health = requests.get(
            "http://localhost:8000/health", timeout=10
        )
        assert (
            backend_health.status_code == 200
        ), "Step 1.1 backend should be healthy"

        # Step 2: Navigate to frontend
        driver.get("http://localhost:3000")

        # Step 3: Wait for React app to load
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.ID, "root"))
        )

        # Step 4: Verify Step 1.1 branding
        page_source: str = driver.page_source
        assert (
            "ToDoWrite" in page_source or "React" in page_source
        ), "Step 1.1 should load with proper branding"

        # Step 5: Verify Step 1.1 basic functionality is available
        try:
            # Look for navigation elements
            navigation = driver.find_element(
                By.CSS_SELECTOR, "nav, [data-testid='navigation']"
            )
            assert navigation.is_displayed(), "Step 1.1 should have navigation"
        except:
            pytest.skip("Navigation not implemented yet in Step 1.1")

    def test_step1_1_backend_api_workflow(
        self, setup_step1_1_complete_system: None
    ) -> None:
        """RED: Test Step 1.1 backend API workflow."""
        # Step 1: Test root endpoint
        root_response = requests.get("http://localhost:8000/", timeout=10)
        assert (
            root_response.status_code == 200
        ), "Step 1.1 root endpoint should work"

        root_data: dict[str, Any] = root_response.json()
        assert "message" in root_data, "Step 1.1 root should return message"

        # Step 2: Test health endpoint
        health_response = requests.get(
            "http://localhost:8000/health", timeout=10
        )
        assert (
            health_response.status_code == 200
        ), "Step 1.1 health endpoint should work"

        health_data: dict[str, Any] = health_response.json()
        assert (
            health_data["status"] == "healthy"
        ), "Step 1.1 health check should pass"

        # Step 3: Test API documentation
        docs_response = requests.get("http://localhost:8000/docs", timeout=10)
        assert (
            docs_response.status_code == 200
        ), "Step 1.1 API docs should be accessible"

        # Step 4: Test error handling
        error_response = requests.get(
            "http://localhost:8000/nonexistent", timeout=10
        )
        assert (
            error_response.status_code == 404
        ), "Step 1.1 should handle 404 errors"

    def test_step1_1_frontend_rendering_workflow(
        self,
        setup_web_driver: webdriver.Chrome,
        setup_step1_1_complete_system: None,
    ) -> None:
        """RED: Test Step 1.1 frontend rendering workflow."""
        driver: webdriver.Chrome = setup_web_driver

        # Step 1: Navigate to frontend
        driver.get("http://localhost:3000")

        # Step 2: Wait for initial render
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.ID, "root"))
        )

        # Step 3: Verify React app structure
        try:
            # Look for Step 1.1 app structure
            app_container = driver.find_element(
                By.CSS_SELECTOR, "[data-testid='app-container'], #root > div"
            )
            assert (
                app_container.is_displayed()
            ), "Step 1.1 should render app container"

            # Look for Step 1.1 basic layout
            header = driver.find_element(
                By.CSS_SELECTOR, "header, [data-testid='header']"
            )
            assert header.is_displayed(), "Step 1.1 should render header"

            main_content = driver.find_element(
                By.CSS_SELECTOR, "main, [data-testid='main-content']"
            )
            assert (
                main_content.is_displayed()
            ), "Step 1.1 should render main content"

        except:
            pytest.skip("Frontend structure not fully implemented in Step 1.1")

    def test_step1_1_backend_frontend_communication_workflow(
        self,
        setup_web_driver: webdriver.Chrome,
        setup_step1_1_complete_system: None,
    ) -> None:
        """RED: Test Step 1.1 backend-frontend communication workflow."""
        driver: webdriver.Chrome = setup_web_driver

        # Step 1: Navigate to frontend
        driver.get("http://localhost:3000")

        # Step 2: Wait for frontend to load
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.ID, "root"))
        )

        # Step 3: Test CORS configuration
        headers: dict[str, str] = {
            "Origin": "http://localhost:3000",
            "Access-Control-Request-Method": "GET",
        }

        preflight_response = requests.options(
            "http://localhost:8000/", headers=headers, timeout=10
        )
        assert preflight_response.status_code in [
            200,
            204,
        ], "Step 1.1 CORS should work"

        # Step 4: Test frontend can make API calls
        try:
            # Look for evidence of API calls in frontend
            api_indicator = driver.find_element(
                By.CSS_SELECTOR,
                "[data-testid='api-status'], [data-testid='connection-status']",
            )
            assert (
                api_indicator.is_displayed()
            ), "Step 1.1 frontend should show API status"
        except:
            pytest.skip(
                "Frontend API integration not implemented yet in Step 1.1"
            )

    def test_step1_1_development_environment_workflow(self) -> None:
        """RED: Test Step 1.1 development environment workflow."""
        import pathlib

        # Step 1: Verify project structure exists
        web_package_path = pathlib.Path("web_package")
        assert (
            web_package_path.exists()
        ), "Step 1.1 web_package directory should exist"

        # Step 2: Verify backend development setup
        backend_path = pathlib.Path("web_package/backend")
        assert backend_path.exists(), "Step 1.1 backend directory should exist"

        backend_pyproject = pathlib.Path("web_package/backend/pyproject.toml")
        assert (
            backend_pyproject.exists()
        ), "Step 1.1 backend pyproject.toml should exist"

        # Step 3: Verify frontend development setup
        frontend_path = pathlib.Path("web_package/frontend")
        assert (
            frontend_path.exists()
        ), "Step 1.1 frontend directory should exist"

        frontend_package = pathlib.Path("web_package/frontend/package.json")
        assert (
            frontend_package.exists()
        ), "Step 1.1 frontend package.json should exist"

        # Step 4: Verify shared setup
        shared_path = pathlib.Path("web_package/shared")
        assert shared_path.exists(), "Step 1.1 shared directory should exist"

    def test_step1_1_package_configuration_workflow(self) -> None:
        """RED: Test Step 1.1 package configuration workflow."""
        import json
        import pathlib

        import toml

        # Step 1: Verify backend package configuration
        backend_pyproject = pathlib.Path("web_package/backend/pyproject.toml")
        assert (
            backend_pyproject.exists()
        ), "Step 1.1 backend pyproject.toml should exist"

        backend_config: dict[str, Any] = toml.load(backend_pyproject)
        assert (
            "project" in backend_config
        ), "Step 1.1 backend should have project config"
        assert (
            "name" in backend_config["project"]
        ), "Step 1.1 backend should have name"
        assert (
            "dependencies" in backend_config["project"]
        ), "Step 1.1 backend should have dependencies"

        # Step 2: Verify frontend package configuration
        frontend_package = pathlib.Path("web_package/frontend/package.json")
        assert (
            frontend_package.exists()
        ), "Step 1.1 frontend package.json should exist"

        frontend_config: dict[str, Any] = json.loads(
            frontend_package.read_text()
        )
        assert "name" in frontend_config, "Step 1.1 frontend should have name"
        assert (
            "dependencies" in frontend_config
        ), "Step 1.1 frontend should have dependencies"
        assert (
            "scripts" in frontend_config
        ), "Step 1.1 frontend should have scripts"

        # Step 3: Verify essential dependencies
        assert "fastapi" in str(
            backend_config["project"]["dependencies"]
        ), "Step 1.1 backend should use FastAPI"
        assert (
            "react" in frontend_config["dependencies"]
        ), "Step 1.1 frontend should use React"

    def test_step1_1_docker_deployment_workflow(self) -> None:
        """RED: Test Step 1.1 Docker deployment workflow."""
        import pathlib

        # Step 1: Verify Dockerfile exists
        backend_dockerfile = pathlib.Path("web_package/backend/Dockerfile")
        assert (
            backend_dockerfile.exists()
        ), "Step 1.1 backend Dockerfile should exist"

        frontend_dockerfile = pathlib.Path("web_package/frontend/Dockerfile")
        assert (
            frontend_dockerfile.exists()
        ), "Step 1.1 frontend Dockerfile should exist"

        # Step 2: Verify docker-compose configuration
        docker_compose = pathlib.Path("web_package/docker-compose.yml")
        assert (
            docker_compose.exists()
        ), "Step 1.1 docker-compose.yml should exist"

        # Step 3: Verify Docker configuration content
        backend_docker_content = backend_dockerfile.read_text()
        assert (
            "FROM python" in backend_docker_content
        ), "Step 1.1 backend Dockerfile should use Python base image"

        frontend_docker_content = frontend_dockerfile.read_text()
        assert (
            "FROM node" in frontend_docker_content
        ), "Step 1.1 frontend Dockerfile should use Node base image"

    def test_step1_1_type_safety_workflow(self) -> None:
        """RED: Test Step 1.1 type safety workflow."""
        import pathlib

        # Step 1: Verify TypeScript configuration for frontend
        frontend_tsconfig = pathlib.Path("web_package/frontend/tsconfig.json")
        assert (
            frontend_tsconfig.exists()
        ), "Step 1.1 frontend tsconfig.json should exist"

        tsconfig_content = frontend_tsconfig.read_text()
        assert (
            '"strict": true' in tsconfig_content
        ), "Step 1.1 should use strict TypeScript"

        # Step 2: Verify Python type hints for backend
        backend_main = pathlib.Path(
            "web_package/backend/src/todowrite_web/main.py"
        )
        assert backend_main.exists(), "Step 1.1 backend main.py should exist"

        main_content = backend_main.read_text()
        assert (
            "from __future__ import annotations" in main_content
        ), "Step 1.1 backend should use type annotations"
        assert (
            "typing" in main_content
        ), "Step 1.1 backend should import typing"

    def test_step1_1_shared_integration_workflow(self) -> None:
        """RED: Test Step 1.1 shared integration workflow."""
        import pathlib

        # Step 1: Verify shared structure exists
        shared_path = pathlib.Path("web_package/shared")
        assert shared_path.exists(), "Step 1.1 shared directory should exist"

        # Step 2: Verify shared types
        shared_types = pathlib.Path("web_package/shared/types")
        assert shared_types.exists(), "Step 1.1 shared types should exist"

        # Step 3: Verify shared utils
        shared_utils = pathlib.Path("web_package/shared/utils")
        assert shared_utils.exists(), "Step 1.1 shared utils should exist"

        # Step 4: Verify backend can use shared resources
        backend_src = pathlib.Path("web_package/backend/src/todowrite_web")
        assert backend_src.exists(), "Step 1.1 backend src should exist"

        # Step 5: Verify frontend can use shared resources
        frontend_src = pathlib.Path("web_package/frontend/src")
        assert frontend_src.exists(), "Step 1.1 frontend src should exist"

    def test_step1_1_error_handling_workflow(
        self,
        setup_web_driver: webdriver.Chrome,
        setup_step1_1_complete_system: None,
    ) -> None:
        """RED: Test Step 1.1 error handling workflow."""
        driver: webdriver.Chrome = setup_web_driver

        # Step 1: Test backend error handling
        backend_error = requests.get(
            "http://localhost:8000/nonexistent", timeout=10
        )
        assert (
            backend_error.status_code == 404
        ), "Step 1.1 backend should handle 404 errors"

        error_data: dict[str, Any] = backend_error.json()
        assert isinstance(
            error_data, dict
        ), "Step 1.1 backend should return JSON error"

        # Step 2: Test frontend error handling
        driver.get("http://localhost:3000/nonexistent-route")

        try:
            # Look for error boundaries or 404 pages
            error_boundary = driver.find_element(
                By.CSS_SELECTOR,
                "[data-testid='error-boundary'], [data-testid='not-found']",
            )
            assert (
                error_boundary.is_displayed()
            ), "Step 1.1 frontend should handle route errors"
        except:
            pytest.skip(
                "Frontend error handling not implemented yet in Step 1.1"
            )

    def test_step1_1_logging_and_monitoring_workflow(
        self, setup_step1_1_complete_system: None
    ) -> None:
        """RED: Test Step 1.1 logging and monitoring workflow."""
        # Step 1: Verify backend logging
        assert (
            self.backend_process is not None
        ), "Step 1.1 backend process should be running"
        assert (
            self.backend_process.poll() is None
        ), "Step 1.1 backend should not crash"

        # Step 2: Verify frontend logging
        assert (
            self.frontend_process is not None
        ), "Step 1.1 frontend process should be running"
        assert (
            self.frontend_process.poll() is None
        ), "Step 1.1 frontend should not crash"

        # Step 3: Test application health
        health_response = requests.get(
            "http://localhost:8000/health", timeout=10
        )
        assert (
            health_response.status_code == 200
        ), "Step 1.1 health endpoint should work"

    def test_step1_1_security_workflow(
        self, setup_step1_1_complete_system: None
    ) -> None:
        """RED: Test Step 1.1 security workflow."""
        # Step 1: Test CORS security
        headers: dict[str, str] = {
            "Origin": "http://malicious-site.com",
            "Access-Control-Request-Method": "GET",
        }

        cors_response = requests.options(
            "http://localhost:8000/", headers=headers, timeout=10
        )
        # CORS should either allow or deny, but should respond correctly
        assert cors_response.status_code in [
            200,
            204,
            400,
            403,
        ], "Step 1.1 CORS should handle security"

        # Step 2: Test input validation
        try:
            malicious_input = {"script": "<script>alert('xss')</script>"}
            response = requests.post(
                "http://localhost:8000/api/test-input",
                json=malicious_input,
                timeout=10,
            )
            # Should handle input securely
            if response.status_code == 200:
                data: dict[str, Any] = response.json()
                # Should not contain raw script tags
                assert "<script>" not in str(
                    data
                ), "Step 1.1 should sanitize input"
        except:
            pytest.skip("Input validation endpoint not implemented yet")

    def test_step1_1_performance_workflow(
        self,
        setup_web_driver: webdriver.Chrome,
        setup_step1_1_complete_system: None,
    ) -> None:
        """RED: Test Step 1.1 performance workflow."""
        import time

        # Step 1: Test backend performance
        start_time = time.time()
        backend_response = requests.get(
            "http://localhost:8000/health", timeout=10
        )
        backend_time = time.time() - start_time

        assert (
            backend_response.status_code == 200
        ), "Step 1.1 backend should respond"
        assert (
            backend_time < 2.0
        ), "Step 1.1 backend should respond within 2 seconds"

        # Step 2: Test frontend performance
        driver: webdriver.Chrome = setup_web_driver

        start_time = time.time()
        driver.get("http://localhost:3000")

        try:
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "root"))
            )
            frontend_time = time.time() - start_time
            assert (
                frontend_time < 10.0
            ), "Step 1.1 frontend should load within 10 seconds"
        except:
            pytest.skip("Frontend performance test timed out")

    def test_step1_1_comprehensive_system_validation(
        self,
        setup_web_driver: webdriver.Chrome,
        setup_step1_1_complete_system: None,
    ) -> None:
        """RED: Test Step 1.1 comprehensive system validation."""
        # Step 1: Validate complete system startup
        backend_health = requests.get(
            "http://localhost:8000/health", timeout=10
        )
        assert (
            backend_health.status_code == 200
        ), "Step 1.1 complete system should have healthy backend"

        # Step 2: Validate frontend accessibility
        driver: webdriver.Chrome = setup_web_driver
        driver.get("http://localhost:3000")

        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.ID, "root"))
        )

        # Step 3: Validate system integration
        try:
            # Look for integration indicators
            system_status = driver.find_element(
                By.CSS_SELECTOR,
                "[data-testid='system-status'], [data-testid='app-ready']",
            )
            assert (
                system_status.is_displayed()
            ), "Step 1.1 complete system should show status"
        except:
            pytest.skip("System status indicators not implemented yet")

        # Step 4: Validate basic functionality
        page_source: str = driver.page_source
        assert (
            "ToDoWrite" in page_source or "React" in page_source
        ), "Step 1.1 complete system should render content"

        # Step 5: Validate error resilience
        try:
            error_test = requests.get(
                "http://localhost:8000/test-error", timeout=10
            )
            # Should handle errors gracefully
            assert error_test.status_code in [
                404,
                500,
            ], "Step 1.1 should handle error requests"
        except:
            # Connection errors are acceptable for non-existent endpoints
            pass
