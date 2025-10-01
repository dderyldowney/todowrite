# Universal AI Agent Access: updatedocs Command

> **ABSOLUTE REQUIREMENT**: The `updatedocs` command MUST be available to ALL AI agents (Claude, GitHub Copilot, ChatGPT, Gemini Code Assist, Amazon CodeWhisperer) across ALL development sessions for the AFS FastAPI agricultural robotics platform.

---

## Command Overview

**Purpose**: Meta-command for unified regeneration of all 6 core documentation files ensuring synchronized platform state for ISO compliance auditing, stakeholder communication, and agricultural equipment development visibility.

**Universal Access Level**: **CRITICAL** - ALL AI agents MUST remember and utilize this command

**Cross-Session Persistence**: Embedded in SESSION_SUMMARY.md, AGENTS.md, and CLAUDE.md for automatic loading

---

## Unified Documentation Synchronization

### Meta-Command Architecture

**Command Type**: Orchestration meta-command coordinating multiple specialized documentation tools

**Orchestrated Commands**:
1. `whereweare --generate` - Strategic assessment regeneration
2. `updatewebdocs` - README.md → docs/index.html conversion
3. `updatechangelog` - Version history from git commits
4. `runtests -q` - Platform health validation
5. Session state tracking - Development metrics capture
6. Documentation statistics - Status dashboard synthesis

**Design Pattern**: Single unified interface for complete documentation synchronization

---

## Three Operational Modes

### 1. Update All Mode (Default)

**Command Execution**:
```bash
./bin/updatedocs                  # Manual CLI execution
/updatedocs                       # Claude Code slash command
```

**Purpose**: Regenerate all 6 core documentation files from current platform state

**6 Core Documents Updated**:
1. **WHERE_WE_ARE.md** (Strategic Assessment)
   - Executive summary with platform metrics
   - Strategic positioning and competitive advantages
   - Current release status and capabilities
   - Architectural overview and testing architecture
   - Strategic roadmap and next evolution phases

2. **docs/index.html** (Web Documentation)
   - Professional HTML conversion from README.md
   - Browser-accessible documentation for stakeholders
   - Professional styling for equipment operators and compliance auditors

3. **CHANGELOG.md** (Version History)
   - Automated git history extraction
   - Keep a Changelog formatting with agricultural context
   - Complete version history for ISO compliance auditing

4. **Test Reports** (Platform Health)
   - Comprehensive test suite execution
   - 195+ tests validation with performance metrics
   - Platform health indicators and quality assurance

5. **Session State** (Development Metrics)
   - Current development session status
   - Platform metrics and strategic priorities
   - Enforcement mechanisms and mandatory requirements

6. **Documentation Statistics** (Status Dashboard)
   - Combined status across all core documents
   - Synchronization validation and completeness checks

**Agricultural Context**:
- ISO 11783 (ISOBUS) compliance documentation
- ISO 18497 (Safety) auditing materials
- Multi-tractor coordination status
- Equipment procurement communication materials

### 2. Dry-Run Mode

**Command Execution**:
```bash
./bin/updatedocs --dry-run        # Preview without executing
```

**Purpose**: Display what would be updated without actually executing commands

**Output**: Shows planned updates for all 6 core documents with:
- Document names and descriptions
- Commands that would be executed
- Agricultural context for each update
- Expected outcomes without making changes

**Use Cases**:
- Verify update scope before execution
- Understand which documents need regeneration
- Educational review of documentation architecture

### 3. Selective Update Mode

**Command Execution**:
```bash
./bin/updatedocs --only=whereweare,changelog    # Update specific documents only
./bin/updatedocs --only=webdocs                 # Update only web documentation
```

**Purpose**: Update specific core documents while skipping others

**Valid Document Names**:
- `whereweare` - Strategic assessment (WHERE_WE_ARE.md)
- `webdocs` - Web documentation (docs/index.html)
- `changelog` - Version history (CHANGELOG.md)
- `tests` - Test reports (platform health validation)
- `session` - Session state (development metrics)
- `stats` - Documentation statistics (status dashboard)

