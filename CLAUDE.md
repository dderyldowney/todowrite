# CLAUDE.md

**ToDoWrite PostgreSQL Backend System Configuration**
**Last Updated: 2025-11-22**
**Status: FULLY OPERATIONAL**

---

## ⚠️ **CRITICAL: COMPREHENSIVE MANDATE**

**ALL DEVELOPMENT REQUIREMENTS - ZERO EXCEPTIONS**

### **MANDATORY COMPLIANCE:**
- **ToDoWrite Planning**: ALL work MUST start with goal/concept/task breakdown
- **TDD Enforcement**: Red-Green-Refactor cycle REQUIRED for all code
- **System Separation**: Never mix ToDoWrite with session storage
- **HAL Token Optimization**: Mandatory monitoring and enforcement

**SEE:** [`.claude/STREAMLINED_MANDATE.md`](./.claude/STREAMLINED_MANDATE.md) for complete requirements
**SEE:** [`.claude/SYSTEM_SEPARATION_MANDATE.md`](./.claude/SYSTEM_SEPARATION_MANDATE.md) for system separation rules

---

## 🚀 **SYSTEM OVERVIEW**

This project uses a **complete PostgreSQL backend system** built on the existing MCP PostgreSQL container with comprehensive 12-layer hierarchy and association tables.

### **Current Architecture:**
- ✅ **Container**: `mcp-postgres` (running 23+ hours, auto-restart enabled)
- ✅ **Database**: `mcp_tools` with user `mcp_user`
- ✅ **Port**: 5433 (mapped from container port 5432)
- ✅ **Tables**: 42 total tables with complete associations
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

### **Table Structure (42 Tables):**
**Core Hierarchy Tables (12):**
- `goals` - Top-level objectives
- `concepts` - Strategic concepts linked to goals
- `contexts` - Development contexts
- `constraints` - Project constraints
- `requirements` - Detailed requirements
- `acceptance_criteria` - Success criteria
- `interface_contracts` - API contracts
- `phases` - Project phases
- `steps` - Implementation steps
- `tasks` - Specific tasks
- `sub_tasks` - Detailed subtasks
- `commands` - Executable commands

**Supporting Tables:**
- `labels` - Tags and categorization
- `sessions` - Cross-session tracking

**Association Tables (28):**
- `goals_concepts`, `goals_contexts`, `goals_labels`, `goals_phases`, `goals_tasks`
- `concepts_contexts`, `concepts_labels`, `requirements_concepts`, `requirements_contexts`, `requirements_labels`
- `constraints_goals`, `constraints_labels`, `constraints_requirements`
- `acceptance_criteria_labels`, `acceptance_criteria_interface_contracts`
- `interface_contracts_labels`, `interface_contracts_phases`
- `phases_labels`, `phases_steps`
- `steps_labels`, `steps_tasks`
- `tasks_labels`, `tasks_sub_tasks`
- `sub_tasks_labels`, `sub_tasks_commands`
- `commands_labels`
- `requirements_acceptance_criteria`

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
SELECT 'Goals:', COUNT(*) FROM goals
UNION ALL
SELECT 'Concepts:', COUNT(*) FROM concepts
UNION ALL
SELECT 'Tables:', COUNT(*) FROM information_schema.tables
WHERE table_schema='public' AND table_name LIKE '%';
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
- ✅ mcp_tools database chosen to avoid conflicts
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
- ✅ PostgreSQL Backend: COMPLETE (42 tables, association system)
- ✅ Models API Integration: COMPLETE (existing lib_package)
- ✅ Data Persistence: COMPLETE (cross-session)
- ✅ Container Management: COMPLETE (auto-restart)
- ✅ Association System: COMPLETE (28 association tables)
- ✅ Session Tracking: COMPLETE (audit trail)

**Ready for full development work with guaranteed data persistence and session continuity.**
