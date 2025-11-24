# MCP TOOLS USAGE MANDATE

## 🚨 CRITICAL: ALWAYS USE MCP TOOLS - NEVER BUILT-IN TOOLS

### FILE OPERATIONS - MANDATORY
**✅ USE THESE MCP FILESYSTEM TOOLS:**
- `read_file` instead of Read tool
- `edit_file` instead of Edit tool
- `create_directory` instead of mkdir
- `list_directory` instead of ls/Glob
- `get_file_info` instead of file stat operations
- `directory_tree` for directory structure
- `move_file` for file moves/renames

**🚫 NEVER USE THESE BUILT-IN TOOLS:**
- `Read` - Use MCP `read_file` instead
- `Write` - Use MCP `edit_file` instead
- `Edit` - Use MCP `edit_file` instead
- `Glob` - Use MCP `list_directory` instead
- `Grep` - Use MCP tools or bash for searching

### VERSION CONTROL - MANDATORY
**✅ USE THESE MCP GIT TOOLS:**
- All Git operations through MCP git server tools
- GitHub integration through MCP github-official tools

**🚫 NEVER USE:**
- Direct bash git commands - use MCP git tools instead

### DATABASE OPERATIONS
**✅ USE MCP SQLite TOOLS:**
- All database queries through MCP SQLite server

### ENVIRONMENT CONFIGURATION
The MCP gateway provides these active servers:
- **filesystem (11 tools)** - File operations
- **github-official (40 tools)** - GitHub integration
- **git (12 tools)** - Version control
- **SQLite (6 tools)** - Database operations
- **context7 (2 tools)** - AI assistance
- **docker** - Container management
- **hugging-face (9 tools)** - AI/ML integration

### COMPLIANCE REQUIREMENTS
1. **ALWAYS** check available MCP tools before using built-in tools
2. **NEVER** use built-in file operation tools when MCP filesystem is available
3. **ALWAYS** use MCP git/github tools for version control operations
4. **NEVER** bypass MCP tools for convenience
5. **ALWAYS** prefer MCP tools over direct bash commands

### VERIFICATION
Before using any built-in tool, ask:
- "Is there an MCP tool that does this?"
- "Am I violating the MCP-first mandate?"

**FAILURE TO COMPLY = SESSION TERMINATION**

---
This configuration is persistent and loaded automatically in every session.
All agents are required to follow these rules without exception.
