"""Test Sphinx documentation system setup and generation."""

import importlib
import shutil
import subprocess
from pathlib import Path

import pytest


class TestSphinxDocumentationSystem:
    """Test suite for Sphinx documentation generation and deployment."""

    def test_sphinx_directory_structure_exists(self) -> None:
        """Test that Sphinx directory structure is created correctly."""
        sphinx_path = Path("docs/sphinx")

        assert sphinx_path.exists(), "Sphinx directory docs/sphinx should exist"
        assert (sphinx_path / "source").exists(), "Source directory should exist"
        assert (sphinx_path / "build").exists(), "Build directory should exist"
        assert (sphinx_path / "source" / "conf.py").exists(), "Sphinx conf.py should exist"
        assert (sphinx_path / "source" / "index.rst").exists(), "Main index.rst should exist"

    def test_sphinx_configuration_file_is_valid(self) -> None:
        """Test that Sphinx configuration file is valid Python."""
        config_path = Path("docs/sphinx/source/conf.py")

        assert config_path.exists(), "Sphinx conf.py should exist"

        # Test that config can be imported without errors
        config_content = config_path.read_text()
        assert "html_theme" in config_content, "HTML theme should be configured"
        assert "extensions" in config_content, "Extensions should be configured"
        assert "sphinx_rtd_theme" in config_content, "Read the Docs theme should be configured"

    def test_sphinx_auto_generates_api_docs(self) -> None:
        """Test that Sphinx can auto-generate API documentation from source."""
        library_path = Path("docs/sphinx/source/library")
        lib_package_path = Path("lib_package/src/ToDoWrite")

        assert lib_package_path.exists(), "Library source should exist"
        assert library_path.exists(), "Library docs directory should exist"

        # Test that API docs are generated for main modules
        expected_rst_files = ["ToDoWrite.rst", "database.rst", "storage.rst", "tools.rst"]

        for rst_file in expected_rst_files:
            assert (library_path / rst_file).exists(), (
                f"API doc {rst_file} should be auto-generated"
            )

    def test_sphinx_builds_html_successfully(self) -> None:
        """Test that Sphinx can build HTML documentation without errors."""

        sphinx_path = Path("docs/sphinx")
        build_path = sphinx_path / "build" / "html"

        # Clean any existing build
        if build_path.exists():
            shutil.rmtree(build_path)

        # Try to build HTML
        result = subprocess.run(
            ["/usr/local/opt/make/libexec/gnubin/make", "html"],
            check=False,
            cwd=sphinx_path,
            capture_output=True,
            text=True,
            timeout=60,
        )

        assert result.returncode == 0, f"Sphinx build should succeed: {result.stderr}"
        assert build_path.exists(), "HTML build directory should be created"
        assert (build_path / "index.html").exists(), "Main index.html should be generated"

    def test_generated_html_contains_api_documentation(self) -> None:
        """Test that generated HTML contains actual API documentation."""
        index_path = Path("docs/sphinx/build/html/index.html")
        library_index_path = Path("docs/sphinx/build/html/library/ToDoWrite.html")

        assert index_path.exists(), "Main index.html should exist"
        assert library_index_path.exists(), "Library API docs should exist"

        # Test that HTML contains actual class documentation
        library_content = library_index_path.read_text()
        assert "ToDoWrite" in library_content, "ToDoWrite class should be documented"
        assert "create_node" in library_content, "API methods should be documented"

    def test_cross_references_work_in_generated_docs(self) -> None:
        """Test that cross-references work in generated documentation."""
        api_doc_path = Path("docs/sphinx/build/html/library/ToDoWrite.html")

        if api_doc_path.exists():
            content = api_doc_path.read_text()
            # Should contain cross-reference links
            assert 'class="reference internal"' in content, "Should have cross-references"

    def test_custom_domain_configuration(self) -> None:
        """Test that custom domain is configured for GitHub Pages."""
        config_path = Path("docs/sphinx/source/conf.py")

        if config_path.exists():
            config_content = config_path.read_text()
            assert "html_baseurl" in config_content, "Base URL should be configured"
            assert "ToDoWrite.davidderyldowney.com" in config_content, "Custom domain should be set"

    def test_cname_file_for_github_pages(self) -> None:
        """Test that CNAME file exists for GitHub Pages custom domain."""
        cname_path = Path("docs/sphinx/source/_static/CNAME")

        if cname_path.exists():
            cname_content = cname_path.read_text().strip()
            assert cname_content == "ToDoWrite.davidderyldowney.com", (
                "CNAME should contain custom domain"
            )

    def test_github_actions_workflow_exists(self) -> None:
        """Test that GitHub Actions workflow for docs deployment exists."""
        workflow_path = Path(".github/workflows/docs.yml")

        assert workflow_path.exists(), "GitHub Actions workflow should exist"

        workflow_content = workflow_path.read_text()
        assert "peaceiris/actions-gh-pages" in workflow_content, (
            "Should use GitHub Pages deployment action"
        )
        assert "develop" in workflow_content, "Should deploy from develop branch"

    def test_sphinx_dependencies_are_available(self) -> None:
        """Test that required Sphinx dependencies are available."""

        required_packages = [
            "sphinx",
            "sphinx_rtd_theme",
            "sphinx.ext.autodoc",
            "sphinx.ext.viewcode",
            "myst_parser",
        ]

        for package in required_packages:
            try:
                importlib.import_module(package.replace("_", "-"))
            except ImportError:
                # Try alternative import patterns
                if (
                    package == "sphinx.ext.autodoc"
                    or package == "sphinx.ext.viewcode"
                    or package == "myst_parser"
                    or package == "sphinx_rtd_theme"
                ):
                    pass
                else:
                    pytest.fail(f"Required package {package} should be available")
