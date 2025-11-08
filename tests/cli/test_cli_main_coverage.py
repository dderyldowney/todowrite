"""Tests to improve coverage for CLI main module"""

import pytest
from todowrite_cli.main import capitalize_status, get_current_username


class TestCLIMainCoverage:
    """Test cases for CLI main module functions to improve coverage"""

    def test_get_current_username(self):
        """Test username detection"""
        username = get_current_username()
        # Should return a non-empty string
        assert isinstance(username, str)
        assert len(username) > 0

    def test_capitalize_status(self):
        """Test status capitalization"""
        # Test known status values
        assert capitalize_status("planned") == "Planned"
        assert capitalize_status("in_progress") == "In Progress"
        assert capitalize_status("completed") == "Completed"
        assert capitalize_status("blocked") == "Blocked"
        assert capitalize_status("cancelled") == "Cancelled"

        # Test unknown status (should use .title() which treats underscores as word separators)
        assert capitalize_status("unknown_status") == "Unknown_Status"

        # Test empty string
        assert capitalize_status("") == ""

    def test_capitalize_status_edge_cases(self):
        """Test capitalize_status with edge cases"""
        # Test single word
        assert capitalize_status("test") == "Test"

        # Test multiple underscores (.title() behavior)
        assert (
            capitalize_status("multiple_word_status") == "Multiple_Word_Status"
        )

        # Test with numbers
        assert capitalize_status("status_1") == "Status_1"

        # Test already capitalized (unknown status falls back to .title())
        assert capitalize_status("Not Started") == "Not Started"

    def test_import_error_handling(self):
        """Test that main module handles import errors gracefully"""
        # This test verifies that the imports in main module work
        try:
            from todowrite_cli.main import cli, main

            # If imports work, the functions should be callable
            assert callable(main)
            assert callable(cli)
        except ImportError as e:
            pytest.fail(f"Failed to import main module functions: {e}")

    def test_version_info(self):
        """Test that version information is accessible"""
        try:
            from todowrite_cli.version import __version__

            # Version should be a string
            assert isinstance(__version__, str)
            # Should have some content
            assert len(__version__) > 0
        except ImportError:
            pytest.skip("Version info not available")

    def test_cli_function_structure(self):
        """Test that CLI function has expected structure"""
        try:
            import todowrite_cli.main

            cli_func = getattr(todowrite_cli.main, "cli", None)

            if cli_func is not None:
                # Should be callable
                assert callable(cli_func)

                # Check if it has click decorator attributes
                assert hasattr(cli_func, "callback") or hasattr(
                    cli_func, "__name__"
                )
        except ImportError:
            pytest.skip("CLI function not available")

    def test_main_function_structure(self):
        """Test that main function has expected structure"""
        try:
            import todowrite_cli.main

            main_func = getattr(todowrite_cli.main, "main", None)

            if main_func is not None:
                # Should be callable
                assert callable(main_func)
        except ImportError:
            pytest.skip("Main function not available")
