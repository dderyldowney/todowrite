#!/usr/bin/env python3
"""
Universal Git Hook: Prevent Python Cache Files from Being Committed

This hook ensures that NO Python cache files (__pycache__, .pyc, etc.)
are EVER committed to ANY git repository - this is a universal principle
that applies to ALL projects using Python, not just ToDoWrite.

This hook checks:
1. __pycache__ directories (anywhere in the project)
2. .pyc, .pyo, .pyd files (anywhere in the project)
3. Python build artifacts
4. Returns appropriate exit codes for CI/CD integration

Universal Rule: PYTHON CACHE FILES SHOULD NEVER BE COMMITTED TO GIT
"""

import sys
from pathlib import Path


def find_python_cache_files(root_dir: str) -> list[str]:
    """
    Find all Python cache files in the repository.

    Args:
        root_dir: Root directory of the git repository

    Returns:
        List of file paths that are Python cache files
    """
    cache_files = []
    cache_patterns = [
        "__pycache__",  # Cache directories
        "*.pyc",  # Compiled Python files
        "*.pyo",  # Optimized Python files
        "*.pyd",  # Python dynamic files
        "*$py.class",  # Java class files (from Jython)
        ".Python",  # Build directory
    ]
    # Note: dist/ and sdist/ excluded by directory exclusions above

    # Directories to exclude from cache file search
    exclude_dirs = {
        ".git",
        ".venv",  # Virtual environments
        "venv",  # Virtual environments
        "env",  # Virtual environments
        "__pycache__",  # Handled separately
        "node_modules",  # Node.js modules
        ".pytest_cache",  # Pytest cache
        ".coverage",  # Coverage reports
        "htmlcov",  # HTML coverage reports
        "dist",  # Distribution directories (rebuilt each release)
        "sdist",  # Source distributions (rebuilt each release)
        "build",  # Build directories (rebuilt each build)
        # Note: Some projects use build/ for legitimate build scripts,
        # but for most projects, build/ should be gitignored
    }

    root_path = Path(root_dir)

    # Find __pycache__ directories first
    for pattern in cache_patterns:
        if pattern.endswith("/"):
            # Directory pattern
            for path in root_path.rglob(pattern.rstrip("/")):
                if path.is_dir():
                    # Check if path is under any excluded directory
                    path_str = str(path)
                    should_exclude = False
                    for exclude in exclude_dirs:
                        # Check if the path contains the excluded directory as a path component
                        if (
                            f"/{exclude}/" in path_str
                            or path_str.startswith(f"{exclude}/")
                            or path_str.endswith(f"/{exclude}")
                            or path_str == exclude
                        ):
                            should_exclude = True
                            break
                    if not should_exclude:
                        cache_files.extend(str(p) for p in path.rglob("*") if p.is_file())
        else:
            # File pattern
            for path in root_path.rglob(pattern):
                path_str = str(path)
                # Check if path is under any excluded directory
                should_exclude = False
                for exclude in exclude_dirs:
                    # Check if the path contains the excluded directory as a path component
                    if (
                        f"/{exclude}/" in path_str
                        or path_str.startswith(f"{exclude}/")
                        or path_str.endswith(f"/{exclude}")
                        or path_str == exclude
                    ):
                        should_exclude = True
                        break
                if (
                    path.is_file()
                    and not should_exclude
                    and
                    # Exclude build/dist directories that are legitimate
                    "dist/" not in path_str
                    and "build/" not in path_str
                ):
                    cache_files.append(path_str)

    return cache_files


def find_pycache_directories(root_dir: str) -> list[str]:
    """
    Find all __pycache__ directories in the repository.

    Args:
        root_dir: Root directory of the git repository

    Returns:
        List of __pycache__ directory paths
    """
    # Directories to exclude from cache file search
    exclude_dirs = {
        ".git",
        ".venv",  # Virtual environments
        "venv",  # Virtual environments
        "env",  # Virtual environments
        "__pycache__",  # Handled separately
        "node_modules",  # Node.js modules
        ".pytest_cache",  # Pytest cache
        ".coverage",  # Coverage reports
        "htmlcov",  # HTML coverage reports
        "dist",  # Distribution directories (rebuilt each release)
        "sdist",  # Source distributions (rebuilt each release)
        "build",  # Build directories (rebuilt each build)
        # Note: Some projects use build/ for legitimate build scripts,
        # but for most projects, build/ should be gitignored
    }

    root_path = Path(root_dir)
    pycache_dirs = []

    for path in root_path.rglob("__pycache__"):
        if path.is_dir():
            # Check if path is under any excluded directory
            path_str = str(path)
            should_exclude = False
            for exclude in exclude_dirs:
                # Check if the path contains the excluded directory as a path component
                if (
                    f"/{exclude}/" in path_str
                    or path_str.startswith(f"{exclude}/")
                    or path_str.endswith(f"/{exclude}")
                    or path_str == exclude
                ):
                    should_exclude = True
                    break
            if not should_exclude:
                pycache_dirs.append(path_str)

    return pycache_dirs


def check_for_pycache_violations(root_dir: str) -> tuple[int, list[str]]:
    """
    Check for Python cache file violations.

    Args:
        root_dir: Root directory of the git repository

    Returns:
        Tuple of (exit_code, list_of_violations)
    """
    violations = []

    # Check for __pycache__ directories
    pycache_dirs = find_pycache_directories(root_dir)
    if pycache_dirs:
        violations.extend([f"__pycache__ directory found: {d}" for d in pycache_dirs])

    # Check for Python cache files
    cache_files = find_python_cache_files(root_dir)
    if cache_files:
        violations.extend([f"Python cache file found: {f}" for f in cache_files])

    # Determine exit code based on violations
    if violations:
        return 1, violations
    else:
        return 0, []


def main():
    """Main hook function."""
    # Get git repository root
    try:
        git_root = Path(__file__).resolve().parent.parent
    except Exception:
        # Fallback to current directory
        git_root = Path.cwd()

    print("🔍 Universal Python Cache File Check")
    print("=" * 50)
    print(f"Repository root: {git_root}")
    print("Universal Rule: Python cache files should NEVER be committed to git")
    print()

    # Check for violations
    exit_code, violations = check_for_pycache_violations(str(git_root))

    if violations:
        print("❌ VIOLATIONS FOUND:")
        print("=" * 50)
        for violation in violations[:10]:  # Show first 10 violations
            print(f"  • {violation}")

        if len(violations) > 10:
            print(f"  ... and {len(violations) - 10} more violations")

        print()
        print("🚫 BLOCKING COMMIT:")
        print("Python cache files violate git best practices.")
        print("Please remove these files and ensure .gitignore blocks cache files.")
        print()
        print("RECOMMENDED ACTIONS:")
        print("1. Remove cache files: find . -name '__pycache__' -exec rm -rf {} +")
        print("2. Remove .pyc files: find . -name '*.pyc' -delete")
        print("3. Ensure .gitignore has: __pycache__/, *.py[cod], *.pyo")
        print("4. Run: git rm -r --cached __pycache__/")
        print("5. Commit the .gitignore changes")

        sys.exit(exit_code)
    else:
        print("✅ NO PYTHON CACHE FILES FOUND")
        print("Repository is clean of Python cache artifacts.")
        print("Universal cache prevention is working correctly.")
        sys.exit(0)


if __name__ == "__main__":
    main()
