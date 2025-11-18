"""Sphinx configuration file for ToDoWrite documentation."""

import sys
from pathlib import Path

# Add library source to Python path for autodoc
project_root = Path(__file__).parents[3]  # Go up from source/ to project root
lib_source_path = project_root / "lib_package" / "src"
cli_source_path = project_root / "cli_package" / "src"
sys.path.insert(0, str(lib_source_path))
sys.path.insert(1, str(cli_source_path))

# -- Project information --
project = "ToDoWrite"
copyright_year = "2025"
copyright_author = "D Deryl Downey"
author = "D Deryl Downey"
release = "0.4.1"  # Will be updated automatically later

# -- General configuration --
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
    "sphinx.ext.viewcode",
    "sphinx.ext.napoleon",
    "sphinx.ext.intersphinx",
    "sphinx_autodoc_typehints",
    "myst_parser",
]

# MyST parser for markdown support
myst_enable_extensions = [
    "colon_fence",
    "deflist",
    "html_admonition",
    "substitution",
    "tasklist",
]

templates_path = ["_templates"]
exclude_patterns = []

# -- Options for HTML output --
html_theme = "sphinx_rtd_theme"
html_static_path = ["_static"]

# Custom domain configuration for GitHub Pages
html_baseurl = "https://ToDoWrite.davidderyldowney.com"

# GitHub integration
html_context = {
    "display_github": True,
    "github_user": "dderyldowney",
    "github_repo": "ToDoWrite",
    "github_version": "develop/docs/sphinx/source/",
}

# -- Options for autodoc --
autodoc_default_options = {
    "members": True,
    "member-order": "bysource",
    "special-members": "__init__",
    "undoc-members": True,
    "exclude-members": "__weakref__",
}

# -- Intersphinx mapping --
intersphinx_mapping = {
    "python": ("https://docs.python.org/3", None),
    "sqlalchemy": ("https://docs.sqlalchemy.org/en/20/", None),
}

# Napoleon settings
napoleon_google_docstring = True
napoleon_numpy_docstring = True
napoleon_include_init_with_doc = False
napoleon_include_private_with_doc = False

# Type hints
autodoc_typehints = "description"
autodoc_typehints_description_target = "documented"
