# CLAUDE.md

**ToDoWrite PostgreSQL Backend System Configuration**
**Last Updated: 2025-11-21**
**Status: FULLY OPERATIONAL**

---

## 🚀 **SYSTEM OVERVIEW**

This project uses a **complete PostgreSQL backend system** built on the existing MCP PostgreSQL container with comprehensive 12-layer hierarchy and cross-association tables.

### **Current Architecture:**
- ✅ **Container**: `mcp-postgres` (running 23+ hours, auto-restart enabled)
- ✅ **Database**: `mcp_tools` with user `mcp_user`
- ✅ **Port**: 5433 (mapped from container port 5432)
- ✅ **Tables**: 23 total tables with complete associations
- ✅ **Models API**: Existing lib_package Models (Goal → ... → Command)
- ✅ **Data**: 10 goals, 14 concepts, 2 tasks, 1 session (27+ total records)

---

## 🛠️ **ENVIRONMENT SETUP**

### **Required Environment Setup:**
```bash
# 1. Activate virtual environment
source $PWD/.venv/bin/activate

# 2. Set Python path for existing Models API
export PYTHONPATH="lib_package/src:cli_package/src"

# 3. Verify container is running
docker ps --filter "name=mcp-postgres"

# 4. Test database connectivity
python -c "
import psycopg2
conn = psycopg2.connect(
    host='localhost', port=5433, database='mcp_tools',
    user='mcp_user', password='mcp_secure_password_2024'
)
print('✅ Database connection: SUCCESS')
conn.close()
"
```

---

## 🗄️ **DATABASE CONFIGURATION**

### **Connection Parameters (CORRECT):**
```python
db_config = {
    'host': 'localhost',
    'port': 5433,                    # ✅ CORRECT: mcp-postgres container
    'database': 'mcp_tools',         # ✅ CORRECT: existing MCP database
    'user': 'mcp_user',              # ✅ CORRECT: existing MCP user
    'password': 'mcp_secure_password_2024'  # ✅ CORRECT: existing password
}
```

### **Table Structure (23 Tables):**
**Core Hierarchy Tables:**
- `todowrite_goals` - Top-level objectives
- `todowrite_concepts` - Strategic concepts linked to goals
- `todowrite_contexts` - Development contexts
- `todowrite_constraints` - Project constraints
- `todowrite_requirements` - Detailed requirements
- `todowrite_acceptance_criteria` - Success criteria
- `todowrite_interface_contracts` - API contracts
- `todowrite_phases` - Project phases
- `todowrite_steps` - Implementation steps
- `todowrite_tasks` - Specific tasks
- `todowrite_subtasks` - Detailed subtasks
- `todowrite_commands` - Executable commands
- `todowrite_sessions` - Cross-session tracking

**Association Tables (10 additional):**
- `todowrite_goal_concepts` - Goals ↔ Concepts (many-to-many)
- `todowrite_goal_tasks` - Goals ↔ Tasks (direct mapping)
- `todowrite_concept_tasks` - Concepts ↔ Tasks (mapping)
- `todowrite_phase_tasks` - Phases ↔ Tasks (phase-to-task)
- `todowrite_step_tasks` - Steps ↔ Tasks (step-to-task)
- `todowrite_requirement_tasks` - Requirements ↔ Tasks
- `todowrite_task_subtasks` - Tasks ↔ SubTasks (decomposition)
- `todowrite_subtask_commands` - SubTasks ↔ Commands (execution)
- `todowrite_goal_phases` - Goals ↔ Phases (planning)
- `todowrite_phase_steps` - Phases ↔ Steps (process)

---

## 📚 **MODELS API (EXISTING SYSTEM)**

### **Import and Usage:**
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
docker exec mcp-postgres psql -U mcp_user -d mcp_tools -c "
SELECT 'Goals:', COUNT(*) FROM todowrite_goals
UNION ALL
SELECT 'Concepts:', COUNT(*) FROM todowrite_concepts
UNION ALL
SELECT 'Tables:', COUNT(*) FROM information_schema.tables
WHERE table_schema='public' AND table_name LIKE 'todowrite_%';
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
- ✅ Session tracking via todowrite_sessions table

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
- ✅ mcp_tools database chosen to avoid conflicts
- ✅ mcp_user credentials from existing container
- ❌ Do NOT create separate PostgreSQL containers

### **Session Continuity:**
- ✅ All work tracked via session_id in todowrite_sessions table
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