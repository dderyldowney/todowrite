# saveandpush Command

## Purpose

Executes complete session state preservation and repository synchronization workflow in a single command. Automates the entire process of saving TODO state, session state, staging files, updating documentation, and pushing to remote repository for cross-agent accessibility.

## Command Sequence

```bash
bin/saveandpush
bin/saveandpush "Custom commit message"
bin/saveandpush --help
```

## Expected Output

The command will execute the following 8-step workflow:

1. **Save TODO State**: Synchronizes strategic and phase TODO systems via `todo-sync`
2. **Save Session State**: Captures complete session state via `savesession` command
3. **Check Git Status**: Analyzes working directory for modified files
4. **Stage Files**: Adds all modified and untracked files to git staging area
5. **Update CHANGELOG.md**: Regenerates changelog via `updatechangelog` with triple-layer loop protection
6. **Generate Commit Message**: Creates intelligent commit message based on files changed or uses custom message
7. **Create Git Commit**: Commits with proper separation format and agricultural context
8. **Push to Remote**: Pushes changes to origin repository for cross-agent access

## Usage Context

### When to Execute

- **End of Development Sessions**: Before closing work sessions to preserve all progress
- **After Significant Changes**: When multiple files have been modified and need synchronization
- **Cross-Agent Handoff**: Before switching between AI agents to ensure state continuity
- **Programmatic Automation**: As part of automated workflows requiring complete state preservation
- **Emergency State Preservation**: When session limits are approaching and immediate state saving is critical

### Manual Execution

```bash
# Basic usage - auto-generates commit message
./bin/saveandpush

# With custom commit message
./bin/saveandpush "Implement autonomous navigation feature"

# Display help
./bin/saveandpush --help
```

### Programmatic Execution

AI agents can invoke this command to automatically preserve session state:

```python
# Python example for AI agent automation
import subprocess
result = subprocess.run(['./bin/saveandpush', 'Automated session state preservation'],
                       capture_output=True, text=True, cwd='/path/to/afs_fastapi')
```

## Intelligent Commit Message Generation

The command generates context-aware commit messages based on file patterns:

### Strategic/Phase TODO Changes
- **Pattern**: `strategic_todos.json`, `phase_todos.json` modified
- **Commit Type**: `feat(infrastructure)`
- **Context**: Strategic TODO updates with priority management for equipment coordination

### Documentation Changes
- **Pattern**: `.md` files modified
- **Commit Type**: `docs(session)`
- **Context**: Session documentation updates with agricultural robotics compliance

### Configuration Changes
- **Pattern**: Other configuration files
- **Commit Type**: `config(session)`
- **Context**: Session configuration state for agricultural robotics platform

### Custom Messages
- **Pattern**: User-provided message
- **Commit Type**: `docs(session)`
- **Context**: Custom context with complete session preservation workflow

## Agricultural Robotics Compliance

### ISO 11783/18497 Requirements

- **Complete Version History**: CHANGELOG.md updated maintaining compliance auditing requirements
- **Agricultural Context**: All commits include agricultural robotics context for safety-critical systems
- **Cross-Agent Continuity**: Session state preserved for universal AI platform accessibility
- **Safety Documentation**: Complete development state captured for multi-tractor coordination systems

### Cross-Agent Infrastructure Sharing

- **Universal Compatibility**: Command works across Claude Code, GitHub Copilot, ChatGPT, Gemini, CodeWhisperer
- **State Persistence**: TODO systems, session state, and documentation synchronized for all agents
- **Repository Synchronization**: All changes pushed to remote repository for immediate cross-agent access
- **Command Documentation**: Complete specifications shared across all agent configurations

## Error Handling

### Pre-commit Hook Failures
- **TDD Enforcement**: Validates test-first development compliance
- **Safety Standards**: Ensures agricultural robotics safety standards compliance
- **CHANGELOG Enforcement**: Verifies mandatory CHANGELOG.md inclusion
- **Commit Separation**: Validates single concern rule and agricultural context

### Push Failures
- **Network Issues**: Provides local commit preservation with manual push guidance
- **Remote Conflicts**: Displays conflict resolution instructions
- **Authentication**: Guides through repository access configuration

### No Changes Detected
- **Graceful Handling**: Still preserves TODO and session state even without git changes
- **Status Reporting**: Clear indication when repository is already up to date
- **State Verification**: Confirms all state preservation completed successfully

## Success Metrics

### Complete Workflow Success
```
🎉 Complete Session Save and Push Successful!
============================================
✓ TODO state: Synchronized
✓ Session state: Saved
✓ Files staged: X files
✓ CHANGELOG.md: Updated
✓ Commit: abc1234
✓ Push: origin/develop
```

### Agricultural Context Confirmation
```
🌾 Agricultural Context: Session state preserved for cross-agent
   infrastructure sharing supporting ISO 11783/18497 compliance.
```

## Integration with Other Commands

### Command Dependencies
- **todo-sync**: TODO state synchronization
- **savesession**: Session state preservation
- **updatechangelog**: CHANGELOG.md regeneration
- **git operations**: Staging, committing, pushing

### Workflow Integration
- **Before**: `loadsession` (session initialization)
- **During**: Development work with TODO management
- **After**: `saveandpush` (complete state preservation)
- **Next Session**: `loadsession` (state restoration)

## Cross-Session Benefits

### Knowledge Continuity
- **Strategic Context**: All strategic objectives preserved across sessions
- **Phase Progress**: TDD methodology compliance maintained
- **Agricultural Compliance**: ISO standards tracking continued
- **Development State**: Complete project state accessible to all agents

### Efficiency Gains
- **Single Command**: Replaces 8-step manual workflow
- **Error Prevention**: Automated compliance with platform requirements
- **Time Savings**: Eliminates repetitive state preservation tasks
- **Consistency**: Standardized commit formats and documentation updates

---

**Purpose**: Essential command for maintaining session continuity and cross-agent infrastructure sharing in the AFS FastAPI agricultural robotics platform. Ensures complete development state preservation with ISO compliance and universal AI agent accessibility.