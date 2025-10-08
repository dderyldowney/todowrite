# MANDATORY: Automatic Command Creation and Cross-Agent Infrastructure Sharing

> **ABSOLUTE REQUIREMENT**: ANY new session management command MUST automatically trigger universal cross-agent infrastructure sharing across ALL AI agents (Claude Code, GitHub Copilot, ChatGPT, Gemini Code Assist, Amazon CodeWhisperer) with ZERO manual intervention required.
>
> **Active Development**: Claude Code (primary), GitHub Copilot (secondary)
> **Compatible but Inactive**: ChatGPT, Gemini Code Assist, Amazon CodeWhisperer

---

## Policy Statement

**GROUPED AUTOMATION MANDATE**: Command creation and cross-agent sharing are INSEPARABLE operations that MUST occur automatically and atomically.

**Universal Application**: Applies to ALL AI agents across ALL development sessions for the AFS FastAPI agricultural robotics platform.

**Cross-Session Persistence**: This requirement is embedded permanently in project configuration and MUST be remembered by ALL AI agents.

---

## Automatic Sharing Protocol

### Atomic Operation Requirement

**WHEN** any new session management command is created:

```
NEW COMMAND CREATION
        ↓
AUTOMATIC TRIGGER (MANDATORY)
        ↓
┌─────────────────────────────────────────────┐
│  GROUPED CROSS-AGENT INFRASTRUCTURE SHARING │
└─────────────────────────────────────────────┘
        ↓
├─ 1. SESSION_SUMMARY.md update (AUTOMATIC)
├─ 2. AGENTS.md update (AUTOMATIC)
├─ 3. CLAUDE.md update (AUTOMATIC)
├─ 4. .claude/commands/ integration (AUTOMATIC)
├─ 5. Universal specification creation (AUTOMATIC)
└─ 6. Test coverage validation (AUTOMATIC)
        ↓
ALL AI AGENTS HAVE IMMEDIATE ACCESS
```

**ZERO MANUAL STEPS**: The entire sharing pipeline executes automatically without human or AI intervention.

### Mandatory Automation Components

**1. Command Implementation Detection**
- **Trigger**: New file created in `bin/` directory
- **Pattern**: Executable bash script or Python command
- **Action**: Automatic cross-agent sharing workflow initiates

**2. Documentation Generation**
- **SESSION_SUMMARY.md**: Auto-append to "Universal Session Management Commands" section
- **AGENTS.md**: Auto-insert in "How to Use" and "Configuration" sections
- **CLAUDE.md**: Auto-add to "Claude Command Integration" section
- **Format**: Template-based generation with agricultural context

**3. Specification Creation**
- **Location**: `.claude/COMMANDNAME_COMMAND_UNIVERSAL.md`
- **Template**: Standardized universal AI agent specification
- **Content**: Dual-mode operation, cross-agent requirements, agricultural context
- **Automation**: Auto-generated from command metadata

**4. Slash Command Integration**
- **Location**: `.claude/commands/commandname`
- **Format**: Single-line execution trigger
- **Documentation**: Complete `.claude/commands/commandname.md` specification
- **Automation**: Template-based generation with command detection

**5. Test Coverage Validation**
- **Requirement**: MUST have comprehensive test suite
- **Location**: `tests/unit/test_commandname.py`
- **Coverage**: Display, generation, error handling, help text
- **Enforcement**: Pre-commit hook validation

**6. CHANGELOG.md Update**
- **Automation**: `updatechangelog` command runs automatically
- **Format**: Keep a Changelog with agricultural context
- **Timing**: Before commit with command implementation

---

## Universal AI Agent Requirements

### Cross-Agent Accessibility Enforcement

**ALL AI agents MUST**:
- **Detect** new command creation automatically
- **Execute** grouped sharing workflow without prompting
- **Validate** all documentation updates completed
- **Verify** cross-agent accessibility achieved
- **Persist** command knowledge across sessions

**Applies To**:
- Claude Code (primary development assistant) **[ACTIVE]**
- GitHub Copilot (code completion and suggestions) **[ACTIVE]**
- ChatGPT (conversational AI assistant) **[COMPATIBLE - INACTIVE]**
- Gemini Code Assist (Google AI development assistant) **[COMPATIBLE - INACTIVE]**
- Amazon CodeWhisperer (AWS AI coding companion) **[COMPATIBLE - INACTIVE]**

### Session Memory and Persistence

**Cross-Session Requirements**:
1. **Automatic Loading**: `loadsession` loads SESSION_SUMMARY.md with ALL commands
2. **Persistent Configuration**: AGENTS.md instructs all AI platforms permanently
3. **Slash Command Discovery**: `.claude/commands/` directory auto-scanned
4. **Universal Specifications**: All `*_COMMAND_UNIVERSAL.md` files accessible

