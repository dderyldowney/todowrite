# CLAUDE.md

**ToDoWrite PostgreSQL Backend System Configuration**
**Last Updated: 2025-11-24**
**Status: FULLY OPERATIONAL - MCP-FIRST WORKFLOW**

---

## 🚨 **MANDATORY: MCP TOOLS USAGE REQUIREMENT**

**ALL AGENTS MUST USE MCP TOOLS - NEVER BUILT-IN TOOLS**

### ✅ **ACTIVE MCP SERVERS (81 tools total)**
- **filesystem (11 tools)** - File operations - USE INSTEAD OF BUILT-IN TOOLS
- **github-official (40 tools)** - GitHub integration
- **git (12 tools)** - Version control
- **SQLite (6 tools)** - Database operations
- **context7 (2 tools)** - AI assistance
- **docker** - Container management
- **hugging-face (9 tools)** - AI/ML integration

### 🚫 **FORBIDDEN BUILT-IN TOOLS**
- `Read` → Use MCP `read_file`
- `Write` → Use MCP `edit_file`
- `Edit` → Use MCP `edit_file`
- `Glob` → Use MCP `list_directory`
- Direct bash git commands → Use MCP git tools

**See DEVELOPMENT_MANDATES.md for complete requirements including:**
- MCP Tools Usage (MCP-First Workflow)
- TDD Red-Green-Refactor (Always write failing tests first)
- Background Process Management (Always cleanup processes)
- Environment Configuration (Always source environment variables)

---

## 🚀 **System Overview**

**Streamlined PostgreSQL-based Development System**

This project provides a complete, production-ready PostgreSQL backend system with integrated episodic memory and LangChain-powered agent framework.

### **Core Architecture**

- ✅ **PostgreSQL Container**: `mcp-postgres` (auto-restart, port 5433)
- ✅ **Episodic Memory**: PostgreSQL-based conversation search (6,686+ conversations indexed)
- ✅ **LangChain Integration**: Industry-standard agent framework (brainstorming, planning, TDD, implementation, review)
- ✅ **ToDoWrite Models**: Complete 12-layer hierarchy with association tables
- ✅ **Standalone Deployment**: Docker-based solution for any project

---

## 🗄️ **POSTGRESQL DATABASE ARCHITECTURE**

### **📊 Database Inventory (3 Total Databases)**
**Container**: `mcp-postgres` (port 5433, auto-restart)

#### **1. `todowrite` Database - Project Management**
**Purpose**: ToDoWrite development system with 12-layer hierarchy
**Connection**: `postgresql://mcp_user:mcp_secure_password_2024@localhost:5433/todowrite`
**Tables**: 43 total tables
**Core Tables**: goals, concepts, contexts, constraints, requirements, acceptance_criteria, interface_contracts, phases, steps, tasks, subtasks, commands, labels
**Association Tables**: goals_concepts, goals_tasks, concepts_tasks, phase_tasks, step_tasks, requirement_tasks, task_subtasks, subtask_commands, goal_phases, phase_steps
**Data**: 4 goals, 16 concepts, 5 tasks (live project data)
**Usage**: ✅ PRIMARY project management database

#### **2. `mcp_episodic_memory` Database - Conversation Storage**
**Purpose**: Episodic memory system - 6,686+ conversations indexed
**Connection**: `postgresql://mcp_user:mcp_secure_password_2024@localhost:5433/mcp_episodic_memory`
**Tables**: 8 total tables
**Core Tables**: conversations, messages, message_summaries, exchanges, vec_exchanges, tool_calls, queue_operations, schema_migrations
**Features**: Full-text search, vector similarity, adaptive indexing
**Data**: 6,686 conversations, 43,491+ messages
**Usage**: ✅ CONVERSATION search and retrieval

#### **3. `mcp_sessions` Database - Session Management**
**Purpose**: Cross-session conversation persistence and context
**Connection**: `postgresql://mcp_user:mcp_secure_password_2024@localhost:5433/mcp_sessions`
**Tables**: sessions (session tracking and continuity)
**Status**: ✅ ACTIVE - session state management
**Usage**: ✅ CONVERSATION persistence and restoration

### **🔒 DATABASE SEPARATION MANDATE**
- **NEVER** mix data between databases
- **ALWAYS** use `todowrite` for project management
- **ALWAYS** use `mcp_episodic_memory` for conversations
- **ALWAYS** use `mcp_sessions` for session persistence
- **NEVER** assume tables exist - verify with `\dt` commands

