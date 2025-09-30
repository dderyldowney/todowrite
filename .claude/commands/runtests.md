# Command: runtests

## Purpose
Execute the complete AFS FastAPI test suite with standardized reporting format required for all AI agents.

## Command Execution

```bash
pytest --tb=short -v --timeout=120000
```

## Expected Output Format

ALL AI agents MUST follow the standardized test reporting pattern when executing this command:

### 1. Executive Summary Block

```markdown
## Test Suite Execution Complete: [All Tests Passing ✓ / Tests Failing ✗]

**Total Tests**: [count] passed/failed ([percentage]% success rate)
**Execution Time**: [seconds/minutes]
**Platform**: [Python version] on [OS]
```

### 2. Insight Block (Required for Explanatory Output Style)

```markdown
`★ Insight ─────────────────────────────────────`
**Test Suite Growth**: [Analysis of test count trends and significance]

**3-Layer Architecture**: [Explanation of Feature/Unit/Root test organization]

**Agricultural Robotic Interfaces**: [Coverage of ISOBUS, Safety, Motor Control, Data Management, Power Management, Vision systems]
`─────────────────────────────────────────────────`
```

### 3. Test Results Summary

```markdown
### Test Results Summary

**Total Tests**: [count] passed ([percentage]% success rate)
**Execution Time**: [time]
**Platform**: [environment details]
```

### 4. Test Distribution Analysis

```markdown
### Test Distribution by Category

1. **Feature Tests (API & Workflows)**: [count] tests
   - API endpoint consumption ([count] tests)
   - API serialization ([count] tests)
   - Engine workflows ([count] tests)
   - [Additional categories with file references]

2. **Unit Tests (Components)**: [count] tests
   - **Equipment** ([tests/unit/equipment/](tests/unit/equipment/)): [count] tests
   - **API Endpoints** ([tests/unit/api/test_main.py](tests/unit/api/test_main.py)): [count] tests
   - **Monitoring Systems** ([tests/unit/monitoring/](tests/unit/monitoring/)): [count] tests
   - **Infrastructure** ([hooks, services, scripts, stations]): [count] tests
```

### 5. Platform Health Indicators

```markdown
### Platform Health Indicators

✓/✗ **Zero Test Failures**: [Status description]
✓/✗ **Fast Execution**: [Performance assessment]
✓/✗ **Enterprise Standards**: [Type checking, async, fixtures status]
✓/✗ **Agricultural Compliance**: [ISOBUS ISO 11783, Safety ISO 18497 validation]
✓/✗ **Vector Clock Synchronization**: [Distributed systems status with test count]
✓/✗ **Session Management**: [Infrastructure validation with test count]
✓/✗ **CHANGELOG Automation**: [Documentation generation status with test count]
```

### 6. Advisory Notes

```markdown
### Minor Advisory Note / Critical Issues

[Description of warnings, deprecations, performance issues]
[Impact assessment and recommended actions]
```

### 7. Closing Statement

```markdown
**AFS FastAPI v[version]** [status assessment with key capabilities summary]
```

## Usage Context

**When to Use**:
- Verifying platform health after development sessions
- Validating test suite status before commits
- Assessing impact of infrastructure changes
- Generating comprehensive test reports for stakeholders

**Mandatory for ALL AI Agents**:
- Claude Code
- GitHub Copilot
- ChatGPT
- Gemini Code Assist
- Amazon CodeWhisporer
- Any other AI development assistant

## Complete Specification

**Reference**: [.claude/TEST_REPORTING_MANDATORY.md](../.claude/TEST_REPORTING_MANDATORY.md)

## Test Command Variations

```bash
# Standard verbose test run
pytest --tb=short -v --timeout=120000

# Quick smoke test
pytest --tb=short -q --timeout=60000

# With coverage report
pytest --tb=short -v --cov=afs_fastapi --cov-report=html --timeout=120000

# Specific test file
pytest tests/unit/equipment/test_farm_tractor.py --tb=short -v --timeout=60000

# Specific test category
pytest tests/features/ --tb=short -v --timeout=60000
pytest tests/unit/equipment/ --tb=short -v --timeout=60000
```

## Integration with Session Management

This command integrates with the AFS FastAPI session management architecture:

- **Automatic Hook-Based Testing**: Pre-commit hooks execute tests before commits
- **Manual Test Execution**: Use this command for on-demand test suite runs
- **Cross-Agent Consistency**: Ensures identical test reporting across all AI platforms
- **Educational Integration**: Enhanced insights provided when Explanatory output style active

## Agricultural Context Requirements

**CRITICAL**: Test reports MUST highlight safety-critical results:

- **ISOBUS Communication**: ISO 11783 compliance validation status
- **Safety Systems**: ISO 18497 emergency stop and safety zone test results
- **Multi-Tractor Coordination**: Vector clock synchronization validation
- **Performance Constraints**: Embedded equipment timing requirement validation

## Example Output

See [.claude/TEST_REPORTING_MANDATORY.md](../.claude/TEST_REPORTING_MANDATORY.md) for complete example output following all required formatting standards.

---

**Purpose**: Ensures consistent, comprehensive, and educational test reporting across all AI development assistants working on the safety-critical AFS FastAPI agricultural robotics platform.
