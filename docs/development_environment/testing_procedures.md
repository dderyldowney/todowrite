# Testing Procedures

This section outlines the procedures for running tests and interpreting test reports within the AFS FastAPI Agricultural Robotics Platform. Adhering to these procedures ensures the reliability and quality of the codebase, which is paramount for safety-critical agricultural applications.

## 1. Running Tests with `pytest`

The project utilizes `pytest` as its primary testing framework. `pytest` is a powerful and flexible tool that makes it easy to write and run tests.

### 1.1. Running All Tests

To execute all tests across the entire project, navigate to the project's root directory and run:

```bash
pytest
```

This command will discover and run all test files (typically those starting with `test_` or ending with `_test.py`) in the `tests/` directory and its subdirectories.

### 1.2. Running Specific Test Files

To run tests within a specific file, provide the path to the file:

```bash
pytest tests/unit/test_example_command.py
```

### 1.3. Running Specific Tests by Name

You can run individual test functions or methods by specifying their full node ID:

```bash
pytest tests/unit/test_example_command.py::test_example_command_clear_error_message
```

### 1.4. Running Tests with Markers

If tests are marked with custom markers (e.g., `@pytest.mark.integration`), you can run tests with a specific marker:

```bash
pytest -m integration
```

### 1.5. Verbose Output

To get more detailed output during test execution, use the `-v` (verbose) flag:

```bash
pytest -v
```

### 1.6. Stopping on First Failure

To stop test execution immediately after the first failure, use the `-x` flag:

```bash
pytest -x
```

## 2. Interpreting Test Reports

After `pytest` completes its execution, it generates a summary report. Understanding this report is crucial for identifying issues and ensuring code quality.

### 2.1. Test Status Indicators

`pytest` uses various indicators to show the status of each test:

*   `.` (dot): Indicates a successful test (passed).
*   `F` (Failing): Indicates a failed test (assertion failed or unexpected exception).
*   `E` (Error): Indicates an error during test setup or execution (e.g., syntax error, unhandled exception outside of assertions).
*   `S` (Skipped): Indicates a test that was skipped (e.g., due to a missing dependency or a `@pytest.mark.skip` decorator).
*   `x` (XFAIL): Indicates an expected failure (a test that is known to fail but is explicitly marked as such with `@pytest.mark.xfail`).

### 2.2. Summary Section

The report concludes with a summary section that provides an overview of the test run:

```
============================= test session starts ==============================
... (details about platform, pytest version, rootdir)
collected X items

tests/module/test_file.py ..F.S.                                     [100%]

=================================== FAILURES ===================================
____________________ test_example_command_clear_error_message ____________________
... (detailed traceback for failing test)

=============================== warnings summary ===============================
... (any warnings issued during the test run)

=========================== short test summary info ============================
FAILED tests/module/test_file.py::test_example_command_clear_error_message
==================== X failed, Y passed, Z skipped in N.NNs ====================
```

*   **`collected X items`**: Total number of tests discovered.
*   **Test Status Line**: A sequence of dots, Fs, Es, etc., representing the status of each test in the order they were run.
*   **`FAILURES` Section**: Provides detailed tracebacks and assertion messages for any failed tests, helping to pinpoint the exact cause of the failure.
*   **`warnings summary` Section**: Lists any warnings generated during the test run.
*   **`short test summary info`**: A concise summary of the overall test results (e.g., how many passed, failed, skipped).

## 3. Writing New Tests

When writing new tests, follow these best practices:

*   **Test File Naming**: Name test files starting with `test_` or ending with `_test.py` (e.g., `test_my_module.py`).
*   **Test Function Naming**: Name test functions starting with `test_` (e.g., `test_feature_x_works`).
*   **Fixtures**: Utilize `pytest` fixtures (`@pytest.fixture`) to set up and tear down test environments, ensuring tests are isolated and repeatable.
*   **Assertions**: Use standard `assert` statements for verifying expected outcomes.
*   **Clear Error Messages**: Ensure that assertion messages are clear and informative, especially for failing tests, to aid in quick debugging.
*   **Isolation**: Each test should be independent and not rely on the state left by previous tests.

## Agricultural Context in Testing

For the AFS FastAPI Agricultural Robotics Platform, testing is not just about code correctness but also about ensuring the safety and reliability of agricultural operations. Tests should consider:

*   **Safety-Critical Scenarios**: Explicitly test scenarios related to emergency stops, collision avoidance, and communication failures.
*   **ISOBUS Compliance**: Verify that ISOBUS communication and data handling adhere to ISO 11783 standards.
*   **Real-world Data**: Use realistic agricultural data and environmental conditions in integration tests where appropriate.
*   **Performance under Load**: Test the system's performance under various operational loads relevant to multi-tractor coordination and sensor data processing.
