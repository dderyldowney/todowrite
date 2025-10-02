# Universal AI Agent Access: runtests Command

> **ABSOLUTE REQUIREMENT**: The `runtests` command MUST be available to ALL AI agents (Claude Code, GitHub Copilot, ChatGPT, Gemini Code Assist, Amazon CodeWhisperer) across ALL development sessions for the AFS FastAPI agricultural robotics platform, and ALL agents MUST provide standardized test reporting format.

---

## Command Overview

**Purpose**: Executes comprehensive test suite with mandatory standardized reporting format ensuring consistent platform health analysis across all AI development assistants.

**Universal Access Level**: **CRITICAL** - ALL AI agents MUST execute this command using standardized reporting

**Cross-Session Persistence**: Embedded in SESSION_SUMMARY.md, AGENTS.md, CLAUDE.md, and TEST_REPORTING_MANDATORY.md for automatic loading

---

## Single-Mode Operation

### Test Execution with Standardized Reporting

**Command Execution**:
```bash
./bin/runtests                      # Standard verbose test run
./bin/runtests -q                   # Quiet mode (less output)
./bin/runtests --coverage           # With HTML coverage report
./bin/runtests tests/unit/equipment/ # Specific test directory
/runtests                           # Claude Code slash command
```

**Purpose**: Execute complete AFS FastAPI test suite (214 tests) with mandatory standardized reporting format required for all AI agents.

**Output Structure**: ALL AI agents MUST provide:
1. **Executive Summary Block**: Pass/fail status with key metrics
2. **Insight Block**: Educational analysis (when Explanatory style active)
3. **Test Distribution Analysis**: Category breakdown with file links
4. **Platform Health Indicators**: Checklist format with ✓/✗ symbols
5. **Agricultural Context**: Safety-critical and ISO compliance highlights
6. **Advisory Notes**: Warnings and recommended improvements

**Agricultural Context**:
- **Safety-Critical Validation**: 214 tests covering multi-tractor coordination safety
- **ISO 11783 Compliance**: ISOBUS communication protocol validation
- **ISO 18497 Compliance**: Agricultural equipment safety system verification
- **Performance Constraints**: Embedded equipment timing requirement validation
- **Emergency Systems**: Multi-tractor coordination safety mechanisms testing

---

## Universal AI Agent Requirements

### Cross-Agent Accessibility

**ALL AI agents MUST**:
- Execute this command for platform health validation
- Provide standardized test reporting format (6 required sections)
- Highlight safety-critical test results
- Include agricultural context in analysis
- Use markdown link syntax for all file references
- Apply Explanatory insights when output style active

**Applies To**:
- Claude Code (primary development assistant) **[ACTIVE]**
- GitHub Copilot (code completion and suggestions) **[ACTIVE]**
- ChatGPT (conversational AI assistant) **[COMPATIBLE - INACTIVE]**
- Gemini Code Assist (Google AI development assistant) **[COMPATIBLE - INACTIVE]**
- Amazon CodeWhisperer (AWS AI coding companion) **[COMPATIBLE - INACTIVE]**
- ALL future AI development assistants

### Mandatory Reporting Format

**EVERY test execution response MUST include**:

#### 1. Executive Summary Block
```markdown
## Test Suite Execution Complete: [All Tests Passing ✓ / Tests Failing ✗]

**Total Tests**: [count] passed/failed ([percentage]% success rate)
**Execution Time**: [seconds/minutes]
**Platform**: [Python version] on [OS]
```

#### 2. Insight Block (Required for Explanatory Style)
```markdown
`★ Insight ─────────────────────────────────────`
**Test Suite Growth**: [Analysis of test count trends and significance]

**3-Layer Architecture**: [Explanation of Feature/Unit/Root test organization]

**Agricultural Robotic Interfaces**: [Coverage of ISOBUS, Safety, Motor Control,
Data Management, Power Management, Vision systems]
`─────────────────────────────────────────────────`
```

#### 3. Test Distribution Analysis
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
   - **Infrastructure**: [count] tests - [hooks, services, scripts, stations]
```

#### 4. Platform Health Indicators
```markdown
### Platform Health Indicators

✓/✗ **Zero Test Failures**: [Status description]
✓/✗ **Fast Execution**: [Performance assessment - sub-4-second target]
✓/✗ **Enterprise Standards**: [Type checking, async, fixtures status]
✓/✗ **Agricultural Compliance**: [ISOBUS ISO 11783, Safety ISO 18497 validation]
✓/✗ **Vector Clock Synchronization**: [Distributed systems status with test count]
✓/✗ **Session Management**: [Infrastructure validation with test count]
✓/✗ **CHANGELOG Automation**: [Documentation generation status with test count]
```

#### 5. Agricultural Context Requirements
**CRITICAL**: Always highlight safety-critical test results:
- **ISOBUS Communication**: ISO 11783 compliance validation status
- **Safety Systems**: ISO 18497 emergency stop and safety zone test results
- **Multi-Tractor Coordination**: Vector clock synchronization validation
- **Performance Constraints**: Embedded equipment timing requirement validation

#### 6. Advisory Notes
```markdown
### Minor Advisory Note / Critical Issues

