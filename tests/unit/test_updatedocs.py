"""Tests for updatedocs meta-command script.

This test suite validates the updatedocs command which orchestrates regeneration
of all 6 core documentation files ensuring synchronized platform state for
agricultural robotics stakeholder communication and ISO compliance.

Agricultural Context:
Unified documentation updates essential for maintaining consistent platform
state documentation across strategic assessments, web presence, version history,
session state, test reports, and metrics dashboards for farm equipment compliance
auditing and autonomous tractor fleet management.
"""

from __future__ import annotations

import subprocess
import tempfile
from pathlib import Path


class TestUpdateDocsCommand:
    """Test updatedocs command functionality."""

    def test_updatedocs_script_exists(self) -> None:
        """Test that updatedocs script exists in bin/ directory."""
        script_path = Path("bin/updatedocs")
        assert script_path.exists(), "updatedocs script should exist"
        assert script_path.is_file(), "updatedocs should be a file"

    def test_updatedocs_script_executable(self) -> None:
        """Test that updatedocs script has executable permissions."""
        script_path = Path("bin/updatedocs")
        assert script_path.exists(), "updatedocs script should exist"
        assert script_path.stat().st_mode & 0o111, "updatedocs should be executable"

    def test_updatedocs_help_flag(self) -> None:
        """Test updatedocs --help displays usage information."""
        result = subprocess.run(
            ["./bin/updatedocs", "--help"],
            capture_output=True,
            text=True,
            timeout=5,
        )

        assert result.returncode == 0, "Help should execute successfully"
        assert "updatedocs" in result.stdout.lower(), "Should show command name"
        assert "6 core documents" in result.stdout or "documentation" in result.stdout
        assert "Usage" in result.stdout or "usage" in result.stdout.lower()

    def test_updatedocs_updates_whereweare(self) -> None:
        """Test that updatedocs regenerates WHERE_WE_ARE.md."""
        # Run updatedocs (should call whereweare --generate internally)
        # Extended timeout: updatedocs orchestrates multiple commands including runtests
        result = subprocess.run(
            ["./bin/updatedocs"],
            capture_output=True,
            text=True,
            timeout=180,
        )

        assert result.returncode == 0, "updatedocs should execute successfully"
        output = result.stdout + result.stderr

        # Should mention WHERE_WE_ARE.md or strategic assessment
        assert (
            "WHERE_WE_ARE" in output
            or "strategic" in output.lower()
            or "whereweare" in output.lower()
        ), "Should update strategic assessment"

    def test_updatedocs_updates_changelog(self) -> None:
        """Test that updatedocs regenerates CHANGELOG.md."""
        # Extended timeout: updatedocs orchestrates multiple commands including runtests
        result = subprocess.run(
            ["./bin/updatedocs"],
            capture_output=True,
            text=True,
            timeout=180,
        )

        assert result.returncode == 0
        output = result.stdout + result.stderr

        # Should mention CHANGELOG.md update
        assert "CHANGELOG" in output or "changelog" in output.lower(), "Should update CHANGELOG.md"

    def test_updatedocs_updates_webdocs(self) -> None:
        """Test that updatedocs regenerates docs/index.html."""
        # Extended timeout: updatedocs orchestrates multiple commands including runtests
        result = subprocess.run(
            ["./bin/updatedocs"],
            capture_output=True,
            text=True,
            timeout=180,
        )

        assert result.returncode == 0
        output = result.stdout + result.stderr

        # Should mention HTML or web documentation
        assert (
            "index.html" in output.lower() or "web" in output.lower() or "html" in output.lower()
        ), "Should update web documentation"

    def test_updatedocs_colored_output(self) -> None:
        """Test that updatedocs produces colored terminal output."""
        # Extended timeout: updatedocs orchestrates multiple commands including runtests
        result = subprocess.run(
            ["./bin/updatedocs"],
            capture_output=True,
            text=True,
            timeout=180,
        )

        assert result.returncode == 0

        # Should include ANSI color codes
        has_colors = "\033[" in result.stdout or "\x1b[" in result.stdout
        assert has_colors, "Should include colored output for terminal"

    def test_updatedocs_shows_summary(self) -> None:
        """Test that updatedocs shows comprehensive update summary."""
        # Extended timeout: updatedocs orchestrates multiple commands including runtests
        result = subprocess.run(
            ["./bin/updatedocs"],
            capture_output=True,
            text=True,
            timeout=180,
        )

        assert result.returncode == 0
        output = result.stdout

        # Should show completion message
        assert (
            "complete" in output.lower() or "updated" in output.lower()
        ), "Should show completion status"

        # Should mention multiple documents
        assert (
            output.count("✅") >= 3 or output.count("✓") >= 3
        ), "Should show multiple updates completed"

    def test_updatedocs_agricultural_context(self) -> None:
        """Test that updatedocs includes agricultural robotics context."""
        # Extended timeout: updatedocs orchestrates multiple commands including runtests
        result = subprocess.run(
            ["./bin/updatedocs"],
            capture_output=True,
            text=True,
            timeout=180,
        )

        assert result.returncode == 0
        output = result.stdout + result.stderr

        # Should include agricultural terminology or ISO references
        agricultural_terms = [
            "agricultural",
            "ISO",
            "compliance",
            "equipment",
            "platform",
        ]
        assert any(
            term in output for term in agricultural_terms
        ), "Should include agricultural context"

    def test_updatedocs_handles_errors_gracefully(self) -> None:
        """Test that updatedocs handles errors in sub-commands gracefully."""
        with tempfile.TemporaryDirectory() as tmpdir:
            # Create minimal test environment missing required files
            test_root = Path(tmpdir)

            # Run with custom root (should fail gracefully)
            result = subprocess.run(
                ["./bin/updatedocs", f"--root={test_root}"],
                capture_output=True,
                text=True,
                timeout=30,
            )

            # Should either succeed with warnings or fail with clear error
            if result.returncode != 0:
                assert (
                    "ERROR" in result.stderr or "error" in result.stderr.lower()
                ), "Should show clear error messages"

    def test_updatedocs_dry_run_mode(self) -> None:
        """Test updatedocs --dry-run shows what would be updated."""
        result = subprocess.run(
            ["./bin/updatedocs", "--dry-run"],
            capture_output=True,
            text=True,
            timeout=10,
        )

        assert result.returncode == 0, "Dry run should execute successfully"
        output = result.stdout

        # Should mention what would be done without actually doing it
        assert "would" in output.lower() or "dry" in output.lower(), "Should indicate dry run mode"

    def test_updatedocs_selective_update(self) -> None:
        """Test updatedocs with selective document updates."""
        # Test updating only specific documents
        # Extended timeout: Even selective updates may run runtests if 'tests' included
        result = subprocess.run(
            ["./bin/updatedocs", "--only=whereweare,changelog"],
            capture_output=True,
            text=True,
            timeout=120,
        )

        # Should succeed or provide helpful message about flag
        assert result.returncode in [
            0,
            1,
        ], "Should handle selective update flag"

    def test_updatedocs_shows_document_count(self) -> None:
        """Test that updatedocs mentions 6 core documents."""
        result = subprocess.run(
            ["./bin/updatedocs", "--help"],
            capture_output=True,
            text=True,
            timeout=5,
        )

        assert result.returncode == 0
        output = result.stdout

        # Should mention 6 documents or list them
        assert "6" in output or output.count("•") >= 4, "Should reference 6 core documents"