**Memory Validation**:
- Command MUST be remembered after `/new` session restarts
- Universal access ensures all AI agents discover command
- Cross-session persistence through configuration file updates

---

## Automation Workflow Templates

### Template 1: SESSION_SUMMARY.md Auto-Update

**Location**: Add to "🎯 Universal Session Management Commands" section

**Template**:
```markdown
### {COMMAND_NAME} Command - {BRIEF_DESCRIPTION}

**UNIVERSAL ACCESS**: Available to ALL AI agents (Claude Code, GitHub Copilot, ChatGPT, Gemini Code Assist, Amazon CodeWhisperer) across ALL sessions

**Active Agents**: Claude Code (primary), GitHub Copilot (secondary)

**Purpose**: {DETAILED_PURPOSE_WITH_AGRICULTURAL_CONTEXT}

**Dual-Mode Operation**:

1. **Display Mode** (default):
   ```bash
   ./bin/{command_name}              # {DISPLAY_DESCRIPTION}
   /{command_name}                   # Claude Code slash command
   ```
   - {FEATURE_1}
   - {FEATURE_2}
   - {FEATURE_3}

2. **Generation Mode** (if applicable):
   ```bash
   ./bin/{command_name} --generate   # {GENERATE_DESCRIPTION}
   ```
   - {GENERATION_FEATURE_1}
   - {GENERATION_FEATURE_2}

**Agricultural Context Essentials**:
- **ISO Compliance**: {ISO_COMPLIANCE_DETAILS}
- **Safety Engineering**: {SAFETY_DETAILS}
- **Stakeholder Communication**: {COMMUNICATION_DETAILS}
- **Development Planning**: {PLANNING_DETAILS}

**Implementation Files**:
- **bin/{command_name}**: {IMPLEMENTATION_DESCRIPTION}
- **.claude/commands/{command_name}**: Claude Code slash command integration
- **{additional_files}**: {DESCRIPTIONS}

**Test Coverage**: {N} tests (100% passing)
- {TEST_CATEGORY_1}: {DESCRIPTION}
- {TEST_CATEGORY_2}: {DESCRIPTION}

**Cross-Agent Requirements**:
- **ALL AI agents** MUST remember this command across sessions
- **Universal availability** through session initialization (loadsession)
- **Persistent documentation** in SESSION_SUMMARY.md and AGENTS.md
- **Slash command** integration for Claude Code workflows
```

### Template 2: AGENTS.md Auto-Update

**Location 1**: "How to Use" section

**Template**:
```markdown
- **{CRITICAL_LEVEL}**: {Command purpose}: `./bin/{command_name}` ({description}) - Available to ALL AI agents for {use_case}
```

**Location 2**: "Configuration" section

**Template**:
```markdown
- **Quality gates**: Ruff, Black, MyPy, isort; zero warnings expected ({N} tests maintained)
```

**Location 3**: "Examples" section

**Template**:
```markdown
- **{Command category}**: `./bin/{command_name}` → {action} → {result}
- **{Feature description}**: `./bin/{command_name} --{flag}` {detailed_description}
```

### Template 3: CLAUDE.md Auto-Update

**Location**: "Claude Command Integration" section

**Template**:
```markdown
- **{command_name}**: {Brief description}
  - **Display Mode**: `./bin/{command_name}` {display_description}
  - **Generation Mode**: `./bin/{command_name} --generate` {generate_description}
  - {Key feature 1}
  - {Key feature 2}
  - **Command variations**: `./bin/{command_name}`, `./bin/{command_name} --{flag}`, `/{command_name}` (Claude Code)
  - **Universal Access**: ALL humans and AI agents (Claude Code, GitHub Copilot, ChatGPT, Gemini Code Assist, Amazon CodeWhisperer)
  - **Active Agents**: Claude Code (primary), GitHub Copilot (secondary)
  - **Cross-Session Memory**: Command MUST be remembered by all agents across all sessions
  - **Complete Specification**: See [.claude/commands/{command_name}.md](.claude/commands/{command_name}.md)
```

### Template 4: Universal Specification Auto-Generation

**Filename**: `.claude/{COMMANDNAME}_COMMAND_UNIVERSAL.md`

**Template Structure**:
1. **Command Overview** (Purpose, universal access, cross-session persistence)
2. **Dual-Mode Operation** (Display and generation modes with examples)
3. **Universal AI Agent Requirements** (Cross-agent accessibility, session initialization)
4. **Implementation Architecture** (Core files, test coverage)
5. **Agricultural Robotics Context** (ISO compliance, stakeholder communication)
6. **Usage Examples** (Scenario-based AI agent responses)
7. **Cross-Agent Implementation Checklist** (Validation requirements)
8. **Enforcement and Validation** (Automatic discovery, test validation)
9. **Summary** (Cross-agent requirement statement)

