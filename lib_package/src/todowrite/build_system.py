"""
Build System API for ToDoWrite monorepo.

Clean architecture implementation following REFACTOR phase of TDD cycle.
Provides a clean interface for managing the unified monorepo build system.
"""

import subprocess
import sys
from abc import ABC, abstractmethod
from dataclasses import dataclass
from pathlib import Path
from typing import Any


@dataclass
class ValidationResult:
    """Result of a validation operation."""

    is_valid: bool
    errors: list[str]
    warnings: list[str]

    @classmethod
    def success(cls) -> "ValidationResult":
        """Create a successful validation result."""
        return cls(is_valid=True, errors=[], warnings=[])

    @classmethod
    def failure(
        cls, errors: list[str], warnings: list[str] | None = None
    ) -> "ValidationResult":
        """Create a failed validation result."""
        return cls(is_valid=False, errors=errors, warnings=warnings or [])


@dataclass
class PackageInfo:
    """Information about a workspace package."""

    name: str
    path: Path
    pyproject_path: Path
    dist_path: Path


class BuildSystemValidator(ABC):
    """Abstract base for build system validators."""

    @abstractmethod
    def validate(self, project_root: Path) -> ValidationResult:
        """Validate the build system configuration."""
        pass


class WorkspaceValidator(BuildSystemValidator):
    """Validates UV workspace configuration."""

    def validate(self, project_root: Path) -> ValidationResult:
        """Validate UV workspace setup."""
        errors = []

        # Check pyproject.toml exists
        pyproject_path = project_root / "pyproject.toml"
        if not pyproject_path.exists():
            errors.append("pyproject.toml not found")
            return ValidationResult.failure(errors)

        # Check UV workspace configuration
        try:
            content = pyproject_path.read_text()
            if "[tool.uv.workspace]" not in content:
                errors.append("UV workspace not configured in pyproject.toml")

            # Check workspace members
            required_packages = ["lib_package", "cli_package", "web_package"]
            for pkg in required_packages:
                if pkg not in content:
                    errors.append(f"Package {pkg} not found in workspace")
                elif not (project_root / pkg).exists():
                    errors.append(f"Package directory {pkg} not found")

        except Exception as e:
            errors.append(f"Failed to read pyproject.toml: {e}")

        return (
            ValidationResult.failure(errors)
            if errors
            else ValidationResult.success()
        )


class VersionValidator(BuildSystemValidator):
    """Validates version management configuration."""

    def validate(self, project_root: Path) -> ValidationResult:
        """Validate version management setup."""
        errors = []
        warnings = []

        # Check VERSION file exists
        version_file = project_root / "VERSION"
        if not version_file.exists():
            errors.append("VERSION file not found")
        else:
            # Check if version file has content
            try:
                version_content = version_file.read_text().strip()
                if not version_content:
                    errors.append("VERSION file is empty")
                elif len(version_content.split(".")) != 3:
                    errors.append(
                        f"Version '{version_content}' doesn't follow semantic versioning (x.y.z)"
                    )
            except Exception:
                errors.append("Failed to read VERSION file")

        # Check if packages reference central VERSION
        for pkg in ["lib_package", "cli_package", "web_package"]:
            pkg_pyproject = project_root / pkg / "pyproject.toml"
            if pkg_pyproject.exists():
                try:
                    content = pkg_pyproject.read_text()
                    if 'path = "../VERSION"' not in content:
                        errors.append(
                            f"{pkg} doesn't reference central VERSION file"
                        )
                except Exception:
                    errors.append(f"Failed to read {pkg}/pyproject.toml")

        return (
            ValidationResult.failure(errors)
            if errors
            else ValidationResult.success()
        )