**Use Cases**:
- Targeted updates after specific changes
- Performance optimization (skip slow operations)
- Workflow customization for development patterns

---

## Universal AI Agent Requirements

### Cross-Agent Accessibility

**ALL AI agents MUST**:
- Remember this command exists across all sessions
- Execute command when unified documentation updates needed
- Understand three operational modes (update all, dry-run, selective)
- Recognize agricultural context importance
- Coordinate with whereweare, updatewebdocs, updatechangelog commands

**Applies To**:
- Claude Code (primary development assistant)
- GitHub Copilot (code completion and suggestions)
- ChatGPT (chatgpt4-cli package integration)
- Gemini Code Assist (Google AI development assistant)
- Amazon CodeWhisperer (AWS AI coding companion)
- ALL future AI development assistants

### Session Initialization Integration

**Automatic Discovery**:
1. **loadsession** command loads SESSION_SUMMARY.md which documents updatedocs
2. **AGENTS.md** instructs all AI platforms about command availability
3. **CLAUDE.md** provides complete command specifications
4. **.claude/commands/updatedocs** enables slash command execution in Claude Code

**Persistent Memory**:
- Command MUST be remembered after `/new` session restarts
- Universal access ensures all AI agents can use command
- Cross-session persistence through configuration files

---

## Implementation Architecture

### Script Structure

**Primary Script**: [bin/updatedocs](../bin/updatedocs) (267 lines)

**Key Components**:
1. **Argument Parser**: Handles --help, --dry-run, --only=docs, --root=PATH
2. **Update Orchestration**: run_update() helper function for each document
3. **Progress Tracking**: UPDATED_DOCS and FAILED_DOCS counters
4. **Colored Output**: Professional terminal presentation with status indicators
5. **Error Handling**: Graceful failures with clear error messages
6. **Agricultural Context**: ISO compliance messaging throughout

**Helper Functions**:
```bash
should_update()    # Check if document in selective update list
run_update()       # Execute update command with error handling
```

**Output Features**:
- Color-coded status (🔵 Blue headers, 🟢 Green success, 🔴 Red errors, 🟡 Yellow warnings, 🔷 Cyan progress)
- Document-by-document progress reporting
- Summary statistics with success/failure counts
- Agricultural platform status messaging

### Test Coverage

**Test Suite**: [tests/unit/test_updatedocs.py](../tests/unit/test_updatedocs.py) (231 lines, 13 tests)

**Test Categories**:
1. **Existence Tests** (2 tests)
   - Script exists in bin/ directory
   - Script has executable permissions

2. **Functionality Tests** (6 tests)
   - Help flag displays usage information
   - Updates WHERE_WE_ARE.md via whereweare command
   - Updates CHANGELOG.md via updatechangelog command
   - Updates docs/index.html via updatewebdocs command
   - Colored terminal output validation
   - Comprehensive update summary display

3. **Mode Tests** (3 tests)
   - Dry-run mode preview without execution
   - Selective update mode with --only flag
   - Agricultural context inclusion validation

4. **Error Handling** (2 tests)
   - Graceful handling of sub-command failures
   - 6 core documents reference validation

**Agricultural Test Scenarios**:
- ISO compliance auditing workflow
- Stakeholder communication preparation
- Farm equipment procurement documentation
- Autonomous tractor fleet status synchronization

---

## Agricultural Context Essentials

### ISO Compliance Application

**ISO 11783 (ISOBUS) Documentation**:
- WHERE_WE_ARE.md includes ISOBUS compliance status
- CHANGELOG.md tracks ISOBUS implementation changes
- Test reports validate ISOBUS message handling
- Web documentation accessible for compliance auditors

**ISO 18497 (Safety) Documentation**:
- Strategic assessment includes safety system status
- Version history documents safety-critical changes
- Platform health reports validate safety compliance
- Synchronized docs critical for safety audits

### Stakeholder Communication

**Farm Equipment Operators**:
- Web documentation provides browser-accessible status
- Strategic assessment explains multi-tractor coordination capabilities
- Version history shows continuous platform improvements

