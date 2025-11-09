"""Tests for other tools modules (tw_lint_soc, tw_stub_command, tw_trace)"""

from pathlib import Path

import pytest
from todowrite.tools.tw_lint_soc import main as lint_main
from todowrite.tools.tw_stub_command import main as stub_main
from todowrite.tools.tw_trace import main as trace_main


class TestTwLintSoc:
    """Test cases for tw_lint_soc module"""

    def test_import_module(self):
        """Test that the module can be imported"""
        # If import succeeded at module level, test passes
        assert lint_main is not None

    def test_module_exists(self):
        """Test that the module file exists and has expected content"""
        tools_path = Path("lib_package/src/todowrite/tools/tw_lint_soc.py")
        assert tools_path.exists()
        content = tools_path.read_text()
        # Check that it has some basic expected content
        assert "def main" in content or "if __name__" in content


class TestTwStubCommand:
    """Test cases for tw_stub_command module"""

    def test_import_module(self):
        """Test that the module can be imported"""
        try:
            assert stub_main is not None
        except (ImportError, TypeError):
            pytest.skip("tw_stub_command module not available")

    def test_module_exists(self):
        """Test that the module file exists and has expected content"""
        tools_path = Path("lib_package/src/todowrite/tools/tw_stub_command.py")
        assert tools_path.exists()
        content = tools_path.read_text()
        # Check that it has some basic expected content
        assert "def main" in content or "if __name__" in content


class TestTwTrace:
    """Test cases for tw_trace module"""

    def test_import_module(self):
        """Test that the module can be imported"""
        try:
            assert trace_main is not None
        except (ImportError, TypeError):
            pytest.skip("tw_trace module not available")

    def test_module_exists(self):
        """Test that the module file exists and has expected content"""
        tools_path = Path("lib_package/src/todowrite/tools/tw_trace.py")
        assert tools_path.exists()
        content = tools_path.read_text()
        # Check that it has some basic expected content
        assert "def main" in content or "if __name__" in content


class TestToolsIntegration:
    """Integration tests for tools modules"""

    def test_all_tools_modules_exist(self):
        """Test that all expected tools modules exist"""
        tools_dir = Path("lib_package/src/todowrite/tools")
        expected_modules = [
            "extract_schema.py",
            "tw_lint_soc.py",
            "tw_stub_command.py",
            "tw_trace.py",
            "tw_validate.py",
        ]

        for module_name in expected_modules:
            module_path = tools_dir / module_name
            assert (
                module_path.exists()
            ), f"Expected module {module_name} not found"

    def test_tools_modules_are_python_files(self):
        """Test that tools modules are valid Python files"""
        tools_dir = Path("lib_package/src/todowrite/tools")
        for tool_file in tools_dir.glob("*.py"):
            if tool_file.name != "__init__.py":
                content = tool_file.read_text()
                # Basic Python file checks
                assert (
                    "import" in content
                    or "from" in content
                    or "def" in content
                ), f"Tool file {tool_file.name} doesn't appear to be a valid Python module"
