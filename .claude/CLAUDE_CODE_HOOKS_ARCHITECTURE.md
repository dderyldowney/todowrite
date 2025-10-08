# Claude Code Hooks Architecture for AFS FastAPI

## Overview

The AFS FastAPI agricultural robotics platform uses **Claude Code lifecycle hooks** to enforce Test-First Development methodology, commit quality standards, and safety compliance at the IDE level—intercepting operations before they execute.

This document describes the hook architecture, wrapper implementation, and enforcement behavior.

## Hook System Architecture

### Two-Layer Hook System

The platform uses a **dual-layer hook architecture**:

1. **Claude Code Hooks** (IDE lifecycle layer)
   - Intercept operations before execution in Claude Code IDE
   - Validate user prompts, tool calls, and session initialization
   - Block non-compliant operations before they affect codebase
   - Located in: `.claude/hooks/`

2. **Git Pre-Commit Hooks** (version control layer)
   - Validate commits before they enter repository history
   - Enforce separation of concerns and changelog compliance
   - Provide detailed file-level validation
   - Configured via: `.pre-commit-config.yaml`

### Hook Lifecycle Events

Claude Code provides three lifecycle hook events:

#### SessionStart
**Trigger**: When new Claude Code session begins
**Purpose**: Initialize project context and load session state
**Current Hook**: `session_initialization.py`

**Behavior**:
- Detects new sessions via marker file strategy (5-minute expiration)
- Automatically executes `loadsession` command
- Loads SESSION_SUMMARY.md context
- Restores v0.1.3 platform state and strategic priorities

#### UserPromptSubmit
**Trigger**: When user submits prompt to Claude Code
**Purpose**: Enforce Test-First Development methodology before code generation
**Current Hook**: `user_prompt_tdd_wrapper.py`

**Behavior**:
- Analyzes prompt content for implementation keywords
- Detects code generation requests (add, implement, create, write, build, generate)
- Validates prompt mentions TDD methodology (test, RED-GREEN-REFACTOR, failing test)
- **BLOCKS** prompts requesting implementation without test-first approach
- Provides guidance on proper TDD phrasing

**Example Blocking Scenarios**:
```
❌ "Implement multi-tractor synchronization"
❌ "Add field allocation feature"
❌ "Create ISOBUS communication class"
```

**Example Allowed Prompts**:
```
✅ "Following TDD, implement multi-tractor synchronization"
✅ "Write failing tests first, then add field allocation"
✅ "Using RED-GREEN-REFACTOR, create ISOBUS class"
✅ "Explain how synchronization works" (not implementation)
✅ "Fix the hooks config" (maintenance, not new code)
```

#### PreToolUse
**Trigger**: Before any tool execution (Bash, Write, Edit, Read, etc.)
**Purpose**: Validate operations before they modify codebase or execute commands
**Current Hooks**:
- `session_initialization.py` (runs first for every tool)
- `pre_tool_validation_wrapper.py` (validates git/safety operations)

**Behavior**:
- Intercepts git commit operations
- Validates commit message format (type(scope): description)
- Warns when modifying safety-critical files
- **BLOCKS** malformed git commit messages
- Allows other operations (Read, Grep, file modifications)

## Wrapper Hook Implementation

### Why Wrappers Are Needed

The original enforcement scripts (`tdd_enforcement.py`, `commit_separation_enforcement.py`, etc.) were designed as **git pre-commit hooks**:
- Accept file paths via command-line arguments (`sys.argv`)
- Validate staged files before commit
- No stdin input handling

Claude Code hooks require different interface:
- Read JSON from stdin describing operation context
- Parse tool/prompt data from JSON structure
- Exit with status 0 (allow) or 1 (block)

**Wrappers adapt git hook logic to Claude Code hook interface.**

### Wrapper Architecture

#### user_prompt_tdd_wrapper.py

**Location**: `.claude/hooks/user_prompt_tdd_wrapper.py`
**Lifecycle**: UserPromptSubmit
**Purpose**: Enforce Test-First Development for code generation prompts

