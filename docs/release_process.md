# Release Process

The release process for ToDoWrite ensures a structured and consistent approach to publishing new versions of the project. It involves several key steps, from feature freeze to final publication.

## Steps

1.  **Feature Freeze**:
    *   All new features, bug fixes, and enhancements intended for the upcoming release are merged into the `develop` branch.
    *   No new development work for the release is initiated after this point.

2.  **Comprehensive Testing**:
    *   Thorough testing is performed on the `develop` branch to identify and resolve any remaining bugs or regressions. This includes:
        *   Running the full unit test suite (`python -m pytest`).
        *   Executing integration tests against both SQLite and PostgreSQL.
        *   Manual testing of key functionalities.

3.  **Version Bump**:
    *   The project version is updated in the `pyproject.toml` file.
    *   We adhere to [Semantic Versioning (SemVer)](https://semver.org/), meaning:
        *   **MAJOR** version when you make incompatible API changes.
        *   **MINOR** version when you add functionality in a backward-compatible manner.
        *   **PATCH** version when you make backward-compatible bug fixes.

4.  **Changelog Update**:
    *   The `CHANGELOG.md` file is updated to reflect all changes included in the new release.
    *   Changes are categorized (e.g., Features, Bug Fixes, Breaking Changes, Documentation, Internal) and clearly described.

5.  **Merge `develop` to `main`**:
    *   Once testing is complete and the version and changelog are updated, the `develop` branch is merged into the `main` branch.
    *   The `main` branch always represents the latest stable release.

6.  **Tag Release**:
    *   A Git tag is created for the new version on the `main` branch. The tag name should follow the format `vX.Y.Z` (e.g., `v0.1.0`).
    *   ```bash
        git tag -a vX.Y.Z -m "Release vX.Y.Z"
        git push origin vX.Y.Z
        ```

7.  **Build and Publish**:
    *   The package is built into distributable formats (e.g., wheel, sdist).
    *   The built package is then published to the Python Package Index (PyPI).
    *   ```bash
        python -m build
        python -m twine upload dist/*
        ```

8.  **Draft Release Notes**:
    *   Release notes are drafted on the GitHub repository's "Releases" page.
    *   These notes summarize the key changes, new features, and bug fixes, often referencing the `CHANGELOG.md`.