[Description of warnings, deprecations, performance issues]
[Impact assessment and recommended actions]
```

---

## Implementation Architecture

### Core Files

**Executable Script**:
- **bin/runtests**: Bash script (154 lines) with colored output and comprehensive test execution
- Argument parsing: `-q/--quiet`, `--cov/--coverage`, `--quick`, specific test paths
- Error handling and exit code propagation
- Professional terminal presentation with ANSI color codes
- Mandatory reporting reminder for AI agents

**pytest Configuration**:
- **pytest.ini**: Timeout settings, markers, test discovery patterns
- Default timeout: 120 seconds per test (configurable)
- Comprehensive test collection from tests/ directory

**Command Integration**:
- **.claude/commands/runtests**: Single-line slash command trigger
- **.claude/commands/runtests.md**: Complete command specification (160 lines)
- **.claude/TEST_REPORTING_MANDATORY.md**: Comprehensive reporting requirements (193 lines)

### Test Coverage

**Platform Test Suite**: 214 tests (211 passing, 3 xfail)

**Test Categories**:
1. **Feature Tests (API & Workflows)**: 30 tests
   - API endpoint consumption (11 tests)
   - API serialization (7 tests)
   - Engine workflows (5 tests)
   - Farm tractor workflows (5 tests)
   - Root-level edge cases (2 tests)

2. **Unit Tests (Components)**: 184 tests
   - **Equipment** ([tests/unit/equipment/](tests/unit/equipment/)): 57 tests
   - **API Endpoints** ([tests/unit/api/test_main.py](tests/unit/api/test_main.py)): 6 tests
   - **Monitoring Systems** ([tests/unit/monitoring/](tests/unit/monitoring/)): 10 tests
   - **Infrastructure**: 111 tests (hooks, services, scripts, stations, commands)

**Execution Performance**: Sub-4-second runtime for complete suite (3.26s typical)

---

## Agricultural Robotics Context

### Safety-Critical System Validation

**ISO 18497 Compliance Testing**:
- Emergency stop propagation across multi-tractor fleet
- Safety zone boundary validation for autonomous field operations
- PLc/PLd/PLe safety level verification
- Operator override system functionality testing

**ISO 11783 Compliance Testing**:
- ISOBUS communication protocol validation
- Message frame parsing and generation accuracy
- Equipment interface compatibility verification
- Network management functionality testing

**Multi-Tractor Coordination Testing**:
- Vector clock synchronization validation (11 tests)
- Conflict-free operation ordering verification
- Fleet coordination safety mechanisms
- Distributed system consistency validation

### Regulatory Compliance

**Audit Trail Requirements**:
- Complete test execution history for certification
- Safety-critical test result documentation
- Performance metric validation records
- Quality assurance evidence for regulatory reviews

**Certification Support**:
- ISO compliance evidence generation
- Test coverage metrics for safety systems
- Performance validation for embedded equipment
- Professional documentation for equipment approval processes

---

## Usage Examples

### Scenario 1: Pre-Commit Validation

**Context**: Developer completing feature implementation before commit

**AI Agent Response**:
```markdown
I'll validate platform health before committing changes:

[Execute: ./bin/runtests]

## Test Suite Execution Complete: All Tests Passing ✓

**Total Tests**: 214 passed (100% success rate)
**Execution Time**: 3.26 seconds
**Platform**: Python 3.12.8 on macOS

### Platform Health Indicators

✓ **Zero Test Failures**: All 214 tests passing
✓ **Fast Execution**: Sub-4-second runtime maintained
✓ **Enterprise Standards**: Type checking, async support operational
✓ **Agricultural Compliance**: ISOBUS and safety systems fully validated
✓ **Vector Clock Synchronization**: 11 tests confirm distributed systems operational
✓ **Session Management**: 19 tests validate infrastructure integrity

**Platform ready for commit**: All safety-critical systems validated.
```

### Scenario 2: Coverage Analysis

**Context**: Team lead requests comprehensive test coverage report

**AI Agent Response**:
```markdown
I'll generate a detailed coverage analysis:

[Execute: ./bin/runtests --coverage]

## Test Suite Execution Complete: All Tests Passing ✓

