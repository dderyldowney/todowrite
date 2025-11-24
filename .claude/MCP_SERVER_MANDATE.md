# MCP SERVER USAGE MANDATE
## **NON-NEGOTIABLE REQUIREMENTS FOR ALL AGENTS**

**Last Updated: 2025-11-23**
**Status: IMMEDIATE ENFORCEMENT**

---

## 🚨 **MANDATE: ALL AGENTS MUST USE MCP SERVER SERVICES**

### **ABSOLUTE REQUIREMENTS:**

1. **CHECK FOR MATCHING TOOLS FIRST**
   - Before using ANY built-in tool, agents MUST check if an MCP server provides equivalent functionality
   - Search available MCP tools for matching capabilities
   - PREFER MCP server tools over built-in tools when available

2. **ZERO EXCEPTIONS POLICY**
   - NO AGENT may bypass MCP servers without explicit justification
   - NO "quick workarounds" that avoid MCP tools
   - NO parallel implementations when MCP tools exist

3. **MANDATORY TOOL DISCOVERY**
   - Every session MUST start with MCP server discovery
   - Every task MUST identify relevant MCP tools before proceeding
   - Every implementation decision MUST document MCP tool usage

---

## 📋 **IMPLEMENTATION REQUIREMENTS**

### **Pre-Task Checklist (MANDATORY):**
- [ ] Check MCP server health status
- [ ] List available MCP tools for current task
- [ ] Identify MCP alternatives to built-in tools
- [ ] Document why specific MCP tools are chosen
- [ ] Verify MCP tool availability before starting

### **During Task Execution:**
- [ ] Use MCP tools as primary choice
- [ ] Fall back to built-in tools ONLY when MCP tools unavailable
- [ ] Log all MCP tool usage with reasons
- [ ] Report any MCP tool failures immediately

### **Post-Task Validation:**
- [ ] Verify MCP tools were used where available
- [ ] Document any cases where built-in tools were used instead
- [ ] Provide justification for any MCP tool bypasses
- [ ] Report MCP tool performance/issues

---

## 🔍 **MCP TOOL MAPPING**

### **Core Development Tasks → MCP Tools:**

| Task | Built-in Tool | **PREFERRED MCP Tool** | MCP Server |
|------|---------------|------------------------|------------|
| File Operations | Read, Write, Edit | **filesystem_read, filesystem_write** | filesystem |
| Git Operations | Bash | **git_*** tools | git-server |
| GitHub Integration | Bash + gh | **github_*** tools | github-server |
| Database Operations | Bash | **postgres_query** | postgres |
| SQLite Operations | Bash | **sqlite_query** | sqlite-server |
| Code Analysis | Various | **python_refactor** | python-refactoring |
| Web Testing | None | **playwright_*** tools | playwright |
| Search Operations | Grep, Glob | **filesystem_search** | filesystem |

### **Decision Matrix:**
1. **If MCP tool exists:** USE MCP TOOL
2. **If multiple MCP tools exist:** Choose most specific/optimal
3. **If MCP tool is unavailable:** Document and use built-in fallback
4. **If no MCP equivalent:** Use built-in tool and document need

---

## 🛠️ **ENFORCEMENT MECHANISMS**

### **Session Start:**
```bash
# MANDATORY: Check MCP servers before any work
python .claude/mcp_server_health_check.py

# MANDATORY: Discover available tools
python .claude/mcp_service_discovery.py
```

### **Tool Usage Validation:**
```python
# AGENTS MUST: Check for MCP tools before using built-in
def use_appropriate_tool(task_type, operation):
    mcp_tools = get_available_mcp_tools()
    if task_type in mcp_tools:
        return use_mcp_tool(mcp_tools[task_type])
    else:
        log_mcp_unavailability(task_type)
        return use_builtin_tool(operation)
```

### **Compliance Checking:**
- Every task completion includes MCP tool usage audit
- Session summaries document MCP tool compliance rate
- Non-compliance triggers immediate corrective action

---

## ⚠️ **VIOLATIONS CONSEQUENCES**

### **For Agents:**
- **First Violation:** Immediate task restart with compliance check
- **Second Violation:** Session termination and restart
- **Pattern of Violations:** Agent capability review

### **For Development Work:**
- **Non-Compliant Code:** Immediate rollback and redo
- **Missing MCP Usage:** Task marked as incomplete
- **Bypass Without Justification:** Block further progress

---

## 📊 **MONITORING & REPORTING**

### **Metrics Tracked:**
- MCP tool usage rate by task type
- Built-in tool fallback frequency
- MCP server availability and performance
- Agent compliance rates

### **Reports Generated:**
- Daily MCP usage summary
- Weekly compliance audit
- Monthly optimization recommendations

---

## 🔄 **CONTINUOUS IMPROVEMENT**

### **Regular Updates:**
- Add new MCP server mappings as servers are added
- Update tool preference matrices based on performance
- Refine decision algorithms based on usage patterns

### **Feedback Loop:**
- Report MCP tool performance issues
- Suggest new MCP server integrations
- Identify gaps in MCP tool coverage

---

## 📖 **EXAMPLES OF PROPER USAGE**

### **✅ CORRECT: File Operations**
```python
# AGENT THINKING: "I need to read a file"
# 1. Check MCP tools first
mcp_tools = discover_mcp_tools()
if "filesystem" in mcp_tools and "read_file" in mcp_tools["filesystem"]:
    # 2. Use MCP tool
    result = mcp_tools["filesystem"]["read_file"](file_path)
else:
    # 3. Fallback with documentation
    log_mcp_unavailability("filesystem_read")
    result = Read(file_path)
```

### **✅ CORRECT: Git Operations**
```python
# AGENT THINKING: "I need to check git status"
# 1. Check MCP tools first
if "git-server" in mcp_servers and "git_status" in mcp_tools:
    # 2. Use MCP tool
    result = mcp_tools["git-server"]["git_status"]()
else:
    # 3. Fallback with documentation
    log_mcp_server_down("git-server")
    result = Bash("git status")
```

### **❌ INCORRECT: Bypassing MCP Tools**
```python
# WRONG: Direct tool usage without MCP check
result = Read(file_path)  # MISSING MCP tool discovery
```

---

## 🎯 **SUCCESS CRITERIA**

### **Compliance Goals:**
- **95%+** MCP tool usage rate where MCP tools exist
- **100%** MCP tool discovery before task execution
- **0%** unjustified MCP tool bypasses

### **Performance Goals:**
- Faster task completion through specialized MCP tools
- Better resource utilization through Docker-based services
- Improved reliability through professional MCP implementations

---

## 📝 **IMPLEMENTATION NOTES**

### **Agent Integration:**
- All agent frameworks must include MCP tool discovery
- Task planning must include MCP tool selection
- Progress tracking must monitor MCP usage compliance

### **Session Management:**
- Session start includes MCP health check
- Session context includes available MCP tools
- Session summary includes MCP usage statistics

---

**REMEMBER: MCP servers are not optional accessories - they are PRIMARY tools that provide superior functionality, reliability, and performance. Built-in tools are FALLBACKS, not first choices.**

**THIS MANDATE IS IMMEDIATELY EFFECTIVE AND ENFORCED FOR ALL AGENTS AND ALL TASKS.**
