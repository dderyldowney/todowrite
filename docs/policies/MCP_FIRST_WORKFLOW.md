# MCP-First Workflow Policy

## 🚨 MCP-FIRST MANDATE (NO EXCEPTIONS)

You MUST use MCP tools **before** any built-in or OpenAI/Anthropic tool capability.

### Active MCP Servers (81 tools total)

#### Current MCP Server Configuration
- **filesystem (11 tools)** - File operations
- **github-official (40 tools)** - GitHub integration
- **git (12 tools)** - Version control
- **SQLite (6 tools)** - Database operations
- **context7 (2 tools)** - AI assistance
- **docker** - Container management
- **hugging-face (9 tools)** - AI/ML integration

### 🚫 FORBIDDEN BUILT-IN TOOLS

**NEVER USE these built-in tools when MCP equivalents exist:**
- ❌ Built-in Read
- ❌ Built-in Write
- ❌ Built-in Edit
- ❌ Built-in Glob
- ❌ Direct Bash for filesystem
- ❌ Direct Git commands
- ❌ Non-MCP refactoring
- ❌ Assuming a tool is unavailable without checking MCP discovery first

### 🔴 REQUIRED ACTIONS

**MANDATORY workflow:**
1. **ALWAYS run MCP discovery** before any work
2. **ALWAYS use MCP filesystem, git, refactoring, database tools FIRST**
3. **NEVER bypass MCP** unless explicitly instructed by user in the same message

If a task cannot be completed with MCP → **STOP and ask**.

- `Read` → Use MCP `read_file`
- `Write` → Use MCP `edit_file`
- `Edit` → Use MCP `edit_file`
- `Glob` → Use MCP `list_directory`
- `Bash` (for file operations) → Use MCP filesystem tools
- Direct bash git commands → Use MCP git tools

### 🔴 MCP-FIRST WORKFLOW MANDATE

#### Required Actions
1. **ALWAYS** use MCP tools for file operations BEFORE using Read/Edit/Write
2. **ALWAYS** use MCP git tools BEFORE using bash git commands
3. **ALWAYS** use MCP python_refactoring for code changes BEFORE manual editing
4. **ALWAYS** use MCP database tools before direct SQL commands
5. **NEVER** use built-in Claude Code tools when MCP equivalents exist
6. **MANDATORY**: Research capabilities BEFORE assuming limitations
7. **VERIFICATION REQUIRED**: Confirm MCP servers are healthy before starting work
8. **VIOLATION**: Any bypass of MCP tools requires explicit justification in reasoning

### MCP Server Health & Discovery

#### Health Check Commands
```bash
# Verify all MCP servers are running and healthy
python .claude/mcp_server_health_check.py

# Discover available MCP services
python .claude/mcp_service_discovery.py

# Verify MCP capabilities
python .claude/mcp_capability_discovery.py
```

#### MCP Infrastructure Lifecycle

**🔴 EXPECTATION & REALITY:**
- **EXPECTATION**: MCP servers AND Docker MCP Gateway toolsets ARE already running
- **REALITY**: They will STAY RUNNING before, during, and after ALL sessions
- **NEVER stop/kill MCP servers or Docker MCP Gateway** - they serve ALL projects on the machine
- **NOT project-specific** - All MCP infrastructure are shared system resources
- **NO lifecycle management** - Scripts should NOT control any MCP infrastructure uptime

### Allowed Operations
- **✅ Verify server health** - Check if servers are running
- **✅ Restart individual servers** - Only if specific server is malfunctioning
- **✅ Restart AS NEEDED** - For troubleshooting or maintenance
- **✅ Discover available services** - Query capabilities and status

### Forbidden Operations
- **❌ Stop ALL MCP servers** - Never at session end or project cleanup
- **❌ Stop Docker MCP Gateway** - Gateway toolsets serve all projects
- **❌ Kill MCP processes** - All MCP infrastructure are system-wide resources
- **❌ Automatic shutdown** - No session-based lifecycle management
- **❌ Project-specific culling** - MCP infrastructure serves multiple projects

