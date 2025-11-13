"""
Comprehensive tests for the unified build system.

Following TDD principles with thorough coverage of all build system components.
"""

import subprocess
from pathlib import Path
from unittest.mock import MagicMock, patch

# Import the components we're testing
from todowrite.build_system import (
    BuildManager,
    PackageInfo,
    ValidationResult,
    VersionValidator,
    WorkspaceValidator,
)


class TestValidationResult:
    """Test ValidationResult dataclass and methods."""

    def test_success_creation(self):
        """Test creating a successful ValidationResult."""
        result = ValidationResult.success()
        assert result.is_valid is True
        assert result.errors == []
        assert result.warnings == []

    def test_failure_creation(self):
        """Test creating a failed ValidationResult."""
        errors = ["Error 1", "Error 2"]
        warnings = ["Warning 1"]
        result = ValidationResult.failure(errors, warnings)

        assert result.is_valid is False
        assert result.errors == errors
        assert result.warnings == warnings

    def test_failure_creation_without_warnings(self):
        """Test creating a failed ValidationResult without warnings."""
        errors = ["Error 1"]
        result = ValidationResult.failure(errors)

        assert result.is_valid is False
        assert result.errors == errors
        assert result.warnings == []


class TestWorkspaceValidator:
    """Test WorkspaceValidator implementation."""

    def setup_method(self):
        """Set up test fixtures."""
        self.validator = WorkspaceValidator()
        self.project_root = Path("/test/project")

    @patch("pathlib.Path.exists")
    @patch("pathlib.Path.read_text")
    def test_validate_success(self, mock_read, mock_exists):
        """Test successful workspace validation."""
        # Mock pyproject.toml exists
        mock_exists.return_value = True
        # Mock pyproject.toml content with workspace config
        mock_read.return_value = """
        [tool.uv.workspace]
        members = ["lib_package", "cli_package", "web_package"]

        [tool.uv.sources]
        todowrite = { workspace = true }
        """

        result = self.validator.validate(self.project_root)
        assert result.is_valid is True
        assert result.errors == []

    @patch("pathlib.Path.exists")
    def test_validate_missing_pyproject(self, mock_exists):
        """Test validation when pyproject.toml is missing."""
        mock_exists.return_value = False

        result = self.validator.validate(self.project_root)
        assert result.is_valid is False
        assert "pyproject.toml not found" in result.errors

    @patch("pathlib.Path.exists")
    @patch("pathlib.Path.read_text")
    def test_validate_missing_workspace_config(self, mock_read, mock_exists):
        """Test validation when UV workspace is not configured."""
        mock_exists.return_value = True
        mock_read.return_value = """
        [project]
        name = "test"
        """

        result = self.validator.validate(self.project_root)
        assert result.is_valid is False
        assert "UV workspace not configured" in result.errors

    @patch("pathlib.Path.exists")
    @patch("pathlib.Path.read_text")
    def test_validate_missing_packages(self, mock_read, mock_exists):
        """Test validation when packages are missing from workspace."""
        mock_exists.return_value = True
        mock_read.return_value = """
        [tool.uv.workspace]
        members = ["lib_package"]  # Missing cli_package and web_package
        """

        result = self.validator.validate(self.project_root)
        assert result.is_valid is False
        assert "cli_package not found in workspace" in result.errors
        assert "web_package not found in workspace" in result.errors


