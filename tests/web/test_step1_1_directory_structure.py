"""
RED PHASE: Tests for Step 1.1 - Create web_package directory structure
These tests MUST FAIL before implementation exists.
NO MOCKING ALLOWED - Tests will use real file system.
"""

from __future__ import annotations

import pathlib


class TestWebPackageDirectoryStructure:
    """Test that web_package directory structure is created correctly."""

    def test_web_package_root_directory_exists(self) -> None:
        """RED: Test that web_package root directory exists."""
        web_package_path: pathlib.Path = pathlib.Path("web_package")
        assert web_package_path.exists(), "web_package directory should exist"
        assert web_package_path.is_dir(), "web_package should be a directory"

    def test_backend_directory_structure(self):
        """RED: Test that backend directory structure exists."""
        backend_path = pathlib.Path("web_package/backend")
        assert (
            backend_path.exists()
        ), "web_package/backend directory should exist"
        assert (
            backend_path.is_dir()
        ), "web_package/backend should be a directory"

    def test_backend_src_structure(self):
        """RED: Test that backend/src/todowrite_web structure exists."""
        backend_src_path = pathlib.Path(
            "web_package/backend/src/todowrite_web"
        )
        assert (
            backend_src_path.exists()
        ), "web_package/backend/src/todowrite_web should exist"
        assert (
            backend_src_path.is_dir()
        ), "web_package/backend/src/todowrite_web should be a directory"

    def test_backend_init_file_exists(self):
        """RED: Test that backend __init__.py exists."""
        init_path = pathlib.Path(
            "web_package/backend/src/todowrite_web/__init__.py"
        )
        assert (
            init_path.exists()
        ), "web_package/backend/src/todowrite_web/__init__.py should exist"
        assert (
            init_path.is_file()
        ), "web_package/backend/src/todowrite_web/__init__.py should be a file"

    def test_backend_main_py_exists(self):
        """RED: Test that backend main.py exists."""
        main_path = pathlib.Path(
            "web_package/backend/src/todowrite_web/main.py"
        )
        assert (
            main_path.exists()
        ), "web_package/backend/src/todowrite_web/main.py should exist"
        assert (
            main_path.is_file()
        ), "web_package/backend/src/todowrite_web/main.py should be a file"

    def test_frontend_directory_structure(self):
        """RED: Test that frontend directory structure exists."""
        frontend_path = pathlib.Path("web_package/frontend")
        assert (
            frontend_path.exists()
        ), "web_package/frontend directory should exist"
        assert (
            frontend_path.is_dir()
        ), "web_package/frontend should be a directory"

    def test_frontend_src_structure(self):
        """RED: Test that frontend/src structure exists."""
        frontend_src_path = pathlib.Path("web_package/frontend/src")
        assert (
            frontend_src_path.exists()
        ), "web_package/frontend/src directory should exist"
        assert (
            frontend_src_path.is_dir()
        ), "web_package/frontend/src should be a directory"

    def test_frontend_public_structure(self):
        """RED: Test that frontend/public structure exists."""
        frontend_public_path = pathlib.Path("web_package/frontend/public")
        assert (
            frontend_public_path.exists()
        ), "web_package/frontend/public directory should exist"
        assert (
            frontend_public_path.is_dir()
        ), "web_package/frontend/public should be a directory"

    def test_frontend_index_html_exists(self):
        """RED: Test that frontend index.html exists."""
        index_path = pathlib.Path("web_package/frontend/public/index.html")
        assert (
            index_path.exists()
        ), "web_package/frontend/public/index.html should exist"
        assert (
            index_path.is_file()
        ), "web_package/frontend/public/index.html should be a file"

    def test_shared_directory_exists(self):
        """RED: Test that shared directory exists."""
        shared_path = pathlib.Path("web_package/shared")
        assert (
            shared_path.exists()
        ), "web_package/shared directory should exist"
        assert shared_path.is_dir(), "web_package/shared should be a directory"

    def test_docker_compose_exists(self):
        """RED: Test that docker-compose.yml exists."""
        docker_path = pathlib.Path("web_package/docker-compose.yml")
        assert (
            docker_path.exists()
        ), "web_package/docker-compose.yml should exist"
        assert (
            docker_path.is_file()
        ), "web_package/docker-compose.yml should be a file"

    def test_nginx_conf_exists(self):
        """RED: Test that nginx.conf exists."""
        nginx_path = pathlib.Path("web_package/nginx.conf")
        assert nginx_path.exists(), "web_package/nginx.conf should exist"
        assert nginx_path.is_file(), "web_package/nginx.conf should be a file"

    def test_backend_pyproject_toml_exists(self):
        """RED: Test that backend pyproject.toml exists."""
        pyproject_path = pathlib.Path("web_package/backend/pyproject.toml")
        assert (
            pyproject_path.exists()
        ), "web_package/backend/pyproject.toml should exist"
        assert (
            pyproject_path.is_file()
        ), "web_package/backend/pyproject.toml should be a file"

    def test_frontend_package_json_exists(self):
        """RED: Test that frontend package.json exists."""
        package_json_path = pathlib.Path("web_package/frontend/package.json")
        assert (
            package_json_path.exists()
        ), "web_package/frontend/package.json should exist"
        assert (
            package_json_path.is_file()
        ), "web_package/frontend/package.json should be a file"

    def test_backend_pyproject_toml_content(self):
        """RED: Test that backend pyproject.toml has required content."""
        pyproject_path = pathlib.Path("web_package/backend/pyproject.toml")
        assert pyproject_path.exists(), "pyproject.toml should exist"

        content = pyproject_path.read_text()
        assert (
            "[tool.poetry]" in content or "[build-system]" in content
        ), "pyproject.toml should have build system"
        assert (
            'name = "todowrite-web"' in content
        ), "pyproject.toml should have correct package name"

    def test_frontend_package_json_content(self):
        """RED: Test that frontend package.json has required content."""
        package_json_path = pathlib.Path("web_package/frontend/package.json")
        assert package_json_path.exists(), "package.json should exist"

        content = package_json_path.read_text()
        assert '"name"' in content, "package.json should have name field"
        assert (
            '"react"' in content or '"next"' in content
        ), "package.json should have React framework"

    def test_readme_exists(self):
        """RED: Test that README.md exists in web_package."""
        readme_path = pathlib.Path("web_package/README.md")
        assert readme_path.exists(), "web_package/README.md should exist"
        assert readme_path.is_file(), "web_package/README.md should be a file"
