# TDD Requirements Policy

## 🚨 UNEQUIVOCAL TDD ENFORCEMENT

### Mandatory TDD Workflow

**ALL CODE** MUST follow strict TDD workflow without exception:

1. **RED PHASE**: Start with failing test
2. **GREEN PHASE**: Minimal code to pass test only
3. **REFACTOR PHASE**: Improve code while tests pass

### 🔴 TDD Mandate Verification

```bash
# STEP 1: Write failing test FIRST (MUST FAIL)
pytest tests/ -v -k "your_new_feature"  # MUST show failure

# STEP 2: Implement minimal code to pass (ONLY after test fails)
# ... write implementation ...

# STEP 3: Verify test passes (MUST PASS)
pytest tests/ -v -k "your_new_feature"  # MUST show success

# STEP 4: All tests must pass (MANDATORY)
pytest tests/ -v  # ALL tests MUST pass
```

## 🚫 Forbidden Workflow Violations

**NEVER ALLOWED:**
- ❌ Writing code without a failing test
- ❌ "Quick fixes"
- ❌ Mocking core logic
- ❌ Skipping tests
- ❌ Partial testing

**Specific violations:**
- **❌ NO CODE** without failing test first
- **❌ NO IMPLEMENTATION** before test exists and fails
- **❌ NO "QUICK FIXES"** without test coverage
- **❌ NO SKIP-TEST excuses** for "simple changes"
- **❌ NO PRODUCTION CODE** that isn't tested

If you cannot apply TDD → **STOP**.

### Anti-TDD Patterns (Prohibited)

```python
# ❌ FORBIDDEN - Writing code without test first
def calculate_total(items):
    return sum(item.price for item in items)  # No test exists

# ❌ FORBIDDEN - Quick fixes without coverage
def quick_fix():
    # Fixing bug without writing test first
    return "patched result"

# ❌ FORBIDDEN - Mocking core functionality
def test_user_creation():
    with mock.patch('database.save_user'):  # Don't mock core logic
        # test implementation
```

## Real Data Testing Requirements

### Validation Requirements
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

## Correct TDD Implementation Example

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

## TDD Compliance Enforcement

### Startup Enforcement
- **startup_enforcement.py** verifies pytest exists and tests can run
- **Compliance Check #9**: External research after 3 validation failures
- **Compliance Check #10**: No unconditional "All Tests Passed" messages
- **Zero-tolerance policy**: Any TDD violation = immediate work stoppage

### Testing Standards
- **Package Development**: `uv run lib_package/src/todowrite/module/script.py`
- **CLI Development**: `uv run cli_package/src/todowrite_cli/commands.py`
- **Testing**: `uv run pytest tests/lib_package/` or `uv run pytest tests/cli_package/`
- **Environment Variables**: `env VAR_NAME="value" uv run command`

### Red-Green-Refactor Cycle

#### RED Phase
1. **Write a failing test** that clearly demonstrates the desired functionality
2. **Ensure test fails** for the right reason
3. **Run test suite** to confirm it's the only failure

#### GREEN Phase
1. **Write minimal code** to make the test pass
2. **No extra functionality** beyond what's needed
3. **Run test suite** to confirm all tests pass

#### REFACTOR Phase
1. **Improve code quality** while keeping tests passing
2. **Remove duplication**, improve naming, enhance structure
3. **Run test suite** after each refactor step
4. **Keep functionality identical**

## Validation Checklist

Before submitting any work:

1. ✅ Failing test written FIRST
2. ✅ Test fails for expected reason
3. ✅ Minimal implementation written
4. ✅ Test passes with implementation
5. ✅ All existing tests still pass
6. ✅ Real data used (no fakes/mocks unless user-specified)
7. ✅ Cross-package integration tested
8. ✅ Validation function produces expected results
9. ✅ No unconditional success messages
10. ✅ All failures tracked and reported
11. ✅ Exit codes correct (0 for success, 1 for any failure)
