# Contributing to ToDoWrite

We welcome contributions to ToDoWrite! By following these guidelines, you can help us maintain code quality, consistency, and a smooth development process.

## How to Contribute

1.  **Fork the Repository**: Start by forking the ToDoWrite repository on GitHub.
2.  **Clone Your Fork**: Clone your forked repository to your local machine.
    ```bash
    git clone https://github.com/your-username/todowrite.git
    cd todowrite
    ```
3.  **Create a New Branch**: Create a new branch for your feature or bug fix.
    ```bash
    git checkout -b feature/your-feature-name
    # or
    git checkout -b bugfix/issue-description
    ```
4.  **Set up Development Environment**:

    **Option A: Using uv (Recommended)**
    ```bash
    # Install dependencies and packages using uv
    uv sync

    # Install both packages in development mode
    uv pip install -e "./lib_package[dev]"
    uv pip install -e "./cli_package[dev]"
    ```

    **Option B: Using pip**
    ```bash
    # Install both packages in development mode
    pip install -e "./lib_package[dev]"
    pip install -e "./cli_package[dev]"

    # Or run the provided setup script
    ./setup_dev.sh
    ```

    **Note**: uv is our recommended package manager for faster dependency installation and better dependency resolution.
5.  **Make Your Changes**: Implement your feature or fix the bug. Ensure your code adheres to the project's [Code Style](#code-style) and includes comprehensive [Testing](#testing) and [Documentation](#documentation).
6.  **Run Tests**: Before submitting, run all tests to ensure your changes haven't introduced any regressions.
    ```bash
    # Set PYTHONPATH to include both package source directories
    export PYTHONPATH="lib_package/src:cli_package/src"

    # Run all tests
    python -m pytest

    # For PostgreSQL integration tests, ensure you have Docker running and the container is up:
    docker-compose up -d
    python -m pytest
    docker-compose down
    ```
7.  **Commit Your Changes**: Write clear and concise commit messages. Follow the [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/) specification (e.g., `feat: add new feature`, `fix: resolve bug in X`).
8.  **Push to Your Fork**: Push your local branch to your GitHub fork.
    ```bash
    git push origin feature/your-feature-name
    ```
9.  **Create a Pull Request (PR)**: Open a pull request from your forked repository to the `develop` branch of the main ToDoWrite repository. Provide a detailed description of your changes.

## Quality Standards

ToDoWrite adheres to the following quality standards:

1.  **Type Safety**: All code must include comprehensive Python 3.12+ type hints.
2.  **Documentation**: Functions, classes, and modules require clear and concise docstrings. New features should be documented in the relevant user guides or API references.
3.  **Testing**: New features and bug fixes require corresponding unit and/or integration tests. All tests must pass before a PR can be merged.
4.  **Database Compatibility**: Changes must work seamlessly with both SQLite and PostgreSQL.

## Code Style

We follow standard Python best practices and enforce code formatting:

*   **Python 3.12+ features and syntax**: Utilize modern Python constructs.
*   **Modern union syntax**: Use `|` instead of `typing.Union`.
*   **SQLAlchemy 2.0 patterns**: Adhere to the latest SQLAlchemy conventions.
*   **Dataclasses**: Prefer dataclasses for data modeling where appropriate.
*   **Ruff**: Code is linted and formatted using [Ruff](https://docs.astral.sh/ruff/), which provides both fast linting and formatting in a single tool.

## Release Process

### 🚀 Automated Release (Recommended)

**For a fully automated release, use the new release script:**

```bash
# Cut a specific release (e.g., 0.4.2)
./scripts/release.sh 0.4.2

# Cut a patch release (0.4.1 → 0.4.2)
./scripts/release.sh patch

# Preview a release without making changes
./scripts/release.sh patch --dry-run
```

**Just say "cut a 0.4.2 release" and any agent will know to run `./scripts/release.sh 0.4.2`**

The automated script handles the entire process:
- ✅ Prerequisites checks (tests, linting, git status)
- ✅ Version bumping with README/fallback updates
- ✅ Git operations (merge, tag, push)
- ✅ GitHub release creation
- ✅ Package building and publishing to TestPyPI & PyPI
- ✅ Error handling with rollback capabilities

### 📖 Manual Process (Deprecated)

**📖 For the complete manual release process, see [docs/RELEASE_WORKFLOW.md](docs/RELEASE_WORKFLOW.md)**

The manual release process involves the following steps:

1.  **Feature Freeze**: All new features are merged into the `develop` branch.
2.  **Testing**: Comprehensive testing is performed on the `develop` branch.
3.  **Version Bump**: The project version is updated using the enhanced bump script:
    ```bash
    python scripts/bump_version.py patch  # or minor/major
    # This automatically updates VERSION file and README badges
    ```
4.  **Changelog Update**: A `CHANGELOG.md` file is updated with all changes since the last release.
5.  **Merge to `main`**: The `develop` branch is merged into the `main` branch.
6.  **Tag Release**: A Git tag is created for the new version (e.g., `v1.2.3`).
7.  **GitHub Release**: Release is created on GitHub with auto-generated notes.
8.  **Build and Publish**: Both packages are published to TestPyPI first, then PyPI:
    ```bash
    ./scripts/publish.sh test clean  # Verify on TestPyPI
    ./scripts/publish.sh prod clean   # Then publish to PyPI
    ```

**Key Improvements:**
- ✅ **Automated README Updates**: No manual version updates needed in documentation
- ✅ **TestPyPI Verification**: Always test on TestPyPI before production
- ✅ **Enhanced Bump Script**: Supports `--verify-only`, `--dry-run`, and incremental bumps
- ✅ **Comprehensive Documentation**: Step-by-step instructions with troubleshooting

See [docs/RELEASE_WORKFLOW.md](docs/RELEASE_WORKFLOW.md) for the complete 8-step process with detailed commands, verification checkpoints, and rollback procedures.

### Version Management

This project uses a centralized version management system with a single `VERSION` file as the source of truth. See [VERSION_MANAGEMENT.md](VERSION_MANAGEMENT.md) for complete details.

## Need Help?

If you have any questions or need assistance, please open an issue on the GitHub repository.
