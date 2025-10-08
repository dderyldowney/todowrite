# pytest Configuration Standards for AFS FastAPI

**Purpose**: Document the centralized pytest configuration used across the AFS FastAPI agricultural robotics platform to ensure consistent test execution behavior for all developers and AI agents.

## Configuration File: pytest.ini

**Location**: [pytest.ini](../pytest.ini) (Project Root)

The pytest.ini file provides centralized configuration for test execution behavior, plugins, custom markers, and output formatting. All pytest executions (manual, wrapper scripts, CI/CD pipelines) automatically use this configuration.

## Current Configuration

```ini
[pytest]
minversion = 6.0
addopts = -ra --strict-markers --import-mode=importlib
testpaths = tests
asyncio_default_fixture_loop_scope = function
markers =
    integration: mark a test as an integration test.
    unit: mark a test as a unit test.
    slow: mark a test as slow.
    serial: mark a test as serial (not to be run in parallel with other tests).
```

## Configuration Settings Explained

### minversion = 6.0

**Purpose**: Enforces minimum pytest version requirement

**Agricultural Context**: Ensures all developers and CI/CD environments use pytest ≥6.0, which provides modern features essential for async testing patterns used extensively in FastAPI agricultural equipment APIs.

**Impact**: Prevents compatibility issues with older pytest versions that lack async test support.

### addopts = -ra --strict-markers --import-mode=importlib

**Purpose**: Default command-line options applied to all pytest executions

**Options Breakdown**:
- `-ra`: Show extra test summary for **all** test results (passed, failed, skipped, xfailed, xpassed)
- `--strict-markers`: Raise errors for undefined test markers (prevents typos like `@pytest.mark.intergration`)
- `--import-mode=importlib`: Use Python's importlib for test imports (modern import strategy)

**Agricultural Context**:
- `-ra` provides comprehensive test summaries essential for safety-critical validation
- `--strict-markers` prevents marker typos that could accidentally skip safety tests
- `importlib` mode ensures consistent imports across different execution environments

### testpaths = tests

**Purpose**: Defines root directory for test discovery

**Agricultural Context**: Centralizes all test files in the [tests/](../tests/) directory, maintaining clear separation between production code ([afs_fastapi/](../afs_fastapi/)) and test code. This structure is essential for agricultural robotics where mixing test and production code could lead to safety-critical deployment errors.

**Test Organization**:
```
tests/
├── features/          # Feature-level integration tests (real-world workflows)
├── unit/              # Unit tests (component isolation)
│   ├── api/          # FastAPI endpoint tests
│   ├── equipment/    # Farm tractor and robotic interface tests
│   ├── hooks/        # Pre-commit hook tests
│   ├── monitoring/   # Soil/water monitor tests
│   ├── scripts/      # Utility script tests
│   └── services/     # Vector clock and coordination tests
└── test_*.py          # Root-level edge case tests
```

### asyncio_default_fixture_loop_scope = function

**Purpose**: Explicitly sets async fixture loop scope to function-level

**Agricultural Context**: FastAPI testing heavily uses async fixtures for HTTP client creation, database sessions, and equipment simulation. Function-level scope ensures:
- Each test gets a fresh event loop (prevents cross-test contamination)
- Async fixtures reset between tests (critical for equipment state isolation)
- Predictable behavior across pytest-asyncio version updates

**Why Explicit Configuration**: pytest-asyncio is transitioning to require explicit loop scope configuration. Setting this prevents deprecation warnings and ensures forward compatibility.

**Safety Impact**: Function-level scope prevents one test's async operation from affecting another—essential when simulating multi-tractor coordination scenarios where test isolation prevents false positives.

## Custom Test Markers

### @pytest.mark.integration

**Usage**: Mark tests that validate integration between multiple components

**Example**: Testing ISOBUS message flow from tractor through API to coordination system

```python
@pytest.mark.integration
def test_multi_tractor_coordination_workflow():
    """Validate complete workflow from tractor state changes to fleet coordination."""
    # Integration test spanning equipment, API, and coordination layers
```

### @pytest.mark.unit

**Usage**: Mark tests that validate single component behavior in isolation

**Example**: Testing individual FarmTractor class methods

```python
@pytest.mark.unit
def test_tractor_emergency_stop():
    """Validate emergency stop activates correctly without external dependencies."""
    # Pure unit test with no external system interaction
```

### @pytest.mark.slow

**Usage**: Mark tests with longer execution times (>1 second)

**Example**: Tests involving database migrations, heavy computations, or realistic timing delays

**Use Case**: Can be excluded from rapid development cycles: `pytest -m "not slow"`

```python
@pytest.mark.slow
def test_field_operation_complete_cultivation():
    """Simulate complete field cultivation with realistic timing delays."""
    # Test includes realistic equipment operation delays
```

### @pytest.mark.serial

**Usage**: Mark tests that cannot run in parallel (state-dependent or resource-contention)

**Example**: Tests that modify global configuration or use exclusive hardware resources

**Use Case**: Ensures these tests run sequentially even with `pytest-xdist` parallel execution

```python
@pytest.mark.serial
def test_modify_global_equipment_registry():
    """Test that modifies shared equipment registry state."""
    # Must run serially to prevent race conditions
```

## Running Tests with Markers

### Run only integration tests
```bash
pytest -m integration
```

### Run only unit tests
```bash
pytest -m unit
```

### Exclude slow tests
```bash
pytest -m "not slow"
```

### Run integration tests but skip slow ones
```bash
pytest -m "integration and not slow"
```

### Run only serial tests
```bash
pytest -m serial
```

