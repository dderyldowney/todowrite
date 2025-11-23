# 🚨 COMPREHENSIVE DEVELOPMENT MANDATE

**ABSOLUTE REQUIREMENTS - ZERO EXCEPTIONS**

## 🗄️ **DATABASE ARCHITECTURE (3 DATABASES)**

### **1. `todowrite` - Project Management**
- **Purpose**: 12-layer hierarchy (goals → commands)
- **Tables**: goals, concepts, contexts, constraints, requirements, acceptance_criteria, interface_contracts, phases, steps, tasks, subtasks, commands, labels + 30 associations
- **Connection**: `postgresql://mcp_user:mcp_secure_password_2024@localhost:5433/todowrite`
- **Data**: 4 goals, 16 concepts, 5 tasks
- **🚫 NEVER**: Store session/conversation data

### **2. `mcp_episodic_memory` - Conversations**
- **Purpose**: Conversation search and indexing (6,686+ conv)
- **Tables**: conversations, messages, exchanges, vec_exchanges, tool_calls, queue_operations, schema_migrations
- **Connection**: `postgresql://mcp_user:mcp_secure_password_2024@localhost:5433/mcp_episodic_memory`
- **🚫 NEVER**: Store ToDoWrite project data

### **3. `mcp_tools` - Legacy**
- **Purpose**: Original MCP tools compatibility
- **Tables**: 6 total (mostly system)
- **Status**: ⚠️ LEGACY - AVOID for new development
- **🚫 DO NOT USE** for new development

### **CRITICAL VERIFICATION:**
```bash
# Verify todowrite database
docker exec mcp-postgres psql -U mcp_user -d todowrite -c "SELECT COUNT(*) FROM goals;"

# Verify episodic memory database
docker exec mcp-postgres psql -U mcp_user -d mcp_episodic_memory -c "SELECT COUNT(*) FROM conversations;"

# Verify active goals exist (MANDATORY before work)
docker exec mcp-postgres psql -U mcp_user -d todowrite -c "SELECT COUNT(*) FROM goals WHERE status='active';"
```

## 🚨 **DATABASE SEPARATION MANDATE**
- **NEVER** mix data between databases
- **NEVER** use `mcp_tools` for new development
- **NEVER** assume table locations - check with `\dt`
- **IMMEDIATELY REJECT** any cross-database references

## 🚨 **NON-NEGOTIABLE TODOWRITE USAGE**

### **ABSOLUTE REQUIREMENTS:**
- **ALL development** MUST start with ToDoWrite planning
- **NO code implementation** without goal/concept/task breakdown
- **ZERO EXCEPTIONS** for "quick fixes", "urgent", "simple", "prototype", "learning"
- **ALL agents** MUST enforce this requirement

### **MANDATORY WORKFLOW:**
```python
from .claude.todowrite_database_manager import ToDoWriteDatabaseManager
manager = ToDoWriteDatabaseManager()

# STEP 1: ALWAYS START WITH GOAL
goal = manager.create_goal("Title", "Description")

# STEP 2: BREAK DOWN INTO CONCEPTS/TASKS
concept = manager.create_layer_item('concept', "Title", "Description")
task = manager.create_layer_item('task', "Title", "Description")

# STEP 3: ONLY THEN IMPLEMENT CODE
# ... implementation code here ...

# STEP 4: TRACK COMPLETION
manager.mark_item_complete(task.id)
```

### **FORBIDDEN PATTERNS:**
- ❌ Direct coding without ToDoWrite planning
- ❌ "Quick fixes" that bypass hierarchy
- ❌ Implementation without goal/concept breakdown
- ❌ Skipping task tracking for "simple" changes
- ❌ Any agent claiming ToDoWrite is "optional"

## 🔬 **MANDATORY TDD & RED-GREEN-REFACTOR**

### **ABSOLUTE TDD REQUIREMENTS:**
- **RED PHASE**: Write failing test FIRST - ALWAYS
- **GREEN PHASE**: Write minimal code to pass test - ALWAYS
- **REFACTOR PHASE**: Improve code while tests pass - ALWAYS
- **NO DIRECT IMPLEMENTATION** without failing test first
- **ZERO EXCEPTIONS** for any anti-TDD patterns

### **MANDATORY TDD WORKFLOW:**
```python
# STEP 1: RED - Write failing test FIRST
import pytest
def test_feature():
    result = function_to_test()
    assert result is not None  # FAILS initially

# STEP 2: GREEN - Minimal implementation
def function_to_test():
    return {"result": "success"}  # Minimal code to pass

# STEP 3: REFACTOR - Improve while tests pass
# ... refactoring with continuous test confirmation ...
```

### **TDD VERIFICATION:**
```bash
# BEFORE implementing ANY feature:
pytest tests/ -v  # Confirm tests exist and fail

# AFTER implementation:
pytest tests/ -v  # Confirm all tests pass

# NO DIRECT CODING ALLOWED WITHOUT FAILING TESTS FIRST
```

### **FORBIDDEN ANTI-PATTERNS:**
- ❌ Writing implementation code before tests
- ❌ "I'll write tests later" approach
- ❌ Skipping tests for "simple" code
- ❌ Direct coding without test failure confirmation
- ❌ Any agent claiming TDD is "optional"

## 🚨 **COMPREHENSIVE MANDATE CHECKLIST**

### **BEFORE ANY WORK - MANDATORY VERIFICATION:**
- [ ] **ToDoWrite planning** - Goals/concepts/tasks created
- [ ] **TDD Red phase** - Failing tests written FIRST
- [ ] **Database separation** - Verify correct database usage
- [ ] **Active goals exist** - Confirm with verification command
- [ ] **Tests exist and fail** - Confirm with pytest

### **ZERO BYPASS COMPREHENSIVE POLICY:**
- **ALL AGENTS** must enforce ALL requirements simultaneously
- **NO EXCEPTIONS** for any reason (urgent, simple, prototype, learning)
- **IMMEDIATE REJECTION** of any violation
- **MANDATORY VERIFICATION** before proceeding with work
- **COMPLETE COMPLIANCE** required for ALL development activities

---

**🔒 THIS MANDATE IS NON-NEGOTIABLE AND ABSOLUTE**
**🔒 VIOLATIONS WILL BE IMMEDIATELY REJECTED**
**🔒 ALL AGENTS MUST ENFORCE ALL REQUIREMENTS**
**🔒 NO BYPASSING ALLOWED FOR ANY REASON**