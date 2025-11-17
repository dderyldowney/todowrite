"""Test documentation organization and integration."""

from pathlib import Path


class TestDocumentationOrganization:
    """Test suite for documentation reorganization and integration."""

    def test_new_docs_directory_structure_exists(self) -> None:
        """Test that the new docs directory structure is created."""
        docs_root = Path("docs")

        # Check main directories exist
        assert (docs_root / "README.md").exists(), "docs/README.md should exist"
        assert (docs_root / "sphinx").exists(), "docs/sphinx should exist"

        # Check new organizational directories
        assert (docs_root / "library").exists(), "docs/library should exist"
        assert (docs_root / "cli").exists(), "docs/cli should exist"
        assert (docs_root / "shared").exists(), "docs/shared should exist"

        # Check shared subdirectories
        assert (docs_root / "shared" / "development").exists(), (
            "docs/shared/development should exist"
        )
        assert (docs_root / "shared" / "release").exists(), "docs/shared/release should exist"
        assert (docs_root / "shared" / "contributing").exists(), (
            "docs/shared/contributing should exist"
        )

    def test_development_docs_moved_to_shared_development(self) -> None:
        """Test that development-specific docs are moved to shared/development."""
        shared_dev = Path("docs/shared/development")

        # Key development docs should be moved
        assert (shared_dev / "BUILD_SYSTEM.md").exists(), (
            "BUILD_SYSTEM.md should be in shared/development"
        )
        assert (shared_dev / "DEVELOPMENT_WORKFLOW.md").exists(), (
            "DEVELOPMENT_WORKFLOW.md should be in shared/development"
        )
        assert (shared_dev / "ENFORCEMENT_SYSTEM.md").exists(), (
            "ENFORCEMENT_SYSTEM.md should be in shared/development"
        )
        assert (shared_dev / "CLAUDE_AUTO_GUIDE.md").exists(), (
            "CLAUDE_AUTO_GUIDE.md should be in shared/development"
        )

    def test_release_docs_moved_to_shared_release(self) -> None:
        """Test that release-specific docs are moved to shared/release."""
        shared_release = Path("docs/shared/release")

        # Release docs should be moved
        assert (shared_release / "RELEASE_WORKFLOW.md").exists(), (
            "RELEASE_WORKFLOW.md should be in shared/release"
        )
        assert (shared_release / "PyPI_HOWTO.md").exists(), (
            "PyPI_HOWTO.md should be in shared/release"
        )
        assert (shared_release / "VERSION_MANAGEMENT.md").exists(), (
            "VERSION_MANAGEMENT.md should be in shared/release"
        )

    def test_cli_docs_moved_to_cli_directory(self) -> None:
        """Test that CLI-specific docs are moved to cli/ directory."""
        cli_dir = Path("docs/cli")

        # CLI docs should be moved
        assert (cli_dir / "README.md").exists(), "cli/README.md should exist"
        assert (cli_dir / "ZSH_INTEGRATION.md").exists(), "ZSH_INTEGRATION.md should be in cli/"

    def test_library_docs_directory_structure(self) -> None:
        """Test that library docs directory has proper structure."""
        lib_dir = Path("docs/library")

        # Library directory should have subdirectories
        assert (lib_dir / "README.md").exists(), "library/README.md should exist"
        assert (lib_dir / "guides").exists(), "library/guides should exist"
        assert (lib_dir / "examples").exists(), "library/examples should exist"

    def test_archive_directory_created(self) -> None:
        """Test that archive directory exists for historical docs."""
        archive_dir = Path("docs/shared/archive")
        assert archive_dir.exists(), "docs/shared/archive should exist"

    def test_duplicated_files_removed_from_docs_root(self) -> None:
        """Test that duplicate/old files are removed from docs root."""
        docs_root = Path("docs")

        # Files that should have been moved or archived
        files_that_should_be_gone = [
            "BUILD_SYSTEM.md",
            "DEVELOPMENT_WORKFLOW.md",
            "ENFORCEMENT_SYSTEM.md",
            "installation.md",  # duplicate we identified
        ]

        for file_name in files_that_should_be_gone:
            assert not (docs_root / file_name).exists(), (
                f"{file_name} should be removed from docs root"
            )

    def test_sphinx_can_include_markdown_files(self) -> None:
        """Test that Sphinx configuration supports markdown files."""
        config_path = Path("docs/sphinx/source/conf.py")

        if config_path.exists():
            config_content = config_path.read_text()
            assert "myst_parser" in config_content, (
                "myst_parser should be configured for markdown support"
            )

    def test_docs_root_readme_is_navigation_hub(self) -> None:
        """Test that docs/README.md serves as navigation hub."""
        docs_readme = Path("docs/README.md")

        if docs_readme.exists():
            content = docs_readme.read_text()
            # Should reference the new structure
            assert "library/" in content, "Should reference library/"
            assert "cli/" in content, "Should reference cli/"
            assert "shared/" in content, "Should reference shared/"
            assert "sphinx/" in content, "Should reference sphinx/"

    def test_no_duplicate_installation_files(self) -> None:
        """Test that we don't have duplicate installation guides."""
        docs_root = Path("docs")

        # Should only have one installation guide in the right place
        installation_files = list(docs_root.glob("**/INSTALLATION_GUIDE.md"))
        installation_files.extend(docs_root.glob("**/installation.md"))

        # Should not have both files - we decided to consolidate
        assert len(installation_files) <= 1, "Should not have duplicate installation files"
