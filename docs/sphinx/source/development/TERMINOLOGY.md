# TERMINOLOGY GUIDE

## 1. Project / Distribution
The installable Python project defined by `pyproject.toml`.
Examples: `todowrite`, `todowrite-cli`, `todowrite-web` (if split into separate distributions).

---

## 2. Package
A directory containing an `__init__.py` file.
Examples:
- `todowrite`
- `todowrite_cli`
- `todowrite_web`

---

## 3. Top-Level Package
The main import namespace of a distribution.
Examples:
- `todowrite` (library)
- `todowrite_cli` (CLI)
- `todowrite_web` (FastAPI web app)

---

## 4. Subpackage
A package located inside another package (a subdirectory with its own `__init__.py`).
Examples:
- `todowrite.core`
- `todowrite.models`
- `todowrite_web.api`
- `todowrite_web.dependencies`

**Rule:** folder + `__init__.py` = subpackage.

---

## 5. Module
A single `.py` file that can be imported.
Examples:
- `todowrite/utils.py` → module `todowrite.utils`
- `todowrite/core/planner.py` → module `todowrite.core.planner`
- `todowrite/models/task.py` → module `todowrite.models.task`

**Rule:** `.py` file = module.

---

## 6. Submodule (Informal Only)
A casual term for “a module inside a package.”
Prefer explicitly saying *subpackage* or *module*.

---

## 7. Package Initializer (`__init__.py`)
The file that initializes a package.
Used for:
- defining public API
- setting `__all__`
- package metadata
- shortcut imports

Examples:
- `todowrite/__init__.py`
- `todowrite_cli/__init__.py`
- `todowrite_web/__init__.py`

---

## 8. Entry Point Module (`__main__.py`)
A module that allows a package to be executed via:

```
python -m package_name
```

Example:
- `todowrite_cli/__main__.py`
  → The CLI entrypoint module for the ToDoWrite CLI.

---

## 9. Console Script (Entry Point Script)
The executable installed by the package via the `project.scripts` section of `pyproject.toml`.

Example:

```toml
[project.scripts]
todowrite = "todowrite_cli.__main__:main"
```

Terminology:
- “Console script `todowrite`”
- “Entry point script”

---

## 10. Library Package
The package that contains the core domain logic and business rules.

For this project:
- `todowrite`

---

## 11. CLI Package
The package implementing the command-line interface.

For this project:
- `todowrite_cli`
- Contains:
  - **Package initializer:** `todowrite_cli.__init__`
  - **CLI entrypoint module:** `todowrite_cli.__main__`
  - **Console script:** `todowrite`

---

## 12. FastAPI Application Package
A package containing the ASGI web application built with FastAPI.

For this project:
- `todowrite_web`

Includes terminology:
- **ASGI application module** → `todowrite_web.main`
- **ASGI application object** → `app` inside `main.py`
- **API subpackage** → `todowrite_web.api`
- **API modules** → e.g., `todowrite_web.api.tasks`

---

## 13. Full Project Mapping Example

```
todowrite/                # library package
    __init__.py           # package initializer
    core/                 # subpackage
        __init__.py
        planner.py        # module
    models/               # subpackage
        __init__.py
        task.py           # module
    utils.py              # module

todowrite_cli/            # CLI package
    __init__.py
    __main__.py           # CLI entrypoint module

todowrite_web/            # FastAPI application package
    __init__.py
    main.py               # ASGI application module
    api/                  # API subpackage
        __init__.py
        tasks.py          # API module
```

---

## 14. Quick Reference

| Term | Meaning |
|------|---------|
| **Package** | Folder with `__init__.py` |
| **Subpackage** | Nested package |
| **Module** | `.py` file |
| **Submodule** | Informal term for module inside a package |
| **Package initializer** | `__init__.py` |
| **Entry point module** | `__main__.py` |
| **Console script** | Installed CLI executable |
| **Library package** | Main domain logic |
| **CLI package** | Command-line interface |
| **FastAPI application package** | Web frontend |
