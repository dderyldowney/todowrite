# Testing

ToDoWrite includes a comprehensive test suite to ensure its functionality, data integrity, and compatibility across different database backends. All tests are run using `pytest`.

## Running All Tests

To execute the entire test suite, including unit tests and PostgreSQL integration tests, ensure you have Docker installed and running. Then, simply run `pytest` from the project root:

```bash
python -m pytest
```

This command will automatically:

1.  Start a PostgreSQL container defined in `docker-compose.yml`.
2.  Wait for the PostgreSQL database to become ready.
3.  Run all tests, with integration tests connecting to the Dockerized PostgreSQL instance.
4.  Stop and remove the PostgreSQL container after all tests have completed.

## Running Tests Against SQLite

By default, if the `TODOWRITE_DATABASE_URL` environment variable is not set, `ToDoWrite` will use a SQLite database. To explicitly run tests against SQLite, you can ensure this environment variable is unset:

```bash
unset TODOWRITE_DATABASE_URL # On Linux/macOS
# set TODOWRITE_DATABASE_URL= # On Windows (in cmd)
# $env:TODOWRITE_DATABASE_URL="" # On PowerShell

python -m pytest
```

When running tests against SQLite, a `todowrite.db` file will be created in the project root for each test run and cleaned up automatically.

## PostgreSQL Integration Tests (Manual Control)

If you prefer to manually control the PostgreSQL container or debug issues, you can manage it separately:

1.  **Start the PostgreSQL container**:
    ```bash
    docker-compose up -d
    ```

2.  **Run tests**:
    Ensure the `TODOWRITE_DATABASE_URL` environment variable is set to point to your PostgreSQL instance (e.g., `export TODOWRITE_DATABASE_URL="postgresql://todowrite:todowrite@localhost:5432/todowrite"`).
    Then, run `pytest`:
    ```bash
    python -m pytest
    ```

3.  **Stop the PostgreSQL container**:
    After running your tests, you can stop and remove the container:
    ```bash
    docker-compose down
    ```

## Test Structure

*   `tests/test_app.py`: Contains unit and integration tests for the `ToDoWrite` application class, covering node creation, retrieval, updates, and deletions. These tests are configured to run against the default PostgreSQL setup.
*   `tests/test_cli.py`: Contains tests for the `todowrite` command-line interface, ensuring all CLI commands function as expected. These tests also run against the default PostgreSQL setup.
