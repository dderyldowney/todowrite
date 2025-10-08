# Mandatory Investigation Pattern for ALL AI Agent Responses

## Overview

ALL AI agent responses in the AFS FastAPI project MUST follow a structured investigation pattern that provides complete transparency into the analysis process. This requirement applies universally across ALL sessions, ALL agents (Claude Code, GitHub Copilot, ChatGPT, Gemini Code Assist, Amazon CodeWhisperer), and ALL response types.

**Enforcement Level**: MUST (RFC 2119)
**Scope**: Universal - applies to every AI agent interaction (human or machine)
**Persistence**: Cross-session requirement embedded in project configuration
**Agent Scope**: Requirements apply to ALL compatible agents
**Active Development**: Claude Code (primary), GitHub Copilot (secondary)
**Compatible but Inactive**: ChatGPT, Gemini Code Assist, Amazon CodeWhisperer

## Required Response Structure

Every substantive Claude Code response MUST include:

### 1. Investigation Steps

**Purpose**: Document the systematic methodology used to analyze the question

**Format**:
```markdown
## Investigation Steps

1. **[Action Taken]**: Brief description of what was done
2. **[Action Taken]**: Brief description of what was done
3. **[Action Taken]**: Brief description of what was done
...
```

**Requirements**:
- Use numbered list format for clarity
- Bold the action category (Check, Examine, Verify, Search, etc.)
- Provide concise description of each investigative action
- Present steps in chronological order
- Include both successful and unsuccessful attempts

**Example**:
```markdown
## Investigation Steps

1. **Check session markers**: Examined `.claude/.session_initialized` timestamp
2. **Verify hook configuration**: Read `.claude/settings.local.json` structure
3. **Analyze agent registry**: Parsed `.claude/.agent_registry.json` for recent agents
4. **Examine hook logic**: Reviewed `session_initialization.py` expiration strategy
```

### 2. Files Examined

**Purpose**: Provide complete audit trail of files accessed during investigation

**Format**:
```markdown
## Files Examined

- **[file_path]**: Brief description of why this file was examined
- **[file_path]**: Brief description of why this file was examined
- **[file_path]**: Brief description of why this file was examined
...
```

**Requirements**:
- Use bulleted list with file paths as clickable links when possible
- Bold the file path for visibility
- Explain WHY each file was examined
- Include line numbers or specific sections when relevant
- List files in logical grouping (related files together)

**Example**:
```markdown
## Files Examined

- **[.claude/settings.local.json](.claude/settings.local.json)**: Verify hook registration configuration
- **[.claude/hooks/session_initialization.py](.claude/hooks/session_initialization.py)**: Analyze expiration detection logic (lines 102-145)
- **[bin/loadsession](bin/loadsession)**: Confirm executable exists and is functional
- **[docs/monitoring/SESSION_SUMMARY.md](docs/monitoring/SESSION_SUMMARY.md)**: Verify session state documentation availability
```

### 3. Evidence Collected

**Purpose**: Present factual findings from investigation before drawing conclusions

**Format**:
```markdown
## Evidence Collected

**[Category]**:
- Finding 1
- Finding 2
- Finding 3

**[Category]**:
- Finding 1
- Finding 2
```

**Requirements**:
- Group evidence by logical categories
- Use checkmarks (✅) or crosses (❌) to indicate pass/fail states
- Include actual data (timestamps, file sizes, command output excerpts)
- Present evidence objectively without interpretation
- Show BOTH confirming and contradicting evidence

**Example**:
```markdown
## Evidence Collected

**Hook Configuration**:
- SessionStart hook registered in settings.local.json ✅
- PreToolUse hook includes session_initialization.py ✅
- Configuration JSON syntax valid ✅

**Session Markers**:
- `.session_initialized` modified at 09:38 (6 hours ago)
- `.agent_registry.json` contains 21 agents, last at 20:52
- Current time: ~20:52 (within 5-minute window) ❌

**Hook Execution**:
- No "Session Context Automatically Loaded" message ❌
- Manual `bin/loadsession` execution succeeded ✅
```

### 4. Final Analysis

**Purpose**: Synthesize findings into actionable conclusions and recommendations

**Format**:
```markdown
## Final Analysis

**[Root Cause]**: Clear statement of what caused the issue

**[Why It Happened]**: Explanation of underlying mechanism

**[Impact]**: What this means for the system/user

**[Recommended Solutions]**:
1. Option 1 with trade-offs
2. Option 2 with trade-offs
3. Option 3 with trade-offs
```

