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

## 4️⃣ VERIFICATION-BEFORE-CONTINUE MANDATE

### 🔍 **MANDATORY PRE-WORK VERIFICATION - CANNOT BE SKIPPED OR BYPASSED**

**⚠️ CRITICAL: BEFORE STARTING ANY WORK - NO EXCEPTIONS - ABSOLUTELY MANDATORY**

#### **📋 MANDATORY SELF-VERIFICATION QUESTIONS** - Must answer before ANY action:
   - "Is there an MCP tool that does this instead of built-in tools?"
   - "Am I violating the MCP-first mandate?"
   - "Have I written a failing test first (TDD Red-Green-Refactor)?"
   - "Are there conflicting background processes running?"
   - "Are environment variables properly sourced and verified?"
   - "Is my work aligned with ALL development mandates?"

#### **🧠 MANDATE UNDERSTANDING VERIFICATION** - Must confirm understanding of:
   - Read and understood ALL mandates in this DEVELOPMENT_MANDATES.md file
   - Read and understood MCP tools usage requirements completely
   - Understand TDD Red-Green-Refactor process thoroughly
   - Understand background process management requirements completely
   - Understand environment configuration requirements completely

#### **🔧 SYSTEM READINESS VERIFICATION** - Must verify all systems:
   ```bash
   # 1. PostgreSQL container running
   docker ps --filter "name=mcp-postgres"

   # 2. Database connectivity tested
   docker exec mcp-postgres psql -U mcp_user -d todowrite -c "SELECT COUNT(*) FROM goals;"

   # 3. Environment variables sourced and verified
   echo "Project Dir: ${TODOWRITE_PROJECT_DIR}"
   echo "Database URL: ${MCP_FILESYSTEM_DATABASE_URL}"

   # 4. No conflicting processes running
   ps aux | grep -E "(mcp|gateway)" | grep -v grep || echo "Clean process state verified"
   ```

#### **📝 WORK PREPARATION VERIFICATION** - Must confirm work is properly prepared:
   - Active ToDoWrite items exist for the current task
   - Session context is properly loaded and fully understood
   - Task is properly broken down into manageable, clear steps
   - Implementation approach fully aligns with all development mandates
   - All required prerequisites are verified and ready

### ✅ **MANDATORY VERIFICATION COMMANDS** - Must pass ALL before ANY work:
```bash
# 1. Verify PostgreSQL container is running and accessible
docker ps --filter "name=mcp-postgres"

# 2. Test database connectivity to todowrite database
docker exec mcp-postgres psql -U mcp_user -d todowrite -c "SELECT COUNT(*) FROM goals;"

# 3. Verify environment variables are properly sourced and accessible
echo "Project Directory: ${TODOWRITE_PROJECT_DIR}"
echo "ToDoWrite Database: ${TODOWRITE_DATABASE_URL}"

# 4. Verify clean process state (no conflicting MCP processes)
echo "Checking for conflicting processes..."
if pgrep -f "docker mcp gateway" > /dev/null; then
    echo "❌ ERROR: Conflicting MCP gateway processes found!"
    echo "❌ Run: pkill -f 'docker mcp gateway' and try again"
    exit 1
else
    echo "✅ Clean process state verified"
fi

# 5. Verify TDD readiness for code implementation tasks
if [ -d "tests" ]; then
    echo "🔴 TDD Readiness Check - Must see failing tests for NEW features:"
    pytest tests/ -v || echo "⚠️ WARNING: No tests found - Create failing tests first!"
fi

# 6. Interactive verification prompts (cannot be automated)
echo "📋 MANDATORY UNDERSTANDING CONFIRMATION:"
echo "   ✅ Have you read and understood DEVELOPMENT_MANDATES.md? (MUST confirm)"
echo "   ✅ Do you understand MCP-first workflow requirements? (MUST confirm)"
echo "   ✅ Do you understand TDD Red-Green-Refactor process? (MUST confirm)"
echo "   ✅ Do you understand background process management? (MUST confirm)"
echo "   ✅ Do you understand all zero-tolerance policies? (MUST confirm)"
```

### 🚫 **ANTI-VERIFICATION PATTERNS - STRICTLY FORBIDDEN**
- **NEVER** skip verification for "quick fixes" or "simple changes" - NO EXCEPTIONS
- **NEVER** assume compliance without explicit, thorough verification
- **NEVER** proceed without answering ALL verification questions completely
- **NEVER** start work without confirming clean process state
- **NEVER** implement without confirming TDD readiness (for code tasks)
- **NEVER** bypass ANY verification step for convenience or speed
- **NEVER** proceed until ALL verification steps pass successfully

### ⚠️ **ABSOLUTE ZERO-TOLERANCE VERIFICATION POLICY**
- **VERIFICATION FAILURE = IMMEDIATE WORKFLOW TERMINATION** - No exceptions
- **NO SKIPPING** - All verification steps are absolutely mandatory for ALL work
- **NO SHORTCUTS** - No exceptions for any reason whatsoever
- **NO ASSUMPTIONS** - Must verify explicitly and thoroughly
- **NO PROCEEDING** - Must pass ALL verification before ANY work begins
- **RESTART REQUIRED** - If any verification fails, must fix issues and restart verification

---

## 5️⃣ ENVIRONMENT CONFIGURATION MANDATE

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
