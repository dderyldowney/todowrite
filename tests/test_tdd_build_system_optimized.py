"""
Optimized TDD Tests for Build System Extensions.

These tests are optimized to avoid hanging by testing individual components
instead of running full test suites with coverage.
"""

import subprocess
import time
from pathlib import Path


class TestOptimizedTDDFeatures:
    """Optimized TDD tests that avoid hanging by testing components directly."""

    def test_build_manager_dependency_analysis_fast(self):
        """GREEN: Test BuildManager dependency analysis without heavy operations."""
        # Import and test the method directly without subprocess
        try:
            from build_system import BuildManager

            manager = BuildManager()
            analysis = manager.analyze_dependencies()

            # Verify structure without waiting for heavy operations
            assert isinstance(analysis, dict), "Should return dict"
            assert "total_packages" in analysis, "Should include total_packages"
            assert "dependencies" in analysis, "Should include dependencies"
            assert "shared_dependencies" in analysis, "Should include shared_dependencies"
            assert isinstance(analysis["total_packages"], int), "total_packages should be int"
            assert isinstance(analysis["dependencies"], dict), "dependencies should be dict"

        except ImportError as e:
            assert False, f"BuildManager should be importable: {e}"
        except Exception as e:
            assert False, f"BuildManager.analyze_dependencies() should work: {e}"

    def test_audit_command_syntax_check(self):
        """GREEN: Test audit command exists and has proper syntax."""
        # Test script exists and is executable
        build_script = Path(__file__).parent.parent / "dev_tools" / "build.sh"
        assert build_script.exists(), "Build script should exist"
        assert build_script.is_file(), "Build script should be a file"

        # Test script has the audit function
        script_content = build_script.read_text()
        assert "run_audit()" in script_content, "Script should have run_audit function"
        assert "audit)" in script_content, "Script should handle audit command"

        # Test audit command syntax (quick dry run)
        result = subprocess.run(
            ["./dev_tools/build.sh", "help"],
            check=False,
            capture_output=True,
            text=True,
            cwd=Path(__file__).parent.parent,
            timeout=5,  # Short timeout
        )

        assert result.returncode == 0, "Help command should work"
        assert "audit" in result.stdout, "Audit should be in help output"

    def test_quality_gate_argument_parsing_fast(self):
        """GREEN: Test quality gate argument parsing without running full tests."""
        build_script = Path(__file__).parent.parent / "dev_tools" / "build.sh"

        # Test script has enhanced quality-gate function
        script_content = build_script.read_text()
        assert "run_quality_gate()" in script_content, "Script should have quality-gate function"
        assert "--coverage-threshold" in script_content, "Should support threshold argument"
        assert "--strict" in script_content, "Should support strict mode"
        assert "Invalid coverage threshold" in script_content, "Should validate input"

        # Test invalid threshold validation (should fail fast)
        result = subprocess.run(
            ["./dev_tools/build.sh", "quality-gate", "--coverage-threshold", "150"],
            check=False,
            capture_output=True,
            text=True,
            cwd=Path(__file__).parent.parent,
            timeout=5,  # Short timeout
        )

        assert result.returncode == 1, "Should reject invalid threshold"
        assert "Coverage threshold must be between 1 and 100" in result.stdout, (
            "Should show validation error"
        )

        # Test unknown option handling
        result = subprocess.run(
            ["./dev_tools/build.sh", "quality-gate", "--unknown-option"],
            check=False,
            capture_output=True,
            text=True,
            cwd=Path(__file__).parent.parent,
            timeout=5,
        )

        assert result.returncode == 1, "Should reject unknown option"
        assert "Unknown option: --unknown-option" in result.stdout, "Should show error message"

    def test_quality_gate_help_output(self):
        """GREEN: Test quality gate provides helpful usage information."""
        result = subprocess.run(
            ["./dev_tools/build.sh", "quality-gate", "--unknown"],
            check=False,
            capture_output=True,
            text=True,
            cwd=Path(__file__).parent.parent,
            timeout=5,
        )

        assert result.returncode == 1, "Should fail on unknown option"
        assert "Usage: quality-gate" in result.stdout, "Should show usage information"

    def test_build_script_structure(self):
        """GREEN: Test build script has proper structure and functions."""
        build_script = Path(__file__).parent.parent / "dev_tools" / "build.sh"
        script_content = build_script.read_text()

        # Check for key functions
        required_functions = [
            "run_audit()",
            "run_quality_gate()",
            "print_status()",
            "print_success()",
            "print_error()",
            "print_warning()",
        ]

        for func in required_functions:
            assert func in script_content, f"Script should have {func}"

        # Check for error handling patterns
        assert "set -e" in script_content, "Script should exit on errors"
        assert "function show_usage()" in script_content or "show_usage()" in script_content, (
            "Should have usage function"
        )

    def test_build_manager_class_structure(self):
        """GREEN: Test BuildManager class has proper structure."""
        try:
            from build_system import BuildManager

            # Check class can be instantiated
            manager = BuildManager()
            assert manager is not None, "BuildManager should be instantiable"

            # Check required methods exist
            assert hasattr(manager, "analyze_dependencies"), (
                "Should have analyze_dependencies method"
            )
            assert callable(manager.analyze_dependencies), "analyze_dependencies should be callable"

        except ImportError as e:
            assert False, f"BuildManager should be importable: {e}"

    def test_fast_quality_gate_timeout_protection(self):
        """GREEN: Test quality gate has timeout protection by checking for quick validation."""
        # This test verifies that argument validation works quickly
        # before any long-running operations start

        start_time = time.time()

        result = subprocess.run(
            ["./dev_tools/build.sh", "quality-gate", "--coverage-threshold", "0"],
            check=False,
            capture_output=True,
            text=True,
            cwd=Path(__file__).parent.parent,
            timeout=10,  # Should fail fast
        )

        elapsed = time.time() - start_time

        # Should fail quickly on invalid input (under 5 seconds)
        assert elapsed < 5.0, f"Should fail fast on invalid threshold, took {elapsed:.1f}s"
        assert result.returncode == 1, "Should reject zero threshold"


