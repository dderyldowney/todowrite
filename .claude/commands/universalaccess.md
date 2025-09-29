# universalaccess Command

## Purpose

Enables universal access to the `loadsession` command for ALL Claude Code agents, ensuring persistent project context restoration across all agent types and sessions.

## Command Sequence

```
bin/universalaccess
```

## Expected Output

The command will:

1. **Universal Agent Access**: Ensure ALL agents (main, subagents, specialized) can execute loadsession
2. **Persistent Context**: Maintain project context across session boundaries
3. **Cross-Agent Registry**: Register agent initialization for multi-agent tracking
4. **Global Session State**: Establish persistent session markers for continuity

## Universal Agent Support

### Supported Agent Types

- **Main Claude Code Sessions**: Primary development environment
- **General-Purpose Agents**: Multi-step task automation
- **Specialized Agents**: statusline-setup, output-style-setup
- **Subagents**: Task tool spawned agents
- **Cross-Session Agents**: Persistent across multiple /new invocations

### Access Mechanisms

**Direct Command Access**:
```bash
bin/loadsession  # Primary access method
```

**Hook-Based Access**:
- Automatic execution through PreToolUse hooks
- SessionStart initialization triggers
- UserPromptSubmit context verification

**Agent Registry Access**:
- Multi-agent tracking through `.claude/.agent_registry.json`
- Cross-session persistence via `.claude/.global_session_state`
- Universal access marker at `.claude/.universal_access_enabled`

## Persistent Session Management

### Session Detection Strategies

**Multi-Layered Detection**:
1. **Primary Session Marker**: `.claude/.session_initialized` (per-session)
2. **Global Session State**: `.claude/.global_session_state` (cross-session)
3. **Agent Registry**: `.claude/.agent_registry.json` (multi-agent tracking)
4. **Universal Access**: `.claude/.universal_access_enabled` (all agent types)

### Cross-Session Behavior

**Persistence Mechanisms**:
- 24-hour agent activity window for continuous operation
- Automatic cleanup of stale agent registrations
- Global session state preservation across `/new` commands
- Universal access guarantee for all subsequent agents

## Usage Context

### When to Execute

- **Automatic**: Triggered by hook system for new sessions/agents
- **Manual**: Direct command execution for context restoration
- **Verification**: Ensuring agent has proper project context
- **Troubleshooting**: Resolving context access issues

### Agent Integration

**Seamless Operation**:
- Zero configuration required for new agents
- Automatic context inheritance from parent sessions
- Persistent behavior across agent spawning
- Universal command availability guarantee

## Technical Specifications

### Agent Identification

**Unique Agent IDs**:
```
agent_[8-char-hex]_[timestamp]
```

**Registry Structure**:
```json
{
  "agent_abc12345_1234567890": {
    "initialized_at": 1234567890.123,
    "project_root": "/path/to/project",
    "loadsession_executed": true
  }
}
```

### Environment Variables

**Agent Awareness**:
- `CLAUDE_AGENT_ID`: Unique identifier for current agent
- Passed to loadsession execution for tracking
- Available for agent-specific context customization

### Performance Characteristics

**Optimization Features**:
- Extended timeout (45 seconds) for agent operations
- Graceful failure handling for registry operations
- Non-blocking execution for tool operations
- Minimal overhead for initialized sessions

## Cross-Agent Compatibility

### Agent Communication

**Context Sharing**:
- Shared project root directory context
- Common agent registry for coordination
- Global session state for continuity
- Universal access markers for verification

### Inheritance Patterns

**Parent-to-Child Context**:
- Main session initializes base context
- Subagents inherit initialized state
- Specialized agents access shared context
- Cross-session agents maintain continuity

## Quality Assurance

### Verification Methods

**Access Verification**:
```bash
# Check universal access marker
ls .claude/.universal_access_enabled

# Verify agent registry
cat .claude/.agent_registry.json

# Confirm global session state
ls .claude/.global_session_state

# Execute universal access verification
bin/universalaccess
```

**Context Validation**:
- SESSION_SUMMARY.md availability verification
- Project state documentation access
- Strategic priority context confirmation
- Agricultural robotics domain knowledge validation

## Integration with Project Workflow

### Session Initialization Sequence

1. **Execute `/new`** to start Claude Code session
2. **Universal access hook triggers** automatically
3. **Agent registration** occurs transparently
4. **Context inheritance** from previous sessions
5. **Universal loadsession access** guaranteed for all operations

### Development Continuity

**Seamless Experience**:
- No manual initialization steps required
- Automatic context restoration across sessions
- Universal agent access without configuration
- Persistent behavior across development cycles

## Command Rationale

**Universal Agent Access**: The AFS FastAPI platform requires sophisticated multi-agent coordination for agricultural robotics development. The universalaccess command ensures that ALL agents, regardless of type or spawning method, have immediate access to complete project context through the loadsession mechanism, enabling confident continuation of advanced agricultural robotics development across all agent interactions.

## Version Control

This command specification is version-controlled as part of the .claude/commands/ framework, ensuring consistent team-wide universal access and maintaining the project's professional development standards across all agent types.

---

**Command Type**: Universal Agent Access Management
**Priority**: Critical - Ensures universal context access for all agents
**Dependencies**: loadsession script, hook system, agent registry
**Output**: Universal agent access with persistent session management