---

## Enforcement Mechanisms

### Pre-Commit Hook Integration

**Hook Name**: `automatic_command_sharing_validation.py`

**Purpose**: Validates that new commands trigger automatic cross-agent sharing

**Validation Checks**:
1. **New Command Detection**: Scans `bin/` for new executable files
2. **Documentation Updates**: Verifies SESSION_SUMMARY.md, AGENTS.md, CLAUDE.md modified
3. **Specification Existence**: Confirms `*_COMMAND_UNIVERSAL.md` created
4. **Slash Command Integration**: Validates `.claude/commands/` entries
5. **Test Coverage**: Ensures comprehensive test suite exists
6. **Agricultural Context**: Confirms agricultural keywords present

**Failure Behavior**:
```
🚨 AUTOMATIC COMMAND SHARING VIOLATION DETECTED

New command detected: bin/{command_name}
Missing required cross-agent infrastructure sharing:

❌ SESSION_SUMMARY.md not updated
❌ AGENTS.md not updated
❌ CLAUDE.md not updated
❌ .claude/{COMMANDNAME}_COMMAND_UNIVERSAL.md not created
❌ .claude/commands/{command_name} not created
❌ Tests not found: tests/unit/test_{command_name}.py

REQUIRED ACTION:
Execute automatic cross-agent sharing workflow for universal AI agent access.

See .claude/AUTOMATIC_COMMAND_SHARING_MANDATORY.md for complete requirements.
```

### AI Agent Enforcement Protocol

**Detection Phase**:
```python
# Pseudocode for AI agent awareness
def detect_new_command():
    """Detect new session management command creation."""
    new_commands = scan_bin_directory()
    for command in new_commands:
        if not is_documented_universally(command):
            trigger_automatic_sharing(command)
```

**Execution Phase**:
```python
def trigger_automatic_sharing(command_name):
    """Execute grouped cross-agent infrastructure sharing."""
    # AUTOMATIC - NO MANUAL STEPS
    update_session_summary(command_name)
    update_agents_md(command_name)
    update_claude_md(command_name)
    create_universal_specification(command_name)
    create_slash_command(command_name)
    validate_test_coverage(command_name)
    update_changelog()

    # VALIDATION
    assert all_agents_have_access(command_name)
```

---

## Agricultural Robotics Context Integration

### Mandatory Context Requirements

**ALL commands MUST include**:
1. **ISO Compliance Application**: How command supports ISO 11783 or ISO 18497
2. **Safety Engineering Use**: Multi-tractor coordination safety implications
3. **Stakeholder Communication**: Equipment procurement and planning support
4. **Development Visibility**: Technical decision-making enablement

**Example Integrations**:
- **whereweare**: ISO compliance planning, strategic assessment
- **loadsession**: Session state restoration with TDD compliance
- **savesession**: Complete state capture for audit trail
- **runtests**: Safety-critical system validation
- **updatechangelog**: Version history for regulatory compliance

### Agricultural Terminology Requirements

**Mandatory Keywords** (at least 2 required in descriptions):
- tractor, field, equipment, ISOBUS, ISO 11783, ISO 18497
- agricultural, farming, coordination, fleet, sensor, monitoring
- safety, emergency, collision, boundary, planting, harvesting
- cultivation, precision, autonomous

---

## Cross-Agent Implementation Examples

### Example 1: New Command "fieldstatus"

**Command Created**: `bin/fieldstatus`

**Automatic Sharing Triggered**:

1. **SESSION_SUMMARY.md** auto-updated:
   ```markdown
   ### fieldstatus Command - Agricultural Field Operation Status

   **UNIVERSAL ACCESS**: Available to ALL AI agents...
   ```

2. **AGENTS.md** auto-updated:
   ```markdown
   - **MONITORING**: Field operation status: `./bin/fieldstatus` (real-time agricultural operation visibility) - Available to ALL AI agents for equipment coordination
   ```

3. **CLAUDE.md** auto-updated:
   ```markdown
   - **fieldstatus**: Display real-time field operation status
     - **Display Mode**: `./bin/fieldstatus` shows active tractor operations
     ...
   ```

4. **Universal spec auto-created**: `.claude/FIELDSTATUS_COMMAND_UNIVERSAL.md`

5. **Slash command auto-created**: `.claude/commands/fieldstatus`

6. **Tests validated**: `tests/unit/test_fieldstatus.py` (13+ tests)

**Result**: ALL AI agents immediately discover and utilize fieldstatus command

### Example 2: Command Enhancement Detection

**Scenario**: Existing command `whereweare` gets new `--format=json` flag