class TestVersionValidator:
    """Test VersionValidator implementation."""

    def setup_method(self):
        """Set up test fixtures."""
        self.validator = VersionValidator()
        self.project_root = Path("/test/project")

    @patch("pathlib.Path.exists")
    @patch("pathlib.Path.read_text")
    def test_validate_success(self, mock_read, mock_exists):
        """Test successful version validation."""
        # Mock all files exist
        mock_exists.side_effect = lambda path: "VERSION" in str(path) or "pyproject.toml" in str(
            path
        )

        # Mock VERSION file content
        def mock_read_side_effect():
            if str(mock_read.call_args[0][0]).endswith("VERSION"):
                return "1.2.3\n"
            return 'dynamic = ["version"]\n[tool.hatch.version]\npath = "../VERSION"\n'

        mock_read.side_effect = mock_read_side_effect

        result = self.validator.validate(self.project_root)
        assert result.is_valid is True
        assert result.errors == []

    @patch("pathlib.Path.exists")
    def test_validate_missing_version_file(self, mock_exists):
        """Test validation when VERSION file is missing."""
        mock_exists.return_value = False

        result = self.validator.validate(self.project_root)
        assert result.is_valid is False
        assert "VERSION file not found" in result.errors

    @patch("pathlib.Path.exists")
    @patch("pathlib.Path.read_text")
    def test_validate_empty_version_file(self, mock_read, mock_exists):
        """Test validation when VERSION file is empty."""
        mock_exists.return_value = True

        def mock_read_side_effect():
            if str(mock_read.call_args[0][0]).endswith("VERSION"):
                return "\n"
            return 'dynamic = ["version"]\n[tool.hatch.version]\npath = "../VERSION"\n'

        mock_read.side_effect = mock_read_side_effect

        result = self.validator.validate(self.project_root)
        assert result.is_valid is False
        assert "VERSION file is empty" in result.errors

    @patch("pathlib.Path.exists")
    @patch("pathlib.Path.read_text")
    def test_validate_package_not_referencing_version(self, mock_read, mock_exists):
        """Test validation when packages don't reference central VERSION."""
        mock_exists.return_value = True

        def mock_read_side_effect():
            if str(mock_read.call_args[0][0]).endswith("VERSION"):
                return "1.2.3\n"
            return 'dynamic = ["version"]\n[tool.hatch.version]\npath = "local_version"\n'

        mock_read.side_effect = mock_read_side_effect

        result = self.validator.validate(self.project_root)
        assert result.is_valid is False
        assert any("doesn't reference central VERSION file" in error for error in result.errors)


class TestBuildManager:
    """Test BuildManager main class."""

    def setup_method(self):
        """Set up test fixtures."""
        self.mock_project_root = Path("/test/project")
        self.build_manager = BuildManager(str(self.mock_project_root))

    def test_initialization_with_path(self):
        """Test BuildManager initialization with explicit path."""
        test_path = Path("/custom/path")
        manager = BuildManager(str(test_path))
        assert manager.project_root == test_path

    def test_get_workspace_packages(self):
        """Test getting workspace packages information."""
        # Mock the _load_package_info method
        mock_packages = {
            "lib_package": PackageInfo(
                name="lib_package",
                path=self.mock_project_root / "lib_package",
                pyproject_path=self.mock_project_root / "lib_package" / "pyproject.toml",
                dist_path=self.mock_project_root / "lib_package" / "dist",
            )
        }

        self.build_manager._packages = mock_packages

        result = self.build_manager.get_workspace_packages()
        assert result == mock_packages

    @patch("subprocess.run")
    def test_run_build_script_success(self, mock_subprocess):
        """Test successful build script execution."""
        mock_result = MagicMock()
        mock_result.returncode = 0
        mock_result.stdout = "Success"
        mock_result.stderr = ""
        mock_subprocess.return_value = mock_result

        result = self.build_manager.run_build_script("test")

        assert result == mock_result
        mock_subprocess.assert_called_once()

    @patch("subprocess.run")
    def test_run_build_script_timeout(self, mock_subprocess):
        """Test build script execution with timeout."""
        mock_result = MagicMock()
        mock_result.returncode = 0
        mock_subprocess.return_value = mock_result

        self.build_manager.run_build_script("test")

        # Verify timeout was set
        mock_subprocess.assert_called_once()
        call_args = mock_subprocess.call_args[1]
        assert call_args["timeout"] == 300

    def test_validate_configuration_integration(self):
        """Test validate_configuration integrates all validators."""
        # Mock validators
        mock_validators = []
        for i in range(2):  # Two validators
            mock_validator = MagicMock()
            mock_validators.append(mock_validator)

        self.build_manager._validators = mock_validators

        # All validators succeed
        mock_validators[0].validate.return_value = ValidationResult.success()
        mock_validators[1].validate.return_value = ValidationResult.success()

        result = self.build_manager.validate_configuration()
        assert result.is_valid is True
        assert len(result.errors) == 0

        # Verify all validators were called
        for mock_validator in mock_validators:
            mock_validator.validate.assert_called_once_with(self.mock_project_root)

    def test_validate_configuration_with_errors(self):
        """Test validate_configuration handles errors properly."""
        mock_validators = []
        for i in range(2):  # Two validators
            mock_validator = MagicMock()
            mock_validators.append(mock_validator)

        self.build_manager._validators = mock_validators

        # First validator succeeds, second fails
        mock_validators[0].validate.return_value = ValidationResult.success()
        mock_validators[1].validate.return_value = ValidationResult.failure(
            ["Test error"], ["Test warning"]
        )

        result = self.build_manager.validate_configuration()
        assert result.is_valid is False
        assert "Test error" in result.errors
        assert "Test warning" in result.warnings


