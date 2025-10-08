# Universal AI Agent Access: runtests Command

**Requirement**: The `runtests` command must be available to ALL AI agents (see [SESSION_SUMMARY.md](../SESSION_SUMMARY.md#universal-ai-agents)) with standardized test reporting format.

---

## Command Overview

**Purpose**: Executes comprehensive test suite (214 tests) with mandatory standardized 6-section reporting format.

**Usage**: Pre-commit validation, coverage analysis, safety-critical system validation.

**Access**: Universal across all AI agents.

---

## Command Execution

```bash
./bin/runtests                      # Standard verbose test run
./bin/runtests -q                   # Quiet mode
./bin/runtests --coverage           # With HTML coverage report
./bin/runtests tests/unit/equipment/ # Specific test directory
```

**Output**: 214 tests (211 passing, 3 xfail) with sub-4-second runtime.

---

## Mandatory Reporting Format

**ALL AI agents MUST provide 6 sections**:

1. **Executive Summary**: Pass/fail status, total tests, execution time, platform
2. **Insight Block**: Test architecture explanation (when Explanatory style active)
3. **Test Distribution**: Category breakdown (Feature tests, Unit tests) with file links
4. **Platform Health Indicators**: Checklist (✓/✗) for zero failures, performance, compliance
5. **Agricultural Context**: ISO 11783, ISO 18497, multi-tractor coordination highlights
6. **Advisory Notes**: Warnings, deprecations, recommended improvements

**File Reference Standard**: Use markdown links `[filename.py](path/to/filename.py)` (never backticks or HTML).

---

## Implementation Architecture

**Executable Script**: bin/runtests (154 lines) with argument parsing, colored output, mandatory reporting reminders

**pytest Configuration**: pytest.ini with 120s timeout, comprehensive test discovery

**Test Coverage**: 214 tests across 3-layer architecture
- Feature Tests (30): API workflows, equipment operations
- Unit Tests (184): Equipment (57), API (6), Monitoring (10), Infrastructure (111)

---

## Usage Patterns

**Pre-Commit Validation**: Execute runtests before commits, provide standardized analysis

**Coverage Analysis**: Use `--coverage` flag, generate htmlcov/index.html report

**Safety-Critical Validation**: Target equipment tests for ISO 18497 compliance verification

---

## Troubleshooting

**pytest not found**: `pip install pytest pytest-asyncio pytest-timeout`

**Tests failing unexpectedly**: Run with `-v` flag, check git diff for recent changes

**Permission denied**: `chmod +x bin/runtests`

**Timeout errors**: Check pytest.ini timeout settings (default 120s)

**AI agent non-compliant reporting**: Execute loadsession, reference TEST_REPORTING_MANDATORY.md

---

## Integration

**Related Commands**:
- `loadsession` - Loads reporting requirements
- `savesession` - Records test suite status
- `whereweare` - Shows test metrics in strategic assessment
- `updatechangelog` - Documents test coverage updates

**Session Architecture Role**: Phase 6 (Helper Commands) with Phase 4 (Enforcement) integration

---

## Summary

**Requirement**: ALL AI agents must execute runtests with standardized 6-section reporting format highlighting safety-critical test results.

**Rationale**: Consistent test analysis ensures all AI platforms identify ISO 18497 emergency systems, ISO 11783 ISOBUS communication, and multi-tractor coordination failures with appropriate urgency—preventing deployment of code that compromises equipment safety.

---

**Version**: 1.0.0 | **Updated**: October 2, 2025 | **Status**: MANDATORY