## Why Centralized Configuration Matters for Agricultural Robotics

### Consistency Across Environments

**Development Machines**: All developers get identical test behavior regardless of local setup

**CI/CD Pipelines**: Automated builds execute tests with exact same configuration

**AI Agent Execution**: Claude, GPT, Gemini, Copilot, CodeWhisperer all execute tests identically

### Safety-Critical Validation

**Strict Markers**: Prevents accidental marker typos that could skip safety tests

**Import Isolation**: `importlib` mode ensures clean imports preventing cross-test pollution

**Async Fixture Scope**: Function-level isolation prevents multi-tractor simulation tests from interfering

### Test Organization

**Clear Structure**: `testpaths = tests` enforces separation of production and test code

**Comprehensive Reporting**: `-ra` ensures all test results visible (no hidden failures)

**Marker System**: Custom markers enable targeted testing (run only safety tests, skip slow tests)

## Integration with Test Infrastructure

### bin/runtests Wrapper

The [bin/runtests](../bin/runtests) wrapper automatically uses pytest.ini configuration:

```bash
./bin/runtests              # Uses pytest.ini settings
./bin/runtests --coverage   # Adds coverage, still uses pytest.ini
./bin/runtests -q          # Quiet mode, still uses pytest.ini
```

### Pre-commit Hooks

Pre-commit test execution uses pytest.ini configuration ensuring commit validation matches development testing.

### CI/CD Pipelines

GitHub Actions and other CI systems use pytest.ini ensuring deployment validation matches local testing.

## Agricultural Robotics Best Practices

### 1. Always Use Markers for Test Organization

```python
@pytest.mark.unit
@pytest.mark.integration  # Can combine markers
def test_tractor_api_integration():
    """Test that validates unit behavior AND integration with API."""
    pass
```

### 2. Mark Slow Tests to Enable Rapid Feedback

```python
@pytest.mark.slow
def test_complete_field_harvest_simulation():
    """Realistic 30-second field harvest simulation."""
    time.sleep(30)  # Realistic equipment timing
```

### 3. Use Serial Marker for State-Dependent Tests

```python
@pytest.mark.serial
def test_equipment_registry_modification():
    """Modify shared equipment state (must run serially)."""
    # Modifies global state requiring serial execution
```

### 4. Leverage Async Fixture Scope for Clean Tests

The function-level `asyncio_default_fixture_loop_scope` ensures each test gets fresh async context:

```python
@pytest.mark.asyncio
async def test_api_tractor_status(async_client):
    """Each test gets fresh async client (no cross-test contamination)."""
    response = await async_client.get("/api/tractor")
    assert response.status_code == 200
```

## Modifying pytest.ini Configuration

**IMPORTANT**: Changes to pytest.ini affect ALL test executions across the platform.

### Adding New Markers

1. Add marker to `markers` section in pytest.ini
2. Document marker purpose and usage in this file
3. Update test files to use new marker
4. Commit with agricultural context explaining why marker is needed

**Example**:
```ini
markers =
    safety_critical: mark tests validating ISO 18497 safety compliance.
```

### Changing Default Options

Changes to `addopts` affect all test runs. Document reasoning:

```ini
# Adding verbosity by default
addopts = -ra --strict-markers --import-mode=importlib -v
```

**Agricultural Context**: Would make all test runs verbose by default (might be excessive)

### Adjusting Async Fixture Scope

**WARNING**: Changing `asyncio_default_fixture_loop_scope` affects async fixture behavior platform-wide.

**Current**: `function` (recommended for safety-critical isolation)

**Alternatives**:
- `class`: Share event loop across test class methods (reduces overhead but risks cross-test pollution)
- `module`: Share event loop across entire test module (dangerous for equipment state tests)
- `session`: Share event loop across entire test session (NOT RECOMMENDED for agricultural robotics)

**Recommendation**: Keep `function` scope for maximum test isolation in safety-critical multi-tractor coordination scenarios.

## Test Execution Performance

**Current Metrics** (161 tests):
- **Execution Time**: ~3 seconds (all tests)
- **Pass Rate**: 100% (zero failures)
- **Async Tests**: ~40% of test suite
- **Fixture Overhead**: Minimal with function-level scope

**Performance Goals**:
- Maintain sub-5-second execution for full suite
- Enable rapid Test-First Development feedback
- Support frequent test execution during TDD RED-GREEN-REFACTOR cycles

## Cross-Agent Consistency

All AI agents (Claude, GPT, Gemini, Copilot, CodeWhisperer) execute tests using identical pytest.ini configuration, ensuring:

- **Consistent Results**: Same test outcomes regardless of AI platform
- **Reproducible Issues**: Failures reproduce identically across agents
- **Unified Reporting**: Standardized test output format (see [TEST_REPORTING_MANDATORY.md](../.claude/TEST_REPORTING_MANDATORY.md))

## References

- **Test Execution**: [bin/runtests](../bin/runtests) - Wrapper script using pytest.ini
- **Test Reporting**: [.claude/TEST_REPORTING_MANDATORY.md](../.claude/TEST_REPORTING_MANDATORY.md) - Required reporting format
- **Test Architecture**: [WORKFLOW.md](../WORKFLOW.md) - Complete testing framework documentation
- **TDD Methodology**: [TDD_WORKFLOW.md](../TDD_WORKFLOW.md) - Test-First development practices

---

**Purpose**: This documentation ensures all developers and AI agents understand pytest configuration standards essential for maintaining consistent, safe, and reliable test execution across the AFS FastAPI agricultural robotics platform.