### Recovery Procedures (Only When Infrastructure Dies)

```bash
# ONLY use if MCP servers or Gateway are NOT running (unexpected failure):
docker mcp server ls  # Check Docker MCP Gateway status
bash .claude/start-mcp-servers.sh  # Recovery for MCP servers

# ONLY use if specific MCP server or Gateway is malfunctioning:
docker restart <specific-mcp-container>  # Individual server recovery
docker mcp gateway restart  # Docker MCP Gateway recovery
bash .claude/restart-mcp-servers.sh  # Bulk MCP server recovery

# Verify all MCP infrastructure is running (expected state):
python .claude/mcp_server_health_check.py
docker mcp server ls
```

### Normal Operation
- **EXPECT all MCP infrastructure running** - MCP servers AND Docker MCP Gateway
- **NO startup/shutdown scripts needed** - Should already be running
- **Health verification only** - Confirm infrastructure is running as expected
- **Leave everything running** - At session end, MCP infrastructure continues serving other projects

### MCP Tool Usage Patterns

#### File Operations
```python
# CORRECT - MCP-first approach
mcp__agentic_control_framework__read_file(path="src/models.py")
mcp__agentic_control_framework__write_file(path="src/models.py", content="...")

# FORBIDDEN - Built-in tools
# Read(path="src/models.py")  # ❌ FORBIDDEN
# Write(path="src/models.py", content="...")  # ❌ FORBIDDEN
```

#### Git Operations
```bash
# CORRECT - MCP git tools
mcp__github_official_create_pull_request(...)
mcp__git_commit(...)

# FORBIDDEN - Direct bash git
# bash git add .  # ❌ FORBIDDEN
# bash git commit -m "..."  # ❌ FORBIDDEN
```

#### Database Operations
```python
# CORRECT - MCP database tools
mcp__postgresql_mcp_execute_query(query="SELECT * FROM tasks")
mcp__sqlite_execute_query(...)

# FORBIDDEN - Direct SQL
# bash docker exec mcp-postgres psql ...  # ❌ FORBIDDEN
```

### MCP Workflow Examples

#### Discovery Before Implementation
```python
# 1. Discover available MCP tools first
mcp_tools = list_mcp_resources()

# 2. Check if desired capability exists
if 'filesystem' in mcp_tools:
    # 3. Use MCP tool
    result = mcp__filesystem_read_file("config.yaml")
else:
    # 4. Only then consider alternatives
    raise Exception("Required MCP capability not available")
```

#### Error Handling
```python
try:
    # Try MCP tool first
    result = mcp__git_repository_status()
except Exception as e:
    # Log the MCP failure
    logger.error(f"MCP git tool failed: {e}")

    # Only consider alternatives if user explicitly permits
    if user_explicitly_allowed_alternatives:
        # Use built-in tool as fallback
        result = git_status()
    else:
        # Ask for user guidance
        raise Exception("MCP tool unavailable - user guidance required")
```

### Verification & Compliance

#### Pre-Work Checklist
Before starting any work:

1. ✅ MCP server health check completed
2. ✅ Required MCP capabilities discovered
3. ✅ MCP tools confirmed available for task
4. ✅ No bypass of MCP tools without explicit justification
5. ✅ Infrastructure lifecycle policy understood

#### Compliance Validation
```bash
# Verify MCP-first compliance
python .claude/mcp_compliance_check.py

# Check for violations
python .claude/mcp_violation_scanner.py
```

### Philosophy

**All MCP infrastructure (servers, Docker MCP Gateway, and toolsets) are like system databases** - they are EXPECTED to be running continuously and remain running across all sessions and projects. Production database tables contain persistent business and system data that must be preserved. Development and testing databases/tables may be created and removed as needed during development work. Recovery scripts are ONLY for unexpected outages of any MCP component.
