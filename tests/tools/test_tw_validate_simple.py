"""Simple tests for tw_validate main function"""

import os
import sys
import tempfile
from pathlib import Path

import pytest

from todowrite.tools.tw_validate import main


class TestTwValidateMain:
    """Test cases for tw_validate main function"""

    def test_main_help_option(self):
        """Test that main function handles help option"""
        with pytest.raises(SystemExit) as excinfo:
            # Save original argv
            original_argv = sys.argv
            try:
                sys.argv = ["tw_validate", "--help"]
                main()
            except SystemExit as e:
                # Help option should exit with code 0
                assert e.code == 0
                raise
            finally:
                sys.argv = original_argv

    def test_main_no_files_scenario(self):
        """Test main function behavior when no files exist"""
        with tempfile.TemporaryDirectory() as temp_dir:
            # Create a schema file
            schema_file = Path(temp_dir) / "schema.json"
            schema_file.write_text('{"type": "object"}')

            # Change to temp directory where no configs/plans exists
            original_argv = sys.argv
            original_cwd = os.getcwd()

            try:
                os.chdir(temp_dir)
                sys.argv = ["tw_validate", "--schema", str(schema_file)]
                # Should exit with code 0 when no files found (not an error)
                with pytest.raises(SystemExit) as excinfo:
                    main()
                assert excinfo.value.code == 0
            finally:
                os.chdir(original_cwd)
                sys.argv = original_argv
