"""Utility functions for the AFS FastAPI platform.

This module provides general-purpose utilities including external file viewing
capabilities for documentation and development workflow enhancement.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path
from typing import TypedDict

from .config import get_viewer_config


class ViewerConfig(TypedDict):
    """Type definition for viewer configuration entries."""

    name: str
    command: str | list[str]
    platforms: list[str]
    description: str


class ExternalViewerError(Exception):
    """Exception raised when external viewer operations fail."""

    pass


class MarkdownViewer:
    """External viewer manager for Markdown files.

    Provides functionality to open Markdown files in external applications
    with pre-configured viewers and automatic application detection.

    Agricultural Development Context:
    This utility enhances the documentation workflow for the AFS FastAPI platform,
    allowing developers to easily preview comprehensive documentation files like
    WORKFLOW.md, TDD_WORKFLOW.md, and PROJECT_STRATEGY.md in dedicated Markdown
    editors for better readability during development.
    """

    # Pre-configured viewers with their command patterns
    CONFIGURED_VIEWERS: dict[str, ViewerConfig] = {
        "macdown": {
            "name": "MacDown",
            "command": ["open", "-a", "MacDown"],
            "platforms": ["darwin"],
            "description": "Dedicated Markdown editor with live preview",
        },
        "typora": {
            "name": "Typora",
            "command": ["open", "-a", "Typora"],
            "platforms": ["darwin"],
            "description": "WYSIWYG Markdown editor",
        },
        "mark_text": {
            "name": "Mark Text",
            "command": ["open", "-a", "Mark Text"],
            "platforms": ["darwin"],
            "description": "Real-time preview Markdown editor",
        },
        "vscode": {
            "name": "Visual Studio Code",
            "command": ["code"],
            "platforms": ["darwin", "linux", "win32"],
            "description": "Code editor with Markdown preview extension",
        },
        "default_system": {
            "name": "System Default",
            "command": (
                ["open"]
                if sys.platform == "darwin"
                else (["xdg-open"] if sys.platform.startswith("linux") else ["start"])
            ),
            "platforms": ["darwin", "linux", "win32"],
            "description": "System default application for Markdown files",
        },
    }

    def __init__(self, preferred_viewer: str | None = None) -> None:
        """Initialize the Markdown viewer.

        Args:
            preferred_viewer: Key of preferred viewer from CONFIGURED_VIEWERS.
                            Defaults to configured preference or 'macdown' on macOS systems.
        """
        config = get_viewer_config()
        self.preferred_viewer = (
            preferred_viewer or config.get_preferred_viewer() or self._get_default_viewer()
        )
        self.available_viewers = self._detect_available_viewers()

    def _get_default_viewer(self) -> str:
        """Get the default viewer for the current platform."""
        if sys.platform == "darwin":
            return "macdown"
        elif sys.platform in ("linux", "linux2"):
            return "default_system"
        elif sys.platform == "win32":
            return "default_system"
        else:
            return "default_system"

    def _detect_available_viewers(self) -> list[str]:
        """Detect which configured viewers are available on the system.

        Returns:
            List of viewer keys that are available and compatible with the platform.
        """
        available: list[str] = []
        current_platform = sys.platform

        for viewer_key, config in self.CONFIGURED_VIEWERS.items():
            platforms = config.get("platforms", [])
            if current_platform not in platforms:
                continue

            # For macOS applications, check if they exist
            if current_platform == "darwin" and viewer_key != "default_system":
                app_name = config["command"][2] if len(config["command"]) > 2 else viewer_key
                if self._check_macos_app_exists(app_name):
                    available.append(viewer_key)
            # For command-line tools, check if they're in PATH
            elif viewer_key not in ["macdown", "typora", "mark_text"]:
                command_config = config["command"]

                # Extract the first command element for existence check
                if isinstance(command_config, list):
                    if len(command_config) > 0:
                        command_str = str(command_config[0])
                    else:
                        continue  # Skip empty command list
                else:
                    command_str = str(command_config)

                if self._check_command_exists(command_str):
                    available.append(viewer_key)
            else:
                # Default system viewer is always available
                if viewer_key == "default_system":
                    available.append(viewer_key)

        return available

    def _check_macos_app_exists(self, app_name: str) -> bool:
        """Check if a macOS application exists.

        Args:
            app_name: Name of the application to check.

        Returns:
            True if the application exists, False otherwise.
        """
        try:
            result = subprocess.run(
                ["mdfind", f"kMDItemCFBundleName == '{app_name}'"],
                capture_output=True,
                text=True,
                timeout=5,
            )
            return bool(result.stdout.strip())
        except (subprocess.SubprocessError, subprocess.TimeoutExpired):
            return False

    def _check_command_exists(self, command: str) -> bool:
        """Check if a command exists in the system PATH.

        Args:
            command: Command to check.

        Returns:
            True if the command exists, False otherwise.
        """
        try:
            subprocess.run(
                ["which", command] if sys.platform != "win32" else ["where", command],
                capture_output=True,
                check=True,
                timeout=5,
            )
            return True
        except (subprocess.SubprocessError, subprocess.TimeoutExpired):
            return False

    def open_file(self, file_path: str | Path, viewer: str | None = None) -> bool:
        """Open a Markdown file in an external viewer.

        Args:
            file_path: Path to the Markdown file to open.
            viewer: Specific viewer to use. If None, uses preferred viewer.

        Returns:
            True if file was successfully opened, False otherwise.

        Raises:
            ExternalViewerError: If the file cannot be opened or viewer is not available.

        Agricultural Context:
        Common usage for opening AFS FastAPI documentation files:
        - WORKFLOW.md: Comprehensive testing framework reference
        - TDD_WORKFLOW.md: Test-First development methodology guide
        - PROJECT_STRATEGY.md: Strategic development planning document
        - SESSION_SUMMARY.md: Development session documentation
        """
        file_path = Path(file_path)

        # Validate file exists and is a Markdown file
        if not file_path.exists():
            raise ExternalViewerError(f"File does not exist: {file_path}")

        if file_path.suffix.lower() not in [".md", ".markdown", ".mdown", ".mkd"]:
            raise ExternalViewerError(f"File is not a Markdown file: {file_path}")

        # Determine which viewer to use
        target_viewer = viewer or self.preferred_viewer

        if target_viewer not in self.available_viewers:
            # Fallback to first available viewer
            if self.available_viewers:
                target_viewer = self.available_viewers[0]
            else:
                raise ExternalViewerError("No external viewers available on this system")

        # Get viewer configuration
        if target_viewer not in self.CONFIGURED_VIEWERS:
            raise ExternalViewerError(f"Unknown viewer: {target_viewer}")

        config = self.CONFIGURED_VIEWERS[target_viewer]
        command_template = config["command"]

        # Build command list ensuring all elements are strings
        command: list[str] = []
        if isinstance(command_template, list):
            command = [str(item) for item in command_template]
        else:
            command = [str(command_template)]

        command.append(str(file_path))

        try:
            # Execute the command
            subprocess.run(command, check=True, timeout=10)
            return True
        except subprocess.TimeoutExpired as e:
            raise ExternalViewerError(f"Timeout opening file with {config['name']}") from e
        except subprocess.SubprocessError as e:
            raise ExternalViewerError(f"Failed to open file with {config['name']}: {e}") from e

    def list_available_viewers(self) -> dict[str, dict[str, str | bool]]:
        """List all available viewers with their descriptions.

        Returns:
            Dictionary mapping viewer keys to their configuration info.
        """
        available_info: dict[str, dict[str, str | bool]] = {}
        for viewer_key in self.available_viewers:
            config = self.CONFIGURED_VIEWERS[viewer_key]
            available_info[viewer_key] = {
                "name": str(config["name"]),
                "description": str(config["description"]),
                "is_preferred": viewer_key == self.preferred_viewer,
            }
        return available_info

    def set_preferred_viewer(self, viewer_key: str) -> None:
        """Set the preferred viewer for opening Markdown files.

        Args:
            viewer_key: Key of the viewer to set as preferred.

        Raises:
            ExternalViewerError: If the viewer is not available.
        """
        if viewer_key not in self.available_viewers:
            available = ", ".join(self.available_viewers)
            raise ExternalViewerError(
                f"Viewer '{viewer_key}' is not available. Available viewers: {available}"
            )
        self.preferred_viewer = viewer_key


def open_markdown_file(file_path: str | Path, viewer: str | None = None) -> bool:
    """Convenience function to open a Markdown file in an external viewer.

    Args:
        file_path: Path to the Markdown file to open.
        viewer: Specific viewer to use. If None, uses system default.

    Returns:
        True if file was successfully opened, False otherwise.

    Example:
        >>> # Open WORKFLOW.md in MacDown (if available)
        >>> open_markdown_file("WORKFLOW.md", "macdown")
        True

        >>> # Open using preferred viewer
        >>> open_markdown_file("TDD_WORKFLOW.md")
        True
    """
    try:
        viewer_manager = MarkdownViewer()
        return viewer_manager.open_file(file_path, viewer)
    except ExternalViewerError:
        return False


def list_markdown_viewers() -> dict[str, dict[str, str | bool]]:
    """List all available Markdown viewers on the current system.

    Returns:
        Dictionary with viewer information including names and descriptions.
    """
    viewer_manager = MarkdownViewer()
    return viewer_manager.list_available_viewers()
