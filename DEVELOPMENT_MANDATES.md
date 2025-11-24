# DEVELOPMENT MANDATES

## 🚨 CRITICAL: MANDATORY DEVELOPMENT WORKFLOWS

**ALL AGENTS MUST FOLLOW THESE RULES WITHOUT EXCEPTION**

---

## 1️⃣ MCP TOOLS USAGE MANDATE

### ✅ **USE THESE MCP TOOLS**
- `read_file` instead of Read tool
- `edit_file` instead of Write/Edit tools
- `create_directory` instead of mkdir
- `list_directory` instead of ls/Glob
- `get_file_info` instead of file stat operations
- `directory_tree` for directory structure
- `move_file` for file moves/renames
- MCP git tools for ALL version control
- MCP github tools for ALL GitHub operations

### 🚫 **NEVER USE THESE BUILT-IN TOOLS**
- `Read` → Use MCP `read_file`
- `Write` → Use MCP `edit_file`
- `Edit` → Use MCP `edit_file`
- `Glob` → Use MCP `list_directory`
- `Grep` → Use MCP tools or bash for searching
- Direct bash git commands → Use MCP git tools

---

## 2️⃣ TDD & RED-GREEN-REFACTOR MANDATE

### 🔴 **RED PHASE - ALWAYS FIRST**
1. **WRITE FAILING TEST FIRST** - Always start with a failing test
2. **CONFIRM TEST FAILS** - Run tests to verify failure before implementation
3. **NO IMPLEMENTATION** - Zero code writing before test failure

### 🟢 **GREEN PHASE - MINIMAL IMPLEMENTATION**
1. **MINIMAL CODE ONLY** - Write just enough to pass the failing test
2. **PASSING TESTS REQUIRED** - All tests must pass before proceeding
3. **NO EXTRA FEATURES** - Implement only what the test requires

### 🔄 **REFACTOR PHASE - IMPROVE WHILE GREEN**
1. **TESTS MUST PASS** - All tests stay passing during refactoring
2. **IMPROVE CODE QUALITY** - Clean up, optimize, restructure
3. **MAINTAIN FUNCTIONALITY** - No behavior changes during refactoring

### ✅ **VERIFICATION CHECKPOINTS**
- **BEFORE CODING**: `pytest tests/ -v` (must see failing tests)
- **AFTER IMPLEMENTATION**: `pytest tests/ -v` (must see all passing)
- **AFTER REFACTOR**: `pytest tests/ -v` (must still see all passing)

### 🚫 **ANTI-TDD PATTERNS - FORBIDDEN**
- Writing implementation before tests
- Adding tests after code is "working"
- Skipping RED phase
- Implementing extra features during GREEN phase
- Refactoring without passing tests

---

## 3️⃣ BACKGROUND PROCESS MANAGEMENT MANDATE

### 🔄 **ALWAYS CLEANUP PROCESSES**
1. **IDENTIFY ALL PROCESSES** - List running background processes before starting
2. **KILL EXISTING PROCESSES** - Stop related processes before starting new ones
3. **VERIFY CLEAN STATE** - Confirm no conflicting processes are running
4. **MONITOR PROCESSES** - Track background processes with proper cleanup

### ✅ **MANDATORY CLEANUP COMMANDS**
```bash
# Kill MCP gateway processes
pkill -f "docker mcp gateway"

# Kill Docker containers
docker stop $(docker ps -q --filter "name=mcp*") 2>/dev/null || true
docker rm $(docker ps -aq --filter "name=mcp*") 2>/dev/null || true

# Kill Python processes
pkill -f "python.*mcp" 2>/dev/null || true

# Verify clean state
docker ps --filter "name=mcp*"  # Should show no containers
ps aux | grep "mcp\|gateway" | grep -v grep  # Should show no processes
```

### 📋 **PROCESS MANAGEMENT CHECKLIST**
- [ ] Kill existing MCP gateway processes
- [ ] Stop related Docker containers
- [ ] Remove unused Docker containers/volumes
- [ ] Verify no conflicting processes remain
- [ ] Monitor new background processes
- [ ] Set up proper cleanup on exit

### 🚫 **FORBIDDEN PROCESS BEHAVIORS**
- Starting new processes without killing existing ones
- Leaving zombie processes running
- Ignoring process conflicts
- Skipping verification of clean state
- Starting background processes without monitoring

---

## 4️⃣ ENVIRONMENT CONFIGURATION MANDATE

### 🔧 **ALWAYS SOURCE ENVIRONMENT**
```bash
# Always source environment before running commands
source ~/.env
export PYTHONPATH="lib_package/src:cli_package/src"
source .venv/bin/activate
```

### 📁 **USE ENVIRONMENT VARIABLES**
- `${TODOWRITE_PROJECT_DIR}` - Project directory path
- `${MCP_FILESYSTEM_DATABASE_URL}` - Filesystem database connection
- `${MCP_DATABASE_URL}` - Main database connection
- Never hardcode paths or credentials

---

## 5️⃣ COMPLIANCE VERIFICATION

### ✅ **PRE-WORK CHECKLIST**
Before starting any work, verify:
- [ ] MCP tools are available and preferred over built-ins
- [ ] Test environment is ready (TDD compliance)
- [ ] No conflicting background processes are running
- [ ] Environment variables are properly sourced
- [ ] Required databases and containers are running

### 🔍 **SELF-VERIFICATION QUESTIONS**
Before using any tool or starting any process:
- "Is there an MCP tool that does this instead?"
- "Am I violating the MCP-first mandate?"
- "Have I written a failing test first (TDD)?"
- "Are there conflicting background processes?"
- "Are environment variables properly configured?"

---

## 6️⃣ ENFORCEMENT & VIOLATIONS

### ⚠️ **VIOLATION CONSEQUENCES**
- **MCP Tools Violation**: Immediate session termination
- **TDD Violation**: Code rollback and forced RED phase compliance
- **Process Management Violation**: Forced cleanup and workflow restart
- **Environment Violation**: Configuration reset and proper sourcing

### 🎯 **ZERO TOLERANCE POLICY**
These mandates are **MANDATORY** and **NON-NEGOTIABLE**:
- No exceptions for "quick fixes" or "simple changes"
- No bypassing workflows for convenience
- No assuming compliance without verification
- No proceeding without proper setup

---

**FAILURE TO COMPLY WITH ANY MANDATE = IMMEDIATE WORKFLOW TERMINATION**

---
These mandates are persistent and loaded automatically in every session.
All agents are required to follow these rules without exception.