`★ Insight ─────────────────────────────────────`
**Test Suite Growth**: The platform maintains 214 tests with 211 passing
and 3 expected failures (xfail). This represents comprehensive coverage of
the agricultural robotics platform including equipment control, API operations,
and distributed coordination systems.

**3-Layer Architecture**: Tests span Feature tests (real-world agricultural
workflows), Unit tests (component isolation), and Root-level tests (edge cases),
ensuring validation from high-level scenarios to low-level implementation.

**Agricultural Robotic Interfaces**: Complete coverage across six major
categories—ISOBUS Communication (ISO 11783), Safety & Compliance (ISO 18497),
Motor Control, Data Management, Power Management, and Vision & Sensor Systems.
`─────────────────────────────────────────────────`

### Test Distribution by Category

1. **Feature Tests**: 30 tests validating real-world workflows
2. **Unit Tests**: 184 tests covering components and infrastructure

**Coverage Report Generated**: htmlcov/index.html
Review for detailed line-level coverage analysis.
```

### Scenario 3: Safety-Critical Validation

**Context**: Safety engineer reviewing emergency stop system changes

**AI Agent Response**:
```markdown
I'll validate safety-critical systems with specific focus on emergency procedures:

[Execute: ./bin/runtests tests/unit/equipment/]

## Test Suite Execution Complete: All Tests Passing ✓

**Total Tests**: 57 equipment tests passed (100% success rate)
**Execution Time**: 1.12 seconds
**Focus**: Agricultural equipment safety systems

### Platform Health Indicators - Safety Critical

✓ **Emergency Stop Systems**: ISO 18497 validation passing
✓ **Multi-Tractor Coordination**: Vector clock synchronization operational
✓ **Safety Zone Boundaries**: Autonomous field operation constraints validated
✓ **Operator Override**: Manual control system functionality confirmed

### Agricultural Context - Safety Validation

**ISO 18497 Compliance**: All safety system tests passing
- Emergency stop propagation across fleet: VALIDATED
- Safety zone boundary detection: OPERATIONAL
- Operator override mechanisms: FUNCTIONAL

**ISO 11783 Compliance**: ISOBUS communication validated
- Equipment interface protocols: VERIFIED
- Message frame handling: CORRECT