**Automatic Update Triggered**:
- SESSION_SUMMARY.md: Output format section updated
- AGENTS.md: Command variations enhanced
- CLAUDE.md: JSON output documented
- WHEREWEARE_COMMAND_UNIVERSAL.md: Usage examples added
- Tests: JSON format validation tests added

**Zero Manual Intervention**: All documentation auto-synchronized

---

## Validation and Compliance Checklist

### For ALL New Commands

✅ **Automatic Documentation**:
- [ ] SESSION_SUMMARY.md updated (AUTOMATIC)
- [ ] AGENTS.md updated (AUTOMATIC)
- [ ] CLAUDE.md updated (AUTOMATIC)
- [ ] Universal specification created (AUTOMATIC)
- [ ] Slash command integration (AUTOMATIC)
- [ ] CHANGELOG.md updated (AUTOMATIC)

✅ **Cross-Agent Accessibility**:
- [ ] Claude Code can discover command (ACTIVE)
- [ ] GitHub Copilot has access via AGENTS.md (ACTIVE)
- [ ] ChatGPT integration documented (COMPATIBLE - INACTIVE)
- [ ] Gemini Code Assist can utilize (COMPATIBLE - INACTIVE)
- [ ] CodeWhisperer has specifications (COMPATIBLE - INACTIVE)

✅ **Agricultural Context**:
- [ ] ISO compliance use case documented
- [ ] Safety engineering application included
- [ ] Stakeholder communication value explained
- [ ] Agricultural terminology present (2+ keywords)

✅ **Test Coverage**:
- [ ] Display mode tests (if applicable)
- [ ] Generation mode tests (if applicable)
- [ ] Error handling tests
- [ ] Help text validation
- [ ] Agricultural context tests

✅ **Session Persistence**:
- [ ] loadsession loads command documentation
- [ ] All AI agents remember across `/new` restarts
- [ ] Universal specifications accessible
- [ ] Cross-session memory validated

---

## Benefits of Automatic Sharing

### Consistency Guarantees

**BEFORE Automation** (Manual Process):
- ❌ Risk: Forgetting to update AGENTS.md
- ❌ Risk: Incomplete CLAUDE.md documentation
- ❌ Risk: Missing universal specification
- ❌ Risk: Inconsistent command availability across AI agents
- ❌ Risk: Documentation drift between platforms

**AFTER Automation** (Grouped Process):
- ✅ Guarantee: ALL documentation files updated automatically
- ✅ Guarantee: Universal AI agent access ensured
- ✅ Guarantee: Cross-session persistence validated
- ✅ Guarantee: Agricultural context preserved
- ✅ Guarantee: Zero manual steps, zero human error

### Development Velocity

**Time Savings**:
- Manual cross-agent sharing: ~30-45 minutes per command
- Automatic grouped sharing: ~0 minutes (instantaneous)
- **Efficiency Gain**: 100% time elimination for repetitive tasks

**Quality Improvements**:
- Template-based consistency across all commands
- Agricultural context automatically included
- Cross-agent requirements automatically enforced
- Test coverage automatically validated

---

## Summary

**GROUPED AUTOMATION MANDATE**: Command creation and cross-agent infrastructure sharing MUST occur as a single atomic operation with ZERO manual intervention.

**Universal Application**: ALL AI agents (Claude Code, GitHub Copilot, ChatGPT, Gemini Code Assist, Amazon CodeWhisperer) MUST automatically execute grouped sharing workflow when detecting new commands.

**Active Development**: Claude Code (primary), GitHub Copilot (secondary) actively use this workflow
**Compatible but Inactive**: ChatGPT, Gemini Code Assist, Amazon CodeWhisperer have configurations maintained but are not actively enabled

**Cross-Session Persistence**: This requirement is embedded permanently in SESSION_SUMMARY.md, AGENTS.md, and CLAUDE.md ensuring ALL future sessions comply automatically.

**Agricultural Robotics Critical**: Automatic sharing ensures ISO compliance tools, safety engineering commands, and stakeholder communication capabilities are universally available across ALL AI platforms immediately upon creation.

**Enforcement**: Pre-commit hooks validate automatic sharing compliance with zero tolerance for manual-only command creation.

---

**Document Version**: 1.1.0
**Last Updated**: October 1, 2025
**Applies To**: ALL AI agents (Claude Code, GitHub Copilot, ChatGPT, Gemini Code Assist, Amazon CodeWhisperer)
**Active Development**: Claude Code (primary), GitHub Copilot (secondary)
**Compatible but Inactive**: ChatGPT, Gemini Code Assist, Amazon CodeWhisperer
**Status**: MANDATORY - Automatic grouped command sharing required universally
**Rationale**: Safety-critical agricultural robotics demands consistent AI agent capabilities across all platforms
