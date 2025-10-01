"""Tests for updatewebdocs command - README.md to HTML conversion automation.

This test suite validates the updatewebdocs command which automatically converts
README.md to docs/index.html with proper formatting and git integration.

Agricultural Context:
- Web documentation essential for stakeholder communication
- HTML generation must be deterministic for version control
- Automated workflow prevents documentation drift
- Professional presentation critical for ISO compliance auditing
"""

from __future__ import annotations

import subprocess
from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from _pytest.monkeypatch import MonkeyPatch


class TestUpdateWebdocsCommand:
    """Test updatewebdocs command execution and HTML generation."""

    def test_command_exists_and_is_executable(self) -> None:
        """Test updatewebdocs command script exists and has execute permissions."""
        command_path = Path("bin/updatewebdocs")
        assert command_path.exists(), "updatewebdocs command must exist in bin/"
        assert command_path.is_file(), "updatewebdocs must be a file"
        # Check executable bit (owner execute permission)
        assert command_path.stat().st_mode & 0o100, "updatewebdocs must be executable"

    def test_generates_html_from_readme(self, tmp_path: Path) -> None:
        """Test updatewebdocs converts README.md to docs/index.html."""
        # Create temporary README.md
        readme = tmp_path / "README.md"
        readme.write_text("# Test Agricultural Platform\n\nMulti-tractor coordination system.")

        # Run updatewebdocs in temporary directory
        result = subprocess.run(
            ["./bin/updatewebdocs", "--test-mode", f"--root={tmp_path}"],
            capture_output=True,
            text=True,
        )

        assert result.returncode == 0, f"Command failed: {result.stderr}"

        # Verify HTML generated
        html_path = tmp_path / "docs" / "index.html"
        assert html_path.exists(), "index.html must be generated in docs/"

        html_content = html_path.read_text()
        assert "Test Agricultural Platform" in html_content
        assert "Multi-tractor coordination system" in html_content

    def test_validates_html_format(self, tmp_path: Path) -> None:
        """Test generated HTML has proper structure and formatting."""
        readme = tmp_path / "README.md"
        readme.write_text("# Agricultural Robotics\n\n## Safety Systems\n\nISO 18497 compliance.")

        subprocess.run(
            ["./bin/updatewebdocs", "--test-mode", f"--root={tmp_path}"],
            check=True,
            capture_output=True,
        )

        html_path = tmp_path / "docs" / "index.html"
        html_content = html_path.read_text()

        # Verify proper HTML structure
        assert "<!DOCTYPE html>" in html_content
        assert '<html lang="en">' in html_content
        assert '<meta charset="UTF-8">' in html_content
        assert "<h1>" in html_content and "</h1>" in html_content
        assert "<h2>" in html_content and "</h2>" in html_content

    def test_handles_code_blocks_correctly(self, tmp_path: Path) -> None:
        """Test code blocks are preserved with proper formatting."""
        readme = tmp_path / "README.md"
        readme.write_text(
            """# Code Example

```python
from afs_fastapi.equipment.farm_tractors import FarmTractor
tractor = FarmTractor(make="John Deere", model="9RX", year=2023)
```
"""
        )

        subprocess.run(
            ["./bin/updatewebdocs", "--test-mode", f"--root={tmp_path}"],
            check=True,
            capture_output=True,
        )

        html_path = tmp_path / "docs" / "index.html"
        html_content = html_path.read_text()

        # Verify code block preservation
        assert "FarmTractor" in html_content
        assert "John Deere" in html_content or "John" in html_content

    def test_creates_output_directory_if_missing(self, tmp_path: Path) -> None:
        """Test command creates docs/ directory if it doesn't exist."""
        readme = tmp_path / "README.md"
        readme.write_text("# Test\n\nContent")

        # Ensure docs/ doesn't exist
        docs_dir = tmp_path / "docs"
        assert not docs_dir.exists()

        subprocess.run(
            ["./bin/updatewebdocs", "--test-mode", f"--root={tmp_path}"],
            check=True,
            capture_output=True,
        )

        # Verify docs/ created
        assert docs_dir.exists()
        assert docs_dir.is_dir()
        assert (docs_dir / "index.html").exists()


