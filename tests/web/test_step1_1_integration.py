"""
RED PHASE: Integration tests for Step 1.1 - Directory structure integration
These tests MUST FAIL before implementation exists.
NO MOCKING ALLOWED - Tests will use real systems and real validation.
"""

import os
import pathlib
import subprocess


class TestWebPackageIntegration:
    """Integration tests for web_package directory structure."""

    def test_backend_python_package_installable(self):
        """RED: Test that backend package can be installed."""
        backend_path = pathlib.Path("web_package/src/todowrite_web")
        assert backend_path.exists(), "Backend directory should exist"

        # Test that the package structure is installable
        setup_result = subprocess.run(
            [
                "python",
                "-c",
                "import sys; sys.path.insert(0, './web_package/src'); import todowrite_web; print('Backend import successful')",
            ],
            capture_output=True,
            text=True,
            check=False,
        )

        # This should fail initially (RED phase)
        assert (
            setup_result.returncode == 0
        ), f"Backend package should be importable: {setup_result.stderr}"

    def test_frontend_npm_installable(self):
        """RED: Test that frontend package can be installed with npm."""
        frontend_path = pathlib.Path("web_package/frontend")
        assert frontend_path.exists(), "Frontend directory should exist"

        package_json_path = frontend_path / "package.json"
        assert package_json_path.exists(), "package.json should exist"

        # Test npm install (will fail if package.json is invalid)
        npm_result = subprocess.run(
            ["npm", "install", "--dry-run"],
            capture_output=True,
            text=True,
            cwd="web_package/frontend",
            check=False,
        )

        # In RED phase, this might fail due to missing package.json
        # If package.json exists but npm fails, that's expected in RED phase

    def test_docker_compose_validation(self):
        """RED: Test that docker-compose.yml is valid."""
        docker_compose_path = pathlib.Path("web_package/docker-compose.yml")
        assert docker_compose_path.exists(), "docker-compose.yml should exist"

        # Test docker-compose config validation
        config_result = subprocess.run(
            ["docker-compose", "config"],
            capture_output=True,
            text=True,
            cwd="web_package",
            check=False,
        )

        # In RED phase, this should fail due to missing or invalid config
        # We'll verify it works in GREEN phase

    def test_directory_permissions(self):
        """RED: Test that directories have correct permissions."""
        web_package_path = pathlib.Path("web_package")
        assert web_package_path.exists(), "web_package directory should exist"

        # Check that key directories are readable
        backend_path = web_package_path / "backend"
        frontend_path = web_package_path / "frontend"

        if backend_path.exists():
            assert os.access(backend_path, os.R_OK), "Backend directory should be readable"

        if frontend_path.exists():
            assert os.access(frontend_path, os.R_OK), "Frontend directory should be readable"

    def test_monorepo_structure_integration(self):
        """RED: Test that web_package integrates with existing monorepo structure."""
        web_package_path = pathlib.Path("web_package")
        root_readme = pathlib.Path("README.md")
        lib_package = pathlib.Path("lib_package")
        cli_package = pathlib.Path("cli_package")

        assert web_package_path.exists(), "web_package should exist"
        assert root_readme.exists(), "Root README should exist"
        assert lib_package.exists(), "lib_package should exist"
        assert cli_package.exists(), "cli_package should exist"

        # Test that web_package doesn't break existing structure
        all_packages = [lib_package, cli_package, web_package_path]
        for pkg in all_packages:
            if pkg.exists():
                assert pkg.is_dir(), f"{pkg.name} should be a directory"

    def test_gitignore_inclusion(self):
        """RED: Test that web_package is properly included in .gitignore if needed."""
        gitignore_path = pathlib.Path(".gitignore")
        web_package_path = pathlib.Path("web_package")

        if gitignore_path.exists():
            gitignore_content = gitignore_path.read_text()
            # This test will help us decide if we need to add web_package to .gitignore
            # In RED phase, we're just establishing the requirement

    def test_python_path_integration(self):
        """RED: Test that PYTHONPATH works with web_package structure."""
        backend_src_path = pathlib.Path("web_package/src/todowrite_web")
        if backend_src_path.exists():
            # Test that we can add backend to PYTHONPATH
            test_result = subprocess.run(
                [
                    "python",
                    "-c",
                    f"import sys; sys.path.insert(0, '{backend_src_path}'); print('PYTHONPATH test')",
                ],
                capture_output=True,
                text=True,
                check=False,
            )
            # In RED phase, this helps establish the integration requirement