class TestTDDIntegrationFast:
    """Fast integration tests that avoid hanging."""

    def test_build_system_components_exist(self):
        """GREEN: Test all build system components exist and are accessible."""
        project_root = Path(__file__).parent.parent

        # Check key files exist
        required_files = [
            "dev_tools/build.sh",
            "pyproject.toml",
            "dev_tools/build_system.py",
        ]

        for file_path in required_files:
            full_path = project_root / file_path
            assert full_path.exists(), f"Required file should exist: {file_path}"
            assert full_path.is_file(), f"Should be a file: {file_path}"

        # Check build script is executable
        build_script = project_root / "dev_tools" / "build.sh"
        assert build_script.stat().st_mode & 0o111, "Build script should be executable"

    def test_python_imports_work(self):
        """GREEN: Test critical Python imports work."""
        try:
            # Test core imports
            from build_system import BuildManager

            assert BuildManager is not None, "BuildManager should be importable"

        except ImportError as e:
            assert False, f"Core imports should work: {e}"

    def test_subprocess_timeout_handling(self):
        """GREEN: Test our tests can handle timeouts gracefully."""
        # This is a meta-test to ensure our test suite handles hanging processes
        start_time = time.time()

        try:
            result = subprocess.run(
                ["sleep", "2"],  # Simple 2-second command
                check=False,
                capture_output=True,
                text=True,
                timeout=1,  # 1-second timeout to test timeout handling
            )
            assert False, "Should have timed out"
        except subprocess.TimeoutExpired:
            elapsed = time.time() - start_time
            assert elapsed < 2.0, "Timeout should happen quickly"
            # This is expected - our timeout handling works
