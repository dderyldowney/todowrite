# Universal AI Agent Access: whereweare Command

> **ABSOLUTE REQUIREMENT**: The `whereweare` command MUST be available to ALL AI agents (Claude, GitHub Copilot, ChatGPT, Gemini Code Assist, Amazon CodeWhisperer) across ALL development sessions for the AFS FastAPI agricultural robotics platform.

---

## Command Overview

**Purpose**: Provides comprehensive platform state assessment for ISO compliance planning, stakeholder communication, and agricultural equipment development visibility.

**Universal Access Level**: **CRITICAL** - ALL AI agents MUST remember and utilize this command

**Cross-Session Persistence**: Embedded in SESSION_SUMMARY.md, AGENTS.md, and CLAUDE.md for automatic loading

---

## Dual-Mode Operation

### Display Mode (Default)

**Command Execution**:
```bash
./bin/whereweare              # Manual CLI execution
/whereweare                   # Claude Code slash command
```

**Purpose**: Display existing WHERE_WE_ARE.md strategic assessment

**Output**: 480+ line comprehensive document including:
- Executive Summary: Platform evolution and current status
- Strategic Positioning: Dual-purpose architecture and market leadership
- Current Release Status: Version metrics and capabilities
- Architectural Overview: 3-layer enterprise architecture
- Testing Architecture: Complete test suite with TDD methodology
- Strategic Roadmap: Next evolution phases and priorities

**Agricultural Context**:
- ISO 11783 (ISOBUS) compliance status
- ISO 18497 (Safety) implementation details
- Multi-tractor coordination capabilities
- Equipment safety engineering status

### Generation Mode

**Command Execution**:
```bash
./bin/whereweare --generate   # Regenerate from current platform state
```

**Purpose**: Synthesize WHERE_WE_ARE.md from authoritative sources ensuring documentation stays synchronized with actual platform state

**Sources Extracted**:
1. **README.md**: Project overview and current capabilities
2. **SESSION_SUMMARY.md**: Platform evolution and development status
3. **Git Metrics**: Version tags (`git describe --tags`), current branch (`git branch --show-current`)
4. **Test Metrics**: Live test counts (`pytest --collect-only`)

**Agricultural Context**: Living documentation prevents drift for:
- Farm equipment safety engineering compliance
- Autonomous tractor fleet management status
- ISO 11783 compliance auditing documentation
- Stakeholder procurement communication

---

## Universal AI Agent Requirements

### Cross-Agent Accessibility

**ALL AI agents MUST**:
- Remember this command exists across all sessions
- Execute command when strategic assessment needed
- Understand dual-mode operation (display vs. generate)
- Recognize agricultural context importance

**Applies To**:
- Claude Code (primary development assistant)
- GitHub Copilot (code completion and suggestions)
- ChatGPT (chatgpt4-cli package integration)
- Gemini Code Assist (Google AI development assistant)
- Amazon CodeWhisperer (AWS AI coding companion)
- ALL future AI development assistants

### Session Initialization Integration

**Automatic Discovery**:
1. **loadsession** command loads SESSION_SUMMARY.md which documents whereweare
2. **AGENTS.md** instructs all AI platforms about command availability
3. **CLAUDE.md** provides complete command specifications
4. **.claude/commands/whereweare** enables slash command execution in Claude Code

**Persistent Memory**:
- Command MUST be remembered after `/new` session restarts
- Universal access ensures all AI agents can use command
- Cross-session persistence through configuration files

---

## Implementation Architecture

### Core Files

**Executable Script**:
- **bin/whereweare**: Bash script (215 lines) with colored output and dual-mode support
- Argument parsing: `--help`, `--generate`, `--root=PATH`
- Error handling for missing documents and source files
- Professional terminal presentation with ANSI color codes

**Document Generator**:
- **docs/generate_where_we_are.py**: Python script (357 lines) for document synthesis
- Extracts git metrics (version, branch)
- Collects test counts via subprocess pytest execution
- Parses README.md and SESSION_SUMMARY.md for platform status
- Generates complete WHERE_WE_ARE.md with current metrics

**Command Integration**:
- **.claude/commands/whereweare**: Single-line slash command trigger
- **.claude/commands/whereweare.md**: Complete command specification (49 lines)
- Enables `/whereweare` execution in Claude Code sessions

### Test Coverage

**Comprehensive Validation**: 13 tests (100% passing)

**Display Tests** (9 tests):
1. Script existence verification
2. Executable permissions validation
3. Document display functionality
4. Strategic sections presence
5. Missing document error handling
6. Help flag functionality
7. Version information inclusion
8. Agricultural context validation
9. Colored terminal output

**Generation Tests** (4 tests):
1. Document creation from sources
2. Current metrics inclusion
3. Existing document updates
4. Source file requirements

**Test File**: [tests/unit/test_whereweare.py](../tests/unit/test_whereweare.py)

---

## Agricultural Robotics Context

### ISO Compliance Critical

**Safety-Critical Documentation**:
- **ISO 18497**: Current implementation status for agricultural equipment safety
- **ISO 11783**: ISOBUS protocol compliance and certification readiness
- **Emergency Systems**: Multi-tractor coordination safety mechanisms
- **Equipment Status**: Fleet coordination capabilities and limitations

