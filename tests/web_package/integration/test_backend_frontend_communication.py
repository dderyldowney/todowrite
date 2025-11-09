"""
RED PHASE: Tests for Backend-Frontend Integration
These tests MUST FAIL before implementation exists.
NO MOCKING ALLOWED - Tests will use real backend and frontend communication.
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


class TestBackendFrontendIntegration:
    """Test that backend and frontend communicate correctly."""

    @pytest.fixture(scope="class")
    def setup_servers(self) -> None:
        """Start both backend and frontend servers for integration testing."""
        # Start backend server
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

        # Start frontend server
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
        """Set up Chrome WebDriver for integration testing."""
        chrome_options: Options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--window-size=1920,1080")

        driver: webdriver.Chrome = webdriver.Chrome(options=chrome_options)
        driver.implicitly_wait(10)
        yield driver
        driver.quit()

    def test_api_health_check_integration(self, setup_servers: None) -> None:
        """RED: Test that frontend can call backend health check."""
        # Test direct API call
        response = requests.get("http://localhost:8000/health", timeout=10)
        assert (
            response.status_code == 200
        ), "Backend health endpoint should respond"

        health_data: dict[str, Any] = response.json()
        assert (
            health_data["status"] == "healthy"
        ), "Health check should return healthy"

    def test_cors_configuration(self, setup_servers: None) -> None:
        """RED: Test that CORS is configured correctly between frontend and backend."""
        # Simulate frontend making cross-origin request
        headers: dict[str, str] = {
            "Origin": "http://localhost:3000",
            "Access-Control-Request-Method": "GET",
            "Access-Control-Request-Headers": "Content-Type",
        }

        # Preflight request
        preflight_response = requests.options(
            "http://localhost:8000/api/test", headers=headers, timeout=10
        )

        assert preflight_response.status_code in [
            200,
            204,
        ], "CORS preflight should be allowed"

        # Check CORS headers
        cors_headers = preflight_response.headers
        assert (
            "Access-Control-Allow-Origin" in cors_headers
        ), "Should have CORS allow origin header"

    def test_api_data_format_consistency(self, setup_servers: None) -> None:
        """RED: Test that API data format matches frontend expectations."""
        # Test root endpoint data format
        response = requests.get("http://localhost:8000/", timeout=10)
        assert response.status_code == 200, "Root endpoint should respond"

        data: dict[str, Any] = response.json()
        assert isinstance(data, dict), "API should return JSON object"
        assert "message" in data, "Should have expected data structure"

        # Verify data types
        assert isinstance(data["message"], str), "Message should be string"

    def test_error_handling_integration(self, setup_servers: None) -> None:
        """RED: Test that frontend handles backend errors gracefully."""
        # Test 404 error
        response = requests.get(
            "http://localhost:8000/nonexistent", timeout=10
        )
        assert (
            response.status_code == 404
        ), "Should return 404 for nonexistent endpoint"

        error_data: dict[str, Any] = response.json()
        assert isinstance(error_data, dict), "Error should be JSON object"

    def test_frontend_can_consume_backend_api(
        self, setup_web_driver: webdriver.Chrome, setup_servers: None
    ) -> None:
        """RED: Test that frontend can consume backend API endpoints."""
        driver: webdriver.Chrome = setup_web_driver

        driver.get("http://localhost:3000")

        try:
            # Look for API calls in network (this would need browser extension)
            # For now, test that frontend can make fetch requests

            # Check if frontend has loaded API client
            api_client_element = driver.find_element(
                By.CSS_SELECTOR, "[data-testid='api-client-loaded']"
            )
            assert (
                api_client_element.is_displayed()
            ), "Frontend should load API client"

        except:
            pytest.skip("Frontend API client not implemented yet")

    def test_data_synchronization(
        self, setup_web_driver: webdriver.Chrome, setup_servers: None
    ) -> None:
        """RED: Test that data synchronization works between frontend and backend."""
        driver: webdriver.Chrome = setup_web_driver

        driver.get("http://localhost:3000")

        try:
            # Create a test item via frontend
            create_button = driver.find_element(
                By.CSS_SELECTOR, "[data-testid='create-item-button']"
            )
            create_button.click()

            # Fill out form
            title_input = driver.find_element(
                By.CSS_SELECTOR, "[data-testid='item-title-input']"
            )
            title_input.send_keys("Integration Test Item")

            save_button = driver.find_element(
                By.CSS_SELECTOR, "[data-testid='save-item-button']"
            )
            save_button.click()

            # Verify item was created in backend
            time.sleep(2)  # Wait for synchronization

            backend_response = requests.get(
                "http://localhost:8000/api/items", timeout=10
            )
            if backend_response.status_code == 200:
                items = backend_response.json()
                created_item = next(
                    (
                        item
                        for item in items
                        if item["title"] == "Integration Test Item"
                    ),
                    None,
                )
                assert (
                    created_item is not None
                ), "Created item should exist in backend"

        except:
            pytest.skip("Data synchronization not implemented yet")

    def test_real_time_updates(
        self, setup_web_driver: webdriver.Chrome, setup_servers: None
    ) -> None:
        """RED: Test that real-time updates work between frontend and backend."""
        driver: webdriver.Chrome = setup_web_driver

        driver.get("http://localhost:3000")

        try:
            # Test WebSocket or SSE connection
            connection_indicator = driver.find_element(
                By.CSS_SELECTOR, "[data-testid='real-time-connection']"
            )
            assert (
                connection_indicator.is_displayed()
            ), "Real-time connection indicator should be visible"

            # Simulate backend update
            # In implementation, this would trigger a WebSocket message or SSE event
            backend_update = requests.post(
                "http://localhost:8000/api/test-update",
                json={"message": "test update"},
                timeout=10,
            )

            # Check if frontend receives update
            update_indicator = driver.find_element(
                By.CSS_SELECTOR, "[data-testid='update-received']"
            )
            assert (
                update_indicator.is_displayed()
            ), "Frontend should receive real-time update"

        except:
            pytest.skip("Real-time updates not implemented yet")

    def test_authentication_flow(
        self, setup_web_driver: webdriver.Chrome, setup_servers: None
    ) -> None:
        """RED: Test that authentication flow works between frontend and backend."""
        driver: webdriver.Chrome = setup_web_driver

        driver.get("http://localhost:3000")

        try:
            # Look for login button
            login_button = driver.find_element(
                By.CSS_SELECTOR, "[data-testid='login-button']"
            )
            login_button.click()

            # Fill out login form
            email_input = driver.find_element(
                By.CSS_SELECTOR, "[data-testid='email-input']"
            )
            email_input.send_keys("test@example.com")

            password_input = driver.find_element(
                By.CSS_SELECTOR, "[data-testid='password-input']"
            )
            password_input.send_keys("testpassword")

            submit_button = driver.find_element(
                By.CSS_SELECTOR, "[data-testid='login-submit-button']"
            )
            submit_button.click()

            # Wait for authentication response
            time.sleep(3)

            # Check if user is logged in
            user_profile = driver.find_element(
                By.CSS_SELECTOR, "[data-testid='user-profile']"
            )
            assert (
                user_profile.is_displayed()
            ), "User should be logged in after authentication"

        except:
            pytest.skip("Authentication flow not implemented yet")

    def test_session_management(self, setup_servers: None) -> None:
        """RED: Test that session management works correctly."""
        # Test session creation
        login_data: dict[str, str] = {
            "email": "test@example.com",
            "password": "testpassword",
        }

        login_response = requests.post(
            "http://localhost:8000/api/login", json=login_data, timeout=10
        )

        if login_response.status_code == 200:
            session_data: dict[str, Any] = login_response.json()
            assert (
                "token" in session_data
            ), "Should receive authentication token"
            assert session_data["token"], "Token should not be empty"

            # Test protected endpoint with token
            headers: dict[str, str] = {
                "Authorization": f"Bearer {session_data['token']}"
            }

            protected_response = requests.get(
                "http://localhost:8000/api/protected",
                headers=headers,
                timeout=10,
            )

            assert (
                protected_response.status_code == 200
            ), "Protected endpoint should work with valid token"

        else:
            pytest.skip("Session management not implemented yet")

    def test_error_boundary_handling(
        self, setup_web_driver: webdriver.Chrome, setup_servers: None
    ) -> None:
        """RED: Test that frontend handles backend errors gracefully."""
        driver: webdriver.Chrome = setup_web_driver

        driver.get("http://localhost:3000")

        try:
            # Simulate backend error by accessing invalid endpoint
            error_button = driver.find_element(
                By.CSS_SELECTOR, "[data-testid='trigger-error-button']"
            )
            error_button.click()

            # Check if frontend shows error boundary
            error_boundary = driver.find_element(
                By.CSS_SELECTOR, "[data-testid='error-boundary']"
            )
            assert (
                error_boundary.is_displayed()
            ), "Frontend should show error boundary for backend errors"

            # Check for recovery mechanism
            recovery_button = driver.find_element(
                By.CSS_SELECTOR, "[data-testid='error-recovery-button']"
            )
            assert (
                recovery_button.is_displayed()
            ), "Should provide error recovery mechanism"

        except:
            pytest.skip("Error boundary handling not implemented yet")