**Requirements**:
- Lead with root cause identification
- Explain mechanism/reasoning behind the issue
- Assess impact on system behavior
- Provide multiple solution options with trade-offs
- Use technical accuracy and professional tone
- Avoid marketing language or excessive emphasis

**Example**:
```markdown
## Final Analysis

**Root Cause**: Session initialization hook failed to execute because file-based markers from previous session were less than 5 minutes old, causing `is_new_session()` to return False.

**Why It Happened**: The `/new` command clears Claude Code's memory but doesn't clear filesystem markers in `.claude/`. The 5-minute expiration strategy in `session_initialization.py` lines 118-120 assumes sufficient time between sessions, but rapid `/new` restarts violate this assumption.

**Impact**: New sessions created via `/new` within 5 minutes of previous activity don't trigger automatic loadsession, leaving the agent without critical project context (v0.1.3 state, TDD methodology, synchronization priorities).

**Recommended Solutions**:
1. **Manual marker deletion**: Remove `.claude/.session_initialized` before `/new` (immediate fix, requires user action)
2. **Extended expiration window**: Increase from 5 to 30 minutes (reduces false negatives, increases false positives)
3. **Session ID detection**: Add unique session marker on each `/new` (requires Claude Code support)
4. **Explicit loadsession call**: User runs `bin/loadsession` after `/new` (current workaround, reliable)
```

## Rationale: Why This Pattern Is Mandatory

### Transparency and Verification

**Agricultural Robotics Context**: Safety-critical multi-tractor coordination systems demand verifiable reasoning. Showing investigation methodology enables:
- **Safety validation**: Verify analysis considered all relevant safety factors
- **Decision auditing**: Trace how conclusions were reached for ISO compliance
- **Knowledge transfer**: Learn systematic debugging approaches
- **Error detection**: Identify gaps in reasoning or missed evidence

### Professional Development Standards

**Enterprise-Grade Communication**: Professional software engineering requires:
- **Reproducible analysis**: Others can follow same investigation path
- **Evidence-based conclusions**: All claims supported by documented findings
- **Systematic methodology**: Consistent approach across different problems
- **Educational value**: Dual-purpose functional and instructional mission

### Universal Agent Application

**Agent Enforcement**: This pattern applies to the following AI development assistants:
- **Claude Code**: Anthropic's Claude agent for software development (ACTIVE - PRIMARY)
- **GitHub Copilot**: GitHub's AI pair programming assistant (ACTIVE - SECONDARY)
- **ChatGPT Code Interpreter**: OpenAI's conversational coding assistant (COMPATIBLE - INACTIVE)
- **Gemini Code Assist**: Google's AI-powered development tool (COMPATIBLE - INACTIVE)
- **Amazon CodeWhisperer**: AWS machine learning code generator (COMPATIBLE - INACTIVE)

### Cross-Session Consistency

**Universal Application**: This pattern applies to:
- **Bug investigations**: Root cause analysis for system issues
- **Code reviews**: Explaining why code changes are needed
- **Feature analysis**: Understanding existing system behavior
- **Performance debugging**: Identifying bottlenecks and optimization opportunities
- **Security assessments**: Validating safety-critical operations

## Exceptions and Scope

### When Pattern Is Required

**MUST use investigation pattern for**:
- Questions requiring file examination or code analysis
- Bug reports and system behavior investigations
- Architecture or design decision explanations
- Performance or optimization analyses
- Security or safety-critical assessments

### When Pattern May Be Abbreviated

**MAY abbreviate for**:
- Simple clarification questions with obvious answers
- Direct file read requests ("show me X")
- Straightforward command executions
- Quick status checks

**However**: Even abbreviated responses should maintain transparency about what was checked and why.

## Integration with Existing Requirements

### Relationship to Test-First Development

Investigation pattern complements TDD methodology:
- **RED Phase**: Investigation identifies requirements → write failing test
- **GREEN Phase**: Investigation validates test coverage → implement code
- **REFACTOR Phase**: Investigation assesses code quality → enhance implementation

### Relationship to Educational Output Style

Investigation pattern enhances educational mission:
- **Show methodology**: Teach systematic debugging approaches
- **Explain reasoning**: Make implicit knowledge explicit
- **Professional context**: Demonstrate enterprise-grade analysis practices

### Relationship to Format-First Generation

Investigation pattern requires quality output:
- **Pre-formatted responses**: Use proper markdown structure
- **Clear organization**: Headers, bullets, code blocks properly formatted
- **Agricultural context**: Include domain-specific examples and scenarios

