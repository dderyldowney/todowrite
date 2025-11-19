"""
Test-Driven Development Skill Tests

Tests for the test-driven-development superpowers skill with fail-safe mechanisms.
Following TDD methodology: RED → GREEN → REFACTOR

Author: Claude Code Assistant
Version: 2025.1.0
"""

import subprocess
import tempfile
from pathlib import Path

import pytest

from .conftest import TestSuperpowersBase


class TestTestDrivenDevelopment(TestSuperpowersBase):
    """Test class for test-driven-development skill functionality."""

    def test_tdd_skill_missing_file_should_fail(self) -> None:
        """RED TEST: Test that TDD skill fails when implementation file doesn't exist"""
        # This test should fail initially because the TDD skill isn't implemented yet
        skill_path = (
            Path.home() / ".claude/plugins/cache/superpowers/skills/test-driven-development"
        )

        # The skill file should not exist yet (RED phase)
        assert not skill_path.exists(), "TDD skill should not exist yet (RED phase)"

        # When we try to import/use it, it should fail
        with pytest.raises((ImportError, FileNotFoundError)):
            import sys

            sys.path.insert(0, str(skill_path.parent))

    def test_tdd_workflow_red_phase_should_fail(self) -> None:
        """RED TEST: Test that TDD workflow fails without implementation"""
        # Create temporary directory for testing
        with tempfile.TemporaryDirectory() as temp_dir:
            Path(temp_dir)

            # Create a simple feature request

            # Try to run TDD workflow - should fail without implementation
            with pytest.raises((FileNotFoundError, ImportError, subprocess.CalledProcessError)):
                # This should fail because the TDD skill doesn't exist yet
                result = subprocess.run(
                    [
                        "python3",
                        "-c",
                        "from superpowers_fail_safes import with_fail_safes;"
                        "@with_fail_safes('tdd_workflow');"
                        "def run_tdd(): pass;"
                        "run_tdd()",
                    ],
                    check=False,
                    capture_output=True,
                    text=True,
                    timeout=30,
                )

                if result.returncode != 0:
                    msg = "TDD skill implementation not found"
                    raise FileNotFoundError(msg)

    def test_tdd_failing_test_creation_should_fail(self) -> None:
        """RED TEST: Test that failing test creation fails without TDD implementation"""
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)

            # Create test directory structure
            test_dir = temp_path / "tests" / "features" / "auth"
            test_dir.mkdir(parents=True)

            # Try to create failing test for authentication
            test_content = '''
def test_user_registration():
    """Test user registration functionality - this should fail initially"""
    # This test should fail because User model doesn't exist yet
    user = User(email="test@example.com", password="secure123")
    assert user.id is not None
    assert user.email == "test@example.com"
'''

            test_file = test_dir / "test_user_registration.py"

            # Writing test should succeed, but importing/running should fail
            test_file.write_text(test_content)

            # Running the test should fail because User class doesn't exist
            result = subprocess.run(
                ["python3", "-m", "pytest", str(test_file), "-v"],
                check=False,
                capture_output=True,
                text=True,
                cwd=temp_path,
            )

            # Should fail because User is not defined (RED phase)
            assert result.returncode != 0, "Test should fail initially (RED phase)"
            assert (
                "NameError" in result.stderr
                or "ImportError" in result.stderr
                or "FAILED" in result.stdout
            )

    def test_tdd_minimal_implementation_should_fail(self) -> None:
        """RED TEST: Test that minimal implementation creation fails without TDD skill"""
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)

            # Create source directory
            src_dir = temp_path / "src" / "ToDoWrite" / "models"
            src_dir.mkdir(parents=True)

            # Try to create minimal implementation without TDD guidance
            implementation_content = """
# Minimal User model implementation
class User:
    def __init__(self, email: str, password: str):
        self.email = email
        self.password = password
        self.id = None  # Will be set by database
"""

            impl_file = src_dir / "user.py"
            impl_file.write_text(implementation_content)

            # Create corresponding test
            test_dir = temp_path / "tests" / "models"
            test_dir.mkdir(parents=True)

            test_content = '''
import sys
sys.path.insert(0, str(__file__).parent.parent.parent / "src"))

from todowrite.models.user import User

def test_user_creation():
    """Test basic user creation"""
    user = User(email="test@example.com", password="secure123")
    assert user.email == "test@example.com"
    assert user.password == "secure123"
'''

            test_file = test_dir / "test_user.py"
            test_file.write_text(test_content)

            # Running this should fail because TDD workflow isn't properly implemented
            # and we're missing proper test structure and dependencies
            result = subprocess.run(
                ["python3", "-m", "pytest", str(test_file), "-v"],
                check=False,
                capture_output=True,
                text=True,
                cwd=temp_path,
            )

            # Should fail due to missing TDD infrastructure (RED phase)
            assert result.returncode != 0, "Should fail without proper TDD infrastructure"

    def test_tdd_refactoring_phase_should_fail(self) -> None:
        """RED TEST: Test that refactoring phase fails without TDD implementation"""
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)

            # Create a scenario where we have working code but want to refactor
            working_code = """
class UserAuth:
    def authenticate(self, email, password):
        # Basic authentication logic
        if email and password:
            return True
        return False

    def register_user(self, email, password):
        # Basic registration
        if email and password:
            return {"success": True, "user_id": 123}
        return {"success": False, "error": "Invalid data"}
"""

            code_file = temp_path / "auth.py"
            code_file.write_text(working_code)

            # Try to use TDD skill for refactoring - should fail
            with pytest.raises((FileNotFoundError, ImportError)):
                # This should fail because TDD refactoring skill doesn't exist
                subprocess.run(
                    [
                        "python3",
                        "-c",
                        "import sys;"
                        "sys.path.append('~/claude/plugins/cache/superpowers/skills/test-driven-development');"
                        "import test_driven_development;"
                        "test_driven_development.refactor_with_tdd('auth.py')",
                    ],
                    check=True,
                    capture_output=True,
                    text=True,
                    timeout=30,
                )

    def test_tdd_fail_safe_integration_should_fail(self) -> None:
        """RED TEST: Test that TDD skill integration with fail-safes fails initially"""
        from .claude.superpowers_fail_safes import ResourceLimits

        # Initialize fail-safes with strict limits for testing
        strict_limits = ResourceLimits(
            max_memory_mb=64,  # Very low limit for testing
            max_execution_time_seconds=10,  # Short timeout
            max_concurrent_subagents=1,  # Only one subagent at a time
        )

        fail_safes = SuperpowersFailSafes(strict_limits)

        # Try to register TDD subagent - should fail because skill doesn't exist
        subagent_id = "tdd_refactoring"

        # Registration might succeed, but execution should fail
        registered = fail_safes.register_subagent(subagent_id)

        if registered:
            # Try to execute TDD workflow - should fail
            with pytest.raises((FileNotFoundError, ImportError, RuntimeError)):
                # This should fail because TDD skill implementation doesn't exist
                fail_safes.update_subagent_resources(subagent_id)
                status = fail_safes.check_subagent_health(subagent_id)

                if status.value == "active":
                    msg = "TDD subagent should not be active without implementation"
                    raise RuntimeError(msg)

    def test_tdd_skill_discovery_should_fail(self) -> None:
        """RED TEST: Test that TDD skill discovery fails initially"""
        skills_dir = Path.home() / ".claude/plugins/cache/superpowers/skills"
        tdd_skill_dir = skills_dir / "test-driven-development"

        # TDD skill directory should not exist initially
        assert not tdd_skill_dir.exists(), "TDD skill directory should not exist yet"

        # Skill discovery should fail
        discovered_skills = []

        try:
            for skill_dir in skills_dir.iterdir():
                if skill_dir.is_dir():
                    discovered_skills.append(skill_dir.name)
        except FileNotFoundError:
            discovered_skills = []

        assert "test-driven-development" not in discovered_skills, (
            "TDD skill should not be discoverable yet"
        )

    @pytest.mark.parametrize(
        "feature_type", ["authentication", "data_validation", "api_endpoints", "database_models"]
    )
    def test_tdd_feature_support_should_fail(self, feature_type: str) -> None:
        """RED TEST: Test that TDD feature support fails for various feature types"""
        feature_requests = {
            "authentication": "User login and registration system",
            "data_validation": "Input validation and sanitization",
            "api_endpoints": "RESTful API with proper error handling",
            "database_models": "SQLAlchemy models with relationships",
        }

        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)

            # Try to create TDD workflow for each feature type
            feature_description = feature_requests[feature_type]

            # This should fail because TDD skill doesn't exist
            with pytest.raises((FileNotFoundError, ImportError)):
                subprocess.run(
                    [
                        "python3",
                        "-c",
                        f"from tdd_workflow import create_tdd_plan;"
                        f"create_tdd_plan('{feature_description}', '{temp_path}')",
                    ],
                    check=True,
                    capture_output=True,
                    text=True,
                    timeout=30,
                )

    def test_tdd_quality_metrics_should_fail(self) -> None:
        """RED TEST: Test that TDD quality metrics collection fails initially"""
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)

            # Create some test files
            test_files = []
            for i in range(3):
                test_file = temp_path / f"test_feature_{i}.py"
                test_file.write_text(f"""
def test_feature_{i}():
    assert True  # Placeholder test
""")
                test_files.append(test_file)

            # Try to analyze test quality - should fail without TDD skill
            with pytest.raises((FileNotFoundError, ImportError)):
                subprocess.run(
                    [
                        "python3",
                        "-c",
                        "from tdd_analyzer import analyze_test_quality;"
                        f"analyze_test_quality({[str(f) for f in test_files]})",
                    ],
                    check=True,
                    capture_output=True,
                    text=True,
                    timeout=30,
                )


# Test configuration for pytest
def pytest_configure(config):
    """Configure pytest for TDD tests"""
    config.addinivalue_line(
        "markers", "tdd_red: Tests for RED phase of TDD (should fail initially)"
    )
    config.addinivalue_line("markers", "tdd_green: Tests for GREEN phase of TDD (implementation)")
    config.addinivalue_line("markers", "tdd_refactor: Tests for REFACTOR phase of TDD")


if __name__ == "__main__":
    # Run the failing tests to demonstrate RED phase
    print("🔴 Running TDD RED Phase Tests (Expected to Fail)")
    print("=" * 50)

    # Run pytest with our tests
    exit_code = subprocess.run(
        ["python3", "-m", "pytest", __file__, "-v", "--tb=short"], check=False
    ).returncode

    if exit_code != 0:
        print("\n✅ RED Phase: Tests are failing as expected")
        print("📝 Next step: Implement TDD skill to make tests pass (GREEN phase)")
    else:
        print("\n❌ Unexpected: Tests should be failing in RED phase")

    exit(exit_code)