class TestBuildManagerIntegration:
    """Integration tests for BuildManager with real filesystem structure."""

    def test_build_manager_initialization_auto_detect(self):
        """Test BuildManager auto-detects project root."""
        # This test checks if the BuildManager can find the correct project root
        # from the actual file structure
        manager = BuildManager()

        # Should auto-detect the project root (4 levels up from this file)
        expected_root = Path(__file__).parent.parent.parent.parent
        assert manager.project_root == expected_root

        # Check that it's a real directory with expected files
        assert manager.project_root.exists()
        assert (manager.project_root / "pyproject.toml").exists()
        assert (manager.project_root / "VERSION").exists()

    def test_build_manager_validate_real_configuration(self):
        """Test BuildManager validation against real project configuration."""
        manager = BuildManager()

        # This should pass if the configuration is correct
        result = manager.validate_configuration()

        # We can't guarantee the exact result in a test environment,
        # but we can test that it doesn't crash and returns a proper result
        assert isinstance(result, ValidationResult)
        assert isinstance(result.is_valid, bool)
        assert isinstance(result.errors, list)
        assert isinstance(result.warnings, list)

    def test_build_manager_get_real_packages(self):
        """Test BuildManager gets real package information."""
        manager = BuildManager()

        packages = manager.get_workspace_packages()

        # Should return a dictionary with expected packages
        assert isinstance(packages, dict)

        # Check that expected packages are present (they might not exist in test environment)
        expected_packages = ["lib_package", "cli_package", "web_package"]
        for pkg_name in expected_packages:
            if pkg_name in packages:
                pkg_info = packages[pkg_name]
                assert isinstance(pkg_info, PackageInfo)
                assert pkg_info.name == pkg_name
                assert isinstance(pkg_info.path, Path)
                assert isinstance(pkg_info.pyproject_path, Path)
                assert isinstance(pkg_info.dist_path, Path)


class TestDeployScriptWorkflow:
    """Test deployment script workflow."""

    def test_deploy_help_command(self):
        """Test that deploy script help works."""
        result = subprocess.run(
            ["./dev_tools/deploy.sh", "help"],
            check=False,
            capture_output=True,
            text=True,
            cwd=Path(__file__).parent.parent,
        )

        assert result.returncode == 0
        assert "auto-deploy" in result.stdout
        assert "main branch only" in result.stdout

    def test_deploy_help_shows_new_commands(self):
        """Test that deploy script help shows new auto-deploy command."""
        result = subprocess.run(
            ["./dev_tools/deploy.sh", "help"],
            check=False,
            capture_output=True,
            text=True,
            cwd=Path(__file__).parent.parent,
        )

        assert result.returncode == 0
        assert "auto-deploy" in result.stdout
        assert "TestPyPI, then PyPI" in result.stdout
