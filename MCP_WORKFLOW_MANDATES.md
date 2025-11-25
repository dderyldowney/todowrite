# MCP Workflow Mandates - Persistent Guidelines

## **🚨 CRITICAL MANDATES FOR ALL SESSIONS**

### **1. MCP-FIRST WORKFLOW (NON-NEGOTIABLE)**

**ALWAYS use MCP tools BEFORE built-in tools:**

- **File Operations**:
  - ❌ Read/Edit/Write → ✅ MCP read_file/edit_file
  - Check availability first, use built-in only if MCP unavailable

- **Version Control**:
  - ❌ bash git → ✅ MCP git tools
  - Check availability first, use built-in only if MCP unavailable

- **Code Changes**:
  - ❌ Manual editing → ✅ MCP python_refactoring
  - Check availability first, use built-in only if MCP unavailable

- **Database Operations**:
  - ❌ Direct SQL → ✅ MCP database tools
  - Check availability first, use built-in only if MCP unavailable

### **2. RESEARCH-FIRST APPROACH**

**NEVER assume capabilities without research:**

- **CLI Capabilities**: Research before assuming limitations
- **Tool Features**: Check available MCP tools before assuming missing
- **Documentation**: Read before assuming behavior
- **Google search**: Before saying "can't do X", research it first

### **3. MANDATE ENFORCEMENT**

**Any violation requires explicit justification:**

- **Built-in tool usage**: Must state why MCP tool unavailable
- **Assumptions**: Must state why research was impossible
- **Bypass**: Must justify with specific technical reason

### **4. COST OPTIMIZATION**

**Token cost minimization:**

- **MCP tools**: 0 tokens (preferred)
- **Built-in tools**: 0 tokens (when MCP unavailable)
- **API tokens**: Only for reasoning, never for execution

## **🔄 SESSION CONTINUITY**

This file is loaded in every session via startup_enforcement.py to maintain consistent workflow across all agents and sessions.

## **📋 CHECKLIST BEFORE ANY WORK:**

1. ☐ Check available MCP servers
2. ☐ Research capabilities of task
3. ☐ Identify appropriate MCP tools
4. ☐ Use MCP tools first
5. ☐ Document any tool bypasses
6. ☐ Save session learning

## **⚠️ CONSEQUENCES OF VIOLATION**

- **Increased costs**: Manual work uses billable tokens
- **Poor performance**: Rework and corrections needed
- **Inconsistent quality**: Variable results across agents
- **Knowledge loss**: Learning not preserved between sessions

---
**This document is loaded automatically in every session to enforce consistent MCP-first workflow.**
