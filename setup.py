"""Setup script for todowrite package."""

import sys
from pathlib import Path

# Add the project root to Python path to import version
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

try:
    from todowrite.version import get_version
except ImportError:
    # Fallback for when version.py is not available during development
    def get_version():
        return "0.1.7.1"


# Read the contents of README file for long description
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding="utf-8")

setup_params = {
    "name": "todowrite",
    "version": get_version(),
    "author": "dderyldowney",
    "author_email": "dderyldowney@gmail.com",
    "description": "A standalone task management system with hierarchical planning framework.",
    "long_description": long_description,
    "long_description_content_type": "text/markdown",
    "url": "https://github.com/dderyldowney/todowrite",
    "project_urls": {
        "Bug Tracker": "https://github.com/dderyldowney/todowrite/issues",
        "Documentation": "https://github.com/dderyldowney/todowrite",
        "Source Code": "https://github.com/dderyldowney/todowrite",
    },
    "packages": ["todowrite"],
    "package_data": {
        "todowrite": ["schemas/*.json"],
    },
    "py_modules": [],
    "python_requires": ">=3.12",
    "install_requires": [
        "sqlalchemy>=2.0.0",
        "typing-extensions>=4.0.0",
        "click>=8.0.0",
        "psycopg2-binary>=2.9.0",
        "PyYAML>=6.0.0",
        "jsonschema>=4.0.0",
    ],
    "extras_require": {
        "dev": [
            "pyright>=1.1.0",
            "types-PyYAML>=6.0.12",
            "types-jsonschema>=4.0.0",
            "sqlalchemy>=2.0.0",
            "types-click>=7.1.0",
            "ruff>=0.7.0",
            "black>=24.0.0",
            "isort>=5.13.0",
            "pytest>=8.0.0",
            "pre-commit>=4.0.0",
            "bandit[toml]>=1.7.0",
        ]
    },
    "entry_points": {
        "console_scripts": [
            "todowrite=todowrite.cli:cli",
        ],
    },
    "classifiers": [
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "Topic :: Office/Business :: Scheduling",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Text Processing :: Markup :: Markdown",
    ],
    "keywords": "task management, todo, hierarchical planning, cli, productivity",
}

if __name__ == "__main__":
    import setuptools

    setuptools.setup(**setup_params)
