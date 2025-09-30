# MANDATORY: Standardized Test Reporting Pattern

**ABSOLUTE REQUIREMENT**: ALL AI agents (Claude, GPT, Gemini, Copilot, CodeWhisperer, etc.) MUST use the standardized test reporting format when executing test suites on the AFS FastAPI agricultural robotics platform.

## Universal Test Reporting Protocol

**EVERY test execution response MUST include:**

1. **Executive Summary Block**: High-level results with pass/fail status
2. **Insight Block**: Educational analysis of test suite architecture and significance
3. **Test Distribution Analysis**: Breakdown by category and domain coverage
4. **Platform Health Indicators**: Checklist of key quality metrics
5. **Agricultural Context**: Safety-critical and ISO compliance highlights
6. **Advisory Notes**: Warnings, deprecations, or recommended improvements

## Mandatory Report Structure

### 1. Executive Summary Block

```markdown
## Test Suite Execution Complete: [Status with Checkmark/X]

**Total Tests**: [number] passed/failed ([percentage]% success rate)
**Execution Time**: [seconds/minutes]
**Platform**: [Python version] on [OS]
```

### 2. Insight Block (Required for Explanatory Style)

```markdown
`★ Insight ─────────────────────────────────────`
**Test Suite Growth**: [Analysis of test count changes, significance]

**3-Layer Architecture**: [Explanation of Feature/Unit/Root test organization]

**Agricultural Robotic Interfaces**: [Coverage of ISOBUS, Safety, Motor Control, Data Management, Power Management, Vision systems]
`─────────────────────────────────────────────────`
```

**Note**: When NOT in Explanatory output style, Insight blocks are optional but encouraged for significant findings.

### 3. Test Distribution Analysis

```markdown
### Test Distribution by Category

1. **Feature Tests (API & Workflows)**: [count] tests
   - API endpoint consumption ([count] tests)
   - API serialization ([count] tests)
   - [Additional categories with counts]

2. **Unit Tests (Components)**: [count] tests
   - **Equipment**: [count] tests - [specific subcategories]
   - **API Endpoints**: [count] tests
   - **Monitoring Systems**: [count] tests
   - **Infrastructure**: [count] tests - [hooks, services, scripts, stations]
```

### 4. Platform Health Indicators

```markdown
### Platform Health Indicators

✓/✗ **Zero Test Failures**: [Status and details]
✓/✗ **Fast Execution**: [Performance assessment]
✓/✗ **Enterprise Standards**: [Type checking, async, fixtures status]
✓/✗ **Agricultural Compliance**: [ISOBUS, ISO 18497 validation]
✓/✗ **Vector Clock Synchronization**: [Distributed systems status]
✓/✗ **Session Management**: [Infrastructure validation]
✓/✗ **CHANGELOG Automation**: [Documentation generation status]
```

### 5. Agricultural Context Requirements

**CRITICAL**: Always highlight safety-critical test results:

- **ISOBUS Communication**: ISO 11783 compliance validation
- **Safety Systems**: ISO 18497 emergency stop and safety zone tests
- **Multi-Tractor Coordination**: Vector clock synchronization and conflict resolution
- **Performance Constraints**: Embedded equipment timing requirements

### 6. Advisory Notes

Document any warnings, deprecations, or recommended improvements:

```markdown
### Minor Advisory Note / Critical Issues

[Description of warnings, deprecations, or issues]
[Impact assessment and recommended actions]
```

## Enforcement and Scope

- **Universal Application**: Applies to ALL AI agents on AFS FastAPI platform
- **Cross-Session Persistence**: Requirement embedded permanently in project configuration
- **Agent Agnostic**: Pattern applies regardless of AI platform or implementation
- **Test Commands**: Applies to `pytest`, `pytest -v`, `pytest --cov`, and all testing variations
- **Educational Integration**: Enhanced insights when Explanatory output style active

## File Reference Integration

**MANDATORY**: Use markdown link syntax for all file and code references:

- Files: `[filename.py](path/to/filename.py)`
- Specific lines: `[filename.py:42](path/to/filename.py#L42)`
- Directories: `[tests/unit/equipment/](tests/unit/equipment/)`

**Never use backticks or HTML tags for file references** - always use clickable markdown links.

## Test Execution Commands

When executing tests, use appropriate timeout values:

```bash
# Standard test run
pytest --tb=short -v --timeout=120000

# With coverage
pytest --tb=short -v --cov=afs_fastapi --cov-report=html --timeout=120000

# Specific test file
pytest tests/unit/equipment/test_farm_tractor.py --tb=short -v --timeout=60000

# Quick smoke test
pytest --tb=short -q --timeout=60000
```

## Example Complete Report

```markdown
## Test Suite Execution Complete: All Tests Passing ✓

`★ Insight ─────────────────────────────────────`
**Test Suite Growth**: The platform now has **161 tests** (up from the expected 148), indicating active development. The execution time of **3.26 seconds** demonstrates excellent performance for a comprehensive enterprise test suite.

**3-Layer Architecture**: Tests are organized across Feature (real-world agricultural workflows), Unit (component isolation), and Root-level (edge cases) layers, providing comprehensive coverage from high-level user scenarios down to low-level implementation details.

**Agricultural Robotic Interfaces**: The test suite validates six major categories of professional equipment interfaces—ISOBUS Communication, Safety & Compliance, Motor Control, Data Management, Power Management, and Vision & Sensor Systems—all critical for ISO 11783 and ISO 18497 compliance.
`─────────────────────────────────────────────────`

### Test Results Summary

**Total Tests**: 161 passed (100% success rate)
**Execution Time**: 3.26 seconds
**Platform**: Python 3.12.8 on macOS

### Test Distribution by Category

1. **Feature Tests (API & Workflows)**: 30 tests
   - API endpoint consumption (11 tests)
   - API serialization (7 tests)
   - Engine workflows (5 tests)
   - Farm tractor workflows (5 tests)
   - Root-level edge cases (2 tests)

2. **Unit Tests (Components)**: 131 tests
   - **Equipment** ([tests/unit/equipment/](tests/unit/equipment/)): 57 tests
   - **API Endpoints** ([tests/unit/api/test_main.py](tests/unit/api/test_main.py)): 6 tests
   - **Monitoring Systems** ([tests/unit/monitoring/](tests/unit/monitoring/)): 10 tests
   - **Infrastructure**: 58 tests

### Platform Health Indicators

✓ **Zero Test Failures**: All 161 tests passing
✓ **Fast Execution**: Sub-4-second runtime for comprehensive suite
✓ **Enterprise Standards**: Type checking, async support, comprehensive fixtures operational
✓ **Agricultural Compliance**: ISOBUS and safety systems fully validated
✓ **Vector Clock Synchronization**: Distributed systems foundation operational (11 tests)
✓ **Session Management**: Initialization and enforcement hooks validated (19 tests)
✓ **CHANGELOG Automation**: 13 tests validating automated documentation generation

### Minor Advisory Note

[Description of any warnings or issues]

**AFS FastAPI v0.1.3** remains in excellent health with a robust, comprehensive test suite covering equipment control, API operations, monitoring systems, and synchronization infrastructure.
```

## RATIONALE

Safety-critical agricultural robotics demands consistent, comprehensive test analysis from ALL development assistants (human or AI). Standardized test reporting enables:

- **Quality Validation**: Uniform assessment of platform health across AI assistants
- **Safety Assurance**: Consistent highlighting of ISO compliance and safety-critical tests
- **Educational Value**: Clear explanations of test architecture and significance
- **Decision Support**: Actionable insights for development prioritization
- **Cross-Session Continuity**: Comparable test reports across different sessions and AI platforms

This standardization is essential for maintaining enterprise-grade reliability in multi-tractor coordination systems where test result interpretation directly impacts safety and operational decisions.