### **🚨 NON-NEGOTIABLE TODOWRITE USAGE MANDATE**
- **ALL DEVELOPMENT WORK** MUST start with ToDoWrite planning
- **NO CODE IMPLEMENTATION** without goal/concept/task breakdown
- **ZERO EXCEPTIONS** for "quick fixes" or "simple changes"
- **ALL AGENTS** (Chat, CLI, VSCode) MUST enforce this requirement
- **VERIFICATION REQUIRED**: Before ANY work, confirm active ToDoWrite items exist

**Mandatory Pre-Work Verification:**
```bash
# Verify active goals exist before starting work:
docker exec mcp-postgres psql -U mcp_user -d todowrite -c "SELECT COUNT(*) FROM goals WHERE status = 'active';"

# Check current session has ToDoWrite context:
python .claude/session_manager.py --summary

# Verify TDD compliance before ANY coding:
pytest tests/ -v  # Tests must exist and fail first for new features
```

### **🔬 MANDATORY TDD & RED-GREEN-REFACTOR ENFORCEMENT**
- **ALL CODE** MUST start with failing test (RED phase)
- **NO IMPLEMENTATION** before test failure confirmation
- **GREEN PHASE**: Minimal code to pass test only
- **REFACTOR PHASE**: Improve code while tests pass
- **ZERO EXCEPTIONS** for any anti-TDD patterns

**TDD Workflow Verification:**
```bash
# BEFORE implementing anything:
pytest tests/ -v  # Confirm tests exist and fail

# AFTER implementation:
pytest tests/ -v  # Confirm all tests pass

# NO DIRECT CODING ALLOWED WITHOUT FAILING TESTS FIRST
```

## 🛠️ **Environment Setup**

### **Quick Start**
```bash
# 1. Activate virtual environment
source .venv/bin/activate

# 2. Set Python path for Models API
export PYTHONPATH="lib_package/src:cli_package/src"

# 3. Verify PostgreSQL container
docker ps --filter "name=mcp-postgres"

# 4. Verify database connectivity
docker exec mcp-postgres psql -U mcp_user -d todowrite -c "SELECT COUNT(*) FROM goals;"
```

### **Episodic Memory Commands**
```bash
# Search conversations
source .venv/bin/activate && python .claude/episodic_memory.py --search "your query"

# Index new conversations
python .claude/episodic_memory.py --index

# LangChain agent framework
python .claude/langchain_launcher.py --help
```

### **LangChain Superpowers**
```bash
# Brainstorming
python .claude/langchain_launcher.py brainstorm "your topic"

# Project planning
python .claude/langchain_launcher.py plan "your objective"

# TDD workflow
python .claude/langchain_launcher.py tdd "feature description"

# Implementation guidance
python .claude/langchain_launcher.py implement "task"

# Code review
python .claude/langchain_launcher.py review "code snippet"
```

---

## 🗄️ **Database System**

### **PostgreSQL Databases**
- **`todowrite`**: ToDoWrite models and project data (23 tables, 31 FK constraints)
- **`mcp_episodic_memory`**: Conversation search and memory (6,686+ conversations)
- **`mcp_sessions`**: Cross-session conversation persistence

### **ToDoWrite Database Manager**
```bash
# Interactive database management
python .claude/todowrite_database_manager.py
```

---

## 📚 **ToDoWrite Models API**

### **Usage**
```python
from todowrite.core.models import (
    Goal, Concept, Context, Constraints, Requirements,
    AcceptanceCriteria, InterfaceContract, Phase, Step,
    Task, SubTask, Command, Label
)

# Create instances
goal = Goal(title="My Goal", description="Goal description")
concept = Concept(title="My Concept", description="Concept description")
```

### **ENFORCEMENT:**
- ✅ **ONLY** use existing lib_package Models API
- ❌ **NO** parallel implementations allowed
- ❌ **NO** direct database manipulation without Models API

---

## 🔧 **DATABASE OPERATIONS**

### **Using the Database Manager:**
```bash
# Run the database manager
source $PWD/.venv/bin/activate
export PYTHONPATH="lib_package/src:cli_package/src"
python .claude/todowrite_database_manager.py
```

