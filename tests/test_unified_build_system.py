"""
Tests for the unified monorepo build system.

Following Red-Green-Refactor methodology:
1. RED: Write failing test
2. GREEN: Make test pass with minimal implementation
3. REFACTOR: Clean up the implementation
"""

import subprocess
import sys
from pathlib import Path


class TestUnifiedBuildSystem:
    """Test the unified monorepo build system functionality."""

    def test_build_script_exists_and_executable(self):
        """RED: Test that the build script exists and is executable."""
        build_script = Path(__file__).parent.parent / "dev_tools" / "build.sh"

        # This should fail initially
        assert build_script.exists(), "Build script should exist"
        assert build_script.is_file(), "Build script should be a file"
        assert oct(build_script.stat().st_mode)[-3:] == "755", "Build script should be executable"

    def test_build_script_help_command(self):
        """RED: Test that build script responds to help command."""
        result = subprocess.run(
            ["./dev_tools/build.sh", "help"],
            check=False,
            capture_output=True,
            text=True,
            cwd=Path(__file__).parent.parent,
        )

        # This should fail initially
        assert result.returncode == 0, "Help command should succeed"
        assert "ToDoWrite Monorepo Build Script" in result.stdout
        assert "Commands:" in result.stdout

    def test_deploy_script_pypi_after_testpypi_workflow(self):
        """RED: Test that deploy script has automatic PyPI deployment after TestPyPI success."""
        deploy_script = Path(__file__).parent.parent / "dev_tools" / "deploy.sh"

        # This should fail initially - we're testing for functionality that doesn't exist yet
        assert deploy_script.exists(), "Deploy script should exist"

        # Check that deploy script has workflow for automatic PyPI deployment
        result = subprocess.run(
            ["./dev_tools/deploy.sh", "help"],
            check=False,
            capture_output=True,
            text=True,
            cwd=Path(__file__).parent.parent,
        )

        assert result.returncode == 0, "Deploy help should succeed"

        # This should pass - we implemented auto-deploy functionality
        assert "auto-deploy" in result.stdout, (
            "Should have automatic PyPI deployment after TestPyPI"
        )

    def test_build_system_api_interface(self):
        """RED: Test that build system has proper Python API interface."""
        # This should fail - we're testing for an API that doesn't exist yet
        try:
            from todowrite.build_system import BuildManager

            build_manager = BuildManager()
            assert build_manager is not None, "BuildManager should be available"
        except ImportError:
            # This is the RED state - the import should fail
            assert False, "BuildManager API should exist but doesn't"

    def test_uv_workspace_configuration(self):
        """RED: Test that UV workspace is properly configured."""
        pyproject_path = Path(__file__).parent.parent / "pyproject.toml"

        with open(pyproject_path) as f:
            content = f.read()

        # This should fail initially
        assert "[tool.uv.workspace]" in content, "UV workspace should be configured"
        assert "lib_package" in content, "lib_package should be in workspace"
        assert "cli_package" in content, "cli_package should be in workspace"
        assert "web_package" in content, "web_package should be in workspace"

    def test_shared_dependency_groups(self):
        """RED: Test that shared dependency groups are configured."""
        pyproject_path = Path(__file__).parent.parent / "pyproject.toml"

        with open(pyproject_path) as f:
            content = f.read()

        # This should fail initially
        assert "[dependency-groups]" in content, "Dependency groups should be configured"
        assert "dev =" in content, "Dev dependency group should exist"
        assert "core =" in content, "Core dependency group should exist"

    def test_unified_ruff_configuration(self):
        """RED: Test that Ruff configuration is unified."""
        pyproject_path = Path(__file__).parent.parent / "pyproject.toml"

        with open(pyproject_path) as f:
            content = f.read()

        # This should fail initially
        assert "[tool.ruff]" in content, "Ruff should be configured"
        assert "line-length = 100" in content, "Should have consistent line length"
        assert 'target-version = "py312"' in content, "Should have target Python version"

    def test_central_version_management(self):
        """RED: Test that version management is centralized."""
        version_file = Path(__file__).parent.parent / "VERSION"

        with open(version_file) as f:
            version_content = f.read().strip()

        # This should fail initially
        assert version_file.exists(), "VERSION file should exist"
        assert len(version_content.split(".")) == 3, "Version should be semantic (x.y.z)"

        # Check that packages reference this central VERSION file
        lib_pyproject = Path(__file__).parent.parent / "lib_package" / "pyproject.toml"
        with open(lib_pyproject) as f:
            lib_content = f.read()

        assert 'dynamic = ["version"]' in lib_content, "lib_package should use dynamic version"
        assert 'path = "../VERSION"' in lib_content, "lib_package should reference central VERSION"

    def test_packages_build_with_hatchling(self):
        """RED: Test that packages build successfully with hatchling."""
        lib_package = Path(__file__).parent.parent / "lib_package"

        # Try to build lib_package - this should fail if not properly configured
        result = subprocess.run(
            [sys.executable, "-m", "build", str(lib_package)],
            check=False,
            capture_output=True,
            text=True,
            cwd=lib_package,
        )

        # This should fail initially, showing our test catches build issues
        assert result.returncode == 0, f"lib_package should build successfully: {result.stderr}"

        # Check that wheel and tar.gz are created
        dist_dir = lib_package / "dist"
        assert dist_dir.exists(), "dist directory should be created"
        assert any(dist_dir.glob("*.whl")), "Wheel file should be created"
        assert any(dist_dir.glob("*.tar.gz")), "Source distribution should be created"

    def test_build_script_validate_command(self):
        """RED: Test that build script has validate command that doesn't exist yet."""
        # This should definitely fail - we're testing for a command that doesn't exist
        result = subprocess.run(
            ["./dev_tools/build.sh", "validate"],
            check=False,
            capture_output=True,
            text=True,
            cwd=Path(__file__).parent.parent,
        )

        # This should fail in RED state - validate command doesn't exist yet
        assert result.returncode == 0, f"Validate command should exist and succeed: {result.stderr}"
        assert "Build system validation completed successfully" in result.stdout, (
            "Should show validation success"
        )

    def test_package_independence_maintained(self):
        """RED: Test that packages can still be built independently."""
        cli_package = Path(__file__).parent.parent / "cli_package"

        # Each package should have its own pyproject.toml
        cli_pyproject = cli_package / "pyproject.toml"
        assert cli_pyproject.exists(), "CLI package should have its own pyproject.toml"

        # Should be buildable independently
        result = subprocess.run(
            [sys.executable, "-m", "build", str(cli_package)],
            check=False,
            capture_output=True,
            text=True,
            cwd=cli_package,
        )

        assert result.returncode == 0, f"cli_package should build independently: {result.stderr}"