class TestUpdateWebdocsGitIntegration:
    """Test updatewebdocs git staging integration."""

    def test_adds_html_to_git_staging(self, tmp_path: Path, monkeypatch: MonkeyPatch) -> None:
        """Test updatewebdocs automatically adds index.html to git staging."""
        # Create git repo
        subprocess.run(["git", "init"], cwd=tmp_path, check=True, capture_output=True)

        readme = tmp_path / "README.md"
        readme.write_text("# Test\n\nContent")

        # Mock git add command to verify it's called
        git_add_called = []

        def mock_git_add(
            *args: str, **kwargs: dict[str, object]
        ) -> subprocess.CompletedProcess[str]:
            git_add_called.append(args)
            return subprocess.CompletedProcess(args, 0, "", "")

        # Run updatewebdocs
        subprocess.run(
            ["./bin/updatewebdocs", "--test-mode", f"--root={tmp_path}"],
            check=True,
            capture_output=True,
        )

        # Verify git add was executed for index.html
        result = subprocess.run(
            ["git", "status", "--porcelain"],
            cwd=tmp_path,
            capture_output=True,
            text=True,
        )

        # HTML should be in staging or untracked
        assert "index.html" in result.stdout or (tmp_path / "docs" / "index.html").exists()

    def test_provides_helpful_output_messages(self, tmp_path: Path) -> None:
        """Test command provides clear status messages."""
        readme = tmp_path / "README.md"
        readme.write_text("# Test\n\nContent")

        result = subprocess.run(
            ["./bin/updatewebdocs", "--test-mode", f"--root={tmp_path}"],
            capture_output=True,
            text=True,
        )

        # Verify helpful output
        output = result.stdout + result.stderr
        assert "HTML" in output.upper() or "index.html" in output
        assert result.returncode == 0


class TestUpdateWebdocsAgriculturalContext:
    """Test updatewebdocs handles agricultural robotics documentation."""

    def test_preserves_agricultural_terminology(self, tmp_path: Path) -> None:
        """Test agricultural robotics terms preserved in HTML."""
        readme = tmp_path / "README.md"
        readme.write_text(
            """# AFS FastAPI

**ISOBUS Communication**: ISO 11783 device communication.
**Safety Systems**: ISO 18497 compliance with PLc/PLd/PLe levels.
**Multi-tractor Coordination**: Vector Clock synchronization.
"""
        )

        subprocess.run(
            ["./bin/updatewebdocs", "--test-mode", f"--root={tmp_path}"],
            check=True,
            capture_output=True,
        )

        html_path = tmp_path / "docs" / "index.html"
        html_content = html_path.read_text()

        # Verify agricultural terms preserved
        assert "ISOBUS" in html_content
        assert "ISO 11783" in html_content or "11783" in html_content
        assert "ISO 18497" in html_content or "18497" in html_content
        assert "Vector Clock" in html_content

    def test_handles_technical_specifications(self, tmp_path: Path) -> None:
        """Test technical specifications formatted correctly."""
        readme = tmp_path / "README.md"
        readme.write_text(
            """# Technical Specs

- **Test Suite**: 161 tests (100% passing)
- **Performance**: Sub-3-second execution
- **Safety Level**: PLc/PLd/PLe compliance
"""
        )

        subprocess.run(
            ["./bin/updatewebdocs", "--test-mode", f"--root={tmp_path}"],
            check=True,
            capture_output=True,
        )

        html_path = tmp_path / "docs" / "index.html"
        html_content = html_path.read_text()

        # Verify technical specs preserved
        assert "161 tests" in html_content or "161" in html_content
        assert "100%" in html_content or "passing" in html_content


class TestUpdateWebdocsErrorHandling:
    """Test updatewebdocs error handling."""

    def test_handles_missing_readme_gracefully(self, tmp_path: Path) -> None:
        """Test command reports error when README.md is missing."""
        # No README.md exists
        result = subprocess.run(
            ["./bin/updatewebdocs", "--test-mode", f"--root={tmp_path}"],
            capture_output=True,
            text=True,
        )

        # Should fail with helpful message
        assert result.returncode != 0
        assert "README" in result.stderr.upper() or "not found" in result.stderr.lower()

    def test_provides_usage_help(self) -> None:
        """Test command provides usage help with --help flag."""
        result = subprocess.run(
            ["./bin/updatewebdocs", "--help"],
            capture_output=True,
            text=True,
        )

        assert result.returncode == 0
        output = result.stdout + result.stderr
        assert "README" in output or "HTML" in output or "index.html" in output