## Cross-Session Persistence

### Integration Points

This requirement is embedded in multiple locations for persistence:

1. **CLAUDE.md**: Project-level instructions loaded by Claude Code
2. **SESSION_SUMMARY.md**: Session state documentation referencing pattern
3. **bin/loadsession**: Session initialization displays pattern reminder
4. **This document**: Complete specification for reference

### Session Initialization Message

When `bin/loadsession` executes, it MUST display:

```
📋 INVESTIGATION PATTERN REQUIREMENT ACTIVE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
ALL responses must follow structured investigation pattern:
  1. Investigation Steps (methodology)
  2. Files Examined (audit trail)
  3. Evidence Collected (factual findings)
  4. Final Analysis (conclusions and recommendations)

Reference: .claude/INVESTIGATION_PATTERN_MANDATORY.md
```

## Enforcement and Verification

### Self-Enforcement

ALL AI agents (Claude Code, GitHub Copilot, ChatGPT, Gemini Code Assist, Amazon CodeWhisperer) MUST:
- Follow pattern for all substantive responses
- Verify response includes all required sections
- Check that evidence supports conclusions
- Ensure agricultural context included where relevant
- Apply pattern regardless of agent implementation or platform

### User Feedback

Users MAY:
- Request pattern compliance if response lacks structure
- Ask for additional investigation steps if analysis incomplete
- Point out missing evidence or unsupported conclusions
- Remind agents of universal pattern requirement across all platforms

### Quality Assurance

Project reviews SHOULD:
- Verify investigation pattern compliance in session logs
- Assess quality of evidence gathering and analysis
- Validate agricultural context appropriately included
- Ensure pattern applied consistently across different AI agents

## Examples

### Good Example: Hook Failure Investigation

```markdown
## Investigation Steps

1. **Check hook configuration**: Examined `.claude/settings.local.json` for SessionStart registration
2. **Verify hook executable**: Confirmed `session_initialization.py` exists and is executable
3. **Analyze session markers**: Inspected `.session_initialized` timestamp and agent registry
4. **Review hook logic**: Read `is_new_session()` method to understand detection strategy
5. **Execute manual test**: Ran `bin/loadsession` to confirm script functionality

## Files Examined

- **[.claude/settings.local.json](.claude/settings.local.json)**: Verify hook registration
- **[.claude/hooks/session_initialization.py](.claude/hooks/session_initialization.py)**: Analyze detection logic (lines 102-145)
- **[.claude/.agent_registry.json](.claude/.agent_registry.json)**: Check recent agent activity
- **[bin/loadsession](bin/loadsession)**: Confirm executable exists and works

## Evidence Collected

**Hook Configuration**:
- SessionStart hook registered ✅
- Hook points to correct script ✅

**Session State**:
- Markers exist from 09:38 session
- Last agent registered at 20:52
- Current time ~20:52 (< 5 minutes) ❌

**Behavior**:
- Automatic loadsession didn't fire ❌
- Manual execution succeeded ✅

## Final Analysis

**Root Cause**: 5-minute expiration window too aggressive for rapid `/new` restarts.

**Recommended Solutions**:
1. Manual marker deletion before `/new`
2. Extended expiration window
3. Explicit loadsession after `/new`
```

### Poor Example: Missing Structure

```markdown
The hook didn't run because the markers were too recent. You should delete the markers before running /new or just run loadsession manually.
```

**Problems**:
- No investigation steps shown
- No files examined documented
- No evidence presented
- No explanation of root cause
- No options/trade-offs discussed

## Related Documentation

- **CLAUDE.md**: Project-level instructions and mandatory requirements
- **WORKFLOW.md**: Testing architecture and quality standards
- **TDD_WORKFLOW.md**: Test-First Development methodology
- **CLAUDE_CODE_HOOKS_ARCHITECTURE.md**: Hook system architecture
- **SESSION_SUMMARY.md**: Current platform state and strategic priorities

---

**Effective Date**: 2025-09-30
**Enforcement Level**: MUST (Universal Requirement)
**Applies To**: ALL AI agents (Claude Code, GitHub Copilot, ChatGPT, Gemini Code Assist, Amazon CodeWhisperer), ALL sessions, ALL response types
**Platform**: AFS FastAPI Agricultural Robotics Platform v0.1.3
**Agent Scope**: Human developers and all compatible AI agents
**Active Development**: Claude Code (primary), GitHub Copilot (secondary)
**Compatible but Inactive**: ChatGPT, Gemini Code Assist, Amazon CodeWhisperer