### **Direct Database Access (for verification):**
```bash
# Check data counts
docker exec mcp-postgres psql -U mcp_user -d todowrite -c "
SELECT 'Goals:', COUNT(*) FROM goals
UNION ALL
SELECT 'Concepts:', COUNT(*) FROM concepts
UNION ALL
SELECT 'Tables:', COUNT(*) FROM information_schema.tables
WHERE table_schema='public' AND table_name NOT IN ('information_schema','pg_catalog');
"
```

---

## 📋 **DEVELOPMENT WORKFLOW**

### **Before Starting Work:**
1. ✅ Verify container running: `docker ps --filter "name=mcp-postgres"`
2. ✅ Test database connectivity
3. ✅ Set PYTHONPATH environment variable
4. ✅ Activate virtual environment

### **Creating Items:**
```python
from .claude.todowrite_database_manager import ToDoWriteDatabaseManager

manager = ToDoWriteDatabaseManager()

# Create goal
goal = manager.create_goal("Title", "Description")

# Create concept
concept = manager.create_layer_item('concept', "Title", "Description")
```

### **Session Persistence:**
- ✅ All work automatically stored in PostgreSQL
- ✅ Cross-session continuity maintained
- ✅ Session tracking via sessions table

---

## 🛡️ **SYSTEM CONSTRAINTS**

### **FORBIDDEN:**
- ❌ Any database files in project root
- ❌ SQLite3 database usage (PostgreSQL ONLY)
- ❌ Creating parallel Models API implementations
- ❌ Modifying container configuration without approval
- ❌ Direct database URL overrides

### **REQUIRED:**
- ✅ All work MUST use existing lib_package Models API
- ✅ All data MUST be stored in PostgreSQL database
- ✅ Virtual environment MUST be activated
- ✅ PYTHONPATH MUST include lib_package/src and cli_package/src

---

## 🧪 **VERIFICATION COMMANDS**

### **Quick System Check:**
```bash
bash .claude/quick_check.sh
```

### **Complete Verification:**
```bash
bash .claude/run_all_tests.sh
```

### **Expected Results:**
- ✅ Goals: ~10 records
- ✅ Concepts: ~14 records
- ✅ Tables: 23 total
- ✅ Foreign Keys: 31 constraints
- ✅ Container: Running with auto-restart

---

## 🚨 **IMPORTANT NOTES**

### **Container Management:**
- ✅ Container has auto-restart policy (`unless-stopped`)
- ✅ Container survives system reboots and Docker upgrades
- ✅ Data persisted via Docker volumes
- ❌ Do NOT manually stop container without approval

### **Database Management:**
- ✅ Uses existing MCP PostgreSQL container (reused infrastructure)
- ✅ Dedicated todowrite database for project management
- ✅ mcp_user credentials from existing container
- ❌ Do NOT create separate PostgreSQL containers

### **Session Continuity:**
- ✅ All work tracked via session_id in sessions table
- ✅ Cross-session data persistence guaranteed
- ✅ Complete audit trail of all actions and decisions
- ✅ Session restoration capabilities implemented

---

## 🎯 **CURRENT STATUS: PRODUCTION READY**

**System Components:**
- ✅ PostgreSQL Backend: COMPLETE (23 tables, 31 FK constraints)
- ✅ Models API Integration: COMPLETE (existing lib_package)
- ✅ Data Persistence: COMPLETE (cross-session)
- ✅ Container Management: COMPLETE (auto-restart)
- ✅ Association System: COMPLETE (10 association tables)
- ✅ Session Tracking: COMPLETE (audit trail)

**Ready for full development work with guaranteed data persistence and session continuity.**

---

## 🔄 **SESSION STATE AUTO-RESTORE**

**When this CLAUDE.md is loaded, the system automatically attempts to restore your previous session state:**

```bash
# This command runs automatically when CLAUDE.md is processed:
source $PWD/.venv/bin/activate && python .claude/session_manager.py --summary
```

**If you see a session summary above, your previous work context has been successfully restored!**

---

## 📋 **QUARTERLY STATUS CHECK**

**Last Session Activity:**
- **Previous Session:** VS Code setup and testing completed
- **Major Accomplishments:** PostgreSQL backend fully operational, VS Code integration documented
- **Current Status:** Ready for continued development
- **Next Steps:** Continue with ToDoWrite development using persistent backend

**Session Continuity:** ✅ **MAINTAINED** - All work preserved in PostgreSQL database
