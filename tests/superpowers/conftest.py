"""
Pytest configuration for superpowers tests.

Provides base classes and common fixtures for testing superpowers functionality.
"""

import tempfile
from pathlib import Path

import pytest


class TestSuperpowersBase:
    """Base class for superpowers tests with common setup utilities."""

    def setup_method(self):
        """Set up test environment before each test method."""
        # Create temporary directory for test files
        self.temp_dir = Path(tempfile.mkdtemp())

    def teardown_method(self):
        """Clean up after each test method."""
        # Clean up temporary directory if it exists
        if hasattr(self, "temp_dir") and self.temp_dir.exists():
            import shutil

            shutil.rmtree(self.temp_dir, ignore_errors=True)

    def create_temp_file(self, filename: str, content: str) -> Path:
        """Create a temporary file with given content."""
        file_path = self.temp_dir / filename
        file_path.write_text(content)
        return file_path

    def run_command(self, command: list, cwd: Path = None) -> tuple:
        """Run a command and return (returncode, stdout, stderr)."""
        import subprocess

        if cwd is None:
            cwd = self.temp_dir

        result = subprocess.run(
            command, check=False, cwd=cwd, capture_output=True, text=True, timeout=30
        )

        return result.returncode, result.stdout, result.stderr


@pytest.fixture
def temp_test_dir():
    """Provide a temporary directory for testing."""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield Path(tmpdir)