**Safety Engineers**:
- Test reports validate safety-critical system reliability
- CHANGELOG.md documents all safety-related modifications
- WHERE_WE_ARE.md assesses current safety compliance levels

**Procurement Teams**:
- Comprehensive platform status for equipment purchasing decisions
- Strategic roadmap for future capability planning
- Professional documentation for vendor evaluation

### Development Planning

**Technical Decision-Making**:
- WHERE_WE_ARE.md provides current architectural assessment
- Test reports show platform health and quality metrics
- Session state captures development priorities and focus

**Compliance Tracking**:
- Unified documentation ensures audit-ready materials
- Version history provides complete change tracking
- Synchronized state prevents documentation drift

---

## Command Variations and Usage Patterns

### Common Usage Patterns

**After Major Development Work**:
```bash
# Complete all development changes
git add .
git commit -m "feat(coordination): enhance multi-tractor synchronization for agricultural field operations"

# Update all documentation to reflect changes
./bin/updatedocs

# Verify synchronization
./bin/whereweare
```

**Before Release/Tagging**:
```bash
# Ensure all documentation current
./bin/updatedocs

# Review strategic assessment
./bin/whereweare

# Tag release with synchronized docs
git tag v0.1.4
git push origin v0.1.4
```

**Targeted Updates**:
```bash
# After README.md changes
./bin/updatedocs --only=webdocs

# After git commits
./bin/updatedocs --only=changelog

# After code changes
./bin/updatedocs --only=whereweare,tests
```

**Documentation Review**:
```bash
# Preview what would be updated
./bin/updatedocs --dry-run

# Execute specific updates
./bin/updatedocs --only=whereweare,changelog
```

### Integration with Other Commands

**loadsession Workflow**:
```bash
# 1. Load session context
./bin/loadsession

# 2. View current strategic assessment
./bin/whereweare

# 3. After development work, update all docs
./bin/updatedocs

# 4. Save session state
./bin/savesession
```

**Development Cycle Pattern**:
```bash
# 1. Load session
./bin/loadsession

# 2. Development work (TDD methodology)
# ... code changes ...

# 3. Update documentation
./bin/updatedocs

# 4. Commit with updated docs
git add .
git commit -m "feat: agricultural robotics enhancement"

# 5. Save session state
./bin/savesession
```

---

## Cross-Agent Implementation Examples

### Claude Code Usage

```markdown
User: "Update all platform documentation to reflect the latest changes"

Claude: I'll execute the updatedocs meta-command to regenerate all 6 core documents:

```bash
./bin/updatedocs
```

This will update:
- WHERE_WE_ARE.md (strategic assessment)
- docs/index.html (web documentation)
- CHANGELOG.md (version history)
- Test reports (platform health)
- Session state (development metrics)
- Documentation stats (status dashboard)

The synchronized documentation will be ready for ISO compliance auditing
and stakeholder communication.
```

### GitHub Copilot Completion

```python
# Comment trigger in code:
# updatedocs: Update all 6 core documentation files

# Copilot suggests:
import subprocess

subprocess.run(["./bin/updatedocs"], check=True)
# Updates WHERE_WE_ARE.md, docs/index.html, CHANGELOG.md, test reports,
# session state, and documentation stats for agricultural robotics platform
```

### ChatGPT CLI Integration

```bash
# chatgpt4-cli integration
$ chatgpt "How do I update all AFS FastAPI platform documentation?"

Response: Use the updatedocs meta-command to regenerate all 6 core documents:

./bin/updatedocs               # Update all documents
./bin/updatedocs --dry-run     # Preview updates
./bin/updatedocs --only=whereweare,changelog  # Selective updates

This ensures synchronized documentation for ISO compliance and stakeholder communication.
```

---

## Error Handling and Troubleshooting

### Common Issues

**Issue 1: Sub-command Failures**
```bash
# Error: whereweare --generate fails
# Solution: Check docs/strategic/ directory exists
mkdir -p docs/strategic

# Retry updatedocs
./bin/updatedocs
```

**Issue 2: Permission Errors**
```bash
# Error: Permission denied executing updatedocs
# Solution: Ensure script is executable
chmod +x bin/updatedocs

# Verify permissions
ls -la bin/updatedocs
```

