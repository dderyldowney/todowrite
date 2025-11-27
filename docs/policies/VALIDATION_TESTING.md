# Validation & Testing Policy

## 📋 Validation Requirements

### Real Data Testing Mandate
- **Always test with actual data**, never fake inputs
- **Cross-package integration**: Test real data flow between packages
- **Expected Results**: Verify outputs against concrete expected results
- **No Mocking**: NEVER mock core functionality, especially inter-package communication
- **Real Implementations Only**: Test with actual code, real data, and real connections
- **User-Exception Only**: Mock only when explicitly instructed by USER for specific portions

### Usage Functions Before Tests
- **ALL relevant usage functions MUST successfully output expected results BEFORE any creation of tests**
- **Results Before Lint**: ALL usage functionality MUST produce expected results BEFORE addressing any Pylint or other linter warnings
- **External Research After 3 Failures**: If a usage function fails validation 3 consecutive times, use external research tools

### Validation Output Requirements
- **NEVER print "All Tests Passed"** unless ALL tests actually passed
- **ALWAYS verify actual results** against expected results BEFORE printing ANY success message
- **ALWAYS track ALL failures** and report them at the end
- **ALWAYS include test counts** (e.g., "3 of 5 tests failed")
- **ALWAYS exit with code 1** if ANY tests fail, code 0 ONLY if ALL pass

## Validation Implementation Template

```python
# CORRECT VALIDATION FOR MONOREPO with full type coverage:
if __name__ == "__main__":
    import sys

    all_validation_failures: list[str] = []
    total_tests: int = 0

    # Test 1: Core library functionality
    total_tests += 1
    from todowrite.core.models import Task
    test_task: Task = Task(title="Test Task", description="Test Description")
    expected_title: str = "Test Task"
    if test_task.title != expected_title:
        failure_message: str = f"Library model: Expected '{expected_title}', got '{test_task.title}'"
        all_validation_failures.append(failure_message)

    # Test 2: CLI integration
    total_tests += 1
    from todowrite_cli.commands import create_task
    try:
        cli_result: ValidationResult = create_task("CLI Test Task")
        if not cli_result.success:
            all_validation_failures.append("CLI integration: Task creation failed")
    except Exception as e:
        error_message: str = f"CLI integration: Unexpected error {e}"
        all_validation_failures.append(error_message)

    # Test 3: Database connectivity
    total_tests += 1
    try:
        from todowrite.database.connection import get_connection
        conn = get_connection()
        if conn is None:
            all_validation_failures.append("Database connectivity: Could not establish connection")
    except Exception as e:
        all_validation_failures.append(f"Database connectivity: Unexpected error {e}")

    # Final validation result
    failed_count: int = len(all_validation_failures)
    if failed_count > 0:
        print(f"❌ VALIDATION FAILED - {failed_count} of {total_tests} tests failed:")
        for failure_index: int, failure_message in enumerate(all_validation_failures, start=1):
            print(f"  {failure_index}. {failure_message}")
        sys.exit(1)
    else:
        success_message: str = f"✅ VALIDATION PASSED - All {total_tests} tests produced expected results"
        print(success_message)
        sys.exit(0)
```

## Testing Strategy

### Test Categories

#### Unit Tests
- Test individual functions and methods
- Use real data, not mocks
- Focus on business logic validation
- Include cross-package integration tests

#### Integration Tests
- Test data flow between packages
- Verify database operations
- Test CLI-library integration
- Validate external service connections

#### Validation Tests
- Every module includes validation function
- Test with real data scenarios
- Verify expected outputs match actual results
- Track and report all failures

### Test Data Standards

#### Real Data Requirements
```python
# ✅ CORRECT - Real data testing
def test_task_creation():
    """Test task creation with real data."""
    real_data = {
        "title": "Implement user authentication",
        "description": "Add OAuth2 authentication for user login",
        "priority": "high",
        "due_date": "2024-12-01"
    }

    task = Task(**real_data)
    assert task.title == real_data["title"]
    assert task.status == "pending"  # Default value

# ❌ FORBIDDEN - Fake/mock data
def test_task_creation():
    """Test with fake data."""
    mock_data = {"title": "fake title"}  # Too simplistic
    # ... unrealistic test scenario
```

#### Cross-Package Integration
```python
# ✅ CORRECT - Testing real integration
def test_cli_to_database_flow():
    """Test complete CLI → Database flow."""
    # Use real CLI command
    result = subprocess.run([
        "python", "-m", "todowrite_cli", "create",
        "--title", "Integration Test Task"
    ], capture_output=True, text=True)

    # Verify in database
    with get_connection() as conn:
        cursor = conn.execute("SELECT * FROM tasks WHERE title = ?", ("Integration Test Task",))
        task_record = cursor.fetchone()
        assert task_record is not None
```

### Validation Protocol

#### Pre-Work Validation
1. **Environment Setup**: Verify all dependencies are installed
2. **Database Connectivity**: Confirm database connections work
3. **Import Validation**: Test all critical imports succeed

#### Function Validation
1. **Input Validation**: Test with various input types
2. **Output Verification**: Confirm outputs match expectations
3. **Error Handling**: Test error scenarios appropriately
4. **Edge Cases**: Validate boundary conditions

#### Integration Validation
1. **Package Communication**: Test data flow between packages
2. **External Services**: Verify external service interactions
3. **Database Operations**: Confirm database read/write operations
4. **CLI Operations**: Test command-line interface functionality

### Failure Handling

#### Tracking Requirements
- **All failures must be tracked** in validation results
- **Detailed error messages** explaining what failed and why
- **Failure categorization** (syntax, logic, integration, etc.)
- **Suggested fixes** for common failure patterns

#### External Research Protocol
After 3 consecutive validation failures:
1. **Stop implementation attempts**
2. **Research the problem** using external resources
3. **Document research findings**
4. **Apply new approach** based on research
5. **Document the solution** for future reference

### Compliance Checklist

Before submitting any work:

1. ✅ All validation functions test with real data
2. ✅ No unconditional "All Tests Passed" messages
3. ✅ All failures tracked and reported with counts
4. ✅ Exit codes correct (0 for success, 1 for any failure)
5. ✅ Cross-package integration tested
6. ✅ Expected results explicitly verified
7. ✅ No mocking of core functionality
8. ✅ External research conducted after 3 failures
9. ✅ Results validated before linting
10. ✅ Usage functions work before test creation

### Test Environment Setup

#### Development Environment
```bash
# Install dependencies
uv sync

# Setup test database
uv run python -m todowrite_cli --setup-test-db

# Run specific validation
PYTHONPATH="lib_package/src:cli_package/src" python lib_package/src/todowrite/module/__init__.py
```

#### Continuous Integration
```bash
# Run all validations
uv run pytest tests/ -v
uv run python -m todowrite_cli --validate-all-modules

# Check coverage
uv run pytest tests/ --cov=lib_package --cov=cli_package --cov-report=term-missing
```

### Performance Validation

#### Response Time Testing
- Validate function response times are acceptable
- Test with realistic data volumes
- Monitor memory usage during operations
- Verify scalability under load

#### Database Performance
- Test query performance with real data volumes
- Validate connection pooling effectiveness
- Monitor database transaction times
- Verify index effectiveness for common queries
