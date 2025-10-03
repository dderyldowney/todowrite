# Dual TODO State Persistence Mandatory

**AFS FastAPI Agricultural Robotics Platform**
**Universal Requirement for ALL AI Agents**
**Session Continuity Critical Infrastructure**

---

## Mandatory State Persistence Requirements

### **Universal Application**
- **ALL AI agents** (Claude, Copilot, ChatGPT, Gemini, CodeWhisperer) MUST maintain dual TODO state
- **Cross-session continuity** essential for agricultural robotics development momentum
- **Automatic synchronization** prevents context loss between session limits

### **Dual Stack Management**
1. **Strategic Stack**: Long-term agricultural platform objectives
2. **Phase Stack**: Current implementation steps with TDD methodology

### **Automatic State Synchronization**

**Trigger Points** (automatic sync on every):
- Strategic objective creation/completion
- Phase step addition/completion
- Development session start/end
- Any TODO command execution

**Storage System**:
- `.claude/strategic_todos.json` - Strategic objectives persistence
- `.claude/phase_todos.json` - Phase implementation tracking
- `.claude/todo_sync_state.json` - Session handoff metadata

### **Session Initialization Protocol**

**MANDATORY**: Every agent session MUST:
1. Execute `./bin/loadsession` (includes dual TODO context)
2. Auto-load strategic and phase state
3. Display current development momentum
4. Show next priority focus

**Session Termination Protocol**:
1. Execute `./bin/todo-handoff` before ending session
2. Auto-sync state to persistent storage
3. Prepare context for next agent/session

### **Core Commands Integration**

**Strategic Management** (4 commands):
- `strategic-add` - Add development objectives
- `strategic-list` - View strategic priorities
- `strategic-complete` - Mark milestones complete
- `strategic-status` - Progress visualization

**Phase Management** (5 commands):
- `phase-start` - Begin aligned development
- `phase-add` - Add TDD implementation steps
- `phase-complete` - Track step completion
- `phase-status` - Detailed progress view
- `phase-end` - Archive completed phases

**Integrated Management** (3 commands):
- `todo-status` - Unified overview
- `todo-handoff` - Session preparation
- `todo-restore` - Context restoration

### **Cross-Session Continuity**

**Agent Handoff Requirements**:
- Previous agent context fully preserved
- Current work status immediately visible
- Next priorities clearly identified
- Development momentum maintained

**Session Limit Handling**:
- State automatically saved before limit
- Next session loads complete context
- Zero development momentum loss
- Seamless agricultural platform advancement

### **Agricultural Safety Integration**

**Critical for Safety-Critical Systems**:
- ISO 11783/18497 compliance development tracking
- Multi-tractor coordination progress visibility
- Emergency system implementation monitoring
- Field operation readiness assessment

### **Implementation Notes**

**Auto-Sync Integration**: All TODO commands automatically call `./bin/todo-sync --silent` for immediate state persistence.

**Universal Access**: Commands work identically across all AI agents and human sessions.

**Token Efficiency**: Minimal overhead design ensures efficient session token usage while maintaining complete context.

---

## Enforcement

**Automatic Validation**: Session initialization hooks verify dual TODO system operational status.

**Cross-Agent Compliance**: All agents inherit identical TODO management infrastructure.

**Agricultural Platform Continuity**: Essential for professional agricultural robotics development requiring systematic progress tracking across complex multi-session development cycles.

**Universal Standard**: This becomes the mandatory development pattern for all AFS FastAPI agricultural robotics platform work.