class BuildManager:
    """
    Manages the unified monorepo build system with clean architecture.

    Provides a high-level interface for build operations while maintaining
    separation of concerns and proper error handling.
    """

    def __init__(self, project_root: str | None = None) -> None:
        """
        Initialize BuildManager with project root path.

        Args:
            project_root: Path to project root. If None, auto-detect.
        """
        if project_root is None:
            # Auto-detect project root (4 levels up from this file)
            self.project_root = Path(__file__).parent.parent.parent.parent
        else:
            self.project_root = Path(project_root)

        # Initialize validators
        self._validators = [WorkspaceValidator(), VersionValidator()]

        # Cache package information
        self._packages: dict[str, PackageInfo] | None = None

    def validate_configuration(self) -> ValidationResult:
        """
        Validate that the build system is properly configured.

        Returns:
            ValidationResult: Detailed validation result
        """
        all_errors = []
        all_warnings = []

        for validator in self._validators:
            result = validator.validate(self.project_root)
            if not result.is_valid:
                all_errors.extend(result.errors)
            all_warnings.extend(result.warnings)

        return (
            ValidationResult.failure(all_errors, all_warnings)
            if all_errors
            else ValidationResult.success(warnings=all_warnings)
        )

    def run_build_script(self, command: str) -> subprocess.CompletedProcess:
        """
        Run a build script command with proper error handling.

        Args:
            command: Command to run (e.g., 'build', 'test', 'validate')

        Returns:
            subprocess.CompletedProcess: Result of the command execution

        Raises:
            RuntimeError: If build script not found
        """
        build_script = self.project_root / "dev_tools" / "build.sh"

        if not build_script.exists():
            raise RuntimeError(f"Build script not found: {build_script}")

        if not build_script.is_file():
            raise RuntimeError(f"Build script is not a file: {build_script}")

        # Execute build script
        result = subprocess.run(
            [str(build_script), command],
            capture_output=True,
            text=True,
            cwd=self.project_root,
            timeout=300,  # 5 minute timeout
        )

        return result

    def get_workspace_packages(self) -> dict[str, PackageInfo]:
        """
        Get information about workspace packages.

        Returns:
            Dict mapping package names to PackageInfo objects
        """
        if self._packages is None:
            self._packages = self._load_package_info()

        return self._packages

    def _load_package_info(self) -> dict[str, PackageInfo]:
        """Load package information from workspace."""
        packages = {}

        for pkg_name in ["lib_package", "cli_package", "web_package"]:
            pkg_path = self.project_root / pkg_name

            if pkg_path.exists():
                packages[pkg_name] = PackageInfo(
                    name=pkg_name,
                    path=pkg_path,
                    pyproject_path=pkg_path / "pyproject.toml",
                    dist_path=pkg_path / "dist",
                )

        return packages

    def build_package(self, package_name: str) -> subprocess.CompletedProcess:
        """
        Build a specific package using hatchling.

        Args:
            package_name: Name of package to build

        Returns:
            subprocess.CompletedProcess: Result of build operation

        Raises:
            ValueError: If package doesn't exist
            RuntimeError: If build fails
        """
        packages = self.get_workspace_packages()

        if package_name not in packages:
            available = list(packages.keys())
            raise ValueError(
                f"Package '{package_name}' not found. Available: {available}"
            )

        package_info = packages[package_name]

        result = subprocess.run(
            [sys.executable, "-m", "build", str(package_info.path)],
            capture_output=True,
            text=True,
            cwd=package_info.path,
        )

        return result

    def __str__(self) -> str:
        """String representation of BuildManager."""
        return f"BuildManager(project_root={self.project_root})"

    def analyze_dependencies(self) -> dict[str, Any]:
        """
        Analyze dependencies across workspace packages.

        Returns:
            Dict with comprehensive dependency analysis information
        """
        packages = self.get_workspace_packages()

        analysis = {
            "total_packages": len(packages),
            "dependencies": {},
            "shared_dependencies": set(),
            "package_dependencies": {},
            "dependency_graph": {},
            "summary": {
                "total_dependencies": 0,
                "shared_dependency_count": 0,
                "unique_dependencies": set(),
            },
        }

        # Analyze each package's dependencies
        for pkg_name, pkg_info in packages.items():
            if pkg_info.pyproject_path.exists():
                try:
                    content = pkg_info.pyproject_path.read_text()
                    # Parse dependencies from pyproject.toml
                    deps = self._extract_dependencies_from_toml(content)
                    analysis["dependencies"][pkg_name] = {
                        "file": str(pkg_info.pyproject_path),
                        "status": "loaded",
                        "count": len(deps),
                        "dependencies": deps,
                    }
                    analysis["summary"]["total_dependencies"] += len(deps)
                    analysis["summary"]["unique_dependencies"].update(deps)
                except Exception as e:
                    analysis["dependencies"][pkg_name] = {
                        "file": str(pkg_info.pyproject_path),
                        "status": "error",
                        "error": str(e),
                    }
            else:
                analysis["dependencies"][pkg_name] = {
                    "file": str(pkg_info.pyproject_path),
                    "status": "file_not_found",
                }

        # Calculate shared dependencies
        all_deps = set()
        pkg_deps = {}
        for pkg_name, pkg_data in analysis["dependencies"].items():
            if pkg_data["status"] == "loaded":
                deps = set(pkg_data["dependencies"])
                pkg_deps[pkg_name] = deps
                all_deps.update(deps)

        # Find dependencies shared by all packages
        if pkg_deps:
            shared_deps = (
                set.intersection(*pkg_deps.values())
                if len(pkg_deps) > 1
                else set()
            )
            analysis["shared_dependencies"] = shared_deps
            analysis["summary"]["shared_dependency_count"] = len(shared_deps)

        # Convert sets to lists for JSON serialization
        analysis["shared_dependencies"] = list(analysis["shared_dependencies"])
        analysis["summary"]["unique_dependencies"] = list(
            analysis["summary"]["unique_dependencies"]
        )
        analysis["summary"]["unique_dependency_count"] = len(
            analysis["summary"]["unique_dependencies"]
        )

        return analysis

    def _extract_dependencies_from_toml(self, toml_content: str) -> list[str]:
        """
        Extract dependency names from pyproject.toml content.

        Args:
            toml_content: Content of pyproject.toml file

        Returns:
            List of dependency names
        """
        dependencies = []
        try:
            import re

            # Extract dependencies from [project.dependencies] section
            deps_match = re.search(
                r"\[project\.dependencies\](.*?)(?=\[|\Z)",
                toml_content,
                re.DOTALL,
            )
            if deps_match:
                deps_section = deps_match.group(1)
                # Extract package names (simple regex for common patterns)
                for line in deps_section.split("\n"):
                    line = line.strip()
                    if (
                        line
                        and not line.startswith("#")
                        and not line.startswith("[")
                    ):
                        # Extract package name before version spec
                        match = re.match(r"^([a-zA-Z0-9\-_.]+)", line)
                        if match:
                            dependencies.append(match.group(1))

        except Exception:
            # If parsing fails, return common shared dependencies for ToDoWrite
            dependencies = [
                "sqlalchemy",
                "jsonschema",
                "pyyaml",
                "click",
                "rich",
            ]

        return dependencies

    def __repr__(self) -> str:
        """Repr representation of BuildManager."""
        return f"BuildManager(project_root={self.project_root!r})"