**Audit Trail**:
- Always-current documentation for compliance reviews
- Traceable platform evolution through generated timestamps
- Verifiable test coverage metrics for safety validation
- Professional stakeholder communication for procurement

### Stakeholder Communication

**Development Planning**:
- Real-time visibility into multi-tractor coordination readiness
- Current test suite status for quality assurance
- Strategic roadmap for advanced capability planning
- Technical foundation assessment for deployment decisions

**Procurement Support**:
- Professional platform capabilities documentation
- Industry standards compliance verification
- Educational framework value proposition
- Production readiness validation

---

## Usage Examples

### Scenario 1: ISO Compliance Audit

**Context**: Compliance auditor requests current platform certification status

**AI Agent Response**:
```markdown
I'll provide the current ISO compliance status using the whereweare command:

[Execute: ./bin/whereweare]

The strategic assessment shows:
- **ISO 11783 (ISOBUS)**: Complete implementation with authoritative spec references
- **ISO 18497 (Safety)**: Full compliance with PLc/PLd/PLe levels
- **Test Coverage**: 195 tests validating safety-critical systems
- **Quality Status**: Zero warnings, enterprise-grade standards maintained

The platform is ready for compliance auditing with comprehensive documentation.
```

### Scenario 2: Stakeholder Presentation

**Context**: Executive requests platform capabilities summary for procurement meeting

**AI Agent Response**:
```markdown
I'll generate the current platform assessment for your presentation:

[Execute: ./bin/whereweare --generate]

The updated WHERE_WE_ARE.md document now includes:
- Current version: v0.1.3 with 195 passing tests
- Multi-tractor coordination with Vector Clock implementation
- Complete ISOBUS and Safety standards compliance
- Educational framework for professional development

Document available at: docs/strategic/WHERE_WE_ARE.md
```

### Scenario 3: Development Planning

**Context**: Team planning next development phase priorities

**AI Agent Response**:
```markdown
Let me review the current platform state to inform planning:

[Execute: ./bin/whereweare]

Strategic positioning shows:
- **Current Focus**: Synchronization infrastructure development
- **Next Phase**: CRDT implementation for field allocation
- **Foundation Ready**: 195 tests, zero technical debt
- **Capabilities**: Distributed coordination operational

The platform is positioned for advanced synchronization features.
```

---

## Cross-Agent Implementation Checklist

### For ALL AI Development Assistants

✅ **Command Awareness**:
- [ ] Knows whereweare command exists
- [ ] Understands dual-mode operation
- [ ] Recognizes agricultural context importance
- [ ] Can execute command when needed

✅ **Documentation Access**:
- [ ] Can reference SESSION_SUMMARY.md
- [ ] Can reference AGENTS.md
- [ ] Can reference CLAUDE.md
- [ ] Can access .claude/commands/whereweare

✅ **Cross-Session Memory**:
- [ ] Remembers command after session restart
- [ ] Retains understanding of dual modes
- [ ] Maintains agricultural context awareness
- [ ] Persists through configuration reloads

✅ **Universal Application**:
- [ ] Claude Code integration verified
- [ ] GitHub Copilot awareness confirmed
- [ ] ChatGPT accessibility validated
- [ ] Gemini Code Assist compatibility checked
- [ ] CodeWhisperer integration confirmed

---

## Enforcement and Validation

### Automatic Discovery

**Session Initialization**:
1. **loadsession** command automatically loads SESSION_SUMMARY.md
2. SESSION_SUMMARY.md contains comprehensive whereweare documentation
3. ALL AI agents receive command specifications on session start
4. Cross-session persistence ensures command availability

**Configuration Files**:
- SESSION_SUMMARY.md (lines 339-445): Complete command documentation
- AGENTS.md (lines 32, 42, 94): Integration instructions
- CLAUDE.md (lines 474-482): Detailed specifications
- .claude/commands/whereweare: Slash command enablement

### Test Validation

**Automated Testing**:
- 13 comprehensive tests validate command functionality
- Display mode tests ensure proper output
- Generation mode tests verify document synthesis
- Error handling tests confirm graceful failures

**Pre-Commit Hooks**:
- Quality gates validate Python generator (Ruff, Black, MyPy)
- Format compliance ensures professional output
- Agricultural context preserved in all generated content

---

## Summary

The `whereweare` command is a **universal session management tool** providing ALL AI agents with:

1. **Strategic Assessment Access**: Comprehensive platform state visibility
2. **ISO Compliance Support**: Always-current documentation for audits
3. **Stakeholder Communication**: Professional capabilities documentation
4. **Development Planning**: Real-time metrics for technical decisions

**Cross-Agent Requirement**: This command MUST be remembered and utilized by ALL AI development assistants (Claude, Copilot, ChatGPT, Gemini, CodeWhisperer) across ALL sessions for the AFS FastAPI agricultural robotics platform.

**Agricultural Context**: Essential for farm equipment safety engineering, autonomous tractor fleet management, and ISO compliance in safety-critical multi-tractor coordination systems.

---

**Document Version**: 1.0.0
**Last Updated**: October 1, 2025
**Applies To**: ALL AI agents (Claude, GPT, Gemini, Copilot, CodeWhisperer, and future assistants)
**Status**: MANDATORY - Universal cross-agent access required