**Implementation Pattern**:
```python
def main():
    # Read JSON from stdin
    hook_data = json.loads(sys.stdin.read())

    # Extract prompt text
    user_prompt = hook_data.get("prompt", "")

    # Validate TDD compliance
    validator = TDDPromptValidator()
    is_valid, error_message = validator.validate_prompt(user_prompt)

    if not is_valid:
        print(error_message, file=sys.stderr)
        sys.exit(1)  # BLOCK operation

    sys.exit(0)  # ALLOW operation
```

**Validation Logic**:
1. Check for implementation keywords (implement, add, create, write, build, generate)
2. Allow non-implementation requests (explain, describe, read, search, refactor)
3. For implementation requests: require test/TDD keywords
4. Block requests without test-first approach

#### pre_tool_validation_wrapper.py

**Location**: `.claude/hooks/pre_tool_validation_wrapper.py`
**Lifecycle**: PreToolUse
**Purpose**: Validate git commits and safety-critical file modifications

**Implementation Pattern**:
```python
def main():
    # Read JSON from stdin
    hook_data = json.loads(sys.stdin.read())

    # Extract tool information
    tool_name = hook_data.get("tool", "")
    parameters = hook_data.get("parameters", {})

    # Validate based on tool type
    validator = PreToolValidator()
    is_valid, error_message = validator.validate_tool_operation(hook_data)

    if not is_valid:
        print(error_message, file=sys.stderr)
        sys.exit(1)  # BLOCK operation

    sys.exit(0)  # ALLOW operation
```

**Validation Logic**:
1. **Git Commit Operations**: Extract commit message, validate format
2. **Code Modifications**: Check if safety-critical file, warn if applicable
3. **Other Operations**: Allow without validation

### Relationship to Git Hooks

Git pre-commit hooks (`.git/hooks/pre-commit`) run **independently** via pre-commit framework:

**Separation of Responsibilities**:

| Hook Type | When Runs | What Validates | Enforcement |
|-----------|-----------|----------------|-------------|
| Claude Code UserPromptSubmit | Before prompt processed | TDD methodology in user request | Block non-TDD prompts |
| Claude Code PreToolUse | Before tool executes | Commit message format, safety warnings | Block malformed commits |
| Git pre-commit | Before commit finalizes | File changes, test coverage, changelog, separation | Block non-compliant commits |

**Why Both Are Needed**:
- Claude Code hooks provide **early feedback** (before code is even generated)
- Git hooks provide **comprehensive validation** (after code is written, before history)
- Together they create **defense in depth** for agricultural robotics quality

## Configuration

### settings.local.json

**Location**: `.claude/settings.local.json`

**Hook Registration**:
```json
{
  "hooks": {
    "SessionStart": [
      {
        "matcher": "*",
        "hooks": [
          {
            "type": "command",
            "command": ".claude/hooks/session_initialization.py"
          }
        ]
      }
    ],
    "UserPromptSubmit": [
      {
        "matcher": "*",
        "hooks": [
          {
            "type": "command",
            "command": ".claude/hooks/user_prompt_tdd_wrapper.py"
          }
        ]
      }
    ],
    "PreToolUse": [
      {
        "matcher": "*",
        "hooks": [
          {
            "type": "command",
            "command": ".claude/hooks/session_initialization.py"
          },
          {
            "type": "command",
            "command": ".claude/hooks/pre_tool_validation_wrapper.py"
          }
        ]
      }
    ]
  }
}
```

**Hook Execution Order**:
- Multiple hooks in same lifecycle event run **sequentially**
- If any hook exits non-zero, operation is **blocked**
- PreToolUse runs session_initialization first (for context), then validation

## Testing and Verification

### After IDE Restart

Claude Code should automatically:
1. Load hooks from `.claude/settings.local.json`
2. Execute SessionStart hook when session begins
3. Run UserPromptSubmit hook when you submit prompts
4. Run PreToolUse hooks before every tool execution

### Verification Methods

#### Test SessionStart Hook
1. Execute `/new` to start fresh session
2. First tool use should show: "🚀 AFS FastAPI Session Context Automatically Loaded"
3. Indicates session_initialization.py executed successfully

