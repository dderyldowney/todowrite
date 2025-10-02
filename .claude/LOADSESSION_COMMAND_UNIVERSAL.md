# Universal AI Agent Access: loadsession Command

**Requirement**: The `loadsession` command must be available to ALL AI agents across all development sessions for the AFS FastAPI agricultural robotics platform.

---

## Command Overview

**Purpose**: Restores complete project context (conceptual, contextual, functional) from SESSION_SUMMARY.md.

**Usage**: Execute immediately after `/new` for all AFS FastAPI sessions.

**Access**: Universal across all AI agents (see [SESSION_SUMMARY.md](../SESSION_SUMMARY.md#universal-ai-agents)).

---

## Command Execution

```bash
./bin/loadsession              # Manual CLI execution
bin/loadsession                # Direct execution
```

**Output Includes**:
- Platform status (version, test metrics, quality status)
- Strategic priority (synchronization infrastructure focus)
- Documentation framework references
- Development environment details
- Mandatory requirements (6 universal frameworks)
- Session management commands

**Agricultural Context**: ISO 11783/18497 compliance, multi-tractor coordination, Test-First Development for safety-critical systems.

---

## AI Agent Requirements

**ALL AI agents must**:
- Execute after `/new` session initialization
- Understand platform state before development work
- Recognize mandatory requirements
- Apply agricultural context to all decisions

**Session Initialization**:
1. Automatic: [.claude/hooks/session_initialization.py](hooks/session_initialization.py) (5-min staleness detection)
2. Manual fallback: `bin/loadsession`
3. Documentation references: AGENTS.md, CLAUDE.md, SESSION_SUMMARY.md

---

## Implementation Architecture

### Core Files

**Executable Script**:
- **bin/loadsession**: Bash script (114 lines) with colored output and comprehensive state restoration
- Displays platform status, strategic priority, documentation framework
- Shows mandatory requirements reminders (TDD, investigation pattern)
- Professional terminal presentation with ANSI color codes

**Context Source**:
- **docs/monitoring/SESSION_SUMMARY.md**: Primary session state documentation (304 lines)
- Contains platform metrics, mandatory requirements, commands, references
- Updated through savesession compaction protocol

**Command Integration**:
- **.claude/commands/loadsession**: Single-line slash command trigger (future)
- **.claude/commands/loadsession.md**: Complete command specification (88 lines)
- **docs/EXECUTION_ORDER.md**: 6-phase session initialization architecture

### Test Coverage

**Comprehensive Validation**: 10 tests for automatic session initialization

**Hook Tests** ([tests/unit/hooks/test_session_initialization.py](../tests/unit/hooks/test_session_initialization.py)):
1. New session detection via staleness
2. Session marker file creation
3. Agent registry updates
4. Automatic loadsession triggering
5. Manual execution fallback
6. 5-minute expiration validation
7. Error handling for missing SESSION_SUMMARY.md
8. Integration with Claude Code hooks
9. Cross-session persistence
10. Agricultural context preservation

**Note**: Command execution itself uses bash script (not Python), so tests focus on automatic initialization hook logic.

---

## Usage Examples

### New Session Initialization

Automatic hook execution or manual `./bin/loadsession` after `/new` command:

- Loads SESSION_SUMMARY.md with platform status
- Displays test suite metrics and strategic priorities
- Shows mandatory requirements reminders
- Presents documentation framework references

### Manual Context Restoration

Execute `./bin/loadsession` if automatic initialization fails. Confirms SESSION_SUMMARY.md loaded with platform status and mandatory requirements.

### Cross-Agent Usage

ALL AI agents (Claude, Copilot, ChatGPT, Gemini, CodeWhisperer) execute command at session start to restore:
- Platform version and test metrics
- Strategic focus and mandatory requirements
- Agricultural context and standards compliance

---

## Enforcement and Validation

**Automatic Discovery**: [.claude/hooks/session_initialization.py](hooks/session_initialization.py) with 5-minute staleness detection and manual fallback.

**Test Coverage**: 10 tests validate session initialization (see `tests/unit/hooks/test_session_initialization.py`).

**Manual Verification**:
```bash
./bin/loadsession                               # Execute command
./bin/whereweare                                # Validate state
```

---

## Session Architecture Integration

**6-Phase Initialization** (see [docs/EXECUTION_ORDER.md](../docs/EXECUTION_ORDER.md)):
1. Automatic hook-based initialization
2. Manual session loading (loadsession role)
3. Conceptual context loading
4. Enforcement & validation
5. Mandatory requirement references
6. Helper commands & utilities

**Related Commands**: See [SESSION_SUMMARY.md - Universal Session Management Commands](../SESSION_SUMMARY.md#universal-session-management-commands) for savesession, whereweare, runtests, and others.

---

## Troubleshooting

### "SESSION_SUMMARY.md not found"

**Cause**: Missing or moved SESSION_SUMMARY.md file
**Solution**:
```bash
# Verify location
ls -la docs/monitoring/SESSION_SUMMARY.md

# If missing, check git history
git log --all --full-history -- docs/monitoring/SESSION_SUMMARY.md
```

### "Automatic loadsession didn't trigger"

**Cause**: Rapid `/new` restart within 5-minute staleness window
**Solution**: Execute manually
```bash
./bin/loadsession
```

### "Permission denied"

**Cause**: Script not executable
**Solution**:
```bash
chmod +x bin/loadsession
```

### "Context not fully understood after loadsession"

**Cause**: AI agent didn't properly parse SESSION_SUMMARY.md
**Solution**:
1. Verify SESSION_SUMMARY.md format is correct
2. Manually read and explain key sections to AI agent
3. Check AI agent logs for parsing errors

---

## Summary

**Universal Requirement**: The `loadsession` command is CRITICAL infrastructure for ALL AI agents working on the AFS FastAPI agricultural robotics platform. It ensures complete project context restoration across sessions, maintaining safety-critical development standards and preventing knowledge loss that could compromise multi-tractor coordination system integrity.

**Cross-Agent Accessibility**: ALL compatible AI agents (Claude Code, GitHub Copilot, ChatGPT, Gemini Code Assist, Amazon CodeWhisperer) MUST remember and execute this command immediately after session initialization to understand platform state, mandatory requirements, and agricultural context.

**Safety-Critical Justification**: Lost session context in agricultural robotics development risks generating code that bypasses Test-First Development, ignores ISO compliance requirements, or misunderstands safety-critical multi-tractor coordination mechanisms—potentially leading to equipment damage, crop loss, or operator injury.

---

**Document Version**: 1.0.0
**Last Updated**: October 2, 2025
**Applies To**: ALL AI agents (Claude Code, GitHub Copilot, ChatGPT, Gemini Code Assist, Amazon CodeWhisperer)
**Active Development**: Claude Code (primary), GitHub Copilot (secondary)
**Compatible but Inactive**: ChatGPT, Gemini Code Assist, Amazon CodeWhisperer
**Status**: MANDATORY - Must execute after `/new` for complete context restoration
**Rationale**: Safety-critical agricultural robotics demands consistent session context across all AI platforms