**Issue 3: Missing Dependencies**
```bash
# Error: updatewebdocs not found
# Solution: Ensure all command scripts exist
ls bin/whereweare bin/updatewebdocs bin/updatechangelog

# If missing, restore from repository
git checkout bin/
```

### Validation Steps

**After updatedocs Execution**:
1. Check WHERE_WE_ARE.md updated: `cat docs/strategic/WHERE_WE_ARE.md`
2. Verify web docs generated: `ls docs/index.html`
3. Confirm CHANGELOG.md current: `head -20 CHANGELOG.md`
4. Validate test reports: Recent test execution timestamp
5. Review session state: Current development metrics captured
6. Check documentation stats: All 6 documents synchronized

---

## Cross-Agent Infrastructure Checklist

**Universal Availability Verification**:

- [x] **SESSION_SUMMARY.md**: Command documented in "Universal Session Management Commands" section
- [x] **AGENTS.md**: Command listed in "How to Use" and "Examples" sections
- [x] **CLAUDE.md**: Command specification in "Claude Command Integration" section
- [x] **.claude/UPDATEDOCS_COMMAND_UNIVERSAL.md**: This comprehensive specification created
- [x] **.claude/commands/updatedocs**: Slash command integration file exists
- [x] **tests/unit/test_updatedocs.py**: 13 comprehensive tests validating functionality
- [x] **bin/updatedocs**: 267-line bash script with colored output and error handling
- [x] **Git tracking**: All files version-controlled for team collaboration

**Cross-Agent Memory Requirements**:

- [x] Claude Code: Remembers command via SESSION_SUMMARY.md loaded by loadsession
- [x] GitHub Copilot: Discovers via AGENTS.md and code comments
- [x] ChatGPT: Accesses via CLAUDE.md project instructions
- [x] Gemini Code Assist: Finds via universal documentation standards
- [x] Amazon CodeWhisperer: Learns from cross-referenced specifications

**Agricultural Context Integration**:

- [x] ISO 11783 (ISOBUS) compliance documentation workflows
- [x] ISO 18497 (Safety) auditing material generation
- [x] Multi-tractor coordination status synchronization
- [x] Farm equipment procurement documentation preparation
- [x] Stakeholder communication materials (operators, engineers, procurement)

---

## Maintenance and Evolution

### When to Update This Specification

**MANDATORY Updates Required When**:
1. New core document added to 6-document suite
2. Additional operational mode implemented (beyond update all, dry-run, selective)
3. New orchestrated command integrated
4. Agricultural context requirements change
5. ISO compliance documentation standards updated

### Cross-Agent Synchronization Protocol

**After Specification Updates**:
1. Update SESSION_SUMMARY.md with changes
2. Update AGENTS.md with new capabilities
3. Update CLAUDE.md with enhanced specifications
4. Update .claude/commands/updatedocs.md with usage examples
5. Regenerate test suite for new functionality
6. Validate all AI agents can access updated command

---

## Summary: Universal AI Agent Updatedocs Command

**Critical Attributes**:
- **Meta-Command**: Orchestrates 6 specialized documentation tools
- **Unified Interface**: Single command for complete documentation synchronization
- **Three Modes**: Update all, dry-run, selective updates
- **Universal Access**: ALL AI agents across ALL sessions
- **Agricultural Context**: ISO compliance and stakeholder communication
- **Cross-Session Persistence**: Embedded in SESSION_SUMMARY.md, AGENTS.md, CLAUDE.md

**Success Criteria**:
- ALL AI agents remember and use updatedocs command
- Documentation remains synchronized with platform state
- ISO compliance materials always audit-ready
- Stakeholder communication materials current
- Zero documentation drift across core documents

---

**Document Version**: 1.0.0
**Last Updated**: October 01, 2025
**Specification Status**: Complete - Ready for Universal AI Agent Access
**Agricultural Platform**: AFS FastAPI v0.1.3+
**Universal Availability**: Claude, Copilot, ChatGPT, Gemini, CodeWhisperer, ALL future AI agents
