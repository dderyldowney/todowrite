"""
RED PHASE: Tests for Step 1.1 - Backend Directory Structure
These tests MUST FAIL before implementation exists.
NO MOCKING ALLOWED - Tests will use real file system.
"""

from __future__ import annotations

import pathlib


class TestWebPackageBackendDirectoryStructure:
    """Test that web_package backend directory structure is created correctly."""

    def test_web_package_root_directory_exists(self) -> None:
        """RED: Test that web_package root directory exists."""
        web_package_path: pathlib.Path = pathlib.Path("web_package")
        assert web_package_path.exists(), "web_package directory should exist"
        assert web_package_path.is_dir(), "web_package should be a directory"

    def test_backend_directory_structure(self) -> None:
        """RED: Test that backend directory structure exists."""
        backend_path: pathlib.Path = pathlib.Path(
            "web_package/src/todowrite_web"
        )
        assert (
            backend_path.exists()
        ), "web_package/src/todowrite_web directory should exist"
        assert (
            backend_path.is_dir()
        ), "web_package/src/todowrite_web should be a directory"

    def test_backend_src_structure(self) -> None:
        """RED: Test that backend/src/todowrite_web structure exists."""
        backend_src_path: pathlib.Path = pathlib.Path(
            "web_package/src/todowrite_web"
        )
        assert (
            backend_src_path.exists()
        ), "web_package/src/todowrite_web should exist"
        assert (
            backend_src_path.is_dir()
        ), "web_package/src/todowrite_web should be a directory"

    def test_backend_init_file_exists(self) -> None:
        """RED: Test that backend __init__.py exists."""
        init_path: pathlib.Path = pathlib.Path(
            "web_package/src/todowrite_web/__init__.py"
        )
        assert (
            init_path.exists()
        ), "web_package/src/todowrite_web/__init__.py should exist"
        assert (
            init_path.is_file()
        ), "web_package/src/todowrite_web/__init__.py should be a file"

    def test_backend_main_py_exists(self) -> None:
        """RED: Test that backend main.py exists."""
        main_path: pathlib.Path = pathlib.Path(
            "web_package/src/todowrite_web/main.py"
        )
        assert (
            main_path.exists()
        ), "web_package/src/todowrite_web/main.py should exist"
        assert (
            main_path.is_file()
        ), "web_package/src/todowrite_web/main.py should be a file"

    def test_backend_pyproject_toml_exists(self) -> None:
        """RED: Test that backend pyproject.toml exists."""
        pyproject_path: pathlib.Path = pathlib.Path(
            "web_package/src/todowrite_web/pyproject.toml"
        )
        assert (
            pyproject_path.exists()
        ), "web_package/src/todowrite_web/pyproject.toml should exist"
        assert (
            pyproject_path.is_file()
        ), "web_package/src/todowrite_web/pyproject.toml should be a file"

    def test_backend_pyproject_toml_content(self) -> None:
        """RED: Test that backend pyproject.toml has required content."""
        pyproject_path: pathlib.Path = pathlib.Path(
            "web_package/src/todowrite_web/pyproject.toml"
        )
        assert pyproject_path.exists(), "pyproject.toml should exist"

        content: str = pyproject_path.read_text()
        assert (
            "[tool.poetry]" in content or "[build-system]" in content
        ), "pyproject.toml should have build system"
        assert (
            'name = "todowrite-web"' in content
        ), "pyproject.toml should have correct package name"

    def test_backend_api_structure(self) -> None:
        """RED: Test that backend API directory structure exists."""
        api_path: pathlib.Path = pathlib.Path(
            "web_package/src/todowrite_web/api"
        )
        assert api_path.exists(), "Backend API directory should exist"
        assert api_path.is_dir(), "Backend API directory should be a directory"

    def test_backend_api_v1_structure(self) -> None:
        """RED: Test that backend API v1 directory structure exists."""
        api_v1_path: pathlib.Path = pathlib.Path(
            "web_package/src/todowrite_web/api/v1"
        )
        assert api_v1_path.exists(), "Backend API v1 directory should exist"
        assert (
            api_v1_path.is_dir()
        ), "Backend API v1 directory should be a directory"

    def test_backend_init_files_in_api_structure(self) -> None:
        """RED: Test that __init__.py files exist in API structure."""
        api_inits: list[pathlib.Path] = [
            pathlib.Path("web_package/src/todowrite_web/api/__init__.py"),
            pathlib.Path("web_package/src/todowrite_web/api/v1/__init__.py"),
        ]

        for init_file in api_inits:
            assert (
                init_file.exists()
            ), f"API init file should exist: {init_file}"
            assert (
                init_file.is_file()
            ), f"API init should be a file: {init_file}"
