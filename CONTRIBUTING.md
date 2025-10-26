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
    ```bash
    pip install -e .
    ```
5.  **Make Your Changes**: Implement your feature or fix the bug. Ensure your code adheres to the project's [Code Style](#code-style) and includes comprehensive [Testing](#testing) and [Documentation](#documentation).
6.  **Run Tests**: Before submitting, run all tests to ensure your changes haven't introduced any regressions.
    ```bash
    python -m pytest
    ```
    For PostgreSQL integration tests, ensure you have Docker running and the container is up:
    ```bash
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
*   **Black**: Code is formatted using [Black](https://github.com/psf/black).
*   **isort**: Imports are sorted using [isort](https://pycqa.github.io/isort/).
*   **Ruff**: Code is linted using [Ruff](https://beta.ruff.rs/docs/).

## Release Process

The release process for ToDoWrite involves the following steps:

1.  **Feature Freeze**: All new features are merged into the `develop` branch.
2.  **Testing**: Comprehensive testing is performed on the `develop` branch.
3.  **Version Bump**: The project version is updated in `pyproject.toml` according to [Semantic Versioning](https://semver.org/).
4.  **Changelog Update**: A `CHANGELOG.md` file is updated with all changes since the last release.
5.  **Merge to `main`**: The `develop` branch is merged into the `main` branch.
6.  **Tag Release**: A Git tag is created for the new version (e.g., `v0.1.0`).
7.  **Build and Publish**: The package is built and published to PyPI.
8.  **Release Notes**: Release notes are drafted on GitHub, summarizing the changes.

## Need Help?

If you have any questions or need assistance, please open an issue on the GitHub repository.
