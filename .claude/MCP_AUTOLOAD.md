# Docker MCP Gateway Auto-Load Configuration

This document describes the comprehensive auto-loading setup for Docker MCP Gateway with 9 powerful MCP servers in the TodoWrite project.

## Configuration Summary

**Project:** TodoWrite (`/Users/dderyldowney/Documents/GitHub/dderyldowney/todowrite`)
**MCP Servers:** 9 servers covering development, documentation, and deployment
**Total Tools:** 91+ tools available

## What's Configured

### 1. Project-Level MCP Configuration
File: `~/.claude.json` (TodoWrite project section)

```json
"mcpServers": {
  "MCP_DOCKER": {
    "command": "source ~/.env && docker",
    "args": [
      "mcp",
      "gateway",
      "run",
      "--servers",
      "context7,docker,github-official,git,filesystem,postgres,SQLite,hugging-face,playwright"
    ]
  }
}
```

### 2. Auto-Start Script
File: `.claude/start-mcp.sh`

Executable script that starts the MCP Gateway:
```bash
#!/bin/bash
source ~/.env
docker mcp gateway run --servers context7,docker,github-official,git,filesystem,postgres,SQLite,hugging-face,playwright --log-calls
```

### 3. Session Startup Hook
File: `.claude/hooks/session_start_mcp.py`

Python hook that runs on session start to:
- Verify Context7 API key is loaded from `~/.env`
- Test Docker MCP Gateway connectivity
- Report tool availability

## Usage

### Manual Start
```bash
# Quick start with Context7 and Docker
.claude/start-mcp.sh

# Or run directly
source ~/.env && docker mcp gateway run --servers context7,docker
```

### Available Tools

**Context7 (2 tools) - 📚 Documentation:**
- `resolve-library-id` - Find libraries by name
- `get-library-docs` - Fetch up-to-date documentation for any library/framework

**Docker (1 tool) - 🐳 Container Management:**
- Docker CLI access for container management

**GitHub (40 tools) - 🐙 Code & Repository Management:**
- Repository operations, issues, PRs, releases, workflows, actions, codespaces
- Complete GitHub API access for collaborative development

**Git (12 tools) - 📂 Version Control:**
- Git operations, commits, branches, merging, history, remotes
- Low-level git functionality for precise version control

**Filesystem (Multiple tools) - 📁 File Operations:**
- File read/write, directory operations, file search, permissions
- Safe file system access with proper sandboxing

**PostgreSQL (Multiple tools) - 🐘 Database Management:**
- Database connections, queries, schema management, migrations
- Production-ready PostgreSQL database operations

**SQLite (6 tools) - 🗃️ Local Database:**
- Local database operations, queries, schema management
- Lightweight database for local data persistence

**Hugging Face (9 tools) - 🤗 AI/ML Models:**
- Model access, downloads, inference, dataset operations
- State-of-the-art AI/ML models and tools

**Playwright (21 tools) - 🎭 Web Automation:**
- Browser automation, testing, web scraping, screenshot capture
- Cross-browser web automation and testing

**Total: 91+ Development Tools**

## Environment Requirements

**Required in `~/.env`:**
```bash
CONTEXT7_API_KEY=ctx7sk-your-api-key-here
```

## Verification

### Test Configuration
```bash
# Test dry-run (should show 91+ tools)
source ~/.env && docker mcp gateway run --servers context7,docker,github-official,git,filesystem,postgres,SQLite,hugging-face,playwright --dry-run

# Run session startup hook
python .claude/hooks/session_start_mcp.py
```

### Expected Output
```
✅ Docker MCP Gateway is ready with full server suite
📚 Context7: 2 tools available
🐳 Docker: 1 tool available
🐙 GitHub: 40 tools available
📂 Git: 12 tools available
📁 Filesystem: Available
🐘 PostgreSQL: Available
🗃️ SQLite: 6 tools available
🤗 Hugging Face: 9 tools available
🎭 Playwright: 21 tools available
🔧 Total: 91+ tools ready
```

## Adding More MCP Servers

### Edit Project Configuration
Add servers to the `args` array in `~/.claude.json`:

```json
"args": [
  "mcp",
  "gateway",
  "run",
  "--servers",
  "context7,docker,github-official,git,filesystem,postgres,SQLite,hugging-face,playwright,slack,stripe"
]
```

### Popular Additional Servers
- `slack` - Slack integration and messaging
- `stripe` - Payment processing and financial services
- `aws-core-mcp-server` - AWS cloud services
- `filesystem` - Additional file system operations
- `notion` - Notion workspace integration
- `linear` - Issue tracking and project management
- `redis` - In-memory database operations

## Troubleshooting

### Context7 API Key Issues
```bash
# Check if API key is loaded
source ~/.env && echo $CONTEXT7_API_KEY

# Should start with "ctx7sk-"
```

### Docker MCP Gateway Issues
```bash
# Test Docker connectivity
docker version

# Test MCP gateway dry-run
docker mcp gateway run --servers context7,docker,github-official,git,filesystem,postgres,SQLite,hugging-face,playwright --dry-run
```

### Configuration Not Loading
1. Verify you're in the TodoWrite project directory
2. Check `~/.claude.json` has the correct `mcpServers` configuration
3. Ensure `.claude/start-mcp.sh` is executable

## Auto-Load Behavior

The MCP servers are configured to auto-load in two ways:

1. **Project Configuration:** Added to `~/.claude.json` for the TodoWrite project
2. **Session Hook:** Runs verification on session start to ensure everything is ready

This ensures all 91+ MCP tools are available whenever you start a Claude Code session in the TodoWrite project, providing instant access to a comprehensive development toolkit including documentation, container management, version control, database operations, AI/ML capabilities, and web automation.
