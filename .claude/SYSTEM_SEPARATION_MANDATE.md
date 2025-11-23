# 🚨 SYSTEM SEPARATION MANDATE

**See [STREAMLINED_MANDATE.md](./STREAMLINED_MANDATE.md) for complete compliance requirements.**

## 🔴 **CRITICAL SEPARATION RULES**

### **TWO COMPLETELY SEPARATE SYSTEMS:**
1. **ToDoWrite Models API**: Project management (goals → commands)
   - Tables: `goals`, `concepts`, `contexts`, `constraints`, `requirements`, `acceptance_criteria`, `interface_contracts`, `phases`, `steps`, `tasks`, `subtasks`, `commands`, `labels` + associations
   - API: `todowrite.core.models`
   - 🚫 NEVER: Store session/conversation data

2. **Session Storage**: Memory continuity
   - Tables: `sessions`, `session_messages`, `session_exchanges`, `session_tools`, `queue_operations`, `schema_migrations`
   - 🚫 NEVER: Store ToDoWrite project data

### **ABSOLUTELY FORBIDDEN:**
- ❌ Adding `session_id` to ToDoWrite models
- ❌ Storing Goal/Concept/Task data in session storage
- ❌ Cross-system queries or relationships
- ❌ Mixing project hierarchy with conversation memory
- ❌ Any code that references both systems simultaneously

### **VERIFICATION (MANDATORY):**
```bash
# Verify clean separation (MUST return 0)
docker exec mcp-postgres psql -U mcp_user -d mcp_tools -c "
SELECT
    (SELECT COUNT(*) FROM information_schema.columns
     WHERE column_name = 'session_id' AND table_name IN (
         'goals', 'concepts', 'contexts', 'constraints', 'requirements',
         'acceptance_criteria', 'interface_contracts', 'phases', 'steps',
         'tasks', 'subtasks', 'commands', 'labels'
     )) as polluted_columns;
"

# Expected: 0 (MUST BE ZERO)
```

**🔒 ZERO EXCEPTIONS - IMMEDIATE REJECTION OF ALL VIOLATIONS**
**🔒 ALL REQUIREMENTS IN [STREAMLINED_MANDATE.md](./STREAMLINED_MANDATE.md) APPLY**