#### Test UserPromptSubmit Hook
1. Submit prompt: "Implement new tractor coordination feature"
2. Should see: "🚫 TDD METHODOLOGY VIOLATION DETECTED"
3. Indicates user_prompt_tdd_wrapper.py blocked non-TDD request

#### Test PreToolUse Hook
1. Attempt git commit with malformed message: `git commit -m "added stuff"`
2. Should see: "🚫 GIT COMMIT SEPARATION VIOLATION"
3. Indicates pre_tool_validation_wrapper.py blocked non-compliant commit

### Debugging Hook Issues

**Hook Not Firing**:
- Check `.claude/settings.local.json` syntax (must be valid JSON)
- Verify hook scripts are executable: `ls -l .claude/hooks/*.py`
- Confirm hook scripts have `#!/usr/bin/env python3` shebang
- Check Python script has no syntax errors: `python3 .claude/hooks/script.py`

**Hook Blocking Incorrectly**:
- Review wrapper validation logic for false positives
- Check implementation keyword patterns in validators
- Verify allowed operation patterns (explain, describe, etc.)

**Hook Errors**:
- Hooks print errors to stderr (visible in Claude Code output)
- Hooks exit 0 on errors to avoid blocking on infrastructure issues
- Check for JSON parsing errors or missing fields

## Agricultural Context and Rationale

### Why Strict Enforcement?

**Safety-Critical Systems**:
- Multi-tractor coordination systems operate heavy agricultural equipment
- Equipment failures can cause property damage or safety incidents
- ISO 18497 and ISO 11783 compliance require comprehensive validation
- Test-First Development ensures bulletproof reliability

**Code Quality Standards**:
- Agricultural robotics demands enterprise-grade code quality
- Separation of concerns enables surgical fixes during emergencies
- CHANGELOG.md provides audit trail for safety compliance
- Comprehensive testing validates performance constraints

### Enforcement Philosophy

**Zero Exceptions Policy**:
- ALL development (human and AI) must follow Test-First Development
- ALL commits must follow separation of concerns
- ALL commits must include CHANGELOG.md updates
- NO code enters codebase without proper validation

**Defense in Depth**:
- Multiple enforcement layers (IDE hooks + git hooks)
- Early feedback (block before code generation)
- Comprehensive validation (block before commit)
- Agricultural context throughout (safety-first approach)

## Maintenance and Evolution

### Adding New Hooks

To add new enforcement hooks:

1. **Create wrapper script**: `.claude/hooks/new_hook_wrapper.py`
2. **Implement main()**: Read JSON from stdin, validate, exit 0/1
3. **Make executable**: `chmod +x .claude/hooks/new_hook_wrapper.py`
4. **Register in settings**: Add to appropriate lifecycle event
5. **Document behavior**: Update this architecture document

### Modifying Validation Logic

To change validation rules:

1. **Edit wrapper script**: Modify validation patterns/logic
2. **Test changes**: Submit test prompts/operations
3. **Document updates**: Update this architecture document
4. **Consider git hooks**: Update git pre-commit hooks if needed

### Disabling Hooks (Not Recommended)

To temporarily disable enforcement:

1. **Comment out in settings.local.json**: Remove hook from lifecycle event
2. **Restart IDE**: Reload Claude Code configuration
3. **Re-enable after debugging**: Restore hook registration

**WARNING**: Disabling enforcement bypasses safety-critical validation for agricultural robotics platform.

## Related Documentation

- **CLAUDE.md**: Project instructions including TDD requirements
- **TDD_WORKFLOW.md**: Complete Test-First Development methodology
- **TDD_FRAMEWORK_MANDATORY.md**: Comprehensive TDD enforcement policies
- **GIT_COMMIT_SEPARATION_MANDATORY.md**: Commit separation requirements
- **AUTOMATIC_SESSION_INITIALIZATION.md**: Session initialization hook details
- **SESSION_SUMMARY.md**: Current platform state and strategic priorities

---

**Last Updated**: 2025-09-29
**Platform Version**: v0.1.3
**Architecture**: Claude Code Hooks + Git Pre-Commit Hooks
**Purpose**: Enforce Test-First Development and safety standards for agricultural robotics