**Recommendation**: Safety-critical systems operational and compliant with
agricultural equipment standards. Changes cleared for production deployment.
```

---

## Cross-Agent Implementation Checklist

**For ALL AI development assistants**:

### Command Execution
- [ ] Can execute `./bin/runtests` command
- [ ] Can parse pytest output correctly
- [ ] Can execute with variations (-q, --coverage, specific paths)
- [ ] Can interpret exit codes (0 = success, non-zero = failures)

### Standardized Reporting
- [ ] Provides Executive Summary Block with pass/fail status
- [ ] Includes Insight Block when Explanatory style active
- [ ] Generates Test Distribution Analysis with category breakdown
- [ ] Creates Platform Health Indicators checklist (✓/✗ format)
- [ ] Highlights Agricultural Context for safety-critical results
- [ ] Documents Advisory Notes for warnings/issues

### File Reference Standards
- [ ] Uses markdown link syntax: `[filename.py](path/to/filename.py)`
- [ ] Never uses backticks or HTML tags for file references
- [ ] Includes line numbers when relevant: `[file.py:42](path/to/file.py#L42)`
- [ ] Links to test directories: `[tests/unit/equipment/](tests/unit/equipment/)`

### Agricultural Context Application
- [ ] Recognizes ISO 11783 (ISOBUS) compliance requirements
- [ ] Understands ISO 18497 (Safety) validation importance
- [ ] Highlights multi-tractor coordination test results
- [ ] Identifies safety-critical test failures immediately
- [ ] Applies performance constraint context (embedded systems)

### Cross-Session Memory
- [ ] Remembers command after session restart
- [ ] Retains standardized reporting requirements
- [ ] Maintains agricultural context awareness
- [ ] Persists through configuration reloads

---

## Enforcement and Validation

### Automatic Discovery

**Session Initialization**:
1. **loadsession** command automatically loads SESSION_SUMMARY.md
2. SESSION_SUMMARY.md references TEST_REPORTING_MANDATORY.md
3. ALL AI agents receive reporting requirements on session start
4. Cross-session persistence ensures consistent reporting

**Configuration Files**:
- SESSION_SUMMARY.md: Complete runtests documentation
- TEST_REPORTING_MANDATORY.md: Comprehensive reporting requirements (193 lines)
- AGENTS.md: Integration instructions for all AI platforms
- CLAUDE.md: Detailed command specifications
- .claude/commands/runtests.md: Complete command reference

### Pre-Commit Validation

**Quality Gates**:
- Pre-commit hooks execute test suite before allowing commits
- Failures block commit until resolved
- Agricultural context validated in test implementations
- Performance thresholds enforced (sub-4-second target)

**Manual Validation**:
```bash
# Verify runtests executable
./bin/runtests --help

# Execute test suite manually
./bin/runtests

# Check coverage
./bin/runtests --coverage

# Validate specific categories
./bin/runtests tests/unit/equipment/
```

---

## Integration with Session Architecture

### 6-Phase Session Initialization

**Complete Flow** ([docs/EXECUTION_ORDER.md](docs/EXECUTION_ORDER.md)):

1. **Automatic Hook-Based Initialization**: SessionStart hook loads context
2. **Manual Session Loading**: `bin/loadsession` includes runtests requirements
3. **Conceptual Context Loading**: TEST_REPORTING_MANDATORY.md loaded
4. **Enforcement & Validation**: Pre-commit hooks execute tests
5. **Mandatory Requirement References**: Complete reporting specifications
6. **Helper Commands & Utilities**: runtests available as session tool

**runtests Role**: Phase 6 (Helper Commands) with Phase 4 (Enforcement) integration

### Related Commands

**loadsession** - Restores complete session context including test reporting requirements
```bash
./bin/loadsession  # Loads TEST_REPORTING_MANDATORY.md specifications
```

**savesession** - Captures test suite status in session state
```bash
./bin/savesession  # Records current test count and health metrics
```

**whereweare** - Displays strategic assessment including test suite status
```bash
./bin/whereweare  # Shows 214 tests in platform metrics
```

**updatechangelog** - Documents test-related changes in version history
```bash
./bin/updatechangelog  # Includes test coverage updates
```

---

## Troubleshooting

### "pytest not found"

**Cause**: pytest not installed in Python environment
**Solution**:
```bash
# Install pytest
pip install pytest pytest-asyncio pytest-timeout

# Verify installation
pytest --version
```

### "Tests failing unexpectedly"

**Cause**: Code changes introduced regressions
**Solution**:
```bash
# Run verbose output for details
./bin/runtests -v

# Check specific failing category
./bin/runtests tests/unit/equipment/ -v

# Review git diff for recent changes
git diff HEAD~1
```

### "Permission denied executing runtests"

**Cause**: Script not executable
**Solution**:
```bash
chmod +x bin/runtests
```

### "Timeout errors during test execution"

**Cause**: Tests exceeding pytest.ini timeout configuration
**Solution**:
```bash
# Check pytest.ini timeout settings
cat pytest.ini | grep timeout

# Increase timeout if needed (edit pytest.ini)
# timeout = 180  # Increase from 120 to 180 seconds
```

### "AI agent not providing standardized reporting"

**Cause**: Agent doesn't have TEST_REPORTING_MANDATORY.md context
**Solution**:
1. Execute `./bin/loadsession` to load complete context
2. Explicitly reference `.claude/TEST_REPORTING_MANDATORY.md`
3. Remind agent of 6-section reporting requirement
4. Verify agent has access to CLAUDE.md instructions

---

## Summary

**Universal Requirement**: The `runtests` command is CRITICAL infrastructure for ALL AI agents working on the AFS FastAPI agricultural robotics platform. It ensures consistent platform health validation with standardized reporting format across all development assistants.

**Cross-Agent Accessibility**: ALL compatible AI agents (Claude Code, GitHub Copilot, ChatGPT, Gemini Code Assist, Amazon CodeWhisperer) MUST execute this command using the mandatory 6-section reporting format to provide consistent, comprehensive, and educational test analysis.

**Safety-Critical Justification**: Agricultural robotics platforms demand rigorous testing with consistent result interpretation. Standardized reporting ensures ALL AI agents highlight safety-critical test failures (ISO 18497 emergency systems, ISO 11783 ISOBUS communication, multi-tractor coordination) with appropriate urgency—preventing deployment of code that could compromise equipment safety or operational integrity.

**Educational Integration**: The mandatory Insight Block (when Explanatory style active) ensures developers understand test suite architecture, platform growth trends, and agricultural robotics interface coverage—fulfilling the platform's dual-purpose mission of functional excellence and professional education.

---

**Document Version**: 1.0.0
**Last Updated**: October 2, 2025
**Applies To**: ALL AI agents (Claude Code, GitHub Copilot, ChatGPT, Gemini Code Assist, Amazon CodeWhisperer)
**Active Development**: Claude Code (primary), GitHub Copilot (secondary)
**Compatible but Inactive**: ChatGPT, Gemini Code Assist, Amazon CodeWhisperer
**Status**: MANDATORY - Standardized reporting required for all test executions
**Rationale**: Safety-critical agricultural robotics demands consistent test analysis across all AI platforms
